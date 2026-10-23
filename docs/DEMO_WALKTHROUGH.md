# Adaptive Loop: Complete Interactive Demo & System Walkthrough

> **A Beginner-Friendly, Visual Guide to Clinical Decision Support for Longevity Medicine**  
> *Written for everyone — no prior programming, medical, or data science background required.*

---

## 1. The Big Picture: Why Does Adaptive Loop Exist?

Imagine you visit a doctor because you want to live a long, healthy life and avoid heart disease. The doctor tests your blood, hands you a supplement regimen (like Citrus Bergamot) and an exercise recommendation (like 45 minutes of Zone 2 cardio three times a week), and says:

> *"See you in six months for your next blood test!"*

For the next 180 days, you are inside what longevity clinicians call the **"Six-Month Black Box"**:

```
[ Day 0: Blood Test ] ──────▶ [ 180-Day Black Box: Life Happens! ] ──────▶ [ Day 180: Blood Test ]
                                  • Did you take the supplement?
                                  • Did you get sick or travel?
                                  • Did you switch high-stress jobs?
                                  • Did your sleep improve or crash?
```

During those six months, you wear a smartwatch (Apple Watch, Oura Ring, or Whoop) that logs your heart rate, sleep quality, and heart rate variability (HRV) every single minute. Yet when you return on Day 180, your doctor looks **only** at the two blood tests. 

If your cholesterol improved, the doctor assumes the supplement worked. If it got worse, they assume the supplement failed.

### The Fatal Flaw: The "Attribution Fallacy"
In real life, health is complicated:
- What if your cholesterol improved because you **quit a toxic job** in Month 2 and your stress levels plummeted?
- What if your biometrics looked worse because you **caught a viral respiratory infection** two weeks before the test?
- What if you only remembered to take the pills **25% of the time**?

Attributing the outcome purely to the supplement without looking at your daily smartwatch data and major life events is an **Attribution Fallacy**.

