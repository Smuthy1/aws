
from flask import Flask, render_template, request, url_for, redirect, session
import time
import random
import hashlib


app = Flask(__name__)
app.secret_key = b'\x1f\xa5h\x16d\xc8\xbeg\x16\x83\xc4\xb9\xb2\xfc%\xc9'


@app.route("/", methods = ['GET'])
def index(): 
	return render_template('index.html')


if __name__ == '__main__': 
   app.run(host = '0.0.0.0')

TIME = time.strftime("%a, %x, %X")
SENDER = "User0"
PAYER = "User0"

txs = []


class Blockchain():
  blockPool = []
  blocks = []
  accounts = {"User100" : 100, "User10" : 10} 
  uncTx = []

  

  def Querry(self):
    print(self.accounts)
    print(self.blocks)

  def get_prev_block_hash(self):
    if len(Blockchain.blocks) > 0:
      lastBlock = Blockchain.blocks[len(Blockchain.blocks) - 1]
      return lastBlock["Hash"]
    else:
      return 0
  
  def pack(self, blockdata):
    Blockchain.blocks.append(blockdata)
    self.menu()
  
  def create(self):

    prev_block_hash = self.get_prev_block_hash()
    transactions = []
    block_hash = ''
    hashOfblock = ''
    blockTemplate = {"Hash": '', "Prev_block_hash": '', "Transactions" : []}
    listOfKeys = ["Hash", "Prev_block_hash", "Transactions"]
    
    

    for uncTx in Blockchain.uncTx:
      transactions.append(uncTx)

    dataToHash = str(prev_block_hash) + str(transactions)
 
    for i in range(0, 10000000000000):
      if hashOfblock[0:3] != '000':
        data = str(i) + dataToHash
        hashOfblock = hashlib.sha256(str(data).encode()).hexdigest()
      else:
        break
    block_hash = hashOfblock
    

    dataForBlock = [block_hash, prev_block_hash, transactions] 
    #txCounter = Blockchain.blocks[len(Blockchain.blocks)-1]["Transactions"]

    

    for data in dataForBlock:
      blockTemplate.update({listOfKeys[dataForBlock.index(data)]:data})

 
    blockdata = blockTemplate
    Blockchain.uncTx.clear()
    self.pack(blockdata)




  def menu(self):
    print('''
      1) Create an account
      2) Check Balance
      3) Get some Money
      4) Send money
      ''')
    
    userInput = int(input("--> "))
    if userInput == 1:
      accountName = Tx().initAccount()
      print("We have created an account called: ", accountName)
      self.run()
      self.menu()
    elif userInput == 2 and len(Blockchain.accounts) != 0:
      var = str(input("Input your account name: "))
      try:
        #print(Blockchain.accounts)
        print("You have:", Blockchain.accounts[var], "tokens")
        self.menu()
      except:
        print("Invalid account name")
        self.menu()
    elif userInput == 3 and len(Blockchain.accounts) != 0:
        receiver = str(input("Input your account name: "))
        data = 'mint'
        amount = 100 
        Tx.AddTx(data, SENDER, PAYER, receiver, amount)
        print("100 tokens added")
        Tx().TransmitTx()
        self.run()
        self.menu()
    elif userInput == 4 and len(Blockchain.accounts) != 0:
        data = 'send'
        sender = str(input("Input your account name: "))
        receiver = str(input("Input the account name of the account you want to send the money to: ")) 
        payer = str(input("Input account name of the acoount that is paying for the fee: "))
        amount = int(input("Input the amount you want to send: "))

        Tx.AddTx(data,sender, payer, receiver, amount)
        Tx().TransmitTx()
        #Blockchain().Querry()
        print("Successfully sent")
        self.run()
        self.menu()
    
    elif userInput == 5:
      self.run()
    
    elif userInput == 6:
      #print(Blockchain.uncTx)
      self.Querry()
      self.menu()


    else:
      print("You need to create an account first")
      self.menu()
  

  def run(self):
      if len(self.uncTx) >= 1:
       # print(self.uncTx)
        for tx in self.uncTx:
          if self.uncTx[self.uncTx.index(tx)]["Data"] == 'send':
            sender = self.uncTx[self.uncTx.index(tx)]["Sender"]
            senderBalance = self.accounts[sender]
            amount = self.uncTx[self.uncTx.index(tx)]["Amount"]
            if senderBalance >= amount:
              afterDeductBalance = senderBalance - (amount - 1)
              self.accounts.update({sender:afterDeductBalance})
              receiver = self.uncTx[self.uncTx.index(tx)]["Receiver"]
              receiverBalance = self.accounts[receiver]
              afterAddBalance = receiverBalance + (amount - 1)
              self.accounts.update({receiver:afterAddBalance})
              self.uncTx[self.uncTx.index(tx)]["State"] = 'Approved'
            else:
              self.uncTx[self.uncTx.index(tx)]["State"] = 'Not Approved, inssuficient funds'

          if self.uncTx[self.uncTx.index(tx)]["Data"] == 'create':
            newAccount = self.uncTx[self.uncTx.index(tx)]["Receiver"]
            self.accounts[newAccount] = 0
            self.uncTx[self.uncTx.index(tx)]["State"] = 'Approved New Account'
              
            
          if self.uncTx[self.uncTx.index(tx)]["Data"] == 'mint':
            receiver = self.uncTx[self.uncTx.index(tx)]["Receiver"]
            receiverBalance = self.accounts[receiver]
            amount = self.uncTx[self.uncTx.index(tx)]["Amount"]
            afterAddBalance = receiverBalance + (amount - 1)
            self.accounts.update({receiver:afterAddBalance})  
            self.uncTx[self.uncTx.index(tx)]["State"] = 'MINT NEW TOKENS'    
            
        self.create()

      else:
        self.create()
        self.menu()

