# database.py
import sqlite3
import json
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "elfshark.db"):
        self.db_path = db_path
        self.init_db()
        self.load_products()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, icon TEXT, sort_order INTEGER DEFAULT 0)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, name TEXT NOT NULL,
            category TEXT, subcategory TEXT, brand TEXT, price REAL NOT NULL,
            stock INTEGER DEFAULT 0, is_active BOOLEAN DEFAULT 1)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            username TEXT, full_name TEXT, products_json TEXT NOT NULL,
            total_amount REAL NOT NULL, status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        conn.commit()
        conn.close()
        print("✅ База данных готова")
    
    def load_products(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM products')
        cursor.execute('DELETE FROM categories')
        
        categories = [
            (1, '💧 Жидкости', '💧', 1),
            (2, '🔌 POD-системы', '🔌', 2),
            (3, '🚬 Одноразки', '🚬', 3),
            (4, '🏷️ Скидочные', '🏷️', 4),
        ]
        
        for cat in categories:
            cursor.execute('INSERT INTO categories VALUES (?, ?, ?, ?)', cat)
        
        products = self._get_all_products()
        
        for prod in products:
            try:
                cursor.execute('''INSERT OR REPLACE INTO products 
                    (code, name, category, subcategory, brand, price, stock)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (prod['code'], prod['name'], prod['category'],
                     prod['subcategory'], prod['brand'], prod['price'], prod['stock']))
            except Exception as e:
                print(f"⚠️ Ошибка {prod['code']}: {e}")
        
        conn.commit()
        conn.close()
        print(f"✅ Загружено {len(products)} товаров")
    
    def _get_all_products(self) -> List[Dict]:
        products = []
        
        # ===== ЖИДКОСТИ =====
        liquids = [
            {'code': '00492', 'name': 'Chaser F/P 60mg (Ягоди)', 'category': 'Жидкости', 'subcategory': 'CHASER', 'brand': 'Chaser', 'price': 790, 'stock': 3},
            {'code': '01448', 'name': 'Chaser Ice Shot 1ml (Ice Shot)', 'category': 'Жидкости', 'subcategory': 'CHASER', 'brand': 'Chaser', 'price': 190, 'stock': 29},
            {'code': '01030', 'name': 'Chaser Special 60mg (Punch)', 'category': 'Жидкости', 'subcategory': 'CHASER', 'brand': 'Chaser', 'price': 790, 'stock': 1},
            {'code': '00822', 'name': 'ELFLIQ 5% 30ml (Apple Peach)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 22},
            {'code': '00754', 'name': 'ELFLIQ 5% 30ml (Apple Pear)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 62},
            {'code': '00804', 'name': 'ELFLIQ 5% 30ml (Blackberry Lemon)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 11},
            {'code': '00807', 'name': 'ELFLIQ 5% 30ml (Blackcurrant annised)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 97},
            {'code': '00821', 'name': 'ELFLIQ 5% 30ml (Blueberry)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 51},
            {'code': '00756', 'name': 'ELFLIQ 5% 30ml (Blueberry Raspberry Pomegranate)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 3},
            {'code': '00757', 'name': 'ELFLIQ 5% 30ml (Blueberry Rose Mint)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 46},
            {'code': '00755', 'name': 'ELFLIQ 5% 30ml (Blue Razz Ice)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 36},
            {'code': '01033', 'name': 'ELFLIQ 5% 30ml (Blue Razz Lemonade)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 46},
            {'code': '00819', 'name': 'ELFLIQ 5% 30ml (Cherry)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 53},
            {'code': '00818', 'name': 'ELFLIQ 5% 30ml (Cherry Cola)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 62},
            {'code': '00758', 'name': 'ELFLIQ 5% 30ml (Cherry Lemon Peach)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 45},
            {'code': '00809', 'name': 'ELFLIQ 5% 30ml (Cola)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 75},
            {'code': '00760', 'name': 'ELFLIQ 5% 30ml (Double Apple)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 56},
            {'code': '00803', 'name': 'ELFLIQ 5% 30ml (ELF Jack)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 79},
            {'code': '00762', 'name': 'ELFLIQ 5% 30ml (Green Grape Rose)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 23},
            {'code': '00764', 'name': 'ELFLIQ 5% 30ml (Lemon Lime)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 41},
            {'code': '00765', 'name': 'ELFLIQ 5% 30ml (Mango Peach)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 48},
            {'code': '01034', 'name': 'ELFLIQ 5% 30ml (P&B Cloud)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 67},
            {'code': '01272', 'name': 'ELFLIQ 5% 30ml (Pina Colada)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 41},
            {'code': '00767', 'name': 'ELFLIQ 5% 30ml (Pineapple Ice)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 59},
            {'code': '00815', 'name': 'ELFLIQ 5% 30ml (Pink Grapefruit)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 62},
            {'code': '00814', 'name': 'ELFLIQ 5% 30ml (Pink Lemonade)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 31},
            {'code': '00768', 'name': 'ELFLIQ 5% 30ml (Pink Lemonade Soda)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 64},
            {'code': '01032', 'name': 'ELFLIQ 5% 30ml (Rhubarb Snoow)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 93},
            {'code': '00770', 'name': 'ELFLIQ 5% 30ml (Sour Watermelon Gummy)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 3},
            {'code': '00813', 'name': 'ELFLIQ 5% 30ml (Spearmint)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 66},
            {'code': '00772', 'name': 'ELFLIQ 5% 30ml (Strawberry Cherry Lemon)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 49},
            {'code': '00812', 'name': 'ELFLIQ 5% 30ml (Strawberry Ice)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 67},
            {'code': '01035', 'name': 'ELFLIQ 5% 30ml (Strawberry Snoow)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 59},
            {'code': '00810', 'name': 'ELFLIQ 5% 30ml (Watermelon)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 85},
            {'code': '00773', 'name': 'ELFLIQ 5% 30ml (Watermelon Cherry)', 'category': 'Жидкости', 'subcategory': 'ELFLIQ', 'brand': 'ElfBar', 'price': 890, 'stock': 51},
            {'code': '00800', 'name': 'HQD 5% 30ml (Banana Ice)', 'category': 'Жидкости', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 850, 'stock': 9},
            {'code': '00649', 'name': 'HQD 5% 30ml (Lemon lime)', 'category': 'Жидкости', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 850, 'stock': 19},
            {'code': '00801', 'name': 'HQD 5% 30ml (Mr Blue)', 'category': 'Жидкости', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 850, 'stock': 9},
            {'code': '00802', 'name': 'HQD 5% 30ml (Strawberry Ice)', 'category': 'Жидкости', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 850, 'stock': 80},
            {'code': '00651', 'name': 'HQD 5% 30ml (Strawberry raspberry cherry ice)', 'category': 'Жидкости', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 850, 'stock': 67},
            {'code': '00652', 'name': 'HQD 5% 30ml (Watermelon ice)', 'category': 'Жидкости', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 850, 'stock': 74},
            {'code': '01576', 'name': 'PUFFY LIQUID 5% (Banana cherry)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 81},
            {'code': '01577', 'name': 'PUFFY LIQUID 5% (Berri kiwi)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 94},
            {'code': '01578', 'name': 'PUFFY LIQUID 5% (Black grape mint)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 63},
            {'code': '01579', 'name': 'PUFFY LIQUID 5% (Blueberry raspberry)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 90},
            {'code': '01580', 'name': 'PUFFY LIQUID 5% (Grape Raspberry Black Plum)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 86},
            {'code': '01581', 'name': 'PUFFY LIQUID 5% (Ice mojito mint)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 61},
            {'code': '01582', 'name': 'PUFFY LIQUID 5% (Lemon grapefruit)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 79},
            {'code': '01583', 'name': 'PUFFY LIQUID 5% (Pineapple coconut)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 80},
            {'code': '01584', 'name': 'PUFFY LIQUID 5% (Strawberry energy watermelon)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 71},
            {'code': '01585', 'name': 'PUFFY LIQUID 5% (Watermelon Bubble gum)', 'category': 'Жидкости', 'subcategory': 'PUFFY', 'brand': 'Puffy', 'price': 790, 'stock': 87},
            {'code': '01290', 'name': 'Vozol Prime (Berry)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 85},
            {'code': '01299', 'name': 'Vozol Prime (Berry Peach)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 90},
            {'code': '01288', 'name': 'Vozol Prime (Blueberry Ice)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 98},
            {'code': '01276', 'name': 'Vozol Prime (Blueberry Razz Lemon)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 91},
            {'code': '01296', 'name': 'Vozol Prime (Blueberry watermelon)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 88},
            {'code': '01300', 'name': 'Vozol Prime (Cherry Cola)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 97},
            {'code': '01282', 'name': 'Vozol Prime (Dragon Fruit Banana Cherry)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 69},
            {'code': '01274', 'name': 'Vozol Prime (Grape Ice)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 65},
            {'code': '01277', 'name': 'Vozol Prime (Kiwi Passion Fruite Guava)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 91},
            {'code': '01287', 'name': 'Vozol Prime (LavaFire)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 89},
            {'code': '01284', 'name': 'Vozol Prime (Lemon Lime)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 109},
            {'code': '01301', 'name': 'Vozol Prime (Love 777)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 74},
            {'code': '01285', 'name': 'Vozol Prime (Mint ice)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 101},
            {'code': '01283', 'name': 'Vozol Prime (Mixed Berries)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 94},
            {'code': '01294', 'name': 'Vozol Prime (Peach Ice)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 83},
            {'code': '01295', 'name': 'Vozol Prime (Perfume Lemon)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 78},
            {'code': '01292', 'name': 'Vozol Prime (Pineapple Passion Fruit Lime)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 71},
            {'code': '01298', 'name': 'Vozol Prime (Pomegranate lemonade)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 75},
            {'code': '01286', 'name': 'Vozol Prime (Purple candy)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 87},
            {'code': '01280', 'name': 'Vozol Prime (Sour Apple Ice)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 80},
            {'code': '01279', 'name': 'Vozol Prime (Strawberry Ice cream)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 73},
            {'code': '01293', 'name': 'Vozol Prime (Strawberry Kiwi)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 98},
            {'code': '01297', 'name': 'Vozol Prime (Strawberry Watermelon)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 105},
            {'code': '01281', 'name': 'Vozol Prime (Watermelon Bubble Gum)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 68},
            {'code': '01275', 'name': 'Vozol Prime (Watermelon Ice)', 'category': 'Жидкости', 'subcategory': 'Vozol Prime', 'brand': 'Vozol', 'price': 950, 'stock': 84},
        ]
        
        # ===== POD-СИСТЕМЫ =====
        pods = [
            {'code': '00439', 'name': 'ELFBAR ELFX (Black)', 'category': 'POD-системы', 'subcategory': 'ELF X', 'brand': 'ElfBar', 'price': 1490, 'stock': 118},
            {'code': '01143', 'name': 'ELFBAR ELFX (Blue)', 'category': 'POD-системы', 'subcategory': 'ELF X', 'brand': 'ElfBar', 'price': 1490, 'stock': 70},
            {'code': '00440', 'name': 'ELFBAR ELFX (Gray)', 'category': 'POD-системы', 'subcategory': 'ELF X', 'brand': 'ElfBar', 'price': 1490, 'stock': 14},
            {'code': '01144', 'name': 'ELFBAR ELFX (Pink)', 'category': 'POD-системы', 'subcategory': 'ELF X', 'brand': 'ElfBar', 'price': 1490, 'stock': 7},
            {'code': '01145', 'name': 'ELFBAR ELFX (Purple)', 'category': 'POD-системы', 'subcategory': 'ELF X', 'brand': 'ElfBar', 'price': 1490, 'stock': 11},
            {'code': '00441', 'name': 'ELFBAR ELFX (Silver)', 'category': 'POD-системы', 'subcategory': 'ELF X', 'brand': 'ElfBar', 'price': 1490, 'stock': 3},
            {'code': '00437', 'name': 'ELFBAR ELFX Pod x3 (0.6)', 'category': 'POD-системы', 'subcategory': 'ELF X', 'brand': 'ElfBar', 'price': 590, 'stock': 129},
            {'code': '00438', 'name': 'ELFBAR ELFX Pod x3 (0.8)', 'category': 'POD-системы', 'subcategory': 'ELF X', 'brand': 'ElfBar', 'price': 590, 'stock': 123},
            {'code': '01351', 'name': 'ELFBAR ELFX MINI Kit (Black)', 'category': 'POD-системы', 'subcategory': 'ELF X MINI', 'brand': 'ElfBar', 'price': 1290, 'stock': 45},
            {'code': '01358', 'name': 'ELFBAR ELFX MINI Kit (Gold)', 'category': 'POD-системы', 'subcategory': 'ELF X MINI', 'brand': 'ElfBar', 'price': 1290, 'stock': 6},
            {'code': '01356', 'name': 'ELFBAR ELFX MINI Kit (Lilac)', 'category': 'POD-системы', 'subcategory': 'ELF X MINI', 'brand': 'ElfBar', 'price': 1290, 'stock': 5},
            {'code': '01355', 'name': 'ELFBAR ELFX MINI Kit (Ocean)', 'category': 'POD-системы', 'subcategory': 'ELF X MINI', 'brand': 'ElfBar', 'price': 1290, 'stock': 6},
            {'code': '01354', 'name': 'ELFBAR ELFX MINI Kit (Sky)', 'category': 'POD-системы', 'subcategory': 'ELF X MINI', 'brand': 'ElfBar', 'price': 1290, 'stock': 8},
            {'code': '00095', 'name': 'ELFBAR ELFX PRO (Blue)', 'category': 'POD-системы', 'subcategory': 'ELF X PRO', 'brand': 'ElfBar', 'price': 1690, 'stock': 9},
            {'code': '00096', 'name': 'ELFBAR ELFX PRO (Purple)', 'category': 'POD-системы', 'subcategory': 'ELF X PRO', 'brand': 'ElfBar', 'price': 1690, 'stock': 20},
            {'code': '00098', 'name': 'ELFBAR ELFX PRO (Pink)', 'category': 'POD-системы', 'subcategory': 'ELF X PRO', 'brand': 'ElfBar', 'price': 1690, 'stock': 24},
            {'code': '00945', 'name': 'HQD Cirak (Black)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1290, 'stock': 25},
            {'code': '00946', 'name': 'HQD Cirak (Blue)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1290, 'stock': 8},
            {'code': '00947', 'name': 'HQD Cirak (Gold)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1290, 'stock': 15},
            {'code': '00948', 'name': 'HQD Cirak (Pink)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1290, 'stock': 17},
            {'code': '00949', 'name': 'HQD Cirak (White)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1290, 'stock': 18},
            {'code': '00952', 'name': 'HQD Zest cart 3pcs (0.4)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 450, 'stock': 24},
            {'code': '00953', 'name': 'HQD Zest cart 3pcs (0.8)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 450, 'stock': 30},
            {'code': '00950', 'name': 'HQD Cirak cart 2pcs (0.9)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 390, 'stock': 34},
            {'code': '00951', 'name': 'HQD Cirak cart 2pcs (1.25)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 390, 'stock': 41},
            {'code': '01506', 'name': 'HQD Zest Suit (Blue green)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1190, 'stock': 5},
            {'code': '00940', 'name': 'HQD Zest Suit (Blue pink)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1190, 'stock': 5},
            {'code': '01507', 'name': 'HQD Zest Suit (Green purple)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1190, 'stock': 5},
            {'code': '01508', 'name': 'HQD Zest Suit (Green white)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1190, 'stock': 5},
            {'code': '00942', 'name': 'HQD Zest Suit (Marble green)', 'category': 'POD-системы', 'subcategory': 'HQD', 'brand': 'HQD', 'price': 1190, 'stock': 30},
            {'code': '01589', 'name': 'OXVA Xlim GO 2 (Green Ripple)', 'category': 'POD-системы', 'subcategory': 'OXVA', 'brand': 'OXVA', 'price': 1890, 'stock': 3},
            {'code': '01590', 'name': 'OXVA Xlim GO 2 (Light Brown Shadow)', 'category': 'POD-системы', 'subcategory': 'OXVA', 'brand': 'OXVA', 'price': 1890, 'stock': 8},
            {'code': '01594', 'name': 'OXVA Xlim V3 Cartridge 3pcs (0.4)', 'category': 'POD-системы', 'subcategory': 'OXVA', 'brand': 'OXVA', 'price': 690, 'stock': 6},
            {'code': '01595', 'name': 'OXVA Xlim V3 Cartridge 3pcs (0.6)', 'category': 'POD-системы', 'subcategory': 'OXVA', 'brand': 'OXVA', 'price': 690, 'stock': 2},
            {'code': '01596', 'name': 'OXVA Xlim V3 Cartridge 3pcs (0.8)', 'category': 'POD-системы', 'subcategory': 'OXVA', 'brand': 'OXVA', 'price': 690, 'stock': 5},
            {'code': '01597', 'name': 'OXVA Xlim V3 Cartridge 3pcs (1.2)', 'category': 'POD-системы', 'subcategory': 'OXVA', 'brand': 'OXVA', 'price': 690, 'stock': 12},
            {'code': '00255', 'name': 'Solana Pod Kit (Silver)', 'category': 'POD-системы', 'subcategory': 'SOLANA', 'brand': 'Solana', 'price': 990, 'stock': 18},
            {'code': '00823', 'name': 'VAPORESSO XROS 4 Mini (Black)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2190, 'stock': 3},
            {'code': '00824', 'name': 'VAPORESSO XROS 4 Mini (Camo Red)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2190, 'stock': 3},
            {'code': '00825', 'name': 'VAPORESSO XROS 4 Mini (Camo Silver)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2190, 'stock': 4},
            {'code': '00826', 'name': 'VAPORESSO XROS 4 Mini (Camo Yellow)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2190, 'stock': 4},
            {'code': '00921', 'name': 'VAPORESSO XROS 4 Mini (Champagne Gold)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2190, 'stock': 3},
            {'code': '00827', 'name': 'VAPORESSO XROS 4 Mini (Ice Blue)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2190, 'stock': 4},
            {'code': '00828', 'name': 'VAPORESSO XROS 4 Mini (Ice Green)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2190, 'stock': 3},
            {'code': '00829', 'name': 'VAPORESSO XROS 4 Mini (Ice Purple)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2190, 'stock': 3},
            {'code': '00830', 'name': 'VAPORESSO XROS 4 Mini (Space Gray)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2190, 'stock': 4},
            {'code': '01267', 'name': 'VAPORESSO XROS 5 (Blue Silk)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2490, 'stock': 6},
            {'code': '01338', 'name': 'VAPORESSO XROS 5 (Carbon Stripe)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2490, 'stock': 5},
            {'code': '01339', 'name': 'VAPORESSO XROS 5 (Coral Red)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2490, 'stock': 8},
            {'code': '01269', 'name': 'VAPORESSO XROS 5 (Gray Silk)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2490, 'stock': 2},
            {'code': '01341', 'name': 'VAPORESSO XROS 5 (Jade Green)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2490, 'stock': 4},
            {'code': '01342', 'name': 'VAPORESSO XROS 5 (Lavender purple)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2490, 'stock': 3},
            {'code': '01343', 'name': 'VAPORESSO XROS 5 (Opal Pink)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2490, 'stock': 4},
            {'code': '01270', 'name': 'VAPORESSO XROS 5 (Opal White)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2490, 'stock': 5},
            {'code': '01271', 'name': 'VAPORESSO XROS 5 (Violet Silk)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2490, 'stock': 6},
            {'code': '01309', 'name': 'VAPORESSO XROS 5 MINI (Black)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 6},
            {'code': '01262', 'name': 'VAPORESSO XROS 5 MINI (Carbon Black)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 7},
            {'code': '01263', 'name': 'VAPORESSO XROS 5 MINI (Flowing Blue)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 9},
            {'code': '01264', 'name': 'VAPORESSO XROS 5 MINI (Flowing Green)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 6},
            {'code': '01265', 'name': 'VAPORESSO XROS 5 MINI (Flowing Pink)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 4},
            {'code': '01310', 'name': 'VAPORESSO XROS 5 MINI (Pastel Crystal)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 2},
            {'code': '01311', 'name': 'VAPORESSO XROS 5 MINI (Purple)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 9},
            {'code': '01312', 'name': 'VAPORESSO XROS 5 MINI (Rose Red)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 6},
            {'code': '01266', 'name': 'VAPORESSO XROS 5 MINI (Sky Blue)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 7},
            {'code': '01314', 'name': 'VAPORESSO XROS 5 MINI (Titanium Silver)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2290, 'stock': 4},
            {'code': '01472', 'name': 'VAPORESSO Xros Pro 2 (Dawn Purple)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2690, 'stock': 1},
            {'code': '01473', 'name': 'VAPORESSO Xros Pro 2 (Gem Green)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2690, 'stock': 1},
            {'code': '01475', 'name': 'VAPORESSO Xros Pro 2 (Glittering Gold)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2690, 'stock': 1},
            {'code': '01476', 'name': 'VAPORESSO Xros Pro 2 (Glittering Silver)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2690, 'stock': 3},
            {'code': '01478', 'name': 'VAPORESSO Xros Pro 2 (Storm Blue)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 2690, 'stock': 1},
            {'code': '01484', 'name': 'VAPORESSO VIBE SE (Black)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 4},
            {'code': '01485', 'name': 'VAPORESSO VIBE SE (Blue)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 5},
            {'code': '01486', 'name': 'VAPORESSO VIBE SE (Frozen Mint)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 5},
            {'code': '01488', 'name': 'VAPORESSO VIBE SE (Grapefruit Soda)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 5},
            {'code': '01487', 'name': 'VAPORESSO VIBE SE (Grape Purple)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 5},
            {'code': '01489', 'name': 'VAPORESSO VIBE SE (Ice Blueberry)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 5},
            {'code': '01490', 'name': 'VAPORESSO VIBE SE (Ice Cream Pink)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 5},
            {'code': '01491', 'name': 'VAPORESSO VIBE SE (Mocha Coffee)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 5},
            {'code': '01492', 'name': 'VAPORESSO VIBE SE (Strawberry Red)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 5},
            {'code': '01493', 'name': 'VAPORESSO VIBE SE (White)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 1990, 'stock': 5},
            {'code': '00854', 'name': 'VAPORESSO Cartridge ECO NANO (1.2)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 490, 'stock': 1},
            {'code': '01307', 'name': 'VAPORESSO Cartridge Corex 3.0 (0.6)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 590, 'stock': 23},
            {'code': '01308', 'name': 'VAPORESSO Cartridge Corex 3.0 (0.8)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 590, 'stock': 33},
            {'code': '01495', 'name': 'VAPORESSO VIBE SE CARTRIDGE (0.7/1.0)', 'category': 'POD-системы', 'subcategory': 'VAPORESSO', 'brand': 'Vaporesso', 'price': 490, 'stock': 12},
        ]
        
        # ===== ОДНОРАЗКИ =====
        disposables = [
            {'code': '00275', 'name': 'ELF BAR BC10000 Touch (Mtn Splash)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1590, 'stock': 20},
            {'code': '01519', 'name': 'ELF BAR BC 45000 (Blackberry Lemonade)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 66},
            {'code': '01513', 'name': 'ELF BAR BC 45000 (Blackurrant Grape)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 10},
            {'code': '01510', 'name': 'ELF BAR BC 45000 (Blue Razz Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 63},
            {'code': '01509', 'name': 'ELF BAR BC 45000 (Cherry Peach Soda)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 79},
            {'code': '01511', 'name': 'ELF BAR BC 45000 (Double Mint)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 39},
            {'code': '01520', 'name': 'ELF BAR BC 45000 (Grapefruit Green Tea)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 11},
            {'code': '01522', 'name': 'ELF BAR BC 45000 (Kiwi Pineapple Peach)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 43},
            {'code': '01514', 'name': 'ELF BAR BC 45000 (Lemon Lime)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 34},
            {'code': '01512', 'name': 'ELF BAR BC 45000 (Pear Soda)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 73},
            {'code': '01517', 'name': 'ELF BAR BC 45000 (Pomegranate Raspberry Lime)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 62},
            {'code': '01516', 'name': 'ELF BAR BC 45000 (Red Raspberry Strawberry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 10},
            {'code': '01523', 'name': 'ELF BAR BC 45000 (Sour Apple Kiwi)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 10},
            {'code': '01524', 'name': 'ELF BAR BC 45000 (Strawberry Grapefruit)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 9},
            {'code': '01515', 'name': 'ELF BAR BC 45000 (Watermelon Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2290, 'stock': 55},
            {'code': '01598', 'name': 'EBCREATE BC PRO 40000 (Aurora Berries)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 46},
            {'code': '01600', 'name': 'EBCREATE BC PRO 40000 (Blackberry Grape)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 50},
            {'code': '01599', 'name': 'EBCREATE BC PRO 40000 (Black Mint)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 64},
            {'code': '01601', 'name': 'EBCREATE BC PRO 40000 (Blue Razz Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 49},
            {'code': '01602', 'name': 'EBCREATE BC PRO 40000 (Grape Twist)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 60},
            {'code': '01603', 'name': 'EBCREATE BC PRO 40000 (Pineapple POM)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 64},
            {'code': '01604', 'name': 'EBCREATE BC PRO 40000 (Sour Apple Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 54},
            {'code': '01605', 'name': 'EBCREATE BC PRO 40000 (Sour Fcuking Fab)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 47},
            {'code': '01606', 'name': 'EBCREATE BC PRO 40000 (Strawberry Blend)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 66},
            {'code': '01607', 'name': 'EBCREATE BC PRO 40000 (Strawberry Kiwi)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 61},
            {'code': '01608', 'name': 'EBCREATE BC PRO 40000 (Strawberry Raspberry Frost)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 61},
            {'code': '01609', 'name': 'EBCREATE BC PRO 40000 (Toasted Pineapple)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 55},
            {'code': '01610', 'name': 'EBCREATE BC PRO 40000 (Triple Berry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 45},
            {'code': '01611', 'name': 'EBCREATE BC PRO 40000 (Watermelon Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 56},
            {'code': '01612', 'name': 'EBCREATE BC PRO 40000 (Watermelon Peach Frost)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 66},
            {'code': '01613', 'name': 'EBCREATE BC PRO 40000 (Winter Mint)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2190, 'stock': 68},
            {'code': '01261', 'name': 'ELF BAR GH 33000 PRO (Apple Kiwi Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 37},
            {'code': '01250', 'name': 'ELF BAR GH 33000 PRO (Blue Razz Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 64},
            {'code': '01258', 'name': 'ELF BAR GH 33000 PRO (Cherry Pomegranate Pineapple)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 58},
            {'code': '01247', 'name': 'ELF BAR GH 33000 PRO (Granny Cherry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 60},
            {'code': '01249', 'name': 'ELF BAR GH 33000 PRO (Grapefruit Passion Guava)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 52},
            {'code': '01248', 'name': 'ELF BAR GH 33000 PRO (Grape Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 61},
            {'code': '01253', 'name': 'ELF BAR GH 33000 PRO (Kiwi Pineapple Peach)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 43},
            {'code': '01259', 'name': 'ELF BAR GH 33000 PRO (Lemon Lime)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 42},
            {'code': '01251', 'name': 'ELF BAR GH 33000 PRO (Mountain Mint)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 51},
            {'code': '01252', 'name': 'ELF BAR GH 33000 PRO (Pear Soda)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 69},
            {'code': '01260', 'name': 'ELF BAR GH 33000 PRO (Pine Needles)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 76},
            {'code': '01256', 'name': 'ELF BAR GH 33000 PRO (Pomegranate Burst)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 67},
            {'code': '01254', 'name': 'ELF BAR GH 33000 PRO (Raspberry Grapefruit Lemon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 63},
            {'code': '01257', 'name': 'ELF BAR GH 33000 PRO (Sour Strawberry Dragonfruit)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 79},
            {'code': '01255', 'name': 'ELF BAR GH 33000 PRO (Watermelon Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 60},
            {'code': '00924', 'name': 'ELF BAR ICE KING 30000 (Banana Cake)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 33},
            {'code': '00925', 'name': 'ELF BAR ICE KING 30000 (Blackberry Cranberry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 35},
            {'code': '00926', 'name': 'ELF BAR ICE KING 30000 (Blue Razz Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 31},
            {'code': '00927', 'name': 'ELF BAR ICE KING 30000 (Cherry Pomegranate Cranberry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 31},
            {'code': '00928', 'name': 'ELF BAR ICE KING 30000 (ELF BULL)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 41},
            {'code': '00929', 'name': 'ELF BAR ICE KING 30000 (Grape Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 33},
            {'code': '00930', 'name': 'ELF BAR ICE KING 30000 (Kiwi Passion Fruit Guava)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 33},
            {'code': '00931', 'name': 'ELF BAR ICE KING 30000 (Lime Cola)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 33},
            {'code': '00932', 'name': 'ELF BAR ICE KING 30000 (Miami Mint)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 26},
            {'code': '00933', 'name': 'ELF BAR ICE KING 30000 (Peach Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 31},
            {'code': '00934', 'name': 'ELF BAR ICE KING 30000 (Pink Lemonade)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 34},
            {'code': '00935', 'name': 'ELF BAR ICE KING 30000 (Ribena Lychee)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 33},
            {'code': '00937', 'name': 'ELF BAR ICE KING 30000 (Strawberry kiwi Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 35},
            {'code': '00936', 'name': 'ELF BAR ICE KING 30000 (Strawberry Watermelon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 48},
            {'code': '00938', 'name': 'ELF BAR ICE KING 30000 (Watermelon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1890, 'stock': 64},
            {'code': '01228', 'name': 'VOZOL RAVE 40000 (Blueberry Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 10},
            {'code': '01214', 'name': 'VOZOL RAVE 40000 (Blue Razz Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 38},
            {'code': '01232', 'name': 'VOZOL RAVE 40000 (Cool Mint)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 3},
            {'code': '01233', 'name': 'VOZOL RAVE 40000 (Double Apple)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 9},
            {'code': '01234', 'name': 'VOZOL RAVE 40000 (Grape Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 8},
            {'code': '01223', 'name': 'VOZOL RAVE 40000 (Peach Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 18},
            {'code': '01236', 'name': 'VOZOL RAVE 40000 (Strawberry Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 26},
            {'code': '01315', 'name': 'VOZOL RAVE 40000 (Strawberry Mango)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 10},
            {'code': '01238', 'name': 'VOZOL RAVE 40000 (Strawberry Watermelon)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 9},
            {'code': '01245', 'name': 'VOZOL RAVE 40000 (Strawmelon Peach)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 43},
            {'code': '01226', 'name': 'VOZOL RAVE 40000 (Watermelon Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2090, 'stock': 22},
            {'code': '01325', 'name': 'VOZOL Vista 40000 (Blueberry Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 27},
            {'code': '01328', 'name': 'VOZOL Vista 40000 (Blue Razz Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 15},
            {'code': '01331', 'name': 'VOZOL Vista 40000 (Cherry Cola)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 13},
            {'code': '01329', 'name': 'VOZOL Vista 40000 (Double Apple)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 21},
            {'code': '01377', 'name': 'VOZOL Vista 40000 (Frozen Strawberry Kiwi)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 25},
            {'code': '01323', 'name': 'VOZOL Vista 40000 (Grape Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 10},
            {'code': '01324', 'name': 'VOZOL Vista 40000 (Juicy Peach)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 41},
            {'code': '01336', 'name': 'VOZOL Vista 40000 (Lychee Orange Passion Fruit)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 18},
            {'code': '01332', 'name': 'VOZOL Vista 40000 (Melon Gum)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 25},
            {'code': '01334', 'name': 'VOZOL Vista 40000 (Peach Berry)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 22},
            {'code': '01378', 'name': 'VOZOL Vista 40000 (Strawberry Banana)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 31},
            {'code': '01327', 'name': 'VOZOL Vista 40000 (Strawberry Watermelon)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 27},
            {'code': '01326', 'name': 'VOZOL Vista 40000 (Watermelon Bubblegum)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 33},
            {'code': '01337', 'name': 'VOZOL Vista 40000 (Watermelon Ice)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2190, 'stock': 50},
            {'code': '01541', 'name': 'VOZOL GEAR 50000 (Black raspberry smoothie)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2390, 'stock': 33},
            {'code': '01546', 'name': 'VOZOL GEAR 50000 (Cherry Cola)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2390, 'stock': 59},
            {'code': '01565', 'name': 'VOZOL GEAR 50000 (Super Mint)', 'category': 'Одноразки', 'subcategory': 'VOZOL', 'brand': 'Vozol', 'price': 2390, 'stock': 71},
            {'code': '00908', 'name': 'RAYA D3 25000 (Apple Peach)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 57},
            {'code': '00905', 'name': 'RAYA D3 25000 (Blackberry Cranberry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 53},
            {'code': '00450', 'name': 'RAYA D3 25000 (Blueberry ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 53},
            {'code': '00449', 'name': 'RAYA D3 25000 (Blueberry Raspberry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 45},
            {'code': '00907', 'name': 'RAYA D3 25000 (Blue Razz Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 64},
            {'code': '00451', 'name': 'RAYA D3 25000 (Double Apple)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 52},
            {'code': '00453', 'name': 'RAYA D3 25000 (Grape Cherry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 59},
            {'code': '00454', 'name': 'RAYA D3 25000 (Grape Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 38},
            {'code': '00916', 'name': 'RAYA D3 25000 (Grape Mint)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 35},
            {'code': '00632', 'name': 'RAYA D3 25000 (Kiwi Passion Fruit Guava)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 65},
            {'code': '00915', 'name': 'RAYA D3 25000 (Lemon Lime lce)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 64},
            {'code': '00635', 'name': 'RAYA D3 25000 (Peach Berry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 57},
            {'code': '00458', 'name': 'RAYA D3 25000 (Peach Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 35},
            {'code': '00459', 'name': 'RAYA D3 25000 (Strawberry Grape)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 36},
            {'code': '00909', 'name': 'RAYA D3 25000 (Strawberry lce)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 49},
            {'code': '00903', 'name': 'RAYA D3 25000 (Strawberry Raspberry Cherry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 33},
            {'code': '00904', 'name': 'RAYA D3 25000 (Strawberry Watermelon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 53},
            {'code': '00633', 'name': 'RAYA D3 25000 (Vimto)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 46},
            {'code': '00460', 'name': 'RAYA D3 25000 (Watermelon Bubble Gum)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 36},
            {'code': '00462', 'name': 'RAYA D3 25000 (Watermelon ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 45},
            {'code': '00461', 'name': 'RAYA D3 25000 (Watermelon Lemon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1690, 'stock': 65},
            {'code': '00037', 'name': 'ELF BAR RI3000 (Grape Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 690, 'stock': 6},
            {'code': '00040', 'name': 'ELF BAR RI3000 (Strawberry Banana)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 690, 'stock': 2},
            {'code': '00042', 'name': 'ELF BAR RI3000 (Watermelon Coconut Water)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 690, 'stock': 33},
            {'code': '00043', 'name': 'ELF BAR RI3000 (Watermelon Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 690, 'stock': 28},
            {'code': '00044', 'name': 'ELF BAR RI3000 (Watermelon Kiwi Berry Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 690, 'stock': 22},
            {'code': '01360', 'name': 'Lush King Pro 40000 (Black Currant Pineapple)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 11},
            {'code': '01372', 'name': 'Lush King Pro 40000 (Black Grape Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 5},
            {'code': '01373', 'name': 'Lush King Pro 40000 (Blue Razz Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 5},
            {'code': '01364', 'name': 'Lush King Pro 40000 (Cactus Lime)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 6},
            {'code': '01365', 'name': 'Lush King Pro 40000 (Cherry Burst)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 36},
            {'code': '01362', 'name': 'Lush King Pro 40000 (Cucumber Lime)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 28},
            {'code': '01361', 'name': 'Lush King Pro 40000 (Milky Oolong)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 98},
            {'code': '01366', 'name': 'Lush King Pro 40000 (Mountain Mint)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 40},
            {'code': '01370', 'name': 'Lush King Pro 40000 (Pomegranate Burst)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 6},
            {'code': '01371', 'name': 'Lush King Pro 40000 (Sour Apple Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 13},
            {'code': '01367', 'name': 'Lush King Pro 40000 (Sour Pineapple ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 10},
            {'code': '01369', 'name': 'Lush King Pro 40000 (Sour Strawberry Dragonfruit)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 6},
            {'code': '01109', 'name': 'MoonNight 40000 (Blue razz ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 10},
            {'code': '01110', 'name': 'MoonNight 40000 (Cheery watermelon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 10},
            {'code': '01112', 'name': 'MoonNight 40000 (Grape ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 12},
            {'code': '01111', 'name': 'MoonNight 40000 (Grape Raspberry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 10},
            {'code': '01113', 'name': 'MoonNight 40000 (Kiwi Passion Fruite Guava)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 10},
            {'code': '01114', 'name': 'MoonNight 40000 (Lemon Lime)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 45},
            {'code': '01115', 'name': 'MoonNight 40000 (Lime Cola)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 10},
            {'code': '01116', 'name': 'MoonNight 40000 (Mango peach watermelon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 10},
            {'code': '01117', 'name': 'MoonNight 40000 (Miami mint)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 35},
            {'code': '01118', 'name': 'MoonNight 40000 (Peach ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 10},
            {'code': '01119', 'name': 'MoonNight 40000 (Pomegranate Burst)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 12},
            {'code': '01120', 'name': 'MoonNight 40000 (Watermelon Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1990, 'stock': 10},
            {'code': '01075', 'name': 'Nic King (Blue razz ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 44},
            {'code': '01076', 'name': 'Nic King (Chilly River)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 45},
            {'code': '01077', 'name': 'Nic King (Grape Cranberry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 48},
            {'code': '01078', 'name': 'Nic King (Grapefruit Green Tea)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 38},
            {'code': '01079', 'name': 'Nic King (Icy Blue Rose)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 42},
            {'code': '01080', 'name': 'Nic King (Key Lime)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 44},
            {'code': '01081', 'name': 'Nic King (Lemon Lime Ice Tea)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 40},
            {'code': '01082', 'name': 'Nic King (Pear Soda)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 37},
            {'code': '01083', 'name': 'Nic King (Pineapple Dragonfruit Grapefruit)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 39},
            {'code': '01084', 'name': 'Nic King (Pomegranate Burst)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 46},
            {'code': '01085', 'name': 'Nic King (Sour Apple Watermelon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 36},
            {'code': '01086', 'name': 'Nic King (Sour Cherry Candy)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 38},
            {'code': '01087', 'name': 'Nic King (Sour Strawberry Dragonfruit)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 38},
            {'code': '01088', 'name': 'Nic King (Watermelon Cherry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 42},
            {'code': '01089', 'name': 'Nic King (Watermelon Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 36},
            {'code': '01090', 'name': 'Sour King (Lemon Lime Ice Tea)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 97},
            {'code': '01091', 'name': 'Sour King (Red Raspberry Strawberry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 56},
            {'code': '01092', 'name': 'Sour King (Sour Apple Candy)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 76},
            {'code': '01093', 'name': 'Sour King (Sour Apple Pear)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 88},
            {'code': '01094', 'name': 'Sour King (Sour Blueberry Watermelon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 61},
            {'code': '01095', 'name': 'Sour King (Sour Kiwi Lemonade)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 54},
            {'code': '01096', 'name': 'Sour King (Sour Strawberry Kiwi)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 65},
            {'code': '01097', 'name': 'Sour King (Sour Triple Berry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 59},
            {'code': '01098', 'name': 'Sweet King (Apple Watermelon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 20},
            {'code': '01099', 'name': 'Sweet King (Grape ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 4},
            {'code': '01100', 'name': 'Sweet King (Jasmine Raspberry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 44},
            {'code': '01101', 'name': 'Sweet King (Kiwi Pineapple Peach)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 48},
            {'code': '01102', 'name': 'Sweet King (Pear Soda)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 68},
            {'code': '01103', 'name': 'Sweet King (Pine Needle Mint)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 67},
            {'code': '01105', 'name': 'Sweet King (Watermelon Cherry)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 1790, 'stock': 33},
            {'code': '01496', 'name': 'TRIO 40000 (Cool Menthol)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 56},
            {'code': '01497', 'name': 'TRIO 40000 (LA Grape)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 52},
            {'code': '01498', 'name': 'TRIO 40000 (Peach Twist)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 51},
            {'code': '01499', 'name': 'TRIO 40000 (Pineapple Lime)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 50},
            {'code': '01500', 'name': 'TRIO 40000 (Pomegranate Blast)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 45},
            {'code': '01501', 'name': 'TRIO 40000 (Raspberry Watermelon)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 40},
            {'code': '01502', 'name': 'TRIO 40000 (Sakura Grape)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 40},
            {'code': '01503', 'name': 'TRIO 40000 (Sour Apple Ice)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 48},
            {'code': '01504', 'name': 'TRIO 40000 (Sour Strawberry Dragonfruit)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 40},
            {'code': '01505', 'name': 'TRIO 40000 (Strawberry Orange Lime)', 'category': 'Одноразки', 'subcategory': 'ELF BAR', 'brand': 'ElfBar', 'price': 2090, 'stock': 48},
        ]
        
        # ===== СКИДОЧНЫЕ =====
        discount = [
            {'code': '01447', 'name': 'Funky Monkey (Contis)', 'category': 'Скидочные', 'subcategory': 'Funky Monkey', 'brand': 'Funky Monkey', 'price': 590, 'stock': 28},
            {'code': '01414', 'name': 'JooYoo 10k 5% (Blueberry raspberry)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 8},
            {'code': '01417', 'name': 'JooYoo 10k 5% (Blue razz)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 8},
            {'code': '01423', 'name': 'JooYoo 10k 5% (Cherry ice)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01416', 'name': 'JooYoo 10k 5% (Clear)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01422', 'name': 'JooYoo 10k 5% (Grape ice)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01429', 'name': 'JooYoo 10k 5% (Kiwi passion fruit guava)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 7},
            {'code': '01427', 'name': 'JooYoo 10k 5% (lemon tart)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 8},
            {'code': '01428', 'name': 'JooYoo 10k 5% (Mint ice)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 8},
            {'code': '01419', 'name': 'JooYoo 10k 5% (Mojito)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 7},
            {'code': '01418', 'name': 'JooYoo 10k 5% (OAT milk puding)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 7},
            {'code': '01420', 'name': 'JooYoo 10k 5% (Peach ice)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01421', 'name': 'JooYoo 10k 5% (Pineapple cocounut)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01415', 'name': 'JooYoo 10k 5% (Pineapple mango peach)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01426', 'name': 'JooYoo 10k 5% (Rut bear)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01424', 'name': 'JooYoo 10k 5% (Strawberry ice)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01430', 'name': 'JooYoo 10k 5% (Strawberry kiwi)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01425', 'name': 'JooYoo 10k 5% (Watermelon ice)', 'category': 'Скидочные', 'subcategory': 'JooYoo', 'brand': 'JooYoo', 'price': 690, 'stock': 9},
            {'code': '01446', 'name': 'SnoopySmoke 15k 5% (Bahama mama)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 14},
            {'code': '01434', 'name': 'SnoopySmoke 15k 5% (Blue razz ice)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 15},
            {'code': '01441', 'name': 'SnoopySmoke 15k 5% (Cool Mint)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 16},
            {'code': '01433', 'name': 'SnoopySmoke 15k 5% (Grape ice)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 15},
            {'code': '01432', 'name': 'SnoopySmoke 15k 5% (Luch ice)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 18},
            {'code': '01435', 'name': 'SnoopySmoke 15k 5% (Mexican mango ice)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 19},
            {'code': '01437', 'name': 'SnoopySmoke 15k 5% (Pina colada)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 27},
            {'code': '01436', 'name': 'SnoopySmoke 15k 5% (Pineapple ice)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 29},
            {'code': '01445', 'name': 'SnoopySmoke 15k 5% (Red Juice)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 16},
            {'code': '01442', 'name': 'SnoopySmoke 15k 5% (Strawberry banana)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 15},
            {'code': '01439', 'name': 'SnoopySmoke 15k 5% (Strawberry ice)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 18},
            {'code': '01440', 'name': 'SnoopySmoke 15k 5% (Strawberry kiwi)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 16},
            {'code': '01431', 'name': 'SnoopySmoke 15k 5% (Tripple Berry ice)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 17},
            {'code': '01438', 'name': 'SnoopySmoke 15k 5% (Tropical rainbow blast)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 14},
            {'code': '01443', 'name': 'SnoopySmoke 15k 5% (Watermelon ice)', 'category': 'Скидочные', 'subcategory': 'SnoopySmoke', 'brand': 'SnoopySmoke', 'price': 790, 'stock': 16},
            {'code': '01408', 'name': 'YOCCO 12k 5% (California Cherry)', 'category': 'Скидочные', 'subcategory': 'YOCCO', 'brand': 'YOCCO', 'price': 750, 'stock': 21},
            {'code': '01413', 'name': 'YOCCO 12k 5% (Miami mint)', 'category': 'Скидочные', 'subcategory': 'YOCCO', 'brand': 'YOCCO', 'price': 750, 'stock': 23},
            {'code': '01406', 'name': 'YOCCO 12k 5% (Stawnana)', 'category': 'Скидочные', 'subcategory': 'YOCCO', 'brand': 'YOCCO', 'price': 750, 'stock': 23},
            {'code': '01411', 'name': 'YOCCO 12k 5% (Strawkiwi)', 'category': 'Скидочные', 'subcategory': 'YOCCO', 'brand': 'YOCCO', 'price': 750, 'stock': 24},
            {'code': '01410', 'name': 'YOCCO 12k 5% (Strawmelon)', 'category': 'Скидочные', 'subcategory': 'YOCCO', 'brand': 'YOCCO', 'price': 750, 'stock': 25},
            {'code': '01407', 'name': 'YOCCO 12k 5% (Watermelon ice)', 'category': 'Скидочные', 'subcategory': 'YOCCO', 'brand': 'YOCCO', 'price': 750, 'stock': 25},
            {'code': '01412', 'name': 'YOCCO 12k 5% (Yammy gummy)', 'category': 'Скидочные', 'subcategory': 'YOCCO', 'brand': 'YOCCO', 'price': 750, 'stock': 25},
            {'code': '01388', 'name': 'BLK 10k 2% (Blueberry cherry crangberry)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 8},
            {'code': '01400', 'name': 'BLK 10k 2% (Blueberry raspberry blackberry)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 12},
            {'code': '01386', 'name': 'BLK 10k 2% (Blueberry Raspberry ice)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 13},
            {'code': '01391', 'name': 'BLK 10k 2% (Blueberry sour raspberry)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 13},
            {'code': '01390', 'name': 'BLK 10k 2% (Cherry ice)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 14},
            {'code': '01405', 'name': 'BLK 10k 2% (Cherry Peach Lemonade)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 12},
            {'code': '01395', 'name': 'BLK 10k 2% (Fizzy cherry)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 13},
            {'code': '01385', 'name': 'BLK 10k 2% (Fresh Mint)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 23},
            {'code': '01394', 'name': 'BLK 10k 2% (Gummy bear)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 22},
            {'code': '01396', 'name': 'BLK 10k 2% (Ice pop)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 23},
            {'code': '01393', 'name': 'BLK 10k 2% (Lemon Lime)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 24},
            {'code': '01403', 'name': 'BLK 10k 2% (Mango passion fruit mojito)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 11},
            {'code': '01381', 'name': 'BLK 10k 2% (Monster)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 13},
            {'code': '01384', 'name': 'BLK 10k 2% (Mr black)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 12},
            {'code': '01380', 'name': 'BLK 10k 2% (Mr Blue)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 23},
            {'code': '01399', 'name': 'BLK 10k 2% (Oasis)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 14},
            {'code': '01382', 'name': 'BLK 10k 2% (Pineapple ice)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 24},
            {'code': '01404', 'name': 'BLK 10k 2% (Pineapple mango guava)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 20},
            {'code': '01402', 'name': 'BLK 10k 2% (Rhubarb Raspberry Orange)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 23},
            {'code': '01389', 'name': 'BLK 10k 2% (Skittles)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 20},
            {'code': '01392', 'name': 'BLK 10k 2% (Sommer beries)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 21},
            {'code': '01387', 'name': 'BLK 10k 2% (Strawberry kiwi watermelon)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 9},
            {'code': '01398', 'name': 'BLK 10k 2% (Strawberry raspberry)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 24},
            {'code': '01397', 'name': 'BLK 10k 2% (Strawberry raspberry cherry ice)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 24},
            {'code': '01383', 'name': 'BLK 10k 2% (Tripple mango)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 24},
            {'code': '01401', 'name': 'BLK 10k 2% (Watermelon ice)', 'category': 'Скидочные', 'subcategory': 'BLK', 'brand': 'BLK', 'price': 590, 'stock': 19},
        ]
        
        return liquids + pods + disposables + discount
    
    def get_categories(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categories ORDER BY sort_order')
        categories = [{"id": c[0], "name": c[1], "icon": c[2], "sort_order": c[3]} for c in cursor.fetchall()]
        conn.close()
        return categories
    
    def get_products(self, category: Optional[str] = None, subcategory: Optional[str] = None, search: Optional[str] = None) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM products WHERE is_active = 1'
        params = []
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        if subcategory:
            query += ' AND subcategory = ?'
            params.append(subcategory)
        if search:
            query += ' AND (name LIKE ? OR code LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += ' ORDER BY name'
        cursor.execute(query, params)
        
        products = [{
            "id": p[0], "code": p[1], "name": p[2], "category": p[3],
            "subcategory": p[4], "brand": p[5], "price": p[6],
            "stock": p[7], "is_active": p[8]
        } for p in cursor.fetchall()]
        
        conn.close()
        return products
    
    def get_subcategories(self, category: str) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT subcategory FROM products WHERE category = ? AND is_active = 1 ORDER BY subcategory', (category,))
        subcategories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return subcategories
    
    def create_order(self, user_id: int, username: str, full_name: str, products: list, total: float) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (user_id, username, full_name, products_json, total_amount) VALUES (?, ?, ?, ?, ?)',
                      (user_id, username, full_name, json.dumps(products), total))
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return order_id
    
    def get_stats(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM products WHERE is_active = 1')
        total_products = cursor.fetchone()[0]
        conn.close()
        return {"total_products": total_products}

db = Database()