import pickle
import face_recognition

def save_encoding(path,image_name):
            face_encoding= face_recognition.face_encodings(path,None,100,"large")[0]
            with open(f"face_embaddings/{image_name}.dat", "wb") as data:
               pickle.dump(face_encoding,data)

