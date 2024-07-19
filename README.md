<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2024 Sam Blenny -->
# BLE Gamepad

work in progress (alpha)


## Hardware

![QT Py ESP32-S3 dev board with rotary encoder and gamepad](qtpyS3Zero2.jpeg)

- 8BitDo Zero 2f Bluetooth gamepad
  ([product page](https://www.8bitdo.com/zero2/))

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


## Getting Started

To begin, assemble the rotary encoder and knob,
[install CircuitPython 9.1](https://learn.adafruit.com/adafruit-qt-py-esp32-s3/circuitpython-2)
then copy the project bundle code to your CIRCUITPY drive. Once that's all done,
`code.py` will begin sending messages to the serial console. Use the rotary
encoder knob to select menu options.
