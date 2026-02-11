import reflex as rx
import os
from reflex_google_auth import google_oauth_provider
from app.components.sidebar import sidebar
from app.components.onboarding_view import onboarding_view
from app.components.lab_view import lab_view
from app.components.course_view import course_view
from app.components.diagnostic_view import diagnostic_view
from app.components.review_view import review_view
from app.states.navigation import NavState
from app.states.auth import AuthState


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.is_authenticated,
            rx.fragment(
                sidebar(),
                rx.el.main(
                    rx.match(
                        NavState.current_page,
                        ("home", onboarding_view()),
                        ("diagnostic", diagnostic_view()),
                        ("courses", course_view()),
                        ("lab", lab_view()),
                        ("reviews", review_view()),
                        (
                            "settings",
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "settings",
                                        class_name="h-12 w-12 text-slate-700 mb-4",
                                    ),
                                    rx.el.h2(
                                        "Settings",
                                        class_name="text-white text-2xl font-bold mb-2",
                                    ),
                                    rx.el.p(
                                        "Manage your profile and learning preferences.",
                                        class_name="text-slate-500",
                                    ),
                                    class_name="flex flex-col items-center justify-center h-full p-20 border-2 border-dashed border-slate-800 rounded-3xl",
                                ),
                                class_name="p-8 h-screen",
                            ),
                        ),
                        rx.el.div("Not Found", class_name="text-white"),
                    ),
                    class_name="flex-1 md:ml-64 bg-slate-950 min-h-screen transition-all duration-300",
                ),
            ),
            onboarding_view(),
        ),
        class_name="flex min-h-screen font-['Inter'] selection:bg-indigo-500/30",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    lambda: google_oauth_provider(index(), client_id=os.getenv("GOOGLE_CLIENT_ID", "")),
    route="/",
)