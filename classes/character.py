# Class for character details
class Character:
    def __init__(self, title, name, level, money, summary, history, race, gender, religion, traits, status, stats, equipment, trinkets, appearance, clothing, combat, magic, notes, relationships):
        self.title = title
        self.name = name
        self.level = level
        self.money = money
        self.summary = summary
        self.history = history
        self.race = race
        self.gender = gender
        self.religion = religion
        self.traits = traits
        self.status = status
        self.stats = stats
        self.equipment = equipment
        self.trinkets = trinkets
        self.appearance = appearance
        self.clothing = clothing
        self.combat = combat
        self.magic = magic
        self.notes = notes
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
            race=data.get('race'),
            gender=data.get('gender'),
            religion=data.get('religion'),
            traits=data.get('traits'),
            status=data.get('status'),
            stats=data.get('stats'),
            equipment=data.get('equipment'),
            trinkets=data.get('trinkets'),
            appearance=data.get('appearance'),
            clothing=data.get('clothing'),
            combat=data.get('combat'),
            magic=data.get('magic'),
            notes=data.get('notes'),
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
            "race": self.race,
            "gender": self.gender,
            "religion": self.religion,
            "traits": self.traits,
            "status": self.status,
            "stats": self.stats,
            "equipment": self.equipment,
            "trinkets": self.trinkets,
            "appearance": self.appearance,
            "clothing": self.clothing,
            "combat": self.combat,
            "magic": self.magic,
            "notes": self.notes,
            "relationships": self.relationships
        }
    
    def fast_status_description(self, physical_state, mental_state, condition=None):

        if condition is not None:
            condition = condition.lower()

        physical_descriptions = {
            0: "on the brink of death due to severe injuries",
            1: "gravely injured",
            2: "critically injured",
            3: "severely injured",
            4: "very injured",
            5: "injured",
            6: "moderately injured",
            7: "slightly injured",
            8: "with minor injuries",
            9: "almost fully recovered",
            10: "in perfect physical condition"
        }
    
        mental_descriptions = {
            0: "feeling fine and mentally resolved",
            1: "feeling good and mentally stable",
            2: "maintaining a positive outlook",
            3: "generally composed",
            4: "mentally stable",
            5: "occasionally stressed but coping",
            6: "struggling with some stress",
            7: "experiencing frequent stress",
            8: "highly anxious and troubled",
            9: "emotionally distressed",
            10: "overwhelmed by severe stress"
        }
        
        condition_descriptions = {
            # Afflictions
            "fearful": "paralyzed by overwhelming fear and unable to think or act logically.",
            "paranoid": "consumed by intense paranoia, convinced their teammates will stab them in the back the moment they turn their back.",
            "selfish": "driven by extreme selfishness, ignoring the team in favor of personal safety.",
            "masochistic": "indulging in self-destructive behaviors in their strong desire for physical pain.",
            "abusive": "engaging in violently abusive actions towards friend and foe alike.",
            "hopeless": "crushed by a sense of utter hopelessness and sapped of all motivation.",
            "irrational": "acting with complete irrationality and mumbling utter nonsense.",
            "refracted": "tormented by incomprehensible cosmic horrors.",
            "rapturous": "lost in a state of ecstatic rapture.",
            "discordant": "battling uncontrollable multiple personalities.",
            "ferocious": "overcome by a ferocious, uncontrollable rage.",
            # Virtuous states
            "stalwart": "displaying unwavering determination.",
            "courageous": "exhibiting remarkable courage.",
            "focused": "possessing an intense focus.",
            "powerful": "radiating a commanding presence.",
            "vigorous": "brimming with energy and vitality."
        }
        
        description = f"Physically {physical_descriptions[physical_state]}, {mental_descriptions[mental_state]}"
        
        if condition and condition in condition_descriptions:
            conjunction = "and" # if mental_state <= 5 else "but"
            description += f" {conjunction} {condition_descriptions[condition]}"
        
        self.status['physical'] = physical_state
        self.status['mental'] = 10 - mental_state
        self.status['affliction'] = condition
        self.status['description'] = description
    
    def nothing(self):
        # Do nothing. This method exists just to handle the 'nothing' command gracefully.
        pass

    def update_stats(self, field, change):
        self.update_stat(self, field, change)

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

    def update_appearance(self, field, description):
        if field in self.appearance:
            self.appearance[field] = description
        else:
            print(f"Appearance attribute {field} does not exist.")

    def update_clothing(self, field, description):
        if field in self.clothing:
            self.clothing[field] = description
        else:
            print(f"Clothing attribute {field} does not exist.")

    def add_trait(self, trait):
        self.gain_trait(trait)

    def update_trait(self, trait):
        self.gain_trait(trait)

    def add_quirk(self, trait):
        self.gain_trait(trait)

    def gain_trait(self, trait):
        if trait not in self.traits:
            self.traits.append(trait)

    def lose_trait(self, trait):
        if trait in self.traits:
            self.traits.remove(trait)

    def add_note(self, note):
        self.gain_note(note)

    def gain_note(self, note):
        self.notes.append(note)

    def lose_note(self, note):
        if note in self.notes:
            self.notes.remove(note)

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

    def gain_combat_strength(self, strength):
        if strength not in self.combat['strengths']:
            self.combat['strengths'].append(strength)

    def lose_combat_strength(self, strength):
        if strength in self.combat['strengths']:
            self.combat['strengths'].remove(strength)

    def gain_combat_weakness(self, weakness):
        if weakness not in self.combat['weaknesses']:
            self.combat['weaknesses'].append(weakness)

    def lose_combat_weakness(self, weakness):
        if weakness in self.combat['weaknesses']:
            self.combat['weaknesses'].remove(weakness)

    def update_relationship_affinity(self, title, change):
        # If change is str +x change to int x
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        if title in self.relationships:
            self.relationships[title]['affinity'] += change
        else:
            print(f"No relationship with {title} exists to update affinity.")

    def update_relationship_dynamic(self, title, dynamic):
        if title in self.relationships:
            self.relationships[title]['dynamic'] = dynamic
        else:
            print(f"No relationship with {title} exists to update dynamic.")

    def update_relationship_description(self, title, description):
        if title in self.relationships:
            self.relationships[title]['description'] = description
        else:
            print(f"No relationship with {title} exists to update description.")

    def has_money(self, amount):
        # Check if the character has amount or more money
        return bool(self.money >= amount)

    def has_disease(self):
        # Check if the character has a disease
        return bool(self.status['diseases'])