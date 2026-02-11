import reflex as rx
from typing import Optional
from app.services.ai_generator import generate_course_curriculum
import logging


class OnboardingState(rx.State):
    search_query: str = ""
    is_diagnostic_shown: bool = False
    skill_level: str = ""
    is_processing: bool = False

    @rx.event
    def handle_search_change(self, value: str):
        self.search_query = value

    @rx.event
    async def submit_topic(self, form_data: dict[str, str]):
        query = form_data.get("search_query", "")
        self.search_query = query
        if not query.strip():
            yield rx.toast("Please enter a topic to start learning")
            return
        self.is_processing = True
        yield
        import asyncio

        await asyncio.sleep(1)
        self.is_processing = False
        self.is_diagnostic_shown = True

    @rx.event
    async def select_skill(self, level: str):
        self.skill_level = level
        self.is_processing = True
        yield rx.toast(
            f"Level set to {level}. Starting diagnostic assessment...", duration=3000
        )
        from app.states.navigation import NavState
        from app.states.diagnostic import DiagnosticState

        diagnostic = await self.get_state(DiagnosticState)
        yield DiagnosticState.start_diagnostic(self.search_query)
        nav = await self.get_state(NavState)
        nav.current_page = "diagnostic"
        self.is_processing = False
        self.is_diagnostic_shown = False
        self.search_query = ""
        self.skill_level = ""

    @rx.event
    def reset_flow(self):
        self.search_query = ""
        self.is_diagnostic_shown = False
        self.skill_level = ""
        self.is_processing = False