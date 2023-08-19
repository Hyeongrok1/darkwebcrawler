from cryptos import *
c = Bitcoin()

# create wallet
import hashlib 
priv = hashlib.sha256('kisia_lim'.encode('utf-8')).hexdigest()
pub = c.privtopub(priv)
addr = c.pubtoaddr(pub)
print(addr)

def bitcoinInfo(addr):
    inputs = c.unspent(addr)
    total = 0
    for i in inputs:
        # print(i)
        total += i["value"]
        print(i)
        if i["address"] != addr:
            bitcoinInfo(i["address"])
        
    print(total)
    
addr = "1LQoWist8KkaUXSPKZHNvEyfrEkPHzSsCd"

bitcoinInfo(addr)