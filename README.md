# 🏥 Hospital AI – Multi-Agent Operations Assistant

An autonomous multi-agent hospital operations dashboard built for hackathon demonstration.
Sixteen specialized AI agents (Patient Admission, Emergency Response, Diagnosis Support,
Treatment Planning, Pharmacy, Surgery Scheduling, Nursing Coordination, Laboratory,
Medical Imaging, Patient Flow, Blood Inventory, Organ Inventory & Matching, Testing &
Screening, Emergency Allocation, and Compliance & Data Security) feed findings into a
central **Chief Decision Agent**, which detects conflicts, prioritizes urgent issues,
and produces an explainable, human-approved action plan.

> ⚠️ **All data in this application is simulated.** This is an operational
> decision-support prototype and is **not** a replacement for qualified
> healthcare professionals or real clinical systems.

## Tech Stack

- Python
- Streamlit (UI)
- SQLite (storage)
- Pandas (data handling)
- Plotly (charts)
- Custom CSS (styling)

## Project Structure

```
hospital_ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── agents/
│   ├── base_agent.py
│   ├── admission_agent.py
│   ├── emergency_agent.py
│   ├── diagnosis_agent.py
│   ├── treatment_agent.py
│   ├── pharmacy_agent.py
│   ├── surgery_agent.py
│   ├── nursing_agent.py
│   ├── laboratory_agent.py
│   ├── imaging_agent.py
│   ├── patient_flow_agent.py
│   ├── blood_inventory_agent.py
│   ├── organ_inventory_agent.py
│   ├── screening_agent.py
│   ├── emergency_allocation_agent.py
│   ├── compliance_agent.py
│   └── chief_decision_agent.py
│
├── database/
│   ├── database.py
│   └── seed_data.py
│
├── pages_app/
│   ├── dashboard.py
│   ├── patients.py
│   ├── agents.py
│   ├── emergency.py
│   ├── laboratory.py
│   ├── imaging.py
│   ├── surgery.py
│   ├── pharmacy.py
│   ├── nursing.py
│   ├── analytics.py
│   └── system_status.py
│
├── utils/
│   ├── helpers.py
│   └── styles.py
│
└── assets/
    └── styles.css
```

## Setup — Windows PowerShell

```powershell
# 1. Navigate to the project folder
cd hospital_ai

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python -m streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.
The SQLite database (`database/hospital.db`) and its seed data are created
automatically on first run, and re-running the app will **not** duplicate data.

## Publishing to GitHub

```powershell
git init
git add .
git commit -m "Initial commit: Hospital AI Multi-Agent Operations Assistant"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

## Notes

- All patient, clinical, and operational data is **simulated** for demonstration only.
- The Chief Decision Agent's recommendations always require human approval for
  CRITICAL and HIGH priority situations — this system does not act autonomously
  on clinical matters.
- Database initialization and seeding are idempotent: tables are only seeded
  when empty, so repeated runs are safe.
