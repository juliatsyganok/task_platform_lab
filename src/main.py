import asyncio
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
sys.path.append(os.path.join(os.getcwd(), 'src'))

from class_task import Task
from sources import GeneratorTaskSource
from task_queue import TaskQueue
from filters import filt_priority
from executor import Executor
from handlers import NotificationHandler

async def main():
    print("Получаем задачи из источника")
    ffrom = GeneratorTaskSource(count=3, prefix="демо")
    tasks = ffrom.get_tasks()
    for i in tasks:
        print(f"Создана задача: {i.id}")

    print("\nзадачи в list_q и фильтруем")
    list_q = TaskQueue()
    list_q.add_many(tasks)

    list_q.add(Task("важная-1", "Срочно сделать", priority="high"))
    
    print(f"Всего задач в очереди: {len(list_q)}")
    
    pri = list(filt_priority(list_q, "high"))
    print(f"Важных задач найдено: {len(pri)}")

    print("\nАсинхронно выполняем задачи")
    devel = Executor()
    devel.add_handler("high", NotificationHandler())
    devel.add_handler("medium", NotificationHandler())

    async with devel:
        for i in pri:
            print(f"Отправляем на выполнение: {i.id}")
            await devel.add_task(i)
        
        await asyncio.sleep(2)
    

if __name__ == "__main__":
    asyncio.run(main())
