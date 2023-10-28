# -*- coding: utf-8 -*-

class TimeWheelPod:
    class Node:
        def __init__(self, session, expire) -> None:
            self.session = session
            self.expire = expire

    class TimeWheel:
        def __init__(self, slot_size) -> None:
            self.slot_size = slot_size
            self.slots = [[] for i in range(slot_size)]
            self.next_slot = 0
        
        def _push_node(self, node, delta):
            idx = (self.next_slot + delta - 1) % self.slot_size
            self.slots[idx].append(node)
        
        def Tick(self):
            out = self.slots[self.next_slot]
            self.slots[self.next_slot] = []
            self.next_slot = (self.next_slot + 1) % self.slot_size
            return out

    def __init__(self, size_list) -> None:
        self.wheels = [TimeWheelPod.TimeWheel(size_list[i]) for i in range(len(size_list))]
        self.ranges = [0 for i in range(len(size_list))]
        self.far = [] # beyond wheels range
        upper = 1
        for i,tw in enumerate(self.wheels):
            upper *= tw.slot_size
            self.ranges[i] = upper
        self.tick = 0
    
    def _push_node(self, node):
        delta = node.expire - self.tick
        expire = self.wheels[0].next_slot + delta - 1
        for i, tw in enumerate(self.wheels):
            if expire < self.ranges[i]:
                if i == 0:
                    tw._push_node(node, delta)
                else:
                    tw._push_node(node, expire//self.ranges[i-1])
                return i
        
        self.far.append(node)
        return -1
    
    def _execute(self):
        node_list = self.wheels[0].Tick()
        return [node.session for node in node_list]

    def _shift(self):
        for i, tw in enumerate(self.wheels):
            if tw.next_slot != 0:
                break
            if i == len(self.wheels)-1:
                move_list = self.far
                self.far = []
                for node in move_list:
                    self._push_node(node)
            else: