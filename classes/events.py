from prompting import prompt_claude, clean_response_claude, system_prompts, consequences_prompts

class InputEvent:
    def __init__(self, category, title, num_characters, summary, outcomes, keywords, keyword_range, fields, length, npcs, locations, conditions, consequences):
        self.title = title
        self.category = category
        self.num_characters = num_characters
        self.summary = summary
        self.outcomes = outcomes
        self.keywords = keywords
        self.keyword_range = keyword_range
        self.fields = fields
        self.length = length
        self.npcs = npcs
        self.locations = locations
        self.conditions = conditions
        self.consequences = consequences
        self.name_to_title = {}  # Mapping of character names to titles for command processing
    

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title' , 'Event title'),
            category=data.get('category', 'random'),
            num_characters=data.get('num_characters', 1),
            summary=data.get('summary', 'Event summary'),
            outcomes=data.get('outcomes', [0, 0, 1, 0, 0]),
            keywords=data.get('keywords', []),
            keyword_range=data.get('keyword_range', [1, 5]),
            fields=data.get('fields', []),
            length=data.get('length', 1),
            npcs=data.get('npcs', []),
            locations=data.get('locations', []),
            conditions=data.get('conditions', {}),
            consequences=data.get('consequences', [])
        )
    
    def to_dict(self):
        return {
            "title": self.title,
            "category": self.category,
            "num_characters": self.num_characters,
            "summary": self.summary,
            "outcomes": self.outcomes,
            "keywords": self.keywords,
            "keyword_range": self.keyword_range,
            "fields": self.fields,
            "length": self.length,
            "npcs": self.npcs,
            "locations": self.locations,
            "conditions": self.conditions,
            "consequences": self.consequences
        }
    

