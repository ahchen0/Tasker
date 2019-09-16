## linked_list.py
##
## a doubly-linked list.
##
## by Leland Pierce, June 2, 2019
##
##

class linked_list():
    """
    """
    def __init__(self):
        """
        """
        self.first=None
        self.last=None
        self.size=0

    def __str__(self):
        """
        For printing the linked-list
        """
        ## for printing the list
        ret = "<linked_list>"
        node = self.first
        while node:
            ret += str(node)
            ret +=", "
            node = node.next
        ret += "</linked_list>"
        return ret

    def append(self,x=None):
        """
        Appends x, the linked_list_item to the end of the linked-list.
        If x is not a linked_list_item, it makes it one first.
        Always succeeds.
        """
        
        if x is None:
            xx=linked_list_item()
        else:
            ## if necessary, make x be a linked_list_item:
            try:
                ## if this succeeds, x is already a
                ## linked_list_item, so do nothing.
                xx=x.copy()
            except:
                ## here we need to create a linked_list_item
                ## from the passed-in item
                xx=linked_list_item(x)
                
        if self.first is None:
            ## start new linked list
            self.first=xx
            self.last=xx
            self.size=1
        elif self.size==1:
            self.first.next = x
            self.size += 1
            x.previous = self.first
            self.last=x
        else:
            ## append to end of existing list:
            self.last.next = xx
            self.size += 1
            xx.previous = self.last
            self.last =xx




    
    def insert(self,index,x=None):
        """
        Insers x, the linked_list_item before an existing item 
        in the linked-list, with position = index.
        If x is not a linked_list_item, it makes it one first.
        If there is not an item with the specified index, False is returned,
        other wise True is returned.
        """
        ##print("linked_list::insert: START index="+str(index))
        if x is None:
            x=linked_list_item()
        else:
            ## if necessary, make x be a linked_list_item:
            try:
                ## if this succeeds, x is already a
                ## linked_list_item, so do nothing.
                a=x.next
            except:
                ## here we need to create a linked_list_item
                ## from the passed-in item
                x=linked_list_item(x)
                
        ##print("linked_list::insert: START at a")
        if self.first is None:
            ## empty linked list
            return False
        else:
            ##print("linked_list::insert: START at b")
            ## try to insert
            try:
                node = self.nodeat(index)
            except:
                return False

            ##print("linked_list::insert: START at c")

            if node.previous is None:
                ## special code for inserting before the start node:
                self.first = x
                x.previous = None
                x.next     = node
                node.previous = x
                self.size += 1
            else:
                ## general code for inserting elsewhere:
                previous_node = node.previous
                previous_node.next=x
                x.previous = previous_node
                x.next=node
                node.previous = x
                self.size += 1

            ##print("linked_list::insert: START at d")

            return True
        

    def remove(self,x):
        """
        Removes x, the linked_list_item from the list
        Raises TypeError if x is not a linked_list_item
        Raises ValueError if linked-list is empty
        Returns True on success, False on failure
        """
        ## test if x is a linked_list_item
        try:
            a=x.next
        except:
            raise TypeError("linked_list: arg of remove() is not a linked_list_item")

        if self.size == 0:
            raise ValueError("linked_list: cannot remove item from empty linked-list")

        ## look for node to delete:
        node = self.first
        ## special case for first:
        if node == x:
            next = self.first.next
            if next is not None:
                self.first = next
                self.first.previous = None
            else:
                ## list has only item:
                self.first = None
            del node
            self.size -= 1
            return True
                
        
        ## general case:
        ret=False
        while node:
            if node == x:
                ##print("linked_list::remove: deleting node")
                previous_node = node.previous
                next_node     = node.next
                if previous_node is not None:
                    previous_node.next = next_node
                if next_node is not None:
                    next_node.previous = previous_node
                del node
                self.size -= 1
                ret = True
                break
            node = node.next

        return ret

    def nodeat(self,i):
        """
        Returns node at index i.
        First node is index 0.
        Raises TypeError if i is not an integer
        Raises ValueError if i is not within the bounds of the list,
           ie: 0 <= i < size
        """
        ## check that i is an integer between 0 and size:
        if type(i) is not int:
            raise TypeError("linked_list: arg of nodeat must an integer")
        if i<0 or i>=self.size:
            raise ValueError("linked_list: arg of nodeat must be >=0 and < size")

        index=0
        node=self.first
        while node:
            if index==i:
                return node
            node = node.next
            index += 1

        return None

    
        
class linked_list_item():
    """
    Class used for any item in a linked_list.
    """
    def __init__(self,value=None):
        self.next=None
        self.previous=None
        self.value=value

    def __str__(self):
        """
        For printing the linked-list-item
        """
        ## for printing an item:
        ret = "<linked_list_item>"
        ret += "'value': "+str(self.value)
        ##ret += "'value': "+str(self.value["identifier"])
        ret += "</linked_list_item>"
        return ret

    def copy(self):
        """
        returns a new linked_list_item, with the value attribute a copy
        of the current linked_list_item
        next and previous are both None.
        """
        b = linked_list_item()
        b.value = self.value
        return b
