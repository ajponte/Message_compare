'''Testing of functions.'''

import message_compare
import pprint
from ucb import  interact
def test_get_msg_ids():
    '''Message IDs from nooptest1.'''
    
    print("Gathering all message id's for nooptest1...")
    nooptest1_gmail_msg_ids = message_compare.get_msg_ids("imap.gmail.com", 993, "[Gmail]/All Mail", "nooptest1@lbl.gov", 
                                "THEPASSWORD")
    pprint.pprint(nooptest1_gmail_msg_ids)
    
    print("Gathering all message id's for S_perlmutter")
    '''Message ID's from s_perlmutter@lbl.gov.'''
    saul_gmail_msg_ids = message_compare.get_msg_ids("imap.gmail.com", 993, "[Gmail]/All Mail", "s_perlmutter@lbl.gov", "THEPASWORD")
    
def main():
    test_get_msg_ids()
    interact()
if __name__ == "__main__":
    main()
