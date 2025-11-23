import reflex as rx
import reflex_enterprise as rxe
from app.states.main_state import MainState, Student, Activity
from app.components.add_activity_dialog import add_activity_dialog


def grade_input(student: Student, activity: Activity) -> rx.Component:
    """An individual grade input cell."""
    return rx.el.div(
        rx.el.input(
            type="text",
            on_change=lambda val: MainState.set_grade(
                student["id"], activity["id"], val
            ),
            on_blur=MainState.save_grade(student["id"], activity["id"]),
            class_name="w-[40px] text-center bg-transparent border-b border-transparent focus:border-orange-500 hover:border-gray-300 outline-none text-sm font-medium text-gray-700 p-1 transition-colors placeholder-gray-300",
            placeholder="-",
            default_value=student["grades"][activity["id"]],
        ),
        class_name="w-32 shrink-0 flex justify-center p-2 border-r border-gray-100 last:border-r-0",
    )


def activity_header(activity: Activity) -> rx.Component:
    """Header for an activity column with tooltip."""
    return rx.el.div(
        rx.el.div(
            rx.el.span(activity["description"], class_name="truncate max-w-[100px]"),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        activity["description"], class_name="font-bold text-white mb-1"
                    ),
                    rx.el.p(activity["date"], class_name="text-white/80 text-xs"),
                    class_name="bg-gray-800 text-white text-xs rounded px-2 py-1 shadow-lg whitespace-nowrap",
                ),
                class_name="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block z-10",
            ),
            class_name="relative group cursor-help flex justify-center",
        ),
        class_name="w-32 shrink-0 px-2 py-3 text-center text-xs font-semibold text-gray-500 uppercase tracking-wider bg-gray-50 border-r border-gray-200 last:border-r-0 flex items-center justify-center",
    )


@rx.memo
def draggable_student_row(student: Student) -> rx.Component:
    """A single draggable row in the gradebook."""
    drop_params = rxe.dnd.DropTarget.collected_params
    return rxe.dnd.draggable(
        rxe.dnd.drop_target(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "grip-horizontal",
                        class_name="h-4 w-4 text-gray-300 group-hover:text-gray-500",
                    ),
                    class_name="w-12 shrink-0 flex items-center justify-center border-r border-gray-100 p-3 cursor-grab active:cursor-grabbing",
                ),
                rx.el.div(
                    rx.el.div(
                        student["name"], class_name="font-medium text-gray-900 truncate"
                    ),
                    class_name="w-64 shrink-0 flex items-center px-4 py-3 border-r border-gray-100",
                ),
                rx.foreach(
                    MainState.activities,
                    lambda activity: grade_input(student, activity),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            student["average"],
                            class_name=rx.cond(
                                student["average"] >= 70,
                                "inline-flex items-center justify-center w-8 h-6 bg-green-100 text-green-700 text-xs font-bold rounded",
                                rx.cond(
                                    student["average"] > 0,
                                    "inline-flex items-center justify-center w-8 h-6 bg-red-100 text-red-700 text-xs font-bold rounded",
                                    "text-gray-300 font-medium text-sm",
                                ),
                            ),
                        ),
                        class_name="flex items-center justify-center w-full",
                    ),
                    class_name="w-24 shrink-0 flex items-center justify-center px-4 py-3 border-l border-gray-100 ml-auto",
                ),
                class_name=rx.cond(
                    drop_params.is_over,
                    "flex min-w-full bg-orange-50 border-b border-orange-300 relative z-10 transition-colors",
                    "flex min-w-full bg-white border-b border-gray-100 hover:bg-gray-50 group transition-colors",
                ),
            ),
            accept=["student"],
            on_drop=lambda data: MainState.reorder_students(data["id"], student["id"]),
        ),
        type="student",
        item={"id": student["id"]},
        key=student["id"],
    )


