import reflex as rx
from datetime import datetime
from typing import TypedDict


class Badge(TypedDict):
    id: str
    name: str
    description: str
    icon: str
    earned_date: str


class UserStatsState(rx.State):
    xp_total: int = 1250
    xp_today: int = 0
    current_streak: int = 4
    longest_streak: int = 7
    last_activity_date: str = datetime.now().strftime("%Y-%m-%d")
    courses_completed: int = 1
    quizzes_completed: int = 12
    lessons_completed: int = 45
    badges: list[Badge] = [
        {
            "id": "b1",
            "name": "Early Bird",
            "description": "Learn before 8 AM",
            "icon": "sun",
            "earned_date": "2024-03-01",
        }
    ]

    @rx.var
    def level_name(self) -> str:
        if self.xp_total < 500:
            return "Novice"
        if self.xp_total < 2000:
            return "Apprentice"
        if self.xp_total < 5000:
            return "Scholar"
        return "Master"

    @rx.var
    def level_progress(self) -> int:
        if self.xp_total < 500:
            return int(self.xp_total / 500 * 100)
        if self.xp_total < 2000:
            return int((self.xp_total - 500) / 1500 * 100)
        if self.xp_total < 5000:
            return int((self.xp_total - 2000) / 3000 * 100)
        return 100

    @rx.var
    def next_level_xp(self) -> int:
        if self.xp_total < 500:
            return 500
        if self.xp_total < 2000:
            return 2000
        if self.xp_total < 5000:
            return 5000
        return self.xp_total

    @rx.event
    def add_xp(self, amount: int, source: str):
        old_level = self.level_name
        self.xp_total += amount
        self.xp_today += amount
        new_level = self.level_name
        if old_level != new_level:
            yield rx.toast(
                f"🎉 Level Up! You're now a {new_level}!",
                duration=5000,
                close_button=True,
            )
        yield UserStatsState.update_streak
        yield UserStatsState.check_badges

    @rx.event
    def update_streak(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if self.last_activity_date != today:
            yesterday = (datetime.now() - rx.Var.create(1).to(object)).strftime(
                "%Y-%m-%d"
            )
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
            self.last_activity_date = today

    @rx.event
    def complete_quiz(self, score: int, total: int):
        xp = score * 10
        if score == total:
            xp += 100
        self.quizzes_completed += 1
        yield UserStatsState.add_xp(xp, "Quiz Completion")

    @rx.event
    def complete_lesson(self):
        self.lessons_completed += 1
        yield UserStatsState.add_xp(50, "Lesson Completion")

    @rx.event
    def check_badges(self):
        if self.quizzes_completed >= 10 and (
            not any((b["id"] == "q10" for b in self.badges))
        ):
            new_badge = {
                "id": "q10",
                "name": "Quiz Master",
                "description": "Complete 10 quizzes",
                "icon": "award",
                "earned_date": datetime.now().strftime("%Y-%m-%d"),
            }
            self.badges.append(new_badge)
            yield rx.toast(
                f"🏆 New Badge: {new_badge['name']}!", duration=5000, close_button=True
            )