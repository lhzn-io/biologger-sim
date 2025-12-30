Copyright WILEY-VCH Verlag GmbH & Co. KGaA, 69469 Weinheim, Germany, 2019.

Supporting Information

for Small, DOI: 10.1002/smll.201804385

Noninvasive Featherlight Wearable Compliant “Marine Skin”:
Standalone Multisensory System for Deep-Sea Environmental
Monitoring

Sohail F. Shaikh, Harold F. Mazo-Mantilla, Nadeem Qaiser,
Sherjeel M. Khan, Joanna M. Nassar, Nathan R. Geraldi,
Carlos M. Duarte, and Muhammad M. Hussain*

Supporting Information

Title: Non-invasive featherlight wearable compliant “Marine Skin” – standalone multi-
sensory system for deep-sea environment monitoring

Sohail F. Shaikh1, Harold F. Mazo-Mantilla1, Nadeem Qaiser1, Sherjeel  M. Khan1, Joanna M.
Nassar2, Nathan R. Geraldi3, Carlos M. Duarte3, and Muhammad M. Hussain1*

1mmh Labs, Electrical Engineering, Computer Electrical Mathematical Science and Engineering
Division  (CEMSE),  King  Abdullah  University  of  Science  and  Technology  (KAUST),  Thuwal
23955-6900, Saudi Arabia.
2California Institute of Technology, Pasadena, CA 91125, USA.
3Red Sea Research Center (RSRC), Division of Biological and Environmental Sciences and
Engineering (BESE), King Abdullah University of Science and Technology (KAUST), Thuwal
23955-6900, Saudi Arabia.

*Corresponding author’s e-mail: <muhammadmustafa.hussain@kaust.edu.sa>

Keywords:  marine  ecology,  flexible  systems,  non-invasive  tag,  soft  packaging,  hybrid
integration,

1. Material and Design Optimisation

1.1. Temperature Sensor

Oceanic temperature is relatively stable in response to changes in climates, for example,

the  change  in  oceanic  temperature  is  effectively  0.1  °C  for  0.6  °C  change  in  global  average

temperature  in  the  last  century.    However,  the  temperature  of  the  seawater  varies  with  the

increasing depth (200-1500 m) known as thermocline region, which also has a significant effect

on  the  marine  ecosystems  at  different  depths.  [1–4]    We  compare  the  performance  of  the

temperature sensor with the performance of the commercial temperature sensor integrated circuit

(IC) from Sensirion. Commercial temperature sensor IC from Sensirion is attached to next to the

fabricated temperature sensor on the wafer for accurate temperature detection. Both the reference

and test sensors are subjected to heating from room temperature of 21 °C all the way up to 80 °C

using a hot air gun. Initially, both the sensors record the values for room temperature which starts

1

increasing as the hot air gun is brought closer and closer to the sensor gradually. From  Figure

S1, we can clearly observe that change in resistance of version 2 sensor follows exactly with the

reference  standard.  Instantaneous  variations  in  the  resistance  change  not  only  suggest  that  the

resolution  is  high  but  also  the  response  and  recovery  times  match  are  at  least  on  par  with  the

status quo if not better.

1.2. Salinity Sensor

Similarly, the salinity of the seawater is fairly constant at the surface and at greater depths

(> 800 m) but it varies rapidly in the halocline region (the region of rapid change of salinity, ~

300 – 1000 m) similar to thermocline region for temperature. Variations in the oceanic salinity

have been reported to  affect the water cycles and the oceanic  circulation. Factors that increase

the salinity gradually of the oceanic surface are naturally counterbalanced by the inflow of fresh

water from rivers, global ice melting, and precipitation of rainwater.[5,6] Ocean surface salinity is

also  one  of  the  key  parameters  in  understanding  the  effects  of  freshwater  intake  on  the  ocean

dynamics due to occurrences of 86% evaporation and 78% global precipitation over the ocean.

Thus,  quantifying  temperature  and  salinity  can  provide  us  with  the  basic  understanding  of  the

adaptability,  habitat,  food  habits  and  growth  profiles  of  the  marine  species.  In  addition,  the

density of seawater varies with the variation in temperature, depth, and the salinity. Variations in

the density of water are significantly observed in pycnocline region (~ 200 – 500 m) (a subset of

the halocline and thermocline regions) whereas, the density variation saturates at depths beyond

