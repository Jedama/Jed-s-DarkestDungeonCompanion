import { loadEstateData, createNewEstate, createEvent } from './apiClient.js';
import { addCharacter, setEstateName, getState, setEventType } from './state.js';
import { renderCharacterList, renderCharacterDetails } from './character.js';
import { initializeRecruit, populateDropdown } from './recruit.js';
import { initializeEventHandler, processEventResult } from './events.js';
import { showLoading, hideLoading } from './loading.js';
import { elementManager } from './elementManager.js';

document.addEventListener("DOMContentLoaded", initializeApp);

function initializeApp() {
    console.log("DOM fully loaded and parsed");

    elementManager.initialize();
    renderCharacterList();
    const { storyModal } = initializeEventHandler();
    initializeRecruit(storyModal);

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
}

function handleSavefileSubmission() {
    const estateName = elementManager.get('savefileNameInput').value.trim();
    if (estateName) {
        console.log("Savefile name entered:", estateName);
        setEstateName(estateName);
        console.log("Estate name after setting:", getState().estateName);
        elementManager.get('savefileModal').style.display = "none";
        loadGame(estateName);
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
        renderCharacterList(elements);
        const firstCharacterName = Object.keys(estateData.characters)[0];
        if (firstCharacterName) {
            renderCharacterDetails(firstCharacterName);
        }
    } else {
        console.error("Estate characters not found or not an object");
    }
}

function handleRecruitButtonClick(elements) {
    // Show the recruit modal
    document.getElementById("recruit-modal").style.display = "block";
    
    // Populate the dropdown
    populateDropdown(elements);
}

async function handleEventButtonClick(elements) {
    try {
      showLoading();
      const result = await createEvent('random', 'Argument4', [], [], '');
      hideLoading();
      setEventType('random', '');
      processEventResult(result, elements.storyModal, elements);
    } catch (error) {
      console.error('Error creating event:', error);
      // Handle the error (e.g., show an error message to the user)
    }
}