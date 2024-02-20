from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
from UI import Ui_Form
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


class Form_controller(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setup_control()

        self.gauss = np.array([
            [0.045, 0.122, 0.045],
            [0.122, 0.332, 0.122],
            [0.045, 0.122, 0.045]])

        self.sobel_x = np.array([
            [-1.0, 0.0, 1.0],
            [-2.0, 0.0, 2.0],
            [-1.0, 0.0, 1.0]])

        self.sobel_y = np.array([
            [1.0, 2.0, 1.0],
            [0.0, 0.0, 0.0],
            [-1.0, -2.0, -1.0]])

        self.kernel_len = len(self.gauss[0])

    def setup_control(self):
        # TODO
        # qpushbutton doc: https://doc.qt.io/qt-5/qpushbutton.html
        self.ui.pushButton_14.clicked.connect(self.open_file)
        self.ui.pushButton_4.clicked.connect(self.Gauss)
        self.ui.pushButton_5.clicked.connect(self.sobelX)
        self.ui.pushButton_6.clicked.connect(self.sobelY)
        self.ui.pushButton_13.clicked.connect(self.magnitude)
        self.ui.pushButton_7.clicked.connect(self.resizeimg)
        self.ui.pushButton_8.clicked.connect(self.trans)
        self.ui.pushButton_9.clicked.connect(self.rotate)
        self.ui.pushButton_15.clicked.connect(self.shearing)

    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self, "Open file", "./")                 # start path
        # print(filename, filetype)
        result = os.path.split(filename)[1]
        self.img = cv2.imread(filename, -1)
        gray_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.gray_img = np.asarray(gray_image)/255.0

        self.ui.label.setText(result)

    def pad_image(self, image, height, width):
        """
        Returns image padded with zeros. For example: Input [2, 2] --> Output [0, 0, 0, 0]
                                                            [2, 2]            [0, 2, 2, 0]
                                                                              [0, 2, 2, 0]
                                                                              [0, 0, 0, 0]
        """
        pad = int((self.kernel_len - 1)/2)  # padding to preserve image size
        padded_img = np.zeros((height + 2*pad, width + 2*pad))
        padded_img[pad: height + pad, pad: width + pad] = image
        return padded_img

    def conv2d(self, image, kernel):
        """ 
        Computes 2d convolution multyplying kernel by image.
        """
        output_img = np.zeros_like(image)
        height, width = image.shape
        padded_img = self.pad_image(image, height, width)

        for x_out in range(height):
            for y_out in range(width):
                """ 
                 Mapping center coordinates from gray img to padded image 
                 E.g. Coord [0,0] in gray --> [1, 1] in padded image                
                """
                x_pad, y_pad = x_out+1, y_out+1
                x_indices = [x_pad-1, x_pad, x_pad+1]
                y_indices = [y_pad-1, y_pad, y_pad+1]
                img_window = padded_img[x_indices, :][:, y_indices]
                output_img[x_out][y_out] = np.sum(
                    np.multiply(img_window, kernel)).astype('float32')

        return output_img

    def Gauss(self):
        kernel = self.gauss
        blur_img = self.conv2d(self.gray_img, kernel)
        cv2.imshow("Gaussian Blur", blur_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return blur_img

    def sobelX(self):
        kernel = self.gauss
        blur_image = self.conv2d(self.gray_img, kernel)
        kernel = self.sobel_x
        self.sobel_X_image = self.conv2d(blur_image, kernel)
        cv2.imshow("Sobel X", self.sobel_X_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return self.sobel_X_image

    def sobelY(self):
        kernel = self.gauss
        blur_image = self.conv2d(self.gray_img, kernel)
        kernel = self.sobel_y
        self.sobel_Y_image = self.conv2d(blur_image, kernel)
        cv2.imshow("Sobel Y", self.sobel_Y_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return self.sobel_Y_image

    def magnitude(self):
        x = self.sobel_X_image
        y = self.sobel_Y_image
        mag = np.sqrt(pow(x, 2)+pow(y, 2))
        cv2.imshow("Magnitude", mag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def resizeimg(self):
        resize = cv2.resize(self.img, (215, 215))
        # 2x3 矩陣，x 軸平移 200，y 軸平移 100
        M = np.float32([[1, 0, 0], [0, 1, 0]])
        self.output = cv2.warpAffine(resize, M, (430, 430))

        cv2.imshow("Resize", self.output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def trans(self):
        resize = cv2.resize(self.img, (215, 215))
        M = np.float32([[1, 0, 215], [0, 1, 215]])
        self.output_trans = cv2.warpAffine(self.output, M, (430, 430))
        self.result = cv2.addWeighted(self.output, 1, self.output_trans, 1, 0)
        cv2.imshow("translate and overlay", self.result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def rotate(self):
        # # 中心點 (240, 180)，旋轉 45 度，尺寸 1
        M = cv2.getRotationMatrix2D((215, 215), 45, 0.5)
        self.output_rotate = cv2.warpAffine(self.result, M, (430, 430))
        cv2.imshow("Rotate and scale", self.output_rotate)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def shearing(self):
        pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
        pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
        M = cv2.getAffineTransform(pts1, pts2)
        img_shear = cv2.warpAffine(self.output_rotate, M, (430, 430))
        cv2.imshow("Share", img_shear)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
