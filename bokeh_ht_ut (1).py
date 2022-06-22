import matplotlib.pyplot as plt
import math
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Button, Div

import numpy as np
from bokeh.plotting import ColumnDataSource, figure, show

# pole powierzchni przekroju poprzecznego zbiornika
A = 1.5
# współczynnik beta
B = 0.035
# okres probkowania
T_p = 0.1
# czas symulacji
Tsim = 360
# ilość probek
N = int(Tsim / T_p)
# wartość zadana
h_target = 1.5
u_n = 1
# maksymalna wysokosc cieczy w zbiorniku
h_max = 5
# ???
k_p = 0.5
# ??? T_i = 1.5
T_i = 0.5
# ???
# T_d = 2.5
T_d = 0.5
# natężenie dopływu
Qd = 0.005 * u_n

h_list = [4.0, 4.0]
e_0 = h_target - h_list[0]
e_list = [e_0]
u_n_list = [u_n]

# which plot index should be drawn again

plot_to_generate_slider = Slider(start=1, end=1000, value=0, step=1, title="p_t_g")

bokeh_height_plot = [None, None, None, None, None]
bokeh_voltage_plot = [None, None, None, None, None]


def reset_values():
    h_list.clear()
    h_list.append(4.0)
    h_list.append(4.0)
    e_list.clear()
    u_n_list.clear()
    e_list.append(e_0)
    u_n_list.append(u_n)


def regulation_error(i):
    return h_target - h_list[i]


def calc_res(n):
    regulation_error_sum = 0
    for k in range(1, n):
        regulation_error_sum += e_list[k]
    return regulation_error_sum


def calc_current(i):
    return k_p * (e_list[i] + (T_p / T_i) * calc_res(i) + (T_d / T_p) * (e_list[i] - e_list[i - 1]))


def calc_doplyw(u_n):
    return 0.005 * u_n


def generate_PID_data():
    reset_values()
    for i in range(1, N):
        # e_list.append(regulation_error(i))
        e_list.append(h_target - h_list[i])

        # u_n = calc_current(i)
        u_n = k_p * (e_list[i] + (T_p / T_i) * calc_res(i) + (T_d / T_p) * (e_list[i] - e_list[i - 1]))
        # u_n_list.append(u_n)
        u_n_list.append(u_n)
        # Qd = calc_doplyw(u_n_list[-1])
        Qd = 0.005 * u_n_list[-1]

        h_new = (T_p / A) * (Qd - B * math.sqrt(h_list[-1])) + h_list[-1]
        if h_new < 0:
            h_new = 0
        if h_new > h_max:
            h_new = h_max
        h_list.append(h_new)
    print(h_list)
    print("PID data ok")


def plot_draw():
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
    ax3 = fig.add_subplot(111, zorder=-1)
    for _, spine in ax3.spines.items():
        spine.set_visible(False)
    ax3.tick_params(labelleft=False, labelbottom=False, left=False, right=False)
    ax3.get_shared_x_axes().join(ax3, ax1)
    ax3.grid(axis="x")

    wykres_wysokosc = ax1.plot(h_list, color='b', label="1 row")
    ax1.set_title('Height(t) - wysokosc cieczy w zbiorniku')
    ax1.set_xlabel('Sample No')
    ax1.set_ylabel('Height')
    wykres_uchyb = ax2.plot(e_list, color='b', label="1 row")
    ax2.set_title('Error value(t) - uchyb')
    ax2.set_xlabel('Sample No')
    ax2.set_ylabel('Error value (h(t) - h_target)')

    ax1.grid()
    ax2.grid()
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.25)
    plt.show()


def pid_local_matplotlib():
    generate_PID_data()
    plot_draw()


