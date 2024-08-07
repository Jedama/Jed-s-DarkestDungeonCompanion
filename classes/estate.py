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

    def start_event(self, event_category='random', event_title=None, titles = [], modifiers = []):
        # Start an event by title
        return self.eventHandler.craft_event(self.characters, event_category, event_title, titles, modifiers + self.keywords)

    def recruit(self, title, quirks=[], name = ''):

        character_data = read_json(os.path.join('data/character_templates', title))
        if character_data:
            character = Character.from_dict(character_data)
            if name != '':
                character.name = name
            
            self.add_character(character)
        else:
            print(f'Character template not found: {title}')

        recruit_title, recruit_story, recruit_consequences = self.eventHandler.craft_event(self.characters, 'recruit', '', [title], quirks)

        ordered_characters = self.eventHandler.recruit_rank_characters(self.characters, self.leader, character)

        return f'Recruit: {name}', recruit_story, recruit_consequences, ordered_characters
    
    def quick_encounter(self, event_category='', event_title='', titles = []):

        return self.eventHandler.quick_event(self.characters, event_category, event_title, titles)

    def encounter(self, enemies = [], event_category = 'dungeon', event_title='Encounter Start', modifiers=[]):

        self.eventHandler.craft_event(self.characters, event_category, event_title, self.dungeon_team, keywords=modifiers, enemies=enemies, region=self.dungeon_region)

    
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

    def add_relationship_placeholder(self, titles):

        def initialize_placeholder(character, other_character):
            if other_character.title not in character.relationships:
                character.relationships[other_character.title] = {
                    "affinity": 0,
                    "dynamic": "Neutral",
                    "description": ""
                }

        if not titles or len(titles) < 2:
            print("At least two character titles are required.")
            return
        
        first_character = self.characters.get(titles[0])
        if not first_character:
            print(f"Character {titles[0]} not found in the estate.")
            return

        for other_title in titles[1:]:
            other_character = self.characters.get(other_title)
            if other_character:
                initialize_placeholder(first_character, other_character)
                initialize_placeholder(other_character, first_character)
            else:
                print(f"Character {other_title} not found in the estate.")
            
            
        
