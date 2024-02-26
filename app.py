from flask import Flask, request, jsonify, render_template, session, g
from flask_sqlalchemy import SQLAlchemy
from models import Review, Cart, Favorites, Waitlist, Comparison, User, Order, Items
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://kholod:12345@localhost/hillel_shop')
db = SQLAlchemy(app)

app.secret_key = 1111


# Самописний менеджер контексту
def before_request():
    g.db = db.create_all()


@app.teardown_request
def teardown_request(exception=None):
    db.session.remove()


# Функція для отримання загальної суми кошика
def get_cart_total(items):
    cart = session.get('cart', {})
    total = 0.0

    # Логіка для отримання цін товарів з бази даних чи іншого джерела
    items = items.query.all()
    item_prices = {item.id: item.price for item in items}

    for item_id, quantity in cart.items():
        if item_id in item_prices:
            total += item_prices[item_id] * quantity

    return total


# Обробка реєстрації користувача

@app.route('/register', methods=['POST'])
def register():
    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    return render_template('login.html')


@app.route('/shop/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Items.query.get(item_id)
    if item:
        return render_template('item.html', item=item)
    else:
        return render_template('item_not_found.html')


@app.route('/shop/items/<int:item_id>/review', methods=['POST'])
def post_review(item_id):
    text = request.form['text']
    rating = request.form['rating']

    review = Review(item_id=item_id, text=text, rating=rating)
    db.session.add(review)
    db.session.commit()

    return render_template('review_posted.html')


@app.route('/shop/items/<int:item_id>/review', methods=['GET'])
def get_reviews(item_id):
    reviews = Review.query.filter_by(item_id=item_id).all()
    return render_template('reviews.html', reviews=reviews)


@app.route('/shop/items/<int:item_id>/review/<int:review_id>', methods=['GET'])
def get_review(item_id, review_id):
    review = Review.query.filter_by(item_id=item_id, id=review_id).first()
    if review:
        return render_template('review.html', review=review)
    else:
        return render_template('review_not_found.html')


@app.route('/shop/items/<int:item_id>/review/<int:review_id>', methods=['PUT'])
def update_review(item_id, review_id):
    text = request.form['text']
    rating = request.form['rating']

    review = Review.query.filter_by(item_id=item_id, id=review_id).first()
    if review:
        review.text = text
        review.rating = rating
        db.session.commit()
        return render_template('review_updated.html')
    else:
        return render_template('review_not_found.html')


@app.route('/shop/items', methods=['GET'])
def get_items():
    # Отримати параметри запиту для фільтрації, сортування та розбивки за сторінками
    category = request.args.get('category', type=int)
    order = request.args.get('order', default='price', type=str)
    page = request.args.get('page', default=1, type=int)

    # Логіка для вибору товарів з бази даних за заданими параметрами
    items = Items.query.filter_by(category=category).order_by(order).paginate(page=page, per_page=10)

    return render_template('items.html', items=items.items)


@app.route('/shop/search', methods=['POST'])
def search_items():
    # Отримати дані для пошуку з тіла запиту
    data = request.json
    search_query = data.get('search_query')
    # Логіка для пошуку товарів за заданим запитом у базі даних
    items = Items.query.filter(Items.name.ilike(f"%{search_query}%")).all()
    return render_template('search_results.html', items=items)


@app.route('/shop/cart', methods=['GET'])
def get_cart():
    # Логіка отримання вмісту корзини з бази даних або іншого джерела
    cart_items = Cart.query.all()
    return render_template('cart.html', cart_items=cart_items)


@app.route('/shop/cart', methods=['POST', 'PUT'])
def update_cart():
    # Отримати дані для оновлення корзини з параметрів запиту або тіла запиту
    item_id = request.args.get('item_id', type=int)
    amount = request.args.get('amount', type=int)

    if request.method == 'POST':
        # Логіка для додавання товару у корзину в базі даних
        cart_item = Cart(item_id=item_id, quantity=amount)
        db.session.add(cart_item)
        db.session.commit()
        return render_template('cart_update_success.html', message=f"Item {item_id} added to the cart successfully")
    elif request.method == 'PUT':
        # Логіка для оновлення кількості товару у корзині в базі даних
        cart_item = Cart.query.filter_by(item_id=item_id).first()
        cart_item.quantity = amount
        db.session.commit()
        return render_template('cart_update_success.html', message=f"Item {item_id} updated in the cart successfully")


@app.route('/shop/cart', methods=['DELETE'])
def delete_item_from_cart():
    # Отримати ідентифікатор товару для видалення з параметрів запиту
    item_id_to_delete = request.args.get('item_id', type=int)
    # Логіка для видалення товару з корзини в базі даних
    Cart.query.filter_by(item_id=item_id_to_delete).delete()
    db.session.commit()
    return render_template('cart_update_success.html',
                           message=f"Item {item_id_to_delete} removed from the cart successfully")


@app.route('/shop/cart/order', methods=['GET'])
def fill_order_form():
    # Логіка для отримання даних для оформлення замовлення (форми)
    # Повернути результат у форматі JSON
    return render_template('order_form.html', message="Provide shipping details and payment information")


# shop/favorites/<list_id> [GET]
@app.route('/shop/favorites/<int:list_id>', methods=['GET'])
def get_favorite_list(list_id):
    # Логіка отримання вмісту списку улюблених товарів за list_id
    favorite_items = Favorites.query.filter_by(list_id=list_id).all()
    return render_template('favorites.html', list_id=list_id, favorites=favorite_items)


# shop/favorites/<list_id> [PUT]
@app.route('/shop/favorites/<int:list_id>', methods=['PUT'])
def update_favorite_list(list_id):
    # Отримати дані для оновлення списку улюблених товарів з тіла запиту
    data = request.json
    updated_favorite_items = data.get('favorites', [])

    # Оновити список улюблених товарів в базі даних
    Favorites.query.filter_by(list_id=list_id).delete()
    db.session.commit()

    for item_id in updated_favorite_items:
        favorite_item = Favorites(list_id=list_id, item_id=item_id)
        db.session.add(favorite_item)

    db.session.commit()

    return render_template('favorites_result.html', message=f"Favorite list {list_id} updated successfully",
                           favorites=updated_favorite_items)


# shop/favorites [POST]
@app.route('/shop/favorites', methods=['POST'])
def create_favorite_list():
    # Отримати дані для створення нового списку улюблених товарів з тіла запиту
    data = request.json
    new_favorite_items = data.get('favorites', [])

    # Створити новий список улюблених товарів в базі даних

    return render_template('favorites_result.html', message="New favorite list created successfully",
                           favorites=new_favorite_items)


# shop/waitlist [GET]
@app.route('/shop/waitlist', methods=['GET'])
def get_waitlist():
    # Отримати дані списку очікування з бази даних
    waitlist_items = Waitlist.query.all()

    return render_template('waitlist_result.html', waitlist=waitlist_items)


# shop/waitlist [PUT]
@app.route('/shop/waitlist', methods=['PUT'])
def update_waitlist():
    # Отримати дані для оновлення списку очікування з тіла запиту
    data = request.json
    updated_waitlist_items = data.get('waitlist', [])

    # Оновити список очікування в базі даних
    Waitlist.query.delete()
    db.session.commit()

    for item_id in updated_waitlist_items:
        waitlist_item = Waitlist(item_id=item_id)
        db.session.add(waitlist_item)

    db.session.commit()

    return render_template('waitlist_result.html', message="Waitlist updated successfully",
                           waitlist=updated_waitlist_items)


# admin/items [POST]
@app.route('/admin/items', methods=['POST'])
def create_item():
    # Отримати дані для створення нового товару з тіла запиту
    data = request.json
    # Створити новий товар в базі даних
    return render_template('item_result.html', message="New item created successfully")


# shop/favorites/<list_id> [PUT]
@app.route('/shop/favorites/<int:list_id>', methods=['PUT'])
def update_favorite_list(list_id):
    # Отримати дані для оновлення списку улюблених товарів з тіла запиту
    data = request.json
    updated_favorite_items = data.get('favorites', [])

    # Оновити список улюблених товарів в базі даних
    favorite_list = Favorites.query.get(list_id)
    if favorite_list:
        favorite_list.items = updated_favorite_items
        db.session.commit()

    return render_template('favorites_result.html', message=f"Favorite list {list_id} updated successfully",
                           favorites=updated_favorite_items)


# shop/favorites [POST]
@app.route('/shop/favorites', methods=['POST'])
def create_favorite_list():
    # Отримати дані для створення нового списку улюблених товарів з тіла запиту
    data = request.json
    new_favorite_items = data.get('favorites', [])

    # Створити новий список улюблених товарів в базі даних
    new_favorite_list = Favorites(items=new_favorite_items)
    db.session.add(new_favorite_list)
    db.session.commit()

    return render_template('favorites_result.html', message="New favorite list created successfully",
                           favorites=new_favorite_items)


# shop/waitlist [GET]
@app.route('/shop/waitlist', methods=['GET'])
def get_waitlist():
    # Отримати дані списку очікування з бази даних
    waitlist_items = Waitlist.query.all()

    return render_template('waitlist_result.html', waitlist=waitlist_items)


# shop/waitlist [PUT]
@app.route('/shop/waitlist', methods=['PUT'])
def update_waitlist():
    # Отримати дані для оновлення списку очікування з тіла запиту
    data = request.json
    updated_waitlist_items = data.get('waitlist', [])

    # Оновити список очікування в базі даних
    waitlist = Waitlist.query.first()
    if waitlist:
        waitlist.item_id = updated_waitlist_items
        db.session.commit()

    return render_template('waitlist_result.html', message="Waitlist updated successfully",
                           waitlist=updated_waitlist_items)


# admin/items [POST]
@app.route('/admin/items', methods=['POST'])
def create_item():
    # Отримати дані для створення нового товару з тіла запиту
    data = request.json

    # Створити новий товар в базі даних
    new_item = Items(name=data.get('name'), description=data.get('description'), price=data.get('price'))
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "New item created successfully"})


