class ElementManager {
  constructor() {
    this.elements = {};
  }

  initialize() {
    this.elements = {
      savefileModal: document.getElementById("savefile-modal"),
      savefileSubmit: document.getElementById("savefile-submit"),
      savefileNameInput: document.getElementById("savefile-name"),
      saveButton: document.getElementById("save-button"),
      eventButton: document.getElementById("event-button"),
      recruitButton: document.getElementById("recruit-button"),
      characterGrid: document.getElementById("character-grid"),
      characterInfo: document.querySelector('.character-info'),
      characterTraits: document.getElementById('character-traits'),
      healthBookmark: document.querySelector('.health-bookmark'),
      mentalBookmark: document.querySelector('.mental-bookmark'),
      strengthStat: document.querySelector('.stat-item[data-stat="strength"]'),
      agilityStat: document.querySelector('.stat-item[data-stat="agility"]'),
      intelligenceStat: document.querySelector('.stat-item[data-stat="intelligence"]'),
      authorityStat: document.querySelector('.stat-item[data-stat="authority"]'),
      sociabilityStat: document.querySelector('.stat-item[data-stat="sociability"]'),
      storyModal: document.getElementById("story-modal"),
      returnButton: document.getElementById("return-btn"),
      continueButton: document.getElementById("continue-btn"),
      storyPanel: document.querySelector('.story-panel'),
      storyCards: document.querySelector('.story-cards'),
      recruitModal: document.getElementById("recruit-modal"),
      recruitDropdown: document.getElementById("recruit-dropdown"),
      recruitIcon: document.getElementById("recruit-icon"),
      recruitNameInput: document.getElementById("recruit-name"),
      recruitModifierInput: document.getElementById("recruit-modifier"),
      recruitModifierContainer: document.getElementById("recruit-modifier-container"),
      recruitHireButton: document.getElementById("recruit-hire"),
      dungeonEventModal: document.getElementById("dungeonevent-modal"),
      dungeonEventDropdown: document.getElementById("dungeonevent-dropdown"),
      dungeonEventBounty: document.getElementById('bounty-list'),
      dungeonEventProceed: document.getElementById('proceed-button'),
      factionButtonsWrapper: document.getElementById('faction-buttons-wrapper'),
      galleryView: document.getElementById('gallery-view'),
      dungeonView: document.getElementById('dungeon-view')
    };
  }

  get(elementName) {
    return this.elements[elementName];
  }

  getAll() {
    return this.elements;
  }
}

export const elementManager = new ElementManager();