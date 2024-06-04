class Enemy:
    def __init__(self, title, summary, race, gender, faction, stats, equipment, appearance, clothing, combat, magic, notes):
        self.title = title
        self.summary = summary
        self.race = race
        self.gender = gender
        self.faction = faction
        self.stats = stats
        self.equipment = equipment
        self.appearance = appearance
        self.clothing = clothing
        self.combat = combat
        self.magic = magic
        self.notes = notes

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            summary=data.get('summary'),
            race=data.get('race'),
            gender=data.get('gender'),
            faction=data.get('faction'),
            stats=data.get('stats'),
            equipment=data.get('equipment'),
            appearance=data.get('appearance'),
            clothing=data.get('clothing'),
            combat=data.get('combat'),
            magic=data.get('magic'),
            notes=data.get('notes')
        )

    def to_dict(self):
        return {
            "title": self.title,
            "summary": self.summary,
            "race": self.race,
            "gender": self.gender,
            "faction": self.faction,
            "stats": self.stats,
            "equipment": self.equipment,
            "appearance": self.appearance,
            "clothing": self.clothing,
            "combat": self.combat,
            "magic": self.magic,
            "notes": self.notes
        }