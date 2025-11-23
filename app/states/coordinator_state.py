import reflex as rx
import asyncio
import random
import logging
from typing import TypedDict
from app.utils.mongo import get_collection, grade_to_int


class StudentAverage(TypedDict):
    id: str
    name: str
    averages: dict[str, float]
    overall_average: float


class CoordinatorState(rx.State):
    """State for the Coordinator Dashboard."""

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
    subjects: list[str] = [
        "Matemáticas",
        "Inglés",
        "Ciencias Naturales",
        "Historia",
        "Educación Física",
        "Arte",
    ]
    selected_grade: str = ""
    selected_section: str = ""
    is_loading_data: bool = False
    students_data: list[StudentAverage] = []

    @rx.var
    def class_average(self) -> float:
        if not self.students_data:
            return 0.0
        total = sum((s["overall_average"] for s in self.students_data))
        return round(total / len(self.students_data), 1)

    @rx.var
    def highest_average(self) -> float:
        if not self.students_data:
            return 0.0
        return max((s["overall_average"] for s in self.students_data))

    @rx.var
    def lowest_average(self) -> float:
        if not self.students_data:
            return 0.0
        return min((s["overall_average"] for s in self.students_data))

    @rx.var
    def passing_rate(self) -> str:
        if not self.students_data:
            return "0.0%"
        passing_count = sum(
            (1 for s in self.students_data if s["overall_average"] >= 10)
        )
        rate = passing_count / len(self.students_data) * 100
        return f"{rate:.1f}%"

    @rx.event
    def set_selected_grade(self, grade: str):
        self.selected_grade = grade
        self.students_data = []
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
        self.students_data = []

    @rx.event
    async def load_students_for_section(self):
        """Load student data from MongoDB."""
        if not self.selected_grade or not self.selected_section:
            return
        self.is_loading_data = True
        self.students_data = []
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
            real_students = []
            for doc in cursor:
                first_name = doc.get("estudiante_nombres", "").split(" ")[0]
                last_name = doc.get("estudiante_apellidos", "").split(" ")[0]
                averages = {}
                total_score = 0
                for subject in self.subjects:
                    score = round(random.uniform(10, 20), 1)
                    averages[subject] = score
                    total_score += score
                overall = round(total_score / len(self.subjects), 1)
                real_students.append(
                    {
                        "id": str(doc.get("_id")),
                        "name": f"{first_name} {last_name}".title(),
                        "averages": averages,
                        "overall_average": overall,
                    }
                )
            real_students.sort(key=lambda x: x["overall_average"], reverse=True)
            self.students_data = real_students
        except Exception as e:
            logging.exception(f"Error loading coordinator data: {e}")
            self.students_data = []
        self.is_loading_data = False

    @rx.event
    def export_report(self):
        """Placeholder for exporting report data."""
        return rx.toast(
            "Exporting academic performance report...",
            duration=3000,
            position="bottom-right",
        )