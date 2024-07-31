// apiClient.js
import { state } from './state.js';

function compileEstateData(additionalData = {}) {
  return {
      "estateName": state.estateName,
      "characters": state.characters,
      ...additionalData
  };
}

export async function loadEstateData(savefileName) {
  const response = await fetch(`/estates/${savefileName}/estate.json`);
  if (response.ok) return response.json();
  if (response.status === 404) return null;
  throw new Error(`HTTP error! Status: ${response.status}`);
}

export async function createNewEstate(savefileName) {
  const response = await fetch(`/api/create_estate/${savefileName}`, { method: 'POST' });
  if (!response.ok) {
    throw new Error(`Failed to create new estate. Status: ${response.status}`);
  }
  return response.json();
}

export async function saveEstate() {
  try {
      const estateData = compileEstateData();
      const response = await fetch('/api/save-estate', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(estateData),
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Estate saved successfully:', result);
      return result;
  } catch (error) {
      console.error('Error saving estate:', error);
      throw error;
  }
}

export async function fetchDefaultCharacterInfo() {
  const response = await fetch('/api/default_character_info');
  if (!response.ok) {
    throw new Error('Failed to fetch character info');
  }
  return response.json();
}

export async function createEvent(eventType, eventTitle, eventCharacters, eventModifiers, recruitName) {
  try {
      const estateData = compileEstateData({
          eventType: eventType,
          eventTitle: eventTitle,
          eventCharacters: eventCharacters,
          eventModifiers: eventModifiers,
          recruitName: recruitName
      });

      const response = await fetch('/api/create-event', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(estateData),
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Event created successfully:', result);
      return result;
  } catch (error) {
      console.error('Error creating event:', error);
      throw error;
  }
}