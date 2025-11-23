import reflex as rx
from app.states.auth_state import AuthState
from app.states.coordinator_state import CoordinatorState
from app.components.shared import dashboard_loading


def stat_card(
    label: str, value: str, icon: str, icon_class: str, bg_class: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=icon_class, size=24),
            class_name=f"h-12 w-12 rounded-full {bg_class} flex items-center justify-center mb-3",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow",
    )


def stats_section() -> rx.Component:
    return rx.el.div(
        stat_card(
            "Class Average",
            CoordinatorState.class_average.to_string(),
            "calculator",
            "text-blue-600",
            "bg-blue-100",
        ),
        stat_card(
            "Highest Grade",
            CoordinatorState.highest_average.to_string(),
            "trophy",
            "text-emerald-600",
            "bg-emerald-100",
        ),
        stat_card(
            "Lowest Grade",
            CoordinatorState.lowest_average.to_string(),
            "trending-down",
            "text-red-600",
            "bg-red-100",
        ),
        stat_card(
            "Passing Rate",
            CoordinatorState.passing_rate,
            "users",
            "text-violet-600",
            "bg-violet-100",
        ),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 w-full",
    )


def subject_header(subject: str) -> rx.Component:
    return rx.el.th(
        rx.el.div(subject, class_name="truncate", title=subject),
        class_name="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase tracking-wider border-l border-gray-100 min-w-[100px]",
    )


def score_cell(score: float) -> rx.Component:
    return rx.el.td(
        rx.el.span(
            score,
            class_name=rx.cond(
                score >= 90,
                "text-emerald-600 font-bold",
                rx.cond(
                    score >= 70, "text-gray-700 font-medium", "text-red-600 font-bold"
                ),
            ),
        ),
        class_name="px-4 py-3 text-center whitespace-nowrap border-l border-gray-100",
    )


def student_row(student: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            student["name"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 sticky left-0 bg-white z-10 border-r border-gray-100 shadow-[4px_0_8px_-4px_rgba(0,0,0,0.05)]",
        ),
        rx.foreach(
            CoordinatorState.subjects,
            lambda subject: score_cell(student["averages"][subject]),
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    student["overall_average"],
                    class_name=rx.cond(
                        student["overall_average"] >= 70,
                        "inline-flex items-center justify-center w-12 h-6 bg-green-100 text-green-700 text-xs font-bold rounded",
                        "inline-flex items-center justify-center w-12 h-6 bg-red-100 text-red-700 text-xs font-bold rounded",
                    ),
                ),
                class_name="flex justify-center",
            ),
            class_name="px-4 py-3 whitespace-nowrap text-center border-l border-gray-200 bg-gray-50 sticky right-0 z-10 shadow-[-4px_0_8px_-4px_rgba(0,0,0,0.05)]",
        ),
        class_name="hover:bg-gray-50 transition-colors",
    )


def results_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Academic Performance Report",
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.span(
                        f"{CoordinatorState.students_data.length()} Students",
                        class_name="ml-3 px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs font-medium border border-gray-200",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-4 w-4 mr-2"),
                    "Export Report",
                    on_click=CoordinatorState.export_report,
                    class_name="flex items-center px-3 py-1.5 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm transition-colors",
                ),
                class_name="p-6 border-b border-gray-200 flex items-center justify-between bg-white rounded-t-xl",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Student Name",
                                class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50 z-20 border-r border-gray-200 shadow-[4px_0_8px_-4px_rgba(0,0,0,0.05)]",
                            ),
                            rx.foreach(CoordinatorState.subjects, subject_header),
                            rx.el.th(
                                "Overall",
                                class_name="px-4 py-3 text-center text-xs font-bold text-gray-700 uppercase tracking-wider sticky right-0 bg-gray-100 z-20 border-l border-gray-200 shadow-[-4px_0_8px_-4px_rgba(0,0,0,0.05)]",
                            ),
                        ),
                        class_name="bg-gray-50",
                    ),
                    rx.el.tbody(
                        rx.foreach(CoordinatorState.students_data, student_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden animate-fade-in",
        )
    )


