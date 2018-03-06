# 3-D-Reconstruction-of-an-object-from-a-single-image

This project focuses on an implementation of the paper “single view metrology” (Criminisi, Reid and Zisserman, ICCV99). It describes
how aspects of the affine 3D geometry of a scene can be computed from a single perspective image with some prior knowledge. Following steps were involved in this project:
1)	In the 1st step of the project, we took an image of a 3D box by following the 3 point perspective imaging methodology. 
2) We read the image and apply Line Segment Detector(LSD) algorithm on the image. The algorithm detects several lines in the image  and outputs a pair of points for each line, the starting co-ordinates and the end co-ordinates of the line. This code is contained in the file lsd_svm.py. 
3)We then sort the lines belonging to X, Y and Z axis based on the angle they make with the X-axis. These lines are then separately passed through FitLine method of openCV with distType set to ‘CV_DIST_WELSCH’. 
It uses a modification of the RANSAC algorithm to fit the line. The lines detected are then marked and written into a text file .
4) The input to the below code(SVM.py) is taken from the input file, input.txt
5)

     
