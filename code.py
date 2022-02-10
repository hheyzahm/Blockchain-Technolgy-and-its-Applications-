import collections
import hashlib
from datetime import date


class Block:
    def __init__(self, index, timeStamp, transaction, previousHash=''):
        self.transaction = transaction
        self.previousHash = previousHash
        self.index = index
        self.timeStamp = timeStamp
        self.nounce = 0
        self.hash = self.calculateHash()

    # includes all the content in the sha256 hash and then calculates the hash
    def calculateHash(self):
        strng = str(self.nounce) + str(self.index) + str(self.timeStamp) + str(self.previousHash) + str(self.transaction)
        return hashlib.sha256(strng.encode()).hexdigest()

    # this function mines the blocks to the block chain
    def mineBlock(self, difficulty):
        while list(self.hash[0:difficulty]) != ['0'] * difficulty:
            if(self.nounce==4000000000):
                return False
            self.nounce = self.nounce + 1
            self.hash = self.calculateHash()
        return True



# a class for transactions
class Transaction:
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount


class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.difficulty = 1
        self.pendingTransaction = []
        self.miningReward = 100
        self.index = 1

    def createGenesisBlock(self):
        return Block(0, 'today', [], 'null hash')

    # gets the last block in the blockchain list
    def getLatestBlock(self):
        return self.chain[-1]

    #takes the transactions from the thread pool and adds them into hte block
    def minePendingTransaction(self, miningRewardAddress):
        self.pendingTransaction.sort(key=lambda x:x.amount,reverse=True)
        sletedTransaction=self.pendingTransaction[:2]
        block = Block(self.index, date.today(), sletedTransaction, self.getLatestBlock().hash)
        remove=self.pendingTransaction[:2]
        for i in remove:
            self.pendingTransaction.remove(i)
        result=block.mineBlock(self.difficulty)
        while(result==False):
            if len(self.pendingTransaction)==0:
                break
            self.pendingTransaction.append(remove[:1])
            sletedTransaction.remove(remove[:1])
            newTransction=self.pendingTransaction.pop()
            sletedTransaction.append(newTransction)
            block = Block(self.index, date.today(), sletedTransaction, self.getLatestBlock().hash)
            result=block.mineBlock(self.difficulty)
            
            


        print('block successfully added')
        self.chain.append(block)
        self.createTransaction(Transaction(None, miningRewardAddress, self.miningReward))

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]

            # recalculates the hash and matches it with already calculated hash
            # checks if the data is been tempered with
            if currentBlock.hash != currentBlock.calculateHash():
                return False
            # checks the links of the entire chain and matches the previous hash of current block with the hash of
            # the previous block
            if currentBlock.previousHash != previousBlock.hash:
                return False

        return True

    def createTransaction(self, transaction):
        self.pendingTransaction.append(transaction)

    def getBalanceOfAddress(self, address):
        balance = 0
        for block in self.chain:
            if len(block.transaction) == 0:
                continue
            for trans in block.transaction:
                if trans.fromAddress == address:
                    balance -= trans.amount
                if trans.toAddress == address:
                    balance += trans.amount
        return balance


myBitcoin = Blockchain()
myBitcoin.createTransaction(Transaction('imran', 'jawad', 200))
myBitcoin.createTransaction(Transaction('imran', 'jawad', 400))
print('start mining')
myBitcoin.minePendingTransaction('bitminor')
print('balance of bitminor is ')
print(myBitcoin.getBalanceOfAddress('bitminor'))
