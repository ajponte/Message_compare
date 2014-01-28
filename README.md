Message_compare Tool.  Version 1.1
===================================
This tool can be used for after a migration between IMAP servers.  It will output which messages (if any) didn't make it. 
The A.P.I. allows flexibility in how the main file can be constructed.
---------
Usage:
--------
  python message_compare.py
  
  Optional Arguments Include:
  ---------------
  INPUT_FILE.txt
  --------------
  Where INPUT_FILE.txt is a file of the form:
  
  server path (e.g. imap.gmail.com)
  user name (e.g. name@gmail.com)
  password
  folder (e.g. "INBOX")
  
  ----------------
  OUTPUT_FILE.txt
  ----------------
  Where OUTPUT_FILE.txt is a file where all output will be directed.
  
  
