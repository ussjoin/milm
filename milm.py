#! env python3
"""

This program generates timestamped milk labels.

"""

import time
import os
import subprocess

import treepoem # https://github.com/adamchainz/treepoem
from wand.image import Image # https://docs.wand-py.org/
from wand.drawing import Drawing
from wand.color import Color
import readchar

# https://brother-ql.net/ - this program calls the command-line utilities,
#   but doesn't use them pythonically

import milm_config

# Label notes:
# 1.2 inches high
# 2.2 inches wide


def make_label():
    now = time.strftime('%b %d %I:%M %p',time.localtime())
    
    # 2.2" wide, 1.2" tall, and brother_ql expects 290 dpi for this.
    # Aztec code is 0.3" square.
    # 1D barcode is 1.6" wide and 0.4" high.
    res = 290
    with Image(width=696, height=348, background = Color('white')) as img:
        draw_l1 = Drawing()
        draw_l1.text_alignment = 'center'
        draw_l1.font = './Roboto-Medium.ttf'
        draw_l1.font_size = 26
        draw_l1.text(int(img.width/2), int(res * 0.15), milm_config.LINE_ONE)
        draw_l1(img)
        
        draw_l2 = Drawing()
        draw_l2.text_alignment = 'center'
        draw_l2.font = './Roboto-Medium.ttf'
        draw_l2.font_size = 26
        draw_l2.text(int(img.width/2), int(res * 0.25), milm_config.LINE_TWO)
        draw_l2(img)
        
        draw_name = Drawing()
        draw_name.text_alignment = 'left'
        draw_name.font = './Roboto-Medium.ttf'
        draw_name.font_size = 26
        draw_name.text(int(res * 0.1), int(res * 0.4), milm_config.PATIENT)
        draw_name(img)
        
        draw_mrn = Drawing()
        draw_mrn.text_alignment = 'left'
        draw_mrn.font = './Roboto-Medium.ttf'
        draw_mrn.font_size = 26
        draw_mrn.text(int(res * 0.1), int(res * 0.5), f"MRN: {milm_config.MRN}")
        draw_mrn(img)
        
        draw_csn = Drawing()
        draw_csn.text_alignment = 'left'
        draw_csn.font = './Roboto-Medium.ttf'
        draw_csn.font_size = 26
        draw_csn.text(int(res * 0.1), int(res * 0.6), f"CSN: {milm_config.CSN}")
        draw_csn(img)
        
        draw_dob = Drawing()
        draw_dob.text_alignment = 'left'
        draw_dob.font = './Roboto-Medium.ttf'
        draw_dob.font_size = 26
        draw_dob.text(int(res * 0.1), int(res * 0.7), f"DOB: [{milm_config.DOB}]")
        draw_dob(img)
        
        draw_contents = Drawing()
        draw_contents.text_alignment = 'right'
        draw_contents.font = './Roboto-Medium.ttf'
        draw_contents.font_size = 32
        draw_contents.text(int(img.width-res * 0.1), int(res * 0.4), f"{milm_config.CONTENTS}")
        draw_contents(img)
        
        draw_dt = Drawing()
        draw_dt.text_alignment = 'right'
        draw_dt.font = './Roboto-Medium.ttf'
        draw_dt.font_size = 26
        draw_dt.text(int(img.width-res * 0.1), int(res * 0.55), "Date/Time Pumped:")
        draw_dt(img)
        
        draw_contents = Drawing()
        draw_contents.text_alignment = 'right'
        draw_contents.font = './Roboto-Medium.ttf'
        draw_contents.font_size = 32
        draw_contents.text(int(img.width-res * 0.1), int(res * 0.7), now)
        draw_contents(img)
        
        az_bc = treepoem.generate_barcode(
            barcode_type = "azteccode",
            data = milm_config.BARCODE_DATA,
            )
        
        csn_bc = treepoem.generate_barcode(
            barcode_type = "code128",
            data = milm_config.CSN,
            )
        
        
        az_bc.save('aztmp.png', format='PNG')
        draw_az = Drawing()
        az_bc_w = Image(filename='aztmp.png')
        az_bc_w.resize(width=int(az_bc_w.width*1.4), height=int(az_bc_w.height*1.4), filter='point')
        draw_az.composite(operator='atop', left=int(img.width*0.8), top=int(res*0.8),
            width=az_bc_w.width, height=az_bc_w.height, image=az_bc_w)
        draw_az(img)
        
        csn_bc.save('csntmp.png', format='PNG')
        draw_csnbc = Drawing()
        csn_bc_w = Image(filename='csntmp.png')
        csn_bc_w.resize(width=int(csn_bc_w.width * 2.3), height=int(csn_bc_w.height), filter='point')
        draw_csnbc.composite(operator='atop', left=int(img.width*0.02), top=int(res*0.8),
            width=csn_bc_w.width, height=csn_bc_w.height, image=csn_bc_w)
        draw_csnbc(img)
        

        img.save(filename='temp.png')
        subprocess.run(
            ["brother_ql_create --model QL-800 --label-size 62 ./temp.png > labelout.bin"],
            shell=True, check=False)
        subprocess.run([f"brother_ql_print labelout.bin {milm_config.PRINTER_IDENTIFIER}"],
            shell=True, check=False)
        os.remove('temp.png')
        os.remove('aztmp.png')
        os.remove('csntmp.png')
        os.remove('labelout.bin')

if __name__ == "__main__":
    while True:
        print("Press any key to make a label.")
        key = readchar.readchar()
        if key == readchar.key.CTRL_C:
            exit(0)
        make_label()

