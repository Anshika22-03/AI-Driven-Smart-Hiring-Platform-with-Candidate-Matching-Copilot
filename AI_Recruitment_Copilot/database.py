import sqlite3
from datetime import datetime

DB_NAME = "recruitment.db"


# =========================
# CREATE DATABASE
# =========================

def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        resume_file TEXT,

        resume_text TEXT,

        status TEXT DEFAULT 'Pending',

        upload_date TEXT
    )
    """)

    conn.commit()
    conn.close()


# =========================
# ADD CANDIDATE
# =========================

def add_candidate(name, resume_file, resume_text):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates
    (name,resume_file,resume_text,status,upload_date)

    VALUES(?,?,?,?,?)
    """,(

        name,
        resume_file,
        resume_text,
        "Pending",
        datetime.now().strftime("%d-%m-%Y %H:%M")

    ))

    conn.commit()
    conn.close()


# =========================
# GET ALL CANDIDATES
# =========================

def get_all_candidates():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM candidates
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================
# GET CANDIDATE
# =========================

def get_candidate(candidate_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM candidates
    WHERE id=?
    """,(candidate_id,))

    row = cursor.fetchone()

    conn.close()

    return row


# =========================
# UPDATE STATUS
# =========================

def update_status(candidate_id,status):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE candidates

    SET status=?

    WHERE id=?
    """,(status,candidate_id))

    conn.commit()
    conn.close()


# =========================
# DELETE CANDIDATE
# =========================

def delete_candidate(candidate_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM candidates

    WHERE id=?
    """,(candidate_id,))

    conn.commit()
    conn.close()


# =========================
# DASHBOARD COUNTS
# =========================

def get_dashboard_stats():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM candidates")
    applications = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)

    FROM candidates

    WHERE status='Pending'
    """)
    pending = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)

    FROM candidates

    WHERE status='Shortlisted'
    """)
    shortlisted = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)

    FROM candidates

    WHERE status='Rejected'
    """)
    rejected = cursor.fetchone()[0]

    conn.close()

    return applications,pending,shortlisted,rejected