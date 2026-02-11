import reflex as rx
from app.states.navigation import NavState
from app.states.review import ReviewState
from app.states.i18n import I18nState


def nav_item(item: dict[str, str]) -> rx.Component:
    is_active = NavState.current_page == item["id"]
    return rx.el.button(
        rx.el.div(
            rx.icon(
                item["icon"],
                class_name=rx.cond(is_active, "text-indigo-400", "text-slate-400")
                + " h-5 w-5",
            ),
            rx.el.span(
                rx.match(
                    item["id"],
                    (
                        "home",
                        I18nState.translations[I18nState.current_language][
                            "nav.explore"
                        ],
                    ),
                    (
                        "courses",
                        I18nState.translations[I18nState.current_language][
                            "nav.courses"
                        ],
                    ),
                    (
                        "lab",
                        I18nState.translations[I18nState.current_language]["nav.lab"],
                    ),
                    (
                        "reviews",
                        I18nState.translations[I18nState.current_language][
                            "nav.reviews"
                        ],
                    ),
                    (
                        "settings",
                        I18nState.translations[I18nState.current_language][
                            "nav.settings"
                        ],
                    ),
                    item["label"],
                ),
                class_name="font-medium",
            ),
            class_name="flex items-center gap-3",
        ),
        rx.cond(
            (item["id"] == "reviews") & (ReviewState.pending_count > 0),
            rx.el.span(
                ReviewState.pending_count.to_string(),
                class_name="ml-auto bg-indigo-500 text-[10px] font-bold text-white px-2 py-0.5 rounded-full",
            ),
        ),
        on_click=lambda: NavState.set_page(item["id"]),
        class_name=rx.cond(
            is_active,
            "flex items-center justify-between w-full px-4 py-3 bg-slate-800 text-white rounded-xl transition-all border border-slate-700/50",
            "flex items-center justify-between w-full px-4 py-3 text-slate-400 hover:text-white hover:bg-slate-800/50 rounded-xl transition-all",
        ),
    )


from app.states.user_stats import UserStatsState


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("zap", class_name="text-indigo-500 h-6 w-6"),
                        class_name="bg-indigo-500/10 p-2 rounded-lg",
                    ),
                    rx.el.h1(
                        "SkillForge",
                        class_name="text-xl font-bold tracking-tight text-white",
                    ),
                    class_name="flex items-center gap-3 px-2",
                ),
                rx.el.button(
                    rx.el.span(I18nState.current_flag, class_name="text-xl"),
                    on_click=rx.cond(
                        I18nState.current_language == "en",
                        I18nState.set_language("es"),
                        I18nState.set_language("en"),
                    ),
                    class_name="p-2 hover:bg-slate-800 rounded-xl transition-all border border-slate-800",
                ),
                class_name="flex items-center justify-between mb-10 p-2",
            ),
            rx.el.div(
                rx.el.p(
                    I18nState.translations[I18nState.current_language]["nav.menu"],
                    class_name="text-[10px] font-bold text-slate-500 tracking-widest mb-4 px-4",
                ),
                rx.el.nav(
                    rx.foreach(NavState.nav_items, nav_item),
                    class_name="flex flex-col gap-1",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src="https://api.dicebear.com/9.x/notionists/svg?seed=Felix",
                            class_name="h-10 w-10 rounded-full bg-slate-700",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Alex Rivera",
                                    class_name="text-sm font-semibold text-white",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "flame", class_name="h-3 w-3 text-orange-500"
                                    ),
                                    rx.el.span(
                                        UserStatsState.current_streak.to_string(),
                                        class_name="text-[10px] font-bold text-orange-500",
                                    ),
                                    class_name="flex items-center gap-0.5",
                                ),
                                class_name="flex items-center justify-between w-full",
                            ),
                            rx.el.p(
                                UserStatsState.level_name,
                                class_name="text-[10px] text-indigo-400 font-bold uppercase tracking-wider",
                            ),
                            class_name="flex flex-col flex-1",
                        ),
                        class_name="flex items-center gap-3 p-3 bg-slate-800/40 rounded-2xl border border-slate-700/30",
                    ),
                    rx.el.div(
                        rx.el.div(
                            class_name="h-full bg-indigo-500",
                            style={"width": f"{UserStatsState.level_progress}%"},
                        ),
                        class_name="w-full h-1 bg-slate-700 mt-2 rounded-full overflow-hidden",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="mt-auto pt-6",
            ),
            class_name="flex flex-col h-full p-6",
        ),
        class_name="fixed left-0 top-0 h-screen w-64 bg-slate-900 border-r border-slate-800 z-10 hidden md:block",
    )