// static/app.js
const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

const API_BASE = window.location.origin;
const MANAGER_USERNAME = "sharkbet12";

let cart = [];
let products = [];
let categories = [];
let currentCategory = null;
let userSettings = { language: 'ru', currency: 'RUB', theme: 'dark' };

const currencyRates = {
    RUB: { rate: 1, symbol: '₽' },
    UAH: { rate: 0.37, symbol: '₴' },
    USD: { rate: 0.011, symbol: '$' }
};

const languages = {
    ru: { flag: '🇷🇺', search: '🔍 Поиск товаров...', catalog: 'Каталог', cart: 'Корзина', total: 'Итого:', checkout: 'Оформить заказ', continue: 'Продолжить' },
    en: { flag: '🇬🇧', search: '🔍 Search products...', catalog: 'Catalog', cart: 'Cart', total: 'Total:', checkout: 'Checkout', continue: 'Continue' },
    uk: { flag: '🇺🇦', search: '🔍 Пошук товарів...', catalog: 'Каталог', cart: 'Кошик', total: 'Всього:', checkout: 'Оформити замовлення', continue: 'Продовжити' }
};

// ==================== THEME ====================

function initTheme() {
    const saved = localStorage.getItem('elfshark_settings');
    if (saved) {
        try { userSettings = { ...userSettings, ...JSON.parse(saved) }; } catch (e) { }
    }

    document.documentElement.setAttribute('data-theme', userSettings.theme);

    const themeSwitch = document.getElementById('themeSwitch');
    const settingsTheme = document.getElementById('settingsTheme');

    if (themeSwitch) themeSwitch.checked = userSettings.theme === 'dark';
    if (settingsTheme) settingsTheme.value = userSettings.theme;
}

function changeTheme(theme) {
    userSettings.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    saveSettings();
    const themeSwitch = document.getElementById('themeSwitch');
    if (themeSwitch) themeSwitch.checked = theme === 'dark';
}

function saveSettings() {
    localStorage.setItem('elfshark_settings', JSON.stringify(userSettings));
}

// ==================== LANGUAGE ====================

function changeLanguage(lang) {
    userSettings.language = lang;
    saveSettings();
    applyLanguage();
    const settingsLang = document.getElementById('settingsLang');
    if (settingsLang) settingsLang.value = lang;
}

function applyLanguage() {
    const lang = languages[userSettings.language];
    if (!lang) return;

    const searchInput = document.getElementById('searchInput');
    if (searchInput) searchInput.placeholder = lang.search;

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === userSettings.language);
    });
}

// ==================== CURRENCY ====================

function changeCurrency(currency) {
    userSettings.currency = currency;
    saveSettings();
    renderProducts();
    updateCartTotal();
    const settingsCurrency = document.getElementById('settingsCurrency');
    if (settingsCurrency) settingsCurrency.value = currency;
}

// ==================== AGE ====================

function checkAge() {
    const ageVerified = localStorage.getItem('elfshark_ageVerified');
    if (!ageVerified) {
        document.getElementById('ageModal').classList.add('active');
    } else {
        const welcomeShown = localStorage.getItem('elfshark_welcomeShown');
        if (!welcomeShown) {
            document.getElementById('welcomeModal').classList.add('active');
        } else {
            showMainApp();
        }
    }
}

function confirmAge() {
    localStorage.setItem('elfshark_ageVerified', 'true');
    document.getElementById('ageModal').classList.remove('active');
    setTimeout(() => {
        document.getElementById('welcomeModal').classList.add('active');
    }, 300);
}

function rejectAge() {
    tg.showAlert('Извините, вам должно быть 18+');
    tg.close();
}

function goToShop() {
    localStorage.setItem('elfshark_welcomeShown', 'true');
    saveSettings();
    document.getElementById('welcomeModal').classList.remove('active');
    showMainApp();
}

// ==================== SETTINGS ====================

