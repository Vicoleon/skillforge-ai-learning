import reflex as rx
from app.states.courses import CourseState


def progress_circle() -> rx.Component:
    return rx.el.div(
        rx.el.svg(
            rx.el.circle(
                cx="50",
                cy="50",
                r="40",
                class_name="stroke-slate-800 fill-none",
                stroke_width="8",
            ),
            rx.el.circle(
                cx="50",
                cy="50",
                r="40",
                class_name="stroke-indigo-500 fill-none transition-all duration-1000",
                stroke_width="8",
                stroke_dasharray="251.2",
                stroke_dashoffset=rx.cond(
                    CourseState.overall_progress > 0,
                    (251.2 * (1 - CourseState.overall_progress / 100)).to_string(),
                    "251.2",
                ),
                stroke_linecap="round",
                transform="rotate(-90 50 50)",
            ),
            view_box="0 0 100 100",
            class_name="w-32 h-32",
        ),
        rx.el.div(
            rx.el.span(
                f"{CourseState.overall_progress}%",
                class_name="text-2xl font-bold text-white",
            ),
            class_name="absolute inset-0 flex items-center justify-center",
        ),
        class_name="relative",
    )


from app.states.user_stats import UserStatsState


def stats_summary() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"{UserStatsState.level_name} • {UserStatsState.xp_total} XP",
                        class_name="text-xs font-bold text-indigo-400",
                    ),
                    rx.el.span(
                        f"Next level: {UserStatsState.next_level_xp} XP",
                        class_name="text-[10px] text-slate-500",
                    ),
                    class_name="flex justify-between mb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="h-full bg-indigo-500 transition-all duration-500",
                        style={"width": f"{UserStatsState.level_progress}%"},
                    ),
                    class_name="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("flame", class_name="h-5 w-5 text-orange-500"),
                    rx.el.span(
                        f"{UserStatsState.current_streak} Day Streak",
                        class_name="text-sm font-bold text-white",
                    ),
                    class_name="flex items-center gap-2 px-4 py-2 bg-orange-500/10 rounded-xl border border-orange-500/20",
                ),
                class_name="shrink-0",
            ),
            class_name="flex items-center gap-8 bg-slate-900/80 border border-slate-800 p-4 rounded-2xl mb-8 shadow-xl shadow-black/20",
        )
    )


from app.states.i18n import I18nState


def course_header() -> rx.Component:
    return rx.el.div(
        stats_summary(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    CourseState.course_title,
                    class_name="text-3xl font-bold text-white mb-2",
                ),
                rx.el.p(
                    CourseState.course_description,
                    class_name="text-slate-400 max-w-2xl text-lg",
                ),
                class_name="flex-1",
            ),
            progress_circle(),
            class_name="flex flex-col md:flex-row items-center gap-8 mb-10 p-8 bg-slate-900/50 rounded-3xl border border-slate-800",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    I18nState.translations[I18nState.current_language][
                        "course.progress"
                    ],
                    class_name="text-xs font-bold text-slate-500 uppercase tracking-widest",
                ),
                rx.el.p(
                    I18nState.translations[I18nState.current_language][
                        "course.modules_completed"
                    ]
                    .replace("{completed}", CourseState.completed_count.to_string())
                    .replace("{total}", CourseState.total_count.to_string()),
                    class_name="text-sm text-indigo-400 font-medium",
                ),
                class_name="flex flex-col",
            ),
            class_name="px-2 mb-6",
        ),
    )


