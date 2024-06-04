from .consequence import Consequences
from .enemy import Enemy
from .events import InputEvent, OutputEvent
from .faction import Faction
from .location import Location
from .npc import NPC

from storage import load_json, read_json, read_txt_all

import copy
import os
import random

class EventHandler:
    def __init__(self):
        self.events_by_type = {}                                # Dictionary to store events by type
        self.consequences_by_type = {}                          # Dictionary to store consequences by type
        self.npcs_by_type = {}                                  # Dictionary to store NPCs
        self.enemies_by_type = {}                               # Dictionary to store enemies by faction
        self.keywords = read_txt_all('data/keywords')  
        self.locations = load_json('data/locations', Location.from_dict)  
        self.factions =  load_json('data/factions', Faction.from_dict)  
        self.load_all_consequences()                            # Load all consequences at initialization
        self.load_all_events()                                  # Load all events at initialization
        self.load_all_npcs()
        self.load_all_enemies()


    def load_all_events(self):
        directory = ('data/events')
        for event_type in os.listdir(directory):
            full_path = os.path.join(directory, event_type)
            if os.path.isdir(full_path):
                self.events_by_type[event_type] = load_json(full_path, InputEvent.from_dict)

    def load_all_npcs(self):
        directory = ('data/npcs')
        for npc_type in os.listdir(directory):
            full_path = os.path.join(directory, npc_type)
            if os.path.isdir(full_path):
                self.npcs_by_type[npc_type] = load_json(full_path, NPC.from_dict)

    def load_all_enemies(self):
        directory = ('data/enemies')
        for enemy_type in os.listdir(directory):
            full_path = os.path.join(directory, enemy_type)
            if os.path.isdir(full_path):
                self.enemies_by_type[enemy_type] = load_json(full_path, Enemy.from_dict)

    def load_all_consequences(self):
        directory = ('data/consequences')
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)
            consequence_type = filename[:-5]
            self.consequences_by_type[consequence_type] =  Consequences.from_dict(read_json(full_path))

    def craft_event(self, characters, event_type='random', event_title=None, titles=[], keywords=[], enemies=[], region=''):
        
        def craft_event_with_characters(event):
            # Ensure that the number of specified titles does not exceed the number of characters required by the event
            if len(titles) > event.num_characters:
                print(f"Too many titles specified for event '{event.title}'. Expected {event.num_characters} or fewer.")
                return None, None
            
            event_characters = self.process_characters(input_event, characters, titles)
            if event_characters:
                # Create output event
                output_event = OutputEvent(title = event.title, type = event.type, characters = event_characters, fields = event.fields, length = event.length)

                self.process_summary(event, output_event, event_characters, enemies)
                self.process_keywords(event, output_event, keywords)
                self.process_outcome(event, output_event) 
                self.process_location(event, output_event, region)
                self.process_npcs(event, output_event)
                self.process_consequences(event, output_event)
                self.process_enemies(output_event, enemies)

                return output_event.craft_event()
                # self.process_enemies()
            else:
                print(f"No valid characters found for event '{event.title}'")
                return None, None
        
        events = self.events_by_type.get(event_type, {})
        if not events:
            print(f"No events available for type '{event_type}'")
            return
        
        if event_title:
            event_instance = events.get(event_title)
            input_event = copy.deepcopy(event_instance)
            if not input_event:
                print(f"No event found with title '{event_title}'")
                return

            event_story, event_consequences = craft_event_with_characters(input_event)
            if event_story and event_consequences:
                return event_story, event_consequences
        else:
            while True:
                input_event = random.choice(list(events.values()))
                if input_event.num_characters >= len(titles):
                    event_story, event_consequences = craft_event_with_characters(input_event)
                    if event_story and event_consequences:
                        return event_story, event_consequences
                print(f"No valid characters found for event '{input_event.title}' or event invalid for specified characters. Trying another event...")

    def process_summary(self, input_event, output_event, characters, enemies):
        # In event summary, replace placeholders with character names
        summary = input_event.summary
        for i in range(len(characters)):
            summary = summary.replace(f'[Character {i+1}]', characters[i].name)
            summary = summary.replace(f'[character {i+1}]', characters[i].name)

        # Format the enemy list into a grammatically correct string
        if enemies:
            if len(enemies) == 1:
                enemies_str = f'a single {enemies[0]}'
            else:
                enemies_str = ', '.join(enemies[:-1]) + ', and ' + enemies[-1]

            # Replace the enemies placeholder with the formatted enemy string
            summary = summary.replace('[Enemies]', enemies_str)

        output_event.summary = summary



    def process_keywords(self, input_event, output_event, keywords=None):
        # Fetch keyword range from the event, default to [1, 5] if not present
        keyword_range = getattr(input_event, 'keyword_range', [1, 5])
        min_keywords, max_keywords = keyword_range

        if not keywords:
            # Determine the number of keywords to choose
            num_keywords = random.randint(min_keywords, max_keywords)
            
            # Pick a random sample of keywords
            picked_keywords = random.sample(self.keywords, num_keywords)
        else:
            picked_keywords = keywords

        # Get existing keywords from the event
        event_keywords = getattr(input_event, 'keywords', [])

        # Combine event keywords with picked keywords
        output_event.keywords = event_keywords + picked_keywords
    
    def process_outcome(self, input_event, output_event):
        # Default distribution with 'neutral' being the most probable
        distribution = getattr(input_event, 'outcomes', [0, 0, 1, 0, 0])
        
        # Calculate the total sum of the distribution
        total_sum = sum(distribution)

        # If [0, 0, 0, 0, 0] is provided, the outcome is based on user input
        if total_sum == 0:
            output_event.outcome = "Contextual"
            return
        
        # Generate a random number between 1 and the total sum
        random_number = random.randint(1, total_sum)
        
        # Find the corresponding outcome based on the random number
        cumulative_sum = 0
        outcomes = ['horrible', 'bad', 'neutral', 'good', 'excellent']
        for i, count in enumerate(distribution):
            cumulative_sum += count
            if random_number <= cumulative_sum:
                output_event.outcome = outcomes[i]
                return
            
    def process_location(self, input_event, output_event, region):
        # Fetch location terms from the event, default to empty list if none exist
        event_locations = getattr(input_event, 'locations', [])

        # Check if a region is provided and if it's not already included in the locations
        if region and region not in event_locations:
            event_locations.append(region)

        if not event_locations:
            return {}

        # Create a new dictionary containing the relevant location terms (title and description only)
        location_dict = {}
        for term in event_locations:
            if term in self.locations:
                location_details = self.locations[term]
                location_dict[term] = {
                    "title": location_details.title,
                    "description": location_details.description
                }

        # Get NPCs from locations and append to event.npcs
        event_npcs = getattr(input_event, 'npcs', [])
        for term in event_locations:
            if term in self.locations:
                location_entry = self.locations[term]
                if location_entry.npcs:
                    # Ensure npcs is treated as a list
                    event_npcs.append(location_entry.npcs)

        # Remove duplicates and update input_event NPCs (as they will be processed next)
        input_event.npcs = list(set(event_npcs))

        # Update event location
        output_event.locations = location_dict

    def process_enemies(self, output_event, enemies=[]):
        
        unique_enemies = list(set(enemies))  # Remove duplicates to get unique enemy types
        processed_enemies = {}  # To store processed enemy data
        processed_factions = {} # To store processed factions

        # Get all enemies
        for enemy in unique_enemies:
        # Check if the enemy exists in the categorization and hasn't been processed yet
            for category in self.enemies_by_type:
                category_enemies = self.enemies_by_type[category]
                if enemy in category_enemies:
                    processed_enemies[enemy] = category_enemies[enemy]

                    # Get faction for enemy
                    faction = processed_enemies[enemy].faction
                    # Check if all unique enemies have been processed
                    if faction and faction not in processed_factions:
                        processed_factions[faction] = self.factions.get(faction, {})
                    
                    if len(processed_enemies) == len(unique_enemies):
                        break  # Exit the loop early if all have been processed

        output_event.enemies = processed_enemies
        output_event.factions = processed_factions

            
    def process_npcs(self, input_event, output_event):
        # Fetch npc titles from the event, default to empty list if none exist
        event_npc_titles = getattr(input_event, 'npcs', [])
        if not event_npc_titles:
            return {}

        # Initialize an empty dictionary to store the NPCs found
        event_npcs = {}

        # Loop through each category in the npcs_by_type dict
        for category in self.npcs_by_type:
            # Filter NPCs that are listed in the event_npc_titles and are present in the current category
            category_npcs = self.npcs_by_type[category]
            found_npcs = {title: category_npcs[title] for title in event_npc_titles if title in category_npcs}

            # Update the event_npcs dict with the NPCs found in this category
            event_npcs.update(found_npcs)

        output_event.npcs = event_npcs
            
    def process_characters(self, event, characters_dict, titles=[]):
        def meets_conditions(character, condition):
            method_name = condition['method']
            args = condition.get('args', [])
            method = getattr(character, method_name)
            return method(*args)

        selected_titles = [None] * event.num_characters  # Initialize list with placeholders

        conditions = getattr(event, 'conditions', None)

        if conditions:
            # If conditions are provided, process each condition
            for condition in conditions:
                character_index = condition['character'] - 1  # Convert 1-based to 0-based index

                # Prepare a list of candidates with title characters at the front
                candidates = [title for title in titles if title in characters_dict] + \
                            [title for title in characters_dict.keys() if title not in titles]
                random.shuffle(candidates)  # Shuffle to randomize the selection order

                character_found = False
                # Go through all candidates until one meets the conditions
                for candidate in candidates:
                    character = characters_dict[candidate]
                    if meets_conditions(character, condition):
                        selected_titles[character_index] = candidate
                        character_found = True
                        print(f'Character found for condition: {condition}, {candidate}')
                        break

                # If no character is found, return None
                if not character_found:
                    print(f'No character found for condition: {condition}')
                    return None

        # Ensure all title characters can still fit in the selected titles
        for i, title in enumerate(titles):
            if title not in selected_titles:
                for j in range(event.num_characters):
                    if selected_titles[j] is None:
                        selected_titles[j] = title
                        break
                else:
                    print(f"Not enough slots for title '{title}'.")
                    return

        # Fill in remaining positions with random characters
        remaining_characters = [title for title in characters_dict.keys() if title not in selected_titles]
        random.shuffle(remaining_characters)
        for i in range(event.num_characters):
            if selected_titles[i] is None:
                if not remaining_characters:
                    print("Not enough characters to fill the event.")
                    return
                selected_titles[i] = remaining_characters.pop()

        return [characters_dict[title] for title in selected_titles]
    
    
    def process_consequences(self, input_event, output_event):
        compiled_consequences = []

        if input_event.type in ['random', 'story', 'dungeon']:
            compiled_consequences = self.consequences_by_type['Default'].consequences
        elif input_event.type == "town":
            if input_event.title == "Recruit":
                compiled_consequences = self.consequences_by_type['Default'].consequences
                compiled_consequences += self.consequences_by_type['Recruit'].consequences

        if input_event.num_characters > 2:
            compiled_consequences += self.consequences_by_type['MultipleCharacters'].consequences

        if getattr(input_event, 'consequences', None):
            compiled_special_consequences = self.consequences_by_type['Special'].consequences

            for consequence_command in input_event.consequences:

                for special_consequence in compiled_special_consequences:

                    if special_consequence['command'] == consequence_command:
                        compiled_consequences.append(special_consequence)

        output_event.consequences = compiled_consequences


        
        

