Whitford and Klimley  Anim Biotelemetry            (2019) 7:26
<https://doi.org/10.1186/s40317-019-0189-z>

Animal Biotelemetry

REVIEW

Open Access

An overview of behavioral, physiological,
and environmental sensors used in animal
biotelemetry and biologging studies
Malachi Whitford1,2 and A. Peter Klimley3*

Abstract
Background:  The ability to remotely monitor the behavior of animals and their interactions with their environment
has revolutionized how ecologists conduct studies. The creative use and placement of sensors on both biologging
and biotelemetric platforms can greatly expand the amount of information that can be garnered from ecological
studies.

Results:  Sophisticated transmitters and data loggers, which once were built by the biologists that used them, are
available off the shelf from many commercial manufacturers. The ability to purchase a wide variety of electronic tags
has allowed for a wider adoption of electronic tags across ecology, but has resulted in many biologists utilizing them
with little understanding of how they function. The purpose of this review is to provide a reader-friendly description
of the many sensors available to monitor the behavior, physiology, and environment of both terrestrial and aquatic
animals. Our approach here is firstly to describe the electrical and mechanical principles behind each type of sensor
and secondly to present one or two classic examples of how they have been used to provide insights into the biol-
ogy of species from a diversity of taxa. Behavioral sensors that record the speed, acceleration, tilt angle, and direction
of movement of an animal as well as its swimming depth or flight altitude will be described. Additional sensors are
mentioned that detect feeding and spawning behavior as well as the proximity to conspecifics, prey, and predators.
Physiological sensors will be described that monitor muscular, sensory, brain, gastric activity as well as body tempera-
ture, and sound production. Environmental sensors will be described that measure irradiance, dissolved oxygen, and
magnetic field intensity. It is our hope that this review serves as springboard for biologists to develop innovative ways
to learn more about their subjects using the myriad sensors that are available today, and the exciting new sensors to
be developed in the future.

Keywords:  Electronics, Sensors, Transmitters, Data loggers

Introduction
Ecologists  have  long  sought  an  understanding  of  the
behavior,  physiology,  and  environmental  conditions
experienced by animals as they move through and inter-
act  with  their  environment.  Due  to  the  technological

*Correspondence:  <apklimley@ucdavis.edu>
3 Department of Wildlife, Fish, and Conservation Biology, University
of California, Davis, One Shields Drive, Davis, CA 95616, USA
Full list of author information is available at the end of the article

advances  made  over  the  last  40  years,  many  different
methodologies have been generated to better understand
the  lives  of  animals  that  go  unnoticed  by  the  surveil-
lance  of  an  onsite  observer.  Broadly,  the  methods  used
to  monitor  animals  fall  under  the  umbrella  term  “biote-
lemetry”, which can be defined as the “remote measure-
ment  of  physiological,  behavioral  or  energetic  data”  [1].
It  is  now  common  place  to  incorporate  some  aspect  of
biotelemetry  into  any  study  involving  free-ranging  ani-
mals. The  degree  to  which  biotelemetry  is  implemented

© The Author(s) 2019. This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing,
adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and
the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material
in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material
is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the
permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit <http://creat> iveco
mmons .org/licen ses/by/4.0/. The Creative Commons Public Domain Dedication waiver (<http://creat> iveco mmons .org/publi cdoma in/
zero/1.0/) applies to the data made available in this article, unless otherwise stated in a credit line to the data.

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 2 of 24

in  studies,  however,  varies  greatly,  from  the  use  of  data
loggers, which must be retrieved to access stored data, to
acoustic-, radio-, and satellite transmitters that send their
information  to  either  land-based  receivers  (portable  or
stationary), or to a satellite circling the earth.

The  diversity  of  sensors  available  to  ecologists  has
grown  extensively  over  the  last  several  decades,  from
primitive thermistors included in the circuitry of the ear-
liest  radio  and  acoustic  transmitters  to  complex  multi-
axial  accelerometers  [2]  and  magnetometers  [3]  with
very  high  sampling  rates.  Although  sensors  are  increas-
ingly  accessible,  many  biologists  that  utilize  electronic
tags do not have a functional understanding of their basic
operating principles. We designed this review to provide
biologists with a clear and concise understanding of the
basic  operating  principles  employed  in  any  of  the  com-
monly  used  sensor  technologies.  We  recommend  that
biologists,  when  using  electronic  transmitters  and  data
loggers,  obtain  at  least  rudimentary  understanding  of
how sensors work in order to have full confidence in the
accuracy of the measurements they provide.

Deploying transmitters without fully grasping how they
work  can  lead  to  erroneous  results.  The  second  author
(APK)  witnessed  the  following  scenario.  The  position-
determinations  from  the  archival  tags  used  to  track  the
migration  of  tuna  appeared  inaccurate,  far  outside  the
range of where individuals of the species had been caught
in the past. Longitude and latitude were estimated by the
firmware of the tag based on the recordings of a built-in
photocell—the  photocell  measured  the  rise  and  fall  of
irradiance  levels  from  dawn  to  dusk  in  Universal  Time
allowing for an estimation of “apparent noon”, the time at
which the sun is at its zenith relative to when it is over-
head  of  Greenwich,  England.  This  was  used  to  provide
the longitude and latitude in a geolocation of the tuna.

Photocells  require  a  period  of  time  after  illumina-
tion to reach a stable level of conductance and the level
is dependent upon the prior state. The rate and amount
of change in conductance is dependent upon their prior
level of illumination, whether dark or light. This is com-
monly  called  “memory”  or  “light  history”  [4].  The  con-
ductance  of  a  cell  increases  slowly  when  previously  in
the  dark  condition  during  dawn  and  decreases  quickly
when previously in the light condition during dusk reach-
ing  different  stable  levels  of  conductance.  This  absence
of a strict correspondence of the resistance of the cell to
the  level  of  illumination  makes  it  an  imprecise  detector
of the timing of dawn and dusk. In the case of the afore-
mentioned  study  on  tuna  migrations,  this  ‘light  history’
phenomenon resulted an inaccurate estimation of appar-
ent  noon  as  well  as  daylength  that  resulted  in  an  inac-
curate  estimation  of  the  animals’  geolocation.  Replacing
the  photocells  with  photodiodes,  which  do  not  exhibit

a  “light  history”,  provided  more  accurate  geopositions.
Understanding  how  these  tags  function  is  therefore
important to choose the appropriate technology for study
questions.

Here, we will firstly describe a variety of different sen-
sors  and  discuss  the  basic  principles  that  allow  them  to
function. Secondly, we will provide brief examples in the
scientific  literature  as  to  how  they  have  been  used  thus
far. Our intentions are to: (1) increase the accessibility of
the  basic  principles  behind  sensor  functionality,  and  (2)
generate  a  basic  understanding  amongst  biologists  that
may help to further advance the application and innova-
tion of sensor technology. As part of our review, we will
identify  the  advantages  and  disadvantages  of  these  sen-
sors so that readers are aware of them. Due to the large
numbers of sensor technologies that have been developed
and their extensive applications, this review is not meant
be  an  exhaustive,  rather  this  review  is  meant  to  serve  a
springboard  for  biologists  less  familiar  with  the  basic
principles behind the most common sensor technologies.
The  variety  of  sensors  that  can  be  used  in  electronic
tagging  studies  is  extensive,  but  can  generally  be  sepa-
rated  into  three  general  types:  behavioral,  physiological,
and environmental. Our review will separate the sensors
into  these  three  categories.  However,  it  is  important  to
note  that  sensors  can  be  deployed  in  a  number  of  ways
and  are  not  necessarily  relegated  to  only  one  type  of
measurement. In other words, sensors tend to be versa-
tile, and many can be used to measure different compo-
nents of an animal’s ecology depending on how they are
deployed. For example, a thermistor can be used to meas-
ure body temperature if internally implanted into an ani-
mal as a physiological sensor, or air or water temperature
if attached externally to an organism as an environmental
sensor. Below we discuss, in turn, a variety of sensors that
are  readily  available  to  any  behaviorists,  physiologists,
ecologists, and conservation biologists.

Behavioral sensors
Speed and rate of movement

How do you measure the speed of a falcon making a dive
to capture prey or a blue marlin making a long-distance
migration? When measuring the rate of movement, it is
important  to  consider  the  difference  between  a  direct
measure  of  an  animal’s  locomotor  performance  through
its respective medium (such as air or water) and its rela-
tive  movement  over  ground.  For  both  measurements,
you  need  the  time  interval  between  measurements  and
the  distance  traveled;  however,  the  sampling  frequency
differs  depending  on  the  type  of  data  desired.  To  meas-
ure the diving speed of a falcon, the sampling rate would
need  be  relatively  high  (> 100  Hz),  while  the  sampling
rate  needed  to  assess  the  average  speed  of  marlin  on  a

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 3 of 24

long-distance migration would be relatively low and may
even  include  only  a  few  points  over  a  long  track.  High
sampling  rates,  however,  require  more  data  storage  and
are often not possible over long durations.

When  swimming  or  flying,  the  rate  of  movement  of
a  given  animal  is  a  product  of  both  the  animals  move-
ment  and  the  movement  of  the  medium  (air  or  water),
however,  several  studies  use  methods  to  parse  out  how
much  each  factor  contributes  to  the  overall  movement
of the animal. The two have been distinguished by using
vector  analysis  to  determine  the  distance  and  direction
of  the  movement  between  two  positions  by  subtracting
the  movement  due  to  passive  transport  in  the  medium
from the movement between two points on the ground.
A  good  example  of  this  was  the  demonstration  of  posi-
tive  and  negative  rheotaxis  by  migrating  green  sturgeon
[5]. Determining speed requires the use of a sensor that
detects locomotion relative to a medium, whereas rate of
movement is based on two position determinations sep-
arated  by  time.  These  positions  can  be  determined  by  a
variety of methods, but are mainly based on radar, GPS,
or ARGOS satellite positions.

The speed of locomotion for terrestrial species is essen-
tially a rate of movement as the animal walks or runs over
ground. The rate of straight-line movement can be deter-
mined  by  dividing  the  distance  between  two  points  on
the path of the animal by the time interval separating the
two position determinations. This methodology has been
widely  deployed  in  studies  on  animal  movement.  For
example, by using GPS collars and calculating the speed
of wolves using a sampling rate of ~ 2 fixes/h, it was found

that wolves reduced their average rate of movement dur-
ing  snowstorms  [6].  The  flight  speeds  of  birds  are  usu-
ally rates of movement based on position determinations
by  radar,  GPS,  or  the  ARGOS  satellites.  To  separate  the
contribution of wind to the movement of a bird, a simi-
lar type of vector analysis can be used as in aquatic spe-
cies to infer the flight speed. This approach was used to
study the migratory movements of savannah sparrows as
they passed three digital telemetry arrays [7]. The ground
speed of the sparrows was calculated by dividing the dis-
tance between telemetry stations by the time it took each
bird  to  be  detected  at  the  respective  stations. The  effect
of  wind  was  then  calculated  by  considering  both  meas-
ured wind speed and the difference between the angle the
bird traveled and direction of the wind. A vector analysis
similar  to  the  one  described  above  was  then  performed
to  parse  out  the  relative  contribution  of  wind  speed  to
flight duration and ground speed. For a recent review of
rates of movement related to allometric and phylogenetic
effects, see [8].

Swimming  speed  of  aquatic  animals  has  been  deter-
mined  using  either  of  two  electronic  components,  the
reed  switch  and  inductive  coil.  The  reed  switch  consists
of  two  moveable  metallic  leads  within  a  glass  ampule
(upper  left  in  Fig.  1).  The  two  leads  remain  apart  when
a  magnet  is  distant,  preventing  current  flow  through
the  switch;  the  two  leads  are  drawn  together  when  the
magnet  is  close,  permitting  current  to  flow  through  the
switch  (Fig.  2a).  The  closing  of  the  contacts  results  in  a
momentary  digital  pulse  (Fig.  2b).  The  inductive  coil
consists  of  a  coil  of  insulated  wire  (lower  left  in  Fig.  1).

Fig. 1  Two paddle wheel sensors used to record swimming speed. Pictures of a reed switch and coil (left) and a propellor and paddle wheel sensor
with these two components (right). Wheel with magnet in one paddle shown rotating toward the two sensors (center)

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 4 of 24

Fig. 2  Diagram of reed switch in open-circuit condition when
magnet is away (left) and closed-circuit condition when magnet is
adjacent (right) (a). A digital pulse in the output is produced when
the magnet passes the switch and closes the circuit (b)

Fig. 3  The passage of a magnet causing perpendicular movement of
charges in p-type semiconductor to create a peak in the Hall voltage
(adapted from [9])

