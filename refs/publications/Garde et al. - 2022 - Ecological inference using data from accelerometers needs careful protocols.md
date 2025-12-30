Received: 16 July 2021 |  Accepted: 20 December 2021
DOI: 10.1111/2041-210X.13804

R E S E A R C H   A R T I C L E

Ecological inference using data from accelerometers needs
careful protocols

Baptiste Garde1  |   Rory P. Wilson1  |   Adam Fell1,2 |   Nik Cole3 |   Vikash Tatayah4 |
Mark D. Holton1 |   Kayleigh A. R. Rose1  |   Richard S. Metcalfe5 |   Hermina Robotka6 |
Martin Wikelski7,8  |   Fred Tremblay9 |   Shannon Whelan9  |   Kyle H. Elliott9 |
Emily L. C. Shepard1

1Department of Biosciences, Swansea University, Swansea, UK; 2Biological and Environmental Sciences, University of Stirling, Stirling, UK; 3Durrell Wildlife
Conservation Trust, La Profonde Rue, Jersey, Jersey; 4Mauritian Wildlife Foundation, Vacoas, Mauritius; 5Applied Sports Science, Technology, Exercise
and Medicine Research Centre (A- STEM), Swansea University, Swansea, UK; 6Max Planck Institute for Ornithology, Seewiesen, Germany; 7Department of
Migration, Max Planck Institute of Animal Behavior, Radolfzell, Germany; 8Centre for the Advanced Study of Collective Behaviour, University of Konstanz,
Constance, Germany and 9Department of Natural Resources Sciences, McGill University, Sainte- Anne- de- Bellevue, QC, Canada

Correspondence
Baptiste Garde
Email: <baptiste.garde@swansea.ac.uk>

Funding information
H2020 European Research Council,
Grant/Award Number: 715874; Horizon
2020; European Union; European
Research Council

Abstract

1. Accelerometers in animal- attached tags are powerful tools in behavioural ecol-

ogy, they can be used to determine behaviour and provide proxies for movement-

based energy expenditure. Researchers are collecting and archiving data across

systems,  seasons  and  device  types.  However,  using  data  repositories  to  draw

ecological inference requires a good understanding of the error introduced ac-

Handling Editor: Aaron Ellison

cording to sensor type and position on the study animal and protocols for error

assessment and minimisation.

2. Using laboratory trials, we examine the absolute accuracy of tri- axial accelerom-

eters and determine how inaccuracies impact measurements of dynamic body

acceleration (DBA), a proxy for energy expenditure, in human participants. We

then examine how tag type and placement affect the acceleration signal in birds,

using  pigeons  Columba  livia  flying  in  a  wind  tunnel,  with  tags  mounted  simul-

taneously in two positions, and back-  and tail- mounted tags deployed on wild

kittiwakes Rissa tridactyla. Finally, we present a case study where two genera-

tions of tag were deployed using different attachment procedures on red- tailed

tropicbirds Phaethon rubricauda foraging in different seasons.

3. Bench tests showed that individual acceleration axes required a two- level cor-

rection to eliminate measurement error. This resulted in DBA differences of up

to 5% between calibrated and uncalibrated tags for humans walking at a range

of speeds. Device position was associated with greater variation in DBA, with

upper and lower back- mounted tags varying by 9% in pigeons, and tail-  and back-

mounted tags varying by 13% in kittiwakes. The tropicbird study highlighted the

This is an open access article under the terms of the Creative Commons Attribution License, which permits use, distribution and reproduction in any medium,
provided the original work is properly cited.
© 2022 The Authors. Methods in Ecology and Evolution published by John Wiley & Sons Ltd on behalf of British Ecological Society.

Methods Ecol Evol. 2022;13:813–825.

wileyonlinelibrary.com/journal/mee3

 |  813

814 |   Methods in Ecology and Evolu(cid:13)on

difficulties  of  attributing  changes  in  signal  amplitude  to  a  single  factor  when

confounding influences tend to covary, as DBA varied by 25% between seasons.

4. Accelerometer accuracy, tag placement and attachment critically affect the sig-

nal amplitude and thereby the ability of the system to detect biologically mean-

ingful  phenomena.  We  propose  a  simple  method  to  calibrate  accelerometers

that can be executed under field conditions. This should be used prior to deploy-

ments and archived with resulting data. We also suggest a way that researchers

can assess accuracy in previously collected data, and caution that variable tag

placement and attachment can increase sensor noise and even generate trends

that have no biological meaning.

K E Y W O R D S
accelerometry, accuracy, biologger, biotelemetry, calibration, DBA, tag placement

1  |  I NTRO D U C TI O N

et  al.,  2011).  Unsurprisingly,  these  data  have  been  collected  using

different methods of attachment and by deploying a variety of dif-

Animal- attached  tags  have  revolutionised  our  understanding  of

ferent tags without critical analysis of the compatibility of different

wild  animal  ecology  (Bograd  et  al.,  2010;  Sequeira  et  al.,  2021;

datasets (Sequeira et al., 2021).

Yoda,  2019).  Of  the  sensors  often  used,  accelerometers  (Yoda

Tag position on the body is likely to affect acceleration values,

et al., 1999) are regarded as a particularly powerful tool for study-

as pointed out by Wilson et al. (2020), who noted that DBA (Qasem

ing  wild  animal  behavioural  ecology,  with  studies  using  them  to

et al., 2012) varied with tag position in humans wearing back-  and

look  at  the  occurrence  and  intensity  of  behaviour  (Chakravarty

waist- mounted tags running on a treadmill (with DBA values varying

et  al.,  2019;  Fehlmann  et  al.,  2017),  assess  movement  character-

istics (Shepard et al., 2008) and as a proxy for energy expenditure

by ~0.25 g at intermediate speeds). This is easy to understand since
humans have a flexible spine. Birds, on the other hand, have an es-

(Wilson  et  al.,  2020).  The  latter  has  developed  rapidly  since  the

sentially immoveable box- like thorax (Baumel, 1993). Differences in

demonstration that dynamic body acceleration (DBA) is related to

acceleration between tags placed on the back and the neck (Kölzsch

energy expenditure across a range of vertebrates and invertebrates

et al., 2016) or the tail (Elliott, 2016) are easy to associate with in-

(Halsey et al., 2009; Wilson et al., 2006, 2019). Such measurements

dependent movement of the head or tail, but the thorax itself can

have great potential for understanding animal strategies, in partic-

experience pitch changes over the wingbeat cycle (Su et al., 2012;

ular studying how animals respond to changes in food availability

Tobalske & Dial, 1996), which may affect the acceleration recorded

(Kokubun et al., 2011), climate (Gudka et al., 2019) and anthropo-

by  loggers  depending  on  their  position.  In  line  with  this,  we  note

genic  threats  or  activity  (Nickel  et  al.,  2021;  Payne  et  al.,  2015;

that the precise position of the accelerometer chips on the circuit

Yorzinski et al., 2015).

boards may also affect the acceleration measured by the sensors,

In terrestrial mammals (cf. Field et al., 2011 for a comparison with

particularly in cases where the circuit board is long relative to the

marine mammals), accelerometers tend to be attached using collars,

bird’s back and where the chip could be positioned close to either

providing  a  largely  standardised  position  of  attachment,  although

end.

collars have their own complications in terms of the need to obtain a

At a more fundamental level, the fabrication of loggers with ac-

good fit and account for collar rotation in data interpretation (Wilson

celerometers involves extensive heating as the sensors are soldered

et al., 2020). In contrast, researchers use different attachment posi-

to  the  circuit  boards.  Although  the  literature  notes  that  there  is  a

tions on birds. For instance, tags are deployed on the lower back, the

temperature- dependent  output  of  accelerometers  under  normal

tail or the belly of seabirds depending on the species and the tag po-

operating conditions (this normally being corrected within the chip;

sition associated with least detriment (Elliott, 2016; Ropert- Coudert

e.g. Yin et al., 2019), the heating process changes the output versus

et al., 2003; Vandenabeele et al., 2014). Researchers working with

acceleration in a fundamentally different manner (Ruzza et al., 2018),

raptors may deploy tags using backpack or leg- loop harnesses (e.g.

even if they are carefully calibrated prior to this process (see https://

Harel et al., 2017; Williams et al., 2015 respectively), which results

<www.mouser.co.uk/datas> heet/2/389/dm001 03319 - 17980 35.pdf).

in differences in tag position. The widespread availability and use of

Specifically,  while  the  vector  sum  of  the  three  acceleration  chan-

accelerometers mean that large datasets, collected over years, are

nels  should  be  1  when  a  unit  is  at  rest  (Won  &  Golnaraghi,  2009),

now  available,  providing  valuable  information  about  behaviour,  in-

this can vary after heating, resulting in error in the estimation of the

