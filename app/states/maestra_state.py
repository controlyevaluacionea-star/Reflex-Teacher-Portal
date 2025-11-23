import reflex as rx
import asyncio
import random
import logging
from typing import TypedDict
from app.utils.mongo import get_collection, grade_to_int, to_object_id


class Student(TypedDict):
    id: str
    name: str
    initials: str
    grade: str
    section: str
    overall_average: float
    contact_email: str
    parent_name: str
    parent_phone: str
    academic_notes: str
    behavioral_notes: str


class MaestraState(rx.State):
    """State for the Maestra Dashboard."""

    grade_options: list[str] = [
        "1st Grade",
        "2nd Grade",
        "3rd Grade",
        "4th Grade",
        "5th Grade",
        "6th Grade",
        "7th Grade",
        "8th Grade",
        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year",
        "5th Year",
    ]
    section_options: list[str] = ["A", "B", "U"]
    selected_grade: str = ""
    selected_section: str = ""
    is_loading_students: bool = False
    students: list[Student] = []
    selected_student_id: str | None = None
    editing_student: Student = {
        "id": "",
        "name": "",
        "initials": "",
        "grade": "",
        "section": "",
        "overall_average": 0.0,
        "contact_email": "",
        "parent_name": "",
        "parent_phone": "",
        "academic_notes": "",
        "behavioral_notes": "",
    }

    @rx.event
    def set_selected_grade(self, grade: str):
        self.selected_grade = grade
        self.students = []
        self.selected_student_id = None
        self._reset_editing_student()
        grade_int = grade_to_int(grade)
        if grade_int <= 8:
            self.section_options = ["U"]
            self.selected_section = "U"
        else:
            self.section_options = ["A", "B"]
            self.selected_section = ""

    @rx.event
    def set_selected_section(self, section: str):
        self.selected_section = section
        self.students = []
        self.selected_student_id = None
        self._reset_editing_student()

    def _reset_editing_student(self):
        self.editing_student = {
            "id": "",
            "name": "",
            "initials": "",
            "grade": "",
            "section": "",
            "overall_average": 0.0,
            "contact_email": "",
            "parent_name": "",
            "parent_phone": "",
            "academic_notes": "",
            "behavioral_notes": "",
        }

    @rx.event
    def select_student(self, student_id: str):
        if self.selected_student_id == student_id:
            self.selected_student_id = None
        else:
            self.selected_student_id = student_id
            for s in self.students:
                if s["id"] == student_id:
                    self.editing_student = s.copy()
                    break

    @rx.event
    def update_editing_student(self, field: str, value: str):
        """Update a field in the editing student object."""
        self.editing_student[field] = value

    @rx.event
    async def save_student_changes(self):
        """Save changes made to the student in MongoDB."""
        if not self.selected_student_id:
            return
        try:
            col = get_collection("2025-2026")
            col.update_one(
                {"_id": to_object_id(self.selected_student_id)},
                {
                    "$set": {
                        "contact_email": self.editing_student["contact_email"],
                        "parent_name": self.editing_student["parent_name"],
                        "parent_phone": self.editing_student["parent_phone"],
                        "academic_notes": self.editing_student["academic_notes"],
                        "behavioral_notes": self.editing_student["behavioral_notes"],
                    }
                },
            )
            for i, s in enumerate(self.students):
                if s["id"] == self.selected_student_id:
                    self.students[i] = self.editing_student
                    break
            self.selected_student_id = None
            yield rx.toast(
                "Información actualizada correctamente.",
                position="bottom-right",
                duration=3000,
                close_button=True,
            )
        except Exception as e:
            logging.exception(f"Error al guardar: {e}")
            yield rx.toast(f"Error al guardar: {str(e)}", position="bottom-right")

    @rx.event
    def cancel_editing(self):
        """Cancel editing and clear selection."""
        self.selected_student_id = None

    @rx.event
    async def load_students_for_grade_section(self):
        """Load student data for the selected grade and section."""
        if not self.selected_grade or not self.selected_section:
            return
        self.is_loading_students = True
        self.students = []
        self.selected_student_id = None
        yield
        grade_int = grade_to_int(self.selected_grade)
        try:
            col = get_collection("2025-2026")
            cursor = col.find(
                {
                    "estudiante_grado": grade_int,
                    "estudiante_seccion": self.selected_section,
                }
            )
            loaded = []
            for doc in cursor:
                first_name = doc.get("estudiante_nombres", "").split(" ")[0]
                last_name = doc.get("estudiante_apellidos", "").split(" ")[0]
                full_name = f"{first_name} {last_name}".title()
                initials = f"{first_name[0]}{last_name[0]}"
                loaded.append(
                    {
                        "id": str(doc.get("_id")),
                        "name": full_name,
                        "initials": initials,
                        "grade": self.selected_grade,
                        "section": self.selected_section,
                        "overall_average": round(random.uniform(10, 20), 1),
                        "contact_email": doc.get("contact_email", ""),
                        "parent_name": doc.get("parent_name", ""),
                        "parent_phone": doc.get("parent_phone", ""),
                        "academic_notes": doc.get("academic_notes", ""),
                        "behavioral_notes": doc.get("behavioral_notes", ""),
                    }
                )
            self.students = loaded
        except Exception as e:
            logging.exception(f"Error loading maestra students: {e}")
            self.students = []
        self.is_loading_students = False