# import warnings
# warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from scipy import interpolate

# 76
# 42

###Словарь имеющий вид пиксель:длинна волны, получен опытным путем в первой версии программы (не моей)###
waves_dic = {
    144:4021.870,
    185:4024.739,
    262:4029.636,
    297:4030.492,
    317:4031.965,
    406:4041.285,
    447:4043.905,
    457:4044.611,
    514:4049.331,
    553:4051.906,
    561:4052.466,
    573:4052.664,
    594:4053.728,
    601:4054.883,
    626:4057.346,
    636:4058.229,
    646:4058.760,
    656:4059.721,
    691:4062.444,
    702:4063.440,
    712:4064.450,
    730:4065.392,
    752:4067.275,
    763:4067.982,
    799:4070.779,
    821:4072.800,
    836:4073.775,
    849:4074.791,
    872:4076.637,
    894:4078.358,
    910:4079.250,
    926:4080.887,
    931:4081.300,
    941:4082.117,
    961:4083.667,
    971:4084.499,
    981:4085.166,
    1002:4087.103,
    1020:4088.377,
    1031:4089.222,
    1039:4090.077,
    1068:4092.267,
    1112:4095.978,
    1125:4097.112,
    1138:4098.187,
    1170:4100.793,
    1176:4101.274,
    1211:4104.128,
    1238:4106.353,
    1251:4107.492,
    1278:4109.808,
    1317:4112.966,
    1333:4114.449,
    1382:4118.549,
    1401:4120.211,
    1419:4121.806,
    1428:4122.510,
    1441:4123.745,
    1470:4126.190,
    1487:4127.707,
    1551:4132.903,
    1559:4133.862,
    1568:4134.510,
    1595:4137.004,
    1626:4139.923,
    1650:4141.867,
    1671:4143.645,
    1696:4146.070,
    1716:4147.673,
    1733:4149.370,
    1743:4150.264,
    1783:4153.405,
    1791:4154.657,
    1816:4156.742,
    1826:4157.791,
    1837:4158.798,
    1910:4165.420,
    1936:4167.891,
    1970:4170.906,
    1982:4171.913,
    1990:4172.706,
    2001:4173.926,
    2021:4175.640,
    2030:4176.572,
    2041:4177.596,
    2060:4178.868,
    2084:4181.757,
    2091:4182.897,
    2117:4184.895,
    2141:4187.044,
    2150:4187.501,
    2186:4191.558,
    2227:4195.480,
    2236:4195.214,
    2254:4198.268,
    2271:4198.645,
    2285:4200.927,
    2316:4203.572,
    2332:4205.546,
    2344:4206.702,
    2347:4207.131,
    2363:4208.615,
    2381:4210.352,
    2415:4213.650,
    2433:4215.425,
    2440:4216.186,
    2454:4217.555,
    2472:4219.365,
    2481:4220.348,
    2501:4222.221,
    2521:4225.711,
    2544:4226.430,
    2573:4229.516,
    2613:4233.612,
    2635:4235.942,
    2659:4238.039,
    2665:4238.621,
    2675:4239.733,
    2704:4242.652,
    2710:4243.894,
    2728:4245.260,
    2735:4246.090,
    2750:4247.433,
    2756:4248.226,
    2770:4250.130,
    2790:4250.790,
    2853:4258.324,
    2865:4260.003,
    2883:4260.479,
    2935:4266.936,
    2941:4267.630,
    2950:4268.758,
    2960:4269.700,
    3008:4273.870,
    3078:4282.406,
    3105:4285.445,
    3145:4290.361,
    3159:4291.466,
    3175:4294.128,
    3219:4298.040,
    3230:4299.241,
    3244:4300.625,
    3255:4302.192,
    3277:4304.552,
    3285:4305.455,
    3305:4307.906,
    3320:4309.199,
    3370:4315.067,
    3428:4321.800,
    3461:4325.765,
    3480:4327.096,
    3559:4337.049,
    3681:4351.549,
    3690:4352.737,
    3739:4358.505,
    3814:4367.743,
    3830:4369.774,
    3861:4373.563,
    3880:4375.933,
    3936:4382.773,
    3950:4383.547,
    3980:4388.154,
    4000:4390.954,
    4081:4401.293,
    4105:4404.752,
    4131:4407.714,
    4138:4408.419,
    4177:4415.125,
    4395:4442.343,
    4400:4443.197,
    4435:4447.722,
    4974:4525.146,
    5024:4531.152,
    5134:4592.655,
}

