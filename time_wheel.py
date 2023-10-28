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
                move_list = self.wheels[i+1].Tick()
                for node in move_list:
                    self._push_node(node)

    # Returns:
    #  +1 wheel idx [0, wheel_size) if in wheel range, -1(represent far list) otherwise
    def Push(self, session, delta):
        assert delta > 0, "delta Non-positive"
        expire = self.tick + delta
        node = TimeWheelPod.Node(session, expire)
        return self._push_node(node)

    # tick once
    def Tick(self):
        self.tick += 1
        out = self._execute()
        self._shift()
        return out
    
    # tick elapse times
    def Update(self, elapse):
        out = []
        for i in range(elapse):
            self.tick += 1
            out.extend(self._execute())
            self._shift()
        return out

# Arguments:
#  +1 wheel size list
def NewPod(size_list):
    return TimeWheelPod(size_list)