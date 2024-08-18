import { fetchDungeonEvents } from './apiClient.js';
import { elementManager } from './elementManager.js';

export function initializeDungeonEventModal() {

    createFactionButtons();
    populateDropdown();
}



function createFactionButtons() {
    const buttonWrapper = elementManager.get('factionButtonsWrapper');
    
    const factions = ['brigand', 'husk', 'unholy'];

    factions.forEach(faction => {
        const button = document.createElement('img');
        button.className = 'faction-button';
        button.id = `faction-${faction}`;

        // Set background image
        button.style.backgroundImage = `url('/graphics/default/assets/button/${faction}.png')`;
        
        // Add click event listener
        button.addEventListener('click', () => handleFactionButtonClick(faction));
        
        buttonWrapper.appendChild(button);
    });
}

function handleFactionButtonClick(factionName) {
    console.log(`${factionName} faction selected`);
    // Add your logic here for what should happen when a faction is selected
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