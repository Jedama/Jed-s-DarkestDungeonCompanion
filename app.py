from flask import Flask, request, jsonify, render_template, send_from_directory
from classes import Estate, Character
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

@app.route('/api/create-event', methods=['POST'])
def create_event_endpoint():
    data = request.json
    
    # Create an Estate instance with the data
    estate = Estate(data['estateName'])
    for title, char_data in data['characters'].items():
        character = Character.from_dict(char_data)
        estate.add_character(character)
    
    # Call the start_event method with the additional data
    input_category = data['eventCategory']
    input_event = data['eventTitle']
    input_titles = data['eventCharacters']
    input_modifiers = data['eventModifiers']
    input_name = data['recruitName']

    story_title = ''
    story_text = ''
    importance_list = []

    if input_category == 'recruit':
        story_title, story_text, consequence_dict, importance_list = estate.recruit(
            input_titles[0],
            input_modifiers,
            input_name,
        )
    elif input_category == 'first_encounter':
        
        estate.add_relationship_placeholder(input_titles)

        story_title, story_text, consequence_dict = estate.start_event(
            event_category = input_category,
            event_title = f'First Encounter {len(input_titles)}',
            titles = input_titles, 
            modifiers = input_modifiers
        )
    elif input_category == 'quick_encounter':

        estate.add_relationship_placeholder(input_titles)

        consequence_dict = estate.quick_encounter(
            event_category = input_category,
            event_title = f'Quick Encounter {len(input_titles)}',
            titles = input_titles
        )

    else:
        story_title, story_text, consequence_dict = estate.start_event(
            event_category = input_category,
            event_title = input_event, 
            titles = input_titles, 
            modifiers = input_modifiers
        )
        
    updated_characters = {title: estate.characters[title].to_dict() for title in consequence_dict.keys() if title in estate.characters}
    
    response_data = {
        'characters': updated_characters,
        'eventCategory': input_category,
        'title': story_title,  
        'storyText': story_text,
        'consequences': consequence_dict,
        'recruitGroups': importance_list
    }

    return jsonify(response_data), 200

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
    
# Helper function to check if an estate exists
def check_estate_exists(estate_name):
    return os.path.exists(f'estates/{estate_name}/estate.json')

if __name__ == '__main__':
    app.run(debug=True)