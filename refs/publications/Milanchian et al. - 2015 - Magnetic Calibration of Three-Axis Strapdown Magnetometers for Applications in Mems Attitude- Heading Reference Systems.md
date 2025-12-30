         Amirkabir University of Technology
    (Tehran Polytechnic)
       Vol. 47 - No. 1 - Spring 2015, pp. 55- 65

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)

)

AIJ-MISC)

Magnetic Calibration of Three-Axis Strapdown
Magnetometers for Applications in Mems Attitude-
Heading Reference Systems

Hamed Milanchian1, Jafar Keighobadi1 and Hossein Nourmohammadi1*

1-Department of Mechanical Engineering, University of Tabriz, Tabriz, Iran

ABSTRACT

In a strapdown magnetic compass, heading angle is estimated using the Earth's magnetic field measured
by  Three-Axis  Magnetometers  (TAM).  However,  due  to  several  inevitable  errors  in  the  magnetic  system,
such  as  sensitivity  errors,  non-orthogonal  and  misalignment  errors,  hard  iron  and  soft  iron  errors,
measurement noises and local magnetic fields, there are large error between the magnetometers' outputs and
actual  geomagnetic  field  vector.  This  is  the  necessity  of  magnetic  calibration  of  TAM,  especially  in
navigation  application  to  achieve  the  true  heading  angle.  In  this  paper,  two  methodologies,  including
clustering  swinging  method  and  clustering  velocity  vector  method  are  presented  for  magnetic  compass
calibration. Several factors for clustering process have been introduced and analyzed. The algorithms can be
applied  in  both  low-cost  MEMS  magnetometer  and  high-accuracy  magnetic  sensors.  The  proposed
calibration algorithms have been evaluated using in-ground and in-flight tests. It can be concluded from the
experimental  results  that,  applying  the  clustering  calibration  algorithms  bring  about  a  considerable
enhancement in the accuracy of magnetic heading angle

KEYWORDS

Magnetic  Calibration,  Magnetic  heading  angle,  clustering  calibration  method,  Swinging  method,

Velocity vector method.

٭Corresponding Author, Email: <hnourmohammadi@tabrizu.ac.ir>

 Vol. 47 - No. 1 - Spring 2015

   55

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Hamed Milanchian, Jafar Keighobadi, and Hossein Nourmohammadi

1. INTRODUCTION

