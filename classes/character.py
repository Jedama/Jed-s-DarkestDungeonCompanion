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
        # Do nothing. This method exists just to handle the 'nothing' command gracefully.
        pass

    def update_stat(self, field, change):

        # If change is str +x change to int x
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        if field in self.stats:
            self.stats[field] += change
        else:
            print(f"Stat {field} does not exist.")

    def update_status_physical(self, change):

        # If change is str +x change to int x
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        self.status['physical'] += change

    def update_status_mental(self, change):

        self.status['mental'] += change

    def update_status_description(self, description):
        self.status['description'] = description

    def update_appearance_description(self, field, description):
        if field in self.appearance:
            self.appearance[field] = description
        else:
            print(f"Appearance attribute {field} does not exist.")

    def update_clothing_description(self, field, description):
        if field in self.appearance['clothing']:
            self.appearance['clothing'][field] = description
        else:
            print(f"Clothing attribute {field} does not exist.")

    def gain_trait(self, trait):
        if trait not in self.traits:
            self.traits.append(trait)

    def lose_trait(self, trait):
        if trait in self.traits:
            self.traits.remove(trait)

    def gain_note(self, note):
        self.other_notes.append(note)

    def lose_note(self, note):
        if note in self.other_notes:
            self.other_notes.remove(note)

    def gain_equipment(self, equipment):
        self.equipment.append(equipment)

    def lose_equipment(self, equipment):
        if equipment in self.equipment:
            self.equipment.remove(equipment)

    def lose_trinket(self, trinket):
        if trinket in self.trinkets:
            self.trinkets.remove(trinket)

    def update_summary(self, new_summary):
        self.summary = new_summary

    def update_history(self, new_history):
        self.history = new_history

    def update_religion(self, new_religion):
        self.religion = new_religion

    def gain_fighting_strength(self, strength):
        if strength not in self.fighting_style['strengths']:
            self.fighting_style['strengths'].append(strength)

    def lose_fighting_strength(self, strength):
        if strength in self.fighting_style['strengths']:
            self.fighting_style['strengths'].remove(strength)

    def gain_fighting_weakness(self, weakness):
        if weakness not in self.fighting_style['weaknesses']:
            self.fighting_style['weaknesses'].append(weakness)

    def lose_fighting_weakness(self, weakness):
        if weakness in self.fighting_style['weaknesses']:
            self.fighting_style['weaknesses'].remove(weakness)

    def update_relationship_affinity(self, title, change):
        # If change is str +x change to int x
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        if title in self.relationships:
            self.relationships[title]['affinity'] += change
        else:
            print(f"No relationship with {title} exists to update affinity.")

    def update_relationship_description(self, title, description):
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