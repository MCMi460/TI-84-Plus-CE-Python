# Now supports TI-84 Plus CE Python Calculators
import math, time

def is_generator(iterable): # Hacky generator check on TI
    return isinstance(iterable, type(None for i in ''))

class Err(Exception):
    pass

class Pythagorean_Triples:
    def brute_search(recursion_depth:int = 200):
        nums = list(range(recursion_depth))
        i = 1
        while i < len(nums):
            a = nums[i]
            for b in range(a, recursion_depth):
                c = math.sqrt(a**2 + b**2) # Pythagorean theorem
                if c % 1 == 0:
                    if b in nums[i:]:
                        nums.remove(b)
                    yield (a, b, int(c))
            i += 1

    def formula_search(recursion_depth:int = 10): # Not as refined - recursion_depth is much more intensive
        for m in range(1, recursion_depth):
            for n in range(m + 1, recursion_depth):
                a = -1 * (m**2 - n**2)
                b = 2 * m * n
                c = m**2 + n**2
                yield (a, b, c)

classes = [
    (Pythagorean_Triples,
    'Pythagorean Triples',
    (
        (
            Pythagorean_Triples.brute_search, # Function
            'brute_search', # Name
            { # Requirements
                'recursion_depth:int': 200,
            },
        ),
        (
            Pythagorean_Triples.formula_search,
            'formula_search',
            {
                'recursion_depth:int': 10,
            },
        ),
    )),
]

def gui():
    cursor = 0

    disp_cursor(0)
    key = None
    depth = classes
    back = []
    printed = []
    while True: # Event loop
        disp_clr()
        disp_at(1, '0: Back', 'left')
        for option in range(len(depth)):
            disp_at(option + 2, '%s: %s' % (option + 1, depth[option][1]), 'left')
        key = resolve_key(wait_key()) - 1
        if key == -1:
            if len(back) == 0:
                break
            depth = back[-1]
            back = back[:-1]
        elif type(depth[key][2]) == tuple: # If tuple, then act as class
            back.append(depth)
            depth = depth[key][2]
        else: # Otherwise dict, act as function
            ret = depth[key][0]()
            if is_generator(ret):
                ret = list(ret)
            if isinstance(ret, list):
                printed = ret
            else:
                printed = [ret,]
            if calc:
                scroll = 0
                kscroll = 3
                while kscroll in [3, 4]:
                    for i in range(1, 10):
                        disp_at(i, '%s' % (printed[i - 1 - scroll],), 'left') # Fix scrolling tomorrow
                    print('\n[Press any key to continue]')
                    kscroll = wait_key()
                    if kscroll == 4 and scroll > 0:
                        scroll -= 1
                    elif kscroll == 3 and scroll < len(printed) - 1:
                        scroll += 1
            else:
                print('\n'.join(map(str, printed)))
                print('\n[Press any key to continue]')
                wait_key()
            printed = []
    raise Err('Ended')

def resolve_key(key:int):
    if isinstance(key, str):
        return int(key)
    key = str(key)
    keys = {
        '142': 0,
        '143': 1,
        '144': 2,
    }
    if not key in keys.keys():
        raise Err('Key not registered for program')
    return keys[key]

if __name__ == '__main__':
    import os
    print('Running on computer!')
    calc = False
    # Define TI functions for computer debugging
    def wait_key():
        return input('Key: ')
    def disp_cursor(i):
        return
    def disp_at(row, text, align):
        print(text)
    def disp_clr():
        os.system('clear')
else:
    from ti_system import *
    print('Running on calculator!')
    calc = True

try:
    gui()
except Err as msg:
    print('\n%s' % msg)
