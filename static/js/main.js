import { elementManager } from './elementManager.js';
import { loadEstateData, saveEstate } from './apiClient.js';
import { addCharacter, setDungeonTeam, setEstateName } from './state.js';

import { initializeDungeonView, updateDungeonView } from './dungeon.js';
import { initializeEventHandler, createEvent } from './events.js';
import { initializeRecruit, populateDropdown } from './recruit.js';
import { renderCharacterList, renderCharacterDetails } from './character.js';

document.addEventListener("DOMContentLoaded", initializeApp);

function initializeApp() {
    console.log("DOM fully loaded and parsed");

    elementManager.initialize();
    renderCharacterList();
    initializeEventHandler();
    initializeRecruit();
    initializeDungeonView();

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

function handleSavefileKeyUp(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        handleSavefileSubmission();
    }
}

async function loadOrNewGame(savefileName) {
    console.log("Loading game with savefile:", savefileName);
    try {
        let estateData = await loadEstateData(savefileName);
        handleEstateData(estateData);
    } catch (error) {
        console.error('Error loading estate:', error);
    }
}

function handleEstateData(estateData) {
    if (estateData.characters && typeof estateData.characters === 'object') {
        Object.values(estateData.characters).forEach(addCharacter);
        renderCharacterList();

        setDungeonTeam(estateData.dungeon_team)
        switchToView(estateData.dungeon_region);

        const firstCharacterName = Object.keys(estateData.characters)[0];
        if (firstCharacterName) {
            renderCharacterDetails(firstCharacterName);
        }
    } else {
        console.error("Estate characters not found or not an object");
    }
}

export function switchToView(region) {
    const galleryView = elementManager.get('galleryView');
    const dungeonView = elementManager.get('dungeonView');
    
    document.body.style.backgroundImage = `url('/graphics/default/assets/background/${encodeURIComponent(region)}.png')`;

    if (region == 'manor') {
        galleryView.style.display = 'block';
        dungeonView.style.display = 'none';
    } else {
        galleryView.style.display = 'none';
        dungeonView.style.display = 'block';
        updateDungeonView();
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