def module_card(module: dict) -> rx.Component:
    status = module["status"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.match(
                    status,
                    (
                        "completed",
                        rx.icon(
                            "lamp_wall_down", class_name="h-6 w-6 text-emerald-500"
                        ),
                    ),
                    ("locked", rx.icon("lock", class_name="h-6 w-6 text-slate-600")),
                    rx.icon("heading_4", class_name="h-6 w-6 text-indigo-500"),
                ),
                rx.el.span(
                    rx.match(
                        status,
                        (
                            "completed",
                            I18nState.translations[I18nState.current_language][
                                "course.completed"
                            ],
                        ),
                        (
                            "locked",
                            I18nState.translations[I18nState.current_language][
                                "course.locked"
                            ],
                        ),
                        I18nState.translations[I18nState.current_language][
                            "course.active"
                        ],
                    ),
                    class_name=rx.match(
                        status,
                        (
                            "completed",
                            "text-[10px] font-bold text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded",
                        ),
                        (
                            "locked",
                            "text-[10px] font-bold text-slate-500 bg-slate-500/10 px-2 py-1 rounded",
                        ),
                        "text-[10px] font-bold text-indigo-400 bg-indigo-400/10 px-2 py-1 rounded",
                    ),
                ),
                class_name="flex items-center justify-between mb-4",
            ),
            rx.el.h3(module["title"], class_name="text-lg font-bold text-white mb-2"),
            rx.el.p(
                module["description"],
                class_name="text-sm text-slate-400 mb-6 flex-1 line-clamp-2",
            ),
            rx.el.div(
                rx.el.div(
                    class_name=rx.match(
                        status,
                        ("completed", "h-full bg-emerald-500"),
                        ("locked", "h-full bg-slate-700"),
                        "h-full bg-indigo-500",
                    ),
                    style={"width": f"{module['progress']}%"},
                ),
                class_name="w-full h-1 bg-slate-800 rounded-full overflow-hidden mb-6",
            ),
            rx.el.button(
                rx.match(
                    status,
                    (
                        "completed",
                        I18nState.translations[I18nState.current_language][
                            "course.review_module"
                        ],
                    ),
                    (
                        "locked",
                        I18nState.translations[I18nState.current_language][
                            "course.locked"
                        ],
                    ),
                    I18nState.translations[I18nState.current_language][
                        "course.start_learning"
                    ],
                ),
                on_click=CourseState.action_module(module["id"], status),
                class_name=rx.match(
                    status,
                    (
                        "completed",
                        "w-full min-h-[48px] py-3 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 rounded-xl border border-emerald-500/20 transition-all font-semibold text-sm cursor-pointer touch-manipulation",
                    ),
                    (
                        "locked",
                        "w-full min-h-[48px] py-3 bg-slate-800/50 text-slate-600 rounded-xl border border-slate-800 transition-all font-semibold text-sm cursor-not-allowed touch-manipulation",
                    ),
                    "w-full min-h-[48px] py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl shadow-lg shadow-indigo-600/20 transition-all font-semibold text-sm cursor-pointer touch-manipulation",
                ),
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=rx.match(
            status,
            (
                "completed",
                "p-6 bg-slate-900 border border-emerald-500/30 rounded-3xl h-full shadow-xl shadow-emerald-500/5",
            ),
            (
                "locked",
                "p-6 bg-slate-900/40 border border-slate-800 rounded-3xl h-full opacity-60",
            ),
            "p-6 bg-slate-900 border border-indigo-500/30 rounded-3xl h-full shadow-xl shadow-indigo-500/10",
        ),
    )


def level_up_modal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span("🎉", class_name="text-6xl mb-6 block animate-bounce"),
                rx.el.h2(
                    I18nState.translations[I18nState.current_language][
                        "course.level_complete"
                    ]
                    .replace("{level}", CourseState.current_level)
                    .replace("{topic}", CourseState.course_topic),
                    class_name="text-2xl font-bold text-white mb-2",
                ),
                rx.el.p(
                    I18nState.translations[I18nState.current_language][
                        "course.ready_advance"
                    ].replace("{next_level}", CourseState.next_level_label),
                    class_name="text-slate-400 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Modules Completed",
                            class_name="text-xs text-slate-500 uppercase font-bold",
                        ),
                        rx.el.p(
                            CourseState.total_count.to_string(),
                            class_name="text-xl font-bold text-indigo-400",
                        ),
                        class_name="flex-1 p-4 bg-slate-800 rounded-2xl",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "XP Earned",
                            class_name="text-xs text-slate-500 uppercase font-bold",
                        ),
                        rx.el.p("300", class_name="text-xl font-bold text-emerald-400"),
                        class_name="flex-1 p-4 bg-slate-800 rounded-2xl",
                    ),
                    class_name="flex gap-4 w-full mb-8",
                ),
                rx.el.div(
                    rx.el.button(
                        I18nState.translations[I18nState.current_language][
                            "course.take_assessment"
                        ],
                        on_click=CourseState.start_level_up,
                        class_name="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-bold transition-all shadow-lg shadow-indigo-600/20 mb-3",
                    ),
                    rx.el.button(
                        I18nState.translations[I18nState.current_language][
                            "course.stay_current"
                        ],
                        on_click=CourseState.set_show_level_up_modal(False),
                        class_name="w-full py-4 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-2xl font-semibold transition-all",
                    ),
                    class_name="w-full",
                ),
                class_name="flex flex-col items-center text-center",
            ),
            class_name="bg-slate-900 border border-slate-700 p-10 rounded-[2.5rem] shadow-2xl max-w-md w-full relative overflow-hidden",
        ),
        class_name="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300",
    )


def course_view() -> rx.Component:
    return rx.el.div(
        rx.cond(CourseState.show_level_up_modal, level_up_modal()),
        course_header(),
        rx.el.div(
            rx.foreach(CourseState.modules, module_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="p-8 max-w-7xl mx-auto",
    )