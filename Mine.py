# -*- coding: utf-8 -*-

# chr(17)

import random
import os
import sys

class Mine(object):
	"""docstring for Mine"""
	def __init__(self):
		super(Mine, self).__init__()
		# print 'init'
		self.x, self.y, self.mineNum = 9, 9, 9
		self.map = [['?' for col in xrange(self.y)] for row in xrange(self.x)]		# 玩家眼中的棋盘
		# print 'self'
		self.data = [[0 for col in xrange(self.y)] for row in xrange(self.x)]		# 真实棋盘
		self.lose = False
		self.openNum = 0
		count = 0
		# 造棋盘，9为雷
		while count < self.mineNum:
			x = random.randint(0, 8)
			y = random.randint(0, 8)
			if self.data[x][y] == 9:
				continue
			self.data[x][y] = 9
			count += 1
		for i in xrange(self.x):
			for j in xrange(self.y):
				if self.data[i][j] == 9:
					continue
				else:
					self.countMine(i, j)

	@property
	def openNum(self):
		return self.__openNum

	@openNum.setter
	def openNum(self, value):
		self.__openNum = value

	@property
	def lose(self):
		return self.__lose

	@lose.setter
	def lose(self, value):
		self.__lose = value
		
	@property
	def x(self):
		return self.__x

	@x.setter
	def x(self, value):
		self.__x = value

	@property
	def y(self):
		return self.__y

	@y.setter
	def y(self, value):
		self.__y = value

	@property
	def mineNum(self):
		return self.__mineNum

	@mineNum.setter
	def mineNum(self, value):
		self.__mineNum = value

	# 造棋盘，给每个风格赋值为周围的雷数
	def countMine(self, x, y):
		count = 0
		if x > 0:
			count += (1 if self.data[x - 1][y] == 9 else 0)
			if y > 0:
				count += (1 if self.data[x - 1][y - 1] == 9 else 0)
			if y + 1 < self.y:
				count += (1 if self.data[x - 1][y + 1] == 9 else 0)
		if x + 1 < self.x:
			count += (1 if self.data[x + 1][y] == 9 else 0)
			if y > 0:
				count += (1 if self.data[x + 1][y - 1] == 9 else 0)
			if y + 1 < self.y:
				count += (1 if self.data[x + 1][y + 1] == 9 else 0)
		if y > 0:
			count += (1 if self.data[x][y - 1] == 9 else 0)
		if y + 1 < self.y:
			count += (1 if self.data[x][y + 1] == 9 else 0)
		self.data[x][y] = count

	@property
	def data(self):
		return self.__data

	@data.setter
	def data(self, value):
		# print 'setter'
		self.__data = value

	@property
	def map(self):
		return self.__map

	@map.setter
	def map(self, value):
		# print 'setter'
		self.__map = value

	@property
	def error(self):
		return self.__error

	@error.setter
	def error(self, value):
		self.__error = value

	# 输出棋盘、操作、游戏胜负在控制台
	def show(self):
		print ' ',
		for i in xrange(self.x):
			print ' ' + str(i),
		print ''
		print ' ',
		for i in xrange(self.x):
			print '--',
		print ''
		for i in xrange(self.x):
			print str(i) + '|',
			for j in xrange(self.y):
				print self.map[i][j] + ' ',
			print ''
		print '1. Input a position like 0,0,s to insure the land is safety' 
		print '2. Input a position like 0,0,c to insure the land is mine -> ' + chr(17) 
		print '3. Input a position like 0,0,d to distinct the near land -> ?'
		print '-->', 
		if self.lose:
			print 'boom'
			sys.exit()
		# 如果打开数 + 雷数 == 总数，说明不是雷的都打开了，判定为success
		if self.openNum + self.mineNum == self.x * self.y:
			print 'success'
			sys.exit()

	# 判断是否出界
	def check(self, x, y):
		if x < 0 or x >= self.x or y < 0 or y >= self.y:
			return False
		return True

	# 打开空格周围所有的空格
	def dfs(self, x, y):
		mp = self.map[x][y]
		num = self.data[x][y]
		if mp.isdigit() or mp == chr(17):
			return
		if num == 9:
			return
		if num > 0:
			self.map[x][y] = str(num)
			self.openNum += 1
			return
		self.map[x][y] = str(num)
		self.openNum += 1
		for i in xrange(-1, 2, 1):
			for j in xrange(-1, 2, 1):
				nx, ny = x + i, y + j
				if self.check(nx, ny):
					self.dfs(nx, ny)


	# 开格子
	def insureSafety(self, x, y):
		# 如果被开过或者被插过红旗，就不能打开
		if self.map[x][y] == chr(17) or self.map[x][y].isdigit():
			return
		# 雷，判定为lose
		elif self.data[x][y] == 9:
			self.map[x][y] = '*'
			self.lose = True
			return
		# 打开非0数字格
		elif self.data[x][y] > 0:
			self.map[x][y] = str(self.data[x][y])
			self.openNum += 1
		else:
			self.dfs(x, y)

	# 插红旗
	def insureMine(self, x, y):
		# 已打开过，不能插红旗
		if not self.map[x][y].isdigit():
			self.map[x][y] = chr(17)

	# 移除红旗
	def unsureMine(self, x, y):
		# 已打开过，没有红旗可移除
		if not self.map[x][y].isdigit():
			self.map[x][y] = '?'

	# 操作
	def play(self, operation):
		params = operation.split(',')
		# 输入不合法
		if len(params) != 3:
			self.show()
			print operation + ' illeagel input'
			print '-->',
			return
		if (params[0].isdigit() == False) or (params[1].isdigit() == False) or (params[2] != 's' and params[2] != 'c' and params[2] != 'd'): 
			self.show()
			print operation + ' illeagel input'
			print '-->',
			return

		# 具体操作
		x, y, op = int(params[0]), int(params[1]), params[2]
		out = 'null'
		if op == 's':
			self.insureSafety(x, y)
			out = 'insure safe'
		elif op == 'c':
			self.insureMine(x, y)
			out = 'insure mine'
		elif op == 'd':
			self.unsureMine(x, y)
			out = 'unsure mine'
		self.show()
		print 'last operation: ' + out + ' at (' + params[0] + ', ' + params[1] + ')'
		print '-->',



if __name__ == '__main__':
	mine = Mine()
	os.system('cls')
	mine.show()
	while True:
		s = raw_input()
		os.system('cls')
		mine.play(s)
