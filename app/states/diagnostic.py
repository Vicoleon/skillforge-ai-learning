import reflex as rx
from typing import TypedDict, Optional
from app.services.diagnostic_generator import (
    generate_diagnostic_questions,
    analyze_diagnostic_results,
    generate_adaptive_curriculum,
)
from app.states.i18n import I18nState
import logging


class DiagnosticOption(TypedDict):
    id: str
    text: str


class DiagnosticQuestion(TypedDict):
    id: str
    question: str
    subtopic: str
    difficulty: str
    options: list[DiagnosticOption]
    correct_id: str
    explanation: str


class UserAnswer(TypedDict):
    question_id: str
    selected_answer: str
    is_correct: bool


class DiagnosticState(rx.State):
    topic: str = ""
    target_level: str = "Beginner"
    questions: list[DiagnosticQuestion] = []
    current_question_index: int = 0
    user_answers: list[UserAnswer] = []
    is_loading: bool = False
    is_complete: bool = False
    overall_score: int = 0
    proficiency_level: str = ""
    strengths: list[str] = []
    weaknesses: list[str] = []
    recommended_focus: str = ""

    @rx.var
    def current_question(self) -> DiagnosticQuestion:
        if not self.questions or self.current_question_index >= len(self.questions):
            return {
                "id": "",
                "question": "Loading...",
                "subtopic": "",
                "difficulty": "",
                "options": [],
                "correct_id": "",
                "explanation": "",
            }
        return self.questions[self.current_question_index]

    @rx.var
    def progress(self) -> int:
        if not self.questions:
            return 0
        return int(self.current_question_index / len(self.questions) * 100)

    @rx.var
    def total_questions(self) -> int:
        return len(self.questions)

    @rx.event
    async def start_diagnostic(self, topic: str, language: str = "en"):
        self.topic = topic
        self.is_loading = True
        self.questions = []
        self.user_answers = []
        self.current_question_index = 0
        self.is_complete = False
        yield
        try:
            self.questions = await generate_diagnostic_questions(topic, language)
        except Exception as e:
            logging.exception("Failed to start diagnostic")
            yield rx.toast("Error generating diagnostic questions.")
        finally:
            self.is_loading = False

    @rx.event
    def answer_question(self, option_id: str):
        if not self.questions:
            return
        current_q = self.questions[self.current_question_index]
        is_correct = option_id == current_q["correct_id"]
        self.user_answers.append(
            {
                "question_id": current_q["id"],
                "selected_answer": option_id,
                "is_correct": is_correct,
            }
        )
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
        else:
            return DiagnosticState.complete_diagnostic

    @rx.event
    async def complete_diagnostic(self):
        self.is_loading = True
        yield
        try:
            i18n = await self.get_state(I18nState)
            results = await analyze_diagnostic_results(
                self.questions, self.user_answers, i18n.current_language
            )
            self.overall_score = results.get("overall_score", 0)
            self.proficiency_level = results.get("proficiency_level", "Beginner")
            self.strengths = results.get("strengths", [])
            self.weaknesses = results.get("weaknesses", [])
            self.recommended_focus = results.get(
                "recommended_focus", "Start learning basics."
            )
            self.is_complete = True
        except Exception as e:
            logging.exception("Error completing diagnostic")
            yield rx.toast("Error analyzing results.")
        finally:
            self.is_loading = False

    @rx.event
    async def generate_personalized_path(self):
        self.is_loading = True
        yield rx.toast("Designing your personalized curriculum...", duration=3000)
        try:
            analysis_data = {
                "overall_score": self.overall_score,
                "proficiency_level": self.proficiency_level,
                "strengths": self.strengths,
                "weaknesses": self.weaknesses,
                "recommended_focus": self.recommended_focus,
            }
            i18n = await self.get_state(I18nState)
            from app.states.courses import CourseState
            from app.states.navigation import NavState

            courses = await self.get_state(CourseState)
            courses.advance_to_next_level()
            modules = await generate_adaptive_curriculum(
                self.topic, analysis_data, i18n.current_language, courses.current_level
            )
            courses.course_topic = self.topic
            courses.course_title = f"{courses.current_level} {self.topic} Mastery"
            courses.course_description = self.recommended_focus
            if modules:
                courses.modules = modules
            nav = await self.get_state(NavState)
            nav.current_page = "courses"
        except Exception as e:
            logging.exception("Error generating path")
            yield rx.toast("Failed to generate curriculum.")
        finally:
            self.is_loading = False

    @rx.event
    async def start_level_up_diagnostic(
        self, topic: str, current_level: str, target_level: str, language: str = "en"
    ):
        self.topic = topic
        self.target_level = target_level
        self.is_loading = True
        self.questions = []
        self.user_answers = []
        self.current_question_index = 0
        self.is_complete = False
        yield
        try:
            self.questions = await generate_diagnostic_questions(
                topic, language, current_level, target_level
            )
        except Exception as e:
            logging.exception("Failed to start level up diagnostic")
            yield rx.toast("Error generating assessment.")
        finally:
            self.is_loading = False