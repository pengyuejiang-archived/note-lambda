# 参考资料：https://www.cnblogs.com/fangbei/p/build-blockchain.html
# 学术资料：https://blog.csdn.net/bmwgaara/article/details/79059007
import hashlib as hl
import datetime as dt
import os
import json

# 全局变量：
index = 0

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

	# 区块链的
	block_info = {}

# 以上是通用的Blcok结构，但是创世区块是需要特殊定义的：
def create_genesis_block():
	os.mkdir('blocks/')
	return Block(index, dt.datetime.now(), 'Genesis Block', '0')


# 用于通过上一个区块创建下一个区块：
def next_block(last_block):
	index = last_block.index + 1
	timestamp = dt.datetime.now()
	data = 'Block #' + str(index)
	prev_hash = last_block.hash
	return Block(index, timestamp, data, prev_hash)

# 广播区块编号和散列值，多半调试用
def broadcast():
	print('\nBlock #{} has been added to the blockchain!'.format(index))
	print('Hash: {}'.format(get_hash_by_index(index)))

# 重要函数，用于保存区块到本地
def save_block(block_to_add):
	block = block_to_add
	block.block_info = {
		'index': str(block.index),
		'timestamp': str(block.timestamp),
		'data': str(block.data),
		'prev_hash': str(block.prev_hash),
		'hash': str(block.hash)
	}
	filename = 'blocks/Block#{}.json'.format(block.index)
	with open(filename, 'w') as f_obj:
		json.dump(block.block_info, f_obj)

# 服务函数
# 通过索引找到区块的所有信息
def get_block_info_by_index(index):
	filename = None
	# 找到该目录下第一个包含该名字的文件
	for file in os.listdir('blocks/'):
		if str(index) in file:
			filename = str(file)
			break
	with open('blocks/' + filename) as f_obj:
		return f_obj.read().rstrip()

# 上面那个不太好用了，这个是为命令行界面独家定制的：
def generate_new_block():
	global index # 参考资料：https://blog.csdn.net/u011304970/article/details/72820836
	prev_hash = get_hash_by_index(index)
	index += 1
	new_timestamp = dt.datetime.now()
	data = 'Block #' + str(index)
	return Block(index, new_timestamp, data, prev_hash)

# 利用json可以快速且准确地找到我们需要的信息
def get_hash_by_index(index):
	filename = None
	# 找到该目录下第一个包含该名字的文件
	# os.listdir的用法参考自官方文档
	for file in os.listdir('blocks/'):
		if str(index) in file:
			filename = str(file)
			break
	with open('blocks/' + filename) as f_obj:
		block = json.load(f_obj)
	return block['hash']

# 主函数，下面其实还可以分
if __name__ == '__main__':

	# 一、读取Core.json文件（初始化操作）
	corefile = 'Core.json'
	# 如果存在那是最好
	try:
		with open(corefile) as f_obj:
			index = json.load(f_obj)
	# 如果不存在则创建Core.json文件并载入初始值
	# 然后初始化创世区块
	except FileNotFoundError:
		with open(corefile, 'w') as f_obj:
			f_obj.write('0')
			# 创世区块的建立过程
			genesis_block = create_genesis_block()
			print('\nThe genesis block was created!')
			save_block(genesis_block)
			print('Hash: {}'.format(genesis_block.hash))

	# 二、进入交互式界面
	while True:
		print('\n==========Menu==========')
		print('Now there are', index + 1, 'blocks locally.')
		print('1. View block information')
		print('2. Generate new block')
		print('3. Purge the blockchain')
		service = input('Please select your service ["q" to exit]: ')
		if service == 'q':
			break
		try:
			service = int(service)
		except ValueError:
			print('\nOops! That does not seem like an option.')
		else:
			if service == 1:
				try:
					review_index = int(input('\nPlease type in the index' +
							' of the block you want to review: '))
				except ValueError:
					print('Oops! That does not seem like an option.')
				else:
					# 判断机制：
					if review_index > index:
						print('\nOops! The number is too large!')
						continue

					print('\n' + get_block_info_by_index(review_index))
			elif service == 2:
				# print('\nGenerating new block...')
				save_block(generate_new_block())
				broadcast()
				filename = 'Core.json'
				with open(filename, 'w') as f_obj:
					f_obj.write(str(index))
			elif service == 3:
				# 防误删机制
				confirmation = input('Are you really sure about this [y/n]? ')
				if confirmation != 'y':
					continue
				# print('\nPurging blockchain...')
				for i in range(index + 1):
					os.remove('blocks/Block#' + str(i) + '.json')
				# 下面的代码是不在循环里头的：
				# os库的具体使用指南请参见官方文档
				os.rmdir('blocks/')
				os.remove('Core.json')
				index = 0
				# 如果都删光了是要重启的
				break
			else:
				print('\nError.')
