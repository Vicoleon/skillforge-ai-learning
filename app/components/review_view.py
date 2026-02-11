import reflex as rx
from app.states.review import ReviewState


def rating_button(label: str, color: str, quality: int) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: ReviewState.complete_review(quality),
        class_name=f"flex-1 py-3 {color} text-white rounded-xl font-bold text-sm transition-all hover:scale-105 active:scale-95",
    )


def review_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                ReviewState.current_item["topic"].upper(),
                class_name="text-[10px] font-bold text-indigo-400 tracking-widest mb-4 block",
            ),
            rx.el.div(
                rx.el.h2(
                    rx.cond(
                        ReviewState.is_flipped,
                        ReviewState.current_item["definition"],
                        ReviewState.current_item["concept"],
                    ),
                    class_name="text-3xl font-bold text-center text-white",
                ),
                on_click=ReviewState.toggle_flip,
                class_name="relative w-full h-80 bg-slate-900 border-2 border-slate-800 rounded-[2rem] flex items-center justify-center p-8 cursor-pointer shadow-2xl transition-all hover:border-indigo-500/30",
            ),
            rx.cond(
                ReviewState.is_flipped,
                rx.el.div(
                    rx.el.p(
                        "How well did you know this?",
                        class_name="text-slate-500 text-sm mb-4 text-center",
                    ),
                    rx.el.div(
                        rating_button("Again", "bg-rose-600", 0),
                        rating_button("Hard", "bg-orange-600", 3),
                        rating_button("Good", "bg-indigo-600", 4),
                        rating_button("Easy", "bg-emerald-600", 5),
                        class_name="flex gap-3",
                    ),
                    class_name="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-300",
                ),
                rx.el.p(
                    "Click card to reveal definition",
                    class_name="text-slate-600 text-sm mt-6 text-center animate-pulse",
                ),
            ),
            class_name="max-w-md w-full mx-auto",
        ),
        class_name="flex flex-col items-center justify-center min-h-[60vh]",
    )


def dashboard_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar-check", class_name="h-16 w-16 text-indigo-500 mb-6"),
                rx.el.h2(
                    rx.cond(
                        ReviewState.pending_count > 0,
                        f"{ReviewState.pending_count} Concepts Due for Review",
                        "All Caught Up!",
                    ),
                    class_name="text-3xl font-bold text-white mb-2",
                ),
                rx.el.p(
                    rx.cond(
                        ReviewState.pending_count > 0,
                        "Consistency is key to mastering new skills. Start your daily review session.",
                        "You've completed all your scheduled reviews for today. Great job!",
                    ),
                    class_name="text-slate-400 mb-10",
                ),
                rx.cond(
                    ReviewState.pending_count > 0,
                    rx.el.button(
                        "Start Review Session",
                        rx.icon("play", class_name="h-4 w-4 ml-2"),
                        on_click=ReviewState.start_session,
                        class_name="px-10 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-bold shadow-xl shadow-indigo-600/20 transition-all flex items-center",
                    ),
                    rx.el.div(
                        rx.el.span("🎉", class_name="text-4xl block mb-4"),
                        rx.el.p(
                            "Check back tomorrow for more!",
                            class_name="text-slate-500 font-medium",
                        ),
                        class_name="text-center",
                    ),
                ),
                class_name="flex flex-col items-center text-center",
            ),
            class_name="bg-slate-900/50 border border-slate-800 p-20 rounded-[3rem] shadow-2xl",
        ),
        class_name="max-w-4xl mx-auto py-12 px-4",
    )


def review_view() -> rx.Component:
    return rx.el.div(
        rx.cond(
            ReviewState.is_reviewing,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="h-1 bg-indigo-500 transition-all duration-500",
                        style={
                            "width": f"{(ReviewState.current_index + 1) / ReviewState.pending_count * 100}%"
                        },
                    ),
                    class_name="w-full h-1 bg-slate-800 fixed top-0 left-0 md:left-64 z-50",
                ),
                review_card(),
            ),
            dashboard_view(),
        ),
        class_name="w-full min-h-screen bg-slate-950",
    )