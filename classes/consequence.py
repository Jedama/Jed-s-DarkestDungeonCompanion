class Consequences:
    def __init__(self, title, consequences):
        self.title = title
        self.consequences = consequences

    @classmethod
    def from_dict(cls, data):
        return cls(data['title'], data['consequences'])
    
    def to_dict(self):
        return {
            "title": self.title,
            "consequences": self.consequences
        }