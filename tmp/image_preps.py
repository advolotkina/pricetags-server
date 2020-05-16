from PIL import Image
import sys
import os


def prepare_image(filename):
    file_path = os.path.abspath(os.path.join(filename, 'good.jpg'))
    image = Image.open(file_path)
    width, height = image.size

    new_width = 370
    new_height = int(new_width * height / width)

    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    image.save(file_path)
    root_path = os.getcwd()
    os.chdir(filename)
    print(filename, file_path)
    cmd = f"php /home/zhblnd/diplom/lv_utils/img_conv_core.php \"name=good&img={file_path}&cf=indexed_4&format=bin_332\""
    os.system(cmd)
    os.chdir(root_path)


if __name__ == '__main__':
    for file in sys.argv[1:]:
        prepare_image(file)