function openSettings() {
    document.getElementById('settingsPanel').style.display = 'block';
    document.getElementById('settingsLang').value = userSettings.language;
    document.getElementById('settingsCurrency').value = userSettings.currency;
    document.getElementById('settingsTheme').value = userSettings.theme;
}

function closeSettings() {
    document.getElementById('settingsPanel').style.display = 'none';
}

// ==================== MAIN APP ====================

function showMainApp() {
    document.getElementById('mainApp').style.display = 'block';

    const savedCart = localStorage.getItem('elfshark_cart');
    if (savedCart) {
        try { cart = JSON.parse(savedCart); updateCartBadge(); } catch (e) { }
    }

    applyLanguage();
    loadCategories();
    loadProducts();
}

// ==================== CATEGORIES ====================

async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE}/api/categories`);
        const data = await response.json();
        categories = data.categories || [];

        const grid = document.getElementById('categoriesGrid');
        if (grid) {
            grid.innerHTML = categories.map(cat => `
                <div class="category-card" onclick="selectCategory(this, '${cat.name}')">
                    <span class="category-icon">${cat.icon}</span>
                    <h3>${cat.name}</h3>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Categories error:', error);
    }
}

function selectCategory(element, name) {
    document.querySelectorAll('.category-card').forEach(c => c.classList.remove('active'));
    element.classList.add('active');

    if (currentCategory === name) {
        currentCategory = null;
        document.getElementById('productsTitle').textContent = '🔥 Все товары';
    } else {
        currentCategory = name;
        document.getElementById('productsTitle').textContent = `🔥 ${name}`;
    }

    loadProducts();
}

// ==================== PRODUCTS ====================

async function loadProducts() {
    const grid = document.getElementById('productsGrid');
    const empty = document.getElementById('emptyProducts');
    const count = document.getElementById('productsCount');

    if (grid) grid.innerHTML = '<div class="loading">Загрузка...</div>';
    if (empty) empty.style.display = 'none';

    try {
        let url = `${API_BASE}/api/products`;
        if (currentCategory) {
            url += `?category=${encodeURIComponent(currentCategory)}`;
        }

        const response = await fetch(url);
        const data = await response.json();
        products = data.products || [];

        if (count) count.textContent = `${products.length} товаров`;

        if (products.length === 0) {
            if (grid) grid.innerHTML = '';
            if (empty) empty.style.display = 'block';
            return;
        }

        renderProducts();

    } catch (error) {
        console.error('Products error:', error);
        if (grid) {
            grid.innerHTML = `<div class="empty-state"><p>⚠️ Ошибка: ${error.message}</p><button onclick="loadProducts()" class="btn btn-primary" style="margin-top: 10px;">Повторить</button></div>`;
        }
    }
}

