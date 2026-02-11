import reflex as rx
from app.states.lab import LabState
from app.states.tutor import TutorState
from app.components.tutor_panel import tutor_panel


def tab_button(label: str, tab_id: str) -> rx.Component:
    is_active = LabState.active_tab == tab_id
    return rx.el.button(
        label,
        on_click=lambda: LabState.set_active_tab(tab_id),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-semibold text-indigo-400 border-b-2 border-indigo-500 transition-all",
            "px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-300 transition-all",
        ),
    )


def nav_controls(
    current: int, total: int, on_prev: rx.event.EventType, on_next: rx.event.EventType
) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("chevron-left", class_name="h-5 w-5"),
            on_click=on_prev,
            disabled=current == 0,
            class_name="p-2 bg-slate-800 rounded-lg text-slate-400 hover:text-white disabled:opacity-30",
        ),
        rx.el.span(
            f"{current + 1} / {total}",
            class_name="text-sm font-bold text-slate-500 mx-4",
        ),
        rx.el.button(
            rx.icon("chevron-right", class_name="h-5 w-5"),
            on_click=on_next,
            disabled=current == total - 1,
            class_name="p-2 bg-slate-800 rounded-lg text-slate-400 hover:text-white disabled:opacity-30",
        ),
        class_name="flex items-center justify-center p-4",
    )


def feedback_area() -> rx.Component:
    return rx.cond(
        LabState.is_feedback_visible,
        rx.el.div(
            rx.el.div(
                rx.match(
                    LabState.feedback_type,
                    (
                        "success",
                        rx.icon(
                            "lamp_wall_down", class_name="h-5 w-5 text-emerald-400"
                        ),
                    ),
                    ("error", rx.icon("wheat", class_name="h-5 w-5 text-rose-400")),
                    rx.icon("info", class_name="h-5 w-5 text-indigo-400"),
                ),
                rx.el.p(LabState.feedback_message, class_name="text-sm text-slate-200"),
                class_name="flex items-start gap-3",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-4 w-4 text-slate-500"),
                on_click=LabState.dismiss_feedback,
                class_name="hover:bg-slate-700/50 p-1 rounded-lg transition-colors",
            ),
            class_name=rx.match(
                LabState.feedback_type,
                (
                    "success",
                    "flex items-center justify-between p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl mt-4",
                ),
                (
                    "error",
                    "flex items-center justify-between p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl mt-4",
                ),
                "flex items-center justify-between p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl mt-4",
            ),
        ),
        rx.fragment(),
    )


def editor_view() -> rx.Component:
    is_lang = LabState.topic_type == "language"
    return rx.el.div(
        rx.cond(
            is_lang,
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "EXERCISE",
                        class_name="text-[10px] font-bold text-indigo-500 tracking-widest mb-2 block",
                    ),
                    rx.el.h3(
                        LabState.current_exercise["prompt"],
                        class_name="text-3xl font-bold text-white mb-8 leading-tight",
                    ),
                    rx.el.textarea(
                        default_value="",
                        on_change=LabState.set_current_code,
                        placeholder="Type your answer or translation here...",
                        class_name="w-full bg-slate-900/50 p-8 text-xl text-indigo-100 font-medium outline-none rounded-3xl border border-slate-800 focus:border-indigo-500/50 transition-all resize-none min-h-[200px] shadow-inner",
                        spell_check=False,
                    ),
                    class_name="max-w-3xl mx-auto w-full p-10",
                ),
                nav_controls(
                    LabState.current_exercise_index,
                    10,
                    LabState.prev_exercise,
                    LabState.next_exercise,
                ),
                class_name="flex-1 flex flex-col justify-center",
            ),
            rx.fragment(
                rx.el.div(
                    rx.foreach(
                        rx.Var.range(1, 25),
                        lambda i: rx.el.span(
                            i.to_string(),
                            class_name="block text-slate-600 text-xs text-right pr-4 font-mono select-none",
                        ),
                    ),
                    class_name="w-12 pt-4 bg-slate-900/50 border-r border-slate-800",
                ),
                rx.el.textarea(
                    default_value=LabState.current_code,
                    on_change=LabState.set_current_code,
                    placeholder="# Your code here",
                    class_name="flex-1 bg-transparent p-4 text-indigo-300 font-mono text-sm outline-none resize-none h-full placeholder:text-slate-700",
                    spell_check=False,
                ),
            ),
        ),
        rx.el.button(
            rx.icon(
                rx.cond(is_lang, "check-circle", "play"), class_name="h-5 w-5 mr-2"
            ),
            rx.cond(is_lang, "Check Answer", "Run Code"),
            on_click=LabState.run_code,
            class_name="absolute bottom-12 right-12 flex items-center bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-4 rounded-2xl shadow-xl shadow-indigo-600/30 transition-all font-bold tracking-wide z-10",
        ),
        class_name="relative flex flex-1 bg-slate-950 min-h-[500px] overflow-hidden flex-col",
    )


