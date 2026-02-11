import reflex as rx


class NavState(rx.State):
    current_page: str = "home"

    @rx.event
    def set_page(self, page: str):
        self.current_page = page

    nav_items: list[dict[str, str]] = [
        {"label": "Explore", "icon": "compass", "id": "home"},
        {"label": "My Courses", "icon": "book-open", "id": "courses"},
        {"label": "Active Lab", "icon": "terminal", "id": "lab"},
        {"label": "Reviews", "icon": "calendar", "id": "reviews"},
        {"label": "Settings", "icon": "settings", "id": "settings"},
    ]