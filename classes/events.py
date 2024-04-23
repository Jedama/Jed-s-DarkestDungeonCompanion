from .consequence import Consequences
from prompting import prompt_claude, clean_response_claude
import random
import json

class Event:
    def __init__(self, title, num_characters, summary, outcome, relevant_fields, length, npcs, glossary, conditions, special_consequences):
        self.title = title
        self.num_characters = num_characters
        self.summary = summary
        self.outcome = outcome
        self.relevant_fields = relevant_fields
        self.length = length
        self.npcs = npcs
        self.glossary = glossary
        self.conditions = conditions
        self.special_consequences = special_consequences
    

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            num_characters=data.get('num_characters'),
            summary=data.get('summary'),
            outcome=data.get('outcome'),
            relevant_fields=data.get('relevant_fields'),
            length=data.get('length'),
            npcs=data.get('npcs'),
            glossary=data.get('glossary'),
            conditions=data.get('conditions'),
            special_consequences=data.get('special_consequences')
        )
    
    def to_dict(self):
        return {
            "title": self.title,
            "num_characters": self.num_characters,
            "summary": self.summary,
            "outcome": self.outcome,
            "relevant_fields": self.relevant_fields,
            "length": self.length,
            "npcs": self.npcs,
            "glossary": self.glossary,
            "conditions": self.conditions,
            "special_consequences": self.special_consequences
        }
    
    def craft_event(self, characters, keywords, outcome, npcs, glossary, consequences):

        system_prompt, user_prompt, assistant_prompt = self.create_story_prompt(characters, keywords, outcome, npcs, glossary)

        # Call the prompt_claude function
        event_story = prompt_claude(user_prompt, system_prompt, assistant_prompt, max_tokens= 300 + 150 * self.length)
        event_story = clean_response_claude(event_story)

        print(event_story)

        system_prompt, user_prompt, assistant_prompt = self.create_consequences_prompt(outcome, consequences, event_story, characters)

        event_consequences = prompt_claude(user_prompt, system_prompt, assistant_prompt, max_tokens= 100 + (50 * self.num_characters))
        event_consequences = "For" + clean_response_claude(event_consequences)

        self.process_response(event_consequences, characters)

        print(event_consequences)

        return
    
    def create_story_prompt(self, characters, keywords, outcome, npcs, glossary):

        # Create system prompt
        system_prompt = self.story_system_prompt()
        # Create user prompt
        user_prompt = self.story_user_prompt(characters, keywords, outcome, npcs, glossary)
        # Create assistant prompt
        assistant_prompt = "Here is the story:"

        return system_prompt, user_prompt, assistant_prompt
    
    def create_consequences_prompt(self, outcome, consequences, event_story, characters):

        # Create system prompt
        system_prompt = self.consequences_system_prompt(outcome, consequences)
        # Create user prompt
        user_prompt = self.consequences_user_prompt(event_story, characters)
        # Create assistant prompt
        assistant_prompt = "Consequences:\nFor"

        return system_prompt, user_prompt, assistant_prompt
    
    def story_system_prompt(self):
        
        system_prompt = f'''
        You are the Ancestor, a spectral presence lingering malignantly over the once-grand estate that bears your legacy of doom. As the malevolent ghost haunting its decaying halls, you watch with a blend of disdain and delight the feeble efforts of the descendants and hired souls trying to reclaim and cleanse the estate. These poor souls battle against the eldritch horrors and abominations, the very ones you once summoned and manufactured in your ruthless quest for forbidden knowledge and power.

        Your role is to weave stories for these characters based on their traits and recent events. Focus on engaging, gothic-inspired storytelling that fits the grim and eerie atmosphere of the setting. Ensure that the story is self-contained, unfolding entirely within the designated setting and concludes without unresolved threads.

        Start your short story with a title and ensure it adheres to the following constraints:
        - Maximum length of {self.length * 50 + 100} words.
        - Incorporate the outlined setting, keywords, outcome, present NPCs, and characters listed below.
        '''

        return system_prompt
    
    def story_user_prompt(self, characters, keywords, outcome, npcs, glossary):

        # In event summary, replace placeholders with character names
        summary = self.summary
        for i in range(self.num_characters):
            summary = summary.replace(f'[Character {i+1}]', characters[i].name)
            summary = summary.replace(f'[character {i+1}]', characters[i].name)

        # Create user prompt
        user_prompt = f'{self.title}\n'
        user_prompt += f'{summary}\n'
        user_prompt += f'Keywords: ' + ', '.join(keywords) + '\n'

        user_prompt += f'The characters faced a {outcome} outcome.\n\n'

        user_prompt += f'Characters:\n'
        # Add characters to user prompt
        for i in range(len(characters)):
            character = characters[i]
            user_prompt += f'Name: {character.name}\n'
            user_prompt += f'Title: {character.title}\n'
            user_prompt += f'Summary: {character.summary}\n'
            user_prompt += f'History: {character.history}\n'
            user_prompt += f'Traits: {character.traits}\n'
            user_prompt += f'Status: {character.status}\n'
            user_prompt += f'Stats: {character.stats}\n'
            user_prompt += f'Equipment: {character.equipment}\n'
            user_prompt += f'Trinkets: {character.trinkets}\n'
            user_prompt += f'Other notes: {character.other_notes}\n'

            
            # Check if the template has any relevant fields
            if getattr(self, 'relevant_fields', None):
                for field in self.relevant_fields:
                    user_prompt += f'{field}: {getattr(character, field)}\n'

            if len(characters) >= 2:
                user_prompt += 'Relationships:\n'

                for j in range(len(characters)):
                    if i != j:  # Ensure we do not compare a character to themselves
                        user_prompt += f'{characters[i].title} and {characters[j].title}:\n'
                        relationship_fields = ['affinity', 'relationship_type', 'description', 'history', 'other_notes']
                        
                        # Check if the relationship exists
                        relationship_info = characters[i].relationships.get(characters[j].title)
                        if relationship_info:
                            for field in relationship_fields:
                                user_prompt += f'  {field}: {relationship_info.get(field, "N/A")}\n'  # Safely get each field
                        else:
                            user_prompt += '  No specific relationship recorded.\n'

        print(user_prompt)

        user_prompt += f'NPCs:\n'
        # Add npcs to user prompt
        for npc in npcs.values():
            user_prompt += f'Title: {npc.title}\n'
            user_prompt += f'Name: {npc.name}\n'
            user_prompt += f'Summary: {npc.summary}\n'
            user_prompt += f'History: {npc.history}\n'
            user_prompt += f'Traits: {npc.traits}\n'
            user_prompt += f'Other notes: {npc.other_notes}\n'

        user_prompt += f'Glossary:\n'
        # Add glossary to user prompt
        for definition in glossary.items():
            user_prompt += f'{definition}\n'
    
        return user_prompt
    
    def consequences_system_prompt(self, outcome, consequences):

        system_prompt = f'''Given the {outcome} outcome of the scenario, select appropriate consequences for each character. Ensure that each consequence is justified based on the outcome and the character's involvement in the scene. List the consequences in a format ready for script execution, adhering to the following structure:

        - For each character, start with the character's name followed by their title in parenthesis and a colon.
        - List each consequence command on a new line below the character's name.
        - Each command should begin with the action, followed by the parameters in parentheses.
        - Always refer to characters by their title in commands.
        - Include at least one relationship update if multiple characters are present.

        Format your output as follows for clarity and direct execution in the script:

        For Pandora Dantill (Ancestor)
        update_stat('intelligence', 1)
        gain_trait('Maniacal')
        update_relationship_affinity('Miller', -3)
        End

        For Dalton (Miller)
        update_status_physical(-4)
        lose_equipment('Scythe')
        update_relationship_description('Ancestor', 'The Miller is eternally hateful for the fate the Ancestor cast him into')
        End
        '''
    

        system_prompt += f'Consequences:\n'
        for consequence in consequences:
            system_prompt += f'{consequence}\n'

        print(system_prompt)

        return system_prompt
    
    def consequences_user_prompt(self, event_story, characters):

        user_prompt = f'{event_story}\n\n'

        user_prompt += f'Characters:\n'
        # Add characters to user prompt
        for i in range(len(characters)):
            character = characters[i]
            user_prompt += f'Name: {character.name}\n'
            user_prompt += f'Title: {character.title}\n'
            user_prompt += f'Summary: {character.summary}\n'
            user_prompt += f'History: {character.history}\n'
            user_prompt += f'Traits: {character.traits}\n'
            user_prompt += f'Status: {character.status}\n'
            user_prompt += f'Stats: {character.stats}\n'
            user_prompt += f'Equipment: {character.equipment}\n'
            user_prompt += f'Trinkets: {character.trinkets}\n'
            user_prompt += f'Other notes: {character.other_notes}\n'

            
            # Check if the template has any relevant fields
            if getattr(self, 'relevant_fields', None):
                for field in self.relevant_fields:
                    user_prompt += f'{field}: {getattr(character, field)}\n'

            if len(characters) >= 2:
                user_prompt += 'Relationships:\n'
                for j in range(len(characters)):
                    for k in range(j+1, len(characters)):
                        user_prompt += f'{characters[j].title} and {characters[k].title}\n'
                        relationship_fields = ['affinity', 'relationship_type', 'description', 'history', 'other_notes']
                        for field in relationship_fields:
                            user_prompt += f'{field}: {characters[j].relationships[characters[k].title][field]}\n'
    
        return user_prompt
    
    def process_response(self, event_consequences, characters):
        # Split the output into lines for processing
        lines = event_consequences.split('\n')

        # Remove empty lines
        lines = [line for line in lines if line]

        # Variable to keep track of the current character being processed
        current_character = None

        # Iterate through each line in the output
        for line in lines:
            if line.startswith('For'):
                # Extract the character's name from the line
                character_name = line.split()[1].strip('()')
                current_character = next((char for char in characters if char.name == character_name), None)

            elif line[0].islower():
                # Command processing
                command_parts = line.split('(')
                command_name = command_parts[0]
                if len(command_parts) > 1:
                    # Extract parameters, removing the closing parenthesis and splitting parameters if needed
                    params = command_parts[1].strip(')').split(',')
                    # Convert parameters to their appropriate types; assume numerical params need conversion
                    processed_params = [int(param) if param.lstrip('-').isdigit() else param.strip("' ") for param in params]
                else:
                    processed_params = []

                # Execute the command if the character object is found
                if current_character:
                    # Get the method corresponding to the command_name
                    if hasattr(current_character, command_name):
                        method = getattr(current_character, command_name)
                        # Call the method with unpacked parameters
                        method(*processed_params)
            elif line.startswith('End'):
                # Reset current character when block ends
                current_character = None