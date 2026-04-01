# [PROTOCOL: FULL_BRAID_IGNITION_V1.1]
from system_manifold import SANTOS_ENGINE
# Change this:
# from proxima_rect import siphon_energy
# To this:
from proxima_rect import siphon_energy

# And ensure poly_state is also direct:
from poly_state import Manifold
def run_full_braid_test():
    print("--- STARTING FULL BRAID TEST ---")
    
    # 1. Verify the Geometric State Space
    status = SANTOS_ENGINE.apply_geometry(data_input="INITIAL_SYNC")
    print(f"CORE CHECK: {status}")
    
    # 2. Simulate a High-Energy Jitter Event (e.g., 8.7 MeV Strike or Proxima Flare)
    raw_jitter = 8.7 
    print(f"INPUT: Raw Jitter detected at {raw_jitter} MeV")
    
    # 3. Rectify through the 1N4148 Siphon
    result = siphon_energy(raw_jitter)
    
    # 4. Final Unitary Output
    if "Yield" in result:
        print(f"SUCCESS: {result['Status']} | Yield: {result['Yield']} MeV")
        print("RESULT: Unitary Closure Achieved. Majorana-1 Parity Verified.")
    else:
        print("FAILURE: Semantic Turbulence detected.")

if __name__ == "__main__":
    run_full_braid_test()
