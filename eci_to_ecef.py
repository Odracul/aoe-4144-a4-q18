# eci_to_ecef.py
#
# Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km...
#   converts eci to ecef frame

# Parameters: ECI coordinates and date
#   year:
#   month: 
#   day:
#   hour:
#   minute:
#   second:
#   eci_x_km:
#   eci_y_km:
#   eci_z_km:

# Output:
#   ?
#
# Written by Lucas Libovicz-Kilgore

# import Python modules
import math # math module
import sys # argv
import numpy as np

# constants
R_E_KM = 6378.137
E_E    = 0.081819221456


# initialize script arguments
year = float('nan') 
month = float('nan') 
day = float('nan') 
hour = float('nan')
minute = float('nan')
second = float('nan')
eci_x_km = float('nan')
eci_y_km = float('nan')
eci_z_km = float('nan')

# parse script arguments
if len(sys.argv) == 10:
  year = float(sys.argv[1])
  month = float(sys.argv[2])
  day = float(sys.argv[3])
  hour = float(sys.argv[4])
  minute = float(sys.argv[5])
  second = float(sys.argv[6])
  eci_x_km = float(sys.argv[7])
  eci_y_km = float(sys.argv[8])
  eci_z_km = float(sys.argv[9])
else:
  print(\
    'Usage: '\
    'python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km'\
  )
  exit()

### script below this line ###

# calculate
#Converting to Julian Date
JD = int(day-32075 + 1461*(year+4800+(month-14)/12)/4 + 367*(month-2-(month-14)/12*12)/12 - 3*((year+4900+(month-14)/12)/100)/4)
JDmid = JD - 0.5
Dfrac = (second + 60*(minute + 60*hour))/86400
jd_frac = JDmid + Dfrac

#Finding theta GMST
w = 7.292115 * 10**-5
T_uti = (jd_frac - 2451545)/36525
Theta_GMST = math.fmod(67310.54841 + (876600*60*60 + 8640184.812866)*T_uti + 0.093104*T_uti**2 +  -6.2*10**-6*T_uti**3, 86400)
if Theta_GMST < 0:
   Theta_GMST = Theta_GMST + 86400
Theta_GMST_final= Theta_GMST * w 
print(Theta_GMST_final)
#If rounding is required
Theta_GMST_final = round(Theta_GMST_final,6)

Rz = np.array([[math.cos(-1*Theta_GMST_final), -1*math.sin(-1*Theta_GMST_final), 0],
               [math.sin(-1*Theta_GMST_final), math.cos(-1*Theta_GMST_final), 0],
               [0, 0, 1]])

eci = np.array([eci_x_km, eci_y_km, eci_z_km])

ecef = np.dot(Rz,eci)

ecef_x_km = ecef[0]
ecef_y_km = ecef[1]
ecef_z_km = ecef[2]

print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)