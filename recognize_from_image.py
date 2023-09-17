import numpy as np
import pickle
import face_recognition
import cv2
import  os

class recognize_from_image:

    known_face_names = []
    def start_image_recognition(self, path):

        for image in os.listdir('face_embaddings'):
            image_names = os.path.splitext(image)[0]
            self.known_face_names.append(os.path.splitext(image_names)[0])

        image = face_recognition.load_image_file(path)
        known_face_encodings = []

        face_locations_in_test_image = face_recognition.face_locations(image)
        face_encodings_in_test_image = face_recognition.face_encodings(image, face_locations_in_test_image,100,'large')
        face_names = []

        for embeddings in os.listdir("face_embaddings"):

            with open(f"face_embaddings/{embeddings}", "rb") as f:
                    data = pickle.load(f)

                    known_face_encodings.append(data)


        with open("final_embaddings/all_face_encodings.dat", "wb") as f:
                    data = pickle.dump(known_face_encodings,f)

        with open("final_embaddings/all_face_encodings.dat", "rb") as f:
            data1 = pickle.load( f)


        for encodeface, face_location in zip(face_encodings_in_test_image, face_locations_in_test_image):

                        matches = face_recognition.compare_faces(data1, encodeface,0.3)

                        name = "Unknown"
                        face_distances = face_recognition.face_distance(data1, encodeface)
                        images_match_index = np.argmin(face_distances)

                        y1 = face_location[0]
                        x1 = face_location[3]
                        x2 = face_location[1]
                        y2 = face_location[2]


                        confidence_score = (1 - face_distances[images_match_index])*100
                        confidence_score = "{:.2f}".format(confidence_score)

                        if matches[images_match_index]:

                                name = self.known_face_names[images_match_index]
                                face_names.append(name)
                                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                                display_name = os.path.splitext(name)[0]
                                cv2.putText(image, display_name, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)

        if len(face_names) > 1:
            output_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f'./static2/multiple_image.jpg', output_image)
            return "Found More Known Faces"
        else:
            output_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f'./static2/{name}.jpg', output_image)
            result= f'{name}@{confidence_score}'
            return result
