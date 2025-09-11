import numpy as np
import torch
from .base_policy import Policy

from tdeployBooster.core.controller.base_controller import Controller
from deploylib.deploy_manager import DeployManager

from deploylib.deploy_manager import DeployManager, MotionBufferCfg

from tdeployBooster.basic.joint_names.booster_k1 import LAB_JOINT_NAMES, MUJOCO2LAB_CAST, LAB2MUJOCO_CAST
from tdeployBooster.basic.motion_align.booster_k1 import K1_MOTION_ALIGN_CFG

default_qpos = [
    0.0,  0.0,
    0.25, -1.4, 0.0, -0.5,
    0.25, 1.4, 0.0, 0.5,
    -0.1, 0.0, 0.0, 0.2, -0.1, 0.0,
    -0.1, 0.0, 0.0, 0.2, -0.1, 0.0,
]
default_qpos = np.array(default_qpos)

class WholeBodyPolicy(Policy):
    
    def __init__(self, cfg):
        self.device = "cpu"
        super().__init__(cfg)
        self.obs_base_repeat = 5

        
        self.obs_scales = [
            0.25,
            1.0,
            1.0,
            0.05,
            1.0
        ]

        self.obs = None
            
    def _init_inference_variables(self):
        super()._init_inference_variables()
        self.action_scale = self.cfg["policy"]["control"]["action_scale"]
        
        cfg = MotionBufferCfg(
            regen_pkl=False,
            motion_type="GMR",
            motion_name="amass/booster_k1/deploy.yaml",
            motion_lib_type="MotionLibDofPos"
        )
        
        self.manager = DeployManager(
            motion_buffer_cfg=cfg,
            motion_align_cfg=K1_MOTION_ALIGN_CFG,
            lab_joint_names=LAB_JOINT_NAMES,
            robot_type="k1",
            dt=self.policy_interval,
            device=self.device
        )
        
    def update(self):
        is_update = self.manager.step()
        if torch.any(is_update):
            print("Motion updated.")
            self.manager.set_finite_state_machine_motion_ids(
                motion_ids=torch.tensor([1], device=self.device, dtype=torch.long)
            )
        
    def construct_obs(self, cli: Controller):

        motions_terms = [
            self.manager.loc_dof_pos.reshape(-1),
            self.manager.loc_root_vel.reshape(-1),
        ]

        base_terms = [
            cli.base_ang_vel,
            cli.projected_gravity,
            cli.dof_pos[MUJOCO2LAB_CAST],
            cli.dof_vel[MUJOCO2LAB_CAST],
            self.actions,
        ]
        
        base_terms = [ term * fac for term, fac in zip(base_terms, self.obs_scales)]
        # base_terms = [ np.concatenate([term] * self.obs_base_repeat, axis=-1) for term in base_terms]

        self.obs = np.concatenate(motions_terms + base_terms, axis=-1).reshape(-1)
        return self.obs
    
    def inference(self, cli: Controller, **kwargs):
        # Construct Obs
        
        self.construct_obs(cli=cli)
        
        self.actions[:] = self.policy(torch.from_numpy(self.obs).unsqueeze(0)).detach().numpy()
        
        # self.actions *= 0
        # self.actions[:] = self.actions

        self.actions[:] = np.clip(
            self.actions,
            -self.cfg["policy"]["normalization"]["clip_actions"],
            self.cfg["policy"]["normalization"]["clip_actions"],
        )
        # self.dof_targets[:] = self.default_dof_pos
        self.dof_targets[:22] = self.actions[LAB2MUJOCO_CAST]  * self.action_scale

        # self.dof_targets[3] = default_qpos[3]
        # self.dof_targets[7] = default_qpos[7]
        
        return self.dof_targets