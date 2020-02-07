from os import listdir, makedirs, unlink
from os.path import isfile, join, dirname, abspath, exists
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

LOG_FILE = "log.txt"
MAX_COLLAGE_IMAGES = 4
SEP_LINE = "--------------------------\n"

BUFFER_PATH = join(dirname(abspath(__file__)), "buffer")

TEXT_OFFSET = 40
OUTLINE = 3
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONT = ImageFont.truetype("ubuntu700.ttf", 85)

WATERMARK_IMAGE = "watermark.png"
WATERMARK_OFFSET = 30

CANVAS_IMAGE = join(BUFFER_PATH, "canvas.png")
LOGO_IMAGE = "logo.png"
BORDER_SIZE = 15

COLLAGE_FOLDER = "kolaże"


def logMessage(message):
    print(message)
    try:
        file = open(LOG_FILE, "a+")
        file.write(message)
        file.close()
    except Exception as e:
        print("Unable to write " + LOG_FILE + "\n" + str(e))

def errorMessage(text, exception):
    message = "[ERROR] " + text + "\n" + str(exception)
    now = str(datetime.now())
    message = SEP_LINE + now + "\n" + message + "\n"
    logMessage(message)

# Raw image size 6016 x 4016
# Scaled image size 2000 x 1335
class PicSize:
    def __init__(self, long=0, short=0):
        self.LONG = 900
        self.SHORT = 601
        self.long = long
        self.short = short

    def isCorrect(self):
        if (self.long >= self.LONG) and (self.short >= self.SHORT):
            return True
        return False

class Picture:
    def __init__(self, location="", width=0, height=0):
        self.location = location
        self.width = width
        self.height = height


class ImageSelector:
    def __init__(self, rootFolder):
        self.rootFolder = rootFolder
        self.portraitCollagePictures = []
        self.landscapeCollagePictures = []

    def collagePicturesExist(self):
        if self.portraitExist() or self.landscapeExist():
            return True
        return False

    def portraitExist(self):
        if self.portraitCollagePictures:
            return True
        return False

    def landscapeExist(self):
        if self.landscapeCollagePictures:
            return True
        return False

    def createPictureList(self):

        imageFiles = self.getImageFiles()
        portraitImages = []
        landscapeImages = []

        for image in imageFiles:
            try:
                with Image.open(image) as img:
                    width, height = img.size

                    if width < height:
                        portraitImages.append(
                            Picture(image, width, height))
                    else:
                        landscapeImages.append(
                            Picture(image, width, height))
            except Exception as e:
                errorMessage("Unable to open " + image, e)

        self.portraitCollagePictures = self.assignCollagePictures(portraitImages)
        self.landscapeCollagePictures = self.assignCollagePictures(landscapeImages)

    def getImageFiles(self):
        files = [f for f in listdir(self.rootFolder) if isfile(join(self.rootFolder, f))]
        return [join(self.rootFolder, i) for i in files if i.endswith(".jpg") or i.endswith(".png")]


    def assignCollagePictures(self, imageList):
        if not imageList:
            return

        imageListSize = len(imageList)
        setsOfFour = imageListSize // 4

        collagePictures = []
        if (setsOfFour > 0):
            for s in range(setsOfFour):
                collagePictures.append([imageList[i] for i in range(4*s, 4*(s + 1))])

        if (setsOfFour == 0) or (imageListSize % 4 != 0):
            collagePictures.append([imageList[i] for i in range(4*setsOfFour, imageListSize)])

        return collagePictures

    


