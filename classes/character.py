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
            range(0, 11): "on the brink of death due to severe injuries",
            range(11, 21): "gravely injured",
            range(21, 31): "critically injured",
            range(31, 41): "severely injured",
            range(41, 51): "very injured",
            range(51, 61): "injured",
            range(61, 71): "moderately injured",
            range(71, 81): "slightly injured",
            range(81, 91): "with minor injuries",
            range(91, 101): "in perfect physical condition"
        }

        mental_descriptions = {
            range(0, 11): "feeling fine and mentally resolved",
            range(11, 21): "feeling good and mentally stable",
            range(21, 31): "maintaining a positive outlook",
            range(31, 41): "generally composed",
            range(41, 51): "mentally stable",
            range(51, 61): "occasionally stressed but coping",
            range(61, 71): "struggling with some stress",
            range(71, 81): "experiencing frequent stress",
            range(81, 91): "highly anxious and troubled",
            range(91, 101): "overwhelmed by severe stress"
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

        def get_description(state, descriptions):
            for range_key, description in descriptions.items():
                if state in range_key:
                    return description
            return "in an unknown state"

        physical_description = get_description(physical_state, physical_descriptions)
        mental_description = get_description(mental_state, mental_descriptions)

        description = f"Physically {physical_description}, {mental_description}"

        if condition and condition in condition_descriptions:
            conjunction = "and"
            description += f" {conjunction} {condition_descriptions[condition]}"

        self.status['physical'] = physical_state
        self.status['mental'] = 100 - mental_state
        self.status['affliction'] = condition
        self.status['description'] = description
    
    def nothing(self):
        # Do nothing. This method exists just to handle the 'nothing' command gracefully.
        pass

    def update_stats(self, field, change):
        return self.update_stat(self, field, change)

    def update_stat(self, field, change):
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        if field in self.stats:
            self.stats[field] = max(0, min(10, self.stats[field] + change))
            return f"{field.capitalize()} {'+' if change >= 0 else ''}{change}"
        else:
            return f"Stat {field} does not exist."

    def update_status_physical(self, change):
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        self.status['physical'] = max(0, min(10, self.status['physical'] + change))
        return f"Health {'+' if change >= 0 else ''}{change}"

    def update_status_mental(self, change):
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        self.status['mental'] = max(0, min(10, self.status['mental'] + change))
        return f"Mental {'+' if change >= 0 else ''}{change}"

    def update_status_description(self, description):
        self.status['description'] = description
        return "↻Status"

    def update_appearance(self, field, description):
        if field in self.appearance:
            self.appearance[field] = description
            return f"↻Appearance"
        else:
            return f"Appearance attribute {field} does not exist."

    def update_clothing(self, field, description):
        if field in self.clothing:
            self.clothing[field] = description
            return f"↻Clothing"
        else:
            return f"Clothing attribute {field} does not exist."

    def add_trait(self, trait):
        return self.gain_trait(trait)

    def update_trait(self, trait):
        return self.gain_trait(trait)

    def add_quirk(self, trait):
        return self.gain_trait(trait)

    def gain_trait(self, trait):
        if trait not in self.traits:
            self.traits.append(trait)
            return f"+'{trait}'"
        return f"Already has trait: {trait}"

    def lose_trait(self, trait):
        if trait in self.traits:
            self.traits.remove(trait)
            return f"-'{trait}'"
        return f"Didn't have trait: {trait}"

    def add_note(self, note):
        return self.gain_note(note)

    def gain_note(self, note):
        self.notes.append(note)
        return "+Note"

    def lose_note(self, note):
        if note in self.notes:
            self.notes.remove(note)
            return "-Note"
        return "Note not found"

    def gain_equipment(self, equipment):
        self.equipment.append(equipment)
        return f"+Equipment"

    def lose_equipment(self, equipment):
        if equipment in self.equipment:
            self.equipment.remove(equipment)
            return f"-Equipment"
        return f"Didn't have equipment: {equipment}"

    def gain_trinket(self, trinket):
        self.trinkets.append(trinket)
        return f"+Trinket"


    def lose_trinket(self, trinket):
        if trinket in self.trinkets:
            self.trinkets.remove(trinket)
            return f"-Trinket: {trinket}"
        return f"Didn't have trinket: {trinket}"
    
    def gain_wound(self, note):
        self.status['wounds'].append(note)
        return "+Wound"

    def update_summary(self, new_summary):
        self.summary = new_summary
        return "↻Summary"

    def update_history(self, new_history):
        self.history = new_history
        return "↻History"

    def update_religion(self, new_religion):
        self.religion = new_religion
        return "↻Religion"

    def gain_combat_strength(self, strength):
        if strength not in self.combat['strengths']:
            self.combat['strengths'].append(strength)
            return f"+Proficiency"
        return f"Already had combat strength: {strength}"

    def lose_combat_strength(self, strength):
        if strength in self.combat['strengths']:
            self.combat['strengths'].remove(strength)
            return f"-Proficiency"
        return f"Didn't have combat strength: {strength}"

    def gain_combat_weakness(self, weakness):
        if weakness not in self.combat['weaknesses']:
            self.combat['weaknesses'].append(weakness)
            return f"+Vulnerability"
        return f"Already had combat weakness: {weakness}"

    def lose_combat_weakness(self, weakness):
        if weakness in self.combat['weaknesses']:
            self.combat['weaknesses'].remove(weakness)
            return f"-Vulnerability"
        return f"Didn't have combat weakness: {weakness}"

    def update_relationship_affinity(self, title, change):
        if isinstance(change, str):
            change = int(change.replace('+', ''))

        if title in self.relationships:
            self.relationships[title]['affinity'] += change
            return f"[{title}] Affinity {'+' if change >= 0 else ''}{change}"
        else:
            return f"[{title}] No relationship"

    def update_relationship_dynamic(self, title, dynamic):
        if title in self.relationships:
            self.relationships[title]['dynamic'] = dynamic
            return f"[{title}] Dynamic update"
        else:
            return f"[{title}] No relationship"

    def update_relationship_description(self, title, description):
        if title in self.relationships:
            self.relationships[title]['description'] = description
            return f"[{title}] Desc. update"
        else:
            return f"[{title}] No relationship"

    def has_money(self, amount):
        # Check if the character has amount or more money
        return bool(self.money >= amount)

    def has_disease(self):
        # Check if the character has a disease
        return bool(self.status['diseases'])