from __future__ import print_function
import Comparator
import Accumulator
import os
import sys
import getopt
import pprint
import getpass
from Message_Compare import ucb
import prettytable #https://code.google.com/p/prettytable/

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

'''The default file which all output will be sent to.'''
OUTPUT_FILE = "output.txt"

'''The default line seperator for output.'''
LINE_SEPERATOR = "----------------------------------"

def header_info(msg_ids, accumulator):
    """Given a list of MESSAGE-IDs, prints the associated headers.
       associated with the messages in the ACCUMULATOR."""
    headers = []
    for ms_id in msg_ids:
        if ms_id in accumulator.headers_map.keys():
            headers.append(accumulator.headers_map[ms_id])
    return headers

def print_table(lst):
    """Prints a table of the data in the list LST."""
    col_width = [max(len(x) for x in col) for col in zip(*lst)]
    for line in lst:
        print ("| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |")           
    

     
def main():
    """Main function.  Prompts user for input.  Outputs the Message-ID
       of each message in both the source and destination.  Outputs the 
       number of messages which are different between source and destination.
       Sends a formatted table with the header content of the missing messages
       to OUTPUT_FILE."""
    
    ####GET ALL MESSAGES FROM GMAIL###
    gmail_usr_name = raw_input("Enter the gmail user name: \n")
    gmail_passwrd = getpass.getpass("Enter the Gmail password: \n")
    print("Please wait while message IDs for Gmail are populated...")
    gmail_accumulator = Accumulator.Accumulator(GMAIL_PATH, gmail_usr_name, gmail_passwrd,
                                                IMAP_PORT, "Migrated/sent-mail")
    gmail_msg_ids = gmail_accumulator.get_ids()
    pprint.pprint(gmail_msg_ids)
    
    ####GET ALL MESSAGES FROM IMAP###
    IMAP2_usr_name = raw_input("Enter the IMAP2 user name: \n")
    IMAP2_passwrd = getpass.getpass("Enter the IMAP2 password: \n")
    print("Please wait while message IDs for IMAP are populated")
    
    #path is temporarily imap.gmail.com for testing.
    IMAP2_accumulator = Accumulator.Accumulator("imap.gmail.com", IMAP2_usr_name, IMAP2_passwrd,
                                                IMAP_PORT, "[Gmail]/sent-mail")
    IMAP2_msg_ids = IMAP2_accumulator.get_ids()
    pprint.pprint(IMAP2_msg_ids)
    
    ###FIND THE DIFFERENCES BETWEEN IMAP AND GMAIL.####
    compare_ids = Comparator.Comparator(gmail_msg_ids, IMAP2_msg_ids)
    diff_ids = compare_ids.compare()

    
    print("-------------------------------------------------------------------------------------")
    print("There are {num} messages in IMAP2/{fldr1} which are not in Gmail/{fldr2}\n".format(num = len(diff_ids),
                                                                                            fldr1 = IMAP2_accumulator.folder,
                                                                                            fldr2 = gmail_accumulator.folder))
    print("--------------------------------------------------------------------------------------")
    pprint.pprint(diff_ids)
    
    print("Here is a list of the headers of each message ID which is not in Gmail:\n")
    headers = header_info(diff_ids, gmail_accumulator)
    
    ###print a table of the info of the missing messages.###
    table = prettytable.PrettyTable(["TO", "FROM", "SUBJECT"])
    table.align["TO"] = "l"
    table.padding_width = 1
    for hdr in headers:
        table.add_row(hdr)
    print(table)
    
    ###write the output to OUTPUT_FILE.###

    output_file = open(OUTPUT_FILE, 'w')
    output_file.write("There are {num} messages in IMAP2/{fldr1} which are not in Gmail/{fldr2}\n".format(num = len(diff_ids),
                                                                                            fldr1 = IMAP2_accumulator.folder,
                                                                                           fldr2 = gmail_accumulator.folder))
    for ids in diff_ids:
        output_file.write(str(ids) + "\n")
    output_file.write(LINE_SEPERATOR)
    output_file.write(str(table)) 
    output_file.close()
    
    ucb.interact()
    
def usage():
    """Calls the Usage file."""
    with open(USAGE, 'r') as f:
        for line in f:
            print(line)
        
if __name__ == "__main__":
    main()  
    
