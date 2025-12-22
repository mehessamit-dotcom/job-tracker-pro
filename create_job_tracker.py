import sqlite3
import pandas as pd
from datetime import datetime

# Connect to (or create) the database
db_path = "job_tracker.db"
conn = sqlite3.connect(db_path)

# Create tables
conn.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_applied DATE NOT NULL,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    country TEXT NOT NULL,
    source TEXT NOT NULL,
    status TEXT NOT NULL,
    salary REAL,
    tech_stack TEXT,
    notes TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    date DATE NOT NULL,
    interaction_type TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (application_id) REFERENCES applications (id)
)
""")

# Insert sample data (30+ realistic applications for analysis)
sample_applications = [
    ("2025-11-01", "Google", "Junior Data Analyst", "Germany", "LinkedIn", "rejected", 45000, "Python, SQL, Pandas", "No response after 2 weeks"),
    ("2025-11-02", "Siemens", "Data Engineer", "Germany", "Company Website", "interview", 52000, "Python, SQL, AWS", "Technical interview scheduled"),
    ("2025-11-03", "Amazon", "Business Analyst", "USA", "Indeed", "applied", None, "Excel, SQL, Tableau", ""),
    ("2025-11-05", "Microsoft", "Data Analyst", "Germany", "LinkedIn", "offer", 48000, "Python, PowerBI", "Waiting for final offer details"),
    ("2025-11-07", "BMW", "Data Scientist", "Germany", "Xing", "interview", 55000, "Python, ML, TensorFlow", "Passed HR screening"),
    ("2025-11-10", "SAP", "BI Analyst", "Germany", "Company Website", "rejected", 42000, "SQL, PowerBI", "No technical fit"),
    ("2025-11-12", "Zalando", "Data Analyst", "Germany", "LinkedIn", "applied", None, "Python, SQL", ""),
    ("2025-11-15", "Deutsche Bank", "Risk Analyst", "Germany", "Indeed", "interview", 46000, "Python, Excel", "Phone screening done"),
    ("2025-11-18", "Airbnb", "Data Analyst", "USA", "LinkedIn", "rejected", None, "SQL, R", "Too junior"),
    ("2025-11-20", "Tesla", "Data Engineer", "Germany", "Company Website", "applied", None, "Python, AWS, Docker", ""),
    ("2025-11-22", "Adidas", "Business Intelligence Analyst", "Germany", "Xing", "interview", 44000, "SQL, Tableau", "Test task received"),
    ("2025-11-25", "N26", "Data Analyst", "Germany", "LinkedIn", "applied", None, "Python, SQL", ""),
    ("2025-11-27", "HelloFresh", "Pricing Analyst", "Germany", "Indeed", "rejected", None, "Excel, SQL", "No Python experience"),
    ("2025-11-28", "Delivery Hero", "Data Analyst", "Germany", "Company Website", "interview", 43000, "Python, SQL", "HR interview scheduled"),
    ("2025-11-30", "Flixbus", "Revenue Analyst", "Germany", "LinkedIn", "applied", None, "SQL, Excel", ""),
]

# Insert sample applications
conn.executemany("""
INSERT INTO applications (date_applied, company, role, country, source, status, salary, tech_stack, notes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", sample_applications)

# Insert sample interactions
sample_interactions = [
    (1, "2025-11-10", "email", "Automated rejection email"),
    (2, "2025-11-12", "phone interview", "30min screening call"),
    (2, "2025-11-20", "technical test", "SQL test assigned"),
    (4, "2025-11-25", "email", "Verbal offer received"),
    (5, "2025-11-15", "phone interview", "HR screening passed"),
    (8, "2025-11-28", "phone interview", "Technical discussion"),
    (11, "2025-11-28", "technical test", "Python test received"),
]

conn.executemany("""
INSERT INTO interactions (application_id, date, interaction_type, notes)
VALUES (?, ?, ?, ?)
""", sample_interactions)

conn.commit()
conn.close()

print(f"✅ Database created: {db_path}")
print("📊 Sample data loaded (15 applications + 7 interactions)")
print("Ready for analysis!")
