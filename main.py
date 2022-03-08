from function import *
from setup import *

data = InputFile(path_csv_file)
data.sort_input()

save_image = False
plot_beam_layout(data.zone_1_element, data.zone_1_zpos, data.zone_1_tag, data.zone_1_comment, zone='1',
                 show_label=True, save_image=False)
plot_beam_layout(data.zone_2_element, data.zone_2_zpos, data.zone_2_tag, data.zone_2_comment, zone='2',
                 show_label=True, save_image=save_image)
plot_beam_layout(data.zone_3A_element, data.zone_3A_zpos, data.zone_3A_tag, data.zone_3A_comment, zone='3A',
                 show_label=True, save_image=save_image)
plot_beam_layout(data.zone_3B_element, data.zone_3B_zpos, data.zone_3B_tag, data.zone_3B_comment, zone='3B',
                 show_label=True, save_image=save_image)
plot_beam_layout(data.zone_4_element, data.zone_4_zpos, data.zone_4_tag, data.zone_4_comment, zone='4',
                 show_label=False, save_image=save_image)
plot_beam_layout(data.zone_5_element, data.zone_5_zpos, data.zone_5_tag, data.zone_5_comment, zone='5',
                 show_label=True, save_image=save_image)