When  a  magnet  passes  close  to  it,  a  pulse  of  current  of
varying  voltage  depending  upon  the  number  of  turns  in
the  coil  is  induced  within  a  circuit,  which  is  converted
to  a  digital  pulse.  The  reed  switch  or  inductive  coil  can
be  mounted  near  a  paddle  wheel  (lower  right  in  Fig.  1)
or  propeller  (upper  right  in  Fig.  1)  that  rotates  with  the
animal’s movement through an aquatic medium to meas-
ure swimming speed. A magnet is contained within one
of the paddles of the wheel or fin of the propeller (center
in  Fig.  1).  Every  time  the  magnet  moves  over  the  reed
switch, the circuit will be completed, and a digital pulse
of current will indicate one full propeller rotation. Simi-
larly, every time the magnet passes the inductor, a peak in
current  and  digital  pulse  will  be  induced  indicating  one
full rotation of the paddle wheel. The frequency of pulses
from both sensors can then be calibrated to the animal’s
swimming speed [9]. A good example of this approach is
the use of a magnet-equipped paddle wheel to determine
the swimming speed of the blue marlin [10].

Limb and jaw movements

Passing  a  magnet  near  a  semiconductor  has  been  used
to  provide  information  about  body  movements  of  many
animals.  When  a  magnetic  field  interacts  with  a  semi-
conductor, a Hall voltage (named after its inventor Edwin
Hall) is generated. A Hall voltage is generated due to the
magnet  field  causing  a  difference  in  charges  across  the

semiconductor  in  a  direction  perpendicular  to  current
flow through the semiconductor (Fig. 3) [11]. These sen-
sors  attached  externally  to  an  animal  and  paired  with
the  external  attachment  of  a  magnet  in  a  strategic  loca-
tion  can  provide  valuable  information  on  an  animal’s
body movements. This methodology was used to record
how the flipper strokes of Magellanic penguins (Sphenis-
cus  magellanicus)  change  with  diving  behavior  [12].  To
study penguin flipper movement, a magnet was attached
to the underside of the flipper and the Hall effect sensor
was attached to the body just ventral to the flipper. As a
result, each time a penguin moved its flipper, the proxim-
ity of the magnet to the sensor generated an increase in
the voltage potential, which was then used to determine
the position of the flipper relative to the sensor. Similarly,
Hall  sensors  have  been  successfully  utilized  to  monitor
the  jaw  movements  and  feeding  behavior  of  a  variety  of
species [13].

Body acceleration

There are three types of sensors used to measure acceler-
ation or change in speed. There are capacitive micro-elec-
tric–mechanical  systems  (MEMS),  piezocapacitive,  and
piezoelectric accelerometers [14]. MEMS accelerometers
are  particularly  good  at  recording  low-frequency  vibra-
tions,  motions,  and  steady-state  accelerations,  but  they
suffer  from  a  poor  signal  to  noise  ratio,  a  limited  band-
width,  and  are  mostly  restricted  to  smaller  acceleration

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 5 of 24

levels.  They  are  mainly  used  in  cellular  phones  and
mechanical  computer  drives  and  are  now  being  used  in
some  data  loggers  with  a  single  electronic  component
recording  both  magnetic  field  and  acceleration  in  three
axes. A detailed description of how MEMS sensors work
is provided in our discussion on magnetic field sensors.

Piezocapacitive accelerometers have a very wide band-
width  which  permits  the  detection  of  sudden  shock
events  such  as  the  crashing  of  a  car.  Piezoelectric  accel-
erometers are composed of a ceramic material, zirconate
titanate,  which  under  acceleration  produces  a  propor-
tional  electric  charge  or  output.  They  are  very  popular
and are available in a great number of different sensitivi-
ties, weights, sizes and shapes. These have been the most
commonly used acceleration sensors in data loggers and
transmitters.

It  is  imperative  to  first  understand  the  piezoelectric
effect  in  order  to  appreciate  how  these  sensors  of  accel-
eration, or change in speed, function. When mechanical
stress  is  applied  to  a  piezoelectric  material,  the  material
produces  an  electric  charge  proportional  to  the  amount
of  mechanical  stress  applied—the  direct  piezoelectric
effect  [15].  When  no  force  is  applied  to  a  material,  the
charges  in  the  electron  dipole  movements  cancel  each
other resulting in no voltage produced within the mate-
rial (Fig. 4a). When force is applied, for example by pres-
sure  exerted  by  the  finger,  the  shape  of  the  crystal  is
distorted  and  the  charges  no  longer  cancel  each  other

out,  resulting  in  more  positive  charges  on  one  side  and
more  negative  charges  on  the  other  (Fig.  4b).  The  pres-
sure results in the crystal generating a voltage. The piezo-
electric effect was discovered in 1880 [16].

An  accelerometer  can  be  used  to  record  an  animal’s
movements  as  well  as  its  behavior,  and  this  has  enabled
biologists  to  monitor  animals  without  having  to  rely  on
direct observation. A PZT rests on a small mass held in
place with a spring. Due to inertial forces, animal move-
ment  causes  the  small  weight  to  shift  and  move,  and
thus  places  differing  amounts  of  force  on  the  PZT.  The
amount of force on the ceramic PZT changes with each
movement,  and  this  change  in  force  generates  an  either
increasing  or  decreasing  charge,  or  voltage.  These  volt-
ages  can  be  converted  to  force  through  calibration.  As
force equals mass times acceleration, the acceleration of
the  animal  bearing  the  sensor  can  be  calculated  given
knowledge of the magnitude of the force and the mass in
the accelerometer. Again, as the accelerometer is moved,
the force the mass places on the PZT changes and results
in a charge proportional to the force applied by the mass.
The  force  the  mass  places  on  the  PZT  is  either  greater,
equal,  or  less  than  occurs  by  gravity  alone.  Think  of  a
mass  at  the  end  of  a  spring  in  contact  with  a  piezoelec-
tric  element  in  the  absence  of  movement.  If  the  mass  is
above  the  piezoelectric  with  its  force  directed  down-
ward, its magnitude will be equal to that of gravity, or 1
G (Fig. 5a). If the mass is below the element and its force

Fig. 4  A description of the piezoelectric effect. Charges are balanced in the crystal when no force is applied resulting in no voltage being induced
across the material (a). Charges become unbalanced when force is applied generating a voltage across the material (b) (figure is adapted from [15])

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 6 of 24

Fig. 5  The basic principles of an accelerometer when measuring
static acceleration. As the accelerometer is not moving (and is
static), gravity is the sole force acting on the transducer. As such,
the accelerometer readings represent the interaction between
downward gravitational force relative to accelerometer position.
These positions are upright, upside down, or perpendicular to the
force of gravity (a). The continuous change in static acceleration
is plotted over the 180° angles of the sensor including the three
positions shown above (b) (adapted from [19])

is in the upward direction, its magnitude will be equal to
the  negative  gravitational  force,  or  − 1  G.  If  the  mass  is
to  the  side,  there  will  be  no  gravitational  force  exerted,
or  0  G.  There  is  a  continuous  change  in  static  accelera-
tion  between  these  three  positions  where  the  mass  is  in
an upright position, perpendicular to the force of gravity,
or upside down (Fig. 5b). The basic accelerometer design
is limited in the information it can provide as it only pro-
vides measurements along a single axis of movement. To
overcome  this  limitation,  adding  additional  accelerom-
eters set orthogonal to one another can yield insights into
the 3-dimensional movements of animals. These are usu-
ally contained on data loggers, which can store large files
of  measurements  in  memory  that  can  be  downloaded
upon  retrieval.  Of  course,  there  are  trade-offs  between
the  temporal  resolution  at  which  measurements  are
made  and  the  active  life  of  the  data  logger  [17].  In  con-
trast  with  data  loggers,  transmitters  usually  transmit  a
summed  value  of  acceleration  over  a  given  time  period
that is a more general measure of overall activity due to
the limitation in data transmission.

In  animal  behavior  studies,  a  triaxial  accelerometer  is
commonly used and each accelerometer then describes a
different type of animal movement: surge, which consists
of  anteroposterior  movements,  heave,  which  indicates
dorsoventral  movements,  and  sway,  which  describes
lateral  movements  [18].  These  movements  are  tanta-
mount  to  changes  in  pitch,  yaw,  and  roll  well  known  to

Fig. 6  Typical placement of an accelerometer on a quadrupedal
vertebrate, in this case an anteater with the orientation of the
accelerometer axes to record surge, heave, and sway (adapted from
[18])

the  airplane  pilot.  The  typical  orientations  of  a  triaxial
accelerometer’s  axes  when  deployed  on  an  animal  are
illustrated on the tamandua, a small anteater (Tamandua
mexicana) (Fig. 6).

Static acceleration is easily interpretable. For example,
an  accelerometer  attached  to  the  back  of  a  quadrupedal
animal while standing will register 0 g in the surge direc-
tion  and  1  g  in  the  heave  direction  and  0  g  in  the  sway
directions. If the animal were to then lay down on its side,
as may occur with resting behavior, the sway accelerom-
eter  will  register  either  1  G  or  − 1  G,  depending  on  the
orientation  of  the  accelerometer  and  the  direction  that
animals lays down. At the same time, the surge and heave
accelerometer  would  register  0  g.  A  triaxial  accelerom-
eter was used to identify the body positions of a badger
(Meles meles) as it lay on its side or lay on its back [19].
While the badger was on its side, the mass was not press-
ing  against  the  ceramic  exerting  no  force  of  gravity  and
producing no voltage, giving a heave force of 0 G. While
the  badger  was  ventral  side  up,  gravity  was  pushing  the
mass  downward  and  away  from  the  PZT  to  produce  a
drop-in voltage corresponding to a heave force of − 1 G.
Triaxial accelerometers can be used to record the pos-
tural  changes  and  locomotory  movements  of  species.
An  overall  measure  of  the  forces  during  locomotion,
termed  overall  dynamic  body  acceleration  (ODBA),  is
calculated  by  summing  the  absolute  values  of  the  forces
measured on three orthogonal axes after the static meas-
urements  have  been  removed.  These  tri‐axial  acceler-
ometers  measure,  very  precisely  and  accurately,  every
dynamic change in body orientation and movement from
its  static  state.  This  enables  the  researcher  to  identify

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 7 of 24

fine-scale  behaviors,  activity  levels,  and  energy  output
[2].  For  example,  the  ODBA  has  been  used  to  study  the
differences  between  a  hopping  and  non-hopping  cane
toad  (Bufo  marinus)  [20].  The  CDBA  of  the  toad  was
close to a gravitational force of zero when sitting still but
when hopping the force alternated between a fraction of
1 G when on ground and 4 G when jumping. The mean
ODBA can be used to calculate the energy cost per unit
time for the cane toad.

Body tilt

A  mercury  switch  is  a  simple  dichotomous  switch
composed  of  a  hermetically  sealed  glass  chamber  that
contains  a  bead  of  conductive  mercury,  and  two  con-
necting  leads  that  penetrate  the  housing  near  one
another  but  do  not  connect  to  complete  a  circuit
(above in Fig. 7). When the sensor is rotated, the mer-
cury bead will move around the housing and by touch-
ing  both  electrical  leads  simultaneously  will  complete
a  circuit  depending  on  the  orientation  of  the  switch
(below  in  Fig.  7).  Through  the  appropriate  placement
of  a  mercury  tilt  switch,  this  simple  device  can  yield
valuable  insight  into  the  behavior  of  animals.  A  com-
mon  use  of  mercury  tilt  switches  in  animal  telemetry
is  to  use  the  dichotomous  nature  of  the  switch  to  dis-
cern  specific  behaviors  that  involve  a  stereotyped  pat-
tern of movement such as head lowering during feeding
bouts. For example, a mercury tilt switch was used in a
radio  transmitter  to  discern  feeding  by  golden  plovers
(Pluvialis  dominica)  [21].  The  switch  was  attached  to

Fig. 7  Diagram of mercury tilt sensors in open-circuit (above) and
closed-circuit conditions (below)

the neck of a plover. When the bird lowered its head to
feed, the conductive liquid mercury covered both leads,
completing  the  circuit  and  increasing  the  pulse  rate  of
the  transmitter.  When  the  bird  walked  with  its  head
upright or extended forward, the mercury covered only
one lead in the housing, resulting in an open circuit and
slow  pulse  rate.  The  number  of  pecks  per  minute  was
related to the number of pulses per minute using a lin-
ear regression. The number of pulses per minute could
then  be  used  to  identify  the  frequency  of  feeding  each
minute.

Flying height

Flying  altitude  is  recorded  using  an  altimeter  which
measures the vertical distance (parallel to the direction
of the gravity force) in relation to a reference level, typi-
cally, sea or ground. The classical barometric altimeter
contains  an  aneroid,  which  is  a  small,  partially  evacu-
ated  capsule  with  an  elastic  top  attached  to  a  pointer.
As air pressure changes, the elastic portion of the aner-
oid  will  expand  and  contract  and  cause  a  correspond-
ing change in the needle position. Modern aircraft have
a  knob  that  adjusts  the  device  to  a  sea-level  reference
pressure and the change in pressure is indicated by the
rotation  of  a  needle  in  a  small  Kollsman  window  on  a
gauge, which is calibrated to provide altitude. A 1-mbar
decrease  in  air  pressure  is  equivalent  to  an  8.23  m
increase  in  height  above  sea  level  [22].  The  problem
with  this  and  other  conventional  altitude-measuring
technologies  is  the  difficulty  in  measuring  ultra-low
pressures, where there is a lack of resolution and accu-
racy  in  the  absolute  pressure  sensing  elements.  Fur-
thermore,  the  sensors  take  up  considerable  space,  and
for  this  reason,  it  is  impractical  to  use  them  in  minia-
ture electronic tags.

