from __future__ import print_function
import Comparator
import Accumulator
import os
import sys
import pprint
import getpass
import ucb
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
OUTPUT_FILE = "output/fwMail2000d.txt"

'''The default IMAP2 folder to grab Message-IDs from.'''
IMAP2_FOLDER = "fwMail2000d"

'''The default Gmail folder to grab Message-IDs from.'''
GMAIL_FOLDER = "fwMail2000d"

'''The default line separator for output.'''
LINE_SEPARATOR = "--------------------------------\n"

def header_info(msg_ids, accumulator):
    """Given a list of MESSAGE-IDs, prints the associated headers.
       associated with the messages in the ACCUMULATOR."""
    headers = []
    for ms_id in msg_ids:
        if ms_id in accumulator.headers_map.keys():
            headers.append(accumulator.headers_map[ms_id])
    return headers
         

     
def main():
    """Main function.  Prompts user for input.  Outputs the Message-ID
       of each message in both the source and destination.  Outputs the 
       number of messages which are different between source and destination.
       Sends a formatted table with the header content of the missing messages
       to OUTPUT_FILE."""
    
    ####GET ALL MESSAGES FROM GMAIL###
   # gmail_usr_name = raw_input("Enter the gmail user name: \n")
   # gmail_passwrd = getpass.getpass("Enter the Gmail password: \n")
    print("Please wait while message IDs for Gmail are populated...")
    gmail_accumulator = Accumulator.Accumulator(GMAIL_PATH, "usr_name", "pass",
                                                IMAP_PORT, GMAIL_FOLDER)
    gmail_msg_ids = gmail_accumulator.get_ids()
    pprint.pprint(gmail_msg_ids)
    
    ####GET ALL MESSAGES FROM IMAP###
    #IMAP2_usr_name = raw_input("Enter the IMAP2 user name: \n")
    #IMAP2_passwrd = getpass.getpass("Enter the IMAP2 password: \n")
    print("Please wait while message IDs for IMAP are populated")
    
    IMAP2_accumulator = Accumulator.Accumulator("imap2.lbl.gov", "usr-name", "pass,
                                                IMAP_PORT, IMAP2_FOLDER)
    IMAP2_msg_ids = IMAP2_accumulator.get_ids()
    pprint.pprint(IMAP2_msg_ids)
    
    gmail_unique_ids = gmail_accumulator.get_unique_ids()
    ###FIND THE DIFFERENCES BETWEEN IMAP AND GMAIL.####
    compare_ids = Comparator.Comparator(IMAP2_msg_ids, gmail_unique_ids)
    diff_ids = compare_ids.compare()
    
    ###FIND THE DUPLICATE IDs FROM IMAP2.###
    
    dups = IMAP2_accumulator.get_duplicate_ids()
    dup_headers = header_info(dups, IMAP2_accumulator)
    print("{num_msgs} messages in IMAP2/{fldr}\n".format(num_msgs = IMAP2_accumulator.count_ids(), fldr = IMAP2_accumulator.folder))
    print("{num_msgs} messages in GMAIL/{fldr}\n".format(num_msgs = gmail_accumulator.count_ids(), fldr = gmail_accumulator.folder))
    
    print("-------------------------------------------------------------------------------------")
    print("There are {num} messages in IMAP2/{fldr1} which are not in Gmail/{fldr2}\n".format(num = len(diff_ids),
                                                                                            fldr1 = IMAP2_accumulator.folder,
                                                                                            fldr2 = gmail_accumulator.folder))
    print("--------------------------------------------------------------------------------------")
    pprint.pprint(diff_ids)

    print("Here is a list of the headers of each message ID which is not in Gmail:\n")
    headers = header_info(diff_ids, IMAP2_accumulator)

    ###print a table of the info of the missing messages.###
    table = prettytable.PrettyTable(["TO", "FROM", "SUBJECT"])
    table.align["TO"] = "l"
    table.padding_width = 1
    for hdr in headers:
        table.add_row(hdr)
    print(table)


    ###write the output to OUTPUT_FILE.###

    output_file = open(OUTPUT_FILE, 'w')
    output_file.write("\n")
    output_file.write("{num_msgs} messages in IMAP2/{fldr}\n".format(num_msgs = IMAP2_accumulator.count_ids(), fldr = IMAP2_accumulator.folder))
    output_file.write("{num_msgs} messages in GMAIL/{fldr}\n".format(num_msgs = gmail_accumulator.count_ids(), fldr = gmail_accumulator.folder))
    output_file.write("There are {num} messages in IMAP2/{fldr1} which are not in Gmail/{fldr2} \n".format(num = len(diff_ids),
                                                                                            fldr1 = IMAP2_accumulator.folder,
                                                                                           fldr2 = gmail_accumulator.folder))

    ###OUUTPUT THE TABLE###

    output_file.write(str(table)) 
    output_file.write(LINE_SEPARATOR)

    output_file.close()

    ucb.interact()

def usage():
    """Calls the Usage file."""
    with open(USAGE, 'r') as f:
        for line in f:
            print(line)
        
if __name__ == "__main__":
    main()  
    
