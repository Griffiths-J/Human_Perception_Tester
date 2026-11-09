import csv
from pathlib import Path


APP_FOLDER = Path(__file__).resolve().parent
CSV_FILE = APP_FOLDER / "experiment_results.csv"

CSV_COLUMNS = [
    "timestamp",
    "participant_id",
    "visual_condition",
    "contrast_level",
    "size_level",
    "brightness_percent",
    "task_type",
    "time_taken_seconds",
    "ease_of_use_rating",
    "identification_response",
    "target_size_px",
    "target_distance_px",
    "trial_number"
]


def create_csv():

    if not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0:

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=CSV_COLUMNS
            )

            writer.writeheader()

        return

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        existing_columns = reader.fieldnames or []

        if existing_columns == CSV_COLUMNS:

            return

        if not set(existing_columns).issubset(CSV_COLUMNS):

            raise ValueError(
                "The results CSV contains columns that this app does not recognize."
            )

        existing_results = list(reader)

    temporary_file = CSV_FILE.with_suffix(".csv.tmp")

    with open(temporary_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_COLUMNS
        )

        writer.writeheader()

        writer.writerows(existing_results)

    temporary_file.replace(CSV_FILE)


def save_result(result):

    create_csv()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_COLUMNS
        )

        writer.writerow(result)