For  the  reasons  mentioned  above,  the  altimeters  that
show the greatest for data loggers and transmitters utilize
MEMS. This altimeter consists of a small silicon element
deposited  on  a  substrate  that  changes  in  its  capacitance
with  an  increase  or  decrease  in  altitude  (Fig.  8b).  The
sensor is interfaced with an amplification circuit and an
analog-to-digital converter. The sensor itself is very small,
6  mm  in  diameter  and  1.7  mm  high  with  a  small  cur-
rent  consumption  of  0.5–50  µA  and  a  supply  voltage  of
3–5 V. For a comprehensive description of the design of
this MEMS sensor and testing of its accuracy, see the fol-
lowing Ref. [25]. Altimeters are often integrated into GPS
tags placed on birds. A discussion of altimeters is availa-
ble in this review of tracking birds [26] and two examples
of  their  use  by  researchers  are  to  describe  the  soaring
modes in eagles [27] and to understand how ospreys use
thermal uplift when migrating over the open seas [28].

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 8 of 24

metal  is  stretched  or  compressed,  it  becomes  longer  or
shorter  resulting  in  a  change  of  its  electrical  resistance
to current. If the compression is less than in its original
state, the strip will elongate and become thinner (middle
left  in  Fig.  9a),  and  its  resistance  increases.  If  the  com-
pression  is  greater  than  in  its  original  state,  it  becomes
shorter  and  widens  (bottom  left  on  Fig.  9a).  The  strip
can be used to measure pressure if the stresses are kept
within  the  elastic  limit  of  the  metal  so  that  it  does  not
become  permanently  deformed.  When  stretched,  the
overall  resistance  of  the  gauge  is  greater,  and  less  cur-
rent will flow through the gauge relative to a given volt-
age.  When  compressed,  more  current  will  flow  through
the gauge given the same voltage. The typical strain gauge
has a small resistance range of 30 ohms under maximum
pressure to 3000 ohms under minimum pressure. Forces
producing a resistance range beyond the capacity of the
strain  gauge  would  permanently  damage  the  metallic
strips themselves, thus ruining the sensor.

A Wheatstone bridge circuit is needed to measure such
extremely small changes in resistance with high accuracy.
With no force applied to the carrier, both strain gauges,
R #1 and R #2, have equivalent resistances and the bridge
is  balanced  (upper  right  in  Fig.  9b).  In  contrast,  when  a
downward  force  is  exerted  on  the  free  end  of  the  car-
rier,  it  will  flex  downward  stretching  gauge  R  #1  and
compressing  gauge  R  #2  at  the  same  time,  producing  a
change in resistance (lower right in Fig. 9b). Complemen-
tary  pairs  of  strain  gauges  can  be  bonded  to  the  carrier,
including R #3 and R #4, producing even greater sensitiv-
ity. This latter arrangement is called a full-bridge circuit.

A strain gauge has previously been used to record the
depth  of  ‘yo-yo’  dives  by  scalloped  hammerhead  sharks
during their highly oriented nighttime movements of up
to  20  km  away  from  a  seamount  to  feed  in  the  pelagic
environment [29]. The sensor consisted of a thin copper
wire  wound  around  four  posts  in  a  full-bridge  circuit,
which  was  enclosed  within  a  miniature  puck-shaped
stainless-steel  capsule  (middle  in  Fig.  9b).  Above  the
strain  gauge  was  a  thermistor  embedded  in  clear  epoxy,
which provided simultaneous measurements of tempera-
ture during the dives. Similarly, the whale shark exhibits
four dive patterns [30], but they most often dive in a pat-
tern that resembles the up and down movement of a ‘yo-
yo’, characteristic of many oceanic species. During these
dives  they  stay  only  briefly  at  the  greatest  depth.  How-
ever,  at  other  times  they  make  ‘bottom  bounce’  dives,
during which they swim up and down along the bottom
or “U-dives” where they stay at a single depth for longer
periods of time in deeper water.

Each  strain  gauge  has  a  pressure  range  to  which  it
responds.  For  that  reason,  biologist  needs  to  specify  to
the  manufacturer  the  depth  range  over  which  the  fish,

Fig. 8  The piezoelectric depth sensor consists of a pressure port,
a summing member, which exerts force on a quartz crystal (a) [23].
Digital pressure sensor used to determine barometric pressure and
altitude (b) [24]

Swimming depth

An  animal’s  underwater  depth  has  usually  been  meas-
ured  using  a  piezoelectric  strain  gauge.  A  piezoelectric
depth gauge operates by the same principles as an accel-
erometer, but with minor alterations in the way that pres-
sure  is  applied.  The  piezoelectric  material  is  positioned
inside a housing, which is either cylindrical or rectangu-
lar, and one end of the housing is composed of a pliable
diaphragm  (Fig.  8a).  Due  to  the  increasing  pressures  at
greater depths in the ocean, the diaphragm exerts greater
pressure  on  a  force  summing  member  that  transmits
pressure on to the piezoelectric material. Then, due to the
piezoelectric effect (explained earlier), an electric charge
is formed that is proportional to the amount of pressure
imposed on the piezoelectric material by the diaphragm.
The  strain  gauge  consists  of  a  pattern  of  strain-sensi-
tive,  metallic  foil  that  is  conductive  and  deposited  on  a
flexible backing material, that is not conductive, called a
carrier  (upper  right  in  Fig.  9a).  As  a  strip  of  conductive

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 9 of 24

Fig. 9  The strain gauge consists of a transducer, consisting of an element that changes resistance based on the force of pressure (a). A force is
applied to the carrier that causes the Wheatstone bridge to become unbalanced (bottom right in b). The resistance in strain gauge #1 increases
and in gauge #2 decreases (bottom left in b), and this results in a small resistance change. Shown in center is strain gauge transducer, consisting
of four inner posts with coiled wire around them that change the resistance in a full Wheatstone bridge circuit based on the compression of the
stainless-steel capsule

shark,  or  marine  mammal  dives.  The  manufacturer  will
equip  the  tag  with  a  strain  gauge  sensitive  over  that
range of depths. Each atmosphere of pressure, based on
that  pressure  measured  at  sea  level,  exerts  14.7  lb  per
square  inch  (psi).  The  pressure  under  water  increments
one atmosphere for every 10 m increase in depth. If the
subject  of  the  study  descends  to  a  depth  of  1000  m,  the
manufacturer  would  equip  your  tag  with  a  strain  gauge
sensitive to a range of pressures from zero to 161.7 psi—
the amount of surface pressure plus ten additional atmos-
pheres  of  pressure.  The  output  from  the  Wheatstone
bridge is usually converted to a digital signal, and that is
done with an analog-to-digital converter. These are most
often  8-bit  converters,  dividing  the  range  of  pressures
(depths) by 256 increments. In this case, the resolution of
the depth gauge can be calculated by dividing the range
of  1000  m  by  256  to  get  a  3.9-m  depth  resolution.  The
challenge  to  the  biologist  with  an  imperfect  knowledge
of the diving ability of a subject is to provide the manu-
facturer with an inclusive range yet having it is narrow as
possible  to  maximize  the  resolution  of  the  tag;  in  other
words, there is a trade-off between resolution and assur-
ance  that  the  sensor  will  not  be  destroyed  by  exceeding
its  maximum  depth  range  Analog-to-digital  converters

do exist that are 10-bit, dividing the depth range by 1024
divisions and providing a resolution of 1.0 m for the same
depth  range.  A  smaller  range  can  be  chosen  for  a  spe-
cies confined to relatively shallow water of the continen-
tal shelf than a species inhabiting the deep ocean basins,
where the subject might dive to depths exceeding 1000 as
is the case for many pelagic species.

Swimming direction

Monitoring  the  bearing  or  direction  of  motion  of  an
animal  movement  can  be  highly  informative,  as  it  can
elucidate  the  various  ways  that  animals  move  through,
interact, and navigate their environment. The most basic
bearing  detector  is  a  light-based  sensor  composed  of
three  parts:  a  light  emitter  array,  a  compass  wheel  with
magnet,  and  a  light  detector  array.  These  three  compo-
nents  are  then  positioned  within  a  housing,  one  on  top
of  the  other  in  the  order  mentioned  (Fig.  10a).  In  other
words,  a  compass  wheel  that  orients  to  magnetic  north
is  mounted  between  the  light  emitter  array  below  and
the light detector array above—both of which are fixed in
place.

This  sensor  includes  two  pairs  of  light  emitters  and
detectors  positioned  offset  from  each  other  90°  on

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 10 of 24

the  degree  of  opaqueness  in  the  compass  wheel.  As  the
compass wheel rotates, the amount of light reaching the
detector will change as more or less light passes through
the  disk  as  the  LED–photocell  pairs  move,  but  the  disk
with  the  transmission  gradients  with  a  magnet  attached
remains  oriented  toward  the  north.  Therefore,  the  light
measured  by  the  light  detector  will  correspond  to  posi-
tion on the wheel, and, as a result, will provide informa-
tion on the animal’s bearing.

Two  pairs  of  light  emitters  and  detectors  are  used  to
correct for the location on the compass wheel where the
most opaque and most transparent sections in the wheel
meet.  There  is  confusion  when  the  light  from  a  LED–
photocell  pair  passes  over  the  boundary  between  maxi-
mum to minimum transmission because it records over a
short distance the same values of transmission recorded
elsewhere on the circular gradient (Fig. 10c). However, at
the  same  time  the  second  LED  gives  the  true  direction.
This principle can be illustrated based on the calibration
of  a  transmitter.  The  transmitter  is  placed  on  a  surface
with a compass rose with a strong magnet positioned in
the north direction. The transmitter is then rotated along
with  the  two  LED–photocell  pairs  fixed  in  place  in  the
endcap  of  the  transmitter  while  the  disk  with  the  trans-
mitter  gradient  stays  oriented  toward  north.  The  resist-
ances  of  the  two  photocells,  displaced  90°,  are  shown  in
a  radial  plot  covering  360°.  The  resistances  of  sensor  #1
are  denoted  by  solid  circles  and  those  of  sensor  #2  are
indicated by clear circles. Note that between 60° and 90°,
the  resistances  measured  by  sensor  #1  decrease  rapidly
as  the  LED  passes  over  the  abrupt  change  in  the  gradi-
ent (see blue arrows in Fig. 10c). At this time, the sensor
# 2  provides  the  true  bearing  of  the  swimming  animal.
The resistance of sensor #2 changes rapidly from 150° to
180° (see red arrows in Fig. 10c), and at this time sensor
# 1 provides the true compass direction of the swimming
animal. The sensor is shown in Fig. 10a with the follow-
ing:  (1)  the  magnet  attached  to  the  pivot  and  permitted
to  rotate  between  the  lower  and  middle  extensions  of
the  endcap;  (2)  the  LEDs  mounted  in  holes  in  the  mid-
dle extension; (3) the disk with the transparency gradient
between the middle and top extension, and (4) the photo-
cells on the top of the top extension. The gradient bearing
sensor  is  far  more  accurate  than  another  direction  sen-
sor using the optical principle, the wedge-removed bear-
ing sensor, because it provides higher resolution bearing
measurements. This  type  of  sensor  was  used  to  demon-
strate that a hammerhead shark swam in a highly direc-
tional  manner  as  they  swam  over  a  distance  of  20  km
from  a  seamount  to  its  pelagic  feeding  grounds  and
returned to the seamount on the following day [29].

In the future, an animal’s swimming or flight headings
may  be  recorded  using  magnetic-field  sensing,  MEMS

Fig. 10  Explanation of the light gradient sensor. The most basic
bearing sensor design is composed of three parts: a light emitter
array, a compass wheel with magnet, and a light detector array (a).
A transparency gradient on a disk of negative film shown with the
boundary between the most transparent and least transparent
wedge (b). The resistance of the two photoresistors are plotted
over a directional rose of 360°, with the blue arrows indicating the
ambiguity zone for sensor #1 and red arrows denoting the ambiguity
zone for sensor #2 (c). The sensor is shown without its opaque
coating to keep out external light. One must be careful to cover the
sensor with multiple coasts of a dark epoxy paint and to measure
resistances when the room light are off and on to make sure no
external light enters the sensor

the  compass  wheel  carrying  a  disk  with  a  transmis-
sion  gradient  (Fig.  10a).  This  is  usually  created  from  a
film  negative  exposed  for  increasing  times  to  produce  a
radial transmission gradient (Fig. 10b). The sensor oper-
ates  by  detecting  differences  in  light  that  correspond  to

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 11 of 24

