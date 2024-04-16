# Class for character details
class Character:
    def __init__(self, title, name, level, summary, history, religion, traits, status, stats, equipment, trinkets, appearance, fighting_style, magic, other_notes, relationships):
        self.title = title
        self.name = name
        self.level = level
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

# Class for happening details
class Happening:
    def __init__(self, title, num_characters, summary, outcome, relevant_fields, length):
        self.title = title
        self.num_characters = num_characters
        self.summary = summary
        self.outcome = outcome
        self.relevant_fields = relevant_fields
        self.length = length

# Class for consequence details
class Consequences:
    def __init__(self, title, consequences):
        self.title = title
        self.consequences = consequences