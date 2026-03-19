// static/app.js — ElfShark Mini App

const tg = window.Telegram?.WebApp;
if (tg) {
    tg.expand();
    tg.ready();
    console.log("🦈 | TG OK");
} else {
    console.log("🦈 | Browser Mode");
}

const API = window.location.origin;
const MANAGER = "lovemelt";

// i18n runtime helpers
let CURRENT_LANG = localStorage.getItem('es_lang') || 'ru';
function t(key){
    try{ return (TRANSLATIONS[CURRENT_LANG] && TRANSLATIONS[CURRENT_LANG][key]) || TRANSLATIONS['ru'][key] || key; }catch(e){ return key }
}

// ==================== PHOTO MAP ====================
// Соответствие подкатегорий/брендов и фотографий из /fotos
const PHOTO_MAP = {
    // Жидкости
    'ELFLIQ': '/fotos/ELFLIQ 5% 30ml.webp',
    'CHASER': '/fotos/PUFFY LIQUID 5%.webp',
    'PUFFY': '/fotos/PUFFY LIQUID 5%.webp',
    'HQD': '/fotos/HQD 5% 30ml Original.webp',
    'Vozol Prime': '/fotos/vozol Prime.webp',
    // POD-системы
    'ELF X': '/fotos/ELFBAR ELFX.webp',
    'ELF X MINI': '/fotos/ELFBAR ELFX MINI Kit.webp',
    'ELF X PRO': '/fotos/ELFBAR ELFX PRO.webp',
    'OXVA': '/fotos/OXVA Xlim V3 CARTRIDGE.webp',
    'SOLANA': '/fotos/ELFBAR ELFX.webp',
    'VAPORESSO': '/fotos/XROS 5.webp',
    // POD бренды через Vaporesso
    'XROS 4': '/fotos/XROS 4 Mini.webp',
    'XROS 5 MINI': '/fotos/XROS 5 MINI.webp',
    'XROS 5': '/fotos/XROS 5.webp',
    'Xros Pro 2': '/fotos/Xros Pro 2.webp',
    'VIBE SE': '/fotos/VIBE SE.webp',
    'HQD Cirak': '/fotos/Cirak.webp',
    'HQD Zest': '/fotos/Zest cart.webp',
    // Одноразки
    'ELF BAR': '/fotos/BC 45000.webp',
    'VOZOL': '/fotos/VOZOL RAVE 40000.webp',
    // По именам брендов
    'ElfBar': '/fotos/BC 45000.webp',
    'Vozol': '/fotos/VOZOL RAVE 40000.webp',
};

// Более точное маппирование по подпо имени товара
const NAME_PHOTO_MAP = [
    { key: 'BC 45000', photo: '/fotos/BC 45000.webp' },
    { key: 'BC10000', photo: '/img/elfbar bc 10000.png' },
    { key: 'GH 33000', photo: '/fotos/GH 33000 PRO.webp' },
    { key: 'ICE KING 30000', photo: '/fotos/ICE KING 30000.webp' },
    { key: 'RAYA D3', photo: '/fotos/RAYA D3 25000.webp' },
    { key: 'RI3000', photo: '/img/elfbarri3000.png' },
    { key: 'MoonNight', photo: '/fotos/MoonNight 40000.webp' },
    { key: 'Nic King', photo: '/fotos/Nic King.webp' },
    { key: 'Sour King', photo: '/fotos/Sour King.webp' },
    { key: 'Sweet King', photo: '/fotos/Sweet King.webp' },
    { key: 'VOZOL RAVE', photo: '/fotos/VOZOL RAVE 40000.webp' },
    { key: 'VOZOL GEAR', photo: '/fotos/VOZOL GEAR ICE&SWEET 50000.webp' },
    { key: 'VOZOL Vista', photo: '/fotos/Vista 40000.webp' },
    { key: 'ELVBAR ELFX MINI', photo: '/fotos/ELFBAR ELFX MINI Kit.webp' },
    { key: 'ELFBAR ELFX MINI', photo: '/fotos/ELFBAR ELFX MINI Kit.webp' },
    { key: 'ELFBAR ELFX PRO', photo: '/fotos/ELFBAR ELFX PRO.webp' },
    { key: 'ELFBAR ELFX Pod', photo: '/fotos/ELFBAR ELFX.webp' },
    { key: 'ELFBAR ELFX', photo: '/fotos/ELFBAR ELFX.webp' },
    { key: 'ELFLIQ', photo: '/fotos/ELFLIQ 5% 30ml.webp' },
    { key: 'HQD Cirak', photo: '/fotos/Cirak.webp' },
    { key: 'HQD Zest cart', photo: '/fotos/Zest cart.webp' },
    { key: 'HQD 5%', photo: '/fotos/HQD 5% 30ml Original.webp' },
    { key: 'Vozol Prime', photo: '/fotos/vozol Prime.webp' },
    { key: 'OXVA Xlim V3', photo: '/fotos/OXVA Xlim V3 CARTRIDGE.webp' },
    { key: 'VAPORESSO XROS 5 MINI', photo: '/fotos/XROS 5 MINI.webp' },
    { key: 'VAPORESSO XROS 5', photo: '/fotos/XROS 5.webp' },
    { key: 'VAPORESSO XROS 4', photo: '/fotos/XROS 4 Mini.webp' },
    { key: 'VAPORESSO Xros Pro', photo: '/fotos/Xros Pro 2.webp' },
    { key: 'VAPORESSO VIBE SE', photo: '/fotos/VIBE SE.webp' },
    { key: 'VAPORESSO Cartridge', photo: '/fotos/XROS 5.webp' },
    { key: 'Chaser', photo: '/fotos/PUFFY LIQUID 5%.webp' },
    { key: 'PUFFY', photo: '/fotos/PUFFY LIQUID 5%.webp' },
    { key: 'Solana', photo: '/fotos/ELFBAR ELFX.webp' },
];

function getProductPhoto(product) {
    const name = product.name || '';
    // Try name-based match first (most specific)
    for (const entry of NAME_PHOTO_MAP) {
        if (name.includes(entry.key)) return encodeURI(entry.photo);
    }
    // Fallback to subcategory map
    const sub = product.subcategory || '';
    if (PHOTO_MAP[sub]) return encodeURI(PHOTO_MAP[sub]);
    // Fallback to brand
    const brand = product.brand || '';
    if (PHOTO_MAP[brand]) return encodeURI(PHOTO_MAP[brand]);
    return null;
}

// ==================== STATE ====================
let allProducts = [];
let filteredProducts = [];
let categories = [];
let currentCategory = null;
let currentSubcat = null;
let cart = [];
let searchQuery = '';

let favorites = [];
let purchaseHistory = [];

// ==================== INIT ====================
document.addEventListener('DOMContentLoaded', () => {
    const ageOk = localStorage.getItem('es_age');
    if (ageOk) hideAgeGate();

    const saved = localStorage.getItem('es_cart');
    if (saved) { try { cart = JSON.parse(saved); } catch (e) { } }
    updateCartUI();
    // prefill manual username if available
    const savedUser = localStorage.getItem('es_username');
    if (savedUser) {
        const el = document.getElementById('checkoutUsername');
        if (el) el.value = savedUser;
    }
    // load favorites & history
    try { favorites = JSON.parse(localStorage.getItem('es_fav') || '[]'); } catch (e) { favorites = [] }
    try { purchaseHistory = JSON.parse(localStorage.getItem('es_history') || '[]'); } catch (e) { purchaseHistory = [] }

    // try to sync favorites from server if we have a username/manual username
    (async function syncFavoritesFromServer(){
        try{
            const manual = localStorage.getItem('es_username') || '';
            if(!manual) return; // no user identity to sync
            const res = await fetch(`${API}/api/favorites?username=${encodeURIComponent(manual)}`);
            const data = await res.json();
            if(data && data.success && Array.isArray(data.favorites)){
                // map server favorites (product_code) -> local favorites array (id unknown)
                // attempt to resolve product ids from allProducts if already loaded
                const codes = data.favorites.map(f=>f.product_code);
                const resolved = [];
                for(const c of codes){
                    const prod = allProducts.find(p=>p.code===c);
                    if(prod) resolved.push({id:prod.id, name:prod.name, price:prod.price});
                    else resolved.push({id:0, code:c, name:c, price:0});
                }
                if(resolved.length) { favorites = resolved; localStorage.setItem('es_fav', JSON.stringify(favorites)); }
            }
        }catch(e){ /* ignore sync errors */ }
    })();

    // apply translations early so header buttons and placeholders are localized
    try{ applyTranslations(localStorage.getItem('es_lang') || CURRENT_LANG); }catch(e){}
    // ensure settings handlers are available even if modal opens later
    try{ if(typeof registerSettingsHandlers==='function') registerSettingsHandlers(); }catch(e){}
});

function hideAgeGate() {
    const gate = document.getElementById('ageGate');
    if (gate) {
        gate.classList.remove('active');
        setTimeout(() => {
            gate.remove(); // Completely remove from DOM to prevent blocking clicks
            showApp();
        }, 300);
    } else {
        showApp();
    }
}

// Settings modal: language & currency
function showSettingsIfNeeded(){
    const lang = localStorage.getItem('es_lang');
    const curr = localStorage.getItem('es_curr');
    // if either missing, show modal
    if (!lang || !curr) {
        const modal = document.getElementById('settingsModal');
        if (modal) modal.classList.remove('hidden');
    // ensure handlers are registered (idempotent)
    registerSettingsHandlers();
        // apply translations live if language is already known (but modal opened due lack of curr)
        if (lang) applyTranslations(lang);
    } else {
        applyCurrencyToUI();
    }
}

