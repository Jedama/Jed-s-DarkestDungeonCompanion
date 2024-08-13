import subprocess
import math
import json
from pathlib import Path

class SaveEditor:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.title_translation = self.load_title_translation()

    def _run_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print(f"Error output: {e.stderr}")
            return None

    def load_title_translation(self):
        with open('static/json/character_constants.json', 'r') as f:
            character_constants = json.load(f)
        
        return {v['officialTitle']: k for k, v in character_constants.items()}

    def translate_title(self, title):
        return self.title_translation.get(title.lower(), title)

    def process_heroes_data(self, data):
        original_heroes = data['base_root']['heroes']
        processed_heroes = {}

        for hero_data in original_heroes.values():
            hero_info = hero_data['hero_file_data']['raw_data']['base_root']
            hero_class = hero_info['heroClass']
            translated_class = self.translate_title(hero_class)
            processed_heroes[translated_class] = hero_info

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
    
    def update_characters(self, estate, save_data):
        updated_characters = {}
        for title in estate.dungeon_team:
            
            char = estate.characters[title]
            translated_title = self.translate_title(title)
            
            # Update mental status based on m_Stress from save data
            if translated_title in save_data:
                m_stress = save_data[translated_title].get('m_Stress', 0.0)
                char.status['mental'] = max(0, int(100 - m_stress))

            updated_characters[title] = char.to_dict()
        
        return updated_characters