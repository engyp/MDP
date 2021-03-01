# **MDP**
The Multidisciplinary Design Project (MDP) objective is to build a robotic system that can explore an unknown area and avoid obstacles in an arena. This repository consists of raspberry pi communication and image recognition scripts.

### System Components
![alt text](https://github.com/engyp/MDP/blob/master/Documentation/rpi%20diagram.png)

# Raspberry Pi
[Raspberry Pi Setup](https://github.com/engyp/MDP/blob/master/Documentation/Setting%20up%20Raspberry%20Pi%20(Ver%202018a).pdf)


# Tensorflow

### Requirements

* TensorFlow 1.5
*	TensorFlow-gpu 1.5
*	CUDA 9.0
*	cuDNN 7.0.5
*	Anaconda with Python 3.6
*	Protobuf 3.13.0.1
*	Pillow 8.0.1	•	Lxml 4.6.1
*	Cython 0.29.21
*	Contextlib2 0.6.0
*	Matplotlib 3.3.2
*	Pandas 1.1.3
*	Opencv-python 1.0

### Imagine Recognition
[Detailed Steps](https://github.com/engyp/MDP/blob/master/Documentation/Rpi%20Wiki.docx)

### Training Images
![alt text](https://github.com/engyp/MDP/blob/master/Documentation/Training%20Samples.JPG)

### Labelling Images and Classification
![alt text](https://github.com/engyp/MDP/blob/master/Documentation/Labelling.JPG)

### Model Training
When training begins, it will step through training batches and reporting the loss at each step. At the start, the loss rate is high, and it gets lower as the object detection classifier trains.

![alt text](https://github.com/engyp/MDP/blob/master/Documentation/model%20training%201.JPG)

After few hours of training, the loss should be around 0.05 to be accurate enough. Terminal the program by press CTRL+C.

![alt text](https://github.com/engyp/MDP/blob/master/Documentation/model%20training%202.JPG)

In the Tensorboard, select TotalLoss tab to see the overall loss of the classifier over time. X axis is the loss rate and Y axis is the number of steps.

![alt text](https://github.com/engyp/MDP/blob/master/Documentation/model%20training%203.JPG)

### Test out object detection
![alt text](https://github.com/engyp/MDP/blob/master/Documentation/9_white.jpg)
![alt text](https://github.com/engyp/MDP/blob/master/Documentation/w_green.jpg)