To  determine  heading  angle  of  a  vehicle,  three-axis
MEMS  magnetic  compasses  are  widely  used  in  low-cost
attitude-heading  reference  systems  (AHRS).  In
the
AHRS, 3-axis orientations of a vehicle, including, attitude
and  heading  angles  are  estimated.  These  angles  are  also
),  pitch
called  as  Euler  angles  characterized  by  roll  (

(

)  and  yaw  (

).  In  order  to  improve  the  AHRS

the

performance  and  accuracy,  it  can  be  integrated  with  the
magnetic  compass  system.  Magnetic  compass  comprises
three-axis  magnetometer  which  should  be  coupled
appropriately  with
inertial  sensors  of  Inertial
Measurement  Unit  (IMU),  i.e.  gyros  and  accelerometers
[1]. Precise calibration of the TAM has a crucial effect on
the  attitude-heading  accuracy  of  the  AHRS  systems
integrated  with  magnetic  compass.  An  important  issue
with  the  integrated  AHRS/Magnetic  systems  is  that  the
magnetic  compass
the
is  greatly
environmental  effects.  For  example,  all  vehicles  are
partially  made  of  iron-based  materials  that  can  generate
magnetic  fields.  Therefore,  the  magnetic  field  measured
by  a  compass  is  indeed  a  combination  of  the  Earth’s
magnetic  field,
induced  magnetic  field  of  the
magnetized  vehicle  body  and  other  magnetic  anomalies
caused  by  the  environmental  effects  [2].  To  estimate  the
heading  angles  of  the  vehicle  by  use  of  magnetic
compasses,  it  is  very  necessary  to  filter  the  Earth's
magnetic fields from the magnetometer measurements.

impressed  by

the

TAM  Calibration  should  be  performed  due  to  the
variation of the local magnetic effects with respect to the
location,  environment  and  operation  of  the  onboard
electronic  devices.  There  are  several  methodologies  for
magnetic  compass  calibration  divided  into  offline  or
online  calibration  and  attitude  independent  or  attitude
dependent  calibration  [3-5].  Gebre-Egziabher  et  al.  have
estimated  the  calibration  parameters  of  magnetometer,
including  bias  and  scale  factor  using  least  square
estimator  in  the  first  step  and  algebraic  estimation
algorithm in the second step. In this algorithm, there is no
need for using any external references and calibration has
been  done  based  on  the  magnetic  field  domain.  They
advanced a recursive least square estimation algorithm for
magnetic  calibration  [6].  Wang  and  Gao,  developed  a
nonlinear model for the relationship between the compass
heading  angle  and  the  true  heading  [7].  Using  neural
network  and  estimating  the  model  coefficients,  they
calibrated the magnetic compass. Kao and Tsai proposed
a  magnetic  compass  calibration  algorithm  based  on  the

the

the  device

to  increase

normalized value of GPS velocity vector [8]. Keighobadi
proposed  a  new  regression  model
the
convergence  probability  of
the  calibration  process.
Mamdani type fuzzy batch least-square (FBLS) algorithm
was  designed  to  estimate  the  calibration  bias  and  scale
factors  of  the  magnetometers  [9].  Two  techniques  have
been  proposed  in  [10]  for  fast  automatic  3D-space
magnetometer calibration requiring small space coverage.
Theproposed techniques perform 3D-space magnetometer
three  magnetometer
calibration  by  calibrating
the
in
readings
magnetometer  useful
in
untethered  devices,  especially  in  pedestrian  navigation
There  are  many  researches  concerned  with  ellipsoid
fitting  algorithms  in  magnetic  sensor calibration  [11-14].
Given the  fact that the error model of magnetic compass
is  an  ellipsoid,  Fang  et  al.  adopted  a  constraint  least
square  method  to  estimate  the  magnetic  calibration
parameters  [11].  Kanatani  et  al.  extended  a  hyper  least
square  estimator
for  ellipsoid  problem  of  TAM
calibration [12]. In another work, Lou et al. realized a fast
field  error  calibration  in  STM32  embedded  systems
Based on ellipsoid fitting algorithm [14].

frame,  which  makes
for  determining  heading

Using  online  methods,  in  spite  of  good  results,  have
some  drawbacks  to  be  performed.  For  example,  an
external  reference  signal  should  be  available  during  the
navigation.  In  the  case  of  using  GPS  as  the  reference
signal,  it  must  be  noticed  that  the  GPS  is  not  working
properly near high buildings and natural barriers. Also, it
can be interrupted by radio signals. Moreover, the online
calibrations  are  performed  with  a  higher
level  of
calculations  compared  to  offline  methods.  This  can  lead
to  divergence  in  the  estimation  process.  Taking  into
account  these  facts,  one  can  appreciate  the  necessity  of
periodic offline calibration algorithms. Offline calibration
process brings about more convergence in the estimation
algorithm.  This  is  because  of  the  persistently  exited
signals  produced  by
to
continuous  rotations  in  different  orientations.  In  the
offline methods, the external reference is required only in
the calibration process and after estimating the calibration
parameters,  they  will  be  used  in  real-time  mode  without
any  reference.  However,  the  estimated  parameters  in
offline methods are not global parameters.

the  magnetometers  during

Attitude

independent  algorithms  usually

include
model based methods which are so difficult to use. In the
practical applications, they frequently lead to converging
and signal excitation problems. It is because of having no
external reference and the only parameter reference is the

56

  Vol. 47 - No. 1 - Spring 2015



Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Magnetic Calibration Of Three-Axis Strapdown Magnetometers For
Applications In MEMS Attitude-Heading Reference Systems

magnetic  field  domain  which  is  not  working  properly  in
the  low-cost  sensors.  Attitude  dependent  methods  are
heading  domain  and  velocity  domain  algorithms.  The
main drawback of the attitude dependent algorithms is the
accuracy  of  attitude  angles  which  affect  the  calibration,
especially in airborne tests.

The  main  aim  of  the  paper  is  to  develop  an  efficient
algorithm  so  as  to  improve  the  accuracy  of  offline  and
attitude  dependent  calibration  algorithms  and  also  wipe
out  the  limitations  and  complication  of  online  methods.
Calibration  parameters  of  each  classical  method  do  not
seem  to  be  fixed  for  the  MEMS  sensors  and  vary  from
test  to  test  in  different  trajectories  and  maneuvers.  A
scheme is required to detect the dependency of calibration
parameters  upon  test  conditions.  To  acquire  this  aim,
clustering calibration of TAM is proposed in the paper.

2. STRAPDOWN MAGNETIC COMPASS SYSTEM

As  an  aiding-navigation  system,  magnetic  compass
comprises  three-axis  strapdown  magnetometer  which
detects the strength and direction of the Earth's magnetic
field.  Giving  the  horizontal  plane  components  of  the
Earth's magnetic field, the magnetic heading angle can be
determined.  In  the  navigation,  directions  are  usually
expressed  with  respect  to  geographical  or  true  north.
Depending on where the magnetic compass is located on
the surface of the Earth, the angle between true north and
magnetic north (i.e. magnetic declination angle) can vary
widely.  The  local  magnetic  declination  is  given  on  most
maps,  to  allow  the  map  to  be  oriented  with  a  compass
parallel  to  true  north.  Some  magnetic  compasses include
the  magnetic
means
declination, so that the compass shows true directions. In
the  integrated  AHRS/Magnetic  system,  TAM  sensors
must be mounted in aligns with the inertial sensors of the
IMU. Earth's magnetic field components are measured by
the TAM sensors.

to  manually  compensate

for

(1)

in  which,

,

  and

  are  the  components  of

magnetic  field  vector  in  the  body  frame  (b-frame).
Magnetometers'  outputs  can  be  transformed  from  the  b-
frame to navigation frame (n-frame) as follows:

(2)

where,

  is  the  magnetic  field  vector  in  n-frame  and

  is  the  Direction  Cosine  Matrix  (DCM)  from  the  b-

frame to n-frame defined with respect to the Euler angles
[15].

(3)

In

the  horizontal  plane,

the  magnetic  vector

components can be calculated as follows[16].

(4)

Figure  (1)  shows  the  magnetic  heading  angle  and
horizontal plane components of the magnetic field vector.

Determining

  and

  from  equation  (4),  the

magnetic  heading  angle  can  be  calculated  as  shown  in
Fig. 1.

(5)

Fig. 1.  Magnetic heading angle and horizontal plane components

of the magnetic field vector

Due  to  environmental  effects  and  external  magnetic
anomalies,  the  heading  angle  calculated  from  equations
(4)  and  (5)  is  not  accurate.  To  enhance  the  magnetic
heading accuracy, TAM must be appropriately calibrated.

3. CALIBRATION ALGORITHMS

  Calibration algorithms of the magnetometers can be
divided  into  heading  domain  algorithms,  magnetic  field
vector  algorithms  and  horizontal  plane's  magnetic  field
vector algorithms. In the heading domain algorithms, the
magnetic heading angle is calibrated in order to decrease
the  heading  error  of  the  magnetic  compass.  After

Vol. 47 - No. 1 - Spring 2015

  57

TbbbbxyzMMMMbxMbyMbzMnnbbMCMnMnbCnbCCCSSSCSSCSCCSCCSSSSSCSSSSCCCCcossinsincossin0cossinsinsincoscoscoshbxxhbyyhbzzMMMMMMhxMhyM1tanhymhxMM

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Hamed Milanchian, Jafar Keighobadi, and Hossein Nourmohammadi

calculating  the  heading  angle  from  the  magnetic  field
measured  by  TAM  sensors,  calibration  is  carried  out  on
the computed angle. Magnetic field vector and horizontal
plane's  magnetic  field  vector  algorithms  calibrate  each
output of the TAM, directly. Giving the calibrated values
of  TAM's  outputs,  the  corrected  heading  angle  is
computed.  Magnetic  field  vector  algorithms  are  usually
model-based  methods  and  cannot  be  an  efficient
calibration for low-cost MEMS sensors.

N  known  headings.  The  heading  error

  is  computed

for each known heading as follows:

(7)

where

  is  the  reference  value  of  the  heading  angle.

Eventually,  the  following  regression  model  can  be
constituted for all of the N measurements.

In  the  paper,  two  calibration  methods,  including
clustering swinging method and clustering velocity vector
method  are  presented.  Swinging  method  and  velocity
vector method are in the category of heading domain and
horizontal  plane's  magnetic  field  vector  algorithms,
respectively.  Batched  least-squares  (BLS)  algorithm  is
utilized  as  estimation  algorithm  in  both  calibration
methods. Least-squares estimation algorithms bring about
a  good  tracking  performance  because  of  their  linear
optimal features resulting from minimizing the sum of the
squared  prediction  errors  [17].  Taking  into  account  the
calculation  cost  offline  BLS  have  been  applied  in  the
calibration  process.  Online  calibrations  are  performed
with  a  higher  level  of  calculations  compared  to  offline
methods. Using any kind of online methods (model based
methods,  attitude  dependent  methods  and  etc.)  brings
about  high amount of calculation due to the fact that the
estimation  problem
the
navigation  algorithm.  Using  some  techniques  such  as
batch  least-squares  and  forgetting  factors,  the  level  of
calculation
is  decreased.
least-squares  algorithm
However,  trying  to  decrease  the  calculations  often  leads
to  divergence  in  the  estimation  process.  For  instance
small  batches  in  a  least  square  estimator  may  result  in  a
regressor  matrix  that  doesn’t  satisfy  a  high  order  of
persistent excitation.

is  required  persistently

in

in

A.  Swinging Method
In  the  swinging  method,  calibration  is  carried  out
based  on  the  perturbation  of  equation  (5),  the  basic
magnetic  heading  equation.  The  following  equation  is
defined as the heading error equation.

(6)

Equation  (6)  is  a  reduced-order  Fourier  series  in
which the coefficients A, B, C, D and E are functions of
the  hard  and  soft  iron  errors  [18].  The  procedure  for
is  so-called
the  Fourier  coefficients
estimation  of
“swinging”.  This  involves  leveling  and  rotating  the
vehicle  containing  the  magnetometer  through  a  series  of

(8)

Using BLS algorithm [19], the coefficients A through
E can be estimated from equation (8). Instead of leveling
and  rotating,  the  vehicle  can  be  traveled  through  a
specified  trajectory  called  calibration  track  as  shown  in
Fig. 2.

Fig. 2.  Calibration track with known heading angle

The  reference  heading  angle  would  be  available
throughout  the  calibration  track  by  use  of  an  aiding
navigation  system  such  as  GPS  or  accurate  INS.  Using
the reference heading angle, the calibration parameters in
equation  (6)  are  determined.  Finally,  the  corrected  value
of  magnetic  heading  angle  will  be  estimated  through  the
following equation.

(9)

B.  Velocity Vector Method
In  the  velocity  vector  method,  calibration  is  carried
out based on the horizontal plane magnetic field vector. A
reference  value  for  velocity  vector  is  required  in  this

58

  Vol. 47 - No. 1 - Spring 2015

ˆˆˆˆsin()cos()sin(2)cos(2)mmmmABCDEˆrefmref1111122222ˆˆˆˆ1sincossin2cos2ˆˆˆˆ1sincossin2cos2ˆˆˆˆ1sincossin2cos2NNNNNABCDEˆˆsin()cos()ˆˆˆsin(2)cos(2)mmmmmcABCDElatitudelongitudecalibration trajectory

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Magnetic Calibration Of Three-Axis Strapdown Magnetometers For
Applications In MEMS Attitude-Heading Reference Systems

algorithm. Giving the velocity component in the east and
north direction, the vehicle heading can be determined by
equation (10).

Assuming  small  declination  angle,  the  following
regression  model  can  be  derived  for  the  velocity  vector
method based on equations (12) – (14).

And  the  normalized  velocity  vector  can  be  found  as

(15)

(10)

follows:

(11)

In the case of using GPS velocity to get the reference
heading  angle,  some  considerations  must  be  adopted.  In
the GPS receivers, the velocity vector is measured based
on the Doppler frequency or pseudo-range rate [20]. GPS
track  angle  would  be  corrupted  by  the  measurement
noises  at  low  speed.  Therefore,  the  vehicle  should  be
moved at reasonable speed to acquire good calibration. In
addition,  signal  blockage  in  urban  environments  would
affect the heading accuracy.

Defining  bias  and  scale  factor,

the  horizontal
components of the magnetic field vector can be modeled
by equation (12).

Fig. 3.  TAM heading vector and normalized velocity vector

(12)

where,

  and

  are the horizontal components of

least

Using

square

the  calibration
parameters  can  be  found.  Horizontal  components  of  the
magnetic field unit vector can be found based on equation

algorithm

TAM's  outputs.

  and

  are  true  values  of  the

(13). Giving

 and

, magnetic heading angle can

magnetic  field.
respectively. Equation (12) can be rewritten as follows:

  are  bias  and  scale  factor,

  and

(13)

In  equation  (13)  unit  vector  components  of  the

horizontal magnetic field are specified by

 and

.

As  shown  in  Fig.  3,

  and

  are  expressed  with

respect to

 and

 by equation (14).

(14)

where,

 is the declination angle.

be  calculated  by  equation  (1).  Eventually,  the  calibrated
heading  angle  in  this  method  would  be  determined  by
adding  the  declination  angle  to  the  magnetic  heading
angle as follows:

(16)

C.  Clustering Calibration Methods
In  spite  of  the  good  accuracy  of  online  magnetic
calibration,  there  are  some  drawbacks  that  restrict  the
practical  application  of  online  TAM  calibration  in  the
magnetic  compass.  High  amount  of  calculation  and
necessity  of  reference  signal  availability  are  the  main
drawbacks of online calibration. On the other hand, using
offline  methods  did  not  require  much  calculation.
However,  it  has  lower  accuracy.  Bearing  in  mind  these
facts, one can appreciate the importance of advancing an
accurate  calibration  algorithm,  especially  for  navigation
purposes.

Vol. 47 - No. 1 - Spring 2015

  59

1tan()eastvnorthVV(,)(sin,cos)ENvvuuˆ()ˆ()hhhhxxxxhhhhyyyyMGMCMGMCˆhyMˆhyMhxMhyMhChGˆˆhhhhxxxxhhhhyyyymMkBmMkBhxmhymhxmhymNuEucos()sin()sin()cos()hEyhNxumumˆ001ˆ010hxhhyEyNhxhNhxEykkuMuBuMuBhxmhymmc

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Hamed Milanchian, Jafar Keighobadi, and Hossein Nourmohammadi

Calibration  parameters  of  each  classical  method  do
not seem to be fixed for the MEMS sensor and vary from
test  to  test  in  different  trajectories  and  maneuvers.  A
scheme  was  required  to  detect  the  dependency  of
calibration  parameters  upon  test  conditions.  To  acquire
this aim, clustering calibration of TAM is proposed in the
paper.

be  estimated.  The  efficiency  of  the  clustering  factors  in
the  calibration  accuracy  will  be  surveyed  in  the  next
section.

Every

test  has

its  own  conditions,  such  as
acceleration, angular rates and domain of headings. In the
clustering calibration method, the test data is divided into
several  classes,  and  each  class  is  named  a  cluster.  Test
classification  is  done  based  on  the  vehicle  maneuvering.
Calibration  parameters  of  swinging  method  and  vector
velocity  method  are  determined  for  each  cluster.  The
clustered  calibration  parameters  could  be  used  in  any
other  test  with  pre-obtained  conditions.  Updating  classic
swinging  method  and  classic  vector  velocity  with
clustering swinging method and clustering vector velocity
method  would  enhance  the  performance  and  accuracy of
offline  calibration  of  the  magnetic  compass.  Schematic
view  of  the  proposed  clustering  calibration  method  is
depicted  in  Fig.  4.  Maneuver  intensity  of  the  vehicle's
motion  throughout  the  calibration  track  can  be  specified
based  on  different  factors,  including  norm  of  the  rate

vector

, norm of the acceleration vector

, norm

of the magnetic field vector

, heading angle

,

y-component  of  the  acceleration  vector

  and  the

angular  velocity  about  the  z-axis

.  Rate  vector and

acceleration  vector  are  dynamical  properties  of  the
vehicle's  motion.  So,  they  can  be  a  good  factor  for  data
clustering. Magnetic field vector is chosen due to the fact
that  its  norm  is  ideally  constant  in  a  specific  area.
However,  because  of  magnetic  anomalies  and  other
effects,  it  is  not  so.  Hence,  Clustered  parameters  for

 is suggested. Heading angle
different magnitudes of
is  chosen,  because  calibration  parameters  may  vary

according  to  heading  angles.

  and

  are  the  main

factors  of  changing  the  heading  angles.  So,  they  can  be
efficient factors in the clustering process.

The procedure for clustering calibration method is in a

)  is
way  that,  one  of  the  mentioned  factors  (e.g.
analyzed  in  a  specified  calibration  test  trajectory  and
clusters  are  created  (3  to  5  clusters  are  suggested).  All
TAM data will be classified in these clusters. Calibration
process (swinging method or vector velocity method) will
be  carried  out  individually  in  each  cluster.  Finally,  the
calibration  parameters  corresponding to each cluster will

Fig. 4.  Schematic view of the proposed clustering calibration

method

4. EXPERIMENTAL RESULTS AND DISCUSSION

In  order  to  assess  the  performance  of  the  presented
TAM  calibration  algorithm,  several  experimental  tests
have been exerted on both ground and airborne vehicles.
The  algorithm  has  been  evaluated  in  two  in-ground  in-
flight tests.

A.   In-Ground Test
The in-ground test has been executed in the campus of
the  University  of  Tabriz.  Experimental  data  were logged

60

  Vol. 47 - No. 1 - Spring 2015

()b()ab()Mb()()bya()bzMbbyabzb

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Magnetic Calibration Of Three-Axis Strapdown Magnetometers For
Applications In MEMS Attitude-Heading Reference Systems

through  ANALOG  DEVICE  ADIS16407  IMU  sensors
comprised  of  accelerometers,  gyros  and  magnetometers.
In addition, a GARMIN GPS receiver and VITANS INS
have  been  used  during  the  test  in  order  to  provide  the
reference data. In the experiment, it must be noticed that,
the  magnetic  sensors  should  not  be  so  close  to  ferrous
metals.  Taking  into  account  this  fact,  the  IMU  which
contains the magnetometers was mounted on an aluminum
profile far away the vehicle's body as shown in Fig. 5.

Vehicle's  motion  throughout  the  test  trajectory  is
divided  into  two  parts:  calibration  track  and  evaluation
track. In the course of calibration track, the reference data
is  available.  Calibration  process  is  executed  for  this  part
of the test trajectory. After finishing the calibration track,
the  results  are  evaluated  over  the  evaluation  track.  This
track  is  just  for  assessing  the  accuracy  of  the  proposed
offline  calibration  algorithm.  The  calibration  track  lasts
200  seconds  and  evaluation  duration  is  300  seconds.  To
analyze  to  the  calibration  accuracy,  heading  error  is
defined as follows:

(17)

where,

  is  the  calibrated  magnetic  heading  angle  and

  is  the  reference  value  of  the  heading  angle.  The

heading  error  will  be  calculated  in  both  calibration  and
evaluating  track.  In  the  perfect  mode,  the  heading  error
converges  to  zero.  So  the  mean  and  RMS  values  of
heading error signal should be zero for a good calibration
process. However, because of system noises and magnetic
disturbances, this is not fully reachable.

The calibration and evaluation tracks in the in-ground
test are depicted in Fig. 6. The results are shown in Tab. 1
and  Tab.  2.  The  mean and RMS values of heading error
would  be  calculated  in  all  tracks.  However,  in  order  to
assess  the  proposed  algorithm,  the  evaluation  track  is
more important compared to calibration track.

Table  (1)  shows  the  performance  of  the  swinging
calibration method. Without applying calibration process,
6.26 deg of mean value and 19.96 deg of RMS value are
obtained for heading error in the calibration track. Using
classic swinging method, these values are reduced to zero
mean  and  4.84  deg  RMS.  In  the  evaluation  track,  the
heading  error  reaches  the  mean  value  of  -1.4  deg  and
RMS  value  of  7.14  deg.  Therefore,  the  calibration
parameters  estimated  in  the  calibration  track  result  in  a
good  performance  in  the  evaluation  track.  Among  the

clustering  factors,

  clustering  has  the  best  accuracy.

 Clustering method not only reduces the RMS value to

4.34  deg  in  the  calibration  track,  but  also  has  a  mean
value  of  -1.33  deg  and  RMS  value  of  6.36  deg  in  the
evaluation track.

(b)

IMU

INS

Fig. 5.  (a) IMU-ADIS16407, (b) Experiment devices placed on the

vehicle

GPS

(a)

Fig. 6.  In-ground test, (a) Calibration track, (b) Evaluation track

Vol. 47 - No. 1 - Spring 2015

  61

crefcrefbzbz38.05238.05338.05438.05538.05638.05738.05846.32646.32846.3346.33246.33446.33646.33846.34latitudelongitude  calibration track38.05238.05338.05438.05538.05638.05738.05846.32646.32846.3346.33246.33446.33646.33846.34latitudelongitude  calibration trackevaluation track

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Hamed Milanchian, Jafar Keighobadi, and Hossein Nourmohammadi

TABLE 1.  THE RESULTS OF THE SWINGING CALIBRATION
ALGORITHM IN THE IN-GROUND TEST

Calibration

Evaluation

Without
calibration
Classic
calibration

:
n
o

d
e
s
a
b

g
n
i
r
e
t
s
u
l
C

Mean
(deg)

RMS
(deg)

Mean
(deg)

RMS
(deg)

6.26

19.96

14.84

21.87

0

0

0

0

0

0

0

4.84

-1.40

7.14

4.40

4.75

4.83

4.48

4.60

-2.94

-1.56

-1.41

-2.00

-1.57

4.34

-1.33

8.53

7.32

7.15

7.76

7.04

6.36

Similar  results  have  been  obtained  for  the  velocity
vector  method  as  shown  in  Tab.  2.  The  classic  velocity
vector algorithm has a mean value of 0.04 deg and RMS
value  of  5.03  deg  in  the  calibration  track.  In  the
evaluation track, these values are -0.81 deg and 6.89 deg,

respectively.  Like  swinging  method,

  clustering

method  has  the  best  results  in  both  calibration  and
evaluation tracks.

TABLE 2. . THE RESULTS OF THE VELOCITY VECTOR
CALIBRATION ALGORITHM IN THE IN-GROUND TEST

Calibration

Evaluation

Without
calibration

Classic
calibration

:
n
o
d
e
s
a
b
g
n
i
r
e
t
s
u
l
C

Mean
(deg)
6.26

RMS
(deg)
19.96

Mean
(deg)
14.84

RMS
(deg)
21.87

0.04

5.03

-0.81

6.89

0.10

0.05

0.04

0.03

0.05

0.06

4.40

4.99

5.02

4.53

4.88

4.73

-1.49

-0.99

-0.81

-1.34

-1.06

-0.81

8.04

7.04

6.90

7.18

6.69

6.14

Due  to  heading  domain  calibration  in  the  swinging
algorithms, zero mean heading errors are achieved in the
calibration track. But, the mean values are not so close to
zero  in  the  evaluation  track.  In  velocity  vector  method,

the  calibration  process  is  executed  on  the  horizontal
components  of  the  magnetic  field  vector.  So,  the  mean
values of heading error in calibration track are not exactly
zero  like  swinging  method.  However,  velocity  vector
method  has  a  better  performance  compared  to  swinging
method  as  velocity  vector  method  nearly  repeats  those
mean  values  in  evaluation  track.  It  must  be  noticed  that,
the  calibration  track  plays  a  key  role  in  the  offline
calibration.  The  vehicle's  maneuver  in  the  calibration
track must be rich enough to results in a good accuracy of
the calibration parameters.

B.   In-Flight Test
In  order  to  make  a  certain  decision  about  the
performance  of  the  proposed  calibration  method,  the
algorithms  are  also  evaluated  in  the  airborne  test.  The
calibration  and  evaluation  tracks  in  the  in-flight  test  are
depicted  in  Fig.  7.  The  MEMS magnetometers that have
been  used  in  the  airborne  test  are  not  the  same  as  the
sensors used in the car test.

After  calibrating  the  magnetic  system,  the  estimated
to  both
calibration  parameters  have  been  applied
calibration  and  evaluation  tracks  and  the  results  are
shown in Tab. 3 and Tab. 4. The main difference between
car  and  airborne  tests  is  the  maneuver's  characteristics.
The variation of tilt angles of the vehicle will be higher in
the  car  test.  Therefore,  the  accuracy  of  roll  and  pitch
angles  for  transforming  the  magnetometers'  outputs  from
the body frame to the horizontal plane (see equation (4))
is more important to get a better calibration process.

Without  applying  any  calibration  algorithms,  the
heading errors in the airborne test are lower compared to
those  of  the  car  test.  This  is  due  to  different  magnetic
sensors  used  in  the  airborne  test.  Both standard methods
of swinging and velocity vector algorithms have  heading
errors  so  close  to  non-calibrated  heading  error  signal.
Classic  swinging  and  velocity  vector  calibrations  results
in 11.56 deg RMS value and 10.88 deg RMS value in the
evaluation track which are so close to 11.57 degree.

Among  the  clustering  methods,  clustering  based  on

the

  leads  to  the  best  performance.  Clustering

swinging  method  based  on

  has  zero  mean  and  6.16

deg RMS

62

  Vol. 47 - No. 1 - Spring 2015

ˆmbabMbbyabzbzˆmbabMbbyabzbzbz

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Magnetic Calibration Of Three-Axis Strapdown Magnetometers For
Applications In MEMS Attitude-Heading Reference Systems

analog  and  raw  data  of  magnetometers,  they  cannot  be
detected  directly.  Therefore,
impact  of  such
phenomena  on  the  data  obtained  from  ADC  converter
along  with  the  other  noises  and  anomalies  has  been
identified and compensated as calibration parameters.

the

5. CONCLUSION

In  the  low-cost  AHRS,  it  is  very  difficult  to estimate
the  heading  angle  with  an  acceptable  precision.  This  is
because  of  using  low-precision  MEMS  inertial  sensors
(i.e.  gyros  and  accelerometers),  modeling  and  parameter
uncertainties  as  well  as  the  filter  algorithm  complexity.
To  overcome  this  drawback,  integrated  AHRS/Magnetic
system  is  proposed.  Using  magnetic  compass  as  an
aiding-navigation  system,  the  accuracy  of  heading  angle
estimated in the low-cost AHRS will be enhanced. On the
other  hand,  the  magnetic  compass  is  impressed  by
magnetic  anomalies  and  induced  magnetic  fields  as
external  disturbances.  Therefore,  magnetic  compass
calibration is very essential to achieve a good accuracy in
the  heading  angle.  In  this  paper,  a  novel  method  for
offline  calibration  of  the  MEMS  magnetic  compass
system  was  proposed.  Based  on  swinging  method  and
velocity vector method, two different methodologies have
been  developed  in  the  paper.  In  order  to  enhance  the
accuracy  of  offline  magnetic  calibration,  the  classic
swinging and velocity vector algorithms were extended to
clustering  ones.  Several  clustering  factors,  including rate
vector, acceleration vector, magnetic field vector, heading
angle,  y-components  of  the  acceleration  and  angular
velocity  about  the  z-axis  have  been  presented.  The
efficiency  of  each  factor  on  the  calibration  accuracy  has
been  surveyed.  According  to  experimental  results,  it  can

be concluded that the clustering based on

 leads to the

best  performance  in  both  swinging  and  velocity  vector
methods.

TABLE 3. THE RESULTS OF THE SWINGING CALIBRATION
ALGORITHM IN THE IN-FLIGHT TEST

Calibration

Evaluation

Without
calibration
Classic
calibration

:
n
o

d
e
s
a
b

g
n
i
r
e
t
s
u
l
C

Mean
(deg)
-2.60

RMS
(deg)
14.04

Mean
(deg)
-1.97

RMS
(deg)
11.57

0

0

0

0

0

0

0

10.32

3.70

11.56

9.43

10.01

9.97

8.04

9.93

7.81

3.08

2.84

5.23

3.46

15.98

10.47

10.65

13.93

11.65

6.16

1.11

7.86

TABLE 4.  THE RESULTS OF THE VELOCITY VECTOR
CALIBRATION ALGORITHM IN THE IN-FLIGHT TEST

Calibration

Evaluation

Without
calibration

Classic
calibration

:
n
o

d
e
s
a
b

g
n
i
r
e
t
s
u
l
C

Mean
(deg)
-2.60

RMS
(deg)
14.04

Mean
(deg)
-1.97

RMS
(deg)
11.57

-0.80

13.31

-1.95

10.88

0.06

-0.78

-0.74

0.32

-0.75

9.34

12.91

12.93

9.28

12.97

7.16

-0.67

-2.22

-0.85

-1.97

15.78

11.51

10.71

12.73

10.91

-0.12

7.94

-1.49

7.71

Value  in  the  calibration  track  and  1.11  deg  mean
value  and  7.86  deg  RMS  value  in  evaluation  track.
Applying clustering velocity vector, mean values reach to
-0.12 deg and -1.49 deg in the calibration and evaluation
tracks and the RMS values are 7.94 deg and 7.71 deg.

Considering  experimental  results  of  both  in-ground

and  in-flight  tests,  it  can  be  concluded  that  like

clustering  method  has  the  best  accuracy  in  the  different
maneuvers and different magnetic sensors.

The  effects  of  some  nonlinear  phenomena  such  as
hysteresis and saturation have been entered in the form of
bias  and  scale  factor.  However,  due  to  inaccessibility  of

Vol. 47 - No. 1 - Spring 2015

  63

ˆmbabMbbyabzˆmbabMbbyabzbzbz

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Hamed Milanchian, Jafar Keighobadi, and Hossein Nourmohammadi

(a)

(b)

Fig. 7.  In-flight test, (a) Calibration track, (b) Evaluation track

REFERENCES

[1]

[2]

[3]

 Alandry,  B.,  et  al.,  “A  fully  integrated  inertial
measurement  unit:  application  to  attitude  and
heading  determination,”  Sensors  Journal,  IEEE,
vol. 11, no. 11, pp. 2852-2860, 2011.

Storms, W., J. Shockley, and J. Raquet, “Magnetic
field  navigation
indoor  environment,”
Ubiquitous  Positioning  Indoor  Navigation  and
Location Based Service (UPINLBS), 2010: IEEE,
2010.

in  an

Crassidis,  J.L.,  K.-L.  Lai,  and  R.R.  Harman,
“Real-time
three-axis
attitude-independent
magnetometer  calibration,”  Journal  of  Guidance,
Control, and Dynamics, vol. 28, no.1, pp. 115-120,
2005.

[4]  Han, S. and J. Wang, “A novel method to integrate
IMU  and  magnetometers  in  attitude  and  heading
reference systems,” Journal of Navigation, vol. 64,
no. 04, pp. 727-738, 2011.

[5]  Wahdan, A., et al., “Magnetometer calibration for
portable navigation devices in vehicles using a fast
and
Intelligent
Transportation  Systems,  IEEE  Transactions  on,
vol. 15, no. 5, pp. 2347-2352, 2014.

autonomous

technique,”

[6]  Gebre-Egziabher,  D.,  et  al.,  “Calibration  of
strapdown  magnetometers
field
domain,”  Journal  of  Aerospace  Engineering,  vol.
19, no. 2, pp. 87-102, 2006.

in  magnetic

[7]  Wang,  J.-H.  and  Y.  Gao,  “A  new  magnetic
compass  calibration  algorithm  using  neural
networks,” Measurement Science and Technology,
vol. 17, no. 1, pp. 153, 2006.

[8]  Kao,  W.-W.  And  C.-L.  Tsai,  “Adaptive  and
learning  calibration  of  magnetic  compass,”
Measurement  Science  and  Technology,  vol.  17,
no. 11, pp. 3073, 2006.

[9]  Keighobadi,  J.,  “Fuzzy  calibration  of  a  magnetic
compass  for  vehicular  applications,”  Mechanical
Systems and Signal Processing, vol. 25, no. 6, pp.
1973-1987, 2011.

[10]  Wahdan, A., J. Georgy, and A. Noureldin, “Three-
Dimensional Magnetometer Calibration with Small
Space Coverage for Pedestrians,” Sensors Journal,
IEEE, vol. 15, no.1, pp. 598-609, 2015.

[11]  Li,  X.  and  Z.  Li,  “A  new  calibration  method  for
tri-axial  field  sensors  in  strap-down  navigation
systems,”  Measurement  Science  and  technology,
vol. 23, no. 10, pp. 105105, 2012.

[12]  Kanatani,  K.  and  P.  Rangarajan,  “Hyper  least
ellipses,”
squares
of
Computational Statistics & Data Analysis, vol. 55,
no. 6, pp. 2197-2208, 2011.

circles

fitting

and

[13]  Feng,  W.,  et  al.,  “A  calibration  method  of  three-
axis magnetic sensor based on ellipsoid fitting,” J.
Inf. Comput. Sci, vol. 10, pp. 1551-1558, 2013.

[14]  Lou,  X.,  L.  Zhou,  and  Y.  Jia,  “Realization  of
for  Three-Axis
Ellipsoid  Fitting  Calibration
Magnetic  Sensor  Based  on  STM32  Embedded
System,
in  Human  Centered  Computing,”
Springer, pp. 717-726, 2015.

[15]  Titterton, D. and J.L. Weston, “Strapdown inertial
navigation technology,” vol. 17: IET, 2004.

[16]  Li,  W.  and  J.  Wang,  “Effective  adaptive  Kalman
filter  for  MEMS-IMU/magnetometers  integrated
attitude and heading reference systems,” Journal of
Navigation, vol. 66, no. 01, pp. 99-113, 2013.

[17]  Li,  W.  and  J.  Wang,  “Effective  adaptive  Kalman
filter  for  MEMS-IMU/magnetometers  integrated
attitude and heading reference systems,” Journal of
Navigation, vol. 66, no. 01, pp. 99-113, 2013.

64

  Vol. 47 - No. 1 - Spring 2015

34.7334.7434.7534.7634.7734.7850.8950.950.9150.9250.9350.9450.95latitudelongitude  calibration track34.7334.7434.7534.7634.7734.7850.8950.950.9150.9250.9350.9450.95latitudelongitude  calibration trackevaluation track

Amirkabir International  Journal of Science & Research
(Modeling, Identification, Simulation & Control)
(AIJ-MISC)

Magnetic Calibration Of Three-Axis Strapdown Magnetometers For
Applications In MEMS Attitude-Heading Reference Systems

[18]  Guo,  P.,  et  al.  “The  soft  iron  and  hard  iron
calibration  method  using  extended  kalman  filter
for  attitude  and  heading  reference  system,”
Position,  Location  and  Navigation  Symposium,
IEEE/ION. 2008: IEEE, 2008.

[19]  Simon,  D.,  Optimal  state  estimation:  Kalman,  H
infinity,  and  nonlinear  approaches,  John  Wiley  &
Sons, 2006.

[20]  Bevly,  D.M.,  et  al.,  “The  use  of  GPS  based
velocity  measurements  for  improved  vehicle  state
estimation,”  American  Control  Conference,.
Proceedings of the 2000. 2000: IEEE, 2000.

Vol. 47 - No. 1 - Spring 2015

  65