function openSettingsModal(){
    const modal = document.getElementById('settingsModal');
    if(!modal) return;
    modal.classList.remove('hidden');
    // re-run handlers to sync active states
    document.querySelectorAll('.lang-btn').forEach(b=>{ b.classList.remove('active'); if(b.dataset.lang === (localStorage.getItem('es_lang') || CURRENT_LANG)) b.classList.add('active'); });
    document.querySelectorAll('.curr-btn').forEach(b=>{ b.classList.remove('active'); if(b.dataset.curr === (localStorage.getItem('es_curr') || 'USD')) b.classList.add('active'); });
    // ensure handlers are present
    registerSettingsHandlers();
    // try to focus the first button for keyboard/interaction
    const first = modal.querySelector('.lang-btn'); if(first) first.focus();
}

// Fallback onclick handlers for HTML buttons (ensures clicks work even if listeners failed)
function selectLanguage(btn){
    if(!btn) return;
    document.querySelectorAll('.lang-btn').forEach(x=>x.classList.remove('active'));
    btn.classList.add('active');
    try{ applyTranslations(btn.dataset.lang); }catch(e){}
}
function selectCurrency(btn){
    if(!btn) return;
    document.querySelectorAll('.curr-btn').forEach(x=>x.classList.remove('active'));
    btn.classList.add('active');
    try{ localStorage.setItem('es_curr', btn.dataset.curr); applyCurrencyToUI(); }catch(e){}
}
function saveSettings(){
    const selLang = document.querySelector('.lang-btn.active');
    const selCurr = document.querySelector('.curr-btn.active');
    if(!selLang || !selCurr) return showToast(t('settings.choose_both'));
    const chosenLang = selLang.dataset.lang;
    const chosenCurr = selCurr.dataset.curr;
    localStorage.setItem('es_lang', chosenLang);
    localStorage.setItem('es_curr', chosenCurr);
    CURRENT_LANG = chosenLang;
    applyCurrencyToUI();
    applyTranslations(CURRENT_LANG);
    const modal = document.getElementById('settingsModal'); if(modal) modal.classList.add('hidden');
    showToast(t('settings.saved'));
}

// Register handlers for language/currency buttons and save action. Idempotent.
function registerSettingsHandlers(){
    // languages
    document.querySelectorAll('.lang-btn').forEach(b=>{
        // avoid multiple identical listeners by cloning node if already has a marker
        if(b.dataset._registered === '1') return;
        b.addEventListener('click', ()=>{
            document.querySelectorAll('.lang-btn').forEach(x=>x.classList.remove('active'));
            b.classList.add('active');
            // apply translations immediately
            applyTranslations(b.dataset.lang);
        });
        // mark as registered
        b.dataset._registered = '1';
    });

    // currencies
    document.querySelectorAll('.curr-btn').forEach(b=>{
        if(b.dataset._registered === '1') return;
        b.addEventListener('click', ()=>{
            document.querySelectorAll('.curr-btn').forEach(x=>x.classList.remove('active'));
            b.classList.add('active');
            // update UI totals immediately (but numeric values remain server-based)
            localStorage.setItem('es_curr', b.dataset.curr);
            applyCurrencyToUI();
        });
        b.dataset._registered = '1';
    });

    const save = document.getElementById('saveSettingsBtn');
    if(save && save.dataset._registered !== '1'){
        save.addEventListener('click', ()=>{
            const selLang = document.querySelector('.lang-btn.active');
            const selCurr = document.querySelector('.curr-btn.active');
            if (!selLang || !selCurr) { showToast(t('settings.choose_both')); return; }
            const chosenLang = selLang.dataset.lang;
            const chosenCurr = selCurr.dataset.curr;
            localStorage.setItem('es_lang', chosenLang);
            localStorage.setItem('es_curr', chosenCurr);
            CURRENT_LANG = chosenLang;
            applyCurrencyToUI();
            applyTranslations(chosenLang);
            const modal = document.getElementById('settingsModal'); if (modal) modal.classList.add('hidden');
            showToast(t('settings.saved'));
        });
        save.dataset._registered = '1';
    }
}

function applyCurrencyToUI(){
    // Re-render product list and cart so formatPrice() is used everywhere
    try{
        renderProducts();
    }catch(e){}
    try{
        renderCartBody();
    }catch(e){}

    // update totals
    const total = cart.reduce((s, i) => s + i.price * i.quantity, 0);
    const totalEl = document.getElementById('cartTotalPrice');
    if (totalEl) totalEl.textContent = formatPrice(total);

    // update checkout sum inside translated checkout text
    const checkoutSumEl = document.getElementById('checkoutSum');
    if (checkoutSumEl) checkoutSumEl.textContent = formatPrice(total);
}

function currencySymbol(code){
    switch(code){
        case 'USD': return '$';
        case 'UAH': return '₴';
        case 'PLN': return 'zł';
        default: return code;
    }
}

function confirmAge() {
    localStorage.setItem('es_age', '1');
    hideAgeGate();
}

function rejectAge() {
    if (tg) tg.close(); else window.close();
}

function showApp() {
    const app = document.getElementById('app');
    app.classList.remove('hidden');
    loadCategories();
    loadProducts();
    // show settings modal if language/currency not configured
    setTimeout(()=>{ try{ showSettingsIfNeeded(); }catch(e){} }, 200);
}

// ==================== CATEGORIES ====================
async function loadCategories() {
    try {
        const res = await fetch(`${API}/api/categories`);
        const data = await res.json();
        categories = data.categories || [];
        renderCategories();
    } catch (e) { console.error('Categories error:', e); }
}

function renderCategories() {
    const scroll = document.getElementById('categories');
    if (!scroll) return;

    // Create new list to avoid side effects
    let catsToShow = [...categories];

    // Language-agnostic category keywords (lowercased tokens for detection)
    const CATEGORY_KEYWORDS = {
        liquids: ['жид','liquid','płyn','рідин','рідини','рідина','liquids','рід'],
        pods: ['под систем','под-систем','подсистем','pod system','pod-system','system pod','systemy pod','pods','pod-системы','podсистемы'],
        cartridges: ['картридж','cartridge','картриджі'],
        disposables: ['однораз','disposable','jednorazowe']
    };

    // Helper to present translated category names when possible (checks keywords across languages)
    function displayCategoryName(raw){
        if(!raw) return '';
        const lower = (raw||'').toLowerCase();
        if(CATEGORY_KEYWORDS.liquids.some(k => lower.includes(k))) return t('cats.liquids') || raw;
        if(CATEGORY_KEYWORDS.pods.some(k => lower.includes(k))) return t('cats.pods') || raw;
        if(CATEGORY_KEYWORDS.cartridges.some(k => lower.includes(k))) return t('cats.cartridges') || raw;
        if(CATEGORY_KEYWORDS.disposables.some(k => lower.includes(k))) return t('cats.disposables') || raw;
        return raw;
    }

    scroll.innerHTML =
            `<button class="cat-chip active" onclick='selectCategory(this, null)'>🔥 ${t('cats.all')}</button>` +
            catsToShow.map(c => {
                // Use single-quote attribute so JSON.stringify(...) (which emits a quoted string)
                // does not break HTML attributes on names that contain spaces/quotes.
                const label = displayCategoryName(c.name);
                return `<button class="cat-chip" onclick='selectCategory(this, ${JSON.stringify(c.name)})'>
                    ${c.icon || ''} ${label}
                </button>`;
        }).join('');
}

function stopPropagation(e) { e.stopPropagation(); }

function selectCategory(el, name) {
    document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    currentCategory = name;
    currentSubcat = null;

    if (name) {
        loadSubcategories(name);
    }
    else {
        document.getElementById('subcatsWrap').classList.add('hidden');
    }
    loadProducts();
}

