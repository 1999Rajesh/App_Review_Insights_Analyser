import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from app.config import settings


class EmailSender:
    """Send weekly digest emails via SMTP"""
    
    def __init__(
        self,
        smtp_server: Optional[str] = None,
        smtp_port: Optional[int] = None,
        sender_email: Optional[str] = None,
        sender_password: Optional[str] = None
    ):
        """
        Initialize email sender.
        
        Args:
            smtp_server: SMTP server address (e.g., smtp.gmail.com)
            smtp_port: SMTP port (465 for SSL, 587 for TLS)
            sender_email: Sender email address
            sender_password: Sender email password or app password
        """
        self.smtp_server = smtp_server or settings.SMTP_SERVER
        self.smtp_port = smtp_port or settings.SMTP_PORT
        self.sender_email = sender_email or settings.SENDER_EMAIL
        self.sender_password = sender_password or settings.SENDER_PASSWORD
    
    def send_weekly_digest(
        self,
        report_content: str,
        recipient_email: Optional[str] = None,
        subject: Optional[str] = None
    ) -> bool:
        """
        Send weekly digest email with the report.
        
        Args:
            report_content: HTML or markdown report content
            recipient_email: Recipient email (defaults to settings.RECIPIENT_EMAIL)
            subject: Email subject line
            
        Returns:
            True if sent successfully
            
        Raises:
            Exception: If email sending fails
        """
        recipient = recipient_email or settings.RECIPIENT_EMAIL
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject or "Weekly App Review Pulse"
        msg['From'] = self.sender_email
        msg['To'] = recipient
        
        # Convert markdown to simple HTML for better rendering
        html_content = self._markdown_to_html(report_content)
        
        # Attach plain text version
        msg.attach(MIMEText(report_content, 'plain', 'utf-8'))
        
        # Attach HTML version
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        try:
            # Send via SMTP
            if self.smtp_port == 465:
                # SSL connection
                with smtplib.SMTP_SSL(
                    self.smtp_server, 
                    self.smtp_port,
                    timeout=10
                ) as server:
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
            else:
                # TLS connection
                with smtplib.SMTP(
                    self.smtp_server, 
                    self.smtp_port,
                    timeout=10
                ) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
            
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            raise Exception(
                f"SMTP authentication failed. Check credentials. Error: {str(e)}"
            )
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
    
    def _markdown_to_html(self, markdown_text: str) -> str:
        """
        Simple markdown to HTML converter for email.
        
        Args:
            markdown_text: Text in markdown format
            
        Returns:
            HTML formatted string
        """
        html = markdown_text
        
        # Headers
        import re
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # Bold
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # Italic
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # Line breaks
        html = html.replace('\n', '<br>\n')
        
        # Horizontal rule
        html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)
        
        # List items
        html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^(\d+)\. (.+)$', r'<li>\2</li>', html, flags=re.MULTILINE)
        
        # Wrap in basic HTML structure
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h1 {{ color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }}
                h2 {{ color: #555; }}
                h3 {{ color: #666; }}
                strong {{ color: #222; }}
                hr {{ border: none; border-top: 1px solid #ddd; margin: 20px 0; }}
                .footer {{ color: #888; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            {html}
            <div class="footer">
                Generated by App Review Insights Analyzer
            </div>
        </body>
        </html>
        """
        
        return html
    
    def test_connection(self) -> bool:
        """
        Test SMTP connection with current settings.
        
        Returns:
            True if connection successful
            
        Raises:
            Exception: If connection fails
        """
        try:
            if self.smtp_port == 465:
                with smtplib.SMTP_SSL(
                    self.smtp_server, 
                    self.smtp_port,
                    timeout=10
                ) as server:
                    server.login(self.sender_email, self.sender_password)
            else:
                with smtplib.SMTP(
                    self.smtp_server, 
                    self.smtp_port,
                    timeout=10
                ) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
            
            return True
            
        except Exception as e:
            raise Exception(f"SMTP connection test failed: {str(e)}")
