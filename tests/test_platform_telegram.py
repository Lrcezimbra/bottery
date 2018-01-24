import pytest

from bottery.message import Message
from bottery.platform.telegram.engine import (TelegramChat, TelegramEngine,
                                              TelegramUser)


@pytest.fixture
def engine():
    return TelegramEngine


@pytest.fixture
def user():
    return TelegramUser


@pytest.fixture
def chat():
    return TelegramChat


@pytest.fixture()
def message():
    return Message(
        id='',
        platform='',
        text='',
        user=user,
        chat=chat,
        timestamp='',
        raw='',
    )


@pytest.fixture()
def data_message():
    return {
        'message': {
            'chat': {
                'first_name': 'Lucas',
                'id': 12345678,
                'last_name': 'Rangel Cezimbra',
                'type': 'private',
                'username': 'Lrcezimbra'
            },
            'date': 1516787847,
            'from': {
                'first_name': 'Lucas',
                'id': 12345678,
                'is_bot': False,
                'language_code': 'en-US',
                'last_name': 'Rangel Cezimbra',
                'username': 'Lrcezimbra'
            },
            'message_id': 2,
            'text': 'Hi bot, how are you?'
        },
        'update_id': 987456321
    }


@pytest.mark.parametrize('chat_type,id_expected', [
    ('group', 456),
    ('private', 123),
])
def test_platform_telegram_engine_get_chat_id(chat_type,
                                              id_expected, engine, message):
    setattr(message.chat, 'id', id_expected)
    setattr(message.chat, 'type', chat_type)
    setattr(message.user, 'id', id_expected)
    assert engine.get_chat_id(engine, message) == id_expected


def test_build_message(engine, data_message, user, chat):
    message_data = data_message['message']

    message = engine.build_message(engine, data_message)

    assert message.id == message_data['message_id']
    assert message.text == message_data['text']
    assert message.timestamp == message_data['date']
    assert message.raw == data_message


def test_build_message_without_text(data_message, engine):
    '''
    Telegram can send a message without text.
    For example, when a bot is added to a group.
    '''
    message_data_without_text = data_message['message']
    del message_data_without_text['text']

    message = engine.build_message(engine, data_message)

    assert message.id == message_data_without_text['message_id']
    assert message.text is not None
    assert message.text == ''
    assert message.timestamp == message_data_without_text['date']
    assert message.raw == data_message