// ==================== SUBCATEGORIES ====================
async function loadSubcategories(category) {
    try {
        const res = await fetch(`${API}/api/subcategories?category=${encodeURIComponent(category)}`);
        const data = await res.json();
        renderSubcategories(data.subcategories || []);
    } catch (e) { }
}
function renderSubcategories(subs){
    const wrap = document.getElementById('subcatsWrap');
    const scroll = document.getElementById('subcategories');
    if(!wrap || !scroll) return;
    if (!subs || !subs.length) { wrap.classList.add('hidden'); return; }

    // Subcategory translations
    const SUBCAT_TRANSLATIONS = {
        'HQD': { en: 'HQD', uk: 'HQD', pl: 'HQD', ru: 'HQD' },
        'OXVA': { en: 'OXVA', uk: 'OXVA', pl: 'OXVA', ru: 'OXVA' },
        'VAPORESSO': { en: 'VAPORESSO', uk: 'VAPORESSO', pl: 'VAPORESSO', ru: 'VAPORESSO' },
        'ELF X': { en: 'ELF X', uk: 'ELF X', pl: 'ELF X', ru: 'ELF X' },
        'ELFLIQ': { en: 'ELFLIQ', uk: 'ELFLIQ', pl: 'ELFLIQ', ru: 'ELFLIQ' },
        'PUFFY': { en: 'PUFFY', uk: 'PUFFY', pl: 'PUFFY', ru: 'PUFFY' },
        'CHASER': { en: 'CHASER', uk: 'CHASER', pl: 'CHASER', ru: 'CHASER' },
        'Vozol Prime': { en: 'Vozol Prime', uk: 'Vozol Prime', pl: 'Vozol Prime', ru: 'Vozol Prime' },
        'BC 45000': { en: 'BC 45000', uk: 'BC 45000', pl: 'BC 45000', ru: 'BC 45000' },
        'BC PRO 40000': { en: 'BC PRO 40000', uk: 'BC PRO 40000', pl: 'BC PRO 40000', ru: 'BC PRO 40000' },
        'GH 33000 PRO': { en: 'GH 33000 PRO', uk: 'GH 33000 PRO', pl: 'GH 33000 PRO', ru: 'GH 33000 PRO' },
        'ICE KING 30000': { en: 'ICE KING 30000', uk: 'ICE KING 30000', pl: 'ICE KING 30000', ru: 'ICE KING 30000' },
        'MoonNight 40000': { en: 'MoonNight 40000', uk: 'MoonNight 40000', pl: 'MoonNight 40000', ru: 'MoonNight 40000' },
        'Vozol Prime': { en: 'Vozol Prime', uk: 'Vozol Prime', pl: 'Vozol Prime', ru: 'Vozol Prime' },
        'VOZOL RAVE': { en: 'VOZOL RAVE', uk: 'VOZOL RAVE', pl: 'VOZOL RAVE', ru: 'VOZOL RAVE' },
        'VOZOL Vista': { en: 'VOZOL Vista', uk: 'VOZOL Vista', pl: 'VOZOL Vista', ru: 'VOZOL Vista' },
        'VOZOL GEAR': { en: 'VOZOL GEAR', uk: 'VOZOL GEAR', pl: 'VOZOL GEAR', ru: 'VOZOL GEAR' },
        'ELF X MINI': { en: 'ELF X MINI', uk: 'ELF X MINI', pl: 'ELF X MINI', ru: 'ELF X MINI' },
        'ELF X PRO': { en: 'ELF X PRO', uk: 'ELF X PRO', pl: 'ELF X PRO', ru: 'ELF X PRO' },
        'XROS 4 Mini': { en: 'XROS 4 Mini', uk: 'XROS 4 Mini', pl: 'XROS 4 Mini', ru: 'XROS 4 Mini' },
        'XROS 5': { en: 'XROS 5', uk: 'XROS 5', pl: 'XROS 5', ru: 'XROS 5' },
        'XROS 5 MINI': { en: 'XROS 5 MINI', uk: 'XROS 5 MINI', pl: 'XROS 5 MINI', ru: 'XROS 5 MINI' },
        'Xros Pro 2': { en: 'Xros Pro 2', uk: 'Xros Pro 2', pl: 'Xros Pro 2', ru: 'Xros Pro 2' },
        'VIBE SE': { en: 'VIBE SE', uk: 'VIBE SE', pl: 'VIBE SE', ru: 'VIBE SE' },
        'HQD Cirak': { en: 'HQD Cirak', uk: 'HQD Cirak', pl: 'HQD Cirak', ru: 'HQD Cirak' },
        'HQD Zest': { en: 'HQD Zest', uk: 'HQD Zest', pl: 'HQD Zest', ru: 'HQD Zest' },
        'SOLANA': { en: 'SOLANA', uk: 'SOLANA', pl: 'SOLANA', ru: 'SOLANA' },
    };

    function getSubcatName(raw) {
        if (!raw) return '';
        if (SUBCAT_TRANSLATIONS[raw] && SUBCAT_TRANSLATIONS[raw][CURRENT_LANG]) {
            return SUBCAT_TRANSLATIONS[raw][CURRENT_LANG];
        }
        return raw;
    }

    scroll.innerHTML =
        `<button class="subcat-chip active" onclick='selectSubcat(this, null)'>${t('subcat.all')}</button>` +
        subs.map(s => `<button class="subcat-chip" onclick='selectSubcat(this, ${JSON.stringify(s)})'>${getSubcatName(s)}</button>`).join('');
    wrap.classList.remove('hidden');
}

