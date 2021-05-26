import ffmpeg
import subprocess
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#for cropping and creating frames
video_rec = '/Users/rajireddy.annadi/Downloads/test3/video_rec.webm'
screen_rec = '/Users/rajireddy.annadi/Downloads/test3/screen_rec.webm'
# cmd = 'ffmpeg -y -i {} {} {}'.format(in_vid, encoding_opts2, out_vid)
# cmd = 'ffmpeg -i {} -vf fps=10 screen_frames/out%d.png'.format()
dir_path = os.path.dirname(os.path.abspath(video_rec))
print(dir_path)

cmd = 'mkdir {}/screen_frames'.format(dir_path)
subprocess.call(cmd, shell=True)
cmd = 'mkdir {}/video_frames'.format(dir_path)
subprocess.call(cmd, shell=True)

cmd = 'ffmpeg -i {} -filter:v "crop=317:238:2:3" {}/cropped_screen.webm'.format(screen_rec, dir_path)
subprocess.call(cmd, shell=True)
cropped_screen = dir_path + '/cropped_screen.webm'
cmd = 'ffmpeg -i {} -vf fps=30 {}/screen_frames/out%d.png'.format(cropped_screen, dir_path)
subprocess.call(cmd, shell=True)
cmd = 'ffmpeg -i {} -vf fps=30 {}/video_frames/out%d.png'.format(video_rec, dir_path)
subprocess.call(cmd, shell=True)
#creating frames code ends here
    
def normalize(a):
    return (a - min(a))/(np.std(a))

def NCC(src, dst):
    denA = 0
    denB = 0
    num = 0
    src = src - np.mean(src)
    dst = dst - np.mean(dst)

    num = np.multiply(src, dst)
    denA = np.multiply(src, src)
    denB = np.multiply(dst, dst)
    num = np.sum(np.sum(num))
    denA = np.sum(np.sum(denA))
    denB = np.sum(np.sum(denB))
    if ((np.sqrt(denA) * np.sqrt(denB)) == 0):
        return 0
    ncc = num / (np.sqrt(denA) * np.sqrt(denB))
    return ncc

# to check for one frame match
infile = '/Users/rajireddy.annadi/Downloads/test3/screen_frames/out1.png'
img = cv2.imread(infile, cv2.cv2.IMREAD_GRAYSCALE)
print(img.shape)
bigImgPath = '/Users/rajireddy.annadi/Downloads/test3/video_frames/out1218.png'
bigImg = cv2.imread(bigImgPath, cv2.cv2.IMREAD_GRAYSCALE)
width = img.shape[1]
height = img.shape[0]
dim = (width, height)

resized = cv2.resize(bigImg, dim, interpolation=cv2.INTER_AREA)
resized = cv2.flip(resized, 1)
resized = resized.ravel()
resized = normalize(resized)

print(resized.shape)
maxNCC  = 0
maxIndex = -1
for i in range(1, 1300):
    infile = '/Users/rajireddy.annadi/Downloads/test3/screen_frames/out' + str(i) + '.png'
    img = cv2.imread(infile, cv2.cv2.IMREAD_GRAYSCALE)
    img = img.ravel()
    img = normalize(img)
    temp = NCC(img, resized)
    if(temp > maxNCC):
        maxIndex = i
        maxNCC = temp

print(maxIndex)
print(maxNCC)
# to check for one frame match ends here

def getTime(image_num, fps):
    num_seconds = image_num//fps
    time_point = str(num_seconds//60) + ':' + str(num_seconds%60) + ':' + str(1000/30 * (image_num%fps))
    return time_point

def getDMMatrix(path, start, m, diff, flag, dim):
    ret = []
    for i in range(m):
        image_num = start + m * diff
        infile = path + '/out' + str(image_num) + '.png'
        img = cv2.imread(infile, cv2.cv2.IMREAD_GRAYSCALE)
        if(flag):
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img = img.ravel()
        img = normalize(img)
        ret.append(img)
    return ret

def getOffset(path1, path2, start, m, diff): #path2 is smaller images(screen cropped)
    infile = path2 + '/out1.png'
    img = cv2.imread(infile, cv2.cv2.IMREAD_GRAYSCALE)
    width = img.shape[1]
    height = img.shape[0]
    dim = (width, height)

    DMmatrix1 =  getDMMatrix(path1, start, m, diff, True,  dim)
    maxNCC = -1
    bestT = -np.inf
    for t in range(-399, 0):
        print(t)
        DMmatrix2 = getDMMatrix(path2, start + t, m, diff, False,  dim)
        ncc = NCC(DMmatrix1, DMmatrix2)
        if(ncc > maxNCC):
            maxNCC = ncc
            bestT = t
    print(bestT)
    print(maxNCC)
    print(abs(bestT))
# for getting offset between two videos
# getOffset('/Users/rajireddy.annadi/Downloads/test3/video_frames', '/Users/rajireddy.annadi/Downloads/test3/screen_frames', 400, 90 ,10)# 600 + 10 * 30







