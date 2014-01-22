'''Testing of functions.'''

import message_compare
import pprint
from ucb import  interact
import Comparator
nooptest1_msg_ids = []
nooptest2_msg_ids = []

def test_get_msg_ids():
    # To run the test for real, replace "THEPASSWORD" witb the actual password.
    '''Message IDs from nooptest1.'''
    print("Gathering all message id's for nooptest1...")
    nooptest1_msg_ids = message_compare.get_msg_ids("imap.gmail.com", 993, "[Gmail]/All Mail", "nooptest1@lbl.gov", 
                                "THEPASSWORD")
    pprint.pprint(nooptest1_msg_ids)
    
    print("Gathering all message id's for nooptest2..")
    '''Message ID's from nooptest2...'''
    nooptest2_msg_ids = message_compare.get_msg_ids("imap.gmail.com", 993, "[Gmail]/All Mail", "nooptest2@lbl.gov", "THEPASSWORD")
    pprint.pformat(nooptest2_msg_ids)
    
    return nooptest1_msg_ids, nooptest2_msg_ids

def test_comparator():
    msg_ids1 , msg_ids2 = test_get_msg_ids()
    compare_ids = Comparator.Comparator(msg_ids1, msg_ids2)
    return compare_ids.compare()
    
def main():
    diff_msgs = test_comparator()
    interact()
if __name__ == "__main__":
    main()
