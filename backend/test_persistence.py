#!/usr/bin/env python3
"""
Test complete user account persistence flow:
1. Register new user → data saved to database
2. Login with same credentials → should work without recreating account
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.db.mongodb import connect_to_mongodb
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister, UserLogin
from app.db.models.user import User

async def test_account_persistence():
    """Test that user accounts persist between sessions"""
    
    print("🔧 Connecting to MongoDB...")
    await connect_to_mongodb()
    
    # Test credentials
    test_email = "persistencetest@example.com"
    test_password = "MySecurePassword123"
    test_name = "Persistence Test User"
    
    print(f"\n📝 Step 1: Check if user already exists...")
    existing_user = await User.find_one(User.email == test_email)
    if existing_user:
        print(f"⚠️  User already exists, deleting for clean test...")
        await existing_user.delete()
        print(f"✅ Deleted existing user")
    
    print(f"\n🆕 Step 2: Register new user account...")
    try:
        user_data = UserRegister(
            email=test_email,
            password=test_password,
            full_name=test_name,
            phone="+1234567890"
        )
        
        user, tokens = await AuthService.register_user(user_data)
        print(f"✅ Registration successful!")
        print(f"   📧 Email: {user.email}")
        print(f"   👤 Name: {user.full_name}")
        print(f"   🆔 User ID: {user.id}")
        print(f"   🏷️  Role: {user.role.value}")
        print(f"   🔐 Has password hash: {'Yes' if user.password_hash else 'No'}")
        print(f"   🗄️  Saved to database: ✅")
        
        user_id = str(user.id)
        
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        return False
    
    print(f"\n🔍 Step 3: Verify user exists in database...")
    try:
        # Check if user exists in database
        db_user = await User.get(user_id)
        if db_user:
            print(f"✅ User found in database!")
            print(f"   📧 Email: {db_user.email}")
            print(f"   👤 Name: {db_user.full_name}")
            print(f"   📱 Phone: {db_user.phone}")
            print(f"   📅 Created: {db_user.created_at}")
            print(f"   ✅ Active: {db_user.is_active}")
        else:
            print(f"❌ User not found in database!")
            return False
            
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False
    
    print(f"\n🔐 Step 4: Login with same credentials (simulating return visit)...")
    try:
        login_data = UserLogin(
            email=test_email,
            password=test_password
        )
        
        user, tokens = await AuthService.authenticate_user(login_data)
        print(f"✅ Login successful - No account recreation needed!")
        print(f"   📧 Email: {user.email}")
        print(f"   👤 Name: {user.full_name}")
        print(f"   🆔 User ID: {user.id}")
        print(f"   🏷️  Role: {user.role.value}")
        print(f"   🎫 Access Token: {tokens.access_token[:30]}...")
        print(f"   🎫 Refresh Token: {tokens.refresh_token[:30] if tokens.refresh_token else 'None'}...")
        
        # Verify it's the same user
        if str(user.id) == user_id:
            print(f"✅ Same user account - data persistence confirmed!")
        else:
            print(f"❌ Different user ID - something went wrong!")
            return False
            
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    print(f"\n🧪 Step 5: Test login with wrong password...")
    try:
        wrong_login = UserLogin(
            email=test_email,
            password="WrongPassword123"
        )
        
        user, tokens = await AuthService.authenticate_user(wrong_login)
        print(f"❌ Login should have failed with wrong password!")
        return False
        
    except ValueError as e:
        print(f"✅ Correctly rejected wrong password: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print(f"\n🧹 Step 6: Cleanup test user...")
    try:
        test_user = await User.get(user_id)
        if test_user:
            await test_user.delete()
            print(f"✅ Test user cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
    
    return True

async def main():
    print("=" * 60)
    print("🧪 ScamShield Account Persistence Test")
    print("Testing: Register → Save to DB → Login without recreating")
    print("=" * 60)
    
    try:
        success = await test_account_persistence()
        
        if success:
            print(f"\n🎉 ALL TESTS PASSED!")
            print(f"✅ User registration saves to database")
            print(f"✅ Users can login with saved credentials") 
            print(f"✅ No need to recreate accounts")
            print(f"✅ Wrong passwords are properly rejected")
        else:
            print(f"\n❌ SOME TESTS FAILED!")
            
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())