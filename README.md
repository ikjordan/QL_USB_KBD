# QL_USB_KBD
This Circuit Python code for the Raspberry Pi Pico 2040 allows a [Sinclair QL](https://en.wikipedia.org/wiki/Sinclair_QL) with a GB keyboard to be converted to a GB USB keyboard that can be used in Linux or MS Windows.

**No working QLs were harmed in the producion of this project, and no non-reversible changes were made to the QL case**

## Background
The Sinclair QL was launched in 1984, and production was discontinued in 1986. Therefore the electronics are over 35 years old. Whilst they have proved resilient, and there are still firms that will repair them, there are examples where the mainboard is no longer functional. 

This project provides code on the Raspberry Pi Pico 2040 that can decode signals from the keyboard matrix and send corresponding USB HID (Human Interface Devices) messages to a host computer.

The QL keybaord layout is similar to a GB keyboard, with some small exceptions e.g:  
Position of £ key  
Position of " and @  
No dedicated backspace and delete. (Control Left and Control Right is used instead).

The code translates keypresses so that the keyboard appears as a standard GB USB keyboard (albeit with less keys).

## Connecting the keyboard membrane
The QL keyboard membrane connects through one 9 way and one 11 way Connfly Ds1020 connector. These can be very difficult to source for an individual. I found some 12 way Ds1020 connectors on ebay. These can be used as long as the membrane is inserted firmly at one end of the connector.

Ironically the keyboard membrane is probably the most fragile component in the QL. It is very likely that any membrane of a significant age will need to be replaced before attempting this project. Luckily newly manufactured replacements are [readily available](https://www.sellmyretro.com/offer/details/new-sinclair-ql-keyboard-membrane-2340), and of higher quality than the original.

The 20 lines from the membrane (9 rows, 11 columns) are routed to the first 20 GPIO lines on a Raspberry Pico. This can be simply achieved by mounting the Ds1020 on Veroboard, with PCB headers then taking the output to the Pico. I am sure those with more hardware skills than me could easily fabricate a dedicated PCB, including mounting the Pico 2040.

No diodes are used in the circuit. The keyboard functions well in the normal case without them. Currently the code is configured so only 3 simultaneous keypresses are registered, to prevent ghosting. This could be improved to allow more keypresses from a single keyrow.  

## Indicating the state of CAPS Lock
The QL case includes a Yellow Power LED. It draws approximately 15mA.

In this project, it is connected to the Pico in series with a 220 Ω resister. The power LED has been configured to be on when CAPS LOCK is *not* set, and off when CAPS LOCK is not set. It has been configured this way, so that the Power light glows when in the more common setting i.e. CAPS LOCK is not enabled.

## Installation
The project uses Circuit Python, and the Adafruit Matrix Keypad library. Instructions for installation can be found [here] (https://learn.adafruit.com/matrix-keypad/python-circuitpython)

The code must run automatically on power up. In addition the usual auto-mount of the CIRCUITPY drive should be disabled. 

`boot.py` is used to prevent automount. Using `code.py` as the filename for the code file ensures that the code will run on power on (see [here](https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/circuitpy-midi-serial)).

Both `boot.py` and `code.py` should be copied to the root directory of the CIRCUITPY drive.

### Debug
For debug purposes `key_test_ql.py` can be run. This is similar to `code.py`, but includes `print` commands, so keystrokes can be seen in REPL.


# Why?
Some people may question why a 35 year old keyboard of debatable quality should be converted to USB. There are two main reasons why I did this:
1) I consider the QL case as a good example of industrial design.
2) It allows use of a modern emulator (either under MS Windows or [Linux](https://github.com/SinclairQL/sQLux) with an authentic keyboard.

It is also ammusing that a $3 dollar part, running two m0+ cores at 125MHz, with 264kB of RAM and 2MB of Flash, is being used to control the keyboard of the QL, when originally the main QL processor ran at 7.5MHz, and accessed 128kB of RAM!
