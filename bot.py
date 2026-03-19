# bot.py
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from database import db
from config import TOKEN, ADMIN_IDS, MANAGER_ID, MANAGER_USERNAME, PORT, WEBAPP_URL, DEFAULT_CURRENCY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Секретный код для входа в админ-панель
ADMIN_SECRET = "321"

# Временное хранилище сессий (user_id -> is_admin)
admin_sessions = set()

# ==================== FSM STATES ====================

class AdminStates(StatesGroup):
    waiting_for_code = State()
    waiting_for_product_code = State()
    waiting_for_action = State()
    waiting_for_new_stock = State()
    waiting_for_new_price = State()
    waiting_for_discount = State()


# ==================== KEYBOARDS ====================

def get_main_keyboard():
    # Cache busting: append ?v=13.2 to force Telegram to refresh the landing page
    url = f"{WEBAPP_URL}?v=13.2"
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍️ Открыть магазин", web_app=WebAppInfo(url=url))]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return kb

def get_admin_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить остаток", callback_data="admin_stock")],
        [InlineKeyboardButton(text="Изменить цену", callback_data="admin_price")],
        [InlineKeyboardButton(text="Сделать скидку", callback_data="admin_discount")],
        [InlineKeyboardButton(text="Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="Выйти из панели", callback_data="admin_exit")],
    ])
    return kb


# ==================== HANDLERS ====================

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user_name = message.from_user.first_name or "друг"
    await message.answer(
        f"👋 Привет, <b>{user_name}</b>!\n\n"
        f"Добро пожаловать в <b>ElfShark</b> — магазин электронных сигарет!\n\n"
        f"Большой ассортимент жидкостей, POD-систем и одноразок\n"
        f"Только оригинальная продукция\n"
        f"Быстрое оформление заказа\n\n"
        f"18+ Продажа только совершеннолетним\n\n"
        f"Нажми кнопку ниже, чтобы открыть каталог:",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )


