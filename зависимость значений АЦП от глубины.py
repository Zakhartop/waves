import numpy as np
import matplotlib.pyplot as plt

with open("values_ADC_for_20mm_kalib.txt", "r") as data:
    values_ADC_20 = np.array([float(i) for i in data.read().split("\n")])

with open("values_ADC_for_40mm_kalib.txt", "r") as data:
    values_ADC_40 = np.array([float(i) for i in data.read().split("\n")])

with open("values_ADC_for_60mm_kalib.txt", "r") as data:
    values_ADC_60 = np.array([float(i) for i in data.read().split("\n")])

with open("values_ADC_for_80mm_kalib.txt", "r") as data:
    values_ADC_80 = np.array([float(i) for i in data.read().split("\n")])

with open("values_ADC_for_100mm_kalib.txt", "r") as data:
    values_ADC_100 = np.array([float(i) for i in data.read().split("\n")])

with open("values_ADC_for_120mm_kalib.txt", "r") as data:
    values_ADC_120 = np.array([float(i) for i in data.read().split("\n")])

srednee_values_ADC = np.array([sum(values_ADC_20)/len(values_ADC_20),
                                    sum(values_ADC_40)/len(values_ADC_40),
                                    sum(values_ADC_60)/len(values_ADC_60),
                                    sum(values_ADC_80)/len(values_ADC_80),
                                    sum(values_ADC_100)/len(values_ADC_100),
                                    sum(values_ADC_120)/len(values_ADC_120)])

deep = np.array([20, 40, 60, 80, 100, 120])

sr_znach_ADC = sum(values_ADC_20**2)/5
sr_znach_deep = sum(deep**2)/5

coefs = np.polyfit(srednee_values_ADC, deep, 1)# коэффициенты
func = np.poly1d(coefs)#функция по этим коэффициентам
print("Коэффициенты:", func)


plt.scatter(srednee_values_ADC, deep, c = '#0d00ff')
plt.plot(srednee_values_ADC, func(srednee_values_ADC), label = "h = 99.13U -72.51", color = "red") #Написать в названии коэффициенты
plt.minorticks_on()

plt.grid(which='major')
plt.grid(which='minor', linestyle=':')
plt.tight_layout()
plt.xlabel('Напряжение, В', fontsize=10, fontweight='bold')
plt.ylabel('Глубина, мм', fontsize=10, fontweight='bold')

plt.legend()
plt.show()