function selectSubcat(el, name) {
    document.querySelectorAll('.subcat-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    currentSubcat = name;
    applyFilters();
}

// ==================== PRODUCTS ====================
async function loadProducts() {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = `<div class="loading-state"><div class="spinner"></div><p>${t('loading')}</p></div>`;

    try {
        let url = `${API}/api/products?t=${Date.now()}`;
        if (currentCategory) url += `&category=${encodeURIComponent(currentCategory)}`;
        const res = await fetch(url);
        const data = await res.json();
        allProducts = data.products || [];
        applyFilters();
    } catch (e) {
        document.getElementById('productsGrid').innerHTML =
            `<div class="empty-state"><span>⚠️</span><p>${t('errors.load')}</p><small>${e.message}</small></div>`;
    }
}

function applyFilters() {
    let result = [...allProducts];
    if (currentSubcat) result = result.filter(p => p.subcategory === currentSubcat);
    if (searchQuery) {
        const q = searchQuery.toLowerCase();
        result = result.filter(p =>
            p.name.toLowerCase().includes(q) ||
            (p.code || '').toLowerCase().includes(q) ||
            (p.brand || '').toLowerCase().includes(q)
        );
    }
    filteredProducts = result;
    renderProducts();
}

function renderProducts() {
    const grid = document.getElementById('productsGrid');
    const countEl = document.getElementById('productCount');
    const label = document.getElementById('currentCategoryTitle');

    // Language-agnostic category keywords (lowercased tokens for detection)
    const CATEGORY_KEYWORDS = {
        liquids: ['жид','liquid','płyn','рідин','рідини','рідина','liquids','рід'],
        pods: ['под систем','под-систем','подсистем','pod system','pod-system','system pod','systemy pod','pods','pod-системы','podсистемы'],
        cartridges: ['картридж','cartridge','картриджі'],
        disposables: ['однораз','disposable','jednorazowe']
    };

    // Helper to present translated category names when possible
    function displayCategoryName(raw){
        if(!raw) return '';
        const lower = (raw||'').toLowerCase();
        if(CATEGORY_KEYWORDS.liquids.some(k => lower.includes(k))) return t('cats.liquids') || raw;
        if(CATEGORY_KEYWORDS.pods.some(k => lower.includes(k))) return t('cats.pods') || raw;
        if(CATEGORY_KEYWORDS.cartridges.some(k => lower.includes(k))) return t('cats.cartridges') || raw;
        if(CATEGORY_KEYWORDS.disposables.some(k => lower.includes(k))) return t('cats.disposables') || raw;
        return raw;
    }

    label.textContent = currentCategory ? displayCategoryName(currentCategory) : t('cats.all_full');
    countEl.textContent = `${filteredProducts.length} ${t('unit.pcs')}`;

    if (!filteredProducts.length) {
    grid.innerHTML = `<div class="empty-state"><span>🔍</span><p>${t('search.no_results')}</p><small>${t('search.try_change_filters')}</small></div>`;
        return;
    }

    // Group products by model for ALL categories (including "All")
    const shouldGroup = true;

    let productsToShow = [];

    if (shouldGroup) {
        // Group by model key (name before parentheses)
        const groups = new Map();
        filteredProducts.forEach(p => {
            const modelKey = getModelKeyForGrouping(p);
            if (!groups.has(modelKey)) {
                groups.set(modelKey, []);
            }
            groups.get(modelKey).push(p);
        });

        // Create grouped product cards
        groups.forEach((variants, modelKey) => {
            productsToShow.push({
                ...variants[0],
                _variants: variants,
                _isGrouped: true,
                _modelKey: modelKey
            });
        });
        
        // Sort: Vozol first, then ElfBar, then others (only in "All" category)
        if (!currentCategory || currentCategory === t('cats.all_full')) {
            productsToShow.sort((a, b) => {
                const aName = (a._modelKey || a.name || '').toUpperCase();
                const bName = (b._modelKey || b.name || '').toUpperCase();

                const aIsVozol = aName.includes('VOZOL') || aName.includes('VOZ');
                const aIsElfBar = aName.includes('ELF BAR') || aName.includes('ELFBAR') || aName.includes('ELF');
                const bIsVozol = bName.includes('VOZOL') || bName.includes('VOZ');
                const bIsElfBar = bName.includes('ELF BAR') || bName.includes('ELFBAR') || bName.includes('ELF');

                // Vozol first, then ElfBar, then others
                if (aIsVozol && !bIsVozol) return -1;
                if (bIsVozol && !aIsVozol) return 1;
                if (aIsElfBar && !bIsElfBar) return -1;
                if (bIsElfBar && !aIsElfBar) return 1;
                return 0;
            });
        }
    } else {
        productsToShow = filteredProducts;
    }

    grid.innerHTML = productsToShow.map(p => productCard(p)).join('');
}

function getModelKeyForGrouping(prod) {
    const name = (prod.name || '').trim();
    const beforeParen = name.split('(')[0].trim();
    return beforeParen.replace(/\s+/g, ' ');
}

function productCard(p) {
    const inCart = cart.find(i => i.id === p.id);
    const outOfStock = Number(p.stock) === 0;
    const photo = getProductPhoto(p);

    // For grouped products, use model key as name
    const displayName = p._isGrouped ? (p._modelKey || p.name) : p.name;
    const safeName = escapeHtml(displayName || '');
    const safePrice = escapeHtml(p.price == null ? '' : p.price);
    const priceWithSymbol = formatPrice(p.price);

    const thumbHtml = photo
        ? `<img src="${photo}" alt="${safeName}" loading="lazy">`
        : '';

    const btnText = outOfStock ? t('product.out_of_stock') : (inCart ? `${t('product.in_cart')} (${inCart.quantity})` : t('product.add'));
    const btnCls = outOfStock ? '' : (inCart ? 'in-cart' : '');
    const stockCls = p.stock > 10 ? 'stock-ok' : (p.stock > 0 ? 'stock-low' : 'stock-out');

    // For grouped products (disposables with flavors), show flavor slots
    let flavorsHtml = '';
    if (p._isGrouped && p._variants && p._variants.length > 1) {
        const totalStock = p._variants.reduce((sum, v) => sum + Number(v.stock), 0);
        
        flavorsHtml = `
            <div class="flavor-slots">
                ${p._variants.slice(0, 6).map(v => {
                    const flavorName = (v.name.includes('(') ? v.name.split('(').slice(1).join('(').replace(/\)$/, '').trim() : '') || v.subcategory || '';
                    const vStockCls = v.stock > 0 ? 'flavor-in-stock' : 'flavor-out';
                    return `<span class="flavor-chip ${vStockCls}" title="${escapeHtml(flavorName)}">${escapeHtml(flavorName.substring(0, 15))}${flavorName.length > 15 ? '...' : ''}</span>`;
                }).join('')}
                ${p._variants.length > 6 ? `<span class="flavor-more">+${p._variants.length - 6}</span>` : ''}
            </div>
        `;
    }

    const firstVariantId = p._isGrouped ? p._variants[0].id : p.id;
    const favId = firstVariantId;
    
    return `
    <div class="product-card">
    <button class="fav-btn" onclick="toggleFavorite(${favId})">${favorites.find(f=>f.id===favId)?'❤':'♡'}</button>
        <div class="product-thumb ${photo ? 'has-photo' : ''}">
            ${thumbHtml}
            ${outOfStock && !p._isGrouped ? `<div class="out-badge">${t('product.out_of_stock_badge')}</div>` : ''}
        </div>
        <div class="product-info">
            <div class="product-name">${safeName}</div>
            ${flavorsHtml}
            <div class="product-meta">
                <span class="product-price">${priceWithSymbol}</span>
                <span class="product-stock ${stockCls}">${p._isGrouped ? p._variants.reduce((s,v)=>s+Number(v.stock),0) : escapeHtml(p.stock)} ${t('unit.pcs')}</span>
            </div>
            <button class="add-btn ${btnCls}" ${outOfStock && !p._isGrouped ? 'disabled' : ''} onclick="openProductModal(${favId})">
                ${btnText}
            </button>
        </div>
    </div>`;
}

// ==================== SEARCH ====================
let searchTimer = null;
function onSearch(q) {
    searchQuery = q;
    const clearBtn = document.getElementById('searchClear');
    if (clearBtn) clearBtn.classList.toggle('hidden', !q);
    clearTimeout(searchTimer);
    searchTimer = setTimeout(applyFilters, 250);
}

function clearSearch() {
    const input = document.getElementById('searchInput');
    if (input) input.value = '';
    onSearch('');
}

// ==================== CART ====================
function addToCart(productId) {
    const product = allProducts.find(p => p.id === productId) || filteredProducts.find(p => p.id === productId);
    if (!product || product.stock === 0) return;

    const existing = cart.find(i => i.id === productId);
    if (existing) {
        if (existing.quantity >= product.stock) { showToast(t('toasts.no_more_stock')); return; }
        existing.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    saveCart();
    updateCartUI();
    applyFilters();
    if (tg?.HapticFeedback) tg.HapticFeedback.impactOccurred('light');
    showToast(t('toasts.added_to_cart'));
}

function updateQuantity(productId, delta) {
    const item = cart.find(i => i.id === productId);
    if (!item) return;
    const prod = allProducts.find(p=>p.id===productId) || item;
    // enforce stock limit
    const maxStock = Number(prod.stock) || Infinity;
    item.quantity += delta;
    if (item.quantity > maxStock) item.quantity = maxStock;
    if (item.quantity <= 0) cart = cart.filter(i => i.id !== productId);
    saveCart();
    updateCartUI();
    renderCartBody();
    applyFilters();
}

function saveCart() { localStorage.setItem('es_cart', JSON.stringify(cart)); }

function updateCartUI() {
    const count = cart.reduce((s, i) => s + i.quantity, 0);
    const countEl = document.getElementById('cartCount');
    if (countEl) { countEl.textContent = count; countEl.classList.toggle('hidden', count === 0); }

    const footer = document.getElementById('cartFooter');
    if (footer) footer.classList.toggle('hidden', cart.length === 0);

    const total = cart.reduce((s, i) => s + i.price * i.quantity, 0);
    const totalEl = document.getElementById('cartTotalPrice');
    if (totalEl) totalEl.textContent = formatPrice(total);

    const checkoutSumEl = document.getElementById('checkoutSum');
    if (checkoutSumEl) checkoutSumEl.textContent = formatPrice(total);
}

function openCart() {
    console.log("🛒 Opening cart...");
    const backdrop = document.getElementById('drawerBackdrop');
    const drawer = document.getElementById('cartDrawer');
    if (backdrop && drawer) {
        backdrop.classList.remove('hidden');
        drawer.classList.remove('hidden');
        renderCartBody();
        updateCartUI();
    } else {
        console.error("❌ Cart DOM elements missing!");
    }
}

function closeCart() {
    document.getElementById('drawerBackdrop').classList.add('hidden');
    document.getElementById('cartDrawer').classList.add('hidden');
}

function renderCartBody() {
    const body = document.getElementById('cartBody');
    if (!cart.length) {
        body.innerHTML = `<div class="empty-cart"><span>🛒</span><p>${t('cart.empty.title')}</p><small>${t('cart.empty.desc')}</small></div>`;
        return;
    }

    body.innerHTML = cart.map(item => {
        const photo = getProductPhoto(item);
        const thumbHtml = photo
            ? `<img src="${photo}" alt="${escapeHtml(item.name)}" style="width:100%;height:100%;object-fit:cover;border-radius:8px;">`
            : `<span style="font-size:24px;">${getCategoryEmoji(item)}</span>`;

        const safeName = escapeHtml(item.name || '');
    const safePrice = escapeHtml(item.price * item.quantity);
    const priceWithSymbol = formatPrice(item.price * item.quantity);

        return `
        <div class="cart-item">
            <div class="cart-item-icon">${thumbHtml}</div>
            <div class="cart-item-info">
                <div class="cart-item-name">${safeName}</div>
                <div class="cart-item-price">${priceWithSymbol}</div>
            </div>
            <div class="cart-item-qty">
                <button class="qty-btn" onclick="updateQuantity(${item.id}, -1)">−</button>
                <span class="qty-num">${escapeHtml(item.quantity)}</span>
                <button class="qty-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
            </div>
        </div>`;
    }).join('');
}

// ==================== CHECKOUT ====================
async function checkout() {
    if (!cart.length) return;
    // prevent double submit
    if (window.__es_checkout_in_progress) return showToast(t('checkout.in_progress'));
    window.__es_checkout_in_progress = true;
    const checkoutBtn = document.querySelector('.checkout-btn');
    if (checkoutBtn) setButtonLoading(checkoutBtn, true);
    showToast(t('checkout.processing'));

    // Enhanced TG Data Extraction v4.0 (deploy fix)
    let user = {};
    const tgData = window.Telegram?.WebApp;

    // Force init to ensure initData is available
    if (tgData && !tgData.initData) {
        try { tgData.ready(); } catch(e) {}
    }

    // Attempt 1: initDataUnsafe (most reliable)
    if (tgData?.initDataUnsafe?.user) {
        user = tgData.initDataUnsafe.user;
        console.log("✅ Got user from initDataUnsafe");
    }

    // Attempt 2: initData manual parse (fallback)
    if ((!user.id || !user.username) && tgData?.initData) {
        try {
            const params = new URLSearchParams(tgData.initData);
            const userJson = params.get('user');
            if (userJson) {
                const parsed = JSON.parse(userJson);
                user = { ...user, ...parsed }; // merge to preserve initDataUnsafe fields
                console.log("✅ Merged user from initData");
            }
        } catch (e) { console.error("Data parse err:", e); }
    }

    // Attempt 3: direct WebApp properties
    if (!user.id && tgData) {
        user = {
            id: tgData.initDataUnsafe?.user?.id || 0,
            username: tgData.initDataUnsafe?.user?.username || '',
            first_name: tgData.initDataUnsafe?.user?.first_name || tgData?.initDataUnsafe?.user?.first_name || '',
            last_name: tgData.initDataUnsafe?.user?.last_name || ''
        };
    }

    console.log("🦈 Checkout User Data v4.0:", user);
    console.log("🦈 initDataUnsafe available:", !!tgData?.initDataUnsafe);
    console.log("🦈 initData available:", !!tgData?.initData);

    const userId = user.id || 0;
    const username = user.username || '';
    const firstName = user.first_name || '';
    const lastName = user.last_name || '';
    const fullName = [firstName, lastName].filter(Boolean).join(' ') || t('checkout.anonymous_name');
    const total = cart.reduce((s, i) => s + i.price * i.quantity, 0);

    // read manual username fallback and persist - REQUIRED field
    const manualUsernameInput = document.getElementById('checkoutUsername');
    const manualUsername = manualUsernameInput ? manualUsernameInput.value.trim().replace(/^@/, '') : '';
    
    // Validate: username is required
    const finalUsername = username || manualUsername;
    if (!finalUsername) {
        showToast(t('checkout.username_required') || 'Введите username для оформления заказа');
        window.__es_checkout_in_progress = false;
        if (checkoutBtn) setButtonLoading(checkoutBtn, false);
        return;
    }
    
    if (manualUsername) localStorage.setItem('es_username', manualUsername);

    const orderData = {
        user_id: userId,
        username: finalUsername,
        full_name: fullName,
        raw_data: tgData?.initData || '',
        raw_init_unsafe: tgData?.initDataUnsafe || null,
        raw_user: (user && Object.keys(user).length) ? user : null,
        manual_username: manualUsername || null,
        products: cart.map(i => ({ id: i.id, name: i.name, code: i.code, price: i.price, quantity: i.quantity })),
        total: total
    };

    try {
        const controller = new AbortController();
        const timeout = setTimeout(()=>controller.abort(), 15000);
        const res = await fetch(`${API}/api/create_order`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData),
            signal: controller.signal
        });
        clearTimeout(timeout);
        const result = await res.json();

        if (result && result.success) {
            // save history locally
            const history = JSON.parse(localStorage.getItem('es_history')||'[]');
            const entry = { id: result.order_id || (Date.now()), total: total, date: new Date().toLocaleString() };
            history.unshift(entry);
            localStorage.setItem('es_history', JSON.stringify(history));
            purchaseHistory = history;

            if (tg) tg.openTelegramLink(`https://t.me/${MANAGER}`);
            cart = [];
            saveCart();
            updateCartUI();
            closeCart();
            renderCartBody();
            applyFilters();
            showToast((t('checkout.success')) + ` (#${entry.id})`);
            // animate cart footer briefly
            const footer = document.getElementById('cartFooter');
            if(footer){ footer.classList.add('order-success'); setTimeout(()=>footer.classList.remove('order-success'), 1400); }
        } else {
            showToast(t('checkout.error'));
        }
    } catch (e) {
    if (e.name === 'AbortError') showToast(t('errors.timeout'));
    else showToast(t('errors.write_manager'));
        if (tg) tg.openTelegramLink(`https://t.me/${MANAGER}`);
    }
    finally{
        window.__es_checkout_in_progress = false;
        if (checkoutBtn) setButtonLoading(checkoutBtn, false);
    }
}

