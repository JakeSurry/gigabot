from PIL import Image, ImageFont, ImageDraw, ImageSequence, UnidentifiedImageError
import random as rand
import textwrap as tr
import sys
import io
import requests
import warnings
import time
warnings.filterwarnings("error")
warnings.simplefilter("ignore", UserWarning)

class Mememaker():
    def get_text_size(self, top_text, bottom_text, img):

        image_size = img.size

        fontSize = int(image_size[1]/6)
        font = ImageFont.truetype("impact.ttf", fontSize)
        top_text_size = font.getsize(top_text)
        bottom_text_size = font.getsize(bottom_text)

        end = False
        while not end:
            fontSize = fontSize - 1
            font = ImageFont.truetype("impact.ttf", fontSize)
            top_text_size = font.getsize(top_text)
            bottom_text_size = font.getsize(bottom_text)
            if top_text_size[0] < image_size[0]-20 and bottom_text_size[0] < image_size[0]-20:
                end = True
            if fontSize <= 20:
                end = True

        return font, top_text_size, bottom_text_size, image_size, fontSize

    def make_meme(self, top_text, bottom_text, img, font, top_text_size, bottom_text_size, image_size, fontSize):

        topTextPosition = ((image_size[0]/2 - top_text_size[0]/2), 0)
        bottomTextPosition = ((image_size[0]/2 - bottom_text_size[0]/2), image_size[1] - bottom_text_size[1]/.8)

        draw = ImageDraw.Draw(img)

        draw.text(topTextPosition, top_text, font=font, color=(255, 255, 255), stroke_width=round(fontSize*.06), stroke_fill=(0, 0, 0))
        draw.text(bottomTextPosition, bottom_text, font=font, color=(255, 255, 255), stroke_width=round(fontSize*.06), stroke_fill=(0, 0, 0))
        
        return img

def giga_meme(top_text, bottom_text):
    giga_num = rand.randint(0, 9)
    source = f'giga/giga_{giga_num}.jpeg'
    img = Image.open(source)
    mememaker = Mememaker()
    font, top_text_size, bottom_text_size, image_size, fontSize = mememaker.get_text_size(top_text, bottom_text, img)
    meme = mememaker.make_meme(top_text, bottom_text, img, font, top_text_size, bottom_text_size, image_size, fontSize)
    return meme

def custom_meme(top_text, bottom_text, url):
    try:
        if int(requests.head(url).headers['Content-Length']) < 1500000:
            response = requests.get(url)
            img_bytes = io.BytesIO(response.content) 
            img = Image.open(img_bytes)
            mememaker  = Mememaker()
            font, top_text_size, bottom_text_size, image_size, fontSize = mememaker.get_text_size(top_text, bottom_text, img)
            meme = mememaker.make_meme(top_text, bottom_text, img, font, top_text_size, bottom_text_size, image_size, fontSize)
        else:
            meme = 'TOO_LARGE'
    except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema, UnidentifiedImageError) as e:
        meme = 'URL_ERROR'
    return meme

#THIS SECTION IS FOR TESTING MEMEMAKER INDIVIDUAllY
if __name__ == '__main__':
    top_text = input('Top Text: ').upper()
    bottom_text = input('Bottom Text: ').upper()
    url = 'http://wallpaperevo.com/wp-content/uploads/2016/01/Ford-F-150-Raptor-SuperCrew-4K-UHD-Wallpaper.jpg'
    image = custom_meme(top_text, bottom_text, url)
    image.show()
    image.save('test.jpeg')