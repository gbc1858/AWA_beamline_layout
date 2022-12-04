#################
# Program setup #
#################
import pandas as pd
import os


path_beamline_element = os.getcwd() + '/img/'
path_parent_xlsx_file = os.getcwd() + '/20220926_awa_beamline.xlsx'
# path_parent_xlsx_file = os.getcwd() + '/20221102_awa_beamline_CSS.xlsx'
# path_parent_xlsx_file = os.getcwd() + '/20220523_TW-gun_beamline_napac.xlsx'

df = pd.read_excel(path_parent_xlsx_file, engine='openpyxl')
df.to_csv(path_parent_xlsx_file.split('/')[-1].split('.')[0] + '.csv', index=False, quotechar="'")
path_csv_file = path_parent_xlsx_file.rsplit('.', 1)[0] + '.csv'


peach_quad = path_beamline_element + 'peach_quad2.png'
Radiabeam_dipole = path_beamline_element + 'Radiabeam_dipole2.png'
Radiabeam_quad = path_beamline_element + 'Radiabeam_quad2.png'
Radiabeam_skew = path_beamline_element + 'Radiabeam_skew2.png'
solenoid = path_beamline_element + 'solenoid2.png'
IMP_quad = path_beamline_element + 'IMP_quad2.png'
LINAC = path_beamline_element + 'LINAC.png'
YAG = path_beamline_element + 'YAG2.png'
gun = path_beamline_element + 'gun2.png'
linac = path_beamline_element + 'linac2.png'
slit = path_beamline_element + 'slit2.png'
tdc = path_beamline_element + 'tdc2.png'
unknown = path_beamline_element + 'unknown.png'
ict = path_beamline_element + 'ICT2.png'
pets = path_beamline_element + 'PETS2.png'
dut = path_beamline_element + 'DUT2.png'
tw_gun = path_beamline_element + 'tw_gun.png'
YAG_down = path_beamline_element + 'YAGd2.png'
YAG_up = path_beamline_element + 'YAGd3.png'
trim = path_beamline_element + 'trim2.png'
dot = path_beamline_element + 'dot.png'


available_tags = ['gun', 'solenoid', 'linac', 'yag', 'Radiabeam skew', 'Radiabeam dipole', 'IMP quad', 'peach quad',
                  'tdc', 'slit', 'ict', 'pets', 'dut', 'yag_down', 'trim', 'yag_up', 'dot', 'yag_straight']

ANNOTATION_FONT = 10


# if __name__ == '__main__':
