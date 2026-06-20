import mujoco
import mujoco.viewer
import math
import time

model = mujoco.MjModel.from_xml_path(
    "/home/krishna/epa_twin_project/urdf/robot.urdf"
)

data = mujoco.MjData(model)

t = 0.0

with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running():

        t += 0.03

        # Hip
        data.qpos[0] = 0.5 * math.sin(t)

        # Knee
        data.qpos[1] = -0.8 * math.sin(t)

        # Ankle
        data.qpos[2] = 0.4 * math.sin(t)

        mujoco.mj_step(model, data)

        viewer.sync()

        time.sleep(0.01)
