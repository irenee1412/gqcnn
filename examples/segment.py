# import 
import cv2 
from perception import ColorImage, BinaryImage
import os

# parameters, change them, test and optimize for your use case
BINARY_IM_MAX_VAL = np.iinfo(np.uint8).max
BINARY_IM_DEFAULT_THRESH = BINARY_IM_MAX_VAL / 2
LOW_GRAY = 70
UPPER_GRAY = 250
AREA_THRESH_DEFAULT = 1000  
DIST_THRESH_DEFAULT = 20
FRAME = 'name_of_your_rgbd_camera_' # in my case is realsense_overhead

def binary_segmask(image, background, output_dir, filename):
    """
    Create a binary image from the color image 
    :param image: rgb image created with RGBD camera 
    :param background: path to background image to use 
    :param output_dir: path to output dir for processed images
    :param filename: name for saving data
    :return: binary_subtract_pruned
    """

    background1 = cv2.imread(background)
    background = background1.resize((,))
    # convert img to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    # subtract foreground from background
    subtract = background_gray - gray
    # in range for grayscale values
    subtract_im_filtered = cv2.inRange(subtract, LOW_GRAY, UPPER_GRAY)
    # open as ColorImage
    subtract_im_filt = ColorImage(subtract_im_filtered, FRAME)  
    # convert to BinaryImage
    binary_subtract = subtract_im_filt.to_binary(threshold=BINARY_IM_DEFAULT_THRESH)
    # Prune contours
    binary_subtract_pruned = binary_subtract.prune_contours(area_thresh=AREA_THRESH_DEFAULT, dist_thresh=DIST_THRESH_DEFAULT)
    # save binary to npy and png format
    np.save('%s/%s_binary.npy' % (output_dir, filename), binary_subtract_pruned._image_data())
    cv2.imwrite('%s/%s_binary.png' % (output_dir, filename), binary_subtract_pruned._image_data())
    return binary_subtract_pruned

if __name__ == "__main__":
    
    image = cv2.imread()
    output_dir = 'define file adress'
    filename = segment
    
    binary_segmask()
