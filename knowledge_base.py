# ============================================================
# knowledge_base.py
# Contains all IF-THEN rules for the career expert system.
# Each rule has: conditions, career output, explanation, and weight (confidence).
# ============================================================

RULES = [
    # ── Rule 1 ──────────────────────────────────────────────
    {
        "id": "R01",
        "career": "Software Engineer",
        "conditions": {
            "interests": ["coding"],
            "marks": {"math": "high"},
        },
        "explanation": "Strong math skills combined with a coding interest are the core foundation of software engineering.",
        "base_score": 90,
    },
    # ── Rule 2 ──────────────────────────────────────────────
    {
        "id": "R02",
        "career": "Data Scientist",
        "conditions": {
            "interests": ["coding"],
            "marks": {"math": "high", "science": "high"},
            "skills": ["analytical"],
        },
        "explanation": "Data science demands high math & science marks plus strong analytical thinking and coding interest.",
        "base_score": 92,
    },
    # ── Rule 3 ──────────────────────────────────────────────
    {
        "id": "R03",
        "career": "Doctor / Physician",
        "conditions": {
            "interests": ["biology"],
            "marks": {"science": "high"},
        },
        "explanation": "A biology interest paired with high science marks is the classic pathway into medicine.",
        "base_score": 88,
    },
    # ── Rule 4 ──────────────────────────────────────────────
    {
        "id": "R04",
        "career": "Biomedical Researcher",
        "conditions": {
            "interests": ["biology"],
            "marks": {"science": "high", "math": "high"},
            "skills": ["analytical"],
        },
        "explanation": "Biomedical research requires deep science knowledge, strong math, and analytical problem-solving.",
        "base_score": 85,
    },
    # ── Rule 5 ──────────────────────────────────────────────
    {
        "id": "R05",
        "career": "Business Analyst",
        "conditions": {
            "interests": ["business"],
            "skills": ["analytical", "communication"],
        },
        "explanation": "Business analysis blends analytical thinking with communication — exactly your skill set.",
        "base_score": 83,
    },
    # ── Rule 6 ──────────────────────────────────────────────
    {
        "id": "R06",
        "career": "Entrepreneur",
        "conditions": {
            "interests": ["business"],
            "skills": ["creativity", "communication"],
            "personality": ["risk-taker", "leader"],
        },
        "explanation": "Entrepreneurship thrives on creativity, communication, and a risk-taking leadership personality.",
        "base_score": 80,
    },
    # ── Rule 7 ──────────────────────────────────────────────
    {
        "id": "R07",
        "career": "Graphic Designer",
        "conditions": {
            "interests": ["arts"],
            "skills": ["creativity"],
        },
        "explanation": "A creative skill set combined with an arts interest is the perfect match for graphic design.",
        "base_score": 82,
    },
    # ── Rule 8 ──────────────────────────────────────────────
    {
        "id": "R08",
        "career": "UX / UI Designer",
        "conditions": {
            "interests": ["arts", "coding"],
            "skills": ["creativity", "analytical"],
        },
        "explanation": "UX/UI design sits at the intersection of art and technology — matching your mixed interests and skills.",
        "base_score": 87,
    },
    # ── Rule 9 ──────────────────────────────────────────────
    {
        "id": "R09",
        "career": "Journalist / Content Writer",
        "conditions": {
            "interests": ["arts"],
            "marks": {"english": "high"},
            "skills": ["communication", "creativity"],
        },
        "explanation": "High English marks with creativity and communication skills are the hallmarks of a great writer.",
        "base_score": 81,
    },
    # ── Rule 10 ─────────────────────────────────────────────
    {
        "id": "R10",
        "career": "Civil Engineer",
        "conditions": {
            "interests": ["engineering"],
            "marks": {"math": "high", "science": "high"},
        },
        "explanation": "Civil engineering demands high math and science marks alongside an engineering interest.",
        "base_score": 86,
    },
    # ── Rule 11 ─────────────────────────────────────────────
    {
        "id": "R11",
        "career": "Psychologist / Counselor",
        "conditions": {
            "interests": ["social"],
            "skills": ["communication"],
            "personality": ["empathetic", "patient"],
        },
        "explanation": "Psychology requires empathy, patience, and strong communication — all traits you possess.",
        "base_score": 84,
    },
    # ── Rule 12 ─────────────────────────────────────────────
    {
        "id": "R12",
        "career": "Teacher / Educator",
        "conditions": {
            "interests": ["social"],
            "skills": ["communication"],
            "personality": ["patient", "leader"],
        },
        "explanation": "Teaching is ideal for patient, communicative leaders who enjoy social interaction.",
        "base_score": 79,
    },
    # ── Rule 13 ─────────────────────────────────────────────
    {
        "id": "R13",
        "career": "Cybersecurity Analyst",
        "conditions": {
            "interests": ["coding"],
            "skills": ["analytical"],
            "personality": ["detail-oriented"],
        },
        "explanation": "Cybersecurity needs coding interest, sharp analytical skills, and a detail-oriented mindset.",
        "base_score": 88,
    },
    # ── Rule 14 ─────────────────────────────────────────────
    {
        "id": "R14",
        "career": "Marketing Manager",
        "conditions": {
            "interests": ["business", "arts"],
            "skills": ["creativity", "communication"],
        },
        "explanation": "Marketing blends business sense with creative communication — a perfect fit for your profile.",
        "base_score": 80,
    },
    # ── Rule 15 ─────────────────────────────────────────────
    {
        "id": "R15",
        "career": "Environmental Scientist",
        "conditions": {
            "interests": ["biology", "engineering"],
            "marks": {"science": "high"},
            "skills": ["analytical"],
        },
        "explanation": "Environmental science suits those who combine biology/engineering interests with science strength.",
        "base_score": 83,
    },
]
