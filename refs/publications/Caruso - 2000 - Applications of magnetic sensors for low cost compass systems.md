Applications of Magnetic Sensors for
Low Cost Compass Systems

Michael J. Caruso
Honeywell, SSEC

for  heading  determination

Abstract—A  method
is
described here that will include the effects of pitch and roll
as  well  as  the  magnetic  properties  of  the  vehicle.  Using
solid-state  magnetic  sensors  and  a  tilt  sensor,  a  low-cost
compass  system  can  be  realized.  Commercial  airlines
today use attitude and heading reference systems that cost
tens of thousands of dollars. For general aviation, or small
private  aircraft,  this  is  too  costly  for  most  pilots'  budget.
The compass system described here will provide heading,
pitch  and  roll  outputs  accurate  to  one  degree,  or  better.
The shortfall of this low-cost approach is that the compass
outputs are affected by acceleration and turns.  A solution
to this problem is presented at the end of this paper.

BACKGROUND

The  Earth’s  magnetic  field  intensity  is  about  0.5  to  0.6
gauss and has a component parallel to the Earth’s surface
that always point toward magnetic north. This field can be
approximated with a dipole model—the field points down
toward  north  in  the  Northern  Hemisphere,  is  horizontal
and  pointing  north  at  the  equator,  and  point  up  toward
north  in  the  Southern  Hemisphere.  In  all  cases,  the
horizontal direction of the Earth’s field is always pointing
toward  magnetic  north  and  is  used  to  determine  compass
direction.