class OutputEvent:
    def __init__(self, title, category, characters, summary = "", outcome = "Neutral", keywords = [], fields = [], length = 1, npcs = {}, factions = {}, enemies = {}, locations = {}, consequences = []):
        self.title = title
        self.category = category
        self.characters = characters
        self.summary = summary
        self.outcome = outcome
        self.keywords = keywords
        self.fields = fields
        self.length = length
        self.npcs = npcs
        self.locations = locations
        self.factions = factions
        self.enemies = enemies
        self.consequences = consequences
        self.name_to_title = {}  # Mapping of character names to titles for command processing
    

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            category=data.get('category'),
            characters=data.get('characters', {}),
            summary=data.get('summary', "Event summary"),
            outcome=data.get('outcome', 'Neutral'),
            keywords=data.get('keywords', []),
            fields=data.get('fields', []),
            length=data.get('length', 1),
            npcs=data.get('npcs', {}),
            locations=data.get('locations', {}),
            factions=data.get('factions', {}),
            enemies=data.get('enemies', {}),
            conditions=data.get('conditions', {}),
            consequences=data.get('consequences', [])
        )
    
    def to_dict(self):
        return {
            "title": self.title,
            "category": self.category,
            "characters": self.characters,
            "summary": self.summary,
            "outcome": self.outcome,
            "keywords": self.keywords,
            "fields": self.fields,
            "length": self.length,
            "npcs": self.npcs,
            "locations": self.locations,
            "factions": self.factions,
            "enemies": self.enemies,
            "consequences": self.consequences
        }
    
    def craft_event(self):

        self.name_to_title = {char.name: char.title for char in self.characters}

        system_prompt, user_prompt, assistant_prompt = self.create_story_prompt()

        # Call the prompt_claude function
        event_story = prompt_claude(user_prompt, system_prompt, assistant_prompt, max_tokens= 600 + 200 * self.length, temperature=1)
        event_story = clean_response_claude(event_story)

        print(event_story)

        bracket_index = event_story.find(']')
        if bracket_index != -1:
            event_title = event_story[:bracket_index].strip()
            event_story = event_story[bracket_index + 1:].lstrip('\n')
        else:
            event_title = "A darkest tale"
        

        system_prompt, user_prompt, assistant_prompt = self.create_consequences_prompt(event_story)
        event_consequences = prompt_claude(user_prompt, system_prompt, assistant_prompt, max_tokens= 450 + (100 * len(self.characters)), temperature=1)
        event_consequences = "For" + clean_response_claude(event_consequences)

        print(event_consequences)

        consequence_dict, logs = self.process_response(event_consequences)

        return event_title, event_story, consequence_dict, logs
    
    def create_story_prompt(self):

        # Create system prompt
        system_prompt = self.story_system_prompt()
        # Create user prompt
        user_prompt = self.story_user_prompt()
        # Create assistant prompt
        assistant_prompt = "Here is the story:\n ["

        return system_prompt, user_prompt, assistant_prompt
    
    def create_consequences_prompt(self, event_story):

        # Create system prompt
        system_prompt = self.consequences_system_prompt()
        # Create user prompt
        user_prompt = self.consequences_user_prompt(event_story)
        # Create assistant prompt
        assistant_prompt = "Consequences:\nFor"

        return system_prompt, user_prompt, assistant_prompt
    
    def story_system_prompt(self):

        system_prompt = system_prompts(self)

        return system_prompt
    
    def story_user_prompt(self):

        # Create user prompt
        user_prompt = f'{self.title}\n'
        user_prompt += f'{self.summary}\n'
        user_prompt += f'Modifiers: ' + ', '.join(self.keywords) + '\n'

        user_prompt += f'The characters faced a {self.outcome} outcome.\n\n'

        user_prompt += f'Characters:\n'
        # Add characters to user prompt
        for i in range(len(self.characters)):
            character = self.characters[i]
            user_prompt += f'Name: {character.name}\n'
            user_prompt += f'Title: {character.title}\n'
            user_prompt += f'Summary: {character.summary}\n'
            user_prompt += f'Religion: {character.religion}\n'
            user_prompt += f'Traits: {character.traits}\n'
            user_prompt += f'Status: {character.status}\n'
            user_prompt += f'Stats: {character.stats}\n'
            user_prompt += f'Appearance: {character.appearance}\n'
            user_prompt += f'Clothing: {character.clothing}\n'
            user_prompt += f'Equipment: {character.equipment}\n'
            user_prompt += f'Magic: {character.magic}\n'
            user_prompt += f'Other notes: {character.notes}\n'

            
            # Check if the template has any relevant fields
            if getattr(self, 'fields', None):
                for field in self.fields:
                    user_prompt += f'{field}: {getattr(character, field)}\n'

            if len(self.characters) >= 2:
                user_prompt += 'Relationships:\n'

                for j in range(len(self.characters)):
                    if i != j:  # Ensure we do not compare a character to themselves
                        user_prompt += f'{self.characters[i].title} and {self.characters[j].title}:\n'
                        
                        relationship_fields = ['affinity', 'dynamic', 'description']

                        # Check if the relationship exists
                        relationship_info = self.characters[i].relationships.get(self.characters[j].title)
                        if relationship_info:
                            for field in relationship_fields:
                                user_prompt += f'{field}: {relationship_info.get(field, "N/A")}\n'  # Safely get each field
                        else:
                            user_prompt += 'No specific relationship formed yet.\n'

        if self.npcs:
            user_prompt += f'NPCs:\n'
            # Add npcs to user prompt
            for npc in self.npcs.values():
                user_prompt += f'Title: {npc.title}\n'
                user_prompt += f'Name: {npc.name}\n'
                user_prompt += f'Summary: {npc.summary}\n'
                user_prompt += f'History: {npc.history}\n'
                user_prompt += f'Appearance: {npc.appearance}\n'
                user_prompt += f'Clothing: {npc.clothing}\n'
                user_prompt += f'Traits: {npc.traits}\n'
                user_prompt += f'Notes: {npc.notes}\n'

        if self.locations:
            user_prompt += f'Locations:\n'
            # Add location to user prompt
            for location in self.locations.items():
                user_prompt += f'{location}\n'
        
        if self.factions:
            user_prompt += f'Factions:\n'
            # Add Factions to user prompt
            for faction in self.locations.items():
                user_prompt += f'{faction}\n'
        
        if self.enemies:
            user_prompt += f'Enemies:\n'
            # Add enemy to user prompt
            for enemy in self.enemies.values():
                user_prompt += f'Title: {enemy.title}\n'
                user_prompt += f'Summary: {enemy.summary}\n'
                user_prompt += f'Race: {enemy.race}\n'
                user_prompt += f'Gender: {enemy.gender}\n'
                user_prompt += f'Faction: {enemy.faction}\n'
                user_prompt += f'Stats: {enemy.stats}\n'
                user_prompt += f'Equipment: {enemy.equipment}\n'
                user_prompt += f'Appearance: {enemy.appearance}\n'
                user_prompt += f'Clothing: {enemy.clothing}\n'
                user_prompt += f'Combat: {enemy.combat}\n'
                if hasattr(enemy, 'magic') and enemy.magic:
                    user_prompt += f'Magic: {enemy.magic}\n'
                if hasattr(enemy, 'notes') and enemy.notes:
                    user_prompt += f'Notes: {enemy.notes}\n'
    
        return user_prompt
    
    def consequences_system_prompt(self):

        system_prompt = consequences_prompts(self)
    
        system_prompt += f'Possible consequences:\n'
        for consequence in self.consequences:
            system_prompt += f'{consequence}\n'

        return system_prompt
    
    def consequences_user_prompt(self, event_story):

        user_prompt = f'{event_story}\n\n'

        user_prompt += f'Characters:\n'
        # Add characters to user prompt
        for i in range(len(self.characters)):
            character = self.characters[i]
            user_prompt += f'Name: {character.name}\n'
            user_prompt += f'Title: {character.title}\n'
            user_prompt += f'Summary: {character.summary}\n'
            user_prompt += f'History: {character.history}\n'
            user_prompt += f'Traits: {character.traits}\n'
            user_prompt += f'Status: {character.status}\n'
            user_prompt += f'Stats: {character.stats}\n'
            user_prompt += f'Appearance: {character.appearance}\n'
            user_prompt += f'Clothing: {character.clothing}\n'
            user_prompt += f'Trinkets: {character.trinkets}\n'
            user_prompt += f'Other notes: {character.notes}\n'

            
            # Check if the template has any relevant fields
            if getattr(self, 'fields', None):
                for field in self.fields:
                    user_prompt += f'{field}: {getattr(character, field)}\n'

            if len(self.characters) >= 2:
                user_prompt += 'Relationships:\n'
                for j in range(len(self.characters)):
                    for k in range(j+1, len(self.characters)):
                        user_prompt += f'{self.characters[j].title} and {self.characters[k].title}\n'
                        relationship_fields = ['affinity', 'dynamic', 'description']
                        for field in relationship_fields:
                            user_prompt += f'{field}: {self.characters[j].relationships[self.characters[k].title][field]}\n'
    
        return user_prompt
    
    def process_response(self, event_consequences):
        # Split the output into lines for processing
        lines = event_consequences.split('\n')

        # Remove empty lines
        lines = [line for line in lines if line.strip()]

        # Dictionary to store consequence text representations for each character
        consequences = {}
        logs = []

        # Variable to keep track of the current character being processed
        current_character = None

        # Iterate through each line in the output
        for line in lines:
            if line.startswith('For'):
                # Extract the character's title from the line
                # Assuming the format is "For 'Title' (Name)"
                title_start = line.find("'") + 1
                title_end = line.find("'", title_start)
                character_title = line[title_start:title_end]
        
                # Find the character object based on the title
                current_character = next((char for char in self.characters if char.title == character_title), None)

                consequences[character_title] = []

            elif line.startswith('Log'):
                # Extract the log message
                log_message = line[line.find('-') + 1:].strip()
                logs.append(log_message)
            
            elif line[0].islower():
                command_name, target, value = self.process_command(line)

                # Convert character names to titles if needed
                target = self.name_to_title.get(target, target)

                # Execute the command if the character object is found
                method = getattr(current_character, command_name)
                # Check if target is None, and call the method accordingly
                if target is not None:
                    result = method(target, value)  # Assuming the method requires two parameters: target and value
                else:
                    result = method(value)  # Assuming the method only requires value if target is None

                consequences[current_character.title].append(result)

            elif line.startswith('End'):
                # Reset current character when block ends
                current_character = None

        return consequences, logs

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
    

