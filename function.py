import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from setup import *
from matplotlib.transforms import Bbox, TransformedBbox
from matplotlib.legend_handler import HandlerBase
from matplotlib.image import BboxImage
plt.rcParams['savefig.dpi'] = 500


class InputFile:
    def __init__(self, file):
        self.file = file
        self.zone_1_element, self.zone_1_zpos, self.zone_1_tag, self.zone_1_comment = [], [], [], []
        self.zone_2_element, self.zone_2_zpos,  self.zone_2_tag, self.zone_2_comment = [], [], [], []
        self.zone_3A_element, self.zone_3A_zpos, self.zone_3A_tag,  self.zone_3A_comment = [], [], [], []
        self.zone_3B_element, self.zone_3B_zpos,  self.zone_3B_tag, self.zone_3B_comment = [], [], [], []
        self.zone_4_element, self.zone_4_zpos,  self.zone_4_tag, self.zone_4_comment = [], [], [], []
        self.zone_5_element, self.zone_5_zpos,  self.zone_5_tag, self.zone_5_comment = [], [], [], []

    def sort_input(self):
        with open(self.file) as opf:
            data = opf.readlines()[2::]
        for i in range(len(data)):
            row_data = data[i].split(',')
            if row_data[0]:
                self.zone_1_element.append(row_data[0])
                self.zone_1_zpos.append(float(row_data[1]))
                self.zone_1_tag.append(row_data[2])
                self.zone_1_comment.append(row_data[3])

            if row_data[4]:
                self.zone_2_element.append(row_data[4])
                self.zone_2_zpos.append(float(row_data[5]))
                self.zone_2_tag.append(row_data[6])
                self.zone_2_comment.append(row_data[7])

            if row_data[8]:
                self.zone_3A_element.append(row_data[8])
                self.zone_3A_zpos.append(float(row_data[9]))
                self.zone_3A_tag.append(row_data[10])
                self.zone_3A_comment.append(row_data[11])

            if row_data[12]:
                self.zone_3B_element.append(row_data[12])
                self.zone_3B_zpos.append(float(row_data[13]))
                self.zone_3B_tag.append(row_data[14])
                self.zone_3B_comment.append(row_data[15])

            if row_data[16]:
                self.zone_4_element.append(row_data[16])
                self.zone_4_zpos.append(float(row_data[17]))
                self.zone_4_tag.append(row_data[18])
                self.zone_4_comment.append(row_data[19])

            if row_data[20]:
                self.zone_5_element.append(row_data[20])
                self.zone_5_zpos.append(float(row_data[21]))
                self.zone_5_tag.append(row_data[22])
                self.zone_5_comment.append(row_data[23].rstrip())

        self.zone_1_zpos = zpos_ref_to_zero(self.zone_1_zpos, self.zone_1_comment, zone='1')
        self.zone_2_zpos = [i + self.zone_1_zpos[-1] for i in
                            zpos_ref_to_zero(self.zone_2_zpos, self.zone_2_comment, zone='2')]
        self.zone_3A_zpos = [i + self.zone_2_zpos[-1] for i in
                             zpos_ref_to_zero(self.zone_3A_zpos, self.zone_3A_comment, zone='3A')]
        self.zone_3B_zpos = [i + self.zone_3A_zpos[-1] for i in
                             zpos_ref_to_zero(self.zone_3B_zpos, self.zone_3B_comment, zone='3B')]
        self.zone_4_zpos = [i + self.zone_2_zpos[-1] for i in
                            zpos_ref_to_zero(self.zone_4_zpos, self.zone_4_comment, zone='4')]
        self.zone_5_zpos = [i + self.zone_4_zpos[-1] for i in
                            zpos_ref_to_zero(self.zone_5_zpos, self.zone_5_comment, zone='5')]


def zpos_ref_to_zero(zpos, comment, zone):
    zpos_new = []
    x = []
    if zone in ('1', '2', '3A', '3B'):
        # eliminate the elements from the deflected path.
        for i in range(len(comment)):
            if comment[i]:
                x.append(i)
        x.reverse()
        for i in x:
            del zpos[i]
        for i in range(len(zpos)):
            if i >= 1:
                element = sum(zpos[0:i+1])
                zpos_new.append(element)

    if zone in ('4', '5'):
        for i in range(len(zpos)):
            if i >= 1:
                element = sum(zpos[0:i+1])
                # print(element)
                zpos_new.append(element)
    return [zpos[0]] + zpos_new


