// pages/api/send-email.js
import nodemailer from 'nodemailer';

export const send_mail = async (req, res) => {
    if (req.method === 'POST') {
        const { to, subject, text, html } = req.body;

        // Create a transporter using your SMTP configuration
        const transporter = nodemailer.createTransport({
            host: process.env.SMTP_SERVER_HOST, // Example: Gmail SMTP host or any provider
            port: 587, // Standard SMTP port
            secure: false, // Use TLS
            auth: {
                user: process.env.SMTP_SERVER_USERNAME, // Your email address
                pass: process.env.SMTP_SERVER_PASSWORD, // Your email password or App password
            },
        });

        // Email options
        const mailOptions = {
            from: process.env.SMTP_SERVER_USERNAME, // Sender address
            to, // Receiver address
            subject, // Email subject
            text, // Plaintext body
            html, // HTML body
        };

        try {
            // Send email
            await transporter.sendMail(mailOptions);
            res.status(200).json({ message: 'Email sent successfully!' });
        } catch (error) {
            res.status(500).json({ message: 'Failed to send email', error: error.message });
        }
    } else {
        res.status(405).json({ message: 'Method Not Allowed' });
    }
};
