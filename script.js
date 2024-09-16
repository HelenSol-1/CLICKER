let clicks = 0;
let stars = 0;

// Кликабельный мозг (на главном экране)
const brain = document.getElementById('brain');
const clicksDisplay = document.getElementById('clicks');
const starsDisplay = document.getElementById('stars');

// Логика кликов на мозг
brain.addEventListener('click', () => {
    clicks++;
    clicksDisplay.textContent = clicks;
});

// Верхнее меню
document.getElementById('home-btn').addEventListener('click', () => {
    window.location.href = 'index.html'; // Переход на главный экран
});

document.getElementById('buy-stars-btn').addEventListener('click', () => {
    window.location.href = 'buy-stars.html'; // Переход на экран покупки звезд
});

document.getElementById('user-data-btn').addEventListener('click', () => {
    window.location.href = 'input-screen.html'; // Переход на экран изменения данных
});

// Нижнее меню
document.getElementById('feed-brain-btn').addEventListener('click', () => {
    window.location.href = 'product-selection.html'; // Переход на экран выбора продуктов
});

document.getElementById('recommendations-btn').addEventListener('click', () => {
    window.location.href = 'recommendations.html'; // Переход на экран рекомендаций
});

