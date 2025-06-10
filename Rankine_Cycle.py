# Calculator for Rankine Cycle
#from CoolProp.CoolProp import PropsSI
import CoolProp.CoolProp as CP

fluid = 'Water' #fluid set as water for rankine cycle

#User Inputs
P2 = input("Enter Boiler Pressure [kPa] ")
P2 = float(P2)
T3 = input("Enter Steam Inlet Temperature [°C] ")
T3 = float(T3)
P4 = input("Enter Turbine Exhaust Pressure [kPa] ")
P4 = float(P4)
nT = input("Enter Turbine Efficiency as a decimal ")
nT = float(nT)
nP = input("Enter Pump Efficiency as a decimal ")
nP = float(nP)
print("\n")

#Unit Conversions, using Kelvin and Pascals
P2 = P2 * 1000
P3 = P2
P4 = P4 * 1000
P1 = P4
T3 = T3 + 273.15

#Enthalpy and Entropy
s3 = CP.PropsSI('S', 'T', T3, 'P', P3, fluid)
h3 = CP.PropsSI('H', 'T', T3, 'P', P3, fluid)
s4s = s3 #Isentropic turbine outlet entropy
h4s = CP.PropsSI('H', 'S', s4s, 'P', P4, fluid) #Isentropic turbine outlet enthalpy
h4a = h3 - (nT * (h3-h4s)) #Actual turbine outlet enthalpy
x4 = CP.PropsSI('Q','P',P4,'H',h4a,fluid)

h1 = CP.PropsSI('H','Q',0,'P',P1,fluid)
T1 = CP.PropsSI('T','Q',0,'P',P1,fluid)
s1 = CP.PropsSI('S','Q',0,'P',P1,fluid)
s2s = s1
h2s = CP.PropsSI('H','S',s2s,'P',P2,fluid) #Isentropic pump discharge enthalpy
h2a = ((1/nP)*(h2s-h1))+h1




#Work and Heat Transfer, units in Joules... not kJ
wts = h3-h4s
wta = h3-h4a
qout = h4a - h1
qin = h3 - h2a
wps = h2s-h1
wpa = h2a-h1



#results
s3 = s3/1000


#print(f"Turbine inlet entropy is {s3:.4f} kJ/K")

wts = wts/1000
wta = wta/1000
qout = qout/1000
qin = qin/1000
wps = wps/1000
wpa = wpa/1000

wnet = wta - wpa
teff = wnet/qin

#print(f"Turbine isentropic work is {wts:.2f} kJ/kg")
print(f"Turbine actual work is {wta:.2f} kJ/kg")
#print(f"Pump isentropic work is {wps:.2f} kJ/kg")
print(f"Pump actual work is {wpa:.2f} kJ/kg")
print(f"Net work out is {wnet:.2f} \n")
print(f"Turbine exhaust steam quality is {x4:.3f} \n")
print(f"Condenser duty is {qout:.2f} kJ//kg")
print(f"Boiler duty is {qin:.2f} kJ/kg \n")
print(f"Thermal efficiency is {teff:.2f}")