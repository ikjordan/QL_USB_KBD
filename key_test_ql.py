import keypad
import board
import usb_hid
import time
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

class alter:
    data = (0, 0, False, False, False)
    changed = False
    
    def altered(self):
        return self.changed

    def set_data(self, converted, original, sh, cnt, alt, pressed):
        if converted != original:
            if pressed:
                self.changed = True
                self.data = ((converted, original, sh, cnt, alt))
            else:
                self.clear_data()

    def get_data(self):
        return self.data

    def clear_data(self):
            self.data = ((0, 0, False, False, False))
            self.changed = False
            
class press:
    last = 0
    kbd = 0
    pressed = {}
    count = 0
    
    def __init__(self, kbd, key_map, touple_list):
        self.kbd = kbd
        self.count = 0
        for val in key_map.values():
            if (val is not None) and (val not in self.pressed):
                self.pressed[val] = False
                
        for m in touple_list:
            for (val,s) in m.values():
                if (val is not None) and (val not in self.pressed):
                    self.pressed[val] = False
        
    def press(self, key):
        if not self.pressed[key]:
            self.kbd.press(key)
            self.last = key
            self.pressed[key] = True
            self.count += 1
        else:
            print("Press ignored", key)

    def release(self, key):
        if self.pressed[key]:
            self.kbd.release(key)
            self.last = 0
            self.count -= 1
            self.pressed[key] = False
        else:
            print("Release ignored", key)
    
    def key_count(self):
        return self.count

    def get_last(self):
        return self.last

def set_modifier(presser, new, old, key):
    if old != new:
        if new:
            print("1. Pressing", key)
            presser.press(key)
        else:
            print("1. Releasing", key)
            presser.release(key)

# Set up a keyboard device.
# For QL 9 row each with 11 columns
# Keycode.SCROLL_LOCK to represent £

key_map = {0 : Keycode.CONTROL,
           1 : Keycode.SHIFT,
           2 : None,
           3 : None,
           4 : None,
           5 : None,
           6 : None,
           7 : None,                                                                                                          
           8 : None,
           9 : None,
           10 : Keycode.ALT,
           11 : None,
           12 : None,
           13 : Keycode.LEFT_ARROW,
           14 : Keycode.ESCAPE,
           15 : Keycode.RIGHT_ARROW,
           16 : Keycode.SPACE,
           17 : Keycode.UP_ARROW,
           18 : Keycode.DOWN_ARROW,
           19 : Keycode.ENTER,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            20 : Keycode.KEYPAD_BACKSLASH,
           21 : None,

           22 : None,
           23 : None,
           24 : None,
           25 : Keycode.X,
           26 : Keycode.V,
           27 : Keycode.N,
           28 : None,
           29 : Keycode.COMMA,
           30 : None,
           31 : Keycode.FORWARD_SLASH,
           32 : None,

           33 : None,
           34 : None,
           35 : Keycode.Z,
           36 : Keycode.C,
           37 : Keycode.B,
           38 : Keycode.M,
           39 : Keycode.PERIOD,
           40 : Keycode.QUOTE,
           41 : Keycode.RIGHT_BRACKET,
           42 : Keycode.SCROLL_LOCK,
           43 : None,

           44 : None,
           45 : None,
           46 : Keycode.CAPS_LOCK,
           47 : Keycode.S,
           48 : Keycode.F,
           49 : Keycode.G,
           50 : Keycode.K,
           51 : Keycode.SEMICOLON,
           52 : Keycode.LEFT_BRACKET,
           53 : Keycode.EQUALS,
           54 : None,

           55 : None,
           56 : None,
           57 : Keycode.THREE,
           58 : Keycode.ONE,
           59 : Keycode.A,
           60 : Keycode.D,
           61 : Keycode.H,
           62 : Keycode.J,
           63 : Keycode.L,
           64 : Keycode.P,
           65 : None,

           66 : None,
           67 : None,
           68 : Keycode.W,
           69 : Keycode.TAB,
           70 : Keycode.R,
           71 : Keycode.Y,
           72 : Keycode.I,
           73 : Keycode.O,
           74 : Keycode.NINE,
           75 : Keycode.MINUS,
           76 : None,

           77 : None,
           78 : None,
           79 : Keycode.TWO,
           80 : Keycode.Q,
           81 : Keycode.E,
           82 : Keycode.T,
           83 : Keycode.SIX,
           84 : Keycode.U,
           85 : Keycode.EIGHT,
           86 : Keycode.ZERO,
           87 : None,

           88 : None,
           89 : None,
           90 : Keycode.F1,
           91 : Keycode.F2,
           92 : Keycode.F3,
           93 : Keycode.FOUR,
           94 : Keycode.FIVE,
           95 : Keycode.SEVEN,
           96 : Keycode.F4,
           97 : Keycode.F5,
           98 : None
           }           

