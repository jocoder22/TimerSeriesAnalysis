#!/usr/bin/env python
import os
import visvis as vv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio as img 
import scipy.ndimage as ndi


path = 'C:\\Users\\Public\\Pictures\\Sample Pictures\\video2.mp4'


reader = img.get_reader(path)

# path2 = 'C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis\\Images'
# os.chdir(path2)
# for i, im in enumerate(reader):
#     print('Mean of frame %i is %1.1f' % (i, im.mean()))
#     if i == 0 or i == 29:
#         plt.imsave("frame_2{}.jpg".format(i), im, cmap='gray')


# im = img.imread('frame_20.jpg')
# print(im.dtype)
# print(im.shape)
# plt.imshow(im)
# plt.show()
# print('#############')
# print(type(im))

# print(im.meta.dpi)

# imt = im[:,:,1]
# print(imt.min())
# print(imt.max())
# imgfilter = ndi.gaussian_filter(imt, sigma=1)
# maskselect = np.where(imgfilter > 150, 1, 0)
# mask = ndi.binary_closing(maskselect)


# # Objects labels
# labels, nlabels = ndi.label(mask)
# print(f'number of lables  = {nlabels}')
# nnlabel = np.arange(1, nlabels+1)
# print(ndi.labeled_comprehension(imt, labels, nnlabel, ndi.mean,
#                                 float, True))


# hist1 = ndi.histogram(imt, 0, 255, 256, labels=labels , index=[4, 5, 6])
# print(len(hist1))


# # Plot the hist, if near normally distributed, the segmentation is doing well
# plt.plot(hist1[0], label="Other Area")
# plt.plot(hist1[1], label="Left Ventricle")
# plt.plot(hist1[2], label="Right Ventricle")
# plt.legend()
# plt.show()

# # select specific pixel: left ventricular pixel
# lv = labels[500, 700]
# print(lv)
# lvMask = np.where(labels == lv, imt, 0)




# hist = ndi.histogram(imt, min=0, max=255, bins=256)

# print(len(hist))

# # Create boxes
# boxes = ndi.find_objects(labels)
# print(boxes[5])
# plt.imshow(imt[boxes[5]])
# plt.show()

# # show all the labels, the different portions
# plt.imshow(labels, cmap='rainbow')
# plt.show()


# # Create lf ventricular box and display it
# lvMask2 = np.where(labels == lv, 1, 0)
# lvbox = ndi.find_objects(lvMask2)
# boxes_lv = imt[lvbox[0]]
# plt.imshow(boxes_lv, cmap='rainbow')
# plt.show()



# # Overlay the left venticular area
# cent = ndi.center_of_mass(imt, labels, index=5)
# plt.imshow(lvMask, cmap='rainbow')
# plt.imshow(imt, cmap='gray')
# plt.scatter(cent[1], cent[0])
# plt.show()

# for i in range(nlabels):
#     lvMask = np.where(labels == i, imt, 0)
#     # plt.imshow(imt, cmap='gray')
#     plt.imshow(lvMask, cmap='rainbow')
#     plt.title(f'this is for number {i}')
#     plt.show()





reader2 = img.get_reader(path)
t = vv.imshow(reader2.get_next_data(), clim=(0, 255))
for im in reader2:
    # vv.processEvents()
    plt.imshow(im)
    plt.pause(0.2)
    t.SetData(im)
