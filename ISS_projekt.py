import math

from bokeh.events import ButtonClick
from bokeh.io import show, curdoc
from bokeh.layouts import column, layout
from bokeh.models import CustomJS, Select, ColumnDataSource, Button, CheckboxButtonGroup, Toggle, CheckboxGroup, Slider
#do uruchomienia należy wpisać w terminalu pycharm "bokeh serve --show ISS_projekt.py"
# zmienne

# Sprawdz pogodę by zacząć
# Pogoda = 0;  # 0 - stop, 1 - słońce, 2 - deszcz, 3-śnieg,4-mgła

# Sprawdz godzinę by zacząć
# Godzina = 1;  # 0-inna godzina niż ustawiono, 1-poprawna

# Studnia
# Sprawdz poziom wody w studni
# Głębokość studni 7m
# Pole powierzchni przekroju studni 3m^2
from bokeh.plotting import figure

A = 3
# preekość napływu 1m^3/h
# prędkość zużycia wody przez zraszacz maksymaklnie 60l/min = 0.001 m3/s
Qd = 0.0003
Qo = 0.001
Qw = Qd - Qo
Qtemp = 60
# Poziom wody w studni musi być większy niż 1,5m
# Maksymalnie woda może mieć 6m wysokości
h_max = 6
h_min = 1.5

# Czas trwania podlewania 15 min
Tsim = 10  # 0,25h
T_p = 0.1

N = int(Tsim / T_p)
h_list = [6]
h_target = 1.5
h_target2 = 6
e_0 = h_target - h_list[0]
e_list = [0]
u_n_list = [3, 3]
GodzinaText = "6.00"

update_interval = 100
roll_over = 100

B = 0.035
k_p = 0.1
T_i = 0.5
T_d = 0.5

run = 0
time: int = 0

# plot
p = figure(x_axis_type="linear", width=600, height=350)
source = ColumnDataSource(dict(x=[], y=[]))
p.circle(x="x", y="y", color="firebrick", line_color="firebrick", source=source)
p.line(x="x", y="y", source=source)

f = figure(x_axis_type="linear", width=600, height=350)
source2 = ColumnDataSource(dict(x=[], y=[]))
f.circle(x="x", y="y", color="firebrick", line_color="firebrick", source=source2)
f.line(x="x", y="y", source=source2)

g = figure(x_axis_type="linear", width=600, height=350)
source3 = ColumnDataSource(dict(x=[], y=[]))
g.circle(x="x", y="y", color="firebrick", line_color="firebrick", source=source3)
g.line(x="x", y="y", source=source3)

pocz = 1
koniec = N

n = 0
number_list = []
i = 1

toggle = Toggle(label="Start", button_type="success")
x = 0
checkboxlist = [0, 0, 0]


def update():
    global x
    global n
    global i
    if toggle.active:
        if checkboxlist[0] == 1:
            if godz.value == "6.00":
                toggle.label = "Stop"
                new_data = dict(x=[n], y=[h_list[-1]])
                source.stream(new_data, rollover=2000)
                p.title.text = "Podlewanie ogrodu"
                f.title.text = "Un"
                g.title.text = "e"
                if buttonclick == True:
                    x = PID_rekur(i)
                else:
                    x = PID_rekur2(i)
                new_data_un = dict(x=[n], y=[u_n_list[-1]])
                source2.stream(new_data_un, rollover=2000)
                new_data_e = dict(x=[n], y=[e_list[-1]])
                source3.stream(new_data_e, rollover=2000)
                n = n + 1
                number_list.append(n)
            else:
                toggle.label = "Stop"
                new_data = dict(x=[n], y=[h_list[-1]])
                source.stream(new_data, rollover=2000)
                p.title.text = "Podlewanie ogrodu"
                f.title.text = "Un"
                g.title.text = "e"
                x = PID_rekur2(i)
                new_data_un = dict(x=[n], y=[u_n_list[-1]])
                source2.stream(new_data_un, rollover=2000)
                new_data_e = dict(x=[n], y=[e_list[-1]])
                source3.stream(new_data_e, rollover=2000)
                n = n + 1
                number_list.append(n)
        else:
            toggle.label = "Stop"
            new_data = dict(x=[n], y=[h_list[-1]])
            source.stream(new_data, rollover=2000)
            p.title.text = "Podlewanie ogrodu"
            f.title.text = "Un"
            g.title.text = "e"
            if buttonclick == True:
                x = PID_rekur(i)
            else:
                x = PID_rekur2(i)
            new_data_un = dict(x=[n], y=[u_n_list[-1]])
            source2.stream(new_data_un, rollover=2000)
            new_data_e = dict(x=[n], y=[e_list[-1]])
            source3.stream(new_data_e, rollover=2000)
            n = n + 1
            number_list.append(n)
    else:
        toggle.label = "Start"
    i = x


def update_intermed(attrname, old, new):
    global buttonclick
    if select.value != "słońce":
        buttonclick = False
        button.label = "Pompa On"


button = Button(label="Pompa On")
buttonStop = Button(label="Stop")
buttonclick = False

stoppomp = False


def slider_update(attr, old, new):
    global k_p
    global T_p
    global T_i
    global Qtemp
    global Qo
    Qtemp = slider_Qo.value
    Qo = Qtemp * 1.66667E-5
    u_n = slider_un.value
    u_n_list.append(u_n)
    k_p = slider_kp.value
    T_p = slider_tp.value
    global T_d
    T_d = slider_td.value
    T_i = slider_ti.value
    update()


