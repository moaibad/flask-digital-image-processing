import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math
from collections import Counter
import cv2
from skimage import io
import os
import shutil


def grayscale():
    img = Image.open("static/img/img_now.jpg")

    if is_grey_scale("static/img/img_now.jpg"):
        return
    else:
        img_arr = np.asarray(img)
        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]
        new_arr = r.astype(int) + g.astype(int) + b.astype(int)
        new_arr = (new_arr/3).astype('uint8')
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")



def is_grey_scale(img_path):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True


def zoomin():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    new_size = ((img_arr.shape[0] * 2),
                (img_arr.shape[1] * 2), img_arr.shape[2])
    new_arr = np.full(new_size, 255)
    new_arr.setflags(write=1)

    r = img_arr[:, :, 0]
    g = img_arr[:, :, 1]
    b = img_arr[:, :, 2]

    new_r = []
    new_g = []
    new_b = []

    for row in range(len(r)):
        temp_r = []
        temp_g = []
        temp_b = []
        for i in r[row]:
            temp_r.extend([i, i])
        for j in g[row]:
            temp_g.extend([j, j])
        for k in b[row]:
            temp_b.extend([k, k])
        for _ in (0, 1):
            new_r.append(temp_r)
            new_g.append(temp_g)
            new_b.append(temp_b)

    for i in range(len(new_arr)):
        for j in range(len(new_arr[i])):
            new_arr[i, j, 0] = new_r[i][j]
            new_arr[i, j, 1] = new_g[i][j]
            new_arr[i, j, 2] = new_b[i][j]

    new_arr = new_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def zoomout():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    x, y = img.size
    new_arr = Image.new("RGB", (int(x / 2), int(y / 2)))
    r = [0, 0, 0, 0]
    g = [0, 0, 0, 0]
    b = [0, 0, 0, 0]

    for i in range(0, int(x/2)):
        for j in range(0, int(y/2)):
            r[0], g[0], b[0] = img.getpixel((2 * i, 2 * j))
            r[1], g[1], b[1] = img.getpixel((2 * i + 1, 2 * j))
            r[2], g[2], b[2] = img.getpixel((2 * i, 2 * j + 1))
            r[3], g[3], b[3] = img.getpixel((2 * i + 1, 2 * j + 1))
            new_arr.putpixel((int(i), int(j)), (int((r[0] + r[1] + r[2] + r[3]) / 4), int(
                (g[0] + g[1] + g[2] + g[3]) / 4), int((b[0] + b[1] + b[2] + b[3]) / 4)))
    new_arr = np.uint8(new_arr)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_left():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (0, 50)), 'constant')[:, 50:]
    g = np.pad(g, ((0, 0), (0, 50)), 'constant')[:, 50:]
    b = np.pad(b, ((0, 0), (0, 50)), 'constant')[:, 50:]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_right():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (50, 0)), 'constant')[:, :-50]
    g = np.pad(g, ((0, 0), (50, 0)), 'constant')[:, :-50]
    b = np.pad(b, ((0, 0), (50, 0)), 'constant')[:, :-50]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_up():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 50), (0, 0)), 'constant')[50:, :]
    g = np.pad(g, ((0, 50), (0, 0)), 'constant')[50:, :]
    b = np.pad(b, ((0, 50), (0, 0)), 'constant')[50:, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_down():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    g = np.pad(g, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    b = np.pad(b, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_addition():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img).astype('uint16')
    img_arr = img_arr+100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_substraction():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img).astype('int16')
    img_arr = img_arr-100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_multiplication():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    img_arr = img_arr*1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_division():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    img_arr = img_arr/1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def convolution(img, kernel):
    h_img, w_img, _ = img.shape
    out = np.zeros((h_img-2, w_img-2), dtype=float)
    new_img = np.zeros((h_img-2, w_img-2, 3))
    if np.array_equal((img[:, :, 1], img[:, :, 0]), img[:, :, 2]) == True:
        array = img[:, :, 0]
        for h in range(h_img-2):
            for w in range(w_img-2):
                S = np.multiply(array[h:h+3, w:w+3], kernel)
                out[h, w] = np.sum(S)
        out_ = np.clip(out, 0, 255)
        for channel in range(3):
            new_img[:, :, channel] = out_
    else:
        for channel in range(3):
            array = img[:, :, channel]
            for h in range(h_img-2):
                for w in range(w_img-2):
                    S = np.multiply(array[h:h+3, w:w+3], kernel)
                    out[h, w] = np.sum(S)
            out_ = np.clip(out, 0, 255)
            new_img[:, :, channel] = out_
    new_img = np.uint8(new_img)
    return new_img


def edge_detection():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=int)
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def blur():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=int)
    kernel = np.array(
        [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def histogram_rgb():
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr.flatten()
        data_g = Counter(g)
        plt.bar(list(data_g.keys()), data_g.values(), color='black')
        plt.savefig(f'static/img/grey_histogram.jpg', dpi=300)
        plt.clf()
    else:
        r = img_arr[:, :, 0].flatten()
        g = img_arr[:, :, 1].flatten()
        b = img_arr[:, :, 2].flatten()
        data_r = Counter(r)
        data_g = Counter(g)
        data_b = Counter(b)
        data_rgb = [data_r, data_g, data_b]
        warna = ['red', 'green', 'blue']
        data_hist = list(zip(warna, data_rgb))
        for data in data_hist:
            plt.bar(list(data[1].keys()), data[1].values(), color=f'{data[0]}')
            plt.savefig(f'static/img/{data[0]}_histogram.jpg', dpi=300)
            plt.clf()


def df(img):  # to make a histogram (count distribution frequency)
    values = [0]*256
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            values[img[i, j]] += 1
    return values


def cdf(hist):  # cumulative distribution frequency
    cdf = [0] * len(hist)  # len(hist) is 256
    cdf[0] = hist[0]
    for i in range(1, len(hist)):
        cdf[i] = cdf[i-1]+hist[i]
    # Now we normalize the histogram
    # What your function h was doing before
    cdf = [ele*255/cdf[-1] for ele in cdf]
    return cdf


def histogram_equalizer():
    img = cv2.imread('static\img\img_now.jpg', 0)
    my_cdf = cdf(df(img))
    # use linear interpolation of cdf to find new pixel values. Scipy alternative exists
    image_equalized = np.interp(img, range(0, 256), my_cdf)
    cv2.imwrite('static/img/img_now.jpg', image_equalized)


def threshold(lower_thres, upper_thres):
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)

    # Check if the array is read-only, and if so, make it writable
    if not img_arr.flags.writeable:
        img_arr = img_arr.copy()

    condition = np.logical_and(np.greater_equal(img_arr, lower_thres),
                               np.less_equal(img_arr, upper_thres))
    print(lower_thres, upper_thres)
    img_arr.setflags(write=1)
    img_arr[condition] = 255
    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_now.jpg")


def crop_normal(n):
    # Load the image
    image = cv2.imread('static/img/img_normal.jpg')


    # Get the dimensions of the image
    height, width, _ = image.shape

    # Calculate the size of each tile
    tile_height = height // n
    tile_width = width // n

    # Define the output directory
    output_directory = 'static/img/tiles/'

    # Check if the directory exists, and if it does, remove it
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

        # Create the output directory
        os.makedirs(output_directory)

    # Initialize a list to store the tiles
    tiles = []

    # Iterate through the image and crop it into tiles
    for i in range(n):
        for j in range(n):
            # Calculate the coordinates for cropping
            y1 = i * tile_height
            y2 = (i + 1) * tile_height
            x1 = j * tile_width
            x2 = (j + 1) * tile_width

            # Crop the tile from the image
            tile = image[y1:y2, x1:x2]

            # Save the tile
            tile_filename = os.path.join(output_directory, f'tile_{i * n + j + 1}.jpg')
            cv2.imwrite(tile_filename, tile)


def get_image_rgb(image_path):
    try:
        with Image.open(image_path) as img:
            rgb_values = list(img.getdata())
            return rgb_values
    except Exception as e:
        return None

def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except Exception as e:
        return None
    

#================================================================================================#

def identity_kernel():
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    kernel = np.array([[0, 0, 0],
                   [0, 1, 0],
                   [0, 0, 0]])
    identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    cv2.imwrite("static/img/img_now.jpg", identity)

def sharpening():
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
    sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    cv2.imwrite("static/img/img_now.jpg", sharp)

def bilateral_filter():
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    bf = cv2.bilateralFilter(src=image,d=9,sigmaColor=75,sigmaSpace=75)
    cv2.imwrite("static/img/img_now.jpg", bf)

def zero_padding():
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    zero_padding = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    cv2.imwrite("static/img/img_now.jpg", zero_padding)

def low_pass_filter(ksize):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    
    lowFilter = np.ones((ksize,ksize),np.float32)/9
    lowFilterImage = cv2.filter2D(image,-1,lowFilter)
    cv2.imwrite("static/img/img_now.jpg", lowFilterImage)

def high_pass_filter(ksize):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)

    lowFilter = np.ones((ksize, ksize), np.float32) / (ksize * ksize)
    lowFilterImage = cv2.filter2D(image, -1, lowFilter)
    
    highPassImage = image - lowFilterImage
    cv2.imwrite("static/img/img_now.jpg", highPassImage)

