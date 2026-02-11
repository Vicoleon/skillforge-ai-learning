import os
import json
import logging
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


def _extract_json_from_text(text: str) -> str:
    """
    Extract JSON content from LLM responses by finding the outermost bounds.
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


def _get_lang_name(code: str) -> str:
    mapping = {"en": "English", "es": "Spanish (Español)"}
    return mapping.get(code, "English")


async def generate_diagnostic_questions(topic: str, language: str = "en") -> list[dict]:
    """
    Generates 8 diagnostic questions covering different subtopics for the given main topic.
    """
    lang_name = _get_lang_name(language)
    prompt = f"\n    Create a diagnostic assessment for the topic '{topic}'.\n    Generate all content in {lang_name}. The questions, options, and explanations must be in {lang_name}.\n    Generate exactly 8 multiple-choice questions that test different sub-skills or concepts within this topic.\n    The questions should range from basic to intermediate difficulty to assess the user's current level.\n    \n    Return a JSON object with a key 'questions' containing an array of question objects.\n    Each question object must have:\n    - id: string (q1, q2, ...)\n    - question: string (The question text)\n    - subtopic: string (The specific concept being tested, e.g., 'Memory Management', 'Syntax', 'Networking')\n    - difficulty: string ('easy', 'medium', 'hard')\n    - options: array of objects [{{'id': 'a', 'text': 'Option A'}}, {{'id': 'b', 'text': 'Option B'}}, ...]\n    - correct_id: string (The id of the correct option)\n    - explanation: string (Brief explanation of why the answer is correct)\n    "
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert evaluator. You always output valid JSON objects.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        raw_content = response.choices[0].message.content
        cleaned_json = _extract_json_from_text(raw_content)
        data = json.loads(cleaned_json)
        return data.get("questions", [])
    except Exception as e:
        logging.exception(f"Error generating diagnostic questions: {e}")
        return [
            {
                "id": "q1",
                "question": "What is the primary function of this topic?",
                "subtopic": "Basics",
                "difficulty": "easy",
                "options": [
                    {"id": "a", "text": "Function A"},
                    {"id": "b", "text": "Function B"},
                    {"id": "c", "text": "Function C"},
                    {"id": "d", "text": "Function D"},
                ],
                "correct_id": "a",
                "explanation": "This is the fundamental concept.",
            }
        ]


async def analyze_diagnostic_results(
    questions: list[dict], answers: list[dict], language: str = "en"
) -> dict:
    """
    Analyzes the user's answers to identify strengths, weaknesses, and recommended focus areas.
    """
    lang_name = _get_lang_name(language)
    analysis_input = {
        "questions": [
            {"id": q["id"], "subtopic": q["subtopic"], "difficulty": q["difficulty"]}
            for q in questions
        ],
        "user_answers": answers,
    }
    prompt = f"\n    Analyze these diagnostic test results provided in JSON format: {json.dumps(analysis_input)}.\n    Generate all content in {lang_name}. The strengths, weaknesses, and recommended focus must be in {lang_name}.\n    \n    Identify the user's proficiency level based on the difficulty of questions answered correctly vs incorrectly.\n    Group the performance by subtopics.\n    \n    Return a JSON object with:\n    - overall_score: integer (0-100)\n    - proficiency_level: string (Beginner, Intermediate, Advanced)\n    - strengths: list of strings (Subtopics or concepts the user knows well)\n    - weaknesses: list of strings (Subtopics or concepts the user needs to focus on)\n    - recommended_focus: string (A sentence describing what the personalized course should focus on)\n    "
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert curriculum advisor. You always output valid JSON objects.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        raw_content = response.choices[0].message.content
        cleaned_json = _extract_json_from_text(raw_content)
        return json.loads(cleaned_json)
    except Exception as e:
        logging.exception(f"Error analyzing diagnostic results: {e}")
        return {
            "overall_score": 0,
            "proficiency_level": "Beginner",
            "strengths": [],
            "weaknesses": ["General Knowledge"],
            "recommended_focus": "Start from the basics.",
        }


async def generate_adaptive_curriculum(
    topic: str, analysis_results: dict, language: str = "en"
) -> list[dict]:
    """
    Generates a personalized curriculum based on diagnostic analysis.
    """
    lang_name = _get_lang_name(language)
    strengths = ", ".join(analysis_results.get("strengths", []))
    weaknesses = ", ".join(analysis_results.get("weaknesses", []))
    focus = analysis_results.get("recommended_focus", "General mastery")
    level = analysis_results.get("proficiency_level", "Beginner")
    prompt = f"\n    Create a structured course curriculum for learning '{topic}'.\n    Generate all content in {lang_name}. The module titles and descriptions must be in {lang_name}.\n    The user has taken a diagnostic test. \n    Their Level: {level}\n    Strengths (Skip deep basics for these): {strengths}\n    Weaknesses (Focus heavily on these): {weaknesses}\n    Recommendation: {focus}\n    \n    The response must be a JSON object with a key 'modules' containing an array of exactly 6 module objects.\n    The curriculum should adapt to fill the gaps in their knowledge (weaknesses) while acknowledging what they already know (strengths).\n    \n    Each module object must have:\n    - id: string (m1, m2, etc)\n    - title: string\n    - description: string (short, 1-2 sentences)\n    - status: string ('completed', 'active', or 'locked')\n    - progress: integer (0-100)\n    \n    Set the first module to 'active' with 0% progress unless they are absolute beginners, in which case the first module might be introductory.\n    "
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
        logging.exception(f"Error generating adaptive curriculum: {e}")
        return []