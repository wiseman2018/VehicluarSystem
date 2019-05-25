import cv2
import numpy as np
import urllib.request

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image

#original = cv2.imread("images/original.jpg")
original = url_to_image("https://res.cloudinary.com/dz6dhr4se/image/upload/v1557927862/mpj0fnuuwycxetyiveim.jpg")
image_to_compare = cv2.imread("images/duplicate1.jpg")


# checking if images are equal
if original.shape == image_to_compare.shape:
    print("the images has same size")
    difference = cv2.subtract(original, image_to_compare)

    b, g, r = cv2.split(difference)

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        print("Images are completely the same")
    else:
        print("images are not equal")


# 2) Check for similarities between the 2 images
sift = cv2.xfeatures2d.SIFT_create()
kp_1, desc_1 = sift.detectAndCompute(original, None)
kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

index_params = dict(algorithm=0, trees=5)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(desc_1, desc_2, k=2)

good_points = []
ratio = 0.6
for m, n in matches:
    if m.distance < ratio*n.distance:
        good_points.append(m)
print(len(good_points))
result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)

    

cv2.imshow("original", original)
cv2.imshow("duplicate", image_to_compare)
cv2.waitKey(0)
cv2.destroyAllWindows()