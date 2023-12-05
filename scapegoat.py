from __future__ import annotations
import json
import math
from typing import List

# Node Class
# You may make minor modifications.

class Node():
    def  __init__(self,
                  key        = None,
                  value      = None,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# Scapegoat Tree Class.
# DO NOT MODIFY.
class SGtree():
    def  __init__(self,
                  a    : int  = None,
                  b    : int  = None,
                  m    : int  = None,
                  n    : int  = None,
                  root : Node = None):
        self.m     = 0
        self.n     = 0
        self.a     = a
        self.b     = b
        self.root  = None

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "k": node.key,
                "v": node.value,
                "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    def insert(self, key: int, value: str):
        # Fill in the details.
        if self.root == None:
            self.m = self.m+1
            self.n = self.n+1
            self.root = Node(key = key, value = value, parent = None)
        else:
            (self.root, temp) = self.insertHelp(self.root, key, value, None, True, 0)
        
    def insertHelp(self, curr: Node, key, value, parent, balancing, depth):
        if curr == None:
            if balancing:
                self.m = self.m+1
                self.n = self.n+1
            scapegoat = False
            if depth > math.log(self.m, self.b/self.a):
                scapegoat = True
            return (Node(key = key, value = value, parent = parent), scapegoat)
        else:
            if key > curr.key:
                (curr.rightchild, scapegoat) = self.insertHelp(curr.rightchild, key, value, curr, balancing, depth+1)
                if balancing and scapegoat:
                    (curr, scapegoat) = self.rebalance(curr, parent)
                return (curr, scapegoat)
            else:
                (curr.leftchild, scapegoat) = self.insertHelp(curr.leftchild, key, value, curr, balancing, depth+1)
                if balancing and scapegoat:
                    (curr, scapegoat) = self.rebalance(curr, parent)
                return (curr, scapegoat)
            
    def rebalance(self, curr: Node, parent):
        left = self.size(curr.leftchild)
        right = self.size(curr.rightchild)
        if right/(left+right+1) > self.a/self.b:
            (listKey, listValue) = (self.inorder(curr))
            listKey = self.binary(listKey)
            listValue = self.binary(listValue)
            curr = Node(key = listKey[0], value = listValue[0], parent = parent)
            for i in range(1, len(listKey)):
                self.insertHelp(curr, listKey[i], listValue[i], parent, False, 0)
            return (curr, False)
        elif left/(left+right+1) > self.a/self.b:
            (listKey, listValue) = (self.inorder(curr))
            listKey = self.binary(listKey)
            listValue = self.binary(listValue)
            curr = Node(key = listKey[0], value = listValue[0], parent = parent)
            for i in range(1, len(listKey)):
                self.insertHelp(curr, listKey[i], listValue[i], parent, False, 0)
            return (curr, False)
        else:
            return (curr, True)
        
    def binary(self, list):
        if list == []:
            return []
        else:
            temp = int(len(list)/2)
            return [list[temp]] + self.binary(list[:(temp)]) + self.binary(list[(temp+1):])

    def size(self, curr):
        if curr == None:
            return 0
        else:
            return 1 + self.size(curr.rightchild) + self.size(curr.leftchild)
        
    def inorder(self, curr):
        if curr == None:
            return ([], [])
        else:
            (leftKey, leftValue) = self.inorder(curr.leftchild)
            (rightKey, rightValue) = self.inorder(curr.rightchild)
            return (leftKey + [curr.key] + rightKey, leftValue + [curr.value] + rightValue)

    def delete(self, key: int):
        if key == self.root.key and self.root.leftchild == None and self.root.rightchild == None:
            self.root = None
            self.m = 0
            self.n = 0
        else:
            self.root = self.deleteHelp(self.root, key, True)
            self.root = self.deleteBalance()

    # def deleteHelp(self, curr: Node, key:int):
    #     if key == curr.key:
    #         if curr.leftchild == None and curr.rightchild == None:
    #             return None
    #         elif curr.leftchild == None:
    #             return curr.rightchild
    #         elif curr.rightchild == None:
    #             return curr.leftchild
    #         else:
    #             temp = self.inOrderSucc(curr.rightchild)
        
    def deleteHelp(self, curr: Node, key:int, first):
        if key == curr.key:
            if first:
                self.n = self.n-1
            if curr.leftchild == None and curr.rightchild == None:
                return None
            elif curr.leftchild == None:
                return curr.rightchild
            elif curr.rightchild == None:
                return curr.leftchild
            else:
                (tempKey, tempValue) = self.inOrderSucc(curr.rightchild)
                curr.rightchild = self.deleteHelp(curr.rightchild, tempKey, False)
                # self.root = self.deleteBalance()
                curr.key = tempKey
                curr.value = tempValue
                return curr
        elif key > curr.key:
            curr.rightchild = self.deleteHelp(curr.rightchild, key, first)
            # self.root = self.deleteBalance()
            return curr
        else:
            #print("LEFT")
            curr.leftchild = self.deleteHelp(curr.leftchild, key, first)
            # self.root = self.deleteBalance()
            return curr

    def deleteBalance(self):
        if self.m > 2*self.n:
            #print("BALANCE")
            (listKey, listValue) = (self.inorder(self.root))
            listKey = self.binary(listKey)
            listValue = self.binary(listValue)
            self.m = self.n
            self.root = Node(key = listKey[0], value = listValue[0], parent = None)
            for i in range(1, len(listKey)):
                self.insertHelp(self.root, listKey[i], listValue[i], None, False, 0)
            return self.root
        else:
            return self.root
    
    def inOrderSucc(self, curr: Node):
        if curr.leftchild == None:
            return (curr.key, curr.value)
        return self.inOrderSucc(curr.leftchild)

    def search(self, search_key: int) -> str:
        list = "["
        list = self.searchHelp(self.root, search_key, list)
        return list
    
    def searchHelp(self, curr: Node, key, acc):
        if key == curr.key:
            return acc + '"' + curr.value + '"' + "]"
        else:
            acc = acc + '"' + curr.value + '"' + ", "
            if key > curr.key:
                return self.searchHelp(curr.rightchild, key, acc)
            else:
                return self.searchHelp(curr.leftchild, key, acc)
