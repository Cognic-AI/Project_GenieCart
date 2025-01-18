import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

def send_secret_email(receiver_email, generated_key,name):
    # Get email credentials from environment variables
    sender_email = os.getenv("SMTP_SERVER_USERNAME")
    password = os.getenv("SMTP_SERVER_PASSWORD")

    # Create the email message
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"Welcome to GenieCart!, {name}"

    # Build the HTML email content
    html_content = f"""
     
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
            <table width="100%" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px;">
              <tr>
                <td style="text-align: center; padding: 10px 0;">
                  <h1 style="font-size: 24px; color: #333;">Welcome to GenieCart</h1>
                </td>
              </tr>
              <tr>
                <td style="padding: 20px; text-align: center;">
                  <p style="font-size: 16px; color: #555;">
                    We're excited to have you onboard! Below is your secret key that you'll use to configure your devices:
                  </p>
                  <h2 style="font-size: 20px; color: #4CAF50; margin-top: 20px;">Secret Key: <strong>{generated_key}</strong></h2>
                  <p style="font-size: 14px; color: #777; margin-top: 10px;">
                    Please keep your key secure and use it to set up your devices as needed.
                  </p>
                </td>
              </tr>
              <tr>
                <td style="padding: 20px; text-align: center; background-color: #f1f1f1; border-radius: 8px;">
                  <p style="font-size: 12px; color: #777;">
                    &copy; 2024 GenieCart. All rights reserved.
                  </p>
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
        return "Email sent successfully!"
    except smtplib.SMTPAuthenticationError:
        raise Exception("Failed to authenticate with SMTP server. Please check your email credentials in the .env file and ensure you're using an App Password if using Gmail.")
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

# For testing - commented out to prevent accidental sends
# send_email("John Doe", "akinduhiman2@gmail.com", [], "Item Name")