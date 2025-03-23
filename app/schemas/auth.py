from pydantic import BaseModel, Field

class SendOtpRequest(BaseModel):
    phone_number: str = Field(..., pattern="^\d{10}$", description="10-digit phone number")

class VerifyOtpRequest(BaseModel):
    phone_number: str = Field(..., pattern="^\d{10}$", description="10-digit phone number")
    otp: str = Field(..., pattern="^\d{6}$", description="6-digit OTP")
