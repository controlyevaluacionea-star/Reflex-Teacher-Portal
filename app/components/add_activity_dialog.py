import reflex as rx
from app.states.main_state import MainState


def add_activity_dialog() -> rx.Component:
    """A modal dialog to add a new assignment/activity."""
    return rx.cond(
        MainState.show_add_activity_dialog,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/50 transition-opacity z-40",
                on_click=lambda: MainState.toggle_add_activity_dialog(False),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Add New Activity",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Description",
                            class_name="block text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            placeholder="e.g. Unit 1 Quiz",
                            on_change=MainState.set_new_activity_description,
                            class_name="w-full px-4 py-2 rounded-lg bg-gray-50 border border-gray-200 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 outline-none transition-all text-gray-900",
                            default_value=MainState.new_activity_description,
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Date",
                            class_name="block text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            type="date",
                            on_change=MainState.set_new_activity_date,
                            class_name="w-full px-4 py-2 rounded-lg bg-gray-50 border border-gray-200 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 outline-none transition-all text-gray-900",
                            default_value=MainState.new_activity_date,
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=lambda: MainState.toggle_add_activity_dialog(
                                False
                            ),
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors",
                        ),
                        rx.el.button(
                            "Add Activity",
                            on_click=MainState.add_activity,
                            disabled=MainState.new_activity_description == "",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-orange-600 hover:bg-orange-700 rounded-lg transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed",
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-xl w-full max-w-md relative z-50 animate-fade-in",
                ),
                class_name="fixed inset-0 flex items-center justify-center z-50 p-4",
            ),
            class_name="relative z-50",
        ),
    )