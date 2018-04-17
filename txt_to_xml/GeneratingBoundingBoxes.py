import sys

sys.path.pop(2)
import cv2
import time
from os import listdir

clicked = False
buttonDown_x = 0
buttonDown_y = 0
buttonUp_x = 0
buttonUp_y = 0
lineData = ""
counter = 0
path = "/home/conrad/PyCharmProjects/Gifspuitwork/sunflowerimages"
currentPath = ""
files = [f for f in listdir(path)]


# set mouse call back function to note down the bounding box coordinates
def onMouse(event, x, y, flags, para):
    global clicked
    global buttonDown_x
    global buttonDown_y
    global buttonUp_x
    global buttonUp_y
    if event:
        print("*********")
    # mouse must drag from the upper left corner to lower right corner
    if event == cv2.EVENT_LBUTTONDOWN:
        buttonDown_x = x
        buttonDown_y = y
    if event == cv2.EVENT_LBUTTONUP:
        buttonUp_x = x
        buttonUp_y = y
        clicked = True
        print((buttonDown_x, buttonDown_y), (buttonUp_x, buttonUp_y))
        global counter
        global currentPath
        counter += 1
        # write the bounding box and label information to new file
        with open("/home/conrad/PyCharmProjects/Gifspuitwork/sunflowertxts/" + str(counter).zfill(10) + ".txt", "w") as dataFile:
            dataFile.write(" ".join(
                [currentPath, "shoue", str(buttonDown_x), str(buttonDown_y), str(buttonUp_x), str(buttonUp_y)]))


def mark_image(data_path):
    global clicked
    cv2.namedWindow(data_path)
    cv2.setMouseCallback(data_path, onMouse)
    image = cv2.imread(data_path)
    print("image path: ", data_path)
    cv2.imshow(data_path, image)
    cv2.waitKey(0)
    cv2.destroyWindow(data_path)


def getNextImage():
    global files
    global path
    if len(files) == 0:
        return None
    current = files.pop(0)
    print
    path + current
    return path + "/" + current


if __name__ == "__main__":
    while True:
        current = getNextImage()
        if current != None:
            global currentPath
            currentPath = current
            mark_image(current)
        else:
            print("finish")
            break