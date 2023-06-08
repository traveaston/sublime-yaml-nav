"""
Utility functions.
"""

from queue import Queue
import threading
import sublime


# Main sublime thread
MAIN_THREAD = threading.current_thread()


def execute_in_sublime_main_thread(callback):
    """
    Executes callback in main sublime thread and returns its result.
    This is needed to mitigate memory leak in plugin_host.
    See https://github.com/DamnWidget/anaconda/issues/97
    """

    if threading.current_thread() == MAIN_THREAD:
        # If we already in the main thread then execute callback immediately
        return callback()

    # Schedule callback in the main thread and block current thread
    q = Queue()
    sublime.set_timeout(lambda: q.put(callback()), 0)
    return q.get(block=True)