@dp.message(Command("admin"))
async def cmd_admin(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_sessions:
        await show_admin_panel(message)
    else:
        await message.answer("🔐 Введите секретный код для входа в панель управления:")
        await state.set_state(AdminStates.waiting_for_code)


# Обработка ЛЮБОГО текстового сообщения — проверяем не является ли оно секретным кодом
@dp.message(F.text)
async def handle_text(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    # === Ожидание секретного кода ===
    if current_state == AdminStates.waiting_for_code:
        if message.text.strip() == ADMIN_SECRET:
            admin_sessions.add(message.from_user.id)
            await state.clear()
            await show_admin_panel(message)
        else:
            await message.answer("❌ Неверный код. Попробуйте ещё раз или напишите /start")
            await state.clear()
        return

    # === Ожидание артикула товара ===
    if current_state == AdminStates.waiting_for_product_code:
        code = message.text.strip()
        product = db.get_product_by_code(code)
        if not product:
            await message.answer(
                f"❌ Товар с артикулом <code>{code}</code> не найден.\n\nВведите другой артикул или /cancel для отмены:",
                parse_mode="HTML"
            )
        else:
            action = data.get('action', 'stock')
            await state.update_data(product_code=code, product_name=product['name'], current_stock=product['stock'], current_price=product['price'])
            
            if action == 'price':
                await message.answer(
                    f"<b>{product['name']}</b>\n"
                    f"Артикул: <code>{code}</code>\n"
                    f"Цена: <b>{product['price']} ₽</b>\n\n"
                    f"Введите новую цену:",
                    parse_mode="HTML"
                )
                await state.set_state(AdminStates.waiting_for_new_price)
            elif action == 'discount':
                await message.answer(
                    f"<b>{product['name']}</b>\n"
                    f"Артикул: <code>{code}</code>\n"
                    f"Цена: <b>{product['price']} ₽</b>\n\n"
                    f"Введите размер скидки в процентах (например 10 для 10%):\n"
                    f"Итоговая цена: <b>{product['price'] * 0.9:.0f} ₽</b>",
                    parse_mode="HTML"
                )
                await state.set_state(AdminStates.waiting_for_discount)
            else:
                await message.answer(
                    f"<b>{product['name']}</b>\n"
                    f"Артикул: <code>{code}</code>\n"
                    f"Текущий остаток: <b>{product['stock']} шт.</b>\n\n"
                    f"Введите новое количество:",
                    parse_mode="HTML"
                )
                await state.set_state(AdminStates.waiting_for_new_stock)
        return

    # === Ожидание нового количества ===
    if current_state == AdminStates.waiting_for_new_stock:
        try:
            new_stock = int(message.text.strip())
            if new_stock < 0:
                raise ValueError
        except ValueError:
            await message.answer("❌ Введите корректное число (>= 0):")
            return

        data = await state.get_data()
        code = data.get('product_code')
        name = data.get('product_name', '')
        old_stock = data.get('current_stock', 0)

        db.update_stock(code, new_stock)
        await state.clear()

        await message.answer(
            f"Остаток обновлён!\n\n"
            f"{name}\n"
            f"Было: {old_stock} шт. → Стало: <b>{new_stock} шт.</b>",
            parse_mode="HTML",
            reply_markup=get_admin_keyboard()
        )
        # Notify flavor watchers if new product matches their queries
        try:
            watchers = db.find_watchers_for_product(name)
            for w in watchers:
                try:
                    txt = f"Внимание! Появился товар, совпадающий с вашим запросом: <b>{w['query_text']}</b>\n\n{name}\nОстаток: {new_stock} шт.\n\nНапишите, чтобы уточнить заказ."
                    if w.get('username'):
                        await bot.send_message(f"@{w['username']}", txt, parse_mode='HTML')
                    elif w.get('user_id') and int(w.get('user_id'))>0:
                        await bot.send_message(int(w.get('user_id')), txt, parse_mode='HTML')
                except Exception as e:
                    logger.error(f"Failed to notify watcher {w}: {e}")
        except Exception as e:
            logger.error(f"Error finding watchers: {e}")
        return

    # === Ожидание новой цены ===
    if current_state == AdminStates.waiting_for_new_price:
        try:
            new_price = float(message.text.strip().replace(',', '.'))
            if new_price < 0:
                raise ValueError
        except ValueError:
            await message.answer("❌ Введите корректное число (>= 0):")
            return

        data = await state.get_data()
        code = data.get('product_code')
        name = data.get('product_name', '')
        old_price = data.get('current_price', 0)

        db.update_price(code, new_price)
        await state.clear()

        await message.answer(
            f"Цена обновлена!\n\n"
            f"{name}\n"
            f"Было: {old_price} ₽ → Стало: <b>{new_price} ₽</b>",
            parse_mode="HTML",
            reply_markup=get_admin_keyboard()
        )
        return

    # === Ожидание скидки ===
    if current_state == AdminStates.waiting_for_discount:
        try:
            discount = float(message.text.strip().replace(',', '.'))
            if discount < 0 or discount > 100:
                raise ValueError
        except ValueError:
            await message.answer("❌ Введите корректный процент от 0 до 100:")
            return

        data = await state.get_data()
        code = data.get('product_code')
        name = data.get('product_name', '')
        old_price = data.get('current_price', 0)
        new_price = round(old_price * (1 - discount / 100))

        db.update_price(code, new_price)
        await state.clear()

        await message.answer(
            f"Скидка применена!\n\n"
            f"{name}\n"
            f"Скидка: {discount}%\n"
            f"Было: {old_price} ₽ → Стало: <b>{new_price} ₽</b>",
            parse_mode="HTML",
            reply_markup=get_admin_keyboard()
        )
        return

    # === Секретный код введён как обычное сообщение ===
    if message.text.strip() == ADMIN_SECRET:
        admin_sessions.add(message.from_user.id)
        await state.clear()
        await show_admin_panel(message)
        return


@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("↩️ Отменено.", reply_markup=get_main_keyboard())
    if message.from_user.id in admin_sessions:
        await message.answer("🔧 Админ-панель:", reply_markup=get_admin_keyboard())


# ==================== ADMIN CALLBACKS ====================

@dp.callback_query(F.data == "admin_stock")
async def admin_stock_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in admin_sessions:
        await callback.answer("Нет доступа", show_alert=True)
        return
    await callback.message.answer(
        "Введите артикул товара (например <code>01519</code>):\n\n"
        "Артикул можно найти в каталоге под названием товара.\n"
        "Для отмены напишите /cancel",
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_product_code)
    await callback.answer()


@dp.callback_query(F.data == "admin_price")
async def admin_price_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in admin_sessions:
        await callback.answer("Нет доступа", show_alert=True)
        return
    await callback.message.answer(
        "Введите артикул товара для изменения цены (например <code>01519</code>):\n\n"
        "Для отмены напишите /cancel",
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_product_code)
    await state.update_data(action='price')
    await callback.answer()


@dp.callback_query(F.data == "admin_discount")
async def admin_discount_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in admin_sessions:
        await callback.answer("Нет доступа", show_alert=True)
        return
    await callback.message.answer(
        "Введите артикул товара для скидки (например <code>01519</code>):\n\n"
        "Для отмены напишите /cancel",
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_product_code)
    await state.update_data(action='discount')
    await callback.answer()


@dp.callback_query(F.data == "admin_stats")
async def admin_stats_callback(callback: types.CallbackQuery):
    if callback.from_user.id not in admin_sessions:
        await callback.answer("Нет доступа", show_alert=True)
        return
    stats = db.get_stats()
    await callback.message.answer(
        f"Статистика магазина\n\n"
        f"Всего товаров: <b>{stats['total_products']}</b>\n"
        f"В наличии: <b>{stats.get('in_stock', 0)}</b>\n"
        f"Нет в наличии: <b>{stats.get('out_of_stock', 0)}</b>",
        parse_mode="HTML",
        reply_markup=get_admin_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "admin_exit")
async def admin_exit_callback(callback: types.CallbackQuery):
    admin_sessions.discard(callback.from_user.id)
    await callback.message.answer("Вы вышли из панели управления.", reply_markup=get_main_keyboard())
    await callback.answer()


async def show_admin_panel(message: types.Message):
    stats = db.get_stats()
    await message.answer(
        f"Панель управления ElfShark\n\n"
        f"Товаров: <b>{stats['total_products']}</b>\n"
        f"В наличии: <b>{stats.get('in_stock', 0)}</b>\n\n"
        f"Выберите действие:",
        parse_mode="HTML",
        reply_markup=get_admin_keyboard()
    )


# ==================== API ENDPOINTS ====================

async def handle_webapp(request):
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            return web.Response(text=f.read(), content_type='text/html')
    except Exception as e:
        return web.Response(text=f"Error: {e}", status=500)

async def api_categories(request):
    try:
        categories = db.get_categories()
        return web.json_response({"categories": categories})
    except Exception as e:
        return web.json_response({"categories": [], "error": str(e)})

async def api_products(request):
    try:
        category = request.query.get('category')
        subcategory = request.query.get('subcategory')
        search = request.query.get('search')
        products = db.get_products(category, subcategory, search)
        return web.json_response({"products": products, "count": len(products)})
    except Exception as e:
        return web.json_response({"products": [], "error": str(e)}, status=500)

async def api_subcategories(request):
    try:
        category = request.query.get('category')
        subcategories = db.get_subcategories(category) if category else []
        return web.json_response({"subcategories": subcategories})
    except Exception as e:
        return web.json_response({"subcategories": [], "error": str(e)})

async def api_create_order(request):
    try:
        data = await request.json()
        logger.info(f"DEBUG: Order Payload Received: {data}")

        raw_init = data.get('raw_data', '')
        raw_user = data.get('raw_user')
        raw_init_unsafe = data.get('raw_init_unsafe')
        user_id = data.get('user_id', 0)
        username = data.get('username', '')
        full_name = data.get('full_name', '')
        manual_username = data.get('manual_username') or ''

        # === Приоритет 1: raw_user (JSON от webapp) ===
        if raw_user and isinstance(raw_user, dict):
            try:
                u = raw_user
                extracted_id = int(u.get('id', 0))
                extracted_username = u.get('username', '')
                extracted_first = u.get('first_name', '')
                extracted_last = u.get('last_name', '')

                if extracted_id > 0:
                    user_id = extracted_id
                if extracted_username:
                    username = extracted_username
                if extracted_first and not full_name:
                    full_name = f"{extracted_first} {extracted_last}".strip() or 'Покупатель'

                logger.info(f"✅ Extracted from raw_user: ID={user_id}, User={username}, Name={full_name}")
            except Exception as e:
                logger.error(f"Failed to parse raw_user: {e}")

        # === Приоритет 2: server-side extraction из initData ===
        if (not user_id or not username) and raw_init:
            try:
                from urllib.parse import parse_qs
                import json
                params = parse_qs(raw_init)
                user_str = params.get('user', [None])[0]
                if user_str:
                    u_data = json.loads(user_str)
                    if not user_id:
                        user_id = int(u_data.get('id', 0))
                    if not username:
                        username = u_data.get('username', '')
                    if not full_name or full_name == 'Покупатель':
                        fn = u_data.get('first_name', '')
                        ln = u_data.get('last_name', '')
                        full_name = f"{fn} {ln}".strip() or full_name
                    logger.info(f"✅ Extracted from raw_data: ID={user_id}, User={username}")
            except Exception as e:
                logger.error(f"Failed to parse raw_init: {e}")

        # === Приоритет 3: raw_init_unsafe ===
        if (not user_id or not username) and raw_init_unsafe:
            try:
                u_obj = raw_init_unsafe.get('user') if isinstance(raw_init_unsafe, dict) else None
                if u_obj:
                    if not user_id:
                        user_id = int(u_obj.get('id', 0))
                    if not username:
                        username = u_obj.get('username', '')
                    if not full_name or full_name == 'Покупатель':
                        fn = u_obj.get('first_name', '')
                        ln = u_obj.get('last_name', '')
                        full_name = f"{fn} {ln}".strip() or full_name
                    logger.info(f"✅ Extracted from raw_init_unsafe: ID={user_id}, User={username}")
            except Exception as e:
                logger.error(f"Failed to parse raw_init_unsafe: {e}")

        # === Приоритет 4: manual_username (fallback) ===
        if not username and manual_username:
            username = manual_username
            logger.info(f"✅ Using manual_username from payload: {username}")

        # === Проверка: username обязателен ===
        if not username:
            logger.warning(f"Order rejected: no username provided. user_id={user_id}, full_name={full_name}")
            return web.json_response({"success": False, "error": "Username обязателен для оформления заказа"}, status=400)

        # === Линкуем пользователя в БД для будущих уведомлений ===
        if user_id > 0:
            try:
                db.link_user(user_id, username or '', full_name or '')
                logger.info(f"Linked tg user {user_id} (@{username or 'no_username'})")
            except Exception as e:
                logger.error(f"Failed to link user: {e}")

        products_list = data.get('products', [])
        total = data.get('total', 0)

        # === Берём актуальные цены из БД для менеджера ===
        products_with_actual_prices = []
        for p in products_list:
            code = p.get('code', '')
            if code:
                db_product = db.get_product_by_code(code)
                if db_product:
                    products_with_actual_prices.append({
                        'name': db_product['name'],
                        'code': code,
                        'price': db_product['price'],
                        'quantity': p.get('quantity', 1)
                    })
                else:
                    products_with_actual_prices.append({
                        'name': p.get('name', 'Неизвестно'),
                        'code': code,
                        'price': p.get('price', 0),
                        'quantity': p.get('quantity', 1)
                    })
            else:
                products_with_actual_prices.append(p)

        order_id = db.create_order(user_id, username, full_name, products_list, total)

        def _sym(code):
            return {'USD':'$','UAH':'₴','PLN':'zł'}.get(code, code)
        cur_sym = _sym(DEFAULT_CURRENCY)
        products_text = "\n".join([
            f"  • {p['name']} x{p.get('quantity', 1)} — {p.get('price', 0)} {cur_sym}"
            for p in products_with_actual_prices
        ])

        logger.info(f"New Order: #{order_id} UserID={user_id}, Username={username}, Name={full_name}, Total={total}")

        # Формируем отображение пользователя
        if username:
            user_link = f"@{username}"
            contact_link = f"https://t.me/{username}"
        else:
            user_link = "<i>не задан</i>"
            contact_link = f"tg://user?id={user_id}"

        mention = f"<a href='tg://user?id={user_id}'>{full_name}</a>"

        manager_text = (
            f"Новый заказ\n\n"
            f"Клиент: {mention}\n"
            f"Username: {user_link}\n"
            f"Telegram ID: <code>{user_id}</code>\n\n"
            f"Товары:\n{products_text}\n\n"
            f"Итого: {total} {cur_sym}\n\n"
            f"Написать клиенту: <a href='{contact_link}'>ссылка</a>"
        )

        try:
            await bot.send_message(MANAGER_ID, manager_text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Failed to notify manager: {e}")

        return web.json_response({"success": True, "order_id": order_id})
    except Exception as e:
        logger.error(f"Order creation error: {e}")
        return web.json_response({"success": False, "error": str(e)}, status=500)


# subscriptions feature removed


async def api_favorite(request):
    try:
        data = await request.json()
        user_id = data.get('user_id', 0)
        username = data.get('username', '') or data.get('manual_username', '')
        product_code = data.get('product_code')
        action = data.get('action', 'add')

        if action == 'add':
            ok = db.add_favorite(user_id, username, product_code)
        else:
            ok = db.remove_favorite(user_id, username, product_code)
        return web.json_response({"success": bool(ok)})
    except Exception as e:
        logger.error(f"Favorite error: {e}")
        return web.json_response({"success": False, "error": str(e)}, status=500)
async def api_favorites(request):
    try:
        user_id = int(request.query.get('user_id', 0))
        username = request.query.get('username', '')
        favs = db.list_favorites(user_id, username)
        return web.json_response({"success": True, "favorites": favs})
    except Exception as e:
        logger.error(f"Favorites list error: {e}")
        return web.json_response({"success": False, "error": str(e)}, status=500)


async def api_watch(request):
    try:
        data = await request.json()
        user_id = data.get('user_id', 0)
        username = data.get('username', '') or data.get('manual_username', '')
        query_text = data.get('query_text', '')
        action = data.get('action', 'add')

        if not query_text:
            return web.json_response({"success": False, "error": "empty query_text"}, status=400)

        if action == 'add':
            ok = db.add_flavor_watch(user_id, username, query_text)
        else:
            ok = db.remove_flavor_watch(user_id, username, query_text)
        return web.json_response({"success": bool(ok)})
    except Exception as e:
        logger.error(f"Watch error: {e}")
        return web.json_response({"success": False, "error": str(e)}, status=500)


async def api_watches(request):
    try:
        user_id = int(request.query.get('user_id', 0))
        username = request.query.get('username', '')
        watches = db.list_flavor_watches(user_id, username)
        return web.json_response({"success": True, "watches": watches})
    except Exception as e:
        logger.error(f"Watches list error: {e}")
        return web.json_response({"success": False, "error": str(e)}, status=500)


async def api_profile_link(request):
    try:
        data = await request.json()
        tg_id = int(data.get('tg_id', 0))
        username = data.get('username') or ''
        first_name = data.get('first_name') or ''
        if not tg_id:
            return web.json_response({"success": False, "error": "no tg_id"}, status=400)
        ok = db.link_user(tg_id, username, first_name)
        return web.json_response({"success": bool(ok)})
    except Exception as e:
        logger.error(f"Profile link error: {e}")
        return web.json_response({"success": False, "error": str(e)}, status=500)


async def api_profile(request):
    try:
        username = request.query.get('username','')
        tg_id = int(request.query.get('tg_id',0) or 0)
        if username:
            u = db.get_user_by_username(username)
        elif tg_id:
            u = db.get_user_by_tgid(tg_id)
        else:
            u = None
        return web.json_response({"success": True, "user": u})
    except Exception as e:
        logger.error(f"Profile fetch error: {e}")
        return web.json_response({"success": False, "error": str(e)}, status=500)


# ==================== STARTUP ====================

async def main():
    runner = None
    try:
        app = web.Application()
        app.router.add_get('/', handle_webapp)
        app.router.add_get('/api/categories', api_categories)
        app.router.add_get('/api/products', api_products)
        app.router.add_get('/api/subcategories', api_subcategories)
        app.router.add_post('/api/create_order', api_create_order)
        app.router.add_post('/api/favorite', api_favorite)
        app.router.add_get('/api/favorites', api_favorites)
        app.router.add_static('/static', path='static', name='static')
        app.router.add_static('/fotos', path='fotos', name='fotos')
        app.router.add_static('/img', path='img', name='img')

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', PORT)

        try:
            await site.start()
        except OSError as e:
            if getattr(e, 'errno', None) == 10048:
                print(f"❌ Ошибка: Порт {PORT} уже занят. Закройте другие программы, использующие этот порт.")
            else:
                print(f"❌ Ошибка при запуске сервера: {e}")
            return

        print(f"\n{'='*50}")
        print(f"ElfShark Server запущен!")
        print(f"{'='*50}")
        print(f"Сервер: http://localhost:{PORT}")
        print(f"Товаров: {db.get_stats()['total_products']}")
        bot_info = await bot.get_me()
        print(f"Бот: @{bot_info.username}")
        print(f"{'='*50}\n")

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Critical error in main: {e}")
    finally:
        if runner:
            await runner.cleanup()
        try:
            await bot.session.close()
        except Exception:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n👋 Сервер остановлен")