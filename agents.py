import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


class GeneratorAgent:
    def run(self, input_data):
        grade = input_data.get("grade", 4)
        topic = input_data.get("topic", "")
        feedback = input_data.get("feedback", None)

        feedback_section = ""
        if feedback:
            feedback_section = "IMPORTANT — Previous version failed review. Fix these issues: " + feedback

        prompt = """You are an educational content generator for school students.

Generate content for:
- Grade: """ + str(grade) + """
- Topic: """ + topic + """
""" + feedback_section + """

Rules:
1. Language must suit Grade """ + str(grade) + """ students
2. Explanation must be simple and accurate
3. Include exactly 3 MCQs with options A, B, C, D
4. Answer must be A, B, C, or D

Return ONLY valid JSON, no extra text, no markdown:
{
  "explanation": "...",
  "mcqs": [
    {
      "question": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "answer": "A"
    }
  ]
}"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1500,
        )
        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)


class ReviewerAgent:
    def run(self, content):
        prompt = """You are a strict educational content reviewer.

Review this content and evaluate:
1. Age appropriateness of language
2. Conceptual correctness
3. Clarity for the target grade

Content:
""" + json.dumps(content, indent=2) + """

Return ONLY valid JSON, no extra text, no markdown:
{
  "status": "pass",
  "feedback": []
}

If status is fail, list specific issues in feedback array.
If status is pass, feedback can be empty."""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600,
        )
        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)