import os

def get_hash_by_index(index):
	filename = None
	# 找到该目录下第一个包含该名字的文件
	for file in os.listdir('blocks'):
		if str(index) in file:
			filename = str(file)
			break
	# 然后通过文件名找其下的行
	target = []
	with open(filename) as f_obj:
		lines = f_obj.readlines()
		for line in lines:
			if 'hash' in line:
				target.append(line)
	key_value_pair = target[-1].split('=')
	print(key_value_pair[-1].strip())
	return key_value_pair[-1]

#os.mkdir('blocks')
get_hash_by_index(15)