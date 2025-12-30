import pandas as pd
from sqlalchemy import create_engine

# -------------------------------
# DB connection
# -------------------------------
engine = create_engine(
    "mysql+pymysql://root:1234@localhost:3306/neuro_db"
)

# -------------------------------
# Load staged data
# -------------------------------
df = pd.read_csv("data/staged/autism_staged.csv")

# -------------------------------
# Helper: find column safely
# -------------------------------
def find_col(possible_names):
    for col in df.columns:
        if col.lower() in possible_names:
            return col
    return None

age_col = find_col(["age"])
gender_col = find_col(["gender", "sex"])
target_col = find_col(["class/asd", "class", "asd", "asd_class"])

print("Detected columns:")
print("age ->", age_col)
print("gender ->", gender_col)
print("asd target ->", target_col)

if not target_col:
    raise ValueError("❌ ASD target column not found")

# -------------------------------
# dim_patient
# -------------------------------
dim_patient = pd.DataFrame({
    "patient_id": df["patient_id"],
    "age": df[age_col] if age_col else None,
    "gender": df[gender_col] if gender_col else None,
    "ethnicity": None,
    "country": None
}).drop_duplicates()

dim_patient.to_sql("dim_patient", engine, if_exists="append", index=False)

# -------------------------------
# dim_behavior (already recreated with behavior_id)
# -------------------------------
df["behavior_type"] = "Autism Screening"
dim_behavior = df[["behavior_type", "severity_level"]].drop_duplicates()
dim_behavior.to_sql("dim_behavior", engine, if_exists="append", index=False)

# -------------------------------
# dim_time (already recreated with time_id)
# -------------------------------
df["assessment_date"] = pd.to_datetime(df["assessment_date"], errors="coerce")

dim_time = df[["assessment_date"]].drop_duplicates()
dim_time["month"] = dim_time["assessment_date"].dt.month
dim_time["year"] = dim_time["assessment_date"].dt.year
dim_time.to_sql("dim_time", engine, if_exists="append", index=False)

# -------------------------------
# Reload dimension maps (EXPLICIT KEYS)
# -------------------------------
behavior_map = pd.read_sql(
    "SELECT behavior_id, behavior_type, severity_level FROM dim_behavior",
    engine
)

time_map = pd.read_sql(
    "SELECT time_id, assessment_date FROM dim_time",
    engine
)

# Ensure datetime alignment
time_map["assessment_date"] = pd.to_datetime(
    time_map["assessment_date"], errors="coerce"
)

# -------------------------------
# Merge to get surrogate keys
# -------------------------------
df = df.merge(
    behavior_map,
    on=["behavior_type", "severity_level"],
    how="left"
)

df = df.merge(
    time_map,
    on="assessment_date",
    how="left"
)

print("Columns after merge:", df.columns.tolist())

# -------------------------------
# HARD VALIDATION
# -------------------------------
if "behavior_id" not in df.columns or df["behavior_id"].isnull().any():
    raise ValueError("❌ behavior_id mapping failed")

if "time_id" not in df.columns or df["time_id"].isnull().any():
    raise ValueError("❌ time_id mapping failed")

# -------------------------------
# fact_sessions
# -------------------------------
fact = df[
    [
        "patient_id",
        "behavior_id",
        "time_id",
        "behavior_score",
        "behavior_score_pct",
        target_col
    ]
]

fact.columns = [
    "patient_id",
    "behavior_id",
    "time_id",
    "behavior_score",
    "behavior_score_pct",
    "asd_class"
]

fact.to_sql("fact_sessions", engine, if_exists="append", index=False)

print("✅ Phase 3 completed successfully")