def terminal_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                LabState.terminal_output,
                lambda line: rx.el.p(
                    line, class_name="font-mono text-xs text-emerald-400 py-0.5"
                ),
            ),
            class_name="p-6",
        ),
        class_name="flex-1 bg-black overflow-auto",
    )


def quiz_option(opt: dict) -> rx.Component:
    is_selected = LabState.selected_quiz_answer == opt["id"]
    is_submitted = LabState.is_quiz_submitted
    is_correct = opt["id"] == LabState.current_module["quiz"]["correct_id"]
    border_color = rx.cond(
        is_submitted,
        rx.cond(
            is_correct,
            "border-emerald-500",
            rx.cond(is_selected, "border-rose-500", "border-slate-800"),
        ),
        rx.cond(is_selected, "border-indigo-500", "border-slate-800"),
    )
    bg_color = rx.cond(
        is_submitted,
        rx.cond(
            is_correct,
            "bg-emerald-500/10",
            rx.cond(is_selected, "bg-rose-500/10", "bg-slate-900/40"),
        ),
        rx.cond(is_selected, "bg-indigo-500/10", "bg-slate-900/40"),
    )
    return rx.el.button(
        rx.el.div(
            rx.el.span(
                opt["id"].upper(), class_name="text-xs font-bold text-slate-500 mr-4"
            ),
            rx.el.span(opt["text"], class_name="text-white"),
            class_name="flex items-center",
        ),
        rx.cond(
            is_submitted & is_correct,
            rx.icon("lamp_wall_down", class_name="h-5 w-5 text-emerald-500"),
            rx.cond(
                is_submitted & is_selected & ~is_correct,
                rx.icon("pen", class_name="h-5 w-5 text-rose-500"),
                rx.fragment(),
            ),
        ),
        on_click=lambda: LabState.select_quiz_answer(opt["id"]),
        disabled=is_submitted,
        class_name=f"w-full flex items-center justify-between p-5 rounded-2xl border {border_color} {bg_color} transition-all hover:scale-[1.01] active:scale-95 disabled:hover:scale-100",
    )


def flashcard_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(
                            LabState.is_flashcard_flipped,
                            LabState.current_flashcard["back"],
                            LabState.current_flashcard["front"],
                        ),
                        class_name="text-3xl font-bold text-center text-white",
                    ),
                    rx.el.p(
                        rx.cond(LabState.is_flashcard_flipped, "DEFINITION", "TERM"),
                        class_name="absolute top-4 left-4 text-[10px] font-black text-indigo-500 tracking-[0.2em]",
                    ),
                    on_click=LabState.flip_flashcard,
                    class_name="relative w-80 h-96 bg-slate-900 border-2 border-slate-800 rounded-[2rem] flex items-center justify-center p-8 cursor-pointer shadow-2xl transition-all hover:scale-105 active:scale-95",
                ),
                class_name="flex justify-center items-center h-full",
            ),
            nav_controls(
                LabState.current_flashcard_index,
                10,
                LabState.prev_flashcard,
                LabState.next_flashcard,
            ),
            class_name="p-10",
        ),
        class_name="flex-1 bg-slate-950",
    )


