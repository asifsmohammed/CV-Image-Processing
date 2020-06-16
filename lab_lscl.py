import cv2
import numpy as np
import sys

# read arguments
if(len(sys.argv) != 7) :
    print(sys.argv[0], ": takes 6 arguments. Not ", len(sys.argv)-1)
    print("Expecting arguments: w1 h1 w2 h2 ImageIn ImageOut.")
    print("Example:", sys.argv[0], " 0.2 0.1 0.8 0.5 fruits.jpg out.png")
    sys.exit()

w1 = float(sys.argv[1])
h1 = float(sys.argv[2])
w2 = float(sys.argv[3])
h2 = float(sys.argv[4])
name_input = sys.argv[5]
name_output = sys.argv[6]

# check the correctness of the input parameters
if(w1<0 or h1<0 or w2<=w1 or h2<=h1 or w2>1 or h2>1) :
    print(" arguments must satisfy 0 <= w1 < w2 <= 1, 0 <= h1 < h2 <= 1")
    sys.exit()

# read image
inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)

if(inputImage is None) :
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()
# cv2.imshow("input image: " + name_input, inputImage)

# check for color image and change w1, w2, h1, h2 to pixel locations 
rows, cols, bands = inputImage.shape
if(bands != 3) :
    print("Input image is not a standard color image:", inputImage)
    sys.exit()

#Converting the image to LAB
image_luv = cv2.cvtColor(inputImage, cv2.COLOR_BGR2LAB)
W1 = round(w1*(cols-1))
H1 = round(h1*(rows-1))
W2 = round(w2*(cols-1))
H2 = round(h2*(rows-1))

# Linear Scaling
def linearStretching(window_l):
    a = np.min(window_l)
    b = np.max(window_l)
    key_val = {}
    for i in range(len(window_l)):
        for j in range(len(window_l[0])):
            if window_l[i][j] in key_val:
                window_l[i][j] = key_val.get(window_l[i][j])    
            else:
                key_val[window_l[i][j]] = ((window_l[i][j] - a) * 255) / (b - a)
                window_l[i][j] = key_val.get(window_l[i][j])
    return window_l

# Applying Linear Scaling only to the window
eqImg = np.copy(image_luv)
eqImg[H1: H2+1, W1: W2+1, 0] = linearStretching(eqImg[H1: H2+1, W1: W2+1, 0])
# cv2.imshow("Linear Stretched Lab Image", eqImg)

eqImg = cv2.cvtColor(eqImg, cv2.COLOR_LAB2BGR)
# cv2.imshow("Linear Stretched BGR Image", eqImg)

# # saving the output - save the Luv Histogram Equalization window image
cv2.imwrite(name_output, eqImg)

# # wait for key to exit
# cv2.waitKey(0)
# cv2.destroyAllWindows()