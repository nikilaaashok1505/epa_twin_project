import shutil
import os

ROOT = os.path.expanduser("~/epa_twin_project")

src = ROOT + "/mjcf/dual_scene.xml"
dst = ROOT + "/mjcf/four_leg_scene.xml"

shutil.copy(src,dst)

with open(dst,"r") as f:
    txt = f.read()


old = '''
<body name="predicted_root_offset" pos="0 1.5 0">
'''

new = '''
<body name="actual_right_offset" pos="0 -0.5 0">

<body name="predicted_root_offset" pos="0 1.5 0">

<body name="predicted_right_offset" pos="0 2.0 0">
'''

txt = txt.replace(old,new)

with open(dst,"w") as f:
    f.write(txt)

print("four_leg_scene.xml created")
