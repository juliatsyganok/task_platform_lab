import asyncio
import logging
from typing import Dict
from class_task import Task
from handlers import Handler

logger = logging.getLogger(__name__)

class Executor:
    def __init__(self):
        self.queue: asyncio.Queue[Task] = asyncio.Queue()
        self.handlers: Dict[str, Handler] = {}
        self.tasks = []
        self.running = False

    def add_handler(self, priority: str, handler: Handler) -> None:
        if not isinstance(handler, Handler):
            raise TypeError("Object is not a Handler")
        self.handlers[priority] = handler

    async def add_task(self, task: Task) -> None:
        await self.queue.put(task)

    async def _worker(self):
        while self.running or not self.queue.empty():
            try:
                task = await asyncio.wait_for(self.queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                continue

            handler = self.handlers.get(task.priority)
            if handler:
                try:
                    await handler.handle(task)
                except Exception as error:
                    logger.error(f"Error in task {task.id}: {error}")
            
            self.queue.task_done()

    async def __aenter__(self):
        self.running = True
        self.tasks = [
            asyncio.create_task(self._worker()),
            asyncio.create_task(self._worker())
        ]
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if not self.queue.empty():
            await self.queue.join()
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
