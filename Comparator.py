'''
A comparator takes two lists of message IDs and determines which IDs are similar.
Created on Jan 21, 2014

@author: aponte
'''

import pprint
class Comparator():
    """A new comparator which will compare message IDs between 
       IDS_LIST1 and IDS_LIST2."""
    def __init__(self, ids_list1, ids_list2):
        self.ids1 = ids_list1
        self.ids2 = ids_list2
        self.diff_messages = []

    def compare(self):
        """Comapres the messages between IDS_LIST1 and IDS_LIST2 to
           find all differences.  Returns a list of the differences."""
        for curr_id in self.ids1:
            if curr_id not in self.ids2:
                self.diff_messages.append(curr_id)
        return self.diff_messages

    def print_diff_messages(self):
        """Prints a formatted list of the messages that differ between IDS_LIST1
           and IDS_LIST2."""
        pprint.pprint(self.diff_messages)


                
