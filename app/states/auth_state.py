import reflex as rx
import asyncio
import logging
from app.utils.mongo import get_collection


class AuthState(rx.State):
    """Handle user authentication state and actions."""

    user: dict[str, str | int | list | dict | bool | None] | None = None
    is_loading: bool = False
    error_message: str = ""
    reg_first_name: str = ""
    reg_last_name: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_confirm_password: str = ""
    reg_role: str = "docente"
    reg_level_media: bool = False
    reg_level_primaria: bool = False
    reg_assignments_media: list[dict[str, str]] = [
        {"area": "", "grado": "", "seccion": ""}
    ]
    reg_assignments_primaria: list[dict[str, str]] = [{"area": "", "grado": ""}]

    @rx.var
    def user_role(self) -> str:
        """Get the role of the current user."""
        if self.user:
            return (
                self.user.get("rol", "teacher")
                if "rol" in self.user
                else self.user.get("role", "teacher")
            )
        return ""

    @rx.event
    def set_reg_role(self, role: str):
        self.reg_role = role

    @rx.event
    def toggle_level_media(self, val: bool):
        self.reg_level_media = val

    @rx.event
    def toggle_level_primaria(self, val: bool):
        self.reg_level_primaria = val

    @rx.event
    def add_media_assignment(self):
        self.reg_assignments_media.append({"area": "", "grado": "", "seccion": ""})

    @rx.event
    def remove_media_assignment(self, index: int):
        if len(self.reg_assignments_media) > 1:
            self.reg_assignments_media.pop(index)

    @rx.event
    def update_media_assignment(self, index: int, field: str, value: str):
        self.reg_assignments_media[index][field] = value

    @rx.event
    def add_primaria_assignment(self):
        self.reg_assignments_primaria.append({"area": "", "grado": ""})

    @rx.event
    def remove_primaria_assignment(self, index: int):
        if len(self.reg_assignments_primaria) > 1:
            self.reg_assignments_primaria.pop(index)

    @rx.event
    def update_primaria_assignment(self, index: int, field: str, value: str):
        self.reg_assignments_primaria[index][field] = value

    @rx.event
    async def login(self, form_data: dict):
        """Handle login form submission."""
        self.is_loading = True
        self.error_message = ""
        yield
        email = form_data.get("email", "")
        password = form_data.get("password", "")
        try:
            docentes_col = get_collection("docentes")
            user_doc = docentes_col.find_one({"email": email, "password": password})
            if user_doc:
                user_doc["_id"] = str(user_doc["_id"])
                self.user = user_doc
                role = user_doc.get("rol", "docente")
                target_role = "teacher"
                if role == "coordinador":
                    target_role = "coordinator"
                elif role == "directivo":
                    target_role = "coordinator"
                elif role == "administrativo":
                    target_role = "maestra"
                self.user["role"] = target_role
                self.is_loading = False
                yield rx.redirect(f"/dashboard/{target_role}")
            else:
                self.error_message = "Credenciales inválidas."
                self.is_loading = False
        except Exception as e:
            logging.exception(f"Login error: {e}")
            self.error_message = f"Error de conexión: {str(e)}"
            self.is_loading = False

    @rx.event
    async def register(self):
        """Handle registration form submission with complex data."""
        self.is_loading = True
        self.error_message = ""
        if self.reg_password != self.reg_confirm_password:
            self.error_message = "Las contraseñas no coinciden."
            self.is_loading = False
            return
        if not self.reg_email or not self.reg_password or (not self.reg_first_name):
            self.error_message = "Por favor complete los campos obligatorios."
            self.is_loading = False
            return
        try:
            docentes_col = get_collection("docentes")
            if docentes_col.find_one({"email": self.reg_email}):
                self.error_message = "Este correo electrónico ya está registrado."
                self.is_loading = False
                return
            levels = []
            if self.reg_level_media:
                levels.append("Media")
            if self.reg_level_primaria:
                levels.append("Primaria")
            assignments = []
            if self.reg_level_media:
                for a in self.reg_assignments_media:
                    if a["area"] and a["grado"]:
                        assignments.append({"nivel": "Media", **a})
            if self.reg_level_primaria:
                for a in self.reg_assignments_primaria:
                    if a["area"] and a["grado"]:
                        assignments.append({"nivel": "Primaria", **a})
            new_user = {
                "nombres": self.reg_first_name,
                "apellidos": self.reg_last_name,
                "email": self.reg_email,
                "password": self.reg_password,
                "rol": self.reg_role,
                "niveles": levels,
                "asignaciones": assignments,
            }
            docentes_col.insert_one(new_user)
            new_user["_id"] = str(new_user.get("_id", ""))
            target_role = "teacher"
            if self.reg_role in ["coordinador", "directivo"]:
                target_role = "coordinator"
            elif self.reg_role == "administrativo":
                target_role = "maestra"
            new_user["role"] = target_role
            self.user = new_user
            self.is_loading = False
            yield rx.redirect(f"/dashboard/{target_role}")
        except Exception as e:
            logging.exception(f"Registration error: {e}")
            self.error_message = f"Error al registrar: {str(e)}"
            self.is_loading = False

    @rx.event
    def logout(self):
        """Clear user session and redirect to login."""
        self.user = None
        self.reg_first_name = ""
        self.reg_last_name = ""
        self.reg_email = ""
        self.reg_password = ""
        self.reg_confirm_password = ""
        self.reg_assignments_media = [{"area": "", "grado": "", "seccion": ""}]
        self.reg_assignments_primaria = [{"area": "", "grado": ""}]
        return rx.redirect("/login")

    @rx.event
    def check_auth(self):
        """Verify user is logged in and redirect to correct dashboard based on role."""
        if self.user is None:
            return rx.redirect("/login")
        role = self.user.get("role", "teacher")
        current_path = self.router.page.path
        expected_path = f"/dashboard/{role}"
        if current_path == "/" or (
            "/dashboard/" in current_path and expected_path not in current_path
        ):
            return rx.redirect(expected_path)