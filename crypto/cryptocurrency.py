import rsa
import binascii
import hashlib
import sys
import datetime
import os

def name():
    print("CamCoin(TM)")

def genesis():
    file = open("block_0.txt", "w")
    file.write("And thus began the uprising")
    file.close()
    print("Genesis block created in 'block_0.txt'")

def generate():
    public, private = rsa.newkeys(1024)
    saveWallet(public, private, sys.argv[1])
    print("New wallet generated in " + sys.argv[1] + " with signature " + address())

def address():
    public, private = loadWallet(sys.argv[1])
    tag = hashlib.sha256(public)
    str = bytesToString(tag)
    return(str.substring(0,15))

def fund():
    specialID = "wampum"
    file = open(sys.argv[3], "w")
    file.write("From: " + specialID + "\n")
    file.write("To: " + sys.argv[1] + "\n")
    file.write("Amount: " + sys.argv[2] + "\n")
    file.write("Date: " + str(datetime.datetime.today()) +"\n")

    file.write("Signature: wampum")

    print("Funded " + sys.argv[1] + " with " + sys.argv[2] + "CamCoins on " + str(datetime.datetime.today()))

def transfer():
    file = open(sys.argv[4], "w")
    file.write("From: " + address() + "\n")
    file.write("To: " + sys.argv[2] + "\n")
    file.write("Amount: " + sys.argv[3] + "\n")
    file.write("Date: " + str(datetime.datetime.today()) + "\n")

    public, private = loadWallet(sys.argv[1])
    sig = rsa.sign(sys.argv[4], private, 'SHA-256')
    file.write(sig)
    print("Transferred " + sys.argv[3] + " from " + sys.argv[1] + " to " + sys.argv[2] + " and the statement to '" + sys.argv[4] + "' on " + str(datetime.datetime.today()))

def balance():
    i = 1
    count = 0
    exists = os.path.isfile('block_' + str(i) + '.txt')
    while exists:
        file = open('block_'+ str(i) +'.txt', 'r')
        for line in file:
            line = file.readline()
            arr = line.split()
            if sys.argv[1] in arr:
                if arr.index('to') < arr.index(sys.argv[1]):
                    count += int(arr[1])
                else:
                    count-= int(arr[1])

        i+=1
        exists = os.path.isfile('block_' + str(i) + '.txt')

    exists = os.path.isfile('ledger.txt')
    while exists:
        ledger = open('ledger.txt', 'r')
        for line in ledger:
            line = ledger.readline()
            arr = line.split()
            if sys.argv[1] in arr:
                if arr.index('to') < arr.index(sys.argv[1]):
                    count += int(arr[1])
                else:
                    count -= int(arr[1])

    return count

def verify():
    public, private = loadWallet(sys.argv[1])

    file = open(sys.argv[2], 'r')

    sender = file.readline()
    a = sender.split()
    z = a[1]
    message = sender

    receiver = file.readline()
    b = receiver.split()
    y = b[1]
    message += receiver

    amount = file.readline()
    c = amount.split()
    x = int(c[1])
    message += amount

    date = file.readline()
    d = date[6:]
    message += date

    sig = file.readline()

    if not rsa.verify(message, sig, public):
        print("Verification failed!")
    elif x > balance():
        print("Not sufficient funds")
    else:
        ledger = open('ledger.txt', 'w')
        ledger.write(z + " transferred " + str(x) + " to " + y + " on " + d)

def mine():
    i = 1
    exists = os.path.isfile('block_' + str(i) + '.txt')
    while exists:
        i += 1
        exists = os.path.isfile('block_' + str(i) + '.txt')

    x = hashFile('block_' + str(i-1) + '.txt')

    file = open('block_' + str(i) + '.txt', 'r')
    ledger = open('ledger.txt', 'r')

    file.write(x)
    file.write(ledger.read())

    block = file.read()
    leading = sys.argv[1]
    nonce = 0
    block += nonce

    hash_obj = hashlib.sha256


    #while str(hashlib.).substring(0,leading) > 0:

def validate():
    i = 1
    exists = os.path.isfile('block_' + str(i) + '.txt')
    while exists:
        file = open('block_' + str(i) + '.txt', 'r')
        if hashFile('block_' + str(i-1) + '.txt') != file.readline():
            print("Chain is not valid")
            return
    print("Blockhain validated")













#gets the hash of a file; from https://stackoverflow.com/a/44873382
def hashFile(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# given an array of bytes, return a hex reprenstation of it
def bytesToString(data):
    return binascii.hexlify(data)

# given a hex reprensetation, convert it to an array of bytes
def stringToBytes(hexstr):
    return binascii.a2b_hex(hexstr)

# Load the wallet keys from a filename
def loadWallet(filename):
    with open(filename, mode='rb') as file:
        keydata = file.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    pubkey = rsa.PublicKey.load_pkcs1(keydata)
    return pubkey, privkey

# save the wallet to a file
def saveWallet(pubkey, privkey, filename):
    # Save the keys to a key format (outputs bytes)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    # Convert those bytes to strings to write to a file (gibberish, but a string...)
    pubkeyString = pubkeyBytes.decode('ascii')
    privkeyString = privkeyBytes.decode('ascii')
    # Write both keys to the wallet file
    with open(filename, 'w') as file:
        file.write(pubkeyString)
        file.write(privkeyString)
    return



