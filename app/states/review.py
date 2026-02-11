import reflex as rx
from typing import TypedDict
from datetime import datetime, timedelta
import uuid


class ReviewItem(TypedDict):
    id: str
    concept: str
    definition: str
    topic: str
    module_id: str
    next_review_date: str
    interval_days: int
    ease_factor: float


class ReviewState(rx.State):
    review_items: list[ReviewItem] = []
    completed_today: int = 0
    is_reviewing: bool = False
    current_index: int = 0
    is_flipped: bool = False

    @rx.var
    def pending_reviews(self) -> list[ReviewItem]:
        today = datetime.now().date()
        return [
            item
            for item in self.review_items
            if datetime.fromisoformat(item["next_review_date"]).date() <= today
        ]

    @rx.var
    def pending_count(self) -> int:
        return len(self.pending_reviews)

    @rx.var
    def current_item(self) -> ReviewItem:
        pending = self.pending_reviews
        if not pending or self.current_index >= len(pending):
            return {
                "id": "",
                "concept": "",
                "definition": "",
                "topic": "",
                "module_id": "",
                "next_review_date": "",
                "interval_days": 0,
                "ease_factor": 2.5,
            }
        return pending[self.current_index]

    @rx.event
    def add_to_review(self, concept: str, definition: str, topic: str, module_id: str):
        for item in self.review_items:
            if item["concept"] == concept and item["module_id"] == module_id:
                return
        new_item: ReviewItem = {
            "id": str(uuid.uuid4()),
            "concept": concept,
            "definition": definition,
            "topic": topic,
            "module_id": module_id,
            "next_review_date": datetime.now().isoformat(),
            "interval_days": 1,
            "ease_factor": 2.5,
        }
        self.review_items.append(new_item)

    @rx.event
    def complete_review(self, quality: int):
        if not self.pending_reviews:
            return
        item_id = self.current_item["id"]
        for i, item in enumerate(self.review_items):
            if item["id"] == item_id:
                if quality < 3:
                    item["interval_days"] = 1
                elif quality == 3:
                    item["interval_days"] = max(1, item["interval_days"])
                else:
                    intervals = [1, 3, 7, 14, 30, 60, 90]
                    current_val = item["interval_days"]
                    next_val = 1
                    for idx, val in enumerate(intervals):
                        if val > current_val:
                            next_val = val
                            break
                        if val == current_val:
                            if idx + 1 < len(intervals):
                                next_val = intervals[idx + 1]
                            else:
                                next_val = val * 2
                            break
                    item["interval_days"] = next_val
                item["next_review_date"] = (
                    datetime.now() + timedelta(days=item["interval_days"])
                ).isoformat()
                self.review_items[i] = item
                break
        self.completed_today += 1
        self.is_flipped = False
        if self.current_index >= len(self.pending_reviews) - 1:
            self.is_reviewing = False
            self.current_index = 0
        else:
            pass

    @rx.event
    def start_session(self):
        if self.pending_count > 0:
            self.is_reviewing = True
            self.current_index = 0
            self.is_flipped = False

    @rx.event
    def toggle_flip(self):
        self.is_flipped = not self.is_flipped