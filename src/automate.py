"""The automation features"""

import threading
from time import sleep
from pynput.keyboard import Listener

# import sys
import pyautogui as pag

pag.FAILSAFE = True  # Default but better be safe lol


def auto_forge(delay: float = 1.0, dismantle=False) -> int:
    """Automates the Forging, returns Status Code for Display"""
    stop_event = threading.Event()
    status_code = 2

    def on_press(key):
        """For pynput keyboard listener"""
        if "esc" in str(key):
            stop_event.set()
            return False
        return None

    ### Get the positions of the Buttons based on Screen Size
    screen_w, screen_h = pag.size()

    # pos_arsenal1 = (screen_w * (1 / 2), screen_h * (53 / 64))
    # pos_arsenal2 = (screen_w * (1 / 2), screen_h * (58 / 64))
    pos_forge = (screen_w * (1 / 2), screen_h * (55 / 64))
    pos_anvil = (screen_w * (1 / 2), screen_h * (28 / 64))
    pos_dagger = (screen_w * (15 / 64), screen_h * (24 / 64))
    pos_center = (screen_w * (1 / 2), screen_h * (40 / 64))

    ### Time to Focus AOW4 Window but click into it just in case
    sleep(1)
    pag.moveTo(pos_center[0], pos_center[1])
    pag.click()

    def forge_loop():
        """The Forging Loop"""
        nonlocal status_code
        try:
            for _ in range(3):
                if stop_event.is_set():
                    status_code = -1
                    break

                pag.moveTo(pos_anvil[0], pos_anvil[1], delay)
                if stop_event.is_set():
                    status_code = -1
                    break
                # pag.click()

                pag.moveTo(pos_dagger[0], pos_dagger[1], delay)
                if stop_event.is_set():
                    status_code = -1
                    break
                # pag.click()

                pag.moveTo(pos_forge[0], pos_forge[1], delay)
                if stop_event.is_set():
                    status_code = -1
                    break
                # pag.click()

        except KeyboardInterrupt, pag.FailSafeException:
            stop_event.set()
            status_code = -1
            return -1

        finally:
            stop_event.set()

        return 2

    forge_thread = threading.Thread(target=forge_loop)
    forge_thread.start()

    with Listener(on_press=on_press) as _listener:
        stop_event.wait()

    forge_thread.join()

    return status_code


if __name__ == "__main__":
    print(auto_forge())
