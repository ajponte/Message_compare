from __future__ import print_function
from email.parser import Parser
from . import Comparator
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
Main entry point.  Given a path to the IMAP2 server, compares the message ID with the appropiate 
message on GMAIL (using IMAP search).  Outputs the contents of the message if
it is not on GMAIL.

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

def get_msg_ids(path, port, folder, usrname, passwrd):
    """Returns a list of all message ID's from the mail server's 
       folder, FOLDER associated with the PATH,using the log in credentials 
       for the user name, USRNAME, and for the password, PASSWRD."""
    msg_ids = []
    connection = imaplib.IMAP4_SSL(path, port)
    connection.login(usrname, passwrd)
    connection.select(folder)
    response, data = connection.uid('FETCH', '1:*', '(RFC822.HEADER)')
    messages = [data[i][1].strip() + "\r\nSize:" + data[i][0].split()[4]
                + "\r\nUID:" + data[i][0].split()[2]
                for i in xrange(0, len(data), 2)]
    for msg in messages:
        msg_str = email.message_from_string(msg)
        message_id = msg_str.get('Message-ID')
        msg_ids.append(message_id)
    return msg_ids
    
 
def main():
    """Main function.  Outputs directions and switches."""
    
    gmail_usr_name = raw_input("Enter the gmail user name: \n")
    gmail_passwrd = getpass.getpass("Enter the Gmail password: \n")
    print("Please wait while message IDs are populated...")
    gmail_msg_ids = get_msg_ids(GMAIL_PATH, IMAP_PORT, "[Gmail]/All Mail", gmail_usr_name, 
                                gmail_passwrd)
    pprint.pprint(gmail_msg_ids)
    IMAP2_usr_name = raw_input("Enter the IMAP2 user name: \n")
    IMAP2_passwrd = getpass.getpass("Enter the IMAP2 password: \n")
    print("Please wait while message IDs are populated")
    IMAP2_msg_ids = get_msg_ids(IMAP2_PATH, IMAP_PORT, "[Gmail]/All Mail", IMAP2_usr_name, 
                                IMAP2_passwrd)
    
    compare_ids = Comparator.Comparator(gmail_msg_ids, IMAP2_msg_ids)
    diff_msgs = compare_ids.compare()
    
    print("Here is a list of the different message IDs:\n")
    pprint(diff_msgs)
    
    
    
    
    ucb.interact()
    
def usage():
    """Calls the Usage file."""
    with open(USAGE, 'r') as f:
        for line in f:
            print(line)
        
if __name__ == "__main__":
    main()  
    