# Five cases where key codes need to be translated to match GB keyboard:
# 1. Shifted key translates to a different shifted key
#   Shift Keycode.TWO -> Shift Keycode.QUOTE
#   Shift Keycode.QUOTE -> Shift Keycode.TWO
#   Shift Keycode.SCROLL_LOCK -> Shift Keycode.POUND

# 2. Shifted key translates to a non shifted key
#   Shift Keycode.THREE -> Keycode.POUND
#   Shift Keycode.F1 -> Keycode.F6
#   Shift Keycode.F2 -> Keycode.F7
#   Shift Keycode.F3 -> Keycode.F8
#   Shift Keycode.F4 -> Keycode.F9
#   Shift Keycode.F5 -> Keycode.F10
#   Shift Keycode.ESCAPE -> Keycode.F11

shift_map = {Keycode.TWO : (Keycode.QUOTE, True),
             Keycode.QUOTE : (Keycode.TWO, True),
             Keycode.SCROLL_LOCK : (Keycode.POUND, True),
             Keycode.THREE : (Keycode.POUND, False),
             Keycode.F1 : (Keycode.F6, False),
             Keycode.F2 : (Keycode.F7, False),
             Keycode.F3 : (Keycode.F8, False),
             Keycode.F4 : (Keycode.F9, False),
             Keycode.F5 : (Keycode.F10, False),
             Keycode.ESCAPE : (Keycode.F11, False)}

# 3. Required key press does not exist - so must map to a shifted key
#   Keycode.SCROLL_LOCK -> shift Keycode.THREE

normal_map = {Keycode.SCROLL_LOCK : (Keycode.THREE, True)}

# 4. Control keys that map to one key press
#   Control Keycode.RIGHT_ARROW -> Keycode.DELETE
#   Control Keycode.LEFT_ARROW -> Keycode.BACKSPACE

control_map = {Keycode.RIGHT_ARROW : (Keycode.DELETE, False),
               Keycode.LEFT_ARROW : (Keycode.BACKSPACE, False)}

# 5. Alt keys that map to one key press
#   Alt Keycode.LEFT_ARROW -> Keycode.HOME
#   Alt Keycode.RIGHT_ARROW -> Keycode.END

alt_map = {Keycode.LEFT_ARROW : (Keycode.HOME, False),
           Keycode.RIGHT_ARROW : (Keycode.END, False)}

time.sleep(1)

### FOR QL:
# 9 rows, 11 columns
km = keypad.KeyMatrix(
    row_pins=(board.GP0, board.GP1, board.GP2, board.GP3,
              board.GP4, board.GP5, board.GP6, board.GP7, board.GP8), 
     column_pins=(board.GP9, board.GP10, board.GP11, board.GP12, board.GP13,
                  board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19) 
)

# Create an event we will reuse
event = keypad.Event()

altered = alter()
kbd = Keyboard(usb_hid.devices)

# Build the map of possible key strokes, and their state
presser = press(kbd,
                key_map,
                [shift_map, normal_map, control_map, alt_map])

