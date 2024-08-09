import { getState, subscribeToState, setDungeonTeam } from './state.js';
import { renderCharacterDetails } from './character.js';
import { elementManager } from './elementManager.js';
import characterInfo from './characterInfo.js';

export function initializeDungeonView() {
    const dungeonView = elementManager.get('dungeonView');
    const dungeonCharactersContainer = dungeonView.querySelector('.dungeon-characters-container');
    const canvas = document.getElementById('dungeon-canvas');
    const ctx = canvas.getContext('2d');

    const characters = dungeonCharactersContainer.querySelectorAll('.dungeon-character');
    characters.forEach(char => {
        char.onload = function() {
            canvas.width = this.width;
            canvas.height = this.height;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(this, 0, 0, canvas.width, canvas.height);
            
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            char.imageData = imageData;
        }
    });

    dungeonCharactersContainer.addEventListener('mousemove', handleInteraction);
    dungeonCharactersContainer.addEventListener('click', handleInteraction);

    subscribeToState(updateDungeonView);
}

function handleInteraction(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    let topWrapper = null;
    const wrappers = Array.from(e.currentTarget.querySelectorAll('.character-wrapper'));
    wrappers.forEach(wrapper => {
        const charImg = wrapper.querySelector('.dungeon-character');
        const charRect = charImg.getBoundingClientRect();
        const charX = x - (charRect.left - rect.left);
        const charY = y - (charRect.top - rect.top);

        if (charX >= 0 && charX < charImg.width && charY >= 0 && charY < charImg.height) {
            const index = (Math.floor(charY) * charImg.width + Math.floor(charX)) * 4;
            if (charImg.imageData && charImg.imageData.data[index + 3] > 0) {
                topWrapper = wrapper;
            }
        }
    });

    if (topWrapper) {
        if (e.type === 'mousemove') {
            const index = Array.from(topWrapper.parentNode.children).indexOf(topWrapper);
            const baseScale = getBaseScale(index);
            const hoverScale = baseScale * 1.05;
            topWrapper.style.transform = topWrapper.style.transform.replace(/scale\([^)]*\)/, `scale(${hoverScale})`);
        } else if (e.type === 'click') {
            const characterTitle = topWrapper.getAttribute('data-title');
            if (characterTitle) {
                renderCharacterDetails(characterTitle);
            }
        }
    }

    wrappers.forEach((wrapper, index) => {
        if (wrapper !== topWrapper) {
            const baseTransform = getBaseTransform(index);
            wrapper.style.transform = baseTransform;
        }
    });
}

export function switchToDungeonView(region) {
    const galleryView = elementManager.get('galleryView');
    const dungeonView = elementManager.get('dungeonView');
    
    galleryView.style.display = 'none';
    dungeonView.style.display = 'block';

    document.body.style.backgroundImage = `url('/graphics/default/assets/background/${encodeURIComponent(region)}.png')`;

    updateDungeonView();

    const wrappers = dungeonView.querySelectorAll('.character-wrapper');
    wrappers.forEach((wrapper, index) => {
        const baseTransform = getBaseTransform(index);
        wrapper.style.transform = baseTransform;
    });
}

export function updateDungeonView() {
    const state = getState();
    const dungeonTeam = state.dungeonTeam || [];
    const characterWrappers = elementManager.get('dungeonView').querySelectorAll('.character-wrapper');

    const reversedTeam = [...dungeonTeam].reverse();

    characterWrappers.forEach((wrapper, index) => {
        const characterTitle = reversedTeam[index];
        const character = state.characters[characterTitle];
        const charImg = wrapper.querySelector('.dungeon-character');
        if (character) {
            charImg.src = `/graphics/default/characters/dungeon/${character.title.toLowerCase()}0.png`;
            charImg.alt = character.name;
            wrapper.setAttribute('data-title', character.title);
            updateStressMeter(index, 6);
        } 
    });
}

export function updateStressMeter(characterIndex, level) {
    if (level < 0 || level > 6) {
        console.error('Stress level must be between 0 and 6');
        return;
    }

    const dungeonView = elementManager.get('dungeonView');
    const characterWrappers = dungeonView.querySelectorAll('.character-wrapper');
    
    if (characterIndex < 0 || characterIndex >= characterWrappers.length) {
        console.error('Invalid character index');
        return;
    }

    const wrapper = characterWrappers[characterIndex];
    const stressMeter = wrapper.querySelector('.stress-meter');
    const characterTitle = wrapper.getAttribute('data-title');
    const characterData = characterInfo[characterTitle];
    
    if (level === 0) {
        stressMeter.style.display = 'none';
    } else {
        stressMeter.style.display = 'block';
        stressMeter.src = `/graphics/default/assets/stat/stresscrown${level}.png`;

        if (characterData && characterData.headPosition) {
            const { x, y } = characterData.headPosition;
            const xPercentage = (x / 832) * 100;
            const yPercentage = (y / 1024) * 100;

            stressMeter.style.left = `${xPercentage}%`;
            stressMeter.style.top = `${yPercentage}%`;
            stressMeter.style.transform = 'translate(-50%, -50%)';
        }
    }
}

function getBaseScale(index) {
    switch(index) {
        case 0:
            return 0.9;
        case 1:
            return 0.925;
        case 2:
            return 0.95;
        case 3:
            return 1;
        default:
            return 1;
    }
}

function getBaseTransform(index) {
    const baseScale = getBaseScale(index);
    switch(index) {
        case 0: return `translateX(-20%) scale(${baseScale})`;
        case 1: return `translateX(20%) scale(${baseScale})`;
        case 2: return `translateX(-50%) scale(${baseScale})`;
        case 3: return `translateX(50%) scale(${baseScale})`;
        default: return '';
    }
}