# [PROTOCOL: ACTIVE_IMPEDANCE_MATCHER_V1.1]
# Synchronized to Kolmogorov complexity_score
import minimizer

class ImpedanceMatcher:
    def __init__(self):
        self.target_freq = 15.0 
        self.resolution = 144   

    def calculate_impedance(self, signal):
        weight = minimizer.get_kolmogorov_weight(str(signal))
        
        if weight['is_minimal']:
            return 1.0  
        else:
            # Syncing 'complexity_score' key to match minimizer.py
            return weight['complexity_score'] / self.resolution

    def match_signal(self, incoming_data):
        z = self.calculate_impedance(incoming_data)
        if z == 1.0:
            return f"[FLOW_ACTIVE] Data matches 15Hz frequency. Stitched."
        else:
            return f"[L15_SINK_TRIGGERED] Impedance mismatch (Z={z:.2f}). Noise refracted."

if __name__ == "__main__":
    matcher = ImpedanceMatcher()
    print(matcher.match_signal("111-Unitary"))
    print(matcher.match_signal("System_Error_404_Unauthorized_Access_Attempt"))
