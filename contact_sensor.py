import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path(
    "/home/krishna/epa_twin_project/urdf/robot.urdf"
)

data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running():

        mujoco.mj_step(model, data)

        print(
            f"Contacts: {data.ncon}",
            end="\r"
        )

        viewer.sync()