def coordinator_dashboard() -> rx.Component:
    """The dashboard page for coordinators."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("layout-dashboard", class_name="h-8 w-8 text-indigo-600"),
                    rx.el.span(
                        "Coordinator",
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
                            "Select a grade and section to view student academic performance.",
                            class_name="text-gray-500 mt-1",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Grade Level",
                                    class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
                                ),
                                rx.el.select(
                                    rx.el.option(
                                        "Select Grade", value="", disabled=True
                                    ),
                                    rx.foreach(
                                        CoordinatorState.grade_options,
                                        lambda option: rx.el.option(
                                            option, value=option
                                        ),
                                    ),
                                    value=CoordinatorState.selected_grade,
                                    on_change=CoordinatorState.set_selected_grade,
                                    class_name="w-full bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-2.5 transition-colors shadow-sm",
                                ),
                                class_name="w-full sm:w-64",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Section",
                                    class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
                                ),
                                rx.el.select(
                                    rx.el.option(
                                        "Select Section", value="", disabled=True
                                    ),
                                    rx.foreach(
                                        CoordinatorState.section_options,
                                        lambda option: rx.el.option(
                                            option, value=option
                                        ),
                                    ),
                                    value=CoordinatorState.selected_section,
                                    on_change=CoordinatorState.set_selected_section,
                                    class_name="w-full bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-2.5 transition-colors shadow-sm",
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
                                        CoordinatorState.is_loading_data,
                                        rx.el.div(
                                            rx.spinner(
                                                size="2", class_name="text-white mr-2"
                                            ),
                                            "Loading Data...",
                                            class_name="flex items-center",
                                        ),
                                        rx.el.div(
                                            rx.icon(
                                                "search", class_name="h-4 w-4 mr-2"
                                            ),
                                            "View Report",
                                            class_name="flex items-center",
                                        ),
                                    ),
                                    on_click=CoordinatorState.load_students_for_section,
                                    disabled=CoordinatorState.is_loading_data
                                    | (CoordinatorState.selected_grade == "")
                                    | (CoordinatorState.selected_section == ""),
                                    class_name="h-[42px] px-6 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[140px]",
                                ),
                                class_name="w-full sm:w-auto",
                            ),
                            class_name="flex flex-col sm:flex-row items-start sm:items-end gap-4",
                        ),
                        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mb-8",
                    ),
                    rx.cond(
                        CoordinatorState.students_data.length() > 0,
                        rx.el.div(
                            stats_section(),
                            results_table(),
                            class_name="flex flex-col gap-6",
                        ),
                        rx.cond(
                            CoordinatorState.is_loading_data,
                            rx.el.div(
                                rx.spinner(size="3", class_name="text-indigo-600 mb-4"),
                                rx.el.p(
                                    "Processing academic records...",
                                    class_name="text-gray-500",
                                ),
                                class_name="flex flex-col items-center justify-center py-12 bg-white rounded-xl border border-gray-100 shadow-sm",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "bar-chart-2",
                                    class_name="h-12 w-12 text-gray-300 mb-4",
                                ),
                                rx.el.h3(
                                    "No Data to Display",
                                    class_name="text-lg font-medium text-gray-900",
                                ),
                                rx.el.p(
                                    "Select a grade and section above to view the academic performance report.",
                                    class_name="text-gray-500 text-center max-w-sm mt-1",
                                ),
                                class_name="flex flex-col items-center justify-center py-20 bg-white rounded-xl border border-gray-200 border-dashed shadow-sm",
                            ),
                        ),
                    ),
                    class_name="max-w-[1600px] mx-auto w-full",
                ),
                class_name="flex-1 p-8 overflow-y-auto bg-gray-50",
            ),
            class_name="flex flex-col h-screen w-full",
        ),
        class_name="font-['Open_Sans']",
    )