import os
from PIL import Image


class Tiler:
    def __init__(self,
                 source_folder_path,
                 destination_folder_path,
                 tiles_height=612,
                 tiles_width=612):
        self.source_folder_path = source_folder_path
        self.destination_folder_path = destination_folder_path
        self.tiles_height = tiles_height
        self.tiles_width = tiles_width

    def image_to_tiles(self, image_name):
        source_image_path = os.path.join(self.source_folder_path, image_name)
        print('Splitting image ' + str(source_image_path) + ' into ' + str(self.tiles_width) +
              ' x ' + str(self.tiles_height) + ' tiles.')

        im = Image.open(source_image_path)
        image_width, image_height = im.size

        n1 = 0
        for i in range(0, image_height, self.tiles_height):
            n1 += 1
            n2 = 0
            for j in range(0, image_width, self.tiles_width):
                n2 += 1
                box = (j, i, j + self.tiles_width, i + self.tiles_height)
                a = im.crop(box)
                destination_path = os.path.join(self.destination_folder_path,
                                                image_name[:-4] + '_' + str(n1) + '-' + str(n2) + image_name[-4:])
                print('Saving tile (' + str(n1) + ', ' + str(n2) + ') at : ' + str(destination_path))
                a.save(destination_path)

    def transform_all_images_in_source_folder(self):
        for image_name in os.listdir(self.source_folder_path):
            if image_name.endswith(".jpg") or image_name.endswith(".png"):
                self.image_to_tiles(image_name=image_name)


if __name__ == '__main__':
    print('Procedure started.')
    """
    tiler = Tiler(source_folder_path='/home/laurent/Documents/Work/CRIM/GeoImageNet/Segmentation/Projects/dataset'
                                     '-reshaper/inputs',
                  destination_folder_path='/home/laurent/Documents/Work/CRIM/GeoImageNet/Segmentation/Projects'
                                          '/dataset-reshaper/results',
                  tiles_height=612,
                  tiles_width=612)
    """
    tiler = Tiler(source_folder_path='/home/laurent/Documents/Work/CRIM/GeoImageNet/Segmentation/Data/DeepGlobe-small-patches/land-train-src',
                  destination_folder_path='/home/laurent/Documents/Work/CRIM/GeoImageNet/Segmentation/Data/DeepGlobe-small-patches/land-train-dst',
                  tiles_height=612,
                  tiles_width=612)
    tiler.transform_all_images_in_source_folder()

