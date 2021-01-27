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

x,y = 0,0
wave = 0
x1,x2,y1,y2 = 0,0,0,0
x11,x22,y11,y22 = 0,0,0,0
x1_step,x2_step =0,0
cropped = 0
last_text = 0

def cropp(gray_image,x1,y1,x2,y2):
    global cropped, spectr
    cv2.destroyWindow('gray')
    cropped = gray_image[y2:y1,x1:x2]
    spectr = gray_image[y22:y11,x11:x22]

# def rotate_image(image, angle,logic=1):
#     cv2.destroyAllWindows()
#     image_center = tuple(np.array(image.shape[1::-1]) / 2)
#     rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
#     result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
#     cv2.namedWindow('rotated', cv2.WINDOW_NORMAL)
#     cv2.imshow('rotated', result)
#     if logic == 0:
#     return result

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

# def mouseCoord_spectr(event,x,y,flags,param):
#     global x1_step,x2_step
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         x1_step = x
#     if event == cv2.EVENT_RBUTTONDBLCLK:
#         x2_step = x

Tk().withdraw()
filename = os.path.abspath(askopenfilename())
gray_image = cv2.imdecode(np.fromfile(filename, dtype = np.uint8), cv2.IMREAD_GRAYSCALE)


cv2.setMouseCallback('gray',mouseCoord_main)
cv2.namedWindow('gray', cv2.WINDOW_NORMAL)
cv2.imshow('gray', gray_image)


while True :
    cv2.setMouseCallback('gray',mouseCoord_main)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        raise SystemExit
    elif k == ord('a') :
        break

cv2.destroyWindow('gray')
if y1<y2:
    cropp(gray_image,x1,y2,x2,y1)
else:
    cropp(gray_image,x1,y1,x2,y2)
graph_image = np.float32(~cropped)
cv2.namedWindow('cropped', cv2.WINDOW_NORMAL)
cv2.imshow('cropped', cropped)

pixels = list(waves_dic.keys())
waves = list(waves_dic.values())
print('Выберите начальную длинну волны')
for i in range(0,len(waves)):
    print(str(i)+')'+str(waves[i]))
print('')
print('Введите номер длинны волны из списка выше: ')
wave0 = int(input())
print('Ждите')
wave0 = waves[wave0]
for i in range(0,len(waves)):
    if waves[i] == wave0:
        pixel0 = pixels[i]
        break
while True:
    if waves[0] == wave0:
        break
    else:
        del waves[0]
        del pixels[0]
diff = []
for i in range(0,len(waves)-1):
    diff.append((pixels[i+1]-pixels[i]))
pixels[0] = 0
pixels[1] = diff[0]
for i in range(2,len(pixels)):
    pixels[i] = pixels[i-1] + diff[i-1]

y_gr, x_gr = graph_image.shape[:2]
row = graph_image[0][0:x_gr]
for i in range(1,y_gr):
    row += graph_image[i][0:x_gr]
row = row / y_gr

interpolated = interpolate.interp1d(list(pixels),list(waves), kind ='cubic')
fig,ax=plt.subplots()
n = row.shape[0]
def f(x, y):
    global wave
    wave = interpolated(x)
    cid =  fig.canvas.mpl_connect('button_press_event',  onclick)
    return str(wave)
def onclick(event):
    global last_text
    if event.dblclick:
        x = event.xdata
        y = event.ydata
        ax.text(x-15, y+2, '--' + str(np.round(wave, 1)),fontsize = 10,rotation=90)
        plt.show()
ax.format_coord=f

x_coord = []
wave_coord =[4025, 4050, 4075, 4100, 4125, 4136, 4138, 4150, 4200, 4250, 4300, 4350, 4400]

flag  = 0
for i in range(0,len(wave_coord)):
    for j in range (1,x_gr):
        if np.round(interpolated(j), 1) == wave_coord[i] and flag == 0:
            wave_num = i
            flag = 1
del wave_coord[:wave_num]

flag = 0
for i in range (0, len(wave_coord)):
    for j in range (1, x_gr):
        if np.round(interpolated(j), 1) == wave_coord[i] and flag == 0:
            flag = 1
            x_coord.append(j)
    flag = 0
for i in range (0, len(wave_coord)):
    if wave_coord[i] == 4136 or wave_coord[i] == 4138:
        wave_coord[i] = ''
wave_coord.insert(0, round(wave0))
x_coord.insert(0, 0)

min_y=int(min(row))
y_coord=[]
y_dots = [0]
for i in range(min_y,300,20):
    y_coord.append(i)
for i in range(20,300,20):
    y_dots.append(i)

plt.ylim (0, 300)
ax.plot(row)
plt.xticks(x_coord,wave_coord)
plt.yticks(y_coord,y_dots)
ax.set_xlabel('Длинна волны (Ангстрем)')
ax.set_ylabel('Интенсивность (относительные единицы)')
plt.show()