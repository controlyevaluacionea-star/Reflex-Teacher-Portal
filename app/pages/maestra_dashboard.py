import reflex as rx
from app.states.auth_state import AuthState
from app.states.maestra_state import MaestraState
from app.components.shared import dashboard_loading


def student_card(student: dict) -> rx.Component:
    """A card component displaying student information."""
    is_selected = MaestraState.selected_student_id == student["id"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    student["initials"], class_name="text-xl font-bold text-emerald-700"
                ),
                class_name="h-14 w-14 rounded-full bg-emerald-100 flex items-center justify-center border-2 border-white shadow-sm shrink-0",
            ),
            rx.el.div(
                rx.el.h3(
                    student["name"],
                    class_name="text-base font-bold text-gray-900 line-clamp-1",
                ),
                rx.el.p(
                    f"{student['grade']} - {student['section']}",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Overall Average",
                    class_name="text-xs font-semibold text-gray-400 uppercase tracking-wide",
                ),
                rx.el.span(
                    student["overall_average"],
                    class_name=rx.cond(
                        student["overall_average"] >= 70,
                        "px-2.5 py-0.5 rounded-full bg-green-100 text-green-700 text-xs font-bold",
                        "px-2.5 py-0.5 rounded-full bg-red-100 text-red-700 text-xs font-bold",
                    ),
                ),
                class_name="flex items-center justify-between w-full",
            ),
            class_name="pt-4 border-t border-gray-100",
        ),
        on_click=lambda: MaestraState.select_student(student["id"]),
        class_name=rx.cond(
            is_selected,
            "bg-emerald-50 p-5 rounded-xl border-2 border-emerald-500 shadow-md cursor-pointer transition-all duration-200 transform scale-[1.02]",
            "bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-emerald-200 cursor-pointer transition-all duration-200",
        ),
    )


