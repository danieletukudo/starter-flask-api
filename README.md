# Face recogntion API

This code is a Flask application that serves as a face recognition API. The application has several routes for receiving images and processing them with face recognition algorithms. The recognized faces are saved in a database and can be later retrieved by name or image ID.

The Flask application is initialized with a Blueprint object which provides a modular structure for organizing the application code. The Blueprint object is used to define two static folders to serve static content like HTML, CSS, and JavaScript files.

# The application routes are as follows:
# The "/add" route 
# request POST

request input  ##"files"
input for name 'first_name','sur_name'

used to upload an image file to the server. The file is checked for allowed extensions and is saved in the "static1" folder. The face recognition algorithm is applied to the image, and if a face is detected, the image's encoding is saved to the database. If the face is not detected, a message is returned to the user indicating that a human face was not found in the uploaded image.

The function first checks if the request method is POST, and then retrieves the uploaded image file from the request using request.files['file'].

The function then checks if the filename of the uploaded image is not empty, and that it has an allowed extension (defined by the allowed_file() function), using the if statement.

If the uploaded image is valid, the function proceeds to use the face_recognition library to detect any human faces in the image. If there is no detected face, the function returns an error message indicating that a clear picture of a person with the face looking at the camera should be uploaded.

If a face is detected in the image, the function proceeds to extract the first and last name of the person from the POST request's form data. Then it saves the uploaded image in the designated UPLOAD_FOLDER, with a unique image name generated using the uuid library.

The function then saves the encoding of the saved image for facial recognition in save_encoding(). The image ID is returned as a JSON response with a status code of 202.

If the uploaded image is not valid, an error message is returned indicating that the uploaded file should be in the correct format with a valid extension.


# The "/search" route 
used to search for a face in the database. The image file is checked for allowed extensions and is processed by the face recognition algorithm. If a face is detected, the face is recognized, and the corresponding image is retrieved from the database and returned to the user with the name of the recognized person. If more than one known face is detected, a message is returned to the user indicating that the image has more than one known face. If the face is not recognized, a message is returned to the user indicating that the face is unknown.
It takes an uploaded image file from the request, runs a face recognition model to identify the person in the image, and returns a response in JSON format.

The first if statement checks if the uploaded file has a filename. If not, it returns a JSON response indicating that no files were inserted yet.

The second if statement checks if the uploaded file has an allowed image file extension. If not, it returns a JSON response asking the user to upload a file with a valid extension.

If the uploaded file is valid, the function calls the recognize_from_image() method from a module named recognize_from_image to identify the person in the image. If the model returns "Unknown" or "None", it means that the person in the image is not recognized, and the function returns a JSON response with the message "Image Unknown". If the model returns "Found More Known Faces", it means that the image contains multiple recognized faces, and the function returns a JSON response with the image URL of a placeholder image showing multiple faces. Otherwise, the model returns the name of the recognized person, and the function returns a JSON response with the image URL of the recognized person's photo.


# ***************************************
# ***************************************
# ***************************************
# ***************************************
# facelib_modular_  face_recognition_pipline
simple and modular framework to perform all stages of face recognition pipeline (detection, alignment, embedding, matching) with the possibility to add and use different models and techniques for each stage.

## content
* what is facelib
* architecture
* video recognition
* usage
* acknowledgment



![friends]( https://github.com/Alloooshe/facelib_modular_face_recognition_pipline/blob/master/images/out.jpg)

## what is facelib ?
the project solves the problem of face recognition by solving each of the following problems individually: face detection, face alignment, face embedding and face matching or recognition, the code reflects the academic partition so that each step can be carried out independently with whatever framework or programming language the user prefers and then it will be integrated in the pipeline. the project also works with video or live stream and implement object tracking to get better results and to reduce the computation cost when dealing with high frame rate.
the project aims to find a software solution that allows developers to quickly customize a face recognition pipeline depending on their needs, also the project help researchers evaluate their models developed for a specific task (such as face embedding) with different detection and alignment methods. there are many other useful use cases for the project. 
the code is organized and documented in a good way so that developers can read and make adjustments relatively easy, the docs is built using sphinx so the user can search for any needed documentation. 
## architecture
![facelib architecture]( https://github.com/Alloooshe/facelib_modular_face_recognition_pipline/blob/master/images/architecture.PNG)

The code architecture consists of independent units that perform independent tasks, the main block is the class FaceCore which handles the pipeline operation but can be used for single tasks such as detection or embedding. 
Each class has the option to “clean” the model it leaded, the FaceCore is built to keep the models in memory in order to avoid loading overhead. This boost the performance of facelib in applications. In any time, you can use the clean option to free memory up. 


## video recognition
The FaceCore class can perform video face recognition and tracking using the function “process stream” (which can handle both live stream and video) , this includes ignoring small faces that appears in a video and once a face is bigger than a threshold it then performs recognition pipeline on that face for N (a variable that you can control) frames and it accumulate the decision made about the identity of the face and makes a final decision, once a final decision is made no more recognition is performed and the function continue to only track the face.  
the decision accumulation can be made in two ways (found to have similar performance) which are voting and feature fusion, in voting each of the first N frames has one vote on the final decision while in feature fusion we take the mean of the N embedding vectors extracted in the N frames for a certain face and then make a final matching using the new embedding vector.
This is important to reduce the computation cost and to make better face recognition. 


 ## usage
coming soon

## demo
[face recognition video]( https://www.youtube.com/watch?v=kSNk_1QLzbQ)

The faceapp.ui contains a  UI generated using PyQt designer (it can be comipled to different platforms) the faceapp.py the python compiled version. You can run the faceapp.py and try image, video and webcam face recognition, you can also add faces to your database. 
## acknowledgment
1. [MTCNN](https://github.com/ipazc/mtcnn)
2. [facenet](https://github.com/davidsandberg/facenet)
3. [SORT](https://github.com/abewley/sort)
4. [arcface](https://github.com/deepinsight/insightface)

