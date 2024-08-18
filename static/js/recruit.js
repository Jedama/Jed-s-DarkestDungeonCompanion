import { fetchDefaultCharacterInfo } from './apiClient.js';
import { getState, addModifier, clearModifiers, getModifiers } from './state.js';
import { createEvent } from './events.js';
import { elementManager } from './elementManager.js';

let cachedCharacterInfo = null;

export function initializeRecruit() {

    elementManager.get('recruitDropdown').addEventListener('change', updateDetails);
    elementManager.get('recruitHireButton').addEventListener('click', handleSubmission);
    elementManager.get('recruitModifierInput').addEventListener('keypress', handleModifierKeyPress);

    function handleModifierKeyPress(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            applyModifier();
        }
    }
}

export async function populateDropdown() {
    try {
        cachedCharacterInfo = await fetchDefaultCharacterInfo();
        const currentCharacters = Object.keys(getState().characters);

        const availableCharacters = Object.keys(cachedCharacterInfo).filter(char =>
            !currentCharacters.includes(char)
        );

        elementManager.get('recruitDropdown').innerHTML = availableCharacters.map(char =>
            `<option value="${char}">${char}</option>`
        ).join('');

        updateDetails();

        elementManager.get('recruitDropdown').focus();

    } catch (error) {
        console.error('Error fetching character info:', error);
    }
}

async function updateDetails() {

    const selectedCharacter = elementManager.get('recruitDropdown').value;
    elementManager.get('recruitIcon').innerHTML = selectedCharacter
        ? `<img src="/graphics/default/characters/recruit/${selectedCharacter.toLowerCase()}0.png" alt="${selectedCharacter}">`
        : '';
    const info = cachedCharacterInfo[selectedCharacter];

    elementManager.get('recruitNameInput').value = info ? info.default_name : '';

    // Clear modifiers and reset seal
    clearModifiers();
    clearModifierText();
    resetSeal();
}

function clearModifierText() {
    const modalContent = elementManager.get('recruitModal').querySelector('.modal-content');
    modalContent.querySelectorAll('#recruit-modifier-overlay').forEach(el => el.remove());
}

function resetSeal() {
    const recruitHireButton = elementManager.get('recruitHireButton');
    recruitHireButton.classList.remove('active');
    recruitHireButton.classList.add('inactive');
}

function applyModifier() {
    const modifier = elementManager.get('recruitModifierInput').value.trim();
    if (modifier) {
        addModifier(modifier);
        elementManager.get('recruitModifierInput').value = '';
        updateModifierOverlay();
        const recruitHireButton = elementManager.get('recruitHireButton');
        recruitHireButton.classList.remove('inactive');
        recruitHireButton.classList.add('active');
    }
}

function updateModifierOverlay() {
    const modalContent = elementManager.get('recruitModal').querySelector('.modal-content');
    const iconRect = elementManager.get('recruitIcon').getBoundingClientRect();
    const modalRect = modalContent.getBoundingClientRect();

    const overlay = document.createElement('div');
    overlay.id = 'recruit-modifier-overlay';

    const modifiers = getModifiers();
    overlay.textContent = modifiers[modifiers.length - 1];

    const positions = [
        { x: '10%', y: '10%' },   // Top-left
        { x: '90%', y: '10%' },   // Top-right
        { x: '10%', y: '90%' },   // Bottom-left
        { x: '90%', y: '90%' },   // Bottom-right
        { x: '50%', y: '10%' },   // Top-center
        { x: '10%', y: '50%' },   // Middle-left
        { x: '90%', y: '50%' },   // Middle-right
        { x: '50%', y: '90%' },   // Bottom-center
        { x: '50%', y: '50%' }    // Center
    ];

    const position = positions[(modifiers.length - 1) % positions.length];

    // Calculate position relative to the modal content
    const left = iconRect.left - modalRect.left + (iconRect.width * parseFloat(position.x) / 100);
    const top = iconRect.top - modalRect.top + (iconRect.height * parseFloat(position.y) / 100);

    overlay.style.left = `${left}px`;
    overlay.style.top = `${top}px`;

    // Center the text on the calculated position
    overlay.style.transform = 'translate(-50%, -50%)';

    // Add random tilt
    const tilt = Math.random() * 40 - 20; // Random angle between -20 and 20 degrees
    overlay.style.transform += ` rotate(${tilt}deg)`;

    // Ensure the overlay is positioned absolutely within the modal content
    overlay.style.position = 'absolute';

    // Append the overlay to the modal content
    modalContent.appendChild(overlay);
}

async function handleSubmission(event) {

    const modifiers = getModifiers();

    if (!modifiers.length) {
        event.preventDefault();
        return; // Do nothing if the seal is inactive
    }

    const characterTitle = elementManager.get('recruitDropdown').value;
    const characterName = elementManager.get('recruitNameInput').value;

    if (characterTitle) {
        elementManager.get('recruitModal').style.display = "none";
        createEvent('recruit', '', [characterTitle], modifiers, characterName);
    } else {
        alert('Please select a character.');
    }
}