function renderProducts() {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;

    const rate = currencyRates[userSettings.currency].rate;
    const symbol = currencyRates[userSettings.currency].symbol;

    grid.innerHTML = products.map(p => {
        const price = Math.round(p.price * rate);
        const isOutOfStock = p.stock === 0;

        return `
            <div class="product-card" onclick="addToCart(${p.id})">
                <div class="product-image-container">
                    <img src="https://via.placeholder.com/300x300/1a1a25/8b5cf6?text=${encodeURIComponent(p.brand || 'ElfShark')}" alt="${p.name}">
                </div>
                <div class="product-info">
                    <div class="product-name">${p.name}</div>
                    <div class="product-code">Арт: ${p.code}</div>
                    <div class="product-footer">
                        <div class="product-price">${price} ${symbol}</div>
                        <div class="product-stock">${p.stock} шт.</div>
                    </div>
                    <button class="add-to-cart" ${isOutOfStock ? 'disabled' : ''}>
                        ${isOutOfStock ? 'Нет в наличии' : 'В корзину'}
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function searchProducts() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    const query = searchInput.value.toLowerCase();
    const filtered = products.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.code.toLowerCase().includes(query)
    );

    products = filtered;
    renderProducts();
    document.getElementById('productsCount').textContent = `${filtered.length} товаров`;
}

// ==================== CART ====================

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product || product.stock === 0) return;

    const existing = cart.find(item => item.id === productId);
    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    localStorage.setItem('elfshark_cart', JSON.stringify(cart));
    updateCartBadge();
    tg.HapticFeedback.impactOccurred('light');
}

function updateCartBadge() {
    const badge = document.getElementById('cartBadge');
    if (badge) {
        const total = cart.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = total;
        badge.style.display = total > 0 ? 'flex' : 'none';
    }
}

function openCart() {
    const modal = document.getElementById('cartModal');
    const itemsContainer = document.getElementById('cartItems');

    if (cart.length === 0) {
        itemsContainer.innerHTML = '<p style="text-align: center; color: var(--text-secondary); padding: 20px;">Корзина пуста</p>';
    } else {
        const rate = currencyRates[userSettings.currency].rate;
        const symbol = currencyRates[userSettings.currency].symbol;

        itemsContainer.innerHTML = cart.map(item => {
            const price = Math.round(item.price * rate);
            return `
                <div class="cart-item">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">${price} ${symbol}</div>
                    <div class="cart-item-quantity">
                        <button class="qty-btn" onclick="updateQuantity(${item.id}, -1)">-</button>
                        <span>${item.quantity}</span>
                        <button class="qty-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
                    </div>
                </div>
            `;
        }).join('');
    }

    updateCartTotal();
    modal.classList.add('active');
}

function closeCart() {
    document.getElementById('cartModal').classList.remove('active');
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    const product = products.find(p => p.id === productId);

    if (!item || !product) return;

    const newQuantity = item.quantity + change;

    if (newQuantity <= 0) {
        cart = cart.filter(i => i.id !== productId);
    } else if (newQuantity <= product.stock) {
        item.quantity = newQuantity;
    } else {
        tg.showAlert('Недостаточно товара');
        return;
    }

    localStorage.setItem('elfshark_cart', JSON.stringify(cart));
    updateCartBadge();
    openCart();
}

function updateCartTotal() {
    const totalEl = document.getElementById('cartTotal');
    if (!totalEl) return;

    const rate = currencyRates[userSettings.currency].rate;
    const symbol = currencyRates[userSettings.currency].symbol;
    const total = Math.round(cart.reduce((sum, item) => sum + (item.price * item.quantity), 0) * rate);
    totalEl.textContent = `${total} ${symbol}`;
}

function checkout() {
    if (cart.length === 0) {
        tg.showAlert('Корзина пуста');
        return;
    }

    // Открываем чат с менеджером
    tg.openTelegramLink(`https://t.me/${MANAGER_USERNAME}`);

    // Копируем текст заказа в буфер
    const rate = currencyRates[userSettings.currency].rate;
    const symbol = currencyRates[userSettings.currency].symbol;
    const total = Math.round(cart.reduce((sum, item) => sum + (item.price * item.quantity), 0) * rate);

    let orderText = `Здравствуйте! Хочу оформить заказ:\n\n`;
    cart.forEach(item => {
        const price = Math.round(item.price * rate);
        orderText += `• ${item.name} x${item.quantity} - ${price} ${symbol}\n`;
    });
    orderText += `\n💰 Итого: ${total} ${symbol}`;

    navigator.clipboard.writeText(orderText).then(() => {
        tg.showAlert('Текст заказа скопирован! Отправьте его менеджеру.');
    });

    // Очищаем корзину
    cart = [];
    localStorage.setItem('elfshark_cart', JSON.stringify(cart));
    updateCartBadge();
    closeCart();
}

// ==================== INIT ====================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🦈 ElfShark App starting...');

    initTheme();
    checkAge();

    // Welcome modal buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            changeLanguage(this.dataset.lang);
        });
    });

    document.querySelectorAll('.currency-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.currency-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            changeCurrency(this.dataset.currency);
        });
    });

    document.getElementById('themeSwitch')?.addEventListener('change', (e) => {
        changeTheme(e.target.checked ? 'dark' : 'light');
    });

    console.log('✅ App initialized!');
});