# -*- coding: utf-8 -*-

import random
import time_wheel

session = 0
def new_session():
    global session
    session += 1
    return session

def new_delta(upper):
    return random.randint(1, upper)

tw = time_wheel.NewPod([60, 60, 24])

records = {}
def new_record(tw, delta_upper):
    global records
    sess = new_session()
    delta = new_delta(delta_upper)
    records[sess] = [tw.tick, delta]
    print(f"push, sess:{sess}, delta:{delta}, at tick:{tw.tick}")
    tw.Push(sess, delta)

total_size = 35
cur_size = 20
for i in range(cur_size):
    if i < 5:
        new_record(tw, 60)
    elif i < 10:
        new_record(tw, 60*60)
    elif i < 15:
        new_record(tw, 60*60*24)
    else:
        new_record(tw, 60*60*24*2)

print("------time wheel tick begin-----")
while records:
    out = tw.Tick()
    for sess in out:
        reg_tick, delta = records[sess]
        print(f"timeout, sess:{sess}, reg_tick:{reg_tick} delta:{delta}, at tick:{tw.tick}")
        assert reg_tick + delta == tw.tick
        del records[sess]

    if out and cur_size <= total_size and random.randint(1, 100) <= 78:
        cur_size += 1
        new_record(tw, 60*60*24*2)

print("------time wheel tick end-----")