cluding flight effort across temporal and spatial scales (Kranstauber

Earth’s  gravitational  component.  This  can  in  turn  introduce  error

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMethods in Ecology and Evolu(cid:13)on

    |  815

into  the  estimation  of  the  ‘dynamic’  acceleration,  or  acceleration

where  x,  y  and  z  are  the  raw  acceleration  values,  for  the  periods

due to movement, which is the basis for acceleration- based proxies

when they were held still. Note that there are six maxima because

for energy expenditure (Wilson et al., 2020). While the engineering

each axis has two values: a minimum and a maximum, which become

literature  discusses  methods  for  identifying  and  correcting  inaccu-

positive in the vectorial sum. In a device with perfect acceleration

racies  in  accelerometer  readings  using  rotational- tilt  platforms  or

sensors, all maxima should be 1.0 g (Won & Golnaraghi, 2009) (al-

motion  rate  tables  (or  similar)  and  adopting  calibration  algorithms

though  the  acceleration  on  earth  varies  with  latitude  by  up  to  a

(Sipos et al., 2011), approaches such as Kalman filter covariance ma-

maximum of 0.0053 g due to the earth’s shape and the centrifugal

trices (Beravs et al., 2012), dynamic filtering for bias issues (Batista

force generated by the planet spinning as well as other processes;

et  al.,  2011)  or  iterative  simulations  for  gain  and  bias  compared  to

Novák, 2010). However, values were always either marginally higher

measured values (Won & Golnaraghi, 2009), the importance of this

or  lower  than  1.0  g  (see  Section  3).  Furthermore,  the  two  maxima

has not been highlighted in the biological literature (Cade et al., 2021).

for  each  axis  differed  (e.g.  Figure  1b).  This  therefore  requires  two

In  this  manuscript,  we  assess  the  error  associated  with  the

steps to be corrected, where; (a) a correction factor is applied to the

sensors themselves and how the position and fixing of the accel-

values in each axis to ensure both absolute ‘maxima’ per axis are the

erometer on the study animal affects acceleration metrics before

same and then (b) a gain is applied to both readings to convert them

proposing simple solutions to minimise these issues. Specifically,

to be exactly 1.0 g. Thus, for each axis used, the following equation

we  examine  the  variability  in  VeDBA  associated  with  improperly

is subtracted;

calibrated tri- axial accelerometers, using a case with humans walk-

ing defined courses at fixed speeds. We then examine how tag po-

sition affects VeDBA and signal amplitude using pigeons Columba

livia  flying  in  a  wind  tunnel  with  two  tags  in  different  locations

Valuex,y,zmin + Valuex,y,zmax
2

)

,

)

