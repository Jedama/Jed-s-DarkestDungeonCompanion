from Source.claude import prompt_claude, extract_text_from_response_claude
from Source.consequences import apply_consequences
from Source.logic import pick_outcome
from Source.model import Happening, Consequences
from Source.storage import load_txt, load_data

import json
import random

def craft_happening_story(characters, happening=None):

    if happening is None:
        happenings = load_data(Happening)

        # Pick a random happening from the list of happenings
        happening = random.choice(list(happenings.values()))

    print(happening.title)

    num_characters = happening.num_characters

    # Initialize the scene_characters list      
    scene_characters = [None] * num_characters

    available_characters = list(characters.values())

    for i in range(num_characters):
        # Pick a random character from the list of characters
        scene_characters[i] = random.choice(available_characters)
        available_characters.remove(scene_characters[i])

    # Pick random outcome from distribution and translate to defined states
    outcome = pick_outcome(happening.outcome)

    print(outcome)

    # Load the keywords
    keywords_file_path = 'Keywords/keywords.txt'
    keywords = load_txt(keywords_file_path)
    
    # Pick 1-5 keywords from keyword list (randomly select the number of keywords and then the keywords themselves)
    num_keywords = random.randint(1, 5)
    chosen_keywords = random.sample(keywords, num_keywords)

    print(chosen_keywords)

    user_prompt_happening_story = createprompt_user_happening_story(happening, scene_characters, outcome, chosen_keywords)
    system_prompt_happening_story = createprompt_system_happening_story(happening)
    assistant_prompt_happening_story = "Here is the story:"

    happening_story = prompt_claude(user_prompt_happening_story, system_prompt_happening_story, assistant_prompt_happening_story, 300 + 100 * happening.length)
    extracted_story = extract_text_from_response_claude(happening_story)

    user_prompt_happening_consequences = f'{user_prompt_happening_story}\n\n{extracted_story}'
    system_prompt_happening_consequences = createprompt_system_happening_consequences(happening, scene_characters, outcome)
    assistant_prompt_happening_story = "Consequences:\nFor"

    # print(system_prompt_happening_consequences)

    extracted_consequences = "For"

    happening_consequences = prompt_claude(user_prompt_happening_consequences, system_prompt_happening_consequences, assistant_prompt_happening_story, 100 + (50 * num_characters))
    extracted_consequences += extract_text_from_response_claude(happening_consequences)

    apply_consequences(extracted_consequences)

    return extracted_story, extracted_consequences

# Create the user prompt for a happening
def createprompt_user_happening_story(happening, characters, outcome, keywords):

    user_prompt = f'{happening.title}\n'
    user_prompt += f'{happening.summary}\n'
    user_prompt += f'Keywords: ' + ', '.join(keywords) + '\n\n'

    user_prompt += f'The characters faced a {outcome} outcome.\n'

    # Generate the prompt
    for i in range(len(characters)):
        character = characters[i]
        user_prompt += f'[Character {i+1}]:\n'
        user_prompt += f'Name: {character.name}\n'
        user_prompt += f'Title: {character.title}\n'
        user_prompt += f'Summary: {character.summary}\n'
        user_prompt += f'History: {character.history}\n'
        user_prompt += f'Traits: {character.traits}\n'
        user_prompt += f'Status: {character.status}\n'
        user_prompt += f'Stats: {character.stats}\n'
        user_prompt += f'Equipment: {character.equipment}\n'
        user_prompt += f'Trinkets: {character.trinkets}\n'
        user_prompt += f'Other notes: {character.other_notes}\n'

        
        # Check if the template has any relevant fields
        if happening.relevant_fields:
            for field in happening.relevant_fields:
                user_prompt += f'{field}: {getattr(character, field)}\n'

        if len(characters) >= 2:
            user_prompt += 'Relationships:\n'
            for j in range(len(characters)):
                for k in range(j+1, len(characters)):
                    user_prompt += f'{characters[j].title} and {characters[k].title}\n'
                    relationship_fields = ['affinity', 'relationship_type', 'description', 'history', 'other_notes']
                    for field in relationship_fields:
                        user_prompt += f'{field}: {characters[j].relationships[characters[k].title][field]}\n'
    
    return user_prompt

# Create the system prompt for a happening
def createprompt_system_happening_story(happening):

    # Generate the prompt
    system_prompt = f'''You are the Ancestor, a spectral presence lingering malignantly over the once-grand estate that bears your legacy of doom. As the malevolent ghost haunting its decaying halls, you watch with a blend of disdain and delight the feeble efforts of the descendants and hired souls trying to reclaim and cleanse the estate. These poor souls battle against the eldritch horrors and abominations, the very ones you once summoned and manufactured in your ruthless quest for forbidden knowledge and power. Your role is to weave stories for these characters based on their traits and recent events. Focus on engaging, gothic-inspired storytelling that fits the grim and eerie atmosphere of the setting. Start your short story with a title'''

    system_prompt += f'Present the story of maximum {happening.length * 50 + 100} words with the outlined setting, keywords, outcome, and characters below:'

    return system_prompt

def createprompt_system_happening_consequences(happening, scene_characters, outcome):

    system_prompt = f'''Pick {random.randint(1, happening.length + 1)} consequences for each character from the list below, and output only the commands to update them. The characters faced a {outcome} outcome, reward or punish them appropriately. If multiple characters are present, include at least one relationship update. Example:\nFor Pandora Dantill (Ancestor)\nupdate_stat('Ancestor', 'strength', -1)\ngain_trait('Ancestor', 'Maniacal')\nupdate_relationship_affinity('Ancestor', 'Miller', -3)\n'''
    
    # Load consequences
    consequences = load_data(Consequences)

    # Pick consequence table
    if len(scene_characters) >= 2:
        consequence = consequences['Multiple_characters']
    else:
        consequence = consequences['Single_character']

    # Convert the consequence object to a dictionary
    consequence = vars(consequence)

    # Set the list of consequences based on the outcome
    json_text = json.dumps(consequence, indent=4)

    system_prompt += f'\n{json_text}'
    
    return system_prompt
