# -*- coding: utf-8 -*-

# 1,	0
# u'■', u'□'

import msvcrt
import time
import os
import random
import sys

# 俄罗斯方块图像，存其在9宫格中的站位，0~8从上到下，从左到右
image = [
	[1, 4, 7], [3, 4, 5],										# I
	[1, 3, 4, 6], [0, 1, 4, 5],									# Z
	[1, 4, 5, 8], [1, 2, 3, 4],									# Z
	[1, 3, 4, 5], [1, 4, 5, 7], [3, 4 ,5 ,7], [1, 3, 4, 7],		# T
	[1, 4, 7, 8], [3, 4, 5, 6], [0, 1, 4, 7], [2, 3, 4, 5],		# L
	[4, 5, 7, 8],
	[]
]

# 俄罗斯方块转化
dirs = {
	0: 1, 1: 0,
	2: 3, 3: 2,
	4: 5, 5: 4,
	6: 7, 7: 8, 8: 9, 9: 6,
	10: 11, 11: 12, 12: 13, 13: 10,
	14: 14
}


# 图像为一个九宫格，cell表示各个格子的站位，连接起来可表示一个图形，x,y分别为九宫格中心的坐标
class Image(object):
	def __init__(self, _type, tetris):
		self.__type = _type						# 图像类型
		self.__cells = image[_type]				# 具体图像在9宫格中的站位
		self.__tetris = tetris 				# 图形所绑定的tetris面板类
		self.__x = 0							# 图形起始x坐标， 注意x为纵轴
		self.__y = 5
		self.adjust()

	@property
	def x(self):
		return self.__x

	@property
	def y(self):
		return self.__y

	@property
	def tetris(self):
		return self.__tetris

	@property
	def type(self):
		return self.__type

	@type.setter
	def type(self, value):
		self.__type = value

	@property
	def cells(self):
		return self.__cells

	@cells.setter
	def cells(self, value):
		self.__cells = value

	# 方块所占格子
	@property
	def placeList(self):
		return self.__placeList

	# 存方块所占格子
	def adjust(self):
		self.__placeList = []
		for cell in self.__cells:
			r = cell / 3
			c = cell % 3
			if self.__x + r - 1 < 0:
				continue
			self.__placeList.append((self.__x + r - 1, self.__y + c - 1))

	# 一格一格往下落
	def slowDown(self):
		if self.checkDown():
			self.__x += 1
			self.adjust();
		else:
			for item in self.__placeList:
				self.__tetris.data[item[0]][item[1]] = 1

	# 快速下落 对应空格键
	def fastDown(self):
		while self.checkDown():
			self.slowDown()

	# 方块左移，调整坐标后，调整方块所占格子
	def turnLeft(self):
		if self.checkLeft():
			self.__y -= 1
			self.adjust();

	# 方块右移
	def turnRight(self):
		if self.checkRight():
			self.__y += 1
			self.adjust();

	# 判断方块是否超过面板底线
	def checkCells(self, cells, __x, __y):
		for cell in cells:
			r, c = cell / 3, cell % 3
			x = __x + r - 1
			y = __y + c - 1
			if x >= self.__tetris.x:
				return False
		return True

	# 判断格子是否以及被占用以及是否超过左右边界
	def checkCellsVis(self, cells, __x, __y):
		for cell in cells:
			r, c = cell / 3, cell % 3
			x = __x + r - 1
			y = __y + c - 1
			if y >= self.tetris.y or y < 0:
				return False
			if self.tetris.data[x][y] == 1:
				return False
		return True

	# 改变形态，对应上键，先用临时变量存变形后的状态 
	def change(self):
		newType = dirs[self.__type]
		newCells = image[newType]

		# 先判断变形后会不会超过面板底线，会的话直接return，不变形
		if not self.checkCells(newCells, self.x, self.y):
			return

		# 然后判断变形后是否超出左右边界以及是否会占到以及被占用的格子，如果不会，就直接变形，会就再进行后续判断
		if self.checkCellsVis(newCells, self.x, self.y):
			self.__type = newType
			self.__cells = newCells
			self.adjust()
			return

		# 判断变形后是否超出左右边界的情况，如果碰到了能不能调整？
		flag = 0
		for cell in newCells:
			r, c = cell / 3, cell % 3
			x = self.__x + r - 1
			y = self.__y + c - 1
			if y < 0:
				# self.__y += 1
				if self.checkRight():
					flag = 1
					break
				else:
					return
				
			if y >= self.__tetris.y:
				if self.checkLeft():
					flag = -1
					break
				else:
					return

		# 碰到右边界还能调整的情况
		if flag == -1:
			if self.checkCellsVis(newCells, self.x, self.y - 1):
				self.turnLeft()
			else:
				return

		# 碰到左边界还能调整的情况
		if flag == 1:
			if self.checkCellsVis(newCells, self.x, self.y + 1):
				self.turnRight()
			else:
				return

		self.__type = newType
		self.__cells = newCells
		self.adjust()

	# 判断是否会超出左边界
	def checkLeft(self):
		for cell in self.__cells:
			r = cell / 3
			c = cell % 3
			if self.__y + c - 1 - 1 < 0:
				return False
			if self.__tetris.data[self.__x + r - 1][self.__y + c - 1 - 1] == 1:
				return False
		return True

	# 判断是否会超出右边界
	def checkRight(self):
		for cell in self.__cells:
			r = cell / 3
			c = cell % 3
			if self.__y + c - 1 + 1 >= self.__tetris.y:
				return False
			if self.__tetris.data[self.__x + r - 1][self.__y + c - 1 + 1] == 1:
				return False
		return True

	# 判断是否还能下落
	def checkDown(self):
		flag = True
		for cell in self.__cells:
			r = cell / 3
			c = cell % 3
			if self.x + r - 1 + 1 >= self.tetris.x:
				flag = False
				break
			if self.tetris.data[self.x + r - 1 + 1][self.y + c - 1] == 1:
				flag = False
				break

		if flag == False:
			for item in self.__placeList:
				self.tetris.data[item[0]][item[1]] = 1
			for cell in self.__cells:
				r = cell / 3
				if self.x + r - 1 < 0:
					self.tetris.lose = True
					return flag
			self.tetris.checkBoard()

		return flag