( (

on  their  back.  Finally,  we  perform  retrospective  analyses  of  two

where x, y and z refer to the three respective orthogonal axes. Then,

field studies to examine how different deployment protocols may

each  axis  is  multiplied  by  a  gain  value  that  scales  the  absolute  mini-

affect  accelerometer- based  results,  in;  (a)  red- tailed  tropicbirds

Phaethon rubricauda equipped with two different types of loggers

attached using marginally different protocols in separate seasons,

and (b) black- legged kittiwakes Rissa tridactyla equipped with tags

mum and maximum values to become 1.0 g. Thus, if xmin = −1.0 g and
xmax = 0.8 g, this gives; [(−1.0 + 0.8)/2] = −0.1. The xmin then becomes
−0.9 g and xmax = 0.9 g. The resultant would then be scaled by multiply-
ing by 1.0/0.9 = 1.1111 (Figure 1c).

either  on  the  back  or  on  the  tail,  as  two  positions  favoured  by

Subsequently, tags were deployed on 12 people, attached to the

seabird researchers for tag placement. Finally, we examined publi-

lower  back  using  elastic.  All  participants  were  healthy  adults  and

cations from biologists using accelerometers over the last 2 years

gave informed consent (protocol approved under code: PG201416A).

to  determine  how  many  of  them  had  indicated  an  accelerometer

Each person walked back and forth on a 25 m straight- line course

calibration protocol.

at  four  different  speeds  (0.69,  0.97,  1.25  and  1.53  m/s;  randomly

2  |  M ATE R I A L S A N D  M E TH O D S

ordered),  each  for  3  min.  Speeds  were  held  constant  using  a  met-
2)0.5

ronome. The mean VeDBA (defined as VeDBA = (xD
where xD, yD and zD are the dynamic body acceleration recorded by
each  of  the  three  channels  of  acceleration— for  details  see  Wilson

2 + yD

2 + zD

2.1  |  Measurement of acceleration accuracy of tri-
axial sensors

et al., 2020) was calculated across each 3- min trial with, and without,

the calibration corrections.

We  first  calibrated  tri- axial  accelerometers  within  five  Daily  Diary

tags (inch board) (Wildbyte Technologies, Swansea University, UK;

2.2  |  Effect of tag position on acceleration

Wilson et al., 2008), by setting them motionless on a table in a series

of defined orientations (each for c. 10 s). Six orientations (hereafter

The effect of tag position was first tested on three pigeons Columba

the ‘6- O method’) were chosen so that the tags always had one of

livia  flying  under  controlled  conditions  in  a  wind  tunnel  at  speeds

their  three  acceleration  axes  perpendicular  to  the  Earth's  surface

ranging from 10 to 22 m/s. Birds were equipped simultaneously with

and  these  were  rotated  according  to  the  six  axes  of  a  die  so  that

two tags recording acceleration at 150 Hz (‘Thumb’ Daily Diary [DD]

each  of  the  three  accelerometer  axes  nominally  reads  −1  and  1  g

units, hereafter type 1 tag). One tag was placed on the upper back,

(Figure 1a).

The outputs of these motionless calibrations were then used to

derive the six respective maxima of the acceleration vectorial sum

given by;

a

=

x2 + y2 + z2

0.5

,

�

‖

‖

�

the other on the lower back, both in the dorsal mid- line. Units meas-

ured 22 × 15 × 9 mm and the distance between them was c. 4 cm.
The  tagging  of  pigeons  and  the  procedure  of  flight  in  a  wind  tun-

nel was approved by the government of Upper Bavaria, ‘Sachgebiet

54— Verbraucherschutz, Veterinärwesen, 80538 München’ with the

record number: Gz.: 55.2- 1- 54- 2532- 86- 2015.

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License816 |   Methods in Ecology and Evolu(cid:13)on

(a)

(b)

)
g
(

m
u
s

l

a
i
r
o
t
c
e
v
n
o
(cid:25)
a
r
e
e
c
c
A

l

(c)

)
g
(

m
u
s

l

a
i
r
o
t
c
e
v
n
o
(cid:25)
a
r
e
e
c
c
A

l

F I G U R E   1 Simple, field viable six-  orientation calibration procedure for helping correct for accelerometer offset and gain errors. (a) Shows
the tag on a flat surface such as a table, with each of the six orientations uppermost (for periods of e.g. 5– 10 s). (b) Shows the raw vectorial
sum of the acceleration data of a typical tag rotated to adopt each of the six positions and (c) shows the same data after correction. In this
case, the respective offsets and gains for the three axes were; Ax (offset −0.027 g, gain 1.023 g), Az (offset −0.018 g, gain 1.021 g) and Ay
(offset 0.025 g, gain 1.000 g). Rotation of the tag at various angles led to pre- correction acceleration vectorial sums varying between 0.948
and 1.037 g. These reduced to between 0.996 and 1.007 g post- correction. Note how the correction process affects all acceleration data,
including such times as when the tag is moving appreciably (such as during rotation) and has centripetal and/or linear acceleration values
(manifest by the dips and peaks between flat tops)

To ensure that only steady sustained level flight was included in

affected by the difference in tag position, we analysed the accelera-

the analysis, we selected sections of consistent flapping flight last-

tion signals across average wingbeats in the three acceleration axes.

ing for at least 2 s (corresponding to c. 10 wingbeat cycles), with no

Each  acceleration  datapoint  was  attributed  to  a  percentage  pro-

gliding or wingbeat interruptions. The stability of the flight was con-

gression across the wingbeat cycle. Then, for every whole percent-

trolled  by  selecting  sections  where  VeDBA  values,  smoothed  over

age value, the heave, surge and sway accelerations were averaged

1 s, were between 0.75 and 3 g and varied by <1.0 g, with no appar-
ent trend (increasing or decreasing) over time. We also discarded the

first second of any flight.

across 10 wingbeats from the same logger. The average values for

the heave, surge and sway accelerations of the upper back- mounted

tag  were  expressed  against  the  values  of  the  lower  back- mounted

We first assessed whether the VeDBA values differed with tag

tag in a linear model, the slope of which was used to determine the

position.  VeDBA  was  calculated  using  a  2  s  smoothing  window  to

difference in signal amplitude between the two tags for each accel-

derive  the  ‘static’  component  (Shepard  et  al.,  2008)  and  then  sub-

eration axis.

tracting  static  values  from  the  raw  acceleration  data  in  each  axis,

To  examine  putative  changes  in  heave  signal  amplitude  (see

before  summing  the  differences  vectorially  (Qasem  et  al.,  2012).

above)  and  VeDBA  associated  with  tag  placement,  we  compared

We  then  assessed  whether  the  peak  amplitude  per  wingbeat  dif-

them between upper and lower back tags using a paired Student’s

fered according to tag location, with the peak amplitude calculated

t- test for VeDBA and a Wilcoxon signed- rank test for amplitude (due

as the difference between the maximum and the minimum value of

to non- homogeneous variances between the two groups [Levene’s

heave acceleration. For this, peaks were detected in the heave axis

(Bishop et al., 2015) to synchronise every wingbeat to a defined start

Test: F- value = 4.159, p = 0.049]). Wingbeat frequency also contrib-
utes to the variation of VeDBA (Van Walsum et al., 2020). Wingbeat

point. Finally, to understand which parts of the wingbeat signal were

frequency was also compared between the two tags using a paired

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

Methods in Ecology and Evolu(cid:13)on

    |  817

Student’s  t- test.  The  statistical  analysis  was  performed  in  RStudio,

Nineteen birds were tagged between February and March 2018

using r version 4.0.3 (R Core Team, 2020).

(using type 2 DDs, Figure 2) while 36 birds were tagged during the

2.3  |  Acceleration error in field studies

second season (September and October 2018, type 1 DDs, Figure 2).

Importantly,  during  the  second  season  though,  the  tags  were  at-

tached  using  only  three  strips  of  tape.  At  the  time,  this  was  con-

sidered  adequate  and  helped  reduce  the  weight  of  the  unit.  Both

As a post hoc example of how different deployment protocols may

units were set to the same sampling frequency (40 Hz). They were,

affect accelerometer- based results, we compared the amplitude of

however,  built  with  different  accelerometers  (type  1:  LSM9DS1,

the heave acceleration signal and VeDBA during the flight of black-

type  2:  LSM303DLHC,  STMicroelectronics,  Geneva,  Switzerland),

legged kittiwakes for two different setups. Twelve kittiwakes were

with  a  substantial  difference  in  sensitivity  (type  1:  0.061  mg,  type

captured  and  tagged  during  their  breeding  season  on  Middleton

Island,  Alaska  (59.43°N,  146.33°W)  and  equipped  with  an  acceler-

2: 1.0 mg sensitivity at ±2 g range). In addition, the accelerometer is
placed at the front of the type 1 unit, and at the back of the type 2

ometer (type 1 DD) placed under their tail, sealed inside heat shrink

unit, leading to an estimated distance of up to 1 cm between them

tubing for waterproofing: This method is popular as it prevents the

once placed on the bird’s back. The type 1 tags used in the second

bird from trying to preen off the package. We equipped four other

birds with the same tags placed on their back and wrapped in two

zip- lock  bags  to  protect  them  from  splash  damage,  while  allowing

season  were  slightly  lighter  (masses;  type  1  unit  =  25.0  g,  type  2
unit  = 27.7  g).  As  with  the  kittiwakes,  level  flapping  flight  was  se -
lected  to  discard  the  effect  of  gliding,  thermal  soaring  or  climbing

pressure  sensors  to  function:  This  other  method  is  particularly  fa-

on acceleration metrics (Williams et al., 2015). We considered level

voured in studies aiming to measure altitude, as it does not require

a full waterproofing, which alters pressure recordings. Tail- mounted

flapping flight to be any section where VeDBA >0.3 g and where the
rate of change of altitude (measured by the pressure sensor of the

tags were also tied to a GPS, while the back- mounted units were in

Daily Diary at 4 Hz) was between −0.5 and 0.5 m/s. To get an estima-

an independent package so that the back- mounted logger package

tion of flight effort that is not affected by signal amplitude, wingbeat

was 1 g heavier (total masses; tail = 21 g, back = 22 g). Two 1- min
sections of level flapping flight were identified for each tag and de-

frequency was also calculated for tropicbirds. Wingbeats were iden-

tified from peaks in the dynamic heave acceleration (dorsoventral),

ployment. The selection was made based on the altitude data from

smoothed over three events (0.075 s). Each segment from peak to

the loggers' pressure sensors (<5 m difference between the highest
and  lowest  altitude  measurements),  after  verifying  that  there  was

peak was counted as a wingbeat cycle, and their duration was used

to calculate wingbeat frequency.

no interruption in the wingbeat pattern found in heave, ascertaining

VeDBA, wingbeat frequency and the amplitude of heave in level

that the bird flapped regularly for the whole period.

flapping flight were derived from accelerometer data for both trop-

In a similar manner, we examined red- tailed tropicbird data from

icbirds and kittiwakes following the same process as pigeons. Data

two  different  nesting  seasons  using  tags  placed  in  a  standard  po-

were not paired, since birds carried one tag at a time, so non- paired

sition  on  their  lower  back  while  using  different  tags.  For  this,  red-

Student’s t- tests and Wilcoxon tests were used to compare the three

tailed tropicbirds at Round Island (19.85°S, 57.79°E) were captured

parameters between loggers.

on  their  nests  and  equipped  with  two  different  units  by  the  same

Since both the tropicbird and kittiwake data were collected from

person using four strips of Tesa tape placed under the feathers and

uncalibrated accelerometers (see above), a situation that we believe

around  the  tags  (Wilson  &  Wilson,  1989).  Ethical  permissions  for

represents  most  of  the  accelerometer  deployments  made  by  the

the use of biologgers on wild red- tailed tropicbirds and black- legged

community to date, we attempted to assess the potential for accel-

kittiwakes  were  granted  by  Swansea  University  AWERB,  permit

erometer error post hoc. We did this by measuring the variability in

040118/39 and 110619/1590 (IP- 1819- 18) respectively.

the vectorial sum at times when the tags were motionless (although

F I G U R E   2 (a) Location of the
accelerometer (interception point of
the three arrows depicting tri- axial
acceleration) on the circuit boards of two
different DD tags (the battery is in light
grey, the GPS in blue and the DD in green)
and (b) location of the accelerometers
within the tags on the back of a red- tailed
tropicbird for the type 1 (red dot) and type
2 (blue dot) tags

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License818 |   Methods in Ecology and Evolu(cid:13)on

not on the study animals) and in different tag orientations, finding up

to five different orientations per logger (e.g. when units were placed

inside bags and the bag placed on the floor/ground). The mean vec-

torial sum of the three axes of acceleration was calculated for each

orientation,  and  compared  between  loggers  and  between  tag  ver-

sions using two ANOVAs.

2.4  |  Calibration protocols within the literature

To examine the awareness of the scientific community about poten-

tial  for  variability  in  accelerometer  data  that  could  be  corrected  by

calibration, we searched the scientific literature from the past 3 years

(2019, 2020 and 2021) to find 100 papers which used accelerometers

on animals. The search was conducted on Google scholar, using the

keywords  ‘accelerometer’  and  ‘animal’.  We  examined  the  first  100

papers documenting deployments of accelerometers on animals, ex-

cluding reports and reviews of other people’s deployments, to note if

there was any mention of an accelerometer calibration process.

3  |  R E S U LT S

F I G U R E   3 Percentage difference between VeDBA values
derived during controlled speed trials with walking humans
using uncalibrated against calibrated (corrected) values. The
mean multiplier is one applied across all three axes and does
not represent the range of values between axes, which can be
considerably higher (see text)

p < 0.001, R2 = 0.97; Figure 4b). The sway model, however, showed
a weak fit (LM: Estimate = 0.18, p < 0.001, R2 = 0.18) and the slope
of their relationship was <1 (Figure 4d).

3.1  |  Measurement of acceleration accuracy of tri-
axial sensors

3.3  |  Effect of tag position on acceleration metrics

Static calibrations of the 15 separate accelerometers within the five

Differences in raw acceleration values also resulted in some varia-

tags  showed  that  axis  offsets  needed  corrections  up  to  between

tion  in  acceleration- derived  metrics  in  both  the  controlled  studies

−0.043 and 0.025 g and had multiplicative factors ranging between

on  pigeons  and  in  the  post  hoc  studies  on  wild  birds:  Upper  back-

0.97 and 1.023. Mean multipliers (across all three axes) for any one

mounted  tags  recorded  a  slightly  higher  VeDBA  than  lower  back-

tag ranged between 0.9933 and 1.0147.

In the walking speed trials with people, the minimum and max-

imum  differences  in  VeDBA  between  calibrated  and  uncalibrated

tags  for  any  one  participant  ranged  between  0.37%  and  5.04%.

