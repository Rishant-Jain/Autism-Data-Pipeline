🧠 Autism Data Pipeline (Autism Screening)

An end-to-end data engineering and analytics project designed to process, store, and analyze autism screening data with a focus on longitudinal patient tracking, severity analysis, and therapy effectiveness.

This project aligns with real-world healthcare analytics use cases and serves as a strong backend analytics layer for neurodevelopmental support systems like Adhirath.

🚀 Project Overview

Clinicians and researchers often struggle to extract actionable insights from scattered mental health and autism screening data.
This project solves that problem by building a structured data pipeline and warehouse that enables:

Session-wise patient progress tracking

Severity-based cohort analysis

Therapy effectiveness evaluation

Data-driven personalized intervention insights

🛠️ Tech Stack

Python – ETL (Extract, Transform, Load)

MySQL – Data Warehouse (Star Schema)

SQL – Analytics & insights

Power BI – Interactive dashboard & visualization

Pandas / SQLAlchemy – Data processing & DB integration

Git & GitHub – Version control
Data Pipeline Phases
🔹 Phase 1 — Extract

Ingests raw autism screening data from publicly available datasets

Handles schema inconsistencies and missing values

🔹 Phase 2 — Transform

Normalizes screening responses (A1–A10)

Computes behavioral scores and severity levels

Cleans demographic attributes

Generates patient IDs

Adds session-level tracking for longitudinal analysis

🔹 Phase 3 — Load

Loads data into a MySQL star schema

Fact table: fact_sessions

Dimension tables:

dim_patient

dim_behavior

dim_time

Implements surrogate keys and referential integrity

🔹 Phase 4 — Analytics & Insights

Tracks improvement across sessions

Identifies high-risk patients

Evaluates therapy effectiveness

Enables age-based and severity-based analysis

⭐ Star Schema Design

Fact Table

fact_sessions

patient_id

behavior_id

time_id

session_number

session_type

behavior_score

behavior_score_pct

asd_class

Dimension Tables

dim_patient (age, gender)

dim_behavior (severity_level)

dim_time (date, month, year)
📊 Key Analytics Questions Answered

Which patients are improving the fastest?

Which severity group benefits most from therapy?

When is intervention not working?

How does age impact therapy response?

Which patients need personalized intervention?

All insights are derived using pure SQL analytics on the data warehouse and visualized using Power BI.

📈 Dashboard (Power BI)

The Power BI dashboard provides:

KPI overview (patients, sessions, severity)

Severity distribution

Session-wise progress tracking

Therapy effectiveness by severity

Patient-level drilldowns

📌 Dashboard screenshots can be found in the /dashboard folder.

🧠 Real-World Impact

This project demonstrates how data engineering and analytics can support:

Clinical decision-making

Early risk identification

Personalized therapy planning

Scalable healthcare analytics systems

It can be directly extended to support ML-based recommendation engines for neurodevelopmental interventions.

▶️ How to Run the Project
# Run ETL pipeline
python etl/extract.py
python etl/transform.py
python etl/load.py


Ensure MySQL is running and the database neuro_db exists.

📌 Future Enhancements

Incremental / scheduled ETL

Real-time data ingestion

ML-based intervention recommendation

Web-based dashboard integration

Support for multiple neurodevelopmental disorders (ADHD, ID)

👤 Author

Rishant Jain
Computer Science & Engineering
Focused on Data Engineering, Analytics, and Healthcare AI
