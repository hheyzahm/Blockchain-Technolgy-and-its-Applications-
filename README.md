# Blockchain-Technolgy-and-its-Applications



Consider the blockchain MemPool Implementation using Python. Implement the blockchain code with following requirements: 
Add Transaction fees as data member in transaction class and every miner can get maximum two transactions from mempool into block at mining time. The selection of transactions based on greedy basis (means get two that have maximum fee). 
- A miner can get 20 coins plus transactions fee as reward.
- Set difficulty level to three
- After executing all nonce values i.e. 0 to 4 billion and in case no Golden Nonce found then miner will swap one lowest fee transaction from block to next highest fee transaction available in mempool.
