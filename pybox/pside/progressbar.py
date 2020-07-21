"""Test mix asyncio with Qt event loop using crawl example from EdgeDB youtube video on:
https://www.youtube.com/watch?v=-CzqsgaXUM8
"""
# PySide2-5.14 httpx qasync
import asyncio
import typing
import time
import httpx

import contextvars
todovar = contextvars.ContextVar('todovar')
totalvar = contextvars.ContextVar('total')


async def progress(
        url: str, algo: typing.Callable[..., typing.Coroutine], updater=None,
) -> None:
    task = asyncio.create_task(algo(url), name=url)
    todo = todovar.get()
    total = totalvar.get()
    todo.add(task)
    start = time.time()
    while todo:
        done, _pending = await asyncio.wait(todo, timeout=0.1)
        # silly way of calculating total % done?
        total.update(todo)
        if updater and (done_pct:= int(100 - (100.0 / len(total)) * len(todo))) > 0:
            updater(done_pct)
        todo.difference_update(done)
        urls = (t.get_name() for t in todo)
        print(f"{len(todo)}: " + ", ".join(sorted(urls))[-75:])
    end = time.time()
    print(f"Took {int(end - start)} seconds")
    updater(100)  # we finish so set to 100%


async def async_main(*, updater=None) -> None:
    todo = set()
    todovar.set(todo)
    totalvar.set(set())
    try:
        print("Starting progress")
        await progress(addr, crawl, updater=updater)
        print("Progess finished")
    except asyncio.CancelledError:
        print("Cancelling :)")
        for task in todo:
            task.cancel()
        done, pending = await asyncio.wait(todo, timeout=0.1)
        todo.difference_update(done)
        todo.difference_update(pending)
        if todo:
            print("Warning: more tasks adeded while we were cancelling")


async def crawl(prefix:str, url:str = "") -> None:
    url = url or prefix
    client = httpx.AsyncClient()
    todo = todovar.get()
    res = await client.get(url)
    for line in res.text.splitlines():
        if line.startswith(prefix):
            task = asyncio.create_task(crawl(prefix, line), name=line)
            todo.add(task)
    await client.aclose()


addr = "https://langa.pl/crawl"
from PySide2 import QtWidgets, QtCore
from qasync import QEventLoop, asyncSlot, asyncClose

@asyncSlot()
async def on_user_request(widget):
    bar = QtWidgets.QProgressDialog(f"Fetching {addr}...", "Cancel", 0, 0)
    bar.setMaximum(100)
    widget.layout().addWidget(bar)
    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    async def run_me():
        await async_main(updater=bar.setValue)
        QtWidgets.QApplication.restoreOverrideCursor()
    task = asyncio.create_task(run_me())
    bar.setValue(0)
    bar.canceled.connect(task.cancel)
    bar.canceled.connect(QtWidgets.QApplication.restoreOverrideCursor)


if __name__ == '__main__':
    import sys
    from functools import partial
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    label = QtWidgets.QLabel(f"Crawl {addr}")
    button = QtWidgets.QPushButton("Start!")
    layout.addWidget(label)
    layout.addWidget(button)
    button.clicked.connect(partial(on_user_request, widget))
    widget.setLayout(layout)
    widget.show()
    with loop:
        sys.exit(loop.run_forever())
