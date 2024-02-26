import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://kholod:12345@localhost/hillel_shop')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MyModel(db.Model):
    __tablename__ = 'my_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


def execute_query(query, parameters=None):
    try:
        result = db.engine.execute(query, parameters)
        return result.fetchall()  # Повертаємо результат запиту
    except SQLAlchemyError as e:
        raise e

def insert_data(table, data):
    try:
        record = MyModel(**data)  # Створюємо новий запис
        db.session.add(record)  # Додаємо запис до сесії
        db.session.commit()  # Зберігаємо зміни
    except SQLAlchemyError as e:
        db.session.rollback()  # Відкат змін у випадку помилки
        raise e

def update_data(table, set_values, condition):
    try:
        MyModel.query.filter_by(**condition).update(set_values)  # Оновлюємо записи за умовою
        db.session.commit()  # Зберігаємо зміни
    except SQLAlchemyError as e:
        db.session.rollback()  # Відкат змін у випадку помилки
        raise e

def delete_data(table, condition):
    try:
        MyModel.query.filter_by(**condition).delete()  # Видаляємо записи за умовою
        db.session.commit()  # Зберігаємо зміни
    except SQLAlchemyError as e:
        db.session.rollback()  # Відкат змін у випадку помилки
        raise e

def select_data(table, columns="*", condition=None):
    try:
        query = MyModel.query.with_entities(*columns)  # Починаємо побудову запиту
        if condition:
            query = query.filter_by(**condition)  # Додаємо умову до запиту, якщо вона є
        result = query.all()  # Виконуємо запит та отримуємо результат
        return result
    except SQLAlchemyError as e:
        raise e

