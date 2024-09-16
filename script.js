let stars = 0;
const brain = document.getElementById('brain');
const starsDisplay = document.getElementById('stars');
const feedBrainBtn = document.getElementById('feed-brain-btn');
const selectDietBtn = document.getElementById('select-diet-btn');

// Переходы между экранами
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

// Логика кликов на мозг
brain.addEventListener('click', () => {
    stars++;
    starsDisplay.textContent = stars;
});

// Переход на экран питания мозга
feedBrainBtn.addEventListener('click', () => {
    if (stars >= 10) {  // Условие для перехода
        showScreen('input-screen');
    } else {
        alert('Недостаточно звезд!');
    }
});

// Логика выбора типа питания и переход на экран продуктов
selectDietBtn.addEventListener('click', () => {
    showScreen('product-screen');
    displayProducts();
});

// Отображение продуктов
function displayProducts() {
    const productList = document.getElementById('product-list');
    productList.innerHTML = '';  // Очищаем список продуктов

    products.forEach(product => {
        const productButton = document.createElement('button');
        productButton.textContent = product.name;
        productButton.addEventListener('click', () => {
            alert(`${product.name}: ${product.calories} ккал`);
        });
        productList.appendChild(productButton);
    });
}
