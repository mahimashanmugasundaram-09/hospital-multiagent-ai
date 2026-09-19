"""
seed_data.py
Populates the database with simulated hospital data.
Idempotent: running this multiple times will NOT create duplicate records.
"""

import random
from datetime import datetime, timedelta
from database.database import get_connection

random.seed(42)

AGENT_NAMES = [
    "Patient Admission Agent",
    "Emergency Response Agent",
    "Medical Diagnosis Support Agent",
    "Treatment Planning Agent",
    "Pharmacy Agent",
    "Surgery Scheduling Agent",
    "Nursing Coordination Agent",
    "Laboratory Testing Agent",
    "Medical Imaging Agent",
    "Patient Flow Agent",
    "Blood Inventory Agent",
    "Organ Inventory & Matching Agent",
    "Testing & Screening Agent",
    "Emergency Allocation Agent",
    "Compliance & Data Security Agent",
    "Chief Decision Agent",
]

DEPARTMENTS = ["Cardiology", "Orthopedics", "Neurology", "General Medicine",
               "Pediatrics", "Emergency", "Oncology", "Surgery"]
PRIORITIES = ["Critical", "High", "Medium", "Low"]
FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Sam",
               "Jamie", "Avery", "Quinn", "Reese", "Rowan", "Dakota", "Skyler"]
LAST_NAMES = ["Sim", "Doe", "Patel", "Kim", "Garcia", "Nguyen", "Smith",
              "Brown", "Lee", "Silva", "Khan", "Ivanov"]


def _now_str(offset_minutes=0):
    return (datetime.now() - timedelta(minutes=offset_minutes)).strftime("%Y-%m-%d %H:%M:%S")


def _random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def _table_empty(conn, table_name):
    count = conn.execute(f"SELECT COUNT(*) as c FROM {table_name}").fetchone()["c"]
    return count == 0