class QuickEvent:
    def __init__(self, category, title, characters, consequences = []):
        self.title = title
        self.category = category
        self.characters = characters
        self.consequences = consequences
    

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            category=data.get('category'),
            characters=data.get('characters', {}),
            consequences=data.get('consequences', [])
        )
    
    def to_dict(self):
        return {
            "title": self.title,
            "category": self.category,
            "characters": self.characters,
            "consequences": self.consequences
        }
    
    def craft_event(self, log, loot_money = 0, loot_trinkets = []):

        system_prompt, user_prompt, assistant_prompt = self.create_consequences_prompt(log, loot_money, loot_trinkets)
        event_consequences = prompt_claude(user_prompt, system_prompt, assistant_prompt, max_tokens= 450 + (100 * len(self.characters)), temperature=1)
        event_consequences = "For" + clean_response_claude(event_consequences)

        print(event_consequences)

        consequence_dict = self.process_response(event_consequences)

        return consequence_dict
    
    def create_consequences_prompt(self, log, loot_money, loot_trinkets):

        # Create system prompt
        system_prompt = self.consequences_system_prompt()
        # Create user prompt
        user_prompt = self.consequences_user_prompt(log, loot_money, loot_trinkets)
        # Create assistant prompt
        assistant_prompt = "Consequences:\nFor"

        return system_prompt, user_prompt, assistant_prompt
    
    def consequences_system_prompt(self):

        system_prompt = consequences_prompts(self)
    
        system_prompt += f'Possible consequences:\n'
        for consequence in self.consequences:
            system_prompt += f'{consequence}\n'

        return system_prompt
    
    def consequences_user_prompt(self, log, loot_money, loot_trinkets):

        user_prompt = f'Characters:\n'
        # Add characters to user prompt
        for i in range(len(self.characters)):
            character = self.characters[i]
            user_prompt += f'Name: {character.name}\n'
            user_prompt += f'Title: {character.title}\n'
            user_prompt += f'Summary: {character.summary}\n'
            user_prompt += f'History: {character.history}\n'
            user_prompt += f'Traits: {character.traits}\n'
            user_prompt += f'Status: {character.status}\n'
            user_prompt += f'Stats: {character.stats}\n'
            user_prompt += f'Appearance: {character.appearance}\n'
            user_prompt += f'Clothing: {character.clothing}\n'
            user_prompt += f'Trinkets: {character.trinkets}\n'
            user_prompt += f'Other notes: {character.notes}\n'

        if log:
            user_prompt += f'Dungeon Log:\n'
            for i in range(len(log)):
                user_prompt += f'Entry {i}: {loot_trinkets}\n'

        if loot_money > 0:
            user_prompt += f'Looted money: {loot_money}\n'

        if loot_trinkets:
            for i in range(len(loot_trinkets)):
                user_prompt += f'Looted trinket: {loot_trinkets}\n'
    
        return user_prompt
    
    def process_response(self, event_consequences):
        # Split the output into lines for processing
        lines = event_consequences.split('\n')

        # Remove empty lines
        lines = [line for line in lines if line.strip()]

        # Dictionary to store consequence text representations for each character
        consequences = {}

        # Variable to keep track of the current character being processed
        current_character = None

        # Iterate through each line in the output
        for line in lines:
            if line.startswith('For'):
                # Extract the character's title from the line
                # Assuming the format is "For 'Title' (Name)"
                title_start = line.find("'") + 1
                title_end = line.find("'", title_start)
                character_title = line[title_start:title_end]
        
                # Find the character object based on the title
                current_character = next((char for char in self.characters if char.title == character_title), None)

                consequences[character_title] = []

            elif line[0].islower():
                command_name, target, value = self.process_command(line)

                # Execute the command if the character object is found
                method = getattr(current_character, command_name)
                # Check if target is None, and call the method accordingly
                if target is not None:
                    result = method(target, value)  # Assuming the method requires two parameters: target and value
                else:
                    result = method(value)  # Assuming the method only requires value if target is None

                consequences[current_character.title].append(result)

            elif line.startswith('End'):
                # Reset current character when block ends
                current_character = None

        return consequences

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
    