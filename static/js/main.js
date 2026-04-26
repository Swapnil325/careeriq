// main.js — CareerIQ wizard logic

// ── State ─────────────────────────────────────────────────────
let currentStep = 1;
const TOTAL_STEPS = 4;

const CAREER_EMOJI = {
  "Software Engineer":           "💻",
  "Data Scientist":              "📊",
  "Doctor / Physician":          "🩺",
  "Biomedical Researcher":       "🔬",
  "Business Analyst":            "📈",
  "Entrepreneur":                "🚀",
  "Graphic Designer":            "🎨",
  "UX / UI Designer":            "🖥️",
  "Journalist / Content Writer": "✍️",
  "Civil Engineer":              "🏗️",
  "Psychologist / Counselor":    "🧠",
  "Teacher / Educator":          "📚",
  "Cybersecurity Analyst":       "🔐",
  "Marketing Manager":           "📣",
  "Environmental Scientist":     "🌿",
};

// ── DOM helpers ───────────────────────────────────────────────
const $ = id => document.getElementById(id);

function showPanel(id) {
  document.querySelectorAll(".step-panel").forEach(p => p.classList.remove("active"));
  $(id).classList.add("active");
}

function setNavStep(step) {
  document.querySelectorAll(".wnav-step").forEach(el => {
    const s = parseInt(el.dataset.step);
    el.classList.remove("active", "done");
    if (s === step) el.classList.add("active");
    if (s < step)  el.classList.add("done");
  });
  $("stepLabel").textContent = step <= TOTAL_STEPS
    ? `Step ${step} of ${TOTAL_STEPS}`
    : "Results";

  const pct = step <= TOTAL_STEPS ? (step / TOTAL_STEPS) * 100 : 100;
  $("progressFill").style.width = pct + "%";
}

// ── Opt-card toggle ───────────────────────────────────────────
document.querySelectorAll(".opt-card").forEach(card => {
  card.addEventListener("click", () => {
    card.classList.toggle("on");
    updateSummary();
  });
});

// ── Radio change → update summary ────────────────────────────
document.querySelectorAll(".scale-opt input").forEach(r => {
  r.addEventListener("change", updateSummary);
});

// ── Collect helpers ───────────────────────────────────────────
function getSelected(containerId) {
  return [...document.querySelectorAll(`#${containerId} .opt-card.on`)]
    .map(c => c.dataset.value);
}

function getMarks() {
  const marks = {};
  ["math", "science", "english"].forEach(s => {
    const r = document.querySelector(`input[name="${s}"]:checked`);
    if (r) marks[s] = r.value;
  });
  return marks;
}

function collect() {
  return {
    interests:   getSelected("interestChips"),
    marks:       getMarks(),
    skills:      getSelected("skillChips"),
    personality: getSelected("personalityChips"),
  };
}

// ── Live summary sidebar ──────────────────────────────────────
function updateSummary() {
  const interests   = getSelected("interestChips");
  const skills      = getSelected("skillChips");
  const personality = getSelected("personalityChips");
  const marks       = getMarks();

  $("sum-interests").querySelector(".sum-val").textContent =
    interests.length ? interests.join(", ") : "—";

  const markStr = Object.entries(marks).map(([k, v]) => `${k}: ${v}`).join(", ");
  $("sum-grades").querySelector(".sum-val").textContent = markStr || "—";

  $("sum-skills").querySelector(".sum-val").textContent =
    skills.length ? skills.join(", ") : "—";

  $("sum-personality").querySelector(".sum-val").textContent =
    personality.length ? personality.join(", ") : "—";
}

// ── Validation ────────────────────────────────────────────────
function validate(step) {
  const errEl = $(`err${step}`);
  errEl.classList.add("hidden");

  if (step === 1 && getSelected("interestChips").length === 0) {
    errEl.classList.remove("hidden"); return false;
  }
  if (step === 2 && Object.keys(getMarks()).length === 0) {
    errEl.classList.remove("hidden"); return false;
  }
  if (step === 3 && getSelected("skillChips").length === 0) {
    errEl.classList.remove("hidden"); return false;
  }
  if (step === 4 && getSelected("personalityChips").length === 0) {
    errEl.classList.remove("hidden"); return false;
  }
  return true;
}

