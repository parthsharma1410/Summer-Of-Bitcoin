#  In my code solution I am first of all sorting all transactions based on fee, and further arranging them based on highest fee to lowest 
#  Then by iterating through the sorted transaction data, the code checks if the transaction has a parent or not.
#  Transactions with no parents can be straightaway added to our resultant block.
#  If a transaction has parents, the code will fetch the parent of the particular transaction and 
#  further find if the parent transaction has a parent.
#  Finally it appends them to the block followed by the child transaction.

class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        # TODO: add code to parse weight and parents fields
        self.weight = int(weight)
        self.parents = parents.split(';')
                        
# Saving list of transactions from mempool.csv
def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('mempool.csv') as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])

# Sorting the transactions on the basis of fee
# Partitioning the array
def partition(array, index1, index2):
    i = (index1-1)         
    pivot = array[index2].fee     
    for j in range(index1, index2):
        if array[j].fee <= pivot:
            i = i+1
            array[i], array[j] = array[j], array[i]
    array[i+1], array[index2] = array[index2], array[i+1]
    return (i+1)

# Using quick sort for sorting
def quickSort(array, index1, index2):
    if len(array) == 1:
        return array
    # Recursion
    if index1 < index2:
        partitioned = partition(array, index1, index2)
        quickSort(array, index1, partitioned-1)
        quickSort(array, partitioned+1, index2)

# Recieving all transaction IDs and their Fees as a dictionary
def dictionaryOfTx_idAndFee(pool):
    dict1 = {}
    for transaction in pool:
        dict1[transaction.txid] = transaction.fee
    return dict1

# Recieving all transaction IDs and their weights as a dictionary
def dictionaryOfTx_idAndWeight(pool):
    b = {}
    for transaction in pool:
        b[transaction.txid] = transaction.weight
    return b

# Deleting all null values
def delNull(block):
    updated=[]
    for txid in block:
        if txid is not None: updated.append(txid)
    return updated

# Get all the transactions with one or more parents
def getEveryChildTransaction(transactions):
    childArray=[]
    for transaction in transactions:
        if len(transaction.parents[0])>0 : childArray.append(transaction.txid)
    return childArray

# Appending all parents and grandparents of a child transaction using recursion 
def addAllParentTransactions(transaction, children, block):
    for parent in transaction.parents:
        if parent not in block:
            if parent in children:
                block.append(addAllParentTransactions(searchForParentsOfParents(parent, transactions), children, block))
            else:
                return parent

# Searching for the parent of a parent
def searchForParentsOfParents(parent, pool):
    for transaction in pool:
        if transaction.txid == parent:
            return transaction
        
# Adding the top transactions and checking if the weight does not exceed 4000000 - provided in the problem statement
def validateEntries(block):
    res = []
    dict2 = dictionaryOfTx_idAndWeight(transactions)
    total_weight = 0
    block = delNull(block)
    i=0
    while i < len(block) and total_weight < 4000000:
        res.append(block[i])
        total_weight = total_weight + dict2[block[i]]
        i = i + 1
    return res

# Writing tx_id content to block.txt
def appendResultToBlock(block):
    with open('block.txt', 'w') as file:
        for txid in block:
            file.write('%s\n' % txid)
            
if __name__ == "__main__":
    
    transactions = parse_mempool_csv()
    
    # Using quicksort to arrange transactions based on fee
    quickSort(transactions, 0, len(transactions)-1)

    # Getting all transactions with atleast one parent
    child_transactions = getEveryChildTransaction(transactions)
    
    block=[]
    
    # Appending transactions to block in order of highest fees
    transactions.reverse()
    for transaction in transactions:
        if not transaction.txid in child_transactions:
            block.append(transaction.txid)
        else:
            addAllParentTransactions(transaction, child_transactions, block)
            block.append(transaction.txid)

    # Adding the top transactions and checking if the weight does not exceed 4000000
    result = validateEntries(delNull(block))
    
    # writing the result to the file block.txt
    appendResultToBlock(result)