import reflex as rx
from app.states.main_state import MainState


def assignment_info_card(assignment: dict) -> rx.Component:
    """Display a card for a single teaching assignment."""
    return rx.el.div(
        rx.el.div(
            rx.icon("book-open", class_name="h-6 w-6 text-orange-600"),
            class_name="h-10 w-10 rounded-lg bg-orange-100 flex items-center justify-center mb-4",
        ),
        rx.el.h3(
            assignment["subject"],
            class_name="text-lg font-bold text-gray-900 mb-2 line-clamp-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Grade", class_name="text-xs font-semibold text-gray-400 uppercase"
                ),
                rx.el.p(
                    assignment["grade"], class_name="text-sm font-medium text-gray-700"
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(class_name="w-px h-8 bg-gray-100 mx-4"),
            rx.el.div(
                rx.el.span(
                    "Section",
                    class_name="text-xs font-semibold text-gray-400 uppercase",
                ),
                rx.el.p(
                    assignment["section"],
                    class_name="text-sm font-medium text-gray-700",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center mt-2",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200 group",
    )


def profile_view() -> rx.Component:
    """The main profile view component."""
    return rx.el.div(
        rx.el.h1("Teacher Profile", class_name="text-2xl font-bold text-gray-900 mb-6"),
        rx.el.div(
            rx.el.div(
                rx.el.span("SA", class_name="text-3xl font-bold text-orange-600"),
                class_name="h-24 w-24 rounded-full bg-orange-100 flex items-center justify-center border-4 border-white shadow-sm shrink-0",
            ),
            rx.el.div(
                rx.el.h2(
                    f"{MainState.teacher_data['first_name']} {MainState.teacher_data['last_name']}",
                    class_name="text-2xl font-bold text-gray-900 mb-1",
                ),
                rx.el.p(
                    "High School Science & Math Department",
                    class_name="text-gray-500 font-medium mb-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("mail", class_name="h-4 w-4 text-gray-400"),
                        rx.el.span(
                            "sarah.anderson@school.edu",
                            class_name="text-sm text-gray-600",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.icon("building-2", class_name="h-4 w-4 text-gray-400"),
                        rx.el.span(
                            "Lincoln High School", class_name="text-sm text-gray-600"
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    class_name="flex flex-col sm:flex-row gap-3",
                ),
                class_name="flex flex-col justify-center",
            ),
            class_name="flex flex-col sm:flex-row items-center sm:items-start gap-6 p-8 bg-white rounded-xl border border-gray-200 shadow-sm mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Current Assignments", class_name="text-xl font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.foreach(
                    MainState.teacher_data["high_school_assignments"],
                    assignment_info_card,
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
        ),
        class_name="animate-fade-in max-w-5xl mx-auto w-full",
    )