import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

def send_email(receiver_name, receiver_email, items, item_name):
    """
    Sends an email with the top 3 recommended items in a professional template.

    :param receiver_name: Name of the recipient.
    :param receiver_email: Email address of the recipient.
    :param items: List of dictionaries containing item details (name, score, link, price).
    :param item_name: Name of the item requested by the user's machine customer.
    """
    # Get email credentials from environment variables
    sender_email = os.getenv("SMTP_SERVER_USERNAME")
    password = os.getenv("SMTP_SERVER_PASSWORD")

    # Sort items by score in descending order and pick the top 3
    top_items = sorted(items, key=lambda x: x.score, reverse=True)[:3]

    # Create the email message
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"Your Recommendations for {item_name} from Geniecart"

    # Build the HTML email content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="background-color: #4CAF50; color: white; text-align: center; padding: 20px;">
                    <h1 style="margin: 0;">Top Recommendations for {receiver_name}</h1>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px;">
                    <p style="font-size: 16px;">Based on your latest machine customer request for <strong>{item_name}</strong>, here are the top 3 items we think best match your request:</p>
                    <table style="width: 100%; border-collapse: collapse;">
    """
    for item in top_items:
        html_content += f"""
                        <tr style="border-bottom: 1px solid #ddd; padding: 10px;">
                            <td style="width: 150px; text-align: center; padding: 10px;">
                                <img src="{item.image_link}" alt="{item.name}" style="width: 120px; height: auto; border-radius: 5px;">
                            </td>
                            <td style="padding: 10px;">
                                <h2 style="margin: 0; font-size: 18px;">{item.name}</h2>
                                <p style="margin: 5px 0; font-size: 14px;"><strong>Price:</strong> {item.currency} {item.price}</p>
                                <a href="{item.link}" style="color: #4CAF50; text-decoration: none; font-size: 14px;">View Item</a>
                            </td>
                        </tr>
        """

    html_content += """
                    </table>
                    <p style="font-size: 14px; margin-top: 20px;">Thank you for using Geniecart! We’re here to help you find the best products for your needs.</p>
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

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(os.getenv("SMTP_SERVER_HOST"), 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return "Email sent successfully!"

