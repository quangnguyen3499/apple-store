import pytest
from platform_backend.common.services.globelabs import (
    M360,
    GlobelabsException,
    GlobelabsAPIException,
)

def test_globelabs_sms_sender(mocker, settings):
    settings.M360_PASSPHRASE = "123"
    settings.M360_SHORTCODE = "123"

    sender = M360()
    mock_response = mocker.patch(
        "platform_backend.common.services.globelabs.requests.post"
    )
    mock_response.return_value.status_code = 201
    assert sender.send("09176828777", "Hello Ray!").status_code == 201


def test_no_configured_settings(settings):
    settings.M360_PASSPHRASE = ""
    settings.M360_SHORTCODE = ""
    sender = M360()
    assert sender.send("09176828777", "Hello Ray!") is None


def test_globelabs_fail_when_empty_mobile():
    sender = M360()
    with pytest.raises(GlobelabsException):
        sender.send("", "hello world")


def test_globelabs_fail_when_empty_message():
    sender = M360()
    with pytest.raises(GlobelabsException):
        sender.send("09171234567", "")


def test_globelabs_invalid_mobile_format():
    sender = M360()
    with pytest.raises(GlobelabsException):
        sender.send("091712345678", "")