def seed_all():
    """Insert seed data only where tables are currently empty."""
    conn = get_connection()

    if _table_empty(conn, "patients"):
        stages = ["Registration", "Triage", "In Treatment", "Observation", "Discharge Pending"]
        for i in range(1, 41):
            pid = f"PT-{1000 + i}"
            conn.execute(
                """INSERT INTO patients
                   (patient_id, name, age, gender, department, priority,
                    admission_status, assigned_bed, current_stage, admission_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    pid,
                    _random_name(),
                    random.randint(1, 95),
                    random.choice(["Male", "Female", "Other"]),
                    random.choice(DEPARTMENTS),
                    random.choice(PRIORITIES),
                    random.choice(["Admitted", "Under Observation", "Discharged", "Waiting"]),
                    f"{random.choice(['A','B','C','D'])}-{random.randint(100,499)}",
                    random.choice(stages),
                    _now_str(random.randint(0, 4000)),
                ),
            )

    if _table_empty(conn, "beds"):
        wards = [("General Ward", 60), ("ICU", 20), ("Emergency Ward", 25),
                 ("Pediatric Ward", 15), ("Surgical Recovery", 18)]
        for ward, total in wards:
            occupied = random.randint(int(total * 0.4), int(total * 0.9))
            conn.execute(
                "INSERT INTO beds (ward, total_beds, occupied_beds) VALUES (?, ?, ?)",
                (ward, total, occupied),
            )

    if _table_empty(conn, "emergency_cases"):
        resources = ["Ventilator", "ICU Bed", "Trauma Team", "Blood Transfusion",
                     "CT Scanner", "Cardiac Monitor", "Surgical Team"]
        for _ in range(12):
            conn.execute(
                """INSERT INTO emergency_cases
                   (patient_name, priority, department, required_resources,
                    waiting_time_min, assigned_agent, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    _random_name(),
                    random.choice(PRIORITIES),
                    random.choice(DEPARTMENTS),
                    random.choice(resources),
                    random.randint(2, 90),
                    "Emergency Response Agent",
                    random.choice(["Waiting", "In Progress", "Resolved"]),
                ),
            )

    if _table_empty(conn, "lab_tests"):
        tests = ["CBC", "Blood Glucose", "Liver Function", "Kidney Function",
                 "COVID-19 PCR", "Lipid Profile", "Thyroid Panel", "Urinalysis"]
        for _ in range(20):
            conn.execute(
                """INSERT INTO lab_tests
                   (patient_id, patient_name, test_name, priority, status, requested_time)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    f"PT-{1000 + random.randint(1, 40)}",
                    _random_name(),
                    random.choice(tests),
                    random.choice(PRIORITIES),
                    random.choice(["Pending", "In Progress", "Completed"]),
                    _now_str(random.randint(0, 600)),
                ),
            )

    if _table_empty(conn, "imaging_scans"):
        scans = ["CT Scan", "MRI", "X-Ray", "Ultrasound"]
        for _ in range(16):
            conn.execute(
                """INSERT INTO imaging_scans
                   (patient_id, patient_name, scan_type, priority, status, scheduled_time)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    f"PT-{1000 + random.randint(1, 40)}",
                    _random_name(),
                    random.choice(scans),
                    random.choice(PRIORITIES),
                    random.choice(["Pending", "Scheduled", "Completed"]),
                    _now_str(random.randint(0, 800)),
                ),
            )

    if _table_empty(conn, "surgeries"):
        surgery_types = ["Appendectomy", "Knee Replacement", "Cardiac Bypass",
                          "Cataract Surgery", "Hernia Repair", "Spinal Fusion"]
        surgeons = ["Dr. Reeve", "Dr. Sato", "Dr. Alvarez", "Dr. Okafor", "Dr. Bianchi"]
        for i in range(8):
            conn.execute(
                """INSERT INTO surgeries
                   (patient_name, surgery_name, operating_room, surgeon,
                    priority, scheduled_time, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    _random_name(),
                    random.choice(surgery_types),
                    f"OR-{(i % 4) + 1}",
                    random.choice(surgeons),
                    random.choice(PRIORITIES),
                    _now_str(-random.randint(0, 1000)),
                    random.choice(["Scheduled", "In Progress", "Completed"]),
                ),
            )

    if _table_empty(conn, "medicines"):
        meds = [
            ("Paracetamol", "Analgesic", 400, 100),
            ("Amoxicillin", "Antibiotic", 60, 80),
            ("Insulin", "Hormone", 45, 50),
            ("Atorvastatin", "Cardiac", 220, 60),
            ("Ibuprofen", "Analgesic", 300, 100),
            ("Salbutamol Inhaler", "Respiratory", 25, 40),
            ("Morphine", "Analgesic (Controlled)", 30, 35),
            ("Metformin", "Diabetes", 180, 70),
            ("Ceftriaxone", "Antibiotic", 15, 30),
            ("Normal Saline IV", "Fluid", 500, 150),
        ]
        for name, cat, stock, threshold in meds:
            status = "Low Stock" if stock < threshold else "In Stock"
            conn.execute(
                """INSERT INTO medicines (name, category, stock_level, reorder_threshold, status)
                   VALUES (?, ?, ?, ?, ?)""",
                (name, cat, stock, threshold, status),
            )

    if _table_empty(conn, "nursing_tasks"):
        nurses = ["Nurse Alvarez", "Nurse Chen", "Nurse Okoye", "Nurse Fischer", "Nurse Rossi"]
        tasks = ["Vitals Check", "Medication Round", "Wound Dressing",
                 "Patient Mobility Assistance", "IV Line Monitoring", "Discharge Prep"]
        for _ in range(18):
            conn.execute(
                """INSERT INTO nursing_tasks (nurse_name, task, patient_name, status, shift)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    random.choice(nurses),
                    random.choice(tasks),
                    _random_name(),
                    random.choice(["Pending", "In Progress", "Completed"]),
                    random.choice(["Morning", "Evening", "Night"]),
                ),
            )

    if _table_empty(conn, "blood_inventory"):
        types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        for bt in types:
            units = random.randint(3, 60)
            status = "Critical" if units < 10 else ("Low" if units < 20 else "Adequate")
            conn.execute(
                "INSERT INTO blood_inventory (blood_type, units_available, status) VALUES (?, ?, ?)",
                (bt, units, status),
            )

    if _table_empty(conn, "organ_inventory"):
        organs = ["Kidney", "Liver", "Heart", "Cornea", "Lung"]
        for organ in organs:
            conn.execute(
                """INSERT INTO organ_inventory (organ_type, status, match_status, location)
                   VALUES (?, ?, ?, ?)""",
                (
                    organ,
                    random.choice(["Available", "Reserved", "In Transit"]),
                    random.choice(["Match Found", "Searching", "Pending Review"]),
                    f"Storage Unit {random.randint(1,3)}",
                ),
            )

    if _table_empty(conn, "screenings"):
        screen_types = ["Infectious Disease Panel", "Pre-Surgical Screening",
                         "Cancer Marker Screening", "Cardiac Risk Screening"]
        for _ in range(10):
            conn.execute(
                """INSERT INTO screenings (patient_name, screening_type, status, result)
                   VALUES (?, ?, ?, ?)""",
                (
                    _random_name(),
                    random.choice(screen_types),
                    random.choice(["Pending", "Completed"]),
                    random.choice(["Normal", "Requires Review", "Pending"]),
                ),
            )

    if _table_empty(conn, "agent_status"):
        tasks_map = {
            "Patient Admission Agent": "Processing new admission requests",
            "Emergency Response Agent": "Triaging incoming emergency cases",
            "Medical Diagnosis Support Agent": "Cross-referencing symptom patterns",
            "Treatment Planning Agent": "Drafting treatment pathways",
            "Pharmacy Agent": "Monitoring medicine stock levels",
            "Surgery Scheduling Agent": "Allocating operating room slots",
            "Nursing Coordination Agent": "Balancing nursing workload",
            "Laboratory Testing Agent": "Tracking pending lab tests",
            "Medical Imaging Agent": "Scheduling imaging scans",
            "Patient Flow Agent": "Analyzing bed occupancy trends",
            "Blood Inventory Agent": "Monitoring blood bank levels",
            "Organ Inventory & Matching Agent": "Matching organ availability",
            "Testing & Screening Agent": "Reviewing screening results",
            "Emergency Allocation Agent": "Allocating emergency resources",
            "Compliance & Data Security Agent": "Auditing data access logs",
            "Chief Decision Agent": "Coordinating cross-agent decisions",
        }
        for agent in AGENT_NAMES:
            conn.execute(
                """INSERT INTO agent_status
                   (agent_name, status, current_task, tasks_completed, last_activity)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    agent,
                    "Active" if agent == "Chief Decision Agent" else random.choice(["Active", "Monitoring"]),
                    tasks_map[agent],
                    random.randint(40, 300),
                    _now_str(random.randint(0, 30)),
                ),
            )

    if _table_empty(conn, "agent_activity_log"):
        sample_activities = [
            ("Emergency Response Agent", "Assigned Priority 1 to incoming trauma case"),
            ("Medical Imaging Agent", "Scheduled CT scan for suspected fracture"),
            ("Laboratory Testing Agent", "Requested CBC panel for admitted patient"),
            ("Nursing Coordination Agent", "Assigned vitals check to on-duty nurse"),
            ("Pharmacy Agent", "Detected low stock on Ceftriaxone"),
            ("Chief Decision Agent", "Generated coordination plan for ED surge"),
            ("Patient Admission Agent", "Processed new patient registration"),
            ("Surgery Scheduling Agent", "Reserved OR-2 for cardiac bypass"),
            ("Blood Inventory Agent", "Flagged O- blood type as critical"),
            ("Compliance & Data Security Agent", "Completed routine access audit"),
        ]
        for i, (agent, activity) in enumerate(sample_activities):
            conn.execute(
                "INSERT INTO agent_activity_log (agent_name, activity, timestamp) VALUES (?, ?, ?)",
                (agent, activity, _now_str(i * 7)),
            )

    if _table_empty(conn, "decisions"):
        conn.execute(
            """INSERT INTO decisions
               (priority, situation, agents_consulted, recommendation, human_approval, status, timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                "CRITICAL",
                "Emergency department demand is increasing while available beds are limited.",
                "Emergency Response Agent, Bed/Patient Flow Agent, Nursing Coordination Agent, Medical Imaging Agent",
                "Prioritize emergency admissions, identify available beds, coordinate nursing capacity "
                "and expedite required imaging.",
                "Required",
                "Awaiting Human Approval",
                _now_str(2),
            ),
        )

    if _table_empty(conn, "compliance_log"):
        checks = [
            ("Access Audit", "Passed", "No unauthorized data access detected in last cycle"),
            ("Data Encryption Check", "Passed", "All patient records encrypted at rest"),
            ("Consent Verification", "Passed", "Consent forms verified for active admissions"),
            ("Retention Policy Check", "Passed", "No records exceeding retention window"),
        ]
        for check_type, status, details in checks:
            conn.execute(
                "INSERT INTO compliance_log (check_type, status, details, timestamp) VALUES (?, ?, ?, ?)",
                (check_type, status, details, _now_str(random.randint(0, 200))),
            )

    conn.commit()
    conn.close()
