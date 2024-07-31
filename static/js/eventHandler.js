// eventHandler.js
import { addCharacter, updateCharacter } from './state.js';
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
  
    getConsequences() {
      return this.eventData.consequences;
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
      continue: () => {
        console.log('Continuing from recruit event');
        // Implement recruit event continue logic here
      },
      return: () => {
        console.log('Returning from recruit event');
        // Implement recruit event return logic here
      }
    }
    // Add more event types as needed
  };
  
  export default eventHandlers;