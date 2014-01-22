####TESTING####
import Accumulator
import ucb

test_accum = Accumulator("imap.gmail.com", "nooptest2@lbl.gov", "LottaSaulsMail", 993, "INBOX") 
ids = test_accum.get_ids()
headers = test_accum.get_header_info()   
ucb.interact()
