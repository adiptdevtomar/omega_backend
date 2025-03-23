from fastapi import APIRouter, HTTPException
from app.utils.mongodb import get_collection
from app.schemas.auth import SendOtpRequest, VerifyOtpRequest
import random
import string
from datetime import datetime, timedelta
import hashlib

router = APIRouter()

# Helper function to generate OTP
def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))

def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()

@router.post("/send-otp")
async def send_otp(request: SendOtpRequest):
    """
    Generate and send OTP to the user.
    """
    phone_number = request.phone_number
    collection = get_collection("user_otps")
    otp = '123456'#generate_otp()
    expiry_time = datetime.utcnow() + timedelta(minutes=5)  # OTP valid for 5 minutesetime object

    # Store OTP and phone number in the database
    hashed_otp = hash_otp(otp)
    collection.update_one(
        {"phone_number": phone_number},  # Match by phone number
        {"$set": {"otp": hashed_otp, "expires_at": expiry_time}},  # Update or insert OTP and expiry
        upsert=True
    )
    
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
async def verify_otp(request: VerifyOtpRequest):
    """
    Verify the OTP provided by the user.
    """
    phone_number = request.phone_number
    otp = request.otp
    collection = get_collection("user_otps")
    record = collection.find_one({"phone_number": phone_number})

    if not record:
        raise HTTPException(status_code=404, detail="OTP not found")

    hashed_otp = hash_otp(otp)
    if record["otp"] != hashed_otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.utcnow() > record["expires_at"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    # OTP is valid, remove the record from the database
    collection.delete_one({"phone_number": phone_number})

    return {"message": "OTP verified successfully"}
