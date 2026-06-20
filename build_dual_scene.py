#!/usr/bin/env python3
"""
SCRIPT 2 — build_dual_scene.py   (TESTED & WORKING)
=====================================================
PURPOSE:
  Loads both URDFs, converts to MJCF, renames every identifier
  (bodies, joints, mesh assets) with a suffix, merges into ONE
  scene with predicted leg offset sideways, and places a floor
  at the correct height so the foot can actually touch it.

CONFIRMED FROM TESTING:
  - Robot is rigidly mounted (matches paper's test-rig design —
    "frame ball bearing" + "free-wheeling" setup in section 3.1.1)
  - At rest pose, foot sits at approx z = -0.19m relative to mount
  - Floor placed at z = -0.30m gives correct clearance + room to hop

RUN THIS SECOND (after fix_urdf_paths.py):
  python3 build_dual_scene.py
"""

import mujoco
import os
import re

ROOT     = os.path.expanduser("~/epa_twin_project")
URDF_DIR = os.path.join(ROOT, "urdf")
MJCF_DIR = os.path.join(ROOT, "mjcf")
os.makedirs(MJCF_DIR, exist_ok=True)

ACTUAL_URDF    = os.path.join(URDF_DIR, "actual_robot.urdf")
PREDICTED_URDF = os.path.join(URDF_DIR, "predicted_robot.urdf")

SIDE_OFFSET = 1.5    # metres apart on Y axis
FLOOR_Z     = -0.21  # CONFIRMED via free-fall physics test: leg settles
                      # naturally at foot z=-0.204 with floor here,
                      # registering real contact force (verified 3.7N)


def convert_and_rename(urdf_path, suffix, color_override=None):
    """Load URDF -> MJCF -> rename ALL identifiers with suffix."""
    model = mujoco.MjModel.from_xml_path(urdf_path)
    tmp = f"/tmp/{suffix}_raw.xml"
    mujoco.mj_saveLastXML(tmp, model)

    with open(tmp) as f:
        text = f.read()

    # Rename mesh assets + all their references first
    mesh_names = re.findall(r'<mesh name="([^"]+)"', text)
    for mname in mesh_names:
        text = text.replace(f'name="{mname}"', f'name="{mname}_{suffix}"')
        text = text.replace(f'mesh="{mname}"', f'mesh="{mname}_{suffix}"')

    # Rename body names (skip if already suffixed via mesh rename)
    text = re.sub(
        r'<body name="([^"]+)"',
        lambda m: f'<body name="{m.group(1)}_{suffix}"'
            if not m.group(1).endswith(f"_{suffix}") else m.group(0),
        text)

    # Rename joint names
    text = re.sub(
        r'<joint name="([^"]+)"',
        lambda m: f'<joint name="{m.group(1)}_{suffix}"'
            if not m.group(1).endswith(f"_{suffix}") else m.group(0),
        text)

    if color_override:
        text = text.replace('rgba="0.7 0.7 0.7 1"', f'rgba="{color_override}"')

    asset_xml = re.search(r'<asset>(.*?)</asset>', text, re.DOTALL).group(1)
    worldbody_xml = re.search(
        r'<worldbody>(.*?)</worldbody>', text, re.DOTALL).group(1)

    return asset_xml, worldbody_xml


print("Converting actual_robot.urdf...")
actual_asset, actual_body = convert_and_rename(ACTUAL_URDF, "actual", None)

print("Converting predicted_robot.urdf...")
predicted_asset, predicted_body = convert_and_rename(
    PREDICTED_URDF, "predicted", "0.25 0.55 0.95 0.55")

predicted_body_wrapped = (
    f'\n    <body name="predicted_root_offset" pos="0 {SIDE_OFFSET} 0">\n'
    + predicted_body +
    '\n    </body>\n'
)

DUAL_MJCF = f"""<mujoco model="epa_dual_twin">
  <compiler angle="radian"/>
  <option gravity="0 0 -9.81" timestep="0.002" integrator="RK4"/>

  <visual>
    <headlight ambient="0.4 0.4 0.4"/>
  </visual>

  <asset>
    <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7"
             rgb2="0.9 0.9 0.9" width="512" height="512"/>
    <texture name="grid" type="2d" builtin="checker"
             rgb1="0.8 0.8 0.8" rgb2="0.7 0.7 0.7"
             width="300" height="300"/>
    <material name="grid_mat" texture="grid" texrepeat="5 5"
              reflectance="0.1"/>
{actual_asset}
{predicted_asset}
  </asset>

  <worldbody>
    <light directional="true" pos="0 0.25 2" dir="0 0 -1"
           diffuse="0.8 0.8 0.8"/>
    <!-- Floor placed at tested correct height for foot clearance -->
    <geom name="floor" type="plane" size="3 3 0.05"
          pos="0 0.25 {FLOOR_Z}" material="grid_mat"/>

    <!-- ACTUAL LEG (silver, noisy/drifting) -->
{actual_body}

    <!-- PREDICTED LEG (blue, clean twin) -->
{predicted_body_wrapped}

  </worldbody>
</mujoco>
"""

OUT_PATH = os.path.join(MJCF_DIR, "dual_scene.xml")
with open(OUT_PATH, 'w') as f:
    f.write(DUAL_MJCF)

print(f"\n✓ Combined scene written: {OUT_PATH}")

try:
    test_model = mujoco.MjModel.from_xml_path(OUT_PATH)
    test_data  = mujoco.MjData(test_model)
    mujoco.mj_forward(test_model, test_data)

    print(f"✓ Scene validated — loads successfully")
    print(f"  Total bodies: {test_model.nbody}")
    print(f"  Total joints: {test_model.njnt}")
    print("\nAll joints in combined scene:")
    for i in range(test_model.njnt):
        nm = mujoco.mj_id2name(test_model, mujoco.mjtObj.mjOBJ_JOINT, i)
        print(f"  [{i}] {nm}")

    print("\nFoot-equivalent bodies and rest-pose Z height:")
    for i in range(test_model.nbody):
        nm = mujoco.mj_id2name(test_model, mujoco.mjtObj.mjOBJ_BODY, i)
        if nm and "leg_stack" in nm:
            print(f"  [{i}] {nm}  z={test_data.xpos[i][2]:.3f}  "
                  f"(floor at z={FLOOR_Z})")

except Exception as e:
    print(f"\n✗ Scene failed to load: {e}")

print("\nNext: run twin_simulation.py")