Aircraft  convention  defines  the  attitude  parameters  in
terms  of  three  angles:  heading,  pitch  and  roll  (see  Figure
1).  These  angles  are  referenced  to  the  local  horizontal
plane.  That  is,  the  plane  perpendicular  to  the  earth's
gravitational vector. Heading is defined as the angle in the
local  horizontal  plane  measured  clockwise  from  a  true
North (earth's polar axis) direction. Pitch is defined as the
angle between the aircraft's longitudinal axis and the local
horizontal plane (positive for nose  up). Roll is defined as
the  angle  about  the  longitudinal  axis  between  the  local
horizontal plane and the actual flight orientation (positive
for right wing down).

1

Figure 1—Coordinate direction (X,Y,Z) and attitude
orientation (roll,pitch) on an aircraft.

The local horizontal plane  is  defined  as  the  plane  normal
to  the  earth's  gravity  vector  (see  Figure  2).  If  a  compass
was sitting in the local horizontal plane, then the roll and
pitch  angles  would  be  zero  and  the  heading  would  be
calculated as:

Heading = arcTan (Yh/Xh)

(1)

where Xh and Yh represent the earth's horizontal magnetic
field  components.  As  the  aircraft  is  rotated,  the  heading
would  sweep  0°  to  360°  referenced  to  magnetic  north.  If
the compass were now tilted, the tilt angles (roll and pitch)
and all three  magnetic  field components (X,Y,Z)  must be
used in order to calculate heading [1].

TILT DETERMINATION

One method to determine the roll and pitch angles is to use
a tilt sensor that senses the direction of gravity.  Common
tilt measuring devices include accelerometers, electrolytic
(fluid)  based  tilt  sensors,  and  gimbaled  mechanical
local
structures.  Another  method
horizontal plane is to use a gyroscope to maintain a known
inertial reference orientation at all times.

to  determine

the

tilt sensor

-roll

pitch

Xh

local horizontal plane

Yh

gravity
vector

Tilt Sensor

3 - Axis
Magnetic
Sensor

Roll

Pitch

X

Y

Z

Analog to
Digital
Converter

µProcessor
interface and
algorithm

Tilt compensated
azimuth or heading

Figure 2—Tilt sensor angles are referenced
to the local horizontal plane defined by gravity.

Figure 3—Compass system block diagram.

Gyroscopes  (gyros)  are  instruments  used  to  measure
precise  angular  motion.  Several  techniques  are  used  to
achieve this such as spinning wheels, vibrating structures,
and  ring  lasers.  The  output  signal  is  proportional  to  the
angular rate of turn. A key consideration when using gyros
is the output drift with time. With periodic correction, the
drift can be compensated for and provide very high levels
of accuracy for roll, pitch, and heading. Gyros are standard
in  navigation  instrument  on  commercial  aircraft  and  will
operate  well  under  accelerating  conditions.  When
compared  to  tilt  sensors,  though,  gyros  tend  to  be  bulky
and expensive and will not be considered here.

Tilt sensors come in many types and sizes. The gimbaled
tilt device usually has two rings mounted at right angles to
each other much like a dual pendulum. A magnetic sensor,
or  compass,  inside of the gimbaled structure  will  remain
suspended in the local horizontal plane for various roll and
pitch  angles.  The  mechanical  structure  of  the  gimbal
makes it susceptible to shock and vibration and can often
take  seconds  for  it  to  become  stable  after  movement.
Gimbaled  compasses  only  require  two  axes  of  magnetic
sensing since the roll and pitch angles are never present in
a  steady-state  condition.  However,  since  the  magnetic
sensors  change  orientation  with  the  compass  platform,
these compasses cannot compensate for the ferrous effects
of its surroundings.

tilt

sensors  measure

Low cost tilt sensors like the two-axis electrolytic and dual
axis  accelerometer  measure  the  roll  and  pitch  angle
directly. Liquid filled electrolytic tilt sensors, resembling a
glass  “thimble”,  use  electrodes  to  monitor  the  fluid
movement  as  the  sensor  changes  angles.  Solid  state
accelerometer
the  Earth’s
gravitational  field  by  means  of  an  electromechanical
circuit [2]. These sensors are similar in that they have two
single axis components that  measure  the  angle  deviations
from  the  local  horizontal  plane.  Signal  conditioning
circuits are used to create an output signal proportional to
the  angle  of  tilt.  These  sensors  are  considered  strapdown
devices since they have no moving or pendulous parts and
are desirable for vehicle applications [3].

COMPASS SYSTEM

If  a  strapdown  compass  is  required  to  output  heading  for
any  orientation  then,  as  a  minimum,  a  compass  system
must have a three-axis magnetic sensor and a two-axis tilt
(see Figure 3). The heading calculation relies on all three
magnetic components (X,Y,Z) so the compass orientation
can  be  mathematically  rotated  to  the  horizontal  plane.
Then,  the  Xh  and  Yh  components  can  be  calculated  to
determine the heading value from equation (1).

In Figure 2, a compass is shown with roll (q ) and pitch (f )
tilt  angles  referenced  to  the  right  and  forward  level
directions.  The  X,  Y,  and  Z  magnetic  readings  can  be
transformed to the horizontal plane (Xh, Yh) by applying
the  rotation  equations  shown  in  equation  (2).  If  these
equations are not  used, then appreciable errors will result
in the heading calculations as shown in Figure 4.

  Xh = X*cos(f ) + Y*sin(q )*sin(f ) - Z*cos(q )*sin(f )
  Yh = Y*cos(q ) + Z*sin(q )

(2)

Once the magnetic components are found in the horizontal
plane, equation (1) can be used to determine  heading. To
minimize processing time,  a  sine and  cosine lookup table
can  be  stored  in  program  memory.  To  account  for  the
arcTan  limits,  the  heading  calculations  must  account  for
the sign of the Xh and Yh readings as shown in (3).

Heading for (Xh <0)  = 180 - arcTan(Yh/Xh)
for (Xh >0, Yh <0) = - arcTan(Yh/Xh)
for (Xh >0, Yh >0) = 360 - arcTan(Yh/Xh)
for (Xh =0, Yh <0) = 90
for (Xh =0, Yh >0) = 270

(3)

2

10

)
e
e
r
g
e
d
(

r
o
r
r

5

0

i

E
g
n
d
a
e
H

-5

pitch (degree)

-10

-5

-2

2

5

10

-10

0

90

180
Heading (degree)

270

360

Figure 4—Heading errors due to pitch without tilt compensation
(Dip Angle =40°).

COMPASS ERROR ANALYSIS

If a compass system has a requirement of better than one
degree of accuracy, then it is important to break down the
error contributed by the tilt sensor and the magnetic sensor
and determine what level of signal processing is required.
Specifically, heading accuracy is affected by:

4   A/D converter resolution
4   Magnetic sensor errors
4   Temperature effects
4   Nearby ferrous materials
4   Compass tilt errors
4   Variation of the earth's field

A/D  Converter  Resolution—To  achieve  a  one-degree
accurate  compass  requires  a  magnetic  sensor  that  can
reliably resolve angular changes to 0.1°. The sensors must
also  exhibit  low  hysteresis  (<0.08%FS),  a  high  degree  of
linearity  (<0.05%FS)  and  be  repeatable.  The  magnetic
fields in the X and Y horizontal plane will typically be in
the 200 mgauss range—more at the equator, less near the
poles.

Using  the  standard  heading  relationship  of  equation  (1),
the  required  A/D  converter  resolution  for  the  magnetic
sensors  can  be  estimated.  If  the  magnetometer  error,  or
uncertainty, is allowed to be 0.1° then:

if:
then:

Error = 0.1° = arcTan(Yh/Xh)
Yh/Xh = 1/573

(4)

This implies that a ratio change of 1 part in 573 will result
in a 0.1° difference. If X and Y were read with a nine-bit
A/D converter there would be only a 1:512 bit resolution.
This means that a 9+ bit A/D converter is needed to meet
the  0.1°  error budget  for  an  (X,Y)  magnetic  field  change
of  200  mgauss.  Since  the  (X,Y)  magnetic  fields  measure
±200  mgauss  for  a  complete  heading  sweep,  the  A/D
converter range should be doubled,  to 10+  bits. To  allow
for hard iron correction  and  larger  horizontal  fields—like
at  the  equator—this  range  should  be  quadrupled  to  ±800
mgauss. Now the A/D converter resolution should be 12+
bits, or 12.163 bits to be more exact.

A  12  bit  A/D  converter  can  be  used  to  provide  a  0.1°
resolution  in  a  200  mgauss  horizontal  field.  This  implies
that the sensor must be able to resolve a 0.39 mgauss field
over a span of ±800 mgauss (1.6 gauss/4096 counts).

Magnetic  Sensor  Errors—Solid  state  magneto-resistive
(MR)  sensors  available  today  can  reliably  resolve  <0.07
mgauss fields [4-7]. This is more than a five times margin
over  the  0.39  mgauss  field  required  to  achieve  0.1°
resolution.

Other  magnetic sensor  specifications  should  support  field
measurement  certainty  better  than  0.5°  to  maintain  an
overall  1°  heading  accuracy.  These  include  the  sensor
noise, linearity, hysteresis, and repeatability errors.

Any gain and offset errors of the magnetic sensor will be
compensated
iron  calibration
(discussed  later)  and  will  not  be  considered  in  the  error
budget.

for  during

the  hard

MR  sensors  can  provide  a  total  error  of  less  than  0.5
mgauss,  which  corresponds  to  a  0.14°  heading  error  as
shown in Table 1.

Parameter

Noise
(BW=10Hz)

Linearity

Hysteresis

Repeatabilit
y

Spec
Limit (1)

Field
Error

Heading
Error

85 ugauss

85 ugauss

<0.01°

0.05 %FS

0.2 mgauss

0.08 %FS

0.32 mgauss

0.08 %FS

0.32 mgauss

0.06°

0.09°

0.09°

Total rms
error

0.49 mgauss

0.14°

(1)  Typical specs for HMC1021/22 MR sensors; FS=400

mgauss

Table 1—Error budget for an MR magnetic sensor

3

temperature

temperature  and

Temperature  Effects—The
coefficient
(tempco)  of  the  sensor  will  also  affect  the  heading
accuracy.  There  are  two  characteristics  of  temperature  to
consider—the  offset  drift  with
the
sensitivity tempco. The sensitivity tempco will appear as a
change  in  output  gain  of  the  sensor  over  temperature
(Figure 5). MR sensors generally have sensitivity tempcos
that  are  well  correlated,  or  matched—especially  sensors
with  two  (X,Y)  axes  in  the  same  package.  The  matching
tempcos imply that the output change over temperature of
the  X  axis  will  track  the  change  in  output  of  the  Y  axis.
This effect will cancel itself since it is the ratio of Y over
X  that  is  used  in  the  heading  calculation  [Azimuth  =
arcTan(Y/X)].  For  example,  as  the  temperature  changes
the  Y  reading  by  12%,  it  also  changes  the  X  reading  by
12%  and
is  canceled.  The  only
consideration is then the dynamic input range of  the  A/D
converter.

the  net  change

The  magnetic  sensor  offset  drift  with  temperature  is  not
correlated and may in fact drift in opposite directions. This
will  have  a  direct  affect  on  the  heading  and  can  cause
appreciable  errors.  There  are  many  ways  to  compensate
for  temperature  offset  drifts  using  digital  and  analog
circuit  techniques.  A  simple  method  to  compensate  for
temperature  offset  drifts  in  MR  sensors  is  to  use  a
switching technique referred to as set/reset switching. This
technique  cancels  the  sensor  temperature  offset  drift,  and
the dc offset voltage as well as the amplifier offset voltage
and its temperature drift.

The transfer curves for a MR magnetic sensor after it has
been set, and then reset, is shown in Figure 6. The set/reset
modes  are  achieved  by  using  an  ac  coupled  driver  to
generate a bi-directional current

)

