import io
import math
import socket
import struct

import cv2
from PIL import Image
from deepface import DeepFace

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Accept a single connection and make a file-like object out of it
try:
        while True:
                connection = server_socket.accept()[0].makefile('rb')
                i=0
                total = 0
                nr_positive = 0
                total_frames = 0
                emotion = ''
                while True:
                        # Read the length of the image as a 32-bit unsigned int. If the
                        # length is zero, quit the loop
                        try:
                                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                        except:
                                break
                        print(image_len)
                        if not image_len:
                                client, addr = server_socket.accept()
                                if total_frames == 0:
                                        total = 0
                                else:
                                        total = nr_positive / total_frames
                                print(total, nr_positive, total_frames, emotion)
                                ack = str(round(total, 2)*100)
                                client.send(ack.encode())
                                break
                        # Construct a stream to hold the image data and read the image
                        # data from the connection
                        image_stream = io.BytesIO()
                        image_stream.write(connection.read(image_len))
                        # Rewind the stream, open it as an image with PIL and do some
                        # processing on it
                        image_stream.seek(0)
                        image = Image.open(image_stream)
                        print('Image is %dx%d' % image.size)
                        image.save('./img/' + str(i) + '.jpg')
                        #img_convert = np.array(Image.open('./img/' + str(i) + '.jpg'))
                        img_convert = cv2.imread('./img/' + str(i) + '.jpg')
                        print(type(img_convert))
                        gray = cv2.cvtColor(img_convert, cv2.COLOR_BGR2GRAY)
                        face = face_classifier.detectMultiScale(gray, 1.3, 5)

                        for (x, y, w, h) in face:
                                try:
                                        result = DeepFace.analyze(
                                                img_convert)  # same thing is happing here as the previous example, we are using the analyze class from deepface and using ‘frame’ as input
                                        print(result[0]['dominant_emotion'])
                                        emotion = result[0]['dominant_emotion']
                                        if result[0]['dominant_emotion'] == "happy" or result[0]['dominant_emotion'] == "surprise":
                                                nr_positive += 1
                                        total_frames += 1
                                        print(nr_positive, total_frames)

                                except:
                                        print("no face")
                                        emotion = "no face"
                                        total_frames += 1

                        i+=1
finally:
    connection.close()
    server_socket.close()
