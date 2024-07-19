import { EventFormGenerator } from './eventFormGenerator.js';
import { fetchOptions, submitEvent, fetchCharacterTitles } from './apiClient.js';

document.addEventListener("DOMContentLoaded", async function() {
    console.log("DOM fully loaded and parsed");

    const savefileModal = document.getElementById("savefile-modal");
    const savefileSubmit = document.getElementById("savefile-submit");
    const savefileNameInput = document.getElementById("savefile-name");
    const eventsButton = document.getElementById("events-button");
    const eventTypeCancel = document.getElementById("event-type-cancel");
    const saveButton = document.getElementById("save-button");

    const eventConfig = await fetch('/event_types.json').then(response => response.json());
    const formGenerator = new EventFormGenerator(eventConfig);

    console.log("HTML elements retrieved");

    let estateName; // Store the estate name globally
    let modifiers = []; // To store the modifiers

    savefileModal.style.display = "block";

    saveButton.addEventListener("click", function() {
        saveEstate();
    });

    function saveEstate() {
        fetch(`/api/estate/${estateName}/save`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("Estate saved successfully!");
            } else {
                alert("Failed to save estate.");
            }
        })
        .catch(error => {
            console.error('Error saving estate:', error);
            alert("An error occurred while saving.");
        });
    }

    // Function to handle savefile submission
    function handleSavefileSubmission() {
        estateName = savefileNameInput.value.trim();
        if (estateName) {
            console.log("Savefile name entered:", estateName);
            savefileModal.style.display = "none";
            loadGame(estateName);
        } else {
            alert("Please enter a savefile name.");
        }
    }

    // Handle savefile submission via button click
    savefileSubmit.addEventListener("click", handleSavefileSubmission);

    // Handle savefile submission via Enter key
    savefileNameInput.addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent the default action
            handleSavefileSubmission();
        }
    });

    // Update your existing event listeners to use these functions
    eventsButton.addEventListener("click", function() {
        openEventCreationModal();
    });

    function openEventCreationModal() {
        const formContainer = document.querySelector('#event-type-modal #form-container');
        formContainer.innerHTML = ''; // Clear existing content
    
        const dynamicFormFields = document.createElement('div');
        dynamicFormFields.id = 'dynamic-form-fields';
    
        const submitButton = document.createElement('button');
        submitButton.textContent = 'Create Event';
        submitButton.addEventListener('click', handleEventSubmission);
    
        formContainer.appendChild(dynamicFormFields);
        formContainer.appendChild(submitButton);
    
        dynamicFormFields.innerHTML = formGenerator.generateForm('Town', 'Recruit');
    
        fetchCharacterTitles().then(titles => {
            formGenerator.populateCharacterSelect('character-title', titles);
        }).catch(error => {
            console.error('Error fetching character titles:', error);
        });
    
        modifiers = formGenerator.setupModifierInput('character-modifiers');
    
        openModal('event-type-modal');
    }

    function handleEventSubmission() {
        const characterTitle = document.getElementById('character-title-input').value;
        if (characterTitle) {
            console.log('Selected character:', characterTitle);
            console.log('Modifiers:', modifiers);
            // Here you would typically send this data to your backend
            alert(`Character ${characterTitle} selected for recruitment!`);
            closeModal('event-type-modal');
        } else {
            alert('Please select a character.');
        }
    }

    function handleEstateData(estateData) {
        if (estateData.characters && typeof estateData.characters === 'object') {
            renderCharacterList(estateData.characters);
        } else {
            console.error("Estate characters not found or not an object");
        }
    }

    function loadGame(savefileName) {
        console.log("Loading game with savefile:", savefileName);
    
        fetch(`/estates/${savefileName}/estate.json`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else if (response.status === 404) {
                    return null;
                } else {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
            })
            .then(data => {
                if (data) {
                    handleEstateData(data);
                } else {
                    console.log("No existing estate data found. Creating new estate...");
                    fetch(`/api/create_estate/${savefileName}`, { method: 'POST' })
                        .then(response => response.json())
                        .then(newEstateData => handleEstateData(newEstateData));
                }
            })
            .catch(error => {
                console.error('Error loading estate:', error);
            });
    }

    function fetchCharacterDetails(estateName, title) {
        return fetch(`/api/character/${estateName}/${title}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            });
    }

    function renderCharacterList(characters) {
        const characterGrid = document.getElementById('character-grid');
        characterGrid.innerHTML = '';
        
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
            characterGrid.appendChild(characterElement);
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
    
        // Update character info
        characterInfo.innerHTML = `
            <img id="character-portrait" class="character-portrait" src="/portraits/${character.title.toLowerCase()}0.png" alt="${character.name}">
            <h2 id="character-name">${character.name}</h2>
            <p>Title: ${character.title}</p>
            <p>Level: <span id="character-level">${character.level}</span></p>
            <p>Money: <span id="character-money">${character.money}</span></p>
            <p id="character-summary">${character.summary}</p>
        `;
    
        // Update relationship info (if available)
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

    function openModal(modalId) {
        document.getElementById(modalId).style.display = "block";
        document.body.classList.add('modal-open');
    }
    
    function closeModal(modalId) {
        document.getElementById(modalId).style.display = "none";
        document.body.classList.remove('modal-open');
    }
});