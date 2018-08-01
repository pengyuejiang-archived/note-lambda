# 参考资料：https://www.cnblogs.com/fangbei/p/build-blockchain.html
# 学术资料：https://blog.csdn.net/bmwgaara/article/details/79059007
import hashlib as hl
import datetime as dt

# 定义Block数据类型：
class Block():

	def __init__(self, index, timestamp, data, prev_hash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.prev_hash = prev_hash
		self.hash = self.hash_block()

	def hash_block(self):
		sha = hl.sha256()
		sha.update((str(self.index) +
				str(self.timestamp) +
				str(self.data) +
				str(self.prev_hash)).encode('utf-8'))
		return sha.hexdigest()

# 以上是通用的Blcok结构，但是创世区块是需要特殊定义的：
def create_genesis_block():
	return Block(0, dt.datetime.now(), 'Genesis Block', '0')

# 用于创建下一个区块：
def next_block(last_block):
	index = last_block.index + 1
	timestamp = dt.datetime.now()
	data = 'Block #' + str(index)
	# Java是可以自动转换成String的
	prev_hash = last_block.hash
	return Block(index, timestamp, data, prev_hash)

def broadcast():
	print('Block #{} has been added to the blockchain!'.format(block_to_add.index))
	print('Hash: {}\n'.format(block_to_add.hash))

def write_to_file(block_to_add):
	block = block_to_add
	filename = 'Block#{}.txt'.format(block.index)
	with open(filename, 'w') as file:
		file.write('Block {\n')
		file.write('\tindex=' + str(block.index) + '\n')
		file.write('\ttimestamp=' + str(block.timestamp) + '\n')
		file.write('\tdata=' + str(block.data) + '\n')
		file.write('\tprev_hash=' + str(block.prev_hash) + '\n')
		file.write('\thash=' + str(block.hash) + '\n')
		file.write('}\n')

if __name__ == '__main__':

	# Create the blockchain & add the genesis block
	blockchain = [create_genesis_block()]
	prev_block = blockchain[0] # 这个有点像指针
	print('The genesis block was created!')
	print('Hash: {}\n'.format(str(prev_block.hash))) # 这个有些不太合理，但是凑合
	write_to_file(prev_block)
	
	# Number of blocks should add to the chain
	# after the genesis block
	blocks_to_add = 64

	# Add blocks to the chain
	for i in range(blocks_to_add):
		block_to_add = next_block(prev_block)
		blockchain.append(block_to_add)
		prev_block = block_to_add
		broadcast()
		write_to_file(block_to_add)

# 2.0新增内容：写入本地