### The Solution: Adaptive Loop
**Adaptive Loop** is an **Intervention Intelligence Engine**. It acts like a brilliant clinical co-pilot that sits between your wearable watch data, your lab blood panels, and your doctor:
1. It continuously stitches together **180 days of daily wearable records** with **Day 0 and Day 180 blood lab tests**.
2. It tracks **lifestyle confounders** (job changes, illnesses, cross-time-zone travel).
3. It runs a **4-stage neuro-symbolic analysis**: a live AI Analyst (powered by Groq's `openai/gpt-oss-120b` 120-billion parameter model) generates medical hypotheses, a mathematical verification engine checks every fact against the database, and an adversarial AI Critic audits the findings for bias or false attribution.
4. If your data is too sparse or corrupted, it has the integrity to **principledly abstain** rather than hallucinate a dangerous guess.

---

## 2. Core Architectural Guarantees (Made Simple)

| Principle | What It Means | Why It Matters to Patients |
| :--- | :--- | :--- |
| **Zero Algorithmic Dishonesty** | No fake mock responses in production, no pre-calculated results stored in advance. Every analysis is computed live. | You can trust that recommendations reflect actual real-time reasoning, not hardcoded marketing scripts. |
| **Neuro-Symbolic Pipeline** | "Neuro" = AI reasoning (LLM). "Symbolic" = Hard rules and exact mathematics (Python/Pandas). | AI can make arithmetic mistakes; cold code does the math, while AI provides clinical nuance. |
| **Dual-Agent Adversarial Audit** | An **Analyst Agent** writes the initial report, and a skeptical **Critic Agent** audits it for cognitive bias and confounders. | Two heads are better than one: the Critic prevents overconfidence and calls out unearned credit. |
| **Principled Abstention Guard** | If data completeness is $<50\%$ or adherence is $<40\%$, the system refuses to guess. | In medicine, saying *"I do not have enough data to know"* is infinitely safer than making a confident wild guess. |

---

## 3. Step 1: The Clinical Command Center (Dashboard Landing)

When you first open the application, you arrive at the **Adaptive Loop Command Center**.

![Dashboard Landing](./screenshots/01_dashboard_landing.png)

### Key Interface Elements:
1. **Top Navigation Bar:**
   - **Adaptive Loop Logo:** Identifies the Intervention Intelligence Engine.
   - **Active Model Badge (`openai/gpt-oss-120b`):** Confirms that real, live inference is wired directly to Groq's 120B open-source reasoning model.
   - **Clinical Decision Support Prototype:** A clear reminder that this tool assists licensed clinicians rather than replacing them.
2. **Cohort Filter Bar:**
   - Allows clinicians to filter patient test cases by medical category: *Cardiometabolic & Longevity*, *Neuro-Endocrine & Sleep Architecture*, *Metabolic Syndrome & Glycemic Control*, or custom cohorts.
3. **Pre-Loaded Benchmark Persona Cards:**
   - **Marcus Vance (MEM-1001):** The *Clean Benchmark* (high adherence, clear physiological improvements, zero confounders).
   - **Elena Rostova (MEM-1002):** The *Confounded Benchmark* (good results, but complicated by a career resignation and a viral illness).
   - **David Chen (MEM-1003):** The *Sparse Benchmark* (missing data and poor adherence, testing safety guards).
4. **Action Button (`+ Add Test Case User`):**
   - Lets you create your own custom patient with custom cohorts and synthetic biometric profiles on the fly.
5. **No Pre-Calculated Results:**
   - Notice that the dashboard starts with a clean slate: no analysis has been computed beforehand. Results are generated on-demand when you click **"Run Adaptive Analysis"**.

---

## 4. Step 2: Exploring Patient Telemetry & Protocols (Marcus Vance)

Let's click on **Marcus Vance (MEM-1001)** and scroll down to view his 180-day health record.

![Marcus Vance Baseline Telemetry](./screenshots/02_marcus_telemetry_protocols.png)

### Understanding the Medical Metrics:
- **Biomarkers (Blood Tests):**
  - **Apolipoprotein B (ApoB):** Measures the number of plaque-causing particles in the bloodstream. Marcus started at `118 mg/dL` and dropped to `94 mg/dL` (a **-20.3%** improvement!).
  - **High-Sensitivity C-Reactive Protein (hs-CRP):** A marker of systemic blood vessel inflammation. Dropped from `2.4 mg/L` to `1.1 mg/L` (a **-54.2%** plunge!).
  - **LDL Cholesterol:** Dropped from `142 mg/dL` to `116 mg/dL` (**-18.3%**).
- **Wearable Trajectory Chart (Rolling 26 Weeks):**
  - **Green Line (HRV - Heart Rate Variability):** Rose steadily from `37.3 ms` to `48.8 ms`. Higher HRV indicates improved cardiovascular fitness and stress resilience.
  - **Red Dotted Line (Resting Heart Rate - RHR):** Decreased from `61.2 bpm` to `55.6 bpm`. A lower resting heart rate shows a stronger, more efficient heart muscle.
  - **Blue & Purple Lines (Sleep):** Steady total sleep (`~7.1 hrs`) and deep sleep (`~1.3 hrs`).
- **Active Protocols:**
  - **Zone 2 Aerobic Base:** 45 minutes, 3 times per week at heart rate 125–138 bpm.
  - **Citrus Bergamot Supplement:** 500 mg daily with evening meal.
  - **Adherence:** Marcus logged an outstanding **88.3% protocol adherence** over 180 days.
- **Confounder Box:**
  - Displays *"0 Events"* — Marcus had no major illnesses or extreme disruptions during this test cycle.

---

## 5. Step 3: Triggering Live Multi-Stage AI Analysis

Now, let's click the vibrant green **"Run Adaptive Analysis"** button.

![Marcus Vance Analysis Executing](./screenshots/03_marcus_analysis_executing.png)

The UI instantly transitions into the **Live Execution Tracker**:
- **Stage 1 (Mathematical Aggregation):** Python aggregates 180 daily wearable records into 26 weekly rolling means and computes exact percentage deltas for lab blood markers.
- **Stage 2 (AI Analyst):** Sends the structured clinical bundle to Groq's `openai/gpt-oss-120b` LLM. The Analyst formulates primary and competing hypotheses.
- **Stage 3 (Deterministic Citation Check):** A rigid Python validator examines every observation ID cited by the AI to guarantee zero hallucinated evidence.
- **Stage 4 (Adversarial Critic Audit):** An adversarial AI Critic reviews the Analyst's hypotheses against the citation check and confounder timeline to spot overconfidence or attribution errors.

---

## 6. Step 4: Clean Responder Synthesis (Marcus Vance)

Within seconds, the live execution finishes, and the comprehensive clinical dossier appears!

![Marcus Vance Analysis Completed](./screenshots/04_marcus_analysis_completed.png)

### Key Insights from the Completed Report:
1. **Canonical Action Badge:**  
   `✔ Continue Protocol As Prescribed` (Green Badge). The system determines the protocol is working safely and effectively.
2. **Stage 2: AI Analyst Reasoning Ledger:**
   - **Primary Hypothesis (Moderate/High Confidence):**  
     *"The combined Zone 2 aerobic base training and daily Citrus Bergamot supplementation are plausibly driving the observed reductions in ApoB (-20.34%), LDL (-18.31%), and CRP (-54.17%) alongside progressive autonomic recovery..."*
   - **Grounded Citations:** The AI explicitly cited `OBS-BIO-APOB-D180`, `OBS-BIO-CRP-D180`, and `OBS-WEAR-HRV-W26`.
   - **Competing Alternative Explanations:** The AI responsibly acknowledges that dietary shifts or regression to the mean could partially contribute.
3. **Stage 4: Adversarial Clinical Audit:**
   - **Deterministic Citations:** `100% Grounded` (Zero hallucinations).
   - **Completeness Gate:** `PASSED` (88.3% completeness).
   - **Critic Verdict:** `VERDICT: APPROVED`. The Critic agrees that Marcus's response is genuine and unconfounded.

---

## 7. Step 5: Confounder Detection & Attribution Fallacy (Elena Rostova)

Next, let's switch to our second patient persona: **Elena Rostova (MEM-1002)** in the *Neuro-Endocrine & Sleep Architecture* cohort.

![Elena Rostova Confounder Timeline](./screenshots/05_elena_confounder_timeline.png)

### The Patient Context:
- **Primary Goal:** Deep sleep restoration & chronic stress reduction.
- **Prescribed Protocols:** Magnesium L-Threonate (400 mg before sleep) and an evening digital screen-time cutoff (10:00 PM).
- **The Numbers Look Great:** Her morning cortisol dropped by **-37.3%** (from 22 to 13.8 mcg/dL) and fasting glucose dropped by **-7.1%**.
- **Look Closely at the Confounders Box:**
  1. `CONF-CAREER-W08 (LIFE STRESS - SEVERE)`: In Week 8, Elena resigned from a grueling high-stress executive job! Her physical training load dropped by 70%, and sleep opportunity increased drastically.
  2. `CONF-ILLNESS-W14 (ILLNESS - MODERATE)`: In Week 14, she caught an acute viral upper respiratory infection (RSV), which crashed her HRV and elevated her heart rate for 6 days.

A naïve algorithm would look at the cortisol drop and declare: *"Magnesium L-Threonate is a miracle supplement!"*  
Let's see what the Adaptive Loop Adversarial Critic does.

---

## 8. Step 6: The Adversarial Critic Audit (Elena Rostova)

We click **"Run Adaptive Analysis"** for Elena.

![Elena Rostova Analysis Critic Audit](./screenshots/06_elena_analysis_critic_audit.png)

### The Result: The AI Critic Intervenes!
1. **Analyst Initial Verdict:** The Analyst initially suggested `CONTINUE_PROTOCOL`.
2. **Critic Verdict:** `VERDICT: AMENDED` (Golden Amber Warning).
3. **The Skeptical Audit:**  
   The Adversarial Critic caught the career transition:
   > *"The major life change (career transition in Week 8) represents a massive confounder that dramatically reduced psychological stress and allostatic load. The cortisol and sleep improvements cannot be solely attributed to Magnesium L-Threonate. Overconfidence penalized."*
4. **Action Downgrade:**  
   The final recommendation was amended to `EXTEND_OBSERVATION` to isolate the supplement's true effect from the job change.

This is the **Attribution Fallacy caught and neutralized** by autonomous dual-agent auditing.

---

## 9. Step 7: Principled Clinical Abstention (David Chen)

What happens when a patient doesn't wear their watch consistently or forgets their protocols? Let's select **David Chen (MEM-1003)** in the *Metabolic Syndrome & Glycemic Control* cohort.

![David Chen Principled Abstention](./screenshots/07_david_abstention_guard.png)

### The Problem:
- **Sparse Telemetry:** Looking at the chart between Weeks 18 and 26, wearable data flatlines. David frequently forgot to wear or charge his sensor device.
- **Low Protocol Adherence:** David only logged **27.8% protocol adherence** (shown in the red pill badge).
- **Confounders:** Multiple international business flights with severe circadian jetlag.

### The Result:
When we click **"Run Adaptive Analysis"**, the engine **does not guess**. The Python state guard fires in under 100 milliseconds:
- **Canonical Action Badge:** `Abstain / More Data Required` (Purple Badge).
- **Principled Abstention Warning:**
  > *"The engine detected insufficient data completeness (63.9%) or low protocol adherence (27.8%). As strictly mandated by clinical safety rules, inference was halted early without fabricating hypotheses."*

In high-stakes medicine, knowing when to **shut up and ask for more data** is the ultimate mark of clinical safety.

---

## 10. Step 8: Adding a Custom Test Case Member & Cohort

Now let's test the interactive data synthesizer! Click the blue **"+ Add Test Case User"** button in the top right.

![Add Custom Member Modal](./screenshots/08_add_member_modal.png)

### Modal Capabilities:
1. **Demographic Profile & Cohort Assignment:**
   - Full Name: `Dr. Julian Croft`
   - Age: `47` | Biological Sex: `MALE`
   - Target Cohort: We select `Cellular Longevity & NAD+ Recovery` (or type any custom cohort name).
   - Primary Health Goal: `Optimize NAD+ synthesis & mitochondrial fatty acid oxidation`.
2. **Prescribed Protocol Builder:**
   - Category (Supplement, Exercise, Nutrition, Lifestyle, Medication).
   - Dosage, Frequency, and Target Adherence rate.
3. **Longitudinal Biomarkers (Day 0 Baseline vs Day 180 Follow-up):**
   - Configurable marker codes, units, and clinical reference ranges.
4. **Telemetry Persona Engine:**
   - Choose between *Clean Responder*, *Confounded Responder*, or *Sparse / Non-Adherent*.

When you click **"Add Member to Database"**, the backend synthesizer mathematically models 180 individual daily records, applies realistic Gaussian noise, injects physiological trends, and commits the records to SQLite.

---

## 11. Step 9: The Newly Created Member in Action

The modal closes, and **Dr. Julian Croft (MEM-2001)** is immediately loaded into the dashboard!

![Custom Member Created](./screenshots/09_custom_member_created.png)

### Notice:
1. **Interactive Member Card:** Displays `Dr. Julian Croft`, cohort `Cellular Longevity & NAD+ Recovery`, a `Custom Test Case` pill, and a trashcan icon to delete the member if needed.
2. **Interactive Hover Tooltips:** Hovering over any week on the trajectory chart displays the exact synchronized weekly averages:
   - *Week 20: HRV = 42.8 ms, Resting HR = 62.8 bpm, Total Sleep = 7.13 hrs, Deep Sleep = 1.51 hrs.*
3. **Clean Slate Guarantee:** The analysis has not been pre-computed. The green **"Run Adaptive Analysis"** button is primed and waiting.

---

## 12. Step 10: Running Live Analysis on the Custom Member

Finally, let's click **"Run Adaptive Analysis"** for Dr. Julian Croft.

![Custom Member Analysis Result](./screenshots/10_custom_member_analysis_result.png)

### What Happened Live Behind the Scenes:
1. The backend compiled Dr. Croft's 180-day telemetry profile and biomarker changes (ApoB dropped by **-21.1%**, hs-CRP dropped by **-53.8%**).
2. Groq's `openai/gpt-oss-120b` LLM analyzed the cellular longevity protocol in real-time.
3. The deterministic verification engine verified that Dr. Croft logged **86.1% adherence** with no confounding events.
4. The Adversarial Critic audited the findings and approved the protocol continuation.
5. The dashboard rendered the synthesized recommendation: `✔ Continue Protocol As Prescribed`.

---

## 13. Summary Matrix of All Benchmark Scenarios

| Patient Persona | Cohort | Telemetry Profile | Adherence | Confounders | Engine Verdict | Clinical Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Marcus Vance** (`MEM-1001`) | Cardiometabolic & Longevity | Clean, high-signal wearable data | 88.3% | None (0) | `APPROVED` | **CONTINUE_PROTOCOL** |
| **Elena Rostova** (`MEM-1002`) | Neuro-Endocrine & Sleep Architecture | Strong improvement, but confounded | 62.2% | Career transition (W08), RSV infection (W14) | `AMENDED` | **EXTEND_OBSERVATION** |
| **David Chen** (`MEM-1003`) | Metabolic Syndrome & Glycemic Control | Sparse sensor data, large data gaps | 27.8% | Transpacific & Transatlantic flights | `ABSTAINED` | **ABSTAIN_MORE_DATA_REQUIRED** |
| **Dr. Julian Croft** (`MEM-2001`) | Cellular Longevity & NAD+ Recovery | Custom created on-demand telemetry | 86.1% | None (0) | `APPROVED` | **CONTINUE_PROTOCOL** |

---

## 14. Verification & Inspection Commands

To run this demo or reproduce any part of the verification independently, use the following commands:

```bash
# 1. Start the FastAPI backend
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. Start the Next.js frontend (in a separate terminal)
cd frontend
npm run dev

# 3. Re-run the automated Playwright demo and screenshot capture
python run_demo_and_capture.py
```

All 10 high-resolution screenshots are permanently archived in:
- Artifacts: `C:\Users\admin\.gemini\antigravity\brain\f31d380e-4922-4144-93ec-efbe752ebaf3\screenshots\`
- Repository: `c:\Users\admin\Downloads\broyo\docs\screenshots\`
