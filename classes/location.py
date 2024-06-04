class Location:
    def __init__(self, title, description, npcs):
        self.title = title
        self.description = description
        self.npcs = npcs

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            description=data.get('description'),
            npcs=data.get('npcs')
        )