mounted tags in pigeons (paired Student’s t- test: difference = −0.167,
t = −2.184, p = 0.043), which was largely due to higher heave values
(Wilcoxon signed- rank test: difference = 0.82 g, W = 94, p = 0.007)
(Figure 5a,d).

Mean  VeDBAs  per  participant  across  speeds  showed  that  the  dif-

In  red- tailed  tropicbirds,  the  type  1  tags,  used  during  the  sec-

ference between calibrated and uncalibrated tags could amount to

ond deployment, recorded both a higher VeDBA (by 25%) (Wilcoxon

2.5%  of  the  calibrated  reading.  Inspection  of  the  measures  under-

taken to calibrate each tag (see above) showed that the percentage

difference  between  the  uncalibrated  and  calibrated  was  primarily

due to the acceleration multiplicator (see above; Figure 3).

3.2  |  Effect of tag position on raw acceleration
in pigeons

In  our  controlled  study  with  pigeons,  plots  of  surge  versus  heave

test: difference = 0.14 g, W = 19, p < 0.001) and heave amplitude (by
29%) (Student’s t- test: difference = 0.40 g, t = −11.78, df = 47.718,
p < 0.001) than the type 2 tags (Figure 5b,e), despite there being no
evidence for a difference in body mass (Student’s t- test: t = 0.282,
p  =  0.779)  or  wing  area  (Student’s  t- test: t  =  −0.773,  p  =  0.446)
between  deployments.  In  kittiwakes,  the  tail  tags  recorded  both  a

higher VeDBA (by 18%) (Wilcoxon test: difference = 0.14 g, W = 14,
p = 0.001), and a higher heave amplitude (by 27%) (Student’s t- test:
difference = −0.60 g, t = −4.4304, df = 9.0178, p = 0.002) than the
back- mounted tags (Figure 5c,f).

acceleration showed how wingbeats under identical conditions re-

There  were  no  differences  in  estimated  wingbeat  frequency

turned markedly different profiles of acceleration depending on the

