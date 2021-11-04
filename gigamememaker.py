from PIL import Image, ImageFont, ImageDraw, UnidentifiedImageError
import random as rand
import textwrap as tr
import sys
import io
import requests
import math

class Mememaker():

    def make_meme(self, top_text, bottom_text, img):
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

        topTextPosition = ((image_size[0]/2 - top_text_size[0]/2), 0)
        bottomTextPosition = ((image_size[0]/2 - bottom_text_size[0]/2), image_size[1] - bottom_text_size[1]/.8)

        draw = ImageDraw.Draw(img)

        if sys.getsizeof(img.tobytes()) > 7900000:
            img = 'TOO_LARGE'
        else:
            draw.text(topTextPosition, top_text, (255,255,255), font=font, stroke_width=round(fontSize*.06), stroke_fill=(0, 0, 0))
            draw.text(bottomTextPosition, bottom_text, (255,255,255), font=font, stroke_width=round(fontSize*.06), stroke_fill=(0, 0, 0))
        return img

def giga_meme(top_text, bottom_text):
    giga_num = rand.randint(0, 9)
    source = f'giga/giga_{giga_num}.jpeg'
    img = Image.open(source)
    mememaker = Mememaker()
    meme = mememaker.make_meme(top_text, bottom_text, img)
    return meme

def custom_meme(top_text, bottom_text, url):
    try:
        response = requests.get(url)
        img_bytes = io.BytesIO(response.content) 
        img = Image.open(img_bytes)
        mememaker  = Mememaker()
        meme = mememaker.make_meme(top_text, bottom_text, img)
    except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, UnidentifiedImageError) as e:
        meme = 'URL_ERROR'
    return meme

if __name__ == '__main__':
    top_text = input('Top Text: ').upper()
    bottom_text = input('Bottom Text: ').upper()
    url = input('URL: ')
    meme = custom_meme(top_text, bottom_text, url)
    meme.show()