document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");

    const currentCharacter = document.getElementById("current-character");
    const characterList = document.getElementById("character-list");
    const eventOptions = document.getElementById("event-options");
    const savefileModal = document.getElementById("savefile-modal");
    const savefileSubmit = document.getElementById("savefile-submit");
    const savefileNameInput = document.getElementById("savefile-name");

    console.log("HTML elements retrieved");

    savefileModal.style.display = "block";

    let estateName; // Store the estate name globally


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

    function handleEstateData(estateData) {
        if (estateData.characters && typeof estateData.characters === 'object') {
            renderCharacterList(Object.keys(estateData.characters));
        } else {
            console.error("Estate characters not found or not an object");
        }
    
        loadEventOptions();
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

    function renderCharacterList(characterTitles) {
        characterList.innerHTML = '';
        characterTitles.forEach(title => {
            const characterElement = document.createElement('div');
            characterElement.classList.add('character-item');
            characterElement.textContent = title;
            characterElement.addEventListener('click', () => loadAndRenderCharacterDetails(title));
            characterList.appendChild(characterElement);
        });
    }

    function loadAndRenderCharacterDetails(title) {
        fetchCharacterDetails(estateName, title)
            .then(renderCharacterDetails)
            .catch(error => {
                console.error(`Error fetching details for character ${title}:`, error);
                currentCharacter.innerHTML = `<p>Error loading character details</p>`;
            });
    }

    function renderCharacterDetails(character) {
        const imageUrl = `/portraits/${character.title.toLowerCase()}0.png`;
        console.log('Attempting to load image:', imageUrl);
        currentCharacter.innerHTML = `
            <img src="${imageUrl}" alt="${character.name}">
            <h2>${character.title}: ${character.name}</h2>
            <p>${character.summary}</p>
            <p>${character.history}</p>
            <!-- Add more details here -->
        `;
    }

    function loadEventOptions() {
        console.log("loadEventOptions function called");

        eventOptions.innerHTML = `<form>
            <label for="event-name">Event Name:</label>
            <input type="text" id="event-name" name="event-name"><br><br>
            <label for="event-description">Event Description:</label>
            <textarea id="event-description" name="event-description"></textarea><br><br>
            <button type="submit">Create Event</button>
        </form>`;
    }
});