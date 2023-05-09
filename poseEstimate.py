import cv2
import time
import torch
import argparse
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms
from utils.datasets import letterbox
from utils.torch_utils import select_device
from models.experimental import attempt_load
from utils.general import non_max_suppression_kpt,strip_optimizer,xyxy2xywh
from utils.plots import output_to_keypoint, plot_skeleton_kpts,colors,plot_one_box_kpt

@torch.no_grad()
def run(poseweights="yolov7-w6-pose.pt",source="football.png",device='cpu',view_img=False,
        save_conf=False,line_thickness = 3,hide_labels=False, hide_conf=True, image_frame=None):

    frame_count = 0  #count no of frames

    # device = select_device(opt.device) #select device

    model = attempt_load(poseweights, map_location='cpu')  #Load model
    _ = model.eval()

    if image_frame is None:
        frame = cv2.imread(source)
    else:
        frame = image_frame.copy()
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names

    frame_width = int(frame.shape[0])  #get video frame width
    frame_height = int(frame.shape[1]) #get video frame height

    print("Frame {} Processing".format(frame_count+1))

    orig_image = frame #store frame
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB) #convert frame to RGB
    image = letterbox(image, stride=64, auto=True)[0]
    image_ = image.copy()
    image = transforms.ToTensor()(image)
    image = torch.tensor(np.array([image.numpy()]))

    image = image.to(device)  #convert image data to device
    image = image.float() #convert image to float precision (cpu)

    with torch.no_grad():  #get predictions
        output_data, _ = model(image)

    nkpt = model.yaml['nkpt'] if 'nkpt' in model.yaml.keys() else model.yaml['kpt_shape'][0] * model.yaml['kpt_shape'][1]
    output_data = non_max_suppression_kpt(output_data,   #Apply non max suppression
                                0.25,   # Conf. Threshold.
                                0.65, # IoU Threshold.
                                nc=model.yaml['nc'], # Number of classes.
                                nkpt=nkpt, # Number of keypoints.
                                kpt_label=True)

    output = output_to_keypoint(output_data)

    im0 = image[0].permute(1, 2, 0) * 255 # Change format [b, c, h, w] to [h, w, c] for displaying the image.
    im0 = im0.cpu().numpy().astype(np.uint8)

    im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR) #reshape image format to (BGR)
    gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh

    count = 0
    for i, pose in enumerate(output_data):  # detections per image

        if len(output_data):  #check if no pose
            for c in pose[:, 5].unique(): # Print results
                n = (pose[:, 5] == c).sum()  # detections per class


            for det_index, (*xyxy, conf, cls) in enumerate(reversed(pose[:,:6])): #loop over poses for drawing on frame
                c = int(cls)  # integer class
                kpts = pose[det_index, 6:]
                count += 1
                label = None  # if opt.hide_labels else (names[c] if opt.hide_conf else f'{names[c]} {conf:.2f}')
                plot_one_box_kpt(xyxy, im0, label=label, color=colors(c, True),
                            line_thickness=3,kpt_label=True, kpts=kpts, steps=3,
                            orig_shape=im0.shape[:2])

    return im0, count


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str, default='yolov7-w6-pose.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default='poop.png', help='video/0 for webcam') #video source
    parser.add_argument('--device', type=str, default='cpu', help='cpu/0,1,2,3(gpu)')   #device arugments
    parser.add_argument('--view-img', action='store_true', help='display results')  #display results
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels') #save confidence in txt writing
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)') #box linethickness
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels') #box hidelabel
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences') #boxhideconf
    opt = parser.parse_args()
    return opt

#function for plot fps and time comparision graph
def plot_fps_time_comparision(time_list,fps_list):
    plt.figure()
    plt.xlabel('Time (s)')
    plt.ylabel('FPS')
    plt.title('FPS and Time Comparision Graph')
    plt.plot(time_list, fps_list,'b',label="FPS & Time")
    plt.savefig("FPS_and_Time_Comparision_pose_estimate.png")
    

#main function
def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    strip_optimizer(opt.device,opt.poseweights)
    main(opt)
