import mujoco
import mujoco.viewer
import csv
import time

model = mujoco.MjModel.from_xml_path(
    "/home/krishna/epa_twin_project/urdf/robot.urdf"
)

data = mujoco.MjData(model)

foot_id = mujoco.mj_name2id(
    model,
    mujoco.mjtObj.mjOBJ_BODY,
    "leg_stack_v1_1"
)

f = open("foot_trajectory.csv", "w", newline="")
writer = csv.writer(f)
writer.writerow(["time", "x", "y", "z"])

start = time.time()

with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running():

        mujoco.mj_step(model, data)

        x, y, z = data.xpos[foot_id]

        writer.writerow([
            time.time() - start,
            x,
            y,
            z
        ])

        viewer.sync()

f.close()
