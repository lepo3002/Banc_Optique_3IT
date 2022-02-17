from skimage import measure


def crop(image):
    contours = measure.find_contours(image, fully_connected='high')
    contour = sorted(contours, key=lambda x: image.shape[0])[-1]
    # contour = contours[0]
    xmax, ymax = contour.max(axis=0).astype(int)
    xmin, ymin = contour.min(axis=0).astype(int)
    region = image[xmin:xmax, ymin:ymax]
    return region

