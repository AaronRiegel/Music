import cv2

class BoundingBox:

    def __init__(self, x1, y1,x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


    def show_box(self,img,x1,y1,x2,y2):
        print(f'Generating Bounding Box')
        cv2.imwrite('preimage.png',img)
        im2 = cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),thickness=1)

        cv2.imwrite('box.png', im2)

