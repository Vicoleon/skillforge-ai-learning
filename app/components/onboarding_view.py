import reflex as rx
from reflex_google_auth import google_login
from app.states.onboarding import OnboardingState
from app.states.i18n import I18nState
from app.states.auth import AuthState


def feature_card(icon: str, title: str, desc: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-8 w-8 text-indigo-500 mb-4"),
        rx.el.h3(title, class_name="text-lg font-bold text-white mb-2"),
        rx.el.p(desc, class_name="text-sm text-slate-400"),
        class_name="p-6 bg-slate-900/50 border border-slate-800 rounded-2xl hover:border-indigo-500/30 transition-all",
    )


def landing_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("zap", class_name="h-12 w-12 text-indigo-500"),
                        rx.el.h1(
                            "SkillForge",
                            class_name="text-2xl font-bold tracking-tight text-white",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.el.button(
                        rx.el.span(I18nState.current_flag, class_name="text-xl mr-2"),
                        rx.el.span(
                            rx.cond(I18nState.current_language == "en", "ES", "EN"),
                            class_name="text-xs font-bold text-slate-400",
                        ),
                        on_click=rx.cond(
                            I18nState.current_language == "en",
                            I18nState.set_language("es"),
                            I18nState.set_language("en"),
                        ),
                        class_name="p-3 hover:bg-slate-800 rounded-2xl transition-all border border-slate-800 flex items-center bg-slate-900/50",
                    ),
                    class_name="flex items-center justify-between mb-8",
                ),
                rx.el.h2(
                    I18nState.translations[I18nState.current_language][
                        "landing.hero_title"
                    ],
                    class_name="text-5xl md:text-6xl font-black text-white mb-6 leading-tight tracking-tight",
                ),
                rx.el.p(
                    I18nState.translations[I18nState.current_language][
                        "landing.hero_subtitle"
                    ],
                    class_name="text-xl text-slate-400 mb-10 max-w-2xl",
                ),
                rx.el.div(google_login(), class_name="transform scale-110 origin-left"),
                class_name="flex flex-col justify-center min-h-[60vh]",
            ),
            rx.el.div(
                feature_card(
                    "brain-circuit",
                    I18nState.translations[I18nState.current_language][
                        "landing.feature_adaptive_title"
                    ],
                    I18nState.translations[I18nState.current_language][
                        "landing.feature_adaptive_desc"
                    ],
                ),
                feature_card(
                    "message-circle",
                    I18nState.translations[I18nState.current_language][
                        "landing.feature_tutor_title"
                    ],
                    I18nState.translations[I18nState.current_language][
                        "landing.feature_tutor_desc"
                    ],
                ),
                feature_card(
                    "target",
                    I18nState.translations[I18nState.current_language][
                        "landing.feature_quiz_title"
                    ],
                    I18nState.translations[I18nState.current_language][
                        "landing.feature_quiz_desc"
                    ],
                ),
                feature_card(
                    "bar-chart-2",
                    I18nState.translations[I18nState.current_language][
                        "landing.feature_progress_title"
                    ],
                    I18nState.translations[I18nState.current_language][
                        "landing.feature_progress_desc"
                    ],
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full mt-12 mb-20",
            ),
            class_name="max-w-5xl mx-auto px-6 pt-20",
        ),
        class_name="min-h-screen bg-slate-950 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/20 via-slate-950 to-slate-950",
    )


