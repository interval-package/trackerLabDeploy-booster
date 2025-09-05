import pickle
import math
import numpy as np
from dataclasses import dataclass

from tdeploy_booster.basic.joint_names.booster_k1 import MUJOCO2REAL_CAST
from .base_policy import Policy

@dataclass
class GMRMotionData:
    dof_poses: np.ndarray
    fps: float
    max_time: float
    
    @property
    def dt(self):
        return 1 / self.fps
    
    @property
    def length(self):
        return self.dof_poses.shape[0]
    
    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path, "rb") as f:
            data = pickle.load(f)
            
        fps = data["fps"]
        root_pos = np.array(data["root_pos"])
        root_rot = np.array(data["root_rot"])
        dof_pos = np.array(data["dof_pos"])
        local_body_pos = np.array(data["local_body_pos"])
            
        return cls(
            dof_pos, fps, dof_pos.shape[0] / fps
        )
        
    def dof_pos_at_time(self, time: float):
        frame = time * self.fps
        idx_l, idx_u = math.min(math.floor(frame), self.length), math.min(math.ceil(frame), self.length)
        blend = frame - idx_l
        tar_dof_pos:np.ndarray = self.dof_poses[idx_l] * blend + self.dof_poses[idx_u] * (1 - blend)
        tar_dof_pos = tar_dof_pos.reshape(-1)
        return tar_dof_pos[MUJOCO2REAL_CAST]
    

class MotionReplayPolicy(Policy):
    
    def __init__(self, cfg):
        super().__init__(cfg)
        self.reset()
        self.data = GMRMotionData.from_file("./target.pkl")
        
    def reset(self):
        self.curr_time = 0
        
    def update(self):
        self.curr_time += self.policy_interval
        if self.curr_time > self.data.max_time:
            self.curr_time = self.data.max_time
    
    def inference(self, **kwargs):
        dof_pos = self.data.dof_pos_at_time(self.curr_time)
        self.dof_targets[:] = dof_pos
        self.update()
        return self.dof_targets[:]