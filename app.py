# ============================================================
# app.py  –  Flask REST API
# ============================================================

from flask import Flask, request, jsonify, render_template
from inference_engine import run_inference

app = Flask(__name__)


# ── Serve the frontend ──────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── POST /predict ───────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts JSON:
    {
        "interests":   ["coding", "business"],
        "marks":       {"math": "high", "science": "medium", "english": "low"},
        "skills":      ["analytical", "communication"],
        "personality": ["detail-oriented", "leader"]
    }

    Returns JSON:
    {
        "status": "success",
        "total_matches": 3,
        "careers": [
            {
                "career":      "Software Engineer",
                "confidence":  90.0,
                "explanation": "...",
                "rule_id":     "R01",
                "matched_on":  ["interests: coding", "marks: math=high"]
            },
            ...
        ]
    }
    """
    data = request.get_json(silent=True)

    # ── Basic validation ─────────────────────────────────────
    if not data:
        return jsonify({"status": "error", "message": "No JSON body received."}), 400

    required_fields = ["interests", "marks", "skills", "personality"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({
            "status":  "error",
            "message": f"Missing fields: {', '.join(missing)}"
        }), 400

    # ── Run inference engine ─────────────────────────────────
    careers = run_inference(data)

    if not careers:
        return jsonify({
            "status":        "success",
            "total_matches": 0,
            "message":       "No matching careers found. Try broadening your inputs.",
            "careers":       []
        })

    return jsonify({
        "status":        "success",
        "total_matches": len(careers),
        "careers":       careers
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
