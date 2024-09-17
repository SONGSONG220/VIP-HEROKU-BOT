import asyncio
import atexit
import signal
import sys

from pyrogram import idle

from Vivek import app

loop = asyncio.get_event_loop_policy().get_event_loop()


def run_shutdown():
    asyncio.ensure_future(app.stop())


def handle_signal(signal_number, frame):
    run_shutdown()
    loop.stop()
    sys.exit(0)


def handle_exit():
    run_shutdown()


 
async def main():
    atexit.register(handle_exit)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGQUIT, handle_signal)
    await app.start()
    await idle()


if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except Exception as e:
        run_shutdown()
        raise e