# TO DO May be able to simplify SHIFT
shift_right = False
shift_left = False
shift = False
alt = False
control = False
cap_lock = not kbd.led_on(Keyboard.LED_CAPS_LOCK)

# Caps Lock Key
led = digitalio.DigitalInOut(board.GP20)
led.direction = digitalio.Direction.OUTPUT
led.value = cap_lock
            
while True:
    if km.events.get_into(event):
        # Convert the event to a specific key
        key_code = key_map.get(event.key_number, 0)
        
        print("")
        print("*** C:", key_code, "P:", event.pressed, "A:", altered.altered(), "S:", shift)

        if (key_code != 0) and ((presser.key_count() < 3) or (not event.pressed)):
            modifier = False
            
            if key_code == Keycode.LEFT_SHIFT or key_code == Keycode.RIGHT_SHIFT:
                if key_code == Keycode.LEFT_SHIFT:
                    shift_left = event.pressed
                elif key_code == Keycode.RIGHT_SHIFT:
                    shift_right = event.pressed
                
                if shift != (shift_left or shift_right):
                    shift = shift_left or shift_right
                    modifier = True
                else:
                    continue    # Just pressing / releasing both shift keys
            elif key_code == Keycode.ALT:
                alt = event.pressed
                modifier = True
            elif key_code == Keycode.CONTROL:
                control = event.pressed
                modifier = True

            if modifier:
                # Was the last code altered?
                if altered.altered():
                    # Undo the last event
                    (converted, original, s, c, a) = altered.get_data()
                    altered.clear_data()

                    # What type of alteration was it? Start by checking for Alt
                    (convert, sh) = alt_map.get(original, (original, False))
                    if (convert == original):
                        (convert, sh) = control_map.get(original, (original, False))
                    if (convert != original):
                        # A control or alt alteration, just remove the old alteration
                        # and reapply
                        print("2. Releasing", converted)
                        presser.release(converted)

                        set_modifier(presser, shift, s, Keycode.SHIFT)
                        set_modifier(presser, control, c, Keycode.CONTROL)
                        set_modifier(presser, alt, a, Keycode.ALT)
                        print("3. Pressing", original)
                        presser.press(original)
                        altered.clear_data()
                        continue

                    # An alteration based on shift
                    if key_code == Keycode.LEFT_SHIFT or key_code == Keycode.RIGHT_SHIFT:
                        if event.pressed:
                            # Shift has been pressed, so we must have previously 
                            # modified a normal key and faked shift
                            (convert, sh) = shift_map.get(original, (original, True))
                            print("Press", convert, original, sh)
                        else:   # shift released
                            (convert, sh) = normal_map.get(original, (original, False))
                            print("Release", convert, original, sh)

                        if (converted != convert):
                            print("Shift converting",converted, convert, original)
                            # Release that key
                            print("4. Releasing", converted)
                            presser.release(converted)
                            
                            # Get shift to the correct state
                            if not sh:
                                print("5. Releasing", Keycode.SHIFT)
                                presser.release(Keycode.SHIFT)
                            else:
                                print("4. Pressing", Keycode.SHIFT)
                                presser.press(Keycode.SHIFT)
                                
                            # Press the new key
                            print("4.5 Pressing", convert)
                            presser.press(convert)
                            altered.set_data(convert, original, sh, control, alt, True)
                            
                        else:
                            if not sh:
                                print("6. Releasing", Keycode.SHIFT)
                                presser.release(Keycode.SHIFT)
                            else:
                                print("6.5 Pressing", Keycode.SHIFT)
                                presser.press(Keycode.SHIFT)
                            altered.clear_data()

                else: # Do not have an altered key
                    if event.pressed:
                    # Special case if pressing shift, may need to change last key
                        if key_code == Keycode.LEFT_SHIFT or key_code == Keycode.RIGHT_SHIFT:
                            last = presser.get_last()
                            if (last and not (control or alt)):
                                (convert, s) = shift_map.get(last, (last, True))
                                altered.set_data(convert, last, s, control, alt, True)
                                
                                if convert != last:
                                    print("6. Releasing", last)
                                    presser.release(last)

                                    if s:
                                        print("5. Pressing", Keycode.SHIFT)
                                        presser.press(Keycode.SHIFT)
                                    print("6. Pressing", convert)
                                    presser.press(convert)
                                else:
                                    print("7. Pressing", Keycode.SHIFT)
                                    presser.press(Keycode.SHIFT)
                            else:
                                print("8. Pressing", Keycode.SHIFT)
                                presser.press(Keycode.SHIFT)
                        else: # Alt or Control
                            print("9. Pressing", key_code)
                            presser.press(key_code)
                    else: # Key released
                        if key_code == Keycode.LEFT_SHIFT or key_code == Keycode.RIGHT_SHIFT:
                            print("7. Releasing", Keycode.SHIFT)
                            presser.release(Keycode.SHIFT)
                        else:
                            print("7.5. Releasing", key_code)
                            presser.release(key_code)
                        
            # A non modifier key (i.e. Not shift, alt or control)
            else:
                if altered.altered():
                    # Undo the last alteration - checking if this is the same keypress
                    (converted, original, s, c, a) = altered.get_data()
                    
                    # is this just that key being released?
                    if event.released:
                        if original == key_code:
                            print("8. Releasing", converted)                                
                            presser.release(converted)
                            set_modifier(presser, shift, s, Keycode.SHIFT)
                            set_modifier(presser, control, c, Keycode.CONTROL)
                            set_modifier(presser, alt, a, Keycode.ALT)
                            altered.clear_data()
                        else:
                            # A previous key is being released
                            presser.release(key_code)
                            print("9. Releasing", key_code)
                        continue
                    else:
                        # Pressing another key, so release the altered one
                        print("10. Releasing", converted)
                        presser.release(converted)
                        set_modifier(presser, shift, s, Keycode.SHIFT)
                        set_modifier(presser, control, c, Keycode.CONTROL)
                        set_modifier(presser, alt, a, Keycode.ALT)
                        altered.clear_data()

                # Previous altered keys have been handled, process this key
                convert = key_code
                s = shift
                c = control
                a = alt

                if event.pressed:   # Release of modified keys already handled
                    # Handle normal key presses
                    if not (shift or control or alt):
                        (convert, s) = normal_map.get(key_code, (key_code, False))
                    # Shift key presses    
                    elif shift and (not (control or alt)):
                        (convert, s) = shift_map.get(key_code, (key_code, True))
                    # Control key presses
                    elif control and (not (shift or alt)):
                        (convert, s) = control_map.get(key_code, (key_code, False))
                        if convert != key_code:
                            c = False
                    # alt key presses
                    elif alt and (not (shift or control)):
                        (convert, s) = alt_map.get(key_code, (key_code, False))
                        if convert != key_code:
                            a = False

                    # Store the alteration
                    altered.set_data(convert, key_code, s, c, a, event.pressed)

                # Handle the altered state first
                if convert != key_code:
                    if event.pressed:
                        set_modifier(presser, s, shift, Keycode.SHIFT)
                        set_modifier(presser, c, control, Keycode.CONTROL)
                        set_modifier(presser, a, alt, Keycode.ALT)
                        print("10. Pressing", convert)
                        presser.press(convert)
                    else: # Release of modified keys are already handled
                        print("Trying to release altered key - BUG")
                else: # Just a simple key press!
                    if event.pressed:
                        print("11. Pressing", key_code)
                        presser.press(key_code)
                    else:
                        print("11. Releasing", key_code)
                        presser.release(key_code)
        else:
            if key_code: 
                print("Key ignored - too many pressed:", presser.key_count())
            else:
                print("Key ignored Unknown code:", event.key_number)

    if (kbd.led_on(Keyboard.LED_CAPS_LOCK) != cap_lock):
        cap_lock = kbd.led_on(Keyboard.LED_CAPS_LOCK)
        led.value = not cap_lock


