from Source.storage import load_data
from Source.logic import reset
from Source.happening import craft_happening_story
from Source.model import Character

characters = reset()

# Generate the prompt
story, consequences = craft_happening_story(characters)

print(story, '\n', consequences)

characters = load_data(Character)