REAL_JOINT_NAMES = [
    "Head_Yaw_Joint",
    "Head_Pitch_Joint",
    "Left_Shoulder_Pitch_Joint",
    "Left_Shoulder_Roll_Joint",
    "Left_Shoulder_Yaw_Joint",
    "Left_Elbow_Joint",
    "Right_Shoulder_Pitch_Joint",
    "Right_Shoulder_Roll_Joint",
    "Right_Shoulder_Yaw_Joint",
    "Right_Elbow_Joint",
    "Left_Hip_Pitch_Joint",
    "Left_Hip_Roll_Joint",
    "Left_Hip_Yaw_Joint",
    "Left_Knee_Joint",
    "Left_Ankle_Up_Joint",
    "Left_Ankle_Down_Joint",
    "Right_Hip_Pitch_Joint",
    "Right_Hip_Roll_Joint",
    "Right_Hip_Yaw_Joint",
    "Right_Knee_Joint",
    "Right_Ankle_Up_Joint",
    "Right_Ankle_Down_Joint",
]

REAL_JOINT_NAMES = [i.lower() for i in REAL_JOINT_NAMES]

LAB_JOINT_NAMES = [
    'Head_yaw_joint',
    'Left_Shoulder_Pitch_joint',
    'Right_Shoulder_Pitch_joint',
    'Left_Hip_Pitch_joint',
    'Right_Hip_Pitch_joint',
    'Head_pitch_joint',
    'Left_Shoulder_Roll_joint',
    'Right_Shoulder_Roll_joint',
    'Left_Hip_Roll_joint',
    'Right_Hip_Roll_joint',
    'Left_Elbow_Pitch_joint',
    'Right_Elbow_Pitch_joint',
    'Left_Hip_Yaw_joint',
    'Right_Hip_Yaw_joint',
    'Left_Elbow_Yaw_joint',
    'Right_Elbow_Yaw_joint',
    'Left_Knee_Pitch_joint',
    'Right_Knee_Pitch_joint',
    'Left_Ankle_Pitch_joint',
    'Right_Ankle_Pitch_joint',
    'Left_Ankle_Roll_joint',
    'Right_Ankle_Roll_joint',
]

LAB_JOINT_NAMES = [i.lower() for i in LAB_JOINT_NAMES]


MUJOCO_JOINT_NAMES = [ 
    'Head_yaw_joint', 
    'Head_pitch_joint', 
    'Left_Shoulder_Pitch_joint', 
    'Left_Shoulder_Roll_joint', 
    'Left_Elbow_Pitch_joint', 
    'Left_Elbow_Yaw_joint', 
    'ARight_Shoulder_Pitch_joint', 
    'Right_Shoulder_Roll_joint', 
    'Right_Elbow_Pitch_joint', 
    'Right_Elbow_Yaw_joint', 
    'Left_Hip_Pitch_joint', 
    'Left_Hip_Roll_joint', 
    'Left_Hip_Yaw_joint', 
    'Left_Knee_Pitch_joint', 
    'Left_Ankle_Pitch_joint', 
    'Left_Ankle_Roll_joint', 
    'Right_Hip_Pitch_joint', 
    'Right_Hip_Roll_joint', 
    'Right_Hip_Yaw_joint', 
    'Right_Knee_Pitch_joint', 
    'Right_Ankle_Pitch_joint', 
    'Right_Ankle_Roll_joint', 
]

LAB_JOINT_NAMES = [i.lower() for i in MUJOCO_JOINT_NAMES]

from .utils import get_indices

# LAB2REAL_CAST = get_indices(LAB_JOINT_NAMES, REAL_JOINT_NAMES, strict=True)
# MUJOCO2REAL_CAST = get_indices(MUJOCO_JOINT_NAMES, REAL_JOINT_NAMES, strict=True)

LAB2MUJOCO_CAST = get_indices(LAB_JOINT_NAMES, MUJOCO_JOINT_NAMES)
MUJOCO2LAB_CAST = get_indices(MUJOCO_JOINT_NAMES, LAB_JOINT_NAMES)
