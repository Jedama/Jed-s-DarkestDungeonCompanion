// apiClient.js
export async function fetchOptions(fetchFunction) {
    // This is a placeholder. You'll need to implement the actual API calls.
    const response = await fetch(`/api/${fetchFunction}`);
    return response.json();
  }
  
  export async function submitEvent(eventData) {
    const response = await fetch('/api/create-event', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(eventData),
    });
    return response.json();
  }

  export async function fetchCharacterTitles() {
    const response = await fetch('/api/character_titles');
    if (!response.ok) {
        throw new Error('Failed to fetch character titles');
    }
    return response.json();
}