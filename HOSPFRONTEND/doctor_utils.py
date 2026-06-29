"""
Shared helpers for resolving a doctor's photo and department name.
Used by both pages/1_dashboard.py and pages/2_consultation.py so the
logic only lives in one place.
"""

import base64
from pathlib import Path

import streamlit as st

# This file lives at the project root (same level as app.py), so
# assets/doctors is just one level down from here.
ASSETS_DIR = Path(__file__).resolve().parent / "assets" / "doctors"

# Your API's `department` field is a plain integer ID, not a name.
# Map each ID to both a photo and a display label.
DEPARTMENT_ID_PHOTOS = {
    1: "general.png",
    2: "derma.png",
    3: "mental.png",
    4: "nutrition.png",
    5: "fitness.png",
}

DEPARTMENT_ID_NAMES = {
    1: "General Medicine",
    2: "Dermatology",
    3: "Mental Health",
    4: "Nutrition",
    5: "Fitness",
}

# Fallback mapping in case the API ever returns a nested
# {"id": 1, "name": "Dermatology"} object instead of a plain ID.
DEPARTMENT_NAME_PHOTOS = {
    "general": "general.png",
    "general medicine": "general.png",
    "dermatology": "derma.png",
    "derma": "derma.png",
    "mental health": "mental.png",
    "mental": "mental.png",
    "nutrition": "nutrition.png",
    "fitness": "fitness.png",
}


@st.cache_data(show_spinner=False)
def load_local_image_as_data_uri(filename: str):
    """Reads an image from assets/doctors and returns a base64 data URI,
    or None if the file doesn't exist yet."""
    path = ASSETS_DIR / filename
    if not path.exists():
        return None
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{encoded}"


def get_department_name(doctor: dict) -> str:
    """Resolves a readable department label from either a plain ID
    or a nested {'id':.., 'name':..} object, depending on the API."""
    department = doctor.get("department")

    if isinstance(department, dict):
        return str(department.get("name") or "").strip()

    if isinstance(department, int):
        return DEPARTMENT_ID_NAMES.get(department, f"Department {department}")

    return str(department or "").strip()


def resolve_doctor_photo(doctor: dict) -> str:
    """Returns a base64 data URI (or fallback URL) for a doctor's photo."""
    department = doctor.get("department")

    # Case 1: plain integer ID (what your API currently returns)
    if isinstance(department, int):
        filename = DEPARTMENT_ID_PHOTOS.get(department)
        if filename:
            data_uri = load_local_image_as_data_uri(filename)
            if data_uri:
                return data_uri

    # Case 2: nested object with a name
    elif isinstance(department, dict):
        name_key = str(department.get("name") or "").strip().lower()
        filename = DEPARTMENT_NAME_PHOTOS.get(name_key)
        if filename:
            data_uri = load_local_image_as_data_uri(filename)
            if data_uri:
                return data_uri

    # Fall back to whatever the API itself provides
    api_photo = doctor.get("photo_url") or doctor.get("image_url")
    if api_photo:
        return api_photo

    # Final fallback: auto-generated initials avatar
    initials = "".join(part[0].upper() for part in doctor["doctor_name"].split()[:2])
    return (
        f"https://ui-avatars.com/api/?name={initials}"
        "&size=256&background=0a0c10&color=00ffdc&bold=true&font-size=0.4"
    )