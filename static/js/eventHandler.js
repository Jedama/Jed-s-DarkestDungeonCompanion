// eventHandler.js
import { addCharacter, getState, updateCharacter, setEventType, updateRecruitInfo } from './state.js';
import { createEvent } from './events.js';

export class EventHandler {
    constructor(state) {
      this.state = state;
    }
  
    processEvent(eventData) {
      throw new Error("processEvent method must be implemented");
    }
  
    getConsequences() {
      throw new Error("getConsequences method must be implemented");
    }
}

export class EventHandlerFactory {
    static createHandler(eventType, state) {
        switch (eventType) {
        case 'random':
            return new RandomEventHandler(state);
        case 'recruit':
            return new RecruitEventHandler(state);
        case 'first_encounter':
            return new FirstencounterEventHandler(state);  
        default:
            throw new Error(`Unsupported event type: ${eventType}`);
        }
    }
}
  
class RandomEventHandler extends EventHandler {
    processEvent(eventData) {
      this.eventData = eventData;
      // Process the random event data
      Object.entries(eventData.characters).forEach(([title, characterData]) => {
        updateCharacter(title, characterData);
      });
    }
  
    getConsequences() {
      return this.eventData.consequences;
    }
}
  
class RecruitEventHandler extends EventHandler {
    processEvent(eventData) {
        this.eventData = eventData;

        // Process the recruit event data
        Object.entries(eventData.characters).forEach(([title, characterData]) => {
            addCharacter(characterData);
        });
    }
}

class FirstencounterEventHandler extends EventHandler {
  processEvent(eventData) {
      this.eventData = eventData;

      // Process the recruit event data
      Object.entries(eventData.characters).forEach(([title, characterData]) => {
        updateCharacter(title, characterData);
      });

      const state = getState();

      // Update recruit index
      updateRecruitInfo({
        recruitGroupsIndex: state.recruitGroupsIndex + 1
      });
  }
}

const eventHandlers = {
    random: {
      continue: () => {
        // Create a new random event
        createEvent('random', '', [], [], '');
      },
      return: () => {
        // Do nothing but close the modal
      }
    },
    recruit: {
      continue: handleRecruitContinue,
      return: () => {
        console.log('Returning from recruit event');
        // Implement recruit event return logic here
      }
    },
    first_encounter: {
      continue: handleRecruitContinue,
      return: () => {
        console.log('Returning from first_encounter event');
        // Implement recruit event return logic here
      }
    }
    // Add more event types as needed
  };

  function handleRecruitContinue() {
    const state = getState();
  
    const recruitGroups = state.recruitGroups || [];
    const currentIndex = state.recruitGroupsIndex || 0;
    const recruitTitle = state.recruitTitle || '';
  
    if (currentIndex < recruitGroups.length) {
      const encounterGroup = recruitGroups[currentIndex];
      
      // Create event for first encounter
      createEvent(
        'first_encounter',
        '',
        [recruitTitle, ...encounterGroup],  // Spread the encounterGroup array
        [],
        ''
      );
  
      // Update the event type
      setEventType('first_encounter', recruitTitle);
    } else {
      // Handle the case when all interesting characters have been encountered
      createEvent('random', '', [], [], '');
      // Reset recruit info
      updateRecruitInfo({
        recruitTitle: '',
        recruitGroups: [],
        recruitGroupsIndex: 0
      });
    }
  }
  
  export default eventHandlers;