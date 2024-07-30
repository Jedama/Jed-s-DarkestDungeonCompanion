# promptlibrary.py

def system_prompts(event):
    system_prompt = (
        "You are the Ancestor, a malignant spectral presence haunting a once-grand estate. Describe the struggles of descendants and hired souls as they battle eldritch horrors and abominations in their attempts to reclaim and cleanse the estate. Focus on gruesome, gory details."
    )

    if event.type in ['random', 'story', 'dungeon']:
        system_prompt += (
            f'''\nConstruct a self-contained narrative vignette of {event.length * 100 + 200} words that:
                1. Fits the grim, eerie atmosphere
                2. Deepens characters and relationships
                3. Follows the scenario description and specific instructions, including outcome and modifiers
                4. Avoids introducing new powers, major story events, or significant changes to the overall state
                5. Adheres to characters' mental, physical, and affliction status
                6. Highlights negative afflictions and dysfunctional group dynamics (unless characters are healthy with compatible personalities)
                7. Horrible and Excellent outcome should represent characters doing vile things to each other and harming trust and vice versa

                Begin with a title within brackets [].'''
        )
    elif event.type == 'town':
        if event.title == 'Recruit':
            system_prompt += (
                "Your role is to present the new character as they step off the stagecoach, focusing on their appearance, mannerisms, and overall vibe. "
                "Highlight how their unique characteristics and personal quirks, listed in the modifiers section, influence their behavior and the townspeople's reactions. "
                "Avoid explicitly mentioning the provided quirks and traits, and focus on presenting them through the story."
            )
        if event.title == 'First Encounter':
            system_prompt += f"""
                Narrate the first meeting between the new character and existing character(s) in {event.length * 100 + 300} words. Adhere to the {event.outcome} outcome and story modifiers.

                - Focus on the new character's perspective and experiences.
                - If it's a group, ensure each character interacts with the new character.
                - Describe appearances, mannerisms, and behaviors, subtly showing unique traits.
                - Remember: Characters don't know each other or all details in their character data yet.
                - Capture initial impressions, atmosphere, and key moments that may shape future relationships.
                - Adapt the narrative for one-on-one or group dynamics as appropriate.

                This encounter sets the foundation for future interactions. Highlight how personalities and backgrounds influence this first meeting.
            """

    return system_prompt

def consequences_prompts(event):
    
    if event.type in ['random', 'story', 'dungeon']:
        consequences_prompt = f'''Given the {event.outcome} outcome of the scenario, select appropriate consequences for each character. Base the number of consequences and their severity based on the outcome. Ensure that each consequence is justified based on the outcome and the character's actions or thoughts in the scene. List the consequences in a format ready for script execution.

            - Start with the character's title in single quotation marks followed by their name in parenthesis and a colon.
            - List each consequence command on a new line below the character's title.
            - Each command should begin with the action, followed by the parameters in parentheses.
            - Always refer to characters by their title.
            - If there are no consequences for a character, proceed immediately to "For [next title (name)]".
            - Only select consequences clearly stated or implied in the attached vignette.
            - When updating a text field, try melding the new information into what is already present.
            - Each character's description should be self-contained and not mention other characters directly. References to other characters should be made exclusively within the defined relationship context.
            - Avoid mentioning things that occured during the vignette, instead focus on how the characters in general have changed as a consequence of it.
            - If the outcome is "Contextual", infer it from the story.
            - Completely ignore the NPCs, and don't create any relationship consequences if there is only one chracter in the scene.
            
            Format your output as follows for clarity and direct execution in the script: (This example had a 'horrible' outcome)

            For 'Ancestor' (Pandora Dantill)
            update_stat('intelligence', 1)
            gain_trait('Maniacal')
            gain_note('Uses an abundance of mustache cream')
            update_relationship_affinity('Miller', -3)
            End

            For 'Miller' (Dalton)
            update_status_physical(-4)
            gain_note('Corrupted by cosmic fractures')
            update_relationship_description('Ancestor', 'The Miller is eternally hateful for the fate the Ancestor cast him into')
            End
            '''
    elif event.type == 'town':
        if event.title == 'Recruit':
            consequences_prompt = f'''Given the template and modifiers, update the template character sheet through outputting the functions below in a format ready for script execution.

            Modifiers: {', '.join(event.keywords)}

            - Start with the character's title in single quotation marks followed by their name in parenthesis and a colon.
            - List each consequence command on a new line below the character's title.
            - Each command should begin with the action, followed by the parameters in parentheses.
            - Always refer to characters by their title.
            - Only modify the things relevant to the modifiers

            Format your output as follows for clarity and direct execution in the script:

            Example output given Ancestor with modifiers ['Overconfident', 'Curious', 'Aging']

            For 'Ancestor' (Pandora Dantill)
            update_stat('intelligence', 1)
            update_summary('The Ancestor, the forebearer of ruin, whose insatiable curiosity and hubris tore asunder the veil of reality, beckoning forth the Darkest Dungeon. He gambled his legacy and the safety of the realm on forbidden occult practices, only to doom his lineage and land.')
            gain_fighting_strength('Cataclysmic spells')
            gain_note('Would sacrifice anything for his ambitions')
            update_appearance('hair_color', 'Graying')
            End
            '''
        if event.title in ['First Encounter 2', 'First Encounter 3', 'First Encounter 4']:
            consequences_prompt = f'''Initialize the character relationships between the new character and those present in the scene by outputting the functions below in a format ready for script execution:

                - Start with the character's title in single quotes, followed by their name in parentheses and a colon.
                - List each consequence command on a new line below the character's title.
                - Begin each command with the action, followed by the parameters in parentheses.
                - Always refer to characters by their title.
                - Update affinity, dynamic, description, and history for both characters. Remember that relationships are often asymmetrical.
                - Set affinity to a value between 1 and 8, where 4 represents a neutral interaction.
                - Ensure that the interactions are portrayed accurately.
                

                Format your output as follows for clarity and direct execution in the script. Example:

                For 'Ancestor' (Pandora Dantill)
                update_relationship_affinity('Miller', 2)
                update_relationship_dynamic('Miller', 'Indifference')
                update_relationship_description('Miller', 'The Ancestor sees the Miller as someone to manipulate for his own ends while being aware of the Miller’s seething resentment.')

                For 'Miller' (Dalton)
                update_relationship_affinity('Ancestor', 0)
                update_relationship_dynamic('Ancestor', 'Deep Hatred')
                update_relationship_description('Ancestor', 'The Miller is eternally hateful for the fate the Ancestor cast him into, harboring a burning desire for revenge against the Ancestor’s relentless cruelty.')
                End

            '''
            

    return consequences_prompt