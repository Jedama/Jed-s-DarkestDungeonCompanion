// state.js

// Create an object to hold our shared state
export const state = {
    // Object to store character information
    characters: {},

    // Estate name
    estateName: '',

    // Current Event Type
    currentEventType: null,

    // For recruit events
    recruitEvent: {
        newCharacter: null,
        interestingEncounters: [],
        currentEncounterIndex: 0
    }
};

export function addCharacter(character) {
    if (!character.title) {
        throw new Error('Character must have a name');
    }
    state.characters[character.title] = character;
}

export function removeCharacter(characterTitle) {
    delete state.characters[characterTitle];
}

export function updateCharacter(characterName, updatedInfo) {
    if (state.characters[characterName]) {
        state.characters[characterName] = { ...state.characters[characterName], ...updatedInfo };
    } else {
        throw new Error(`Character "${characterName}" not found`);
    }
}

export function overwriteCharacter(character) {
    if (!character.title) {
        throw new Error('Character must have a title');
    }
    state.characters[character.title] = character;
}

export function getCharacter(characterName) {
    return state.characters[characterName];
}

export function setEstateName(name) {
    state.estateName = name;
}

// Helper function to get all characters
export function getAllCharacters() {
    return state.characters;
}

// Helper function to get character titles
export function getCharacterTitles() {
    return Object.keys(state.characters);
}

export function setEventType(eventType, title) {
    state.currentEventType = eventType;

    if (eventType === 'Recruit') {
        // Reset recruit event state
        state.recruitEvent = {
            newCharacter: title,
            interestingEncounters: [],
            currentEncounterIndex: 0
        };
    }
}