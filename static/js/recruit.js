import { fetchCharacterInfo } from './apiClient.js';
import { state, addCharacter, getAllCharacters, getCharacterTitles } from './state.js';

export function initializeRecruit() {
    const elements = {
        recruitModal: document.getElementById("recruit-modal"),
        recruitDropdown: document.getElementById("recruit-dropdown"),
        recruitIcon: document.getElementById("recruit-icon"),
        recruitNameInput: document.getElementById("recruit-name"),
        recruitModifierInput: document.getElementById("recruit-modifier"),
        recruitModifierContainer: document.getElementById("recruit-modifier-container"),
        recruitHireButton: document.getElementById("recruit-hire"),
    };

    let characterInfo = {};
    let modifiers = [];

    const positions = [
        {x: '10%', y: '10%'},    // Top-left
        {x: '90%', y: '10%'},  // Top-right
        {x: '10%', y: '90%'},  // Bottom-left
        {x: '90%', y: '90%'},// Bottom-right
        {x: '50%', y: '10%'},   // Top-center
        {x: '10%', y: '50%'},   // Middle-left
        {x: '90%', y: '50%'}, // Middle-right
        {x: '50%', y: '90%'}, // Bottom-center
        {x: '50%', y: '50%'}   // Center
    ];

    elements.recruitDropdown.addEventListener('change', updateDetails);
    elements.recruitHireButton.addEventListener('click', handleSubmission);
    elements.recruitModifierInput.addEventListener('keypress', handleModifierKeyPress);

    function updateDetails() {
        const selectedCharacter = elements.recruitDropdown.value;
        elements.recruitIcon.innerHTML = selectedCharacter
            ? `<img src="/icons/${selectedCharacter.toLowerCase()}0.png" alt="${selectedCharacter}">`
            : '';
        const info = characterInfo[selectedCharacter];
        elements.recruitNameInput.value = info ? info.default_name : '';

        // Clear modifiers and reset seal
        modifiers = [];
        clearModifiers();
        resetSeal();
    }

    function clearModifiers() {
        const modalContent = elements.recruitModal.querySelector('.modal-content');
        modalContent.querySelectorAll('#recruit-modifier-overlay').forEach(el => el.remove());
    }
    
    function resetSeal() {
        elements.recruitHireButton.classList.remove('active');
        elements.recruitHireButton.classList.add('inactive');
    }

    async function populateDropdown() {
        try {
            characterInfo = await fetchCharacterInfo();
            const currentCharacters = getCharacterTitles();

            const availableCharacters = Object.keys(characterInfo).filter(char => 
                !currentCharacters.includes(char)
            );
    
            elements.recruitDropdown.innerHTML = availableCharacters.map(char => 
                `<option value="${char}">${char}</option>`
            ).join('');
            
            updateDetails();
    
        } catch (error) {
            console.error('Error fetching character info:', error);
        }
    }

    function handleModifierKeyPress(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            addModifier();
        }
    }

    function addModifier() {
        const modifier = elements.recruitModifierInput.value.trim();
        if (modifier) {
            modifiers.push(modifier);
            elements.recruitModifierInput.value = '';
            updateModifierOverlay();
            elements.recruitHireButton.classList.remove('inactive');
            elements.recruitHireButton.classList.add('active');
        }
    }

    function updateModifierOverlay() {
        const modalContent = elements.recruitModal.querySelector('.modal-content');
        const iconRect = elements.recruitIcon.getBoundingClientRect();
        const modalRect = modalContent.getBoundingClientRect();
    
        const overlay = document.createElement('div');
        overlay.id = 'recruit-modifier-overlay';
        overlay.textContent = modifiers[modifiers.length - 1];
    
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

    function handleSubmission(event) {
        if (!modifiers.length) {
            event.preventDefault();
            return; // Do nothing if the seal is inactive
        }
    
        const characterTitle = elements.recruitDropdown.value;
        const characterName = elements.recruitNameInput.value;
        
        if (characterTitle) {  
            
            alert(`Character ${characterName} (${characterTitle}) recruited with modifiers: ${modifiers.join(', ')}`);
            
            elements.recruitModal.style.display = "none";
        } else {
            alert('Please select a character.');
        }
    }

    return { populateDropdown };
}