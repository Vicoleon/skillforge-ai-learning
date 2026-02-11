import reflex as rx
from reflex_google_auth import GoogleAuthState
from typing import Any
import json


class AuthState(GoogleAuthState):
    user_data_store: dict[str, dict[str, str | int | list | dict]] = {}

    @rx.var
    def is_authenticated(self) -> bool:
        return self.token_is_valid

    @rx.var
    def current_user_email(self) -> str:
        return self.tokeninfo.get("email", "")

    @rx.var
    def current_user_name(self) -> str:
        return self.tokeninfo.get("name", "Guest")

    @rx.var
    def current_user_picture(self) -> str:
        return self.tokeninfo.get("picture", "")

    @rx.event
    def on_success(self, id_token: dict):
        """Called when login is successful."""
        return AuthState.load_user_progress()

    @rx.event
    async def save_user_progress(self):
        if not self.is_authenticated:
            return
        from app.states.courses import CourseState
        from app.states.diagnostic import DiagnosticState
        from app.states.user_stats import UserStatsState
        from app.states.review import ReviewState
        from app.states.lab import LabState

        courses = await self.get_state(CourseState)
        diagnostic = await self.get_state(DiagnosticState)
        stats = await self.get_state(UserStatsState)
        review = await self.get_state(ReviewState)
        lab = await self.get_state(LabState)
        user_data = {
            "course_topic": courses.course_topic,
            "course_title": courses.course_title,
            "course_description": courses.course_description,
            "current_level": courses.current_level,
            "modules": courses.modules,
            "diagnostic_results": {
                "overall_score": diagnostic.overall_score,
                "proficiency_level": diagnostic.proficiency_level,
                "strengths": diagnostic.strengths,
                "weaknesses": diagnostic.weaknesses,
                "recommended_focus": diagnostic.recommended_focus,
            },
            "xp_total": stats.xp_total,
            "current_streak": stats.current_streak,
            "badges": stats.badges,
            "review_items": review.review_items,
            "current_module_id": lab.current_module_id,
        }
        self.user_data_store[self.current_user_email] = user_data
        yield rx.toast("Progress saved!", duration=2000)

    @rx.event
    async def load_user_progress(self):
        if not self.is_authenticated:
            return
        email = self.current_user_email
        if email not in self.user_data_store:
            return
        data = self.user_data_store[email]
        from app.states.courses import CourseState
        from app.states.diagnostic import DiagnosticState
        from app.states.user_stats import UserStatsState
        from app.states.review import ReviewState
        from app.states.lab import LabState
        from app.states.navigation import NavState

        courses = await self.get_state(CourseState)
        diagnostic = await self.get_state(DiagnosticState)
        stats = await self.get_state(UserStatsState)
        review = await self.get_state(ReviewState)
        lab = await self.get_state(LabState)
        nav = await self.get_state(NavState)
        courses.course_topic = data.get("course_topic", "")
        courses.course_title = data.get(
            "course_title", "Introduction to Systems Programming"
        )
        courses.course_description = data.get(
            "course_description", "Master the fundamentals..."
        )
        courses.current_level = data.get("current_level", "Beginner")
        courses.modules = data.get("modules", courses.modules)
        diag_data = data.get("diagnostic_results", {})
        diagnostic.overall_score = diag_data.get("overall_score", 0)
        diagnostic.proficiency_level = diag_data.get("proficiency_level", "")
        diagnostic.strengths = diag_data.get("strengths", [])
        diagnostic.weaknesses = diag_data.get("weaknesses", [])
        diagnostic.recommended_focus = diag_data.get("recommended_focus", "")
        stats.xp_total = data.get("xp_total", 1250)
        stats.current_streak = data.get("current_streak", 4)
        stats.badges = data.get("badges", stats.badges)
        review.review_items = data.get("review_items", [])
        lab.current_module_id = data.get("current_module_id", "")
        if courses.course_topic:
            nav.current_page = "courses"
        yield rx.toast(f"Welcome back, {AuthState.current_user_name}! Progress loaded.")