import { getState } from './state.js';

const loadingOverlay = document.querySelector('.loading-overlay');
const loadingCard = document.querySelector('.loading-card');
let characterTitles = [];
let currentTitleIndex = 0;

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function createFaces() {
    const state = getState();
    characterTitles = Object.keys(state.characters);
    shuffleArray(characterTitles);

    for (let i = 0; i < 2; i++) {
        const face = document.createElement('div');
        face.className = 'loading-face';
        loadingCard.appendChild(face);
    }
}

function updateImages() {
    const faces = loadingCard.querySelectorAll('.loading-face');
    faces[0].style.backgroundImage = `url('/graphics/default/chibis/${characterTitles[currentTitleIndex].toLowerCase()}0.png')`;
    faces[1].style.backgroundImage = `url('/graphics/default/chibis/${characterTitles[(currentTitleIndex + 1) % characterTitles.length].toLowerCase()}0.png')`;
}

function changeImage() {
    currentTitleIndex = (currentTitleIndex + 2) % characterTitles.length;
    updateImages();
}

export function showLoading() {
    // Get and shuffle character titles
    
    if (!loadingCard.querySelector('.loading-face')) {
        createFaces();
    }
    
    loadingOverlay.style.display = 'flex';
    loadingOverlay.classList.add('active');
    
    // Set initial images
    updateImages();
    
    // Change image every half rotation (3 seconds in this case)
    const intervalId = setInterval(changeImage, 3000);
    
    // Store the interval ID on the overlay element
    loadingOverlay.dataset.intervalId = intervalId;
}

export function hideLoading() {
    loadingOverlay.style.display = 'none';
    loadingOverlay.classList.remove('active');
    
    // Clear the image changing interval
    clearInterval(Number(loadingOverlay.dataset.intervalId));
}