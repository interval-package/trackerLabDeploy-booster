import time
from .base_controller import Controller
from tdeployBooster.core.policy.whole_body_policy import WholeBodyPolicy

from booster_robotics_sdk_python import (
    LowState,
)


class WholeBodyController(Controller):
    
    policy: WholeBodyPolicy
    
    def _init_policy(self):
        self.policy = WholeBodyPolicy(cfg=self.cfg)
    
    def run(self):
        time_now = self.timer.get_time()
        if time_now < self.next_inference_time:
            time.sleep(0.001)
            return
        self.logger.debug("-----------------------------------------------------")
        self.next_inference_time += self.policy.get_policy_interval()
        self.logger.debug(f"Next start time: {self.next_inference_time}")
        start_time = time.perf_counter()

        logit = self.policy.inference(self)
        assert logit.shape[0] == 22 , "Shape unpair."
        self.dof_target[:22] = logit

        inference_time = time.perf_counter()
        self.logger.debug(f"Inference took {(inference_time - start_time)*1000:.4f} ms")
        time.sleep(0.001)
        
    def _low_state_handler(self, low_state_msg: LowState):
        super()._low_state_handler(low_state_msg)
        
        