1000 m.  [2,5] Conventionally, a salinity sensor is a simple 2 electrode design separated by some

distance  (2  mm  in  our  first  version).  To  increase  the  stability  and  the  sensitivity,  we  have

modified  the  design  to  interdigitated  electrode  pattern  and  hence  observed  more  than  ~625%

increase  in  the  sensitivity  with  stable  and  robust  performance  (Figure  S2).  We  also  observed

~135%  increment  in  the  sensitivity  due  to  change  of  material  from  Au  to  Cu  (Figure  S2b),

2

however,  an  effect  has  been  neglected  due  to  corrosive  nature  of  Cu  which  can  degrade  the

performance of exposed salinity sensor underwater.

1.3. Pressure Sensor

The  underwater  pressure  of  the  oceanic  environment  is  directly  related  to  the  height  of

the  water  (

  )  where  P  is  the  hydrostatic  pressure,  (cid:545)  is  the  density  of  water,  g-

acceleration  due  to  gravity,  and  h-represents  the  height  of  water.  The  total  pressure  exerted

 (cid:2172) (cid:3404)  (cid:2251) (cid:942) (cid:2190) (cid:942) (cid:2189)

(Ptotal)  on  any  object  underwater  is  the  combination  of  partial  hydrostatic  pressure  P  and  the

atmospheric pressure (P0), (

) at the sea level which measures 14 psi for each

atmospheric pressure. Conventional pressure sensors have high sensitivity with  a caveat of low

(cid:2172)(cid:2202)(cid:2197)(cid:2202)(cid:2183)(cid:2194)   (cid:3404)  (cid:2172)  (cid:3397)   (cid:2172)(cid:2777)

operating range, which restricts the usage  in  the  marine sensors.  Hence,  we have designed our

depth sensor based on a parallel plate capacitance principle where the capacitance varies linearly

with the increasing depth with extremely good sensitivity and instantaneously. We chose PDMS

due  to  its  compressive  nature  as  a  dielectric  material  for  capacitive  pressure  monitoring

underwater. Due to its inherent compressive nature, we could use it as a dielectric material that

can change the thickness on pressure application and hence the capacitance change is detected in

response to the pressure. PDMS is prepared by mixing the elastomer to curing agent in the ratio

of (10:1) is cured mostly at 90 °C for 60 minutes. However, altering the mixing ratio and curing

temperature  modifies

the  compressibility  and  elasticity  of  PDMS.  To

improve

the

compressibility of the dielectric layer, we modified the PDMS elastomer to curing agent mixture

during preparation. Increase in elastomer ratio (12:1) from (10:1) and curing at a relatively low

temperature  (60  °C)  resulted  in  increased  compressibility  implying  increased  sensitivity.  Also,

the  thickness  of  the  dielectric  layer  plays  an  important  role  in  having  increasing  the  detection

range  of  the  pressure  (or  depth).  We  have  observed  higher  sensitivity  for  1:12  composition  of

PDMS  (Figure  S3a)  whereas  similar  increment  was  observed  for  thickness  of  50  µm  (Figure

3

S3b).  Our  material  choices  and  the  optimisation  has  increased  the  operating  range  up  to  2  km

which  was  only  restricted  due  to  non-availability  of  the  tool  that  can  simulate  higher  pressure

than equivalent to 2 km.

For  depth  measurements  at  a  high-pressure  environment,  we  used  a  hydraulic  pressure

simulation tool available in the lab. The tool has the capabilities to control the applied pressure in

the chamber filled with water up to  a maximum pressure of 3000 psi,  which is  equivalent  to a

depth of 2000 m. However, the recommended maximum value for applied pressure was 2300 psi

for the equipment restricting our measurements to a maximum pressure equivalent to a depth of

1500  m  (Figure  S4).  The  experimental  setup  is  shown  in  Figure  S4b  in  which  the  sensor  is

immersed  in  a  closed  metallic  vessel  (~70  cm  tall  with  an  internal  diameter  of  15  cm)  with

thermal insulation from outside, connected to a digital and manual pressure control system. The

simulation  tool  is  a  custom  designed  set-up  that  has  3  different  components:  pressure  and

temperature  controller,  hydraulic  pump,  and  the  chamber.  The  hydraulic  pump  is  mainly  for

