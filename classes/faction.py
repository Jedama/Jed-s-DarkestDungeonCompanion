class Faction:
    def __init__(self, title, description, appearance):
        self.title = title
        self.description = description
        self.appearance = appearance

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            description=data.get('description'),
            appearance=data.get('appearance')
        )
