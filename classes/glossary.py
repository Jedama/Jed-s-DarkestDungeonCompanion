class GlossaryEntry:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            description=data['description']
        )

    def __repr__(self):
        return f"{self.title}: {self.description}"