applying  manual  pressure  (Figure  S4b  right  inset).  The  applied  pressure  can  be  calibrated  or

readout  using  an  analog  dead  weight  measurement  system  (Ametek  test  &  calibration

instruments)  or  digital  tools  (Digiquartz  Portable  Standard  from  Paroscientific  Inc.).  The  steel

vessel  that  is  filled  with  the  seawater  also  has  waterproof  connectors  that  can  be  connected  to

other tools like Oscilloscope, function generator or any other electronic instrument.  We started

with  digitally  controlling  the  pressure  applied  through  a  small  hydraulic  hand-pump,  however,

observed  a lot of noise in the recording of  the  signal. This  noise was  figured to  be originating

from the electrical interference of the connections of a digital control system to the steel vessel.

We switched to manual control mode and applied pressure in an incremental way up to 1500 m

with  a step size of 30 m (~43 psi). Real-time variation in  capacitance of pressure/depth sensor

4

with respect to the applied changing pressure has been plotted in Figure S3a. It can be seen that

the sensor exhibits a linear relationship to the change in depth of the water with extremely fast

response time. An incremental increase in the capacitance with the corresponding step increase

in applied pressure appears to be constant throughout the entire range. From this response, it can

be conferred that sensor performance neither degrade nor reach a saturation in the value, thereby

can withstand the pressure of water higher than the depths of 2 km. One can observer oscillations

in  the  capacitance  change  from  Figure  S4,  with  incremental  pressure.  These  oscillations  are

arising  from  the decrease in  the pressure during  manual  application of pressure,  and hence the

hydraulic pressure drops initially then ramps up to the desired values. These oscillations to the

variations in the pressure experienced during the step increment confirm high sensitivity and the

resolution of the depth sensor.

2. Rugged Performance Testing

2.1. Cyclic Bending Tests

For  the  reliability  of  the  Marine  Skin,  it  is  important  to  study  the  effect  of  the  harsh

environmental parameters that it may experience. The two important parameters are high salinity

exposure  for  extended  periods  (multiple  weeks)  and  no  degradation  in  the  performance  due  to

physical deformations. First, the ruggedness of the depth sensors and integrity of packaging were

tested  by  subjecting  the  fabricated  Marine  Skin  to  a  large  number  of  bending  cycles  with  the

bending radius of 1 mm. Depth measurements in the lab environment are carried out after 100,

500, 1000, 2500, and 104 bending cycles (Supplementary Video S1). Real-time variations in the

capacitance while submerging in the water in steps of 10 cm each plotted in Figure S5 where the

change  in  each  step  is  consistent  with  the  only  variation  due  to  the  manual  handling  error  in

maintaining constant step height increment. The sharp increase in the capacitance occurs as soon

as the sensor is immersed in water from the air. To confirm the reliability for the ruggedness over

5

different  cycles,  hysteresis  tests  are  performed  where  measurements  are  recorded  at  specific

depths during increasing depths (submerging) and decreasing depths (rising up) of water. Figure

S6  illustrates  excellent  hysteresis  characteristics  of  the  sensors  the  variation  in  depth,

nevertheless, the variations in the hysteresis can also be attributed to variations occurring due to

manual handling.

2.2. Prolonged Exposure to Saline Environment

Similarly,  the  packaging  integrity  is  validated  from  the  prolonged  exposure  of  high

salinity  (41  PSU)  Red  Seawater  on  the  sensors.  We  immersed  the  packaged  Marine  Skin

platform in the seawater and measured the performance after 1 day, 3 days, 7 days, 15 days and

28  days  to  evaluate  the  integrity  of  packaging.  The  real-time  change  in  the  capacitance  with

increasing depth of the water is acquired (Figure S7) for these different scenarios, which show

no degradation in terms of saturation or sensitivity. Thus, we can conclude that the integrity of

packaging and the reliability of the sensors makes the Marine Skin platform an extremely robust,

flexible, and highly lightweight solution for marine environmental monitoring.

3. Attachment Strategies and Wearable Bracelet Design

3.1. Attachment on Large Species

The  tagging  of  the  marine  species  has  always  been  a  non-invasive  method  involving

incisions through skin, tissues, usage of metallic and plastic anchors inserted in the skin. Invasive

method  of  attachment  can  lead  to  the  injury  of  the  species,  which  not  only  introduces  great

