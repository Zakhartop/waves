import numpy as np
import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

def binary(n):  # перевод в двоичную сс
    return [int(i) for i in bin(n)[2:].zfill(8)]

def adc():  # ацп
    value = 0
    for i in range(7, -1, -1):
        value += 2 ** i
        GPIO.output(dac, binary(value))
        time.sleep(0.0005)
        if GPIO.input(comp) == 1:
            value -= 2 ** i
    return value

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(21, GPIO.IN)
listADC = []  # напряжение
list_time = []  # моменты времени падения напряжения
L = float(input(" Введите длину от слива до проводника" ))# длина от проводника до слива из кюветы. снимаем вручную
time.sleep(0.5)

while 1:  # отслеживает открытие крышки слива
    print(GPIO.input(21), "- состояние закрывашки")
    if GPIO.input(21) == 1:
        timeStart = time.time()
        break

listADC.append(3.24 - adc() / 256 * 3.3)
list_time.append(time.time() - timeStart)

while 1:  # отслеживаем момент, когда волна проходит через проводник(момент понижения напряжения)
    time.sleep(0.04)
    listADC.append(3.24 - adc() / 256 * 3.3)
    list_time.append(time.time() - timeStart)
    print(3.24 - adc() / 256 * 3.3, "- напряжение на проводнике")
    if abs(listADC[-1] - listADC[-2]) >= 0.1:
        krit_voltage = listADC[-1]
        delta = time.time() - timeStart# для каждого запуска своё значение
        break
time_Start2 = time.time()
while (time.time() - time_Start2) <= 15:  # снимает напряжение с АЦП и время
    time.sleep(0.1)
    listADC.append(3.24 - adc() / 256 * 3.3)
    list_time.append(time.time() - timeStart)
    print(3.24 - adc() / 256 * 3.3, "<- напряжение на проводнике ----", list_time[-1], "<- время в момент данного измерения")
    if (listADC[-1] < 0.91):
        break

Time = np.array(list_time) #создаем массив numpy с времнем для построения графиков
Voltage = np.array(listADC) #создаем массив numpy с напряжением для построения графиков
Deep = (124.3*Voltage - 112.6) #k и b необходимо взять из программы Зависимость значений АЦП от глубины

print(Voltage)
print(Time)
print(Deep)
print("Время до возмущения", delta)
print("Cкорость распространения волны:", L / delta)# для каждого запуска своё значение и его надо на бумагу записать
print("Критическое напряжение:", krit_voltage)# для каждого запуска своё значение и его надо на бумагу записать13

plt.plot(Time, Deep, label = "h(t)", color = "red")
plt.minorticks_on()

# coefs1 = np.polyfit(Time[:Time.index(krit_voltage)], Deep[:len(Time[:Time.index(krit_voltage)])], 1)#создаем коэффициенты
# func1 = np.poly1d(coefs1)#создает функцию по этим коэффициентам
# plt.plot(Time[:Time.index(krit_voltage)], func1(Time[:Time.index(krit_voltage)]), color = '#0d00ff')
# coefs2 = np.polyfit(Time[:Time.index(krit_voltage)], func1(Time[:Time.index(krit_voltage)]), Deep[:len(Time[:Time.index(krit_voltage)], func1(Time[:Time.index(krit_voltage)]))], 1)#создаем коэффициенты
# func2 = np.poly1d(coefs1)#создает функцию по этим коэффициентам
# plt.plot(Time[Time.index(krit_voltage):Time.index(krit_voltage)+20], func2(Time[Time.index(krit_voltage):Time.index(krit_voltage)+20]), color = '#0d00ff')

plt.grid(which='major')
plt.grid(which='minor', linestyle=':')
plt.tight_layout()
plt.xlabel('t, c', fontsize=10, fontweight='bold')
plt.ylabel('h, м', fontsize=10, fontweight='bold')
plt.legend()
plt.show()
GPIO.cleanup()