###Константы###
x,y = 0,0
wave = 0
x1,x2,y1,y2 = 0,0,0,0
x11,x22,y11,y22 = 0,0,0,0
x1_step,x2_step =0,0
cropped = 0

def cropp(gray_image,x1,y1,x2,y2):
    global cropped, spectr
    cv2.namedWindow('gray', cv2.WINDOW_NORMAL)
    cv2.destroyWindow('gray')
    cropped = gray_image[y2:y1,x1:x2]
    spectr = gray_image[y22:y11,x11:x22]

###Функция для построения белого прямоугольника на этапе обрезки фото, изменяет координаты x1,x2,y1,y1 для обрезки###
def mouseCoord_main(event,x,y,flags,param):
    global x1,x2,y1,y2
    if event == cv2.EVENT_LBUTTONDBLCLK:
        x1 = x
        y1 = y
    if event == cv2.EVENT_RBUTTONDBLCLK:
        x2 = x
        y2 = y
        gray_image_rect = cv2.rectangle(gray_image.copy(), (x1,y1), (x2,y2), (255,0,0), 2) 
        cv2.imshow('gray', gray_image_rect)

Tk().withdraw()#Открываем окно Tkiner
filename = os.path.abspath(askopenfilename())#Получаем путь до картинки
gray_image = cv2.imdecode(np.fromfile(filename, dtype = np.uint8), cv2.IMREAD_GRAYSCALE)#Открываем ее в сером

