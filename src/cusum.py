import numpy as np

class CusumDetector:
    def __init__(self, threshold=1):
        self.threshold = threshold
        self.cumulative_sum = 0

    def detect(self, data):
        alarms = np.zeros(len(data), dtype=bool)
        for i in range(len(data)):
            self.cumulative_sum = max(0, self.cumulative_sum + data[i] - self.threshold)
            if self.cumulative_sum >= self.threshold:
                alarms[i] = True
                self.cumulative_sum = 0
        return alarms


