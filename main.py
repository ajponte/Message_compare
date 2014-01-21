from __future__ import print_function
from email.parser import Parser
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
Main entry point.  Given a .emlx file, compares the message ID with the appropiate 
message on GMAIL (using IMAP search).  Outputs the contents of the message if
it is not on GMAIL.

Created on Jan 21, 2014

@author: aponte
'''

'''The file with usage messages.'''
USAGE = "Usage.txt"

'''For testing purposes.'''
IMAP2_TBIRD_FILE = "tests/input/dxMail2002c"

'''For testing purposes.'''
APPLE_MAIL_FILE = "tests/input/1410088.emlx"

def parse_email_from_file(msg):
    """Parses the file MSG for email headers.  Returns a Parser object holding 
       the headers."""
    headers = Parser().parse(open(msg, 'r'))
    return headers

def get_message_id(psr):
    """Given the Parser object PSR, which holds email header information,
       returns the Message ID of the header."""
    return psr['Message-Id']
msgID = []
msgID.append(None)
def main():
    """Main function.  Outputs directions and switches."""
    
    gmail_user = raw_input("Enter the Gmail Username:")
    gmail_passwd = getpass.getpass("Enter the password:")
    imap2_user = raw_input("Enter the IMAP2 Username:")
    imap2_passwd = getpass.getpass("Enter the password")
    gmail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    imap2 = imaplib.IMAP4_SSL('imap2.lbl.gov', 993)
    gmail.login(gmail_user, gmail_passwd)
    imap2.login(imap2_user, imap2_passwd)
    print("Here is a list of all the mailboxes we can find on Gmail:")
    pprint.pprint(gmail.list())
    print("Here is a list of all mailboxes on IMAP2:")
    pprint.pprint(imap2.list())
    ucb.interact()
    
def usage():
    """Calls the Usage file."""
    with open(USAGE, 'r') as f:
        for line in f:
            print(line)
        
if __name__ == "__main__":
    main()  
    
