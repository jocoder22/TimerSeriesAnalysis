import os
import imageio
import visvis as vv
import matplotlib.pyplot as plt

im = imageio.imread('imageio:chelsea.png')
# vv.imshow(im)
plt.imshow(im)
plt.axis('off')
plt.show()

print(im.shape, im.meta)

vol = imageio.volread('imageio:stent.npz')
# vv.volshow(vol)

for ii in range(vol.shape[0]):
    plt.imshow(vol[:, :, ii])
    plt.axis('off')
    plt.pause(0.01)

print(vol.shape, vol.meta.keys())