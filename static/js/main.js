import { loadEstateData, createNewEstate, createEvent } from './apiClient.js';
import { state, setEstateName, addCharacter } from './state.js';
import { renderCharacterList, renderCharacterDetails } from './character.js';
import { initializeRecruit } from './recruit.js';

document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");

    // DOM Elements
    const elements = {
        savefileModal: document.getElementById("savefile-modal"),
        savefileSubmit: document.getElementById("savefile-submit"),
        savefileNameInput: document.getElementById("savefile-name"),
        eventButton: document.getElementById("event-button"),
        recruitButton: document.getElementById("recruit-button"),
        characterGrid: document.getElementById("character-grid")
    };

    // Initialize
    showSavefileModal();
    initializeEventListeners();
    const { populateDropdown } = initializeRecruit();

    // Function to show savefile modal
    function showSavefileModal() {
        elements.savefileModal.style.display = "block";
    }

    // Event Listeners
    function initializeEventListeners() {
        elements.savefileSubmit.addEventListener("click", handleSavefileSubmission);
        elements.savefileNameInput.addEventListener("keyup", handleSavefileKeyUp);
        elements.recruitButton.addEventListener("click", () => {
            document.getElementById("recruit-modal").style.display = "block";
            populateDropdown();  // Call populateDropdown when the modal is opened
        });
        elements.eventButton.addEventListener("click", handleEventButtonClick);
    }

    function handleSavefileSubmission() {
        const estateName = elements.savefileNameInput.value.trim();
        if (estateName) {
            console.log("Savefile name entered:", estateName);
            setEstateName(estateName);
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

    async function loadGame(savefileName) {
        console.log("Loading game with savefile:", savefileName);
        try {
            let estateData = await loadEstateData(savefileName);
            
            if (estateData) {
                handleEstateData(estateData);
            } else {
                console.log("No existing estate data found. Creating new estate...");
                estateData = await createNewEstate(savefileName);
                handleEstateData(estateData);
            }
        } catch (error) {
            console.error('Error loading estate:', error);
        }
      }

    function handleEstateData(estateData) {
        if (estateData.characters && typeof estateData.characters === 'object') {
            Object.values(estateData.characters).forEach(character => addCharacter(character));
            renderCharacterList(elements);
            const firstCharacterName = Object.keys(estateData.characters)[0];
            if (firstCharacterName) {
                renderCharacterDetails(firstCharacterName);
            }
        } else {
            console.error("Estate characters not found or not an object");
        }
    }

    // Function to process the event result
function processEventResult(result) {
    updateStoryPanel(result.title, result.storyText);
    updateCards(result.consequences);
    showModal();
}

// Function to update the story panel
function updateStoryPanel(title, storyText) {
    const storyPanel = document.querySelector('.story-panel');
    storyPanel.innerHTML = `
        <h2 class="story-title">${title || 'New Event'}</h2>
        <p class="story-text">${storyText || 'No story available.'}</p>
    `;
}

function updateCards(consequences) {
    const cardContainer = document.querySelector('.story-cards');
    cardContainer.innerHTML = ''; // Clear existing cards

    const characters = Object.keys(consequences);

    characters.forEach((character, index) => {
        if (index < 4) { // Limit to 4 cards
            const consequenceList = consequences[character];
            const card = document.createElement('div');
            card.className = 'story-card';
            card.innerHTML = `
                <div class="card-frame"></div>
                <div class="card-content">
                    <div class="card-image" style="background-image: url('/graphics/default/cards/${character.toLowerCase()}0.png')"></div>
                    <h3>${character}</h3>
                    <ul class="consequence-text">
                        ${consequenceList.map(consequence => `<li>${consequence}</li>`).join('')}
                    </ul>
                </div>
            `;
            cardContainer.appendChild(card);
        }
    });
}

// Function to show the modal
function showModal() {
    const modal = document.getElementById('story-modal');
    modal.style.display = 'block';
    document.body.classList.add('modal-open');
}

// Function to hide the modal
function hideModal() {
    const modal = document.getElementById('story-modal');
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');
}

// Updated handleEventButtonClick function
async function handleEventButtonClick() {
    try {
        const result = await createEvent('random', 'random', [], []);
        console.log('Event created:', result);
        processEventResult(result);
    } catch (error) {
        console.error('Error creating event:', error);
        // Handle the error (e.g., show an error message to the user)
    }
}
});