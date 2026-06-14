import mujoco
import mujoco.viewer
import math
import time

model = mujoco.MjModel.from_xml_path(
    "/home/krishna/epa_twin_project/urdf/robot.urdf"
)

data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running():

        t = time.time()

        data.qpos[0] = 0.6 * math.sin(2*t)
        data.qpos[1] = -0.4 * math.sin(2*t)
        data.qpos[2] = 0.3 * math.sin(2*t)

        mujoco.mj_forward(model, data)

        viewer.sync()

        time.sleep(0.01)
