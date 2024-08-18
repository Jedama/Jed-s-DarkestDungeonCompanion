import { getState, subscribeToState } from './state.js';
import { elementManager } from './elementManager.js';

export function renderCharacterList() {
    const updateList = () => {
        const state = getState();
        const characterGrid = elementManager.get('characterGrid');
        characterGrid.innerHTML = '';

        Object.entries(state.characters).forEach(([title, character]) => {
            const characterElement = document.createElement('div');
            characterElement.classList.add('character-item');

            const portraitImg = document.createElement('img');
            portraitImg.src = `/graphics/default/characters/portrait/${title.toLowerCase()}0.png`;
            portraitImg.alt = title;
            portraitImg.classList.add('portrait');

            const frameImg = document.createElement('img');
            const frameLevel = Math.min(character.level, 6);
            frameImg.src = `/graphics/default/assets/stat/level${frameLevel}.png`;
            frameImg.alt = 'frame';
            frameImg.classList.add('frame');

            characterElement.appendChild(portraitImg);
            characterElement.appendChild(frameImg);
            characterElement.addEventListener('click', () => renderCharacterDetails(title));

            characterGrid.appendChild(characterElement);
        });
    };

    updateList(); // Initial render
    return subscribeToState(updateList);
}

export function renderCharacterDetails(title) {
    const state = getState();
    const character = state.characters[title];
    if (!character) {
        console.error(`Character ${title} not found in state`);
        elementManager.get('characterInfo').innerHTML = `<p>Error loading character details</p>`;
        return;
    }

    const characterInfo = elementManager.get('characterInfo');

    // Update character portrait
    const characterPortrait = characterInfo.querySelector('#character-portrait');
    characterPortrait.src = `/graphics/default/characters/portrait/${character.title.toLowerCase()}0.png`;
    characterPortrait.alt = character.name;

    // Update character name
    const characterName = characterInfo.querySelector('#character-name');
    characterName.textContent = character.name;

    // Update character title
    const characterTitle = characterInfo.querySelector('#character-title');
    characterTitle.textContent = `the ${character.title}`;

    // Update trait list
    updateTraits(character.traits);

    // Update health bookmark
    updateBookmark('health', character.status.physical);

    // Update mental bookmark
    updateBookmark('mental', character.status.mental);

    updateCharacterStats(character);
}

function updateTraits(traits) {
    const traitList = elementManager.get('characterTraits');
    traitList.innerHTML = ''; // Clear existing traits

    traits.forEach(trait => {
        const li = document.createElement('li');
        li.textContent = trait;
        traitList.appendChild(li);
    });
}

function updateBookmark(category, status) {
    const bookmark = elementManager.get(`${category}Bookmark`);
    const maxHeight = 400; // Maximum height of the bookmark

    // Normalize status to 0-1 range
    const normalizedStatus = status / 100;

    // Determine texture based on status ranges
    let texture;
    if (normalizedStatus > 0.5) {
        texture = `${category}10`;
    } else if (normalizedStatus > 0.3) {
        texture = `${category}5`;
    } else if (normalizedStatus > 0) {
        texture = `${category}2`;
    } else {
        texture = `${category}0`;
    }

    // Calculate scale (0.5 to 1.3 range)
    const scale = 0.5 + (normalizedStatus * 0.5);

    // Update the background image
    bookmark.style.backgroundImage = `url('/graphics/default/assets/stat/${texture}.png')`;

    // Calculate and set the new height
    const newHeight = maxHeight * scale;
    bookmark.style.height = `${newHeight}px`;
}

function updateCharacterStats(character) {
    const stats = ['strength', 'agility', 'intelligence', 'authority', 'sociability'];
    stats.forEach(stat => {
        const statValue = character.stats[stat] || 0;
        const statItem = elementManager.get(`${stat}Stat`);

        if (statItem) {
            const romanNumeralElement = statItem.querySelector('.stat-number');
            if (romanNumeralElement) {
                romanNumeralElement.textContent = statValue;
            }

            // Update gem appearance
            const gemWrapper = statItem.querySelector('.gem-wrapper');
            if (gemWrapper) {
                // Remove old gem-level classes
                gemWrapper.classList.forEach(className => {
                    if (className.startsWith('gem-level-')) {
                        gemWrapper.classList.remove(className);
                    }
                });
                // Add new gem-level class
                gemWrapper.classList.add(`gem-level-${statValue}`);
            }
        }
    });
}