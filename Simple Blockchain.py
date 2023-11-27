import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

def calculate_hash(index, previous_hash, timestamp, data, nonce):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data) + str(nonce)
    return hashlib.sha256(value.encode()).hexdigest()

def create_genesis_block():
    # Create the first block (genesis block) manually
    return Block(0, "0", time.time(), "Genesis Block", calculate_hash(0, "0", time.time(), "Genesis Block", 0), 0)

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    nonce = 0
    hash = calculate_hash(index, previous_block.hash, timestamp, data, nonce)
    
    # Proof-of-work (mining)
    while not hash.startswith('0000'):
        nonce += 1
        hash = calculate_hash(index, previous_block.hash, timestamp, data, nonce)
    
    return Block(index, previous_block.hash, timestamp, data, hash, nonce)

def is_valid_block(new_block, previous_block):
    # Check if the index is incremented properly
    if previous_block.index + 1 != new_block.index:
        return False
    
    # Check if the previous hash matches
    if previous_block.hash != new_block.previous_hash:
        return False
    
    # Check if the hash of the block is valid
    if new_block.hash != calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data, new_block.nonce):
        return False
    
    # Check if the proof-of-work (hash starting with '0000') is valid
    if not new_block.hash.startswith('0000'):
        return False
    
    return True

# Testing the blockchain
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Add blocks to the blockchain
blocks_to_add = 10
for i in range(1, blocks_to_add + 1):
    new_block_data = f"Block #{i} Data"
    new_block = create_new_block(previous_block, new_block_data)
    
    if is_valid_block(new_block, previous_block):
        blockchain.append(new_block)
        previous_block = new_block
        print(f"Block #{i} added to the blockchain.")
        print(f"Hash: {new_block.hash}\n")
    else:
        print(f"Block #{i} rejected by the blockchain.\n")

# Print the entire blockchain
print("Blockchain:")
for block in blockchain:
    print(f"Index: {block.index}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Hash: {block.hash}")
    print(f"Nonce: {block.nonce}")
    print("\n" + "-" * 20 + "\n")
    
