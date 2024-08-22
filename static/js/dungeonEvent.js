import { fetchDungeonEvents, fetchEnemyNames } from './apiClient.js';
import { elementManager } from './elementManager.js';

let activeFaction = null;
let selectedFactions = [];
let selectedEnemies = [];

const factionGlowColors = {
    'Brigand': '#ffff00', // Yellow
    'Cultist': '#8b0000', // Dark red
    'Undead': '#ffffff'   // White
};

export function initializeDungeonEventModal() {
    createFactionButtons();
    populateDropdown();
    addGlowStyles();
}

async function createFactionButtons() {
    const buttonWrapper = elementManager.get('factionButtonsWrapper');
    
    const enemyData = await fetchEnemyNames();

    const factions = Object.keys(enemyData);

    factions.forEach(faction => {
        const factionButton = document.createElement('img');
        factionButton.classList.add('faction-button');
        factionButton.id = `faction-${faction}`;

        // Set background image
        factionButton.src = `/graphics/default/assets/button/${faction}.png`;

        // Add data attribute for glow color
        factionButton.dataset.glowColor = factionGlowColors[faction] || '#ffff00'; // Default to yellow if not specified

        // Add click event listener
        factionButton.addEventListener('click', () => handleFactionButtonClick(faction, enemyData[faction]));
        buttonWrapper.appendChild(factionButton);
    });
}

function updateFactionButtonStyles() {
    const factionButtons = document.querySelectorAll('.faction-button');
    factionButtons.forEach(button => {
        const faction = button.id.replace('faction-', '');
        if (selectedFactions.includes(faction)) {
            button.classList.add('selected');
            button.style.setProperty('--glow-color', button.dataset.glowColor);
        } else {
            button.classList.remove('selected');
        }
        
        if (faction === activeFaction) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
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

function handleFactionButtonClick(faction, enemies) {
    if (activeFaction === faction) {
        // Toggle faction selection
        if (selectedFactions.includes(faction)) {
            // Deselect the faction and its enemies
            selectedFactions = selectedFactions.filter(f => f !== faction);
            selectedEnemies = selectedEnemies.filter(e => !enemies.includes(e));
        } else {
            // Select only the faction, not its enemies
            if (selectedFactions.length < 4) {
                selectedFactions.push(faction);
            } else {
                console.log("Cannot select more than 4 factions in total.");
                // Optionally, you could add a visual feedback here
            }
        }
        activeFaction = null; // Close the list
        clearBountyList();
    } else {
        // Set as active faction and show enemy list
        activeFaction = faction;
        populateBountyList(enemies);
    }
    updateFactionButtonStyles();
    updateEnemyStyles();
}

function handleEnemySelection(enemy) {
    if (selectedEnemies.includes(enemy)) {
        // Deselect the enemy
        selectedEnemies = selectedEnemies.filter(e => e !== enemy);
        
        // Check if this was the last enemy from its faction
        const factionEnemies = document.querySelectorAll('.bounty-item');
        const anySelected = Array.from(factionEnemies).some(item => selectedEnemies.includes(item.textContent));
        
        if (!anySelected) {
            // If no enemies from this faction are selected, deselect the faction
            selectedFactions = selectedFactions.filter(f => f !== activeFaction);
        }
    } else if (selectedEnemies.length < 4) {
        // Select the enemy
        selectedEnemies.push(enemy);
        
        // Ensure the faction is selected
        if (!selectedFactions.includes(activeFaction)) {
            selectedFactions.push(activeFaction);
        }
    } else {
        console.log("Cannot select more than 4 enemies in total.");
        // Optionally, you could add a visual feedback here
    }
    
    updateEnemyStyles();
    updateFactionButtonStyles();
}

function updateEnemyStyles() {
    const bountyItems = document.querySelectorAll('.bounty-item');
    bountyItems.forEach(item => {
        if (selectedEnemies.includes(item.textContent)) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
}

function populateBountyList(enemies) {
    const bountyList = elementManager.get('dungeonEventBounty');
    bountyList.innerHTML = ''; // Clear existing content

    enemies.forEach(enemy => {
        const bountyItem = document.createElement('div');
        bountyItem.classList.add('bounty-item');
        if (selectedEnemies.includes(enemy)) {
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

        elementManager.get('dungeonEventDropdown').focus();

    } catch (error) {
        console.error('Error fetching character info:', error);
    }
}