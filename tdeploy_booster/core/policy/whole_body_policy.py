import numpy as np
import torch
from .policy_base import Policy

class WholeBodyPolicy(Policy):
    
    def __init__(self, cfg):
        super().__init__(cfg)
    
    def _init_inference_variables(self):
        super()._init_inference_variables()