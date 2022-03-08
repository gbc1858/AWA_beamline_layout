# AWA_beamline_layout

## Description
Generate beamline layout based on the csv input file.

## Usage
1. Install all packages in `requirements.txt`.

2. In `setup.py`, change/verify the path to the beamline input csv (`path_csv_file`), and the image folder for all beamline elements (`path_beamline_element`).

3. Run `main.py` to generate the specific zone map of the beamline, 
   ```python
   from function import *
   from setup import *
   
   data = InputFile(path_csv_file)
   data.sort_input()
   ```
   If want to have label plotted together , 
   ```python
   plot_beam_layout(data.zone_3A_element, data.zone_3A_zpos, data.zone_3A_tag, data.zone_3A_comment, zone='3A',
                    show_label=True, save_image=save_image)
   ```
   ![img](readme_img/zone_3A.png)
   If want to hide the label, 
   ```python
   plot_beam_layout(data.zone_4_element, data.zone_4_zpos, data.zone_4_tag, data.zone_4_comment, zone='4',
                    show_label=False, save_image=save_image)
   ```
   ![img](readme_img/zone_3A_nolabel.png)
   
## TODOs
- [ ] Add an option to generate the whole beamline map.
- [ ] Add extra YAGs on the deflected path after all dipoles (mainly in zone 4 and 5).
![img](readme_img/zone_4.png)
![img](readme_img/zone_5.png)