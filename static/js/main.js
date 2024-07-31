import { loadEstateData, createNewEstate, createEvent } from './apiClient.js';
import { addCharacter, setEstateName, getState } from './state.js';
import { renderCharacterList, renderCharacterDetails } from './character.js';
import { initializeRecruit } from './recruit.js';
import { initializeEventHandler, processEventResult } from './events.js';
import { showLoading, hideLoading } from './loading.js';

document.addEventListener("DOMContentLoaded", initializeApp);

function initializeApp() {
    console.log("DOM fully loaded and parsed");

    const elements = getDOMElements();
    const { storyModal } = initializeEventHandler(elements);
    const { populateDropdown } = initializeRecruit(elements, storyModal);

    showSavefileModal(elements.savefileModal);
    initializeEventListeners(elements, populateDropdown);
}

function getDOMElements() {
    return {
        savefileModal: document.getElementById("savefile-modal"),
        savefileSubmit: document.getElementById("savefile-submit"),
        savefileNameInput: document.getElementById("savefile-name"),
        eventButton: document.getElementById("event-button"),
        recruitButton: document.getElementById("recruit-button"),
        characterGrid: document.getElementById("character-grid"),
        storyModal: document.getElementById("story-modal"),
        returnButton: document.getElementById("return-btn"),
        renderCharacterList
    };
}

function showSavefileModal(modal) {
    modal.style.display = "block";
}

function initializeEventListeners(elements, populateDropdown) {
    elements.savefileSubmit.addEventListener("click", () => handleSavefileSubmission(elements));
    elements.savefileNameInput.addEventListener("keyup", (event) => handleSavefileKeyUp(event, elements));
    elements.recruitButton.addEventListener("click", () => {
        document.getElementById("recruit-modal").style.display = "block";
        populateDropdown();
    });
    elements.eventButton.addEventListener("click", () => handleEventButtonClick(elements));
}

function handleSavefileSubmission(elements) {
    const estateName = elements.savefileNameInput.value.trim();
    if (estateName) {
        console.log("Savefile name entered:", estateName);
        setEstateName(estateName);
        console.log("Estate name after setting:", getState().estateName);
        elements.savefileModal.style.display = "none";
        loadGame(estateName, elements);
    } else {
        alert("Please enter a savefile name.");
    }
}

function handleSavefileKeyUp(event, elements) {
    if (event.key === "Enter") {
        event.preventDefault();
        handleSavefileSubmission(elements);
    }
}

async function loadGame(savefileName, elements) {
    console.log("Loading game with savefile:", savefileName);
    try {
        let estateData = await loadEstateData(savefileName);
        
        if (!estateData) {
            console.log("No existing estate data found. Creating new estate...");
            estateData = await createNewEstate(savefileName);
        }
        
        handleEstateData(estateData, elements);
    } catch (error) {
        console.error('Error loading estate:', error);
    }
}

function handleEstateData(estateData, elements) {
    if (estateData.characters && typeof estateData.characters === 'object') {
        Object.values(estateData.characters).forEach(addCharacter);
        elements.renderCharacterList(elements);
        const firstCharacterName = Object.keys(estateData.characters)[0];
        if (firstCharacterName) {
            renderCharacterDetails(firstCharacterName);
        }
    } else {
        console.error("Estate characters not found or not an object");
    }
}

async function handleEventButtonClick(elements) {
    try {
      showLoading();
      const result = await createEvent('random', '', [], [], '');
      console.log('Event created:', result);
      hideLoading();
      processEventResult(result, elements.storyModal, elements);
    } catch (error) {
      console.error('Error creating event:', error);
      // Handle the error (e.g., show an error message to the user)
    }
}