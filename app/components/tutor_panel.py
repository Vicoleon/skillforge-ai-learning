import reflex as rx
from app.states.tutor import TutorState


def style_button(label: str, value: str, icon: str) -> rx.Component:
    is_selected = TutorState.explanation_style == value
    return rx.el.button(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 mb-1"),
            rx.el.span(label, class_name="text-[10px] font-bold uppercase"),
            class_name="flex flex-col items-center",
        ),
        on_click=lambda: TutorState.set_style(value),
        class_name=rx.cond(
            is_selected,
            "flex-1 py-2 bg-indigo-600 text-white rounded-xl transition-all shadow-lg shadow-indigo-600/20 scale-105",
            "flex-1 py-2 bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 rounded-xl transition-all border border-slate-700",
        ),
    )


def chat_bubble(message: dict) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.div(
            rx.markdown(
                message["content"],
                class_name=rx.cond(
                    is_user,
                    "prose prose-invert prose-sm text-white [&_pre]:bg-indigo-700/50",
                    "prose prose-invert prose-sm text-slate-200 [&_pre]:bg-slate-900/50 [&_strong]:text-indigo-300",
                ),
            ),
            class_name=rx.cond(
                is_user,
                "bg-indigo-600 p-4 rounded-2xl rounded-tr-sm text-sm shadow-md",
                "bg-slate-800 p-4 rounded-2xl rounded-tl-sm text-sm border border-slate-700 shadow-sm",
            ),
        ),
        class_name=rx.cond(
            is_user, "flex justify-end mb-4 ml-12", "flex justify-start mb-4 mr-12"
        ),
    )


def tutor_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "bot", class_name="h-6 w-6 text-indigo-400 mr-3 animate-pulse"
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "AI Coach", class_name="font-bold text-white leading-none"
                        ),
                        rx.el.p(
                            "Context-Aware Help",
                            class_name="text-xs text-slate-400 mt-1",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-5 w-5 text-slate-400 hover:text-white"),
                    on_click=TutorState.toggle_tutor,
                    class_name="p-2 hover:bg-slate-800 rounded-lg transition-colors",
                ),
                class_name="flex items-center justify-between p-6 border-b border-slate-700/50 bg-slate-900/95 backdrop-blur supports-[backdrop-filter]:bg-slate-900/75 sticky top-0 z-10",
            ),
            rx.el.div(
                style_button("Simple", "simple", "baby"),
                style_button("Example", "example", "code"),
                style_button("Deep Dive", "advanced", "brain-circuit"),
                class_name="flex gap-2 p-4 bg-slate-900/50 border-b border-slate-800",
            ),
            rx.el.div(
                rx.foreach(TutorState.messages, chat_bubble),
                rx.cond(
                    TutorState.is_loading,
                    rx.el.div(
                        rx.el.div(
                            class_name="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.3s]"
                        ),
                        rx.el.div(
                            class_name="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.15s]"
                        ),
                        rx.el.div(
                            class_name="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"
                        ),
                        class_name="flex gap-1 p-4 bg-slate-800 rounded-2xl w-fit mb-4 rounded-tl-sm border border-slate-700",
                    ),
                ),
                class_name="flex-1 overflow-y-auto p-6 bg-slate-900/30 scroll-smooth",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.input(
                        name="message",
                        placeholder="Ask about this module...",
                        class_name="flex-1 bg-slate-800 text-white placeholder:text-slate-500 text-sm px-4 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 border border-slate-700",
                        default_value=TutorState.current_input,
                        key=TutorState.current_input,
                    ),
                    rx.el.button(
                        rx.icon(
                            "send-horizontal", class_name="h-5 w-5 text-white ml-0.5"
                        ),
                        type="submit",
                        disabled=TutorState.is_loading,
                        class_name="bg-indigo-600 hover:bg-indigo-500 p-3 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed",
                    ),
                    class_name="flex gap-2",
                ),
                on_submit=TutorState.send_message,
                reset_on_submit=True,
                class_name="p-4 border-t border-slate-800 bg-slate-900",
            ),
            class_name="flex flex-col h-full bg-slate-950 shadow-2xl",
        ),
        class_name=rx.cond(
            TutorState.is_open,
            "fixed inset-y-0 right-0 w-full md:w-[400px] z-[60] transform transition-transform duration-300 ease-in-out translate-x-0 shadow-[-10px_0_30px_-10px_rgba(0,0,0,0.5)]",
            "fixed inset-y-0 right-0 w-full md:w-[400px] z-[60] transform transition-transform duration-300 ease-in-out translate-x-full",
        ),
    )