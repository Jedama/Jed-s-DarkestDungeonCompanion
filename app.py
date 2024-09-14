from flask import Flask, request, jsonify, render_template, send_from_directory
from classes import Estate, Character
from storage import SaveEditor, ConfigManager
import json
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/save-estate', methods=['POST'])
def save_estate_endpoint():
    data = request.json
    
    # Create an Estate instance with the data
    estate = Estate(data['estateName'])
    for title, char_data in data['characters'].items():
        character = Character.from_dict(char_data)
        estate.add_character(character)
    
    # Call the save_estate method
    estate.save_estate()
    
    return jsonify({"message": "Estate saved successfully"}), 200

@app.route('/api/estates/<estate_name>/estate.json')
def serve_estate_json(estate_name):
    estate_path = os.path.join('estates', estate_name, 'estate.json')
    if os.path.exists(estate_path):
        return send_from_directory('estates', f'{estate_name}/estate.json')
    else:
        estate = Estate(estate_name)
        estate.start_campaign()
        estate.save_estate()
        return send_from_directory('estates', f'{estate_name}/estate.json')

from flask import jsonify, request
from werkzeug.exceptions import BadRequest

@app.route('/api/create-event', methods=['POST'])
def create_event_endpoint():
    try:
        data = request.json
        if not data:
            raise BadRequest("No JSON data provided")

        required_fields = ['estateName', 'characters', 'eventCategory', 'eventTitle', 'eventCharacters', 'eventModifiers', 'dungeonEnemies', 'recruitName']
        for field in required_fields:
            if field not in data:
                raise BadRequest(f"Missing required field: {field}")

        # Create an Estate instance with the data
        estate = Estate(data['estateName'])
        for title, char_data in data['characters'].items():
            character = Character.from_dict(char_data)
            estate.add_character(character)

        # Call the start_event method with the additional data
        input_category = data['eventCategory']
        input_event = data['eventTitle']
        input_titles = data['eventCharacters']
        input_modifiers = data['eventModifiers'].split(';')
        input_enemies = data['dungeonEnemies']
        input_name = data['recruitName']

        story_title = ''
        story_text = ''
        importance_list = []
        consequence_dict = {}

        if input_category == 'recruit':
            story_title, story_text, consequence_dict, importance_list = estate.recruit(
                input_titles[0],
                input_modifiers,
                input_name,
            )
        elif input_category == 'first_encounter':
            estate.add_relationship_placeholder(input_titles)
            story_title, story_text, consequence_dict, logs = estate.start_event(
                event_category=input_category,
                event_title=f'First Encounter {len(input_titles)}',
                titles=input_titles, 
                modifiers=input_modifiers
            )
        elif input_category == 'quick_encounter':
            estate.add_relationship_placeholder(input_titles)
            consequence_dict = estate.quick_encounter(
                event_category=input_category,
                event_title=f'Quick Encounter {len(input_titles)}',
                titles=input_titles
            )
        else:
            story_title, story_text, consequence_dict, logs = estate.start_event(
                event_category=input_category,
                event_title=input_event, 
                titles=input_titles, 
                modifiers=input_modifiers
            )
        
        updated_characters = {title: estate.characters[title].to_dict() for title in consequence_dict.keys() if title in estate.characters}
        
        response_data = {
            'characters': updated_characters,
            'eventCategory': input_category,
            'title': story_title,  
            'storyText': story_text,
            'consequences': consequence_dict,
            'logs': logs,
            'recruitGroups': importance_list
        }

        return jsonify(response_data), 200

    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f"Missing key in data: {str(e)}"}), 400
    except AttributeError as e:
        return jsonify({'error': f"Attribute error: {str(e)}"}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error in create_event_endpoint: {str(e)}")
        return jsonify({'error': "An unexpected error occurred"}), 500

@app.route('/api/update-dungeon-team', methods=['POST'])
def update_dungeon_team():
    data = request.json
    estate_name = data.get('estateName')

    try:
        # Load the estate
        estate = Estate(estate_name)

        # Add characters
        for unused_title, char_data in data['characters'].items():
            character = Character.from_dict(char_data)
            estate.add_character(character)

        estate.profile_id = data['estateID']
        estate.dungeon_team = data['dungeonTeam']

        # Initialize ConfigManager and SaveEditor
        config_manager = ConfigManager("config.json")
        save_editor = SaveEditor(config_manager)

        # Get the save data
        save_data = save_editor.decode_save(estate)

        updated_characters = save_editor.update_characters(estate, save_data)

        response_data = {
            'characters': updated_characters,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/api/default_character_info', methods=['GET'])
def get_default_character_info():
    character_info = {}
    template_dir = 'data/character_templates'
    try:
        for filename in os.listdir(template_dir):
            if filename.endswith('.json'):
                with open(os.path.join(template_dir, filename), 'r') as file:
                    data = json.load(file)
                    title = os.path.splitext(filename)[0]
                    character_info[title] = {
                        'default_name': data.get('name', ''),
                        'title': title
                    }
        return jsonify(character_info)
    except FileNotFoundError:
        return jsonify({"error": "Character templates directory not found"}), 404
    except PermissionError:
        return jsonify({"error": "Permission denied when accessing character templates"}), 403
    except json.JSONDecodeError:
        return jsonify({"error": f"Invalid JSON in file {filename}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route('/api/dungeon_events', methods=['GET'])
def get_dungeon_event_titles():
    event_titles = []
    events_dir = 'data/events/dungeon'
    try:
        for filename in os.listdir(events_dir):
            if filename.endswith('.json'):
                with open(os.path.join(events_dir, filename), 'r') as file:
                    events_data = json.load(file)
                    for event in events_data:
                        if event.get('category') == 'dungeon':
                            title = event.get('title')
                            if title:
                                event_titles.append(title)
        return jsonify(event_titles)
    except FileNotFoundError:
        return jsonify({"error": "Dungeon events directory not found"}), 404
    except PermissionError:
        return jsonify({"error": "Permission denied when accessing dungeon events"}), 403
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON in file {filename}: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/api/enemy-names', methods=['GET'])
def get_enemy_names():
    enemy_names = {}
    enemies_dir = 'Data/Enemies'

    try:
        for filename in os.listdir(enemies_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(enemies_dir, filename)
                with open(file_path, 'r') as file:
                    enemies_data = json.load(file)
                    for enemy in enemies_data:
                        enemy_title = enemy.get('title')
                        enemy_factions = enemy.get('faction')
                        
                        if enemy_title:
                            if isinstance(enemy_factions, str):
                                enemy_factions = [enemy_factions]
                            elif not isinstance(enemy_factions, list):
                                continue  # Skip if faction is neither a string nor a list
                            
                            for faction in enemy_factions:
                                if faction not in enemy_names:
                                    enemy_names[faction] = []
                                enemy_names[faction].append(enemy_title)

        return jsonify(enemy_names)
    except FileNotFoundError:
        return jsonify({"error": "Enemies directory not found"}), 404
    except PermissionError:
        return jsonify({"error": "Permission denied when accessing enemy files"}), 403
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON in file: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Helper function to check if an estate exists
def check_estate_exists(estate_name):
    return os.path.exists(f'estates/{estate_name}/estate.json')

if __name__ == '__main__':
    app.run(debug=True)