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
        characterDropdown: document.getElementById("character-dropdown"),
        iconDiv: document.getElementById("character-icon"),
        characterNameInput: document.getElementById("character-name"),
        modifierInput: document.getElementById("modifier"),
        beginRecruitButton: document.getElementById("begin-recruit"),
        characterGrid: document.getElementById("character-grid")
    };

    // Global variables
    let estateName;
    let characterInfo = {};
    let currentCharacters = new Set();

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
        elements.eventsButton.addEventListener("click", openRecruitModal);
        elements.characterDropdown.addEventListener('change', updateIcon);
        elements.beginRecruitButton.addEventListener('click', handleRecruitSubmission);
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
        } else {
            console.error("Estate characters not found or not an object");
            currentCharacters = new Set();
        }
    }

    // Recruit Modal
    function openRecruitModal() {
        populateCharacterDropdown();
        elements.recruitModal.style.display = "block";
    }

    elements.characterDropdown.addEventListener('change', updateCharacterDetails)

    function updateCharacterDetails() {
        const selectedCharacter = elements.characterDropdown.value;
        updateIcon(selectedCharacter);
        updateDefaultName(selectedCharacter);
    }

    function updateDefaultName(characterTitle) {
        const info = characterInfo[characterTitle];
        elements.characterNameInput.value = info ? info.default_name : '';
    }

    async function populateCharacterDropdown() {
        try {
            characterInfo = await fetchCharacterInfo();
            const availableCharacters = Object.keys(characterInfo).filter(char => !currentCharacters.has(char));
            
            elements.characterDropdown.innerHTML = availableCharacters.map(char => 
                `<option value="${char}">${char}</option>`
            ).join('');
            
            if (availableCharacters.length > 0) {
                updateCharacterDetails();
            } else {
                elements.characterDropdown.innerHTML = '<option value="">No characters available</option>';
                updateIcon();
                elements.characterNameInput.value = '';
            }
        } catch (error) {
            console.error('Error fetching character info:', error);
        }
    }

    function updateIcon() {
        const selectedCharacter = elements.characterDropdown.value;
        elements.iconDiv.innerHTML = selectedCharacter
            ? `<img src="/icons/${selectedCharacter.toLowerCase()}0.png" alt="${selectedCharacter}">`
            : '';
    }

    function handleRecruitSubmission() {
        const characterTitle = elements.characterDropdown.value;
        const characterName = elements.characterNameInput.value;
        const modifier = elements.modifierInput.value;
        
        if (characterTitle) {
            console.log('Selected character:', characterTitle);
            console.log('Character name:', characterName);
            console.log('Modifier:', modifier);
            
            // Here you would typically send this data to your backend
            // For now, we'll just show an alert
            alert(`Character ${characterName} (${characterTitle}) recruited with modifier: ${modifier}`);
            
            elements.recruitModal.style.display = "none";
            
            // Repopulate the dropdown to reflect the new state
            populateCharacterDropdown();
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
        const relationshipInfo = document.querySelector('.relationship-info');
    
        characterInfo.innerHTML = `
            <img id="character-portrait" class="character-portrait" src="/portraits/${character.title.toLowerCase()}0.png" alt="${character.name}">
            <h2 id="character-name">${character.name}</h2>
            <p>Title: ${character.title}</p>
            <p>Level: <span id="character-level">${character.level}</span></p>
            <p>Money: <span id="character-money">${character.money}</span></p>
            <p id="character-summary">${character.summary}</p>
        `;
    
        if (character.relationships && Object.keys(character.relationships).length > 0) {
            const firstRelationship = Object.entries(character.relationships)[0];
            relationshipInfo.innerHTML = `
                <h3>Relationship</h3>
                <div id="relationship-detail">
                    <h4 id="relationship-name">${firstRelationship[0]}</h4>
                    <p>Affinity: <span id="relationship-affinity">${firstRelationship[1].affinity}</span></p>
                    <p>Bond: <span id="relationship-bond">${firstRelationship[1].dynamic}</span></p>
                </div>
                <button id="detailed-info">Detailed Information</button>
            `;
        } else {
            relationshipInfo.innerHTML = '<p>No relationships available.</p>';
        }
    }

    function fetchCharacterDetails(estateName, title) {
        return fetch(`/api/character/${estateName}/${title}`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
                return response.json();
            });
    }
});