// eventHandler.js

export function initializeEventHandler(elements) {
    const storyModal = initializeStoryModal(elements);

    function processEventResult(result) {
        updateStoryPanel(result.title, result.storyText);
        updateCards(result.consequences);
        storyModal.show();
    }

    function initializeStoryModal(elements) {
        const modal = {
            show: function() {
                elements.storyModal.style.display = 'block';
                document.body.classList.add('story-modal-open');
            },
            hide: function() {
                elements.storyModal.style.display = 'none';
                document.body.classList.remove('story-modal-open');
                elements.renderCharacterList(elements);  // Update character list when closing modal
            }
        };

        elements.returnButton.addEventListener("click", modal.hide);

        return modal;
    }

    function updateStoryPanel(title, storyText) {
        const storyPanel = elements.storyModal.querySelector('.story-panel');
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
            return 'darkorange';
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
        const cardContainer = elements.storyModal.querySelector('.story-cards');
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

    return {
        processEventResult
    };
}