// ── Navigation ────────────────────────────────────────────────
function goNext(step) {
  if (!validate(step)) return;
  currentStep = step + 1;
  showPanel(`panel${currentStep}`);
  setNavStep(currentStep);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function goBack(step) {
  currentStep = step - 1;
  showPanel(`panel${currentStep}`);
  setNavStep(currentStep);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ── Score tier ────────────────────────────────────────────────
function scoreTier(n) {
  if (n >= 85) return "s-high";
  if (n >= 75) return "s-mid";
  return "s-low";
}

// ── Confetti ──────────────────────────────────────────────────
function launchConfetti() {
  const colors = ["#4f46e5", "#16a34a", "#f59e0b", "#ec4899", "#06b6d4"];
  for (let i = 0; i < 60; i++) {
    const el = document.createElement("div");
    el.className = "confetti-piece";
    el.style.cssText = `left:${Math.random()*100}vw;background:${colors[i%colors.length]};animation-duration:${0.8+Math.random()*1.2}s;animation-delay:${Math.random()*0.5}s;transform:rotate(${Math.random()*360}deg)`;
    document.body.appendChild(el);
    el.addEventListener("animationend", () => el.remove());
  }
}

// ── Build one result row ──────────────────────────────────────
function buildRow(item, rank) {
  const emoji = CAREER_EMOJI[item.career] || "🎯";
  const tier  = scoreTier(item.confidence);
  const delay = (rank - 1) * 0.05;
  const tags  = item.matched_on
    .map(m => `<span class="rr-tag">${m}</span>`)
    .join("");

  return `
  <div class="result-row" style="animation-delay:${delay}s">
    <div class="rr-rank ${rank <= 3 ? "top" : ""}">${rank}</div>
    <div class="rr-body">
      <div class="rr-title">${emoji} ${item.career}</div>
      <p class="rr-why">${item.explanation}</p>
      <div class="score-bar-wrap"><div class="score-bar-fill ${tier}" style="width:0" data-target="${item.confidence}"></div></div>
      <div class="rr-tags" style="margin-top:0.6rem">${tags}</div>
    </div>
    <div class="rr-score">
      <div class="score-circle ${tier}">
        <span class="sc-num">${item.confidence}%</span>
        <span class="sc-lbl">match</span>
      </div>
    </div>
  </div>`;
}

// ── Submit ────────────────────────────────────────────────────
async function submitForm() {
  if (!validate(4)) return;

  $("loaderScreen").classList.remove("hidden");

  try {
    const res  = await fetch("/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(collect()),
    });
    const data = await res.json();
    $("loaderScreen").classList.add("hidden");

    if (data.status === "error") {
      alert(data.message);
      return;
    }

    if (!data.total_matches) {
      showPanel("panelNoResults");
      setNavStep(5);
      return;
    }

    // Populate results
    $("resultsSubtitle").textContent =
      `${data.total_matches} career${data.total_matches > 1 ? "s" : ""} matched your profile, ranked by confidence.`;

    $("resultsGrid").innerHTML = data.careers
      .map((c, i) => buildRow(c, i + 1))
      .join("");

    requestAnimationFrame(() => {
      document.querySelectorAll(".score-bar-fill").forEach(bar => {
        bar.style.width = bar.dataset.target + "%";
      });
    });

    launchConfetti();
    showPanel("panelResults");
    setNavStep(5);
    window.scrollTo({ top: 0, behavior: "smooth" });

  } catch {
    $("loaderScreen").classList.add("hidden");
    alert("Cannot reach the server. Make sure Flask is running on port 5000.");
  }
}

// ── Reset ─────────────────────────────────────────────────────
function resetWizard() {
  document.querySelectorAll(".opt-card.on").forEach(c => c.classList.remove("on"));
  document.querySelectorAll("input[type=radio]").forEach(r => r.checked = false);
  document.querySelectorAll(".panel-error").forEach(e => e.classList.add("hidden"));
  updateSummary();
  currentStep = 1;
  showPanel("panel1");
  setNavStep(1);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

$("resetBtn").addEventListener("click",  resetWizard);
$("resetBtn2").addEventListener("click", resetWizard);
