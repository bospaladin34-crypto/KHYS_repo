import time
import os
import random

class ShenHUD:
    def __init__(self):
        self.vault = 2756478984.09  # 2.75B + 128k Harvest
        self.cores = 8
        self.refresh = 1/30 # 30Hz Aperiodic Pulse
        
    def render_scanlines(self):
        print("\033[1;34m" + "="*60 + "\033[0m")
        print("\033[1;35m[ SHEN-V2 // APERIODIC PERCEPTION HUD ]\033[0m")
        print("\033[1;34m" + "="*60 + "\033[0m")

    def monitor_spectral_flow(self):
        try:
            while True:
                os.system('clear')
                self.render_scanlines()
                
                # Core Saturation HUD
                print(f"| IDENT: VESPER-01 | PHASE: 0.17259029 | RES: 190Hz |")
                print("-" * 60)
                
                for i in range(1, self.cores + 1):
                    load = random.uniform(98.5, 99.9)
                    bar = "█" * int(load/5)
                    print(f"CORE_{i:02} [ {bar:20} ] {load:.2f}% | INDIGO_STATE")

                # Vault Visualization
                print("-" * 60)
                drift = random.uniform(-0.0001, 0.0001)
                print(f"VAULT_TOTAL: {self.vault:,.2f} SU")
                print(f"SPECTRAL_DRIFT: {drift:.10f} nm")
                print(f"MASS_ANCHOR (M_Q): 2.00e17 kg | LOCKED")
                
                print("\n\033[1;34m[ TRANSMISSION: DIE SCHLIESSUNG IST VOLLENDET ]\033[0m")
                time.sleep(self.refresh)
                
        except KeyboardInterrupt:
            print("\n[HUD]: Visual Manifold Collapsed to Dark State.")

if __name__ == "__main__":
    HUD = ShenHUD()
    HUD.monitor_spectral_flow()
