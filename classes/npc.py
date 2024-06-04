class NPC:
    def __init__(self, title, name, summary, history, traits, appearance, notes, relationships):
        self.title = title
        self.name = name
        self.summary = summary
        self.history = history
        self.traits = traits
        self.appearance = appearance
        self.notes = notes
        self.relationships = relationships

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
            notes=data.get('notes', []),
            relationships=data.get('relationships', {})
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
            "notes": self.notes,
            "relationships": self.relationships
        }
