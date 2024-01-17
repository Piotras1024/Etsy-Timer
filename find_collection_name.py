import re
from email_reader import emails_from_sender

print(emails_from_sender)


# txt = '''<https://www.etsy.com/transaction/DUPA-CYCKI-OGIEN-RZEPA-WALL-ART-LABEL-OPCJA-DSADLKJKADSJKLASJKLASDKSADLK;SDA;LASDJKSDAJKLSDAJLK____ASDASDSALKFDLKAFSMKLFKLA==EMAIL-Z-DUPY>
# DupaMoja Cycki Moje Zycie moje, niebieskie niebo lala
# <https://www.etsy.com/transaction/jalsoiljk;saasdjlkasdlkjjklsdajklasfjklsafjklsadjklsdajkl;asdkjl;adsjklasdjkl ajkasdkads;jlkasdlkjadsjlkasd jlasd;jkjkal; jaksdjkals afjks jfas  jkla fjkfdnjk hlgsdnjkhdsnhjklfnjkhsfnkfjsdsfd njsgnjdhsgdnhjgsdnbhgshn ugs nhigsndhi> '''

i = 0
for email in emails_from_sender:
    i += 1
    txt = email['collection_name']
    # Wyrażenie regularne do wyodrębnienia tekstu między linkami i entrem
    pattern = r'<https://www\.etsy\.com/transaction/.*?>(.*?)<https://www\.etsy\.com/transaction'
    print(txt)
    print('--------------------------------------------------------------------------------')
    # Wyszukaj dopasowanie do wyrażenia regularnego
    match = re.search(pattern, txt, re.DOTALL)

    if match:
        # Wyodrębnij dopasowany tekst
        collection_name = match.group(1)
        print("Collection Name:", collection_name)
    else:
        print("No match")

print(i)

'''
W kontekście twojego kodu, re.DOTALL jest używane, aby umożliwić dopasowanie tekstu,
 który może zawierać znaki nowej linii (\n) między 
 <https://www.etsy.com/transaction/tutaj_cokolwiek_aż_do_znaku_większości_> a 
 <https://www.etsy.com/transaction. Bez tej opcji, znaki nowej linii byłyby 
 ignorowane, a dopasowanie mogłoby zostać przerwane na znaku nowej linii.
'''
