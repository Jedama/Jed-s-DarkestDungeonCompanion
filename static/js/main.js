import { loadEstateData, saveEstate } from './apiClient.js';
import { addCharacter, setEstateName, getState } from './state.js';
import { renderCharacterList, renderCharacterDetails } from './character.js';
import { initializeRecruit, populateDropdown } from './recruit.js';
import { initializeEventHandler, createEvent } from './events.js';
import { elementManager } from './elementManager.js';

document.addEventListener("DOMContentLoaded", initializeApp);

function initializeApp() {
    console.log("DOM fully loaded and parsed");

    elementManager.initialize();
    renderCharacterList();
    initializeEventHandler();
    initializeRecruit();

    showSavefileModal();
    initializeEventListeners();
}

function showSavefileModal() {
    elementManager.get('savefileModal').style.display = "block";
}

function initializeEventListeners() {
    elementManager.get('savefileSubmit').addEventListener("click", handleSavefileSubmission);
    elementManager.get('savefileNameInput').addEventListener("keyup", handleSavefileKeyUp);
    elementManager.get('recruitButton').addEventListener("click", handleRecruitButtonClick);
    elementManager.get('eventButton').addEventListener("click", handleEventButtonClick);
    elementManager.get('saveButton').addEventListener("click", handleSaveButtonClick);
}

function handleSavefileSubmission() {
    const estateName = elementManager.get('savefileNameInput').value.trim();
    if (estateName) {
        console.log("Savefile name entered:", estateName);
        setEstateName(estateName);
        elementManager.get('savefileModal').style.display = "none";
        loadOrNewGame(estateName);
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

async function loadOrNewGame(savefileName, elements) {
    console.log("Loading game with savefile:", savefileName);
    try {
        let estateData = await loadEstateData(savefileName);
        handleEstateData(estateData, elements);
    } catch (error) {
        console.error('Error loading estate:', error);
    }
}

function handleEstateData(estateData) {
    if (estateData.characters && typeof estateData.characters === 'object') {
        Object.values(estateData.characters).forEach(addCharacter);
        renderCharacterList();
        const firstCharacterName = Object.keys(estateData.characters)[0];
        if (firstCharacterName) {
            renderCharacterDetails(firstCharacterName);
        }
    } else {
        console.error("Estate characters not found or not an object");
    }
}

function handleRecruitButtonClick() {
    // Show the recruit modal
    document.getElementById("recruit-modal").style.display = "block";
    
    // Populate the dropdown
    populateDropdown();
}

function handleEventButtonClick() {
    createEvent('random', 'Argument4', [], [], '');
}

function handleSaveButtonClick() {
    saveEstate();
}