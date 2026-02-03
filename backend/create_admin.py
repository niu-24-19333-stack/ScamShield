#!/usr/bin/env python3
"""
One-time admin creation script
Run this script once to create the admin user
"""

import asyncio
import os
import sys
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.db.mongodb import connect_to_mongodb
from app.db.models.user import User, UserRole, AuthProvider
from app.core.security import hash_password

async def create_admin():
    """Create admin user with specified credentials"""
    
    print("🔧 Connecting to MongoDB...")
    await connect_to_mongodb()
    
    # Admin credentials
    admin_email = "raghavshivam4321@gmail.com"
    admin_password = "Thakur.4321"
    admin_name = "ScamShield Admin"
    
    # Hash the password
    password_hash = hash_password(admin_password)
    
    # Check if admin already exists
    existing_admin = await User.find_one(User.email == admin_email)
    if existing_admin:
        print(f"❌ Admin user already exists: {admin_email}")
        print(f"   Role: {existing_admin.role.value}")
        print(f"   Active: {existing_admin.is_active}")
        print(f"   Has password: {'Yes' if existing_admin.password_hash else 'No'}")
        
        # Update role if needed
        updates_made = False
        if existing_admin.role != UserRole.ADMIN:
            existing_admin.role = UserRole.ADMIN
            updates_made = True
            print(f"✅ Updated role to admin for: {admin_email}")
        
        # Set password if missing (for OAuth users)
        if not existing_admin.password_hash:
            existing_admin.password_hash = password_hash
            existing_admin.auth_provider = AuthProvider.LOCAL  # Allow both OAuth and password login
            updates_made = True
            print(f"✅ Set password for existing OAuth user: {admin_email}")
        
        # Ensure admin is verified and active
        if not existing_admin.is_verified:
            existing_admin.is_verified = True
            updates_made = True
        
        if not existing_admin.is_active:
            existing_admin.is_active = True
            updates_made = True
        
        if updates_made:
            existing_admin.update_timestamp()
            await existing_admin.save()
            print(f"✅ Admin user updated successfully!")
        
        return
    
    # Create admin user
    admin_user = User(
        email=admin_email,
        password_hash=password_hash,
        full_name=admin_name,
        auth_provider=AuthProvider.LOCAL,
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True,  # Admin is pre-verified
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    try:
        await admin_user.insert()
        print("✅ Admin user created successfully!")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print(f"   Role: {UserRole.ADMIN.value}")
        print("\n🔐 Admin can now log in to access the admin panel")
        
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        raise

async def main():
    """Main function"""
    print("=" * 50)
    print("🛡️  ScamShield Admin Creation Script")
    print("=" * 50)
    
    try:
        await create_admin()
        print("\n✅ Script completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Script failed: {e}")
        sys.exit(1)
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())