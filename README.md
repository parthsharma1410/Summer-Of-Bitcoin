In my code solution I am first of all sorting all transactions based on fee, and further arranging them based on highest fee to lowest
Then by iterating through the sorted transaction data, the code checks if the transaction has a parent or not.
Transactions with no parents can be straightaway added to our resultant block.
If a transaction has parents, the code will fetch the parent of the particular transaction and
further find if the parent transaction has a parent.
Finally it appends them to the block followed by the child transaction.