def pid_bokeh(T_p, T_i, T_d, k_p):
    generate_PID_data()
    N = int(Tsim / T_p)
    t = np.linspace(0, N, N)
    print("h_list:")
    print(h_list)
    print("u_n_list:")
    print(u_n_list)
    h0 = h_list[:]
    h1 = h_list[:]
    h2 = h_list[:]
    h3 = h_list[:]
    h4 = h_list[:]

    u0 = u_n_list[:]
    u1 = u_n_list[:]
    u2 = u_n_list[:]
    u3 = u_n_list[:]
    u4 = u_n_list[:]

    source = ColumnDataSource(data=dict(t=t, h0=h0, h1=h1, h2=h2, h3=h3, h4=h4, u0=u0))

    if plot_to_generate_slider.value == 0:
        h = [1] * 3600
        u = [u_n] * 3600
        source = ColumnDataSource(data=dict(t=t, h0=h, h1=h, h2=h, h3=h, h4=h, u0=u, u1=u, u2=u, u3=u, u4=u))
        for i in range(0, 5, 1):
            bokeh_height_plot[i] = figure(title="h(t) - " + str(i), x_range=(0, N), y_range=(0, 5), width=250,
                                          height=250)
            bokeh_height_plot[i].line('t', 'h' + str(i), source=source, line_width=3, line_alpha=0.6)

            bokeh_voltage_plot[i] = figure(title="u(t) - " + str(i), x_range=(0, N), y_range=(-10, 10), width=250,
                                           height=250)
            bokeh_voltage_plot[i].line('t', 'u' + str(i), source=source, line_width=3, line_alpha=0.6)

    plot_to_generate_pos = plot_to_generate_slider.value % 5

    bokeh_height_plot[plot_to_generate_pos] = figure(title="h(t) - " + str(plot_to_generate_pos), x_range=(0, N),
                                                     y_range=(0, 5), width=250, height=250)
    bokeh_height_plot[plot_to_generate_pos].line('t', 'h' + str(plot_to_generate_pos), source=source, line_width=3,
                                                 line_alpha=0.6)

    bokeh_voltage_plot[plot_to_generate_pos] = figure(title="u(t) - " + str(plot_to_generate_pos), x_range=(0, N),
                                                      y_range=(-10, 10), width=250, height=250)
    bokeh_voltage_plot[plot_to_generate_pos].line('t', 'u' + str(plot_to_generate_pos), source=source, line_width=3,
                                                  line_alpha=0.6)

    # sliders definition - start

    h_target_slider = Slider(start=0, end=5, value=1.5, step=.1, title="h_target")
    h_0_slider = Slider(start=0, end=5, value=4, step=.1, title="h_0")
    u_n_slider = Slider(start=0, end=10, value=1, step=.1, title="u_n")
    k_p_slider = Slider(start=0.01, end=1.0, value=k_p, step=0.01, title="k_p")
    t_p_slider = Slider(start=0.01, end=2.00, value=T_p, step=0.01, title="T_p")
    t_i_slider = Slider(start=1, end=5, value=T_i, step=0.1, title="T_i")
    t_d_slider = Slider(start=1, end=5, value=T_d, step=0.1, title="T_d")

    # sliders definition - end

    # desc divs - start

    plot_divs = [None] * 5

    for i in range(0, 5, 1):
        print(i)
        plot_divs[i] = Div(text="""Your <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The
remaining div arguments are <b>width</b> and <b>height</b>. For this example, those values
are <i>200</i> and <i>100</i>, respectively.""",
                           width=200, height=100)

    # desc divs - end

    callback = CustomJS(
        args=dict(source=source, h_target=h_target_slider, h_0=h_0_slider, u_n=u_n_slider, k_p=k_p_slider,
                  T_p=t_p_slider, T_i=t_i_slider, T_d=t_d_slider, p_t_g=plot_to_generate_slider, desc_divs=plot_divs),
        code="""
                const div_params_desc = desc_divs

                const data = source.data;
                const t = data['t']

                const data_h0 = data['h0']
                const data_h1 = data['h1']
                const data_h2 = data['h2']
                const data_h3 = data['h3']
                const data_h4 = data['h4']

                const data_u0 = data['u0']
                const data_u1 = data['u1']
                const data_u2 = data['u2']
                const data_u3 = data['u3']
                const data_u4 = data['u4']

                const hTarget = h_target.value;
                const Tsim = 360;
                const h0 = h_0.value;
                const Tp = T_p.value;
                const Ti = T_i.value;
                const Td = T_d.value;
                const kp = k_p.value;
                let u_n_list = [u_n.value];
                const h_max = 5;
                const A = 1.5;
                const B = 0.035;

                const ptg = p_t_g.value % 5;

                switch (ptg) {
                  case 0:
                    data_h0[0] = h0;
                    data_h0[1] = h0;
                    break;
                  case 1:
                    data_h1[0] = h0;
                    data_h1[1] = h0;
                    break;
                  case 2:
                    data_h2[0] = h0;
                    data_h2[1] = h0;
                    break;
                  case 3:
                    data_h3[0] = h0;
                    data_h3[1] = h0;
                    break;
                  case 4:
                    data_h4[0] = h0;
                    data_h4[1] = h0;
                }

                console.log(h0)

                let N = parseInt( Tsim / Tp )
                let e_0 = hTarget - h0
                let e_list = [e_0]

                div_params_desc[ptg].text = "Wykres nr: " + p_t_g.value + "<br>" +
                    "h_target = " + hTarget + " , h_0 = " + h0 + "<br> " +
                    "u_start = " + u_n.value + "<br> " +
                    "k_p = " + kp + "<br> " +
                    "T_p = " + Tp + ", T_i = " + Ti + ", T_d = " + Td + "<br> " 


                for (let i = 1; i < N; i++) {
                    switch (ptg) {
                      case 0:
                        e_list.push(hTarget - data_h0[i]) 
                        break;
                      case 1:
                        e_list.push(hTarget - data_h1[i])
                        break;
                      case 2:
                        e_list.push(hTarget - data_h2[i])
                        break
                      case 3:
                        e_list.push(hTarget - data_h3[i])
                        break;
                      case 4:
                        e_list.push(hTarget - data_h4[i])
                    }

                    //e_list.push(hTarget - h[i])

                    let regulation_error_sum = 0
                    for (let k = 0; k < i; k++) {
                        regulation_error_sum += e_list[k]
                    }
                    u_n = kp * (e_list[i] + (Tp / Ti) * regulation_error_sum + (Td / Tp) * (e_list[i] - e_list[ i - 1 ]))
                    u_n_list.push(u_n)

                    let Qd = 0.005 * u_n

                    let last_ind = i

                    let last_h = 1;

                    switch (ptg) {
                      case 0:
                        last_h = data_h0[last_ind];
                        data_u0[i] = u_n
                        break;
                      case 1:
                        last_h = data_h1[last_ind];
                        data_u1[i] = u_n
                        break;
                      case 2:
                        last_h = data_h2[last_ind];
                        data_u2[i] = u_n
                        break;
                      case 3:
                        last_h = data_h3[last_ind];
                        data_u3[i] = u_n
                        break;
                      case 4:
                        last_h = data_h4[last_ind];
                        data_u4[i] = u_n
                    }

                    let h_new = (Tp / A) * (Qd - B * Math.sqrt( last_h )) + last_h

                    if (h_new < 0) {
                        h_new = 0
                    }   
                    if( h_new > h_max) {
                        h_new = h_max
                    }

                    switch (ptg) {
                      case 0:
                        data_h0[i + 1] = h_new
                        break;
                      case 1:
                        data_h1[i + 1] = h_new
                        break;
                      case 2:
                        data_h2[i + 1] = h_new
                        break;
                      case 3:
                        data_h3[i + 1] = h_new
                        break;
                      case 4:
                        data_h4[i + 1] = h_new
                    }
                }

                p_t_g.value = p_t_g.value + 1;

                source.change.emit()
            """)

    # button - start

    button = Button(label="Apply parameters!",
                    button_type="primary",
                    align="center",
                    width=100
                    )

    button.js_on_click(callback)

    # button - end

    layout = column(
        row(
            column(
                bokeh_height_plot[0],
                bokeh_voltage_plot[0],
                plot_divs[0]
            ),
            column(
                bokeh_height_plot[1],
                bokeh_voltage_plot[1],
                plot_divs[1]
            ),
            column(
                bokeh_height_plot[2],
                bokeh_voltage_plot[2],
                plot_divs[2]
            ),
            column(
                bokeh_height_plot[3],
                bokeh_voltage_plot[3],
                plot_divs[3]
            ),
            column(
                bokeh_height_plot[4],
                bokeh_voltage_plot[4],
                plot_divs[4]
            )
        ),
        row(
            column(
                row(
                    h_target_slider,
                    h_0_slider,
                    u_n_slider,
                    k_p_slider
                ),
                row(
                    t_p_slider,
                    t_i_slider,
                    t_d_slider,
                    plot_to_generate_slider
                ),
                button)
        )
    )

    show(layout)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # pid_local_matplotlib()

    pid_bokeh(T_p, T_i, T_d, k_p)