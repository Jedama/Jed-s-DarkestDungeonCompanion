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

  addModifier(modifier) {
    this.setState({
      eventModifiers: [
        ...this.state.eventModifiers,
        modifier
      ]
    });
  }

  clearModifiers() {
    this.setState({ eventModifiers: [] });
  }

  getModifiers() {
    return this.state.eventModifiers || [];
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

  setEventCategory(eventCategory) {
    this.setState({
      currentEventCategory: eventCategory,
      recruitTitle: this.state.recruitTitle,
      recruitGroups: this.state.recruitGroups || [],
      recruitGroupsIndex: this.state.recruitGroupsIndex || 0
    });
  }

  updateRecruitInfo(updatedInfo) {
    this.setState({
      recruitTitle: updatedInfo.recruitTitle || this.state.recruitTitle,
      recruitGroups: updatedInfo.recruitGroups || this.state.recruitGroups,
      recruitGroupsIndex: updatedInfo.recruitGroupsIndex !== undefined ? updatedInfo.recruitGroupsIndex : this.state.recruitGroupsIndex
    });
  }
}

// Initialize the state manager with the initial state
const initialState = {
  characters: {},
  estateName: '',
  eventModifiers: [],
  currentEventCategory: null,
  recruitTitle: '',
  recruitGroups: [],
  recruitGroupsIndex: 0
};

const stateManager = new StateManager(initialState);

// Export methods to interact with the state
export const getState = () => stateManager.getState();
export const setEstateName = (name) => stateManager.setEstateName(name);
export const addCharacter = (character) => stateManager.addCharacter(character);
export const removeCharacter = (characterTitle) => stateManager.removeCharacter(characterTitle);
export const addModifier = (modifier) => stateManager.addModifier(modifier);
export const clearModifiers = () => stateManager.clearModifiers();
export const getModifiers = () => stateManager.getModifiers();
export const updateCharacter = (characterTitle, updatedInfo) => stateManager.updateCharacter(characterTitle, updatedInfo);
export const setEventCategory = (eventCategory, title) => stateManager.setEventCategory(eventCategory, title);
export const updateRecruitInfo = (updatedInfo) => stateManager.updateRecruitInfo(updatedInfo);
export const subscribeToState = (listener) => stateManager.subscribe(listener);

// Helper functions
export const getAllCharacters = () => getState().characters;
export const getCharacterTitles = () => Object.keys(getState().characters);