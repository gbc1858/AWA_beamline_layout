###############
# Program setup
###############
import pandas as pd


path_beamline_element = '/Users/chen/Desktop/ANL_work/HEP_division/beam_layout/img/'
path_parent_xlsx_file = '/Users/chen/Desktop/ANL_work/HEP_division/beam_layout/test.xlsx'

df = pd.read_excel(path_parent_xlsx_file, engine='openpyxl')
df.to_csv(path_parent_xlsx_file.split('/')[-1].split('.')[0] + '.csv', index=False, quotechar="'")
path_csv_file = path_parent_xlsx_file.rsplit('.', 1)[0] + '.csv'


peach_quad = path_beamline_element + 'peach_quad.png'
Radiabeam_dipole = path_beamline_element + 'Radiabeam_dipole.png'
Radiabeam_quad = path_beamline_element + 'Radiabeam_quad.png'
Radiabeam_skew = path_beamline_element + 'Radiabeam_skew.png'
solenoid = path_beamline_element + 'solenoid.png'
IMP_quad = path_beamline_element + 'IMP_quad.png'
LINAC = path_beamline_element + 'LINAC.png'
YAG = path_beamline_element + 'YAG.png'
gun = path_beamline_element + 'gun.png'
linac = path_beamline_element + 'linac.png'
slit = path_beamline_element + 'slit.png'
tdc = path_beamline_element + 'tdc.png'
unknown = path_beamline_element + 'unknown.png'

available_tags = ['gun', 'solenoid', 'linac', 'yag', 'Radiabeam skew', 'Radiabeam dipole', 'IMP quad', 'peach quad',
                  'tdc', 'slit']

# if __name__ == '__main__':
