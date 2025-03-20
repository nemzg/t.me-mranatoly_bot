import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import Message, User, Chat
from app.handlers.commands import CommandHandlers

@pytest.fixture
def message_mock():
    message = AsyncMock(spec=Message)
    message.chat = MagicMock(spec=Chat)
    message.chat.id = -1001234567890
    message.from_user = MagicMock(spec=User)
    message.from_user.id = 123456789
    message.text = "Test message"
    return message

@pytest.fixture
def bot_mock():
    bot = AsyncMock()
    bot.id = 987654321
    return bot

@pytest.fixture
def db_pool_mock():
    pool = AsyncMock()
    conn = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    conn.fetchval.return_value = 1
    return pool

@pytest.mark.asyncio
async def test_command_start(message_mock, bot_mock, db_pool_mock):
    # Подготовка
    message_mock.reply = AsyncMock(return_value=MagicMock(message_id=1))
    command_handlers = CommandHandlers(bot_mock, db_pool_mock)
    
    # Действие
    await command_handlers.command_start(message_mock)
    
    # Проверка
    message_mock.reply.assert_called_once()
    assert "Привет, я бот версии" in message_mock.reply.call_args[0][0]

@pytest.mark.asyncio
async def test_command_version(message_mock, bot_mock, db_pool_mock):
    # Подготовка
    message_mock.reply = AsyncMock(return_value=MagicMock(message_id=1))
    command_handlers = CommandHandlers(bot_mock, db_pool_mock)
    
    # Действие
    await command_handlers.command_version(message_mock)
    
    # Проверка
    message_mock.reply.assert_called_once()
    assert "Версия бота:" in message_mock.reply.call_args[0][0]

@pytest.mark.asyncio
async def test_check_database_health(bot_mock, db_pool_mock):
    # Подготовка
    command_handlers = CommandHandlers(bot_mock, db_pool_mock)
    
    # Действие
    result = await command_handlers.check_database_health()
    
    # Проверка
    assert result is True
    db_pool_mock.acquire.assert_called_once()