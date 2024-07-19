from flask import Flask, jsonify, render_template, request, send_from_directory
from classes import Estate
import os

app = Flask(__name__, static_url_path='', static_folder='static')

# Helper function to check if an estate exists
def check_estate_exists(estate_name):
    return os.path.exists(f'estates/{estate_name}/estate.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/estate/<estate_name>/save', methods=['POST'])
def save_estate(estate_name):
    try:
        estate = Estate.load_estate(estate_name)
        estate.save_estate()
        return jsonify({"status": "success", "message": f"Estate {estate_name} saved successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/characters/<estate_name>')
def get_characters(estate_name):
    estate = Estate.load_estate(estate_name)
    character_titles = [char.title for char in estate.characters.values()]
    return jsonify(character_titles)

@app.route('/api/character/<estate_name>/<title>')
def get_character_details(estate_name, title):
    estate = Estate.load_estate(estate_name)
    character = estate.characters.get(title)
    if character:
        return jsonify({
            "title": character.title,
            "name": character.name,
            "summary": character.summary,
            "history": character.history,
            "race": character.race,
            "gender": character.gender,
            "religion": character.religion,
            "traits": character.traits,
            "status": character.status,
            "stats": character.stats,
            "equipment": character.equipment,
            "trinkets": character.trinkets,
            "appearance": character.appearance,
            "clothing": character.clothing,
            "combat": character.combat,
            "magic": character.magic,
            "notes": character.notes,
            "relationships": character.relationships
        })
    return jsonify({"error": "Character not found"}), 404

@app.route('/api/estate/<estate_name>', methods=['GET'])
def load_or_create_estate(estate_name):
    if check_estate_exists(estate_name):
        estate = Estate.load_estate(estate_name)
        return jsonify({"message": f"Estate {estate_name} loaded", "status": "loaded"})
    else:
        estate = Estate(estate_name)
        estate.start_campaign()
        estate.save_estate()  # Make sure to save the new estate
        return jsonify({"message": f"Campaign started for estate {estate_name}", "status": "started"})

@app.route('/estates/<estate_name>/estate.json')
def serve_estate_json(estate_name):
    estate_path = os.path.join('estates', estate_name, 'estate.json')
    if os.path.exists(estate_path):
        return send_from_directory('estates', f'{estate_name}/estate.json')
    else:
        return jsonify({"error": "Estate not found"}), 404

@app.route('/api/character_titles', methods=['GET'])
def get_character_titles():
    character_titles = []
    template_dir = 'data/character_templates'
    try:
        for filename in os.listdir(template_dir):
            if filename.endswith('.json'):
                character_titles.append(os.path.splitext(filename)[0])
        return jsonify(sorted(character_titles))
    except FileNotFoundError:
        return jsonify({"error": "Character templates directory not found"}), 404
    except PermissionError:
        return jsonify({"error": "Permission denied when accessing character templates"}), 403
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)