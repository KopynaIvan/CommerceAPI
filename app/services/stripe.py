from fastapi import HTTPException
from sqlmodel import Session
import stripe
import os   
from app.models import OrderStatus
from app.services.orders import service_update_order_status

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
def service_create_payment_intent(amount: float, order_id: int):
    payment = stripe.PaymentIntent.create(amount=int(amount*100),currency="usd",metadata={"order_id": str(order_id)})
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

    return {"status": "ok"}