// UI helper: toggle loading state on a button (adds class and disables)
function setButtonLoading(btn, on){
    if(!btn) return;
    if(on){ btn.classList.add('loading'); btn.setAttribute('disabled','disabled'); }
    else { btn.classList.remove('loading'); btn.removeAttribute('disabled'); }
}

// ==================== TOAST ====================
let toastTimer = null;
function showToast(msg, duration = 2500) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    clearTimeout(toastTimer);
    toast.textContent = msg;
    toast.classList.remove('hidden');
    requestAnimationFrame(() => toast.classList.add('show'));
    toastTimer = setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.classList.add('hidden'), 300);
    }, duration);
}

// Category scroll controls
function scrollCats(direction) {
    const scroll = document.getElementById('categories');
    if (!scroll) return;
    const step = Math.round(scroll.clientWidth * 0.6) * direction;
    scroll.scrollBy({ left: step, behavior: 'smooth' });
}

function updateCatArrows() {
    const wrap = document.getElementById('catsWrap');
    const left = document.getElementById('catScrollLeft');
    const right = document.getElementById('catScrollRight');
    const scroll = document.getElementById('categories');
    if (!scroll || !left || !right) return;
    if (scroll.scrollLeft > 10) left.classList.remove('hidden'); else left.classList.add('hidden');
    if (scroll.scrollLeft + scroll.clientWidth < scroll.scrollWidth - 10) right.classList.remove('hidden'); else right.classList.add('hidden');
}

// Add drag-to-scroll for categories
function makeCatsDraggable() {
    const scroll = document.getElementById('categories');
    if (!scroll) return;
    let isDown = false;
    let startX, scrollLeft;
    scroll.addEventListener('mousedown', (e) => { isDown = true; startX = e.pageX - scroll.offsetLeft; scrollLeft = scroll.scrollLeft; scroll.classList.add('dragging'); });
    scroll.addEventListener('mouseleave', () => { isDown = false; scroll.classList.remove('dragging'); });
    scroll.addEventListener('mouseup', () => { isDown = false; scroll.classList.remove('dragging'); });
    scroll.addEventListener('mousemove', (e) => { if (!isDown) return; e.preventDefault(); const x = e.pageX - scroll.offsetLeft; const walk = (x - startX) * 1; scroll.scrollLeft = scrollLeft - walk; updateCatArrows(); });

    // Touch
    scroll.addEventListener('touchstart', (e) => { startX = e.touches[0].pageX - scroll.offsetLeft; scrollLeft = scroll.scrollLeft; });
    scroll.addEventListener('touchmove', (e) => { const x = e.touches[0].pageX - scroll.offsetLeft; const walk = (x - startX) * 1; scroll.scrollLeft = scrollLeft - walk; updateCatArrows(); });
    scroll.addEventListener('scroll', updateCatArrows);
}

// Initialize arrows and drag after DOM ready and categories rendered
function initCategoryControls() {
    makeCatsDraggable();
    // initial arrow visibility
    setTimeout(updateCatArrows, 200);
}

// ensure initCategoryControls is called after categories loaded
const _orig_loadCategories = loadCategories;
loadCategories = async function() {
    await _orig_loadCategories();
    setTimeout(initCategoryControls, 100);
}

async function toggleFavorite(productId){
    const p = allProducts.find(x=>x.id===productId);
    if (!p) return;
    const idx = favorites.findIndex(f=>f.id===productId);
    const manual = localStorage.getItem('es_username') || '';
    const payload = {
        user_id: 0,
        username: manual,
        product_code: p.code,
        action: idx >= 0 ? 'remove' : 'add'
    };

    // update optimistically locally
    if (idx >=0) favorites.splice(idx,1); else favorites.push({id:p.id, name:p.name, price:p.price});
    localStorage.setItem('es_fav', JSON.stringify(favorites));
    applyFilters();

    try{
        const res = await fetch(`${API}/api/favorite`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
        const j = await res.json();
        if(!j || !j.success){
            // revert local change if server rejected
            if (payload.action === 'add') favorites = favorites.filter(f=>f.id!==productId);
            else if (payload.action === 'remove') favorites.push({id:p.id, name:p.name, price:p.price});
            localStorage.setItem('es_fav', JSON.stringify(favorites));
            applyFilters();
            showToast(t('fav.sync_error'));
            return;
        }
        showToast(payload.action === 'add' ? t('fav.added') : t('fav.removed'));
    }catch(e){
        // network error — keep local change as fallback
        console.warn('Favorite sync failed', e);
    showToast(idx >= 0 ? t('fav.removed') : t('fav.added'));
    }
}

function showFavorites(){
    const overlay = document.getElementById('overlayPanel');
    const body = document.getElementById('overlayBody');
    const title = document.getElementById('overlayTitle');
    title.textContent = t('overlay.fav');
    body.innerHTML = favorites.length ? favorites.map(f=>{
        const name = escapeHtml(f.name);
    const price = formatPrice(f.price);
    return `<div class="fav-row"><b>${name}</b> — ${price} <button data-id="${f.id}" class="fav-open-btn">${t('fav.open')}</button></div>`;
    }).join('') : `<p>${t('fav.empty')}</p>`;
    // delegate clicks
    body.querySelectorAll('.fav-open-btn').forEach(btn=>btn.addEventListener('click', e=>{ const id = Number(btn.getAttribute('data-id')); openProductById(id); }));
    overlay.classList.remove('hidden');
}

function showHistory(){
    const overlay = document.getElementById('overlayPanel');
    const body = document.getElementById('overlayBody');
    const title = document.getElementById('overlayTitle');
    title.textContent = t('overlay.history');
    body.innerHTML = purchaseHistory.length ? purchaseHistory.map(h=>`<div class="hist-row"><b>${t('history.order')} #${escapeHtml(h.id)}</b> ${formatPrice(h.total)} — ${escapeHtml(h.date)}</div>`).join('') : `<p>${t('history.empty')}</p>`;
    overlay.classList.remove('hidden');
}

async function showWatches(){
    const overlay = document.getElementById('overlayPanel');
    const body = document.getElementById('overlayBody');
    const title = document.getElementById('overlayTitle');
    title.textContent = t('overlay.flavors');
    const manual = localStorage.getItem('es_username') || '';
    try{
        const res = await fetch(`${API}/api/watches?username=${encodeURIComponent(manual)}`);
        const j = await res.json();
        if(j && j.success && Array.isArray(j.watches) && j.watches.length){
            body.innerHTML = j.watches.map(w=>{
                const q = escapeHtml(w.query_text);
                return `<div class="fav-row">${q} <button data-q="${escapeHtml(w.query_text)}" class="watch-remove-btn">${t('actions.delete')}</button></div>`;
            }).join('');
            body.querySelectorAll('.watch-remove-btn').forEach(b=>b.addEventListener('click', e=>{ removeWatch(b.getAttribute('data-q')); }));
            }else{
            body.innerHTML = `<p>${t('flavors.none')}</p>`;
        }
    }catch(e){ body.innerHTML = `<p>${t('errors.load')}</p>` }
    overlay.classList.remove('hidden');
}

async function removeWatch(query){
    const manual = localStorage.getItem('es_username') || '';
    try{
        const payload = { user_id:0, username:manual, query_text: query, action: 'remove' };
        const res = await fetch(`${API}/api/watch`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
        const j = await res.json();
        if(j && j.success){ showToast(t('actions.deleted')); showWatches(); }
        else showToast(t('errors.generic'));
    }catch(e){ showToast(t('errors.network')) }
}

function closeOverlay(){ document.getElementById('overlayPanel').classList.add('hidden') }

function openProductById(id){ closeOverlay(); openProductModal(id) }

function openProductModal(productId){
    const p = allProducts.find(x=>x.id===productId);
    if (!p) return;
    const modal = document.getElementById('productModal');
    const content = document.getElementById('modalContent');
    const photo = getProductPhoto(p) || '';
    
    // Check if product already has variants (grouped in renderProducts)
    let items = [p];
    if (p._isGrouped && p._variants && p._variants.length) {
        items = p._variants;
    } else {
        // Grouping by model: try to show all flavors/variants that belong to the same model
        function getModelKey(prod){
            const name = (prod.name||'').trim();
            const beforeParen = name.split('(')[0].trim();
            return beforeParen.replace(/\s+/g, ' ');
        }
        const modelKey = getModelKey(p);
        const variants = allProducts.filter(x => getModelKey(x) === modelKey);
        items = variants.length ? variants : [p];
    }
    
    function getModelKeyDisplay(prod){
        const name = (prod.name||'').trim();
        const beforeParen = name.split('(')[0].trim();
        return beforeParen.replace(/\s+/g, ' ');
    }

    function detectPuffCountFromName(name){
        if(!name) return null;
        const m1 = name.match(/(\d{4,5})/); if(m1) return m1[1];
        const m2 = name.match(/(\d+k)/i); if(m2) return m2[1];
        const m3 = name.match(/(\d+%)/); if(m3) return m3[1];
        return null;
    }

    const modelKey = getModelKeyDisplay(items[0]);

    // Build flavor rows
    const flavorRows = items.map(v => {
        const full = v.name || '';
    const flavor = (full.includes('(') ? full.split('(').slice(1).join('(').replace(/\)$/, '').replace(/\)$/,'').trim() : '') || v.subcategory || t('product.default_flavor');
        const puffs = detectPuffCountFromName(v.name) || detectPuffCountFromName(v.subcategory) || '';
        const stockCls = v.stock > 10 ? 'stock-ok' : (v.stock > 0 ? 'stock-low' : 'stock-out');
        return { id: v.id, name: v.name, flavor, price: v.price, stock: v.stock, puffs, cls: stockCls };
    });

    // selected variant tracking
    _selectedVariantId = items[0].id;
    _selectedFlavor = flavorRows[0] ? flavorRows[0].flavor : null;
    _selectedPuffs = flavorRows[0] ? flavorRows[0].puffs : null;

    content.innerHTML = `
        <div class="modal-content modal-product-detail">
            ${photo?`<img src="${photo}" alt="${modelKey}">`:''}
            <h3 class="modal-title">${modelKey}</h3>
            <p class="modal-sub">${formatPrice(items[0].price)}</p>
            <div class="brand-text">${escapeHtml(items[0].brand || '')}</div>
            <div class="flavor-list">
                ${flavorRows.map(fr => `
                    <div class="flavor-item ${fr.cls} ${fr.id===_selectedVariantId? 'active':'' }"
                         onclick="selectVariant(${fr.id})">
                        <div class="flavor-main"><b>${fr.flavor}</b></div>
                        <div class="flavor-meta">${formatPrice(fr.price)}${fr.puffs ? ' • '+fr.puffs+' '+t('unit.puffs') : ''} • ${fr.stock} ${t('unit.pcs')}</div>
                    </div>`).join('')}
            </div>
            <div class="modal-actions">
                <button id="modalAddBtn" class="checkout-btn" onclick="addFlavorToCart()">${t('product.add_to_cart')}</button>
                <button class="btn btn-secondary" onclick="closeProductModal()">${t('actions.cancel')}</button>
            </div>
        </div>
    `;
    modal.classList.remove('hidden');
}

