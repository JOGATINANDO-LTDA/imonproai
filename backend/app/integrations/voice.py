import logging
from typing import Any

from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import Gather, VoiceResponse

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class VoiceService:
    """Serviço de integração de voz/telefone via Twilio."""

    def __init__(self):
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        else:
            self.client = None
            logger.warning("Twilio não configurado. Modo local ativado.")
        self.phone_number = settings.TWILIO_PHONE_NUMBER

    def create_inbound_twiml(
        self, greeting: str = "Olá! Bem-vindo à nossa imobiliária. Como posso ajudar?"
    ) -> str:
        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action="/api/v1/voice/speech-result",
            method="POST",
            timeout=5,
            language="pt-BR",
            speech_timeout="auto",
        )
        gather.say(voice="Pt-BR-FranciscoNeural", language="pt-BR", text=greeting)
        response.append(gather)
        response.redirect("/api/v1/voice/speech-result", method="POST")
        return str(response)

    def create_speech_response(self, text: str, continue_listening: bool = True) -> str:
        response = VoiceResponse()
        if continue_listening:
            gather = Gather(
                input="speech",
                action="/api/v1/voice/speech-result",
                method="POST",
                timeout=5,
                language="pt-BR",
                speech_timeout="auto",
            )
            gather.say(voice="Pt-BR-FranciscoNeural", language="pt-BR", text=text)
            response.append(gather)
            response.redirect("/api/v1/voice/speech-result", method="POST")
        else:
            response.say(voice="Pt-BR-FranciscoNeural", language="pt-BR", text=text)
            response.hangup()
        return str(response)

    def make_call(self, to: str, url: str) -> dict[str, Any]:
        if not self.client:
            raise RuntimeError("Twilio não configurado. Configure TWILIO_ACCOUNT_SID e TWILIO_AUTH_TOKEN.")
        call = self.client.calls.create(
            to=to,
            from_=self.phone_number,
            url=url,
            status_callback="/api/v1/voice/status",
            status_callback_method="POST",
            status_callback_event=["initiated", "ringing", "answered", "completed"],
        )
        return {"call_sid": call.sid, "status": call.status}

    def get_call(self, call_sid: str) -> dict[str, Any]:
        call = self.client.calls(call_sid).fetch()
        return {
            "sid": call.sid,
            "status": call.status,
            "duration": call.duration,
            "start_time": str(call.start_time) if call.start_time else None,
            "end_time": str(call.end_time) if call.end_time else None,
        }

    def create_callback_twiml(self, message: str) -> str:
        response = VoiceResponse()
        response.say(voice="Pt-BR-FranciscoNeural", language="pt-BR", text=message)
        response.hangup()
        return str(response)
