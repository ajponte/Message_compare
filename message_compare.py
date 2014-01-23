from __future__ import print_function
from email.parser import Parser
import Comparator
import Accumulator
import os
import sys
import re
import imaplib
import getopt
import pprint
import getpass
import ucb #to be removed later.  For testing purposes only.
import email
import logging

'''
Main entry point.  Given two paths to IMAP sources, compares the message IDs of 
the two IMAP sources. Outputs the contents of the message iff it does not appear
in both sources.

Created on Jan 21, 2014

@author: aponte

REFERENCES:
http://stackoverflow.com/questions/3775667/how-to-get-message-id-using-imaplib
'''

'''The file with usage messages.'''
USAGE = "Usage.txt"

'''The path to Gmail IMAP.'''
GMAIL_PATH = "imap.gmail.com"

'''The default IMAP port.'''
IMAP_PORT = 993;

'''The path to IMAP2.'''
IMAP2_PATH = "imap2.lbl.gov"
    
def header_info(msg_ids, accumulator):
    """Given a list of MESSAGE-IDs, prints the associated headers.
       associated with the messages in the ACCUMULATOR."""
    headers = []
    for ms_id in msg_ids:
        if ms_id in accumulator.headers_map.keys():
            headers.append(accumulator.headers_map[ms_id])
    return headers
            
    
    
     
def main():
    """Main function.  Prompts user for input."""
    
    ####GET ALL MESSAGES FROM GMAIL###
    gmail_usr_name = raw_input("Enter the gmail user name: \n")
    gmail_passwrd = getpass.getpass("Enter the Gmail password: \n")
    print("Please wait while message IDs for Gmail are populated...")
    gmail_accumulator = Accumulator.Accumulator(GMAIL_PATH, gmail_usr_name, gmail_passwrd,
                                                IMAP_PORT, "[Gmail]/All Mail")
    gmail_msg_ids = gmail_accumulator.get_ids()
    pprint.pprint(gmail_msg_ids)
    
    ####GET ALL MESSAGES FROM IMAP###
    IMAP2_usr_name = raw_input("Enter the IMAP2 user name: \n")
    IMAP2_passwrd = getpass.getpass("Enter the IMAP2 password: \n")
    print("Please wait while message IDs for IMAP2 are populated")
    
    #path is temporarily imap.gmail.com for testing.
    IMAP2_accumulator = Accumulator.Accumulator("imap.gmail.com", IMAP2_usr_name, IMAP2_passwrd,
                                                IMAP_PORT, "[Gmail]/All Mail")
    IMAP2_msg_ids = IMAP2_accumulator.get_ids()
    pprint.pprint(IMAP2_msg_ids)
    
    ###FIND THE DIFFERENCES BETWEEN IMAP AND GMAIL.####
    compare_ids = Comparator.Comparator(gmail_msg_ids, IMAP2_msg_ids)
    diff_ids = compare_ids.compare()
    
    print("Here is a list of the different message IDs:\n")
    pprint.pprint(diff_ids)
    
    print("There are {num} messages in IMAP2 which are not in Gmail".format(num = len(diff_ids)))
    
    print("Here is a list of the headers of each message ID which is not in Gmail:\n")
    
    
    ucb.interact()
    
def usage():
    """Calls the Usage file."""
    with open(USAGE, 'r') as f:
        for line in f:
            print(line)
        
if __name__ == "__main__":
    main()  
    
