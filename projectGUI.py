
import Tkinter as tk
from Tkinter import *
from PIL import Image, ImageTk
import tkFileDialog
# import the necessary packages

from skimage.filters import threshold_local
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import os

root=tk.Tk()
photomain=ImageTk.PhotoImage(Image.open("2.png").resize((50,50), Image.ANTIALIAS))
img=Label(root,image=photomain)
img.pack()
root.title("Document Scanner and Digit Recognition")
f1=Frame(root)
f1.pack(side=TOP,fill=X)
f2 = Frame(root)
f2.pack(side=TOP, fill=X, padx=450)
tk.Label(f1,
		 text="Document Scanner and Digit Recognition",
		 fg="blue", pady=10, padx=20,
		 font="Helvetica 25 bold italic").pack()
tk.Label(f1,
		 text="Document Scanner",
		fg = "black",pady=5,padx=20,
		font = "Helvetica 15 bold").pack()




def docsan():
	filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
										  filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
	image = cv2.imread(filename)
	ratio = image.shape[0] / 500.0
	orig = image.copy()
	image = imutils.resize(image, height=500)

	# convert the image to grayscale, blur it, and find edges
	# in the image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 75, 200)

	# show the original image and the edge detected image
	print("STEP 1: Edge Detection")
	cv2.imshow("Image", image)
	cv2.imshow("Edged", edged)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# find the contours in the edged image, keeping only the
	# largest ones, and initialize the screen contour
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			break

	# show the contour (outline) of the piece of paper
	print("STEP 2: Find contours of paper")
	cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
	cv2.imshow("Outline", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# apply the four point transform to obtain a top-down
	# view of the original image
	warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

	# convert the warped image to grayscale, then threshold it
	# to give it that 'black and white' paper effect
	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	T = threshold_local(warped, 11, offset=10, method="gaussian")
	warped = (warped > T).astype("uint8") * 255

	# show the original and scanned images
	print("STEP 3: Apply perspective transform")
	cv2.imshow("Original", imutils.resize(orig, height=650))
	cv2.imshow("Scanned", imutils.resize(warped, height=650))
	cv2.waitKey(0)
	cv2.destroyAllWindows()


A = tk.Button(f1, text="Run Document Scanner", command=docsan)
A.pack()
tk.Label(f1,
		 text="Digit Recognition on the thermostat",
		 fg="black", pady=20, padx=20,
		 font="Helvetica 15 bold").pack()
tk.Label(f1,
		 text="To recognize the digits on the thermostat using OpenCV and Python",
		 fg="black", pady=5, padx=20, justify=LEFT,
		 font="Helvetica 10").pack()



def runpy():
	DIGITS_LOOKUP = {
		(1, 1, 1, 0, 1, 1, 1): 0,
		(0, 0, 1, 0, 0, 1, 0): 1,
		(1, 0, 1, 1, 1, 1, 0): 2,
		(1, 0, 1, 1, 0, 1, 1): 3,
		(0, 1, 1, 1, 0, 1, 0): 4,
		(1, 1, 0, 1, 0, 1, 1): 5,
		(1, 1, 0, 1, 1, 1, 1): 6,
		(1, 0, 1, 0, 0, 1, 0): 7,
		(1, 1, 1, 1, 1, 1, 1): 8,
		(1, 1, 1, 1, 0, 1, 1): 9
	}
	image = path11
	print image + "..........image"

	# load the example image
	image = cv2.imread(image)

	# pre-process the image by resizing it, converting it to
	# graycale, blurring it, and computing an edge map
	image = imutils.resize(image, height=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(blurred, 50, 200, 255)

	# find contours in the edge map, then sort them by their
	# size in descending order
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
							cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	displayCnt = None

	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if the contour has four vertices, then we have found
		# the thermostat display
		if len(approx) == 4:
			displayCnt = approx
			break

	# extract the thermostat display, apply a perspective transform
	# to it
	warped = four_point_transform(gray, displayCnt.reshape(4, 2))
	output = four_point_transform(image, displayCnt.reshape(4, 2))

	# threshold the warped image, then apply a series of morphological
	# operations to cleanup the thresholded image
	thresh = cv2.threshold(warped, 0, 255,
						   cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

	# find contours in the thresholded image, then initialize the
	# digit contours lists
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
							cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	digitCnts = []

	# loop over the digit area candidates
	for c in cnts:
		# compute the bounding box of the contour
		(x, y, w, h) = cv2.boundingRect(c)

		# if the contour is sufficiently large, it must be a digit
		if w >= 15 and (h >= 30 and h <= 40):
			digitCnts.append(c)

	# sort the contours from left-to-right, then initialize the
	# actual digits themselves
	digitCnts = contours.sort_contours(digitCnts,
									   method="left-to-right")[0]
	digits = []

	# loop over each of the digits
	for c in digitCnts:
		# extract the digit ROI
		(x, y, w, h) = cv2.boundingRect(c)
		roi = thresh[y:y + h, x:x + w]

		# compute the width and height of each of the 7 segments
		# we are going to examine
		(roiH, roiW) = roi.shape
		(dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
		dHC = int(roiH * 0.05)

		# define the set of 7 segments
		segments = [
			((0, 0), (w, dH)),  # top
			((0, 0), (dW, h // 2)),  # top-left
			((w - dW, 0), (w, h // 2)),  # top-right
			((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # center
			((0, h // 2), (dW, h)),  # bottom-left
			((w - dW, h // 2), (w, h)),  # bottom-right
			((0, h - dH), (w, h))  # bottom
		]
		on = [0] * len(segments)

		# loop over the segments
		for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
			# extract the segment ROI, count the total number of
			# thresholded pixels in the segment, and then compute
			# the area of the segment
			segROI = roi[yA:yB, xA:xB]
			total = cv2.countNonZero(segROI)
			area = (xB - xA) * (yB - yA)

			# if the total number of non-zero pixels is greater than
			# 50% of the area, mark the segment as "on"
			if total / float(area) > 0.5:
				on[i] = 1

		# lookup the digit and draw it on the image
		digit = DIGITS_LOOKUP[tuple(on)]
		digits.append(digit)
		cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
		cv2.putText(output, str(digit), (x - 10, y - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

	# display the digits

	print(u"{}{}.{} \u00b0C".format(*digits))
	cv2.imshow("Input", image)
	cv2.imshow("Output", output)
	root11 = Tk()

	tk.Label(root11,
			 text=u"{}{}.{} \u00b0C".format(*digits),
			 fg="black", pady=20, padx=20,
			 font="Helvetica 15 bold").pack()

	root11.mainloop()
	cv2.waitKey(0)


def getimg():
	global path11
	path11 = tkFileDialog.askopenfilename(filetypes=[("Image Files", '.jpg')])
	print path11 + "........getimg"
	os.system(path11)


photo1 = ImageTk.PhotoImage(Image.open("6.png").resize((50, 50), Image.ANTIALIAS))
imaglab1 = Label(f2, image=photo1)
imaglab1.grid(row=0)
A = tk.Button(f2, text="Thermostat Image", command=getimg, height=1, width=35)
A.grid(row=1)
photo = ImageTk.PhotoImage(Image.open("3.png").resize((50, 50), Image.ANTIALIAS))
imaglab = Label(f2, image=photo)
imaglab.grid(row=0, column=1)
B = tk.Button(f2, text="Recoginze digit on thermostat", command=runpy, height=1, width=35)
B.grid(row=1, column=1)
tk.mainloop()


