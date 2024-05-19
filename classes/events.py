from prompting import prompt_claude, clean_response_claude, system_prompts, consequences_prompts

class Event:
    def __init__(self, type, title, num_characters, summary, outcome, keywords, relevant_fields, length, npcs, glossary, conditions, consequences):
        self.title = title
        self.type = type
        self.num_characters = num_characters
        self.summary = summary
        self.outcome = outcome
        self.keywords = keywords
        self.relevant_fields = relevant_fields
        self.length = length
        self.npcs = npcs
        self.glossary = glossary
        self.conditions = conditions
        self.consequences = consequences
        self.name_to_title = {}  # Mapping of character names to titles for command processing
    

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            type=data.get('type'),
            num_characters=data.get('num_characters'),
            summary=data.get('summary'),
            outcome=data.get('outcome', [0, 0, 1, 0, 0]),
            keywords=data.get('keywords', []),
            relevant_fields=data.get('relevant_fields', []),
            length=data.get('length', 1),
            npcs=data.get('npcs', []),
            glossary=data.get('glossary', []),
            conditions=data.get('conditions', []),
            consequences=data.get('consequences', [])
        )
    
    def to_dict(self):
        return {
            "title": self.title,
            "type": self.type,
            "num_characters": self.num_characters,
            "summary": self.summary,
            "outcome": self.outcome,
            "keywords": self.keywords,
            "relevant_fields": self.relevant_fields,
            "length": self.length,
            "npcs": self.npcs,
            "glossary": self.glossary,
            "conditions": self.conditions,
            "consequences": self.consequences
        }
    
    def craft_event(self, event_characters):

        self.name_to_title = {char.name: char.title for char in event_characters}

        system_prompt, user_prompt, assistant_prompt = self.create_story_prompt(event_characters)

        # Call the prompt_claude function
        event_story = prompt_claude(user_prompt, system_prompt, assistant_prompt, max_tokens= 350 + 200 * self.length)
        event_story = clean_response_claude(event_story)

        system_prompt, user_prompt, assistant_prompt = self.create_consequences_prompt(event_story, event_characters)

        event_consequences = prompt_claude(user_prompt, system_prompt, assistant_prompt, max_tokens= 250 + (50 * self.num_characters))
        event_consequences = "For" + clean_response_claude(event_consequences)

        self.process_response(event_consequences, event_characters)

        return event_story, event_consequences
    
    def create_story_prompt(self, event_characters):

        # Create system prompt
        system_prompt = self.story_system_prompt()
        # Create user prompt
        user_prompt = self.story_user_prompt(event_characters)
        # Create assistant prompt
        assistant_prompt = "Here is the story:"

        return system_prompt, user_prompt, assistant_prompt
    
    def create_consequences_prompt(self, event_story, event_characters):

        # Create system prompt
        system_prompt = self.consequences_system_prompt()
        # Create user prompt
        user_prompt = self.consequences_user_prompt(event_story, event_characters)
        # Create assistant prompt
        assistant_prompt = "Consequences:\nFor"

        return system_prompt, user_prompt, assistant_prompt
    
    def story_system_prompt(self):

        system_prompt = system_prompts(self)

        return system_prompt
    
    def story_user_prompt(self, event_characters):

        # In event summary, replace placeholders with character names
        summary = self.summary
        for i in range(self.num_characters):
            summary = summary.replace(f'[Character {i+1}]', event_characters[i].name)
            summary = summary.replace(f'[character {i+1}]', event_characters[i].name)

        # Create user prompt
        user_prompt = f'{self.title}\n'
        user_prompt += f'{summary}\n'
        user_prompt += f'Modifiers: ' + ', '.join(self.keywords) + '\n'

        user_prompt += f'The characters faced a {self.outcome} outcome.\n\n'

        user_prompt += f'Characters:\n'
        # Add characters to user prompt
        for i in range(len(event_characters)):
            character = event_characters[i]
            user_prompt += f'Name: {character.name}\n'
            user_prompt += f'Title: {character.title}\n'
            user_prompt += f'Summary: {character.summary}\n'
            user_prompt += f'History: {character.history}\n'
            user_prompt += f'Religion: {character.religion}\n'
            user_prompt += f'Traits: {character.traits}\n'
            user_prompt += f'Status: {character.status}\n'
            user_prompt += f'Stats: {character.stats}\n'
            user_prompt += f'Equipment: {character.equipment}\n'
            user_prompt += f'Trinkets: {character.trinkets}\n'
            user_prompt += f'Magic: {character.magic}\n'
            user_prompt += f'Other notes: {character.other_notes}\n'

            
            # Check if the template has any relevant fields
            if getattr(self, 'relevant_fields', None):
                for field in self.relevant_fields:
                    user_prompt += f'{field}: {getattr(character, field)}\n'

            if len(event_characters) >= 2:
                user_prompt += 'Relationships:\n'

                for j in range(len(event_characters)):
                    if i != j:  # Ensure we do not compare a character to themselves
                        user_prompt += f'{event_characters[i].title} and {event_characters[j].title}:\n'
                        relationship_fields = ['affinity', 'relationship_type', 'description', 'history', 'other_notes']
                        
                        # Check if the relationship exists
                        relationship_info = event_characters[i].relationships.get(event_characters[j].title)
                        if relationship_info:
                            for field in relationship_fields:
                                user_prompt += f'  {field}: {relationship_info.get(field, "N/A")}\n'  # Safely get each field
                        else:
                            user_prompt += '  No specific relationship formed yet.\n'

        user_prompt += f'NPCs:\n'
        # Add npcs to user prompt
        for npc in self.npcs.values():
            user_prompt += f'Title: {npc.title}\n'
            user_prompt += f'Name: {npc.name}\n'
            user_prompt += f'Summary: {npc.summary}\n'
            user_prompt += f'History: {npc.history}\n'
            user_prompt += f'Traits: {npc.traits}\n'
            user_prompt += f'Other notes: {npc.other_notes}\n'

        user_prompt += f'Glossary:\n'
        # Add glossary to user prompt
        for definition in self.glossary.items():
            user_prompt += f'{definition}\n'

        user_prompt += f'Possible consequences:\n'
        for consequence in self.consequences:
            user_prompt += f"{consequence.get('command')}\n"
    
        return user_prompt
    
    def consequences_system_prompt(self):

        system_prompt = consequences_prompts(self)
    

        system_prompt += f'Consequences:\n'
        for consequence in self.consequences:
            system_prompt += f'{consequence}\n'

        return system_prompt
    
    def consequences_user_prompt(self, event_story, event_characters):

        user_prompt = f'{event_story}\n\n'

        user_prompt += f'Characters:\n'
        # Add characters to user prompt
        for i in range(len(event_characters)):
            character = event_characters[i]
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

            if len(event_characters) >= 2:
                user_prompt += 'Relationships:\n'
                for j in range(len(event_characters)):
                    for k in range(j+1, len(event_characters)):
                        user_prompt += f'{event_characters[j].title} and {event_characters[k].title}\n'
                        relationship_fields = ['affinity', 'relationship_type', 'description', 'history', 'other_notes']
                        for field in relationship_fields:
                            user_prompt += f'{field}: {event_characters[j].relationships[event_characters[k].title][field]}\n'
    
        return user_prompt
    
    def process_response(self, event_consequences, event_characters):
        # Split the output into lines for processing
        lines = event_consequences.split('\n')

        # Remove empty lines
        lines = [line for line in lines if line.strip()]

        # Variable to keep track of the current character being processed
        current_character = None

        # Iterate through each line in the output
        for line in lines:
            if line.startswith('For'):
                # Extract the character's title from the line, assuming it's properly formatted like "For [Title]:"
                character_title = line.split()[1].strip('():')
                # Remove quotes if present, this step might be unnecessary if titles are not quoted
                character_title = character_title.strip("'")
                # Find the character object based on the title
                current_character = next((char for char in event_characters if char.title == character_title), None)

            elif line[0].islower():
                command_name, target, value = self.process_command(line)

                # Convert character names to titles if needed
                target = self.name_to_title.get(target, target)

                # Execute the command if the character object is found
                method = getattr(current_character, command_name)
                # Check if target is None, and call the method accordingly
                if target is not None:
                    method(target, value)  # Assuming the method requires two parameters: target and value
                else:
                    method(value)  # Assuming the method only requires value if target is None

            elif line.startswith('End'):
                # Reset current character when block ends
                current_character = None

    @staticmethod
    def process_command(command):
        # Find the first parenthesis to split the command name from the parameters
        idx = command.find('(')
        if idx == -1:
            return None, None, None  # Invalid command format

        command_name = command[:idx].strip()
        parameter_str = command[idx+1:-1]  # Exclude the last parenthesis

        # Split the parameters at the first comma and remove extra spaces
        idx = parameter_str.find("',")
        if idx == -1:
            argument = None
            value = parameter_str.strip()
        else:
            argument = parameter_str[:idx].strip()
            value = parameter_str[idx+2:].strip()
            argument = argument.strip("'")

        # Remove quotes if present
        value = value.strip("'")

        # Remove any + sign from the value
        value = value.replace('+', '')

        # Remove potential trailing ) from value
        value = value.strip(')')

        # Try converting value to int
        try:
            value = int(value)
        except ValueError:
            pass

        return command_name, argument, value
    