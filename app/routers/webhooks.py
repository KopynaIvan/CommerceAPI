from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from app.services.stripe import handle_webhook
from app.crud import get_session

router = APIRouter()

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, session: Session = Depends(get_session)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    return handle_webhook(payload=payload, sig_header=sig_header, session=session)
