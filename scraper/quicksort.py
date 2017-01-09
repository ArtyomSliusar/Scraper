import abc
import json


class QuickSort(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, alist):
        self.alist = alist

    def sort(self):
        self.sort_helper(self.alist, 0, len(self.alist)-1)

    def sort_helper(self, alist, first, last):
        if first < last:
            splitpoint = self.partition(alist, first, last)
            self.sort_helper(alist, first, splitpoint-1)
            self.sort_helper(alist, splitpoint+1, last)

    @abc.abstractclassmethod
    def get_value(self, alist, index):
        pass

    def partition(self, alist, first, last):
        pivotvalue = self.get_value(alist, first)
        leftmark = first+1
        rightmark = last
        done = False
        while not done:
           while leftmark <= rightmark and self.get_value(alist, leftmark) <= pivotvalue:
               leftmark = leftmark + 1
           while self.get_value(alist, rightmark) >= pivotvalue and rightmark >= leftmark:
               rightmark = rightmark -1
           if rightmark < leftmark:
               done = True
           else:
               temp = alist[leftmark]
               alist[leftmark] = alist[rightmark]
               alist[rightmark] = temp
        temp = alist[first]
        alist[first] = alist[rightmark]
        alist[rightmark] = temp
        return rightmark


class QuickSortJson(QuickSort):

    def __init__(self, json_file, sort_key):
        self.file = json_file
        self.data = self.handle_file(json_file, "load")
        super().__init__(self.data)
        self.sort_key = sort_key

    def handle_file(self, file, command):
        if command == "load":
            with open(file, 'r') as data_file:
                data = json.load(data_file)
            return data
        elif command == "dump":
            with open(file, 'w') as data_file:
                json_obj = json.dumps(self.data, indent=2)
                data_file.write(json_obj)

    def get_value(self, alist, index):
        return int(alist[index][self.sort_key])

    def sort(self):
        super().sort()
        self.handle_file(self.file, "dump")

