import json
from pathlib import Path, PureWindowsPath

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self):
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self.get_default_config()

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_default_config(self):
        return {
            "jar_path": "",
            "save_folder": "",
            "output_path": ""
        }

    def _convert_path(self, windows_path):
        if not windows_path:
            return ""
        # Convert Windows path to WSL path
        return Path('/mnt/c').joinpath(PureWindowsPath(windows_path).relative_to('C:\\')).as_posix()

    def get_jar_path(self):
        return self._convert_path(self.config.get("jar_path", ""))

    def set_jar_path(self, path):
        self.config["jar_path"] = str(Path(path))
        self.save_config()

    def get_save_folder(self):
        return self._convert_path(self.config.get("save_folder", ""))

    def set_save_folder(self, folder):
        self.config["save_folder"] = str(Path(folder))
        self.save_config()

    def get_output_path(self):
        return self._convert_path(self.config.get("output_path", ""))

    def set_output_path(self, path):
        self.config["output_path"] = str(Path(path))
        self.save_config()