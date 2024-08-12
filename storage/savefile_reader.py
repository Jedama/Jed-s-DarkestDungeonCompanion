import subprocess
import json
from pathlib import Path

class SaveEditor:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def _run_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print(f"Error output: {e.stderr}")
            return None

    def process_heroes_data(self, data):
        original_heroes = data['base_root']['heroes']
        processed_heroes = {}

        for hero_data in original_heroes.values():
            hero_info = hero_data['hero_file_data']['raw_data']['base_root']
            hero_class = hero_info['heroClass']
            processed_heroes[hero_class] = hero_info

        return processed_heroes

    def decode_save(self, estate):
        jar_path = self.config_manager.get_jar_path()
        save_folder = self.config_manager.get_save_folder()
        output_path = self.config_manager.get_output_path()
        
        save_file = Path(save_folder) / f"profile_{estate.profile_id}" / "persist.roster.json"
        command = ["java", "-jar", jar_path, "decode", "-o", output_path, str(save_file)]
        
        self._run_command(command)
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        return self.process_heroes_data(data)