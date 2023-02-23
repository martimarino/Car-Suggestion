import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import cv2
from emonet.models import EmoNet

net = EmoNet(n_expression=5).to('cpu')
img = cv2.imread('./image.jpg')
(h, w, c) = img.shape[:3]
# display the image width, height, and number of channels to our
# terminal
print("width: {} pixels".format(w))
print("height: {}  pixels".format(h))
print("channels: {}".format(c))
net(img)