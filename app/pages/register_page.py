import reflex as rx
from app.states.auth_state import AuthState


def assignment_row_media(item: dict, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.el.option("Área de Formación", value="", disabled=True),
            rx.el.option("Matemáticas", value="Matemáticas"),
            rx.el.option("Física", value="Física"),
            rx.el.option("Química", value="Química"),
            rx.el.option("Biología", value="Biología"),
            rx.el.option("Inglés", value="Inglés"),
            rx.el.option("Castellano", value="Castellano"),
            rx.el.option("Educación Física", value="Educación Física"),
            value=item["area"],
            on_change=lambda v: AuthState.update_media_assignment(index, "area", v),
            class_name="w-full p-2 border rounded bg-white",
        ),
        rx.el.select(
            rx.el.option("Grado", value="", disabled=True),
            rx.el.option("1er Año", value="9"),
            rx.el.option("2do Año", value="10"),
            rx.el.option("3er Año", value="11"),
            rx.el.option("4to Año", value="12"),
            rx.el.option("5to Año", value="13"),
            value=item["grado"],
            on_change=lambda v: AuthState.update_media_assignment(index, "grado", v),
            class_name="w-full p-2 border rounded bg-white",
        ),
        rx.el.select(
            rx.el.option("Sección", value="", disabled=True),
            rx.el.option("A", value="A"),
            rx.el.option("B", value="B"),
            value=item["seccion"],
            on_change=lambda v: AuthState.update_media_assignment(index, "seccion", v),
            class_name="w-full p-2 border rounded bg-white",
        ),
        rx.el.button(
            rx.icon("trash", size=16),
            on_click=lambda: AuthState.remove_media_assignment(index),
            type="button",
            class_name="p-2 text-red-500 hover:bg-red-50 rounded",
        ),
        class_name="grid grid-cols-[1.5fr_1fr_1fr_auto] gap-2 mb-2",
    )


def assignment_row_primaria(item: dict, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.el.option("Área Especialista", value="", disabled=True),
            rx.el.option("Música", value="Música"),
            rx.el.option("Artes Plásticas", value="Artes Plásticas"),
            rx.el.option("Educación Física", value="Educación Física"),
            rx.el.option("Inglés", value="Inglés"),
            value=item["area"],
            on_change=lambda v: AuthState.update_primaria_assignment(index, "area", v),
            class_name="w-full p-2 border rounded bg-white",
        ),
        rx.el.select(
            rx.el.option("Grado", value="", disabled=True),
            rx.el.option("1er Grado", value="1"),
            rx.el.option("2do Grado", value="2"),
            rx.el.option("3er Grado", value="3"),
            rx.el.option("4to Grado", value="4"),
            rx.el.option("5to Grado", value="5"),
            rx.el.option("6to Grado", value="6"),
            value=item["grado"],
            on_change=lambda v: AuthState.update_primaria_assignment(index, "grado", v),
            class_name="w-full p-2 border rounded bg-white",
        ),
        rx.el.button(
            rx.icon("trash", size=16),
            on_click=lambda: AuthState.remove_primaria_assignment(index),
            type="button",
            class_name="p-2 text-red-500 hover:bg-red-50 rounded",
        ),
        class_name="grid grid-cols-[2fr_1fr_auto] gap-2 mb-2",
    )


