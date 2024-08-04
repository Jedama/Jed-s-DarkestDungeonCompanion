import { getState, subscribeToState, setDungeonTeam } from './state.js';
import { renderCharacterDetails } from './character.js';
import { elementManager } from './elementManager.js';

export function initializeDungeonView() {
    const dungeonView = elementManager.get('dungeonView');
    const dungeonCharacters = dungeonView.querySelector('.dungeon-characters');

    // Create character slots
    for (let i = 0; i < 4; i++) {
        const characterSlot = document.createElement('div');
        characterSlot.classList.add('dungeon-character');
        characterSlot.setAttribute('data-position', i);
        dungeonCharacters.appendChild(characterSlot);
    }

    // Subscribe to state changes
    subscribeToState(updateDungeonView);
}

export function updateDungeonView() {
    const state = getState();
    const dungeonTeam = state.dungeonTeam || [];
    const dungeonCharacters = elementManager.get('dungeonView').querySelectorAll('.dungeon-character');

    dungeonCharacters.forEach((slot, index) => {
        const characterTitle = dungeonTeam[index];
        const character = state.characters[characterTitle];
        if (character) {
            slot.style.backgroundImage = `url('/graphics/default/dungeon/${character.title.toLowerCase()}0.png')`;
            slot.onclick = () => renderCharacterDetails(character.title);

            // Add character name
            let nameElement = slot.querySelector('.character-name');
            if (!nameElement) {
                nameElement = document.createElement('h3');
                nameElement.classList.add('character-name');
                slot.appendChild(nameElement);
            }
            nameElement.textContent = character.name;

            // Add health and mental bars
            let barsElement = slot.querySelector('.character-bars');
            if (!barsElement) {
                barsElement = document.createElement('div');
                barsElement.classList.add('character-bars');
                barsElement.innerHTML = '<div class="health-bar"></div><div class="mental-bar"></div>';
                slot.appendChild(barsElement);
            }
            barsElement.querySelector('.health-bar').style.width = `${character.status.physical * 10}%`;
            barsElement.querySelector('.mental-bar').style.width = `${character.status.mental * 10}%`;
        } else {
            slot.style.backgroundImage = '';
            slot.onclick = null;
            slot.innerHTML = '';
        }
    });
}

export function switchToDungeonView(region) {
    const galleryView = elementManager.get('galleryView');
    const dungeonView = elementManager.get('dungeonView');
    
    galleryView.style.display = 'none';
    dungeonView.style.display = 'block';

    document.body.style.backgroundImage = `url('/graphics/default/background/${encodeURIComponent(region)}.png')`;

    updateDungeonView();
}