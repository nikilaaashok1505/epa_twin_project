import mujoco
import mujoco.viewer
import math
import time


SCENE = "/home/krishna/epa_twin_project/mjcf/four_leg_scene.xml"

model = mujoco.MjModel.from_xml_path(SCENE)
data = mujoco.MjData(model)


def q(name):

    jid = mujoco.mj_name2id(
        model,
        mujoco.mjtObj.mjOBJ_JOINT,
        name
    )

    return int(model.jnt_qposadr[jid])



hipA=q("Hip_actual")
kneeA=q("Knee_actual")
ankleA=q("Ankle_actual")


hipP=q("Hip_predicted")
kneeP=q("Knee_predicted")
ankleP=q("Ankle_predicted")


t=0


with mujoco.viewer.launch_passive(model,data) as viewer:

    while viewer.is_running():

        t+=0.03


        h=0.5*math.sin(t)
        k=-0.8*math.sin(t)
        a=0.4*math.sin(t)


        data.qpos[hipP]=h
        data.qpos[kneeP]=k
        data.qpos[ankleP]=a


        data.qpos[hipA]=h+0.05*math.sin(0.5*t)
        data.qpos[kneeA]=k+0.05*math.cos(0.5*t)
        data.qpos[ankleA]=a+0.03*math.sin(0.3*t)


        mujoco.mj_forward(model,data)

        viewer.sync()

        time.sleep(0.01)