@app.route('/admin/items', methods=['GET'])
def get_all_items():
    items = Items.query.all()
    return render_template('items_result.html', items=items)


@app.route('/admin/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    item = Items.query.get(item_id)
    if item:
        item.name = data.get('name')
        item.description = data.get('description')
        item.price = data.get('price')
        db.session.commit()
        return render_template('item_updated.html', message=f"Item {item_id} updated successfully", item=data)
    else:
        return render_template('item_not_found.html')


@app.route('/admin/items/<int:item_id>', methods=['GET'])
def get_item_admin(item_id):
    item = Items.query.get(item_id)
    if item:
        return render_template('item_details.html', item=item)
    else:
        return render_template('item_not_found.html')


@app.route('/admin/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Items.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return render_template('item_deleted.html', message=f"Item {item_id} deleted successfully")
    else:
        return render_template('item_not_found.html')


# admin/orders [GET]
@app.route('/admin/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return render_template('orders_result.html', orders=orders)


# admin/orders/<order_id> [PUT]
@app.route('/admin/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    order = Order.query.get(order_id)
    if order:
        order.status = data.get('status')
        db.session.commit()
        return render_template('order_updated.html', message=f"Order {order_id} updated successfully", order=data)
    else:
        return render_template('order_not_found.html')


# admin/stat [GET]
@app.route('/admin/stat', methods=['GET'])
def get_admin_statistics():
    total_items = Items.query.count()
    total_orders = Order.query.count()
    statistics = {"total_items": total_items, "total_orders": total_orders}
    return render_template('admin_statistics.html', statistics=statistics)


# user [PUT]
@app.route('/user', methods=['PUT'])
def update_user_profile():
    data = request.json
    user = User.query.get(data.get('user_id'))
    if user:
        user.name = data.get('name')
        user.email = data.get('email')
        db.session.commit()
        return render_template('user_profile_updated.html', message="User profile updated successfully", user=data)
    else:
        return render_template('user_not_found.html')


# shop/compare/<cmp_id> [GET]
@app.route('/shop/compare/<int:cmp_id>', methods=['GET'])
def get_comparison(cmp_id):
    comparison_items = Comparison.query.filter_by(cmp_id=cmp_id).all()
    return render_template('comparison_result.html', cmp_id=cmp_id, comparison=comparison_items)


# shop/compare/<cmp_id> [PUT]
@app.route('/shop/compare/<int:cmp_id>', methods=['PUT'])
def update_comparison(cmp_id):
    data = request.json
    updated_comparison_items = data.get('comparison', [])
    Comparison.query.filter_by(cmp_id=cmp_id).delete()
    db.session.commit()
    new_comparison_items = [Comparison(cmp_id=cmp_id, item_id=item['item_id'], name=item['name'])
                            for item in updated_comparison_items]
    db.session.add_all(new_comparison_items)
    db.session.commit()
    return render_template('comparison_updated.html', message=f"Comparison {cmp_id} updated successfully",
                           comparison=updated_comparison_items)


# shop/compare [POST]
@app.route('/shop/compare', methods=['POST'])
def create_comparison():
    data = request.json
    new_comparison_items = data.get('comparison', [])
    new_comparison_items = [Comparison(cmp_id=data.get('cmp_id'), item_id=item['item_id'], name=item['name'])
                            for item in new_comparison_items]
    db.session.add_all(new_comparison_items)
    db.session.commit()
    return render_template('comparison_created.html', message="New comparison created successfully",
                           comparison=new_comparison_items)


# Функція для відображення результатів пошуку
@app.route('/shop/search', methods=['POST'])
def search_items():
    # Отримати дані для пошуку з тіла запиту
    data = request.json
    search_query = data.get('search_query')
    # Логіка для пошуку товарів за заданим запитом у базі даних
    items = Items.query.filter(Items.name.ilike(f"%{search_query}%")).all()
    return render_template('search_results.html', keyword=search_query, search_results=items)

# Функція для відображення результатів порівняння товарів
@app.route('/shop/compare/<int:cmp_id>', methods=['GET'])
def get_comparison(cmp_id):
    comparison_items = Comparison.query.filter_by(cmp_id=cmp_id).all()
    selected_products = [item.name for item in comparison_items]
    attributes = {}
    return render_template('comparison_results.html', selected_products=selected_products, attributes=attributes)

if __name__ == "__main__":
    app.run(debug=True)