function closeProductModal(){ document.getElementById('productModal').classList.add('hidden') }

let _selectedFlavor = null;
function selectFlavor(pid, flavor){ _selectedFlavor = flavor; showToast(t('product.flavor_selected') + flavor) }
// New variant selection: select a specific product id (variant)
let _selectedVariantId = null;
let _selectedPuffs = null;
function selectVariant(variantId){
    const v = allProducts.find(x=>x.id===variantId);
    if(!v) return;
    _selectedVariantId = variantId;
    // extract flavor and puffs from name
    const full = v.name || '';
    _selectedFlavor = (full.includes('(') ? full.split('(').slice(1).join('(').replace(/\)$/, '').replace(/\)$/,'').trim() : '') || v.subcategory || null;
    _selectedPuffs = (v.name && (v.name.match(/(\d{4,5}|\d+k)/)||[])[0]) || null;
    // refresh modal selection classes
    document.querySelectorAll('.flavor-item').forEach(el=>el.classList.remove('active'));
    const el = document.querySelector('.flavor-item[onclick*="selectVariant('+variantId+')"]');
    if(el) el.classList.add('active');
    showToast(t('product.flavor_selected') + (_selectedFlavor || t('product.default_flavor')));
}

function addFlavorToCart(){
    const variantId = _selectedVariantId;
    const p = allProducts.find(x=>x.id===variantId);
    if(!p) return showToast(t('errors.variant_not_selected'));
    // Prevent adding more than stock and prevent duplicate separate entries for same variant
    const existing = cart.find(i => i.id === p.id);
    if (existing) {
        if (existing.quantity >= p.stock) return showToast(t('toasts.no_more_stock'));
        existing.quantity += 1;
    } else {
        const prod = {...p, quantity:1, selected_flavor:_selectedFlavor || t('product.default_flavor'), selected_puffs: _selectedPuffs || null};
        cart.push(prod);
    }
    // show quick loading on modal button
    const mbtn = document.getElementById('modalAddBtn');
    if(mbtn) setButtonLoading(mbtn, true);
    setTimeout(()=>{ if(mbtn) setButtonLoading(mbtn, false); }, 600);
    saveCart();
    updateCartUI();
    closeProductModal();
    showToast(t('toasts.added_to_cart'), 1800);
    // purchaseHistory entry will be created on successful order
}

// ---------- Watchlist UI & API ----------
function openWatchPrompt(productId){
    const p = allProducts.find(x=>x.id===productId); if(!p) return; const q = prompt(t('watch.prompt_example'));
    if(!q) return; watchFlavor(q.trim()).then(ok=>{ if(ok) showToast(t('watch.added')) });
}

function watchFlavorPrompt(){
    const q = prompt(t('watch.prompt'));
    if(!q) return; watchFlavor(q.trim()).then(ok=>{ if(ok) showToast(t('watch.added')) });
}

