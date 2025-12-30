Skubel et al. Anim Biotelemetry            (2020) 8:34
<https://doi.org/10.1186/s40317-020-00220-0>

Animal Biotelemetry

METHODOLOGY

Open Access

A scalable, satellite-transmitted data product
for monitoring high-activity events in mobile
aquatic animals
Rachel A. Skubel1*
Daniel Benetti6 and Neil Hammerschlag1,6

, Kenady Wilson2, Yannis P. Papastamatiou3, Hannah J. Verkamp4, James A. Sulikowski5,

Abstract
A growing number of studies are using accelerometers to examine activity level patterns in aquatic animals. However,
given the amount of data generated from accelerometers, most of these studies use loggers that archive acceleration
data, thus requiring physical recovery of the loggers or acoustic transmission from within a receiver array to obtain
the data. These limitations have restricted the duration of tracking (ranging from hours to days) and/or type of species
studied (e.g., relatively sessile species or those returning to predictable areas). To address these logistical challenges,
we present and test a satellite-transmitted metric for the remote monitoring of changes in activity, measured via a
pop-off satellite archival tag (PSAT) with an integrated accelerometer. Along with depth, temperature, and irradiance
for geolocation, the PSAT transmits activity data as a time-series (ATS) with a user-programmable resolution. ATS is
a count of high-activity events, relative to overall activity/mobility during a summary period. An algorithm is used
to identify the high-activity events from accelerometer data and reports the data as a count per time-series interval.
Summary statistics describing the data used to identify high-activity events accompany the activity time-series. In this
study, we first tested the ATS activity metric through simulating PSAT output from accelerometer data logger archives,
comparing ATS to vectorial dynamic body acceleration. Next, we deployed PSATs with ATS under captive conditions
with cobia (Rachycentron canadum). Lastly, we deployed seven pop-off satellite archival tags (PSATs) able to collect
and transmit ATS in the wild on adult sandbar sharks (Carcharhinus plumbeus). In the captive trials, we identified both
resting and non-resting behavior for species and used logistic regression to compare ATS values with observed activ-
ity levels. In captive cobia, ATS was a significant predictor of observed activity levels. For 30-day wild deployments on
sandbar sharks, satellites received 57.4–73.2% of the transmitted activity data. Of these ATS datapoints, between 21.9
and 41.2% of records had a concurrent set of temperature, depth, and light measurements. These results suggest that
ATS is a practical metric for remotely monitoring and transmitting relative high-activity data in large-bodied aquatic
species with variable activity levels, under changing environmental conditions, and across broad spatiotemporal
scales.

Keywords:  Biotelemetry, Biologging, Accelerometers, Activity, Sharks, Behavior, Activity levels, Satellite tags

*Correspondence:  <ras347@miami.edu>
1 Abess Center for Ecosystem Science and Policy, University of Miami,
Coral Gables, FL, USA
Full list of author information is available at the end of the article

Background
Interpretation  of  animal  movement  patterns  has  been  a
central  focus  of  ecological  studies  and  is  a  critical  com-
ponent of modern conservation research [1, 2]. Given the
challenges of directly observing the movements and asso-
ciated behaviors of marine and freshwater animals under
natural conditions, researchers have used biologging and

© The Author(s) 2020. This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing,
adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and
the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material
in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material
is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the
permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit <http://creat> iveco
mmons .org/licen ses/by/4.0/. The Creative Commons Public Domain Dedication waiver (<http://creat> iveco mmons .org/publi cdoma in/
zero/1.0/) applies to the data made available in this article, unless otherwise stated in a credit line to the data.

Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 2 of 14

biotelemetry  tools  to  monitor  activity  remotely.  These
methods provide a glimpse into the animals’ behavior in
wild  environments,  without  the  burden  of  human  pres-
ence for observation [3].

Researchers  have  been  increasingly  integrating  mul-
tiple  sensors  into  tracking  tools  to  provide  additional
information  on  how  aquatic  animals  interact  with  their
environments.  Common  combinations  include  tri-axial
acceleration,  temperature,  and  pressure  (depth)  sensors
(e.g.,  [4,  5]).  Similar  combinations  have  been  used  to
study  where  and  when  certain  behaviors  occur,  such  as
mating  or  feeding  [6–8];  to  investigate  biological  driv-
ers of movement patterns, such as circadian rhythms or
behavioral  thermoregulation  [9,  10];  to  identify  impacts
of  human  activity,  such  as  post-release  fishing  mortal-
ity  [11,  12]  or  provisioning  for  dive  tourism  [13];  and
to  measure  field  metabolic  rates,  infer  thermal  perfor-
mance, and measure activity levels and their responses to
environmental settings [14, 15].

In  activity  studies,  accelerometers  sample  multiple
axes  at  high  frequencies,  often  measuring  and  logging
at > 15 Hz, and up to 500 Hz [16–18]. The total amount of
raw data recorded is therefore too large for transmission
via satellite; as a result, researchers physically recover log-
ging devices to obtain their raw data, or logging devices
transmit their data from within an acoustic receiver array
[18–20].  Tag  recovery  is  logistically  difficult  for  wide-
ranging aquatic animals, such as elasmobranchs and large
teleost fishes that do not return to locations where their
recapture is predictable [21]. To maximize the probability
of retrieving the loggers or having the data transmitted to
an array, accelerometer applications are limited by track-
ing duration (e.g., from hours to days) and/or by the spe-
cies  studied  (e.g.,  less  mobile  species  or  those  returning
to predictable areas) [19–23].

Study aims
Understanding  how  highly  mobile  or  open-ocean  ani-
mals respond to environmental variability, over multiple
months, can give researchers evidence of animals’, popu-
lations’, or species’ spatial and environmental preferences
[24, 25]. Garnering such evidence can contribute to con-
servation  planning  and  management,  such  as  assessing
climate  change  vulnerability  or  species  use  in  protected
and  unprotected  areas  [25–27].  Following  previous
studies [28, 29] (Table 1), we aim to address this area of
research by pairing a compressed metric of activity with
environmental  data  (depth  and  temperature)  and  loca-
tion  data  (geolocation).  Specifically,  we  present  a  novel,
satellite-transmittable,  acceleration-derived  metric  of
high-activity  based  on  measurements  obtained  from
pop-off satellite archival tags (PSAT). PSATs transmit this
metric as an ‘activity time-series’ (ATS), which represents

a  count  of  high-activity  events  per  a  time-series  inter-
val,  where  an  algorithm  identifies  high-activity  events
from  accelerometer  data.  ATS  is  paired  with  an  hourly
measure of mobility (along x, y, and z-axes), and existing
time-series data products for depth and temperature. The
ATS-enabled PSAT can overcome the limited bandwidth
of satellite transmission via Argos by processing the raw
accelerometer  data  onboard  the  tag  and  only  transmit-
ting  the  ATS  time-series  with  concurrent  summary  sta-
tistics of the raw data. Accordingly, this study had three
primary  objectives:  (1)  test  the  ATS  data  product  under
captive conditions to verify that it is a reasonable metric
of  high  activity;  (2)  conduct  wild  deployments  of  ATS-
PSATs to test their utility for measuring and transmitting
ATS time-series data with corresponding mobility, depth,
temperature, and light levels in highly migratory species;
and  (3)  demonstrate  the  utility  of  the  data  obtained  by
comparing the ATS data product against other traditional
accelerometer-derived measures of activity level (specifi-
cally, vectorial dynamic body acceleration, VeDBA).

Methods
PSAT tags

PSATs  are  positively  buoyant  devices  that  continuously
log  sensor  data  for  a  predetermined  length  of  time. The
tag  then  releases  from  the  animal  and  floats  at  the  sur-
face where it transmits data to a receiving satellite in the
Argos  satellite  network  [30,  31].  These  data  commonly
include  temperature,  depth,  and  light  levels,  which  are
used to approximate tag location during the deployment
[32].  These  concurrent  time-series  of  environmental
conditions  contextualize  the  geospatial  location  of  indi-
vidual  animals.  There  are  two  major  drawbacks  to  data
transmission  via  the  Argos  network:  message  size  and
satellite  availability  [33].  Data  messages  are  limited  in
size  and  must  be  transmitted  at  a  very  small  bandwidth
(~ 32  bytes/message);  this  means  that  a  researcher  will
need  more  messages  to  transmit  more  data.  The  Argos
system  comprises  a  network  of  polar-orbiting  satellites;
the  availability  of  these  satellites  can  vary  both  spatially
and  temporally.  PSATs  send  messages  to  the  satellites
without  acknowledgment  of  receipt,  and  corruption  of
messages is possible. To increase the likelihood that sat-
ellites  receive  the  message  correctly,  manufacturers  rec-
ommend sending each message multiple times. However,
if  attempting  to  transmit  an  extensive  amount  of  data
(e.g.,  three  concurrent  time-series),  due  to  the  above-
mentioned  issues,  there  may  be  some  gaps  in  the  data.
To address this limitation, researchers can compress the
data’s dimensions, either by combining several data into
one metric [34] or by recording events based on a prede-
termined  algorithm  which  incorporates  several  streams
of data [17, 28, 29], and/or compress the data temporally,

Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 3 of 14

]
3
4

