import tkinter as tk
from tkinter import ttk

def validate_positive_float(value):
    """Check if the value is a positive float."""
    try:
        float_val = float(value)
        return float_val > 0
    except ValueError:
        return False

def validate_bezier_point(value):
    """Validate bezier control point is between 0 and 1."""
    try:
        float_val = float(value)
        return 0 <= float_val <= 1
    except ValueError:
        return False

def cubic_bezier(t, p0, p1, p2, p3):
    """Calculate position on a cubic bezier curve."""
    u = 1 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    p = uuu * p0 + 3 * uu * t * p1 + 3 * u * tt * p2 + ttt * p3
    return p

def adjust_timing_with_bezier(timings, p1, p2, animation_length):
    """Adjust frame timings using a cubic bezier curve."""
    adjusted_timings = []
    for start_time, end_time in timings:
        t_start = start_time / animation_length
        t_end = end_time / animation_length
        adjusted_start = cubic_bezier(t_start, 0, p1, p2, 1)
        adjusted_end = cubic_bezier(t_end, 0, p1, p2, 1)
        adjusted_timings.append((adjusted_start * animation_length, adjusted_end * animation_length))
    return adjusted_timings

class AnimationToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tower Unite Animation Tool")
        self.geometry("500x400")

        # Frame Rate
        ttk.Label(self, text="Frame Rate (FPS):").grid(column=0, row=0, padx=10, pady=10)
        self.frame_rate = ttk.Entry(self)
        self.frame_rate.grid(column=1, row=0)

        # Animation Length
        ttk.Label(self, text="Animation Length (seconds):").grid(column=0, row=1, padx=10, pady=10)
        self.animation_length = ttk.Entry(self)
        self.animation_length.grid(column=1, row=1)

        # Frame Duration
        ttk.Label(self, text="Frame Duration (seconds):").grid(column=0, row=2, padx=10, pady=10)
        self.frame_duration = ttk.Entry(self)
        self.frame_duration.grid(column=1, row=2)

        # Easing Preset
        ttk.Label(self, text="Easing Preset:").grid(column=0, row=3, padx=10, pady=10)
        self.easing_preset = ttk.Combobox(self, values=["Ease In", "Ease Out", "Ease In-Out", "Custom"])
        self.easing_preset.grid(column=1, row=3)
        self.easing_preset.bind('<<ComboboxSelected>>', self.on_preset_selected)

        # Custom Bezier Controls
        self.custom_bezier_frame = ttk.LabelFrame(self, text="Custom Bezier Controls")
        self.custom_bezier_frame.grid(column=0, row=4, columnspan=2, pady=10, padx=10, sticky="ew")
        ttk.Label(self.custom_bezier_frame, text="P1:").grid(column=0, row=0, padx=10, pady=5)
        self.p1 = ttk.Entry(self.custom_bezier_frame)
        self.p1.grid(column=1, row=0)
        ttk.Label(self.custom_bezier_frame, text="P2:").grid(column=2, row=0, padx=10, pady=5)
        self.p2 = ttk.Entry(self.custom_bezier_frame)
        self.p2.grid(column=3, row=0)
        self.custom_bezier_frame.grid_remove()

        # Calculate Button
        self.calculate_button = ttk.Button(self, text="Calculate", command=self.calculate)
        self.calculate_button.grid(column=0, row=5, columnspan=2, pady=10)

    def on_preset_selected(self, event):
        if self.easing_preset.get() == "Custom":
            self.custom_bezier_frame.grid()
        else:
            self.custom_bezier_frame.grid_remove()

    def calculate(self):
        frame_rate = float(self.frame_rate.get())
        animation_length = float(self.animation_length.get())
        frame_duration = float(self.frame_duration.get())
        p1 = float(self.p1.get()) if self.p1.get() and self.easing_preset.get() == "Custom" else 0.25
        p2 = float(self.p2.get()) if self.p2.get() and self.easing_preset.get() == "Custom" else 0.75
        object_timings = adjust_timing_with_bezier(
            [(i / frame_rate, min((i / frame_rate) + frame_duration, animation_length)) for i in range(int(frame_rate * animation_length))],
            p1, p2, animation_length)
        self.display_results(object_timings)

    def display_results(self, object_timings):
        results_text = f"Total Objects: {len(object_timings)}\n\nTimings:\n"
        for i, (start, end) in enumerate(object_timings):
            results_text += f"Object {i+1}: Unhide at {start:.2f}s, Hide at {end:.2f}s\n"
        print(results_text)  # Ideally, display this in the GUI

if __name__ == "__main__":
    app = AnimationToolApp()
    app.mainloop()