sensor. The direction of movement can be recorded using
a three-axis magnetometer to identify the earth’s dipolar
field  and  successive  measurements  of  acceleration  with
a  3-axis  accelerometer. The  operation  of  the  former  will
be  explained  when  describing  environmental  sensors.
The  Xtrinsic  MAG3110  3-axis  magnetometer  is  only
2  mm × 2  mm × 0.85  mm  and  can  be  interfaced  with  a
similarly  small  3-axis  accelerometer.  Most  automobiles
are  now  equipped  with  this  technology  and  display  the
direction the car is being driven on the instrument panel.
Since  a  propellor  or  paddle  wheel  is  not  necessary  for
sensor operation, it is likely this technology will be used
not  only  to  monitor  movement  in  water  but  also  in  air.
Hence,  it  would  provide  information  on  the  speed  and
direction ambulatory movements of terrestrial animals as
well as the flight of birds.

Predation

To  understand  the  ecology  of  an  animal,  it  is  important
to understand when and how it forages; predation events,
though ubiquitous, are rarely observed, but sensor tech-
nologies can allow remote “observation” of when an ani-
mal consumes a prey item. The ingestion of prey has been
recorded by a sensor that consists of a pair of electrodes
that  are  covered  with  a  non-conductive  polymer.  The
tag is attached externally to the prey. Once the predator
ingests  prey,  and  it  lies  within  predator’s  stomach,  the
rising  acidity  within  the  stomach  either  (1)  changes  the
magnetic properties of the polymer, which is detected by
the microprocessor in the tag on the prey, or (2) dissolves
the  polymer  and  consequently  permits  current  to  flow
between  the  liquid  and  electrodes  (pers.  commun,  Dale
Webber, VEMCO Ltd.). This triggers a change in the tag’s
acoustic  transmission  that  indicates  predation.  Another
approach to determining when feeding events occur is to
measure  the  bulk  electrical  impedance  measured  across
two  electrodes  [31].  A  prototype  data  logger  was  used
to  record  changes  in  impedance  inside  the  stomachs  of
captive  free-swimming  tiger  and  sandbar  sharks  while
feeding  in  the  natural  environment.  Feeding  and  diges-
tion events produced characteristic changes in electrical
impedance of the stomach contents. These were recorded
in  five  successive  phases:  (1)  an  empty  stomach  (pre-
ingestion), (2) ingestion, (3) a chemical ‘lag’ period, (4) a
mechanical  ‘chyme’  period,  and  (5)  stomach  evacuation.
The  duration  of  the  chyme  phase  was  positively  related
to meal size. A significant positive regression was found
between the duration of the chyme phase and meal size
both  for  the  tiger  and  sandbar  sharks.  A  third  approach
has  been  to  place  an  ultrasonic  receiver  on  an  animal
such  as  an  elephant  seal,  which  can  detect  the  signal  of
a  transmitter  attached  to  prey  [32].  This  technique  only
provides an inference that predation may have occurred,

when in reality the detection of a signal indicates a tagged
animal is in the proximity of the predator. Receivers were
placed  on  ten  elephant  seals  and  retrieved  over  periods
up to 6 months when they returned to the colony to molt.
The  files  downloaded  from  the  receivers  recorded  the
signals  of  several  potential  prey,  one  chinook  salmon,  a
lingcod, a steelhead trout, and a black rockfish. However,
this sensor also detected potential predators of the north-
ern elephant seal. Four of the ten elephant seals detected
great white sharks.

Spawning

Due  to  the  infrequency  and  short  duration  of  repro-
ductive  bouts  in  many  species,  the  use  of  sensory  tech-
nologies  can  greatly  expand  our  understanding  of
reproductive  biology.  A  spawning  tag  is  currently  under
development  that  consists  of  paired  internal  and  exter-
nal  transmitters.  The  unit  is  deployed  by  injecting  a
small  acoustic  beacon  that  continually  pulses  into  the
oviduct  of  an  adult  egg-laying  female  fish.  Attached  to
the  fish  is  an  externally  harnessed  pop-up  satellite  tag
(PSAT)  which  includes  an  acoustic  receiver.  When  the
fish  spawns,  the  acoustic  beacon  is  ejected  along  with
the eggs that compose the spawn. As the fish swims away
from the site of spawning, the beacon’s signal is no longer
detected.  The  consistent  absence  of  detection  of  the
beacon  by  the  satellite  tag  indicates  that  the  beacon  has
been  permanently  ejected  and  that  spawning  has  likely
occurred. The PSAT release mechanism is then activated,
allowing the PSAT to float to the surface where it down-
loads  information  to  the  ARGOS  satellite  constellation.
The  location  and  timing  of  a  spawning  event  is  deter-
mined by when and where the tag rises to the surface and
its subsequent detection by an ARGOS satellite. The tag
also transmits a data packet, including information about
behavior, such as swimming speed and depth, as well as
properties of the environment, such as the water temper-
ature associated with the spawning event [33].

Sociality

Animal aggregations can occur for many reasons (repro-
duction,  feeding,  defense,  etc.),  but  understanding  the
complex  relationships  between  animals  in  close  prox-
imity  to  one  another  is  difficult,  particularly  in  spe-
cies  where  individual  identity  cannot  be  discerned  from
external  morphology  and  coloration.  Social  interactions
can  be  studied  through  the  use  of  proximity  sensors.
One  form  of  proximity  sensor  consists  of  a  receiver  that
can  quickly  decode  the  identity  of  multiple  signals.  In
the  marine  environment,  the  receivers  have  either  been
stationary,  as  first  used  in  this  environment  to  identify
interactions  among  white  sharks  when  feeding  at  a  par-
ticular  site,  like  would  occur  when  feeding  on  seals  at  a

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 12 of 24

seal colony [34, 35] and later to study the social interac-
tions  among  lemon  sharks  in  a  lagoon  [36].  Receivers
attached  to  elephant  seals  have  been  successfully  used
to not only detect potential prey and predators, but also
conspecifics  [32].  Two  of  the  eight  elephant  seals  carry-
ing  receivers  detected  other  tagged  elephant  seals.  The
receiver placed on the elephant seals was bulky, a smaller
tag,  the  “Business  Card”  tag  has  been  manufactured  by
Vemco  Ltd.  (Halifax,  Canada).  The  business  card  tag
cycles  between  transmitting  its  unique  code  and  listen-
ing  for  additional  coded  signals  on  other  individuals.
They  can  thus  be  detected  by  a  stationary  receiver,  and
the  identities  of  those  other  tags  encountered  with  the
times of the interactions can be downloaded from the tag
if recovered. For a description of how business card tags
have  been  used  to  study  Galapagos  sharks,  see  Ref.  [37]
and the associated website (<http://www.himb.hawai> i.edu/
ReefP redat or/Busin ess%20Car d%20Tag .html)  provides  a
detailed description. Given the added capability of trans-
mitting  the  detections  stored  in  the  business  card  tags
to  either  a  receiver  or  a  second  business  card  tag,  this
mobile  peer-to-peer  technology  (MP2B)  has  the  prom-
ise of determining how long tagged individuals remain in
schools, how often they encounter tagged predators, and
when mating occurs between tagged individuals.

Proximity  sensors,  however,  have  also  been  used  in
the terrestrial environment. Passive integrated transmit-
ters (PIT) have been used to detect the degree of social-
ity or territoriality at hummingbird feeding stations [38].
More  sophisticated  proximity  recording  systems  are
composed  of  low-power  radio  transmitters  and  receiv-
ers  on  animals,  which  are  capable  of  detecting  nearby
loggers—making  up  Wireless  Sensor  Network  (WSN).
They  operate  on  an  ultra-high  frequency  (UHF)  from
300  MHz  to  3  GHz.  These  can  either  be  a  data  logger,
deployed upon animals with the detection files retrieved
upon  capture  or  as  telemetric  units  that  download  their
files via a modem or a network of stand-alone receivers.
More recently, these units have been able to provide the
locations of interactions via the integration of GPS units
[39].  This  is  particularly  valuable  with  mobile  animals,
which may move outside an array of proximity detectors.
These animal-borne proximity detectors have been used
to  examine,  intra-specific  relationships  [40],  social  sys-
tems [41], and contact rate and associated disease trans-
mission [42].

Physiological sensors
Brain, muscular, or heart activity

The activity of an organ can be recorded by inserting two
electrodes  into  different  body  parts  and  recording  the
voltage. The oscillations of voltage over time are recorded
as  an  electrogram,  which  can  be  converted  to  a  digital

signal  and  stored  within  the  memory  of  an  electronic
tag.  Electrograms  have  been  used  to  identify  the  olfac-
tory  responses  of  lemon  sharks  (Negaprion  brevirostris)
to different chemicals [43]. In this case, the signals were
displayed on an oscilloscope but could be stored within a
tag. This example is presented, as it illustrates the holistic
potential  of  electrograms  in  describing  the  responsive-
ness of animals to an environmental stimulus, despite the
measurements having not been stored within a tag. Elec-
trodes  were  implanted  within  the  olfactory  bulb,  which
receives  input  from  the  efferent  nerves  leading  away
from  nasal  capsule  (see  positions  1  and  2  in  Fig.  11b).
The changing voltage over time was expressed as an elec-
troencephalogram  (EEG),  recording  the  brain’s  electrical
activity to the chemical stimulation of the nares. In addi-
tion, an EEG was also recorded from electrodes inserted
into the medulla (see positions 3 and 4 in Fig. 11b), which
controls  gill  movements,  to  determine  whether  they
open  or  close  upon  detecting  the  chemical.  Finally,  an
electromyogram  (EMG)  was  obtained  by  inserting  elec-
trodes into myomeres in the tail muscle (see positions 5
and  6  in  Fig.  11a).  Briefly,  an  EMG  measures  the  motor
unit action potential, which is the summation of the indi-
vidual action potentials from each muscle fiber within a
motor  unit  generated  during  a  muscle  contraction  rela-
tive  to  a  reference  electrode.  The  line  in  the  upper  left

Fig. 11  Electrical activity of brain and muscle. Illustration of
placement of electrodes in tail muscle to record electromyogram
(EMG) (a) and in the olfactory bulb and medulla to record
electroencephalogram (EEG) (b). Waveforms indicating the activity of
the gills, olfactory bulb, and tail muscle (c) (adapted from [43])

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 13 of 24

corner of Fig. 11c shows the amount of time glycine took
to spread throughout the tank. The positive and negative
excursions of waveform of the olfactory organ increased
tenfold (middle trace in Fig. 11c), showing that the shark
detected  the  chemical  stimulus.  The  small  truncated
square  wave  in  the  top  waveform  recorded  from  the
medulla indicated that the shark abruptly closed its gills
to  become  streamlined  before  dashing  forward  toward
the  chemical  source  (top  trace  in  Fig.  11c).  Finally,  the
powerful tail beat associated with the acceleration of the
shark  is  indicated  by  the  large  excursion  in  the  poten-
tial  recorded  on  the  electromyogram  (bottom  trace  in
Fig. 11c).

The ability to record muscle contractions via EMG, has
been  commonly  used  in  studies  of  fishes  since  this  pio-
neering laboratory study. For example, the energetic cost
of swimming when experiencing variations in water cur-
rent  speeds  has  been  measured  for  rainbow  trout.  Tail
beat  frequencies  and  oxygen  consumptions  for  different
flow  speeds  were  determined  in  a  Brett-type  respirom-
eter  [44].  This  permitted  the  recording  of  swimming
speeds  and  oxygen  consumption  rates  of  rainbow  trout
(Oncorhynchus  mykiss)  after  being  released  into  a  river,
and as they experienced changes in current speed result-
ing from water being released from a nearby dam. Swim-
ming speed and oxygen consumption were both found to
increase  in  accordance  with  the  speed  of  the  river  cur-
rent;  however,  when  the  current  speed  was  at  its  peak,
swimming  speed  and  oxygen  consumption  decreased.  It
is likely that the trout sought out and remained in eddies
behind rocks within the river when the speed of current
was  at  its  peak.  In  terrestrial  system,  a  notable  use  of
EMG  has  been  the  remote  study  of  mastication.  A  cus-
tom  radio-telemetry  based  animal-borne  EMG  system
was  used  to  observe  the  chewing  behavior  of  free-rang-
ing  howler  monkeys  (Alouatta  palliate).  Several  elec-
trodes were implanted in the jaw musculature as well as a
ground electrode implanted into the muscles on the back.
The transmitter/EMG unit was then glued to the back of
the animal. Although technological issues did occur, they
were able to successfully use EMG to monitor the mon-
keys’ feeding behavior [45].

The use of electrocardiograms (ECG or EKG) to moni-
tor  the  heart  rate  of  free-ranging  animals  has  been
around for several decades [43], but has been used infre-
quently  within  transmitters  and  data  loggers.  The  prin-
ciples  behind  ECG  are  similar  to  EMG,  however,  ECG
records  the  constant  depolarization  and  repolarization
patterns associated with a heartbeat. The depolarizations
of the heart muscles send electrical potentials that prop-
agate  through  bodily  tissues.  The  waveform  expresses
the  activity  of  the  heart  over  time.  An  ECG  sensor  in  a
radio  transmitter  was  used  to  study  heart  rate  and  its

