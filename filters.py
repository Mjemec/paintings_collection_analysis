"""
file with filters that should return vector
"""

import torch
from torchvision import transforms

from utils.general import non_max_suppression_kpt
from utils.plots import output_to_keypoint, plot_skeleton_kpts

import cv2
import numpy as np

from matplotlib import pyplot as plt

def get_face_count(img):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
    return len(faces)

def get_people_count(img):
    # Load pre-trained YOLOv3 model for object detection
    net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

    # Get names of output layers
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Load image and convert to blob format
    img_blob = cv2.dnn.blobFromImage(img, scalefactor=1 / 255, size=(416, 416), swapRB=True, crop=False)

    # Set input for YOLOv3 network
    net.setInput(img_blob)

    # Run forward pass through YOLOv3 network
    detections = net.forward(output_layers)

    # Initialize counters for people and confidence scores
    num_people = 0
    confidences = []

    # Loop over detected objects and count people
    for detection in detections:
        for detected_object in detection:
            scores = detected_object[5:]
            class_id = np.argmax(scores)

            if class_id == 0:  # Class ID 0 is for people
                confidence = scores[class_id]
                if confidence > 0.5:  # Set threshold for confidence score
                    num_people += 1
                    confidences.append(float(confidence))

    # Return number of people and average confidence score
    return num_people, np.mean(confidences)


def get_histogram(image, flat=True):
    hist_1 = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist_2 = cv2.calcHist([image], [1], None, [256], [0, 256])
    hist_3 = cv2.calcHist([image], [2], None, [256], [0, 256])

    hists = list()
    hists.append(np.array(hist_1.T.tolist()[0]))
    hists.append(np.array(hist_2.T.tolist()[0]))
    hists.append(np.array(hist_3.T.tolist()[0]))
    if flat:
        return np.array(hists).flatten()
    else:
        return np.array(hists)


def get_lines_count(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Apply Hough transform to detect lines
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

    # Count number of lines
    num_lines = 0
    if lines is not None:
        num_lines = len(lines)

    return num_lines


def get_contour_count(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return len(contours)


def get_pose_mjeme(image):
    def load_model():
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model = torch.load('yolov7-w6-pose.pt', map_location=device)['model']
        # Put in inference mode
        model.float().eval()

        if torch.cuda.is_available():
            # half() turns predictions into float16 tensors
            # which significantly lowers inference time
            model.half().to(device)
        return model

    model = load_model()

    def run_inference(image):
        # image = cv2.imread(url)  # shape: (480, 640, 3)
        # # Resize and pad image
        # image = letterbox(image, 960, stride=64, auto=True)[0]  # shape: (768, 960, 3)
        # # Apply transforms
        img = transforms.ToTensor()(image)  # torch.Size([3, 768, 960])
        # Turn image into batch
        img = img.unsqueeze(0)  # torch.Size([1, 3, 768, 960])
        output, _ = model(img)  # torch.Size([1, 45900, 57])
        return output, img

    def visualize_output(output, image):
        output = non_max_suppression_kpt(output,
                                         0.25,  # Confidence Threshold
                                         0.65,  # IoU Threshold
                                         nc=model.yaml['nc'],  # Number of Classes
                                         nkpt=model.yaml['nkpt'],  # Number of Keypoints
                                         kpt_label=True)
        with torch.no_grad():
            output = output_to_keypoint(output)
        nimg = image[0].permute(1, 2, 0) * 255
        nimg = nimg.cpu().numpy().astype(np.uint8)
        nimg = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
        for idx in range(output.shape[0]):
            plot_skeleton_kpts(nimg, output[idx, 7:].T, 3)
        plt.figure(figsize=(12, 12))
        plt.axis('off')
        plt.imshow(nimg)
        plt.show()

    output, im = run_inference(image)  # Bryan Reyes on Unsplash
    visualize_output(output, im)

"""
def get_pose_edges(img1):
    model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
    movenet = model.signatures['serving_default']

    # Resize image
    img = img1.copy()
    img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 384,640)
    input_img = tf.cast(img, dtype=tf.int32)

    # Detection section
    results = movenet(input_img)
    keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))

    # Render keypoints
    loop_through_people(img1, keypoints_with_scores, EDGES, 0.1)

    cv2.imshow('Movenet Multipose', img1)

    if cv2.waitKey(10) & 0xFF==ord('q'):
        break

# Function to loop through each person detected and render
def loop_through_people(frame, keypoints_with_scores, edges, confidence_threshold):
    for person in keypoints_with_scores:
        draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)
"""