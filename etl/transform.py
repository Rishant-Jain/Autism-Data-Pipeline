import pandas as pd
import numpy as np
import os
from datetime import date

RAW_PATH = "data/raw/Autism_Screening_Data_Combined.csv"
STAGED_PATH = "data/staged/autism_staged.csv"

def transform_data():
    df = pd.read_csv(RAW_PATH)

    # -----------------------------
    # Detect screening columns (A1–A10)
    # -----------------------------
    score_cols = [
        col for col in df.columns
        if col.startswith("A") and col[1:].isdigit()
    ]

    if len(score_cols) == 0:
        raise ValueError("❌ No screening columns (A1–A10) found")

    print("✅ Detected screening columns:", score_cols)

    # -----------------------------
    # Normalize screening answers
    # -----------------------------
    for col in score_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .map({"Yes": 1, "No": 0, "1": 1, "0": 0})
        )

    # -----------------------------
    # Behavioral score
    # -----------------------------
    df["behavior_score"] = df[score_cols].sum(axis=1)
    df["behavior_score_pct"] = (df["behavior_score"] / len(score_cols)) * 100

    # -----------------------------
    # Severity level
    # -----------------------------
    def severity(pct):
        if pct < 30:
            return "Low"
        elif pct < 60:
            return "Medium"
        else:
            return "High"

    df["severity_level"] = df["behavior_score_pct"].apply(severity)

    # -----------------------------
    # Clean age
    # -----------------------------
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df["age"] = df["age"].fillna(df["age"].median())

    # -----------------------------
    # Normalize gender
    # -----------------------------
    if "gender" in df.columns:
        df["gender"] = (
            df["gender"]
            .astype(str)
            .str.lower()
            .replace({"m": "male", "f": "female"})
        )

    # -----------------------------
    # Patient & assessment info
    # -----------------------------
    df["patient_id"] = ["P" + str(i + 1).zfill(5) for i in range(len(df))]
    df["assessment_date"] = date.today()

    # =====================================================
    # 🔥 PHASE 4 — SESSION TRACKING (NEW)
    # =====================================================
    df["session_number"] = df.groupby("patient_id").cumcount() + 1

    df["session_type"] = df["session_number"].apply(
        lambda x: "Screening" if x == 1 else "Follow-up"
    )
    # =====================================================

    # -----------------------------
    # Save staged data
    # -----------------------------
    os.makedirs("data/staged", exist_ok=True)
    df.to_csv(STAGED_PATH, index=False)

    print("\n✅ Phase 2 + Phase 4 session tracking completed")
    print("📁 Staged file:", STAGED_PATH)
    print("📊 Rows:", df.shape[0])
    print("📊 Columns:", df.shape[1])

if __name__ == "__main__":
    transform_data()
