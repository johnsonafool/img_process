import os

 
def load_file():

    ROOT = os.getcwd()
    
    imgs_dir = os.path.join(ROOT, "img")
    imgs =  os.listdir(imgs_dir)

    jsons_dir = os.path.join(ROOT, "mask_json")
    jsons =  os.listdir(jsons_dir)
    
    def last_chars(x):
        return(x[-9:])
    
    img_ls = []
    for img in sorted(imgs, key = last_chars):    
        img_ls.append(os.path.join(imgs_dir, img))

    json_ls = []
    for json in sorted(jsons, key = last_chars):    
        json_ls.append(os.path.join(jsons_dir, json))


    img_with_json = dict([[y,json_ls[x]] for x,y in enumerate(img_ls)])

    for i, j in img_with_json.items():        
        print(f'{i}\t{j}\t\n', file=open("test.txt", "a"))


load_file()