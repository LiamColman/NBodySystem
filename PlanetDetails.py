from SolarSystemClass import Solar_System
from PlanetClass import Particle
import numpy as np

'''
This includes all of the data needed for the Main file to call from when the user selects what planets they want to use. Includes a list at the bottom so that
the user can easily input all of the planets with one input.
'''

Sun = Particle([0,0,0],[0,0,0],[0,0,0], 'Sun' , 1.988500e30, 1)

XM = 4.084217816261603E+10 
YM = 2.598240510791251E+10 
ZM =-1.623674110765200E+09
VXM=-3.568553704251848E+04 
VYM= 4.322809705093970E+04 
VZM= 6.806042593881369E+03

Mercury = Particle([XM,YM,ZM],[VXM,VYM,VZM],[0.,0.,0.],'Mercury',3.302e23,1)

Xe = 7.302579439081165E+10 
Ye = 1.284225156158267E+11 
Ze =-5.696862336628139E+06
VXe=-2.636970047250137E+04 
VYe= 1.460633029507864E+04 
VZe=-1.180673846515212

Earth = Particle([Xe,Ye,Ze],[VXe,VYe,VZe],[0.,0.,0.],'Earth',5.972e24,1)

Xm = 7.322709559870157E+10 
Ym = 1.287359352978607E+11 
Zm =-3.464250193195790E+07
VXm=-2.727967731306602E+04 
VYm= 1.514129146953787E+04 
VZm= 4.779418291023330E+01

Moon = Particle([Xm,Ym,Zm],[VXm,VYm,VZm],[0.,0.,0.],'Moon', 7.34767309e22,1)


Xj =-3.606662947981693E+11 
Yj =-7.163382023384180E+11 
Zj = 1.104531201290467E+10
VXj= 1.152278912999085E+04 
VYj=-5.264225801866817E+03 
VZj=-2.359468722813196E+02

Jupiter = Particle([Xj,Yj,Zj],[VXj,VYj,VZj],[0.,0.,0.],'Jupiter', 1898.13e24,1)

Xm = 2.010994344276515E+11 
Ym = 6.443356232519405E+10 
Zm =-3.584390472185608E+09
VXm=-6.467952444206917E+03 
VYm= 2.514421087152283E+04 
VZm= 6.855839755386750E+02

Mars = Particle([Xm,Ym,Zm],[VXm,VYm,VZm],[0.,0.,0.],'Mars', 6.4171e23,1)

Xv = 2.746789464175658E+10 
Yv = 1.042417303458428E+11 
Zv =-1.547890889359638E+08
VXv=-3.398230832120434E+04 
VYv= 8.754329805556662E+03 
VZv= 2.081159012174295E+03

Venus = Particle([Xv,Yv,Zv],[VXv,VYv,VZv],[0.,0.,0.],'Venus', 48.685e23,1)

Xs = 2.621315392424523E+11 
Ys =-1.482143569598016E+12 
Zs = 1.532961037923259E+10
VXs= 8.993685651250400E+03 
VYs= 1.647418234555717E+03 
VZs=-3.860222628062793E+02

Saturn = Particle([Xs,Ys,Zs],[VXs,VYs,VZs],[0.,0.,0.],'Saturn', 5.6834e26,1)

Xn = 4.331166068690323E+12
Yn = -1.138104249522513E+12
Zn = -7.639035634116089E+10
VXn = 1.356588852330393E+03
VYn = 5.285529678836857E+03
VZn = -1.396568226250610E+02

Neptune = Particle([Xn,Yn,Zn],[VXn,VYn,VZn],[0,0,0],'Neptune',1.024e26,1)

Xu =2.557458233202205E+12
Yu = 1.513728431054077E+12
Zu = -2.749550735243422E+10
VXu = -3.507315780532064E+03
VYu = 5.537942825667759E+03
VZu = 6.613352426198560E+01

Uranus = Particle([Xu,Yu,Zu],[VXu,VYu,VZu],[0,0,0],'Uranus',8.681e25,1)

AllPlanetDetails = [Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune]