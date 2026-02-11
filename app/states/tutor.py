import reflex as rx
from typing import TypedDict
from app.services.tutor_generator import generate_tutor_response
from app.states.i18n import I18nState
import asyncio


class ChatMessage(TypedDict):
    role: str
    content: str


class TutorState(rx.State):
    is_open: bool = False
    messages: list[ChatMessage] = [
        {
            "role": "assistant",
            "content": "Hi! I'm your AI Tutor. I see what you're working on. How can I help you understand this better?",
        }
    ]
    current_input: str = ""
    is_loading: bool = False
    explanation_style: str = "simple"

    @rx.event
    def toggle_tutor(self):
        self.is_open = not self.is_open

    @rx.event
    def set_input(self, value: str):
        self.current_input = value

    @rx.event
    def set_style(self, style: str):
        self.explanation_style = style

    @rx.event
    def clear_chat(self):
        self.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared. What else can I help you with?",
            }
        ]

    @rx.event
    async def send_message(self, form_data: dict[str, str]):
        user_msg = form_data.get("message", "").strip()
        if not user_msg:
            return
        self.messages.append({"role": "user", "content": user_msg})
        self.current_input = ""
        self.is_loading = True
        yield
        from app.states.courses import CourseState
        from app.states.lab import LabState
        from app.states.diagnostic import DiagnosticState

        course_state = await self.get_state(CourseState)
        lab_state = await self.get_state(LabState)
        diag_state = await self.get_state(DiagnosticState)
        i18n = await self.get_state(I18nState)
        context = {
            "topic": course_state.course_topic,
            "module_title": lab_state.current_module["title"],
            "module_content": lab_state.current_module["content"],
            "user_level": diag_state.proficiency_level,
            "weaknesses": diag_state.weaknesses,
            "quiz_performance": f"Correct: {lab_state.quiz_performance['correct']}, Total: {lab_state.quiz_performance['total']}",
        }
        response_text = await generate_tutor_response(
            user_msg, context, self.explanation_style, i18n.current_language
        )
        self.messages.append({"role": "assistant", "content": response_text})
        self.is_loading = False