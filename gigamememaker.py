from PIL import Image, ImageFont, ImageDraw 
import random as rand
import textwrap as tr
import sys
import io

class Gigamememaker():
    def get_giga(self):
        giga_num = rand.randint(0, 9)
        source = f'giga/giga_{giga_num}.jpeg'
        return source

    def make_meme(self, top_text, bottom_text, filename):
        img = Image.open(filename)
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

        outlineRange = int(fontSize/15)
        for x in range(-outlineRange, outlineRange+1):
            for y in range(-outlineRange, outlineRange+1):
                draw.text((topTextPosition[0]+x, topTextPosition[1]+y), top_text, (0,0,0), font=font)
                draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottom_text, (0,0,0), font=font)

        draw.text(topTextPosition, top_text, (255,255,255), font=font)
        draw.text(bottomTextPosition, bottom_text, (255,255,255), font=font)

        return img

    def main(self, top_text, bottom_text):
        source = self.get_giga()
        giga = self.make_meme(top_text, bottom_text, source)
        return giga

def main(top_text, bottom_text):
    giga = Gigamememaker()
    giga = giga.main(top_text, bottom_text)
    return giga

if __name__ == '__main__':
    top_text = input('Top Text: ').upper()
    bottom_text = input('Bottom Text: ').upper()
    giga = Gigamememaker()
    giga.main(top_text, bottom_text)
