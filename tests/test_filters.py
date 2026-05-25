import pytest
from class_task import Task
from task_queue import TaskQueue
from filters import filt_status, filt_priority, filt_ready, filt_all, take

def test_task_queue_basic():
    tq = TaskQueue()
    assert len(tq) == 0
    assert tq.is_empty

    t1 = Task("1", "Task 1", priority="high")
    t2 = Task("2", "Task 2", priority="low")

    tq.add(t1)
    assert len(tq) == 1
    assert not tq.is_empty

    tq.add_many([t2])
    assert len(tq) == 2

    assert tq.get("1") == t1
    assert tq.get("2") == t2

    with pytest.raises(KeyError):
        tq.get("3")

    removed = tq.remove("1")
    assert removed == t1
    assert len(tq) == 1

    with pytest.raises(KeyError):
        tq.remove("1")

    with pytest.raises(TypeError):
        tq.add("not a task")

def test_task_queue_iteration():
    tq = TaskQueue()
    tasks = [Task(str(i), f"Task {i}") for i in range(3)]
    tq.add_many(tasks)

    iterated = list(tq)
    assert iterated == tasks

    # Repeatable iteration
    iterated2 = list(tq)
    assert iterated2 == tasks

def test_filters():
    tasks = [
        Task("1", "T1", priority="high", status="new"),
        Task("2", "T2", priority="medium", status="in_progress"),
        Task("3", "T3", priority="low", status="done"),
    ]

    assert len(list(filt_status(tasks, "new"))) == 1
    assert len(list(filt_status(tasks, "in_progress"))) == 1
    assert len(list(filt_status(tasks, "done"))) == 1
    with pytest.raises(ValueError):
        list(filt_status(tasks, "invalid"))

    assert len(list(filt_priority(tasks, "high"))) == 1
    assert len(list(filt_priority(tasks, "medium"))) == 1
    assert len(list(filt_priority(tasks, "low"))) == 1
    with pytest.raises(ValueError):
        list(filt_priority(tasks, "invalid"))

    # is_ready: status != done and priority != low
    # T1: high, new -> ready
    # T2: medium, in_progress -> ready
    # T3: low, done -> not ready
    ready = list(filt_ready(tasks))
    assert len(ready) == 2
    assert "3" not in [t.id for t in ready]

    filtered_all = list(filt_all(tasks, "new", "high"))
    assert len(filtered_all) == 1
    assert filtered_all[0].id == "1"

def test_take():
    tasks = [Task(str(i), f"Task {i}") for i in range(5)]
    taken = list(take(tasks, 3))
    assert len(taken) == 3
    assert [t.id for t in taken] == ["0", "1", "2"]

    taken_more = list(take(tasks, 10))
    assert len(taken_more) == 5
