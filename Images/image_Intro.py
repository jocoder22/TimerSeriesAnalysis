import os
import imageio
import visvis as vv
import matplotlib.pyplot as plt


im = imageio.imread('imageio:chelsea.png')
vv.imshow(im)


im = imageio.imread('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjpZ6-hb3L0awMVteZtZY9aEUDEK73ozF511Byna2QY7a5QJ69xw')
im2 = imageio.imread('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUt-xUUhv0lxyBzTJP7uJj97cYZXVrgC3ebxIMP849vMGqA7z4')

plt.imshow(im)
plt.axis('off')
plt.show()

plt.imshow(im2)
plt.axis('off')
plt.show()

print(im.shape, im.meta)

# vol = imageio.volread('imageio:stent.npz')
# vv.volshow(vol)

# for ii in range(vol.shape[0]):
#     plt.imshow(vol[:, :, ii])
#     plt.axis('off')
#     plt.pause(0.01)

# print(vol.shape, vol.meta.keys())