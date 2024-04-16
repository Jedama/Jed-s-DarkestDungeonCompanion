from Source.logic import find_character, save_character
import ast

def apply_consequences(response):
    lines = response.split("\n")

    # Removing empty lines and stripping white spaces
    lines = [line.strip() for line in lines if line.strip()]

    # Removing lines that start with a capital letter
    commands = [line for line in lines if not line[0].isupper()]

    # Processing each command
    for command in commands:
        # Extracting the function name and the argument part
        func_name, args_str = command.split('(', 1)
        # Evaluate the arguments string to actual arguments
        args = ast.literal_eval('(' + args_str)
        # Call the function with the unpacked arguments
        command_dispatcher[func_name](*args)


def nothing():
    print("No action is taken.")

def update_stat(character_title, field, change):

    # Find the character with the specified title
    character = find_character(character_title)
    character.stats[field] += change

    save_character(character)


def update_physical_state(character_title, change):

    # Find the character with the specified title
    character = find_character(character_title)
    character.status['physical'] += change

    save_character(character)

def update_mental_state(character_title, change):

    # Find the character with the specified title
    character = find_character(character_title)
    character.status['mental'] += change

    save_character(character)

def update_relationship_affinity(character_title, relationship_title, change):

    # Find the character with the specified title
    character = find_character(character_title)
    character.relationships[relationship_title]['affinity'] += change

    save_character(character)

def update_status_description(character_title, description):

    # Find the character with the specified title
    character = find_character(character_title)
    character.status['description'] = description

    save_character(character)

def update_appearance_description(character_title, field, description):
    
    # Find the character with the specified title
    character = find_character(character_title)
    character.appearance[field] = description

    save_character(character)

def update_clothing_description(character_title, field, description):
    
    # Find the character with the specified title
    character = find_character(character_title)
    character.appearance['clothing'][field] = description

    save_character(character)

def gain_trait(character_title, trait):
    
    # Find the character with the specified title
    character = find_character(character_title)
    character.traits.append(trait)

    save_character(character)

def lose_trait(character_title, trait):
    # Find the character with the specified title

    character = find_character(character_title)
    character.traits.remove(trait)

    save_character(character)

def gain_note(character_title, note):
    
    # Find the character with the specified title
    character = find_character(character_title)

    # Add the note to the character's notes
    character.other_notes.append(note)

    save_character(character)

def lose_note(character_title, note):
    # Find the character with the specified title

    character = find_character(character_title)

    # Remove the note from the character's notes
    character.notes.remove(note)
    print(f"{character_title} loses a note: {note}.")

    save_character(character)

def lose_trinket(character_title, trinket):
    # Find the character with the specified title

    character = find_character(character_title)

    # Remove the trinket from the character's trinkets
    character.trinkets.remove(trinket)
    print(f"{character_title} loses a trinket: {trinket}.")

    save_character(character)

def gain_equipment(character_title, equipment):
    # Find the character with the specified title

    character = find_character(character_title)

    # Add the equipment to the character's equipment
    character.equipment.append(equipment)
    print(f"{character_title} gains new equipment: {equipment}.")

    save_character(character)

def lose_equipment(character_title, equipment):

    # Find the character with the specified title
    character = find_character(character_title)
    character.equipment.remove(equipment)

    save_character(character)

def update_relationship_description(character_title, relationship_title, description):

    # Find the character with the specified title
    character = find_character(character_title)
    character.relationships_description[relationship_title] = description

    save_character(character)

def update_relationship_history(character_title, relationship_title, history):

    # Find the character with the specified title
    character = find_character(character_title)
    character.relationships[relationship_title]['history'] = history

    save_character(character)

def update_relationship_notes(character_title, relationship_title, notes):

    # Find the character with the specified title
    character = find_character(character_title)
    character.relationships[relationship_title]['other_notes'] = notes

    save_character(character)

command_dispatcher = {
    "nothing": nothing,
    "update_stat": update_stat,
    "update_physical_state": update_physical_state,
    "update_mental_state": update_mental_state,
    "update_relationship_affinity": update_relationship_affinity,
    "update_status_description": update_status_description,
    "update_appearance_description": update_appearance_description,
    "update_clothing_description": update_clothing_description,
    "gain_note": gain_note,
    "lose_note": lose_note,
    "gain_trait": gain_trait,
    "lose_trait": lose_trait,
    "lose_trinket": lose_trinket,
    "gain_equipment": gain_equipment,
    "lose_equipment": lose_equipment,
    "update_relationship_description": update_relationship_description,
    "update_relationship_history": update_relationship_history,
    "update_relationship_notes": update_relationship_notes
}