def quiz_option(opt: dict) -> rx.Component:
    is_selected = LabState.selected_quiz_answer == opt["id"]
    is_submitted = LabState.is_quiz_submitted
    is_correct = opt["id"] == LabState.current_quiz_question["correct_id"]
    border_color = rx.cond(
        is_submitted,
        rx.cond(
            is_correct,
            "border-emerald-500",
            rx.cond(is_selected, "border-rose-500", "border-slate-800"),
        ),
        rx.cond(is_selected, "border-indigo-500", "border-slate-800"),
    )
    bg_color = rx.cond(
        is_submitted,
        rx.cond(
            is_correct,
            "bg-emerald-500/10",
            rx.cond(is_selected, "bg-rose-500/10", "bg-slate-900/40"),
        ),
        rx.cond(is_selected, "bg-indigo-500/10", "bg-slate-900/40"),
    )
    return rx.el.button(
        rx.el.div(
            rx.el.span(
                opt["id"].upper(), class_name="text-xs font-bold text-slate-500 mr-4"
            ),
            rx.el.span(opt["text"], class_name="text-white"),
            class_name="flex items-center",
        ),
        rx.cond(
            is_submitted & is_correct,
            rx.icon("lamp_wall_down", class_name="h-5 w-5 text-emerald-500"),
            rx.cond(
                is_submitted & is_selected & ~is_correct,
                rx.icon("pen", class_name="h-5 w-5 text-rose-500"),
                rx.fragment(),
            ),
        ),
        on_click=lambda: LabState.select_quiz_answer(opt["id"]),
        disabled=is_submitted,
        class_name=f"w-full flex items-center justify-between p-5 rounded-2xl border {border_color} {bg_color} transition-all hover:scale-[1.01] active:scale-95 disabled:hover:scale-100",
    )


def quiz_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        LabState.current_quiz_question["difficulty"].upper(),
                        class_name=rx.match(
                            LabState.current_quiz_question["difficulty"],
                            (
                                "easy",
                                "text-[10px] font-bold text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded",
                            ),
                            (
                                "medium",
                                "text-[10px] font-bold text-indigo-400 bg-indigo-400/10 px-2 py-1 rounded",
                            ),
                            (
                                "hard",
                                "text-[10px] font-bold text-rose-400 bg-rose-400/10 px-2 py-1 rounded",
                            ),
                            "text-[10px] font-bold text-slate-400 bg-slate-400/10 px-2 py-1 rounded",
                        ),
                    ),
                    rx.el.span(
                        f"Score: {LabState.quiz_performance['correct']} / {LabState.quiz_performance['total']}",
                        class_name="text-[10px] font-bold text-slate-500 bg-slate-800 px-2 py-1 rounded",
                    ),
                    class_name="flex items-center gap-2 mb-4",
                ),
                rx.el.h3(
                    LabState.current_quiz_question["question"],
                    class_name="text-xl font-bold text-white mb-10 leading-relaxed",
                ),
                rx.el.div(
                    rx.foreach(LabState.current_quiz_question["options"], quiz_option),
                    class_name="flex flex-col gap-4",
                ),
                rx.cond(
                    ~LabState.is_quiz_submitted,
                    rx.el.button(
                        "Submit Answer",
                        on_click=LabState.submit_quiz,
                        class_name="w-full mt-10 py-5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-bold tracking-wide transition-all shadow-lg shadow-indigo-600/20",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    rx.cond(
                                        LabState.quiz_result == "correct",
                                        "Correct!",
                                        "Not quite.",
                                    ),
                                    class_name=rx.cond(
                                        LabState.quiz_result == "correct",
                                        "text-emerald-400 font-bold text-lg mb-2",
                                        "text-rose-400 font-bold text-lg mb-2",
                                    ),
                                ),
                                rx.el.p(
                                    LabState.current_quiz_question["explanation"],
                                    class_name="text-slate-300 text-sm leading-relaxed",
                                ),
                                class_name="text-left",
                            ),
                            class_name="mt-10 p-6 bg-slate-900/80 rounded-2xl border border-slate-800",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Next Question",
                                rx.icon("arrow-right", class_name="ml-2 h-4 w-4"),
                                on_click=LabState.next_quiz_question,
                                class_name="w-full mt-4 py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold transition-all flex items-center justify-center",
                            ),
                            rx.cond(
                                LabState.should_review,
                                rx.el.button(
                                    "Review Lesson Material",
                                    rx.icon("book", class_name="mr-2 h-4 w-4"),
                                    on_click=LabState.dismiss_feedback,
                                    class_name="w-full mt-3 py-3 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-xl text-sm font-semibold hover:bg-indigo-500/20 transition-all flex items-center justify-center",
                                ),
                            ),
                        ),
                    ),
                ),
                class_name="p-10 max-w-2xl mx-auto",
            )
        ),
        class_name="flex-1 bg-slate-950 overflow-y-auto",
    )


