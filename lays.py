import numpy as np
import cv2 
import matplotlib.pyplot as plt

#  Loading the image to be testedls
# gets image from camera
cam = cv2.VideoCapture(0)

def detectobject(test_image):
     #test_image = cv2.imread('lays2.jpg')

     test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

     haar_cascade = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/Lays_classifier.xml')

     faces_rects = haar_cascade.detectMultiScale(test_image_gray)

     print('Objects found: ', len(faces_rects))

     for x,y,w,h in faces_rects:
          cv2.rectangle(test_image, (x, y), (x+w, y+h), (0, 0, 255), 10)
          

     plt.imshow(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
     plt.show()

def sift(img2):
     #reading image
     img1 = cv2.imread('/home/pi/finalProj/image/lays1.jpg')  
     #img2 = cv2.imread('lays2.jpg') 

     img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
     img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

     #sift
     sift = cv2.xfeatures2d.SIFT_create()

     keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
     keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

     FLANN_INDEX_KDTREE = 0

     index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
     search_params = dict(checks=50)   # or pass empty dictionary

     flann = cv2.FlannBasedMatcher(index_params,search_params)

     matches = flann.knnMatch(descriptors_1,descriptors_2,k=2)

     # Need to draw only good matches, so create a mask
     matchesMask = [[0,0] for i in range(len(matches))]
     count = 0
     # ratio test as per Lowe's paper
     for i,(m,n) in enumerate(matches):
          if m.distance < 0.7*n.distance:
               count +=1
               matchesMask[i]=[1,0]

     draw_params = dict(matchColor = (0,255,0),
                    singlePointColor = (255,0,0),
                    matchesMask = matchesMask,
                    flags = 0)

     img3 = cv2.drawMatchesKnn(img1,keypoints_1,img2,keypoints_2,matches,None,**draw_params)
     print(len(matches))
     print(count)
     if count >= 10:
          print("Detected Lays")
     plt.imshow(img3,),plt.show()
               
val, img = cam.read()
detectobject(img)
sift(img)
