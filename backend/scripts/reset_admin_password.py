"""
ScamShield - Reset Admin Password Script
Run this if login still fails after Render update
"""

import asyncio
import bcrypt
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db.mongodb import connect_to_mongo
from app.db.models.user import User
from app.core.config import settings


async def reset_admin_password():
    """Reset admin user password"""
    
    # Connect to database
    await connect_to_mongo()
    
    # Find admin user
    admin_user = await User.find_one({"email": "raghavshivam4321@gmail.com"})
    
    if not admin_user:
        print("❌ Admin user not found!")
        return
    
    # Hash new password
    new_password = "Admin123!"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
    
    # Update password
    admin_user.password_hash = hashed_password.decode('utf-8')
    await admin_user.save()
    
    print(f"✅ Admin password reset successfully!")
    print(f"📧 Email: {admin_user.email}")
    print(f"🔑 Password: {new_password}")
    print(f"👤 Role: {admin_user.role.value}")


if __name__ == "__main__":
    asyncio.run(reset_admin_password())