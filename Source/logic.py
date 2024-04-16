from Source.storage import save_data, load_data, reset_characters
from Source.model import Character

import random

def pick_outcome(distribution):
    # Calculate the total sum of the distribution
    total_sum = sum(distribution)
    
    # Generate a random number between 1 and the total sum
    random_number = random.randint(1, total_sum)
    
    # Iterate through the distribution and find the corresponding outcome
    cumulative_sum = 0
    for i, count in enumerate(distribution):
        cumulative_sum += count
        if random_number <= cumulative_sum:
            return ['horrible', 'bad', 'neutral', 'good', 'excellent'][i]
        
def save_character(character):
    # Load the characters
    characters = load_data(Character)
    
    # Overwrite the character with the same title
    characters[character.title] = character
    
    # Save the characters
    save_data(characters, Character)

def find_character(character_title):

    # Load the characters
    characters = load_data(Character)

    if character_title in characters:
        return characters[character_title]
    else:
        print(f"Character with title '{character_title}' not found.")
        return None

def reset():
    reset_characters()
    characters = load_data(Character, 'Character_templates')
    return characters