# class HandlerImage(HandlerBase):
#     def __init__(self, img_path):
#         self.image_data = plt.imread(img_path)
#         super(HandlerImage, self).__init__()
#
#     def create_artists(self, legend, orig_handle,
#                        x0, y0, width, height, fontsize, transform,):
#         new_bbox = Bbox.from_bounds(x0 + width / 4, y0,
#                                     height * self.image_data.shape[1]*2 / self.image_data.shape[0],
#                                     height*2)
#
#         tbb = TransformedBbox(new_bbox, transform)
#         image = BboxImage(tbb)
#         image.set_data(self.image_data)
#         self.update_prop(image, orig_handle, legend)
#         return [image]


def plot_beamline_element(x, y, image_path, ax=None, zoom=0.1):
    try:
        img = plt.imread(image_path)
    except TypeError:
        print('Load image error.')
        pass
    im = OffsetImage(img, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.grid(ls=':', alpha=0.5)
    ax.autoscale()
    return artists


def plot_beam_layout(element_name, zpos, tag, comment, zone, show_label=True, save_image=False):
    fig, ax1 = plt.subplots(figsize=(12, 3))
    for i in range(len(tag)):
        y = 0               # meaningless y value for plotting the deflected path only
        if comment[i] == 'upper stage 1':
            y = 0.04        # meaningless y value for plotting the deflected path only
        elif comment[i] == 'upper stage 2':
            y = 0.09        # meaningless y value for plotting the deflected path only

        if tag[i] == 'Radiabeam skew':
            plot_beamline_element(zpos[i], [y], Radiabeam_skew, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.017),
                         ha='center', rotation=45) if show_label else None
        if tag[i] == 'peach quad':
            plot_beamline_element(zpos[i], [y], peach_quad, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.017),
                         ha='center', rotation=45) if show_label else None
        if tag[i] == 'Radiabeam dipole':
            plot_beamline_element(zpos[i], [y], Radiabeam_dipole, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.017),
                         ha='center', rotation=0) if show_label else None
        if tag[i] == 'yag':
            plot_beamline_element(zpos[i], [y], YAG, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.017),
                         ha='center', rotation=45) if show_label else None
        if tag[i] == 'IMP quad':
            plot_beamline_element(zpos[i], [y], IMP_quad, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.023),
                         ha='center', rotation=45) if show_label else None
        if tag[i] == 'solenoid':
            plot_beamline_element(zpos[i], [y], solenoid, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.023),
                         ha='center', rotation=45) if show_label else None
        if tag[i] == 'gun':
            plot_beamline_element(zpos[i], [y], gun, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(-35, y + 0),
                         ha='center', rotation=0) if show_label else None
        if tag[i] == 'linac':
            plot_beamline_element(zpos[i], [y], linac, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.017),
                         ha='center', rotation=0) if show_label else None
        if tag[i] == 'slit':
            plot_beamline_element(zpos[i], [y], slit, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.023),
                         ha='center', rotation=45) if show_label else None
        if tag[i] == 'tdc':
            plot_beamline_element(zpos[i], [y], tdc, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.017),
                         ha='center', rotation=0) if show_label else None
        if tag[i] == 'ict':
            plot_beamline_element(zpos[i], [y], ict, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.023),
                         ha='center', rotation=45) if show_label else None
        if tag[i] == 'pets':
            plot_beamline_element(zpos[i], [y], pets, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.017),
                         ha='center', rotation=0) if show_label else None
        if tag[i] == 'dut':
            plot_beamline_element(zpos[i], [y], dut, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.017),
                         ha='center', rotation=45) if show_label else None
        if tag[i] not in available_tags:
            plot_beamline_element(zpos[i], [y], unknown, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], y + 0.017),
                         ha='center', rotation=45) if show_label else None

    plt.gca().invert_xaxis()
    plt.xlabel('z from gun start (cm)', fontsize=12)
    plt.title('Layout of Zone ' + zone + f'\n(Input file: {path_parent_xlsx_file.split("/")[-1]})', fontsize=12)
    if zone == '4':
        plt.ylim(0.005, 0.15)
    elif zone == '5':
        plt.ylim(-0.05, 0.09)
    else:
        plt.ylim(-0.05, 0.05)
    ax1.axes.yaxis.set_ticklabels([])
    plt.tight_layout()
    fig.savefig('zone_' + zone + '.png', format='png') if save_image else None
    plt.show()
