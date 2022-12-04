import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from setup import *
plt.rcParams['savefig.dpi'] = 500


class InputFile:
    def __init__(self, file):
        self.file = file
        self.zone_1_element, self.zone_1_zpos, self.zone_1_tag, self.zone_1_comment = [], [], [], []
        self.zone_2_element, self.zone_2_zpos, self.zone_2_tag, self.zone_2_comment = [], [], [], []
        self.zone_3A_element, self.zone_3A_zpos, self.zone_3A_tag, self.zone_3A_comment = [], [], [], []
        self.zone_3B_element, self.zone_3B_zpos, self.zone_3B_tag, self.zone_3B_comment = [], [], [], []
        self.zone_4_element, self.zone_4_zpos, self.zone_4_tag, self.zone_4_comment = [], [], [], []
        self.zone_5_element, self.zone_5_zpos, self.zone_5_tag, self.zone_5_comment = [], [], [], []

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
        for i in x:
            del zpos[i]
        for i in range(len(zpos)):
            if i >= 1:
                element = sum(zpos[0:i + 1])
                zpos_new.append(element)

    if zone in ('4', '5'):
        for i in range(len(zpos)):
            if i >= 1:
                element = sum(zpos[0:i + 1])
                zpos_new.append(element)
    return [zpos[0]] + zpos_new


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
    ax.autoscale()
    img_h, img_w = len(img)/2 * 0.00006, len(img[0])/2 * 0.1
    return img_h, img_w


def plot_beam_arrow(z: list, y):
    diff = [j - i for i, j in zip(z[:-1], z[1:])]
    diff_sort = sorted(diff)[::-1][0:3]
    if type(y) == list:
        z_end = z[-1] + (z[-1] - z[0]) * 0.025
        plt.plot(z + [z_end], y + [y[-1]], c='grey', alpha=.5, zorder=-1)
        plt.arrow(z_end, y[-1], 5, 0.000, shape='full', lw=0, length_includes_head=True, color='grey',
                  head_width=.0055, head_length=5, alpha=0.8)
    else:
        for i in diff_sort:
            index = diff.index(i)
            plt.arrow((z[index + 1] - z[index]) / 2 + z[index], y, 5, 0.000, shape='full', lw=0,
                      length_includes_head=True,
                      color='grey', head_width=.0035, head_length=5, alpha=0.8)
        z_end = z[-1] + (z[-1] - z[0]) * 0.025
        plt.arrow(z_end, y, 5, 0.000, shape='full', lw=0, length_includes_head=True, color='grey',
                  head_width=.0035, head_length=5, alpha=0.8)
        plt.plot([z[0], z_end], [y, y], c='grey', alpha=.5, zorder=-1)


