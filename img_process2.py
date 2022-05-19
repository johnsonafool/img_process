import os
import json
from fsspec import filesystem
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from skimage.io import imread, imshow
from skimage.color import label2rgb
from yaml import load


# img_dir = "/Users/johnson/Desktop/img_process/train_anno_jpg"
# json_dir = "/Users/johnson/Desktop/img_process/json"

# img_path = "/Users/johnson/Desktop/img_process/train_anno_jpg/00000000.jpg"
# json_path = "/Users/johnson/Desktop/img_process/json/00000001.json"

out_img = ""
out_seg = ""
out_overlap = ""
out_overview = ""


def create_mask(img, js):
    # img_path = img_path
    # json_path = json_path
    img = imread(img, plugin='pil')[:,:,:3]

    # Conversion dimension of image create mask same size
    y_max = img.shape[0]
    x_max = img.shape[1]

    # Open the mask file
    read_file = open(js, "r")
    data = json.load(read_file)

    # Add each polygon to list
    shapes = data['shapes']
    polys = []
    for index in range(shapes.__len__()):
        points = np.array(shapes[index]['points']).astype(int)
        polys.append(points)

    # "Draw" the polygons
    msk = Image.new('L', (x_max, y_max), 0)  # (w, h)
    for i in range(len(polys)):
        pol = polys[i]
        pol = [tuple(l) for l in pol]
        ImageDraw.Draw(msk).polygon((pol), outline=1, fill=1)

    mask = np.array(msk)

    # Visualize
    fig, ax = plt.subplots(1,3, figsize=(12,4), dpi=400)
    ax[0].set_title('Raw image')
    ax[0].imshow(img)
    ax[1].set_title('Segmentation')
    ax[1].imshow(mask)
    ax[2].set_title('Groundtruth')
    ax[2].imshow(label2rgb(mask>0, img, bg_label = 0))
    
    # out = fig.savefig()
    return fig

# create_mask("/Users/johnson/Desktop/img_process/train_anno_jpg/00000000.jpg", "/Users/johnson/Desktop/img_process/json/00000001.json")


def load_file():

    ROOT = os.getcwd()
    
    imgs_dir = os.path.join(ROOT, "train_anno_jpg")
    imgs =  os.listdir(imgs_dir)

    jsons_dir = os.path.join(ROOT, "json")
    jsons =  os.listdir(jsons_dir)
    
    def last_chars(x):
        return(x[-6:])
    
    img_ls = []
    for img in sorted(imgs, key = last_chars):    
        # return(os.path.join(imgs_dir, img))
        img_ls.append(os.path.join(imgs_dir, img))

    json_ls = []
    for json in sorted(jsons, key = last_chars):    
        # return(os.path.join(jsons_dir, json))
        json_ls.append(os.path.join(jsons_dir, json))


    img_with_json = dict([[y,json_ls[x]] for x,y in enumerate(img_ls)])

    for i, j in img_with_json.items():
        outdir = os.path.join(ROOT, "output")
        fig = create_mask(i, j)
        return fig
        # plt.savefig('0'+i)
        # print(i)
        # print(j)
        

    # with open(img,'rb') as thefile:
    #     create_mask() 

load_file()




# def load_file():
#     ROOT = os.getcwd()
#     #go to different folder
#     imgs = os.path.join(ROOT, "train_anno_jpg")
#     file_list =  os.listdir(imgs):
    
#     def last_4chars(x):
#         return(x[-4:])

#     sorted(file_list, key = last_4chars)   
    # iteration of files in folder
    # for file in os.listdir(dir):
    #     files = os.path.join(dir, file)

    # return files

# load_file()

# class image_process():
