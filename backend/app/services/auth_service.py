"""
auth_service.py - Authentication business logic
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple

from app.db.models.user import User, UserRole
from app.db.models.user_settings import UserSettings
from app.db.models.subscription import Subscription, PlanTier, SubscriptionStatus
from app.db.models.token_blacklist import TokenBlacklist
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_verification_token,
    generate_reset_token,
    get_token_expiry,
)
from app.core.config import settings
from app.schemas.auth import UserRegister, UserLogin, Token


class AuthService:
    """
    Service for authentication operations.
    """
    
    @staticmethod
    async def register_user(data: UserRegister) -> Tuple[User, Token]:
        """
        Register a new user.
        
        Returns:
            Tuple of (User, Token)
            
        Raises:
            ValueError: If email already exists
        """
        # Check if email exists
        existing = await User.find_one(User.email == data.email.lower())
        if existing:
            raise ValueError("Email already registered")
        
        # Create user
        user = User(
            email=data.email.lower(),
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            phone=data.phone,
            verification_token=generate_verification_token(),
        )
        await user.insert()
        
        # Create default settings
        settings_obj = UserSettings(user_id=str(user.id))
        await settings_obj.insert()
        
        # Create free subscription
        subscription = Subscription(
            user_id=str(user.id),
            plan_id="free",
            plan_tier=PlanTier.FREE,
            status=SubscriptionStatus.ACTIVE,
        )
        await subscription.insert()
        
        # Generate tokens
        tokens = AuthService._create_tokens(str(user.id))
        
        return user, tokens
    
    @staticmethod
    async def authenticate_user(data: UserLogin) -> Tuple[User, Token]:
        """
        Authenticate user and return tokens.
        
        Returns:
            Tuple of (User, Token)
            
        Raises:
            ValueError: If credentials are invalid
        """
        # Find user
        user = await User.find_one(User.email == data.email.lower())
        if not user:
            raise ValueError("Invalid email or password")
        
        # Check password
        if not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        # Check if active
        if not user.is_active:
            raise ValueError("Account has been deactivated")
        
        # Update last login
        user.last_login = datetime.utcnow()
        await user.save()
        
        # Generate tokens
        tokens = AuthService._create_tokens(str(user.id))
        
        return user, tokens
    
    @staticmethod
    async def refresh_tokens(refresh_token: str) -> Token:
        """
        Refresh access token using refresh token.
        
        Returns:
            New Token object
            
        Raises:
            ValueError: If refresh token is invalid
        """
        # Check if blacklisted
        if await TokenBlacklist.is_blacklisted(refresh_token):
            raise ValueError("Token has been revoked")
        
        # Decode token
        payload = decode_token(refresh_token)
        if not payload:
            raise ValueError("Invalid refresh token")
        
        # Check token type
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")
        
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")
        
        # Verify user exists and is active
        user = await User.get(user_id)
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        
        # Generate new tokens
        return AuthService._create_tokens(user_id)
    
    @staticmethod
    async def logout(token: str):
        """
        Logout by blacklisting the token.
        """
        expiry = get_token_expiry(token)
        if expiry:
            await TokenBlacklist.add_to_blacklist(token, expiry)
    
    @staticmethod
    async def request_password_reset(email: str) -> Optional[str]:
        """
        Request password reset.
        
        Returns:
            Reset token if user exists, None otherwise
        """
        user = await User.find_one(User.email == email.lower())
        if not user:
            # Don't reveal if email exists
            return None
        
        # Generate reset token
        reset_token = generate_reset_token()
        user.reset_token = reset_token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        await user.save()
        
        # In production, send email here
        # For now, return token (for testing)
        return reset_token
    
    @staticmethod
    async def reset_password(token: str, new_password: str):
        """
        Reset password using token.
        
        Raises:
            ValueError: If token is invalid or expired
        """
        user = await User.find_one(User.reset_token == token)
        if not user:
            raise ValueError("Invalid reset token")
        
        if user.reset_token_expires < datetime.utcnow():
            raise ValueError("Reset token has expired")
        
        # Update password
        user.password_hash = hash_password(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        user.update_timestamp()
        await user.save()
    
    @staticmethod
    async def verify_email(token: str) -> User:
        """
        Verify email using token.
        
        Returns:
            User object
            
        Raises:
            ValueError: If token is invalid
        """
        user = await User.find_one(User.verification_token == token)
        if not user:
            raise ValueError("Invalid verification token")
        
        user.is_verified = True
        user.verification_token = None
        user.update_timestamp()
        await user.save()
        
        return user
    
    @staticmethod
    async def change_password(
        user: User,
        current_password: str,
        new_password: str
    ):
        """
        Change password for logged-in user.
        
        Raises:
            ValueError: If current password is wrong
        """
        if not verify_password(current_password, user.password_hash):
            raise ValueError("Current password is incorrect")
        
        user.password_hash = hash_password(new_password)
        user.update_timestamp()
        await user.save()
    
    @staticmethod
    def _create_tokens(user_id: str) -> Token:
        """
        Create access and refresh tokens.
        """
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
