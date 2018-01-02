import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image, ImageChops

update = False

def threshold(thres, img):
    lim = img.convert('L')
    table = []
    for i in range(256):
        if i < thres:
            table.append(0)
        else:
            table.append(1)
    bim = lim.point(table, "1")
    return bim

def pull_screenshot():
    """
    docstring here
    """
    for n in range(1, 100):
        if (not os.path.exists("%d.png" % (n))):
            name = "%d.png" % (n)
            os.system('adb shell screencap -p /sdcard/%s' % name)
            os.system('adb pull /sdcard/%s .' % name)
            return name
    return

def crop(img):
    """

    """
    #(shotname, extension) = os.path.splitext(filename)
    # 第一幅图
    img1 = img.crop((200, 100, 1020, 920))
    #img1.save(shotname + '_1' + extension)

    # 第二幅图
    img2 = img.crop((200, 1000, 1020, 1820))
    #img2.save(shotname + '_2' + extension)

    img3 = ImageChops.difference(img1, img2)
    #img3.show()
    img4 = threshold(10, img3)
    img.paste(img4, (200, 100, 1020, 920))
    #img.show()
    #plt.imshow(img)
    #plt.axvline(200)
    #imfigure.set_array(np.array(img))

def on_key_press(event):
    global update
    update = True

def tap(x, y):
    cmd = 'adb shell input tap ' + str(x) + ' ' + str(y)
    print(cmd)
    os.system(cmd)

def onClick(event):
    ix, iy = event.xdata, event.ydata
    tap(ix, iy)
    return

def updatefig(*args):
    global update
    if update:
        imgname = pull_screenshot()
        img = Image.open(imgname)
        crop(img)
        imfigure.set_array(np.array(img))
        update = False
    return imfigure,

savefilename = '1.png'
img = Image.open(savefilename)

fig = plt.figure()
imfigure = plt.imshow(img, animated=True)

fig.canvas.mpl_connect('button_press_event', onClick)
fig.canvas.mpl_connect('key_press_event', on_key_press)
ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()
