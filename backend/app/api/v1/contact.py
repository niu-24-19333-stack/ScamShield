"""
contact.py - Contact form routes
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


router = APIRouter(prefix="/contact", tags=["Contact"])


class ContactMessage(BaseModel):
    """Schema for contact form submission"""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=10, max_length=5000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "subject": "support",
                "message": "I need help with my account..."
            }
        }


class ContactResponse(BaseModel):
    """Response for contact form"""
    status: str
    message: str
    ticket_id: Optional[str] = None


# In-memory storage for demo (in production, use database or email service)
contact_messages = []


@router.post(
    "/",
    response_model=ContactResponse,
    summary="Submit contact form"
)
async def submit_contact(data: ContactMessage):
    """
    Submit a contact form message.
    
    In production, this would:
    - Send email notification to support team
    - Create a support ticket
    - Store in database
    
    For demo, we store in memory and return success.
    """
    # Generate a ticket ID
    import secrets
    ticket_id = f"TKT-{secrets.token_hex(4).upper()}"
    
    # Store the message
    contact_messages.append({
        "ticket_id": ticket_id,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "email": data.email,
        "subject": data.subject,
        "message": data.message,
        "created_at": datetime.utcnow().isoformat(),
        "status": "new"
    })
    
    print(f"📧 New contact form submission:")
    print(f"   Ticket: {ticket_id}")
    print(f"   From: {data.first_name} {data.last_name} <{data.email}>")
    print(f"   Subject: {data.subject}")
    print(f"   Message: {data.message[:100]}...")
    
    return ContactResponse(
        status="success",
        message="Thank you for your message! We'll get back to you within 24 hours.",
        ticket_id=ticket_id
    )


@router.get(
    "/messages",
    summary="Get all contact messages (admin)"
)
async def get_contact_messages():
    """
    Get all contact form submissions.
    This is a simple admin endpoint for demo purposes.
    """
    return {
        "items": contact_messages,
        "total": len(contact_messages)
    }
