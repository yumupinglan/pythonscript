from PIL import Image
import tesserocr

p1 = Image.open('/home/willieyu/captchayt.php')
str=tesserocr.image_to_text(p1)
print(str)