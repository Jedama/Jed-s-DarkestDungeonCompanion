import { loadEstateData, createNewEstate, createEvent } from './apiClient.js';
import { addCharacter, setEstateName, getState } from './state.js';
import { renderCharacterList, renderCharacterDetails } from './character.js';
import { initializeRecruit } from './recruit.js';
import { initializeEventHandler, processEventResult } from './events.js';
import { showLoading, hideLoading } from './loading.js'; 

document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");

    // DOM Elements
    const elements = {
        savefileModal: document.getElementById("savefile-modal"),
        savefileSubmit: document.getElementById("savefile-submit"),
        savefileNameInput: document.getElementById("savefile-name"),
        eventButton: document.getElementById("event-button"),
        recruitButton: document.getElementById("recruit-button"),
        characterGrid: document.getElementById("character-grid"),
        storyModal: document.getElementById("story-modal"),
        returnButton: document.getElementById("return-btn"),
        renderCharacterList: renderCharacterList  // Add this function to elements
    };

    // Initialize
    showSavefileModal();
    initializeEventListeners();
  
    const { storyModal } = initializeEventHandler(elements);
    const { populateDropdown } = initializeRecruit(elements, storyModal);

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
            console.log("Estate name after setting:", getState().estateName);
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

    // Updated handleEventButtonClick function
    async function handleEventButtonClick() {
        try {
            showLoading();
            const result = await createEvent('random', '', [], [], '');
            console.log('Event created:', result);
            hideLoading();
            processEventResult(result, storyModal, elements);
        } catch (error) {
            console.error('Error creating event:', error);
            // Handle the error (e.g., show an error message to the user)
        }
    }
});