according  to  where  tags  were  mounted  in  either  pigeons  (paired

tag position (Figure 4a). We also found corresponding differences in

values of the heave and surge according to tag position (Figure 4b–

d):  the  upper  tag  recorded  a  lower  magnitude  of  surge  (LM:
Estimate = 0.76, p < 0.001, R2 = 0.41, with a slope < 1, Figure 4c), but
a higher magnitude of heave than the lower tag (LM: Estimate = 1.2,

Student’s t- test: t = 1.954, p = 0.067) or kittiwakes (Wilcoxon test:
W = 100, p = 0.227). In tropicbirds, there was a seasonal difference
in  wingbeat  frequency,  with  type  2  tags  recording  a  higher  wing-

beat frequency (by 3%) than the type 1 DDs (Student’s t- test: differ-

ence = −0.14 Hz, t = 3.72, df = 35.19, p < 0.001).

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseF I G U R E   4 (a) Plot of mean heave
versus surge acceleration through
time for a pigeon during an average
wingbeat cycle derived from a lower
back-  (red) and an upper back- mounted
tag (blue), both recording at 150 Hz.
Each point corresponds to a mean value
of acceleration calculated across all
flights for a given percentage through
the wingbeat, starting from the peak of
acceleration of the downstroke (black
point). The value of each point was
smoothed over a window of 10 points
(10%) to reduce noise. Regressions of the
upper against lower tag acceleration for
defined points throughout the wingbeat
cycle show; (b) heave, (c) surge and (d)
sway accelerations (note the changing axis
scales). The regression between the two
tags is represented in grey, and the y = x
line is shown in red

(a)

Methods in Ecology and Evolu(cid:13)on

    |  819

Time

(b)

(c)

(d)

We  found  a  positive  relationship  between  wingbeat  frequency

3.5  |  Calibration protocols within the literature

and  heave  amplitude  during  tropicbird  level  flapping  flight  (LMM,

season 1: estimate = 0.249, intercept = 0.254, SE = 0.021, t = 13.339,
p < 0.001; season 2: estimate = 0.746, intercept = −1.084, SE = 0.024,
t = 19.710, p < 0.001; R2
c = 0.72). The slope was, however,
steeper during season 2 (Figure 6), in line with the higher amplitude

m = 0.56, R2

Of  the  100  papers  examined,  only  five  mentioned  any  calibration

protocol  for  accelerometers  that  might  have  led  to  the  correction

of at least one of the sources of errors mentioned above (although

many were not explicit enough to be sure). No publication explicitly

of heave recordings (see Figure 5).

referred to all potential errors.

3.4  |  Post hoc quantification of
accelerometer inaccuracy

4  |  D I S C U S S I O N

This work highlights that there is currently virtually no discussion of

The  comparison  of  stationary  data  recorded  by  the  two  tag  types

acceleration calibration within the scientific literature even though

deployed on tropicbirds indicated that the vectorial sum was lower in

variation in acceleration measured by tags on flying birds (and pre-

the type 2 tag (Wilcoxon test: W = 98, p = 0.005, difference = 0.03 g;
Figure 7). Standard deviations of the vectorial sum (type 1: 0.03; type

sumably other animals engaged in any activity) can be due to; (i) dif-

ferences in sensitivity (Table SI1) and calibration between sensors,

2: 0.05) however, indicate that errors are more variable within type 2.

and that, in any event, variation occurs due to (ii) the placement of

We could not determine multipliers for the three acceleration chan-

the tag (or the sensor within the tag) as well as (iii) variation due to the

nels to calibrate the data based on this approach, as the heave and

animal  itself.  It  is  therefore  normal  to  attribute  all  variation  to  the

surge  channels  did  not  cover  the  whole  spectrum  of  their  possible

activity  of  the  animal  itself  but  the  validity  of  doing  this  is  criti-

distribution (−1 to 1 g) while the tag was motionless.

cally dependent on the other two factors. Indeed, as our work with

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License820 |   Methods in Ecology and Evolu(cid:13)on

(a)

(b)

(c)

(d)

(e)

(f)

F I G U R E   5 Comparison of VeDBA (a–  c) and heave signal amplitude (d– f) between tags in pigeons (a, d), red- tailed tropicbirds (b, e) and
black- legged kittiwakes (c, f). Bold horizontal lines indicate the median vectorial sum for each tag, extremes of the box the upper and lower
quartiles, and whiskers the extreme values (excluding outliers, represented by open circles). Notches represent 1.58 IQR/√n (n being the
number of observations) on either side of the median and suggest a significant difference when they do not overlap

F I G U R E   6 Relationship between the
wingbeat frequency and heave amplitude
of red- tailed tropicbirds during two field
seasons. Birds were equipped with type
2 tags in season 1 (red) and type 1 tags
in season 2 (blue). In season 2, tags were
attached using one less strip of tape,
which could reduce tag stability. Full lines
represent the linear relationship between
wingbeat frequency and amplitude and
dashed lines the confidence intervals

tropicbirds shows, multiple influences can interact and make it hard,

The  variation  in  acceleration  is  used  to  examine  animal  be-

if not impossible, to separate causes from effects in acceleration sig-

haviour  within  a  multitude  of  research  thrusts,  some  of  which  use

natures. Studies that do not consider points (i) and (ii) may, therefore,

acceleration  data  in  slightly  different  ways.  These  range  from  the

be  misrepresenting  animal  activity  both  in  terms  of  intensity  and

precise definition of heave, surge or sway values, or their derivatives

extent. We propose an easy, rapid calibration method, that can be

(such as pitch and roll and DBA), which can be used in algorithms to

conducted at a field site with minimal equipment, and substantially

identify behaviours (e.g. Fehlmann et al., 2017; Nathan et al., 2012)

reduces  sensor- induced  errors.  We  also  provide  recommendations

through the use of acceleration- derived metrics to define energy ex-

about tag attachment methods to avoid interpreting tag position ef-

penditure (in e.g. doubly labelled water vs. DBA regressions; Pagano

fects as biologically meaningful.

& Williams, 2019), to measure travelling speed (Bidder et al., 2012;

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMethods in Ecology and Evolu(cid:13)on

    |  821

F I G U R E   7 Comparison of the vectorial
sum of the raw acceleration recorded
by various immobile type 1 (dark boxes)
and type 2 tags (light boxes). Each point
corresponds to a different unknown
orientation. Thick black lines indicate
the median vectorial sum for each tag,
extremes of the box the upper and lower
quartiles, and whiskers the extreme values
(excluding outliers)

Gunner et al., 2021) and studies looking at animal effort over time

speed must be very slow. Using this calibration will therefore allow

and space (Duriez et al., 2018; Halsey et al., 2011). Errors due to sen-

researchers to ascribe the most substantive variation in acceleration

sor inaccuracy and differences in placement are most severe when

signal to specific axes.

axes are considered individually (e.g. deriving pitch from the surge

Our suggestion of dealing with errors post hoc by looking at the

axis). However, they are also relevant when all three orthogonal axes

vectorial sum of the acceleration when tags were stationary could

are considered, as inaccuracies in one axis can either be mitigated or

not be used to correct the various axes in our study because all six

compounded by inaccuracies in another (see Figure 3). Within vec-

orientations required for the calibrations were not known, and the

torial (or absolute) sums of acceleration metrics, the overall error will

study subjects did not adopt the appropriate postures. However, this

depend on the relative errors of  the different axes and the extent

process does at least serve to indicate some of the extent of devi-

to which they vary during the activity in question. For example, in

ation of the sensors from the expected range (see Figure 5). In this

flapping birds or bats, almost all variation in acceleration measures

regard,  we  note  that  we  have  presented  results  in  this  work  from

occur in the heave and surge axes (e.g. Wilson et al., 2008, and see

only one tag manufacturer (type 1 and type 2 tags use two different

Figure 4a– d) so errors in the sway are less important. Cognisance of

chips; the type 1 is far superior having a sensitivity of 0.061 mg [in a

the axis- specific errors will help mitigate those errors that could be

interpreted as a biological effect.

range of ±2 g], while the type 2 only has a sensitivity of 1 mg for this
range), but we have measured, in passing, more substantive variation

by other manufacturers (see Table SI1).

4.1  |  Calibrations

The issue of inaccurate sensors can be at least partially mitigated by

the 6- O method suggested in this work, although we note that this

4.2  |  Why does accelerometer position affect
acceleration?

only  effectively  calibrates  between  −1  and  1  g,  while  the  gravita-

The position of an accelerometer on an animal should affect the ac-

tional  component  experienced  by  some  animals,  for  example,  dur-

celeration  perceived  by  the  sensor  during  movement  according  to

ing  turning  (Wilson  et  al.,  2013),  will  increase  beyond  these  limits.

its location, and indeed that is the basis behind many biomechani-

Although, ideally, the tags should be calibrated with each of the ac-

cal studies (e.g. Giansanti et al., 2003; Hyde et al., 2008). However,

celerometer  axes  held  perfectly  vertically  (something  that  is  chal-

there  is  poor  appreciation  in  the  behavioural  ecology  community

lenging to do once a circuit board is potted in a housing), in practice,

that this premise is also valid for trunk- mounted tags. This may seem

this is not critical, and holding the axes as close to vertical as possi-

irrelevant for birds where the thorax can be considered a single im-

ble should suffice. This is because the response of an accelerometer

mobile unit, in contrast to bead- string models that may indicate what

to the static acceleration of the earth’s gravity follows a sine wave

is expected in species with a flexible back (Underhill & Doyle, 2006).

so  that  an  accelerometer  that  is  placed  10°  off  the  vertical  (i.e.  at

Our work has shown, however, that the location of trunk- mounted

80°), reads a value that is 98.5% of the full- scale value that would

accelerometers  on  birds  does  play  a  role  in  modulating  accelera-

be  given  if  the  accelerometer  axis  were  held  perfectly  vertical  (so

tion values (Figure 4) and this is presumably because the bird body

that  if  there  is  an  error  in  this  axis,  98.5%  of  it  will  be  covered  by

pitches during the wingbeat cycle (although part of the differences

this orientation). If it is impossible to reliably estimate the angle of

that we observed may also be due to the movement of the scapulae

the logger because of the housing, for instance, gently rotating the

and perhaps the neck during flapping). Depending on the degree of

logger around in every direction would be needed to cover all six ori-

pitch,  the  centre  of  pitch  rotation  and  the  position  of  the  acceler-

entations, although this process is particularly sensitive to centrip-

ometer, this will change the extent of movement (d), which can be

etal acceleration, which is added to the static signal, so the rotation

defined  by  the  length  of  a  section  of  a  circumference  around  the

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License822 |   Methods in Ecology and Evolu(cid:13)on

centre point of rotation according to D = 2πr(360/P), where r is the
radius or distance between the centre of pitch rotation and the sen-

appears  unlikely,  as  higher  signal  amplitudes  were  recorded  in  the

season with lower wingbeat frequencies, despite the fact that these

sor, and P is the maximum pitch angle (in degrees). The duration of

parameters are positively correlated within each season (Figure 6).

the  wingbeat  cycle  will  define  the  vertical  speed  of  the  tag  at  its

It therefore appears that the factors driving seasonal differences in

location, with the recorded acceleration being the change in speed

signal amplitude are different to those driving seasonal changes in

over time. The formula shows how the effect of changed accelera-

wingbeat frequency.

tion will be more prominent with increasing distance of a tag from

The difference in signal amplitude may also arise due to changes

the centre point of rotation and so will have the greatest potential

in  the  stability  of  the  tag  attachment  between  seasons.  Wilson

to  vary  in  larger  birds,  all  other  things  being  equal.  This  may  also

et  al.  (2021)  note  how  accelerometers  in  loosely  fitted  collars  on

account  for  the  changed  acceleration  metrics  in  tail-   versus  body-

terrestrial  mammals  provide  a  signal  that  varies  with  collar  tight-

mounted tags (Figure 5c,f) in our kittiwake study, although part of

ness.  Although  the  use  of  tape  to  attach  devices  to  birds  (Wilson

that is presumably due to the relative instability of the tail. In fact,

et al., 1997) provides a much more intimate association between the

to  our  knowledge,  there  is  little  information  on  the  extent  of  bird

tag  and  the  bird  body,  we  believe  that  if  this  method  is  not  stan-

body change in pitch during flight (but see Su et al., 2012; Tobalske &

dardised (and it was not in our study, as the amount of tape varied

Dial, 1996) although controlled experiments with multiple calibrated

between seasons), it can lead to major variation in acceleration val-

accelerometers could change that. In the meantime, we suggest that

ues, particularly in animals with highly dynamic movement, such as

users attempt to place accelerometers in identical positions on their

flight. In birds, this issue may be exacerbated by tag movement due

study animals for comparative purposes, which should also involve

to air flow over the body which can cause the device to vibrate more

knowing the position of the sensors within the tags rather than just

or less depending on attachment (cf. Wilson et al., 2020). It is also

considering the tags themselves (Figures 1 and 3).

germane  to  consider  that  the  stability  of  the  tag  attachment  may

Fortunately,  there  is  no  a  priori  reason  why  tags  placed  differ-

change  over  time  in  longer- term  deployments.  These  issues  have

ently on a bird thorax or inaccurate accelerometers should affect de-

long been recognised in the wearable sensors industry for humans

termination of wingbeat frequency since points of inflection will still

(Jayasinghe  et  al.,  2019).  Consequently,  we  cannot,  in  good  faith,

be represented correctly with respect to time within the wingbeat

compare  VeDBA  or  wingbeat  amplitudes  of  tropicbirds  between

cycle (Figure 4a,b). Indeed, this is what we observed in our controlled

seasons, although the wingbeat frequency will be unaffected by the

pigeon flight trials and in the kittiwakes (despite a small difference in

attachment procedure, tag position or sensor inaccuracies.

tag mass, see Whelan et al., 2021). In contrast, the tropicbird work

indicates that there was a real change in wingbeat frequency across

the two seasons, and this seems to be related to changes in environ-

5  |  CO N C LU S I O N S

mental conditions (Garde et al., in prep).

4.3  |  Post hoc studies and differences
between tags

Accelerometer inaccuracies can result in errors in the raw accelera-

tion of up to 5% per axis and, depending on the extent and direction

of the errors across all three orthogonal axes, this can affect DBA

metrics accordingly. Tag placement can also result in errors in DBA

metrics  of  up  to  9.7%  in  flapping  flight  for  our  units,  although  we

The bigger question is the extent to which observed differences in

note that the scale of the errors varies between device types. Finally,

uncalibrated accelerometers can be attributed to the animals rather

non- standardised  tag  attachment  procedures  can  result  in  highly

than to tag position, attachment techniques or sensor variability. In

variable  dynamic  acceleration  values.  Taken  together,  these  repre-

our  tropicbird  example,  the  differences  in  VeDBA  and  signal  am-

sent a potentially important source of error in both raw acceleration

plitude were not consistent with the differences found in pigeons,

values,  which  are  commonly  used  to  calculate  body  pitch  and  roll

where higher values were recorded in the upper tag. This suggests

and/or  as  parameters  to  define  particular  behaviours,  and  derived

that the variation in signal amplitude in tropicbirds was not related to

metrics  such  as  DBA.  Attachment  procedures  should  be  adapted

tag position. Furthermore, the difference in amplitude was appreci-

to  the  species  tagged,  as  the  effect  of  different  tag  placements

ably larger between the two tag types on tropicbirds, than between

may  vary  from  one  species  to  the  other  (e.g.  Kölzsch  et  al.,  2016;

the upper and lower tags used in pigeons, even though the tropicbird

Vandenabeele  et  al.,  2014),  and  to  the  study,  as  different  metrics

tags were placed in a way that minimised the distance between their

may be measured more reliably using one particular method (Kölzsch

respective accelerometers. The scale of the variability is not consist-

et  al.,  2016),  making  the  use  of  a  standardised  procedure  difficult.

ent with that caused by uncalibrated sensors, as the difference be-

Animal disturbance and study purposes should be considered before

tween vectorial sum values in 6- O calibrated tags and uncalibrated

adjusting tag placement for the compatibility of datasets, and there-

tags (in general) amounted to a mean maximum of 2.5%. In contrast,

fore, researchers should be aware of the attachment methods used

in  flapping  flight,  the  difference  in  VeDBA  between  tags  and  sea-

to compare acceleration metrics between studies reliably (Sequeira

sons  reached  25%.  This  order  of  magnitude  difference  might  ap-

et  al.,  2021).  Importantly,  we  highlight  that  sensor  inaccuracy  can

pear to indicate seasonal changes in flight effort. However, this also

be  largely  mitigated  by  performing  a  rapid  calibration.  There  is

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMethods in Ecology and Evolu(cid:13)on

    |  823

therefore a need for researchers to undertake such calibrations prior

R E F E R E N C E S

to each deployment and include this in their archived data as well as

to standardise their tag attachment procedure as much as possible.

The last decade has been hailed as a golden age in biologging, due to

the availability of powerful sensors in animal- attached technologies.

The  data  repositories  that  archive  these  data  represent  extremely

valuable  resources  for  the  community  (e.g.  Davidson  et  al.,  2020),

but  there  is  an  urgent  need  for  calibrations  that  allow  data  to  be

standardised in order for their full potential to be realised now and

in the years to come.

AC K N OW L E D G E M E N T S

Special  thanks  to  Jenna  Schlener  and  Charlotte  Rees- Roderick  for

their contribution to the kittiwake and the wind tunnel studies, re-

spectively, as well as to the participants of the walking experiment.

We  are  grateful  to  the  National  Parks  and  Conservation  Service,

Government of Mauritius, who provided permission to access Round

Island  to  tag  red- tailed  tropicbirds.  This  work  was  funded  by  the

European Research Council starter grant 715874 to ELCS, under the

European Union’s Horizon 2020 research and innovation program.

C O N FL I C T O F I N T E R E S T

We declare we have no competing interests.

AU T H O R S '  C O N T R I B U T I O N S

Red- tailed  tropicbird  data  were  collected  by  A.F.,  N.C.  and  V.T.;

Human data were collected by K.A.R.R., R.P.W. and R.S.M.; Pigeon

data  were  collected  by  H.R.  and  E.L.C.S.  under  the  supervision  of

M.W.; Black- legged kittiwake data were collected by B.G., F.T., S.W.

and K.H.E.; M.D.H. designed the tags used in this study and provided

technical information about accelerometers; Data analysis was car-

ried  out  by  R.P.W.  and  B.G.;  Calibrations  were  designed  by  R.P.W.

and M.D.H.; The manuscript was written by B.G., R.P.W. and E.L.C.S.

All authors contributed to the revision of the manuscript, gave final

approval  for  publication  and  agree  to  be  held  accountable  for  the

work performed therein.

P E E R R E V I E W

The peer review history for this article is available at <https://publo>

ns.com/publo n/10.1111/2041- 210X.13804.

DATA  AVA I L A B I L I T Y S TAT E M E N T

Data  and  code  used  for  the  analyses  of  this  manuscript  are  avail-

able from the Dryad Digital Repository <https://datad> ryad.org/stash/

datas et/doi:10.5061/dryad.f7m0c fxwj (Garde et al., 2022).

O R C I D

Baptiste Garde

 <https://orcid.org/0000-0002-8726-6279>

Rory P. Wilson

 <https://orcid.org/0000-0003-3177-0107>

Kayleigh A. R. Rose

 <https://orcid.org/0000-0001-7023-2809>

Martin Wikelski

 <https://orcid.org/0000-0002-9790-7025>

Shannon Whelan

 <https://orcid.org/0000-0003-2862-327X>

Emily L. C. Shepard

 <https://orcid.org/0000-0001-7325-6398>

Batista, P., Silvestre, C., Oliveira, P., & Cardeira, B. (2011). Accelerometer
calibration and dynamic bias and gravity estimation: Analysis, de-
sign,  and  experimental  evaluation.  IEEE  Transactions  on  Control
Systems  Technology,  19(5),  1128– 1137.  <https://doi.org/10.1109/>
TCST.2010.2076321

Baumel,  J.  J.  (1993).  Handbook  of  avian  anatomy:  Nomina  anatomica
avium.  In  Publications  of  the  Nuttall  Ornithological  Club  (USA),
No. 23.

Beravs,  T.,  Podobnik,  J.,  &  Munih,  M.  (2012).  Three- axial  accelerom-
eter  calibration  using  Kalman  filter  covariance  matrix  for  online
estimation  of  optimal  sensor  orientation.  IEEE  Transactions  on
Instrumentation and Measurement, 61(9), 2501– 2511.

Bidder,  O.  R.,  Qasem,  L.  A.,  &  Wilson,  R.  P.  (2012).  On  higher  ground:
How well can dynamic body acceleration determine speed in vari-
able  terrain?  PLoS  ONE,  7(11),  e50556.  <https://doi.org/10.1371/>
journ al.pone.0050556

Bishop, C. M., Spivey, R. J., Hawkes, L. A., Batbayar, N., Chua, B., Frappell,
P.  B.,  Milsom,  W.  K.,  Natsagdorj,  T.,  Newman,  S.  H.,  Scott,  G.  R.,
Takekawa,  J.  Y.,  Wikelski,  M.,  &  Butler,  P.  J.  (2015).  The  roller
coaster  flight  strategy  of  bar- headed  geese  conserves  energy
during Himalayan migrations. Science, 347(6219), 250– 254. https://
doi.org/10.1126/scien ce.1258732

Bograd, S., Block, B., Costa, D., & Godley, B. (2010). Biologging technolo-
gies: New tools for conservation. Introduction. Endangered Species
Research, 10, 1– 7. <https://doi.org/10.3354/esr00269>

Cade,  D.  E.,  Gough, W.  T.,  Czapanskiy,  M.  F.,  Fahlbusch,  J.  A.,  Kahane-
Rapport,  S.  R.,  Linsky,  J.  M.  J.,  Nichols,  R.  C.,  Oestreich,  W.  K.,
Wisniewska, D. M., Friedlaender, A. S., & Goldbogen, J. A. (2021).
Tools  for  integrating  inertial  sensor  data  with  video  bio- loggers,
including  estimation  of  animal  orientation,  motion,  and  position.
Animal Biotelemetry, 9(1), 1– 21.

Chakravarty, P., Cozzi, G., Ozgul, A., & Aminian, K. (2019). A novel biome-
chanical approach for animal behaviour recognition using acceler-
ometers. Methods in Ecology and Evolution, 10(6), 802– 814. https://
doi.org/10.1111/2041- 210X.13172

Davidson,  S.  C.,  Bohrer,  G.,  Gurarie,  E.,  LaPoint,  S.,  Mahoney,  P.  J.,
Boelman, N. T., Eitel, J. U. H., Prugh, L. R., Vierling, L. A., Jennewein,
J., Grier, E., Couriot, O., Kelly, A. P., Meddens, A. J. H., Oliver, R. Y.,
Kays, R., Wikelski, M., Aarvak, T., Ackerman, J. T., … Hebblewhite,
M. (2020). Ecological insights from three decades of animal move-
ment  tracking  across  a  changing  Arctic.  Science,  370(6517),  712–
715. <https://doi.org/10.1126/scien> ce.abb7080

Duriez, O., Peron, G., Gremillet, D., Sforzi, A., & Monti, F. (2018). Migrating
ospreys use thermal uplift over the open sea. Biology Letters, 14(12),
20180687. <https://doi.org/10.1098/rsbl.2018.0687>

Elliott,  K.  H.  (2016).  Measurement  of  flying  and  diving  metabolic  rate
in  wild  animals:  Review  and  recommendations.  Comparative
Biochemistry and Physiology Part A: Molecular & Integrative Physiology,
202, 63– 77. <https://doi.org/10.1016/j.cbpa.2016.05.025>

Fehlmann,  G.,  O’Riain,  M.  J.,  Hopkins,  P.  W.,  O’Sullivan,  J.,  Holton,
M. D., Shepard, E. L. C., & King, A. J. (2017). Identification of be-
haviours from accelerometer data in a wild social primate. Animal
Biotelemetry, 5(1), 6. <https://doi.org/10.1186/s4031> 7- 017- 0121- 3

Field,  I.  C.,  Harcourt,  R.  G.,  Boehme,  L.,  De  Bruyn,  P.  J.  N.,  Charrassin,
J.  B.,  McMahon,  C.  R.,  Bester,  M.  N.,  Fedak,  M.  A.,  &  Hindell,
M.  A.  (2011).  Refining  instrument  attachment  on  phocid  seals.
Marine Mammal Science, 28(3), E325– E332.

Garde,  B.,  Wilson,  R.  P.,  Fell,  A.,  Cole,  N.,  Tatayah,  V.,  Holton,  M.  D.,
Wikelski,  M.,  Tremblay,  F.,  Whelan,  S.,  Elliott,  K.  H.,  &  Shepard,
E.  L.  C.  (2022).  Data  from:  Ecological  inference  using  data  from
accelerometers  needs  careful  protocols.  Dryad  Data  Repository,
<https://doi.org/10.5061/dryad.f7m0c> fxwj

Giansanti, D., Macellari, V., Maccioni, G., & Cappozzo, A. (2003). Is it feasi-
ble to reconstruct body segment 3- D position and orientation using

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License824 |   Methods in Ecology and Evolu(cid:13)on

accelerometric  data?  IEEE  Transactions  on  Biomedical  Engineering,
50(4), 476– 483.

Gudka, M., Santos, C. D., Dolman, P. M., Abad- Gómez, J. M., & Silva, J.
P. (2019). Feeling the heat: Elevated temperature affects male dis-
play activity of a lekking grassland bird. PLoS ONE, 14(9), e0221999.
<https://doi.org/10.1371/journ> al.pone.0221999

Gunner,  R.  M.,  Holton,  M.  D.,  Scantlebury,  M.  D.,  van  Schalkwyk,  L.,
English,  H.  M.,  Williams,  H.  J.,  Börger,  L.,  Redcliffe,  J.,  Yoda,  K.,
Yamamoto, T., Ferreira, S., Govender, D., Viljoen, P., Bruns, A., Bell,
S. H., Marks, N., & Wilson, R. P. (2021). Dead- reckoning animal move-
ments in R– A reappraisal using Gundog. Tracks.

Halsey, L. G., Shepard, E. L. C., Quintana, F., Gomez Laich, A., Green, J. A., &
Wilson, R. P. (2009). The relationship between oxygen consumption
and body acceleration in a range of species. Comparative Biochemistry
and Physiology Part A: Molecular & Integrative Physiology, 152(2), 197–
202. <https://doi.org/10.1016/j.cbpa.2008.09.021>

Halsey,  L.  G.,  Shepard,  E.  L.  C.,  &  Wilson,  R.  P.  (2011).  Assessing  the
development  and  application  of  the  accelerometry  technique  for
estimating  energy  expenditure.  Comparative  Biochemistry  and
Physiology -  A Molecular and Integrative Physiology, 158(3), 305– 314.
<https://doi.org/10.1016/j.cbpa.2010.09.002>

Harel, R., Spiegel, O., Getz, W. M., & Nathan, R. (2017). Social foraging
and  individual  consistency  in  following  behaviour:  Testing  the  in-
formation Centre hypothesis in free- ranging vultures. Proceedings
of  the  Royal  Society  B:  Biological  Sciences,  284(1852),  20162654.
<https://doi.org/10.1098/rspb.2016.2654>

Hyde,  R.  A.,  Ketteringham,  L.  P.,  Neild,  S.  A.,  &  Jones,  R.  J.  S.  (2008).
Estimation of upper- limb orientation based on accelerometer and gy-
roscope  measurements.  IEEE Transactions on Biomedical Engineering,
55(2), 746– 754. <https://doi.org/10.1109/TBME.2007.912647>

Jayasinghe, U., Harwin, W. S., & Hwang, F. (2019). Comparing clothing-
mounted sensors with wearable sensors for movement analysis and
activity  classification.  Sensors,  20(1),  82.  <https://doi.org/10.3390/>
s2001 0082

Kokubun,  N.,  Kim,  J.- H.,  Shin,  H.- C.,  Naito,  Y.,  &  Takahashi,  A.  (2011).
Penguin  head  movement  detected  using  small  accelerometers:
A  proxy  of  prey  encounter  rate.  Journal  of  Experimental  Biology,
214(22), 3760– 3767. <https://doi.org/10.1242/jeb.058263>

Kölzsch,  A.,  Neefjes,  M.,  Barkway,  J.,  Müskens,  G.  J.  D.  M.,  van
Langevelde,  F.,  de  Boer,  W.  F.,  Prins,  H.  H.  T.,  Cresswell,  B.  H.,  &
Nolet, B. A. (2016). Neckband or backpack? Differences in tag de-
sign and their effects on GPS/accelerometer tracking results in large
waterbirds.  Animal Biotelemetry,  4(1),  13.  <https://doi.org/10.1186/>
s4031 7- 016- 0104- 9

Kranstauber,  B.,  Cameron,  A.,  Weinzerl,  R.,  Fountain,  T.,  Tilak,  S.,
Wikelski, M., & Kays, R. (2011). The Movebank data model for an-
imal tracking. Environmental Modelling & Software, 26(6), 834– 835.
<https://doi.org/10.1016/j.envso> ft.2010.12.005

Nathan, R., Spiegel, O., Fortmann- Roe, S., Harel, R., Wikelski, M., & Getz,
W. M. (2012). Using tri- axial acceleration data to identify behavioral
modes  of  free- ranging  animals:  General  concepts  and  tools  illus-
trated  for  griffon  vultures.  Journal  of  Experimental  Biology,  215(6),
986– 996. <https://doi.org/10.1242/jeb.058602>

Nickel, B. A., Suraci, J. P., Nisi, A. C., & Wilmers, C. C. (2021). Energetics and
fear of humans constrain the spatial ecology of pumas. Proceedings
of  the  National  Academy  of  Sciences  of  the  United  States  of  America,
118(5), e2004592118. <https://doi.org/10.1073/pnas.20045> 92118
Novák, P. (2010). High resolution constituents of the Earth's gravitational
field.  Surveys  in  Geophysics,  31(1),  1– 21.  <https://doi.org/10.1007/>
s1071 2- 009- 9077- z

Pagano, A. M., & Williams, T. M. (2019). Estimating the energy expendi-
ture  of  free- ranging  polar  bears  using  tri- axial  accelerometers:  A
validation  with  doubly  labeled  water.  Ecology  and  Evolution,  9(7),
4210– 4219. <https://doi.org/10.1002/ece3.5053>

decreases  with  increasing  anthropogenic  disturbance.  Marine  Biology,
162(3), 539– 546. <https://doi.org/10.1007/s00227-> 014- 2603- 7
Qasem,  L.,  Cardew,  A.,  Wilson,  A.,  Griffiths,  I.,  Halsey,  L.  G.,  Shepard,
E. L. C., Gleiss, A. C., & Wilson, R. (2012). Tri- axial dynamic accel-
eration  as  a  proxy  for  animal  energy  expenditure;  should  we  be
summing values or calculating the vector? PLoS ONE, 7(2), e31187.
<https://doi.org/10.1371/journ> al.pone.0031187

R Core Team. (2020). R: A language and environment for statistical comput-

ing. Retrieved from <https://www.r-> proje ct.org/

Ropert- Coudert,  Y.,  Grémillet,  D.,  Ryan,  P.,  Kato,  A.,  Naito,  Y.,  &  Le
Maho,  Y.  (2003).  Between  air  and  water:  The  plunge  dive  of  the
cape  gannet  Morus  capensis.  Ibis,  146(2),  281– 290.  <https://doi>.
org/10.1111/j.1474- 919x.2003.00250.x

Ruzza, G., Guerriero, L., Revellino, P., & Guadagno, F. M. (2018). Thermal
compensation of low- cost MEMS accelerometers for tilt measure-
ments. Sensors, 18(8), 2536. <https://doi.org/10.3390/s1808> 2536

Sequeira, A. M. M., O’Toole, M., Keates, T. R., McDonnell, L. H., Braun,
C. D., Hoenner, X., Jaine, F. R. A., Jonsen, I. D., Newman, P., Pye, J.,
Bograd, S. J., Hays, G. C., Hazen, E. L., Holland, M., Tsontos, V. M.,
Blight, C., Cagnacci, F., Davidson, S. C., Dettki, H., … Weise, M. (2021).
A standardisation framework for bio- logging data to advance eco-
logical research and conservation. Methods in Ecology and Evolution,
12(6), 996– 1007. <https://doi.org/10.1111/2041-> 210X.13593
Shepard,  E.,  Wilson,  R.,  Quintana,  F.,  Gómez  Laich,  A.,  Liebsch,  N.,
Albareda, D., Halsey, L. G., Gleiss, A., Morgan, D. T., Myers, A. E.,
Newman, C., & McDonald, D. (2008). Identification of animal move-
ment  patterns  using  tri- axial  accelerometry.  Endangered  Species
Research, 10(1), 47– 60. <https://doi.org/10.3354/esr00084>

Sipos, M., Paces, P., Rohac, J., & Novacek, P. (2011). Analyses of triaxial
accelerometer  calibration  algorithms.  IEEE  Sensors  Journal,  12(5),
1157– 1165.

Su,  J.- Y.,  Ting,  S.- C.,  Chang,  Y.- H.,  &  Yang,  J.- T.  (2012).  A  passerine
spreads  its  tail  to  facilitate  a  rapid  recovery  of  its  body  posture
during hovering. Journal of the Royal Society Interface, 9(72), 1674–
1684. <https://doi.org/10.1098/rsif.2011.0737>

Tobalske,  B.  W.,  &  Dial,  K.  P.  (1996).  Flight  kinematics  of  black- billed
magpies  and  pigeons  over  a  wide  range  of  speeds.  Journal  of
Experimental Biology, 199(2), 263– 280.

Underhill,  P.  T.,  &  Doyle,  P.  S.  (2006).  Alternative  spring  force  law  for
bead- spring  chain  models  of  the  worm- like  chain.  Journal  of
Rheology, 50(4), 513– 529. <https://doi.org/10.1122/1.2206713>
Van Walsum, T. A., Perna, A., Bishop, C. M., Murn, C. P., Collins, P. M.,
Wilson, R. P., & Halsey, L. G. (2020). Exploring the relationship be-
tween flapping behaviour and accelerometer signal during ascend-
ing  flight,  and  a  new  approach  to  calibration.  Ibis,  162(1),  13– 26.
<https://doi.org/10.1111/ibi.12710>

Vandenabeele, S. P., Grundy, E., Friswell, M. I., Grogan, A., Votier, S. C., &
Wilson, R. P. (2014). Excess baggage for birds: Inappropriate place-
ment  of  tags  on  gannets  changes  flight  patterns.  PLoS  ONE,  9(3),
e92657. <https://doi.org/10.1371/journ> al.pone.0092657

Whelan,  S.,  Hatch,  S.  A.,  Benowitz- Fredericks,  Z.  M.,  Parenteau,  C.,
Chastel,  O.,  &  Elliott,  K.  H.  (2021).  The  effects  of  food  supply  on
reproductive hormones and timing of reproduction in an income-
breeding seabird. Hormones and Behavior, 127, 104874. <https://doi>.
org/10.1016/j.yhbeh.2020.104874

Williams,  H.  J.,  Shepard,  E.  L.  C.,  Duriez,  O.,  &  Lambertucci,  S.  A.
(2015).  Can  accelerometry  be  used  to  distinguish  between  flight
types in soaring birds? Animal Biotelemetry, 3(1), 1– 11. <https://doi>.
org/10.1186/s4031 7- 015- 0077- 0

Wilson,  J.  W.,  Mills,  M.  G.  L.,  Wilson,  R.  P.,  Peters,  G.,  Mills,  M.  E.  J.,
Speakman,  J.  R.,  Durant,  S.  M.,  Bennett,  N.  C.,  Marks,  N.  J.,  &
Scantlebury,  M.
jubatus,  balance
(2013).  Cheetahs,  Acinonyx
turn  capacity  with  pace  when  chasing  prey.  Biology  Letters,  9(5),
20130620. <https://doi.org/10.1098/rsbl.2013.0620>

Payne,  N.  L.,  van  der  Meulen,  D.  E.,  Suthers,  I.  M.,  Gray,  C.  A.,  &  Taylor,
M. D. (2015). Foraging intensity of wild mulloway Argyrosomus japonicus

Wilson,  R.  P.,  Börger,  L.,  Holton,  M.  D.,  Scantlebury,  D.  M.,  Gómez-
Laich, A., Quintana, F., Rosell, F., Graf, P. M., Williams, H., Gunner,

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseR., Hopkins, L., Marks, N., Geraldi, N. R., Duarte, C. M., Scott, R.,
Strano, M. S., Robotka, H., Eizaguirre, C., Fahlman, A., & Shepard,
E. L. C. (2020). Estimates for energy expenditure in free- living an-
imals  using  acceleration  proxies:  A  reappraisal.  Journal  of  Animal
Ecology, 89(1), 161– 172. <https://doi.org/10.1111/1365-> 2656.13040
Wilson,  R.  P.,  Holton,  M.,  Wilson,  V.  L.,  Gunner,  R.,  Tysse,  B.,  Wilson,
G. I., Quintana, F., Duarte, C., & Scantlebury, D. M. (2019). Towards
informed metrics for examining the role of human- induced animal
responses in tag studies on wild animals. Integrative Zoology, 14(1),
17– 29. <https://doi.org/10.1111/1749-> 4877.12328

Wilson, R. P., Pütz, K., Peters, G., Culik, B., Scolaro, J. A., Charrassin, J.- B.,
&  Ropert- Coudert,  Y.  (1997).  Long- term  attachment  of  transmit-
ting and recording devices to penguins and other seabirds. Wildlife
Society Bulletin, 25, 101– 106.

Wilson, R. P., Rose, K. A., Gunner, R., Holton, M. D., Marks, N. J., Bennett,
N. C., Bell, S. H., Twining, J. P., Hesketh, J., Duarte, C. M., Bezodis,
N.,  Jezek,  M.,  Painter,  P.,  Silovsky,  V.,  Crofoot,  M.  C.,  Harel,  R.,
Arnould, J. P. Y., Allan, B. M., Whisson, D. A., … Scantlebury, D. M.
(2021). Animal lifestyle changes acceptable mass limits for attached
tags. BioRxiv, 441641. <https://doi.org/10.1101/2021.04.27.441641>
Wilson,  R.  P.,  Shepard,  E.  L.  C.,  &  Liebsch,  N.  (2008).  Prying  into  the  inti-
mate details of animal lives: Use of a daily diary on animals. Endangered
Species Research, 4(1– 2), 123– 137. <https://doi.org/10.3354/esr00064>

Wilson, R. P., White, C. R., Quintana, F., Halsey, L. G., Liebsch, N., Martin,
G. R., & Butler, P. J. (2006). Moving towards acceleration for esti-
mates of activity- specific metabolic rate in free- living animals: The
case of the cormorant. Journal of Animal Ecology, 75(5), 1081– 1090.
<https://doi.org/10.1111/j.1365-> 2656.2006.01127.x

Wilson, R. P., & Wilson, M.- P. T. J. (1989). Tape: A package- attachment

technique for penguins. Wildlife Society Bulletin, 17, 77– 79.

Won,  S.  P.,  &  Golnaraghi,  F.  (2009).  A  triaxial  accelerometer  calibra-
tion  method  using  a  mathematical  model.  IEEE  Transactions  on
Instrumentation and Measurement, 59(8), 2144– 2153.

Methods in Ecology and Evolu(cid:13)on

    |  825

Yin, Y., Fang, Z., Liu, Y., & Han, F. (2019). Temperature- insensitive struc-
ture  design  of  micromachined  resonant  accelerometers.  Sensors,
19(7), 1544.

Yoda, K. (2019). Advances in bio- logging techniques and their application
to  study  navigation  in  wild  seabirds.  Advanced  Robotics,  33(3– 4),
108– 117. <https://doi.org/10.1080/01691> 864.2018.1553686
Yoda, K., Sato, K., Niizuma, Y., Kurita, M., Bost, C., Le Maho, Y., & Naito,
Y.  (1999).  Precise  monitoring  of  porpoising  behaviour  of  Adelie
penguins  determined  using  acceleration  data  loggers.  Journal  of
Experimental Biology, 202(22), 3121– 3126. <https://doi.org/10.1242/>
jeb.202.22.3121

Yorzinski, J. L., Chisholm, S., Byerley, S. D., Coy, J. R., Aziz, A., Wolf, J. A.,
& Gnerlich, A. C. (2015). Artificial light pollution increases noctur-
nal  vigilance  in  peahens.  PeerJ,  3,  e1174.  <https://doi.org/10.7717/>
peerj.1174

S U P P O R T I N G I N FO R M AT I O N

Additional  supporting  information  may  be  found  in  the  online

version of the article at the publisher’s website.

How to cite this article: Garde, B., Wilson, R. P., Fell, A., Cole,

N., Tatayah, V., Holton, M. D., Rose, K. A., Metcalfe, R. S.,

Robotka, H., Wikelski, M., Tremblay, F., Whelan, S., Elliott, K. H.

& Shepard, E. L. (2022). Ecological inference using data from

accelerometers needs careful protocols. Methods in Ecology and

Evolution, 13, 813–825. <https://doi.org/10.1111/2041->

210X.13804

GARDE et al. 2041210x, 2022, 4, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13804> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
