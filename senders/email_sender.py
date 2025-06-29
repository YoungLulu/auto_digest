import smtplib
import yagmail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict, Any
import os


class EmailSender:
    def __init__(self, smtp_config: Dict[str, Any] = None):
        """
        Initialize email sender with SMTP configuration.
        
        Args:
            smtp_config: Dict with keys: host, port, username, password, use_tls
        """
        self.smtp_config = smtp_config or self._get_default_config()
        self.yag = None
        
        # Try to initialize yagmail if possible
        try:
            if self.smtp_config.get('username') and self.smtp_config.get('password'):
                self.yag = yagmail.SMTP(
                    self.smtp_config['username'], 
                    self.smtp_config['password']
                )
        except Exception as e:
            print(f"Could not initialize yagmail: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default SMTP configuration from environment variables."""
        return {
            'host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
            'port': int(os.getenv('SMTP_PORT', '587')),
            'username': os.getenv('SMTP_USERNAME', ''),
            'password': os.getenv('SMTP_PASSWORD', ''),
            'use_tls': os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
        }
    
    def send_digest_email(self, 
                         to_email: str,
                         subject: str,
                         html_content: str,
                         attachments: List[str] = None,
                         date_str: str = None) -> bool:
        """
        Send digest email with optional attachments.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            attachments: List of file paths to attach
            date_str: Date string for subject formatting
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        # Always use smtplib for QQ email (yagmail has issues with QQ)
        return self._send_with_smtplib(to_email, subject, html_content, attachments)
    
    def _send_with_yagmail(self, 
                          to_email: str, 
                          subject: str, 
                          html_content: str, 
                          attachments: List[str] = None) -> bool:
        """Send email using yagmail (simpler approach)."""
        try:
            contents = [html_content]
            
            if attachments:
                for attachment_path in attachments:
                    if Path(attachment_path).exists():
                        contents.append(attachment_path)
            
            self.yag.send(
                to=to_email,
                subject=subject,
                contents=contents
            )
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email with yagmail: {e}")
            return False
    
    def _send_with_smtplib(self, 
                          to_email: str, 
                          subject: str, 
                          html_content: str, 
                          attachments: List[str] = None) -> bool:
        """Send email using standard smtplib."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Add attachments
            if attachments:
                for attachment_path in attachments:
                    if Path(attachment_path).exists():
                        self._add_attachment(msg, attachment_path)
            
            # Send email
            if self.smtp_config['port'] == 465:
                # Use SSL for port 465
                server = smtplib.SMTP_SSL(self.smtp_config['host'], self.smtp_config['port'])
            else:
                # Use TLS for port 587
                server = smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port'])
                server.ehlo()
                if self.smtp_config['use_tls']:
                    server.starttls()
                    server.ehlo()
            
            # Login and send
            if self.smtp_config['username'] and self.smtp_config['password']:
                server.login(self.smtp_config['username'], self.smtp_config['password'])
            
            text = msg.as_string()
            server.sendmail(self.smtp_config['username'], to_email, text)
            server.quit()
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email with smtplib: {e}")
            return False
    
    def _add_attachment(self, msg: MIMEMultipart, file_path: str):
        """Add file attachment to email message."""
        path = Path(file_path)
        
        with open(path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {path.name}'
        )
        
        msg.attach(part)
    
    def send_daily_digest(self, 
                         to_email: str,
                         report_files: Dict[str, str],
                         date_str: str,
                         summary_stats: Dict[str, Any] = None) -> bool:
        """
        Send daily digest email with report files.
        
        Args:
            to_email: Recipient email address
            report_files: Dict of format -> file_path
            date_str: Date string for the digest
            summary_stats: Optional summary statistics
            
        Returns:
            bool: True if sent successfully
        """
        subject = f"🧠 AI Coding Digest - {date_str}"
        
        # Read HTML content if available
        html_content = ""
        if "html" in report_files and Path(report_files["html"]).exists():
            with open(report_files["html"], 'r', encoding='utf-8') as f:
                html_content = f.read()
        else:
            # Fallback content
            html_content = self._create_fallback_html_content(date_str, summary_stats)
        
        # Prepare attachments (exclude HTML since it's the main content)
        attachments = []
        for format_type, file_path in report_files.items():
            if format_type != "html" and Path(file_path).exists():
                attachments.append(file_path)
        
        return self.send_digest_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            attachments=attachments,
            date_str=date_str
        )
    
    def _create_fallback_html_content(self, date_str: str, summary_stats: Dict[str, Any] = None) -> str:
        """Create fallback HTML content when main HTML report is not available."""
        stats_html = ""
        if summary_stats:
            stats_html = f"""
            <p><strong>Summary Statistics:</strong></p>
            <ul>
                <li>Total Items: {summary_stats.get('total_items', 'N/A')}</li>
                <li>Sources: {summary_stats.get('sources', 'N/A')}</li>
                <li>Categories: {summary_stats.get('categories', 'N/A')}</li>
            </ul>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Coding Digest - {date_str}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
                h1 {{ color: #333; border-bottom: 2px solid #007acc; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
            </style>
        </head>
        <body>
            <h1>🧠 AI Coding Digest - {date_str}</h1>
            <p>Your daily digest of AI coding research and tools.</p>
            
            {stats_html}
            
            <p>Please find the detailed reports in the attached files.</p>
            
            <div class="footer">
                <p>Generated by AI Coding Digest System</p>
                <p>Powered by Claude Code</p>
            </div>
        </body>
        </html>
        """


if __name__ == "__main__":
    # Test email sender
    sender = EmailSender()
    
    test_html = """
    <html>
    <body>
        <h1>Test AI Coding Digest</h1>
        <p>This is a test email.</p>
    </body>
    </html>
    """
    
    # This would need actual email configuration to work
    print("Email sender initialized. Configure SMTP settings in environment variables to send emails.")
    print("Required environment variables:")
    print("- SMTP_HOST")
    print("- SMTP_PORT")
    print("- SMTP_USERNAME")
    print("- SMTP_PASSWORD")
    print("- SMTP_USE_TLS")