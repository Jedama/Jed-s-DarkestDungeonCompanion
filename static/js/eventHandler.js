// eventHandler.js
import { addCharacter, getState, updateCharacter, setEventCategory, updateRecruitInfo, addLog } from './state.js';
import { createEvent } from './events.js';

export class EventHandler {
    constructor(state) {
      this.state = state;
    }
  
    processEvent(eventData) {
      this.eventData = eventData;
      this.processCharacters();
      this.processLogs();
    }

    processCharacters() {
      Object.entries(this.eventData.characters || {}).forEach(([title, characterData]) => {
        updateCharacter(title, characterData);
      });
    }

    processLogs() {
      (this.eventData.logs || []).forEach(log => {
        addLog('story', log);
      });
    }
  
    getConsequences() {
      return this.eventData.consequences;
    }
}

export class EventHandlerFactory {
    static createHandler(eventCategory, state) {
        switch (eventCategory) {
        case 'random':
          return new RandomEventHandler(state);
        case 'dungeon':
          return new DungeonEventHandler(state);
        case 'recruit':
          return new RecruitEventHandler(state);
        case 'first_encounter':
          return new FirstEncounterEventHandler(state);  
        case 'quick_encounter':
          return new QuickEncounterEventHandler(state);  
        default:
            throw new Error(`Unsupported event category: ${eventCategory}`);
        }
    }
}
  
class RandomEventHandler extends EventHandler {
    // No need to override processEvent as it uses the base implementation
}
  
class RecruitEventHandler extends EventHandler {
    processEvent(eventData) {
        super.processEvent(eventData);
        // Additional recruit-specific logic
        Object.entries(this.eventData.characters).forEach(([title, characterData]) => {
            addCharacter(characterData);
        });
    }

    // Override processLogs to do nothing for recruit events
    processLogs() {}
}

class FirstEncounterEventHandler extends EventHandler {
    // No need to override processEvent as it uses the base implementation
}

class QuickEncounterEventHandler extends EventHandler {
    // No need to override processEvent as it uses the base implementation
}

class DungeonEventHandler extends EventHandler {
  processLogs() {
    (this.eventData.logs || []).forEach(log => {
      addLog('dungeon', log);
    });
  }
}

const eventHandlers = {
    random: {
      continue: () => {
        // Create a new random event
        createEvent('random', '', [], [], [], '');
      },
      return: () => {
        // Do nothing but close the modal
      }
    },
    recruit: {
      continue: handleRecruitContinue,
      return: handleRecruitReturn
    },
    first_encounter: {
      continue: handleRecruitContinue,
      return: () => {
        console.log('Returning from first_encounter event');
        // Implement recruit event return logic here
      }
    }
    // Add more event categorys as needed
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
        [],
        ''
      );
  
      // Update the event category
      setEventCategory('first_encounter', recruitTitle);
    } else {
      // Handle the case when all interesting characters have been encountered
      createEvent('random', '', [], [], [], '');
      
      setEventCategory('random', recruitTitle);
      // Reset recruit info
      updateRecruitInfo({
        recruitTitle: '',
        recruitGroups: [],
        recruitGroupsIndex: 0
      });
    }
  }

  async function handleRecruitReturn() {
    let state = getState();
  
    const recruitGroups = state.recruitGroups || [];
    const recruitTitle = state.recruitTitle || '';
  
    while (state.recruitGroupsIndex < recruitGroups.length) {
      const encounterGroup = recruitGroups[state.recruitGroupsIndex];
      
      // Create event for first encounter
      await createEvent(
        'quick_encounter',
        '',
        [recruitTitle, ...encounterGroup],  // Spread the encounterGroup array
        [],
        [],
        ''
      );

      state = getState();

      // Update recruit index
      updateRecruitInfo({
        recruitGroupsIndex: state.recruitGroupsIndex + 1
      });
  
      // Update the event category
      setEventCategory('quick_encounter', recruitTitle);
    } 
  }
  
  export default eventHandlers;