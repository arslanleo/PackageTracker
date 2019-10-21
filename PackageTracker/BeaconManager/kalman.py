class SingleStateKalmanFilter(object):

    def __init__(self, A=1, B=0, C=1, x=0, P=0.005, Q=0.00001, R=0.01):
        self.A = A  # Process dynamics
        self.B = B  # Control dynamics
        self.C = C  # Measurement dynamics
        self.current_state_estimate = x  # Current state estimate
        self.current_prob_estimate = P  # Current probability of state estimate
        self.Q = Q  # Process covariance
        self.R = R  # Measurement covariance

    def current_state(self):
        return self.current_state_estimate

    def step(self, control_input, measurement):
        # Prediction step
        predicted_state_estimate = self.A * self.current_state_estimate + self.B * control_input
        predicted_prob_estimate = (self.A * self.current_prob_estimate) * self.A + self.Q

        # Observation step
        innovation = measurement - self.C * predicted_state_estimate
        innovation_covariance = self.C * predicted_prob_estimate * self.C + self.R

        # Update step
        kalman_gain = predicted_prob_estimate * self.C * 1 / float(innovation_covariance)
        self.current_state_estimate = predicted_state_estimate + kalman_gain * innovation

        # eye(n) = nxn identity matrix.
        self.current_prob_estimate = (1 - kalman_gain * self.C) * predicted_prob_estimate