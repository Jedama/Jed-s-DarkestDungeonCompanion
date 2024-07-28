import { getAllCharacters, getCharacter } from './state.js';

export function renderCharacterList(elements) {
    elements.characterGrid.innerHTML = '';
    const characters = getAllCharacters();
    
    Object.entries(characters).forEach(([title, character]) => {
        const characterElement = document.createElement('div');
        characterElement.classList.add('character-item');
        
        const portraitImg = document.createElement('img');
        portraitImg.src = `/graphics/default/portraits/${title.toLowerCase()}0.png`;
        portraitImg.alt = title;
        portraitImg.classList.add('portrait');
        
        const frameImg = document.createElement('img');
        const frameLevel = Math.min(character.level, 6);
        frameImg.src = `/graphics/default/background/level${frameLevel}.png`;
        frameImg.alt = 'frame';
        frameImg.classList.add('frame');
        
        characterElement.appendChild(portraitImg);
        characterElement.appendChild(frameImg);
        characterElement.addEventListener('click', () => renderCharacterDetails(title));
        
        elements.characterGrid.appendChild(characterElement);
    });
}

export function renderCharacterDetails(title) {
    const character = getCharacter(title);
    if (!character) {
        console.error(`Character ${title} not found in state`);
        document.querySelector('.character-info').innerHTML = `<p>Error loading character details</p>`;
        return;
    }

    const characterInfo = document.querySelector('.character-info');

    // Update character portrait
    const characterPortrait = characterInfo.querySelector('#character-portrait');
    characterPortrait.src = `/graphics/default/portraits/${character.title.toLowerCase()}0.png`;
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
    const traitList = document.getElementById('character-traits');
    traitList.innerHTML = ''; // Clear existing traits
    
    traits.forEach(trait => {
        const li = document.createElement('li');
        li.textContent = trait;
        traitList.appendChild(li);
    });
}

function updateBookmark(type, status) {
    const bookmark = document.querySelector(`.${type}-bookmark`);
    const maxHeight = 400; // Maximum height of the bookmark

    let texture, scale;

    if (status > 5) {
        texture = `${type}10`;
        scale = status / 10; // Scale from 0.6 to 1 for status 6 to 10
    } else if (status > 3) {
        texture = `${type}5`;
        scale = (status - 3) / 2; // Scale from 0.5 to 1 for status 4 to 5
    } else if (status > 0) {
        texture = `${type}2`;
        if (status === 3) {
            scale = 1.3; // Full size for status 3
        } else if (status === 2) {
            scale = 1; // 85% size for status 2
        } else { // status === 1
            scale = 0.6; // 70% size for status 1
        }
    } else {
        texture = `${type}0`;
        scale = 1; // Full size for the smallest texture
    }

    // Update the background image
    bookmark.style.backgroundImage = `url('/graphics/default/background/${texture}.png')`;

    // Calculate and set the new height
    const newHeight = maxHeight * scale;
    bookmark.style.height = `${newHeight}px`;
}

function updateCharacterStats(character) {
    const stats = ['strength', 'agility', 'intelligence', 'authority', 'sociability'];
    stats.forEach(stat => {
        const statValue = character.stats[stat] || 0;
        const statItem = document.querySelector(`.stat-item[data-stat="${stat}"]`);
        
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