behavioral correlates in the American alligator (Alligator
mississippiensis). For years it was believed that all croco-
diles and alligators experience bradycardia (slowed heart
rate) while submerged, however, it had not been empiri-
cally  shown.  To  test  this  notion,  researchers  sutured
radio transmitters the scutes of alligators and implanted
ECG  electrodes  within  [46].  Unexpectedly,  bradycardia
was  detected  when  canoists  approached  the  alligators
close enough to track them, whereas their long submer-
gence  times  did  not  elicit  bradycardia.  That  said,  the
heart  rate  of  southern  elephant  seals  (Mirounga  angu-
stirostris), however, does slow while they make repeated
‘yo-yo’ dives in the open ocean [47]. Note that the nega-
tive excursions in heart rate slow to roughly 20 beats/min
while  they  are  swimming  at  depths  of  500–600  m. They
stop  swimming  once  they  reach  the  surface,  to  breath.
Their swimming speed varies between 1 and 2 ms−1 dur-
ing their repeated dives.

Gastric activity

The digestion of prey within the stomach can be inferred
by  recording  an  increase  in  acidity,  as  enzymes  are
released to aid in digestion. A measure of acidity, which
aids in digestion within the stomach, is pH. pH is a meas-
ure of the hydrogen ion concentration within a solution.
The  concentrations  of   H+  vary  greatly  from  10  to   10−15
molar (M). For that reason, concentrations are expressed
on  a  logarithmic  scale.  The  pH  is  defined  as  minus  the
logarithmic base 10 of  H+, or the following:

pH = − log[H+].

It is expressed in a scale that ranges from 0 to 14. Aque-
ous  solution  with  a  pH  less  than  seven  are  acidic,  while
solutions with a pH greater than seven are alkaline. A pH
of  seven  is  neutral  indicating  that  the  concentration  of
 H3O+ ions is equal to that of  OH− ions.

Studies monitoring the internal pH of animals are rare.
However,  pH  sensors  have  been  developed  for  use  with
data  loggers  and  acoustic  transmitters  to  record  gastric
acidity  in  free-ranging  animals  [48,  49].  The  pH  sensor
measures  the  external  concentration  of  hydrogen  ions
based on an internal reference concentration. The device
on the data logger consists of an inner glass tube with a
filling solution of a constant pH of seven enclosed within
an outer plastic tube containing a solution saturated with
potassium chloride to serve as a reference (Fig. 12b) [50].
The distal end of the glass tube extends out of the plas-
tic enclosure and is exposed to the external environment.
One electrode made of silver wire coated with silver chlo-
ride  is  contained  within  the  outer  chamber  immersed
within  the  reference  solution;  another  electrode  is
enclosed within the inner chamber immersed in the fill-
ing  solution.  Hydrogen  ions  from  the  external  aqueous

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 14 of 24

A  data  logger  with  this  sensor  (Fig.  12b)  was  inserted
into  the  stomach  of  penguins  (Spheniscus  magellanicus)
to  detect  their  feeding  behaviors  while  at  sea  [48].  The
data logger recorded pH and temperature within the pen-
guin’s  stomach.  The  penguin  left  its  nest  at  0300  hours
and returned at 2300 hours. There were four large nega-
tive  excursions  in  the  temperature  record  between  0600
and  0800  hours  when  the  penguin  consumed  cold-bod-
ied  fish  and  two  less  extensive  negative  excursions  later
between 1100 and 1200 hours when additional fish were
consumed,  but  the  temperature  decreases  were  less
because  the  stomach  was  full  of  fish.  Corresponding  to
these negative excursions in the temperature record were
positive  excursions  in  the  pH  record  as  the  acids  were
neutralized during the digestion of the prey. As the stom-
ach  became  full,  the  temperature  of  the  stomach  slowly
decreased  whereas  the  pH  of  the  stomach  slowly  rose.
Once  the  prey  items  were  digested,  the  penguin’s  stom-
ach temperature rose slowly and the pH dropped slowly
to  the  levels  present  before  prey  consumption.  Later
in  the  year,  changes  in  stomach  acidity  were  recorded
when  penguins  were  rearing  of  chicks.  Adult  penguins
that  were  incubating  eggs  had  a  relatively  constant  pH,
whereas the pH within the stomachs of penguins rearing
young increased, likely to inhibit the digestion of the fish
they had captured at sea. This elevation in pH is consist-
ent  with  the  parent’s  goal  of  providing  their  young  with
the largest meal possible when regurgitating the contents
of their stomach upon reaching the nest. The gastric pH
has  been  recorded  for  blacktip  sharks  carrying  acoustic
transmitters  inserted  into  the  stomach  as  well  as  stom-
ach  temperature  [49].  Feeding  events  were  detected  by
periodic elevations of the pH upon feeding captive sharks
food  items.  Meal  size  could  be  determined  based  on  a
regression  of  known  meal  sizes  and  areas  in  the  eleva-
tion of the curves of pH as a function of known meal size.
Hence, it would be possible to determine the meal sizes
of free-swimming sharks.

Reproductive hormonal activity and stress response

Many  physiological  states  can  be  determined  from  the
analysis  of  blood  samples.  For  example,  male  reproduc-
tive  condition  in  sharks  can  be  determined  based  on
concentrations  of  testosterone  and  dihydrotestosterone
[51];  female  reproductive  state  can  be  determined  from
changing levels of estradiol, progesterone, and testoster-
one [52]. High stress is indicated by high levels of corti-
sol,  catecholamines,  and  lactate  as  well  as  low  levels  of
glucose. There is currently available a miniaturized blood
sampler produced by Little Leonard of Tokyo, Japan [53].
It  is  designed  for  use  with  marine  mammals.  It  consists
of six modules, each consisting of a syringe that removes
either  blood  from  a  vein  or  artery  or  interstitial  fluids

Fig. 12  Plastic tube with a reference solution of saturated potassium
chloride with an enclosed glass tube with a solution that increases
in pH upon diffusion of hydrogen ions into the tube from the
external aquatic environment. Electrodes record the electric potential
between the two solutions (a) (adapted from [48]). A pH sensor
used to record gastric pH and temperature within the stomachs of
foraging emperor penguins (b) (taken from [48])

environment diffuse into the glass tube through the per-
meable distal end and increase the electric potential. The
more  hydrogen  ions  that  diffuse  into  the  glass  tube,  the
higher the electric potential and lower the pH. The volt-
age measured between the two electrodes is processed to
produce a pH value of the solution.

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 15 of 24

from the surrounding tissues and a sampler to store the
fluids  (Fig.  13a).  The  samplers  are  fastened  to  a  plate
with  an  electronic  controller,  and  this  plate  is  attached
to  the  skin  of  a  large  marine  mammal  such  as  a  seal  or
whale (Fig. 13b). The device can be programmed to draw
blood with a syringe at specific intervals. Chemical sen-
sors  for  glucose  and  lactate,  which  are  on  the  market
already, need only very small amounts of media for accu-
rate  measurements  of  concentrations.  In  many  cases,  it
may be better to sample interstitial fluid from the tissue
under the skin rather than blood from a capillary, as the
interstitial fluid is less viscous than blood, which makes it
easier to handle within the syringe, and it is not necessary
to treat interstitial fluids with heparins, as is needed with
blood  to  prevent  coagulation  during  storage.  The  chal-
lenge to this technology is to reduce the size of this data
logger  so  that  it  can  be  used  with  smaller  bony  fishes,
sharks, and rays. However, there is a strong motivation to
do so because there is keen interest among physiologists

in  monitoring  the  physiological  responses  of  animals  to
their  social  and  physical  environments  in  their  natural
environment as has been done in the laboratory.

Muscle or gastric temperature

Temperature-sensitive resistors, or thermistors, were one
the first and remain one of the most used sensors in ani-
mal  tracking  systems  [54].  A  thermistor  is  a  specialized
electrical  resistor  designed  to  impede  electrical  current
but with the degree of resistance imposed on the circuit
controlled  by  temperature.  They  can  be  very  small  and
easily  fit  on  an  electronic  tag  (Fig.  9b).  The  most  com-
monly  used  type  of  thermistor  is  known  as  a  negative
temperature  coefficient  thermistor,  meaning  that  the
electrical  resistance  decreases  as  temperature  increases
(Fig. 14b). In animal telemetry, the relationship between
the thermistor’s resistance and temperature is often used
to  modulate  the  inter-pulse  interval  for  transmitters  or
the pulse rate of animal-borne data loggers.

A thermistor is usually calibrated by placing the trans-
mitter, either acoustic or radio, or data logger in a water
bath  and  incrementing  the  temperature  slowly  while
recording  the  sensor’s  output.  Based  on  Ohm’s  law,  the

Fig. 13  Blood sampling data logger with syringe and sampler (a)
as well as six individual samplers with microprocessor controller
mounted on plate (b) for attachment to marine mammal (Taken from
[53])

Fig. 14  Picture of thermistor (a) with a plot of the changes in
resistance of a thermistor, intervals between pulses, or frequency of
pulses produced by an acoustic or radio transmitter in response to
changing temperatures (b)

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 16 of 24

current  (I)  passing  through  a  circuit  equals  its  voltage
potential (V) divided by its resistance (R):

I =

E
R .

This  change  in  current  flowing  through  the  thermis-
tor  in  a  data  logger  is  converted  to  a  digital  value  with
an  analog-to-digital  converter.  In  an  acoustic  or  radio
transmitter,  the  current  passing  through  the  resistor
charges a capacitor, which discharges when full charged.
The resistance of a negative coefficient thermistor is high
in  the  presence  of  cold  temperatures  (see  black  curve
in  Fig.  14b)  permitting  less  current  to  flow  through  the
circuit  to  charge  the  capacitor—thus  resulting  in  longer
intervals  between  discharges  of  pulses  of  acoustic  or
radio  energy  (see  blue  curve  in  Fig.  14b)  to  produce  a
slower pulse rate (see bottom of red curve). In the pres-
ence  of  high  temperatures,  the  resistance  of  the  ther-
mistor  is  low,  permitting  more  current  to  flow  through
the  circuit  to  charge  the  capacitor—hence  resulting  in
shorter intervals between the discharge of pulses to result
in a high pulse rate. Generally, a linear curve is fitted to
a  few  paired  temperatures  and  inter-pulse  intervals  or
pulse  rates  to  calibrate  the  inter-pulse  interval  to  the
transmitter temperature. A linear equation

T = mx + b,

where x is either inter-pulse interval or pulse rate is pro-
vided  by  the  tag  manufacturer  to  the  client  to  manually
enter  into  the  firmware  of  a  portable  or  autonomous
receiver using software provided by the manufacturer to
automatically  convert  the  two  independent  variables  to
temperature measurements (T).

There are many studies utilizing thermistors to provide
insight into the behavior of animals and their relationship
to the external environment. Only a few examples will be
presented here for brevity. It is obvious that thermistors
can  be  used  as  environmental  sensors.  For  example,  a
transmitter  or  data  logger  attached  externally  to  an  ani-
mal can be used to determine whether it enters a warmer
or  cooler  environment.  However,  it  is  less  obvious  that
thermistors  can  also  act  as  physiological  sensors  when
implanted  within  the  body  of  an  animal.  Transmitters
with  thermistors  can  be  inserted  into  the  musculature
or a body cavity (e.g., peritoneal) of an animal to record
its  body  temperature  or  into  its  stomach  to  record  gas-
tric  temperature.  Changes  in  stomach  temperature  can
indicate the ingestion of prey, as was found when juvenile
white sharks were fed cold fish fillets [55].

Let  us  discuss  a  few  more  studies  in  greater  detail
in  the  terrestrial  and  aquatic  environments.  Thermis-
tor-equipped  to  internally  implanted  radio  transmit-
ters  have  been  used  to  relate  temperature  to  the  daily

activity  of  the  northern  Pacific  rattlesnake  (Crotalus
oreganus)  [56].  By  coupling  in  situ  videography  with
near  constant  monitoring  of  the  rattlesnakes’  body
temperature,  the  study  could  examine  how  body  tem-
perature changed with behavior, location, and environ-
mental factors. Rattlesnakes were found to cease above
ground  activity  once  their  body  temperature  reached
a  threshold  (~ 31  °C).  The  study  also  found  that  body
temperature did not influence whether a strike towards
prey  would  be  successful,  but  may  influence  whether
snakes will attempt to strike potential prey.

Thermistors  have  often  been  used  to  study  tempera-
ture  regulation  of  animals  in  the  aquatic  environment.
For  example,  an  adult  white  shark  (Carcharodon  car-
charias)  maintained  a  constant  body  temperature  of
18°  despite  making  ‘yo-yo’  dives  into  waters  as  cold
as  4  °C  [57].  The  stomach  temperature  of  the  shortfin
mako  shark  (Isurus  oxyrinchus),  another  endotherm,
remained constant at roughly 28–29 °C during day and
night  despite  swimming  in  water  that  ranged  from  15
to 22° [58].

Environmental sensors
Sound and echo‑emission and reception

