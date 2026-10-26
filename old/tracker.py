from sgp4.api import Satrec
from sgp4.api import jday
# import variables as vl
from datetime import datetime, timezone
import tleLoader as tle




sat = Satrec.twoline2rv(tle.line1,tle.line2)
# this takes the two lines from TLE and returns a satellite object

# print(vl.line1)
# print(vl.line2)

#jd,fr = jday(2026,10,13,17,30,15)
now = datetime.now(timezone.utc)
jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second + now.microsecond / 1e6)
# sgp4 needs the time as a julian date

result = sat.sgp4(jd,fr)
# this returns the position of the satellite
# in (e,r,v)
# e is error code (0 is success), r = position (km), v = velocity (a three-number typle describing how quickly the satellite is moving in each coreesponding direction)
# r is three numbers (x,y,z) in kilometers from the earth's center, not latitude and longitude
# v is velocity: ~~~~~~~~~~

# FOR FUTURE FIX:   if e returns anything other than 0, then disgard the TLE lines and wait
#   for another batch


# from last run: r = (1152.8623888232212, 6603.221241129225, 1143.1773926696235)
#   v = (-4.92133444877243, -0.15899214543228152, 5.866152468046533)
print('\n')
print(result)
print('\n')


# TEME is a coordinate frame