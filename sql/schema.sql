USE neuro_db;

CREATE TABLE dim_patient (
    patient_id VARCHAR(10) PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    ethnicity VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE dim_behavior (
    behavior_id INT AUTO_INCREMENT PRIMARY KEY,
    behavior_type VARCHAR(50),
    severity_level VARCHAR(10)
);

CREATE TABLE dim_time (
    time_id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_date DATE,
    month INT,
    year INT
);

CREATE TABLE fact_sessions (
    session_fact_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(10),
    behavior_id INT,
    time_id INT,
    behavior_score INT,
    behavior_score_pct FLOAT,
    asd_class VARCHAR(10),
    FOREIGN KEY (patient_id) REFERENCES dim_patient(patient_id),
    FOREIGN KEY (behavior_id) REFERENCES dim_behavior(behavior_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);
