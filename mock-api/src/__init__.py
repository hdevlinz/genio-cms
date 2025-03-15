import json
import os
from typing import Any, List


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "resources")


def load_data_from_json(filename: str) -> List[Any]:
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(
            f"File not found: {filepath}. Please run the data generation script first."
        )
        return []
    except json.JSONDecodeError:
        print(
            f"JSON decode error in file: {filepath}. Is the file in correct JSON format?"
        )
        return []


def save_data_to_json(filename: str, data: List[Any]) -> None:
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving data to {filepath}: {e}")
