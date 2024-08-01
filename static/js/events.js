// events.js
import { startEvent } from './apiClient.js';
import { EventHandlerFactory } from './eventHandler.js';
import { renderCharacterList } from './character.js';
import { getState, setEventType, updateRecruitInfo } from "./state.js";
import { elementManager } from './elementManager.js';
import { showLoading, hideLoading } from './loading.js';
import eventHandlers from './eventHandler.js';


export function initializeEventHandler() {
    const storyModal = initializeStoryModal();

    return { storyModal };
}

export async function createEvent(eventType, eventName, eventCharacter, eventModifiers, recruitName) {
    try {
        showLoading();
        const result = await startEvent(eventType, eventName, eventCharacter, eventModifiers, recruitName);
        hideLoading();
        processEventResult(result);
    } catch (error) {
        console.error('Error creating event:', error);
        // Handle the error (e.g., show an error message to the user)
    }
}

export function processEventResult(result) {
    const state = getState();
    const eventHandler = EventHandlerFactory.createHandler(result.eventType, state);
    
    eventHandler.processEvent(result);
  
    updateStoryPanel(result.title, result.storyText);
    updateCards(result.consequences);

    const storyModal = elementManager.get('storyModal');
    storyModal.style.display = 'block';

    // Update the current event type in the state
    setEventType(result.eventType);

    if (result.eventType == 'recruit') {
        updateRecruitInfo({
            recruitTitle: Object.keys(result.consequences)[0],
            recruitGroups: result.recruitGroups,
            recruitGroupsIndex: 0
        });
    }
}

function initializeStoryModal() {
    const modal = {
        show: function() {
            elementManager.get('storyModal').style.display = 'block';
            document.body.classList.add('story-modal-open');
        },
        hide: function() {
            elementManager.get('storyModal').style.display = 'none';
            document.body.classList.remove('story-modal-open');
            renderCharacterList();  // Update character list when closing modal
        }
    };

    elementManager.get('returnButton').addEventListener("click", () => {
        const currentEventType = getState().currentEventType;
        if (eventHandlers[currentEventType] && eventHandlers[currentEventType].return) {
            eventHandlers[currentEventType].return();
        }
        modal.hide();
    });

    elementManager.get('continueButton').addEventListener("click", () => {
        const currentEventType = getState().currentEventType;
        if (eventHandlers[currentEventType] && eventHandlers[currentEventType].continue) {
            eventHandlers[currentEventType].continue();
        }
    });

    return modal;
}

function updateStoryPanel(title, storyText) {
    const storyPanel = elementManager.get('storyPanel');
    storyPanel.innerHTML = `
        <h2 class="story-title">${title || 'New Event'}</h2>
        <p class="story-text">${storyText || 'No story available.'}</p>
    `;
}

const consequenceColorMap = {
    'Strength': 'crimson',
    'Agility': 'green',
    'Intelligence': 'dodgerblue',
    'Authority': 'darkmagenta',
    'Sociability': 'yellow',
    'Health': 'red',
    'Mental': 'white',
    'Money': 'gold',
    'Note': 'burlywood',
    'Appearance': 'beige',
    'Clothing': 'violet',
    'Status': 'lightseagreen',
    'Wound': 'darkred',
    'Disease': '#90EE90',
    'Equipment': 'silver',
    'Religion': 'lightyellow',
};

function getConsequenceColor(consequence) {
    // Check for positive consequence (+ "[text]")
    if (consequence.includes("+'")) {
        return 'orange';
    }
    
    // Check for negative consequence (- "[text]")
    if (consequence.includes("-'")) {
        return 'orangered';
    }

    // Check for keyword matches
    for (const [keyword, color] of Object.entries(consequenceColorMap)) {
        if (consequence.includes(keyword)) {
            return color;
        }
    }

    return 'lightsteelblue'; // default color
}

