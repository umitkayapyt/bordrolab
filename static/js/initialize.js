import { setupEventListeners } from './eventListeners.js';
import { initializePage } from './eventListeners.js';

document.addEventListener('DOMContentLoaded', function () {
    console.log("Sayfa yüklendi, başlangıç fonksiyonları çağırılıyor.");
    setupEventListeners();  // Olay dinleyicilerini kur
    initializePage();       // Sayfa yüklendiğinde yapılacak işlemleri başlat
});