slider_Qo = Slider(start=0, end=60, value=Qtemp, step=1, title="Wydajność pompy")
slider_Qo.on_change("value", slider_update)
slider_un = Slider(start=0, end=10, value=3, step=.1, title="U_n")
slider_un.on_change("value", slider_update)
slider_kp = Slider(start=0.01, end=1.0, value=k_p, step=0.01, title="k_p")
slider_kp.on_change("value", slider_update)
slider_tp = Slider(start=0.01, end=2.00, value=T_p, step=0.01, title="T_p")
slider_tp.on_change("value", slider_update)
slider_td = Slider(start=1, end=5, value=T_d, step=0.1, title="T_d")
slider_td.on_change("value", slider_update)
slider_ti = Slider(start=1, end=5, value=T_i, step=0.1, title="T_i")
slider_td.on_change("value", slider_update)


def PID_rekur(i):
    global k_p
    e_list.append(h_target - h_list[i])
    u_n = k_p * (e_list[i] + (T_p / T_i) * calc_res(i) + (T_d / T_p) * (e_list[i] - e_list[i - 1]))
    u_n_list.append(u_n)
    #print(e_list[-1])
    Qd1 = Qw * u_n_list[-1]
    h_new = (T_p / A) * (Qd1 - B * math.sqrt(h_list[-1])) + h_list[-1]
    if h_new < h_min:
        h_new = h_min
    if h_new > h_max:
        h_new = h_max
    h_list.append(h_new)
    print(i, " h ", h_list[i], " e ", e_list[i],"un",u_n_list[i])
    i = i + 1
    return i


def PID_rekur2(i):
    e_list.append(h_target2 - h_list[i])
    u_n = k_p * (e_list[i] + (T_p / T_i) * calc_res(i) + (T_d / T_p) * (e_list[i] - e_list[i - 1]))
    u_n_list.append(u_n)
    Qd1 = Qd * u_n_list[-1]
    h_new = (T_p / A) * (Qd1 + B * math.sqrt(h_list[-1])) + h_list[-1]
    if h_new < h_min:
        h_new = h_min
    if h_new > h_max:
        h_new = h_max
    h_list.append(h_new)
    print(i," h ",h_list[i]," e ",e_list[i],"un",u_n_list[i])
    i = i + 1
    return i


def update_button(event):
    global buttonclick
    global i
    global stoppomp
    if select.value == "słońce":
        buttonclick = not buttonclick
    if buttonclick == True:
        button.label = "Pompa Off"
    else:
        button.label = "Pompa On"


def update_checkbox(attr, old, new):
    global Qd
    if checkbox_group.active[0] == 1:
        print("0")
        checkboxlist[0] = 1
    else:
        checkboxlist[0] = 0
    if checkbox_group.active[1] == 1:
        print("1")
        checkboxlist[1] = 1
    else:
        checkboxlist[1] = 0
    if checkbox_group.active[2] == 1:
        print("2")
        Qd = 0
        checkboxlist[2] = 1
    else:
        Qd = 0.0003
        checkboxlist[2] = 0


chlabels = ["włącznik czasowy", "wyłącznik czasowy", "susza"]
checkbox_group = CheckboxGroup(labels=chlabels)
checkbox_group.on_click(update_checkbox)
button.on_click(update_button)

select = Select(title="Pogoda:", value="słońce", options=["słońce", "deszcz", "śnieg", "mgła"])
select.on_change("value", update_intermed)

godz = Select(title="Godzina:", value="6.00",
              options=["0.00", "1.00", "2.00", "3.00", "4.00", "5.00", "6.00", "7.00", "8.00", "9.00", "10.00",
                       "11.00", "12.00", "13.00", "14.00", "15.00", "16.00", "17.00", "18.00", "19.00", "20.00",
                       "21.00", "22.00", "23.00", "24.00"])
godz.on_change("value", update_intermed)


def pogoda():
    if select.value == "słońce":
        Pogoda = 1
    elif select.value == "deszcz":
        Pogoda = 2
    elif select.value == "śnieg":
        Pogoda = 3
    elif select.value == "mgła":
        Pogoda = 4
    return Pogoda;


def godzina():
    if GodzinaText == godz.value:
        Godzina = 1
    else:
        Godzina = 0
    return Godzina


def calc_res(n):
    regulation_error_sum = 0
    for k in range(1, n):
        regulation_error_sum += e_list[k]
    return regulation_error_sum


p.xaxis.major_label_orientation = math.radians(80)
p.xaxis.axis_label = "N"
p.yaxis.axis_label = "H"
f.xaxis.major_label_orientation = math.radians(80)
f.xaxis.axis_label = "N"
f.yaxis.axis_label = "UN"
g.xaxis.major_label_orientation = math.radians(80)
g.xaxis.axis_label = "N"
g.yaxis.axis_label = "e"
lay_out = layout([[p], [f], [g]], [[select], [godz]], [[button], [toggle]], [[checkbox_group]],
                 [[slider_Qo], [slider_un], [slider_kp], [slider_tp], [slider_td], [slider_ti]])
curdoc().title = "Podlewanie ogrodu"
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update, 500)