async function watchFlavor(query){
    try{
        const manual = localStorage.getItem('es_username') || '';
        const payload = { user_id: 0, username: manual, query_text: query, action: 'add' };
        const res = await fetch(`${API}/api/watch`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
        const j = await res.json();
        return j && j.success;
    }catch(e){ console.warn('watch error', e); return false }
}

// subscriptions removed

// --------- Profile Linking (client) ---------
// Try to extract Telegram user object from WebApp and send to server to link
async function windowTelegramUser(){
    const tgData = window.Telegram?.WebApp;
    let user = {};
    if (tgData?.initDataUnsafe?.user) user = tgData.initDataUnsafe.user;
    else if (tgData?.initData){
        try{ const params = new URLSearchParams(tgData.initData); const uj = params.get('user'); if(uj) user = JSON.parse(uj); }catch(e){}
    }
    return user && Object.keys(user).length ? user : null;
}

async function linkProfile(){
    const user = await windowTelegramUser();
    let username = '';
    let tg_id = 0;

    if(user){ username = user.username || ''; tg_id = user.id || 0; }

    if(!username){
        // ask manual username fallback
    const manual = prompt(t('profile.enter_username'));
    if(!manual) return showToast(t('profile.link_cancelled'));
        username = manual.replace(/^@/, '').trim();
    }

    // send to server
    try{
        const payload = { username: username, tg_id: tg_id };
        const res = await fetch(`${API}/api/profile/link`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
        const j = await res.json();
        if(j && j.success){
            localStorage.setItem('es_username', username);
            showToast(t('profile.linked'));
        }else{
            showToast(t('profile.link_error'));
        }
    }catch(e){ console.warn('linkProfile error', e); showToast(t('errors.network')); }
}

// Helper: escape user-provided text for safe HTML insertion
function escapeHtml(input){
    if (input === null || input === undefined) return '';
    return String(input)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Format numeric price: convert to selected currency
function formatPrice(value){
    if (value == null || value === '') return '';
    const num = Number(value);
    const selectedCurr = localStorage.getItem('es_curr') || 'USD';
    
    // Convert price using rates
    const rates = conversionRates();
    const rate = rates[selectedCurr] || 1;
    const converted = num * rate;
    
    const formatted = (Math.round(converted) === converted) ? String(Math.round(converted)) : converted.toFixed(2);
    return `${formatted} ${currencySymbol(selectedCurr)}`;
}

function conversionRates(){
    // Rates from RUB to other currencies. Base currency in DB is RUB.
    return {
        'USD': 0.011,    // ~90 RUB = 1 USD
        'UAH': 0.45,     // ~2.2 RUB = 1 UAH
        'PLN': 0.044     // ~23 RUB = 1 PLN
    };
}

// Translations map for basic UI strings
const TRANSLATIONS = {
    ru: {
        'age.title': 'Подтвердите возраст',
        'age.text': 'Этот магазин содержит продукцию строго 18+. Вам уже исполнилось 18 лет?',
        'age.yes': 'Да, мне есть 18+',
        'age.no': 'Мне меньше 18',
        'age.note': 'Входя в магазин, вы подтверждаете соблюдение правил и регламентов.',
        'header.fav': '❤ Избранное',
        'header.history': '🕘 История',
        'header.link': '🔗 Привязать профиль',
        'header.settings': '⚙️ Настройки',
        'header.fav_aria': 'Избранное',
        'header.history_aria': 'История',
        'header.settings_aria': 'Настройки',
        'cats.scroll_left': 'Влево',
        'cats.scroll_right': 'Вправо',
        'search.placeholder': 'Поиск товаров...',
        'cart.checkout': 'Оформить за <span id="checkoutSum">0</span>',
        'checkout.username_label': 'Telegram username (без @) — опционально',
        'settings.choose_lang': 'Выберите язык:',
        'settings.choose_curr': 'Выберите валюту:',
        'settings.save': 'Сохранить',
        'settings.choose_both': 'Пожалуйста, выберите язык и валюту',
        'settings.saved': 'Сохранено',
        'cart.title': '🛒 Мой заказ',
        'header.cart': '🛒 КОРЗИНА',
        'cart.empty.title': 'Корзина пуста',
        'cart.empty.desc': 'Добавьте товары из каталога',
        'product.add_to_cart': 'Добавить в корзину',
        'product.notify_when': 'Уведомить при появлении',
        'actions.cancel': 'Отмена',
        'product.flavor_selected': 'Выбран вкус: ',
        'product.default_flavor': 'Стандартный',
        'errors.variant_not_selected': 'Ошибка — вариант не выбран',
        'toasts.no_more_stock': '⚠️ Больше нет в наличии',
        'toasts.added_to_cart': 'Добавлено в корзину',
        'actions.delete': 'Удалить',
        'actions.deleted': 'Удалено',
        'errors.generic': 'Ошибка',
        'unit.puffs': 'тяг',
        'watch.prompt_example': 'Уведомить при появлении вкуса. Введите часть названия вкуса (например "Watermelon"):',
        'watch.added': 'Добавлено в список оповещений',
        'watch.prompt': 'Уведомить при появлении вкуса. Введите часть названия вкуса:',
        'profile.enter_username': 'Введите ваш Telegram username (без @), для получения уведомлений:',
        'profile.link_cancelled': 'Привязка отменена',
        'profile.linked': 'Профиль привязан',
        'profile.link_error': 'Ошибка привязки',
        'loading': 'Загружаем...',
        'errors.load': 'Ошибка загрузки',
        'cats.liquids': 'Жидкости',
        'cats.pods': 'Под системы',
        'cats.cartridges': 'Картриджи',
        'cats.disposables': 'Одноразки',
        'cats.all_full': 'Все товары',
        'cats.all': 'Все',
        'unit.pcs': 'шт.',
        'search.no_results': 'Ничего не найдено',
        'search.try_change_filters': 'Попробуй изменить фильтры',
        'product.out_of_stock': '✕ Нет в наличии',
        'product.in_cart': '✓ В корзине ',
        'product.add': '+ В корзину',
        'product.out_of_stock_badge': 'Нет в наличии',
        'cats.liquids_keyword': 'Жид',
        'cats.disposables_keyword': 'Одно',
        'checkout.in_progress': 'Оформление уже выполняется...',
        'checkout.processing': 'Оформление заказа...',
        'checkout.anonymous_name': 'Покупатель',
        'checkout.username_label': 'Telegram username (без @) — обязательно',
        'checkout.username_placeholder': '@username или username',
        'checkout.username_required': '❌ Введите username для оформления заказа',
        'checkout.success': '✅ Заказ оформлен',
        'checkout.error': '❌ Ошибка при оформлении',
        'errors.timeout': '⚠️ Таймаут — проверьте соединение',
        'errors.write_manager': '⚠️ Напишите менеджеру напрямую',
        'errors.network': 'Сетевая ошибка',
        'subcat.all': 'Все',
        'overlay.fav': 'Избранное',
        'overlay.history': 'История',
        'history.order': 'Заказ №',
        'history.empty': 'История пуста',
        'fav.open': 'Открыть',
        'fav.empty': 'Пусто',
        'flavors.none': 'Нет любимых вкусов',
        'overlay.flavors': 'Любимые вкусы',
        'fav.added': 'Добавлено в избранное',
        'fav.removed': 'Удалено из избранного',
        'fav.sync_error': 'Ошибка синхронизации избранного'
    },
    // Settings modal labels
    // keys: settings.choose_lang, settings.choose_curr, settings.save
    // these are added per-language below
    en: {
        'age.title': 'Confirm your age',
        'age.text': 'This shop contains 18+ products. Are you 18 or older?',
        'age.yes': 'Yes, I am 18+',
        'age.no': 'I am under 18',
        'age.note': 'By entering, you confirm compliance with regulations.',
        'header.fav': '❤ Favorites',
        'header.history': '🕘 History',
        'header.link': '🔗 Link profile',
        'header.settings': '⚙️ Settings',
        'header.fav_aria': 'Favorites',
        'header.history_aria': 'History',
        'header.settings_aria': 'Settings',
        'cats.scroll_left': 'Scroll left',
        'cats.scroll_right': 'Scroll right',
        'search.placeholder': 'Search products...',
        'cart.checkout': 'Checkout <span id="checkoutSum">0</span>',
        'checkout.username_label': 'Telegram username (without @) — optional',
        'settings.choose_lang': 'Choose language:',
        'settings.choose_curr': 'Choose currency:',
        'settings.save': 'Save',
        'settings.choose_both': 'Please choose language and currency',
        'settings.saved': 'Saved',
        'cart.title': '🛒 My Order',
        'header.cart': '🛒 CART',
        'cart.empty.title': 'Your cart is empty',
        'cart.empty.desc': 'Add products from the catalog',
        'product.add_to_cart': 'Add to cart',
        'product.notify_when': 'Notify me when available',
        'actions.cancel': 'Cancel',
        'product.flavor_selected': 'Selected flavor: ',
        'product.default_flavor': 'Default',
        'errors.variant_not_selected': 'Error — variant not selected',
        'toasts.no_more_stock': '⚠️ Out of stock',
        'toasts.added_to_cart': 'Added to cart',
        'actions.delete': 'Delete',
        'actions.deleted': 'Deleted',
        'errors.generic': 'Error',
        'unit.puffs': 'puffs',
        'watch.prompt_example': 'Notify when flavor appears. Enter part of flavor name (e.g. "Watermelon"):',
        'watch.added': 'Added to watchlist',
        'watch.prompt': 'Notify when flavor appears. Enter part of flavor name:',
        'profile.enter_username': 'Enter your Telegram username (without @) to receive notifications:',
        'profile.link_cancelled': 'Linking cancelled',
        'profile.linked': 'Profile linked',
        'profile.link_error': 'Linking error',
        'loading': 'Loading...',
        'errors.load': 'Load error',
        'cats.liquids': 'Liquids',
        'cats.pods': 'Pod systems',
        'cats.cartridges': 'Cartridges',
        'cats.disposables': 'Disposables',
        'cats.all_full': 'All products',
        'cats.all': 'All',
        'unit.pcs': 'pcs',
        'search.no_results': 'Nothing found',
        'search.try_change_filters': 'Try changing filters',
        'product.out_of_stock': '✕ Out of stock',
        'product.in_cart': '✓ In cart ',
        'product.add': '+ Add',
        'product.out_of_stock_badge': 'Out of stock',
        'cats.liquids_keyword': 'Liquid',
        'cats.disposables_keyword': 'Disposable',
        'checkout.in_progress': 'Checkout already in progress...',
        'checkout.processing': 'Processing order...',
        'checkout.anonymous_name': 'Customer',
        'checkout.username_label': 'Telegram username (without @) — required',
        'checkout.username_placeholder': '@username or username',
        'checkout.username_required': '❌ Enter username to place order',
        'checkout.success': '✅ Order placed',
        'checkout.error': '❌ Error placing order',
        'errors.timeout': '⚠️ Timeout — check your connection',
        'errors.write_manager': '⚠️ Please contact the manager directly',
        'errors.network': 'Network error',
        'subcat.all': 'All',
        'overlay.fav': 'Favorites',
        'overlay.history': 'History',
        'history.order': 'Order #',
        'history.empty': 'History is empty',
        'fav.open': 'Open',
        'fav.empty': 'Empty',
        'flavors.none': 'No favorite flavors',
        'overlay.flavors': 'Favorite flavors',
        'fav.added': 'Added to favorites',
        'fav.removed': 'Removed from favorites',
        'fav.sync_error': 'Favorites sync error'
    },
    uk: {
        'age.title': 'Підтвердіть свій вік',
        'age.text': 'Цей магазин містить продукцію 18+. Вам виповнилося 18 років?',
        'age.yes': 'Так, мені більше 18',
        'age.no': 'Мені менше 18',
        'age.note': 'Увійшовши в магазин, ви підтверджуєте дотримання правил.',
        'header.fav': '❤ Улюблені',
        'header.history': '🕘 Історія',
        'header.link': '🔗 Прив\'язати профіль',
        'header.settings': '⚙️ Налаштування',
        'header.fav_aria': 'Улюблені',
        'header.history_aria': 'Історія',
        'header.settings_aria': 'Налаштування',
        'cats.scroll_left': 'Вліво',
        'cats.scroll_right': 'Вправо',
        'search.placeholder': 'Пошук товарів...',
        'cart.checkout': 'Оформити замовлення <span id="checkoutSum">0</span>',
        'checkout.username_label': 'Telegram username (без @) — опціонально',
        'settings.choose_lang': 'Виберіть мову:',
        'settings.choose_curr': 'Виберіть валюту:',
        'settings.save': 'Зберегти',
        'settings.choose_both': 'Будь ласка, оберіть мову та валюту',
        'settings.saved': 'Збережено',
        'cart.title': '🛒 Моє замовлення',
        'header.cart': '🛒 КОШИНА',
        'cart.empty.title': 'Кошик порожній',
        'cart.empty.desc': 'Додайте товари з каталогу',
        'product.add_to_cart': 'Додати до кошика',
        'product.notify_when': 'Повідомити при появі',
        'actions.cancel': 'Скасувати',
        'product.flavor_selected': 'Вибраний смак: ',
        'product.default_flavor': 'Стандартний',
        'errors.variant_not_selected': 'Помилка — варіант не вибраний',
        'toasts.no_more_stock': '⚠️ Більше немає в наявності',
        'toasts.added_to_cart': 'Додано до кошика',
        'actions.delete': 'Видалити',
        'actions.deleted': 'Видалено',
        'errors.generic': 'Помилка',
        'unit.puffs': 'тяг',
        'watch.prompt_example': 'Повідомити при появі смаку. Введіть частину назви (наприклад "Watermelon"):',
        'watch.added': 'Додано до списку сповіщень',
        'watch.prompt': 'Повідомити при появі смаку. Введіть частину назви смаку:',
        'profile.enter_username': 'Введіть ваш Telegram username (без @), щоб отримувати сповіщення:',
        'profile.link_cancelled': 'Прив\'язування скасовано',
        'profile.linked': 'Профіль прив\'язано',
        'profile.link_error': 'Помилка прив\'язки',
        'loading': 'Завантаження...',
        'errors.load': 'Помилка завантаження',
        'cats.liquids': 'Рідини',
        'cats.pods': 'Под системи',
        'cats.cartridges': 'Картриджі',
        'cats.disposables': 'Одноразки',
        'cats.all_full': 'Всі товари',
        'cats.all': 'Всі',
        'unit.pcs': 'шт.',
        'search.no_results': 'Нічого не знайдено',
        'search.try_change_filters': 'Спробуйте змінити фільтри',
        'product.out_of_stock': '✕ Немає в наявності',
        'product.in_cart': '✓ У кошику ',
        'product.add': '+ Додати',
        'product.out_of_stock_badge': 'Немає в наявності',
        'cats.liquids_keyword': 'Жид',
        'cats.disposables_keyword': 'Одно',
        'checkout.in_progress': 'Оформлення вже виконується...',
        'checkout.processing': 'Оформлення замовлення...',
        'checkout.anonymous_name': 'Покупець',
        'checkout.username_label': 'Telegram username (без @) — обов\'язково',
        'checkout.username_placeholder': '@username або username',
        'checkout.username_required': '❌ Введіть username для оформлення замовлення',
        'checkout.success': '✅ Замовлення оформлено',
        'checkout.error': '❌ Помилка при оформленні',
        'errors.timeout': '⚠️ Таймаут — перевірте підключення',
        'errors.write_manager': '⚠️ Напишіть менеджеру безпосередньо',
        'errors.network': 'Помилка мережі',
        'subcat.all': 'Усі',
        'overlay.fav': 'Улюблені',
        'overlay.history': 'Історія',
        'history.order': 'Замовлення №',
        'history.empty': 'Історія пуста',
        'fav.open': 'Відкрити',
        'fav.empty': 'Пусто',
        'flavors.none': 'Немає улюблених смаків',
        'overlay.flavors': 'Улюблені смаки',
        'fav.added': 'Додано до обраного',
        'fav.removed': 'Видалено з обраного',
        'fav.sync_error': 'Помилка синхронізації обраного'
    },
    pl: {
        'age.title': 'Potwierdź swój wiek',
        'age.text': 'Ten sklep zawiera produkty 18+. Masz 18 lat lub więcej?',
        'age.yes': 'Tak, mam 18+',
        'age.no': 'Mam mniej niż 18',
        'age.note': 'Wchodząc do sklepu potwierdzasz zgodność z regulaminem.',
        'header.fav': '❤ Ulubione',
        'header.history': '🕘 Historia',
        'header.link': '🔗 Powiąż profil',
        'header.settings': '⚙️ Ustawienia',
        'header.fav_aria': 'Ulubione',
        'header.history_aria': 'Historia',
        'header.settings_aria': 'Ustawienia',
        'cats.scroll_left': 'W lewo',
        'cats.scroll_right': 'W prawo',
        'search.placeholder': 'Szukaj produktów...',
        'cart.checkout': 'Zamów za <span id="checkoutSum">0</span>',
        'checkout.username_label': 'Telegram username (bez @) — opcjonalnie',
        'settings.choose_lang': 'Wybierz język:',
        'settings.choose_curr': 'Wybierz walutę:',
        'settings.save': 'Zapisz',
        'settings.choose_both': 'Proszę wybrać język i walutę',
        'settings.saved': 'Zapisano',
        'cart.title': '🛒 Moje zamówienie',
        'header.cart': '🛒 KOSZYK',
        'cart.empty.title': 'Twój koszyk jest pusty',
        'cart.empty.desc': 'Dodaj produkty z katalogu',
        'product.add_to_cart': 'Dodaj do koszyka',
        'product.notify_when': 'Powiadom, gdy dostępne',
        'actions.cancel': 'Anuluj',
        'product.flavor_selected': 'Wybrany smak: ',
        'product.default_flavor': 'Domyślny',
        'errors.variant_not_selected': 'Błąd — wariant nie wybrany',
        'toasts.no_more_stock': '⚠️ Brak w magazynie',
        'toasts.added_to_cart': 'Dodano do koszyka',
        'actions.delete': 'Usuń',
        'actions.deleted': 'Usunięto',
        'errors.generic': 'Błąd',
        'unit.puffs': 'łyków',
        'watch.prompt_example': 'Powiadom, gdy smak się pojawi. Wprowadź część nazwy smaku (np. "Watermelon"):',
        'watch.added': 'Dodano do listy powiadomień',
        'watch.prompt': 'Powiadom, gdy smak się pojawi. Wprowadź część nazwy smaku:',
        'profile.enter_username': 'Wprowadź swoją nazwę użytkownika Telegram (bez @), aby otrzymywać powiadomienia:',
        'profile.link_cancelled': 'Przypięcie anulowane',
        'profile.linked': 'Profil powiązany',
        'profile.link_error': 'Błąd przypinania',
        'loading': 'Ładowanie...',
        'errors.load': 'Błąd ładowania',
        'cats.liquids': 'Płyny',
        'cats.pods': 'Systemy pod',
        'cats.cartridges': 'Kartridże',
        'cats.disposables': 'Jednorazowe',
        'cats.all_full': 'Wszystkie produkty',
        'cats.all': 'Wszystkie',
        'unit.pcs': 'szt.',
        'search.no_results': 'Nic nie znaleziono',
        'search.try_change_filters': 'Spróbuj zmienić filtry',
        'product.out_of_stock': '✕ Brak w magazynie',
        'product.in_cart': '✓ W koszyku ',
        'product.add': '+ Dodaj',
        'product.out_of_stock_badge': 'Brak w magazynie',
        'cats.liquids_keyword': 'Liquid',
        'cats.disposables_keyword': 'Disposable',
        'checkout.in_progress': 'Realizacja zamówienia już w toku...',
        'checkout.processing': 'Przetwarzanie zamówienia...',
        'checkout.anonymous_name': 'Klient',
        'checkout.username_label': 'Telegram username (bez @) — wymagane',
        'checkout.username_placeholder': '@username lub username',
        'checkout.username_required': '❌ Wprowadź username, aby złożyć zamówienie',
        'checkout.success': '✅ Zamówienie złożone',
        'checkout.error': '❌ Błąd przy składaniu zamówienia',
        'errors.timeout': '⚠️ Przekroczono czas — sprawdź połączenie',
        'errors.write_manager': '⚠️ Skontaktuj się bezpośrednio z menedżerem',
        'errors.network': 'Błąd sieci',
        'subcat.all': 'Wszystko',
        'overlay.fav': 'Ulubione',
        'overlay.history': 'Historia',
        'history.order': 'Zamówienie #',
        'history.empty': 'Historia pusta',
        'fav.open': 'Otwórz',
        'fav.empty': 'Pusto',
        'flavors.none': 'Brak ulubionych smaków',
        'overlay.flavors': 'Ulubione smaki',
        'fav.added': 'Dodano do ulubionych',
        'fav.removed': 'Usunięto z ulubionych',
        'fav.sync_error': 'Błąd synchronizacji ulubionych'
    }
};

function applyTranslations(lang){
    CURRENT_LANG = lang || CURRENT_LANG;
    const map = TRANSLATIONS[CURRENT_LANG] || TRANSLATIONS['ru'];
    // apply text nodes
    Object.keys(map).forEach(key => {
        const els = document.querySelectorAll('[data-i18n="' + key + '"]');
        els.forEach(el => { el.innerHTML = map[key]; });
        const ph = document.querySelectorAll('[data-i18n-placeholder="' + key + '"]');
        ph.forEach(el => { el.setAttribute('placeholder', map[key]); });
        const aria = document.querySelectorAll('[data-i18n-aria-label="' + key + '"]');
        aria.forEach(el => { el.setAttribute('aria-label', map[key]); });
    });
    // re-render UI parts that depend on translated labels
    try{ renderCategories(); }catch(e){}
    try{ renderSubcategories([]); }catch(e){}
    try{ renderProducts(); }catch(e){}
}