discomfort  to  the  tagged  individual  but  also  can  affect  their  normal  movements  and  behavior.

Thus, the requirement of 2% body weight of the bio-loggers, flexibility and non-invasive nature

of the devices are under focus. Our focus was on making a flexible standalone system that can

adhere to all these norms in addition to having a completely non-invasive tagging mechanism. In

6

past, Marine Skin version 1, was tested for its flexibility and non-invasive method attachment on

tiger shark, wobbegong shark, and stingray (Figure 7). We mounted the sensors on a cylindrical

CAN host attached to a steel clamp that was attached to the dorsal fin of the shark. This method

can  only  be  applicable  to  large  species  with  the  dorsal  fin  acting  as  an  anchor  for  the  sensing

system.  For  other  species  with  comparatively  smoother  and  mucous  skin  or  smaller  sized

animals,  we  needed  to  use  other  techniques.  Superglue  can  be  used  on  the  species  with  hard

shells (turtles, crab etc.) whereas as dental/surgical glue was tested on a wobbegong and Stingray

(Supplementary  Video  S3).  The  hydrodynamic  forces  due  to  the  stream  of  water  detach  the

sensors from the body of the animal. Not only the water stream but also this glue is dissolvable

in water in 48 hours making this method unsuitable for long-term deployment.

3.2. Wearable Bracelet Design

We  designed  a  unique  strategy  of  making  a  soft  elastic  wearable  jacket  (bracelet)  like

structure to host the sensors made from the same material. The wearable gadget can be wrapped

around  the  species  and  its  strong  locking  mechanism  can  prevent  it  from  detachment  due  to

water stream itself. We made 3D printed molds for replicating the wearable modules, followed

by  pouring  PDMS  to  cure  at  60  °C  for  an  hour.  This  cured  wearable  jacket  design  embedded

with the sensory platform can be easily peeled from the mold (Figure S9). In the initial design,

we used the locking mechanism of soft-pins and the holes made from the same PDMS material

(Figure  S9c).  However,  the  design  of  the  soft  pins  was  not  strong  enough  to  withstand  the

stream  pressure,  in  addition,  the  adhesive  strength  was  not  sufficient  to  hold  the  jacket  on  the

skin. We modified the design to incorporate a 3D printed pin structure for increasing the strength

of  the  locking  mechanism.  These  3D  printed  mushroom  pins  provide  excellent  strength  and

hence the successful attachment on barramundi and seabream fishes can be seen in video S4 and

7

S5. Dental adhesive can be used on the inner lining of the soft wearable bracelet to reduce the

friction  between  the  elastic  soft  material  and  the  skin  and  hence  reducing  the  minuscule

probability of injury due to this soft bracelet.

REFERENCES

[1]

J.  B.  C.  Jackson,  M.  X.  Kirby,  W.  H.  Berger,  K.  A.  Bjorndal,  L.  W.  Botsford,  B.  J.

Bourque, R. H. Bradbury, R. Cooke, J. Erlandson, J. A. Estes, T. P. Hughes, S. Kidwell,

C. B. Lange, H. S. Lenihan, J. M. Pandolfi, C. H. Peterson, R. S. Steneck, M. J. Tegner, R.

R. Warner, Science (80-. ). 2001, 293, 629.

[2]  USEPA,  “Climate  Change  Indicators:  Stream  Temperature,”  can  be  found  under

<https://www.epa.gov/climate-indicators/climate-change-indicators-sea-surface->

temperature, 2016.

[3]

S. C. Doney, M. Ruckelshaus, J. Emmett Duffy, J. P. Barry, F. Chan, C. A. English, H. M.

Galindo, J. M. Grebmeier, A. B. Hollowed, N. Knowlton, J. Polovina, N. N. Rabalais, W.

J. Sydeman, L. D. Talley, Ann. Rev. Mar. Sci. 2012, 4, 11.

[4]

J. H. Koo, D. C. Kim, H. J. Shim, T. H. Kim, D. H. Kim, Adv. Funct. Mater. 2018, DOI

10.1002/adfm.201801834.

[5]

“Salinity

|

Science  Mission

Directorate,”

can

be

found

under

<https://science.nasa.gov/earth-science/oceanography/physical-ocean/salinity>,  n.d.  in  Int.

Geophys., 1994, pp. 171–203.

8

SUPPORTING FIGURES

