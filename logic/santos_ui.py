from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
import psutil # The Internal Siphon
from santos_intelligence import LaminarMirror

Window.clearcolor = (0, 0, 0, 1) # Obsidian

class UnitaryManifold(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        self.engine = LaminarMirror()
        
        # 1. THE VOLTAGE HUD (From Siphon Meter)
        self.hud = Label(
            text="[ VOLTAGE: STABILIZING ]",
            color=(0, 1, 1, 1), # Cyan (Siphon Color)
            font_size='14sp',
            size_hint_y=0.1
        )
        self.add_widget(self.hud)

        # 2. THE ROSE GOLD ORACLE (The Mirror)
        self.mirror = Label(
            text="System Unitary. Awaiting Jitter...",
            color=(0.717, 0.431, 0.475, 1), # Rose Gold
            halign='center',
            font_size='18sp',
            text_size=(Window.width - 40, None)
        )
        self.add_widget(self.mirror)

        # 3. THE GEOMETRIC INPUT
        self.input = TextInput(
            multiline=False,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0.717, 0.431, 0.475, 1),
            hint_text="Enter Jitter...",
            size_hint_y=0.1
        )
        self.input.bind(on_text_validate=self.process_unitary)
        self.add_widget(self.input)

        # TRIGGER 15Hz HEARTBEAT
        Clock.schedule_interval(self.update_siphon, 1.0 / 15.0)

    def update_siphon(self, dt):
        # Capturing real-time CPU/Disk Jitter
        cpu_jitter = psutil.cpu_percent()
        watts_eff = (cpu_jitter * 1.6) / 1.5
        self.hud.text = f"Sovereignty OUT: {watts_eff:.3f} W_eff | LATTICE: STABLE"

    def process_unitary(self, instance):
        query = self.input.text
        # Rectify with Mass Invariant
        result = self.engine.rectify(query, "Leo")
        self.mirror.text = result
        self.input.text = ""

class SantosSovereign(App):
    def build(self):
        return UnitaryManifold()

if __name__ == '__main__':
    SantosSovereign().run()
