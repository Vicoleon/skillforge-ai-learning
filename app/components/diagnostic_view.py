import reflex as rx
from app.states.diagnostic import DiagnosticState


def question_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                f"Question {DiagnosticState.current_question_index + 1} of {DiagnosticState.total_questions}",
                class_name="text-xs font-bold text-indigo-400 uppercase tracking-widest mb-2 block",
            ),
            rx.el.h3(
                DiagnosticState.current_question["question"],
                class_name="text-2xl font-bold text-white mb-6 leading-relaxed",
            ),
            rx.el.div(
                rx.foreach(
                    DiagnosticState.current_question["options"],
                    lambda opt: rx.el.button(
                        rx.el.div(
                            rx.el.span(
                                opt["id"].upper(),
                                class_name="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-xs font-bold text-slate-400 group-hover:bg-indigo-500 group-hover:text-white transition-all mr-4",
                            ),
                            rx.el.span(
                                opt["text"], class_name="text-slate-200 font-medium"
                            ),
                            class_name="flex items-center",
                        ),
                        on_click=lambda: DiagnosticState.answer_question(opt["id"]),
                        class_name="group w-full p-4 bg-slate-900/50 hover:bg-slate-800 border border-slate-800 hover:border-indigo-500/50 rounded-2xl transition-all text-left flex items-center",
                    ),
                ),
                class_name="flex flex-col gap-3",
            ),
            class_name="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl",
        ),
        class_name="max-w-2xl w-full mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500",
    )


def results_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Assessment Complete",
                class_name="text-3xl font-bold text-white mb-2 text-center",
            ),
            rx.el.p(
                f"We've analyzed your skills in {DiagnosticState.topic}.",
                class_name="text-slate-400 text-center mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"{DiagnosticState.overall_score}%",
                        class_name="text-4xl font-black text-white",
                    ),
                    rx.el.span(
                        DiagnosticState.proficiency_level,
                        class_name="text-sm font-bold text-indigo-400 uppercase tracking-wider mt-1",
                    ),
                    class_name="flex flex-col items-center justify-center p-6 bg-slate-800/50 rounded-2xl border border-slate-700 w-full mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h4(
                            "Strengths",
                            class_name="text-sm font-bold text-emerald-400 mb-3 uppercase",
                        ),
                        rx.foreach(
                            DiagnosticState.strengths,
                            lambda s: rx.el.div(
                                rx.icon("check", class_name="h-3 w-3 mr-2"),
                                s,
                                class_name="inline-flex items-center px-3 py-1 bg-emerald-500/10 text-emerald-300 text-xs rounded-full border border-emerald-500/20 mr-2 mb-2",
                            ),
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "Focus Areas",
                            class_name="text-sm font-bold text-rose-400 mb-3 uppercase",
                        ),
                        rx.foreach(
                            DiagnosticState.weaknesses,
                            lambda w: rx.el.div(
                                rx.icon("target", class_name="h-3 w-3 mr-2"),
                                w,
                                class_name="inline-flex items-center px-3 py-1 bg-rose-500/10 text-rose-300 text-xs rounded-full border border-rose-500/20 mr-2 mb-2",
                            ),
                        ),
                    ),
                    class_name="text-left w-full mb-8",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Our Recommendation",
                        class_name="text-sm font-bold text-slate-500 mb-2 uppercase",
                    ),
                    rx.el.p(
                        DiagnosticState.recommended_focus,
                        class_name="text-slate-300 text-sm leading-relaxed",
                    ),
                    class_name="bg-indigo-500/5 border border-indigo-500/10 p-4 rounded-xl w-full mb-8",
                ),
                class_name="flex flex-col items-center",
            ),
            rx.el.button(
                "Generate Personalized Course",
                rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                on_click=DiagnosticState.generate_personalized_path,
                disabled=DiagnosticState.is_loading,
                class_name="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold tracking-wide transition-all shadow-lg shadow-indigo-600/20 flex items-center justify-center",
            ),
            class_name="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl max-w-lg w-full mx-auto animate-in zoom-in-95 duration-500",
        ),
        class_name="flex items-center justify-center w-full",
    )


def diagnostic_view() -> rx.Component:
    return rx.el.div(
        rx.cond(
            DiagnosticState.is_loading,
            rx.el.div(
                rx.icon(
                    "squirrel", class_name="h-12 w-12 text-indigo-500 animate-spin mb-4"
                ),
                rx.el.h3(
                    rx.cond(
                        DiagnosticState.is_complete,
                        "Analyzing your results...",
                        "Preparing your assessment...",
                    ),
                    class_name="text-xl font-semibold text-white animate-pulse",
                ),
                class_name="flex flex-col items-center justify-center min-h-[60vh]",
            ),
            rx.cond(
                DiagnosticState.is_complete,
                results_view(),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            class_name="h-1 bg-indigo-500 transition-all duration-500",
                            style={"width": f"{DiagnosticState.progress}%"},
                        ),
                        class_name="w-full h-1 bg-slate-800 fixed top-0 left-0 z-50 md:left-64 md:w-[calc(100vw-16rem)]",
                    ),
                    rx.el.div(
                        question_card(),
                        class_name="flex flex-col items-center justify-center min-h-[80vh] px-4",
                    ),
                ),
            ),
        ),
        class_name="w-full min-h-screen bg-slate-950",
    )