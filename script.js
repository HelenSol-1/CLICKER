// Получаем элементы DOM
const brain = document.getElementById('brain');
const scoreDisplay = document.getElementById('score');
const starsDisplay = document.getElementById('stars');
const energyDisplay = document.getElementById('energy');
const upgradeBtn = document.getElementById('upgrade-btn');
const taskBtn = document.getElementById('task-btn');
const resetBtn = document.getElementById('reset-btn');

// Инициализация переменных
let score = localStorage.getItem('brainScore') ? parseInt(localStorage.getItem('brainScore')) : 0;
let stars = localStorage.getItem('brainStars') ? parseInt(localStorage.getItem('brainStars')) : 0;
let energy = localStorage.getItem('brainEnergy') ? parseInt(localStorage.getItem('brainEnergy')) : 10;
let clickMultiplier = localStorage.getItem('clickMultiplier') ? parseInt(localStorage.getItem('clickMultiplier')) : 1;
let upgradeCost = 100; // Стоимость апгрейда

// Обновляем отображение очков, звёзд и энергии
scoreDisplay.textContent = score;
starsDisplay.textContent = stars;
energyDisplay.textContent = energy;

// Обработчик кликов по мозгу
brain.addEventListener('click', () => {
    if (energy > 0) {
        score += clickMultiplier;
        scoreDisplay.textContent = score;
        energy--;
        energyDisplay.textContent = energy;
        localStorage.setItem('brainScore', score);
        localStorage.setItem('brainEnergy', energy);
    } else {
        alert('Недостаточно энергии. Подожди восстановления!');
    }
});

// Ежедневные задания
taskBtn.addEventListener('click', () => {
    let taskCompleted = confirm('Реши задачу: 2 + 2 = ?');
    if (taskCompleted) {
        let starsEarned = 5;
        stars += starsEarned;
        starsDisplay.textContent = stars;
        localStorage.setItem('brainStars', stars);
        alert(`Ты получил ${starsEarned} звёзд за выполнение задания!`);
    }
});

// Апгрейд мощности кликов
upgradeBtn.addEventListener('click', () => {
    if (stars >= upgradeCost) {
        clickMultiplier++;
        stars -= upgradeCost;
        starsDisplay.textContent = stars;
        upgradeCost *= 2; // Увеличение стоимости апгрейда
        alert('Мощность кликов увеличена!');
        localStorage.setItem('brainStars', stars);
        localStorage.setItem('clickMultiplier', clickMultiplier);
    } else {
        alert('Недостаточно звёзд для улучшения.');
    }
});

// Сброс прогресса
resetBtn.addEventListener('click', () => {
    score = 0;
    stars = 0;
    energy = 10;
    clickMultiplier = 1;
    scoreDisplay.textContent = score;
    starsDisplay.textContent = stars;
    energyDisplay.textContent = energy;
    localStorage.clear();
});

// Восстановление энергии каждые 5 минут
setInterval(() => {
    if (energy < 10) {
        energy++;
        energyDisplay.textContent = energy;
        localStorage.setItem('brainEnergy', energy);
    }
}, 300000); // 5 минут = 300000 миллисекунд

// Обновление счётчиков при загрузке страницы
window.addEventListener('load', () => {
    scoreDisplay.textContent = score;
    starsDisplay.textContent = stars;
    energyDisplay.textContent = energy;
});
