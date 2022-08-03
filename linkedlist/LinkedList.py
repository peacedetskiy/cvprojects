from random import randint

# a linked list unit. contains data and a pointer to a next unit(node).
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# a class to use it in linked list later to iterate through it
class Iterator:
    def __init__(self, head):
        self.current = head


    def __iter__(self):
        return self


    def __next__(self):
        if not self.current:
            raise StopIteration
        else:
            t = self.current.data
            self.current = self.current.next
            return t


# custom linked list class with essential methods and two additional functions
class LinkedList:
    def __init__(self):
        self.head = None
        self.index = 0

    # add some data to end
    def add_to_end(self, new_data):
        node = Node(new_data)
        if self.head is None:
            self.head = node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = node

    # add some data to beginning
    def add_to_beginning(self, new_data):
        node = Node(new_data)
        node.next = self.head
        self.head = node


    # delete the first node
    def del_from_beginning(self):
        if self.head is None:
            return
        node = self.head.next
        self.head.next = None
        self.head = node


    # delete the last node
    def del_from_end(self):
        if self.head is None:
            return
        if self.head.next is None:
            self.head = None
            return
        last = self.head
        before = None
        while last.next:
            before = last
            last = last.next
        before.next = None
        last = None


    # delete a node from any given position
    def del_from_pos(self, k):
        try:
            if self.head is None:
                return
            if k == 0:
                self.del_from_beginning()
                return
            i = 1
            last = self.head.next
            before = self.head
            while i < k:
                before = last
                last = last.next
                i += 1
            before.next = last.next
            last = None
        except AttributeError:
            return


    # tell linked list how to print itself in string format
    def __str__(self):
        if self.head is None:
            return ''
        s = f'{self.head.data}, '
        if self.head.next is None:
            return s[:-2]
        last = self.head.next
        s += f'{last.data}, '
        while last.next:
            s += f'{last.next.data}, '
            last = last.next
        return s[:-2]


    # makes it able to iterate through list
    def __iter__(self):
        return Iterator(self.head)


    # generate a linked list with given size but random values from any interval
    def generate(self, size, a=-5, b=5):
        try:
            for i in self.l_random(size, a, b):
                self.add_to_end(i)
        except TypeError:
            print('Enter valid number.')
            return


    # a generator that is used to randomize values for a random list generator above
    def l_random(self, size, a=-5, b=5):
        i = 0
        while i < size:
            x = randint(a, b)
            i += 1
            yield x


    # a magic method to get length of the list
    def __len__(self):
        t = 0
        last = self.head
        while last.next:
            t += 1
            last = last.next
        t += 1
        return t


    # an extra custom function to delete every second element from a list(for fun)
    def del_every_second(self):
        if self.head is None:
            return
        if self.head.next is None:
            return
        if self.head.next.next is None:
            self.head.next = None
            return
        last = self.head
        while last.next.next:
            if last.next:
                last.next = last.next.next
                last = last.next
            if last.next is None:
                break
        if last.next:
            if last.next.next is None:
                last.next = None


    # an extra custom function to split a list into 
    # two separate linked lists by half(for fun)
    def split_into_two(self, l1, l2):
        try:
            if self.head is None:
                return
            last = self.head
            if last.next is None:
                if last.data > 0:
                    l1.add_to_end(last.data)
                else:
                    l2.add_to_end(last.data)
            while last.next:
                if last.data > 0:
                    l1.add_to_end(last.data)
                else:
                    l2.add_to_end(last.data)
                last = last.next
            if last.data > 0:
                l1.add_to_end(last.data)
            else:
                l2.add_to_end(last.data)
        except AttributeError:
            print("Please pass linked lists.")