# 面板类，image为当前正在下落的图形，x,y分别为横纵坐标，data数组表示为该格是否被占有
class Tetris(object):

	def __init__(self):
		self.__data = [[0 for col in range(11)] for row in range(20)]
		self.__score = 0
		self.__image = Image(15, self)
		self.__x = 20
		self.__y = 11
		self.__lose = False

	@property
	def lose(self):
		return self.__lose

	@lose.setter
	def lose(self, value):
		self.__lose = value

	@property
	def x(self):
		return self.__x

	@property
	def y(self):
		return self.__y

	@property
	def data(self):
		return self.__data

	@property
	def image(self):
		return self.__image

	@data.setter
	def data(self, value):
		self.__data = value

	@image.setter
	def image(self, value):
		self.__image = value

	# 显示格子，data[i][j]为1的话表示已经被占用
	def show(self):
		# print self.image.placeList, self.image.type
		# for i in range(5):
		# 	for j in range(self.__y):
		# 		print self.__data[i][j],
		# 	print ""
		os.system('cls')
		# print self.image.x, self.image.y
		for i in range(self.__x):
			for j in range(self.__y):
				if self.__data[i][j] == 1 or (i, j) in self.image.placeList:
					print u'■',
				else:
					print u'□',
			print ""
		print 'score: ' + str(self.__score)
		if self.lose:
			print 'you lose'
			sys.exit()

	def keyPressed(self):
		#功能键由两个char组成
		key1 = ord(msvcrt.getch())

		if key1 == 32:						#空格
			self.image.fastDown()
		elif key1 == 81 or key1 == 113:
			sys.exit()
		elif key1 == 224:
			key2 = ord(msvcrt.getch())
			if key2 == 72:						#上箭头
				self.image.change()
			elif key2 == 75:					#左箭头
				self.image.turnLeft()
			elif key2 == 77:					#右箭头
				self.image.turnRight()

	# 消除行
	def checkBoard(self):
		delList = []
		for i in range(self.x):
			flag = True
			for j in range(self.y):
				if self.data[i][j] == 0:
					flag = False
					break
			if flag:
				delList.append(i) 
				self.__score += 1

		for i in delList:
			self.delRow(i)

	# 删除行，从上往下删除
	def delRow(self, row):
		for i in range(row, 0, -1):
			for j in range(self.y):
				self.data[i][j] = self.data[i - 1][j]



if __name__ == '__main__':
	# 创建面板类并绑定图像类
	tetris = Tetris()
	tetris.image = Image(random.randint(0, 14), tetris)
	pre = time.time()
	# msvcrt.kbhit()监听输入
	while not msvcrt.kbhit() or not tetris.keyPressed():
		# 大于1s就重绘
		if time.time() - pre >= 1:
			# 图形能下落就自动下落，否则重新绑定一个新的图形
			if tetris.image.checkDown():
				tetris.image.slowDown()
			else:
				tetris.image = Image(random.randint(0, 14), tetris)
			tetris.show()
			pre = time.time()
			

		# if msvcrt.kbhit():
		# 	t.show()

		# # msvcrt.kbhit()监听输入
		# if t.image.checkDown():
		# 	i.slowDown()	
		# else:
		# 	i = Image(random.randint(0, 14), t)
		# 	t.image = i
		# t.show()

		# os.system('cls')