,

8
2
[

]
4
4

,

9
2
[

]
4
4

,

9
2
[

f
e
R

l

t
n
a
h
p
e
e
n
r
e
h
t
u
o
s
d
n
a
1
4

-

l
e
d
d
e
w
s
e
t
o
h
c
y
n
o
t
p
e
L
(

l
l

e
d
e
W

1
3

i

)
e
n
n
o
e

l

a
g
n
u
o
r
i

M

(

s
l
a
e
s

l

s
u
s
s
o
g
o
p
p
H

i

(

t
u
b

i
l

a
h
c
fi
c
a
P

i

l

)
s
i
p
e
o
n
e
t
s

l

s
u
s
s
o
g
o
p
p
H

i

(

t
u
b

i
l

a
h
c
fi
c
a
P

i

l

)
s
i
p
e
o
n
e
t
s

s
y
a
d
8
3
3
o
t
p
u
r
o

f

z
H
-

1
f

o
y
r
a
m
m
u
s
h
-

2

s
y
a
d
0
6
/
a
t
a
d

z
H
-

1
f

o
y
r
a
m
m
u
s
h
-

2

s
y
a
d
0
6
/
a
t
a
d

]
y
d
u
t
s

s
i
h
T
[

i

s
u
n
h
r
a
h
c
r
a
C

(

s
k
r
a
h
s

r
a
b
d
n
a
S

z
H
-

1
f

o
s
e
i
r
a
m
m
u
s
h
-

1
d
n
a
s
-

5
7

)
s
u
e
b
m
u
p

l

s
y
a
d
0
3
/
a
t
a
d

]
4
3
[

s
u
r
o
h
p
o
i
t
s
I
(

h
s
fi

l
i

a
s
c
fi
c
a
P

i

z
H
-

5
2
6
5
1
f

.

o
s
e
i
r
a
m
m
u
s
n
m
-

3

i

)
s
u
r
e
t
p
y
t
a
p

l

a
t
a
d

T
A
S
P

T
A
S
P

,

d
e
s
u

t
n
e
m
p
u
q
e

i

,
r
o
i
v
a
h
e
b

r
o

y
t
i
v
i
t
c
a

d
e
t
e
g
r
a
t

e
h
t

i

g
n
d
u
l
c
n

i

,
s
l
a
m
n
a

i

e
n
i
r
a
m

r
o
f

r
u
o
i
v
a
h
e
b

r
o
/
d
n
a

y
t
i
v
i
t
c
a

f
o

s
c
i
r
t
e
m

d
e
v
i
r
e
d
-

r
e
t
e
m
o
r
e
l
e
c
c
A

1
e
l
b
a
T

c
i
r
t
e
m
e
h
t
g
n
i
s
u
s
e
i
d
u
t
s
r
o
y
d
u
t
s
e
l
p
m
a
x
e
d
n
a

s
e
i
c
e
p
S

n
a
p
s
e
m

i
t
/
y
c
n
e
u
q
e
r
F

t
n
e
m
p
u
q
E

i

y
t
i
v
i
t
c
a
t
e
g
r
a
T

n
o
i
t
a
c
fi
i
t
n
e
d

I

c
i
r
t
e
M

)

d
e
d
e
e
n

l

a
v
e
i
r
t
e
r
e
c
v
e
d
o
n

i

(

n
o
i
s
s
i

m
s
n
a
r
t
a
t
a
d
e
r
o
f
e
b
d
e
t
a
u
c
a
C

l

l

)
i
i
l

.

z
H
6
1
t
a
h
5
2
2
y
r
e
v
e
d
e
z
i
r
a
m

-

e
v
o
m
y
d
o
b
d
n
a
d
a
e
h
d
p
a
r

i

i

g
n
n
n
u
r
(
a
n
a
h
t

r
e
t
a
e
r
g
n
o
i
t

-

l

m
u
s
d
n
a
d
e
p
m
a
s
e
v
d
e
n
O

i

g
a
t
e
t
i
l
l

e
t
a
s
y
a
e
R

l

i

a
v
s
t
p
m
e
t
t
a
g
n
g
a
r
o
f
-

e
v
D

i

i

l

-

a
r
e
e
c
c
a
n

i

e
g
n
a
h
c
d
n
o
c
e
s
-

r
e
P

)
t
p
m
e
t
t
a
h
c
t
a
c
y
e
r
p

(

A
C
r
P

s
t
n
e
m

l

e
u
a
v
)

l

d
o
h
s
e
r
h
t

e
g
a
r
e
v
a

+

T
A
S
P

i

,
t
u
o
b
g
n
m
m
w
s
a
f

i

i

o
g
n
n
n
g
e
B

i

m
o
r
f
T
A
S
P
f

o
h
c
t
i

w
s

t
p
u
r
b
A

)
t
n
e
v
e
n
w
o
d
k
c
o
n
k
(

D
K

y
t
i
l

a
t
r
o
m

l

a
t
n
o
z
i
r
o
h
o
t

l

a
c
i
t
r
e
v

T
A
S
P

i

d
e
n
a
t
s
u
s
(

i

r
o
v
a
h
e
b
g
n
m
m
w
S

i

i

l

a
c
i
t
r
e
v
m
o
r
f

,
t
l
i
t
T
A
S
P
f

o
e
e
r
g
e
D

)

g

(

t
l
i

T

y
t
i
l

a
t
r
o
m

,
)
y
r
o
t
a
t
l
a
s

r
o

s
i
x
a
-

z
a
v

i

l

a
t
n
o
z
i
r
o
h
o
t

y
t
i
v
i
t
c
a
h
g
h
e
v
i
t
a
e
R

l

i

-

l
i

b
o
m

f

o
s
e
c
n
a
t
s
n

i

d
n
o
c
e
s
-

r
e
P

)
s
e
i
r
e
s
-

e
m

i
t
y
t
i
v
i
t
c
a
(
S
T
A

i

i

h
g
h
c
m
a
n
y
d
a
g
n
d
e
e
c
x
e
y
t
i

i

l

d
o
h
s
e
r
h
t
y
t
i
v
i
t
c
a

y
t
i
v
i
t
c
a

l

a
n
r
u
D

i

,

l

l

x
g
n
o
a
n
o
i
t
a
r
e
e
c
c
a
d
e
z
i
r
o
t
c
e
V

G

s
e
x
a
-

z
d
n
a

,

y

l

i

a
v
e
i
r
t
e
r
e
c
v
e
d
e
r
o
f
e
b
d
e
t
a
u
c
a
C

l

l

]
5
4
[

j

)
r
o
a
m

s
u
r
g
a
P
(

m
a
e
r
b
a
e
s
d
e
R

l

a
o
i
r
e
S
(

h
s
fi
g
n
k

i

l
i

a
t
w
o

l
l

e
y
d
n
a

)
i
d
n
a
a

l

l

h
5
4
–
8
1
/
z
H
0
0
5

r
e
g
g
o

l

r
e
t
e
m
o
r
e
e
c
c
A

l

i

s
r
o
v
a
h
e
b
e
p
a
c
s
E

d
e
n
fi
e
d
y

l
l

a
u
n
a
m

s
d
e
e
c
x
E

s
t
n
e
v
e
n
o
i
t
a
r
e
e
c
c
a
t
s
r
u
B

l

l

d
o
h
s
e
r
h
t
n
o
i
t
a
r
e
e
c
c
a

l

]
9
1
[

]
6
4
[

)
a
n

i
l

u
t
i
v
a
c
o
h
P
(

l

a
e
s

r
o
b
r
a
H

A
N
n
a
p
s
e
m

i
t
/
z
H
3
3
3
d
n
a
0
0
2

r
e
g
g
o

l

r
e
t
e
m
o
r
e
e
c
c
A

l

)

n
o
i
t
c
u
s
d
n
a

l

