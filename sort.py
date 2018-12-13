import random as rand
import time

data = [rand.randint(0, 1000000) for _ in range(100000)]
small = [rand.randint(1, 100) for _ in range(20)]

# TESTING AND VALIDATION

def time_fn(f, args, printed=False):
    start = time.time() * 1000
    r = f(*args)
    end = time.time() * 1000
    if printed:
        print(r)
    return end-start

def validate(f, v_min=1, v_max=1000000, trials=10, N_min=1, N_max=1000):
    if f([]) != sorted([]):
        return False
    for i in range(trials):
        D = [rand.randint(v_min, v_max) for _ in range(rand.randint(N_min, N_max))]
        if f(D) != sorted(D):
            return False
    return True

def runsuite(f):
    if not validate(f):
        print("Sorting function invalid!")
        return
    rt = time_fn(f, (data,))
    st = time_fn(sorted, (data,))
    print("-----------------------------------------------------\nFunction", f, \
            "\n-----------------------------------------------------\nRuntime: %.5f ms" % rt, \
            "\nSlower by %.5f ms vs default (%.5f ms)" % (rt-st, st))

def swap(L, i, j):
    L[i], L[j] = L[j], L[i]

#######################################################################################

def insertion_sort(D):
    for i in range(len(D)):
        minV = D[i]
        minI = i
        for k in range(i+1, len(D)):
            if D[k] < minV:
                minV = D[k]
                minI = k
        D[i], D[k] = minV, D[i]
    return D

########################################################################################

class MinHeap:
    def __init__(self):
        self.heap = [None]
        self.i = 1

    def bubbleup(self, i):
        p = i // 2
        while p > 0 and self.heap[i] < self.heap[p]:
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p
            p = i // 2

    def downshift(self, c, i_max):
        while c * 2 <= i_max:
            p1, p2 = c * 2, c * 2 + 1
            p = p1 if (p2 > i_max) or (self.heap[p1] < self.heap[p2]) else p2
            if self.heap[p] < self.heap[c]:
                self.heap[p], self.heap[c] = self.heap[c], self.heap[p]
                c = p
            else:
                break

    def insert(self, e):
        if len(self.heap) == self.i:
            self.heap.append(e)
        else:
            self.heap[self.i] = e
        self.bubbleup(self.i)
        self.i += 1

    def pop(self):
        if self.i == 1:
            return None
        top = self.heap[1]
        self.i -= 1
        self.heap[1] = self.heap[self.i]
        self.downshift(1, self.i)
        return top

    def peek(self):
        if self.i == 1:
            return None
        return self.heap[1]

    def bulk_heapify(self):
        i_max = self.i - 1  
        N = i_max // 2
        for i in range(N, 0, -1):
            self.downshift(i, i_max)

    def bulk_insert(self, D):
        d_i = 0
        preallocated = len(self.heap) - self.i
        for i in range(preallocated):
            self.heap[preallocated+i] = D[d_i+i]
        d_i = preallocated
        for e in D[d_i:]:
            self.heap.append(e)
        self.i += len(D)
        self.bulk_heapify()

def heapsort(D):
    heap = MinHeap()
    for e in D:
        heap.insert(e)
    return [heap.pop() for _ in range(len(D))]

def bulk_heapsort(D):
    heap = MinHeap()
    heap.bulk_insert(D)
    return [heap.pop() for _ in range(len(D))]

##############################################################################

def insertion_sort(D):
    D_copy = D
    for i,e in enumerate(D_copy):
        j = i
        while j > 0 and D_copy[j] < D_copy[j-1]:
            D_copy[j-1], D_copy[j] = D_copy[j], D_copy[j-1]
            j -= 1
    return D_copy

##############################################################################

def mergesort(D):
    def merge(l1, l2):
        i = j = 0
        len1, len2 = len(l1), len(l2)
        ml = []
        while i < len1 and j < len2:
            if l1[i] < l2[j]:
                ml.append(l1[i])
                i += 1
            else:
                ml.append(l2[j])
                j += 1
        return ml + (l1[i:] if j == len2 else l2[j:])

    def divide(D, threshhold=25):
        if len(D) <= 1:
            return D
        if len(D) < threshhold:
            return insertion_sort(D)
        pivot = len(D) // 2
        return merge(divide(D[:pivot], threshhold), divide(D[pivot:], threshhold))
    return divide(D, 10)

##############################################################################

def quicksort(D):
    def partition(partD):
        high = 0
        L = len(partD)
        swap(partD, L // 2, L-1)
        pivot = partD[-1]
        for i in range(L-1):
            if partD[i] <= pivot:
                swap(partD, i, high)
                high += 1
        swap(partD, high, L-1)
        return high

    def qsort(D, threshhold=25):
        if len(D) <= 1:
            return D
        if len(D) < threshhold:
            return insertion_sort(D)
        mid = partition(D)
        return qsort(D[:mid]) + qsort(D[mid:])
    D_copy = D
    return qsort(D_copy, int(len(D)*0.2))
