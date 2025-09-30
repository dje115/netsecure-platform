#!/usr/bin/env python3
"""
Quick script to reset admin password
Run with: python reset-admin-password.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.security import get_password_hash
from app.core.database import SessionLocal
from app.models.user import User

def reset_admin_password():
    """Reset admin password to 'admin123'"""
    
    db = SessionLocal()
    try:
        # Find admin user
        admin = db.query(User).filter(User.username == 'admin').first()
        
        if not admin:
            print("❌ Admin user not found!")
            print("Creating new admin user...")
            
            new_admin = User(
                username='admin',
                email='admin@security.local',
                hashed_password=get_password_hash('admin123'),
                full_name='Administrator',
                role='admin',
                is_superuser=True,
                is_active=True
            )
            db.add(new_admin)
            db.commit()
            print("✅ Admin user created!")
            print("   Username: admin")
            print("   Password: admin123")
        else:
            # Reset password
            admin.hashed_password = get_password_hash('admin123')
            admin.is_active = True
            db.commit()
            print("✅ Admin password reset!")
            print("   Username: admin")
            print("   Password: admin123")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    print("🔐 Resetting admin password...")
    reset_admin_password()


