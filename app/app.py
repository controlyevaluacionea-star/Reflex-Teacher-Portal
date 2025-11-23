import reflex as rx
from app.pages.login_page import login_page
from app.pages.register_page import register_page
from app.pages.teacher_dashboard import teacher_dashboard
from app.pages.coordinator_dashboard import coordinator_dashboard
from app.pages.maestra_dashboard import maestra_dashboard
from app.states.auth_state import AuthState
from app.states.main_state import MainState
from app.components.shared import dashboard_loading


def index() -> rx.Component:
    """Root page acting as a router. Redirects to appropriate dashboard or login."""
    return rx.el.div(dashboard_loading())


import reflex_enterprise as rxe

app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(login_page, route="/login", title="Login | Teacher's Portal")
app.add_page(register_page, route="/register", title="Register | Teacher's Portal")
app.add_page(
    teacher_dashboard,
    route="/dashboard/teacher",
    on_load=[AuthState.check_auth, MainState.load_dashboard_data],
    title="Teacher Dashboard",
)
app.add_page(
    coordinator_dashboard,
    route="/dashboard/coordinator",
    on_load=AuthState.check_auth,
    title="Coordinator Dashboard",
)
app.add_page(
    maestra_dashboard,
    route="/dashboard/maestra",
    on_load=AuthState.check_auth,
    title="Maestra Dashboard",
)
app.add_page(index, route="/", on_load=AuthState.check_auth)