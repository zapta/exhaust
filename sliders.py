import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Button, Slider, TextBox, TransformedPatchPath


# Based on the example here:
# https://matplotlib.org/stable/gallery/widgets/slider_demo.html


def sum_magnitude(f: int, l: float) -> float:
    """Compute the gain for given frequency and pipe length"""
    # Delay in seconds for round trip in the pipe.
    dt = (2 * l) / SOUND_SPEED
    # Cycle time in secs.
    tcycle = 1 / f
    # Delta phase in radians.
    dphase = (2 * np.pi * dt) / tcycle
    # Compute the magnitude of the sum wave.
    magnitude = np.sqrt(2 + 2 * np.cos(dphase))
    assert isinstance(magnitude, float)
    # Normalize to max of 1.0.
    return magnitude / 2.0


STAGES = 3
INITIAL_LENGTHES = [23, 46, 90]

# The freq range [10, 1000] in step of 10
FREQS = np.arange(10, 1001, 10)

# Meter per second.
SOUND_SPEED = 343


# Create the figure and the line that we will manipulate
fig, graph_ax = plt.subplots(num="Supression Model", figsize=(12, 6))

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.06, right=0.95, bottom=0.45, top=0.9)

gain_sliders_ticks = np.linspace(0, 100, 101)

slider_pitch = 0.03
slider_width = 0.03
slider_bottom = 0.05
slider_height = 0.25


length_sliders = []
for i in range(STAGES):
    left_pos = 0.95 - ((STAGES - i) * slider_pitch)
    temp_axes = fig.add_axes([left_pos, slider_bottom, slider_width, slider_height])
    length_sliders.append(
        Slider(
            ax=temp_axes,
            label=f"L{i + 1}",
            valmin=0,
            valmax=100,
            valinit=INITIAL_LENGTHES[i],
            valstep=gain_sliders_ticks,
            orientation="vertical",
        )
    )

# Initial plot.
# (line,) = ax.plot(angles, y_func(angles, gain_sliders, span_slider, freq_sliders[0]), lw=2)
magnitude_lines = []
for i in range(STAGES):
    magnitude_line = graph_ax.plot(FREQS, [0] * len(FREQS), lw=2, alpha=0.3)[0]
    magnitude_lines.append(magnitude_line)

total_magnitudes_line = graph_ax.plot(FREQS, [0] * len(FREQS), lw=3)[0]

graph_ax.set_ylim([0, 1.2])
graph_ax.grid()


# The function to be called anytime a slider's value changes
def update(ignored):
    pass
    lengths = [float(s.val) / 100 for s in length_sliders]
    # print(lengths)
    total_magnitudes = [1.0] * len(FREQS)
    # sensors_gains = utils.sensor_controls_to_gains(args.sensors, sliders_gains)
    for i in range(STAGES):
        magnitudes = [0] * len(FREQS)
        for j in range(len(FREQS)):
            m = sum_magnitude(FREQS[j], lengths[i])
            magnitudes[j] = m
            total_magnitudes[j] = total_magnitudes[j] * m
        magnitude_lines[i].set_ydata(magnitudes)
        magnitude_lines[i].set_label(f"Stage-{i+1}")

    total_magnitudes_line.set_ydata(total_magnitudes)
    total_magnitudes_line.set_label(f"Total")

    plt.legend(loc="upper right")
    fig.canvas.draw_idle()


for slider in length_sliders:
    slider.on_changed(update)


update(None)
plt.show()