Figure S1: Comparison  of the performance of (A) version 1 and version 2 temperature sensor
for material choice and improved sensitivity, and (B)Version 2 comparison and calibration with

9

the commercial temperature sensor IC from Sensirion. Fabricated sensors changes the resistance
corresponding to the temperature with the response exactly following the reference sensor.

Figure  S2:  Comparison  of  the  performance  of  (A)  previous  version  and  present  version  water
salinity sensor for improved sensitivity by modified design, and (B) Present version comparison

10

for two different material choices of Au and Cu. An increase of ~625% sensitivity is observed
due to design modification, while increase in sensitivity has been neglected.

Figure  S3: Dielectric material  optimisation for pressure  increasing the pressure sensitivity and
the range of depths that can be measured. (A) Effect of the variation in the mixing ratio of PDMS
elastomer  to  curing  agent,  with  (12:1)  ratio  showing  higher  sensitivity  due  to  increased

11

compressibility.  (B)  Effect  of  dielectric  thickness  variation  on  sensitivity  and  absolute  values,
optimum thickness is 50 µm.

Figure S4: Harsh marine environment real-time pressure recording using version 2 Marine Skin
platform,  (A)  demonstrating  linear  increment  with  the  increased  pressure,  high  sensitivity,
resolution  and  fast  response  time  by  observed  oscillations  due  to  manual  handling.  (B)

12

Experimental setup for the high-pressure simulation and testing in the central labs (inset shows
magnified  images  of  digital  control  for  temperature  and  pressure  (left  black  box)  and  manual
control unit for pressure using a hydraulic pump pumped using a manual handheld lever. A dead
weight analog reading is also visible that looks like poles in B.

13

Figure  S5:  Real-time  depth  measurements  over  multiple  bending  cycles.  Measurements  are
recorded after subjecting sensor to the multiple bending cycles (A)-(F) from 0 to 10,000 cycles.
Real-time measurements of change in  capacitance with increasing pressure (due to incremental
depth) are observed with similar sensitivities.

14

Figure  S6:  Robustness  of  the  pressure  sensor  characterized  for  the  pressure  sensor  when
subjected to extreme bending cycle test of (1 mm bending radii) (A) - (F) with 0, 100, 500, 1000,
2500, and 10 thousand cycles respectively. Discrete measurements are plotted at step heights of
~10 cm for observing the hysteresis during submerging and rising from the water in the acrylic
tank.

15

Figure S7: Real-time depth measurements against the time while submerging the sensors in the
seawater in steps of 10 cm to observe the effect of prolonged exposure to saline water. (A) – (E)
Devices were characterized after 1 day, 3 day, 7, 15, and 28 days of immersion in the Red sea
water (41 PSU) and has observed no significant change in performance.

16

Figure  S8:  Scanning  electron  microscopic  (SEM)  images  of  the  soft-polymeric  encapsualted
packaging for studying the biofouling effect. Samples has been submerged in the Red sea water
for 6 weeks and then a standrad process was followed to fix any kind of biological traces on the
sample  followed  by  acquiring  the  SEM  images.  SEM  of  blanket  PDMS  showing  different
textures (A) before and (C) after O2 plasma treatment for samples to be immersed in water. (B)
sample  1  showing  development  of  algea  and  salt  accumulation  with  a  few  traces  of  diatoms
(inset)  after  6  weeks  of  constant  sumbersion  in  the  Red  seawater.  And  (D)  the  significant
reduction  in  the  biofouling  development  due  to  treatment  and  weak  adhesion  forces  of  the
biofouling organisms that are self-released by drag forces within the water stream.

17

Figure S9: (A) 3D printed mold designs for multiple wearable bracelet. (B) Easy peeling-off of
the  flexible  and  stretchable  bracelet  from  the  3D  mold,  (C)  two  designs  having  Marine  Skin
embedded  within  the  bracelet  with  soft-mushroom  pins  to  hold.  Serpentine  structures  (bottom)
can  provide  more  breathability  for  animal  and  stretchability  to  the  bracelet.  (D)  Modified
bracelet  design  with  3D  printed  mushroom  pins  (spherical  and  trapezoidal  shape)  to  improve
inter-locking  mechanism.  (E)  Increased  inter-locking  strength  due  to  the  incorporation  of  3D
printed mushroom pins has little effect on the flexibility.

18
