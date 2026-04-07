from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask, render_template, request, jsonify
from agents import GeneratorAgent, ReviewerAgent

app = Flask(__name__)

generator = GeneratorAgent()
reviewer = ReviewerAgent()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-pipeline", methods=["POST"])
def run_pipeline():
    data = request.json
    grade = int(data.get("grade", 4))
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    generated = generator.run({"grade": grade, "topic": topic})
    review = reviewer.run(generated)
    refined = None

    if review.get("status") == "fail":
        feedback_text = "; ".join(review.get("feedback", []))
        refined = generator.run({
            "grade": grade,
            "topic": topic,
            "feedback": feedback_text
        })

    return jsonify({
        "generated": generated,
        "review": review,
        "refined": refined
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )