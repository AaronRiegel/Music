from PIL import Image

#file = 'TheEntertainer.jpg'

def convertImage(file):
    '''
    Uses PIL to convert a file to png type
    '''

    if(file[-3:] == "png"):
        im = Image.open(file)
        im.save('out.png')
        return im
        print('File {} already a png'.format(file))
    else:

        try:
            im = Image.open(file)
            print("Opening file: ", file)
        except:
            print("Error: Cannot convert image", file)

        rgb_im = im.convert('RGB')
        rgb_im.save('out.png')
        return rgb_im



