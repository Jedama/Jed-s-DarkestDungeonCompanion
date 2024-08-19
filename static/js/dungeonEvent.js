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
        const factionButton = document.createElement('img');
        factionButton.classList.add('faction-button');
        factionButton.id = `faction-${faction}`;

        // Set background image
        factionButton.src = `/graphics/default/assets/button/${faction}.png`;
        
        // Add click event listener
        factionButton.addEventListener('click', () => handleFactionButtonClick(faction));
        
        buttonWrapper.appendChild(factionButton);
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