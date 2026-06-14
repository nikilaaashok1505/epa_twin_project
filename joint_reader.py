import mujoco
import time

model = mujoco.MjModel.from_xml_path(
    "/home/krishna/epa_twin_project/urdf/robot.urdf"
)

data = mujoco.MjData(model)

while True:

    print(
        f"Hip={data.qpos[0]:.3f}",
        f"Knee={data.qpos[1]:.3f}",
        f"Ankle={data.qpos[2]:.3f}"
    )

    time.sleep(0.1)
