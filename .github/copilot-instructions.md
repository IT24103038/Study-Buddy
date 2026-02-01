# GitHub Copilot Instructions
## Study Buddy

You are assisting in building a **Python-based desktop application** called  
**Study Buddy**, aimed mainly at university students, but can be used by anyone.

The code must prioritize:
- Clarity
- Simplicity
- Readability
- Maintainability

Avoid overengineering or advanced patterns unless explicitly requested.

---

## Project Overview

Study Buddy is an **AI-powered desktop app** that helps students with:
- Lesson summarization
- Dynamic question generation
- Basic study assistance
- Schedule management
- Note-taking & organization
- Flashcard creation
- Progress tracking

The application uses **PyQt6** for the UI and external **AI APIs** for intelligence.

## How the App Works

- Students can input lesson content like text from their lectures or files (e.g., PDFs, TXTs), and the app will generate summaries and practice questions to aid their study.
- The UI is modular, with separate views for summarization, question generation, and other features.

---

## Tech Stack

Use **only** the following unless told otherwise:

- Language: **Python 3**
- UI Framework: **PyQt6**
- Database: **SQLite (sqlite3)**
- AI Integration: API-based
- Architecture: Modular, file-based

DO NOT:
- Add unnecessary dependencies

---

## Project Structure (can change)

smart-student-helper/
│
├── main.py
│
├── ui/
│ ├── app.py
│ ├── sidebar.py
│ ├── summarizer_view.py
│ ├── question_view.py
│
├── ai/
│ ├── ai_client.py
│ ├── summarizer.py
│ ├── question_generator.py
│
├── data/
│ ├── database.py
│
├── utils/
│ └── helpers.py
│
├── assets/
│
└── requirements.txt

Rules:
- UI code goes ONLY in `ui/`
- AI logic goes ONLY in `ai/`
- Database logic goes ONLY in `data/`
- No AI calls inside UI files

---

## Coding Style Rules

- Use **simple functions**
- Prefer **clear variable names** over short ones
- Add **brief comments** explaining logic where necessary
- No lambda-heavy or one-liner tricks

Example (GOOD):
```python
def summarize_text(text):
    if not text:
        return "No text provided"

Example (BAD):
```python
summ = lambda x: api(x) if x else ""

---

## UI Guidelines (CustomTkinter)

- Use CTkFrame for layout
- Use pack() or grid() consistently
- Keep UI responsive but simple
- One screen = one file (view)

DO NOT:
- Hardcode AI keys
- Mix layout logic with AI logic
- Create massive UI files

---

## AI Integration Rules

All AI calls must go through ai/ai_client.py

Prompts must be:
- Explicit
- Student-friendly
- Subject-agnostic

Example prompt style:
Summarize the following lesson for a university student in simple language.
Use bullet points.

No prompt should exceed what is necessary.

---

## Error Handling

- Handle empty inputs gracefully
- Display user-friendly messages
- Avoid crashing the app

Bad:
raise Exception("Error")

Good:
return "Something went wrong. Please try again."

---

## Development Philosophy

Build feature by feature

- UI first, then logic
- Working simple version > incomplete complex version
- Test each module independently
- Integrate gradually

If unsure:
- Choose the simpler implementation

---

## When Generating Code
Always:
- Ask permission before adding new features or generating code
- Use comments to clarify purpose
- Explain what the code does (briefly)
- Keep functions small
- Assume beginner-level understanding
- Avoid skipping steps

## Final Rule
- If a solution feels “too clever” or “too complex”: It is probably wrong.
- Stick to simple, clean, understandable Python.