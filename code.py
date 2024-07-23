# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
#
# ble-gamepad
#
# Docs and Reference Code:
# - https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder/python-circuitpython
# - https://docs.circuitpython.org/projects/seesaw/en/latest/api.html
# - https://docs.circuitpython.org/projects/ble/en/latest/api.html
# - https://github.com/adafruit/circuitpython/blob/main/shared-bindings/_bleio/ScanResults.c
# - https://github.com/adafruit/circuitpython/blob/main/shared-bindings/_bleio/ScanEntry.c
# - https://github.com/adafruit/Adafruit_CircuitPython_BLE/blob/main/adafruit_ble/__init__.py
# - https://www.bluetooth.com/specifications/assigned-numbers/
#
from board import STEMMA_I2C
from gc import collect, mem_free
from time import sleep
import usb_cdc

from adafruit_ble import BLERadio
from adafruit_seesaw import digitalio
from adafruit_seesaw.seesaw import Seesaw


def gcCol():
    # Collect garbage and print free memory
    collect()
    print('mem_free', mem_free())

def drainCDCBuf():
    # Drain the serial console buffer
    cons = usb_cdc.console
    if cons:
        w = cons.in_waiting
        if w > 0:
            cons.timeout = 0
            cons.read(w)

def showMenu(choices, context):
    # Show the menu with selected item highlighted
    assert (type(context) == dict) and ('selection' in context), "bad context"
    selection = context['selection']
    assert (0 <= selection) and (selection < len(choices)), "bad selection"
    print("Menu: ", end='')
    for (i, (name, _)) in enumerate(choices):
        if i == selection:
            print('>>%s<<' % name, end='')
        else:
            print('  %s  ' % name, end='')
    print()

def doMenuAction(choices, context):
    # Perform the action for the selected menu item
    assert (type(context) == dict) and ('selection' in context), "bad context"
    selection = context['selection']
    assert (0 <= selection) and (selection < len(choices)), "bad selection"
    (name, actionFn) = choices[selection]
    if actionFn is None:
        print(name, 'is not implemented yet')
    else:
        actionFn(context)

def scan(context):
    # Scan for BLE devices, scan results get saved to context['devices']
    assert (type(context) == dict) and ('devices' in context), "bad context"
    assert (type(context['devices']) == dict), "bad device dictionary"
    t = 15
    print('Scanning with %d second timeout' % t)
    radio = BLERadio()
    devices = {}
    for r in radio.start_scan(timeout=t):
        name = r.complete_name
        if (not r.connectable) or (name is None):
            # Ignore advertisements that are unconnectable or unnamed
            continue
        key = (r.address, name)
        if key in devices:
            # Ignore advertisements we've already seen
            continue
        # Handle a new advertisement
        devices[key] = r
        print(key)
    context['devices'] = devices
    print('Scan done\n')

def devices(context):
    # Print the list of devices from the most recent scan
    assert (type(context) == dict) and ('devices' in context), "bad context"
    assert (type(context['devices']) == dict), "bad device dictionary"
    print('Connectable BLE devices:')
    if len(context['devices']) == 0:
        print('[no devices, try scanning again]')
    for k in context['devices']:
        print(k)
    print()

def connect(context):
    # Connect to a BLE device
    print('Connect is not implemented yet\n')

def disconnect(context):
    # Disconnect from a BLE device
    print('Disconnect is not implemented yet\n')

def main():
    # Initialize stuff then start event loop
    drainCDCBuf()   # usb_cdc.console may have leftover garbage
    gcCol()
    # Configure Seesaw I2C rotary encoder (Adafruit #5880 or #4991)
    ssw = Seesaw(STEMMA_I2C(), addr=0x36)    # address for no jumpers soldered
    sswver = (ssw.get_version() >> 16) & 0xffff
    assert (sswver == 4991), 'unexpected seesaw firmware version (not 4991)'
    ssw.pin_mode(24, Seesaw.INPUT_PULLUP)    # add pullup to knob-click button
    # NAV MENU
    # each item should be a tuple of (name, bound-function)
    choices = [
        ('Scan', scan),
        ('Devices', devices),
        ('Connect', connect),
        ('Disconnect', disconnect),
    ]
    # GLOBAL STATE
    context = {'devices': {}, 'selection': 0}
    # MAIN EVENT LOOP
    prevClick = False
    showMenu(choices, context)
    while True:
        sleep(0.01)
        # Check for newline wake sequence on the serial console
        cons = usb_cdc.console
        if cons and cons.in_waiting > 0:
            # for any console input (probably LF) -> send menu
            drainCDCBuf()
            showMenu(choices, context)
        # Read the rotary encoder (Seesaw I2C)
        (click, delta) = (not ssw.digital_read(24), ssw.encoder_delta())
        if click and (click != prevClick):
            # knob was clicked
            doMenuAction(choices, context)
            showMenu(choices, context)
        prevClick = click
        if delta != 0:
            # knob was turned
            context['selection'] = (context['selection'] + delta) % len(choices)
            showMenu(choices, context)

main()
