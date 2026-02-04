"""
ScamShield - Update Admin Password and Test Login
"""

import asyncio
import bcrypt
import sys
import os
from dotenv import load_dotenv

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from app.db.mongodb import connect_to_mongodb
from beanie import init_beanie
from app.db.models.user import User
from app.services.auth_service import AuthService
from app.schemas.auth import UserLogin


async def update_admin_password_and_test():
    """Update admin password and test login"""
    
    print("🔗 Connecting to database...")
    await connect_to_mongodb()
    
    # Initialize Beanie with User model
    from app.db.mongodb import database
    await init_beanie(database=database, document_models=[User])
    
    # Find admin user
    admin_user = await User.find_one({"email": "raghavshivam4321@gmail.com"})
    
    if not admin_user:
        print("❌ Admin user not found!")
        return
    
    print(f"👤 Found admin user: {admin_user.email}")
    
    # Update password
    new_password = "Thakur.4321"
    
    # Hash new password with bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
    
    # Update in database
    admin_user.password_hash = hashed_password.decode('utf-8')
    await admin_user.save()
    
    print(f"✅ Password updated successfully!")
    print(f"📧 Email: {admin_user.email}")
    print(f"🔑 New Password: {new_password}")
    print(f"👑 Role: {admin_user.role.value}")
    
    # Test login
    print("\n🧪 Testing login...")
    try:
        login_data = UserLogin(email="raghavshivam4321@gmail.com", password=new_password)
        user, tokens = await AuthService.authenticate_user(login_data)
        
        print("✅ Login test SUCCESSFUL!")
        print(f"🎯 User ID: {user.id}")
        print(f"👤 Full Name: {user.full_name}")
        print(f"🏆 Role: {user.role.value}")
        print(f"🔐 Access Token Generated: ✅")
        
    except Exception as e:
        print(f"❌ Login test FAILED: {str(e)}")
    
    # Check all users in database
    print("\n📊 Current users in database:")
    all_users = await User.find_all().to_list()
    for user in all_users:
        print(f"  📧 {user.email} - 👑 {user.role.value}")


if __name__ == "__main__":
    asyncio.run(update_admin_password_and_test())