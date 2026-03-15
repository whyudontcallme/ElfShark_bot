# bot.py
import asyncio
import logging
from aiohttp import web
from database import db
from config import PORT, MANAGER_USERNAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        if category:
            subcategories = db.get_subcategories(category)
        else:
            subcategories = []
        return web.json_response({"subcategories": subcategories})
    except Exception as e:
        return web.json_response({"subcategories": [], "error": str(e)})

async def api_create_order(request):
    try:
        data = await request.json()
        order_id = db.create_order(
            data.get('user_id', 0),
            data.get('username', ''),
            data.get('full_name', ''),
            data.get('products', []),
            data.get('total', 0)
        )
        return web.json_response({"success": True, "order_id": order_id})
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

async def main():
    app = web.Application()
    app.router.add_get('/', handle_webapp)
    app.router.add_get('/api/categories', api_categories)
    app.router.add_get('/api/products', api_products)
    app.router.add_get('/api/subcategories', api_subcategories)
    app.router.add_post('/api/create_order', api_create_order)
    app.router.add_static('/static', path='static', name='static')
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    
    print(f"\n{'='*50}")
    print(f"🦈 ElfShark Server запущен!")
    print(f"{'='*50}")
    print(f"🌐 Откройте: http://localhost:{PORT}")
    print(f"📦 Товаров: {db.get_stats()['total_products']}")
    print(f"💬 Менеджер: @{MANAGER_USERNAME}")
    print(f"{'='*50}\n")
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен") 