def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Registro Docente",
                        class_name="text-3xl font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "Complete el formulario para crear su cuenta.",
                        class_name="text-gray-500 mb-8",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.div(
                            rx.icon(
                                "badge_alert", class_name="h-5 w-5 text-red-500 mr-2"
                            ),
                            rx.el.span(
                                AuthState.error_message,
                                class_name="text-sm text-red-600 font-medium",
                            ),
                            class_name="bg-red-50 border border-red-100 rounded-lg p-4 flex items-center mb-6 animate-fade-in",
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Nombres",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                placeholder="Nombres",
                                on_change=AuthState.set_reg_first_name,
                                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-violet-200 outline-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Apellidos",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                placeholder="Apellidos",
                                on_change=AuthState.set_reg_last_name,
                                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-violet-200 outline-none",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Correo Electrónico",
                            class_name="block text-sm font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="email",
                            placeholder="correo@ejemplo.com",
                            on_change=AuthState.set_reg_email,
                            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-violet-200 outline-none mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Contraseña",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="password",
                                placeholder="••••••••",
                                on_change=AuthState.set_reg_password,
                                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-violet-200 outline-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Confirmar",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="password",
                                placeholder="••••••••",
                                on_change=AuthState.set_reg_confirm_password,
                                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-violet-200 outline-none",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4 mb-6",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Rol",
                            class_name="block text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.select(
                            rx.el.option("Docente", value="docente"),
                            rx.el.option("Coordinador", value="coordinador"),
                            rx.el.option("Directivo", value="directivo"),
                            rx.el.option("Administrativo", value="administrativo"),
                            value=AuthState.reg_role,
                            on_change=AuthState.set_reg_role,
                            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-violet-200 outline-none mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Niveles de Enseñanza",
                            class_name="block text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.div(
                            rx.el.label(
                                rx.el.input(
                                    type="checkbox",
                                    on_change=AuthState.toggle_level_media,
                                    class_name="mr-2 rounded text-violet-600 focus:ring-violet-500",
                                ),
                                "Educación General Media",
                                class_name="flex items-center mr-4",
                            ),
                            rx.el.label(
                                rx.el.input(
                                    type="checkbox",
                                    on_change=AuthState.toggle_level_primaria,
                                    class_name="mr-2 rounded text-violet-600 focus:ring-violet-500",
                                ),
                                "Educación Primaria",
                                class_name="flex items-center",
                            ),
                            class_name="flex flex-wrap gap-4 mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200",
                        ),
                    ),
                    rx.cond(
                        AuthState.reg_level_media,
                        rx.el.div(
                            rx.el.h3(
                                "Asignaciones Media",
                                class_name="text-sm font-bold text-gray-700 mb-2 uppercase",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    AuthState.reg_assignments_media,
                                    lambda item, idx: assignment_row_media(item, idx),
                                ),
                                class_name="space-y-2",
                            ),
                            rx.el.button(
                                "+ Agregar Asignatura",
                                on_click=AuthState.add_media_assignment,
                                class_name="mt-2 text-sm text-violet-600 font-medium hover:text-violet-700",
                            ),
                            class_name="mb-6 p-4 border border-violet-100 bg-violet-50 rounded-lg",
                        ),
                    ),
                    rx.cond(
                        AuthState.reg_level_primaria,
                        rx.el.div(
                            rx.el.h3(
                                "Asignaciones Primaria (Especialista)",
                                class_name="text-sm font-bold text-gray-700 mb-2 uppercase",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    AuthState.reg_assignments_primaria,
                                    lambda item, idx: assignment_row_primaria(
                                        item, idx
                                    ),
                                ),
                                class_name="space-y-2",
                            ),
                            rx.el.button(
                                "+ Agregar Especialidad",
                                on_click=AuthState.add_primaria_assignment,
                                class_name="mt-2 text-sm text-violet-600 font-medium hover:text-violet-700",
                            ),
                            class_name="mb-6 p-4 border border-orange-100 bg-orange-50 rounded-lg",
                        ),
                    ),
                    rx.el.button(
                        rx.cond(
                            AuthState.is_loading,
                            rx.el.div(
                                rx.spinner(size="2", class_name="text-white mr-2"),
                                "Registrando...",
                                class_name="flex items-center justify-center",
                            ),
                            "Registrar Usuario",
                        ),
                        on_click=AuthState.register,
                        disabled=AuthState.is_loading,
                        class_name="w-full py-3.5 rounded-xl bg-violet-600 text-white font-semibold hover:bg-violet-700 active:bg-violet-800 transition-all shadow-lg shadow-violet-200 disabled:opacity-70 disabled:cursor-not-allowed",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "¿Ya tiene una cuenta? ", class_name="text-gray-500"
                        ),
                        rx.el.a(
                            "Iniciar Sesión",
                            href="/login",
                            class_name="text-violet-600 font-semibold hover:text-violet-700 hover:underline transition-colors",
                        ),
                        class_name="mt-8 text-center text-sm",
                    ),
                ),
                class_name="w-full max-w-lg bg-white p-8 md:p-10 rounded-3xl shadow-xl border border-gray-100 max-h-[90vh] overflow-y-auto",
            ),
            class_name="flex min-h-screen w-full items-center justify-center bg-gray-50 p-4",
        ),
        class_name="font-['Inter']",
    )