V
m

(

t
u
p
t
u
O

r
o
s
n
e
S

-2.0

-1.5

-1.0

50

40

30

20

10

0

-10

-0.5

0.0
Applied Field (gauss)

0.5

25° C

75° C

125° C

175° C

200° C

1.0

1.5

2.0

Figure 5—Magnetic sensor output temperature variation
has a pivot point at zero applied field.

4

)

V
m

(

t
u
p
t
u
O
e
g
d
i
r

B

15

10

5

0

-5

-10

-15

-20

Reset

Set

-2

-1

0
Applied Field (gauss)

1

2

Figure 6—Set and reset output transfer curves.

pulse [7]. The two  curves  result  from  an  inversion  of  the
gain  slope  with  a  common  crossover  point  at  the  offset
voltage. For the sensor in Figure 6, the sensor offset is –3
mV.  This  from
the
manufacture  process.  This  offset  is  not  desirable  and  can
be  eliminated  using  the  set/reset  switching  technique
described  below.  Other  methods  of  offset  compensation
are described in ref. [8].

the  resistor  mismatch  during

The  sensor  offset  (Vos)  can  be  eliminated  by  using  a
simple  subtraction  technique.  First  apply  a  set  pulse,
measure  Happlied  and  store  it  as  Vset—Figure  7.  Then
apply  a  reset  pulse  and  store  that  reading  as  Vreset.
Subtract these two readings to eliminate Vos:

Vset = S *Happlied + Vos
Vreset = -S* Happlied + Vos

Vset - Vreset =  S *2* Happlied

(5)
(6)

(7)

The sensor sensitivity (S) is expressed in mV/gauss. Note
that  equation  (7)  has  no  Vos  term.  This  method  also
eliminates the amplifier offset  as  well.  Another  benefit  is
that  the  temperature  drift  of  the  sensor  offset  and  the
amplifier is eliminated! Now, a low cost amplifier can be
used  without  concern  for  its  offset  effects.  This  is  a
powerful  technique  and  is  easy  to  implement  if  the
readings are controlled by a low cost  microprocessor.

Using  this  technique  to  reduce  temperature  effects  can
drop the overall variation in magnetic readings to less than
0.01%/°C.  This  amounts  to  less  than  0.29°  effect  on  the
heading accuracy over a 50°C temperature change.

Vout

Vset

Vos

Vreset

Happlied

time

Happlied

Set

Set

Set/Reset
Pulse

Rst

Figure 7—Set and reset effect on sensor output (Vout)
show the peak-to-peak level is 2*Happlied.

Nearby  Ferrous  Materials—Another  consideration  for
heading accuracy is the effects of nearby ferrous materials
on  the  earth's  magnetic  field  [9-11].  Since  heading  is
based  on  the  direction  of  the  earth's  horizontal  field
(Xh,Yh), the magnetic sensor must be able to measure this
field  without  influence  from  other  nearby  magnetic
sources  or  disturbances.  The  amount  of  disturbance
depends  on  the  material  content  of  the  platform  and
connectors  as  well  as  ferrous  objects  moving  near  the
compass.

When  a  ferrous  object  is  placed  in  a  uniform  magnetic
field it will create disturbances as shown in Figure 8. This
object could be a steel bolt or bracket near the compass or
an iron door latch close to the compass. The net result is a
characteristic  distortion,  or  anomaly,
the  earth’s
magnetic field that is unique to the shape of the object.

to

looking  at

Before
the  effects  of  nearby  magnetic
disturbances,  it  is  beneficial  to  observe  an  ideal  output
curve  with  no  disturbances.  When  a  two-axis  (X,Y)
magnetic  sensor  is  rotated  in  the  horizontal  plane,  the
output plot of Xh vs. Yh will form a circle centered at the
(0,0)  origin  (see  Figure  9).  If  a  heading  is  calculated  at
each point on the circle, the  result  will  be  a  linear  sweep
from 0° to 360°.

Ferrous  Object  +  Uniform  Magnetic  Field  =  Field
Disturbance

Figure 8–Ferrous object disturbance in uniform field.

5

)
s
s
u
a
g
m

