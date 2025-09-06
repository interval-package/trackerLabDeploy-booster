import time
from .base_controller import Controller
from tdeployBooster.core.policy.motion_replay_policy_GMR import MotionReplayPolicy


class ReplayController(Controller):
    
    policy: MotionReplayPolicy
    
    def _init_policy(self):
        self.policy = MotionReplayPolicy(cfg=self.cfg)
    
    def run(self):
        time_now = self.timer.get_time()
        if time_now < self.next_inference_time:
            time.sleep(0.001)
            return
        self.logger.debug("-----------------------------------------------------")
        self.next_inference_time += self.policy.get_policy_interval()
        self.logger.debug(f"Next start time: {self.next_inference_time}")
        start_time = time.perf_counter()

        logit = self.policy.inference()
        assert logit.shape[0] == 22 , "Shape unpair."
        self.dof_target[:] = logit

        inference_time = time.perf_counter()
        self.logger.debug(f"Inference took {(inference_time - start_time)*1000:.4f} ms")
        time.sleep(0.001)
