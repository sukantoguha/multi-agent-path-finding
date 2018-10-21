from collections import defaultdict

class ClosedList:

    def __init__(self):
         self.data_dict = defaultdict(list)

    def insert(self, item):
        self.data_dict[hash(item)].append(item)

    def __contains__(self, item):
        items = self.data_dict[hash(item)]
        if items:
            return item in items
        else:
            return False

    def get(self,item):
        items = self.data_dict[hash(item)]
        if items:
            for x in items:
                if x == item:
                    return x
        return None

    def remove(self, item):
        self.data_dict[hash(item)].remove(item)