def controls_section() -> rx.Component:
    """Section with grade/section selectors and load button."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Grade Level",
                    class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
                ),
                rx.el.select(
                    rx.el.option("Select Grade", value="", disabled=True),
                    rx.foreach(
                        MaestraState.grade_options,
                        lambda option: rx.el.option(option, value=option),
                    ),
                    value=MaestraState.selected_grade,
                    on_change=MaestraState.set_selected_grade,
                    class_name="w-full bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block p-2.5 transition-colors shadow-sm",
                ),
                class_name="w-full sm:w-64",
            ),
            rx.el.div(
                rx.el.label(
                    "Section",
                    class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
                ),
                rx.el.select(
                    rx.el.option("Select Section", value="", disabled=True),
                    rx.foreach(
                        MaestraState.section_options,
                        lambda option: rx.el.option(option, value=option),
                    ),
                    value=MaestraState.selected_section,
                    on_change=MaestraState.set_selected_section,
                    class_name="w-full bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block p-2.5 transition-colors shadow-sm",
                ),
                class_name="w-full sm:w-64",
            ),
            rx.el.div(
                rx.el.label(
                    "\xa0",
                    class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
                ),
                rx.el.button(
                    rx.cond(
                        MaestraState.is_loading_students,
                        rx.el.div(
                            rx.spinner(size="2", class_name="text-white mr-2"),
                            "Loading...",
                            class_name="flex items-center",
                        ),
                        rx.el.div(
                            rx.icon("search", class_name="h-4 w-4 mr-2"),
                            "Load Students",
                            class_name="flex items-center",
                        ),
                    ),
                    on_click=MaestraState.load_students_for_grade_section,
                    disabled=MaestraState.is_loading_students
                    | (MaestraState.selected_grade == "")
                    | (MaestraState.selected_section == ""),
                    class_name="h-[42px] px-6 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium rounded-lg transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[140px]",
                ),
                class_name="w-full sm:w-auto",
            ),
            class_name="flex flex-col sm:flex-row items-start sm:items-end gap-4",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mb-8",
    )


def form_field(
    label: str,
    value: str,
    field_key: str,
    icon: str,
    placeholder: str = "",
    type: str = "text",
) -> rx.Component:
    """Helper for rendering a styled form field with icon."""
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2",
        ),
        rx.el.div(
            rx.icon(
                icon,
                class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                size=16,
            ),
            rx.el.input(
                type=type,
                default_value=value,
                placeholder=placeholder,
                on_change=lambda v: MaestraState.update_editing_student(field_key, v),
                class_name="w-full pl-10 pr-4 py-2.5 rounded-lg bg-gray-50 border border-gray-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition-all text-gray-900 text-sm placeholder-gray-400",
            ),
            class_name="relative",
        ),
        class_name="mb-5",
    )


def textarea_field(
    label: str, value: str, field_key: str, placeholder: str = ""
) -> rx.Component:
    """Helper for rendering a styled textarea."""
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2",
        ),
        rx.el.textarea(
            default_value=value,
            placeholder=placeholder,
            on_change=lambda v: MaestraState.update_editing_student(field_key, v),
            class_name="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition-all text-gray-900 min-h-[120px] text-sm resize-none placeholder-gray-400",
        ),
        class_name="mb-6",
    )


def edit_student_panel() -> rx.Component:
    """Side panel for editing student details with slide-in animation."""
    is_open = MaestraState.selected_student_id
    return rx.el.div(
        rx.el.div(
            class_name=rx.cond(
                is_open,
                "absolute inset-0 bg-gray-900/20 backdrop-blur-sm transition-opacity duration-300 opacity-100 pointer-events-auto",
                "absolute inset-0 bg-gray-900/0 backdrop-blur-none transition-opacity duration-300 opacity-0 pointer-events-none",
            ),
            on_click=MaestraState.cancel_editing,
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Edit Student Details", class_name="text-lg font-bold text-gray-900"
                ),
                rx.el.button(
                    rx.icon("x", size=20),
                    on_click=MaestraState.cancel_editing,
                    class_name="text-gray-500 hover:text-gray-700 p-1.5 hover:bg-gray-100 rounded-full transition-colors",
                ),
                class_name="flex items-center justify-between p-6 border-b border-gray-100 bg-white sticky top-0 z-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            MaestraState.editing_student["initials"],
                            class_name="text-3xl font-bold text-emerald-700",
                        ),
                        class_name="h-24 w-24 rounded-full bg-emerald-100 flex items-center justify-center border-4 border-white shadow-lg mx-auto mb-4",
                    ),
                    rx.el.h4(
                        MaestraState.editing_student["name"],
                        class_name="text-xl font-bold text-gray-900 text-center",
                    ),
                    rx.el.p(
                        f"{MaestraState.editing_student['grade']} - {MaestraState.editing_student['section']}",
                        class_name="text-sm text-gray-500 text-center mb-2",
                    ),
                    rx.el.span(
                        "Active Student",
                        class_name="px-3 py-1 rounded-full bg-emerald-100 text-emerald-700 text-xs font-bold mx-auto block w-fit",
                    ),
                    class_name="flex flex-col items-center mb-8 bg-gradient-to-b from-gray-50 to-white p-8 border-b border-gray-100",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h5(
                            "Personal Information",
                            class_name="text-sm font-bold text-gray-900 mb-4 flex items-center gap-2",
                        ),
                        form_field(
                            "Full Name",
                            MaestraState.editing_student["name"],
                            "name",
                            "user",
                        ),
                        form_field(
                            "Contact Email",
                            MaestraState.editing_student["contact_email"],
                            "contact_email",
                            "mail",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.h5(
                            "Guardian Information",
                            class_name="text-sm font-bold text-gray-900 mb-4 flex items-center gap-2",
                        ),
                        form_field(
                            "Guardian Name",
                            MaestraState.editing_student["parent_name"],
                            "parent_name",
                            "users",
                        ),
                        form_field(
                            "Phone Number",
                            MaestraState.editing_student["parent_phone"],
                            "parent_phone",
                            "phone",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.h5(
                            "Teacher Notes",
                            class_name="text-sm font-bold text-gray-900 mb-4 flex items-center gap-2",
                        ),
                        textarea_field(
                            "Academic Performance Notes",
                            MaestraState.editing_student["academic_notes"],
                            "academic_notes",
                            "Observations on grades and class participation...",
                        ),
                        textarea_field(
                            "Behavioral Observations",
                            MaestraState.editing_student["behavioral_notes"],
                            "behavioral_notes",
                            "Notes on conduct and social interaction...",
                        ),
                    ),
                    class_name="px-6 pb-24",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=MaestraState.cancel_editing,
                    class_name="px-5 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors",
                ),
                rx.el.button(
                    rx.el.div(
                        rx.icon("save", size=16, class_name="mr-2"),
                        "Save Changes",
                        class_name="flex items-center",
                    ),
                    on_click=MaestraState.save_student_changes,
                    class_name="px-5 py-2.5 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg transition-colors shadow-lg shadow-emerald-200",
                ),
                class_name="flex justify-end gap-3 p-4 border-t border-gray-100 bg-white absolute bottom-0 left-0 right-0 z-10",
            ),
            class_name=rx.cond(
                is_open,
                "w-full max-w-md bg-white h-full shadow-2xl flex flex-col relative z-50 ml-auto border-l border-gray-100 transition-transform duration-300 ease-out translate-x-0 pointer-events-auto",
                "w-full max-w-md bg-white h-full shadow-2xl flex flex-col relative z-50 ml-auto border-l border-gray-100 transition-transform duration-300 ease-in translate-x-full pointer-events-auto",
            ),
        ),
        class_name="fixed inset-0 z-50 flex justify-end pointer-events-none overflow-hidden",
    )


def maestra_dashboard() -> rx.Component:
    """The dashboard page for maestras (homeroom/guidance)."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("users", class_name="h-8 w-8 text-emerald-600"),
                    rx.el.span(
                        "Maestra Portal",
                        class_name="text-xl font-bold text-gray-900 tracking-tight",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.button(
                    "Sign out",
                    on_click=AuthState.logout,
                    class_name="text-sm text-gray-600 hover:text-gray-900",
                ),
                class_name="h-16 flex items-center justify-between px-6 border-b border-gray-200 bg-white sticky top-0 z-30",
            ),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            f"Welcome, {AuthState.user['name']}",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Manage student profiles and academic information.",
                            class_name="text-gray-500 mt-1",
                        ),
                        class_name="mb-8",
                    ),
                    controls_section(),
                    rx.cond(
                        MaestraState.students.length() > 0,
                        rx.el.div(
                            rx.el.div(
                                rx.el.h2(
                                    "Class Roster",
                                    class_name="text-lg font-bold text-gray-900",
                                ),
                                rx.el.span(
                                    f"{MaestraState.students.length()} Students",
                                    class_name="px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs font-medium border border-gray-200",
                                ),
                                class_name="flex items-center gap-3 mb-6",
                            ),
                            rx.el.div(
                                rx.foreach(MaestraState.students, student_card),
                                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 animate-fade-in",
                            ),
                        ),
                        rx.cond(
                            MaestraState.is_loading_students,
                            rx.el.div(
                                rx.spinner(
                                    size="3", class_name="text-emerald-600 mb-4"
                                ),
                                rx.el.p(
                                    "Loading student profiles...",
                                    class_name="text-gray-500",
                                ),
                                class_name="flex flex-col items-center justify-center py-24 bg-white rounded-xl border border-gray-100 shadow-sm border-dashed",
                            ),
                            rx.cond(
                                (MaestraState.selected_grade != "")
                                & (MaestraState.selected_section != ""),
                                rx.el.div(
                                    rx.icon(
                                        "users",
                                        class_name="h-12 w-12 text-gray-300 mb-4",
                                    ),
                                    rx.el.h3(
                                        "No Students Found",
                                        class_name="text-lg font-medium text-gray-900",
                                    ),
                                    rx.el.p(
                                        "No student records found for this class section.",
                                        class_name="text-gray-500 text-center mt-1",
                                    ),
                                    class_name="flex flex-col items-center justify-center py-24 bg-white rounded-xl border border-gray-200 shadow-sm border-dashed",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "layout-grid",
                                        class_name="h-12 w-12 text-gray-300 mb-4",
                                    ),
                                    rx.el.p(
                                        "Select a grade and section to view students",
                                        class_name="text-gray-500 font-medium",
                                    ),
                                    class_name="flex flex-col items-center justify-center py-24 bg-white rounded-xl border border-gray-200 shadow-sm border-dashed",
                                ),
                            ),
                        ),
                    ),
                    class_name="max-w-[1600px] mx-auto w-full",
                ),
                class_name="flex-1 p-8 overflow-y-auto bg-gray-50",
            ),
            edit_student_panel(),
            class_name="flex flex-col h-screen w-full",
        ),
        class_name="font-['Open_Sans']",
    )