function processConsequences(consequences) {
    const characterData = {};

    Object.keys(consequences).forEach(character => {
        characterData[character] = {
            relationships: {},
            consequences: []
        };
    });

    Object.entries(consequences).forEach(([character, consequenceList]) => {
        consequenceList.forEach(consequence => {
            const affinityMatch = consequence.match(/\[(.+)\] Affinity ([-+]\d+)/);
            const dynamicMatch = consequence.match(/\[(.+)\] Dynamic update/);
            const descMatch = consequence.match(/\[(.+)\] Desc. update/);

            if (affinityMatch) {
                const targetCharacter = affinityMatch[1];
                const affinityChange = parseInt(affinityMatch[2]);
                if (!characterData[character].relationships[targetCharacter]) {
                    characterData[character].relationships[targetCharacter] = {};
                }
                characterData[character].relationships[targetCharacter].affinity = affinityChange;
            } else if (dynamicMatch) {
                const targetCharacter = dynamicMatch[1];
                if (!characterData[character].relationships[targetCharacter]) {
                    characterData[character].relationships[targetCharacter] = {};
                }
                characterData[character].relationships[targetCharacter].dynamic = 'Dynamic';
            } else if (descMatch) {
                const targetCharacter = descMatch[1];
                if (!characterData[character].relationships[targetCharacter]) {
                    characterData[character].relationships[targetCharacter] = {};
                }
                characterData[character].relationships[targetCharacter].description = 'Description';
            } else {
                characterData[character].consequences.push(consequence);
            }
        });
    });

    return characterData;
}

function updateCards(consequences) {
    const characterData = processConsequences(consequences);
    const cardContainer = elementManager.get('storyCards');
    cardContainer.innerHTML = ''; // Clear existing cards

    const cards = {};

    Object.entries(characterData).forEach(([character, data], index) => {
        if (index < 4) { // Limit to 4 cards
            const card = document.createElement('div');
            card.className = 'story-card';
            card.innerHTML = `
                <div class="card-frame-container">
                    <div class="card-glow"></div>
                    <div class="card-frame"></div>
                    <div class="card-content">
                        <div class="card-image" style="background-image: url('/graphics/default/cards/${character.toLowerCase()}0.png')"></div>
                        <ul class="consequence-text">
                            ${data.consequences.map(consequence => `
                                <li style="color: ${getConsequenceColor(consequence)};">${consequence}</li>
                            `).join('')}
                        </ul>
                        <div class="affinity-change-text"></div>
                    </div>
                    <div class="character-name-container">
                        <div class="character-name">${character}</div>
                    </div>
                </div>
            `;
            cardContainer.appendChild(card);
            cards[character] = card;

            // Add hover effect
            card.addEventListener('mouseover', () => {
                Object.entries(cards).forEach(([targetCharacter, targetCard]) => {
                    if (targetCharacter !== character) {
                        const relationship = data.relationships[targetCharacter] || {};
                        const glowElement = targetCard.querySelector('.card-glow');
                        const affinityChangeText = targetCard.querySelector('.affinity-change-text');
                        const consequenceText = targetCard.querySelector('.consequence-text');

                        // Update glow
                        const affinityChange = relationship.affinity || 0;
                        const isNegative = affinityChange < 0;
                        glowElement.classList.toggle('red', isNegative);
                        const intensity = Math.min(Math.abs(affinityChange) / 5, 1);
                        glowElement.style.opacity = intensity;

                        // Always fade out consequence text and show affinity change text
                        consequenceText.style.opacity = '0';
                        affinityChangeText.style.opacity = '1';

                        // Update affinity change text
                        let changeText = [];
                        if (affinityChange !== 0) {
                            const sign = affinityChange > 0 ? '+' : '';
                            changeText.push(`${sign}${affinityChange} Affinity`);
                        }
                        if (relationship.dynamic) {
                            changeText.push(`↻Dynamic`);
                        }
                        if (relationship.description) {
                            changeText.push(`↻Description`);
                        }

                        affinityChangeText.innerHTML = changeText.join('<br>');
                        affinityChangeText.style.color = affinityChange > 0 ? 'white' : (affinityChange < 0 ? 'red' : 'white');
                    }
                });
            });
            
            card.addEventListener('mouseout', () => {
                Object.values(cards).forEach(targetCard => {
                    const glowElement = targetCard.querySelector('.card-glow');
                    const affinityChangeText = targetCard.querySelector('.affinity-change-text');
                    const consequenceText = targetCard.querySelector('.consequence-text');

                    glowElement.style.opacity = '0';
                    affinityChangeText.style.opacity = '0';
                    consequenceText.style.opacity = '1';
                });
            });
        }
    });
}