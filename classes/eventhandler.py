from .consequence import Consequences
from .events import Event
from .glossary import GlossaryEntry
from .npc import NPC

from storage import load_json, read_json, read_txt_all

import os
import random

class EventHandler:
    def __init__(self):
        self.events_by_type = {}                                # Dictionary to store events by type
        self.consequences_by_type = {}                          # Dictionary to store consequences by type
        self.npcs_by_type = {}                                   # Dictionary to store NPCs
        self.keywords = read_txt_all('data/keywords')  
        self.glossary = load_json('data/glossary', GlossaryEntry.from_dict)   
        self.load_all_consequences()                            # Load all consequences at initialization
        self.load_all_events()                                  # Load all events at initialization
        self.load_all_npcs()

    def load_all_events(self):
        directory = ('data/events')
        for event_type in os.listdir(directory):
            full_path = os.path.join(directory, event_type)
            if os.path.isdir(full_path):
                self.events_by_type[event_type] = load_json(full_path, Event.from_dict)

    def load_all_npcs(self):
        directory = ('data/npcs')
        for npc_type in os.listdir(directory):
            full_path = os.path.join(directory, npc_type)
            if os.path.isdir(full_path):
                self.npcs_by_type[npc_type] = load_json(full_path, NPC.from_dict)

    def load_all_consequences(self):
        directory = ('data/consequences')
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)
            consequence_type = filename[:-5]
            self.consequences_by_type[consequence_type] =  Consequences.from_dict(read_json(full_path))

    def craft_event(self, characters, event_type='random', event_title=None, titles=[], keywords=[]):
        
        def craft_event_with_characters(event):
            # Ensure that the number of specified titles does not exceed the number of characters required by the event
            if len(titles) > event.num_characters:
                print(f"Too many titles specified for event '{event.title}'. Expected {event.num_characters} or fewer.")
                return None, None
            
            event_characters = self.choose_characters(event, characters, titles)
            if event_characters:
                event.type = event_type
                self.choose_keywords(event, keywords)
                self.choose_outcome(event) 
                self.get_event_npcs(event)
                self.get_event_glossary(event)
                self.compile_consequences(event)
                return event.craft_event(event_characters)
            else:
                print(f"No valid characters found for event '{event.title}'")
                return None, None
        
        events = self.events_by_type.get(event_type, {})
        if not events:
            print(f"No events available for type '{event_type}'")
            return
        
        if event_title:
            event = events.get(event_title)
            if not event:
                print(f"No event found with title '{event_title}'")
                return

            event_story, event_consequences = craft_event_with_characters(event)
            if event_story and event_consequences:
                return event_story, event_consequences
        else:
            while True:
                event = random.choice(list(events.values()))
                if event.num_characters >= len(titles):
                    event_story, event_consequences = craft_event_with_characters(event)
                    if event_story and event_consequences:
                        return event_story, event_consequences
                print(f"No valid characters found for event '{event.title}' or event invalid for specified characters. Trying another event...")

    def choose_keywords(self, event, keywords=None):
        # Fetch keyword range from the event, default to [1, 5] if not present
        keyword_range = getattr(event, 'keyword_range', [1, 5])
        min_keywords, max_keywords = keyword_range

        if keywords is None:
            # Determine the number of keywords to choose
            num_keywords = random.randint(min_keywords, max_keywords)
            
            # Pick a random sample of keywords
            picked_keywords = random.sample(self.keywords, num_keywords)
        else:
            picked_keywords = keywords

        # Get existing keywords from the event
        event_keywords = getattr(event, 'keywords', [])

        # Combine event keywords with picked keywords
        event.keywords = event_keywords + picked_keywords
    
    def choose_outcome(self, event):
        # Default distribution with 'neutral' being the most probable
        distribution = getattr(event, 'outcome', [0, 0, 1, 0, 0])
        
        # Calculate the total sum of the distribution
        total_sum = sum(distribution)
        
        # Generate a random number between 1 and the total sum
        random_number = random.randint(1, total_sum)
        
        # Find the corresponding outcome based on the random number
        cumulative_sum = 0
        outcomes = ['horrible', 'bad', 'neutral', 'good', 'excellent']
        for i, count in enumerate(distribution):
            cumulative_sum += count
            if random_number <= cumulative_sum:
                event.outcome = outcomes[i]
            
    def get_event_npcs(self, event):
        # Fetch npc titles from the event, default to empty list if none exist
        event_npc_titles = getattr(event, 'npcs', [])
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

        event.npcs = event_npcs
    
    def get_event_glossary(self, event):
        # Fetch glossary terms from the event, default to empty list if none exist
        event_glossary_terms = getattr(event, 'glossary', [])
        if not event_glossary_terms:
            return {}

        # Create a new dictionary containing the relevant glossary terms
        event_glossary = {term: self.glossary[term] for term in event_glossary_terms if term in self.glossary}
        event.glossary = event_glossary
            
    def choose_characters(self, event, characters_dict, titles=[]):
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
    
    
    def compile_consequences(self, event):
        compiled_consequences = self.consequences_by_type['Default'].consequences

        if event.num_characters > 2:
            compiled_consequences += self.consequences_by_type['MultipleCharacters'].consequences

        if event.title == "Recruit":
            compiled_consequences += self.consequences_by_type['Recruit'].consequences

        if getattr(event, 'consequences', None):
            compiled_special_consequences = self.consequences_by_type['Special'].consequences

            for consequence_command in event.consequences:

                for special_consequence in compiled_special_consequences:

                    if special_consequence['command'] == consequence_command:
                        compiled_consequences.append(special_consequence)

        event.consequences = compiled_consequences


        
        

