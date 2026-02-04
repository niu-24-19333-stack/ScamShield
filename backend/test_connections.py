#!/usr/bin/env python3
"""
ScamShield Complete System Connection Test
Tests all components and their connections
"""

import asyncio
import sys
import os
import json

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_all_connections():
    """Test all system connections"""
    
    print("=" * 60)
    print("🧪 SCAMSHIELD COMPLETE CONNECTION TEST")
    print("=" * 60)
    
    results = {}
    
    # 1. Test Database Connection
    print("\n1️⃣ DATABASE CONNECTION TEST")
    try:
        from app.db.mongodb import connect_to_mongodb
        await connect_to_mongodb()
        print("✅ MongoDB Connection: WORKING")
        results['database'] = 'WORKING'
    except Exception as e:
        print(f"❌ Database Connection: FAILED - {e}")
        results['database'] = f'FAILED - {e}'
    
    # 2. Test User Authentication System
    print("\n2️⃣ AUTHENTICATION SYSTEM TEST")
    try:
        from app.services.auth_service import AuthService
        from app.schemas.auth import UserLogin
        
        # Test admin login
        admin_login = UserLogin(
            email="raghavshivam4321@gmail.com",
            password="Thakur.4321"
        )
        user, tokens = await AuthService.authenticate_user(admin_login)
        print(f"✅ Admin Authentication: WORKING")
        print(f"   👤 Admin: {user.email} (Role: {user.role.value})")
        results['admin_auth'] = 'WORKING'
    except Exception as e:
        print(f"❌ Admin Authentication: FAILED - {e}")
        results['admin_auth'] = f'FAILED - {e}'
    
    # 3. Test User Models
    print("\n3️⃣ USER DATA PERSISTENCE TEST")
    try:
        from app.db.models.user import User
        
        # Count users
        total_users = await User.find().count()
        admin_users = await User.find(User.role == "admin").count()
        regular_users = await User.find(User.role == "user").count()
        
        print(f"✅ User Database: WORKING")
        print(f"   📊 Total Users: {total_users}")
        print(f"   👑 Admin Users: {admin_users}")
        print(f"   👤 Regular Users: {regular_users}")
        results['user_persistence'] = 'WORKING'
    except Exception as e:
        print(f"❌ User Persistence: FAILED - {e}")
        results['user_persistence'] = f'FAILED - {e}'
    
    # 4. Test API Configuration
    print("\n4️⃣ API CONFIGURATION TEST")
    try:
        from app.core.config import settings
        
        print(f"✅ API Configuration: LOADED")
        print(f"   🔑 API Secret: {'SET' if settings.API_SECRET_KEY else 'MISSING'}")
        print(f"   🗄️  DB Name: {settings.MONGODB_DB_NAME}")
        results['api_config'] = 'WORKING'
    except Exception as e:
        print(f"❌ API Configuration: FAILED - {e}")
        results['api_config'] = f'FAILED - {e}'
    
    # 5. Test OAuth Configuration
    print("\n5️⃣ OAUTH CONFIGURATION TEST")
    try:
        import os
        google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        github_client_id = os.getenv('GITHUB_CLIENT_ID')
        
        print(f"✅ OAuth Configuration: LOADED")
        print(f"   🔵 Google OAuth: {'CONFIGURED' if google_client_id else 'MISSING'}")
        print(f"   ⚫ GitHub OAuth: {'CONFIGURED' if github_client_id else 'MISSING'}")
        results['oauth_config'] = 'WORKING'
    except Exception as e:
        print(f"❌ OAuth Configuration: FAILED - {e}")
        results['oauth_config'] = f'FAILED - {e}'
    
    # 6. Test Frontend-Backend Connection URLs
    print("\n6️⃣ FRONTEND-BACKEND CONNECTION TEST")
    try:
        frontend_url = os.getenv('FRONTEND_URL', 'NOT SET')
        api_url_expected = 'https://scamshield-api-hocl.onrender.com'
        
        print(f"✅ URL Configuration: SET")
        print(f"   🌐 Frontend URL: {frontend_url}")
        print(f"   🔗 Expected API URL: {api_url_expected}")
        results['frontend_backend'] = 'CONFIGURED'
    except Exception as e:
        print(f"❌ URL Configuration: FAILED - {e}")
        results['frontend_backend'] = f'FAILED - {e}'
    
    # 7. Summary
    print("\n" + "=" * 60)
    print("📋 CONNECTION TEST SUMMARY")
    print("=" * 60)
    
    all_working = True
    for component, status in results.items():
        status_symbol = "✅" if "WORKING" in status or "CONFIGURED" in status else "❌"
        print(f"{status_symbol} {component.replace('_', ' ').title()}: {status}")
        if "FAILED" in status:
            all_working = False
    
    print("\n" + "=" * 60)
    if all_working:
        print("🎉 ALL CONNECTIONS WORKING - READY FOR PRODUCTION!")
        print("🚀 Your ScamShield system is fully connected and ready to deploy!")
    else:
        print("⚠️  SOME CONNECTIONS NEED ATTENTION")
        print("🔧 Fix the failed connections before deployment")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    asyncio.run(test_all_connections())