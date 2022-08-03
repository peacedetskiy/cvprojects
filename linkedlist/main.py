from LinkedList import LinkedList

# now we'll see how some methods work
# let's create a linked list
L = LinkedList()

# now fill it with random values and look at it
L.generate(10)
print(L)

# here we delete every second element and look what happenned
L.del_every_second()
print(L)

# now let's split it into two lists and look at these new ones
L1 = LinkedList()
L2 = LinkedList()
L.split_into_two(L1, L2)
print(L1)
print(L2)
