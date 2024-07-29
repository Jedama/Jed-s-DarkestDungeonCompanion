class NPC:
    def __init__(self, title, name, summary, history, traits, appearance, clothing, notes):
        self.title = title
        self.name = name
        self.summary = summary
        self.history = history
        self.traits = traits
        self.appearance = appearance
        self.clothing = clothing
        self.notes = notes

    @classmethod
    def from_dict(cls, data):
        # Creates an NPC from a dictionary
        return cls(
            title=data.get('title'),
            name=data.get('name'),
            summary=data.get('summary'),
            history=data.get('history'),
            traits=data.get('traits'),
            appearance=data.get('appearance'),
            clothing=data.get('clothing'),
            notes=data.get('notes', [])
        )

    def to_dict(self):
        # Converts the NPC to a dictionary
        return {
            "title": self.title,
            "name": self.name,
            "summary": self.summary,
            "history": self.history,
            "traits": self.traits,
            "appearance": self.appearance,
            "clothing": self.clothing,
            "notes": self.notes
        }
