import reflex as rx
from typing import TypedDict
from app.services.ai_generator import generate_module_content
from app.states.i18n import I18nState
import logging


class QuizOption(TypedDict):
    id: str
    text: str


class QuizQuestion(TypedDict):
    question: str
    options: list[QuizOption]
    correct_id: str
    difficulty: str
    explanation: str


class Exercise(TypedDict):
    id: str
    prompt: str
    expected_answer: str


class Flashcard(TypedDict):
    id: str
    front: str
    back: str


class ModuleData(TypedDict):
    id: str
    title: str
    content: str
    exercises: list[Exercise]
    flashcards: list[Flashcard]
    quiz_questions: list[QuizQuestion]


class LabState(rx.State):
    active_tab: str = "editor"
    topic_type: str = "programming"
    course_topic_stored: str = ""
    current_code: str = """def main():
    print("Hello, SkillForge!")

if __name__ == "__main__":
    main()"""
    terminal_output: list[str] = ["$ python main.py"]
    selected_quiz_answer: str = ""
    is_quiz_submitted: bool = False
    quiz_result: str = ""
    feedback_message: str = "Tip: Try defining a function to keep your code organized."
    feedback_type: str = "info"
    is_feedback_visible: bool = True
    current_module_id: str = ""
    is_loading: bool = False
    current_exercise_index: int = 0
    current_flashcard_index: int = 0
    current_quiz_index: int = 0
    is_flashcard_flipped: bool = False
    quiz_performance: dict[str, int | dict[str, int]] = {
        "correct": 0,
        "total": 0,
        "streak": 0,
        "incorrect_streak": 0,
        "by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
    }
    show_explanation: bool = False
    current_difficulty: str = "medium"
    should_review: bool = False
    current_module_data: ModuleData = {
        "id": "placeholder",
        "title": "Loading...",
        "content": "### Preparing your personalized lesson...",
        "exercises": [],
        "flashcards": [],
        "quiz_questions": [],
    }

    @rx.var
    def current_module(self) -> ModuleData:
        return self.current_module_data

    @rx.var
    def current_exercise(self) -> Exercise:
        if not self.current_module_data["exercises"]:
            return {"id": "none", "prompt": "No exercises", "expected_answer": ""}
        return self.current_module_data["exercises"][self.current_exercise_index]

    @rx.var
    def current_flashcard(self) -> Flashcard:
        if not self.current_module_data["flashcards"]:
            return {"id": "none", "front": "None", "back": "None"}
        return self.current_module_data["flashcards"][self.current_flashcard_index]

    @rx.var
    def current_quiz_question(self) -> QuizQuestion:
        if not self.current_module_data["quiz_questions"]:
            return {
                "question": "None",
                "options": [],
                "correct_id": "",
                "difficulty": "medium",
                "explanation": "",
            }
        return self.current_module_data["quiz_questions"][self.current_quiz_index]

    @rx.var
    def progress_percentage(self) -> int:
        return 50

    def _detect_topic_type(self, topic: str) -> str:
        t = topic.lower()
        languages = [
            "spanish",
            "french",
            "russian",
            "german",
            "japanese",
            "chinese",
            "italian",
            "language",
            "english",
        ]
        programming = [
            "python",
            "rust",
            "javascript",
            "coding",
            "programming",
            "c++",
            "java",
            "react",
            "sql",
            "html",
        ]
        for lang in languages:
            if lang in t:
                return "language"
        for prog in programming:
            if prog in t:
                return "programming"
        return "general"

    @rx.event
    async def load_module_content(self, topic: str, module_title: str, module_id: str):
        self.is_loading = True
        self.course_topic_stored = topic
        self.topic_type = self._detect_topic_type(topic)
        self.current_exercise_index = 0
        self.current_flashcard_index = 0
        self.current_quiz_index = 0
        self.is_flashcard_flipped = False
        yield
        try:
            i18n = await self.get_state(I18nState)
            generated_data = await generate_module_content(
                topic, module_title, i18n.current_language
            )
            self.current_module_data = {
                "id": module_id,
                "title": module_title,
                "content": generated_data["content"],
                "exercises": generated_data["exercises"],
                "flashcards": generated_data["flashcards"],
                "quiz_questions": generated_data["quiz_questions"],
            }
            self.current_code = ""
            if generated_data["exercises"]:
                self.current_code = generated_data["exercises"][0]["prompt"]
            self.active_tab = "practice" if self.topic_type == "language" else "editor"
            self.is_feedback_visible = False
            self.selected_quiz_answer = ""
            self.is_quiz_submitted = False
            self.quiz_result = ""
        except Exception as e:
            logging.exception("Unexpected error loading module")
            yield rx.toast("Failed to load module content. Please try again.")
        finally:
            self.is_loading = False
            yield

    @rx.event
    def next_exercise(self):
        if self.current_exercise_index < len(self.current_module_data["exercises"]) - 1:
            self.current_exercise_index += 1
            self.is_feedback_visible = False

    @rx.event
    def prev_exercise(self):
        if self.current_exercise_index > 0:
            self.current_exercise_index -= 1
            self.is_feedback_visible = False

    @rx.event
    def next_flashcard(self):
        if (
            self.current_flashcard_index
            < len(self.current_module_data["flashcards"]) - 1
        ):
            self.current_flashcard_index += 1
            self.is_flashcard_flipped = False

    @rx.event
    def prev_flashcard(self):
        if self.current_flashcard_index > 0:
            self.current_flashcard_index -= 1
            self.is_flashcard_flipped = False

    @rx.event
    async def schedule_for_review(self, concept: str, definition: str):
        from app.states.review import ReviewState

        review = await self.get_state(ReviewState)
        review.add_to_review(
            concept=concept,
            definition=definition,
            topic=self.course_topic_stored,
            module_id=self.current_module_id,
        )

    @rx.event
    async def flip_flashcard(self):
        self.is_flashcard_flipped = not self.is_flashcard_flipped
        from app.states.user_stats import UserStatsState

        stats = await self.get_state(UserStatsState)
        yield stats.add_xp(5, "Flashcard Review")
        yield LabState.schedule_for_review(
            LabState.current_flashcard["front"], LabState.current_flashcard["back"]
        )

    @rx.event
    def next_quiz_question(self):
        if (
            self.current_quiz_index
            < len(self.current_module_data["quiz_questions"]) - 1
        ):
            self.current_quiz_index += 1
            self.selected_quiz_answer = ""
            self.is_quiz_submitted = False

    @rx.event
    def prev_quiz_question(self):
        if self.current_quiz_index > 0:
            self.current_quiz_index -= 1
            self.selected_quiz_answer = ""
            self.is_quiz_submitted = False

    @rx.event
    async def submit_quiz(self):
        if not self.selected_quiz_answer:
            yield rx.toast("Please select an answer first!")
            return
        self.is_quiz_submitted = True
        self.show_explanation = True
        current_q = self.current_module_data["quiz_questions"][self.current_quiz_index]
        is_correct = self.selected_quiz_answer == current_q["correct_id"]
        difficulty = current_q.get("difficulty", "medium")
        self.quiz_performance["total"] = self.quiz_performance["total"] + 1
        from app.states.user_stats import UserStatsState

        stats = await self.get_state(UserStatsState)
        if is_correct:
            yield stats.add_xp(10, "Quiz Answer")
            self.quiz_result = "correct"
            self.feedback_message = "Correct! Well done."
            self.feedback_type = "success"
            self.quiz_performance["correct"] = self.quiz_performance["correct"] + 1
            self.quiz_performance["streak"] = self.quiz_performance["streak"] + 1
            self.quiz_performance["incorrect_streak"] = 0
            if self.quiz_performance["streak"] >= 3:
                if self.current_difficulty == "easy":
                    self.current_difficulty = "medium"
                    self.quiz_performance["streak"] = 0
                elif self.current_difficulty == "medium":
                    self.current_difficulty = "hard"
                    self.quiz_performance["streak"] = 0
        else:
            self.quiz_result = "incorrect"
            self.feedback_message = f"Not quite."
            self.feedback_type = "error"
            self.quiz_performance["streak"] = 0
            self.quiz_performance["incorrect_streak"] = (
                self.quiz_performance["incorrect_streak"] + 1
            )
            if self.quiz_performance["incorrect_streak"] >= 2:
                if self.current_difficulty == "hard":
                    self.current_difficulty = "medium"
                    self.quiz_performance["incorrect_streak"] = 0
                elif self.current_difficulty == "medium":
                    self.current_difficulty = "easy"
                    self.quiz_performance["incorrect_streak"] = 0
                if self.quiz_performance["incorrect_streak"] >= 2:
                    self.should_review = True
        if not is_correct:
            yield LabState.schedule_for_review(
                current_q["question"], current_q["explanation"]
            )
        self.is_feedback_visible = True

    @rx.event
    async def next_module(self):
        from app.states.courses import CourseState
        from app.states.user_stats import UserStatsState

        stats = await self.get_state(UserStatsState)
        yield stats.complete_lesson()
        courses = await self.get_state(CourseState)
        current_idx = -1
        for i, m in enumerate(courses.modules):
            if m["id"] == self.current_module_id:
                current_idx = i
                break
        if current_idx != -1:
            courses.mark_module_completed(self.current_module_id)
            if current_idx + 1 < len(courses.modules):
                next_m = courses.modules[current_idx + 1]
                async for update in self.load_module_content(
                    courses.course_topic, next_m["title"], next_m["id"]
                ):
                    yield update
            else:
                courses.check_course_completion()
                from app.states.navigation import NavState

                nav = await self.get_state(NavState)
                nav.current_page = "courses"

    @rx.event
    def set_active_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def select_quiz_answer(self, answer_id: str):
        if not self.is_quiz_submitted:
            self.selected_quiz_answer = answer_id

    @rx.event
    def check_practice_answer(self):
        if not self.current_code.strip():
            return rx.toast("Please type your answer first!")
        self.feedback_message = "Excellent! Your answer has been submitted for review."
        self.feedback_type = "success"
        self.is_feedback_visible = True

    @rx.event
    def run_code(self):
        if self.topic_type == "language":
            yield LabState.check_practice_answer
            return
        self.active_tab = "terminal"
        self.terminal_output.append("Running...")
        if "print" in self.current_code:
            self.terminal_output.append("Output: (Simulated Output)")
        else:
            self.terminal_output.append("Output: Done")
        self.feedback_message = "Great job! Your code executed successfully."
        self.feedback_type = "success"
        self.is_feedback_visible = True

    @rx.event
    def dismiss_feedback(self):
        self.is_feedback_visible = False