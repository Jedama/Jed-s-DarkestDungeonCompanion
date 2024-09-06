import { fetchDungeonEvents, fetchEnemyNames } from './apiClient.js';
import { elementManager } from './elementManager.js';
import { createEvent } from './events.js';
import { getState } from './state.js';

let activeFaction = null;
let selections = []; // Array to hold both faction and enemy selections
let enemyData = {}; // To store the mapping of factions to their enemies

const factionGlowColors = {
    'Brigand': '#ffff00',     // Yellow
    'Cultist': '#8b0000',     // Dark red
    'Beast': '#8b4513',       // Brown
    'Undead': '#ffffff',      // White
    'Swinefolk': '#f5deb3',   // Beige
    'Seafolk': '#ffc0cb',     // Pink
    'Fungoid': '#9b8b45',     // Muted yellow-brown
    'Bloodsucker': '#ff0000', // Red
    'Husk': '#00008b',        // Dark blue
    'Coven': '#000080',       // Navy blue
    'Ratfolk': '#808080',     // Gray
    'Ectomorph': '#e0ffff'    // Light cyan
};

export function initializeDungeonEventModal() {
    createFactionButtons();
    populateDropdown();
    setupProceedButton();
    addGlowStyles();
}

function setupProceedButton() {
    const proceedButton = elementManager.get('dungeonEventProceed');
    proceedButton.addEventListener('click', handleProceedButtonClick);
}

function handleProceedButtonClick() {
    const dungeonEventDropdown = elementManager.get('dungeonEventDropdown');
    const storyInput = elementManager.get('dungeonEventStory');

    const state = getState()

    const selectedEvent = dungeonEventDropdown.value;
    const storyDescription = storyInput.value;

    // Create the event using the selections and input data
    createEvent(
        'dungeon',
        selectedEvent,
        state.dungeonTeam,
        storyDescription,
        selections,  // This contains both faction and enemy selections
        ''
    );

    // Close the modal or perform any other necessary actions
    closeDungeonEventModal();
}

function closeDungeonEventModal() {
    const modal = elementManager.get('dungeonEventModal');
    modal.style.display = 'none';
    // Reset selections and other state as needed
    selections = [];
    activeFaction = null;
    updateFactionButtonStyles();
    clearBountyList();
}

async function createFactionButtons() {
    const buttonWrapper = elementManager.get('factionButtonsWrapper');
    
    enemyData = await fetchEnemyNames();

    const factions = Object.keys(enemyData);

    factions.forEach(faction => {
        const factionButton = document.createElement('img');
        factionButton.classList.add('faction-button');
        factionButton.id = `faction-${faction}`;

        factionButton.src = `/graphics/default/assets/button/${faction}.png`;
        factionButton.dataset.glowColor = factionGlowColors[faction] || '#ffff00';

        factionButton.addEventListener('click', () => handleFactionButtonClick(faction));
        buttonWrapper.appendChild(factionButton);
    });
}

function updateFactionButtonStyles() {
    const factionButtons = document.querySelectorAll('.faction-button');
    factionButtons.forEach(button => {
        const faction = button.id.replace('faction-', '');
        button.classList.remove('selected', 'active', 'inactive');
        
        if (selections.includes(faction) || enemyData[faction].some(enemy => selections.includes(enemy))) {
            button.classList.add('selected');
            button.style.setProperty('--glow-color', button.dataset.glowColor);
        }
        
        if (faction === activeFaction) {
            button.classList.add('active');
        } else if (activeFaction !== null && !selections.includes(faction)) {
            button.classList.add('inactive');
        }
    });
}

function addGlowStyles() {
    const style = document.createElement('style');
    style.textContent = `
        #faction-buttons-wrapper .faction-button.selected {
            filter: drop-shadow(0 0 10px var(--glow-color));
        }
    `;
    document.head.appendChild(style);
}

function handleFactionButtonClick(faction) {
    if (activeFaction === faction) {
        // Toggle faction selection
        if (selections.includes(faction)) {
            // Deselect the faction
            selections = selections.filter(item => item !== faction);
        } else {
            // Remove any individual enemies from this faction
            selections = selections.filter(item => !enemyData[faction].includes(item));
            
            // Select the faction if there's room
            if (selections.length < 4) {
                selections.push(faction);
            } else {
                console.log("Cannot select more than 4 items in total.");
                // Future: Add visual feedback here
            }
        }
        activeFaction = null; // Close the list
        clearBountyList();
    } else {
        // Set as active faction and show enemy list
        activeFaction = faction;
        populateBountyList(enemyData[faction]);
    }
    updateFactionButtonStyles();
    updateEnemyStyles();
}

function handleEnemySelection(enemy) {
    const faction = Object.keys(enemyData).find(faction => enemyData[faction].includes(enemy));
    
    if (selections.includes(enemy)) {
        // Deselect the enemy
        selections = selections.filter(item => item !== enemy);
    } else {
        // If the faction placeholder is selected, remove it
        if (selections.includes(faction)) {
            selections = selections.filter(item => item !== faction);
        }
        
        // If we're at the max selections, don't add the new enemy
        if (selections.length >= 4) {
            console.log("Cannot select more than 4 items in total.");
            // Future: Add visual feedback here
            return;
        }
        
        // Select the enemy
        selections.push(enemy);
    }
    
    updateEnemyStyles();
    updateFactionButtonStyles();
}

function updateEnemyStyles() {
    const bountyItems = document.querySelectorAll('.bounty-item');
    bountyItems.forEach(item => {
        if (selections.includes(item.textContent)) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
}

function populateBountyList(enemies) {
    const bountyList = elementManager.get('dungeonEventBounty');
    bountyList.innerHTML = '';

    enemies.forEach(enemy => {
        const bountyItem = document.createElement('div');
        bountyItem.classList.add('bounty-item');
        if (selections.includes(enemy)) {
            bountyItem.classList.add('selected');
        }
        bountyItem.textContent = enemy;
        bountyItem.addEventListener('click', () => handleEnemySelection(enemy));
        bountyList.appendChild(bountyItem);
    });
}

function clearBountyList() {
    const bountyList = elementManager.get('dungeonEventBounty');
    bountyList.innerHTML = '';
}

async function populateDropdown() {
    try {
        const dungeonEvents = await fetchDungeonEvents();

        elementManager.get('dungeonEventDropdown').innerHTML = dungeonEvents.map(char =>
            `<option value="${char}">${char}</option>`
        ).join('');

    } catch (error) {
        console.error('Error fetching character info:', error);
    }
}