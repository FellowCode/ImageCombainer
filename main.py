from PIL import Image
import easygui
import os
from multiprocessing import Process


def combine(key, value, path, mesh_name):
    image_list = []
    resolution = 0

    print(key)

    for img_dir in value:
        img = Image.open(img_dir)
        image_list.append(img.convert('RGBA'))
        resolution = img.size[0]

    color = 'black'
    if key == 'AO':
        color = 'white'
    result = Image.new('RGB', (resolution, resolution), color=color)
    for i in range(0, resolution, 8):
        for j in range(0, resolution, 8):
            if key == 'AO':
                pass
            else:
                for img in image_list:
                    r, g, b, a = img.getpixel((i, j))
                    if a != 0:
                        for ii in range(8):
                            for jj in range(8):
                                result.putpixel((i + ii, j + jj), (r, g, b))
                        break
    result.save(path + '\\{}_{}.png'.format(mesh_name, key))

    print(key, 'complete')


def main():
    input()
    mesh_name = easygui.enterbox(title='Image combiner', msg='Enter mesh name')
    mesh_name = mesh_name.replace(' ', '_')

    path = easygui.diropenbox(msg='Select images folder', title='Image combiner')

    # path = easygui.fileopenbox(msg='Select images', title='Image combiner', default='*.png', filetypes=['*.png'], multiple=True)

    images_dirs = []
    images = {}

    for r, d, f in os.walk(path):
        for file in f:
            if '.png' in file:
                images_dirs.append(os.path.join(r, file))

    for img_dir in images_dirs:
        img_dir_tmp = img_dir[img_dir.rindex('\\') + 1:]
        if '_' in img_dir_tmp:
            group_name = img_dir[img_dir.rindex('_') + 1:img_dir.rindex('.')]
            if not group_name in images:
                images[group_name] = [img_dir]
            else:
                images[group_name].append(img_dir)

    combiners = []

    for key, value in images.items():
        combiner = Process(target=combine, args=(key, value, path, mesh_name))
        combiner.start()
        #combiner.join()
        combiners.append(combiner)

    for combiner in combiners:
        combiner.join()

    easygui.msgbox(title='Image combiner', msg='Complete!')


if __name__ == '__main__':
    main()
