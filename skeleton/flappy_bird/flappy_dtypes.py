class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# TODO: implement a circular list for the bird animation
class CircularList:
    def __init__(self):
        self.last = None

    def add_empty(self, data):
        if self.last is not None:
            return
        new_node = Node(data)
        self.last = None # TODO: fill this in
        self.last.next = None # TODO: fill this in

    def enter(self, data):
        if not self.last:
            self.add_empty(data)
        else:
            new_node = Node(data)
            new_node.next = None # TODO: point this at the previous head of the circular list
            self.last.next = None # TODO: point this at the new head of the circular list

    def append(self, data):
        if not self.last:
            self.add_empty(data)
        else:
            new_node = Node(data)
            # Bonus TODO: fill in the rest and remove pass
            pass

    def display(self):
        # Display the elements of the linked list
        current = self.last.next
        while current:
            # Traverse through each node and print its data
            print(current.data, end=" -> ")
            current = current.next
            if current == self.last.next:
                current = None
        print("head")