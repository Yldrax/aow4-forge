"""The automation features"""

import threading
from time import sleep
from pynput.keyboard import Listener

import pyautogui as pag

pag.FAILSAFE = True  # Default but better be safe


def auto_forge(speed: int = 3, disenchant: bool = False) -> int:
    """Automates the Forging, returns Status Code for Display"""
    status_code = 2

    ### For Interrupting the Thread
    stop_event = threading.Event()

    ### For switching between forging and dismantling
    essence_empty = False
    forged = False
    arsenal_empty = False
    disenchanted = False

    ### Get the positions of the Buttons based on Screen Size
    screen_w, screen_h = pag.size()

    pos_arsenal = (screen_w * (28 / 64), screen_h * (58 / 64))
    pos_forge = (screen_w * (1 / 2), screen_h * (55 / 64))
    pos_anvil = (screen_w * (1 / 2), screen_h * (28 / 64))

    pos_dagger = (screen_w * (14 / 64), screen_h * (26 / 64))
    pos_disenchant = (screen_w * (21 / 128), screen_h * (111 / 128))
    pos_arsenal_1 = (screen_w * (21 / 128), screen_h * (37 / 128))
    pos_arsenal_2 = (screen_w * (21 / 128), screen_h * (46 / 128))
    pos_arsenal_3 = (screen_w * (21 / 128), screen_h * (55 / 128))
    pos_arsenal_4 = (screen_w * (21 / 128), screen_h * (65 / 128))
    pos_arsenal_5 = (screen_w * (21 / 128), screen_h * (74 / 128))
    pos_arsenal_6 = (screen_w * (21 / 128), screen_h * (83 / 128))
    pos_arsenal_7 = (screen_w * (21 / 128), screen_h * (92 / 128))
    pos_arsenal_8 = (screen_w * (21 / 128), screen_h * (102 / 128))

    pos_center = (screen_w * (1 / 2), screen_h * (40 / 64))
    pos_rgb_forge = (round(screen_w * (128 / 256)), round(screen_h * (223 / 256)))
    pos_rgb_disenchant = (round(screen_w * (41 / 256)), round(screen_h * (225 / 256)))

    ### Calc the delay times based on speed setting. Anvil slection loads slow
    anvil_time = 1.5 - (0.3 * speed)
    button_time = 0.5 - (0.1 * speed)

    ### Time to Focus AOW4 Window but click into it just in case
    sleep(1)
    pag.moveTo(pos_center)
    pag.click()
    sleep(button_time)

    ### Pynput keyboard Listener for Interrupting
    def on_press(key):
        """Detect Pressing esc"""
        if "esc" in str(key):
            stop_event.set()
            return False
        return None

    ### Defining the Automation Loops
    def forge_loop():
        """The Forging Loop"""
        nonlocal status_code
        nonlocal essence_empty
        nonlocal forged
        nonlocal arsenal_empty
        try:
            while not essence_empty:
                if stop_event.is_set():
                    status_code = -1
                    break

                pag.moveTo(pos_anvil)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()
                sleep(anvil_time)

                pag.moveTo(pos_dagger)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()

                if pag.pixelMatchesColor(
                    pos_rgb_forge[0], pos_rgb_forge[1], (39, 39, 39), tolerance=2
                ):
                    essence_empty = True
                    continue

                pag.moveTo(pos_forge)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()
                forged = True
                arsenal_empty = False

        except KeyboardInterrupt, pag.FailSafeException:
            stop_event.set()
            status_code = -1
            return -1

        finally:
            stop_event.set()

        return 2

    def disenchant_loop():
        """The Disenchanting Loop"""
        nonlocal status_code
        nonlocal arsenal_empty
        nonlocal disenchanted
        nonlocal essence_empty
        try:
            pag.moveTo(pos_arsenal)
            pag.click()
            sleep(anvil_time)

            while not arsenal_empty:
                if stop_event.is_set():
                    status_code = -1
                    break

                pag.moveTo(pos_arsenal_1)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()

                if pag.pixelMatchesColor(
                    pos_rgb_disenchant[0],
                    pos_rgb_disenchant[1],
                    (0, 0, 0),
                    tolerance=80,
                ):
                    arsenal_empty = True
                    continue

                pag.moveTo(pos_arsenal_2)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()
                pag.moveTo(pos_arsenal_3)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()
                pag.moveTo(pos_arsenal_4)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()
                pag.moveTo(pos_arsenal_5)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()
                pag.moveTo(pos_arsenal_6)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()
                pag.moveTo(pos_arsenal_7)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()
                pag.moveTo(pos_arsenal_8)
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()

                if pag.pixelMatchesColor(
                    pos_rgb_disenchant[0],
                    pos_rgb_disenchant[1],
                    (0, 0, 0),
                    tolerance=80,
                ):
                    arsenal_empty = True
                    continue

                pag.moveTo(pos_disenchant[0], pos_disenchant[1])
                if stop_event.is_set():
                    status_code = -1
                    break
                pag.click()
                sleep(anvil_time)
                disenchanted = True
                essence_empty = False

        except KeyboardInterrupt, pag.FailSafeException:
            stop_event.set()
            status_code = -1
            return -1

        finally:
            stop_event.set()

        return 2

    ### Calling the Loops based on setting
    if not disenchant:
        # Just Forge
        forge_thread = threading.Thread(target=forge_loop)
        forge_thread.start()

        with Listener(on_press=on_press) as _listener:
            stop_event.wait()

        forge_thread.join()

    elif disenchant:
        finished = False
        while not finished:
            # Forge
            forge_thread = threading.Thread(target=forge_loop)
            forge_thread.start()
            with Listener(on_press=on_press) as _listener:
                stop_event.wait()
            forge_thread.join()

            if status_code == -1:
                return -1
            stop_event.clear()

            # Disenchant
            disenchant_thread = threading.Thread(target=disenchant_loop)
            disenchant_thread.start()
            with Listener(on_press=on_press) as _listener:
                stop_event.wait()
            disenchant_thread.join()

            if status_code == -1:
                return -1
            stop_event.clear()

            # If nothing to forge nor disenchant -> finished
            finished = not forged and not disenchanted

            # Reset Variables
            forged = False
            disenchanted = False

    return status_code


if __name__ == "__main__":
    print(auto_forge(disenchant=True))
