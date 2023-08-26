import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons


amplituda = 1.0
czestosc = 0.2
tlumienie = 0.2
wychylenie_w_czasie = 0.0
omega = 0.0

fig, ax = plt.subplots(figsize=(18.5, 9.5))
ax.set_xlabel('t [s]')
ax.set_ylabel('x(t)')
ax.set_ylim(-2, 2)
ax.set_xlim(0, 20)
ax.axhline(0, color='black', linestyle='-')
plt.subplots_adjust(left=0.05, bottom=0.4)

amplituda_slider_ax = plt.axes([0.25, 0.25, 0.65, 0.03])
czestosc_slider_ax = plt.axes([0.25, 0.2, 0.65, 0.03])
tlumienie_slider_ax = plt.axes([0.25, 0.15, 0.65, 0.03])
wychylenie_slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
omega_slider_ax = plt.axes([0.25, 0.05, 0.65, 0.03])
radio_buttons_ax = plt.axes([0.025, 0.18, 0.15, 0.15])

amplituda_slider = Slider(amplituda_slider_ax, 'Amplituda', 0.1, 2.0, valinit=amplituda)
czestosc_slider = Slider(czestosc_slider_ax, 'Częstość', 0.1, 4.0, valinit=czestosc)
tlumienie_slider = Slider(tlumienie_slider_ax, 'Tłumienie', 0.0, 5, valinit=tlumienie)
wychylenie_slider = Slider(wychylenie_slider_ax, 'Wychylenie w czasie (phi)', -2*np.pi, 2*np.pi, valinit=wychylenie_w_czasie)
omega_slider = Slider(omega_slider_ax, 'Omega', 0.0, 10, valinit=omega)
radio_buttons = RadioButtons(radio_buttons_ax, ('Oba', 'Tłumienie', 'Wymuszone'))

t = np.linspace(0, 100, 10000)


def generate_data(amplituda, czestosc, tlumienie, wychylenie_w_czasie, omega):
    omega0 = 2 * np.pi * czestosc
    A = amplituda
    phi = wychylenie_w_czasie
    delta = (tlumienie**2) - 4*(omega0**2)
    Omega = omega0 * omega

    if delta < 0:
        x = A * np.exp((1/2) * (-tlumienie) * t) * np.sin((1/2) * np.sqrt(4 * omega0**2 - tlumienie**2) * t + phi)
    elif delta > 0:
        x = A * np.exp((1 / 2) * (-tlumienie) * t) * (np.exp((1 / 2) * np.sqrt(delta) * t) - np.exp((1 / 2) * (-np.sqrt(delta)) * t))
    y = A * np.cos(omega0 * t + phi)
    #z = 2 * A/(omega0**2 - Omega**2) * (np.sin(((omega0 - Omega) * t)/2 + phi) * np.sin(((omega0 + Omega) * t)/2 + phi))
    #Najpierw stan przejściowy, a następnie stan ustalony
    #if Omega != omega0:
    #   z = np.exp(-tlumienie * omega0 * t) * 2 * A/(omega0**2 - Omega**2) * np.sin(((omega0 - Omega) * t)/2 + phi) * np.sin(((omega0 + Omega) * t)/2 + phi) + y
    #elif Omega == omega0:
    #        z = np.exp(-tlumienie * omega0 * t) * (A * t /(2 * (omega0**2))) * np.sin(omega0 * t + phi) + y
    z = A * np.exp(-tlumienie * omega0 * t) * np.sin(Omega * t + phi) + A * np.cos(omega0 * t + phi)
    return t, x, y, z


t, x, y, z = generate_data(amplituda, czestosc, tlumienie, wychylenie_w_czasie, omega)
linex, = ax.plot(t, x, lw=2, color='red')
linex.set_label('Tłumienie')
liney, = ax.plot(t, y, lw=2, color='blue')
liney.set_label('Wymuszone1')
linez, = ax.plot(t, y, lw=2, color='pink')
linez.set_label('Wymuszone2')


def update_plot(val):
    amplituda = amplituda_slider.val
    czestosc = czestosc_slider.val
    tlumienie = tlumienie_slider.val
    wychylenie_w_czasie = wychylenie_slider.val
    omega = omega_slider.val

    t, x, y, z = generate_data(amplituda, czestosc, tlumienie, wychylenie_w_czasie, omega)
    linex.set_data(t, x)
    liney.set_data(t, y)
    linez.set_data(t, z)
    fig.canvas.draw_idle()


def change_plot(label):
    if label == 'Oba':
        linex.set_visible(True)
        liney.set_visible(True)
        linez.set_visible(True)
    elif label == 'Tłumienie':
        linex.set_visible(True)
        liney.set_visible(False)
        linez.set_visible(False)
    elif label == 'Wymuszone':
        linex.set_visible(False)
        liney.set_visible(True)
        linez.set_visible(True)
    fig.canvas.draw_idle()


amplituda_slider.on_changed(update_plot)
czestosc_slider.on_changed(update_plot)
tlumienie_slider.on_changed(update_plot)
wychylenie_slider.on_changed(update_plot)
omega_slider.on_changed(update_plot)
radio_buttons.on_clicked(change_plot)


ax.legend()
plt.show()