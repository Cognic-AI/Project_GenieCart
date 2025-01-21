import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load environment variables
load_dotenv()

def send_email(receiver_name, receiver_email, items, item_name):
    """
    Sends a purchase receipt email for the bought item.

    :param receiver_name: Name of the recipient.
    :param receiver_email: Email address of the recipient.
    :param items: List containing the purchased item details.
    :param item_name: Name of the purchased item.
    """
    # Get email credentials from environment variables
    sender_email = os.getenv("SMTP_SERVER_USERNAME")
    password = os.getenv("SMTP_SERVER_PASSWORD")

    # Get the purchased item
    purchased_item = items[0]

    # Create the email message
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"Your Purchase Receipt from Geniecart - Order #{hash(item_name) % 10000:04d}"

    # Build the HTML email content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="background-color: #4CAF50; color: white; text-align: center; padding: 20px;">
                    <h1 style="margin: 0;">Purchase Receipt</h1>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px;">
                    <p style="font-size: 16px;">Dear <strong>{receiver_name}</strong>,</p>
                    <p style="font-size: 16px;">Thank you for your purchase! Here are the details of your order:</p>
                    
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <tr style="background-color: #f8f8f8;">
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Item Details</th>
                            <th style="padding: 10px; text-align: right; border-bottom: 2px solid #ddd;">Price</th>
                        </tr>
                        <tr>
                            <td style="padding: 15px; border-bottom: 1px solid #ddd;">
                                <div style="display: flex; align-items: center;">
                                    <img src="{purchased_item.image_link}" alt="{purchased_item.name}" style="width: 100px; height: auto; margin-right: 15px; border-radius: 5px;">
                                    <div>
                                        <h3 style="margin: 0; font-size: 16px;">{purchased_item.name}</h3>
                                        <p style="margin: 5px 0; color: #666;">Product Link: <a href="{purchased_item.link}" style="color: #4CAF50;">View Item</a></p>
                                    </div>
                                </div>
                            </td>
                            <td style="padding: 15px; text-align: right; border-bottom: 1px solid #ddd; font-weight: bold;">
                                {purchased_item.currency} {purchased_item.price}
                            </td>
                        </tr>
                        <tr style="background-color: #f8f8f8;">
                            <td style="padding: 15px; text-align: right; font-weight: bold;">Total:</td>
                            <td style="padding: 15px; text-align: right; font-weight: bold;">
                                {purchased_item.currency} {purchased_item.price}
                            </td>
                        </tr>
                    </table>

                    <div style="background-color: #f8f8f8; padding: 15px; border-radius: 5px; margin-top: 20px;">
                        <h3 style="margin: 0 0 10px 0; color: #333;">Order Information</h3>
                        <p style="margin: 5px 0; font-size: 14px;">Order Number: #{hash(purchased_item.name) % 10000:04d}</p>
                        <p style="margin: 5px 0; font-size: 14px;">Order Date: {datetime.now().strftime('%B %d, %Y')}</p>
                    </div>

                    <p style="font-size: 14px; margin-top: 20px;">If you have any questions about your order, please don't hesitate to contact us.</p>
                </td>
            </tr>
            <tr>
                <td style="background-color: #f1f1f1; text-align: center; padding: 10px; font-size: 12px;">
                    <p style="margin: 0;">&copy; 2024 Geniecart. All rights reserved.</p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Attach the HTML content to the email
    message.attach(MIMEText(html_content, "html"))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(os.getenv("SMTP_SERVER_HOST"), 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return "Purchase receipt email sent successfully!"
    except smtplib.SMTPAuthenticationError:
        raise Exception("Failed to authenticate with SMTP server. Please check your email credentials in the .env file and ensure you're using an App Password if using Gmail.")
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

# For testing - commented out to prevent accidental sends
# send_email("John Doe", "akinduhiman2@gmail.com", [], "Item Name")