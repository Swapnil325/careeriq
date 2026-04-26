# CareerIQ — Student Career Guidance Expert System
### Complete Project Documentation

---

## Table of Contents

1. [What is this project?](#1-what-is-this-project)
2. [How the whole system works — Big Picture](#2-how-the-whole-system-works--big-picture)
3. [Project folder structure](#3-project-folder-structure)
4. [File-by-file explanation](#4-file-by-file-explanation)
   - [knowledge_base.py](#41-knowledge_basepy)
   - [inference_engine.py](#42-inference_enginepy)
   - [app.py](#43-apppy)
   - [templates/index.html](#44-templatesindexhtml)
   - [static/css/style.css](#45-staticcssstylecss)
   - [static/js/main.js](#46-staticjsmainjs)
5. [The Expert System explained simply](#5-the-expert-system-explained-simply)
6. [Forward Chaining — step by step](#6-forward-chaining--step-by-step)
7. [Confidence scoring explained](#7-confidence-scoring-explained)
8. [API reference](#8-api-reference)
9. [Sample request and response](#9-sample-request-and-response)
10. [How to run the project](#10-how-to-run-the-project)
11. [How to add a new career rule](#11-how-to-add-a-new-career-rule)

---

## 1. What is this project?

CareerIQ is a **Rule-Based Expert System** that helps students figure out which career suits them best.

You fill in a form with four things:
- What subjects interest you (coding, biology, business, etc.)
- How good your grades are in Math, Science, and English
- What skills you have (analytical, creative, communication, etc.)
- What your personality is like (leader, empathetic, detail-oriented, etc.)

The system then runs those answers through a set of **IF-THEN rules** (like a doctor's checklist) and tells you which careers match — along with a confidence score and a plain-English explanation for each one.

---

## 2. How the whole system works — Big Picture

Here is the full journey from the moment you click "Analyse my profile" to the moment you see your results:

```
  [ Browser Form ]
       |
       |  User fills in interests, grades, skills, personality
       |
       v
  [ main.js ]
       |
       |  Collects all selected values into a JSON object
       |  Sends POST request to /predict
       |
       v
  [ app.py  —  Flask Server ]
       |
       |  Receives the JSON
       |  Validates that all 4 fields are present
       |  Calls run_inference(data)
       |
       v
  [ inference_engine.py ]
       |
       |  Cleans and normalises the input (lowercase, strip spaces)
       |  Stores it in "working memory"
       |  Loops through every rule in the knowledge base
       |  For each rule: checks if ALL condition groups are satisfied
       |  Calculates a confidence score for each matched rule
       |  Returns a sorted list of matched careers
       |
       v
  [ knowledge_base.py ]
       |
       |  Provides the 15 IF-THEN rules
       |  Each rule has: conditions, career name, explanation, base score
       |
       v
  [ app.py  —  Flask Server ]
       |
       |  Receives the matched careers list
       |  Wraps it in a JSON response
       |  Sends it back to the browser
       |
       v
  [ main.js ]
       |
       |  Receives the JSON response
       |  Builds career cards dynamically in HTML
       |  Displays them on the page with score badges
       |
       v
  [ Browser — Results ]
       Career cards shown, sorted by confidence score
```

---

## 3. Project folder structure

```
career_guidance/
│
├── app.py                  ← Flask web server and REST API
├── inference_engine.py     ← The brain — forward chaining logic
├── knowledge_base.py       ← All 15 IF-THEN career rules
├── requirements.txt        ← Python packages needed
├── README.md               ← This file
│
├── templates/
│   └── index.html          ← The webpage the user sees
│
└── static/
    ├── css/
    │   └── style.css       ← All visual styling
    └── js/
        └── main.js         ← Frontend interactivity and API calls
```

**Why this structure?**
Flask has a specific convention: HTML files go in `templates/`, and everything else (CSS, JS, images) goes in `static/`. Flask knows to look in these exact folders automatically.

---

## 4. File-by-file explanation

---

### 4.1 `knowledge_base.py`

**What it is:** A plain Python file that holds a list called `RULES`. Nothing else. No logic, no functions — just data.

**What one rule looks like:**

```python
{
    "id": "R01",
    "career": "Software Engineer",
    "conditions": {
        "interests": ["coding"],
        "marks":     {"math": "high"},
    },
    "explanation": "Strong math skills combined with a coding interest are the core foundation of software engineering.",
    "base_score": 90,
}
```

**Breaking down each field:**

| Field | What it means |
|---|---|
| `id` | A unique label like R01, R02 — just for tracking |
| `career` | The career name that gets shown to the user |
| `conditions` | The IF part of the IF-THEN rule. All groups listed here must be satisfied |
| `conditions.interests` | At least one of these interests must be selected by the user |
| `conditions.marks` | ALL of these subject-level pairs must match exactly |
| `conditions.skills` | At least one of these skills must be selected |
| `conditions.personality` | At least one of these traits must be selected |
| `explanation` | The sentence shown to the user explaining why this career was suggested |
| `base_score` | The maximum possible confidence score for this career (out of 100) |

**Important:** Not every rule uses all four condition types. For example, Rule R01 only checks `interests` and `marks`. Rule R06 checks `interests`, `skills`, AND `personality`. The more conditions a rule has, the more specific it is.

**The 15 careers covered:**

| Rule | Career |
|---|---|
| R01 | Software Engineer |
| R02 | Data Scientist |
| R03 | Doctor / Physician |
| R04 | Biomedical Researcher |
| R05 | Business Analyst |
| R06 | Entrepreneur |
| R07 | Graphic Designer |
| R08 | UX / UI Designer |
| R09 | Journalist / Content Writer |
| R10 | Civil Engineer |
| R11 | Psychologist / Counselor |
| R12 | Teacher / Educator |
| R13 | Cybersecurity Analyst |
| R14 | Marketing Manager |
| R15 | Environmental Scientist |

---

### 4.2 `inference_engine.py`

**What it is:** The brain of the system. This file takes the user's input, compares it against every rule, and decides which careers match.

It has three functions:

---

**Function 1: `_normalise(value)`**

```python
def _normalise(value):
    if isinstance(value, list):
        return [v.lower().strip() for v in value]
    return value.lower().strip()
```

This is a small helper. It converts everything to lowercase and removes extra spaces. This prevents bugs like "Coding" not matching "coding", or " biology " not matching "biology". It handles both single strings and lists of strings.

---

**Function 2: `_build_working_memory(user_input)`**

```python
def _build_working_memory(user_input: dict) -> dict:
    return {
        "interests":   _normalise(user_input.get("interests", [])),
        "marks":       {k: _normalise(v) for k, v in user_input.get("marks", {}).items()},
        "skills":      _normalise(user_input.get("skills", [])),
        "personality": _normalise(user_input.get("personality", [])),
    }
```

"Working memory" is an AI term for the current known facts. This function takes the raw JSON from the user and turns it into a clean, normalised dictionary. If the user didn't provide a field, it defaults to an empty list so the rest of the code never crashes.

Example — raw input comes in as:
```json
{"interests": ["Coding", "Business"], "marks": {"Math": "High"}, ...}
```

After working memory is built:
```python
{"interests": ["coding", "business"], "marks": {"math": "high"}, ...}
```

---

**Function 3: `_check_rule(rule, wm)`**

This is the core matching function. It takes one rule and the working memory, and decides if the rule fires (matches) or not.

It checks each condition group one by one:

```
interests check:
  → Does the user have AT LEAST ONE of the required interests?
  → If NO  → rule fails immediately, return False
  → If YES → count it as matched, record what matched

marks check:
  → Does the user have ALL of the required subject-grade pairs?
  → If even one mark is missing or wrong → rule fails immediately
  → If ALL match → count it as matched

skills check:
  → Does the user have AT LEAST ONE of the required skills?
  → If NO  → rule fails immediately
  → If YES → count it as matched

personality check:
  → Does the user have AT LEAST ONE of the required traits?
  → If NO  → rule fails immediately
  → If YES → count it as matched
```

Notice the difference: **marks requires ALL to match** (you need both math=high AND science=high for Data Scientist), but **interests/skills/personality only need ONE match** (having "coding" is enough even if the rule also lists "arts").

If all condition groups pass, it calculates the confidence score and returns True.

---

**Function 4: `run_inference(user_input)`**

```python
def run_inference(user_input: dict) -> list[dict]:
    wm      = _build_working_memory(user_input)
    results = []
    for rule in RULES:
        fired, confidence, matched_keys = _check_rule(rule, wm)
        if fired:
            results.append({...})
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results
```

This is the main entry point called by `app.py`. It:
1. Builds working memory from the user input
2. Loops through all 15 rules
3. Collects every rule that fires
4. Sorts the results by confidence score (highest first)
5. Returns the final list

---

### 4.3 `app.py`

**What it is:** The Flask web server. It has two jobs — serve the webpage, and handle the API.

**Route 1: `GET /`**

```python
@app.route("/")
def index():
    return render_template("index.html")
```

When someone opens `http://localhost:5000` in their browser, Flask finds `templates/index.html` and sends it back. That's the form the user fills in.

**Route 2: `POST /predict`**

This is the API endpoint. Here is what it does step by step:

```
1. Read the JSON body from the request
2. If no JSON → return error 400
3. Check that interests, marks, skills, personality are all present
4. If any are missing → return error 400 with a message saying which ones
5. Call run_inference(data) from inference_engine.py
6. If no careers matched → return success with empty list
7. If careers matched → return success with the full list
```

The response always has a `status` field ("success" or "error") so the frontend always knows what happened.

---

### 4.4 `templates/index.html`

**What it is:** The single HTML page the user interacts with. It is structured in clear sections:

| Section | What it does |
|---|---|
| `<header>` | Top navigation bar with the logo |
| `<section class="hero">` | The big intro area with the headline and stats |
| `<form id="careerForm">` | The four-part input form |
| `#sec1` — Interests | Toggle buttons for 6 interest areas |
| `#sec2` — Grades | Radio buttons for Math, Science, English |
| `#sec3` — Skills | Toggle buttons for 6 skills |
| `#sec4` — Personality | Toggle buttons for 6 personality traits |
| `#resultsSection` | Hidden by default, shown after API responds with matches |
| `#noResults` | Hidden by default, shown if no careers matched |
| `#loadingOverlay` | A spinner shown while waiting for the API |

**Why is the results section hidden by default?**
Because there are no results yet. `main.js` removes the `hidden` class once the API responds. This avoids a separate page load — everything happens on one page.

---

### 4.5 `static/css/style.css`

**What it is:** All the visual styling. Key design decisions:

| Decision | Reason |
|---|---|
| Off-white `#f5f4f0` background | Feels like paper, easy on the eyes, not a generic dark theme |
| `Sora` font for headings | Geometric, modern, but not overused |
| `Inter` font for body text | The most readable UI font available |
| Single accent colour `#7c6af7` | One purple used consistently — not a rainbow of colours |
| Score badge colours: green / purple / amber | Green = strong match (85%+), Purple = good match (75–84%), Amber = partial match |
| No gradients on text | Gradients on text are the #1 sign of AI-generated UI |
| `1px solid` borders on cards | Honest, clean — no glow, no shadow theatrics |
| Responsive grid | Works on mobile with a single `@media` query |

---

### 4.6 `static/js/main.js`

**What it is:** All the browser-side logic. It does five things:

**1. Toggle buttons**
```javascript
document.querySelectorAll(".tog").forEach(btn => {
    btn.addEventListener("click", () => btn.classList.toggle("on"));
});
```
Every interest/skill/personality button gets a click listener. Clicking adds or removes the `on` CSS class, which changes the button's appearance (highlighted = selected).

**2. Progress bar**
When the user clicks inside any section, the progress dots at the top update to show how far along they are.

**3. `collect()` — gather form data**
```javascript
function collect() {
    const interests   = [...document.querySelectorAll("#interestChips .tog.on")].map(b => b.dataset.value);
    const skills      = [...document.querySelectorAll("#skillChips .tog.on")].map(b => b.dataset.value);
    const personality = [...document.querySelectorAll("#personalityChips .tog.on")].map(b => b.dataset.value);
    const marks = {};
    ["math","science","english"].forEach(s => {
        const r = document.querySelector(`input[name="${s}"]:checked`);
        if (r) marks[s] = r.value;
    });
    return { interests, marks, skills, personality };
}
```
This reads all selected buttons and checked radio buttons and packages them into the exact JSON format the API expects.

**4. Form submit → API call**
```javascript
document.getElementById("careerForm").addEventListener("submit", async e => {
    e.preventDefault();           // stop the page from refreshing
    overlay.classList.remove("hidden");  // show spinner
    const res  = await fetch("/predict", { method: "POST", ... });
    const data = await res.json();
    // show results or no-match message
});
```
`e.preventDefault()` stops the browser's default form behaviour (which would refresh the page). Instead, it sends the data to Flask using `fetch()` and waits for the response without any page reload.

**5. `buildCard(item, rank)` — render results**
For each career in the API response, this function builds an HTML card string with the career name, emoji, explanation, confidence badge, and matched-on pills. All cards are injected into the page at once using `innerHTML`.

---

## 5. The Expert System explained simply

An Expert System is a program that mimics how a human expert makes decisions.

Think of a doctor diagnosing a patient:
- The doctor has a set of rules in their head: "IF the patient has a fever AND a sore throat → likely strep throat"
- The doctor collects facts about the patient (symptoms)
- The doctor matches those facts against their rules
- The doctor gives a diagnosis with a reason

CareerIQ works exactly the same way:
- The **knowledge base** = the doctor's rules
- The **user's form answers** = the patient's symptoms
- The **inference engine** = the doctor's reasoning process
- The **career suggestions with explanations** = the diagnosis

---

## 6. Forward Chaining — step by step

Forward chaining means: **start with the facts, work towards a conclusion.**

(The opposite, backward chaining, would start with a conclusion and try to prove it — like a lawyer.)

Here is exactly what happens when a user submits the form:

```
Step 1 — Facts are collected
  User selected: interests=[coding], marks={math:high}, skills=[analytical], personality=[detail-oriented]

Step 2 — Working memory is built
  wm = {
    interests:   ["coding"],
    marks:       {"math": "high"},
    skills:      ["analytical"],
    personality: ["detail-oriented"]
  }

Step 3 — Check Rule R01 (Software Engineer)
  Condition: interests must include "coding"   → "coding" IS in wm.interests ✓
  Condition: marks must have math=high         → wm.marks.math IS "high"     ✓
  All conditions passed → Rule FIRES
  Confidence = 90 × (2 matched / 2 total) = 90.0%

Step 4 — Check Rule R02 (Data Scientist)
  Condition: interests must include "coding"   → ✓
  Condition: marks must have math=high         → ✓
  Condition: marks must have science=high      → user did NOT set science → ✗
  One condition failed → Rule does NOT fire

Step 5 — Check Rule R13 (Cybersecurity Analyst)
  Condition: interests must include "coding"   → ✓
  Condition: skills must include "analytical"  → ✓
  Condition: personality must include "detail-oriented" → ✓
  All conditions passed → Rule FIRES
  Confidence = 88 × (3 matched / 3 total) = 88.0%

Step 6 — Continue through all 15 rules...

Step 7 — Sort all fired rules by confidence (highest first)

Step 8 — Return the sorted list
```

---

## 7. Confidence scoring explained

Every rule has a `base_score` — the maximum it can score if all its conditions are met.

The actual confidence is calculated as:

```
confidence = base_score × (number of matched condition groups / total condition groups in the rule)
```

**Example — Rule R02 (Data Scientist, base_score = 92):**

The rule has 3 condition groups: interests, marks, skills.

| Scenario | Matched groups | Confidence |
|---|---|---|
| User has coding + math=high + science=high + analytical | 3 / 3 | 92 × 1.00 = **92.0%** |
| User has coding + math=high + science=high (no analytical) | marks fail → rule doesn't fire | — |

Note: because marks requires ALL subjects to match, a partial marks match causes the whole rule to fail rather than giving partial credit. This is intentional — you can't be a Data Scientist without both math AND science.

**Score badge colours:**
- 🟢 Green badge → 85% and above (strong match)
- 🟣 Purple badge → 75% to 84% (good match)
- 🟡 Amber badge → below 75% (partial match)

---

## 8. API reference

### `POST /predict`

**Request headers:**
```
Content-Type: application/json
```

**Request body fields:**

| Field | Type | Required | Values |
|---|---|---|---|
| `interests` | array of strings | yes | coding, biology, business, arts, engineering, social |
| `marks` | object | yes | keys: math, science, english — values: low, medium, high |
| `skills` | array of strings | yes | analytical, communication, creativity, leadership, problem-solving, teamwork |
| `personality` | array of strings | yes | detail-oriented, leader, empathetic, patient, risk-taker, introvert |

**Response fields:**

| Field | Type | Meaning |
|---|---|---|
| `status` | string | "success" or "error" |
| `total_matches` | number | How many careers matched |
| `careers` | array | List of matched career objects, sorted by confidence |
| `careers[].career` | string | Career name |
| `careers[].confidence` | number | Score from 0–100 |
| `careers[].explanation` | string | Why this career was suggested |
| `careers[].rule_id` | string | Which rule fired (R01–R15) |
| `careers[].matched_on` | array | What specifically matched (for transparency) |

---

## 9. Sample request and response

**Request:**
```json
POST /predict
{
  "interests":   ["coding", "business"],
  "marks":       {"math": "high", "science": "high", "english": "medium"},
  "skills":      ["analytical", "communication"],
  "personality": ["detail-oriented", "leader"]
}
```

**Response:**
```json
{
  "status": "success",
  "total_matches": 5,
  "careers": [
    {
      "career":      "Data Scientist",
      "confidence":  92.0,
      "explanation": "Data science demands high math & science marks plus strong analytical thinking and coding interest.",
      "rule_id":     "R02",
      "matched_on":  ["interests: coding", "marks: math=high, science=high", "skills: analytical"]
    },
    {
      "career":      "Software Engineer",
      "confidence":  90.0,
      "explanation": "Strong math skills combined with a coding interest are the core foundation of software engineering.",
      "rule_id":     "R01",
      "matched_on":  ["interests: coding", "marks: math=high"]
    },
    {
      "career":      "Cybersecurity Analyst",
      "confidence":  88.0,
      "explanation": "Cybersecurity needs coding interest, sharp analytical skills, and a detail-oriented mindset.",
      "rule_id":     "R13",
      "matched_on":  ["interests: coding", "skills: analytical", "personality: detail-oriented"]
    },
    {
      "career":      "Business Analyst",
      "confidence":  83.0,
      "explanation": "Business analysis blends analytical thinking with communication — exactly your skill set.",
      "rule_id":     "R05",
      "matched_on":  ["interests: business", "skills: analytical, communication"]
    },
    {
      "career":      "Entrepreneur",
      "confidence":  80.0,
      "explanation": "Entrepreneurship thrives on creativity, communication, and a risk-taking leadership personality.",
      "rule_id":     "R06",
      "matched_on":  ["interests: business", "skills: communication", "personality: leader"]
    }
  ]
}
```

---

## 10. How to run the project

**Step 1 — Make sure Python is installed**
```bash
python --version
# Should show Python 3.10 or higher
```

**Step 2 — Go into the project folder**
```bash
cd career_guidance
```

**Step 3 — Install Flask**
```bash
pip install -r requirements.txt
```

**Step 4 — Start the server**
```bash
python app.py
```

You will see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**Step 5 — Open the app**

Open your browser and go to:
```
http://localhost:5000
```

**Step 6 — Use the form**
1. Click your interests
2. Select your grade level for each subject
3. Click your skills
4. Click your personality traits
5. Click "Analyse my profile"
6. See your career matches with scores and explanations

---

## 11. How to add a new career rule

Open `knowledge_base.py` and add a new dictionary to the `RULES` list.

Example — adding "Game Developer":

```python
{
    "id": "R16",
    "career": "Game Developer",
    "conditions": {
        "interests": ["coding", "arts"],
        "marks":     {"math": "high"},
        "skills":    ["creativity"],
    },
    "explanation": "Game development combines coding, visual creativity, and strong math — all areas you excel in.",
    "base_score": 86,
},
```

Then open `main.js` and add the emoji for it:
```javascript
"Game Developer": "🎮",
```

That's it. No other file needs to change. The inference engine automatically picks up new rules on the next server restart.

---

*CareerIQ — Built with Python Flask and a Forward Chaining Expert System*
