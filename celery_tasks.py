from celery import Celery
from flask_mail import Message
from flask import current_app
from extensions import mail

celery = Celery(__name__)

@celery.task
def send_order_confirmation_email(user_email, order_details):
    with current_app.app_context():
        msg = Message(subject="Order Confirmation",
                      sender=current_app.config['MAIL_USERNAME'],
                      recipients=[user_email],
                      body=f"Dear customer, your order details are: {order_details}")
        mail.send(msg)