Sound recorders have been placed on animals to moni-
tor their own sonic emissions as well as external sounds
produced  by  other  animals  or  ambient  environmental
sound. The more modern, on-board hydrophones work
on  the  piezoelectric  principle.  Sound  waves  vibrate
a  diaphragm,  and  the  vibrations  direct  pressure  oscil-
lations  on  a  piezoelectric  crystal,  which  produce  an
output  of  voltage  oscillations  (Fig.  15a).  The  onboard
recorders  are  attached  to  cetaceans  using  a  suction
cup attachment, which loses its vacuum over time and
releases  from  the  cetacean  and  floats  to  the  surface.
These units are paired with a radio transmitter so that
they  can  be  located  at  the  surface  of  the  water  once

Fig. 15  Design of a piezoelectric-based hydrophone (adapted from
[59])

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 17 of 24

shed  from  the  body  of  the  cetacean.  It  is  possible  to
attach recorders to the fur-covered bodies of seals and
sea lions with epoxy glue once these pinnipeds replace
their  hair  after  coming  ashore  to  molt  each  year.  The
sound  recorder  can  be  removed  when  they  return  the
following year to molt.

Sound  recorders  have  been  placed  on  porpoises
(Lagenorhynchus albirostris) with suction cups to record
their  eco-location  clicks  in  order  to  learn  how  they  find
their prey [59]. It was found that porpoises decreased the
amplitude  and  interval  between  clicks  as  they  approach
their  prey.  They  estimate  the  distance  to  their  prey  as
they approach by decreasing the sound pressure of their
click to ascertain whether the sound pressure of the echo
is  still  high—evidence  that  they  are  closer  to  the  prey.
This  is  tantamount  to  a  scientist  decreasing  the  gain  of
a receiver when tracking an animal with an acoustic tag
and noting whether the signal is still strong in one direc-
tion  as  the  hydrophone  is  rotated  back  and  forth—evi-
dence  that  the  scientist  is  closer  to  the  tagged  subject.
At  the  same  time,  the  porpoises  reduce  the  interval
between the clicks to enable them to locate the direction
of  the  prey  with  higher  angular  resolution.  Finally,  they
decrease their speed as they turn to seize their prey. On-
board sound recorders have great potential for revealing
the  levels  of  ship  noise  that  whales  are  exposed  to,  and
whether  these  might  interfere  with  their  low-frequency
communication.

Irradiance

The light humans perceive is only a small portion of the
electromagnetic  spectrum.  Electromagnetic  radiation
is  composed  of  minute  packets  of  energy,  quanta,  that
propagate in a straight line while vibrating at distinct fre-
quencies to generate specific wavelengths. These quanta
vary  from  gamma  and  X-rays  with  a  wavelength  of  less
than 1 nm (nm) to radio waves that have a wavelength of
1 km. The human eye is sensitive to wavelengths varying
between 380 and 700 nm (nm) with the greatest sensitiv-
ity  to  wavelengths  around  550  nm.  The  electromagnetic
radiation within this range has been referred historically
as  “light”,  and  the  energy  packets  have  been  referred  to
as “photons”. Humans perceive the wavelengths as color,
and the amplitude of the wavelengths as brightness. The
levels of light vary over a large range of magnitudes from
dim  to  bright.  “Irradiance”,  on  the  other  hand,  is  a  less
specific  term  used  for  the  energy  in  those  wavelengths
within  and  outside  of  the  spectrum  visible  to  humans
[60].  Other  species  are  sensitive  to  wavelengths  that  are
either  shorter  or  longer  than  those,  to  which  humans
are  sensitive.  “Intensity”  is  the  term  used  to  describe
the  amplitude  of  the  vibrations  of  quanta  in  this  more

inclusive range of wavelengths. For this reason, it is bet-
ter to use the more inclusive term, irradiance and inten-
sity, with sensors used to record electromagnetic energy
with a broad diversity of species.

Irradiance  sensors  come  in  two  basic  forms:  photore-
sistors,  most  often  referred  to  as  photocells,  and  photo-
diodes.  The  photocell  operates  in  the  same  fashion  as  a
thermistor, but the electrical resistance changes with the
amount  of  light  rather  than  with  temperature.  A  light
sensitive material, cadmium sulfide, is placed on an insu-
lating  substrate  such  as  a  ceramic.  The  photo-sensitive
material  is  deposited  in  a  zig-zag  pattern  to  achieve  the
required  power  and  resistance  rating  (Fig.  16a).  When
electromagnetic  energy  within  a  particular  wavelength
is  absorbed  by  the  material,  the  valence  electrons  move

Fig. 16  Diagram of photocell (a) with explanation of operation
(b) and plot of how resistance changes as a function of increasing
irradiance level (c)

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 18 of 24

across the bandgap into the conduction band (Fig. 16b),
lowering  the  resistance  and  permitting  current  to  flow
through the circuit (Fig. 16c). Irradiance intensity ranges
greatly,  over  ten  logarithmic  units  from  dawn  to  dusk
[61]. Most photoresistors respond linearly over only five
powers  of  ten.  This  is  also  true  of  the  pigments  in  the
rods  and  cones  of  an  animal’s  retina.  The  rods  contain
pigments  that  are  sensitive  to  low  irradiance  levels,  the
cones  are  responsive  to  high  irradiance  levels.  One  way
to cover this broad range of irradiance levels is to equip
a  transmitter  with  two  photoresistors,  a  more  sensitive
one  with  its  resistance  changing  linearly  over  low  light
intensities  and  a  less  sensitive  one  with  its  resistances
changing  linearly  over  high  light  intensities.  The  differ-
ent  spectral  sensitivities,  blue  shifted  during  low  light
levels, and red shifted during high light levels, of an ani-
mal’s vision can be simulated by covering the photocells
with different gel filters [29]. This emulates scotopic night
vision and photopic day vision of terrestrial and aquatic
vertebrates.  A  problem  with  photoresistors  is  that  they
exhibit “light history”, or their resistance to light changes
over exposure time [4]. Due to the “light history” of pho-
tocells,  it  is  most  often  preferable  to  use  photodiodes
rather than photocells.

Photodiodes  (Fig.  17c)  rely  on  PN-junction  semi-
conductors  [11].  The  devices  provide  more  precise
measures  of  irradiance  than  photocells,  as  photodiode
measurements  remain  the  same  over  time  under  a  con-
stant  illumination.  A  PN-junction  consists  of  two  semi-
conductors,  a  P-type  semiconductor  which  is  positively
charged with free holes and a N-type semiconductor that
is negatively charged with free electrons (Fig. 17a). Elec-
trons  in  the  N  region  near  the  PN-junction  diffuse  into
the  P  region  leaving  behind  positively  charged  ions  in
the  N  region.  They  combine  with  holes,  forming  nega-
tively charged ions in the P region. Holes from the P-type
region  near  the  PN  interface  diffuse  into  the  N-type
region,  leaving  behind  negatively  charged  ions  in  the  P
region.  These  combine  with  electrons,  forming  positive
ions  in  the  N  region.  The  electrical  field  created  by  this
process opposes the diffusion process for both electrons
and  holes.  Connecting  the  P-type  region  to  the  nega-
tive terminal of a power supply and the N-type region to
the positive terminal of a power supply applies a reverse
bias  to  this  electrical  circuit.  Because  the  P-type  mate-
rial is now connected to the negative terminal, the holes
in  the  P-type  material  are  drawn  away  from  the  junc-
tion, leaving behind charged ions and causing the width
of  the  depletion  zone  to  increase.  Similarly,  because  the
N-type region is now connected to the positive terminal
of a power supply, the electrons will also be pulled away
from the junction with an identical effect. This creates a
wide  depletion  layer,  increasing  the  voltage  barrier  and

Fig. 17  A reverse-biased voltage applied to a semiconductor with
P and N regions and a PN-junction to create a wider depletion layer.
When a quanta impinges upon the semiconductor the electrons are
released to move toward the cathode and holes toward the anode (a)
(adapted from [11]). The reverse current produced is proportional to
light intensity (b). Photograph of photodiode (c)

producing  a  high  resistance  to  the  flow  of  charge  carri-
ers across the PN junction. When quanta from irradiance
impinge upon the depletion region of the photodiode, an
electron–hole  pair  is  generated  due  to  the  photoelectric
effect. The free electrons then move toward the cathode,
and  the  positive  charges,  or  holes,  move  to  the  anode
generating an electrical current. Furthermore, as the light
intensity  increases  the  number  of  electron–hole  pairs
generated  also  increases,  making  the  electrical  current
proportional to light intensity (Fig. 17b).

Irradiance is recorded by transmitters and data loggers
for many different reasons. For example, it was recorded
during  the  nightly  migrations  of  scalloped  hammerhead
from a seamount to the surrounding pelagic environment
to feed on squid. At this time the sharks swam with high
directionality. One potential guiding stimulus could have
been the nighttime configuration of the stars or presence
of the moon on the horizon. For this reason, a transmit-
ter was lowered close to the shark, which recorded irradi-
ance with one sensor possessing a sensitivity and spectral
range  matching  that  of  the  rod  receptors  in  the  shark’s
retina and the other with a sensitivity and spectral range
matching  that  of  the  cone  receptors  in  the  retina  [20].
These  measurements  were  used  to  create  contour  maps
of  isolumins,  each  indicating  the  intensity  of  irradiance

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 19 of 24

reaching that depth, on which was superimposed the dive
record  of  the  shark.  The  shark’s  dive  record  was  super-
imposed  on  isolumin  contours  of  irradiance  perceptible
by cones and rods in the shark’s retina. At nighttime the
shark  made  oscillatory  “yo-yo”  dives  between  150  and
400  m  where  the  “photopic”  irradiance  was  less  than
0.0001  µW/cm2/s  and  the  “scotopic”  irradiance  was  less
than  0.001  µW/cm2/s.  The  stars  and  moon  were  cer-
tainly imperceptible at these depths due to low irradiance
levels.

Another reason to record irradiance levels is to identify
the diel nature of certain behaviors. For example, archival
tags  were  placed  within  the  stomachs  of  yellowfin  tuna
with depth, temperature, and light sensors [62]. The ther-
mistors  recorded  an  increase  in  stomach  temperature
following  feeding.  The  irradiance  levels  detected  by  the
photocells  indicated  that  the  tunas  were  feeding  mainly
at  dusk  and  dawn.  In  conclusion,  the  tuna  preferred  to
hunt for prey in low light levels, when the prey presum-
ably are unable to detect them and avoid capture.

Dissolved oxygen

These  sensors  have  been  used  recently  in  the  marine
environment, and the design presented here is based on
one  particular  sensor  used  with  bluntnose  sixgill  sharks
(Hexanchus  griseus)  [63]. This  sensor  consists  of  a  plas-
tic  tube  with  a  gas  permeable  membrane  on  one  end
(Fig.  18a).  Two  insulated  wires  pass  through  the  tube
with one leading to the cathode and another to the anode.
The  tube  is  filled  with  an  electrolytic  solution  that  per-
mits an ionic reaction such as in a battery. Oxygen  (O2)
dissolved  in  the  surrounding  water  diffuses  across  the
membrane into the plastic tube. The  O2 hydrolyzes upon
contact  with  the  cathode  to  produce   H2O2  and  eventu-
ally releases an electron into the electrolyte. The electron
moves  from  the  anode  to  the  cathode  composed  of  sil-
ver chloride (AgCl), which then releases another electron
into  the  electrolytic  solution.  There  is  a  relatively  linear
relationship  to  the  partial  pressure  of   O2  created  within
the  tube  and  the  electrical  current  passing  through
the  electrodes  to  the  logic  circuit  in  the  transmitter
(Fig.  18b).  There  is  an  alternative  design  for  an  oxygen
sensor [64]. A bluntnose sixgill shark (Hexanchus griseus)
was  tracked  over  a  period  of  5  days  with  a  transmitter
equipped with temperature, pressure, and dissolved oxy-
gen  sensors.  The  shark  swam  at  depth  of  300  m  during
daytime and 450 to 600 m at nighttime. The temperatures
at  the  shallow  daytime  depths  varied  around  13  °C  and
during  nighttime  in  the  deeper  water  around  7  °C.  The
percentage of dissolved oxygen relative to saturation was
roughly 60% in the shallower waters during daytime and
20%  in  the  deeper  waters  during  nighttime.  The  shark
made greater depth excursions during the first night with

Fig. 18  Oxygen sensor consisting of a tube with a permeable
membrane at one end and two electrodes passing through the
other end to a cathode and anode (a). A plot of the electrical current
produced at different partial pressures as oxygen diffuses through
the gas permeable membrane of sensor (b). Picture of transmitter
equipped with dissolved oxygen sensor (C) used on bluntnose sixgill
sharks (taken from [63])

correspondingly  greater  variations  in  the  surrounding
water  temperature  and  concentration  of  dissolved  oxy-
gen—a more variable behavior exhibited likely due to the
stress of capture and release on the prior day.

Magnetic field

There  are  many  types  of  magnetic  field  sensors  such  as
nuclear  precession,  optically  pumped,  SQUID,  giant
magneto-resistive,  and  fluxgate  to  name  a  few.  How-
ever,  the  smallest  and  most  sensitive  magnetic  sensors,
which  can  be  incorporated  into  transmitters  and  data
loggers, are Lorentz-based MEMS sensors [65]. This sen-
sor  relies  on  the  mechanical  motion,  or  resonance,  of  a
MEMs structure due to the Lorentz force of an external
magnetic field acting upon a current-carrying conductor.

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 20 of 24

