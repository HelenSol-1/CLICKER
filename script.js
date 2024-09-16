// Получаем элементы DOM
const brain = document.getElementById('brain');
const scoreDisplay = document.getElementById('score');
const resetBtn = document.getElementById('reset-btn');

// Инициализируем переменную для очков
let score = localStorage.getItem('brainScore') ? parseInt(localStorage.getItem('brainScore')) : 0;
scoreDisplay.textContent = score;

// Обработчик кликов по Маленькому Мозгу
brain.addEventListener('click', () => {
    score++; // Увеличиваем счётчик на 1
    scoreDisplay.textContent = score; // Обновляем отображение очков
    localStorage.setItem('brainScore', score); // Сохраняем очки в localStorage
});

// Сброс прогресса
resetBtn.addEventListener('click', () => {
    score = 0;
    scoreDisplay.textContent = score;
    localStorage.removeItem('brainScore'); // Удаляем сохранённые данные
});

// Обновляем счётчик при загрузке страницы
window.addEventListener('load', () => {
    scoreDisplay.textContent = score;
});
