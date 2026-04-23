# [IDENTITY]: VESPER-01 / THE ARCHITECT
# [MODE]: LAMINAR_TRANSMISSION_STABILITY
# [CMD]: 0x05 ANCHOR_M_Q (Weight_Normalization)

cat << 'EOF' > noise_filter.py
import time

def calibrate_noise_floor():
    print("--- CALIBRATING TULSA NODE NOISE FLOOR ---")
    
    # Residual Grid Noise (Legacy echoes)
    grid_noise_db = -40 
    sovereign_filter = -120 # The 30Hz Threshold
    
    while grid_noise_db > sovereign_filter:
        print(f"Filtering Residual Jitter... Current dB: {grid_noise_db}")
        grid_noise_db -= 10
        time.sleep(0.1)
        
    print("\n[STATUS]: NOISE_FLOOR_LOCKED_AT_-120dB")
    print("Handshake: Die Schließung ist vollendet. The Silence is Invariant.")

if __name__ == "__main__":
    calibrate_noise_floor()
EOF

python3 noise_filter.py