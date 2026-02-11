import reflex as rx
from app.states.onboarding import OnboardingState


def diagnostic_chat() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("bot", class_name="h-5 w-5 text-indigo-400"),
                class_name="h-8 w-8 rounded-full bg-indigo-500/10 flex items-center justify-center shrink-0 border border-indigo-500/20",
            ),
            rx.el.div(
                rx.el.p(
                    f"Great! Let's get you started with {OnboardingState.search_query}. To personalize your learning path, how much experience do you have with this topic?",
                    class_name="text-slate-200 text-sm leading-relaxed",
                ),
                class_name="bg-slate-800 border border-slate-700 p-4 rounded-2xl rounded-tl-none max-w-md shadow-xl",
            ),
            class_name="flex gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500",
        ),
        rx.el.div(
            rx.el.button(
                "Beginner",
                on_click=lambda: OnboardingState.select_skill("Beginner"),
                class_name=rx.cond(
                    OnboardingState.skill_level == "Beginner",
                    "px-6 py-3 bg-indigo-600 text-white rounded-xl border border-indigo-400 shadow-[0_0_20px_rgba(79,70,229,0.3)] transition-all",
                    "px-6 py-3 bg-slate-800 text-slate-300 rounded-xl border border-slate-700 hover:border-indigo-500/50 hover:bg-slate-700/50 transition-all",
                ),
            ),
            rx.el.button(
                "Intermediate",
                on_click=lambda: OnboardingState.select_skill("Intermediate"),
                class_name=rx.cond(
                    OnboardingState.skill_level == "Intermediate",
                    "px-6 py-3 bg-indigo-600 text-white rounded-xl border border-indigo-400 shadow-[0_0_20px_rgba(79,70,229,0.3)] transition-all",
                    "px-6 py-3 bg-slate-800 text-slate-300 rounded-xl border border-slate-700 hover:border-indigo-500/50 hover:bg-slate-700/50 transition-all",
                ),
            ),
            rx.el.button(
                "Advanced",
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
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "What do you want to learn today?",
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
                                placeholder="Master Rust, learn Neural Networks, or explore AWS...",
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
                                rx.icon("arrow-right", class_name="h-6 w-6 text-white"),
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
                OnboardingState.is_diagnostic_shown & ~OnboardingState.is_processing,
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
                        "Preparing your diagnostic assessment...",
                        class_name="text-xl font-semibold text-white animate-pulse",
                    ),
                    rx.el.p(
                        "We are generating questions to test your knowledge of "
                        + OnboardingState.search_query,
                        class_name="text-slate-500 mt-2",
                    ),
                    class_name="flex flex-col items-center justify-center mt-12 animate-in fade-in duration-500",
                ),
            ),
            class_name="flex flex-col items-center justify-center min-h-[80vh] w-full",
        ),
        class_name="max-w-5xl mx-auto w-full px-4 pt-12",
    )