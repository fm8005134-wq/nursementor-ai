"""
Nurse Mentor AI - SQLite backend layer (Sprint 6).

Schema simplified for nursing workflow:
    patients     - patient master records
    visits       - one row per patient arrival (auto-created)
    procedures   - procedures done during a visit
    tests        - tests ordered/performed during a visit
"""

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "clinic.db")


# ---------------------------------------------------------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def db_cursor(commit=False):
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        if commit:
            conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
def create_tables():
    with db_cursor(commit=True) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                age         INTEGER,
                gender      TEXT,
                phone       TEXT,
                address     TEXT,
                created_at  TEXT    NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id  INTEGER NOT NULL,
                visit_date  TEXT    NOT NULL,
                created_at  TEXT    NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
                    ON DELETE CASCADE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS procedures (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                visit_id     INTEGER NOT NULL,
                name         TEXT    NOT NULL,
                details      TEXT,
                performed_at TEXT    NOT NULL,
                FOREIGN KEY (visit_id) REFERENCES visits (id)
                    ON DELETE CASCADE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                visit_id     INTEGER NOT NULL,
                name         TEXT    NOT NULL,
                result       TEXT,
                ordered_at   TEXT    NOT NULL,
                FOREIGN KEY (visit_id) REFERENCES visits (id)
                    ON DELETE CASCADE
            );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_visits_patient ON visits (patient_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_visits_date ON visits (visit_date);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_procedures_visit ON procedures (visit_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tests_visit ON tests (visit_id);")


# ---------------------------------------------------------------------------
def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _today():
    return datetime.now().strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# PATIENTS
# ---------------------------------------------------------------------------
def add_patient(name, age=None, gender=None, phone=None, address=None):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO patients (name, age, gender, phone, address, created_at)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (name, age, gender, phone, address, _now()))
        return cur.lastrowid


def get_patient(patient_id):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM patients WHERE id = ?;", (patient_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def search_patients(query):
    like = "%{}%".format(query.strip())
    with db_cursor() as cur:
        cur.execute("""
            SELECT * FROM patients
            WHERE name LIKE ? OR phone LIKE ? OR address LIKE ?
            ORDER BY name COLLATE NOCASE ASC;
        """, (like, like, like))
        return [dict(r) for r in cur.fetchall()]


def list_patients(limit=500, offset=0):
    with db_cursor() as cur:
        cur.execute("""
            SELECT * FROM patients
            ORDER BY id DESC
            LIMIT ? OFFSET ?;
        """, (limit, offset))
        return [dict(r) for r in cur.fetchall()]


def update_patient(patient_id, **fields):
    allowed = {"name", "age", "gender", "phone", "address"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return False
    set_clause = ", ".join("{} = ?".format(k) for k in updates)
    values = list(updates.values()) + [patient_id]
    with db_cursor(commit=True) as cur:
        cur.execute("UPDATE patients SET {} WHERE id = ?;".format(set_clause), values)
        return cur.rowcount > 0


def delete_patient(patient_id):
    with db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM patients WHERE id = ?;", (patient_id,))
        return cur.rowcount > 0


# ---------------------------------------------------------------------------
# VISITS
# ---------------------------------------------------------------------------
def add_visit(patient_id, visit_date=None):
    visit_date = visit_date or _today()
    with db_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO visits (patient_id, visit_date, created_at)
            VALUES (?, ?, ?);
        """, (patient_id, visit_date, _now()))
        return cur.lastrowid


def get_or_create_today_visit(patient_id):
    """Return today's visit id for the patient; create it if missing."""
    today = _today()
    with db_cursor() as cur:
        cur.execute("""
            SELECT id FROM visits
            WHERE patient_id = ? AND visit_date = ?
            ORDER BY id DESC LIMIT 1;
        """, (patient_id, today))
        row = cur.fetchone()
        if row:
            return row["id"]
    return add_visit(patient_id, today)


def get_patient_visits(patient_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT * FROM visits
            WHERE patient_id = ?
            ORDER BY visit_date DESC, id DESC;
        """, (patient_id,))
        return [dict(r) for r in cur.fetchall()]


def get_visit_count(patient_id):
    with db_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM visits WHERE patient_id = ?;", (patient_id,))
        return cur.fetchone()[0]


def delete_visit(visit_id):
    with db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM visits WHERE id = ?;", (visit_id,))
        return cur.rowcount > 0


# ---------------------------------------------------------------------------
# PROCEDURES
# ---------------------------------------------------------------------------
def add_procedure(visit_id, name, details=None):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO procedures (visit_id, name, details, performed_at)
            VALUES (?, ?, ?, ?);
        """, (visit_id, name, details, _now()))
        return cur.lastrowid


def get_visit_procedures(visit_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT * FROM procedures
            WHERE visit_id = ?
            ORDER BY id ASC;
        """, (visit_id,))
        return [dict(r) for r in cur.fetchall()]


def delete_procedure(procedure_id):
    with db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM procedures WHERE id = ?;", (procedure_id,))
        return cur.rowcount > 0


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------
def add_test(visit_id, name, result=None):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO tests (visit_id, name, result, ordered_at)
            VALUES (?, ?, ?, ?);
        """, (visit_id, name, result, _now()))
        return cur.lastrowid


def get_visit_tests(visit_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT * FROM tests
            WHERE visit_id = ?
            ORDER BY id ASC;
        """, (visit_id,))
        return [dict(r) for r in cur.fetchall()]


def update_test_result(test_id, result):
    with db_cursor(commit=True) as cur:
        cur.execute("UPDATE tests SET result = ? WHERE id = ?;", (result, test_id))
        return cur.rowcount > 0


def delete_test(test_id):
    with db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM tests WHERE id = ?;", (test_id,))
        return cur.rowcount > 0


# ---------------------------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------------------------
def monthly_statistics(year=None, month=None):
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    prefix = "{:04d}-{:02d}".format(year, month)

    with db_cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) FROM patients
            WHERE substr(created_at, 1, 7) = ?;
        """, (prefix,))
        total_patients = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*) FROM visits
            WHERE substr(visit_date, 1, 7) = ?;
        """, (prefix,))
        total_visits = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*) FROM procedures p
            JOIN visits v ON v.id = p.visit_id
            WHERE substr(v.visit_date, 1, 7) = ?;
        """, (prefix,))
        total_procedures = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*) FROM tests t
            JOIN visits v ON v.id = t.visit_id
            WHERE substr(v.visit_date, 1, 7) = ?;
        """, (prefix,))
        total_tests = cur.fetchone()[0]

    return {
        "year": year,
        "month": month,
        "prefix": prefix,
        "total_patients": total_patients,
        "total_visits": total_visits,
        "total_procedures": total_procedures,
        "total_tests": total_tests,
    }


def patient_count():
    with db_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM patients;")
        return cur.fetchone()[0]


def visit_count():
    with db_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM visits;")
        return cur.fetchone()[0]


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("DB path:", DB_PATH)
    create_tables()
    print("Tables created.")
    print("Total patients:", patient_count())
    print("Total visits:", visit_count())
    print("Monthly stats:", monthly_statistics())