import requests
import re
import json
from django.conf import settings

import structlog

logger = structlog.get_logger(__name__)


class GlobelabsAPIException(Exception):
    pass


class GlobelabsException(Exception):
    pass


class Globelabs:
    @staticmethod
    def send(mobile: str, message: str):
        if mobile == "" or message == "":
            raise GlobelabsException("mobile and message should not be empty")

        pattern = r"^(0?9|\+?639)\d{9}$"
        match = re.fullmatch(pattern, mobile)
        if not match:
            logger.info("Invalid number format.", mobile_number=mobile)
            raise GlobelabsException("Invalid number format")

        url = settings.GLOBELABS_URL
        payload = {
            "message": message,
            "address": mobile,
            "passphrase": settings.GLOBELABS_PASSPHRASE,
            "app_id": settings.GLOBELABS_APP_ID,
            "app_secret": settings.GLOBELABS_APP_SECRET,
        }

        if not settings.GLOBELABS_APP_ID and not settings.GLOBELABS_APP_SECRET:
            logger.info("SMS module not configured.", message=message, mobile=mobile)
            return

        logger.info("Sending sms message.", message=message, mobile=mobile)
        response = requests.post(url, data=payload)

        if response.status_code == 201:
            logger.info("Sms message successful.", mobile=mobile)
            return response
        else:
            logger.error(
                "Failed to send message.",
                mobile=mobile,
                status_code=response.status_code,
                content=response.content,
            )
            raise GlobelabsAPIException(response.reason)


class M360:
    @staticmethod
    def send(mobile: str, message: str):
        if mobile == "" or message == "":
            raise GlobelabsException("mobile and message should not be empty")

        pattern = r"^(0?9|\+?639)\d{9}$"
        match = re.fullmatch(pattern, mobile)
        if not match:
            logger.info("Invalid number format.", mobile_number=mobile)
            raise GlobelabsException("Invalid number format")

        url = settings.M360_URL + settings.M360_PASSPHRASE
        headers = {"Content-Type": "application/json"}
        payload = {
            "outboundSMSMessageRequest": {
                "clientCorrelator": settings.M360_SHORTCODE,
                "senderAddress": "SARISUKI",
                "outboundSMSTextMessage": {"message": message},
                "address": mobile,
            }
        }

        if not settings.M360_PASSPHRASE and not settings.M360_SHORTCODE:
            logger.info("SMS module not configured.", message=message, mobile=mobile)
            return

        logger.info("Sending sms message.", payload=payload, mobile=mobile)
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 201:
            logger.info("Sms message successful.", mobile=mobile)
            return response
        else:
            logger.error(
                "Failed to send message.",
                mobile=mobile,
                status_code=response.status_code,
                content=response.content,
            )
            raise GlobelabsAPIException(response.reason)