def diagnostic_chat() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("bot", class_name="h-5 w-5 text-indigo-400"),
                class_name="h-8 w-8 rounded-full bg-indigo-500/10 flex items-center justify-center shrink-0 border border-indigo-500/20",
            ),
            rx.el.div(
                rx.el.p(
                    I18nState.translations[I18nState.current_language][
                        "onboarding.skill_question"
                    ],
                    class_name="text-slate-200 text-sm leading-relaxed",
                ),
                class_name="bg-slate-800 border border-slate-700 p-4 rounded-2xl rounded-tl-none max-w-md shadow-xl",
            ),
            class_name="flex gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500",
        ),
        rx.el.div(
            rx.el.button(
                I18nState.translations[I18nState.current_language][
                    "onboarding.beginner"
                ],
                on_click=lambda: OnboardingState.select_skill("Beginner"),
                class_name=rx.cond(
                    OnboardingState.skill_level == "Beginner",
                    "px-6 py-3 bg-indigo-600 text-white rounded-xl border border-indigo-400 shadow-[0_0_20px_rgba(79,70,229,0.3)] transition-all",
                    "px-6 py-3 bg-slate-800 text-slate-300 rounded-xl border border-slate-700 hover:border-indigo-500/50 hover:bg-slate-700/50 transition-all",
                ),
            ),
            rx.el.button(
                I18nState.translations[I18nState.current_language][
                    "onboarding.intermediate"
                ],
                on_click=lambda: OnboardingState.select_skill("Intermediate"),
                class_name=rx.cond(
                    OnboardingState.skill_level == "Intermediate",
                    "px-6 py-3 bg-indigo-600 text-white rounded-xl border border-indigo-400 shadow-[0_0_20px_rgba(79,70,229,0.3)] transition-all",
                    "px-6 py-3 bg-slate-800 text-slate-300 rounded-xl border border-slate-700 hover:border-indigo-500/50 hover:bg-slate-700/50 transition-all",
                ),
            ),
            rx.el.button(
                I18nState.translations[I18nState.current_language][
                    "onboarding.advanced"
                ],
                on_click=lambda: OnboardingState.select_skill("Advanced"),
                class_name=rx.cond(
                    OnboardingState.skill_level == "Advanced",
                    "px-6 py-3 bg-indigo-600 text-white rounded-xl border border-indigo-400 shadow-[0_0_20px_rgba(79,70,229,0.3)] transition-all",
                    "px-6 py-3 bg-slate-800 text-slate-300 rounded-xl border border-slate-700 hover:border-indigo-500/50 hover:bg-slate-700/50 transition-all",
                ),
            ),
            class_name="flex flex-wrap gap-3 mt-6 ml-12 animate-in fade-in slide-in-from-bottom-2 duration-700 delay-300",
        ),
        class_name="w-full mt-12 flex flex-col items-center",
    )


def onboarding_view() -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        I18nState.translations[I18nState.current_language][
                            "onboarding.title"
                        ],
                        class_name="text-4xl md:text-5xl font-bold text-white mb-8 text-center tracking-tight",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "search",
                                    class_name="absolute left-6 top-1/2 -translate-y-1/2 text-slate-400 h-6 w-6",
                                ),
                                rx.el.input(
                                    name="search_query",
                                    placeholder=I18nState.translations[
                                        I18nState.current_language
                                    ]["onboarding.placeholder"],
                                    class_name="w-full bg-slate-800/50 border border-slate-700 text-white py-5 pl-16 pr-6 rounded-3xl focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-500 text-lg shadow-2xl",
                                    default_value=OnboardingState.search_query,
                                    key=OnboardingState.search_query,
                                ),
                                class_name="relative flex-1",
                            ),
                            rx.el.button(
                                rx.cond(
                                    OnboardingState.is_processing,
                                    rx.icon(
                                        "squirrel",
                                        class_name="h-6 w-6 animate-spin text-white",
                                    ),
                                    rx.icon(
                                        "arrow-right", class_name="h-6 w-6 text-white"
                                    ),
                                ),
                                type="submit",
                                disabled=OnboardingState.is_processing,
                                class_name="bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 p-5 rounded-3xl transition-all shadow-lg hover:shadow-indigo-500/20 disabled:opacity-50",
                            ),
                            class_name="flex w-full max-w-3xl gap-4",
                        ),
                        on_submit=OnboardingState.submit_topic,
                        class_name="w-full flex justify-center",
                    ),
                    class_name=rx.cond(
                        OnboardingState.is_diagnostic_shown,
                        "opacity-40 scale-95 blur-[2px] pointer-events-none transition-all duration-700",
                        "transition-all duration-700",
                    ),
                ),
                rx.cond(
                    OnboardingState.is_diagnostic_shown
                    & ~OnboardingState.is_processing,
                    diagnostic_chat(),
                ),
                rx.cond(
                    OnboardingState.is_diagnostic_shown & OnboardingState.is_processing,
                    rx.el.div(
                        rx.icon(
                            "squirrel",
                            class_name="h-12 w-12 text-indigo-500 animate-spin mb-4",
                        ),
                        rx.el.h3(
                            I18nState.translations[I18nState.current_language][
                                "onboarding.preparing"
                            ],
                            class_name="text-xl font-semibold text-white animate-pulse",
                        ),
                        rx.el.p(
                            I18nState.translations[I18nState.current_language][
                                "onboarding.generating_questions"
                            ].replace("{topic}", OnboardingState.search_query),
                            class_name="text-slate-500 mt-2",
                        ),
                        class_name="flex flex-col items-center justify-center mt-12 animate-in fade-in duration-500",
                    ),
                ),
                class_name="flex flex-col items-center justify-center min-h-[80vh] w-full",
            ),
            class_name="max-w-5xl mx-auto w-full px-4 pt-12",
        ),
        landing_page(),
    )