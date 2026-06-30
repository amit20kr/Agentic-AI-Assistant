import threading
from typing import Optional, Tuple

_counter = 0
_lock = threading.Lock()

def get_next_key_pair(num_keys: int, need_brain: bool = True) -> Tuple[Optional[int], int]:
    """Return (brain_key_index, chat_key_index) with round-robin rotation.

    When need_brain is True and there are 2+ keys, brain and chat use
    different keys to avoid rate-limiting collisions. The starting index
    advances on every call for true load balancing.
    """
    global _counter

    if num_keys <= 0:
        return (None, 0)

    if not need_brain:
        with _lock:
            _counter += 1
            idx = _counter % num_keys
        return (None, idx)

    with _lock:
        _counter += 1
        brain_idx = _counter % num_keys

    if num_keys <= 1:
        return (brain_idx, brain_idx)

    chat_idx = (brain_idx + 1) % num_keys
    return (brain_idx, chat_idx)
