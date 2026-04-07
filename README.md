# Eklavya AI — Educational Content Generator

An AI-powered agent pipeline that generates and reviews educational content for school students.

## Features
- Generator Agent — Creates grade-appropriate explanations and MCQs
- Reviewer Agent — Evaluates content for accuracy and clarity
- Auto-refinement — Regenerates content if review fails

## Tech Stack
- Python, Flask
- Groq LLaMA 3.3 70B
- HTML, CSS, JavaScript

## How to Run

1. Clone the repo
2. Install dependencies:
   pip install -r requirements.txt
3. Add your Groq API key in .env:
   GROQ_API_KEY=your_key_here
4. Run the app:
   python app.py
5. Open browser:
   http://127.0.0.1:5000
