#!/usr/bin/env python3
"""
Simple script to send existing reports from outputs/ directory via email
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from senders.email_sender import EmailSender

def find_latest_reports():
    """Find the most recent reports in outputs directory."""
    outputs_dir = Path("outputs")
    if not outputs_dir.exists():
        print("❌ No outputs directory found")
        return None
    
    # Find all report files
    report_files = {}
    latest_date = None
    
    for file_path in outputs_dir.glob("daily_*.json"):
        date_str = file_path.stem.replace("daily_", "")
        try:
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if latest_date is None or file_date > latest_date:
                latest_date = file_date
                latest_date_str = date_str
        except ValueError:
            continue
    
    if latest_date is None:
        print("❌ No valid report files found in outputs/")
        return None
    
    # Collect all formats for the latest date
    for format_type in ["json", "markdown", "html", "pdf"]:
        if format_type == "markdown":
            file_path = outputs_dir / f"daily_{latest_date_str}.md"
        else:
            file_path = outputs_dir / f"daily_{latest_date_str}.{format_type}"
        
        if file_path.exists():
            report_files[format_type] = str(file_path)
    
    return latest_date_str, report_files

def get_summary_stats(json_file_path):
    """Extract summary statistics from JSON report."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {
            "total_items": data.get("total_items", 0),
            "sources": data.get("sources", {}),
            "categories": data.get("categories", {})
        }
    except Exception as e:
        print(f"Warning: Could not read summary stats: {e}")
        return {"total_items": "Unknown", "sources": "Unknown", "categories": "Unknown"}

def send_existing_reports():
    """Send existing reports via email."""
    print("📧 Sending Existing Reports")
    print("-" * 40)
    
    # Find latest reports
    result = find_latest_reports()
    if result is None:
        return False
    
    date_str, report_files = result
    print(f"📅 Found reports for date: {date_str}")
    print(f"📄 Available formats: {list(report_files.keys())}")
    
    # Get summary statistics
    summary_stats = None
    if "json" in report_files:
        summary_stats = get_summary_stats(report_files["json"])
        print(f"📊 Total items: {summary_stats['total_items']}")
        print(f"📊 Sources: {summary_stats['sources']}")
    
    # Initialize email sender
    sender = EmailSender()
    
    # Send email
    print(f"\n📤 Sending reports to 873425118@qq.com...")
    
    success = sender.send_daily_digest(
        to_email="873425118@qq.com",
        report_files=report_files,
        date_str=date_str,
        summary_stats=summary_stats
    )
    
    if success:
        print("✅ Reports sent successfully!")
        print(f"📎 Attachments included:")
        for format_type, file_path in report_files.items():
            if format_type != "html":  # HTML is used as email body
                file_size = Path(file_path).stat().st_size
                print(f"   - {format_type.upper()}: {Path(file_path).name} ({file_size:,} bytes)")
        return True
    else:
        print("❌ Failed to send reports")
        return False

def main():
    print("🧠 AI Coding Digest - Send Reports")
    print("=" * 50)
    
    # Check if outputs directory exists
    if not Path("outputs").exists():
        print("❌ No outputs directory found. Run the digest system first:")
        print("   python runner.py --dry-run")
        return
    
    # Check environment variables
    required_vars = ['SMTP_HOST', 'SMTP_USERNAME', 'SMTP_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Make sure to source your .env file:")
        print("   source .env")
        return
    
    # Send reports
    success = send_existing_reports()
    
    if success:
        print("\n🎉 Email sent successfully!")
    else:
        print("\n❌ Email sending failed. Check your SMTP configuration.")
        print("Test email settings with: python test_email.py")

if __name__ == "__main__":
    main()