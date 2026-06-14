import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path(
    "/home/krishna/epa_twin_project/urdf/robot.urdf"
)

data = mujoco.MjData(model)

foot_id = mujoco.mj_name2id(
    model,
    mujoco.mjtObj.mjOBJ_BODY,
    "leg_stack_v1_1"
)

with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running():

        mujoco.mj_step(model, data)

        x, y, z = data.xpos[foot_id]

        print(
            f"Foot: X={x:.3f}  Y={y:.3f}  Z={z:.3f}",
            end="\r"
        )

        viewer.sync()