a
i
r
o
t
p
a
r
(

i

g
n
d
e
e
F

l

-

a
r
e
e
c
c
a
f

o

l

a
i
t
n
e
r
e
ff
D

i

s
/

m
0
0
0
1
>
n
o
i
t

t
n
e
m

f
l

u
g
n
e
y
e
r
P

l

i

a
v
e
i
r
t
e
r
e
c
v
e
d
r
e
t
f
a
d
e
t
a
u
c
a
C

l

l

A
N

y
c
n
e
u
q
e
r
f

i

h
g
h
-

o
t
-

e
t
a
r
e
d
o
M

r
e
g
g
o

l

r
e
t
e
m
o
r
e
e
c
c
A

l

-

l
e
c
c
a
s
a
(
e
r
u
t
i
d
n
e
p
x
e
y
g
r
e
n
E

,

l

x
g
n
o
a
n
o
i
t
a
r
e
e
c
c
a
e
t
u
o
s
b
A

l

l

(

i

c
m
a
n
y
d

l
l

a
r
e
v
o

(

A
B
D
O

)
z
H
0
1
>

(

f

o
r
e
t
n
e
c
a
d
n
u
o
r
a
n
o
i
t
a
r
e

-

l
e
c
c
a
c
i
t
a
t
s
(
–
)
s
e
x
a
-

z
d
n
a

,

y

)
s
s
a
m

)
y
t
i
v
a
r
g
o
t
e
u
d
n
o
i
t
a
r
e

)

l

n
o
i
t
a
r
e
e
c
c
a
y
d
o
b

e
c
n
e
r
e
f
e
r

r
o
f
d
e
d
u
l
c
n

i

s
i

S
T
A

Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 4 of 14

by choosing a method to summarize data over a certain
period [29]. We combined both strategies by combining
three  axes  of  acceleration  into  one  metric,  summarized
and transmitted as a time-series (described below).

The  PSATs  in  this  study  record  pressure  (depth)  to
1700  m  (± 0.5  m  resolution),  temperature  from  −  40
to  60  °C  (± 0.05  °C  resolution),  and  light  levels  from
5 × 10−12 to 5 × 10−2 W cm−2, at 440 nm resolution. The
devices’  total  length  x  width  measured  124 × 38  mm,
with  a  weight  in  air  of  60  g  (Wildlife  Computers).  This
PSAT samples acceleration along the x, y, and z-axes (Ax,
Ay,  and  Az)  at  8  Hz  for  data  processing  and  calculation
of ATS, and then archives the processed data, along with
raw sensor data every 1 s for storage, which researchers
can access via download if they recover the tag.

The  user  chooses  the  time-series  frequency  and  cor-
responding summary period span for MiniPAT tags. The
summary period is used to parse the data into the time-
series intervals, which the PSAT will transmit via satellite.
This  also  provides  a  way  to  calculate  summary  statistics
to describe the animal or environment over longer dura-
tions  than  the  intervals  themselves.  In  this  study,  the
shortest  possible  time-series  interval  (75  s)  was  used  to
calculate  ATS;  however,  MiniPAT  time-series  can  be
programmed for longer intervals. A longer period would
cause  less  frequent  calculations,  but  would  extend  the
temporal coverage of the data. For example, a 75-s time-
series  uses  a  1-h  summary  period,  and  a  10-min  time-
series  uses  an  8-h  summary  period.  At  the  time  of  this
study, the tag could record and transmit 75-s time-series
data for activity, depth, and temperature, with additional
light-level  data  for  approximately  1  month  (Additional
file 1: Text and Additional file 1: Tables S1 and S2). All tag
conditions are set ahead of deployment using the Wildlife
Computers Tag Agent software.

We attached PSATs to the study animals via a tether to
an  umbrella  dart  embedded  in  the  dorsal  musculature,
such  that  the  tag  trailed ~ 6  cm  off  the  animals.  Tethers
comprised a stainless-steel cable sheathed in surgical tub-
ing and covered by heat-shrunk plastic tubing. We used
this  attachment  method  so  that  the  tags  could  detach
from  the  animal,  float  to  the  surface,  and  transmit  their
data. Tags continuously transmit data through the Argos
satellite  network  until  they  deplete  their  batteries.  We
note  that  most  accelerometer  experiments  on  fish  usu-
ally affix the tag to the dorsal fin, permitting analysis for
tri-axial acceleration to measure fine-scale fish pitch, roll,
and tail-beat frequency. As the ATS-PSATs are tethered,
permitting tag rotation, our application captures the total
force  exerted  on  the  tag  from  fish  movement.  Accord-
ingly, the summary metric is axis-independent and does
not  require  differentiation  among  the  x,  y,  and  z-axes.
As  such,  ATS  is  not  intended  to  provide  information

on,  or  measure  fine-scale  fish  pitch,  roll,  and  tail-beat
frequency,  nor  on  specific  behaviors  such  as  feeding  or
hunting.

Activity metric

In this study, we broadly defined ‘activity’ as an animal’s
whole-body  (locomotory  activity)  movement.  We  tested
a  filtered  metric  of  high  activity  that  can  be  applied
across  species  and  habitats  and  provide  information
about  an  animal’s  behavior  without  recovering  the  tag.
Wildlife  Computers  (WC)  (Wildlife  Computers,  Red-
mond,  WA,  USA),  in  consultation  with  the  authorship
team, developed the ATS metric and incorporated it into
a  WC  MiniPAT  tag.  WC  similarly  records  and  formats
all time-series data on their tags (e.g., at certain frequen-
cies and over certain time spans), so the ATS metric was
designed  to  operate  within  these  parameters.  After  pre-
programmed release from the animal, the PSAT begins a
series of calculations (illustrated in Fig. 1):

1. ‘Mobility’:  Mobility  is  the  row-wise  mean  of  the
standard  deviation  (σ)  of  acceleration   (Ax,   Ay,  and
 Az  are  the  x,  y,  and  z-axes  of  acceleration),  where  σ
is calculated over a 3-s moving window on the 8-Hz
data  that  advances  by  1-s  increments,  and  then
recorded for every 1 s:

Mobilityi = (cid:31)

24
i=1 σ (Axi + Ayi + Azi)
24

.

2. ‘High  activity’  (HA):  for  each  summary  period  (e.g.,
1  h),  the  Mobility  vector  is  centered  to  a  mean  of
0. Any  Mobility  values  occurring  in  the  tail  of  this
skewed  distribution  are  identified  as  HA  events.
Records in the ‘tail’ are isolated by a dynamic thresh-
old  value,  which  is  the  absolute  value  of  the  mini-
mum Mobility value of the centered distribution:

min

cent

HAthresholdi:i+3559 =

ϕ(Mobilityi:i+3599(cid:29)(cid:29)(cid:29)(cid:31)
(cid:31)

(cid:30)

(cid:30)(cid:30)

(cid:31)
(cid:31)
3.  ATS: the number of HA events during each 1-h sum-
mary  period  is  counted  and  split  into  time-series
intervals  (75  s).  The  count  of  HA  events  per  75-s
interval  is  then  transmitted  via  satellite  as  a  time-
series:

ATS[i:i+74] =

75

(cid:31)
i=1

Mi > HAthresholdi:i+74.

Transmitted  time-series  data  for  these  tags  include
the  time-series  data  itself  (ATS:  high  activity  counts
every  75  s)  and  ‘Series  Range’  data  (Additional  file  1:
Table  S1).  The  Series  Range  data  includes  a  set  of  met-
rics  that  describe  the  data  used  to  calculate  ATS  over  a

Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 5 of 14

Fig. 1  A visual depiction of how the activity time-series (ATS) metric is calculated onboard the pop-off satellite tag (PSAT). (1) Tri-axial acceleration
values are sensed at 8 Hz, and (2) are summarized as a single mobility (M) value (the mean standard deviation of the sum of Ax, Ay, and Az over a
3-s moving window). (3) The distribution of M over a set summary period is centered at zero, and a threshold value for HA events is established (the
absolute value of the minimum of the centered distribution), such that (4) an M value greater than the threshold is considered a high-activity (HA)
event. (5) The number of HA events is recorded over predetermined time-series (every 75 s) for transmission as ATS

1-h summary period; Series Range includes the mean and
standard  deviation  of  the  Mobility  vector  that  was  used
to  find  the  High  Activity  (HA)  events  over  each  succes-
sive 1 h. The count of HA events (ATS) over the 1-h sum-
mary period is included with the ‘Series’ data.

The  researcher  can  use  ATS  and  its  associated  sum-
mary  metrics  (e.g.,  Mobility)  to  describe  long-term  and
short-term activity patterns. The hourly mean and SD of
Mobility  provides  a  ‘baseline’  against  which  ATS  events
are  determined.  For  example,  a  1-h  record  of  a  reef  fish
swimming  at  a  moderate,  steady  speed  with  no  changes
in  acceleration  would  cause  low  ATS  values,  moderate
1-h mean Mobility, and low 1-h SD of Mobility. If the reef
fish were to have several bouts of quicker swimming (e.g.,
evading  a  predator),  there  would  be  several  instances  of
higher ATS data-points during the 1-h summary period,
with  higher  SD  in  Mobility.  Were  this  fish  to  rest  on
the  bottom  with  a  few  movements  over  the  hour,  mean
Mobility  would  be  very  low,  although  these  few  move-
ments would be reflected in the ATS values.

Design  considerations  We  note  that  our  metric  is  a
way to infer changes in activity from accelerometer data
on  a  PSAT.  It  is  not  reflective  of  ODBA  or  VeDBA,  and
the  inferences  gained  from  it  are  also  not  equivalent  to
those of ODBA or VeDBA (Table 1). Rather, Mobility and
ATS provide a metric of relatively high activity and when

these active events occur, in a time-series format that cor-
responds to existing time-series metrics for temperature
and  depth.  Given  the  metric,  and  individual  variation
both among and between species, the inference of a spe-
cific behavior is questionable and would likely not broadly
apply.

ATS simulation

To  contextualize  and  differentiate  ATS  from  prior  met-
rics  of  activity,  we  calculated  VeDBA  and  ATS  on  the
same  set  of  archival  data  from  tri-axial  accelerometer
loggers. We used two archives from wild deployments of
accelerometer  loggers,  one  at  50  Hz  from  a  nurse  shark
(Ginglymostoma  cirratum;  OpenTag  Motion  OT3  Data-
logger, Loggerhead Instruments. Sarasota, FL, USA), and
one at 16 Hz from a gray reef shark (Carcharhinus ambly-
rhynchos [9], ORI400-D3GT logger, Little Leonardo Co.,
Tokyo,  Japan).  Archives  were  sub-sampled  to  8  Hz  to
simulate data collected by ATS-PSATs. The sub-sampled
8-Hz  data  were  then  used  to  calculate  ATS  over  75-s
periods. After removing the static component of acceler-
ation  from  gravity  using  a  Butterworth  low-pass  filter
over
calculated  VeDBA
a
VeDBA =
z  ) at 8 Hz (using the packages
(

3-s  window,  we
y + A2
(cid:31)

x + A2

A2

“signal” and “tagtools” in R [35,  36]). We did not expect
that ATS would mirror VeDBA, but that relatively high-
activity  events  would  occur  at  similar  times.  We

 Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 6 of 14

identified  relatively  high-activity  from  VeDBA  by  apply-
ing  a  k-means  clustering  algorithm  with  four  clusters
(using  “stats”  in  R  [37]),  then  visually  compared  VeDBA
clusters with simulated ATS. We did not conduct statisti-
cal tests, because we did not expect ATS and VeDBA to
have similarities in their time-series—rather, we expected
to  see  higher  ATS  values  when  there  were  sustained
‘spikes’ in VeDBA.

Captive trials

Animal  tagging  To  test  the  performance  of  the  ATS
algorithm  for  measuring  burst-activity,  we  deployed  the
tags  on  captive  fish  under  both  video  and  visual  obser-
vation.  We  deployed  tags  on  cobia  (Rachycentron  cana-
dum),  which  allowed  us  to  test  the  performance  of  ATS
in  a  large,  fast-moving  teleost  fish  with  heterogeneous
activity  levels.  We  also  deployed  the  tags  on  a  relatively
slower  moving  fish  with  more  homogenous  activity  lev-
els  (dogfish  sharks,  Squalus  acanthias).  However,  after
considering the video records, we deemed the small size
of the animals (57–66 cm total length, TL) relative to the
tags insufficiently representative of wild applications. We
describe the tags’ data output is alongside that of cobia in
the supplementary electronic materials, however, did not
use these data for further analysis.

We  deployed  ATS-PSATs  over  5  days  on  four  mature
female cobia (103–112 cm TL, weight 8.16–9.07 kg) at the
University  of  Miami’s  Experimental  Hatchery  (UMEH)
facility  in  Miami,  FL,  USA). The  tank  housing  the  cobia
was  20  m  in  diameter  and  1.8  m  in  height  and  received
a constant influx of ultraviolet flow-through seawater fil-
tered down to 10 μm. We programmed the tags to release
from  the  fish  after  5  days.  We  then  recovered  the  tags
from  the  tanks  so  we  could  download  the  archived  data
for  a  comparison  of  raw  data  with  the  transmitted  ATS
product.  We  did  not  intend  our  captive  deployments  to
test the transmission of ATS; rather, we sought to use the
ATS  archive  for  comparison  with  observed  patterns  in
activity level.

Video observation  To record cobia activity patterns, we
mounted three GoPro cameras (two model HERO3 + and
one  model  HERO4,  GoPro,  San  Mateo,  CA)  around
the  tank  (two  downwards-facing,  one  lateral-facing).
Cameras  were  deployed  for  two,  2-h  periods  each  day
(0900–1100  h,  and  1500–1700  h)  to  capture  a  breadth
of behaviors and activity levels based on research facility
staff ’s prior knowledge (e.g., high activity associated with
feeding events). Using the video footage, we first visually
coded fish movements into 8 descriptive categories (Addi-
tional file 1: Table S3), and then sorted these into one of
three activity levels, referred to as  Activityobs: rest, cruis-
ing,  and  quicker  swimming.  “Rest”  was  identified  as  the

fish resting on the bottom of the tank; “cruising” as swim-
ming not preceded by acceleration, or swimming follow-
ing a ‘deceleration’; and “quicker” as swimming following
an acceleration. We assigned  Activityobs for each 1 s of the
video recording, for each fish, to correspond with the 1-s
frequency of PSAT archives.

Analysis  of  captive  trials  To  analyze  the  ability  of  ATS
to reflect a change in activity level, we further condensed
categories of  Activityobs into two states: Resting and Not
Resting. We used Bayesian logistic regression models with
ATS as a predictor of  ActivityObs using the ‘arm’ package
in R [38]. We also ran a multinomial model to see if ATS
could distinguish between additional behavior categories
(resting, cruising, and quicker swimming), using the ‘nnet’
package in R [39].

Wild deployments

To  test  the  ability  and  utility  of  the  ATS-enabled  PSATs
to record and transmit ATS with corresponding environ-
mental data from highly migratory species, we deployed
seven  ATS-PSATS  on  adult  sandbar  sharks  (Carcharhi-
nus plumbeus): two off the coast of Miami (Florida, USA)
and  five  off  the  coast  of  Ocean  City  (Maryland,  USA).
Our goal was to receive full triplets of time-series data to
match  activity  with  depth  and  temperature  data.  In  this
study, we use these data to confirm the potential of ATS
to monitor wild activity and do not infer beyond this. A
more  formal  analysis  of  activity  related  to  the  environ-
ment  will  be  forthcoming.  We  note  that  using  different
species for our wild and captive deployments was practi-
cal  (i.e.,  having  access  to  Cobia  in  a  captive,  observable
setting,  versus  having  no  access  to  sandbar  sharks  in  a
captive setting) and did not interfere with the study goals;
a strength of ATS is its adaptive threshold for HA events,
rather  than  a  pre-set  threshold.  The  tags  produced  data
suitable  for  analysis  so  long  as  the  species  were  suffi-
ciently large-bodied and varied in their activities. Rather
than additional assessment or validation of ATS itself, we
intended the wild deployments to test whether the ATS-
PSATs  work  in  a  field-setting  and  whether  the  tags  can
collect  activity  data  along  with  temperature  and  depth
time-series.

PSAT deployments  Sharks in Miami were caught as part
of an ongoing survey using methods described in Calich
et  al.  [40],  then  briefly  restrained  for  tagging  and  meas-
urement. Sharks in Maryland were caught using rod and
reel  before  tagging,  measurement,  and  release.  PSATs
were attached to the animals using a plastic umbrella dart
inserted  into  the  dorsal  musculature,  using  a  stainless-
steel  applicator.  For  Miami  deployments,  PSATS  were
test tags provided by the manufacturer with known weak

Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 7 of 14

attachment points at the tag release mechanism, so while
we configured them for 30-day deployments, we expected
a premature release for these 2 tags. For Maryland deploy-
ments, we programmed all five PSATS for a 30-day deploy-
ment.  Besides  instrumentation,  each  animal  was  sexed
and measured for pre-caudal, fork, and total lengths [41].

most likely position of an animal at a given time. Before
using  GPE3,  we  removed  observations  from  after  the
PSATs released from the animals (based on depth time-
series showing a rapid ascent and subsequent residency at
the surface) so that movement path calculation was only
based on data from when the PSAT was on the animal.

Analysis  of  wild  deployments  We  estimated  the  move-
ment  paths  of  the  animals  with  the  GPE3  state–space
modeling  tool  in  the  Wildlife  Computers  Data  Portal.
GPE3  uses  transmitted  observations  of  irradiance  (sun-
set  and  sunrise  times),  dive  depth,  and  ambient  surface
temperature data, in combination with a diffusion-based
movement model and known locations (from deployment
location  and  known  Argos  locations),  to  estimate  the

Results
ATS simulation

Using  archived  accelerometer  data  from  wild  deploy-
ments  on  a  nurse  shark  (20  min)  and  a  gray  reef  shark
(6  h),  we  calculated  ATS,  and  VeDBA  (Fig.  2).  Visual
examination  showed  similar  timing  for  ATS  (Fig.  2a,
c),  and  changes  in  VeDBA  (Fig.  2b,  d).  The  reef  shark’s
highest  ATS  values  occurred  within  the  first  two  hours

Fig. 2  A comparison of ATS and Mobility a, c with VeDBA b, d, calculated from two archived tri-axial accelerometry datasets. “High-Activity” (HA)
events based on mobility are indicated by black points, which are counted over 75-s periods to calculate ATS (orange line). In c, a gray line indicates
mean hourly mobility. VeDBA is colored by cluster, determined by a k-means clustering algorithm with a total of 4 clusters, to visualize different
activity levels. ATS and Mobility are not meant to replicate VeDBA, but rather to indicate relative high activity over time

 Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 8 of 14

(Fig.  2c,  d),  when  VeDBA  was  most  frequently  switch-
ing from low to high values. For the remainder of the 6-h
time-series,  ATS  was  lower,  when  VeDBA  values  were
lower and showed fewer instances of switching to a rela-
tively higher magnitude.

Captive deployments

PSAT  deployments  Of  the  four  PSATs  deployed  on
cobia, three tags dislodged prematurely from the fish after
1, 1.5, and 4.5 days, and one tag remained attached for the
full  5  days.  Video  recording  captured  approximately  24
total hours of video for the tag that remained in place for
the full 5 days (Additional file 1: Table S4 and S5, describes
video recording durations for each tag).

ATS  as  a  predictor  of  activity  We  observed  some  vari-
ability  in  observed  activity  during  the  intervals  being
reported by ATS—for instance, between resting and cruis-
ing (Fig. 3a), and between cruising and quicker swimming
(Fig.  3b).  The  time-series  nature  of  ATS  allows  it  to  be
adaptable  throughout  the  deployment,  which  is  evident
from the range of ATS values for each  ActivityObs level. For
example,  Fig.  3  shows  increased  mobility  for  cobia  over
two  time  periods;  in  Fig.  3a,  the  changes  from  ‘resting’
to prolonged durations of ‘cruising’ lead to the identifica-
tion of more ‘Active Events’ via ATS than for the changes
from  ‘cruising’  to  short  durations  of  ‘quicker  swimming’
in  Fig.  3b.  Our  logistic  regression  model  suggested  that
ATS was a significant predictor of  Activityobs (coefficient
estimate  0.322,  standard  error  0.002,  z-test  value  151.5,

p  value  of  the  z  statistic  Pr  ( >|z|) < 0.001;  Additional
file 1: Figures S1–S3) for the cobia, with the odds ratio of
switching from resting to not resting when ATS increased
was 1.38. A pseudo-Chi-square test for goodness of fit fol-
lowing Matthiopoulos et al. [42] returned a value greater
than 0.05, indicating an acceptable model fit.

Wild deployments

PSAT  deployment  descriptions  Miami  We  deployed
the ATS-PSATs in July 2018 on two adult female sandbar
sharks near Miami, FL (FL1 and FL2, Table 2 and Fig. 4).
Both of the sharks were on the fishing gear for less than
30 min ahead of retrieval and tagging, and were in good
condition  upon  release.  The  PSATs  used  in  these  two
deployments  released  after  15  and  1  days  for  the  sharks
FL1 and FL2, respectively. As noted above, these tags were
test tags, so we anticipated the premature release. Because
of the short deployment duration, these tags transmitted
near-complete  datasets  while  floating  at  the  surface:  A
shorter deployment resulted in fewer data collected and
therefore  fewer  data  messages  to  be  transmitted  for  a
complete dataset. Fewer data messages to be transmitted
resulted in greater opportunity to transmit each message
multiple times, and therefore increased the likelihood that
satellites would receive each message without corruption.
For  these  two  tags,  the  majority  (81.1  to  100%)  of  each
activity,  temperature,  and  depth  time-series  were  trans-
mitted and received; 61.7 (FL1) and 94.6% (FL2) contained
the  full  75-s  time-series  triplet  (of  activity,  temperature,
and depth). For ATS alone, 83.3 (FL1) and 94.6% (FL2) of

Fig. 3  For captive cobia CC2, 1-s mobility and Az, and 75-s ATS values over two 8-min periods. The gray bars indicate the count of ATS values, the
black line indicates Az, and circles indicate mobility values (the mean standard deviation of the sum of Ax, Ay, and Az over a 3-s window). The color
of each mobility data-point indicates which activity level was observed for that 1-s timepoint from video observation. Although one individual fish
is displayed here, these patterns were similar across all data

Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 9 of 14

Table 2  Animal  size,  sex,  tagging  location,  deployment  duration,  and  shark  characteristics  for  the  seven  wild
Carcharhinus plumbeus tagged with PSATs

Tagging

Shark characteristics

Movement summary

ID

Date

Lat (DDs)

Lon (DDs)

Duration
(days)

Sex

PCL (cm)

FL (cm)

TL (cm)

Distance (km)

Speed (km/day)

FL1

FL2

MD1

MD2

MD3

MD4

MD5

2018-07-22

2018-07-15

2018-09-19

2018-09-19

2018-09-19

2018-09-30

2018-10-04

25.64

25.80

38.22

38.23

38.22

38.38

38.25

 80.09

 80.08

 75.03

 75.12

 75.12

 74.10

 74.08

−

−

−

−

−

−

−

14

 < 2

30

30

30

30

30

F

F

M

F

F

F

F

160

161

105

120

122

103

105

178

177

115

136

132

113

115

214

217

152

164

163

140

142

582.21

–

241.41

318.46

789.12

832.66

260.34

19.42

–

7.91

12.80

26.05

27.24

8.59

Lat latitude, Lon longitude, PCL pre-caudal length, TL total length

the  hourly  M  records  were  transmitted  and  received
from MD sharks.

Depth  and  temperature  trends  To  demonstrate  the
‘triplet’  of  measurements,  we  show  the  75-s  resolution
time-series  for  activity,  temperature,  depth,  over  the
entire  deployment  for  sharks  FL1  (Fig.  6)  near  Florida,
and MD1 (Fig. 7) near Maryland. Summary data for all 7
deployments (Table 3) shows a higher mean temperature
over  the  deployments  in  FL  (26.7 ± 2.2  °C  for  FL  sharks
vs  22.5 ± 1.8  °C  for  MD  sharks)  and  a  broader  tempera-
ture range (12.3–30.8 °C for FL sharks vs 10.4–26.1 °C for
MD sharks). Depth range was broadest over the deploy-
ments in FL (0-213 m for FL sharks vs 0.5-127 m for MD
sharks).  Mobility  values  had  a  similar  range  between
regions  (28–63  for  FL  sharks  vs  29–63  for  MD  sharks),
with higher mean mobility values for deployments in MD
(37.54 ± 8.98 for FL sharks vs 51.75 ± 11.8 for MD sharks).

Discussion
The simulated activity metric compared with VeDBA

As  we  anticipated,  our  simulation  of  ATS  from  acceler-
ometer  data  loggers  reflected  the  timing  of  switches  to
relatively  high  values  in  the  VeDBA  time-series  (Fig.  2).
Over the six hours of data from the reef shark, the ATS
time-series  showed  a  decrease  that  mirrored  decreasing
VeDBA values over the same time span.

Evaluations of the activity metric based on captive trials

For the captive trials, ATS was a significant predictor of
 ActivityObs.  The  results  of  our  logistic  regression  model
had  an  odds  ratio  greater  than  one,  indicating  that  as
ATS increases, the switch from resting to not resting will
occur more often than not (e.g., 1.38 times more likely).
Our  multinomial  model’s  results  showed  that  ATS  was
a  good  predictor  of  multiple  activity  levels,  with  the
transitions  from  both  resting  to  cruising  and  resting  to

Fig. 4  Tagging locations, tag release locations, and geolocations for
the two sandbar sharks tagged near Miami (Florida, USA). For shark
FL2, only the location of tagging was available

both the time-series and range data were transmitted and
received.

Ocean  City,  MD  We  successfully  deployed  ATS-
PSATs  on  five  sandbar  sharks  off  the  coast  of  Ocean
City,  Maryland,  USA,  in  August  2018  (MD1–MD5  in
Table  2  and  Fig.  5).  All  sharks  were  in  good  condition
upon  release.  Tags  remained  on  the  sharks  for  their
pre-programmed 30-day duration. Each of the five tags
transmitted the majority of each 75-s activity, tempera-
ture,  and  depth  time-series  (56.4–72.1%).  Of  the  time-
points  covering  the  30-day  deployment,  22.2–41.2%
contained  the  full  75-s  time-series  triplet  (of  activity,
temperature,  and  depth).  Additionally,  57.4–73.2%  of

 Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 10 of 14

Fig. 5  a Tagging locations, tag release locations, and geolocations for the five sandbar sharks tagged near Ocean City (Maryland, USA), and b
geolocations for shark MD1, with locations colored by date

quick  swimming  being  significant.  Cobias’  variability  in
 Activityobs likely explains the ability of the model to pre-
dict changes in their activity from ATS; we observed the
fish resting, cruising, and swimming quickly around their
tank, and displaying a significant change in activity dur-
ing  feeding  events.  This  suggests  that  ATS  can  identify
large changes in variable activity patterns. The detection
of  this  variability  in  cobia  suggests  that  ATS  could  play
a role in detecting differences in activity among individ-
ual  sharks,  which  researchers  could  relate  to  life  history
characteristics (size, sex, reproductive stage) or environ-
mental conditions.

Our  results  are  in  line  with  other  studies.  Accelerom-
eters recording at 5 Hz sufficed to capture swimming and
resting behaviors in lemon sharks (Negaprion brevirostris
[25]).  In  sailfish,  satellite-transmitted  metric  of  accel-
eration  data  (the  standard  deviation  of  g,  where  g  is  the
square  root  of  the  sum  of  acceleration  over  3  min)  was
successfully used to characterize general activity patterns
[26].  Despite  a  longer  summary  period  of  3  min,  versus
the 75 s in this study, the authors detected diel periodic-
ity in relative activity levels.

The activity metric in wild deployments

In FL, the short deployment duration enabled a high pro-
portion  of  data  transmission  and  reception,  providing
a  detailed  look  at  post-release  behavior.  For  shark  FL1,
linking  the  estimated  movement  path  with  the  activity

data suggests a relatively low activity for the first 8–9 days
of  the  track.  During  this  time,  the  shark  moved  steadily
northwards, followed by periods of higher activity behav-
ior for the remaining 4 days of the track (Fig. 7a-b) when
the shark remained in a localized area (Fig. 5).

In  MD,  the  longer  deployments  provided  a  broader
perspective  of  activity  levels,  temperature,  depth,  and
spatial  movements.  For  instance,  shark  MD1  moved
directly  southwest  for ~ 6  days  after  tag  deployment,
heading  towards  the  continental  shelf  (Fig.  5).  As  the
shark approached the edge of the shelf, there were more
clustered  locations  for ~ 14  days.  Next,  the  shark  moved
back  to  the  continental  shelf,  and  then  southwards  for
the remainder of the 31-day track. There were three time
periods of sustained higher Mobility and increased ATS
values  during  the  track  (Fig.  7a,  b):  post-release  (Sept.
20), once the shark moved off the shelf, and when it con-
ducted  a  series  of  deeper  dives  in  a  localized  area  (Oct.
6–7 and Oct. 11–12; Fig. 6d). Additionally, MD1 Mobility
values appeared higher at night than during the day prior.

Limitations
The  time-series  nature  of  ATS  renders  it  low  resolution
when  compared  with  recovering  a  full  archive  of  accel-
erometer  data.  As  a  result,  fine-scale  behaviors  such  as
burst  acceleration  events  may  be  obscured  if  they  occur
on  very  short  timescales.  Further,  we  could  not  account
for  the  influence  of  water  flow  on  tag  movement.  This

Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 11 of 14

Fig. 6  For shark FL1, a 75-s ATS (activity time-series), b 1-h Mobility, and c depth at 75-s frequency, and d mean mobility over 1 h, for the 30-day
deployment. Blue circles indicate time-series datapoints, and the thick white or black line represents a smoothed time-series using the loess
method at a 5% span. Shaded gray rectangles indicate sunset to sunrise (20:00 to 06:30)

was  most  limiting  in  captive  testing,  as  cobia  were
smaller  relative  to  the  PSATs,  compared  with  the  sand-
bar sharks. Lastly, the results from the captive trials sug-
gest that while this metric is suitable for teleost fish with
variable levels of activity, benthic fish with homogenous
activity  levels  (e.g.,  smooth  dogfish  sharks)  may  not  be
practical candidates.

The  1-s  archived  values  of  mobility  from  the  cobia
(Fig.  3)  suggest  some  considerations  for  inference.  First,
the  summary  period  for  ATS  may  have  a  lag  effect
because  the  duration  of  an  activity  may  not  fully  occur
within  one  time-series  interval  (Fig.  2a).  Consequently,
the  summary  period  and  time-series  interval  should  be
chosen wisely, ideally using prior knowledge of the study
species.  Second,  short  durations  of  high-mobility  values
did  not  appear  to  have  a  strong  effect  on  ATS  for  cobia
(Fig. 3b). However, the lag effect was not apparent in our
simulation  of  ATS  on  archived  data  from  wild  deploy-
ments  of  accelerometer  loggers  (Fig.  2a,  c);  this  may  be
due to greater variation in activity levels observed for the
archived  data  (nurse  sharks  and  gray  reef  sharks),  such

that  relatively  high-activity  was  more  pronounced  for
those species for the cobia.

Lastly,  in  this  study,  our  ATS-PSATS  were  limited  to
1-month deployments for our choice of tag settings (e.g.,
75-s time-series intervals). For future ATS-PSAT deploy-
ments, developers have extended this recording period to
3 months, with the accelerometer now able to sample at
10 Hz.

Conclusions

In summary, we tested a novel satellite-transmitted met-
ric of activity in captive and wild settings, to approximate
coarse activity levels in free-ranging aquatic animals. This
metric is intended to measure relative changes in activity
levels over a sufficient length of time to capture variabil-
ity across a range of environmental conditions, which can
transmitted  via  satellite.  This  metric  is  not  intended  to
replace  the  high-resolution  data  collection  and  analysis
from  recoverable  devices  which  permit  a  more  detailed
description of behavior and an absolute measure of activ-
ity  level  at  a  specific  time  point.  In  captive  animals,  the

 Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 12 of 14

Fig. 7  For shark MD1, a 75-s ATS (activity time-series), b 1-h Mobility, and c depth at 75-s frequency, and d mean mobility over 1 h, for the 30-day
deployment. Blue circles indicate time-series datapoints, and the thick white or black line represents a smoothed time-series using the loess
method at a 5% span. Shaded gray rectangles indicate sunset to sunrise (20:00 to 06:30)

Table 3  Temperature,  depth,  and  activity  time-series  (ATS),  and  mobility  trends  across  all  five  sharks,  and  all  sharks
analyzed together, based on 75-s transmitted values

ID

Temperature (°C)

Mean

±

 SD

FL1

FL2

All FL

MD1

MD2

MD3

MD4

MD5

All MD

27.02

 1.94

25.45

 2.67

26.71

 2.19

21.77

 1.40

23.96

 0.53

22.11

 1.60

20.63

 1.27

24.10

 1.05

±

±

±

±

±

±

±

±

±

22.54

 1.77

Range

12.3–30.9

15.8–30.2

12.3–30.9

10.4–24.8

22.2–25.3

13.4–25.8

11.8–24.1

13.4–26.1

10.4–26.1

Depth (m)

Mean

±

 SD

ATS

Range

Mean

±

 SD

Range

Mobility

Mean

±

 SD

39.1

 30.5

0.5–213

13.1

 21.7

34.21

 30.77

15.72

 7.98

8.70

 3.75

13.80

 11.10

16.71

 13.00

11.20

 4.66

13.13

 9.36

±

±

±

±

±

±

±

±

±

 6

 5

3

4

–

±

±

3.78

 7.05

3.02

 4.86

4.49

 6.41

3.10

 5.68

5.67

 7.60

±

±

±

±

±

0–142

0–213

1–82.5

1–19

0.5–91.5

0.5–127

1.5–46

0.5–127.0

–

0–73

0–48

–

0–73

0–63

0–73

0–73

0–73

–

35.92

 7.01

37.90

 9.75

37.54

 8.98

45.24

 7.27

60.84

 7.78

49.52

 11.56

62

 2.28

40.58

 9.74

51.75

 11.8

±

±

±

±

±

±

±

±

±

Range

28–63

31–50

28–63

35–63

30–63

31–63

50–63

34–44

29–63

SD indicates standard deviation, range indicates minimum to maximum values, and IQR indicates the interquartile range (25–75th percentiles). ATS is not given across
all sharks, as the values are calculated relative to the individual sharks’ mobility measurements within 75 s. Mobility is recorded hourly

ATS,  recorded  as  a  75-s  time-series  of  acceleration  at
8 Hz, was used to predict visually observed behaviors in
cobia, a large teleost fish. Wild deployments in Maryland
and  Florida  (USA)  produced  a  concurrent  time-series

record of activity, temperature, and depth. This suggests
the potential for interpreting relative activity in the con-
text of an animals’ environment. These data may also be
useful for studying the post-release recovery from fishery

Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 13 of 14

interactions over periods of weeks to months, depending
upon tag settings.

We  particularly  recommend  this  metric  in  settings
feasibly  retrieve  biolog-
where  researchers  cannot
ging  devices.  The  most  successful  research  applications
would  target  animals  that  are  both  relatively  large  (e.g.,
fish > 1.5  m  total  length)  and  undergo  considerable  vari-
ability  in  activity  (e.g.,  from  resting  to  moving,  or  from
slow  to  fast  swimming  speeds).  Although  the  frequency
of the logged activity metric tested here (75 s) is too low
to capture more fine-scale behaviors, we believe this met-
ric  is  measured  at  a  sufficient  frequency  (8  Hz)  ahead
of  filtering  to  be  a  proxy  for  the  distribution  of  general
activity level across time and space. The combination of
ATS,  and  environmental  data  over  longer  periods  pro-
vides  a  unique  opportunity  for  investigating  the  effects
of  temperature  on  activity,  diel  activity  patterns,  activ-
ity  patterns  near  habitat  features  (e.g.,  coral  reefs  ver-
sus  pelagic  areas),  and/or  comparisons  of  high-activity
events  among  individuals  and  species.  This  is  the  first
transmittable  metric  of  continuous  whole-body  activ-
ity available on a PSAT-style tag, and our results suggest
that this activity metric could provide another dimension
(relatively  high-activity)  to  studies  of  long-range  aquatic
animal movements.

Supplementary information
Supplementary information accompanies this paper at https ://doi.
org/10.1186/s4031 7-020-00220 -0.

Additional file 1: Text. Methodology for the deployment of PSATs on
dogfish sharks (Squalus acanthias). Figure S1. An example of camera out-
put used for activity level description and classification, of captive cobia a
and dogfish b. Figure S2. Frequency distribution of archival values from
captive deployments, for mobility (a, b) and activity time-series (ATS) (c, d),
for all animals of each species. Each panel includes mean, standard devia-
tion, and range. Figure S3. A logistic curve based on the results of our
binary logistic regression for  ActivityObs ~ ATS. Teal circles represent obser-
vations of ATS, classified as either resting (0) or not resting (1). Table S1.
Data products generated by the Wildlife Computers miniPAT pop-off
satellite tag (PSAT). Table S2. Estimated deployment durations for the
Wildlife Computers miniPAT pop-off satellite tag (PSAT) incorporating the
ATS metric, depending on the length of the summary period (75 to 600 s).
Percentages represent the probability of receiving 1 message, and a triplet
of messages, sent 10, 20, and 30 times. Table S3. Description of observed
behavior states from video recordings of captive cobia and dogfish. States
were also observed in combination (e.g., quick swimming while rolling/
righting). Table S4. Animal characteristics for captive trials, and temporal
tag and video coverage of fish activity. Tag detachment was based on
visual observation of detachment where possible or estimated from
depth and activity time-series (ATS) records downloaded from tags, as the
point in time where depth and ATS remained constant. Captive dogfish
(Squalus acanthias) are indicated as CD, and captive cobia (Rachycentron
canadum) as CC. Table S5. The number of 1 s labeled visual observations
from video-recording of captive fish behavior, and the proportion of each
behavior (%) with respect to total observations for the species.

Abbreviations
PSAT: Pop-off satellite archival tag; miniPAT: Wildlife Computers-brand
PSAT; ATS: Activity time-series, a count of relatively high-activity events per

time-series interval; Mobility: Raw accelerometer measurements summarized
as the mean standard deviation of the sum of Ax, Ay, and Az; ActivityObs: Visu-
ally observed activity.

Acknowledgements
For their assistance in captive trials, we thank the staff and student volunteers
of the University of Miami Experimental Hatchery, particularly R. Hoenig, J.
Florentino, and S. Mathur, the University of Miami Shark Research and Conser-
vation Program, and the University of New England Department of Marine Sci-
ence. Thank you to Austin Gallagher from Beneath the Waves Inc and his team,
for deploying PSATS on sandbar sharks off Maryland. Thanks to Gaétan Richard
for the initial development of the activity algorithm and providing feedback
on our adaptation for use on a PSAT. We acknowledge that this research was
performed on ancestral Tequesta and Seminole territories.

Authors’ contributions
RS, NH, and YP conceived the ideas and designed methodology for testing
the algorithm; RS, HJV, and NH collected the data; RS analyzed the data and
led the writing of the manuscript, and KW adapted and integrated the ATS
algorithm for use on a PSAT, and assisted with data analysis for captive trials.
All authors contributed critically to the drafts. All authors read and approved
the final manuscript.

Funding
RS is supported by an NSERC PGS-D scholarship from the Government of
Canada, a UM Fellowship from the University of Miami, and a Guy Harvey
Scholarship from Florida Sea Grant and the Guy Harvey Ocean Foundation.
This study was supported by a University of Miami Provost Grant.

Availability of data and materials
The datasets and code produced during the current study are available from
the corresponding author on reasonable request.

Ethics approval and consent to participate
All applicable international, national, and institutional guidelines for the care
and use of animals were followed. All procedures in studies involving animals
were performed following ethical standards of the institution at which the
studies were conducted (the University of Miami Institutional Animal Care and
Use Committee (IACUC), Protocol Numbers [15–238], and the University of
New England IACUC Protocol Number 051518-001).

Consent for publication
Not applicable.

Competing interests
Authors declare no competing interests.

Author details
1 Abess Center for Ecosystem Science and Policy, University of Miami, Coral
Gables, FL, USA. 2 Wildlife Computers, Redmond, WA, USA. 3 Department
of Biological Sciences, Florida International University, North Miami, FL, USA.
4 School of Life Sciences, Arizona State University, Tempe, AZ, USA. 5 School
of Mathematical and Natural Sciences, Arizona State University, Glendale,
AZ, USA. 6 Rosenstiel School of Marine and Atmospheric Science, University
of Miami, Miami, FL, USA.

Received: 26 February 2020   Accepted: 17 October 2020

References

 1. Nathan R, Getz WM, Revilla E, Holyoak M, Kadmon R, Saltz D, et al. A

movement ecology paradigm for unifying organismal movement
research. Proc Natl Acad Sci. 2008. https ://doi.org/10.1073/pnas.08003
75105 .

 2. Hays GC, Bailey H, Bograd SJ, Bowen WD, Campagna C, Carmichael RH,
et al. Translating Marine Animal Tracking Data into Conservation Policy
and Management. Trends Ecol Evol. 2019. https ://doi.org/10.1016/j.
tree.2019.01.009.

 Skubel et al. Anim Biotelemetry            (2020) 8:34

Page 14 of 14

 3. Hussey NE, Kessel ST, Aarestrup K, Cooke SJ, Cowley PD, Fisk AT, et al. Aquatic
animal telemetry: a panoramic window into the underwater world. Science.
2015;348:1255642.

 24. Southall EJ, Sims DW, Witt MJ, Metcalfe JD. Seasonal space-use estimates of
basking sharks in relation to protection and political–economic zones in the
North-east Atlantic. Biol Cons. 2006;132:33–9.

 4. Dean B, Freeman R, Kirk H, Leonard K, Phillips RA, Perrins CM, et al. Behav-

 25. Sequeira AMM, Mellin C, Fordham DA, Meekan MG, Bradshaw CJA. Predict-

ioural mapping of a pelagic seabird: combining multiple sensors and a
hidden Markov model reveals the distribution of at-sea behaviour. J R Soc
Interface. 2012;10:20120570–20120570.

 5. Payne NL, Taylor MD, Watanabe YY, Semmens JM. From physiology to

physics: are we recognizing the flexibility of biologging tools? J Exp Biol.
2014;217:317–22.

 6. Whitney NM, Pratt HL, Pratt TC, Carrier JC. Identifying shark mating behav-

 7.

iour using three-dimensional acceleration loggers. Endang Species Res.
2010;10:71–82.
Scharf AK, LaPoint S, Wikelski M, Safi K. Acceleration data reveal highly
individually structured energetic landscapes in free-ranging fishers (Pekania
pennanti) Ropert-Coudert Y, editor. PLoS ONE. 2016;11:e0145732.

 8. Andrzejaczek S, Gleiss AC, Pattiaratchi CB, Meekan MG. First insights into the

fine-scale movements of the Sandbar Shark Carcharhinus plumbeus. Front
Mar Sci. 2018;5:1–12.

 9. Papastamatiou YP, Watanabe YY, Bradley D, Dee LE, Weng K, Lowe CG, et al.
Drivers of daily routines in an ectothermic marine predator: hunt warm, rest
warmer? PLoS ONE. 2015;10:e0127807.

 10. Gleiss AC, Morgan DL, Whitty JM, Keleher JJ, Fossette S, Hays GC. Are vertical
migrations driven by circadian behaviour? Decoupling of activity and depth
use in a large riverine elasmobranch, the freshwater sawfish (Pristis pristis).
Hydrobiologia. 2016;787:1–11.

 11. Whitney NM, White CF, Anderson PA, Hueter RE, Skomal GB. The physi-

ological stress response, postrelease behavior, and mortality of blacktip
sharks (Carcharhinus limbatus) caught on circle and J-hooks in the Florida
recreational fishery. FB. 2017;115:532–43.

 12. Mohan JA, Jones ER, Hendon JM, Falterman B, Boswell KM, Hoffmayer
ER, et al. Capture stress and post-release mortality of blacktip sharks in
recreational charter fisheries of the Gulf of Mexico. Cooke S, editor. Conserv
Physiol. 2020;8:coaa041.

 13. Barnett A, Payne NL, Semmens JM, Fitzpatrick R. Ecotourism increases the
field metabolic rate of whitetip reef sharks. Biol Conserv . 2016;199:132–6.
 14. Wilson ADM, Brownscombe JW, Krause J, Krause S, Gutowsky LFG, Brooks EJ,
et al. Integrating network analysis, sensor tags, and observation to under-
stand shark ecology and behavior. Behav Ecol. 2015;26:1577–86.
 15. Cooke SJ, Hinch SG, Wikelski M, Andrews RD, Kuchel LJ, Wolcott TG,

et al. Biotelemetry: a mechanistic approach to ecology. Trends Ecol Evol.
2004;19:334–43.

 16. Noda T, Kawabata Y, Arai N, Mitamura H, Watanabe S. Animal-mounted
gyroscope/accelerometer/magnetometer: In situ measurement of the
movement performance of fast-start behaviour in fish. J Exp Mar Biol Ecol.
2014;451:55–68.

 17. Broell F, Noda T, Wright S, Domenici P, Steffensen JF, Auclair J-P, et al. Accel-
erometer tags: detecting and identifying activities in fish and the effect of
sampling frequency. J Exp Biol. 2013;216:1255–64.

 18. Horie J, Mitamura H, Ina Y, Mashino Y, Noda T, Moriya K, et al. Development
of a method for classifying and transmitting high-resolution feeding behav-
ior of fish using an acceleration pinger. Anim Biotelemetry. 2017;5:12.
 19. Ydesen KS, Wisniewska DM, Hansen JD, Beedholm K, Johnson M, Madsen
PT. What a jerk: prey engulfment revealed by high-rate, super-cranial accel-
erometry on a harbour seal (Phoca vitulina). J Exp Biol. 2014;217:2814–2814.

 20. Lear KO, Whitney NM, Brewster LR, Morris JJ, Hueter RE, Gleiss AC.

Correlations of metabolic rate and body acceleration in three species
of coastal sharks under contrasting temperature regimes. J Exp Biol.
2017;220:397–407.

 21. Lear KO, Gleiss AC, Whitney NM. Metabolic rates and the energetic cost of

external tag attachment in juvenile blacktip sharks Carcharhinus limbatus. J
Fish Biol. 2018;93:391–5.

 22. Meekan MG, Fuiman LA, Davis R, Berger Y, Thums M. Swimming strategy

and body plan of the world’s largest fish: implications for foraging efficiency
and thermoregulation. Front Mar Sci. 2015;2:1–8.

 23. White CF, Anderson PA, Hueter RE, Whitney NM, White CF, Anderson PA, et al.
The physiological stress response, postrelease behavior, and mortality of
blacktip sharks (Carcharhinus limbatus) caught on circle and J-hooks in the
Florida recreational fishery. Fish Bull. 2017;115:532–43.

ing current and future global distributions of whale sharks. Glob Change
Biol. 2014;20:778–89.

 26. Boucek RE, Heithaus MR, Santos R, Stevens P, Rehage JS. Can animal habitat
use patterns influence their vulnerability to extreme climate events? An
estuarine sportfish case study. Glob Change Biol. 2017;23:4045–57.
 27. Dedman S, Officer R, Brophy D, Clarke M, Reid DG. Modelling abundance
hotspots for data-poor Irish Sea rays. Ecol Model. 2015;312:77–90.

 28. Cox SL, Orgeret F, Gesta M, Rodde C, Heizer I, Weimerskirch H, et al. Process-
ing of acceleration and dive data on-board satellite relay tags to investigate
diving and foraging behaviour in free-ranging marine predators. O’Hara RB,
editor. Methods Ecol Evol. 2018;9:64–77.

 29. Nielsen JK, Rose CS, Loher T, Drobny P, Seitz AC, Courtney MB, et al. Char-
acterizing activity and assessing bycatch survival of Pacific halibut with
accelerometer Pop-up Satellite Archival Tags. Anim Biotelemetry. 2018;6:10.
 30. Block BA, Dewar H, Farwell C, Prince ED. A new satellite technology for track-

ing the movements of Atlantic bluefin tuna. PNAS. 1998;95:9384–9.

 31. Boustany AM, Davis SF, Pyle P, Anderson SD, Le Boeuf BJ, Block BA. Expanded
niche for white sharks. Nature. 2002. https ://doi.org/10.1038/41503 5b.
 32. Teo SLH, Boustany A, Blackwell S, Walli A, Weng KC, Block BA. Validation of
geolocation estimates based on light level and sea surface temperature
from electronic tags. Mar Ecol Prog Ser. 2004;283:81–98.

 33. Jeanniard-du-Dot T, Trites AW, Arnould JPY, Guinet C. Reproductive success
is energetically linked to foraging efficiency in Antarctic fur seals. Wang D-H,
editor. PLoS ONE. 2017;12:e0174001.

 34. Pohlot BG, Ehrhardt N. An analysis of sailfish daily activity in the Eastern
Pacific Ocean using satellite tagging and recreational fisheries data.
Grabowski J, editor. ICES J Mar Sci. 2018;75:871–9.

 35. signal: Signal processing [Internet]. Signal developers. https ://r-forge .r-proje

ct.org/proje cts/signa l/.Accessed 07 Aug 2020.

 36. DeRuiter S. tagtools: tools for working with data from high-resolution

biologging tags. 2020. https ://githu b.com/stacy derui ter/TagTo ols. Accessed
7 Aug 2020.

 37. R Core Team. R: A language and environment for statistical computing
[Internet]. Vienna: R Foundation for Statistical Computing; 2020. https ://
<www.R-proje> ct.org/.Accessed 07 Aug 2020.

 38. Gelman A, Hill J. Data analysis using regression and multilevel/hierarchical

models. Cambridge: Cambridge University Press; 2007.

 39. Venables WN, Ripley BD. Modern applied statistics with S. Fourth. New York:

Springer; 2002.

 40. Calich H, Estevanez M, Hammerschlag N. Overlap between habitat suitabil-
ity and longline gear management areas reveals vulnerable and protected
habitats for highly migratory sharks. Mar Ecol Prog Ser. 2018;602:183–95.
Irschick DJ, Hammerschlag N. Morphological scaling of body form in
four shark species differing in ecology and life history. Biol J Lin Soc.
2015;114:126–35.

 41.

 42. Matthiopoulos J. How to be a quantitative ecologist. How to be a quantita-

tive ecologist. Chichester: John Wiley & Sons, Ltd; 2011.

 43. Heerah K, Cox SL, Blevin P, Guinet C, Charrassin J-B. Validation of dive forag-

ing indices using archived and transmitted acceleration data: the case of
the weddell seal. Front Ecol Evol. 2019;7:30.

 44. Rose CS, Nielsen JK, Gauvin JR, Loher T, Sethi SA, Seitz AC, et al. Survival

outcome patterns revealed by deploying advanced tags in quantity: Pacific
halibut ( Hippoglossus stenolepis ) survivals after release from trawl catches
through expedited sorting. Can J Fish Aquat Sci. 2019;76:2215–24.

 45. Nishiumi N, Matsuo A, Kawabe R, Payne N, Huveneers C, Watanabe YY, et al.

A miniaturized threshold-triggered acceleration data-logger for recording
burst movements of aquatic animals. J Exp Biol. 2018;221:jeb172346.

 46. Halsey LG, Green JA, Wilson RP, Frappell PB. Accelerometry to estimate

energy expenditure during activity: best practice with data loggers. Physiol
Biochem Zool. 2009;82:396–404.

Publisher’s Note
Springer Nature remains neutral with regard to jurisdictional claims in pub-
lished maps and institutional affiliations.
