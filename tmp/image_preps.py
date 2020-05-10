from PIL import Image
import sys
import os


def prepare_image(filename):
    image = Image.open(filename)
    width, height = image.size

    new_width = 370
    new_height = int(new_width * height / width)

    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    image.save(filename)

    cmd = f"php /home/zhblnd/diplom/lv_utils/img_conv_core.php \"name=good&img={filename}&cf=indexed_4&format=bin_332\""
    os.system(cmd)


if __name__ == '__main__':
    for file in sys.argv[1:]:
        prepare_image(file)
