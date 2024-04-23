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

    def craft_event(self, characters, event_type='random', event_title=None):
        events = self.events_by_type.get(event_type, {})
        if not events:
            print(f"No events available for type '{event_type}'")
            return
        
        if event_title:
            event = events.get(event_title)
            if not event:
                print(f"No event found with title '{event_title}'")
                return
            
            # Try to select characters based on the event's requirements
            event_characters = self.choose_characters(characters, event.num_characters, getattr(event, 'conditions', None))
            # Get npcs in event

            if event_characters:
                # If characters are found that meet the conditions, craft the event
                event.craft_event(event_characters, self.choose_keywords(), self.choose_outcome(event.outcome), self.get_event_npcs(event), self.get_event_glossary(event), self.compile_consequences(event.num_characters, event.special_consequences))
                return
            else:
                print(f"No valid characters found for event '{event.title}'")
                return
            
        # Loop until a suitable event is found
        while True:
            
            event = random.choice(list(events.values()))

            # Try to select characters based on the event's requirements
            event_characters = self.choose_characters(characters, event.num_characters, getattr(event, 'conditions', None))

            if event_characters:
                # If characters are found that meet the conditions, craft the event
                event.craft_event(event_characters, self.choose_keywords(), self.choose_outcome(event.outcome), self.get_event_npcs(event), self.get_event_glossary(event), self.compile_consequences(event.num_characters, event.special_consequences))
                
                return  # Successful crafting of the event, exit the function
            else:
                # If no valid characters were found, log the issue and try a new event (if not fixed to a specific title)
                print(f"No valid characters found for event '{event.title}'. Trying another event...")
                event_title = None  # Reset event title if trying again

    
    def choose_keywords(self, num_keywords=None):
        if num_keywords is None:
            num_keywords = random.randint(1, 5)
        return random.sample(self.keywords, num_keywords)
    
    def choose_outcome(self, distribution):
        # Calculate the total sum of the distribution
        total_sum = sum(distribution)
        
        # Generate a random number between 1 and the total sum
        random_number = random.randint(1, total_sum)
        
        # Iterate through the distribution and find the corresponding outcome
        cumulative_sum = 0
        for i, count in enumerate(distribution):
            cumulative_sum += count
            if random_number <= cumulative_sum:
                return ['horrible', 'bad', 'neutral', 'good', 'excellent'][i]
            
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

        return event_npcs
    
    def get_event_glossary(self, event):
        # Fetch glossary terms from the event, default to empty list if none exist
        event_glossary_terms = getattr(event, 'glossary', [])
        if not event_glossary_terms:
            return {}

        # Create a new dictionary containing the relevant glossary terms
        event_glossary = {term: self.glossary[term] for term in event_glossary_terms if term in self.glossary}
        return event_glossary
            
    def choose_characters(self, characters_dict, num_characters, conditions=None):

        # Initialise event titles list
        selected_titles = []

        # Check for conditions
        if not conditions:
            # If no conditions, pick num_characters random characters
            selected_titles = random.sample(list(characters_dict.keys()), num_characters)
            return [characters_dict[title] for title in selected_titles]
        
        # If conditions, loop over conditions
        for condition in conditions:

            # Add all characters to candidates list
            candidates = list(characters_dict.keys())
            # Remove characters that are already in event_titles
            candidates = [candidate for candidate in candidates if candidate not in selected_titles]
            # Randomise candidates order
            random.shuffle(candidates)

            character_found = False

            for candidate in candidates:
                
                if eval(condition, {}, {"character_1": characters_dict[candidate], "character_2": characters_dict[candidate]}):
                    selected_titles.append(candidate)
                    character_found = True
                    print(f'Character found for condition: {condition}, {candidate}')
                    break
            
            if not character_found:
                print(f'No character found for condition: {condition}')
                return None
            
        # If all conditions are met, return the characters
        return [characters_dict[title] for title in selected_titles]
    
    def compile_consequences(self, num_characters, special_consequences):
        compiled_consequences = self.consequences_by_type['Default'].consequences

        if num_characters > 2:
            compiled_consequences += self.consequences_by_type['MultipleCharacters'].consequences

        if special_consequences:
            compiled_special_consequences = self.consequences_by_type['Special'].consequences

            for consequence_command in special_consequences:

                for special_consequence in compiled_special_consequences:

                    if special_consequence['command'] == consequence_command:
                        compiled_consequences.append(special_consequence)

        return compiled_consequences


        
        

