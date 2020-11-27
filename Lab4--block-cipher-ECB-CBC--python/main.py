import numpy as np
from PIL import Image
import random


def getSmallestDivisorOfArrayDimensions(arr):
		smallest_divisors = []
		width = len(arr[0])
		DivisorRange = range(2, width + 1)
		list_width = [i for i in DivisorRange if width % i == 0]
		if len(list_width)>1:
			smallest_divisors.append(list_width[1])
		else:
			smallest_divisors.append(list_width[0])
		height = len(arr)
		DivisorRange = range(2, height + 1)
		list_height = [i for i in DivisorRange if height % i == 0]
		if len(list_width)>1:
			smallest_divisors.append(list_height[1])
		else:
			smallest_divisors.append(list_height[0])
		return smallest_divisors


def turnArrayIntoBWArray(arr):
		arr_bw = []
		for x in arr:
				temp = []
				for y in x:
						if np.all(np.array([y, [255, 255, 255]])):	# white
								temp.append([1])
						else:	# black
								temp.append([0])
				arr_bw.append(temp)
		return arr_bw


def turnBWArrayIntoArray(arr_bw):
		arr = []
		for x in arr_bw:
				temp = []
				for y in x:
						if np.all(np.array([y, [1]])):	# white
								temp.append([255, 255, 255])
						else:	# black
								temp.append([0, 0, 0])
				arr.append(temp)
		return arr


def turnBWArrayIntoBlockArray(arr, block_width, block_height, arr_bw):
		block_array = []

		for _ in range(len(arr) // block_height):
				block_array.append([])

		for i, _ in enumerate(block_array):
				for _ in range(len(arr[0]) // block_width):
						block_array[i].append([])

		counter_of_block_lines = 0
		counter_of_pixel_blocks = 0

		for x, line in enumerate(arr_bw):
				if x % block_height == 0 and x > 0:
						counter_of_block_lines += 1
				counter_of_pixel_blocks = 0
				for y, pixel in enumerate(line):
						if y % block_width == 0 and y > 0:
								counter_of_pixel_blocks += 1
						block_array[counter_of_block_lines][counter_of_pixel_blocks].append(
								pixel)
		return block_array


def turnBlockArrayIntoBWArray(block_array, block_width, block_height, arr_bw):
		counter_of_block_lines = 0
		counter_of_pixel_blocks = 0
		for x, line in enumerate(arr_bw):
				if x % block_height == 0 and x > 0:
						counter_of_block_lines += 1
				counter_of_pixel_blocks = 0
				for y, pixel in enumerate(line):
						if y % block_width == 0 and y > 0:
								counter_of_pixel_blocks += 1
						arr_bw[x][y] = block_array[counter_of_block_lines][
								counter_of_pixel_blocks].pop(0)
		return arr_bw


def transformBlockArrayECB(key, block_array, block_width, block_height):
		key_pos = 0
		for x, line in enumerate(block_array):
				for y, block in enumerate(line):
						for i, element in enumerate(block):
								block_array[x][y][i] = [block[i][0] ^ key[key_pos % 32][0]]
								key_pos += 1
		return block_array


def transformBlockArrayCBC(key, block_array, block_width, block_height):
		key_pos = 0
		prev_block = []
		for x in range(block_height * block_width):
				prev_block.append([random.randint(0, 1)])
		for x, line in enumerate(block_array):
				for y, block in enumerate(line):
						temp = []
						for k in range(len(block)):
								temp.append([prev_block[k][0] ^ block[k][0]])
						block_array[x][y] = temp
						for i, element in enumerate(block):
								block_array[x][y][i] = [
										block_array[x][y][i][0] ^ key[key_pos % 32][0]]
								key_pos += 1
						prev_block = block_array[x][y]
		return block_array

def encrypt(key,type):
		###ECB
		photo = Image.open("plain.bmp")
		arr = np.asarray(photo)
		block_width, block_height = getSmallestDivisorOfArrayDimensions(arr)
		arr_bw = turnArrayIntoBWArray(arr)
		block_array = turnBWArrayIntoBlockArray(arr, block_width, block_height,
																						arr_bw)
		if type == "ECB":
			block_array = transformBlockArrayECB(key, block_array, block_width,
																						 block_height)
		else:
			block_array = transformBlockArrayCBC(key, block_array, block_width,
																						 block_height)
		arr_bw = turnBlockArrayIntoBWArray(block_array, block_width,
																					 block_height, arr_bw)
		arr = turnBWArrayIntoArray(arr_bw)
		return np.array(arr)

#generowanie klucza o dlugosci 32 
key = []
for x in range(32):
		key.append([random.randint(0, 1)])

im = Image.fromarray((encrypt(key,"CBC")).astype(np.uint8))
im.save("cbc_crypto.bmp")
im2 = Image.fromarray((encrypt(key,"ECB")).astype(np.uint8))
im2.save("ecb_crypto.bmp")
