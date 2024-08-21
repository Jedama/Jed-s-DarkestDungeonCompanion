import { fetchDungeonEvents, fetchEnemyNames } from './apiClient.js';
import { elementManager } from './elementManager.js';

export function initializeDungeonEventModal() {

    createFactionButtons();
    populateDropdown();
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

        // Add click event listener
        factionButton.addEventListener('click', () => handleFactionButtonClick(enemyData[faction]));
        buttonWrapper.appendChild(factionButton);
    });
}

function handleFactionButtonClick(enemies) {
    console.log(enemies);
    populateBountyList(enemies);
}

function populateBountyList(enemies) {
    const bountyList = elementManager.get('dungeonEventBounty');
    bountyList.innerHTML = ''; // Clear existing content

    enemies.forEach(enemy => {
        console.log(enemy)
        const bountyItem = document.createElement('div');
        bountyItem.classList.add('bounty-item');
        bountyItem.textContent = enemy;
        bountyList.appendChild(bountyItem);
    });
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