(

i

l

d
e
F
c
i
t
e
n
g
a
M
h
Y

200

100

0

0

-100

-200

-200

-100

100

200

Xh Magnetic Field (mgauss)

Figure 9—Magnetic sensor outputs (X,Y) rotated
horizontally in the earth’s field with no disturbances.

iron  effects.  Hard

The  effect  of  a  magnetic  disturbance  on  the  heading  will
be  to  distort  the  circle  shown  in  Figure  9.  Magnetic
distortions can be categorized as two types—hard iron and
soft
iron  distortions  arise  from
permanent  magnets  and  magnetized  iron  or  steel  on  the
compass  platform.  These  distortions  will  remain  constant
and  in  a  fixed  location  relative  to  the  compass  for  all
heading  orientations.  Hard  iron  effects  add  a  constant
magnitude field component along each axes of the sensor
output.  This  appears  as  a  shift  in  the  origin  of  the  circle
equal  to  the  hard  iron  disturbance  in  the  Xh  and  Yh  axis
(see  Figure  10).  The  effect  of  the  hard  iron  distortion  on
the heading is a one-cycle error and is shown in Figure 11.

To  compensate  for  hard  iron  distortion,  the  offset  in  the
center  of  the  circle  must  be  determined.  This  is  usually
done by rotating the compass and platform in a circle and
measure  enough  points  on  the  circle  to  determine  this
offset.  Once  found,  the  (X,Y)  offset  can  be  stored  in
memory and subtracted from every reading. The net result
will  be  to  eliminate  the  hard  iron  disturbance  from  the
heading calculation; as if it were not present[1].

The  soft  iron  distortion  arises  from  the  interaction  of  the
earth’s  magnetic  field  and  any  magnetically  soft  material
surrounding the compass. Like the hard iron materials, the
soft  metals  also  distort  the  earth’s  magnetic  field  lines.
The  difference  is  the  amount  of  distortion  from  the  soft
iron  depends  on  the  compass  orientation.  Soft  iron
influence on the field values measured by X and Y sensors
are  depicted  in  Figure  12.  Figure  13  illustrates  the
compass  heading  errors  associated  with  this  effect—also
known as a two cycle error.

150

50

20

10

)
e
e
r
g
e
d
(

-200

-100

0

-50

100

200

-150

-250

r
o
r
r

i

E
g
n
d
a
e
H

90

180

270

360

0

0

-10

-20

)
s
s
u
a
g
m

