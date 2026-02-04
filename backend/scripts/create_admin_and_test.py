"""
ScamShield - Create Admin User and Test Login
"""

import asyncio
import bcrypt
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from app.db.mongodb import connect_to_mongodb
from beanie import init_beanie
from app.db.models.user import User, UserRole
from app.services.auth_service import AuthService
from app.schemas.auth import UserLogin


async def create_admin_and_test():
    """Create admin user and test login"""
    
    print("🔗 Connecting to database...")
    await connect_to_mongodb()
    
    # Initialize Beanie with User model
    from app.db.mongodb import database
    await init_beanie(database=database, document_models=[User])
    
    # Check existing users
    print("\n📊 Checking existing users...")
    all_users = await User.find_all().to_list()
    print(f"Found {len(all_users)} users:")
    for user in all_users:
        print(f"  📧 {user.email} - 👑 {user.role.value}")
    
    # Find admin user
    admin_user = await User.find_one({"email": "raghavshivam4321@gmail.com"})
    
    if admin_user:
        print(f"\n👤 Found existing admin: {admin_user.email}")
        # Update password
        new_password = "Thakur.4321"
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
        admin_user.password_hash = hashed_password.decode('utf-8')
        await admin_user.save()
        print(f"✅ Password updated to: {new_password}")
    else:
        print("\n🆕 Creating new admin user...")
        # Create admin user
        new_password = "Thakur.4321"
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
        
        admin_user = User(
            email="raghavshivam4321@gmail.com",
            password_hash=hashed_password.decode('utf-8'),
            full_name="Admin User",
            role=UserRole.ADMIN,
            is_verified=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        await admin_user.save()
        print(f"✅ Admin user created successfully!")
        print(f"📧 Email: {admin_user.email}")
        print(f"🔑 Password: {new_password}")
        print(f"👑 Role: {admin_user.role.value}")
    
    # Test login
    print("\n🧪 Testing login...")
    try:
        login_data = UserLogin(email="raghavshivam4321@gmail.com", password="Thakur.4321")
        user, tokens = await AuthService.authenticate_user(login_data)
        
        print("✅ Login test SUCCESSFUL!")
        print(f"🎯 User ID: {user.id}")
        print(f"👤 Full Name: {user.full_name}")
        print(f"🏆 Role: {user.role.value}")
        print(f"🔐 Access Token Generated: ✅")
        
        return True
        
    except Exception as e:
        print(f"❌ Login test FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(create_admin_and_test())
    if success:
        print("\n🎉 ADMIN LOGIN IS WORKING!")
    else:
        print("\n💥 ADMIN LOGIN FAILED!")