def band_pass_filter(ksize_low, ksize_high):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    
    lowFilter = np.ones((ksize_low, ksize_low), np.float32) / (ksize_low * ksize_low)
    lowFilterImage = cv2.filter2D(image, -1, lowFilter)
    highFilter = np.ones((ksize_high, ksize_high), np.float32) / (ksize_high * ksize_high)
    highPassImage = image - cv2.filter2D(lowFilterImage, -1, highFilter)
    
    cv2.imwrite("static/img/img_now.jpg", highPassImage)

def blur_filter(ksize):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    cv_blur = cv2.blur(src=image, ksize=(ksize,ksize))
    cv2.imwrite("static/img/img_now.jpg", cv_blur)

def mean_filter(ksize):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    kernel = np.ones((ksize, ksize), np.float32) / 9
    blur = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    cv2.imwrite("static/img/img_now.jpg", blur)

def median_blur(ksize):
    image = cv2.imread("static/img/img_now.jpg")
    cv_median = cv2.medianBlur(image, ksize)
    cv2.imwrite("static/img/img_now.jpg", cv_median)

def gaussian_blur(ksize):
    image = cv2.imread("static/img/img_now.jpg")
    cv_gaussian = cv2.GaussianBlur(image, (ksize, ksize), 0)
    cv2.imwrite("static/img/img_now.jpg", cv_gaussian)
    
