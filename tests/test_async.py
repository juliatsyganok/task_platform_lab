import sys
import pytest 
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import asyncio
from class_task import Task
from handlers import NotificationHandler, CalculationHandler
from executor import Executor


pytestmark = pytest.mark.asyncio


async def test_init_notify():
    handler = NotificationHandler()
    assert handler is not None


async def test_init_calc():
    handler = CalculationHandler()
    assert handler is not None


async def test_init_exec():
    executor = Executor()
    assert executor.running is False
    assert executor.queue.empty() is True


async def test_add_task():
    executor = Executor()
    task = Task("1", "Test", prior="high")
    await executor.add_task(task)
    assert executor.queue.qsize() == 1


async def test_add_handler():
    executor = Executor()
    handler = NotificationHandler()
    executor.add_handler("high", handler)
    assert "high" in executor.handlers
    assert executor.handlers["high"] == handler


async def test_bad_handler():
    executor = Executor()
    with pytest.raises(TypeError):
        executor.add_handler("high", "not_a_handler")


async def test_context():
    executor = Executor()
    async with executor:
        assert executor.running is True
        assert len(executor.tasks) == 2
    assert executor.running is False


async def test_run_notify():
    executor = Executor()
    executor.add_handler("high", NotificationHandler())
    task = Task("2", "Test notify", prior="high")
    async with executor:
        await executor.add_task(task)
        await asyncio.sleep(1.2)
    assert executor.queue.empty() is True


async def test_run_calc():
    executor = Executor()
    executor.add_handler("medium", CalculationHandler())
    task = Task("3", "Test calc", prior="medium")
    async with executor:
        await executor.add_task(task)
        await asyncio.sleep(2.2)
    assert executor.queue.empty() is True


async def test_no_handler():
    executor = Executor()
    executor.add_handler("high", NotificationHandler())
    task = Task("4", "Test no handler", prior="low")
    async with executor:
        await executor.add_task(task)
        await asyncio.sleep(0.6)
    assert executor.queue.empty() is True