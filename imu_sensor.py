import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path(
    "/home/krishna/epa_twin_project/urdf/robot.urdf"
)

data = mujoco.MjData(model)

body_id = 3

with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running():

        mujoco.mj_step(model, data)

        print(
            "Angular Velocity:",
            data.cvel[body_id][:3],
            end="\r"
        )

        viewer.sync()
