// state.js

class StateManager {
    constructor(initialState) {
      this.state = initialState;
      this.listeners = [];
    }
  
    getState() {
      return this.state;
    }
  
    setState(newState) {
      this.state = { ...this.state, ...newState };
      this.notifyListeners();
    }
  
    subscribe(listener) {
      this.listeners.push(listener);
      return () => {
        this.listeners = this.listeners.filter(l => l !== listener);
      };
    }
  
    notifyListeners() {
      this.listeners.forEach(listener => listener(this.state));
    }
  
    // Specific state update methods
    setEstateName(name) {
        console.log("Setting estate name:", name);
        this.setState({ estateName: name });
    }
  
    addCharacter(character) {
      if (!character.title) {
        throw new Error('Character must have a title');
      }
      this.setState({
        characters: {
          ...this.state.characters,
          [character.title]: character
        }
      });
    }
  
    removeCharacter(characterTitle) {
      const { [characterTitle]: removed, ...remainingCharacters } = this.state.characters;
      this.setState({ characters: remainingCharacters });
    }
  
    updateCharacter(characterTitle, updatedInfo) {
      if (this.state.characters[characterTitle]) {
        this.setState({
          characters: {
            ...this.state.characters,
            [characterTitle]: { ...this.state.characters[characterTitle], ...updatedInfo }
          }
        });
      } else {
        throw new Error(`Character "${characterTitle}" not found`);
      }
    }
  
    setEventType(eventType, title) {
      this.setState({
        currentEventType: eventType,
        recruitEvent: eventType === 'Recruit' ? {
          newCharacter: title,
          interestingEncounters: [],
          currentEncounterIndex: 0
        } : null
      });
    }
  }
  
  // Initialize the state manager with the initial state
  const initialState = {
    characters: {},
    estateName: '',
    currentEventType: null,
    recruitEvent: null
  };
  
  const stateManager = new StateManager(initialState);
  
  // Export methods to interact with the state
  export const getState = () => stateManager.getState();
  export const setEstateName = (name) => stateManager.setEstateName(name);
  export const addCharacter = (character) => stateManager.addCharacter(character);
  export const removeCharacter = (characterTitle) => stateManager.removeCharacter(characterTitle);
  export const updateCharacter = (characterTitle, updatedInfo) => stateManager.updateCharacter(characterTitle, updatedInfo);
  export const setEventType = (eventType, title) => stateManager.setEventType(eventType, title);
  export const subscribeToState = (listener) => stateManager.subscribe(listener);
  
  // Helper functions
  export const getAllCharacters = () => getState().characters;
  export const getCharacterTitles = () => Object.keys(getState().characters);