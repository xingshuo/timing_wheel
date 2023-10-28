# -*- coding: utf-8 -*-

import random
import time_wheel

session = 0
def new_session():
    global session
    session += 1
    return session

def new_delta():
    return random.randint(1, 60*60*24 + 60*60*10)

tw = time_wheel.NewPod([60, 60, 24])

records = {}
def new_record(tw):
    global records
    sess = new_session()
    delta = new_delta()
    records[sess] = [tw.tick, delta]
    print(f"push, sess:{sess}, delta:{delta}, at tick:{tw.tick}")
    tw.Push(sess, delta)

total_size = 20
cur_size = 10
for i in range(cur_size):
    new_record(tw)

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
        new_record(tw)

print("------time wheel tick end-----")