import csv
import os
from datetime import datetime


class DataLogger:

    def __init__(self):
        # Finder projektets DATA-mappe
        project_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.log_folder = os.path.join(
            project_path,
            "DATA",
            "LOGS"
        )

        # Opret mappen hvis den ikke findes
        os.makedirs(self.log_folder, exist_ok=True)

    def get_log_file(self):
        """
        Returnerer filnavnet for dagens logfil.
        """

        date = datetime.now().strftime("%Y-%m-%d")

        return os.path.join(
            self.log_folder,
            f"{date}.csv"
        )

    def log(
        self,
        unit="",
        em="",
        oee=0,
        availability=0,
        performance=0,
        quality=0,
        packml=""
    ):
        """
        Gemmer et datapunkt i dagens CSV-fil.
        """

        file_path = self.get_log_file()

        file_exists = os.path.exists(file_path)

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        row = [
            timestamp,
            unit,
            em,
            oee,
            availability,
            performance,
            quality,
            packml
        ]

        with open(
            file_path,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # Hvis filen er ny, skriv header først
            if not file_exists:
                writer.writerow([
                    "Timestamp",
                    "Unit",
                    "EM",
                    "OEE",
                    "Availability",
                    "Performance",
                    "Quality",
                    "PackML"
                ])

            writer.writerow(row)