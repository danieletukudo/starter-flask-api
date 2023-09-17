import cv2
from flask import Flask, request, jsonify, url_for,Blueprint
import os
import  save_encoding
import recognize_from_image
import uuid
import face_recognition

"""
      This is the face  recognition API which takes in the image from the web browser and then passes it to the face recogntion
      model which detects and reocgnizes the face and then sends it back to the browser
      
      It also does face side or profile face detection
       """

app = Flask(__name__, static_url_path='/')

bp1 = Blueprint('bp1', __name__, static_folder='static1')
bp2 = Blueprint('bp2', __name__, static_folder='static2')



# Register the blueprints with the Flask app
app.register_blueprint(bp1)
app.register_blueprint(bp2)

UPLOAD_FOLDER = "./static1"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg','webp'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# saving the image gotten from the browser to the input image folder
# if done saving returns "File uploaded successfully"

@app.route('/add', methods=['POST'])
def save_file():
    try:
        if request.method == 'POST':

            input_image = request.files['file']

            if input_image.filename == '':
                return  jsonify({'response':'No  files inserted yet'})

            if input_image and allowed_file(input_image.filename):

                image = face_recognition.load_image_file(input_image)
                face_loaction = face_recognition.face_locations(image)

                if face_loaction == []:

                    return jsonify({'response': 'No human face, please insert a clear picture of a person with the face looking at the camera'})
                else:
                    name = request.form.to_dict()
                    first_name = name['first_name'].lower()
                    last_name = name['sur_name'].lower()
                    first_name = ''.join(first_name.split())
                    last_name = ''.join(last_name.split())

                    saved_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image_name =  f'{first_name}_{last_name}.{uuid.uuid4()}' + ".jpg"
                    ID = image_name.split('.')[1]
                    cv2.imwrite(
                        os.path.join(app.config['UPLOAD_FOLDER'],image_name),
                        saved_image)
                    save_encoding.save_encoding(saved_image, image_name)
                    # rf.save_encoding
                    return jsonify({'ID':ID})
                    # return f"File uploaded successfully, HERE IS YOUR IMAGE ID: <b>{ID}</b>"
            else:

                return jsonify({'response':'Please upload the right picture file with extension of  png, jpg or jpeg'})

    except:

        return jsonify({'response': 'invalid input'})


# sending the image gotten to the face detection and recognition model for processing
# if done returns the image to the main web page with the detected name on it

@app.route('/search', methods=['POST'])
def run_model():
    try:
        input_image = request.files['file']

        if input_image.filename == '':

            return jsonify({'response':'No  files inserted yet'})
        if input_image and allowed_file(input_image.filename):


            model = recognize_from_image.recognize_from_image()

            result = str(model.start_image_recognition(input_image))

            image =  result.split('@')[0]
            confidence_score =result.split('@')[1]

            if image == "Unknown" or image  == "None":

                return  jsonify({'response':'Image Unknown'})

            elif image == "Found More Known Faces":

                img_url = url_for('bp2.static', filename='multiple_image.jpg', _external=True)
                return jsonify({'image_url': img_url}), 202

            else:

                img_url = url_for('bp2.static', filename=f'{image}.jpg', _external=True)
                return jsonify({
                    'image_url': img_url,
                    'confidence_score': confidence_score

                                }), 202

                # return send_file(f'./static2/{image}.jpg'),202
        else:

            return jsonify({'response': 'Please upload the right picture file with extension of  png, jpg or jpeg'})

    except:
        return jsonify({'response': 'invalid input'})


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=6000,debug=True)





