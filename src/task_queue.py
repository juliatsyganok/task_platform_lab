from class_task import Task
from typing import List

class TaskIterator:
    """ИтераторTaskQueue"""
    def __init__(self, tasks: List[Task]) -> None:
        self._tasks = tasks
        self._index = 0

    def __iter__(self) -> "TaskIterator":
        return self

    def __next__(self) -> Task:
        if self._index >= len(self._tasks):
            raise StopIteration
        task = self._tasks[self._index]
        self._index += 1
        return task

class TaskQueue:
    """Коллекция задач"""
    def __init__(self) -> None:
        self._tasks: List[Task] = []

    def __iter__(self) -> TaskIterator:
        """новый итератор"""
        return TaskIterator(list(self._tasks))

    def __len__(self) -> int:
        return len(self._tasks)

    def add(self, task: Task) -> None:
        """Добавить задачу в конец"""
        if not isinstance(task, Task):
            raise TypeError(f"не задача {type(task).__name__}")
        self._tasks.append(task)

    def add_many(self, tasks: List[Task]) -> None:
        """Добавить список задач"""
        for task in tasks:
            self.add(task)

    def remove(self, task_id: str) -> Task:
        """Удалить задачу по id"""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                return self._tasks.pop(i)
        raise KeyError(f"Задача с id={task_id!r} не найдена")

    def get(self, task_id: str) -> Task:
        """Найти задачу по id без удаления"""
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"Задача с id={task_id!r} не найдена")

    @property
    def is_empty(self) -> bool:
        return len(self._tasks) == 0




