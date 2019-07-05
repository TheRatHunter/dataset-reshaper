import os
from PIL import Image


class Selector:
    def __init__(self, source_folder_path):
        self.source_folder_path = source_folder_path

    def compute_mask_colors_ratio(self, image_name):
        if not image_name[-4:] == '.png':
            print('You should process a mask with this method.')
            exit(-1)

        label_values = []
        number_of_pixels_dict = {}
        source_image_path = os.path.join(self.source_folder_path, image_name)
        print('Analyzing mask ' + str(source_image_path))

        input_img = Image.open(source_image_path)
        # Reduce mask size to speed up the process
        input_img = input_img.convert('P', palette=Image.WEB)
        input_img.thumbnail((50, 50), Image.ANTIALIAS)
        total_nb_pixels = 0
        for val in input_img.getdata():
            total_nb_pixels += 1
            if val not in label_values:
                number_of_pixels_dict[val] = 1
                label_values.append(val)
            else:
                number_of_pixels_dict[val] += 1

        max_proportion = 0.0
        dominant_color = -1
        for key, val in number_of_pixels_dict.items():
            if float(val)/float(total_nb_pixels) > max_proportion:
                max_proportion = float(val)/float(total_nb_pixels)
                dominant_color = key
            print('Proportion of ' + str(key) + ' : ' + str(float(val)/float(total_nb_pixels)))

        print('The dominant color is ' + str(dominant_color))
        return dominant_color

    def process_all_images_in_source_folder(self):
        dominant_colors = []
        classified_masks = {}
        for image_name in os.listdir(self.source_folder_path):
            if image_name.endswith(".png"):
                this_dominant = self.compute_mask_colors_ratio(image_name=image_name)
                if this_dominant not in dominant_colors:
                    dominant_colors.append(this_dominant)
                    classified_masks[this_dominant] = [image_name]
                else:
                    classified_masks[this_dominant].append(image_name)

        print('Classified masks : ' + str(classified_masks))

        print('Writing results in files...')
        for key, val in classified_masks.items():
            f = open(str(key)+'_dominants.txt', 'w+')
            for img_name in val:
                f.write(str(img_name)+'\n')
            f.close()


if __name__ == '__main__':
    print('Procedure started.')

    selector = Selector(source_folder_path='/home/laurent/Documents/Work/CRIM/GeoImageNet/Segmentation/Data/DeepGlobe-small-patches/land-train-dst')
    selector.process_all_images_in_source_folder()
