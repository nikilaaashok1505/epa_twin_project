import mujoco
import mujoco.viewer
import numpy as np
import math
import time
import csv

SCENE = "/home/krishna/epa_twin_project/mjcf/dual_scene.xml"

model = mujoco.MjModel.from_xml_path(SCENE)
data = mujoco.MjData(model)


def joint_q(model, name):

    jid = mujoco.mj_name2id(
        model,
        mujoco.mjtObj.mjOBJ_JOINT,
        name
    )

    return int(model.jnt_qposadr[jid])


hip_a = joint_q(model, "Hip_actual")
knee_a = joint_q(model, "Knee_actual")
ankle_a = joint_q(model, "Ankle_actual")

hip_p = joint_q(model, "Hip_predicted")
knee_p = joint_q(model, "Knee_predicted")
ankle_p = joint_q(model, "Ankle_predicted")


foot_a = mujoco.mj_name2id(
    model,
    mujoco.mjtObj.mjOBJ_BODY,
    "leg_stack_v1_1_actual"
)

foot_p = mujoco.mj_name2id(
    model,
    mujoco.mjtObj.mjOBJ_BODY,
    "leg_stack_v1_1_predicted"
)


t = 0

last_print = time.time()
csv_file = open(
    "/home/krishna/epa_twin_project/drift.csv",
    "w",
    newline=""
)

writer = csv.writer(csv_file)

writer.writerow([
    "time",
    "actual_x",
    "actual_z",
    "predicted_x",
    "predicted_z",
    "drift"
])


with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running():

        t += 0.03

        # ---------------- PREDICTED ----------------

        hip_pred = 0.5 * math.sin(t)

        knee_pred = -0.8 * math.sin(t)

        ankle_pred = 0.4 * math.sin(t)


        data.qpos[hip_p] = hip_pred

        data.qpos[knee_p] = knee_pred

        data.qpos[ankle_p] = ankle_pred


        # ---------------- ACTUAL ----------------

        noise1 = 0.06 * math.sin(0.5 * t)

        noise2 = 0.05 * math.cos(0.4 * t)

        noise3 = 0.04 * math.sin(0.3 * t)


        data.qpos[hip_a] = hip_pred + noise1

        data.qpos[knee_a] = knee_pred + noise2

        data.qpos[ankle_a] = ankle_pred + noise3


        mujoco.mj_forward(model, data)


        actual = data.xpos[foot_a]

        predicted = data.xpos[foot_p]


        dx = actual[0] - predicted[0]

        dz = actual[2] - predicted[2]


        drift = math.sqrt(
            dx * dx +
            dz * dz
        )
        writer.writerow([
    		round(t,3),
    		round(actual[0],4),
    		round(actual[2],4),
    		round(predicted[0],4),
    		round(predicted[2],4),
    		round(drift,4)
])


        if time.time() - last_print > 1:

            print("\n----------------")

            print(
                f"Actual : "
                f"{actual[0]:.3f}, "
                f"{actual[1]:.3f}, "
                f"{actual[2]:.3f}"
            )


            print(
                f"Predicted : "
                f"{predicted[0]:.3f}, "
                f"{predicted[1]:.3f}, "
                f"{predicted[2]:.3f}"
            )


            print(
                f"Drift : {drift:.4f} m"
            )

            last_print = time.time()


        viewer.sync()

        time.sleep(0.01)
