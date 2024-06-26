from storage import read_json

from .character import Character
from .eventhandler import EventHandler

import os

class Estate:
    def __init__(self, title):
        self.title = title
        self.characters = {}
        self.roles = {}
        self.eventHandler = EventHandler()

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

    def start_event(self, event_type='random', event_title=None):
        # Start an event by title
        event_story, event_consequences = self.eventHandler.craft_event(self.characters, event_type, event_title)

        return event_story, event_consequences
    
    def recruit(self, title, quirks=[]):

        character_data = read_json(os.path.join('data/character_templates', title))
        if character_data:
            character = Character.from_dict(character_data)
            self.add_character(character)
        else:
            print(f'Character template not found: {title}')

        return self.eventHandler.craft_event(self.characters, 'town', 'Recruit', ['Vestal'], quirks)
    
    def start_campaign(self, starting_characters = ['Heiress', 'Heir', 'Crusader', 'Highwayman']):

        self.roles["Leader"] = 'Heiress'
        self.roles["Quartermaster"] = 'Heir'
        self.roles["Lawman"] = 'Crusader'
        self.roles["Welcomer"] = 'Heiress'


        for character_title in starting_characters:
            character_data = read_json(os.path.join('data/character_templates', character_title))
            if character_data:
                character = Character.from_dict(character_data)
                self.add_character(character)
            else:
                print(f'Character template not found: {character_title}')
