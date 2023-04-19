import cv2
import face_recognition

# Load the image file
image = cv2.imread('/home/tyrion/PycharmProjects/FaceProject/pics/known_faces/向博.jpg')

# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
rgb_image = image[:, :, ::-1]

# Find all the faces in the image
face_locations = face_recognition.face_locations(rgb_image)

# Loop through each face location and draw a rectangle around it
for (top, right, bottom, left) in face_locations:
    # Draw a rectangle around the face
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(image, 'XiangBo', (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

# Show the resulting image with the rectangles drawn around the faces
# cv2.imshow('Image with faces', image)
# cv2.waitKey(0)

_s = []
for _ in _s:
    print(_)
print(1)
