import asyncio
import logging
from typing import Protocol, runtime_checkable
from class_task import Task

logger = logging.getLogger(__name__)

@runtime_checkable
class Handler(Protocol):
    async def handle(self, task: Task) -> None:
        ...

class NotificationHandler:
    async def handle(self, task: Task) -> None:
        logger.info(f"Start notification for task {task.id}")
        await asyncio.sleep(1)
        logger.info(f"End notification for task {task.id}")

class CalculationHandler:
    async def handle(self, task: Task) -> None:
        logger.info(f"Start calculation for task {task.id}")
        await asyncio.sleep(2)
        logger.info(f"End calculation for task {task.id}")