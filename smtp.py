import smtplib
import os
from dotenv import load_dotenv

i = 0
while i < 1:
    print(i)
    i += 1
    load_dotenv()
    
    s = smtplib.SMTP("smtp.gmail.com", 587)
    
    s.starttls()
    
    
    s.login("fh024163@gmail.com", os.environ["MAILPW"])
    
    s.sendmail(
        "fh024163@gmail.com",
        "F.Huber1@htlkrems.at",
        "Subject: Neuer Login-Versuch\n\nhttps://mis-hdt4.onrender.com."
    )
 
 
 