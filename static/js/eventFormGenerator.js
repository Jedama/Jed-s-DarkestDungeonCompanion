export class EventFormGenerator {
  constructor(config) {
      this.config = config;
  }

  generateForm(category, eventType) {
      const formConfig = this.config[category][eventType];
      let formHTML = '';

      for (const field of formConfig.fields) {
          formHTML += this.generateField(field);
      }

      return formHTML;
  }

  generateField(field) {
    switch (field.type) {
        case 'character-select':
            return `
                <div class="custom-select">
                    <input type="text" id="${field.id}-input" placeholder="${field.label}">
                    <div id="${field.id}-dropdown" class="custom-select-dropdown"></div>
                </div>
            `;
        case 'modifier-input':
            return `
                <div class="modifier-input">
                    <input type="text" id="${field.id}-input" placeholder="${field.label}">
                    <ul id="${field.id}-list" class="modifier-list"></ul>
                </div>
            `;
        default:
            console.warn(`Unsupported field type: ${field.type}`);
            return '';
        }
    }

  populateCharacterSelect(fieldId, titles) {
      const input = document.getElementById(`${fieldId}-input`);
      const dropdown = document.getElementById(`${fieldId}-dropdown`);
      
      dropdown.innerHTML = titles.map(title => `<div class="dropdown-item">${title}</div>`).join('');
      
      input.addEventListener('focus', () => {
          dropdown.style.display = 'block';
      });

      document.addEventListener('click', (event) => {
          if (!event.target.closest('.custom-select')) {
              dropdown.style.display = 'none';
          }
      });

      input.addEventListener('input', () => {
          const filter = input.value.toLowerCase();
          let firstMatch = null;
          Array.from(dropdown.children).forEach(item => {
              const text = item.textContent.toLowerCase();
              if (text.startsWith(filter)) {
                  item.style.display = 'block';
                  if (!firstMatch) firstMatch = item;
              } else {
                  item.style.display = 'none';
              }
          });
          if (firstMatch) {
              firstMatch.scrollIntoView({ block: 'nearest' });
          }
      });

      dropdown.addEventListener('click', (event) => {
          if (event.target.classList.contains('dropdown-item')) {
              input.value = event.target.textContent;
              dropdown.style.display = 'none';
          }
      });
  }

  setupModifierInput(fieldId) {
    const input = document.getElementById(`${fieldId}-input`);
    const list = document.getElementById(`${fieldId}-list`);
    const modifiers = [];

    input.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            const modifier = input.value.trim();
            if (modifier) {
                modifiers.push(modifier);
                const li = document.createElement('li');
                li.textContent = modifier;
                list.appendChild(li);
                input.value = '';
            }
        }
    });

    return modifiers;
    }
}