def plot_beam_layout(element_name, zpos, tag, comment, zone, show_label=True, save_image=False):
    if zone in ['3A', '3B']:
        fig, ax1 = plt.subplots(figsize=(8, 3.5))
    else:
        fig, ax1 = plt.subplots(figsize=(12, 3.5))

    if zone == '4':
        ANNOTATION_FACTOR = 0.012
    if zone in ['1', '2', '3A', '3B']:
        ANNOTATION_FACTOR = 0
    if zone == '5':
        ANNOTATION_FACTOR = 0.003

    y_temp = [0 for _ in range(len(tag))]
    for i in range(len(tag)):
        y = 0           # meaningless y value for plotting the deflected path only
        if comment[i] == 'upper stage 1':
            y = 0.05    # meaningless y value for plotting the deflected path only
            y_temp[i] = 0.05
        elif comment[i] == 'upper stage 2':
            y = 0.10    # meaningless y value for plotting the deflected path only
            y_temp[i] = 0.10

        if tag[i] == 'Radiabeam skew':
            img_h, img_w = plot_beamline_element(zpos[i], [y], Radiabeam_skew, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, img_h + y + ANNOTATION_FACTOR),
                         ha='left', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'peach quad':
            img_h, img_w = plot_beamline_element(zpos[i], [y], peach_quad, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, img_h + y + ANNOTATION_FACTOR),
                         ha='left', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'Radiabeam dipole':
            img_h, img_w = plot_beamline_element(zpos[i], [y], Radiabeam_dipole, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], img_h + y + ANNOTATION_FACTOR),
                         ha='center', rotation=0, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'yag' or tag[i] == 'yag_straight':
            img_h, img_w = plot_beamline_element(zpos[i], [y], YAG, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, img_h + y + ANNOTATION_FACTOR),
                         ha='left', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'yag_down':
            img_h, img_w = plot_beamline_element(zpos[i], [y - 0.03], YAG_down, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, -0.06 + img_h + y),
                         ha='left', rotation=0, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'yag_up':
            img_h, img_w = plot_beamline_element(zpos[i] - 5, [y + 0.03], YAG_up, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y),
                         xytext=(zpos[i] - img_w, img_h + y + 0.04 + ANNOTATION_FACTOR),
                         ha='left', rotation=0, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'IMP quad':
            img_h, img_w = plot_beamline_element(zpos[i], [y], IMP_quad, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, img_h + y + ANNOTATION_FACTOR),
                         ha='left', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'solenoid':
            img_h, img_w = plot_beamline_element(zpos[i], [y], solenoid, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, img_h + y + ANNOTATION_FACTOR),
                         ha='left', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'gun':
            plot_beamline_element(zpos[i], [y], gun, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - 35, 0),
                         ha='center', rotation=0, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'linac':
            img_h, img_w = plot_beamline_element(zpos[i], [y], linac, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], img_h + y + ANNOTATION_FACTOR),
                         ha='center', rotation=0, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'slit':
            img_h, img_w = plot_beamline_element(zpos[i], [y], slit, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y),
                         xytext=(zpos[i] + img_w, -0.8 * img_h + y + ANNOTATION_FACTOR),
                         ha='right', va='top', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'tdc':
            img_h, img_w = plot_beamline_element(zpos[i], [y], tdc, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], img_h + y + ANNOTATION_FACTOR),
                         ha='center', rotation=0, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'ict':
            img_h, img_w = plot_beamline_element(zpos[i], [y], ict, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, img_h + y + ANNOTATION_FACTOR),
                         ha='left', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'pets':
            img_h, img_w = plot_beamline_element(zpos[i], [y], pets, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], img_h + y + ANNOTATION_FACTOR),
                         ha='center', rotation=0, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'dut':
            img_h, img_w = plot_beamline_element(zpos[i], [y], dut, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i], img_h + y + ANNOTATION_FACTOR),
                         ha='center', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'tw_gun':
            img_h, img_w = plot_beamline_element(zpos[i], [y], tw_gun, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, img_h + y + ANNOTATION_FACTOR),
                         ha='left', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] == 'trim':
            img_h, img_w = plot_beamline_element(zpos[i], [y], trim, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, img_h + y + ANNOTATION_FACTOR),
                         ha='left', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None
        if tag[i] not in available_tags:
            img_h, img_w = plot_beamline_element(zpos[i], [y], unknown, ax=ax1)
            ax1.annotate(element_name[i], xy=(zpos[i], y), xytext=(zpos[i] - img_w, img_h + y + ANNOTATION_FACTOR),
                         ha='left', rotation=45, fontsize=ANNOTATION_FONT) if show_label else None

    rmv_index = []
    for i in range(len(tag)):
        rmv_index.append(i) if tag[i] in ['yag_down', 'yag_up', 'yag_straight'] else None

    plt.title('Layout of Zone ' + zone + f'\n(Input file: {path_parent_xlsx_file.split("/")[-1]})', fontsize=12)
    if zone in ['1', '2', '3A', '3B']:
        plot_beam_arrow(zpos, 0)
        ax1.set_ylim(-0.06, 0.045)
    if zone == '4':
        zpos = [i for j, i in enumerate(zpos) if j not in rmv_index]
        y_temp = [i for j, i in enumerate(y_temp) if j not in rmv_index]
        plot_beam_arrow(zpos, y_temp)
        ax1.set_ylim(-0.06, 0.18)
    if zone == '5':
        zpos = [i for j, i in enumerate(zpos) if j not in rmv_index]
        y_temp = [i for j, i in enumerate(y_temp) if j not in rmv_index]
        plot_beam_arrow(zpos, y_temp)
        ax1.set_ylim(-0.06, 0.09)

    ax1.axis('off')
    ax1.set_xlabel('z from gun start (cm)', fontsize=12)
    ax1.axes.yaxis.set_ticklabels([])
    ax1.axes.xaxis.set_ticklabels([])
    plt.tight_layout()
    fig.savefig('zone_' + zone + '.png', format='png') if save_image else None
    plt.show()
