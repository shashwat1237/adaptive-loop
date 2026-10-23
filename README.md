# Adaptive Loop — Intervention Intelligence Engine

> A closed-loop clinical decision support prototype evaluating member health protocols between 6-month blood testing cycles.

---

## 1. System Overview

Between baseline biomarker testing (Day 0) and the repeat laboratory panel (Day 180), longevity medicine faces a **6-month black box**:
- *Was the assigned protocol followed?*
- *What physiological metrics shifted in daily wearable telemetry?*
- *Did acute confounders (illness, career stress, travel) distort the signal?*
- *What does the evidence actually support doing next?*

**Adaptive Loop** solves this through a **Neuro-Symbolic, AI-First Architecture**:
1. **Pandas Statistical Engine:** Computes rolling averages, percentage deltas, completeness scores, and observation registries with zero manual clinical rules.
2. **AI Analyst (`openai/gpt-oss-120b` via Groq):** Formulates primary intervention hypotheses and competing alternative explanations, citing registered observation IDs.
3. **Deterministic Evidence Checker (Python Middleware):** Validates that cited observation IDs exist and arithmetic deltas match ground truth within $\pm 0.5\%$.
4. **Adversarial AI Critic:** Audits the analysis for attribution fallacies, flags unaddressed confounders, penalizes overconfidence, and assigns a clinical action verdict.
5. **Interactive Dashboard (Next.js 14):** Visualizes 180-day longitudinal trends, lab comparisons, confounder overlays, and side-by-side analyst/critic ledgers.

---

## 2. Quickstart Runbook

### 2.1 Backend Setup (FastAPI + SQLite)
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Seed synthetic personas (Marcus Vance, Elena Rostova, David Chen)
python -m app.seed.seeder

# Run automated test suites (18/18 tests)
python -m pytest tests -v

# Launch FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
* **API Endpoints:** `http://localhost:8000/api/v1`
* **Swagger OpenAPI Docs:** `http://localhost:8000/docs`

---

### 2.2 Frontend Setup (Next.js 14 + Tailwind + Recharts)
```bash
# In a separate terminal, navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Build production bundle
npm run build

# Start Next.js server
npm run dev
```
* **Interactive Dashboard:** `http://localhost:3000`

---

## 3. Pre-Calibrated Synthetic Personas

| Persona | Archetype | Clinical Trajectory | Expected Action & Verdict |
| :--- | :--- | :--- | :--- |
| **Marcus Vance** (`MEM-1001`) | Clean Responder | High adherence ($88.3\%$), ApoB dropped $-20.34\%$ ($118 \rightarrow 94$ mg/dL), zero confounders. | `APPROVED` $\rightarrow$ `CONTINUE_PROTOCOL` |
| **Elena Rostova** (`MEM-1002`) | Confounded Case | Deep sleep rose $+61.9\%$, but job resignation in W8 (70% training drop) and illness in W14. | `AMENDED` $\rightarrow$ `ADJUST_WITH_CLINICIAN` (Critic flags job transition as competing explanation) |
| **David Chen** (`MEM-1003`) | Non-Adherent | Berberine protocol, low adherence ($27.8\%$), frequent travel, HbA1c unchanged at $5.9\%$. | `APPROVED` $\rightarrow$ `ABSTAIN_MORE_DATA_REQUIRED` (Identifies non-adherence as primary obstacle) |

---

## 4. Verification & Testing

To execute the automated verification test suite:
```bash
cd backend
python -m pytest tests -v
```
All 18 acceptance tests pass in under 2 seconds:
- Mathematical delta calculations & edge-case zero baselines
- Wearable completeness & protocol adherence rates
- Observation registry lookup & fake citation detection
- Principled abstention guards ($C_{\text{rate}} < 50.0\%$ and $A_{\text{rate}} < 40.0\%$)
- Full 3-persona acceptance pipeline runs
- REST API contracts, 404 error envelopes, and 201 created responses

---

## 5. Repository Layout

```
broyo/
├── specs/                        # Authoritative frozen specification bundle (16 docs)
├── backend/                      # Python 3.11+ / FastAPI application
│   ├── app/
│   │   ├── api/                  # REST endpoints (/health, /members, /analyses)
│   │   ├── engine/               # Aggregator, CitationChecker, LLMClient, Analyst, Critic, Coordinator
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── schemas/              # Pydantic v2 validation models
│   │   └── seed/                 # Synthetic persona dataset generators & seeder
│   ├── tests/                    # Pytest test suites (18 test cases)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                     # Next.js 14 App Router dashboard
│   ├── src/
│   │   ├── app/                  # Main layout and dashboard pages
│   │   ├── components/           # UI components (Chart, Badges, Cards, Selector)
│   │   └── lib/                  # Typed API client & data contracts
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```
