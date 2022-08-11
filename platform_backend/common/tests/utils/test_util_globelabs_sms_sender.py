import pytest
from platform_backend.common.services.globelabs import (
    Globelabs,
    GlobelabsException,
    GlobelabsAPIException,
)


def test_globelabs_sms_sender(mocker, settings):
    settings.GLOBELABS_APP_ID = "123"
    settings.GLOBELABS_APP_SECRET = "123"
    settings.GLOBELABS_PASSPHRASE = "123"

    sender = Globelabs()
    mock_response = mocker.patch(
        "platform_backend.common.services.globelabs.requests.post"
    )
    mock_response.return_value.status_code = 201
    assert sender.send("09176828777", "Hello Ray!").status_code == 201


def test_no_configured_settings(settings):
    settings.GLOBELABS_APP_ID = None
    settings.GLOBELABS_APP_SECRET = None
    sender = Globelabs()
    assert sender.send("09176828777", "Hello Ray!") is None


def test_globelabs_fail_when_empty_mobile():
    sender = Globelabs()
    with pytest.raises(GlobelabsException):
        sender.send("", "hello world")


def test_globelabs_fail_when_empty_message():
    sender = Globelabs()
    with pytest.raises(GlobelabsException):
        sender.send("09171234567", "")


def test_globelabs_invalid_mobile_format():
    sender = Globelabs()
    with pytest.raises(GlobelabsException):
        sender.send("091712345678", "")
