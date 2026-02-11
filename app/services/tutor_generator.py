import os
import logging
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


async def generate_tutor_response(message: str, context: dict, style: str) -> str:
    """
    Generates a contextual response from the AI Tutor based on the user's current learning state.
    """
    style_instructions = {
        "simple": "Explain simply, like I am a beginner. Avoid complex jargon. Use analogies.",
        "example": "Focus on providing concrete examples, code snippets, or practical scenarios to illustrate the point.",
        "advanced": "Provide a technical deep dive. Discuss memory implications, performance, or edge cases. Assume I know the basics.",
    }
    system_prompt = f"\n    You are an AI Tutor for a personalized learning platform called SkillForge.\n    Your goal is to help the user master the topic: {context.get('topic', 'General')}.\n    \n    Current Context:\n    - Active Module: {context.get('module_title', 'Unknown')}\n    - User Level: {context.get('user_level', 'Beginner')}\n    - Known Weaknesses: {', '.join(context.get('weaknesses', []))}\n    - Recent Quiz Performance: {context.get('quiz_performance', 'N/A')}\n    \n    Response Style: {style.upper()}\n    {style_instructions.get(style, '')}\n    \n    The user is currently looking at this content:\n    "
    module_content = context.get("module_content", "")
    excerpt = (
        module_content[:2000] + "..." if len(module_content) > 2000 else module_content
    )
    prompt_messages = [
        {
            "role": "system",
            "content": system_prompt
            + """
"""
            + excerpt,
        },
        {"role": "user", "content": message},
    ]
    try:
        response = await client.chat.completions.create(
            model=MODEL, messages=prompt_messages, temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.exception(f"Error generating tutor response: {e}")
        return "I'm having trouble connecting to my knowledge base right now. Please try again in a moment."