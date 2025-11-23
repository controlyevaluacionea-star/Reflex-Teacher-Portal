import reflex as rx
from app.states.main_state import MainState
from app.components.sidebar import sidebar
from app.components.profile import profile_view
from app.components.student_loader import student_loader
from app.components.shared import dashboard_loading


def mobile_header() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("menu", class_name="h-6 w-6 text-gray-600"),
            on_click=MainState.toggle_sidebar,
            class_name="p-2 hover:bg-gray-100 rounded-lg lg:hidden",
        ),
        rx.el.div(
            rx.icon("graduation-cap", class_name="h-6 w-6 text-orange-600"),
            rx.el.span("Teacher's", class_name="text-lg font-bold text-gray-900 ml-2"),
            class_name="flex items-center lg:hidden",
        ),
        rx.el.div(class_name="w-10 lg:hidden"),
        class_name="h-16 bg-white border-b border-gray-100 flex items-center justify-between px-4 lg:hidden sticky top-0 z-30",
    )


def gradebook_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Gradebook", class_name="text-2xl font-bold text-gray-900 mb-6"),
        student_loader(),
        class_name="animate-fade-in max-w-6xl mx-auto w-full",
    )


def teacher_dashboard() -> rx.Component:
    """The main dashboard page for teachers."""
    return rx.el.div(
        rx.cond(
            MainState.is_loading,
            dashboard_loading(),
            rx.el.div(
                sidebar(),
                rx.el.div(
                    mobile_header(),
                    rx.el.main(
                        rx.match(
                            MainState.current_view,
                            ("gradebook", gradebook_view()),
                            ("profile", profile_view()),
                            gradebook_view(),
                        ),
                        class_name="flex-1 p-4 md:p-8 overflow-y-auto",
                    ),
                    class_name="flex-1 flex flex-col min-w-0 h-screen bg-gray-50",
                ),
                class_name="flex h-screen w-full overflow-hidden",
            ),
        ),
        class_name="font-['Open_Sans']",
    )