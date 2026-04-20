import pandas as pd
import numpy as np
import re

CATEGORY_PATTERNS = {
    "service_outage": [
    # Señales fuertes
        (r"\boutage\b", 5),
        (r"server\s+down", 6),
        (r"\bunavailable\b", 4),
        (r"not\s+responding", 3),
        (r"\bmaintenance\b", 2),

        # "down" pero solo en contextos típicos de caída de servicio
        (r"\bis\s+down\b", 5),
        (r"\bdown\s+for\b", 4),
        (r"\bdown\s+since\b", 4),
        (r"\bservice\s+is\s+down\b", 6),
        (r"\bsite\s+is\s+down\b", 6),
        (r"\bwebsite\s+is\s+down\b", 6),
        (r"\bapp\s+is\s+down\b", 5),
        (r"\bunable\b", 2),
        (r"\bcannot\b", 2),
        (r"\bcan't\b", 2),
        (r"doesn'?t\s+work", 3),
        (r"won'?t\s+work", 3),
        (r"\bhelp\b", 1),
        ],
    "account_access": [
        (r"log\s*in", 3),
        (r"\blogin\b", 3),
        (r"sign\s*in", 3),
        (r"\bpassword\b", 3),
        (r"\breset\b", 2),
        (r"\blocked\b", 3),
        (r"\bverify\b", 2),
        (r"verification", 2),
        (r"\b2fa\b", 3),
        (r"\baccess\b", 2),
        (r"\baccount\b", 1),  # peso bajo porque aparece en muchos contextos
    ],
    "billing_payment": [
        (r"\brefund\b", 4),
        (r"\binvoice\b", 3),
        (r"\bbilling\b", 3),
        (r"\bbill\b", 2),
        (r"\bcharge\b", 3),
        (r"\bcharged\b", 4),
        (r"\bpayment\b", 3),
        (r"\bpay\b", 2),
        (r"\bcard\b", 2),
        (r"\bdebit\b", 2),
        (r"\bcredit\b", 2),
        (r"\bfee\b", 2),
        (r"\bsubscription\b", 2),
    ],
    "delivery_shipping": [
        (r"\btracking\b", 4),
        (r"\bdelivery\b", 3),
        (r"\bshipping\b", 3),
        (r"\bshipped\b", 3),
        (r"\border\b", 2),
        (r"\barrived\b", 2),
        (r"\blate\b", 2),
        (r"\bdelay\b", 2),
        (r"\bcourier\b", 2),
        (r"\bpackage\b", 2),
    ],
    "technical_issue": [
        (r"\berror\b", 3),
        (r"\bbug\b", 4),
        (r"\bissue\b", 2),
        (r"\bproblem\b", 2),
        (r"not\s+working", 3),
        (r"\bcrash\b", 4),
        (r"\bapp\b", 2),
        (r"\bwebsite\b", 2),
        (r"\bupdate\b", 1),
        (r"\bfix\b", 2),
        (r"\bbroken\b", 3),
        (r"not\s+loading", 3),
        (r"won't\s+load", 3),
        (r"\bunable\b", 2),
        (r"\bcannot\b", 2),
        (r"\bcan't\b", 2),
        (r"doesn'?t\s+work", 3),
        (r"won'?t\s+work", 3),
        (r"\bhelp\b", 1),
    ],
}

MIN_SCORE_THRESHOLD = 2

TIE_BREAK_PRIORITY =[ 
    "service_outage",
    "account_access",
    "billing_payment",
    "delivery_shipping",
    "technical_issue",
]



def normalize_series(s: pd.Series) -> pd.Series:
    s = s.astype(str).str.lower().str.strip()
    s = s.str.replace(r"\s+", " ", regex=True)
    return s


def label_dataframe_vectorized(df: pd.DataFrame, text_col: str, category_patterns: dict) -> pd.DataFrame:
    out = df.copy()
    text = normalize_series(out[text_col])

    #Contrucción de matriz de score por categoría 
    score_df = pd.DataFrame(index=out.index)

    for cat, patterns in category_patterns.items():
        cat_score = pd.Series(0, index=out.index, dtype="int32")

        for pat, weigth in patterns:
            mask = text.str.contains(pat, regex=True, na=False)
            cat_score += mask.astype("int32") * weigth
        
        score_df[cat] = cat_score

    
                # 1) mejor score por fila
    best_score = score_df.max(axis=1)

        # 1) por defecto todos son general_support
    best_cat = pd.Series("general_support", index=score_df.index)

    # 2) solo donde hay evidencia suficiente se asigna la mejor categoría
    valid_mask = best_score >= MIN_SCORE_THRESHOLD
    best_cat.loc[valid_mask] = score_df.idxmax(axis=1).loc[valid_mask]

    # 3) endurecer outage (opcional)
    best_cat = best_cat.mask((best_cat == "service_outage") & (best_score < 4), "general_support")

    ties = (score_df.eq(best_score, axis=0)).sum(axis=1) > 1
    ties = ties & valid_mask

    if ties.any():
        tie_mask_df = score_df.eq(best_score, axis=0)
        
        def resolve_one_row(row_bool):
            for cat in TIE_BREAK_PRIORITY:
                if cat in row_bool.index and row_bool[cat]:
                    return cat
                
            return row_bool.index[row_bool.values][0]
        best_cat.loc[ties] = tie_mask_df.loc[ties].apply(resolve_one_row, axis=1)

    out["category_rule"] = best_cat
    out["rule_score"] = best_score.astype(int)

    print("Chequeo (debe ser 0): outage con score 0 =",
          ((out["category_rule"] == "service_outage") & (out["rule_score"] == 0)).sum())
    
    print("\nDistribución de categoría:s")
    print(out["category_rule"].value_counts())

    print("\nMuestra: outage con score bajo(<=5)")
    sample = out[(out["category_rule"] == "service_outage") & (out["rule_score"] <=5)].sample(10, random_state=1)
    print(sample[["rule_score", "text"]].to_string(index=False))

    return out





if __name__ == "__main__":
    in_path = "data/processed/tickets_inbound_clean.csv"
    out_path = "data/processed/tickets_labeled_v1.csv"

    df = pd.read_csv(in_path)

    df_labeled = label_dataframe_vectorized(
        df,
        text_col="text",
        category_patterns=CATEGORY_PATTERNS
    )

    df_labeled.to_csv(out_path, index=False)

    print("Saved:", out_path)
    print(df_labeled["category_rule"].value_counts())

