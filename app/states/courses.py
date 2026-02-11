import reflex as rx
from typing import TypedDict
from app.states.navigation import NavState


class ModuleInfo(TypedDict):
    id: str
    title: str
    description: str
    status: str
    progress: int


class CourseState(rx.State):
    course_topic: str = ""
    course_title: str = "Introduction to Systems Programming"
    course_description: str = "Master the fundamentals of low-level programming, memory management, and concurrency using Rust and C++."
    current_level: str = "Beginner"
    level_progression: list[str] = [
        "Beginner",
        "Intermediate",
        "Advanced",
        "Expert",
        "Master",
    ]
    show_level_up_modal: bool = False
    modules: list[ModuleInfo] = [
        {
            "id": "m1",
            "title": "Foundations of Computation",
            "description": "Learn about algorithmic thinking and basic machine architecture.",
            "status": "completed",
            "progress": 100,
        },
        {
            "id": "m2",
            "title": "Data Structures: Lists",
            "description": "Understanding memory allocation through contiguous and linked lists.",
            "status": "completed",
            "progress": 100,
        },
        {
            "id": "m3",
            "title": "Memory Management",
            "description": "Deep dive into the stack, the heap, and manual memory control.",
            "status": "active",
            "progress": 35,
        },
        {
            "id": "m4",
            "title": "Concurrency Patterns",
            "description": "Exploring mutexes, semaphores, and thread safety in modern apps.",
            "status": "locked",
            "progress": 0,
        },
        {
            "id": "m5",
            "title": "Networking Internals",
            "description": "Building custom protocol handlers and understanding TCP/IP stack.",
            "status": "locked",
            "progress": 0,
        },
        {
            "id": "m6",
            "title": "Final Capstone Project",
            "description": "Design and implement a basic operating system kernel.",
            "status": "locked",
            "progress": 0,
        },
    ]

    @rx.var
    def completed_count(self) -> int:
        return len([m for m in self.modules if m["status"] == "completed"])

    @rx.var
    def total_count(self) -> int:
        return len(self.modules)

    @rx.var
    def overall_progress(self) -> int:
        if not self.modules:
            return 0
        total_progress = sum((m["progress"] for m in self.modules))
        return int(total_progress / len(self.modules))

    @rx.var
    def is_course_complete(self) -> bool:
        if not self.modules:
            return False
        return all((m["status"] == "completed" for m in self.modules))

    @rx.var
    def next_level_label(self) -> str:
        try:
            idx = self.level_progression.index(self.current_level)
            if idx + 1 < len(self.level_progression):
                return self.level_progression[idx + 1]
            return "Grandmaster"
        except ValueError:
            return "Intermediate"

    @rx.event
    async def action_module(self, module_id: str, status: str):
        if status == "locked":
            yield rx.toast(
                "This module is locked. Complete previous modules first!", duration=3000
            )
        else:
            module_title = next(
                (m["title"] for m in self.modules if m["id"] == module_id),
                "Unknown Module",
            )
            from app.states.lab import LabState

            lab = await self.get_state(LabState)
            lab.is_loading = True
            lab.current_module_id = module_id
            nav = await self.get_state(NavState)
            nav.current_page = "lab"
            async for update in lab.load_module_content(
                self.course_topic, module_title, module_id
            ):
                yield update

    @rx.event
    def mark_module_completed(self, module_id: str):
        for i, module in enumerate(self.modules):
            if module["id"] == module_id:
                self.modules[i]["status"] = "completed"
                self.modules[i]["progress"] = 100
                if i + 1 < len(self.modules):
                    if self.modules[i + 1]["status"] == "locked":
                        self.modules[i + 1]["status"] = "active"
                break

    @rx.event
    def check_course_completion(self):
        if self.is_course_complete:
            self.show_level_up_modal = True

    @rx.event
    async def start_level_up(self):
        self.show_level_up_modal = False
        from app.states.diagnostic import DiagnosticState
        from app.states.i18n import I18nState
        from app.states.navigation import NavState

        diagnostic = await self.get_state(DiagnosticState)
        i18n = await self.get_state(I18nState)
        nav = await self.get_state(NavState)
        yield DiagnosticState.start_level_up_diagnostic(
            self.course_topic,
            self.current_level,
            CourseState.next_level_label,
            i18n.current_language,
        )
        nav.current_page = "diagnostic"

    @rx.event
    def advance_to_next_level(self):
        try:
            idx = self.level_progression.index(self.current_level)
            if idx + 1 < len(self.level_progression):
                self.current_level = self.level_progression[idx + 1]
        except ValueError:
            pass
        self.show_level_up_modal = False