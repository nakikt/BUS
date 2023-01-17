from .blockchain import Blockchain

def mine_block(blockchain,  id, address,  name_surname, condition):
    blockchain.add_property(
        id =  id,
        address =  address,
        name_surname = name_surname,
        condition =  condition
    )
# obtain the hash of last block in the blockchain
    last_block_hash = blockchain.hash_block(blockchain.last_block)
# using PoW, get the nonce for the new block to be added to the blockchain
    index = len(blockchain.chain)
    nonce = blockchain.proof_of_work(index, last_block_hash, blockchain.current_property)
# add the new block to the blockchain using the last block hash and the current nonce
    blockchain.append_block(nonce, last_block_hash)





