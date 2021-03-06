import os
import imageio
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt


def format_and_render_plot():
    fig = plt.gcf()
    for ax in fig.axes:
        ax.legend(loc='center right')
        ax.axis('off')
    plt.show()


############# works for 2 D images
path3 = 'C:\\Users\\Public\\Pictures\\Sample Pictures\\foot.jpg'
path2 = 'C:\\Users\\Public\\Pictures\\Sample Pictures\\Hydrangeas.jpg'
path = "C:\\Users\\Jose\\Pictures\\Public\\images3.jpg"
im = imageio.imread(path)

skinMask = (im >= 45) & (im < 145)
boneMask = im >= 45
bones = np.where(boneMask, im, 0)
skin = np.where(skinMask, im, 0)


# bonedilate = ndi.binary_dilation(boneMask, iterations=5)
# boneclosed = ndi.binary_closing(boneMask, iterations=5)

plt.imshow(bones, cmap='gray')
plt.axis('off')
plt.show()


# fig, axes = plt.subplots(1, 3)
# axes[0].imshow(bones)
# axes[1].imshow(bonedilate)
# axes[2].imshow(boneclosed)
# format_and_render_plot()


plt.imshow(skin, cmap='gray')
plt.axis('off')
plt.show()

plt.imshow(im[:,:,0])
plt.axis('off')
plt.show()

im = im[:, :, 0]
weights = [[[0.235, 0.235, 0.235, 0.235, 0.235, 0.235],
            [0.235, 0.235, 0.235, 0.235, 0.235, 0.235],
            [0.235, 0.235, 0.235, 0.235, 0.235, 0.235],
            [0.235, 0.235, 0.235, 0.235, 0.235, 0.235],
            [0.235, 0.235, 0.235, 0.235, 0.235, 0.235]],
           [[0.235, 0.235, 0.235, 0.235, 0.235, 0.235],
            [0.235, 0.235, 0.235, 0.235, 0.235, 0.235],
            [0.235, 0.235, 0.235, 0.235, 0.235, 0.235],
            [0.235, 0.235, 0.235, 0.235, 0.235, 0.235],
            [0.235, 0.235, 0.235, 0.235, 0.235, 0.235]]]

weights = [[0.234,  0.234],
           [0.234,  0.234],
           [0.234,  0.234],
           [0.234,  0.234]]


# Convolve the image with the filter
im_filt = ndi.convolve(im, weights)

# Plot the images
fig, axes = plt.subplots(1, 2)
axes[0].imshow(im)
axes[1].imshow(im_filt)
format_and_render_plot()

hist = ndi.histogram(bones, min=0, max=255, bins=256)

print(hist.shape)
plt.plot(hist)
plt.show()


cdf = hist.cumsum() / hist.sum()
plt.plot(cdf)
plt.show()

Im_equal = cdf[bones] * 255

print('#######################')
print(im.shape)
print(Im_equal.shape)


fig, axs = plt.subplots(2, 1)
plt.axis('off')
axs[0].imshow(im)
axs[1].imshow(Im_equal)
plt.show()



############ On the second Image
im = plt.imread(path)

# Flatten the image into 1 dimension: pixels
pixels = im.flatten()

# Generate a cumulative histogram
cdf, bins, patches = plt.hist(pixels, bins=256, range=(
    0, 256), density=True, cumulative=True)
new_pixels = np.interp(pixels, bins[:-1], cdf*255)

new_image = new_pixels.reshape(im.shape).astype(int)

# Display the new image 
fig, axs = plt.subplots(1, 2)
axs[0].set_title('Original Image')
axs[0].imshow(im)
axs[1].imshow(new_image)
axs[1].set_title('Equalized Image')
axs[1].axis('off')
axs[0].axis('off')
plt.show()





################# 
im = imageio.imread(path)
print('Data type:', im.dtype)
print('Min. value:', im.min())
print('Max value:', im.max())
print(im.shape)

# Plot the grayscale image
plt.imshow(im, vmin=0, vmax=255)
plt.colorbar()
plt.show()


# Generate histogram
hist = ndi.histogram(im, min=0, max=255, bins=256)

# Calculate cumulative distribution
cdf = hist.cumsum() / hist.sum()

# Plot the histogram and CDF
fig, axes = plt.subplots(2, 1, sharex=True)
axes[0].plot(hist, label='Histogram')
axes[1].plot(cdf, label='CDF')
format_and_render_plot()


# Screen out non-bone pixels from "im"
mask_skin = (im >= 45) & (im < 145)
mask_bone = im >= 145
im_bone = np.where(mask_bone, im, 0)
mask_skin = np.where(mask_skin, im, 0)

# Get the histogram of bone intensities
hist = ndi.histogram(mask_skin, min=1, max=255, bins=255)

# Plot masked image and histogram
fig, axes = plt.subplots(2, 1)
axes[0].imshow(im_bone)
axes[1].plot(hist)
format_and_render_plot()


# Apply Sobel filter along both axes
im = im[:,:,1]
print(im.shape)
sobel_ax0 = ndi.sobel(im, axis=0)
sobel_ax1 = ndi.sobel(im, axis=1)


weights = [[+1, 0, -1], [+1, 0, -1], [+1, 0, -1]]

edges = ndi.convolve(im, weights)
# Calculate edge magnitude 
# edges =  np.sqrt(np.square(sobel_ax0) + np.square(sobel_ax1))

# Plot edge magnitude
plt.imshow(edges, cmap='gray')
plt.colorbar()
format_and_render_plot()
