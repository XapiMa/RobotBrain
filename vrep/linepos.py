import cv2
import numpy as np




def linepos(img, ya, yb, thd):
    image = img.copy()
    yoko_a = image[ya, :]
    yoko_b = image[yb, :]

    xmax = image.shape[1]
    xmid = xmax/2
    #print xmax, xmid
    
    if np.max(yoko_a[0:xmid])<thd:
        xa1 = -1
    else:
        xa1 = np.argmax(yoko_a[0:xmid])

    if np.max(yoko_a[xmid:xmax])<thd:
        xa2 = -1
    else:
        xa2 = np.argmax(yoko_a[xmid:xmax])+xmid

    if np.max(yoko_b[0:xmid])<thd:
        xb1 = -1
    else:
        xb1 = np.argmax(yoko_b[0:xmid])
    
    if np.max(yoko_b[xmid:xmax])<thd:
        xb2 = -1
    else:
        xb2 = np.argmax(yoko_b[xmid:xmax])+xmid
        
    #draw line
    cv2.line(image, (0,ya), (xmax,ya), 100, 2)
    cv2.line(image, (0,yb), (xmax,yb), 100, 2)
    

    if xa1!=-1:
        cv2.circle(image,(xa1,ya), 10, 100, -1)
    if xa2!=-1:
        cv2.circle(image,(xa2,ya), 10, 100, -1)
    if xb1!=-1:
        cv2.circle(image,(xb1,yb), 10, 100, -1)
    if xb2!=-1: 
        cv2.circle(image,(xb2,yb), 10, 100, -1)
        
    return xa1, xa2, xb1, xb2, image


if __name__=='__main__':

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    
    while True:
        ret, frame = cap.read()
        
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        xa1, xa2, ya1, ya2, image = linepos(frame, 200, 300, 100)
        
        cv2.imshow('image', image)

        key = cv2.waitKey(10)
        if key == 27:
            break
        if key ==ord('s'):
            cv2.imwrite('image.png', image)

    cap.release()
    cv2.destroyAllWindows()