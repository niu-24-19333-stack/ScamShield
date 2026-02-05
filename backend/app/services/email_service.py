"""
email_service.py - Email service for sending transactional emails
Uses SMTP for sending password reset and verification emails
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Service for sending transactional emails.
    """
    
    @staticmethod
    def _get_smtp_connection():
        """Create SMTP connection."""
        if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            return None
        
        try:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            return server
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            return None
    
    @staticmethod
    def send_email(to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
        """
        Send an email.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML body
            text_content: Plain text body (optional)
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            server = EmailService._get_smtp_connection()
            if not server:
                logger.warning("Email not configured - skipping email send")
                return False
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
            msg['To'] = to_email
            
            # Attach plain text version
            if text_content:
                msg.attach(MIMEText(text_content, 'plain'))
            
            # Attach HTML version
            msg.attach(MIMEText(html_content, 'html'))
            
            server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, msg.as_string())
            server.quit()
            
            logger.info(f"Email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    @staticmethod
    def send_password_reset_email(to_email: str, reset_token: str, user_name: str = None) -> bool:
        """
        Send password reset email.
        
        Args:
            to_email: User's email address
            reset_token: Password reset token
            user_name: User's name (optional)
            
        Returns:
            True if sent successfully
        """
        reset_url = f"{settings.FRONTEND_URL}/reset-password.html?token={reset_token}"
        
        name = user_name or to_email.split('@')[0]
        
        subject = "Reset Your ScamShield Password"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                <tr>
                    <td style="padding: 40px 30px; text-align: center; background: linear-gradient(135deg, #0A0A0A 0%, #1a1a1a 100%);">
                        <h1 style="color: #ffffff; margin: 0; font-size: 28px;">
                            <span style="color: #C41E3A;">Scam</span>Shield
                        </h1>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 40px 30px;">
                        <h2 style="color: #333333; margin: 0 0 20px 0; font-size: 24px;">Reset Your Password</h2>
                        <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                            Hi {name},
                        </p>
                        <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                            We received a request to reset your password. Click the button below to create a new password:
                        </p>
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="text-align: center;">
                                    <a href="{reset_url}" style="display: inline-block; padding: 16px 40px; background-color: #C41E3A; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                                        Reset Password
                                    </a>
                                </td>
                            </tr>
                        </table>
                        <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 30px 0 0 0;">
                            This link will expire in <strong>1 hour</strong>.
                        </p>
                        <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 10px 0 0 0;">
                            If you didn't request this, you can safely ignore this email.
                        </p>
                        <hr style="border: none; border-top: 1px solid #eeeeee; margin: 30px 0;">
                        <p style="color: #999999; font-size: 12px; line-height: 1.6; margin: 0;">
                            If the button doesn't work, copy and paste this link:<br>
                            <a href="{reset_url}" style="color: #C41E3A; word-break: break-all;">{reset_url}</a>
                        </p>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 20px 30px; text-align: center; background-color: #f9f9f9;">
                        <p style="color: #999999; font-size: 12px; margin: 0;">
                            © 2026 ScamShield Pro. Protecting you from scams.
                        </p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        text_content = f"""
        Reset Your ScamShield Password
        
        Hi {name},
        
        We received a request to reset your password. 
        Click this link to create a new password:
        
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request this, you can safely ignore this email.
        
        - ScamShield Team
        """
        
        return EmailService.send_email(to_email, subject, html_content, text_content)
    
    @staticmethod
    def send_verification_email(to_email: str, verification_token: str, user_name: str = None) -> bool:
        """
        Send email verification email.
        
        Args:
            to_email: User's email address
            verification_token: Email verification token
            user_name: User's name (optional)
            
        Returns:
            True if sent successfully
        """
        verify_url = f"{settings.FRONTEND_URL}/verify-email.html?token={verification_token}"
        
        name = user_name or to_email.split('@')[0]
        
        subject = "Verify Your ScamShield Account"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                <tr>
                    <td style="padding: 40px 30px; text-align: center; background: linear-gradient(135deg, #0A0A0A 0%, #1a1a1a 100%);">
                        <h1 style="color: #ffffff; margin: 0; font-size: 28px;">
                            <span style="color: #C41E3A;">Scam</span>Shield
                        </h1>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 40px 30px;">
                        <h2 style="color: #333333; margin: 0 0 20px 0; font-size: 24px;">Verify Your Email</h2>
                        <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                            Hi {name},
                        </p>
                        <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                            Welcome to ScamShield! Please verify your email address by clicking the button below:
                        </p>
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="text-align: center;">
                                    <a href="{verify_url}" style="display: inline-block; padding: 16px 40px; background-color: #C41E3A; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                                        Verify Email
                                    </a>
                                </td>
                            </tr>
                        </table>
                        <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 30px 0 0 0;">
                            If you didn't create an account, you can safely ignore this email.
                        </p>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 20px 30px; text-align: center; background-color: #f9f9f9;">
                        <p style="color: #999999; font-size: 12px; margin: 0;">
                            © 2026 ScamShield Pro. Protecting you from scams.
                        </p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        text_content = f"""
        Verify Your ScamShield Account
        
        Hi {name},
        
        Welcome to ScamShield! Please verify your email address by clicking this link:
        
        {verify_url}
        
        If you didn't create an account, you can safely ignore this email.
        
        - ScamShield Team
        """
        
        return EmailService.send_email(to_email, subject, html_content, text_content)
    
    @staticmethod
    def send_welcome_email(to_email: str, user_name: str = None) -> bool:
        """
        Send welcome email after registration.
        """
        name = user_name or to_email.split('@')[0]
        login_url = f"{settings.FRONTEND_URL}/login.html"
        
        subject = "Welcome to ScamShield Pro!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                <tr>
                    <td style="padding: 40px 30px; text-align: center; background: linear-gradient(135deg, #0A0A0A 0%, #1a1a1a 100%);">
                        <h1 style="color: #ffffff; margin: 0; font-size: 28px;">
                            <span style="color: #C41E3A;">Scam</span>Shield
                        </h1>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 40px 30px;">
                        <h2 style="color: #333333; margin: 0 0 20px 0; font-size: 24px;">Welcome to ScamShield! 🛡️</h2>
                        <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                            Hi {name},
                        </p>
                        <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                            Thank you for joining ScamShield Pro! You now have access to advanced AI-powered scam detection and protection.
                        </p>
                        <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                            <strong>What you can do:</strong>
                        </p>
                        <ul style="color: #666666; font-size: 16px; line-height: 1.8; margin: 0 0 30px 20px; padding: 0;">
                            <li>Scan suspicious messages instantly</li>
                            <li>View detailed threat analysis</li>
                            <li>Track your scan history</li>
                            <li>Get real-time protection alerts</li>
                        </ul>
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="text-align: center;">
                                    <a href="{login_url}" style="display: inline-block; padding: 16px 40px; background-color: #C41E3A; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                                        Go to Dashboard
                                    </a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 20px 30px; text-align: center; background-color: #f9f9f9;">
                        <p style="color: #999999; font-size: 12px; margin: 0;">
                            © 2026 ScamShield Pro. Protecting you from scams.
                        </p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to ScamShield! 🛡️
        
        Hi {name},
        
        Thank you for joining ScamShield Pro! You now have access to advanced AI-powered scam detection and protection.
        
        What you can do:
        - Scan suspicious messages instantly
        - View detailed threat analysis
        - Track your scan history
        - Get real-time protection alerts
        
        Get started: {login_url}
        
        - ScamShield Team
        """
        
        return EmailService.send_email(to_email, subject, html_content, text_content)
