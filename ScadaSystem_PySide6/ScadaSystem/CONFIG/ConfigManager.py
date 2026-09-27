import json
import os


class ConfigManager:

    def __init__(self):
        self.config_path = os.path.join(
            os.path.dirname(__file__),
            "config.json"
        )

        self.config = {}

        self.load()

    def load(self):
        """Indlæser konfigurationen fra config.json."""

        with open(self.config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

    def save(self):
        """Gemmer den aktuelle konfiguration i config.json."""

        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump(
                self.config,
                file,
                indent=4
            )

    def get(self, section, key):
        """Henter en værdi fra konfigurationen."""

        return self.config[section][key]

    def set(self, section, key, value):
        """Ændrer en værdi i konfigurationen."""

        self.config[section][key] = value