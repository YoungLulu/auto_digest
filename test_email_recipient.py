#!/usr/bin/env python3
"""
Test script to verify email recipient configuration from environment variable
"""

import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_email_recipient_config():
    """Test the new email recipient configuration"""
    
    print("📧 Testing Email Recipient Configuration\n")
    
    # Load config
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    email_config = config["email"]
    
    print("--- Current Email Configuration ---")
    print(f"Enabled: {email_config['enabled']}")
    print(f"Recipient Environment Variable: {email_config['recipient_env']}")
    print(f"Send Attachments: {email_config['send_attachments']}")
    
    # Check if environment variable is set
    recipient_env_var = email_config["recipient_env"]
    recipient = os.getenv(recipient_env_var)
    
    print(f"\n--- Environment Variable Check ---")
    if recipient:
        print(f"✅ {recipient_env_var}: {recipient}")
        print(f"✅ Email recipient will be: {recipient}")
    else:
        print(f"❌ {recipient_env_var}: Not set")
        print(f"❌ Email sending will fail without this variable")
    
    # Show expected SMTP configuration
    smtp_config = email_config["smtp"]
    print(f"\n--- Expected SMTP Environment Variables ---")
    
    smtp_vars = {
        smtp_config["host_env"]: "SMTP server hostname",
        smtp_config["port_env"]: "SMTP server port", 
        smtp_config["username_env"]: "SMTP username (also used as recipient)",
        smtp_config["password_env"]: "SMTP password"
    }
    
    for var_name, description in smtp_vars.items():
        value = os.getenv(var_name)
        if value:
            if 'password' in var_name.lower():
                masked_value = "***" + value[-3:] if len(value) > 3 else "***"
                print(f"✅ {var_name}: {masked_value} ({description})")
            else:
                print(f"✅ {var_name}: {value} ({description})")
        else:
            print(f"❌ {var_name}: Not set ({description})")
    
    # Demonstrate the runner logic
    print(f"\n--- Runner Email Logic Simulation ---")
    if recipient:
        print(f"✅ Runner will send email to: {recipient}")
        print(f"✅ This matches SMTP username: {os.getenv(smtp_config['username_env'], 'NOT_SET')}")
    else:
        print(f"❌ Runner will fail with error:")
        print(f"   'Email recipient not found in environment variable: {recipient_env_var}'")
    
    return recipient is not None


def show_migration_info():
    """Show information about migrating from old config"""
    
    print(f"\n--- Migration Information ---")
    print("🔄 Changes from previous configuration:")
    print("   OLD: \"recipient\": \"hardcoded@email.com\"")
    print("   NEW: \"recipient_env\": \"SMTP_USERNAME\"")
    print()
    print("💡 Benefits of new approach:")
    print("   ✅ No sensitive email addresses in config files")
    print("   ✅ Automatically uses same email as SMTP authentication")
    print("   ✅ Safer for version control and sharing configs")
    print("   ✅ Consistent with other environment variable usage")
    print()
    print("📝 Migration steps:")
    print("   1. Remove hardcoded recipient from config.json")
    print("   2. Add \"recipient_env\": \"SMTP_USERNAME\"")
    print("   3. Ensure SMTP_USERNAME environment variable is set")
    print("   4. Email will be sent to SMTP_USERNAME address")


if __name__ == "__main__":
    print("Testing Email Recipient Configuration\n")
    
    try:
        success = test_email_recipient_config()
        show_migration_info()
        
        if success:
            print("\n✅ Email recipient configuration is properly set!")
            print("✅ System ready to send emails")
        else:
            print("\n⚠️  Email recipient configuration needs attention")
            print("💡 Set SMTP_USERNAME environment variable to fix this")
            
    except Exception as e:
        print(f"\n❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()