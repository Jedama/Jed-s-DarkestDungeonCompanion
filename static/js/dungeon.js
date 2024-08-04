import { getState, subscribeToState, setDungeonTeam } from './state.js';
import { renderCharacterDetails } from './character.js';
import { elementManager } from './elementManager.js';

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

    // Set up event listeners for the container
    dungeonCharactersContainer.addEventListener('mousemove', handleInteraction);
    dungeonCharactersContainer.addEventListener('click', handleInteraction);

    // Subscribe to state changes
    subscribeToState(updateDungeonView);
}

export function updateDungeonView() {
    const state = getState();
    const dungeonTeam = state.dungeonTeam || [];
    const dungeonCharacters = elementManager.get('dungeonView').querySelectorAll('.dungeon-character');

    const reversedTeam = [...dungeonTeam].reverse();

    dungeonCharacters.forEach((char, index) => {
        const characterTitle = reversedTeam[index];
        const character = state.characters[characterTitle];
        if (character) {
            char.src = `/graphics/default/dungeon/${character.title.toLowerCase()}0.png`;
            char.alt = character.name;
            char.setAttribute('data-title', character.title);
            
        } 
    });
}

function handleInteraction(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    let topChar = null;
    const characters = Array.from(e.currentTarget.querySelectorAll('.dungeon-character'));
    characters.forEach(char => {
        const charRect = char.getBoundingClientRect();
        const charX = x - (charRect.left - rect.left);
        const charY = y - (charRect.top - rect.top);

        if (charX >= 0 && charX < char.width && charY >= 0 && charY < char.height) {
            const index = (Math.floor(charY) * char.width + Math.floor(charX)) * 4;
            if (char.imageData && char.imageData.data[index + 3] > 0) {
                topChar = char;
            }
        }
    });

    if (topChar) {
        if (e.type === 'mousemove') {
            const index = Array.from(topChar.parentNode.children).indexOf(topChar);
            const baseScale = getBaseScale(index);
            const hoverScale = baseScale * 1.05;
            topChar.style.transform = topChar.style.transform.replace(/scale\([^)]*\)/, `scale(${hoverScale})`);
        } else if (e.type === 'click') {
            const characterTitle = topChar.getAttribute('data-title');
            if (characterTitle) {
                renderCharacterDetails(characterTitle);
            }
        }
    }

    // Reset scale for characters not being hovered
    characters.forEach((char, index) => {
        if (char !== topChar) {
            const baseTransform = getBaseTransform(index);
            char.style.transform = baseTransform;
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

    // Reset character positions and scales
    const characters = dungeonView.querySelectorAll('.dungeon-character');
    characters.forEach((char, index) => {
        const baseTransform = getBaseTransform(index);
        char.style.transform = baseTransform;
    });
}

function getBaseScale(index) {
    switch(index) {
        case 0:
        case 1:
            return 0.9;
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