import numpy as np
import cv2 
import matplotlib.pyplot as plt

#  Loading the image to be testedls
# gets image from camera
cam = cv2.VideoCapture(0)

def detectobject(test_image):
     #test_image = cv2.imread('lays2.jpg')

     test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
     #classifiers
     lays_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/Lays_classifier.xml')
     clorox_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/Clorox_classifier.xml')
     kellogg_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/kellogs_classifier.xml')
     cheetos_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/cheetos_classifier.xml')
     kitkat_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/kitkat_classifier.xml')
     vaseline_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/vaseline_classifier.xml')
     pepsi_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/pepsi_classifier.xml')
     clif_clf = cv2.CascadeClassifier('/home/pi/finalProj/Cascades/clif_classifier.xml')

     #rects
     lays_rects = lays_clf.detectMultiScale(test_image_gray)
     clorox_rects = clorox_clf.detectMultiScale(test_image_gray)
     kellogg_rects = kellogg_clf.detectMultiScale(test_image_gray)
     cheetos_rects = cheetos_clf.detectMultiScale(test_image_gray)
     kitkat_rects = kitkat_clf.detectMultiScale(test_image_gray)
     vaseline_rects = vaseline_clf.detectMultiScale(test_image_gray)
     pepsi_rects = pepsi_clf.detectMultiScale(test_image_gray)
     clif_rects = clif_clf.detectMultiScale(test_image_gray)

            
     print('Objects found: ', len(lays_rects)+len(clorox_rects)++len(kellogg_rects)+
             len(cheetos_rects)+len(kitkat_rects)+len(vaseline_rects)+len(pepsi_rects)+
             len(clif_rects))

     for x,y,w,h in lays_rects:
         cv2.rectangle(test_image, (x, y), (x+w, y+h), (0, 0, 255), 2)
         cv2.putText(test_image,'Lays',(x-5,y-5),cv2.FONT_HERSHEY_COMPLEX,0.5,2)

     for x,y,w,h in clorox_rects:
         cv2.rectangle(test_image, (x,y), (x+w, y+h), (255, 0, 255), 2)
         cv2.putText(test_image,'Clorox',(x-5,y-5),cv2.FONT_HERSHEY_COMPLEX,0.5,2)

     for x,y,w,h in kellogg_rects:
         cv2.rectangle(test_image, (x,y), (x+w, y+h), (0, 255, 0), 2)
         cv2.putText(test_image,'kellogg',(x-5,y-5),cv2.FONT_HERSHEY_COMPLEX,0.5,2)

     for x,y,w,h in kitkat_rects:
         cv2.rectangle(test_image, (x,y), (x+w, y+h), (0, 255, 0), 2)
         cv2.putText(test_image,'Kitkat',(x-5,y-5),cv2.FONT_HERSHEY_COMPLEX,0.5,2)

     for x,y,w,h in cheetos_rects:
         cv2.rectangle(test_image, (x,y), (x+w, y+h), (0, 255, 0), 2)
         cv2.putText(test_image,'Cheetos',(x-5,y-5),cv2.FONT_HERSHEY_COMPLEX,0.5,2)

     for x,y,w,h in vaseline_rects:
         cv2.rectangle(test_image, (x,y), (x+w, y+h), (0, 255, 0), 2)
         cv2.putText(test_image,'Vaseline',(x-5,y-5),cv2.FONT_HERSHEY_COMPLEX,0.5,2)

     for x,y,w,h in pepsi_rects:
         cv2.rectangle(test_image, (x,y), (x+w, y+h), (0, 255, 0), 2)
         cv2.putText(test_image,'Pepsi',(x-5,y-5),cv2.FONT_HERSHEY_COMPLEX,0.5,2)

     for x,y,w,h in clif_rects:
         cv2.rectangle(test_image, (x,y), (x+w, y+h), (0, 255, 0), 2)
         cv2.putText(test_image,'Clif',(x-5,y-5),cv2.FONT_HERSHEY_COMPLEX,0.5,2)

     #plt.imshow(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
     #plt.show()

def sift(img1,img2,thresh):
     #reading image
     #img1 = cv2.imread('/home/pi/finalProj/image/lays1.jpg')  
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

     #img3 = cv2.drawMatchesKnn(img1,keypoints_1,img2,keypoints_2,matches,None,**draw_params)
     print(len(matches))
     print(count)
     if count >= thresh:  # 10 for lays
          print("Detected clorox")
     #plt.imshow(img3,),plt.show()

while(True):               
    val, img = cam.read()
    img_spec = cv2.imread('/home/pi/finalProj/image/clorox.jpg')  
    detectobject(img)
    cv2.imshow('shopping',img)
    cv2.waitKey(25)
    sift(img_spec,img,12)
