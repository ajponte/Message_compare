'''
An Accumulator accumulates message-ID's with messages from a given server.
Created on Jan 22, 2014

@author: aponte
'''
import imaplib
import pprint
import email

class Accumulator:
    """A new Accumalor which will gather message-IDs from the folder FLDR
       on the server SVR.  Login credentials to be provided from the 
      the user name USR and passord PASSWD, using the IMAP port number PORT."""
    def __init__(self, servr, usr = None, passwd = None, port = 993, fldr = "Inbox"):
        self.server = servr
        self.user_name = usr
        self.folder = fldr
        self.port_num = port
        self.password = passwd
        self.count = 0
        self.msg_ids = []

    def get_ids(self):
        """Returns a list of message-IDs from THIS server and folder."""
        connection = imaplib.IMAP4_SSL(self.server, self.port_num)
        connection.login(self.user_name, self.password)
        connection.select(self.folder)
        response, data = connection.uid('FETCH', '1:*', '(RFC822.HEADER)')
        messages = [data[i][1].strip() + "\r\nSize:" + data[i][0].split()[4]
                + "\r\nUID:" + data[i][0].split()[2]
                for i in xrange(0, len(data), 2)]
        for msg in messages:
            msg_str = email.message_from_string(msg)
            message_id = msg_str.get('Message-ID')
            self.msg_ids.append(message_id)
        return self.msg_ids
    
    def count_ids(self):
        """Returns the number of message-IDs in THIS."""
        return len(self.msg_ids)
        
