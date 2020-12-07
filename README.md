# ACC-Cement-Bag-Detector
Developed a software for ACC India to locate, segregate, and provide the count of cement bags in a given image using Computer Vision and Deep Learning. ACC India required the software to detect the total number of cement bags present in a stack using two images (front and top view of cement bags) . Purpose of software was to minimize the losses incurred because of inaccurate counting. Results were incorporated into a web application made using Flask. Object detection neural network was trained using Tensorflow Object Detection API.

Frameworks Used - Flask Web Framework<br/>
Libraries Used - Werkzeug, SQLite, OpenCV, Numpy, Six, Tensorflow, Matplotlib, Pillow<br/>
Modules Used - OS, Sys, Datetime, Tarfile, Zipfile, Collections, Io, Object Detection, Flask mail<br/>

Procedure<br/><br/>

1. Installed TensorFlow Object Detection API.<br/>
2. Took pictures with different backgrounds and varying lighting conditions.<br/>
3. Labelled the data using LabelImg tool.<br/>
4. Generated TFRecords used for training.<br/>
5. Created a label map and training configuration file.<br/>
6. Trained the model until it reached a satisfying loss.<br/>
7. Generated the inference graph for running the model.<br/>
8. Tested the object detector.<br/>


<p align="center"> 
Output
</p>

![](object_detection/image1/11_output.jpg)
![](object_detection/image1/32_output.jpg)
![](object_detection/image1/41_output.jpg)
![](object_detection/image1/51_output.jpg)
![](object_detection/image1/61_output.jpg)

<p align="center"> 
GUI of Web Application
</p>

![](webapp_images/1mw1.JPG)
![](webapp_images/1mw2.JPG)
![](webapp_images/1mw3.JPG)
![](webapp_images/1mw4.JPG)


<p align="center"> 
Type of the object(ie. cement bag) is displayed alongwith the confidence score.
</p>

![](webapp_images/1mw6.JPG)
![](webapp_images/1mw7.JPG)
