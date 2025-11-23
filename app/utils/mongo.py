import logging

MONGO_URI = "mongodb+srv://ender:ender2024@cluster0.oarsibs.mongodb.net/"
DATABASE_NAME = "enderavila"
_client = None


def get_client():
    global _client
    if _client is None:
        try:
            from pymongo import MongoClient

            _client = MongoClient(MONGO_URI)
        except Exception as e:
            logging.exception(f"Failed to connect to MongoDB: {e}")
            raise
    return _client


def get_db():
    return get_client()[DATABASE_NAME]


def get_collection(name: str):
    return get_db()[name]


def grade_to_int(grade_str: str) -> int:
    """Convert string grade representation to integer for DB query."""
    mapping = {
        "1st Grade": 1,
        "1er Grado": 1,
        "2nd Grade": 2,
        "2do Grado": 2,
        "3rd Grade": 3,
        "3er Grado": 3,
        "4th Grade": 4,
        "4to Grado": 4,
        "5th Grade": 5,
        "5to Grado": 5,
        "6th Grade": 6,
        "6to Grado": 6,
        "7th Grade": 7,
        "7mo Grado": 7,
        "8th Grade": 8,
        "8vo Grado": 8,
        "1st Year": 9,
        "1er Año": 9,
        "2nd Year": 10,
        "2do Año": 10,
        "3rd Year": 11,
        "3er Año": 11,
        "4th Year": 12,
        "4to Año": 12,
        "5th Year": 13,
        "5to Año": 13,
    }
    return mapping.get(grade_str, 0)


def int_to_grade(grade_int: int) -> str:
    """Convert db integer grade to string representation."""
    if grade_int <= 6:
        return f"{grade_int}th Grade"
    elif grade_int == 7:
        return "7th Grade"
    elif grade_int == 8:
        return "8th Grade"
    elif grade_int == 9:
        return "1st Year"
    elif grade_int == 10:
        return "2nd Year"
    elif grade_int == 11:
        return "3rd Year"
    elif grade_int == 12:
        return "4th Year"
    elif grade_int == 13:
        return "5th Year"
    else:
        return f"{grade_int}th Grade"


def to_object_id(id_str: str):
    """Convert string to MongoDB ObjectId."""
    from importlib import import_module

    bson = import_module("bson.objectid")
    return bson.ObjectId(id_str)