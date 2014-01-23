'''
An Accumulator accumulates message-ID's with messages from a given server.
Created on Jan 22, 2014

@author: aponte
'''
import imaplib
import pprint
import email
import ucb

class Accumulator:
    """A new Accumalor which will gather message-IDs from the folder FLDR
       on the server SVR.  Login credentials to be provided from the 
      the user name USR and passord PASSWD, using the IMAP port number PORT."""
    def __init__(self, servr, usr, passwd, port, fldr):
        self.server = servr
        self.user_name = usr
        self.folder = fldr
        self.port_num = port
        self.password = passwd
        self.count = 0
        self.msgs = []
        self.msg_ids = []
        self.msg_strings = []
        self.headers_map = {}
        
    def get_ids(self):
        """Returns a list of message-IDs from THIS server and folder.
           Adds the message-IDs to MSG_IDS and HEADERS_MAP."""
        connection = imaplib.IMAP4_SSL(self.server, self.port_num)
        connection.login(self.user_name, self.password)
        connection.select(self.folder)
        response, data = connection.uid('FETCH', '1:*', '(RFC822.HEADER)')
        messages = [data[i][1].strip() + "\r\nSize:" + data[i][0].split()[4]
                + "\r\nUID:" + data[i][0].split()[2]
                for i in xrange(0, len(data), 2)]
        for msg in messages:
            msg_str = email.message_from_string(msg)
            self.msg_strings.append(msg_str)
            message_id = msg_str.get('Message-ID')
            to = msg_str.get("To");
            frm = msg_str.get("From")
            subj = msg_str.get("Subject")
            self.add_to_headers_map(message_id, [to, frm, subj])
            self.msg_ids.append(message_id)
        self.msgs = messages
        return self.msg_ids
    
    def add_to_headers_map(self, message_id, fields):
        """Adds to the map of headers a MESSAGE-ID which is mapped to an 
           array of header FIELDS [TO, FROM, SUBJECT]."""
        self.headers_map[message_id] = fields
        
    def count_ids(self):
        """Returns the number of message-IDs in THIS."""
        self.count = len(self.msg_ids)
        return self.count;
    
    def get_msgs(self):
        """Returns a list of the unformatted messages in THIS."""
        return self.msgs
    
    def get_msg_strings(self):
        """Returns a list of the message email objects."""
        return self.msg_strings
    
    def get_header_info(self):
        """Returns a map from the message-IDs to the header of the message
           (The 'TO', 'FROM', and 'SUBJECT' fields)."""
        hdrs_map = {}
        for msg in self.msg_strings:
            msg_id = msg.get("Message-ID")
            to = msg.get('To')
            frm = msg.get('From')
            subj = msg.get("Subject")
            hdrs_map[msg_id] = [to, frm, subj]
        self.headers_map = hdrs_map
        return hdrs_map
    
    def headers_map(self):
        """Returns the map between the Message-IDs and the Headers"""
        return self.headers_map   
    
    def print_msg_ids(self):
        """Prints all message-ID's in THIS."""
        pprint.pprint(self.msg_ids)

