import reflex as rx
import asyncio
from typing import TypedDict
import uuid
import logging
from app.states.auth_state import AuthState
from app.utils.mongo import get_collection, grade_to_int, int_to_grade


class Assignment(TypedDict):
    subject: str
    grade: str
    section: str


class TeacherData(TypedDict):
    first_name: str
    last_name: str
    high_school_assignments: list[Assignment]


class Activity(TypedDict):
    id: str
    description: str
    date: str


class Student(TypedDict):
    id: str
    name: str
    index: int
    grades: dict[str, str]
    average: float


class MainState(rx.State):
    """Manage the main dashboard state."""

    current_view: str = "gradebook"
    show_sidebar: bool = False
    is_loading: bool = True
    teacher_data: TeacherData = {
        "first_name": "",
        "last_name": "",
        "high_school_assignments": [],
    }
    assignment_options: list[str] = []
    section_options: list[str] = []
    selected_subject: str = ""
    selected_section: str = ""
    show_section_selector: bool = False
    students: list[Student] = []
    is_loading_students: bool = False
    activities: list[Activity] = []
    show_add_activity_dialog: bool = False
    new_activity_description: str = ""
    new_activity_date: str = ""

    @rx.event
    def toggle_add_activity_dialog(self, show: bool):
        """Show or hide the add activity dialog."""
        self.show_add_activity_dialog = show
        if not show:
            self.new_activity_description = ""
            self.new_activity_date = ""

    @rx.event
    def add_activity(self):
        """Add a new activity to the gradebook."""
        if not self.new_activity_description:
            return
        new_id = str(uuid.uuid4())
        new_activity: Activity = {
            "id": new_id,
            "description": self.new_activity_description,
            "date": self.new_activity_date,
        }
        self.activities.append(new_activity)
        for student in self.students:
            student["grades"][new_id] = ""
        self.show_add_activity_dialog = False
        self.new_activity_description = ""
        self.new_activity_date = ""

    @rx.event
    def set_grade(self, student_id: str, activity_id: str, grade: str):
        """Update a student's grade for an activity."""
        for student in self.students:
            if student["id"] == student_id:
                student["grades"][activity_id] = grade
                self.calculate_average(student)
                break

    @rx.event
    def save_grade(self, student_id: str, activity_id: str):
        """Save action for a grade (placeholder for API call)."""
        pass

    @rx.event
    def reorder_students(self, dragged_id: str, target_id: str):
        """Reorder students list when a row is dragged and dropped."""
        if dragged_id == target_id:
            return
        dragged_idx = -1
        target_idx = -1
        for i, s in enumerate(self.students):
            if s["id"] == dragged_id:
                dragged_idx = i
            if s["id"] == target_id:
                target_idx = i
        if dragged_idx != -1 and target_idx != -1:
            student = self.students.pop(dragged_idx)
            if target_idx > dragged_idx:
                target_idx -= 1
            self.students.insert(target_idx, student)
            for i, s in enumerate(self.students):
                s["index"] = i + 1

    @rx.event
    def calculate_average(self, student: Student):
        """Calculate the average grade for a student."""
        total = 0.0
        count = 0
        for grade in student["grades"].values():
            try:
                if grade and grade.strip():
                    val = float(grade)
                    total += val
                    count += 1
            except ValueError as e:
                logging.exception(f"Error calculating average: {e}")
        if count > 0:
            student["average"] = round(total / count, 1)
        else:
            student["average"] = 0.0

    @rx.event
    def toggle_sidebar(self):
        """Toggle the sidebar visibility (mainly for mobile)."""
        self.show_sidebar = not self.show_sidebar

    @rx.event
    def set_view(self, view_name: str):
        """Set the current dashboard view and close sidebar on mobile."""
        self.current_view = view_name
        self.show_sidebar = False

    @rx.event
    def set_selected_subject(self, subject: str):
        """Set the selected subject and update available sections."""
        self.selected_subject = subject
        self.students = []
        sections = []
        for a in self.teacher_data["high_school_assignments"]:
            if a["subject"] == subject:
                if a.get("section"):
                    sections.append(a["section"])
        self.section_options = sorted(list(set(sections)))
        if len(self.section_options) == 1:
            self.selected_section = self.section_options[0]
            self.show_section_selector = True
        elif len(self.section_options) > 1:
            self.selected_section = ""
            self.show_section_selector = True
        else:
            self.selected_section = ""
            self.show_section_selector = False

    @rx.event
    def set_selected_section(self, section: str):
        """Set the selected section."""
        self.selected_section = section
        self.students = []

    @rx.event
    async def load_students(self):
        """Load students from MongoDB for the selected class."""
        if not self.selected_subject or (
            self.show_section_selector and (not self.selected_section)
        ):
            return
        self.is_loading_students = True
        yield
        target_grade_int = 0
        for a in self.teacher_data["high_school_assignments"]:
            if (
                a["subject"] == self.selected_subject
                and a.get("section") == self.selected_section
            ):
                target_grade_int = grade_to_int(a["grade"])
                break
        try:
            students_col = get_collection("2025-2026")
            query = {"estudiante_grado": target_grade_int}
            if self.selected_section:
                query["estudiante_seccion"] = self.selected_section
            cursor = students_col.find(query)
            loaded_students = []
            idx = 1
            for doc in cursor:
                first_name = doc.get("estudiante_nombres", "").split(" ")[0]
                last_name = doc.get("estudiante_apellidos", "").split(" ")[0]
                full_name = f"{first_name} {last_name}".title()
                loaded_students.append(
                    {
                        "id": str(doc.get("_id", idx)),
                        "name": full_name,
                        "index": idx,
                        "grades": {},
                        "average": 0.0,
                    }
                )
                idx += 1
            self.activities = []
            self.students = loaded_students
        except Exception as e:
            logging.exception(f"Error loading students: {e}")
            self.students = []
        self.is_loading_students = False

    @rx.event
    async def load_dashboard_data(self):
        """Load dashboard data from AuthState user."""
        auth_state = await self.get_state(AuthState)
        user = auth_state.user
        if not user:
            return
        first_name = user.get("nombres", "Docente")
        last_name = user.get("apellidos", "")
        assignments = []
        if "asignaciones" in user:
            for a in user["asignaciones"]:
                grade_str = int_to_grade(int(a.get("grado", 0)))
                assignments.append(
                    {
                        "subject": a.get("area", "General"),
                        "grade": grade_str,
                        "section": a.get("seccion", ""),
                    }
                )
        self.teacher_data = {
            "first_name": first_name,
            "last_name": last_name,
            "high_school_assignments": assignments,
        }
        self.assignment_options = sorted(
            list(
                set(
                    (a["subject"] for a in self.teacher_data["high_school_assignments"])
                )
            )
        )
        self.is_loading = False