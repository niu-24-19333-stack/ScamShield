#!/usr/bin/env python3
"""
Test user registration and admin login
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.db.mongodb import connect_to_mongodb
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister, UserLogin

async def test_user_operations():
    """Test user registration and authentication"""
    
    print("🔧 Connecting to MongoDB...")
    await connect_to_mongodb()
    
    print("\n📝 Testing User Registration...")
    
    # Test data
    test_email = "testuser@example.com"
    test_password = "TestPassword123"
    
    try:
        # Try to register a new user
        user_data = UserRegister(
            email=test_email,
            password=test_password,
            full_name="Test User",
            phone="+1234567890"
        )
        
        user, tokens = await AuthService.register_user(user_data)
        print(f"✅ User registration successful!")
        print(f"   User ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Name: {user.full_name}")
        print(f"   Role: {user.role.value}")
        print(f"   Access token: {tokens.access_token[:20]}...")
        
    except ValueError as e:
        if "already registered" in str(e):
            print(f"ℹ️  User already exists: {test_email}")
        else:
            print(f"❌ Registration failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error during registration: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🔐 Testing Admin Login...")
    
    # Test admin login
    admin_email = "raghavshivam4321@gmail.com"
    admin_password = "Thakur.4321"
    
    try:
        login_data = UserLogin(
            email=admin_email,
            password=admin_password
        )
        
        user, tokens = await AuthService.authenticate_user(login_data)
        print(f"✅ Admin login successful!")
        print(f"   User ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Name: {user.full_name}")
        print(f"   Role: {user.role.value}")
        print(f"   Access token: {tokens.access_token[:20]}...")
        
    except ValueError as e:
        print(f"❌ Admin login failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error during admin login: {e}")
        import traceback
        traceback.print_exc()

async def main():
    print("=" * 50)
    print("🧪 ScamShield Authentication Test")
    print("=" * 50)
    
    try:
        await test_user_operations()
        print("\n✅ Testing completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())