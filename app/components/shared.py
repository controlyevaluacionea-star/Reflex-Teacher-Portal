import reflex as rx


def dashboard_loading() -> rx.Component:
    """Shared loading spinner for dashboard pages."""
    return rx.el.div(
        rx.spinner(size="3", class_name="text-orange-600"),
        class_name="min-h-screen w-full flex items-center justify-center bg-white",
    )