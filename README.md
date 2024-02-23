# OpenCV-Computer-Vision Practice two



*Discription:*

***1.This is just a small second project that we want to practice the basic image processing skills for computer vision.***

***2.This topic was focus on image processing over edge detection and image Transformation.***

![image](Figures/GUI.png)




**1.Requirements and dependencies**
  * Python 3.7 (https://www.python.org/downloads/)
  * Opencv-contrib-python (3.4.2.17)
  * Matplotlib 3.1.1
  * UI framework: pyqt5 (5.15.1)



**2.Usage:**

1. Downloads whole repository and change path into the main folder
2. Run `python start.py` .
3. Input the image.
4. Run the whole code.

**3.Feature:**

1.Edge detection

* 3.1 Guassian Blur :
  
    * Extract 3 channels of the image BGR to 3 separated channels.
      
      ![image](Figures/1.1_result.png)
* 3.2 Sobel X:
  
    * Transform image into grayscale image
    * Merge BGR separated channel images from above problem into grayscale image by average weight : (R+G+B)/3.

      ![image](Figures/1.2_result.png)
* 3.3 Sobel Y
  
    * Transform [opencv.png](Figures/opencv.png) from BGR format to HSV format.
    * Generate mask by calling : cv2.inRange(hsv_img , lower_bound , upper_bound)
    * Detect Green and White color in the image by calling : cv2.bitwise_and(bgr_img , bgr_img , mask)

     ![image](Figures/1.3_result.png)
* 3.4 Magnitude
  
   * Here [Dog_Strong.jpg](Figures/Dog_Strong.jpg) and [Dog_Weak.jpg](Figures/Dog_Weak.jpg) to be example

   https://github.com/Kung-hen/Image-processing-and-smooth/assets/95673520/ce2d8d34-6793-4961-8f74-fe055452e71e


    
2.Image Transformation

* 4.1 Resize
   * Apply gaussian filter k x k to input image1.
   * filter kernel equation = (k=2m+1)

https://github.com/Kung-hen/Image-processing-and-smooth/assets/95673520/92b5157a-ce60-4701-bbb1-2a355492ea54

* 4.2 Translation
   * Define: Bilateral magnitude 0 ~ 10, sigmaColor = 90 and sigmaSpace = 90. 
   * Apply Bilateral filter k x k to input image1.
   * filter kernel equation = (k=2m+1)
     
https://github.com/Kung-hen/Image-processing-and-smooth/assets/95673520/ba7cc81d-efd2-4800-ba98-c87b61829303

* 4.3 Rotation scalling
   * Define: Median magnitude 0 ~ 10.
   * Apply Median filter k x k to input image1.
   * filter kernel equation = (k=2m+1)

https://github.com/Kung-hen/Image-processing-and-smooth/assets/95673520/89c4e7a8-0f73-4c8e-bc3d-8f68de7a81d5

* 4.4 Shearing









