
import datetime as date
from snake_coin import *


def create_genesis_block():
    return Block(0, date.datetime.now(), 'GenesisBlock', '0')


def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = 'Block' + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)


block_chain = [create_genesis_block()]
previous_block = block_chain[0]
print('Genesis Block added!')
print('Hash: {}'.format(block_chain[0].hash))

num_blocks = 20
for i in range(num_blocks):
    block_to_add = next_block(previous_block)
    block_chain.append(block_to_add)
    previous_block = block_to_add
    print('Block #{} has been added to the block chain!'.format(block_to_add.index))
    print('Hash: {}'.format(block_to_add.hash))





































