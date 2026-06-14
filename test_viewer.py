import mujoco
import mujoco.viewer
import time
import math

model = mujoco.MjModel.from_xml_path(
    "/home/krishna/epa_twin_project/urdf/robot.urdf"
)

data = mujoco.MjData(model)

t = 0.0

with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running():

        data.qpos[0] = 0.3 * math.sin(t)
        data.qpos[1] = -0.2 * math.sin(t)
        data.qpos[2] = 0.15 * math.sin(t)

        mujoco.mj_forward(model, data)

        viewer.sync()

        t += 0.02

        time.sleep(0.01)
