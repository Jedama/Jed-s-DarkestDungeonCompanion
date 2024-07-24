import { fetchCharacterInfo } from './apiClient.js';

document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");

    // DOM Elements
    const elements = {
        savefileModal: document.getElementById("savefile-modal"),
        savefileSubmit: document.getElementById("savefile-submit"),
        savefileNameInput: document.getElementById("savefile-name"),
        eventsButton: document.getElementById("events-button"),
        saveButton: document.getElementById("save-button"),
        recruitModal: document.getElementById("recruit-modal"),
        recruitDropdown: document.getElementById("recruit-dropdown"),
        recruitIcon: document.getElementById("recruit-icon"),
        recruitNameInput: document.getElementById("recruit-name"),
        recruitModifierInput: document.getElementById("recruit-modifier"),
        recruitModifierContainer: document.getElementById("recruit-modifier-container"),
        recruitHireButton: document.getElementById("recruit-hire"),
        characterGrid: document.getElementById("character-grid")
    };

    // Global variables
    let estateName;
    let characterInfo = {};
    let currentCharacters = new Set();
    let modifiers = [];

    //Positions for modifier text for recruit
    const positions = [
        {x: '0%', y: '0%'},    // Top-left
        {x: '100%', y: '0%'},  // Top-right
        {x: '0%', y: '100%'},  // Bottom-left
        {x: '100%', y: '100%'},// Bottom-right
        {x: '50%', y: '0%'},   // Top-center
        {x: '0%', y: '50%'},   // Middle-left
        {x: '100%', y: '50%'}, // Middle-right
        {x: '50%', y: '100%'}, // Bottom-center
        {x: '50%', y: '50%'}   // Center
    ];

    // Initialize
    showSavefileModal();
    initializeEventListeners();

    // Function to show savefile modal
    function showSavefileModal() {
        elements.savefileModal.style.display = "block";
        // Ensure recruit modal is hidden
        elements.recruitModal.style.display = "none";
    }

    // Event Listeners
    function initializeEventListeners() {
        elements.saveButton.addEventListener("click", saveEstate);
        elements.savefileSubmit.addEventListener("click", handleSavefileSubmission);
        elements.savefileNameInput.addEventListener("keyup", handleSavefileKeyUp);
        elements.eventsButton.addEventListener("click", recruitOpenModal);
        elements.recruitDropdown.addEventListener('change', recruitUpdateDetails);
        elements.recruitHireButton.addEventListener('click', recruitHandleSubmission);
        elements.recruitModifierInput.addEventListener('keypress', recruitHandleModifierKeyPress);
    }

    // Savefile and Estate Management
    function saveEstate() {
        fetch(`/api/estate/${estateName}/save`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                alert(data.status === "success" ? "Estate saved successfully!" : "Failed to save estate.");
            })
            .catch(error => {
                console.error('Error saving estate:', error);
                alert("An error occurred while saving.");
            });
    }

    function handleSavefileSubmission() {
        estateName = elements.savefileNameInput.value.trim();
        if (estateName) {
            console.log("Savefile name entered:", estateName);
            elements.savefileModal.style.display = "none";
            loadGame(estateName);
        } else {
            alert("Please enter a savefile name.");
        }
    }

    function handleSavefileKeyUp(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            handleSavefileSubmission();
        }
    }

    function loadGame(savefileName) {
        console.log("Loading game with savefile:", savefileName);
        fetch(`/estates/${savefileName}/estate.json`)
            .then(response => {
                if (response.ok) return response.json();
                if (response.status === 404) return null;
                throw new Error(`HTTP error! Status: ${response.status}`);
            })
            .then(data => {
                if (data) {
                    handleEstateData(data);
                } else {
                    console.log("No existing estate data found. Creating new estate...");
                    return fetch(`/api/create_estate/${savefileName}`, { method: 'POST' })
                        .then(response => response.json());
                }
            })
            .then(newEstateData => newEstateData && handleEstateData(newEstateData))
            .catch(error => console.error('Error loading estate:', error));
    }

    function handleEstateData(estateData) {
        if (estateData.characters && typeof estateData.characters === 'object') {
            currentCharacters = new Set(Object.keys(estateData.characters));
            renderCharacterList(estateData.characters);
            loadAndRenderCharacterDetails(Object.keys(estateData.characters)[0])
        } else {
            console.error("Estate characters not found or not an object");
            currentCharacters = new Set();
        }
    }

    // Recruit Modal
    function recruitOpenModal() {
        recruitPopulateDropdown();
        elements.recruitModal.style.display = "block";
        modifiers = []; // Reset modifiers
        recruitClearModifiers();
        recruitResetSeal();
    }

    elements.recruitDropdown.addEventListener('change', recruitUpdateDetails)

    function recruitUpdateDetails() {
        const selectedCharacter = elements.recruitDropdown.value;
        elements.recruitIcon.innerHTML = selectedCharacter
            ? `<img src="/icons/${selectedCharacter.toLowerCase()}0.png" alt="${selectedCharacter}">`
            : '';
        const info = characterInfo[selectedCharacter];
        elements.recruitNameInput.value = info ? info.default_name : '';

        // Clear modifiers and reset seal
        modifiers = [];
        recruitClearModifiers();
        recruitResetSeal();
    }

    function recruitClearModifiers() {
        const modalContent = elements.recruitModal.querySelector('.modal-content');
        modalContent.querySelectorAll('#recruit-modifier-overlay').forEach(el => el.remove());
    }
    
    function recruitResetSeal() {
        elements.recruitHireButton.classList.remove('active');
        elements.recruitHireButton.classList.add('inactive');
    }

    async function recruitPopulateDropdown() {
        try {
            characterInfo = await fetchCharacterInfo();
            const availableCharacters = Object.keys(characterInfo).filter(char => !currentCharacters.has(char));
            
            elements.recruitDropdown.innerHTML = availableCharacters.map(char => 
                `<option value="${char}">${char}</option>`
            ).join('');
            
            recruitUpdateDetails();

        } catch (error) {
            console.error('Error fetching character info:', error);
        }
    }

    function recruitHandleModifierKeyPress(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            recruitAddModifier();
        }
    }

    function recruitAddModifier() {
        const modifier = elements.recruitModifierInput.value.trim();
        if (modifier) {
            modifiers.push(modifier);
            elements.recruitModifierInput.value = '';
            recruitUpdateModifierOverlay();
            elements.recruitHireButton.classList.remove('inactive');
            elements.recruitHireButton.classList.add('active');
        }
    }

    function recruitUpdateModifierOverlay() {
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


    function recruitHandleSubmission(event) {
        if (!modifiers.length) {
            event.preventDefault();
            return; // Do nothing if the seal is inactive
        }
    
        const characterTitle = elements.recruitDropdown.value;
        const characterName = elements.recruitNameInput.value;
        
        if (characterTitle) {
            console.log('Selected character:', characterTitle);
            console.log('Character name:', characterName);
            console.log('Modifiers:', modifiers);
            
            alert(`Character ${characterName} (${characterTitle}) recruited with modifiers: ${modifiers.join(', ')}`);
            
            elements.recruitModal.style.display = "none";
            recruitPopulateDropdown();
        } else {
            alert('Please select a character.');
        }
    }

    // Character Management
    function renderCharacterList(characters) {
        elements.characterGrid.innerHTML = '';
        Object.entries(characters).forEach(([title, character]) => {
            const characterElement = document.createElement('div');
            characterElement.classList.add('character-item');
            const portraitImg = document.createElement('img');
            portraitImg.src = `/portraits/${title.toLowerCase()}0.png`;
            portraitImg.alt = title;
            portraitImg.classList.add('portrait');
            const frameImg = document.createElement('img');
            const frameLevel = Math.min(character.level, 6);
            frameImg.src = `/background/level${frameLevel}.png`;
            frameImg.alt = 'frame';
            frameImg.classList.add('frame');
            characterElement.appendChild(portraitImg);
            characterElement.appendChild(frameImg);
            characterElement.addEventListener('click', () => loadAndRenderCharacterDetails(title));
            elements.characterGrid.appendChild(characterElement);
        });
    }

    function loadAndRenderCharacterDetails(title) {
        fetchCharacterDetails(estateName, title)
            .then(renderCharacterDetails)
            .catch(error => {
                console.error(`Error fetching details for character ${title}:`, error);
                document.querySelector('.character-info').innerHTML = `<p>Error loading character details</p>`;
            });
    }

    function renderCharacterDetails(character) {
        const characterInfo = document.querySelector('.character-info');
    
        // Update character portrait
        const characterPortrait = characterInfo.querySelector('#character-portrait');
        characterPortrait.src = `/portraits/${character.title.toLowerCase()}0.png`;
        characterPortrait.alt = character.name;
    
        // Update character name
        const characterName = characterInfo.querySelector('#character-name');
        characterName.textContent = character.name;

        // Update character title
        const characterTitle = characterInfo.querySelector('#character-title');
        characterTitle.textContent = `the ${character.title}`;

        updateCharacterStats(character);
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

    function fetchCharacterDetails(estateName, title) {
        return fetch(`/api/character/${estateName}/${title}`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
                return response.json();
            });
    }
});