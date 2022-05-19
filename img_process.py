import os 
import json 
import re 
import glob
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from skimage.io import imread, imshow
from skimage.color import label2rgb
from yaml import load


def main():

    
    def create_mask(img, js):
       
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

        fig, ax = plt.subplots(1,3, figsize=(12,4), dpi=400)
        ax[0].set_title('Raw image')
        ax[0].imshow(img)
        ax[1].set_title('Segmentation')
        ax[1].imshow(mask)
        ax[2].set_title('Groundtruth')
        ax[2].imshow(label2rgb(mask>0, img, bg_label = 1))
        
        # out = fig.savefig()
        return fig
        

    def load_file():

        ROOT = os.getcwd()
        
        imgs_dir = os.path.join(ROOT, "img")
        imgs =  os.listdir(imgs_dir)

        jsons_dir = os.path.join(ROOT, "mask_json")
        jsons =  os.listdir(jsons_dir)

        print(len(jsons))
        print(len(imgs))
        
        # def last_chars(x):
        #     return(x[-9:])
        
        # img_ls = []
        # for img in sorted(imgs, key = last_chars):    
        #     img_ls.append(os.path.join(imgs_dir, img))

        # json_ls = []
        # for json in sorted(jsons, key = last_chars):    
        #     json_ls.append(os.path.join(jsons_dir, json))


        # img_with_json = dict([[y,json_ls[x]] for x,y in enumerate(img_ls)])

        # for i, j in img_with_json.items():        
        #     # print(f'{i}\t{j}\t\n', file=open("test.txt", "a"))

        #     overview_dir = os.path.join(ROOT, "overview")
        #     fig = create_mask(i, j)
        #     res = re.findall("(\d+).jpg", i)
        #     # print(res[0]) 
        #     # return fig
        #     plt.savefig(os.path.join(overview_dir, res[0]))
            
        # # with open(img,'rb') as thefile:
        # #     create_mask() 

    load_file()


if __name__ == "__main__":
    main()