cv2.namedWindow('gray', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('gray',mouseCoord_main)#Привязываем функцию mouseCoord_main к окну
cv2.namedWindow('gray', cv2.WINDOW_NORMAL)#Позволяем изменять размеры окна
cv2.imshow('gray', gray_image)#Показываем окно

while True :
    cv2.setMouseCallback('gray',mouseCoord_main)#Привязываем функцию состояния мышки к оку
    k = cv2.waitKey(20) & 0xFF #Получаем код символа, напечанного с клавиатуры
    if k == 27: #Если код равен ESC
        cv2.destroyAllWindows()
        raise SystemExit#Все завершаем
    elif k == ord('a') :#Если код равен английской a
        break

cv2.destroyWindow('gray')#Закрываем прошлое окно

if y1<y2:#Кропаем, учитывем правильность координат
    cropp(gray_image,x1,y2,x2,y1)
else:
    cropp(gray_image,x1,y1,x2,y2)

graph_image = np.float32(~cropped)
cv2.namedWindow('cropped', cv2.WINDOW_NORMAL)
cv2.imshow('cropped', cropped)#Показываем кроп

pixels = list(waves_dic.keys())#Разбираем наш словарь на пиксели и 
waves = list(waves_dic.values())#длинны волн

###Просим выбрать начальную длинну волны###
print('Выберите начальную длинну волны')
for i in range(0,len(waves)):
    print(str(i)+')'+str(waves[i]))
print('')
print('Введите номер длинны волны из списка выше: ')
wave0 = int(input())
print('Ждите')
wave0 = waves[wave0]

### Удаляем все что до введенной длинны волны wave0 ###
while True:
    if waves[0] == wave0:
        break
    else:
        del waves[0]
        del pixels[0]

### Не помню что тут происходит :) ###        
diff = []
for i in range(0,len(waves)-1):
    diff.append((pixels[i+1]-pixels[i]))
pixels[0] = 0
pixels[1] = diff[0]
for i in range(2,len(pixels)):
    pixels[i] = pixels[i-1] + diff[i-1]
### Работаем с изображением ###
y_gr, x_gr = graph_image.shape[:2]# Получаем размеры
row = graph_image[0][0:x_gr] #Проходим изображение последовательно построчно и суммируем все строки
for i in range(1,y_gr):
    row += graph_image[i][0:x_gr]
row = row / y_gr#Делим на количество строк и получаем примитивный фильтр шума
# row - наша функция для опр. изображения
### Приводим значения к формату от 0 до 100 ###
row_max = max(row)
row_min = min(row)
for i in range(len(row)):
    row[i]=row[i]-row_min
    row[i]=100*row[i]/row_max
############################

interpolated = interpolate.interp1d(list(pixels),list(waves), kind ='cubic') # Интерполяция 

y_coord = []
for i in range(0,101,20):
    y_coord.append(i)

############################

# wave_list = []

# default_wave_list = [4050, 4075, 4100, 4125, 4150, 4200, 4250, 4300, 4350]

# while True:
#     if wave0 < default_wave_list[0]:
#         wave_list.append(int(wave0))
#         wave_list = wave_list + default_wave_list
#         break
#     del default_wave_list[0]

# print(wave_list)

# x_coord_list = []

# for tmp_wave in wave_list:
#     for i in range(x_gr):
#         coord_wave = np.round(interpolated(i),1)
#         if coord_wave == tmp_wave:
#             x_coord_list.append(i)
#             break

# print(x_coord_list)

# for i in range(len(x_coord_list)-1):
#     print(x_coord_list[i]-x_coord_list[i+1])

############################

numOFticks = 11

wave_list =[]

for i in range(x_gr):
    tmp = interpolated(i)
    if tmp == wave0:
        wave0_coord = i
        break

x_coord_list = []
delta = (x_gr - wave0_coord)/ numOFticks
for i in range(numOFticks):
    x_coord_list.append(np.round(wave0_coord+i*delta,0))

for i in x_coord_list:
    wave_list.append(np.round(interpolated(i),0))

for i in range(len(wave_list)-1):
    if wave_list[i] < 4150 and wave_list[i+1] > 4150:
        wave_list.insert(i+1, "")
        wave_list.insert(i+2, "")
        raze_start = x_coord_list[i]
        raze_end = x_coord_list[i+1]
        raze_center = int((raze_end - raze_start)/2)
        x_coord_list.insert(i+1, raze_start + raze_center-2)
        x_coord_list.insert(i+2, raze_start + raze_center+2)
        break

fig,ax=plt.subplots() #Создаем фигуру графика

listOfannot = []

def f(x, y): #Функция чтобы прсоединить функцию отслеживания нажатия на график и расчета длинны волны в точке
    global wave
    wave = interpolated(x)
    cid =  fig.canvas.mpl_connect('button_press_event',  onclick)
    return  str(np.round(wave, 3))

def onclick(event):# Функция, печатающая координаты на графике по двойному нажатию ЛКМ
    if event.dblclick:
        x = event.xdata
        y = event.ydata
        annot = ax.annotate('--' + str(np.round(wave, 1)), xy=(x,y), xytext=(0,0), textcoords="offset points", rotation=90)
        annot.set_visible(True)
        listOfannot.append(annot)
        fig.canvas.draw() #Перерисовать график
        
def on_press(event):
    pos_list_annot = len(listOfannot) - 1
    print(listOfannot)
    if event.key == 't' and len(listOfannot) !=0: 
        listOfannot[pos_list_annot].set_visible(False)
        del listOfannot[pos_list_annot]
        fig.canvas.draw()
    if event.key == 'a':
        x = listOfannot[pos_list_annot].xy[0]
        y = listOfannot[pos_list_annot].xy[1]
        listOfannot[pos_list_annot].xy = (x-1,y)
        fig.canvas.draw()
    if event.key == 'd':
        x = listOfannot[pos_list_annot].xy[0]
        y = listOfannot[pos_list_annot].xy[1]
        listOfannot[pos_list_annot].xy = (x+1,y)
        fig.canvas.draw()    
    if event.key == 'w':
        x = listOfannot[pos_list_annot].xy[0]
        y = listOfannot[pos_list_annot].xy[1]
        listOfannot[pos_list_annot].xy = (x,y+1)
        fig.canvas.draw()
    if event.key == 's':
        x = listOfannot[pos_list_annot].xy[0]
        y = listOfannot[pos_list_annot].xy[1]
        listOfannot[pos_list_annot].xy = (x,y-1)
        fig.canvas.draw()
        
ax.format_coord=f# Добавляем функцию печати на графике

plt.rcParams['keymap.save'].remove('s')
plt.rcParams['keymap.quit'].remove('q')
plt.ylim (0, 100)
ax.plot(row, color='black')
plt.xticks(x_coord_list, wave_list)
plt.yticks(y_coord)
ax.set_xlabel('Длинна волны (Ангстрем)')
ax.set_ylabel('Интенсивность (относительные единицы)')
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', on_press)
plt.show()