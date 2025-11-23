import reflex as rx
from app.states.auth_state import AuthState
from app.states.main_state import MainState


def sidebar_item(text: str, icon: str, view_name: str) -> rx.Component:
    """A navigation item in the sidebar."""
    active = MainState.current_view == view_name
    return rx.el.button(
        rx.icon(
            icon,
            class_name=rx.cond(
                active, "text-orange-600", "text-gray-500 group-hover:text-gray-700"
            ),
            size=20,
        ),
        rx.el.span(text, class_name="font-medium"),
        on_click=lambda: MainState.set_view(view_name),
        class_name=rx.cond(
            active,
            "flex items-center w-full gap-3 px-3 py-2 rounded-lg bg-orange-50 text-orange-900 transition-colors",
            "flex items-center w-full gap-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-50 group transition-colors",
        ),
    )


def sidebar() -> rx.Component:
    """The responsive sidebar component."""
    return rx.el.aside(
        rx.cond(
            MainState.show_sidebar,
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/20 z-40 lg:hidden backdrop-blur-sm",
                on_click=MainState.toggle_sidebar,
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("graduation-cap", class_name="h-8 w-8 text-orange-600"),
                    rx.el.span(
                        "Teacher's",
                        class_name="text-xl font-bold text-gray-900 tracking-tight",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="h-16 flex items-center px-6 border-b border-gray-100",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.el.p(
                        "MENU",
                        class_name="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2",
                    ),
                    sidebar_item("Gradebook", "clipboard-list", "gradebook"),
                    sidebar_item("Profile", "user", "profile"),
                    class_name="flex flex-col gap-1",
                ),
                class_name="flex-1 px-3 py-6 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "SA", class_name="text-sm font-bold text-orange-600"
                            ),
                            class_name="h-8 w-8 rounded-full bg-orange-100 flex items-center justify-center shrink-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                AuthState.user["name"],
                                class_name="text-sm font-medium text-gray-900 truncate",
                            ),
                            rx.el.p("Teacher", class_name="text-xs text-gray-500"),
                            class_name="flex flex-col min-w-0",
                        ),
                        class_name="flex items-center gap-3 mb-3",
                    ),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4 mr-2"),
                        "Sign out",
                        on_click=AuthState.logout,
                        class_name="flex items-center justify-center w-full px-3 py-2 text-sm font-medium text-gray-600 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors border border-gray-200",
                    ),
                    class_name="p-4 border-t border-gray-100 bg-gray-50/50",
                ),
                class_name="mt-auto",
            ),
            class_name=rx.cond(
                MainState.show_sidebar,
                "fixed inset-y-0 left-0 z-50 w-72 bg-white border-r border-gray-200 flex flex-col transition-transform duration-300 ease-in-out translate-x-0 lg:static lg:translate-x-0 shadow-2xl lg:shadow-none",
                "fixed inset-y-0 left-0 z-50 w-72 bg-white border-r border-gray-200 flex flex-col transition-transform duration-300 ease-in-out -translate-x-full lg:static lg:translate-x-0 shadow-2xl lg:shadow-none",
            ),
        ),
        class_name="flex flex-col h-full",
    )