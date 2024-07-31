// apiClient.js
import { getState } from './state.js';

const BASE_URL = '/api'; // Consider moving this to a config file

function compileEstateData(additionalData = {}) {
  const state = getState();
  return {
    "estateName": state.estateName,
    "characters": state.characters,
    ...additionalData
  };
}

// Helper function for making API requests
async function apiRequest(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, options);

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

// Estate-related API calls
export async function loadEstateData(savefileName) {
  return apiRequest(`/estates/${savefileName}/estate.json`);
}

export async function createNewEstate(savefileName) {
  return apiRequest(`/create_estate/${savefileName}`, 'POST');
}

export async function saveEstate() {
  const estateData = compileEstateData();
  return apiRequest('/save-estate', 'POST', estateData);
}

// Character-related API calls
export async function fetchDefaultCharacterInfo() {
  return apiRequest('/default_character_info');
}

// Event-related API calls
export async function createEvent(eventType, eventTitle, eventCharacters, eventModifiers, recruitName) {
  const estateData = compileEstateData({
    eventType,
    eventTitle,
    eventCharacters,
    eventModifiers,
    recruitName
  });
  return apiRequest('/create-event', 'POST', estateData);
}

// Add any other API calls here...