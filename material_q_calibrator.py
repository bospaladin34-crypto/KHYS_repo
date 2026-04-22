# [PROTOCOL: OMEGA-SANTOS-ULTIMATE]
# [COMPONENT: MATERIAL_QUALITY_CALIBRATOR]
# [IDENTITY: bospaladin34-crypto]

def evaluate_material(name, q_factor):
    print(f"Die Ausstrahlung hat begonnen. Evaluating {name}...")
    
    # Threshold for the Santos Protocol is a Q-Factor > 10.0
    santos_threshold = 10.0
    
    if q_factor >= santos_threshold:
        print(f"[VERIFIED]: {name} (Q={q_factor}) is LAMINAR.")
        return True
    else:
        print(f"[REJECTED]: {name} (Q={q_factor}) is GRID_PARASITE noise.")
        return False

if __name__ == "__main__":
    # Testing our BOM
    evaluate_material("Fused Silica Spine", 144.0)
    evaluate_material("Standard Copper Wire", 2.5) # Will be rejected
    evaluate_material("REBCO Superconductor", 88.0)
