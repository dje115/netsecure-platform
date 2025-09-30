#!/usr/bin/env python3
"""Reset admin password"""
import sys
import os
sys.path.insert(0, '/app')

from app.core.security import get_password_hash
from app.core.database import SessionLocal
from app.models.user import User

def reset_password():
    db = SessionLocal()
    try:
        # Find admin user
        admin = db.query(User).filter(User.username == 'admin').first()
        
        if not admin:
            print("Admin user not found!")
            return False
        
        # Generate new hash
        new_hash = get_password_hash('admin123')
        print(f"Generated hash: {new_hash[:30]}...")
        
        # Update password
        admin.hashed_password = new_hash
        admin.is_active = True
        db.commit()
        
        print("SUCCESS: Admin password reset to 'admin123'")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == '__main__':
    reset_password()

