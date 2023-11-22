import numpy as np
import matplotlib.pyplot as plt

deep = np.log(np.array([60, 80, 100]))
speed = np.log(np.array([829, 1020, 1161]))

sr_znach_kv_deep = sum(deep**2)/5
sr_znach_deep_kv = (sum(deep)/5)**2
sr_znach_kv_speed = sum(speed**2)/5
sr_znach_speed_kv = (sum(speed)/5)**2

coefs = np.polyfit(deep, speed, 1)#создаем коэффициенты
func = np.poly1d(coefs)#создает функцию по этим коэффициентам
print("Коэффициенты:", func)
sigma_b = (1/(5**0.5))*(((sr_znach_kv_speed - sr_znach_speed_kv)/(sr_znach_kv_deep - sr_znach_deep_kv))**0.5)
sigma_a = sigma_b*((sr_znach_kv_speed - sr_znach_speed_kv)**0.5) -2
print("Погрешности", sigma_a, sigma_b)

plt.scatter(deep, speed)
plt.plot(deep, func(deep), label = "Апроксимирующая прямая графика log(V) от log(t) \n "
                                   "ln(c) = 0.62*ln(h) + 4.21 \n "
                                   "a = 0.62 \u00B1 0.41\n"
                                   "b = 4.21 \u00B1 0.71", color = "red")#вбить значения погрешностей
plt.minorticks_on()

plt.grid(which='major')
plt.grid(which='minor', linestyle=':')
plt.tight_layout()
plt.xlabel('ln(h), мм', fontsize=10, fontweight='bold')
plt.ylabel('ln(c), мм/c', fontsize=10, fontweight='bold')

plt.legend()
plt.show()