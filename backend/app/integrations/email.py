import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmailService:
    """Serviço de envio de e-mail via SMTP."""

    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_name = "ImobPro.ai"

    async def send_email(
        self,
        to: str,
        subject: str,
        html_body: str,
        from_email: str | None = None,
    ) -> bool:
        try:
            message = MIMEMultipart("alternative")
            message["From"] = f"{self.from_name} <{from_email or self.user}>"
            message["To"] = to
            message["Subject"] = subject
            message.attach(MIMEText(html_body, "html", "utf-8"))

            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                use_tls=False,
                start_tls=True,
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail para {to}: {e}")
            return False

    async def send_lead_notification(self, to: str, lead_name: str, message: str) -> bool:
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #1a1a2e;">Novo Lead - ImobPro.ai</h2>
            <p><strong>Lead:</strong> {lead_name}</p>
            <p><strong>Mensagem:</strong> {message}</p>
            <hr style="border: 1px solid #e0e0e0;">
            <p style="color: #666; font-size: 12px;">Este é um e-mail automático do ImobPro.ai</p>
        </body>
        </html>
        """
        return await self.send_email(to, f"Novo Lead: {lead_name}", html)

    async def send_follow_up(self, to: str, client_name: str, property_info: str) -> bool:
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #1a1a2e;">Olá, {client_name}!</h2>
            <p>Esperamos que esteja bem. Passando para lembrar do imóvel que você demonstrou interesse:</p>
            <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0;">
                {property_info}
            </div>
            <p>Se tiver alguma dúvida ou quiser agendar uma visita, é só responder este e-mail!</p>
            <p style="color: #666;">Abraços,<br>Equipe ImobPro.ai</p>
        </body>
        </html>
        """
        return await self.send_email(to, f"Lembrete: Imóvel de interesse - {client_name}", html)
