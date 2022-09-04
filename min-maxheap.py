#"I hereby certify that this program is solely the result of my own work (and wikipedias) and is in compliance with the Academic
#Integrity policy of the course syllabus and the academic integrity policy of the CS department.”

import random
import math
import pytest

class Node(object):
    def __init__(self, k, d):
        self.key  = k
        self.data = d
        
    def __str__(self): 
        return "(" + str(self.key) + "," + repr(self.data) + ")"
        
class Heap(object):
    def __init__(self, size):
        
        #making the inherit array
        self.__arr = [None] * size  
        
        #amount of elements
        self.__nElems = 0

    #inserting into the array/heap
    def insert(self, key, data):
            #if its full return none
            if self.__nElems >= len(self.__arr):  
                return None 
            
            #if not full insert
            else:
                self.__arr[self.__nElems] = Node(key,data) 
                
                self.__trickleUp(int(self.__nElems)) 
                
                self.__nElems +=1 
    
    def __parent(self,cur):
        return (cur-1)//2
    
    def __grandparent(self,cur):
        return (((cur-1)//2)-1)//2
    
    def __trickleUp (self, cur):
        
        #setting the parent and grandparent of cur
        parent = self.__parent(cur)
        grandparent= self.__grandparent(cur)

        #finding the cur level
        level = math.floor(math.log2(cur+1))  
        
        #calling min or max based on level
        if level%2 == 0:                                                       
            self.__trickleUpMin(cur, parent, grandparent)               
        
        if level%2 == 1:                                                       
            self.__trickleUpMax(cur, parent, grandparent)        

    def __trickleUpMax(self,cur, parent, grandparent):
        while cur>2:
            #swap case
            if cur > 0 and (self.__arr[cur].key < self.__arr[parent].key): 
                self.__arr[cur], self.__arr[parent] = self.__arr[parent], self.__arr[cur]                       
                self.__trickleUp(parent)              
            #grandparent case
            elif self.__arr[cur].key > self.__arr[grandparent].key:   
                #swap them 
                self.__arr[cur], self.__arr[grandparent] = self.__arr[grandparent], self.__arr[cur]                          
                self.__trickleUp(grandparent)   
            #finish case fall out
            else: return 

    #Trickles up min
    def __trickleUpMin(self,cur, parent, grandparent):
        while cur>2:
            #swap case- swapping with its parent if cur> parent
            if cur > 0 and (self.__arr[cur].key > self.__arr[parent].key): 
                self.__arr[cur], self.__arr[parent] = self.__arr[parent], self.__arr[cur]                       
                self.__trickleUp(parent)              
            
            #grandparent case swap if cur is < grandparent
            elif self.__arr[cur].key < self.__arr[grandparent].key:   
                
                #swap them 
                self.__arr[cur], self.__arr[grandparent] = self.__arr[grandparent], self.__arr[cur]                          
                self.__trickleUp(grandparent)   
            
            #finish case- fall out we finished 
            else: return 

    #this function finds all the kids of the cur and returns them
    def __children(self, cur):

        leftChild = 2*cur + 1
        rightChild = leftChild + 1
        
        #A is Left
        #B is right
        leftA = 2*leftChild + 1
        leftB = leftA+1
        
        rightA = 2*rightChild + 1
        rightB = rightA + 1 
        
        return (leftChild, rightChild, leftA, leftB, rightA, rightB)
    #this function finds the min and max key and index of the kids
    def __decsendants(self, cur):

        indexMin = None
        indexMax = None
        
        #uses children function to get kids
        leftChild, rightChild, leftA, leftB, rightA, rightB= self.__children(cur)
        
        #fencepost and so you dont compare against none for min and max
        if leftChild < self.__nElems:
            #min becomes the left child for now
            min1= max1 = self.__arr[leftChild].key                                     
            indexMax= indexMin = leftChild 
            
        list= [rightChild, leftA, leftB, rightA, rightB]
        
        #go through all possible decsnadants and find the min and max of them
        for i in list:
            
            if i < self.__nElems:
               
                if self.__arr[i].key<= min1:
                    min1= self.__arr[i].key
                    indexMin = i
                
                if self.__arr[i].key>= max1:
                    max1= self.__arr[i].key
                    indexMax = i             
        
        
        return (indexMin, indexMax)
        
    def __trickleDown(self, cur):
 
        #current level
        level = math.floor(math.log2(cur+1))
        
        # if the position is even or a min line
        if level %2 == 0:        
            #use the min heap                                                                             
            self.__trickleDownMin(cur) 
            
        #if the position is odd or a max line
        else:                 
            #use the max heap 
            self.__trickleDownMax(cur) 
            
    def __trickleDownMax(self, cur):

        indexMin, indexMax = self.__decsendants(cur)
        
        leftChild, rightChild, leftA, leftB, rightA, rightB= self.__children(cur)
        
        if indexMax!=None and cur!=None:
            if leftChild < self.__nElems:
                #if it was a grandkid which was the index
                if indexMax == leftA or indexMax== rightA or indexMax==leftB or indexMax==rightB:
                    #if h[m] > h[i] then:
                    if self.__arr[indexMax].key > self.__arr[cur].key:
                        #swap h[m] and h[i]
                        self.__arr[indexMax] , self.__arr[cur] = self.__arr[cur] , self.__arr[indexMax]
                        #if h[m] < h[parent(m)] then:
                        if self.__arr[indexMax].key < self.__arr[(indexMax-1)//2].key:
                            #swap h[m] and h[parent(m)]
                            self.__arr[indexMax] , self.__arr[(indexMax-1)//2]= self.__arr[(indexMax-1)//2],  self.__arr[indexMax]
                        #PUSH-DOWN-MIN(h, m)
                        self.__trickleDown(indexMax)
                #if h[m] > h[i] then:        
                elif  self.__arr[indexMax].key > self.__arr[cur].key:
                    #swap h[m] and h[i]
                    self.__arr[indexMax], self.__arr[cur] = self.__arr[cur], self.__arr[indexMax]  
        
    def __trickleDownMin(self, cur):

        indexMin, indexMax = self.__decsendants(cur)
        
        leftChild, rightChild, leftA, leftB, rightA, rightB= self.__children(cur)
        
        if leftChild < self.__nElems:
            #if it was a grandkid which was the index
            if indexMin == leftA or indexMin== rightA or indexMin==leftB or indexMin==rightB:
                #if h[m] < h[i] then:
                if self.__arr[indexMin].key < self.__arr[cur].key:
                    #swap h[m] and h[i]
                    self.__arr[indexMin] , self.__arr[cur] = self.__arr[cur] , self.__arr[indexMin]
                    #if h[m] > h[parent(m)] then:
                    if self.__arr[indexMin].key > self.__arr[(indexMin-1)//2].key:
                        #swap h[m] and h[parent(m)]
                        self.__arr[indexMin] , self.__arr[(indexMin-1)//2]= self.__arr[(indexMin-1)//2],  self.__arr[indexMin]
                    #PUSH-DOWN-MIN(h, m)
                    self.__trickleDown(indexMin)
            #if h[m] < h[i] then:                
            elif  self.__arr[indexMin].key < self.__arr[cur].key:
                #swap h[m] and h[i]
                self.__arr[indexMin], self.__arr[cur] = self.__arr[cur], self.__arr[indexMin] 
                
              
    def removeMin(self):

        #if not remove the top element with the last element
        if self.__nElems > 0:
            key, data = self.__arr[0].key, self.__arr[0].data
            self.__nElems -= 1                          
            self.__arr[0] = self.__arr[self.__nElems]
            self.__trickleDown(0)
            return (key, data)
        
        else:
            return None,None
       
    def removeMax(self):
        data= None
        key= None    
        
        if self.__nElems == 0: return (None,None)
        cur = 0                                                                 
        left = 2*cur + 1                                                      
        right = left + 1                                                       
        
        #if there is only 1 element- the root
        if  self.__nElems== 1:                   
            key, data= self.__arr[cur].key , self.__arr[cur].data 
            self.__trickleDown(cur) 
        
        #if there is only 2 elements, root and left
        if  self.__nElems== 2:                   
            key, data= self.__arr[left].key , self.__arr[left].data 
            self.__arr[left] = self.__arr[self.__nElems-1]                    
            self.__trickleDown(left)      

       #if more than 2
        elif  self.__nElems > 2:                     
            
            if self.__arr[left].key >= self.__arr[right].key:  
                key, data= self.__arr[left].key , self.__arr[left].data 
                self.__arr[left] = self.__arr[self.__nElems-1]                  
                self.__trickleDown(left)
             
            elif self.__arr[right].key > self.__arr[left].key: 
                key, data= self.__arr[right].key , self.__arr[right].data 
                self.__arr[right] = self.__arr[self.__nElems-1]              
                self.__trickleDown(right) 
                
        #decrement elements
        self.__nElems -=1 
        
        return (key, data)      
    
    #min is the root
    def findMin(self):
        if self.__nElems > 0:
            return self.__arr[0].key , self.__arr[0].data
        return None,None      
    
    #max is the left or right or the middle if there is 1 element
    def findMax(self):
        root=0
        left=1
        right=2
        
        #if its empty there is no max
        if self.__nElems == 0: 
            return None,None
        
        #if there is one return only that
        elif self.__nElems == 1: return self.__arr[0].key ,  self.__arr[0].data

        #if there is 2 items return the left
        elif left < self.__nElems and right >= self.__nElems:
                return self.__arr[left].key,  self.__arr[left].data
        #in all other cases return either right or leftt
        else:
            if self.__arr[left].key > self.__arr[right].key:                # find the max between the children 
                return self.__arr[left].key, self.__arr[left].data
            else: return self.__arr[right].key, self.__arr[right].data
      
    def displayHeap(self):
        print("heapArray: ", end="")
        for m in range(self.__nElems):
            print(str(self.__arr[m]) + " ", end="")
        print()
        
    def __display(self, cur, indent):
        if cur < self.__nElems:
            leftChild  = 2*cur + 1      
            print((" " * indent) + str(self.__arr[cur]))
            if leftChild < self.__nElems:
                self.__display(leftChild,   indent+4)
                self.__display(leftChild+1, indent+4)
    
    def display(self): 
        self.__display(0, 0)
        
    def isMinMaxHeap(self):
            cur = 0
            size = self.__nElems
            
            #keep going until there is no children left checking the children
            while cur < size // 2: 
                leftChild, rightChild, leftA, leftB, rightA, rightB= self.__children(cur)
                level = math.floor(math.log2(cur+1)) 
    
                #if even level
                if level % 2 == 0: 
                    #if there is a right child and the right child is less than its parent or there is a left child and the left child is less than its parent  
                    if (rightChild < size and self.__arr[rightChild].key < \
                        self.__arr[cur].key) or (leftChild < size and self.__arr[leftChild].key \
                        < self.__arr[cur].key):
                        return False
                
                #if odd level
                else:   
                    #if there is a right child and it is greater than its parent or if there is a left child and it is greater than its parent
                    if (rightChild < size and self.__arr[rightChild].key > \
                        self.__arr[cur].key) or (leftChild < size and self.__arr[leftChild].key \
                        > self.__arr[cur].key):
                        return False  
                cur += 1 
            #if have not fallen out it is a heap
            return True                               
                                     
def __main():
    h = Heap(10)  # make a new heap with maximum of 31 elements
    
    for i in range(10):  # insert 30 items
        h.insert(random.randint(0, 10), chr(ord('A') + 1 + i))
    
    while True:
        ans = input("Enter s for show, i for insert, r for removemin, R for removemax, m for min, M for max:   ")
        if ans[:1] == 's':    # show
            h.display()
            
        elif ans[:1] == 'e':  # empty the heap
            h = Heap(31)
        
        elif ans[:1] == 'i':  # insert
            key  = int(input("Enter integer key to insert: "))
            data = input("Enter data to insert: ")
            h.insert(key,data)
            
                
        elif ans[:1] == 'r':  # removemin
            print(h.removeMin() )
        elif ans[:1] == 'R':  # removemax
            print(h.removeMax() )        
        elif ans[:1] == "m": #min
            print ( "it is" , h.findMin() , "that is a min")
        elif ans[:1] == "M": #max
            print ( "it is" , h.findMax() , "that is a max")   
        else:
            print("Invalid command")
           
#if __name__ == '__main__':
    #__main()       




##################Test Code######################
    # most tests are in duos so they are only
    # desribed once, usually one test for min
    # and one test for max
#################################################

def makeRandomHeap(size): #Make a random Heap
    h = Heap(size) 
    for i in range(size): 
        h.insert(random.randint(0, 100000),chr(ord('A') + 1 + i))
    return h    

#testing isHeap which tests if it is a heap
def test_isHeap_big():
    h = makeRandomHeap(100000)
    assert h.isMinMaxHeap
    
    
#testing empty overflow
def test_emptyHeap_min():
    h = Heap(1001)
    assert (None,None) == h.findMin()
    assert (None,None) == h.removeMin() 
    

def test_emptyHeap_max():
    h = Heap(100)
    assert (None,None) == h.findMax()  
    assert (None,None) == h.removeMax()  
    


#inserting 1 asserting its a heap and making sure we remove it for min and max
def test_oneMin():
    h= Heap(31)
    
    h.insert(1,"a")
    assert h.findMin() == (1,"a")
    assert h.removeMin() == (1,"a")
    
def test_oneMax():
    h= Heap(31)
    
    h.insert(1,"a")
    assert h.findMax() == (1,"a")
    assert h.removeMax() == (1,"a")
    
    
#inserting 2 asserting its a heap and making sure we remove it in correct order
def test_twoMin():
    h= Heap(31)
    h.insert(1,"a")
    h.insert(2, "b")
    assert h.findMin() == (1,"a")
    assert h.removeMin() == (1,"a")
    assert h.findMin() == (2,"b")
    assert h.removeMin() == (2,"b")

def test_twoMax():
    h= Heap(31)
    h.insert(1,"a")
    h.insert(2, "b")
    
    assert h.findMax() == (2,"b")
    assert h.removeMax() == (2,"b")
    assert h.findMax() == (1,"a")
    assert h.removeMax() == (1,"a")



#inserting 3 asserting its a heap and making sure we remove it in correct order
def test_threeMin():
    h= Heap(31)
    h.insert(1,"a")
    h.insert(2, "b")
    h.insert(3, "c")
    
    assert h.findMin() == (1,"a")    
    assert h.removeMin() == (1,"a") 
    assert h.findMin() == (2,"b")
    assert h.removeMin() == (2,"b")
    assert h.findMin() == (3,"c")
    assert h.removeMin() == (3,"c")
    

def test_threeMax():
    h= Heap(31)
    h.insert(1,"a")
    h.insert(2, "b")
    h.insert(3, "c")
    assert h.findMax() == (3,"c")
    assert h.removeMax() == (3,"c")
    assert h.findMax() == (2,"b")
    assert h.removeMax() == (2,"b")
    assert h.findMax() == (1,"a")    
    assert h.removeMax() == (1,"a")    

#inserting a bunch of ordered pairs asserting its a heap and making sure we remove it in correct order and that order is preserved, and making sure we have everything

def test_large_min_heap():
    h= Heap(27)
    for i in range (0,26):
        h.insert(i, chr(ord('A')  + i))
    
    assert h.findMin() == (0,"A") 
    assert h.removeMin() == (0,"A")  
    assert h.findMin() == (1,"B")
    assert h.removeMin() == (1,"B")
    assert h.findMin() == (2,"C")  
    assert h.removeMin() == (2,"C")  
    assert h.findMin() == (3,"D")   
    assert h.removeMin() == (3,"D")    
    assert h.findMin() == (4,"E")
    assert h.removeMin() == (4,"E")
    assert h.findMin() == (5,"F") 
    assert h.removeMin() == (5,"F") 
    
    for i in range (0,15):
        h.removeMin()
    assert h.findMin()== (21, "V")
    assert h.removeMin()== (21, "V")
    assert h.findMin()== (22, "W")
    assert h.removeMin()== (22, "W")
    assert h.findMin()== (23, "X")
    assert h.removeMin()== (23, "X")
    assert h.findMin()== (24, "Y")
    assert h.removeMin()== (24, "Y")
    assert h.findMin()== (25, "Z")
    assert h.removeMin()== (25, "Z")

def test_large_max_heap():
    h= Heap(50)
    for i in range (0,26):
        h.insert(i, chr(ord('A')  + i))
    
    assert h.findMax()== (25, "Z")
    assert h.removeMax()== (25, "Z")
    assert h.findMax()== (24, "Y")
    assert h.removeMax()== (24, "Y")
    assert h.findMax()== (23, "X")
    assert h.removeMax()== (23, "X")
    assert h.findMax()== (22, "W")
    assert h.removeMax()== (22, "W")
    assert h.findMax()== (21, "V")
    assert h.removeMax()== (21, "V")
    assert h.findMax()== (20, "U")
    assert h.removeMax()== (20, "U")
    
    for i in range (0,15):
        h.removeMax()    

    assert h.findMax() == (4,"E")
    assert h.removeMax() == (4,"E")
    assert h.findMax() == (3,"D")  
    assert h.removeMax() == (3,"D")  
    assert h.findMax() == (2,"C")    
    assert h.removeMax() == (2,"C")    
    assert h.findMax() == (1,"B")
    assert h.removeMax() == (1,"B")
    assert h.findMax() == (0,"A") 
    assert h.removeMax() == (0,"A") 
    


#inserting a lot of random stuff, removing it all and assuring the one remaining
#at the end was the largest/ smallest num inserted   

def test_huge_random_min():  
    h = Heap(1000)  # make a new heap with maximum of 31 elements
    
    for i in range(999):  # insert 30 items
        h.insert(random.randint(0, 999), "hi")    
    h.insert(1000,"hi")
     
    for i in range(999):  # remove 999 items
        h.removeMin() 
    assert h.removeMin()== (1000,"hi")

def test_huge_random_max():  
    h = Heap(1001)  # make a new heap with maximum of 31 elements
    
    for i in range(999):  # insert 30 items
        h.insert(random.randint(0, 999), "hi")    
    h.insert(-1,"hi")
     
    for i in range(999):  # remove 999 items
        h.removeMax() 
    assert h.removeMax()== (-1,"hi")
    

#inserting a lot of same and making sure only that comes out
def test_inserting_all_of_the_same_thing_max():
    h = Heap(1000)  # make a new heap with maximum of 31 elements
    
    for i in range(999):  # insert 999 items
        h.insert(1, "hi")    
     

    for i in range(990):  # remove 990 items
        assert h.removeMax()== (1,"hi")    

def test_inserting_all_of_the_same_thing_min():
    h = Heap(1000)  # make a new heap with maximum of 31 elements
    
    for i in range(999):  # insert 999 items
        h.insert(1, "hi")    
     
    for i in range(990):  # remove 990 items
        assert h.removeMin()== (1,"hi")    


def test_isHeap():
    h = makeRandomHeap(1000) 
    assert h.isMinMaxHeap()
    
    
#adding random elems from a heap to a list and asserting in multiple ways if they are in order
def test_assert_random_inserts_are_in_order_min():
    h = makeRandomHeap(1000) 
    
    list=[]
     
    #remove and add to list
    for i in range(999):
        r= h.removeMin()[0]
        list+= [r]

    assert list[1]<= list[2]
    assert list[2]<= list[3]
        
    for i in range (len(list)-1):
        assert list[i] <= list[i+1]
    
    assert all(list[i] <= list[i+1] for i in range(len(list) - 1))   


def test_assert_random_inserts_are_in_order_max_HUGE(): #I wanted to do bigger but my mac hated it
    h = makeRandomHeap(10000) 
    
    list=[]
     
    #remove and add to list
    for i in range(10000):
        r= h.removeMax()[0]
        list+= [r]
    
    assert list[1]>= list[2]
    assert list[2]>= list[3]
   
    #asserting the whole list is in order  
    for i in range (1999):
        assert list[i] >= list[i+1]
def test_assert_random_inserts_are_in_order_min_HUGE(): #I wanted to do bigger but my mac hated it
    h = makeRandomHeap(10001) # make a new heap with maximum of 31 elements

    list=[]
     
    #remove and add to list
    for i in range(10000):
        r= h.removeMin()[0]
        list+= [r]

    assert list[1]<= list[2]
    assert list[2]<= list[3]
        
    for i in range (len(list)-1):
        assert list[i] <= list[i+1]
    
#addinf random elements to a heap addinf to list and assuring its in order
def test_assert_random_inserts_are_in_order_min_2():
    h = makeRandomHeap(2000) 
    
    list=[]
     
    #remove and add to list
    for i in range(2000):
        r= h.removeMin()[0]
        list+= [r]
    assert all(list[i] <= list[i+1] for i in range(len(list) - 1))   

def test_assert_random_inserts_are_in_order_max_2():
    
    h = makeRandomHeap(2000) 
    
    list=[]
     
    #remove and add to list
    for i in range(2000):
        r= h.removeMax()[0]
        list+= [r]
        
    assert all(list[i] >= list[i+1] for i in range(len(list) - 1))   
    
#putting random inserted heap in list and asserting the first and last are min and max  
def test_max_of_list_is_the_first_and_min_last():
    h = makeRandomHeap(1000)  # make a new heap with maximum of 1000 elements

    list=[]
    #remove and add to list
    for i in range(999):
        r= h.removeMax()[0]
        list+= [r]    
    assert list[0]== max(list)
    assert list[-1]== min(list)

def test_min_of_list_is_the_first_and_max_last():
    
    h = makeRandomHeap(1000)   
     
    list=[]
    #remove and add to list
    for i in range(999):
        r= h.removeMin()[0]
        list+= [r]    
    assert list[0]== min(list)
    assert list[-1]== max(list)
    
# in an ordered list the RemoveMin should be the next min of heap and max should be the next max of heap
def test_against_OrderedList():
    lists=[]
    h = Heap(10001)
    for i in range(10000):
        lists+= [i]
        h.insert(i, "hi") 
    
    for i in range (5000):
        minFind= h.findMin()
        maxFind= h.findMax()
        min= h.removeMin()
        max= h.removeMax()
        assert min[0]== lists[i]
        assert min == minFind
        assert max[0]== lists[9999-i]
        assert max == maxFind

#add random elements to a heap and list, sort the list and see if its in order with max and min calls simotaneously
def test_against_unOrderedList():
    lists=[]
    h = Heap(10001)
    for i in range(10000):
        r= random.randint(0,1000)
        lists+= [r]
        h.insert(r, "hi") 
    lists.sort()
    for i in range (5000):
        min= h.removeMin()[0]
        max= h.removeMax()[0]
        assert min== lists[i]
        assert max== lists[9999-i]

#add random elements to a heap and list, sort the list and see if its in order with max 
#and min
def test_against_unOrderedList_max():
    lists=[]
    h = Heap(10001)
    for i in range(10000):
        r= random.randint(0,1000)
        lists+= [r]
        h.insert(r, "hi") 
    lists.sort()
    for i in range (9999,0,-1):
        max= h.removeMax()[0]
        assert max== lists[i]


def test_against_unOrderedList_min():
    lists=[]
    h = Heap(10001)
    for i in range(10000):
        r= random.randint(0,1000)
        lists+= [r]
        h.insert(r, "hi") 
    lists.sort()
    for i in range (10000):
        max= h.removeMin()[0]
        assert max== lists[i]

#add  to list and heap sort list and remove max and min and assert they are min and max
def test_against_random_list_():  
    
    for i in range(5):
        lists=[]
        h = Heap(10001)
        value= None        
        for i in range(10000):
            value= random.randint(0,999999)
            lists+= [value]
            h.insert(value, "hi") 
        
        lists.sort()
        
        for i in range (5000):
            min1= h.removeMin()[0]
            max1= h.removeMax()[0]
            assert min1== lists[i]
            assert max1== lists[9999-i]

#adding all values toheap and list at same time removing from heap sorting list and assuring len is ok and the lists are the same
#and no values have been lost
def test_allValuesWereInserted_andPresent_andRemovedInORder():
    for i in range(1):
        lists=[]
        compare= []
        h = Heap(10001)
        value= None        
        for i in range(10000):
            value= random.randint(0,999999)
            lists+= [value]
            h.insert(value, "hi") 
    
        lists.sort()
        
        for i in range (10000):
            r= h.removeMin()
            compare+= [r[0]]
        
        
        assert compare== lists
        assert len(compare)== len(lists)== 10000
    


#adding random elements to list and heap and assuring find min is the same as min() 
#same for max
def test_findMin():
    h = Heap(10001)
    value= None  
    lists=[]
    for i in range(10000):
        value= random.randint(0,999999)
        lists+= [value]
        h.insert(value, "hi") 
        

    minHeap= h.findMin()
    minList= min(lists)
    assert minHeap[0]==minList

def test_findMax():
    h = Heap(10001)
    value= None  
    lists=[]
    for i in range(10000):
        value= random.randint(0,999999)
        lists+= [value]
        h.insert(value, "hi") 
        

    maxHeap= h.findMax()
    maxList= max(lists)
    assert maxHeap[0]==maxList


#adding random elements to list sorting the list and asserting the first element of sorted 
#list is the min of the heap removing from heap and list and continuing to check
def test_findMin_sortedList():
    h = Heap(10001)
    value= None  
    lists=[]
    for i in range(10000):
        value= random.randint(0,999999)
        lists+= [value]
        h.insert(value, "hi") 
        
    lists.sort()
    
    for i in range(9999):
        minHeap= h.findMin()
        minList= lists[0]
        assert minHeap[0]==minList 
        lists= lists[1:]
        h.removeMin()


def test_findMax_sortedList():
    h = Heap(10001)
    value= None  
    lists=[]
    for i in range(10000):
        value= random.randint(0,999999)
        lists+= [value]
        h.insert(value, "hi") 
        
    lists.sort()
    
    for i in range(9999):
        maxHeap= h.findMax()
        maxList= lists[-1]
        assert maxHeap[0]==maxList 
        lists= lists[:-1]
        h.removeMax()

pytest.main(["-v", "-s", "min-maxheap.py"])       