def student_loader() -> rx.Component:
    """Component for selecting class and loading students."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Subject",
                        class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
                    ),
                    rx.el.select(
                        rx.el.option("Select Subject", value="", disabled=True),
                        rx.foreach(
                            MainState.assignment_options,
                            lambda option: rx.el.option(option, value=option),
                        ),
                        value=MainState.selected_subject,
                        on_change=MainState.set_selected_subject,
                        class_name="w-full bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-500 focus:border-orange-500 block p-2.5 transition-colors shadow-sm",
                    ),
                    class_name="w-full sm:w-64",
                ),
                rx.cond(
                    MainState.show_section_selector,
                    rx.el.div(
                        rx.el.label(
                            "Section",
                            class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
                        ),
                        rx.el.select(
                            rx.el.option("Select Section", value="", disabled=True),
                            rx.foreach(
                                MainState.section_options,
                                lambda option: rx.el.option(option, value=option),
                            ),
                            value=MainState.selected_section,
                            on_change=MainState.set_selected_section,
                            class_name="w-full bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-500 focus:border-orange-500 block p-2.5 transition-colors shadow-sm",
                        ),
                        class_name="w-full sm:w-48 animate-fade-in",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "\xa0",
                        class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
                    ),
                    rx.el.button(
                        rx.cond(
                            MainState.is_loading_students,
                            rx.el.div(
                                rx.spinner(size="2", class_name="text-white mr-2"),
                                "Loading...",
                                class_name="flex items-center",
                            ),
                            rx.el.div(
                                rx.icon("users", class_name="h-4 w-4 mr-2"),
                                "Load Students",
                                class_name="flex items-center",
                            ),
                        ),
                        on_click=MainState.load_students,
                        disabled=MainState.is_loading_students
                        | (MainState.selected_subject == "")
                        | MainState.show_section_selector
                        & (MainState.selected_section == ""),
                        class_name="h-[42px] px-5 bg-orange-600 hover:bg-orange-700 text-white text-sm font-medium rounded-lg transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-orange-600 flex items-center justify-center min-w-[140px]",
                    ),
                    class_name="w-full sm:w-auto",
                ),
                class_name="flex flex-col sm:flex-row items-start sm:items-end gap-4 w-full",
            ),
            class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mb-8",
        ),
        rx.cond(
            MainState.students.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Gradebook",
                            class_name="text-xl font-bold text-gray-900 mr-4",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="h-4 w-4 mr-1.5"),
                            "New Activity",
                            on_click=lambda: MainState.toggle_add_activity_dialog(True),
                            class_name="inline-flex items-center px-3 py-1.5 bg-white border border-gray-200 text-gray-700 text-xs font-semibold rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors shadow-sm",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.el.span(
                            f"{MainState.students.length()} Students",
                            class_name="px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs font-medium border border-gray-200",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    class_name="flex items-center justify-between mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            "#",
                            class_name="w-12 shrink-0 px-2 py-3 text-center text-xs font-semibold text-gray-500 uppercase tracking-wider border-r border-gray-100 last:border-r-0",
                        ),
                        rx.el.div(
                            "Student Name",
                            class_name="w-64 shrink-0 px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider border-r border-gray-100 last:border-r-0",
                        ),
                        rx.foreach(MainState.activities, activity_header),
                        rx.el.div(
                            "Avg",
                            class_name="w-24 shrink-0 px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase tracking-wider border-l border-gray-100 ml-auto",
                        ),
                        class_name="flex min-w-full border-b bg-gray-50 sticky top-0 z-20",
                    ),
                    rx.el.div(
                        rx.foreach(
                            MainState.students,
                            lambda student: draggable_student_row(
                                student=student, key=student["id"]
                            ),
                        ),
                        class_name="flex flex-col min-w-full divide-y divide-gray-100",
                    ),
                    class_name="w-full overflow-x-auto border rounded-xl shadow-sm bg-white",
                ),
                class_name="animate-fade-in",
            ),
        ),
        add_activity_dialog(),
        class_name="w-full",
    )