from flask import Flask, request, jsonify, g
import sqlite3
from database_operations import execute_query, insert_data, update_data, delete_data, select_data

app = Flask(__name__)

DATABASE_PATH = 'identifier.sqlite.db'

# Самописний менеджер контексту
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Обробка реєстрації користувача
@app.route('/register', methods=['POST'])
def register():

    return "User registered successfully"

@app.route('/login', methods=['POST'])
def login():
    # Обробка входу користувача
    return "User logged in successfully"

@app.route('/shop/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    # Отримати інформацію про товар з бази даних за item_id
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM items WHERE items.item_id=?", (item_id,))
    item = cursor.fetchone()
    my_db.close()

    if item:
        return str(item)
    else:
        return "Item not found"

@app.route('/shop/items/<int:item_id>/review', methods=['POST'])
def post_review(item_id):
    # Отримати дані про відгук з запиту та зберегти їх у базі даних
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    cursor.execute("INSERT INTO review (item_id, text, rating) VALUES (?, ?, ?)",
                   (item_id, request.form['text'], request.form['rating']))
    my_db.commit()
    my_db.close()
    return "Review posted successfully"

@app.route('/shop/items/<int:item_id>/review', methods=['GET'])
def get_reviews(item_id):
    # Отримати список відгуків для товару з бази даних за item_id
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM review WHERE item_id=?", (item_id,))
    reviews = cursor.fetchall()
    my_db.close()
    return str(reviews)

@app.route('/shop/items/<int:item_id>/review/<int:review_id>', methods=['GET'])
def get_review(item_id, review_id):
    # Отримати конкретний відгук за item_id та review_id з бази даних
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM review WHERE item_id=? AND review_id=?", (item_id, review_id))
    review = cursor.fetchone()
    my_db.close()
    if review:
        return str(review)
    else:
        return "Review not found"

@app.route('/shop/items/<int:item_id>/review/<int:review_id>', methods=['PUT'])
def update_review(item_id, review_id):
    # Отримати дані для оновлення відгуку з запиту та оновити їх у базі даних
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    cursor.execute("UPDATE review SET text=?, rating=? WHERE item_id=? AND review_id=?",
                   (request.form['text'], request.form['rating'], item_id, review_id))
    my_db.commit()
    my_db.close()
    return "Review updated successfully"

@app.route('/shop/items', methods=['GET'])
def get_items():
    # Отримати параметри запиту для фільтрації, сортування та розбивки за сторінками
    category = request.args.get('category', type=int)
    order = request.args.get('order', default='price', type=str)
    page = request.args.get('page', default=1, type=int)

    # Логіка для вибору товарів з бази даних за заданими параметрами
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    items = [{"item_id": 1, "name": "Product 1", "price": 19.99},
             {"item_id": 2, "name": "Product 2", "price": 29.99}]
    my_db.close()
    return str(items)

@app.route('/shop/search', methods=['POST'])
def search_items():
    # Отримати дані для пошуку з тіла запиту
    data = request.json
    search_query = data.get('search_query')
    # Логіка для пошуку товарів за заданим запитом у базі даних
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    items = [{"item_id": 1, "name": "Product 1", "price": 19.99},
             {"item_id": 2, "name": "Product 2", "price": 29.99}]
    my_db.close()
    return str(items)

@app.route('/shop/cart', methods=['GET'])
def get_cart():
    # Логіка отримання вмісту корзини з бази даних або іншого джерела
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    cart_items = [{"item_id": 1, "name": "Product 1", "amount": 2},
                  {"item_id": 2, "name": "Product 2", "amount": 1}]
    my_db.close()
    return str(cart_items)

@app.route('/shop/cart', methods=['POST', 'PUT'])
def update_cart():
    # Отримати дані для оновлення корзини з параметрів запиту
    item_id = request.args.get('item_id', type=int)
    amount = request.args.get('amount', type=int)
    # Логіка для додавання чи оновлення товару у корзині в базі даних
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    cursor.execute("UPDATE cart SET quantity=? WHERE item_id=?", (amount, item_id))
    my_db.commit()
    my_db.close()
    return jsonify({"message": f"Item {item_id} added/updated in the cart successfully"})

@app.route('/shop/cart', methods=['DELETE'])
def delete_item_from_cart():
    # Отримати ідентифікатор товару для видалення з параметрів запиту
    item_id_to_delete = request.args.get('item_id', type=int)
    # Логіка для видалення товару з корзини в базі даних
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    cursor.execute("DELETE FROM cart WHERE item_id=?", (item_id_to_delete,))
    my_db.commit()
    my_db.close()
    return jsonify({"message": f"Item {item_id_to_delete} removed from the cart successfully"})

@app.route('/shop/cart/order', methods=['GET'])
def fill_order_form():
    # Логіка для отримання даних для оформлення замовлення (форми)
    # Повернути результат у форматі JSON
    return jsonify({"message": "Provide shipping details and payment information"})

@app.route('/shop/cart/order', methods=['POST'])
def place_order():
    # Отримати дані для оформлення замовлення з тіла запиту
    data = request.json
    # Логіка для збереження даних замовлення в базі даних
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    my_db.commit()
    my_db.close()
    return jsonify({"message": "Order placed successfully"})

@app.route('/shop/favorites/<int:list_id>', methods=['GET'])
def get_favorite_list(list_id):
    # Логіка отримання вмісту списку улюблених товарів за list_id
    my_db = sqlite3.connect('identifier.sqlite')
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM favorites WHERE list_id=?", (list_id,))
    favorite_items = cursor.fetchall()
    my_db.close()
    return jsonify({"list_id": list_id, "favorites": favorite_items})

# shop/favorites/<list_id> [PUT]
@app.route('/shop/favorites/<int:list_id>', methods=['PUT'])
def update_favorite_list(list_id):
    # Отримати дані для оновлення списку улюблених товарів з тіла запиту
    data = request.json
    updated_favorite_items = data.get('favorites', [])
    # Підключення до бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    # Закриття підключення до бази даних
    connection.close()
    return jsonify({"message": f"Favorite list {list_id} updated successfully", "favorites": updated_favorite_items})


# shop/favorites [POST]
@app.route('/shop/favorites', methods=['POST'])
def create_favorite_list():
    # Отримати дані для створення нового списку улюблених товарів з тіла запиту
    data = request.json
    new_favorite_items = data.get('favorites', [])
    # Підключення до бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    # Закриття підключення до бази даних
    connection.close()

    return jsonify({"message": "New favorite list created successfully", "favorites": new_favorite_items})


# shop/waitlist [GET]
@app.route('/shop/waitlist', methods=['GET'])
def get_waitlist():
    # Підключення до бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    # Закриття підключення до бази даних
    connection.close()
    return jsonify({"waitlist"})

# shop/waitlist [PUT]
@app.route('/shop/waitlist', methods=['PUT'])
def update_waitlist():
    # Отримати дані для оновлення списку очікування з тіла запиту
    data = request.json
    updated_waitlist_items = data.get('waitlist', [])
    # Підключення до бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    # Закриття підключення до бази даних
    connection.close()
    return jsonify({"message": "Waitlist updated successfully", "waitlist": updated_waitlist_items})


# admin/items [POST]
@app.route('/admin/items', methods=['POST'])
def create_item():
    # Отримати дані для створення нового товару з тіла запиту
    request.json()
    # Підключення до бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    # Закриття підключення до бази даних
    connection.close()
    return jsonify({"message": "New item created successfully"})

# shop/favorites/<list_id> [PUT]
@app.route('/shop/favorites/<int:list_id>', methods=['PUT'])
def update_favorite_list(list_id):
    # Отримати дані для оновлення списку улюблених товарів з тіла запиту
    data = request.json
    updated_favorite_items = data.get('favorites', [])
    # Підключення до бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    # Логіка для оновлення списку улюблених товарів в базі даних
    cursor.execute("UPDATE favorites SET items = ? WHERE list_id = ?", (str(updated_favorite_items), list_id))
    connection.commit()
    # Закриття підключення до бази даних
    connection.close()
    return jsonify({"message": f"Favorite list {list_id} updated successfully", "favorites": updated_favorite_items})


# shop/favorites [POST]
@app.route('/shop/favorites', methods=['POST'])
def create_favorite_list():
    # Отримати дані для створення нового списку улюблених товарів з тіла запиту
    data = request.json
    new_favorite_items = data.get('favorites', [])
    # Підключення до бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    # Логіка для створення нового списку улюблених товарів в базі даних
    cursor.execute("INSERT INTO favorites (items) VALUES (?)", (str(new_favorite_items),))
    connection.commit()
    # Закриття підключення до бази даних
    connection.close()
    return jsonify({"message": "New favorite list created successfully", "favorites": new_favorite_items})


# shop/waitlist [GET]
@app.route('/shop/waitlist', methods=['GET'])
def get_waitlist():
    # Підключення до бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    # Логіка отримання вмісту списку очікування
    cursor.execute("SELECT * FROM waitlist")
    waitlist_items = cursor.fetchall()
    # Закриття підключення до бази даних
    connection.close()
    return jsonify({"waitlist": waitlist_items})


# shop/waitlist [PUT]
@app.route('/shop/waitlist', methods=['PUT'])
def update_waitlist():
    # Отримати дані для оновлення списку очікування з тіла запиту
    data = request.json
    updated_waitlist_items = data.get('waitlist', [])
    # Підключення до бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    # Логіка для оновлення списку очікування в базі даних
    cursor.execute("UPDATE waitlist SET item_id = ?", (str(updated_waitlist_items),))
    connection


app = Flask(__name__)

# admin/items [POST]
@app.route('/admin/items', methods=['POST'])
def create_item():
    # Отримати дані для створення нового товару з тіла запиту
    data = request.json
    # Логіка для створення нового товару в базі даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO items (name, description, price) VALUES (?, ?, ?)",
                   (data.get('name'), data.get('description'), data.get('price')))
    connection.commit()
    connection.close()
    return jsonify({"message": "New item created successfully"})


