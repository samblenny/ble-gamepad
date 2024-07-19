# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
#
# ble-gamepad
#
# Docs:
# - https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder/python-circuitpython
# - https://docs.circuitpython.org/projects/seesaw/en/latest/api.html
#
from board import STEMMA_I2C
from gc import collect, mem_free
from time import sleep
import usb_cdc

from adafruit_seesaw import digitalio
from adafruit_seesaw.seesaw import Seesaw


def gcCol():
    # Collect garbage and print free memory
    collect()
    print('mem_free', mem_free())

def drainCDCBuf():
    # Drain the serial console buffer.
    cons = usb_cdc.console
    if cons:
        w = cons.in_waiting
        if w > 0:
            cons.timeout = 0
            cons.read(w)

def showMenu(choices, selection):
    # Show the menu with selected item highlighted
    assert (0 <= selection) and (selection < len(choices)), 'selection OOR'
    for (i, c) in enumerate(choices):
        if i == selection:
            print('[[%s]] ' % c, end='')
        else:
            print('  %s   ' % c, end='')
    print()

def doMenuAction(choices, selection):
    # Perform the action for the selected menu item
    assert (0 <= selection) and (selection < len(choices)), 'selection OOR'
    print(choices[selection], 'is not implemented yet')

def main():
    # Initialize stuff then start event loop
    drainCDCBuf()   # usb_cdc.console may have leftover garbage
    gcCol()
    # Configure Seesaw I2C rotary encoder (Adafruit #5880 or #4991)
    ssw = Seesaw(STEMMA_I2C(), addr=0x36)    # address for no jumpers soldered
    sswver = (ssw.get_version() >> 16) & 0xffff
    assert (sswver == 4991), 'unexpected seesaw firmware version (not 4991)'
    ssw.pin_mode(24, Seesaw.INPUT_PULLUP)    # add pullup to knob-click button
    # MAIN EVENT LOOP
    prevClick = False
    choices = ['Scan', 'Pair', 'Info', 'Connect', 'Disconnect']
    selection = 0
    while True:
        sleep(0.01)
        # Check for newline wake sequence on the serial console
        cons = usb_cdc.console
        if cons and cons.in_waiting > 0:
            # for any console input (probably LF) -> send menu
            drainCDCBuf()
            showMenu(choices, selection)
        # Read the rotary encoder (Seesaw I2C)
        (click, delta) = (not ssw.digital_read(24), ssw.encoder_delta())
        if click and (click != prevClick):
            # knob was clicked
            doMenuAction(choices, selection)
        prevClick = click
        if delta != 0:
            # knob was turned
            selection = (selection + delta) % len(choices)
            showMenu(choices, selection)

main()
