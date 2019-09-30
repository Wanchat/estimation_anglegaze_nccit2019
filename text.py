from PIL import ImageFont, ImageDraw, Image
import numpy as np

fontpath = "data/Prompt-Regular.ttf"

def text(frame, roi, text, size, color):
    font = ImageFont.truetype(fontpath, size)
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)

    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil,  "RGBA")

    draw.rectangle(((roi[0], roi[1]+(offset_y-2)), 
    	(roi[0]+width, roi[1]+descent+baseline)), 
    	fill=(255,255,255,150))

    draw.text(roi, "{}".format(text), font=font, fill=color)

    return  np.array(img_pil)

if __name__ == "__main__":

	import cv2
	img = np.zeros((300,300,3), dtype="uint8")
	img = text(img, (50,100), "hello world", 35, (0,0,255))
	cv2.imshow('out', img)
	cv2.waitKey(0)
