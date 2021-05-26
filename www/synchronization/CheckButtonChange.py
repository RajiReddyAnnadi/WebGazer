import ffmpeg
import subprocess
import os
from PIL import Image
#crop video to get button1.webm and extract frames as ./button_frames/out%d.png
screen = '/Users/rajireddy.annadi/Downloads/test/screen_rec.webm'
dir_path = os.path.dirname(os.path.abspath(screen))
print(dir_path)
cmd = 'ffmpeg -i {} -filter:v "crop=14:14:343:73" {}/button1.webm'.format(screen, dir_path)
subprocess.call(cmd, shell=True)

cmd = 'mkdir {}/button_frames'.format(dir_path)
subprocess.call(cmd, shell=True)
cmd = 'ffmpeg -i {}/button1.webm -vf fps=30 {}/button_frames/out%d.png'.format(dir_path, dir_path)
subprocess.call(cmd, shell=True)

def getTime(image_num, fps):
    num_seconds = image_num//fps
    time_point = str(num_seconds//60) + ':' + str(num_seconds%60) + ':' + str(1000/30 * (image_num%fps))
    return time_point

button_frames_dir = dir_path + '/button_frames/'
arr = os.listdir(button_frames_dir)
num_images = len(arr)

required_image = 0
for image_num in range(1, num_images + 1):
    im = Image.open(button_frames_dir+ 'out' + str(image_num) + '.png') # Can be many different formats.
    pix = im.load()
    print(image_num)
    print(pix[7,7])
    if(pix[7,7,][1] == 255):
        print(image_num)
        required_image = image_num
        break

print(getTime(required_image, 30))