class Tx():

  def TransmitTx(self):
    for tx in txs:
      Blockchain.uncTx.append(tx)
    txs.clear()


  def AddTx(data, sender, payer, receiver, amount):
    accountTx = Transaction(data, sender, payer, receiver, amount).packTransaction()
    txs.append(accountTx)


  def initAccount(self):
    data = 'create'
    accountTx = Transaction(data).updateAccount()
    acountName = accountTx["Receiver"]
    txs.append(accountTx)
    self.TransmitTx()
    return acountName



class Transaction():
  try:
    txNumber = Blockchain.blocks[len(Blockchain.blocks)-1]["Transactions"]
  except:
    txNumber = 0

  def __init__(self, Data = '', Sender = '', Payer = '', Receiver = '', Amount = '', State = ''):
    self.data = Data
    self.time = TIME
    self.sender = Sender
    self.payer = Payer
    self.receiver = Receiver
    self.amount = Amount
    self.state = Amount


  def packTransaction(self):
    
    

    TransactionLocal = {"txNumber" : '', "Time": '', "Data" : '', "Sender" : '', "Payer" : '', "Receiver" : '',  "Amount": '', "State": ''}

    listOfData = [self.txNumber, self.time, self.data, self.sender, self.payer, self.receiver, self.amount, self.state]


    listOfKeys = ["txNumber", "Time", "Data", "Sender", "Payer", "Receiver", "Amount", "State"]

    for data in listOfData:
      if self.sender == self.payer:
        TransactionLocal.update({listOfKeys[listOfData.index(data)]:data})
        TransactionLocal.update({"Payer":self.payer})
      else:
        TransactionLocal.update({listOfKeys[listOfData.index(data)]:data})
    
    return TransactionLocal
    

  def updateAccount(self):


    randomNumber = random.randint(1,10000)
    accountName = "User" + str(randomNumber)

    TransactionLocal = {"txNumber" : '', "Time": '', "Data" : '', "Sender" : '', "Payer" : '', "Receiver" : '',  "Amount": '', "State" : ''}

    listOfData = [ self.txNumber, self.time, self.data, SENDER, PAYER, accountName, self.amount, self.state]

    listOfKeys = ["txNumber", "Time", "Data", "Sender", "Payer", "Receiver", "Amount", "State"]

    for data in listOfData:
      TransactionLocal.update({listOfKeys[listOfData.index(data)]:data})
    
    return TransactionLocal



Blockchain().menu()