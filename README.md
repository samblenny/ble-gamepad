<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2024 Sam Blenny -->
# BLE Gamepad

**NOTE: THIS IS A EXPERIMENT THAT DIDN'T WORK OUT.**

I wanted a solid no-solder-required gamepad option to use in future projects.
The trick is that many gamepads currently on the market use Bluetooth Classic,
while the ESP32-S3 radio is limited to Bluetooth 5.0 BLE. I thought that I
might be able to get something going with one of the Switch Pro compatible
controllers that advertise using Bluetooth 5.0 LE. But, it didn't work out.

After trying lots of stuff without success, I think the way to go is probably
using a different CircuitPython board that has a Bluetooth Classic radio or to
use a USB host board with a USB wireless gamepad adapter.

This is the hardware setup that I used for experimenting with BLE 5.0:

![QT Py ESP32-S3 dev board with rotary encoder and gamepad](qtpyS3Ultimate.jpeg)


## Bluetooth Version Compatibility Problems

[Espressif's ESP32-S3 docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/bluetooth.html)
say that it supports bluetooth 5.0, but not Bluetooth classic.

When I tried my old 8BitDo Zero 2 and 8BitDo SN 30 Pro gamepads, neither of
them showed up with `adafruit_ble.BLERadio.start_scan()`. But, when I tried an
8BitDo Ultimate Controller (Bluetooth 5.0 charging stand version), it did show
up in the BLE scan as a device named `80NA`. However, the available
characteristics of the `80NA` device didn't obviously match up with anything
that I was able to find documentation for.

Based on playing with a few Bluetooth scanner apps and reading *a lot* of
gamepad product pages, my best guess is that, most Bluetooth gamepads currently
on the market (July 2024) probably use Bluetooth Classic. The main exception is
some newer Nintendo Switch compatible gamepads that mention Bluetooth 5.0 in
their specifications. I don't know what those gamepads actually use BLE 5.0
for. The one that I played around with advertises as "Pro Controller" on
Bluetooth Classic and "80NA" on BLE 5.0. It's possible the BLE 5 stuff is used
by the iOS app for remapping buttons on that gamepad.

My main conclusion was that I should try again using a board that has a
Bluetooth Classic radio, or use a USB wireless gamepad adapter, because most
current wireless gamepads appear to use Bluetooth Classic.


## Hardware

- 8BitDo Ultimate Controller with Charging Dock (Bluetooth 5.0 gamepad)
  ([product page](https://www.8bitdo.com/ultimate-bluetooth-controller/))

- Adafruit QT Py ESP32-S3 with 8MB Flash and no PSRAM
  ([product page](https://www.adafruit.com/product/5426),
  [learn guide](https://learn.adafruit.com/adafruit-qt-py-esp32-s3))

- Adafruit I2C Stemma QT Rotary Encoder Breakout with Encoder
  ([product page](https://www.adafruit.com/product/5880),
  [learn guide](https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder))

- Adafruit Violet Micro Potentiometer Knob - 4 pack
  ([product page](https://www.adafruit.com/product/5537))

- Adafruit STEMMA QT / Qwiic JST SH 4-pin Cable - 100mm
  ([product page](https://www.adafruit.com/product/4210))


## Code

My BLE 5.0 scanner code is in [code.py](code.py). It doesn't do much in its
current form, but I'm leaving it here because it might be useful to copy and
paste into other projects.