(

r
o
s
n
e
S
s
x
a
-

Y

i

X-axis Sensor (mgauss)

Heading (degree)

Figure 10— Hard iron offsets when rotated
horizontally in the earth’s field.

Figure 11— Heading error due to hard iron effects known as
single-cycle errors.

)
s
s
u
a
g
m

(

t
u
p
t
u
O
h
Y

-200

-100

200

100

0

0

-100

-200

100

200

0

90

180

270

360

4

2

0

-2

-4

-6

-8

)
e
e
r
g
e
d
(

r
o
r
r

i

E
g
n
d
a
e
H

Xh Output (mgauss)

Heading (degree)

Figure 12—Soft iron distortion when rotated
horizontally in the earth’s field.

Figure 13— Heading error due to soft iron effects known as
two-cycle errors.

Compensating for soft iron effects is a bit  more difficult
than  for  hard  iron  effects.  This  involves  a  bit  more
calculation than a simple subtraction. One way to remove
the  soft  iron  effect  is  to  rotate  the  reading  by  45°,  scale
the major axis to change the ellipse to a circle, then rotate
the  reading  back  by  45°.    This  will  result  in  the  desired
circular output response shown in Figure 9.

Most  ferrous  material  in  vehicles  tend  to  have  hard  iron
characteristics. The best approach is to eliminate any soft
iron  materials  near  the  compass  and  deal  with  the  hard
iron  effects  directly.  It  is  also  recommended  to  degauss
the platform near the compass prior to any hard/soft iron
compensation.

Some  compass  manufacturers  provide  calibration
methods to compensate for the hard and soft iron effects.
Each  calibration  method  is  associated  with  a  specified
physical  movement  of  the  compass  platform  in  order  to
sample the magnetic space surrounding the compass. The
calibration  procedure  can  be  as  simple  as  pointing  the
host  in  three  known  directions,  or  as  complicated  as
moving  in  a  complete  circle  with  pitch  and  roll,  or

6

pointing the host in 24 orientations including variations in
tilt. It is impossible for a marine vessel to perform the 24-
point calibration, but easy for a hand-held platform. If the
compass  is  only  able  to  sample  the  horizontal  field
components  during  calibration,
there  will  be
uncompensated  heading  errors  with  tilt.  Heading  error
curves  can  be  generated  for  several  known  headings  to
improve heading accuracy [10,11].

then

Hard and  soft  iron  distortions  will  vary  from  location  to
location within the same platform. The compass has to be
mounted  permanently  to  its  platform  to  get  a  valid
calibration. A particular calibration is only  valid  for  that
location  of  the  compass.  If  the  compass  is  reoriented  in
the  same  location,  then  a  new  calibration  is  required.  A
gimbaled compass can not satisfy these requirements and
hence the advantage of using a strapdown, or solid state,
magnetic  sensor. It is  possible  to  use  a  compass  without
any  calibration  if  the  need  is  only  for  repeatability  and
not accuracy.

location—sometimes  being  as  large  as  25°.  To  account
for  the  variation  simply  add,  if  Westerly,  or  subtract,  if
Easterly,  the  variation  angle  from  the  corrected  heading
computation.

The  variation  angles  have  been  mapped  over  the  entire
globe.  For  a  given  location  the  variation  angle  can  be
found by using a geomagnetic declination map or a GPS
(Global Positioning System) reading and an IGRF model.
The International Geomagnetic Reference Field (IGRF) is
a  series  of  mathematical  models  describing  the  earth's
field  and  its  time  variation  [12-14].  After  heading  is
determined, the variation correction can be applied to find
true  north  according
the  geographic  region  of
operation.

to

COMPASS INSTALLATION

The performance of a compass will greatly depend on its
installation  location.  A  compass  depends  on  the  earth’s
magnetic field to provide heading. Any distortions of this
magnetic  field  by  other  sources  should  be  compensated
for in order to determine an accurate heading. Sources of
magnetic  fields  include  permanent  magnets,  motors,
electric  currents—either  dc  or  ac,  and  magnetic  metals
such  as  steel  or  iron.  The  influence  of  these  sources  on
compass accuracy can be  greatly  reduced  by  placing  the
compass far from them. Some of the field effects can be
compensated by calibration. However, it is not possible to
time  varying  magnetic  fields;  for
compensate  for
example,  disturbances  generated  by
the  motion  of
magnetic  metals,  or  unpredictable  electrical  current  in  a
nearby  wire.  Magnetic  shielding  can  be  used  for  large
field disturbances from motors or speakers. The best way
to reduce disturbances is distance. Also, never enclose the
compass in a magnetically shielded metallic housing.

ACCELERATION EFFECTS

Any  acceleration  of  the  compass  will  effect  the  tilt  or
accelerometer  outputs  and  will  result  in  heading  errors.
An  aircraft  making  a  turn  will  cause  the  tilt  sensors  to
experience the centripetal force in addition to gravity and
the compass heading will be in error. However, for most
applications the acceleration is small, or is in effect for a
short  duration,  making  a  magnetic  compass  a  useful
navigation  tool.  Inertial  reference  systems  would  be  the
solution  for  applications  that  can  not  tolerate  these
heading  errors.  These  systems  would  weigh,  cost,  and
consume  power  at  least  10  times  more  than  those  of  a
strapdown magnetic compass.

)
s
e
e
r
g
e
d
(

r
o
r
r
E
g
n
d
a
e
H

i

0.6

0.4

0.2

0.0

-0.2

-0.4

-0.6

.3P / 0R

.2P / 0R

0P / .1R

.1P / 0R

0

90

180

270

360

.2P / .2R

Heading (degrees)

Figure 14—Heading error due to roll and pitch tilt errors
(.2P/.2R = .2° error in pitch and roll).

Compass  Tilt  Errors—Heading  errors  due  to  the  tilt
sensor  depend  somewhat  on  geographic  location.  At  the
equator, tilt errors are less critical since the earth's field is
strictly  in  the  horizontal  plane.  This  provides  larger  Xh
and  Yh  readings  and  little  Z  component  correction  [ref.
Equation  (2)].  Near  the  magnetic  poles,  tilt  errors  are
extremely important—since there is less Xh,Yh field and
more Z component. Tilt errors are also dependent on the
heading [ref. Figure 4].

Tilt sensors also have offset, gain errors, and temperature
effects  that  need  to  be  accounted  for.  These  will  not  be
compensated  for  during  hard/soft  iron  calibration,  as  in
the case for the magnetic sensors. The offset error can be
zeroed out after installation and will include any platform
temperature  drifts,
leveling  error.  Also,
linearity,
repeatability,  hysteresis
  and  cross-axis  effects  are
important.  The  tilt  sensor  usually  contributes  the  largest
percentage of error to the heading calculation.

For  a  one  degree  compass,  a  tilt  sensor  with  0.1°
resolution is desired. The total error introduced by the tilt
sensor  should  be  less  than  0.5°.  The  curve  in  Figure  14
shows the effect on heading for various tilt sensor errors.
In this Figure, a pitch error of 0.3° and no roll error can
contribute a 0.5° error alone.

Variation  of  the  Earth’s  Field—The  final  consideration
for  heading  accuracy  is  the  variation,  or  declination,
angle. It is well known that the earth's magnetic poles and
its  axis  of  rotation  are  not  at  the  same  geographical
location.  They  are  about  11.5°  rotation  from  each  other.
This  creates  a  difference  between  the  true  north,  or  grid
north,  and  the  magnetic  north,  or  direction  a  magnetic
compass  will  point.  Simply  it  is  the  angular  difference
between  the  magnetic  and  true  north  expressed  as  an
Easterly or Westerly variation. This difference is defined
as  the  variation  angle  and  is  dependent  on  the  compass

7

CONCLUSION

[4] B.B. Pant, “Magnetoresistive Sensors”, Scientific
Honeyweller, vol. 8, no.1, (Fall 1987) 29-34.

A low cost compass has been discussed here having a one
degree accuracy requirement. At the heart of the compass
is  a  three-axis  MR  magnetic  sensor  and  a  two-axis
electrolytic  tilt  sensor.  Other  circuits  include  a  12  to  14
bit  A/D  converter,  signal  conditioning  electronics  and  a
microprocessor.  The  error  budget  for  heading  accuracy
breaks down as:

Magnetic sensor error
Temperature effects
Signal conditioning
Tilt sensor error

Total Error

0.14°
0.29°
0.05°
0.50°
0.98°

The  effects  of  nearby  magnetic  distortions  can  be
calibrated out of the compass readings once it is secured
to  the  platform.  Caution  must  be  taken  in  finding  a
compass  location  that  is  not  too  near  varying  magnetic
disturbances  and  soft  iron  materials.  Shielding  effects
from  speakers  and  high  current  conductors  near  the
compass may be necessary.

Variations  in  the  earth's  field  from  a  true  north  heading
can  be  accounted  for  if  the  geographical  location  of  the
compass is known. This can be achieved by using a map
marked  with  the  deviation  angles  to  find  the  correct
heading  offset  variation;  or  use  a  GPS  system  and  the
IGRF reference model to compute the variation angle.

to

Low  cost  compasses  of  the  type  described  here  are
errors  during
temporary  heading
susceptible
accelerations  and  banked  turns.  The  heading  accuracy
will be restored once these accelerations diminish. With a
strapdown  compass  there  is  no  accuracy  drift  to  worry
about  since  the  heading  is  based  on  the  true  earth's
magnetic field. They tend to be very rugged to shock and
vibration  effects  and  consume  very  low  power  and  are
small in size.

[5] J.E. Lenz, G.F.Rouse, L.K. Strandjord, B.B.Pant,
A.Metze, H.B.French, E.T.Benser, D.R.Krahn, “A Highly
Sensitive Magnetoresistive Sensors”, Solid State Sensors
and Actuator Workshop, 1992.

[6] J.Goetz, T.Bratland, M.Caruso, “Designing with
Magnetoresistive Sensors”, Sensor Expo Workshop,
Philadelphia, October, 1996.

[7] Sensor Products Data Sheet, "1 and 2 Axis
Magnetoresistive Microcircuits", Honeywell SSEC, 5/99,
<www.magneticsensors.com>.

[8] M.J.Caruso, T.Bratland, C.H.Smith, R.Schneider, “A
New Perspective on Magnetic Field Sensing”, Sensors
Expo Proceedings, October 1998, 195-213.

[9] M.J.Caruso, L.S. Withanawasam, “Vehicle Detection
and Compass Applications using AMR Magnetic
Sensors”, Sensors Expo Proceedings, May 1999, 477-
489.

[10] C.A. Lund, Compasses in Small Craft", Glasgow,
Scotland: Brown, Son & Ferguson, Ltd., 1983, 39-62.

[11] W. Denne, Magnetic Compass Deviation and
Correction, Glasgow, Scotland: Brown, Son & Ferguson,
Ltd., 1998.

[12] Y. Zhao, Vehicle Location and Navigation Systems,
Norwood, MA: Artech House, Inc, 1997, Chapter 3.

[13] National Geomagnetic Information Center, website
URL <http://geomag.usgs.gov/>

[14] National Geophysical Data Center, website URL
<http://www.ngdc.noaa.gov/>

Unit conversion from SI to Gaussian:
    79.6 A/m = 1 oersted
    1 gauss = 1 oersted (in free air)
    1 gauss = 10-4 tesla = 105 gamma
    1 nanotesla = 10 microgauss = 1 gamma

REFERENCES

[1] M.J. Caruso, “Application of Magnetoresistive
Sensors in Navigation Systems”, Sensors and Actuators
1997, SAE SP-1220, (Feb. 1997) 15-21.

[2] M. Horton, C. Kitchin, “A Dual Axis Tilt Sensor
Based on Micromachined Accelerometers”, Sensors,
(April 1996).

[3] Olson, Gregory J., et al, “Nongimbaled Solid-State
Compass”, Solid-State Sensor and Actuator Workshop,
June, 1994.

8