The changes in the resonance of the MEMS structure are
proportional to the strength of the applied magnetic field.
The  degree  of  resonance,  or  deformation,  can  be  meas-
ured  using  capacitive,  piezoelectric,  and  optical  sensing
techniques. Only one of the many designs, the piezoelec-
tric sensor, will be explained in detail (Fig. 19a). This sen-
sor  consists  of  a  series  of  rectangular  loops  of  a  silicon
material  attached  to  an  aluminum  substrate  that  lead
to  a  Wheatstone  bridge.  A  sinusoidal  electrical  current
is  passed  through  the  aluminum  substrate.  An  external
magnetic  field  exerts  a  Lorentz  force  on  the  conductor,
and  this  causes  the  silicon  to  resonate. The  piezo-resist-
ance  of  the  material  changes  proportional  to  the  degree
of its deformation. The induced current within this active
resistor and its absence in a paired inactive resistor, sans
the  conductive  member,  generate  an  output  voltage
across a Wheatstone bridge proportional to the magnetic

field  flux  density.  Shown  is  a  3-axis  magnetoresistor,
which  serves  as  a  companion  to  a  3-axis  accelerometer
in circuits (Fig. 19b) [66] and three single-axis magneto-
inductive  sensors  lying  along  orthogonal  axes  (Fig.  19c)
[67].  The  former  has  a  sensitivity  of  0.1  µT,  the  latter  a
sensitivity of 13 nT.

Magnetic field measurements have been used in archi-
val tags along with irradiance and temperature measure-
ments  to  estimate  latitude.  In  order  to  estimate  latitude
based  on  magnetic  field  intensity,  it  is  necessary  to  first
estimate  the  longitude  of  the  tag.  This  is  determined
using  irradiance  measurements.  The  archival  tag  has  a
very  accurate  internal  clock,  which  can  be  initialized  to
Universal Time. It then estimates the times of sunrise and
sunset  from  rapid  changes  in  the  intensity  of  irradiance
at dawn and dusk. Apparent noon, midway between the
rapid  increase  in  light  at  sunrise  and  the  rapid  decrease

Fig. 19  Diagram of a MEMS piezo-resistive resonant sensor that operates on the principle of the Lorentz force (a) (adapted from [65]). Drawing of
three-axis magneto-resistive sensor (b) (taken from [66]) and picture of three single-axis magneto-inductive sensors oriented along orthogonal axes
(c) (taken from [67])

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 21 of 24

in light at sunset, is then compared to true noon to deter-
mine  longitude—each  hour  difference  between  appar-
ent and true noon equals an offset of 15° from the prime
meridian  on  the  circumference  of  the  earth.  Latitude
can  also  be  estimated  from  irradiance  measurements.
Day length, or the time between sunrise and sunset, var-
ies with distance along a meridian on the earth’s surface.
For this reason, it can be used as an indicator of latitude.
The length of the day at the established longitude can be
entered into a mathematical algorithm that solves for lat-
itude. A 3-axis magnetometer can provide measurements
that also can be used to estimate longitude. The intensi-
ties  recorded  on  the  three  axes  are  summed  to  provide
an overall measurement of total field intensity. The meas-
urement of the intensity of the earth’s main field is then
paired  with  an  estimate  of  longitude,  derived  from  the
daily series of irradiance measurements. Given the longi-
tude of the tagged animal, the latitude can be determined
based upon the measurement of total field intensity. Soft-
ware is available from the United State Geological Survey
that provides a user with total field intensity, given a lon-
gitude  and  latitude  of  any  point  on  earth.  An  algorithm
can  be  used  to  find  the  estimated  latitude  through  an
iterative  examination,  searching  for  the  matching  inten-
sity  along  a  series  of  modeled  intensities  along  the  esti-
mated  line  of  longitude  until  a  match  is  found  between

measured and the modeled field intensity. This process is
illustrated on a map of the earth’s main field (Fig. 20). A
meridian is drawn on the world magnetic model (WMM)
map  at  the  estimated  longitude  to  isoclines  with  the
measured  geomagnetic  intensity  (Fig.  20).  For  geomag-
netic estimates of latitude, there are always two locations
for  each  north–south  line. They  are  widely  separated  so
one  can  be  eliminated  because  it  is  considerably  farther
from the release location or not consistent with previous
daily observations.

The track of an animal will be more accurate and robust
if  multiple  environmental  features  are  used  in  position
determination [68]. For example, in the track of a drifting
transmitter  during  the  spring  2013  equinox,  the  irradi-
ance-based  geopositions  were  far  north  of  the  Doppler-
based ARGOS positions. This discrepancy also occurred
around  the  fall  2013  equinox.  During  these  times,  the
geomagnetic-based  geolocations  were  much  closer  to
satellite-based  positions  than  the  irradiance-based  geo-
positions. However, during the summer equinox of 2013,
both  the  irradiance  and  geomagnetic  position-determi-
nations were accurate, with the latter being slightly more
accurate than the former.

Fig. 20  Illustration of the determination of latitude based on an archival tag’s measurement of total field intensity. Note that there are two solutions
with matching total field intensities. The real location is usually close to the site of tagging (taken from [68])

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 22 of 24

Conclusions
The ability to remotely monitor the behaviors of animals
and their interactions with their environment has revolu-
tionized how ecologists conduct studies. The creative use
and placement of sensors in an electronic tag can greatly
expand the amount of information that can be garnered
from  ecological  studies.  The  values  of  the  diversity  of
sensors  described  here  to  biologists  are  summarized  in
Table  1.  While  a  limited  number  of  measurements  or  a
summary  of  them  can  be  transmitted  over  acoustic  and
radio  bandwidths  to  a  receiver  either  on  land,  water  or
to  a  satellite  passing  over  head,  a  greater  number  can
be  retrieved  from  an  electronic  tag  once  it  is  recovered.
For example, the ARGOS satellites can upload measure-
ments  for  15  min  before  and  15  min  after  passing  over
a  tag  bearing  animal.  A  marine  species  must  be  on  the
surface  to  transmit  data  via  a  radio  signal  while  the  sat-
ellite  passes  overhead.  Even  if  the  tag  releases  from  the
animal  and  rises  to  the  surface,  the  data  transmission
is  dependent  upon  how  many  satellites  pass  overhead.

Data loggers are now outfitted with either electrolytic or
explosive releases that are set to release the tag from the
animal  at  a  specified  time  with  a  radio  beacon  that  per-
mits relocation. A fine-grained description of behavioral
patterns  requires  rapid  sampling  rates  and  these  can  be
accommodated  with  data  loggers  with  their  large  data
capacity, hence their current popularity among the scien-
tific community. The value of telemetry is immense, and
the  following  reviews  illustrate  just  how  revolutionary
transmitter and sensor technologies have been to ecolo-
gist  studying  both  terrestrial  and  aquatic  environments:
“Terrestrial animal tracking as an eye on life and planet”
[69] and “Aquatic animal telemetry: a panoramic window
into the underwater word” [70]. Assuredly, as technologi-
cal advances continue, many biotelemetry systems will be
generated that allow for numerous minute sensors to be
deployed  simultaneously  across  a  large  variety  of  taxa—
studies of small-bodied taxa will likely benefit the most.
As  the  field  expands,  it  will  be  become  more  important
that biologists as a group, have a basic understanding of

Table 1  Value to biologists of using these behavioral, physiological, and ecological sensors on their electronic tags

Type

Property

Sensor

Value to biologist

Advantage/disadvantage

Behavioral

Speed

Reed switch, inductive coil

Record swimming or flight

Can become jammed

speed

Hall effect probe

Record animal movements

Will not become jammed

Piezoelectric transducer, MEMS Record behavioral patterns,

Small and does not become

produce ethogram

jammed

Tilt

Mercury switch

Monitor changes in posture

Altitude, depth

MEMS altitude sensor

Record flight altitude

Works with low pressures

Direction

Optical heading sensor

Ascertain degree of direction-

Can become jammed

Strain gauge

Determine swimming depths

Works only with high pressures

ality

Predation

Spawning

Sociality

MEMS heading sensor

Monitor degree of directionality Doesn’t become jammed

Magnetic/electrode sensors

Identify time of feeding and

prey

Ultrasonic detection

Identify time, environment, and

Need to implant beacon in uterus

behavior

of female

Proximity sensor

Monitor social interactions

Transmitter/receiver needed

Physiological

Brain, muscular, or heart activity Electrograms

Record diverse physiological

Electrodes can become bulky

Gastric activity

Blood chemistry

pH sensor

Blood extractor

responses

Detect ingestion of prey

Monitor reproductive state or

Bulky with multiple syringes

stress

Body temperature

Thermistor

Record endothermy or ecto-

Small and durable

Environmental Air/water irradiance

Photocell

thermy

Determine whether day or

Exhibit light history; are non-

nighttime

stationary over time

Photodiode

Ascertain whether day or

No light history, stationary

nighttime

Air/water temperature

Thermistor

Record whether tropical, tem-

Small and durable

perate, polar, air/water masses

Dissolved oxygen

Magnetic field

Dissolved oxygen sensor

Identify aerobic/anaerobic envir. Relatively bulky

MEMS magnetic field sensor

Use to estimate latitude

Very small and accurate

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 23 of 24

the  operating  principles  behind  biotelemetry  sensors.
As such, it is our intention that this review act as spring-
board  to  further  increase  the  use  of  sensors  and  act  a
mechanism to generate new innovations.

Acknowledgements
The authors would like to extend their appreciation to all of the scientists,
who served as pioneers in the development and utilization of the diversity of
sensors described in this article. It should also be pointed out that the idea
for this manuscript, and other future articles on the different electronic tag
technologies and analytical techniques, using the same format, came from
a seminar series hosted by the second author at the University of California,
Davis. This hugely successful graduate seminar series was held in 2016, and
entitled “Animal Movements in Ecology: How do Transmitters Work?” Finally,
the authors would like to acknowledge the great service the two reviewers
performed in making this a better and more comprehensive treatment of a
very dynamic field, sensor design and its application in biotelemetry.

Authors’ contributions
MW prepared the first draft of the article. APK expanded the scope of the
manuscript by adding descriptions of the functioning of additional sensors.
The latter also created all of the illustrations presented in the review using
the Adobe software, Illustrator. Both authors read and approved the final
manuscript.

Funding
No funding was received to complete the review.

Availability of data and materials
The information presented in this review can be obtained from the authors of
the scientific studies described in this review. A list of the pertinent references
is given at the end of the article.

Ethics approval and consent to participate
This is a review, and for that reason, an Animal Protocol was not obtained from
either the University of California, Davis, or San Diego State University. Neither
were consent to participate forms needed for the review.

Consent for publication
Both authors consent to the publication of this review.

Competing interests
The authors declare that they have no competing interests.

Author details
1 San Diego State University, 5500 Campanile Drive, San Diego, CA 92182, USA.
2 Ecology Graduate Group, University of California, Davis, One Shields Drive,
Davis, CA 95616, USA. 3 Department of Wildlife, Fish, and Conservation Biology,
University of California, Davis, One Shields Drive, Davis, CA 95616, USA.

Received: 16 August 2018   Accepted: 11 December 2019

References

 1. Cooke SJ, Hinch SG, Wikelski M, Andrews RD, Kuchel LJ, Wolcott TG, Butler
PJ. Biotelemetry: a mechanistic approach to ecology. Trends Ecol Evol.
2004;19:334–43.

 2. Nathan R, Spiegel O, Fortmann-Roe S, Harel R, Wikelski M, Getz WM. Using
tri-axial acceleration data to identify behavioral modes of free-ranging
animals: general concepts and tools illustrated for griffon vultures. J Exp
Biol. 2012;215:986–96.

 3. Williams HJ, Holton MD, Shepard ELC, Largey N, Norman B, Ryan PG,

Duriez O, Scantlebury M, Quintana F, Magowan EA, et al. Identification
of animal movement patterns using tri-axial magnetometry. Mov Ecol.
2017;5:6.

 4. Anonymous. VACTEC photoconductive cells. Bulletin PCD-6, St. Louis,

Michigan. 1970. 4 pp.

 5. Kelly JT, Klimley AP. Relating the swimming movements of green
sturgeon to the movement of water currents. Environ Biol Fishes.
2012;93:151–67.

 6. Droghini A, Boutin S. The calm during the storm: snowfall events

decrease the movement rates of grey wolves (Canis lupus). PLoS ONE.
2014;13(10):e0205742.

 7. Mitchell GW, Woodworth BK, Taylor PD, Norris DR. Automated telemetry

reveals age specific differences in flight duration and speed are driven by
wind conditions in a migratory songbird. Mov Ecol. 2015;3:19. https ://doi.
org/10.1186/s4046 2-015-0046-5.

 8. Alerstam T, Rosén M, Backman J, Ericson PGP, Hellgren O. Flight speeds