class CollageCreator:
    def __init__(self, selector):
        self.images = selector
        self.imageCounter = 0
        self.collageCounter = 1
        self.collageFolder = self.createCollageFolder()
        self.collagesTotal = self.getCollagesTotal()


    def getCollagesTotal(self):
        collagesTotal = 0
        if self.images.portraitCollagePictures:
            collagesTotal += len(self.images.portraitCollagePictures)

        if self.images.landscapeCollagePictures:
            collagesTotal += len(self.images.landscapeCollagePictures)

        return collagesTotal


    def createCollages(self):

        if self.images.portraitCollagePictures:
            for pictures in self.images.portraitCollagePictures:
                bufferedPictures = self.resizeImages(pictures)
                self.insertCounterAndWatermark(bufferedPictures)

                try:
                    canvas = self.createBlankCanvas(bufferedPictures)
                    if not canvas: return

                except Exception as e:
                    errorMessage("Unable to create collage canvas", e)
                    self.clearBufferFiles()
                    return

                self.pasteToCanvas(bufferedPictures)

        if self.images.landscapeCollagePictures:
            for pictures in self.images.landscapeCollagePictures:
                bufferedPictures = self.resizeImages(pictures)
                self.insertCounterAndWatermark(bufferedPictures)

                try:
                    canvas = self.createBlankCanvas(bufferedPictures)
                    if not canvas: return

                except Exception as e:
                    errorMessage("Unable to create collage canvas", e)
                    self.clearBufferFiles()
                    return

                self.pasteToCanvas(bufferedPictures)

        self.clearBufferFiles()
        self.logStatistics()

    def resizeImages(self, pictures):

        counter = 0
        bufferedPictures = []
        for picture in pictures:

            size = PicSize(picture.height, picture.width)
            if not size.isCorrect():
                continue

            try:
                reSize = (size.LONG, size.LONG)
                pic = Image.open(picture.location)
                pic.thumbnail(reSize, Image.ANTIALIAS)

                location = join(BUFFER_PATH, "pic-" + str(counter) + ".jpg")
                bufferedPictures.append(Picture(location))
                pic.save(location, "JPEG")

            except Exception as e:
                errorMessage("Unable to resize image", e)

            counter += 1

        return bufferedPictures


    def insertCounterAndWatermark(self, bufferedPictures):

        for picture in bufferedPictures:
            try:
                pic = Image.open(picture.location)
                picture.width, picture.height = pic.size

                self.pasteCounter(pic)
                self.pasteWatermark(pic)

                pic.save(picture.location)

            except Exception as e:
                errorMessage("Unable to insert image counter", e)
                continue

    def pasteCounter(self, image):

        self.imageCounter += 1
        text = str(self.imageCounter)

        draw = ImageDraw.Draw(image)
        for i in range(OUTLINE):
            draw.text((TEXT_OFFSET-i, TEXT_OFFSET), text, font=FONT, fill=WHITE)
            draw.text((TEXT_OFFSET+i, TEXT_OFFSET), text, font=FONT, fill=WHITE)
            draw.text((TEXT_OFFSET, TEXT_OFFSET+i), text, font=FONT, fill=WHITE)
            draw.text((TEXT_OFFSET, TEXT_OFFSET-i), text, font=FONT, fill=WHITE)
            draw.text((TEXT_OFFSET-i, TEXT_OFFSET+i), text, font=FONT, fill=WHITE)
            draw.text((TEXT_OFFSET+i, TEXT_OFFSET+i), text, font=FONT, fill=WHITE)
            draw.text((TEXT_OFFSET-i, TEXT_OFFSET-i), text, font=FONT, fill=WHITE)
            draw.text((TEXT_OFFSET+i, TEXT_OFFSET-i), text, font=FONT, fill=WHITE)

            draw.text((TEXT_OFFSET, TEXT_OFFSET), text, font=FONT, fill=RED)


    def pasteWatermark(self, image):

        watermark = None
        try:
            watermark = Image.open(WATERMARK_IMAGE)
        except Exception as e:
            errorMessage("Unable to open watermark image", e)
            return

        picWidth, picHeight = image.size
        watWidth, watHeight = watermark.size

        offsetWidth = picWidth - watWidth - WATERMARK_OFFSET
        offsetHeight = picHeight - watHeight - WATERMARK_OFFSET

        image.paste(watermark, (offsetWidth, offsetHeight), watermark)

    def createBlankCanvas(self, bufferedPictures):

        width = bufferedPictures[0].width
        height = bufferedPictures[0].height
        size = len(bufferedPictures)

        canvasWidth = 0
        canvasHeight = 0
        if size == 1:
            canvasWidth, canvasHeight = (width + 2*BORDER_SIZE, height + 2*BORDER_SIZE)

        elif size == 2:
            canvasWidth, canvasHeight = (2*width + 3*BORDER_SIZE, height + 2*BORDER_SIZE)

        elif size == 3 or size == 4:
            canvasWidth, canvasHeight = (2*width + 3*BORDER_SIZE, 2*height + 3*BORDER_SIZE)

        else:
            raise Exception("Cannot determine canvas size")

        canvas = Image.new("RGB", (canvasWidth, canvasHeight), WHITE)
        canvas.save(CANVAS_IMAGE, "PNG")

        return canvas

    def pasteToCanvas(self, bufferedPictures):
        if not isfile(CANVAS_IMAGE):
            return


        canvas = None
        pictures = None
        try:
            canvas = Image.open(CANVAS_IMAGE)
            pictures = [Image.open(p.location) for p in bufferedPictures]
        except Exception as e:
            errorMessage("Unable to open collage images")
            return

        if not (canvas or pictures):
            return

        counter = 0
        for picture in pictures:
            width, height = picture.size
            x, y = self.picturePosition(width, height, counter)
            canvas.paste(picture, (x, y))
            counter += 1

        if len(pictures) == 3:
            try:
                logo = Image.open(LOGO_IMAGE)
                logoWidth, logoHeight = logo.size
                canvasWidth, canvasHeight = canvas.size
                x, y = ((3*canvasWidth - 2*logoWidth)//4, (3*canvasHeight - 2*logoHeight)//4)
                canvas.paste(logo, (x, y), logo)
            except Exception as e:
                errorMessage("Unable to create logo in blank collage space", e)

        canvas.save(join(
            self.collageFolder,
            "kolaż-" + self.numberLeadingZeroes(self.collageCounter) + ".jpg"),
            "JPEG")
        self.collageCounter += 1


    def picturePosition(self, width, height, i):
        picturePositions = [
            (BORDER_SIZE, BORDER_SIZE),
            (2*BORDER_SIZE + width, BORDER_SIZE),
            (BORDER_SIZE, 2*BORDER_SIZE + height),
            (2*BORDER_SIZE + width, 2*BORDER_SIZE + height)]

        return picturePositions[i]

    def createCollageFolder(self):
        collageFolder = join(self.images.rootFolder, COLLAGE_FOLDER)
        try:
            if not exists(collageFolder):
                makedirs(collageFolder)
        except Exception as e:
            errorMessage("Unable to create collage folder")

        return collageFolder

    def numberLeadingZeroes(self, number):
        n = ""
        if number < 10:
            n += "0"
        n += str(number)
        return n

    def clearBufferFiles(self):
        for file in listdir(BUFFER_PATH):
            filePath = join(BUFFER_PATH, file)
            try:
                if isfile(filePath):
                    unlink(filePath)
            except Exception as e:
                errorMessage("Unable to delete file", e)


    def logStatistics(self):
        message = "Made " + str(self.collagesTotal) + " collages\n"
        message += "From " + str(self.imageCounter) + " pictures\n"
        message += "Located in: " + self.images.rootFolder
        now = str(datetime.now())
        message = SEP_LINE + now + "\n" + message + "\n"
        logMessage(message)
