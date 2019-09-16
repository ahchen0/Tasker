## OrderedTree.py
##
## by Leland Pierce, June, 2019

## needs a linked-list:
from linked_list import linked_list, linked_list_item


debug=False

## user creates their own root node.
##    with nothing in it.
## then other nodes created in it's children, and their children.
## no attempt to print the root node....
class OrderedTree():
    """
    The children are ordered (using a linked-list)
    And the nodes are organized into a tree of nodes with children.
    There is only one root node.

    Example:
    1. create an ampty tree:
    from OrderedTree import OrderedTree
    tree = OrderedTree()
    
    2. add root node
    tree_root = tree.create_node(identifier="root")

    3. add some children to the root:
    child1 = tree.create_node(identifier="child1", parent=tree_root)
    child2 = tree.create_node(identifier="child2", parent=tree_root)
    child3 = tree.create_node(identifier="child3", parent=tree_root)
    child4 = tree.create_node(identifier="child4", parent=tree_root)

    4. add children to "child1"
    child1_1 = tree.create_node(identifier="child1_1", parent=child1)
    child1_2 = tree.create_node(identifier="child1_2", parent=child1)
    child1_3 = tree.create_node(identifier="child1_3", parent=child1)

    5. remove a node:
    tree.remove_node("child1_1")

    6. debug print the tree:
    tree.print()

    """
    def __init__(self):
        """
        """
        self.identifier_prefix="treeID"
        self.identifier_count = 0
        self.root = None

    ##def __str__(self):
    ##    self.print()

    def create_node(self, identifier=None, parent=None, data=None):
        """
        Create a child node for given parent node. 
        If identifier string is absent, an ID will be generated automatically.
        parent string is the identifier of the parent.
        If parent is absent, a new root node will be created.
        on success, returns the ID as a string
        on failure, returns False
        """
        if debug:
            print("OrderedTree::create_node: start")
            print("                          identifier="+identifier)
        
        if identifier is None:
            identifier=self.identifier_prefix+str(self.identifier_count)
            self.identifier_count += 1
        else:
            if self.identifier_exists(identifier):
                ## identifier already exists
                return False
            
        if debug:
            print("OrderedTree::create_node: a")
            
        if parent is None:
            if debug:
                print("OrderedTree::create_node: parent is none, creating new root node")
            ## create new root node:
            if self.root is not None:
                ## delete existing tree:
                identifier = self.root["identifier"]
                self.remove_node(identifier)
                
            value = {} ## empty dict
            value["parent"]=None
            value["children"]=linked_list()
            value["identifier"]=identifier
            value["data"]=data
            self.root=linked_list_item(value)
            if debug:
                print("OrderedTree::create_node: after adding root node:")
                print(self.root)
        else:
            if debug:
                print("OrderedTree::create_node: parent is NOT none, creating child node")
            ## add node as child of existing node:
            if self.identifier_exists(parent):
                the_parent_node = self.get_node(parent)

                if debug:
                    print("OrderedTree::create_node: the_parent_node.identifier="+
                          the_parent_node.value["identifier"])
                    print("                          expecting: "+parent)

                value = {} ## empty dict     
                value["parent"]=the_parent_node
                value["children"]=linked_list()
                value["identifier"]=identifier
                value["data"]=data

                if debug:
                    print("OrderedTree::create_node: BEFORE adding child to parent:"+parent)
                    print("length of the list: "+str(the_parent_node.value["children"].size ))
                    print(the_parent_node.value["children"])
                the_parent_node.value["children"].append(linked_list_item(value))
                if debug:
                    print("OrderedTree::create_node: AFTER adding child to parent:"+parent)
                    print("length of the list: "+str(the_parent_node.value["children"].size ))
                    print(the_parent_node.value["children"])
            else:
                return False

            
        if debug:
            print("OrderedTree::create_node: end, identifier="+str(identifier))
        return identifier




    def create_node_before(self, index, identifier=None, parent=None, data=None):
        """
        Create a child node for given parent node.
        index is the position of an existing node that this node is to be
           placede BEFORE.
        If identifier string is absent, an ID will be generated automatically.
        parent string is the identifier of the parent.
        If parent is absent, a new root node will be created.
        on success, returns the ID as a string
        on failure, returns False
        """
        ##print("OrderedTree::create_node_before: START, index="+str(index))
        
        if identifier is None:
            identifier=self.identifier_prefix+str(self.identifier_count)
            self.identifier_count += 1
        else:
            if self.identifier_exists(identifier):
                ## identifier already exists
                return False

        ##print("OrderedTree::create_node_before: at a")
        ## must have an existing parent, with existing children
        if parent is None:
            return False

        
        ##print("OrderedTree::create_node_before: at b")
        ## add node as child of existing node:
        if self.identifier_exists(parent):
            the_parent_node = self.get_node(parent)
            
            if debug:
                print("OrderedTree::create_node_before: the_parent_node.identifier="+
                      the_parent_node.value["identifier"])
                print("                          expecting: "+parent)

            value = {} ## empty dict     
            value["parent"]=the_parent_node
            value["children"]=linked_list()
            value["identifier"]=identifier
            value["data"]=data
            
            ##print("OrderedTree::create_node_before: at C")

            if not the_parent_node.value["children"].insert(index,linked_list_item(value)):
                return False
            
            ##if debug:
            ##    print("OrderedTree::create_node_before: after adding child to parent:"+parent)
            ##    print("length of the list: "+str(the_parent_node.value["children"].size ))
            ##    print(the_parent_node.value["children"])
        else:
            return False

        return identifier




    
    def remove_node(self, identifier):
        """
        Remove a node indicated by the string identifier
        All the successors are removed as well.
        Returns the number of removed nodes.
        """
        nremoved=0
        node = self.get_node(identifier)
        if node is None:
            return 0
        
        ## the linked-list that this node is part of:
        parent_node = node.value["parent"]
        node_list = parent_node.value["children"]

        ## contains pairs in order: list from which to remove a node,
        ##                          followed by the node to remove
        remove_list=[]

        ## list I'm in, and mt node:
        children = node.value["children"]
        if node_list is not None:
            remove_list.append(node_list)
            remove_list.append(node)
            
        ## iterate over all children:
        node = children.first
        while node is not None:
            remove_list += self.remove_node_obj(node)
            try:
                node = node.next
            except:
                node = None

        ## do the removal, in inverse order:
        ## (otherwise parents are removed before children,
        ##  which makes the data structure screwed up)
        if debug:
            print("=========listing to remove============")
            for i in reversed(range(len(remove_list))):
                if i%2==0:
                    print("removing: id="+remove_list[i+1].value["identifier"])

        if debug:
            print("=========starting to remove============")
        for i in reversed(range(len(remove_list))):
            if i%2==0:
                if remove_list[i].remove(remove_list[i+1]):
                    nremoved += 1
                if debug:
                    print("nremoved="+str(nremoved))
                    self.print()
                
        return nremoved

    def remove_node_obj(self,node):
        """
        """
        ## marks a node for removal by equality not by identifier.
        ## returns list of nodes to remove (list/node)
        if node is None:
            return []
        
        ## the linked-list that this node is part of:
        parent_node = node.value["parent"]
        node_list = parent_node.value["children"]

        remove_list=[]

        children = node.value["children"]
        if node_list is not None:
            remove_list.append(node_list)
            remove_list.append(node)
            
        ## iterate over all children:
        node = children.first
        while node is not None:
            remove_list += self.remove_node_obj(node)
            try:
                node = node.next
            except:
                node = None
        
        return remove_list

    def next_sibling(self,identifier):
        """
        Returns the next sibling, the node that follows the one indicated 
        by the identifier string.
        Returns None if 'identifier' is unknown, or if there is no next-sibling.
        """
        node = self.get_node(identifier)
        if node is not None:
            try:
                return node.next
            except:
                return None
        else:
            return None
        

    def get_node(self,identifier,start=None):
        """
        Returns a node if the identifier string is valid,
        ie, if there is any node in the Tree that has this identifier string,
        else returns None
        """

        if debug:
            print("OrderedTree::get_node: input: identifier="+identifier)
            
        if start is None:
            start = self.root
            
        node = start
        if node is None:
            return None

        if node.value is None:
            return None

        if debug:
            print("OrderedTree::get_node: at a: type(node) is:")
            print(type(node))
            try:
                print("node.keys:")
                print(node.keys())
            except:
                pass
            try:
                print("node.value:")
                print(node.value)
            except:
                pass
            #print("OrderedTree::get_node: id="+node.value["identifier"])

            
        if node.value["identifier"] == identifier:
            if debug:
                print("OrderedTree:get_node: returning success")
            return node


        ## make list of next nodes:
        next_nodes = []
        
        ## children first:
        children_list = node.value["children"]
        nchildren=children_list.size
        if nchildren > 0:
            for i in range(nchildren):
                a=children_list.nodeat(i)
                if a is not None:
                    next_nodes.append(a)
                
        ## next sibling:
        try:
            a=node.next
            if a is not None:
                next_nodes.append(a)
        except:
            pass
        
        ## check each of the nodes in next-nodes:
        for i in range(len(next_nodes)):
            node =self.get_node(identifier,start=next_nodes[i])
            if node is not None:
                return node

        if debug:
            print("OrderedTree:get_node: returning None")
        return None
                
    def identifier_exists(self,identifier,start=None):
        """
        checks if the given identifier string is in this tree.
        ie, if there is any node in the Tree that has this identifier string,
        returns True if found, False otherwise.
        """
        if start is None:
            start = self.root
            
        node = start
        if node is None:
            return False
        
        if node.value["identifier"] == identifier:
            return True

        ## make list of next nodes:
        next_nodes = []
        
        ## children first:
        children_list = node.value["children"]
        nchildren=children_list.size
        if nchildren > 0:
            for i in range(nchildren):
                a=children_list.nodeat(i)
                if a is not None:
                    next_nodes.append(a)
                if debug:
                    print("OrderedTree::identifier_exists: type(nodeat("+str(i)+")) is:")
                    print(type(children_list.nodeat(i)))
                
        ## next sibling:
        try:
            a=node.next
            if a is not None:
                next_nodes.append(a)
            if debug:
                print("OrderedTree::identifier_exists: type(next_sibling) is:")
                print( type(a) )
        except:
            pass

 
        
        ## check each of the nodes in next-nodes:
        for i in range(len(next_nodes)):
            node =self.get_node(identifier,start=next_nodes[i])
            if node is not None:
                if node.value["identifier"] == identifier:
                    return True
            
        return False

    def print(self,start=None,indent=""):
        """
        debug print a tree: prints identifiers
        start should be an existing node in the tree, or None,
          to start printing at the root of the tree
        indent is a string with spaces for indenting items based 
          on parent/child relationships.
        """
        if start is None:
            start = self.root
            
        node = start
        if node is None:
            print("Empty Tree")
            return

        ##
        identifier = node.value["identifier"]
        print(indent+identifier)
        temp_indent = indent

        ## children first:
        ## children get indented more than parent
        children = node.value["children"]
        nchildren=children.size
        if nchildren > 0:
            for i in range(nchildren):
                self.print(start=children.nodeat(i), indent=temp_indent+"  ")
            
        ## next sibling:
        ## siblings are indented the same amount
        try:
            node = this.next_sibling(identifier)
            if node is not None:
                self.print(start=node,indent=temp_indent)
        except:
            pass
        
        return
        