# admin/items [GET]
@app.route('/admin/items', methods=['GET'])
def get_all_items():
    # Логіка отримання всіх товарів з бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    connection.close()
    return jsonify({"items": items})


# admin/items/<id> [PUT]
@app.route('/admin/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    # Отримати дані для оновлення товару з тіла запиту
    data = request.json
    # Логіка для оновлення товару в базі даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("UPDATE items SET name = ?, description = ?, price = ? WHERE item_id = ?",
                   (data.get('name'), data.get('description'), data.get('price'), item_id))
    connection.commit()
    connection.close()
    return jsonify({"message": f"Item {item_id} updated successfully"})


# admin/items/<id> [GET]
@app.route('/admin/items/<int:item_id>', methods=['GET'])
def get_item_admin(item_id):
    # Логіка отримання конкретного товару за item_id з бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
    item = cursor.fetchone()
    connection.close()
    return jsonify({"item_id": item[0], "name": item[1], "description": item[2], "price": item[3]})


# admin/items/<id> [DELETE]
@app.route('/admin/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    # Логіка для видалення товару за item_id з бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
    connection.commit()
    connection.close()
    return jsonify({"message": f"Item {item_id} deleted successfully"})


# admin/orders [GET]
@app.route('/admin/orders', methods=['GET'])
def get_all_orders():
    # Логіка отримання всіх замовлень з бази даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ord")
    orders = cursor.fetchall()
    connection.close()
    return jsonify({"orders": orders})

# admin/orders/<order_id> [PUT]
@app.route('/admin/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    # Отримати дані для оновлення замовлення з тіла запиту
    data = request.json
    # Логіка для оновлення замовлення в базі даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("UPDATE ord SET status = ? WHERE order_id = ?", (data.get('status'), order_id))
    connection.commit()
    connection.close()
    return jsonify({"message": f"Order {order_id} updated successfully"})


# admin/stat [GET]
@app.route('/admin/stat', methods=['GET'])
def get_admin_statistics():
    # Логіка отримання статистики адміністратора
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM items")
    total_items = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ord")
    total_orders = cursor.fetchone()[0]
    connection.close()
    statistics = {"total_items": total_items, "total_orders": total_orders}
    return jsonify({"statistics": statistics})


# user [PUT]
@app.route('/user', methods=['PUT'])
def update_user_profile():
    # Отримати дані для оновлення профілю користувача з тіла запиту
    data = request.json
    # Логіка для оновлення профілю користувача в базі даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("UPDATE user SET name = ?, email = ? WHERE user_id = ?", (data.get('name'), data.get('email'), data.get('user_id')))
    connection.commit()
    connection.close()
    return jsonify({"message": "User profile updated successfully"})


# shop/compare/<cmp_id> [GET]
@app.route('/shop/compare/<int:cmp_id>', methods=['GET'])
def get_comparison(cmp_id):
    # Логіка отримання списку товарів для порівняння за cmp_id
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM comparison WHERE cmp_id = ?", (cmp_id,))
    comparison_items = cursor.fetchall()
    connection.close()
    return jsonify({"cmp_id": cmp_id, "comparison": comparison_items})


# shop/compare/<cmp_id> [PUT]
@app.route('/shop/compare/<int:cmp_id>', methods=['PUT'])
def update_comparison(cmp_id):
    # Отримати дані для оновлення списку товарів для порівняння з тіла запиту
    data = request.json
    updated_comparison_items = data.get('comparison', [])
    # Логіка для оновлення списку товарів для порівняння в базі даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("UPDATE comparison SET item_id = ?, name = ? WHERE cmp_id = ?",
                   [(item['item_id'], item['name'], cmp_id) for item in updated_comparison_items])
    connection.commit()
    connection.close()
    return jsonify({"message": f"Comparison {cmp_id} updated successfully", "comparison": updated_comparison_items})


# shop/compare [POST]
@app.route('/shop/compare', methods=['POST'])
def create_comparison():
    # Отримати дані для створення нового списку товарів для порівняння з тіла запиту
    data = request.json
    new_comparison_items = data.get('comparison', [])
    # Логіка для створення нового списку товарів для порівняння в базі даних
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO comparison (cmp_id, item_id, name) VALUES (?, ?, ?)",
                       [(data.get('cmp_id'), item['item_id'], item['name']) for item in new_comparison_items])
    connection.commit()
    connection.close()
    return jsonify({"message": "New comparison created successfully", "comparison": new_comparison_items})

if __name__ == "__main__":
    app.run(debug=True)
