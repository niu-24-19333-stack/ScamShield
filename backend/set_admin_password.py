#!/usr/bin/env python3
"""
Simple admin password setter using MongoDB directly
"""

import asyncio
import os
import sys
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    import bcrypt
    
    def simple_hash_password(password: str) -> str:
        """Simple password hashing using bcrypt directly"""
        # Convert password to bytes and hash
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def simple_verify_password(password: str, hashed: str) -> bool:
        """Simple password verification"""
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
except ImportError:
    print("❌ bcrypt not available, using simple hash")
    import hashlib
    
    def simple_hash_password(password: str) -> str:
        """Fallback hash function"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def simple_verify_password(password: str, hashed: str) -> bool:
        """Simple verification"""
        return hashlib.sha256(password.encode()).hexdigest() == hashed

from app.db.mongodb import connect_to_mongodb
from app.db.models.user import User, UserRole, AuthProvider

async def set_admin_password():
    """Set admin password directly"""
    
    print("🔧 Connecting to MongoDB...")
    await connect_to_mongodb()
    
    admin_email = "raghavshivam4321@gmail.com"
    admin_password = "Thakur.4321"
    
    # Find the user
    user = await User.find_one(User.email == admin_email)
    if not user:
        print(f"❌ User not found: {admin_email}")
        return
    
    print(f"📝 Found user: {admin_email}")
    print(f"   Current role: {user.role.value}")
    print(f"   Has password: {'Yes' if user.password_hash else 'No'}")
    
    # Hash password and update user
    try:
        password_hash = simple_hash_password(admin_password)
        print(f"✅ Password hashed successfully")
        
        # Verify the hash works
        if simple_verify_password(admin_password, password_hash):
            print(f"✅ Password verification successful")
        else:
            print(f"❌ Password verification failed")
            return
        
        # Update user
        user.password_hash = password_hash
        user.role = UserRole.ADMIN
        user.is_active = True
        user.is_verified = True
        user.auth_provider = AuthProvider.LOCAL
        user.updated_at = datetime.utcnow()
        
        await user.save()
        
        print(f"✅ Admin user updated successfully!")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print(f"   Role: {user.role.value}")
        
    except Exception as e:
        print(f"❌ Failed to hash password: {e}")
        return

async def main():
    print("=" * 50)
    print("🛡️  ScamShield Simple Admin Setup")
    print("=" * 50)
    
    try:
        await set_admin_password()
        print("\n✅ Admin setup completed!")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())