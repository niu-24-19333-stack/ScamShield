"""
users.py - User management routes
"""

import secrets
import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional

from app.schemas.user import (
    UserResponse,
    UserUpdate,
    UserSettingsResponse,
    UserSettingsUpdate,
    UserStatsResponse,
)
from app.services.user_service import UserService
from app.core.dependencies import get_current_user, get_current_active_user
from app.db.models.user import User


router = APIRouter(prefix="/users", tags=["Users"])


# ==========================================
# API KEY MANAGEMENT
# ==========================================

# In-memory storage for demo (in production, use database)
api_keys_store: dict = {}


class APIKeyResponse(BaseModel):
    """Schema for API key response"""
    api_key: str
    prefix: str
    created_at: str
    expires_at: Optional[str] = None
    status: str = "active"
    
    
class APIKeyInfo(BaseModel):
    """Schema for API key info (without full key)"""
    prefix: str
    created_at: str
    expires_at: Optional[str] = None
    status: str
    last_used: Optional[str] = None


def generate_api_key() -> tuple[str, str]:
    """Generate a secure API key with prefix for identification"""
    # Generate random bytes and convert to hex
    random_bytes = secrets.token_bytes(32)
    key_hash = hashlib.sha256(random_bytes).hexdigest()
    
    # Format: ss_key_xxxxxxxxxxxxxxxxxxxxxxxxxxxx (ScamShield key)
    api_key = f"ss_key_{key_hash[:32]}"
    prefix = f"ss_key_{key_hash[:8]}..."
    
    return api_key, prefix


@router.post(
    "/me/api-key",
    response_model=APIKeyResponse,
    summary="Generate new API key"
)
async def generate_user_api_key(user: User = Depends(get_current_active_user)):
    """
    Generate a new API key for the current user.
    
    **Warning**: This will invalidate any existing API key.
    
    The API key is only shown once - make sure to save it securely.
    """
    user_id = str(user.id)
    
    # Generate new key
    api_key, prefix = generate_api_key()
    
    # Store key info (in production, store hash only)
    now = datetime.now(timezone.utc)
    api_keys_store[user_id] = {
        "key_hash": hashlib.sha256(api_key.encode()).hexdigest(),
        "prefix": prefix,
        "created_at": now.isoformat(),
        "expires_at": None,  # Never expires for now
        "status": "active",
        "last_used": None
    }
    
    return APIKeyResponse(
        api_key=api_key,
        prefix=prefix,
        created_at=now.isoformat(),
        expires_at=None,
        status="active"
    )


@router.get(
    "/me/api-key",
    response_model=APIKeyInfo,
    summary="Get API key info"
)
async def get_user_api_key_info(user: User = Depends(get_current_active_user)):
    """
    Get information about the current user's API key.
    
    **Note**: The full API key is never returned - only metadata.
    """
    user_id = str(user.id)
    
    if user_id not in api_keys_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No API key found. Generate one first."
        )
    
    key_info = api_keys_store[user_id]
    
    return APIKeyInfo(
        prefix=key_info["prefix"],
        created_at=key_info["created_at"],
        expires_at=key_info["expires_at"],
        status=key_info["status"],
        last_used=key_info["last_used"]
    )


@router.delete(
    "/me/api-key",
    summary="Revoke API key"
)
async def revoke_user_api_key(user: User = Depends(get_current_active_user)):
    """
    Revoke the current user's API key.
    
    The API key will immediately stop working.
    """
    user_id = str(user.id)
    
    if user_id not in api_keys_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No API key found to revoke."
        )
    
    # Mark as revoked (or delete)
    api_keys_store[user_id]["status"] = "revoked"
    
    return {
        "status": "success",
        "message": "API key revoked successfully"
    }


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile"
)
async def get_profile(user: User = Depends(get_current_active_user)):
    """
    Get the current user's profile information.
    """
    return await UserService.get_user_profile(user)


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile"
)
async def update_profile(
    data: UserUpdate,
    user: User = Depends(get_current_active_user)
):
    """
    Update the current user's profile.
    
    - **full_name**: New display name
    - **phone**: New phone number
    """
    return await UserService.update_user_profile(user, data)


@router.get(
    "/me/settings",
    response_model=UserSettingsResponse,
    summary="Get user settings"
)
async def get_settings(user: User = Depends(get_current_active_user)):
    """
    Get the current user's settings and preferences.
    """
    return await UserService.get_user_settings(str(user.id))


@router.put(
    "/me/settings",
    response_model=UserSettingsResponse,
    summary="Update user settings"
)
async def update_settings(
    data: UserSettingsUpdate,
    user: User = Depends(get_current_active_user)
):
    """
    Update the current user's settings.
    
    - **email_alerts**: Enable email notifications
    - **sms_alerts**: Enable SMS notifications
    - **auto_block**: Automatically block detected scams
    - **sensitivity**: Detection sensitivity (low/medium/high)
    """
    return await UserService.update_user_settings(str(user.id), data)


@router.get(
    "/me/stats",
    response_model=UserStatsResponse,
    summary="Get user statistics"
)
async def get_stats(user: User = Depends(get_current_active_user)):
    """
    Get the current user's usage statistics.
    """
    return await UserService.get_user_stats(str(user.id))


@router.delete(
    "/me",
    summary="Delete user account"
)
async def delete_account(user: User = Depends(get_current_active_user)):
    """
    Delete (deactivate) the current user's account.
    This is a soft delete - the account can be recovered.
    """
    await UserService.delete_user_account(user)
    
    return {
        "status": "success",
        "message": "Account deactivated successfully"
    }
