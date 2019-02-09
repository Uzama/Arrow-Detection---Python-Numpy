from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
import cv2

WORKING_DIR = os.getcwd()
IMAGES_DIR  = os.path.join(WORKING_DIR, 'images')
MODEL_DIR	= os.path.join(WORKING_DIR, 'model.txt')
MODEL_ARRAY = ['R', 'L', 'S']
MODEL_COUNT = 10

def threshold(imageArray):
	balance_array = []
	new_array = imageArray
	for each_row in imageArray:
		for each_pixel in each_row:
			average_num = sum(each_pixel)/3
			balance_array.append(average_num)
	balance = reduce((lambda x, y: x+y), balance_array)/len(balance_array)
	for each_r in new_array:
		for each_p in each_r:
			if sum(each_p)/3 > balance:
				each_p[0] = 0
				each_p[1] = 0
				each_p[2] = 0
			else:
				each_p[0] = 255
				each_p[1] = 255
				each_p[2] = 255

def create_model():
	model_file = open('model.txt', 'a')
	for model in MODEL_ARRAY:
		for model_count in range(1, MODEL_COUNT+1):
			label 					= model.lower() + str(model_count)
			image_path 				= os.path.join(IMAGES_DIR, label + '.jpg')
			model_image 			= Image.open(image_path)
			model_image_10_x_10 	= model_image.resize((25,25), Image.LANCZOS)
			model_image_array 		= np.array(model_image_10_x_10)
			model_image_array.setflags(write=1)
			threshold(model_image_array)
			model_image_array_list 	= str(model_image_array.tolist())
			line_to_write 			= str(model) + '::'+ model_image_array_list + '\n'
			model_file.write(line_to_write)
	model_file.close()

def resize_and_threshold_image(image):
	image_10_x_10 	= image.resize((25,25), Image.LANCZOS)
	image_array 	= np.array(image_10_x_10)
	image_array.setflags(write=1)
	threshold(image_array)
	return image_array

def find_which_direction(image_path):
	match_array = []
	models = open(MODEL_DIR, 'r').read()
	models = models.split('\n')
	arrow_image = Image.open(image_path)
	arrow_image = resize_and_threshold_image(arrow_image)
	arrow_image_array = np.array(arrow_image)
	arrow_image_array_list = arrow_image_array.tolist()
	check_string = str(arrow_image_array_list)
	for model in models:
		 if len(model) > 3: #neglating '\n'
		 	split_model = model.split('::')
		 	current_model = split_model[0]
		 	current_image_array = split_model[1]
		 	current_image_pixels = current_image_array.split('],')
		 	check_image_pixels = check_string.split('],')
		 	pixel = 0
		 	# count = 0
		 	while pixel < len(current_image_pixels):
		 		if current_image_pixels[pixel] == check_image_pixels[pixel]:
		 			# count += 1
		 			# if count == 10:
		 			# 	count = 0
		 			match_array.append(current_model)
		 		pixel += 1
	matched_models = Counter(match_array)
	return matched_models, arrow_image_array

if __name__ == '__main__':
        # path to your test image
	matched_models, image_array = find_which_direction('images/l2.jpg')
	print(matched_models)
	graphX = []
	graphY = []
	for model in matched_models:
		if model == 'R':
			graphX.append(9)
		elif model == 'S':
			graphX.append(6)
		elif model == 'L':
			graphX.append(3)
		graphY.append(int(matched_models[model]))
	figure = plt.figure()
	grid1 = plt.subplot2grid((4, 4), (0, 0), rowspan=1,  colspan=4)
	grid2 = plt.subplot2grid((4, 4), (1, 0), rowspan=3,  colspan=4)
	grid1.imshow(image_array)
	grid2.bar(graphX, graphY, align='center')
	plt.ylim(700)
	plt.show()
# create_model()






	