def game():
    image = cv2.imread("static/img/img_normal.jpg")

    # ================== Greyscale ==================
    if is_grey_scale("static/img/img_normal.jpg"):
        return
    else:
        img_arr = np.asarray(image)
        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]
        new_arr = r.astype(int) + g.astype(int) + b.astype(int)
        new_arr = (new_arr/3).astype('uint8')
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/cocoki/greyscale.jpg")

    # ================== Move Left ==================
    img_arr = np.asarray(image)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (0, 50)), 'constant')[:, 50:]
    g = np.pad(g, ((0, 0), (0, 50)), 'constant')[:, 50:]
    b = np.pad(b, ((0, 0), (0, 50)), 'constant')[:, 50:]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/cocoki/image_left.jpg")

    # ================== Move Right ==================
    img_arr = np.asarray(image)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (50, 0)), 'constant')[:, :-50]
    g = np.pad(g, ((0, 0), (50, 0)), 'constant')[:, :-50]
    b = np.pad(b, ((0, 0), (50, 0)), 'constant')[:, :-50]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/cocoki/image_right.jpg")

    # ================== Move Up ==================
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(image)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 50), (0, 0)), 'constant')[50:, :]
    g = np.pad(g, ((0, 50), (0, 0)), 'constant')[50:, :]
    b = np.pad(b, ((0, 50), (0, 0)), 'constant')[50:, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/cocoki/image_up.jpg")


    # ================== Move Down ==================
    img_arr = np.asarray(image)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    g = np.pad(g, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    b = np.pad(b, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/cocoki/image_down.jpg")


    # ================== Median Filter ==================
    cv_median = cv2.medianBlur(image, 9)
    cv2.imwrite("static/img/cocoki/median.jpg", cv_median)

    # ================== Edge Detection ==================
    img_arr = np.asarray(image, dtype=int)
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/cocoki/edge_detection.jpg")

    # ================== Sharpening ==================
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
    sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    cv2.imwrite("static/img/cocoki/sharpening.jpg", sharp)

    # ================== Low Pass Filter ==================
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    lowFilter = np.ones((5,5),np.float32)/9
    lowFilterImage = cv2.filter2D(image,-1,lowFilter)
    cv2.imwrite("static/img/cocoki/low_pass.jpg", lowFilterImage)

    # ================== Band Pass Filter ==================
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    
    lowFilter = np.ones((3, 3), np.float32) / (3 * 3)
    lowFilterImage = cv2.filter2D(image, -1, lowFilter)
    highFilter = np.ones((5, 5), np.float32) / (5 * 5)
    highPassImage = image - cv2.filter2D(lowFilterImage, -1, highFilter)
    cv2.imwrite("static/img/cocoki/band_pass.jpg", highPassImage)


    # brightness_addition():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img).astype('uint16')
    img_arr = img_arr+100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/cocoki/brightness_addition.jpg")


    # brightness_substraction():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img).astype('int16')
    img_arr = img_arr-100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/cocoki/brightness_substraction.jpg")


    # brightness_multiplication():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    img_arr = img_arr*1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/cocoki/brightness_multiplication.jpg")


    # brightness_division():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    img_arr = img_arr/1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/cocoki/brightness_division.jpg")