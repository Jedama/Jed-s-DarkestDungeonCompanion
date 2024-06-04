from storage import read_json, load_json, save_json_directory, save_json

from .character import Character
from .eventhandler import EventHandler

import os
import random

class Estate:
    def __init__(self, title):
        self.title = title
        self.money = 0
        self.characters = {}
        self.eventHandler = EventHandler()
        self.dungeon_team = []
        self.dungeon_region = []

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

        # Save each character's data using save_json_directory function from storage.py
        characters_dir = os.path.join(estate_dir, 'characters')
        save_json_directory(characters_dir, self.characters)

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
        event_story, event_consequences = self.eventHandler.craft_event(self.characters, event_type, event_title, titles, modifiers)

        return event_story, event_consequences
    
    def recruit(self, title, quirks=[]):

        def ensure_relationship_placeholder(character, other_character):
            if other_character.title not in character.relationships:
                character.relationships[other_character.title] = {
                    "affinity": 0,
                    "dynamic": "Neutral",
                    "description": "",
                    "history": "",
                    "notes": ""
                }

        character_data = read_json(os.path.join('data/character_templates', title))
        if character_data:
            character = Character.from_dict(character_data)
            self.add_character(character)
        else:
            print(f'Character template not found: {title}')

        recruit_story, recruit_consequences = self.eventHandler.craft_event(self.characters, 'town', 'Recruit', [title], quirks)

        # Store the return values in a list of lists
        encounter_results = []

        # Get a list of other characters in the town
        other_characters = [char for char in self.characters if char != title]

        # Shuffle the order of the encounters
        random.shuffle(other_characters)

        # Loop through every other character in the town
        for other_character in other_characters:
            # Ensure relationship placeholders exist for both characters
            ensure_relationship_placeholder(self.characters[title], self.characters[other_character])
            ensure_relationship_placeholder(self.characters[other_character], self.characters[title])

            result = self.eventHandler.craft_event(self.characters, 'town', 'First Encounter', [title, other_character])
            encounter_results.append(result)

        return recruit_story, recruit_consequences, encounter_results

    def encounter(self, enemies = [], event_type = 'dungeon', event_title='Encounter Start', modifiers=[]):

        self.eventHandler.craft_event(self.characters, event_type, event_title, self.dungeon_team, keywords=modifiers, enemies=enemies, region=self.dungeon_region)

    
    def start_campaign(self, starting_characters = ['Heiress', 'Heir', 'Crusader', 'Highwayman']):

        for character_title in starting_characters:
            character_data = read_json(os.path.join('data/character_templates', character_title))
            if character_data:
                character = Character.from_dict(character_data)
                self.add_character(character)
                self.dungeon_team = starting_characters
                self.dungeon_region = 'The Old Road'
            else:
                print(f'Character template not found: {character_title}')
