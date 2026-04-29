from app.celery_app import celery_app

@celery_app.task
def send_confirmation_email(email: str, order_id: int):
    print(f"Sending confirmation email to {email} for order {order_id}")
