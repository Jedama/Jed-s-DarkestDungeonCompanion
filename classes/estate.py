from storage import read_json, load_json, save_json_directory, save_json

from .character import Character
from .eventhandler import EventHandler

import os

class Estate:
    def __init__(self, title):
        self.title = title
        self.money = 0
        self.leader = 'Heiress'
        self.characters = {}
        self.eventHandler = EventHandler()
        self.dungeon_team = []
        self.dungeon_region = []
        self.keywords = []

    def to_dict(self):
        return {
            'title': self.title,
            'characters': {title: character.to_dict() for title, character in self.characters.items()}
        }

    def save_estate(self):
        estate_data = self.to_dict()

        # Create the main estate directory
        estate_dir = os.path.join('estates', self.title)
        os.makedirs(estate_dir, exist_ok=True)

        # Save estate.json using save_json function from storage.py
        estate_path = os.path.join(estate_dir, 'estate.json')
        save_json(estate_path, estate_data)

    @classmethod
    def from_dict(cls, data):
        estate = cls(data['title'])
        estate.characters = {title: Character.from_dict(char_data) for title, char_data in data['characters'].items()}
        return estate

    @classmethod
    def load_estate(cls, title):
        estate_dir = os.path.join('estates', title)

        # Load estate.json
        estate_path = os.path.join(estate_dir, 'estate.json')
        estate_data = read_json(estate_path)
        if not estate_data:
            raise FileNotFoundError(f"Estate data not found for title: {title}")

        estate = cls.from_dict(estate_data)

        return estate

    def add_character(self, character):
        # Add a character to the dictionary, indexed by their title
        if character.title in self.characters:
            print(f"Character {character.title} already exists.")
        else:
            self.characters[character.title] = character

    def remove_character(self, character_title):
        # Remove a character from the dictionary by their title
        if character_title in self.characters:
            del self.characters[character_title]
        else:
            print(f"Character {character_title} not found.")

    def start_event(self, event_type='random', event_title=None, titles = [], modifiers = []):
        # Start an event by title
        return self.eventHandler.craft_event(self.characters, event_type, event_title, titles, modifiers + self.keywords)

    def recruit(self, title, quirks=[], name = ''):

        def ensure_relationship_placeholder(character, other_character):
            if other_character.title not in character.relationships:
                character.relationships[other_character.title] = {
                    "affinity": 0,
                    "dynamic": "Neutral",
                    "description": ""
                }

        character_data = read_json(os.path.join('data/character_templates', title))
        if character_data:
            character = Character.from_dict(character_data)
            if name != '':
                character.name = name
            
            self.add_character(character)
        else:
            print(f'Character template not found: {title}')

        recruit_title, recruit_story, recruit_consequences = self.eventHandler.craft_event(self.characters, 'town', 'Recruit', [title], quirks)

        ordered_characters = self.eventHandler.recruit_rank_characters(self.characters, self.leader, character)

        # Loop through each group in ordered_characters
        for group in ordered_characters:
            group_encounter_results = []
            
            # Ensure relationships exist between the new character and each character in the group
            for other_title in group:
                if other_title != title:  # Skip if it's the new character
                    ensure_relationship_placeholder(self.characters[title], self.characters[other_title])
                    ensure_relationship_placeholder(self.characters[other_title], self.characters[title])

        return f'Recruit: {name}', recruit_story, recruit_consequences, ordered_characters

        # Store the return values in a list of lists
        encounter_results = []

        # Loop through each group in ordered_characters
        for group in ordered_characters:
            group_encounter_results = []
            
            # Ensure relationships exist between the new character and each character in the group
            for other_title in group:
                if other_title != title:  # Skip if it's the new character
                    ensure_relationship_placeholder(self.characters[title], self.characters[other_title])
                    ensure_relationship_placeholder(self.characters[other_title], self.characters[title])
            
            # Create an encounter for the entire group
            encounter_characters = [title] + group
            result = self.eventHandler.craft_event(self.characters, 'town', f'First Encounter {len(encounter_characters)}', encounter_characters)
            group_encounter_results.append(result)
            
            encounter_results.append(group_encounter_results)

        return recruit_story, recruit_consequences, encounter_results

    def encounter(self, enemies = [], event_type = 'dungeon', event_title='Encounter Start', modifiers=[]):

        self.eventHandler.craft_event(self.characters, event_type, event_title, self.dungeon_team, keywords=modifiers, enemies=enemies, region=self.dungeon_region)

    
    def start_campaign(self, starting_characters = ['Heiress', 'Heir', 'Crusader', 'Highwayman']):

        for character_title in starting_characters:
            character_data = read_json(os.path.join('data/character_templates', character_title))
            if character_data:
                character = Character.from_dict(character_data)
                self.add_character(character)
                #s elf.dungeon_team = starting_characters
                #s elf.dungeon_region = 'The Old Road'
            else:
                print(f'Character template not found: {character_title}')
