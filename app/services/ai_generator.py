import os
import json
import logging
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


def _extract_json_from_text(text: str) -> str:
    """
    Extract JSON content from LLM responses by finding the outermost bounds.
    With JSON mode enabled, this usually returns the text as-is if valid.
    """
    cleaned = text.strip()
    start_idx = cleaned.find("{")
    end_idx = cleaned.rfind("}")
    if start_idx == -1:
        start_idx = cleaned.find("[")
        end_idx = cleaned.rfind("]")
    if start_idx != -1 and end_idx != -1 and (end_idx > start_idx):
        return cleaned[start_idx : end_idx + 1]
    return cleaned


async def generate_course_curriculum(topic: str, skill_level: str) -> list[dict]:
    """
    Generates a list of course modules based on the topic and skill level.
    Returns a list of dictionaries with keys: id, title, description, status, progress.
    """
    prompt = f"\n    Create a structured course curriculum for learning '{topic}' at a '{skill_level}' level.\n    The response must be a JSON object with a key 'modules' containing an array of exactly 6 module objects.\n    The first module should be 'completed' with 100% progress.\n    The second module should be 'active' with 0% progress.\n    The rest should be 'locked' with 0% progress.\n\n    Each module object must have:\n    - id: string (m1, m2, etc)\n    - title: string\n    - description: string (short, 1-2 sentences)\n    - status: string ('completed', 'active', or 'locked')\n    - progress: integer (0-100)\n    "
    raw_content = ""
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert curriculum designer. You always output valid JSON objects.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        raw_content = response.choices[0].message.content
        cleaned_json = _extract_json_from_text(raw_content)
        data = json.loads(cleaned_json)
        return data.get("modules", [])
    except Exception as e:
        logging.exception(f"Error generating curriculum. Raw content: {raw_content}")
        return [
            {
                "id": "m1",
                "title": "Introduction",
                "description": "Basics of the topic.",
                "status": "completed",
                "progress": 100,
            },
            {
                "id": "m2",
                "title": "Core Concepts",
                "description": "Fundamental principles.",
                "status": "active",
                "progress": 0,
            },
            {
                "id": "m3",
                "title": "Advanced Topics",
                "description": "Deep dive into details.",
                "status": "locked",
                "progress": 0,
            },
        ]


async def generate_module_content(topic: str, module_title: str) -> dict:
    """
    Generates detailed content for a specific module, including:
    - Educational content (markdown)
    - 10 Practice Exercises
    - 10 Flashcards
    - 10 Quiz Questions

    Returns a dictionary with:
    - content: string (Detailed Markdown content with headings, examples, and deep explanation)
    - exercises: array of exactly 10 objects [{"id": "e1", "prompt": "Task description", "expected_answer": "answer_code_or_text"}]
    - flashcards: array of exactly 10 objects [{"id": "f1", "front": "Term/Concept", "back": "Definition/Translation"}]
    - quiz_questions: array of exactly 10 objects [{"id": "q1", "question": "Question text", "difficulty": "easy/medium/hard", "explanation": "Brief explanation of the correct answer", "options": [{"id": "a", "text": "Option text"}], "correct_id": "a"}]
    """
    prompt = f"Generate detailed educational content and interactive activities for the module '{module_title}' within the topic '{topic}'. The response must be a JSON object with keys: 'content', 'exercises', 'flashcards', and 'quiz_questions'."
    raw_content = ""
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert tutor. You always output valid JSON objects.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        raw_content = response.choices[0].message.content
        cleaned_json = _extract_json_from_text(raw_content)
        module_data = json.loads(cleaned_json)
        return module_data
    except Exception as e:
        logging.exception(
            f"Error generating module content. Raw content: {raw_content}"
        )
        return {
            "content": f"### {module_title}\n\nError generating content for this module.",
            "exercises": [
                {
                    "id": f"e{i}",
                    "prompt": "Error loading exercise",
                    "expected_answer": "error",
                }
                for i in range(10)
            ],
            "flashcards": [
                {"id": f"f{i}", "front": "Error", "back": "Error loading data"}
                for i in range(10)
            ],
            "quiz_questions": [
                {
                    "id": f"q{i}",
                    "question": "Error loading quiz question",
                    "difficulty": "medium",
                    "explanation": "System error occurred.",
                    "options": [{"id": "a", "text": "Retry"}],
                    "correct_id": "a",
                }
                for i in range(10)
            ],
        }