def lab_view() -> rx.Component:
    return rx.el.div(
        rx.cond(
            LabState.is_loading,
            rx.el.div(
                rx.icon(
                    "squirrel", class_name="h-12 w-12 text-indigo-500 animate-spin mb-4"
                ),
                rx.el.h3(
                    "Preparing your lesson...",
                    class_name="text-xl font-semibold text-white",
                ),
                rx.el.p(
                    "The AI is generating theory, examples, and quizzes for this module.",
                    class_name="text-slate-500 mt-2",
                ),
                class_name="absolute inset-0 z-50 flex flex-col items-center justify-center bg-slate-950/90 backdrop-blur-sm",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Active Module",
                        class_name="text-[10px] font-bold text-indigo-400 bg-indigo-400/10 px-2 py-1 rounded uppercase tracking-wider",
                    ),
                    rx.el.h1(
                        LabState.current_module["title"],
                        class_name="text-2xl font-bold text-white mt-2",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.markdown(
                        LabState.current_module["content"],
                        class_name="prose prose-invert max-w-none text-slate-300 [&_h3]:text-white [&_strong]:text-indigo-300",
                    ),
                    class_name="flex-1 overflow-y-auto mb-8 pr-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            class_name="h-1 bg-indigo-600 transition-all duration-500",
                            style={"width": f"{LabState.progress_percentage}%"},
                        ),
                        class_name="w-full h-1 bg-slate-800 rounded-full overflow-hidden mb-4",
                    ),
                    rx.el.button(
                        "Next Module",
                        rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                        on_click=LabState.next_module,
                        class_name="w-full py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-xl border border-slate-700 transition-all flex items-center justify-center font-semibold",
                    ),
                    class_name="mt-auto",
                ),
                class_name="flex flex-col h-full bg-slate-900/50 p-8 border-r border-slate-800",
            ),
            class_name="w-full md:w-1/2 h-full",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        LabState.topic_type == "language",
                        rx.fragment(
                            tab_button("Practice", "practice"),
                            tab_button("Flashcards", "flashcards"),
                            tab_button("Quiz", "quiz"),
                        ),
                        rx.fragment(
                            tab_button("Editor", "editor"),
                            tab_button("Terminal", "terminal"),
                            tab_button("Quiz", "quiz"),
                        ),
                    ),
                    class_name="flex px-6 border-b border-slate-800 bg-slate-900",
                ),
                rx.cond(
                    LabState.topic_type == "language",
                    rx.match(
                        LabState.active_tab,
                        ("practice", editor_view()),
                        ("flashcards", flashcard_view()),
                        ("quiz", quiz_view()),
                        editor_view(),
                    ),
                    rx.match(
                        LabState.active_tab,
                        ("editor", editor_view()),
                        ("terminal", terminal_view()),
                        ("quiz", quiz_view()),
                        editor_view(),
                    ),
                ),
                rx.el.div(feedback_area(), class_name="p-6"),
                class_name="flex flex-col h-full",
            ),
            class_name="w-full md:w-1/2 h-full bg-slate-950",
        ),
        tutor_panel(),
        rx.cond(
            ~TutorState.is_open,
            rx.el.button(
                rx.icon("bot", class_name="h-6 w-6 mr-2"),
                "Ask Tutor",
                on_click=TutorState.toggle_tutor,
                class_name="fixed bottom-8 right-8 z-40 bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-4 rounded-full font-bold shadow-2xl shadow-indigo-600/40 flex items-center transition-all hover:scale-105 active:scale-95 animate-in slide-in-from-bottom-4 duration-500",
            ),
        ),
        class_name="flex flex-col md:flex-row h-screen w-full overflow-hidden relative",
    )