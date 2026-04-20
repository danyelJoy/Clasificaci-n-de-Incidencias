from __future__ import annotations

import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline


def load_data(path: Path) -> pd.DataFrame:
    print("Leyendo CSV...")
    df = pd.read_csv(path)
    print("Shape original:", df.shape)

    df = df[df["category_rule"] != "general_support"]
    df = df[df["text"].notna()]

    print("Shape después de limpieza:", df.shape)
    return df


def train_model(df: pd.DataFrame):
    X = df["text"]
    y = df["category_rule"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            stop_words="english",
            max_features=20000,
            ngram_range=(1, 2)
        )),
        ("model", LogisticRegression(max_iter=1000))
    ])

    print("\nEntrenando modelo...")
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)

    print("\n=== Classification Report ===\n")
    print(classification_report(y_test, preds))

    return pipeline


def save_model(model, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    print(f"\nModelo guardado en: {path}")


def main():
    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_PATH = BASE_DIR / "data/processed/tickets_labeled_v1.csv"
    MODEL_PATH = BASE_DIR / "models/ticket_classifier.joblib"

    print("Cargando dataset...")
    df = load_data(DATA_PATH)

    print("\nDistribución de clases:")
    print(df["category_rule"].value_counts())

    print("\nEntrenamiento del modelo...")
    model = train_model(df)

    save_model(model, MODEL_PATH)


if __name__ == "__main__":
    main()