among bird species: allometric and phylogenetic effects. PLoS Biol.
2007;5:e197.

 9. Blackwell SB, Haverl CA, Le Boeuf BJ. A method for calibrating swim-

speed recorders. Mar Mamm Sci. 1999;15:894–905.

 10. Block B, Booth D, Carey F. Direct measurement of swimming speeds and

depth of blue marlin. J Exp Biol. 1992;166:267–84.
 11.  Electronics Tutorials. <http://www.elect> ronic s-tutor ials.ws.
 12.  Wilson R, Liebsch N. Up-beat motion in swinging limbs: new insights
into assessing movement in free-living aquatic vertebrates. Mar Biol.
2003;142:537–47.

 13. Ropert-Coudert Y, Kato A, Liebsch N, Wilson RR, Müller G, Baubet E.

Monitoring jaw movements: a cue to feeding activity. Game Wildl Sci.
2004;21:1–19.

 14. Hanley S. Accelerometers: taking the guesswork out of accelerometer
selection. 2016. https ://blog.mide.com/accel erome ter-selec tion.
 15. Qin QH. Introduction to piezoelectricity. In: Advanced mechanics of

piezoelectricity. Berlin: Springer; 2013. pp. 1–19.

 16. Curie J. Development, via compression, of electric polarization in hemihe-
dral crystals with inclined faces. Bull Soc Minerol France. 1880;3:90–3.

 17. Brown DD, LaPoint S, Kays R, Heidrich W, Kümmeth F, Wikelski M.

Accelerometer-informed GPS telemetry: reducing the trade-off between
resolution and longevity. Wildl Soc B. 2012;36:139–46.

 18. Brown DD, Kays R, Wikelski M, Wilson R, Klimley AP. Observing the

unwatchable through acceleration logging of animal behavior. Anim
Biotelem. 2013;1:1–20.

 19. Shepherd ELC, Wilson RP, Quintana F, Laich AG, Leibsch N, Albareda DA,
Halsey LG, Gleiss A, Morgan DT, Myers AE, Newman C, Macdonald DW.
Identification of animal movement using tri-axial accelerometry. Endan-
ger Species Res. 2008;10:47–60.

 20. Halsey LG, White CR. Measuring energetics and behaviour using acceler-

ometry in cane toads Bufo marinus. PLoS ONE. 2010;5(4):e10170.

 21. Whittingham MJ. The use of radio telemetry to measure the feed-

ing behavior of breeding european golden-plovers. J Field Ornithol.
1996;67:463–70.

 22. Grishechkin BY, Baskakov AI. Optimal algorithms for spaceborn altimeter.
In: IEEE international geoscience and remove sensing symposium 2010.
pp. 640–2.
 23.

Instrumentation Today. <http://www.Instr> ument ation today .com.
 24.  Bosch. BMP085 digital barometric pressure sensor. 2019. Available on

Amazon.

 25. Manikandan E, Karthigeyan KA, Arokia-James KI. Micro electro mechani-

cal system (MEMS) based pressure sensor in barometric altimeter. Int J Sci
Eng Res. 2011;2:1–8.

 26. López-López P. Individual-based tracking systems in ornithology: wel-

come to the era of big data. Ardeola. 2016;63:103–36.

 27. Murgatroyd M, Photopoulou T, Underhill LG, Bouten W, Amar A. Where
eagles soar: fine resolution tracking reveals the spatiotemporal use of
differential soaring modes in a large raptor. Ecol Evol. 2018;8:6788–99.
 28. Duriez O, Péron G, Gremillet D, Sforzi A, Monti F. Migrating ospreys use

thermal uplift over the open sea. Biol Lett. 2019. https ://doi.org/10.13157
/arla.63.1.2016.rp5.

 29. Klimley AP. Highly directional swimming by scalloped hammerhead

sharks, Sphyrna lewini, and subsurface irradiance, temperature, bathym-
etry, and geomagnetic field. Mar Biol. 1993;117:1–22.

 30. Gleiss AC, Norman B, Wilson RP. Moved by that sinking feeling: variable
diving geometry underlies movement strategies in whale sharks. Funct
Ecol. 2011;25:595–607.

 31. Meyer CG, Holland KN. Autonomous measurement of ingestion and

digestion processes in free-swimming sharks. J Exp Biol. 2012;215:3681–4.

Whitford and Klimley  Anim Biotelemetry            (2019) 7:26

Page 24 of 24

 32. Hayes SA, Tetschel NM, Michel CI, Campagne C, Robinson PW, Fowler M,
Yack T, Mellinger D, Simmon S, Costa DP, MacFarlane B. Mobile receiv-
ers: releasing the mooring to ‘see’ where fish go. Environ Biol Fishes.
2011;96:189–201.

 33. Flagg M. Sea Tag-SP ‘Ovolutag’ spawning detecting and reporting PSAT
tag: concept and tag report, Desert Star LLC, Monterey, 3 pp (available
from author).

 51. Gelsleichhter JL, Rasmussen EL, Manire CA, Tyminski J, Chang B,

Lombardi-Carlson L. Serum steroid concentrations and development of
reproductive organs during puberty in male bonnethead sharks, Sphyrna
tiburo. Fish Physiol Biochem. 2002;26:389–401.

 52. Manire CA, Rasmussen LEI, Hess DL, Hueter RE. Serum steroid hormones
and reproductive cycle of the female bonnethead shark, Sphyrna tiburo.
Gen. Comp Endochrinol. 1995;97:366–76.

 34. Klimley AP, Le Boeuf BJ, Cantara KM, Richert JE, Davis SF, Van Sommeran

 53. Little Leonard: operator’s manual, sampling system, BS400-D-5S. Little

S. Radio-acoustic positioning: a tool for studying site-specific behavior of
the white shark and large marine vertebrates. Mar Biol. 2001;138:429–46.
 35.  Klimley AP, Le Boeuf BJ, Cantara KM, Richert JE, Davis SF, Van Sommeran

V, Kelly JT. The hunting strategy of white sharks at a pinniped colony. Mar
Biol. 2001;13:617–36.

 36. Guttridge TL, Gruber SH, Krause J, Sims DW. Novel acoustic technology

for studying free-ranging shark social behaviour by recording individuals
interactions. PLoS ONE. 2010;5(2):e9324.

 37. Holland KN, Meyer CG, Dagorn LC. Inter-animal telemetry; results from

first deployment of acoustic “Business Card” tags. Endanger Species Res.
2009;10:287–93.

 38. Bandivadekar RR, Pandit PS, Sollmann R, Thomas MJ, Logan S, Brown JC,
Klimley AP, Johnson CK, Tell LA. Novel tag reading system using radi-
ofrequency identification technology on hummingbird feeders in urban
locations in California: acquiring visitation data to establish pathogen
transmission metrices. PLoS ONE. 2019;13(12):e0211254.

 39. Ossi F, Focardi S, Picco G, Murphy A, Moltenii D, Tolhjurst B, Giannini N,
Gaillard J, Cagnacci F. Understanding and geo-referencing animal con-
tacts: proximity sensor networks integrated with GPS-based telemetry.
Anim Biotelem. 2016;4:1–21.

 40. Krause J, Krause S, Arlinghaus R, Psorakis I, Roberts S, Rutz C. Reality min-

ing of animal social systems. Trends Ecol Evol. 2013;28:541–51.
 41.  Prange S, Gehrt SD, Hauver S. Frequency and duration of contacts

between free-ranging raccoons: uncovering a hidden social system. J
Mammal. 2011;92:1331–42.

Leonardo Inc. 2016; Version 1.11-21.

 54. Osgood DW, Weigl PD. Monitoring activity of small mammals by

temperature-telemetry. Ecology. 1972;53:738–40.

 55. Jorgensen SJ, Gleiss AC, Kanive PE, Chapple TK, Anderson SD, Ezcurra JM,
Brandt WT, Block BA. In the belly of the beast: resolving stomach tag data
to link temperature, acceleration and feeding in white shark (Carcharodon
carcharias). Anim Biotelem. 2015;3:1–10.

 56. Putman BJ, Clark RW. Behavioral thermal tolerances of free-ranging rattle-
snakes (Crotalus oreganus) during the summer foraging season. J Therm
Biol. 2017;65:8–15.

 57. Carey FG, Kanwisher JW, Brazier O, Casey JG, Pratt HL. Temperature activi-
ties of a white shark, Carcharodon carcharias. Copeia. 1982:254–60.
 58. Carey FG, Teal JM, Kanwisher JW. The visceral temperatures of mackerel

sharks (Lamnidae). Physiol Zool. 1981;54:334–44.

 59. Akamatsu T, Wang D, Wang K, Naito Y. Biosonar behaviour of free-ranging

porpoises. Proc R Soc B. 2005;72:797–801.

 60. Klimley AP. The biology of sharks and rays. Chicago: University of Chicago

Press; 2013. p. 512.

 61. Qayum HA, Klimley AP, Richert J, Newton R. Broad-band versus narrow-
band irradiance for estimating latitude by archival tags. Mar Biol.
2006;151:467–81.

 62. Bestley S, Patterson TA, Hindell MA, Gunn JS. Feeding ecology of wild

migratory tunas revealed by archival tag records with visceral warming. J
Anim Ecol. 2008;77:1223–33.

 63. Coffey DM, Holland KN. First autonomous recordings of in situ dissolved

 42. Drewe JA, Weber N, Carter SP, Bearhop S, Harrison XA, Dall SR, McDonald
RA, Delahay RJ. Performance of proximity loggers in recording intra-and
inter-species interactions: a laboratory and field-based validation study.
PLoS ONE. 2012;7:e39068.

oxygen from free-ranging fish. Anim Biotelem. 2015;3:1–9.

 64. Svendsen JC, Aarestrup K, Steffensen JF, Herskin J. A novel acoustic
dissolved oxygen transmitter for fish telemetry. Mar Technol Soc J.
2006;40:103–8.

 43. Hodgson ES, Mathewson RF. Electrophysiological studies of chemore-

 65. Herrera-May AL, Soler-Balcazar JC, Vázquez-Leal H, Martinez-Castillo J,

ception in elasmobranchs. pp. 227–67. In: Hodgson ES, Mathewson RF,
editors. Sensory biology of sharks, skates, and rays. Washington DC: U.S.
Government Printing Office; 1976.

Vigueras-Zuñiga MO, Aguilera-Cortés LA. Recent advances of MEMS reso-
nators for Lorentz force based magnetic field sensors: design, applica-
tions and challenges. Sensors. 2016;16:1359–84.

 44. Cocherell SA, Cocherell DE, Jones GJ, Miranda JB, Thompson LC, Cech JJ

 66. NXP: Xtrinsic MAG3110 three-axis digital magnetometer. Data Sheet,

Jr, Klimley AP. Rainbow trout Oncorhynchus mykiss energetic responses to
pulsed flows in the American River, California, assessed by electromyo-
gram telemetry. Environ Biol Fishes. 2011;90:29–41.

 45. Williams SH, Vinyard CJ, Glander KE, Deffenbaugh M, Teaford MF,

Thompson CL. Telemetry system for assessing jaw-muscle function in
free-ranging primates. Int J Primatol. 2008;29:1441–53.

 46. Smith EN, Allison RD, Crowder WE, Smith EN, Allison RD, Crowder WE.
Bradycardia in a free ranging American alligator. Copeia. 2016:770–2.

 47. Hindel MA, Lea M. Heart rate, swimming speed, and estimated oxygen

consumption of a free-ranging southern elephant seal. Physiol Zool.
1998;71:74–84.

 48. Peters G. A new device for monitoring gastric pH in free-ranging animals.

Am J Physiol. 1997;36:748–53.

 49. Papastamatiou YP, Meyer CG, Holland KN. A new acoustic pH transmitter
for studying the feeding habits of free-ranging sharks. Aquatic Living
Resour. 2007;20:287–90.

 50. Peters G. A reference electrode with free-diffusion liquid junction for
electrochemical measurements under changing pressure conditions.
Anal Chem. 1997;69:2362–6.

MAG3110, Rev. 9.2 2013:1–30.

 67. PNI Sensor Corporation: RM3100 geomagnetic sensor. Data sheet, 2 p.
 68. Klimley AP, Flagg M, Hammerschlag N, Hearn A. The value of using meas-
urements of geomagnetic field in addition to irradiance and sea surface
temperature to estimate geolocations of aquatic animals. Anim Biotelem.
2017;5:1–17.

 69. Kays R, Crofoot MC, Jetz W, Wikelski M. Terrestrial animal tracking as an

eye on life and planet. Science. 2015;348:1222–31.

 70. Hussey NE, Kessel ST, Aarestrup K, Cooke SJ, Cowley PD, Fisk AT, Hardcourt
RG, Holland KN, Iverson SJ, Kocik JF, Mills-Flemming JE, Whoriskey FG.
Aquatic animal telemetry: a panoramic window into the underwater
world. Science. 2015;348:1221.

Publisher’s Note
Springer Nature remains neutral with regard to jurisdictional claims in pub-
lished maps and institutional affiliations.
