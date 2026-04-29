from fastapi import HTTPException
from sqlmodel import Session
import stripe
import os   
from app.models import Order, OrderStatus, User
from app.services.orders import service_update_order_status
from app.tasks import send_confirmation_email

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
def service_create_payment_intent(amount: float, order_id: int):
    payment = stripe.PaymentIntent.create(amount=int(amount*100),
                                          currency="usd",
                                          metadata={"order_id": str(order_id)},
                                          automatic_payment_methods={"enabled":True,
                                                                     "allow_redirects":"never"})
    return payment.client_secret

def handle_webhook(payload: bytes, sig_header: str, session: Session):
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, os.environ["STRIPE_WEBHOOK_SECRET"])

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "payment_intent.succeeded":
        metadata = event["data"]["object"]["metadata"]
        
        if "order_id" not in metadata:
            return {"status": "ignored"}

        order_id = int(metadata["order_id"])
        service_update_order_status(order_id=order_id,new_status=OrderStatus.paid, session=session)

        order = session.get(Order,order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order doesn't exist")

        user = session.get(User,order.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User doesn't exist")

        send_confirmation_email.delay(email=user.email, order_id=order_id)

    return {"status": "ok"}
