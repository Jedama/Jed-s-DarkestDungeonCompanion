# Class for character details
class Character:
    def __init__(self, title, name, level, money, summary, history, religion, traits, status, stats, equipment, trinkets, appearance, fighting_style, magic, other_notes, relationships):
        self.title = title
        self.name = name
        self.level = level
        self.money = money
        self.summary = summary
        self.history = history
        self.religion = religion
        self.traits = traits
        self.status = status
        self.stats = stats
        self.equipment = equipment
        self.trinkets = trinkets
        self.appearance = appearance
        self.fighting_style = fighting_style
        self.magic = magic
        self.other_notes = other_notes
        self.relationships = relationships

    @classmethod
    def from_dict(cls, data):
        # Creates a character from a dictionary
        return cls(
            title=data.get('title'),
            name=data.get('name'),
            level=data.get('level'),
            money=data.get('money'),
            summary=data.get('summary'),
            history=data.get('history'),
            religion=data.get('religion'),
            traits=data.get('traits'),
            status=data.get('status'),
            stats=data.get('stats'),
            equipment=data.get('equipment'),
            trinkets=data.get('trinkets'),
            appearance=data.get('appearance'),
            fighting_style=data.get('fighting_style'),
            magic=data.get('magic'),
            other_notes=data.get('other_notes'),
            relationships=data.get('relationships')
        )

    def to_dict(self):
        # Converts the character to a dictionary
        return {
            "title": self.title,
            "name": self.name,
            "level": self.level,
            "summary": self.summary,
            "history": self.history,
            "religion": self.religion,
            "traits": self.traits,
            "status": self.status,
            "stats": self.stats,
            "equipment": self.equipment,
            "trinkets": self.trinkets,
            "appearance": self.appearance,
            "fighting_style": self.fighting_style,
            "magic": self.magic,
            "other_notes": self.other_notes,
            "relationships": self.relationships
        }
    
    def nothing(self):
        """ Do nothing. This method exists just to handle the 'nothing' command gracefully. """
        pass

    def update_stat(self, field, change):
        """ Update a specific stat by a given amount. """

        # If change is str +x change to int x
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        if field in self.stats:
            self.stats[field] += change
        else:
            print(f"Stat {field} does not exist.")

    def update_physical_state(self, change):
        """ Update the physical state of the character. """

        # If change is str +x change to int x
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        self.status['physical'] += change

    def update_mental_state(self, change):

        # If change is str +x change to int x
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        """ Update the mental state of the character. """
        self.status['mental'] += change

    def update_status_description(self, description):
        """ Update the overall status description of the character. """
        self.status['description'] = description

    def update_appearance_description(self, field, description):
        """ Update a specific feature of the character's appearance. """
        if field in self.appearance:
            self.appearance[field] = description
        else:
            print(f"Appearance attribute {field} does not exist.")

    def update_clothing_description(self, field, description):
        """ Update a specific piece of clothing's description. """
        if field in self.appearance['clothing']:
            self.appearance['clothing'][field] = description
        else:
            print(f"Clothing attribute {field} does not exist.")

    def gain_trait(self, trait):
        """ Add a new trait to the character. """
        if trait not in self.traits:
            self.traits.append(trait)

    def lose_trait(self, trait):
        """ Remove a trait from the character. """
        if trait in self.traits:
            self.traits.remove(trait)

    def gain_note(self, note):
        """ Add a note to the character's profile. """
        self.other_notes.append(note)

    def lose_note(self, note):
        """ Remove a note from the character's profile. """
        if note in self.other_notes:
            self.other_notes.remove(note)

    def gain_equipment(self, equipment):
        """ Add a piece of equipment to the character. """
        self.equipment.append(equipment)

    def lose_equipment(self, equipment):
        """ Remove a piece of equipment from the character. """
        if equipment in self.equipment:
            self.equipment.remove(equipment)

    def lose_trinket(self, trinket):
        """ Remove a trinket from the character. """
        if trinket in self.trinkets:
            self.trinkets.remove(trinket)

    def update_relationship_affinity(self, title, change):
        """ Update the affinity level within the relationship with another character. """
        if title in self.relationships:
            self.relationships[title]['affinity'] += change
        else:
            print(f"No relationship with {title} exists to update affinity.")

    def update_relationship_description(self, title, description):
        """ Update the description within the relationship with another character. """
        if title in self.relationships:
            self.relationships[title]['description'] = description
        else:
            print(f"No relationship with {title} exists to update description.")

    def update_relationship_history(self, title, history):
        """ Update the history within the relationship with another character. """
        if title in self.relationships:
            self.relationships[title]['history'] = history
        else:
            print(f"No relationship with {title} exists to update history.")

    def update_relationship_notes(self, title, notes):
        """ Update the notes within the relationship with another character. """
        if title in self.relationships:
            self.relationships[title]['other_notes'] = notes
        else:
            print(f"No relationship with {title} exists to update notes.")

    def has_money(self, amount):
        # Check if the character has amount or more money
        return bool(self.money >= amount)

    def has_disease(self):
        # Check if the character has a disease
        return bool(self.status['diseases'])