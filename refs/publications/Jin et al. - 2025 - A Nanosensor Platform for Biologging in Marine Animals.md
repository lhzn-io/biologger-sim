A Nanosensor Platform for Biologging in Marine Animals

Xiaojia Jin1, Ali A. Alizadehmojarad1, Volodymyr B. Koman1, Gabriel Sánchez-Velázquez1, Manki
Son1, Rory Wilson2, Mark Meekan3, Carlos M. Duarte4, and Michael S. Strano1, *

1 77 Massachusetts Ave., Department of Chemical Engineering, Massachusetts Institute of Technology, Cambridge,
MA, 02139, USA
2Biosciences, College of Science, Swansea University, Singleton Park, Swansea SA2 8PP, United Kingdom
3Australian Institute of Marine Science, the Indian Ocean Marine Research Centre (IOMRC), The University of
Western Australia (M470), 35 Stirling Highway, 6009 Perth, Australia
4Red Sea Research Center, Division of Biological and Environmental Sciences and Engineering, King Abdullah Uni-
versity of Science and Technology, Thuwal 23955-6900, Saudi Arabia

Corresponding author’s email address: <strano@mit.edu>

KEYWORDS tagging, nanosensor, biologging, biochemical monitoring, steroid sensing

ABSTRACT: Biologging has significantly advanced ecological biology by enabling the collection of data from free-roaming
ani-mals in their natural habitats. Traditionally, these measurements have largely been limited to temperature, pressure,
and movement. Incorporating physiological data of animal biomarkers could yield valuable orthogonal datasets, provid-
ing a more nuanced understanding of organisms in the context of their environments and behaviors. Despite this poten-
tial, successful collection of such biochemical information remains absent, and thus motivates new sensor platforms. To-
wards  this  end,  we  explore  the  hardware  and  nanosensor  optimization  of  animal  implantable  sensors  for  tracking  hor-
mone  levels  in  marine  animals.  The  transducer  element  is  based  on  polymer-wrapped  single-walled  carbon  nanotubes
(SWCNT) that act as nanosensors embedded within a biocompatible poly (ethylene glycol) diacrylate (PEGDA) hydrogel.
This work investigates the performance of the nanosensor hydrogel under various temperatures, illumination conditions,
and nanoparticle concentration in the hydrogel. We further prototype a miniaturized fluores-cent system for integration
into existing,  commercially available acoustic tags widely  used in marine biology studies. We demonstrate a baseline of
100 nM for the detection limit of progesterone as an example of an important hormone in marine animals, using the inte-
grated nanosensor hydrogel in this platform.  Further improvement is possible with optimization of the signal to noise via
hardware  development.  This  developed  form-factor  will  complement  the  presently  collected  data  by  providing  insights
into the physiological state of the animals in the context of their behavior and environments.

Marine  animals  undertake  extensive  migrations,  trav-
ersing  vast  distances  and  sometimes  entire  ocean  basins,
which  pose  significant  challenges  for  direct  observation
and monitoring of their behaviors and environments.1,2 To
overcome  these  challenges,  researchers  have  developed
bio-logging  techniques,  also  known  as  animal  telemetry,
biotelemetry,  or  animal-borne  sensors.3–5  These  methods
involve  equipping  animals  with  miniaturized  tags  to  log
and/or relay data relevant to marine ecology. Bio-logging
has become a cornerstone in the study of marine animals,
offering the opportunity to observe the physical and bio-
logical  environment  through  which  these  animals  travel,
enhancing  our  understanding  of  their  ecology.5,6  This
technology  provides  insight  into  how  animals  interact
with  human  activities1  and  informs  target  conservation
efforts.7

In recent years, marine biologging has witnessed signif-
icant advancements, revolutionizing our understanding of
marine  ecosystems  and  species  behaviors.2  By  attaching
various  tracking  devices  to  marine  animals,  researchers

have  been  able  to  collect  valuable  data  on  their  move-
ments,  foraging  patterns,8  migration  routes,9,10  and  even
physiological  parameters.9,11  For  instances,  satellite  tags
have been used to track the migration patterns and habi-
tat use of sharks,12–14 while accelerometers attached to fish
have  provided  data  on  their  swimming  behavior  and  en-
ergy expenditure.15,16

One  key  area  of  development  in  marine  biologging  is
the  miniaturization  of  tracking  devices.3  Advances  in
technology  have  allowed  for  the  development  of  smaller,
lighter, and more sophisticated tags that can be attached
to  a  wide  range  of  marine  organisms,  including  fish,
mammals,  birds,  and  even  invertebrates.17,18  These  tags
often  incorporate  satellite  or  acoustic  telemetry,  global
positioning  system  (GPS),19  accelerometers,20  and  sensors
for  measuring  environmental  parameters,  such  as  tem-
perature  and  salinity.21  Additionally,  a  significant  devel-
opment  has  been  the  integration  of  biologging  data  with
other sources of information, such as remote sensing and
oceanographic  datasets.2  By  combining  these  datasets,

researchers  can  gain  a  more  comprehensive  understand-
ing of the ecological processes and environmental factors
that influencing marine animal behavior. Such integrated
approaches  have  led  to  breakthroughs  in  our  knowledge
of  marine  food  webs,  species  interactions,  and  the  im-
pacts of environmental changes on marine ecosystems.

Despite the significant advancements in marine biolog-
ging,  measurements  have  predominantly  focused  on
physical  parameters
like  temperature,  pressure,  and
movement.22,23  The  ability  to  monitor  biochemical  mark-
ers in freely moving marine animals remains underdevel-
oped.24,25  Gaining  access  to  such  biochemical  data  would
provide  valuable  orthogonal  datasets  and  enable  a  more
nuanced understanding of their physiology, behavior, and
environmental interactions. One category of chemicals of
significant  importance  is  steroid  hormones.26  Steroid
hormones play a pivotal role in the physiological process-
es  of  marine  animals,  including  sex  determination,  sex
change,  and  stress  response.27,28  Some  species  of  fish,  for
instance,  may  change  their  sex  from  male  to  female, dis-
rupting  the  balance  for  optimal  breeding  and  reproduc-
tion.  Both  genotypic  (GSD)  and  temperature-dependent
(TSD)  sex  determination  mechanisms  exist,  with  warmer
water temperatures during early development potentially
yielding  more  males.29  Moreover,  sex  change  may  occur
later  in  life  as  a  consequence  of  reproductive  potential
relative  to  local  social  pressures.30  Physiologically,  ster-
oids, such as estrogens and androgens, as well as aroma-
tase  inhibitors,  have  been  implicated  in  sex  changes.31  In
addition  to  sex-related  processes,  aquatic  organisms  be-
come  more  susceptible  to  disease  and  stunted  growth
during  periods  of  high  stress,  which  manifests  itself  in
higher  endogenous  cortisol levels.32  The  activity  of  estro-
gens and androgens in the case of sex change and cortisol
in the case of stress provide valuable metrics for assessing
the  conditions  of  marine  animals.  Additionally,  proges-
terone levels in marine organisms have been the focus of
growing  research  because  they  can  reveal  reproductive
events  and  indicate  maturity,  both  of  which  provide  in-
sights into population demographics. 33–35

The  problem  of  continuous  biochemical  monitoring  in
marine  animals  is  associated  with  several  challenges,  in-
cluding (1) residual movement of a sensor with respect to
tissue  causing  measurement  artefacts,  (2)  sensitive  and
selective  detection,  and  (3)  long-term  stability.2,36  While
various  sensor  types  like  electrochemical,37  and  fluoro-
phore-based sensors38 have been explored for biochemical
sensing, none have successfully enabled real-time in vivo
monitoring in freely swimming marine animals. In recent
years,  single-walled  carbon  nanotubes  (SWCNTs)  have
emerged  as  promising  candidates  for  in  vivo  sensing,  of-
fering  advantages  of  photostability  and  near-infrared
(nIR) fluorescence, which allows for deep tissue  penetra-
tion.39,40  Our  group  has  previously  developed  SWCNT-
based  nanosensors  for  detecting  various  analytes  includ-
ing  neurotransmitters,41,42  proteins,43,44  and  hormones.45
Building  on  this  work,  we  now  aim  to  integrate  SWCNT
nanosensors into implantable devices for marine animals,
with a specific focus on monitoring progesterone levels as

an example of a steroid hormone of interest. Specifically,
progesterone  levels  in  marine  organisms  have  been  the
focus  of  growing  research  because  they  can  reveal  repro-
ductive events and indicate  maturity, both of which pro-
vide insights into population demographics.33–35

Herein,  we  present  the  development  and  optimization
of  a  miniaturized,  implantable  biologging  tag  with  an
integrated  SWCNT  nanosensor  for  the  continuous  moni-
toring of progesterone in marine animals.  Marine organ-
isms contain several steroid hormones that may interfere
with the detection of progesterone, the hormone of inter-
est in this study. Key interfering hormones include testos-
terone, estradiol, and cortisol. Although the physiological
level  of  these  steroids  is  almost  in  the  same  range,  we
previously  developed  a  sensor  with  specific  detection  of
progesterone  against  a  panel  of  steroid  hormones.42  The
tag is engineered to  meet the size and  power constraints
of  existing  commercial  fish  tags.  We  have  systematically
characterized  the  nanosensor  performance  in  a  custom
hydrogel  matrix  under  varying  conditions.  Integration  of
the sensor and electronic components into a compact tag
design (Fig.  1) is accompanied by the development of an
analytical  model  to  enhance  and  guide  tag  optimization.
As  a  proof-of-concept,  we  demonstrate  sensitive,  stable,
and  reversible  progesterone  detection  under  simulated
conditions.  This  SWCNT  nanosensor-enabled  tag  pro-
vides  an  unprecedented  platform  for  continuous  in  vivo
biochemical monitoring in marine animals. The ability to
collect  this  new  class  of  data  will  facilitate  more  holistic
biologging  studies  to  decipher  the  complex  interplay  be-
tween animal physiology, behavior, and the environment.
Ultimately,  such  advances  in  marine  biologging  can  in-
form data-driven decision making in marine conservation
and sustainable aquaculture.

The  SWCNT  nanosensor  and  the  supporting  optoelec-
tronic components (Fig.  1b-c) are designed to be located
at  the  tip  of  an  existing  tag  (Fig.  1d),  enabling  modular
architecture. The optoelectronic system is composed of a
light-emitting diode (LED) and a detector. The LED may
be  powered  by  a  tag,  whereas  the  detector  may  transmit
the  acquired  data  into  tag’s  memory.  The  optoelectronic
components  are  separated  from  the  environments  using
an insulating yet optically transparent protective window.
The  window  and  a  capping  system  sandwich  a  sensing
hydrogel  that  is  directly  exposed  to  a  local  environment,
enabling  unobscured  chemical  access  of  sensing  species
to nanosensors.

EXPERIMENTAL SECTION

(HiPCO)  process  were  purchased

Materials.  Raw  single  walled  carbon  nanotubes
(SWCNT)  produced  from  the  High-Pressure  Carbon
from
Monoxide
NanoIntegris and used without further processing (Batch
HR27-104).  Poly  (ethylene  glycol)  diacrylate  (PEGDA)
(Mn  =  10000,  Mn  =  8000,  Mn  =  6000)  were  purchased
from Alfa Aesar. All other materials were purchased from
Sigma-Aldrich.

Figure 1. Vision for future biologging, where biochemical sensors are integrated onto existing tags for biologging providing an
orthogonal set of data for studying the ecology system. (a) A concept of a biologging tag to be used into marine animals with
wireless communication. The tag is comprised of an implantable acoustic telemetry tag, hydrogel carbon nanotube sensors, op-
tical components for the readout, and electronic components for signal transmission to shore stations. (b) A schematic of the
optical component with a protective cap for nanosensor clamping in the form of biocompatible hydrogel. (c) An optical system
for detecting signals from nanosensors is comprised of an excitation LED, a detector, and optimally positioned optical filters. (d)
An acoustic transmitter comprised of a battery and electronic components that convert acoustic signal to digital data.

Cortisol  acrylation. Acrylation of  cortisol was  carried
out  in  accordance  with  the  methods  described  by  Lee  et
al.45 Briefly,  2g cortisol and 850mL trimethylamine (TEA)
were dissolved in 50mL tetrahydrofuran (THF). The solu-
tion  was  then  placed  in  an  ice-bath  with  magnetic  stir-
ring,  followed  by  dropwise  addition  of  acryloyl  chloride
(0.5mL)  diluted  in  THF  (10  vol%).  The  reaction  mixture
was placed in ice-bath for 1h and proceeded at room tem-
perature for 2d. After  completion of the reaction, the so-
lution  was  decanted  from  the  hydrogen  chloride  (HCl)-
TEA salts, and THF was removed by rotary evaporation.

The  product  was  reconstituted  in  50mL  dichloro-
methane  (DCM),  followed  by  three  times  of  HCl  (0.5  M)
wash, two times of NaHCO3 (5 wt%) wash, and one time
of  saturated  aqueous  NaCl  wash.  The  solution  was  then
dried using anhydrous NaSO4. The structure of the prod-
uct  was  confirmed  using  1H  NMR  (Bruker  AVANCE  III-
400 NMR Spectrometer).

Polymer synthesis. Polymer synthesis was done as de-
scribed  previously.45  Briefly,  styrene  (742uL),  acrylic  acid
(1900uL)  and  acrylated  cortisol  (385mg)  monomers  were
dissolved in 10mL of 1,4-dioxane. Hydroquinone monome-
thyl  ether  (MEHQ)  was  removed  acrylic  acid  by  passing
through  a  column  packed  with  inhibitor  removers.  Simi-
larly, 4-tert-butylcatechhol was removed from styrene.  2-
(Dedecylthiocarbonothioylthio)-2-methylpropionic  acid
(67.5mg,  1  equiv.)  and  2,2’-azobis  (2-methylpropionitrile)
(6.08mg,  0.2 equiv.)  were  added  to  the  reaction  mixture.
The solution was purged with N2 for 30mins, and the re-
action  was  proceeded  in  nitrogen  environment  at  70  ⁰C
for 24hrs. The mixture was precipitated in 300mL diethyl
ether  afterwards.  The  unreacted  monomer  was  removed
by reconstituting the product in THF and re-precipitating
in diethyl ether twice. The polymer was dried under vac-

uum  for  3d  and  characterized  using  1H  NMR  (Bruker
AVANCE III-400 NMR Spectrometer).

Polymer SWCNT dispersion. 5 mg of HiPCO SWCNT
and  50  mg  of  polymer  were  mixed  in  5mL  of  PBS.  The
solution  was  adjusted  to  a  final  pH  of  7.4  by  dropwise
addition  of  2M  NaOH.  The  mixture  was  bath  sonicated
for  10min  and  ultrasonicated  using  a  6  mm  probe  at  a
power of 10W for 1h (QSonica). The resulting suspension
was  ultracentrifuged  at  155000  rcf  for  4hr.  The  superna-
tant  (top  80%)  was  collected  for  future  use  and  free  pol-
ymer  was  removed  from  the  suspension  by  dialysis
against  1x  PBS  over  5  days  using  100  kDa  cutoff  Float-a-
Lyzer  devices  (Spectrum  Labs).  The  dialysis  buffer  was
replaced thrice daily. UV-Vis-nIR absorption spectroscopy
(Shimadzu 3101PC) was used to verify the presence of the
characteristic absorption peaks for SWCNTs. The concen-
tration  of  the  final  suspension  was  determined  using  the
absorption  at  632  nm  with  an  extinction  coefficient  of
ϵ632 = 0.036 mg(L cm)−1.46

Near-infrared  fluorescent  spectra  measurements.
The nIR emission spectra of the polymer-SWCNT suspen-
sion  was  measured  using  a  nIR  customized  microscope,
which consists of a Zeiss Axio Vision inverted microscope
body  with  a  20X  objective,  coupled  to  an  Acton  SP2500
spectrometer  and  liquid  nitrogen  cooled  indium  gallium
arsenide  (InGaAs)  1D  detector  (Princeton  Instruments).
In  a  96-well  plate,  the  SWCNT  dispersion  (1mg/L)  were
mixed with progesterone (100μM) to a final volume of 200
μL  in  1X  PBS  with  2 vol%  DMSO. The  spectral  control  is
made  of  similar  aqueous  solution  without  nanotubes.
Following  incubation  for  1hr  on  a  tabletop  shaker,  the
samples  were  illuminated  by  a  150  mW  785  nm  photodi-
ode  laser  (B&W  Tek  Inc.),  and  the  fluorescent  emission
spectra were collected from 950 to 1250nm.

Hydrogel  synthesis.  SWCNT  were  encapsulated  in  a
hydrogel  matrix  using  a  modified  version  of  a  previously
reported  protocol.45  Briefly,  PEGDA  (100mg/L),  SWCNT
dispersion (10mg/L), and 2-hydroxy-4’-(2-hydroxyethoxy)-
2-methylpropiophenone  (0.175mg/L)  were  mixed  in  1X
PBS. The mixture was placed into a customized mold, and
purged  with  N2  for  30mins.  The  solution  was  exposed  to
UV light source (Cure Spot 50, Dymax Corp) protected by
OD  1.5  filter  with  a  final  illumination  intensity  of  23
mW/cm2 for 8min to polymerize and form the hydrogels.
After polymerization, the hydrogels were incubated in 1X
PBS to equilibrate for 48 h before testing.

Standoff measurements. Hydrogels with nanosensors
were excited by a 785 nm laser with an incident power of
15  mW.  Fluorescent  images  of  hydrogels  were  collected
with  a  2D  InGaAs  detector  (Princeton  Instruments  OMA
V)  paired  with  a  Nikon  AF  Micro-Nikkor  60 mm f/2.8D
lens and FEL 900 nm long-pass filter (Thorlabs). The typi-
cal integration time was 2 s.

Hardware  design.  The  LED  (LED670L,  Thorlabs)  was
powered  by  2V  driving  voltage.  The  typical  current  for
nanosensor  measurements  was  45  mA.  A  photodetector
(FGA21,  Thorlabs)  was  biased  at  -3V  with  1  MOhm  load
resistance, equipped  with  low-pass  noise  filter  composed
of  1  kOhm  resistor  and  0.1  µF  capacitor.  The  power  was
delivered by a  custom-made  USB adapter  connected to a
personal computer. The optical power was measured by a
power meter (Thorlabs). The electrical current was meas-
ured  using  Keithley  2002  and  Labjack  U7,  and  recorded
using  a  custom-build  LabVIEW  software.  A  custom  de-
signed  optical  filters  were  used:  7  mm  diameter  700  nm
short-pass and 10 mm diameter 900 nm long-pass (Chro-
ma).  The  enclosures  to  hold  the  electrical  and  optical
components were custom designed in Solidworks and 3D
printed in Ultimaker S3 using PLA material. System opti-
mization  was  performed  using  translation  stage  manipu-
lators (Thorlabs).

Sensor  performance  measurements.  A  hydrogel  (10
mg/L  nanotubes  in  5x5x3  mm3)  was  placed  into  a  minia-
turized  setup,  if  not  stated  otherwise.  The  nanosensor
signal was  calculated as the  difference between  photode-
tector current after and before the addition of the hydro-
gel.  Noise  values  were  calculated  as  a  signal’s  standard
deviation  over  1000  sec  time  period,  if  not  stated  other-
wise.  The  detector  signal-to-noise  ratio  (SNR)  was  calcu-
lated as a ratio between nanosensor signal and noise lev-
els. In this proof-of-concept study, it is important to note
that all the measurements here were performed in-vitro.

Analytical model. The power emitted by LED was cal-
culated using typical performance plots available in specs,
alternatively  it  can  also  be  measured  experimentally.
Spent power to drive LED was calculated as a product of
driving  voltage  and  current.  To  calculate  light  intensity
on  the  hydrogel,  we  took  into  account  LED  spreading
angle, distance to the hydrogel, and its area. Solid angles
were  approximated  as  referred  to  the  central  points  of
LED,  hydrogel,  and  detector.  LED  emission  was  approxi-
mated as the one corresponding to the central LED wave-

length.  Nanotube  absorption  in  the  hydrogel  was  calcu-
lated  as  a  product  of  its  absorbance,  hydrogel  thickness,
and  its  concentration.  The  total  nanotube  emission  was
calculated  using  nanotube  quantum  yield  of  1%.  The
emission  wavelength  was  approximated  as  1100  nm.  We
assume  the  emission  is  isotropic,  i.e.  emitted  in  4π  solid
angle. Only a fraction of the emitted light will be detected
by a photodetector, which will be determined by the dis-
tance  to  the  detector  and  its  area. The  photocurrent  was
calculated  as  a  product  of  the  nanosensor  emission  that
reached  the  detector  and  its  responsivity.  SNR  was  esti-
mated  as  a  ratio  between  the  photocurrent  and  noise,
which  in  turn  was  defined  as  a  product  of  noise  equiva-
lent power and a square root of measurement bandwidth.
The  last  two  values  were  taken  from  the  detector  specs.
To  fit  experimental  data  with  the  developed  analytical
model,  a  single  correction  factor  of  12.5  was  used  to  ac-
count  for  various  limitation  of  the  model,  such  as  reflec-
tions at interfaces, single emission and fluorescence wave-
length, and solid angle approximations.

RESULTS AND DISCUSSION

Nanosensor  Characterization The  progesterone  Co-
rona  Phase  Molecular  Recognition  (CoPhMoRe)  sensor
was  prepared  by  suspending  SWCNT  synthesized  by  the
high-pressure  carbon  monoxide  (HiPCO)  process  with
specifically  designed  templated  polymers(SM8).45  Suc-
cessful  SWCNT  dispersion  with  polymer  was  confirmed
via  UV-Vis-nIR  spectroscopy,  which  revealed  sharp,  dis-
tinct  absorption  peaks  characteristic  of  isolated  SWCNT
(Fig.  2a). Near-infrared (nIR) emission spectra of the dis-
persion, both before and after the addition of 100 μM pro-
gesterone,  were  captured  under  785  nm  laser  excitation
(Fig. 2b).45 The sensor demonstrated a significant turn-on
response,  exhibiting  a  58%  increase  in  fluorescence,
measured  by  integrating  the  total  emission  intensity
across the spectrum, compared to a 23% response (magni-
tude) for the second highest steroid response at the same
concentration of 100 μM.

The SWCNT sensor was encapsulated in a biocompati-
ble  hydrogel  (Fig.  2d-e)  matrix  for  in  vivo  application.
Peak position and relative peak intensity of SM8-SWCNT
in  both  absorption  and  fluoresce  emission  spectra  re-
mained  consistent  (Fig.  2c,  Fig.  S1),  indicating  nearly
identical  dielectric  environments
the
SWCNT in solution and hydrogel form. The sensor’s func-
tionality  within  the  hydrogel  was  confirmed  through  its
response  to  progesterone  at  a  concentration  of  100  μM
dispersed  in  phosphate  buffer  saline  (PBS)-2%  dimethyl-
sulfoxide  (DMSO)  buffer,  with  control  measurements  in
buffer  showing  no  intensity  changes  (Fig.  2f).  The  sen-
sor’s  response  across  both  solution  and  hydrogel  phases
to varying progesterone concentrations was quantitatively
analyzed using the following functional form:

surrounding

(Eq.1)

00DIICICK−=+

Figure  2. Nanosensor characterization. (a) UV-Vis-nIR absorption spectrum of polymer-SWCNT dispersion (6.8  mg/L).
(b) Fluorescence emission spectra of the nanosensor (1 mg/L) before and after the addition of 100 μM progesterone hor-
mone.45 Reprinted from Lee et al, Advanced Healthcare Materials, 9, 2020, with permission from Wiley-VCH. (c) Fluores-
cence spectra of the progesterone sensor in buffer condition and in PEGDA hydrogel solution before crosslinking. (d) Vis-
ible images of PEGDA-8000 hydrogels encapsulated with nanosensors (10 mg/L). Scale bars are 5mm. (e) A near-infrared
fluorescent  image  of  the  hydrogel nanosensor  (10  mg/L). Scale  bars  are  5  mm. (f)  Normalized  fluorescent  intensity  of  a
hydrogel nanosensor (10 mg/L) in a buffer solution with the addition of progesterone (final conc: 100 µM) at t = 450 sec.
(g)  Calibration  curves  and  the  analytical  model  fits  for  nanosensors  in  solution  and  in  the  hydrogel  (data  presented  as
mean ± SEM, n =3). (h) Nanosensor response towards 100 µM progesterone as a function of illumination power in solution
and  in  the  hydrogel  (data  presented  as  mean  ±  SEM,  n  =3).  (i)  Normalized  photoluminescence  intensity  changes  as  a
function of the nanosensor solution temperature (data presented as mean ± SEM, n =3).

where I is the fluorescence intensity after progesterone
addition, I0 is the original intensity, β is the proportionali-
ty  factor  between  analyte  occupancy  and  fluorescence
intensity  change,  C  is  the  progesterone  concentration,
and KD is the equilibrium dissociation constant (Fig.  2g).
The SWCNT sensor was responsive to progesterone from 1
μM  to  200  μM,  serving  as  a  robust  quantitative  tool  to
study  the  progesterone  concentration  in  marine  animals.
The hydrogel-phase SWCNT exhibited a lower magnitude
of  response  to  progesterone  when  compared  to  the  solu-
tion  phase  counterpart,  likely  associated  to  the  con-
straints  of  the  SWCNT-polymer  movements  inside  the
cross-linked hydrogel matrix.

It is important to note that the sensors developed here
are based on our previous study42, where specificity of the
sensor’s  response  towards  progesterone  against  other  in-

terfering  hormones  were  thoroughly  investigated.  Addi-
tionally,  the  stability  of  and  reversibility  of  response  of
sensors  encapsulated  in  hydrogel response  were  also  dis-
cussed.

The sensor response demonstrated a dependency on il-
lumination  power  (Fig.  2h),  with  optimal  performance
observed at approximately 100 mW. This finding suggests
the potential of preserving the sensor functionality while
reducing the power requirement for the miniaturized tag.
As  the  sensor  would  be  ultimately  deployed  in  marine
environment  with  varied  weather  conditions,  we  investi-
gated  the  sensor  fluorescence  at  different  temperature
(Fig.  2i).  The  normalized  SWCNT  fluorescence  was  rela-
tively stable from 5 ⁰C to 35 ⁰C, and started to decrease at
higher  temperatures.  The  observed  stability  further  sup-
ports the hypothesis that sensor response stability can be

Figure 3. Hardware optimization with a 3D-printed modular setup. (a) An experimental modular setup with LED and its short-
pass optical  filter,  a  photodetector  and  its  long-pass  optical  filter,  and  a  glass  slide  supporting  nanosensor  hydrogel  (10  mg/L
nanotubes in 5x5x3 mm3). Exact positions of the components are controlled by precise micromanipulators. Scale bar is 1 cm. (b)
Schematic illustration of the experimental system in (a). (c) Nanosensor fluorescence as a function of the relative component
positions. The center of the detector is located at (0,0), while the center of LED is at (10,0) with an inclination angle of  45º. (d)
Nanosensor fluorescence decreases with the hydrogel height above the electronic components. (e) Nanosensor fluorescence as a
function of the LED inclination angle. (f,g) A near-infrared image of six nanosensor hydrogels without (f) and with (g) a top re-
flector made out of silver mirror. Scale bars are 1 cm. (h) Top reflector enhancement for standoff (red) and mini (yellow) setups.
(i,j) A near-infrared image of three hydrogels with 30 mg/L (i) and 10 mg/L (j) nanosensors. (k) Fluorescence signal enhance-
ments for standoff (red) and mini (yellow) setups for increased sensor concentrations.

enhanced through encapsulation in hydrogels. Hydrogels
exhibit  greater  stability  at  lower  temperatures  compared
to  higher  temperatures,  as  lower  temperatures  mitigate
water  molecule  loss  and  prevent  dehydration.  The  ob-
served changes in fluorescence intensity at elevated tem-
peratures  may  be  attributed  to  the  rearrangement  of  the
corona phase on the surface of the carbon nanotube. The
raw fluorescence spectra at each temperature are present-
ed  in  Fig.  S2.  The  temperature  range  examined  in  this
study  should  be  sufficient,  as  the  temperature  in  marine
environments varies between 0°C and 30°C, depending on
factors  such  as  water  depth,  geographic  location  (e.g.,
proximity  to  the  equator  or  polar  regions),  and  the  time
of year.

Engineering  Design  for  Miniaturized  Fluorescent
Tag A central goal of this work is to integrate the hydro-
gel sensor  with  existing  acoustic  fish  tags, ones  designed
to conform to movement of marine animals. As such, the
miniaturization into and attachment methods of a flexible
form  factor are  critical next steps. We have encapsulated
the  developed  nanosensors  into  a  compact  fluorescent
tag,  incorporating  integrated  excitation  and  detection
optical  paths.  To  optimize  the  tag’s  optoelectronic  per-
formance,  we  selected  several  commercially  available

components.  For  the  photodetection,  we  evaluated  In-
GaAs  photodiodes,  specifically  Thorlabs’  FGA21,  FGA10,
and FDGA05 (Table S1) models, which vary in active area
and  noise  levels.  Ultimately,  the  FGA21  was  chosen  for
benchmarking. For excitation, we chose Thorlabs’ LEDs  -
LED630L, LED645L, and LED670L (Table S2) - that emit
light  at  varying  wavelengths.  Given  the  minimal  varia-
tions  in  nanosensor  absorption  in  this  part  of  the  spec-
trum  and  the  lower  power  demand,  we  have  chosen  to
work  with  the  LED670L.  The  performance  of  other  pho-
todetectors and LEDs can be estimated with a simple scal-
ing  analysis  using  an  analytical  model  discussed  below.
See  Experimental  Section  for  the  details  on  electrical
circuit.

To find an optimal hardware design of the tag, we have
3D-printed  a  modular  setup,  where  positions  of  an  LED
with  the  supporting  700  nm  short-pass  optical  filter  and
the photodetector with the supporting 900 nm long-pass
optical  filter  were  controlled  by  micromanipulators  (Fig.
3a). The nanosensor hydrogel was placed on a glass cover
slip  above  the  hardware,  configured  in  an  inverted  fluo-
rescent setup where the LED was fixed in a slanted posi-
tion  to  prevent  direct  reflection  into  the  photodetector
(Fig.  3b).  This  configuration  facilitated  extensive  optimi

Figure 4. System performance. (a-d) A schematic overview (a) and photographs (b-d) of the miniaturized fluorescence setup.
Scale bars are 1 cm. (e) Photodetector current in response to the hydrogel (10 mg/L nanotubes in 5x5x3 mm 3). (f) Experimental
measurements and analytical model for photodetector current detected from the hydrogel in response to various excitation LED
powers. (g) Same as (f), but for spent electrical power used to drive LED. (h) The measured noise of the photodetector as a func-
tion of the total power. (i) The photodetector noise for 50 nA total photocurrent averaged over various times. (j) Experimental
measurements and analytical model for the photodetector SNR as in (g) with an averaging time of 1000 sec. (k) FFT spectrum of
the photodetector signal with low-frequency components shown in the inset.

zation studies, adjusting geometrical parameters to en-
hance performance. In particular, optimal position of the
hydrogel  with  respect  to  the  LED  and  the  photodetector
was  found  (Fig.  3c),  noting  that  increasing  the  distance
between the hydrogel and electronics reduced the detect-
ed signal (Fig. 3d). Additionally, an LED inclination of 45º
was  found  to  be  optimal  for  maximizing  detection  effi-
ciency (Fig. 3e).

To  enhance  the  signal  further,  the  setup  can  be  modi-
fied to include a top reflector. Introducing a silver mirror
above  the  hydrogels  (Fig.  3f,  g)  extends  the  excitation
path,  increasing  the  fluorescent  signal  by  70%  as  evi-
denced  in  both  the  standard  standoff  and  miniaturized
setups (Fig. 3h). To accommodate such an arrangement, a
capping system from Figure 1 may be modified to include
access channels for sensing species to reach nanosensors.
Additionally,  the  nanosensor  concentration  can  be  in-
creased up to 30 mg/L from the standard 10 mg/L that we
kept in this work, which also increases its fluorescent sig-
nal  by  3.1  times  (Fig.  3i-k).  However,  further  concentra-
tion  increases  can  lead  to  incompatibility  between  the
nanosensor  and  the  hydrogel  matrix,  along  with  en-
hanced  light  reabsorption,  limiting  its  fluorescence  out-
put.

Using  the  optimized  configuration,  we  have  prototyped  a
miniaturized  fluorescent  tag  using  3D  printed  mold  that
houses  electronic  and  optical  components,  as  well  as  the
nanosensor  hydrogel  (Fig.  4a-d).  The  assembly  process  in-

volves inserting electronic components from the back,  plac-
ing optical  filters  and  a  cover  slip  glass  from  above,  and  se-
curing the hydrogel with a top holder. For accurate nanosen-
sor measurements, it's critical to distinguish the nanosensor
signal from the dark current and leakage light current  (Fig.
4e). The presence of the  incident light leakage is  associated
with the fact that the interferometric filters used in our case
deviate  from  their  optimal  performance  in  the  presence  of
angled incidence light caused by the system miniaturization.
As  such  the  sensor  signal  is  calculated  by  subtracting  both
the  dark  current  and  the  leakage  light  measured  in  the  ab-
sence of the hydrogel from the total signal measured in  the
presence of the hydrogel. Typically, with several milliwatts of
optical  power  emitted  by  LED,  we  detect  several  nanoam-
peres  of  photocurrent  emitted  by  the  hydrogel  nanosensor
(Fig.  4f,  g).  Our  analytical  model  detailed  in  the  Experi-
mental section, demonstrates excellent agreement with the
experimental measurements, providing a powerful prediction
tool to rapidly evaluate and optimize various system parame-
ters.

We  further  assessed  noise  levels  of  the  photodetector,
defining  it  as  the  signal’s  standard  deviation.  We  found
that  the  dark  current  noise  represents  a  dominant  com-
ponent,  while  the  shot  noise  plays  a  minor  role,  increas-
ing slowly with the photocurrent (Fig. 4h). The noise lev-
els  decrease  over  10x  when  the  signal  is  averaged  over
extended periods of time (Fig.  4i). Overall, the miniatur-
ized  setup  demonstrates  signal-to-noise  ratio  (SNR)  val-
ues  over  300  for  the  hydrogel  nanosensors  (Fig.  4j),

providing the ability to track nanosensor response in real-
time.  The  Fast  Fourier  Transform  (FFT)  analysis  of  the
signal  does  not  reveal  any  dominant  peaks  and  largely
follows 1/f-noise pattern (Fig. 4k).

Nanosensor  Performance  in  the  Optimized  Hard-
ware Encouraged by high SNR values of the miniaturized
setup, we further tested the ability to detect the nanosen-
sor  response  to  the  progesterone  hormone  in  the  mini
setup. Sensor performance was assessed by measuring its
fluorescent intensity before and 1000 s after hormone ad-
dition,  allowing  the  sensor  signal  to  stabilize.  Due  to  its
binding mechanism, the response of this type of sensor is
measured  as  a  normalized  intensity  change.  The  devel-
oped  miniaturized  setup  successfully  detected  the  addi-
tion  of  100  µM  of  progesterone,  with  a  ~15%  turn-on  re-
sponse (Fig.  5a). In contrast, control measurements with
buffer showed no sensor changes (Fig. 5b). The miniatur-
ized setup also showed different degrees of the nanosen-
sor fluorescence increase in response to different proges-
terone concentrations (Fig. 5a). These results are detailed
in  the  calibration  curve  that  fits  the  data  to  a  sigmoidal
model  of  nanosensor  binding  (Fig.  5c),  which  shows  ex-
cellent  reproducibility  and  repeatability.  The  limit  of  de-
tection (LOD) for the miniaturized setup was determined
as 100 nM. This value was calculated by adding the inten-
sity  change  of  the  nanosensor  from  the  addition  of  only
buffer  (Sblank)  and  three  times  the  standard  deviation
(𝜎blank)  of  the  response  as  the  noise  level.    Additionally,
the nanosensor was exposed to alternating cycles of 0 and
100 µM progesterone in 1X PBS with 2% DMSO (Fig.  5d).
The  sensor  hydrogel exhibited  a  stable  and  reversible  re-
sponse,  allowing  perturbations  in  fluorescence  –  an  im-
continuous  measurements.
portant

feature

for

Figure  5.  Nanosensor  sensing performance  in  mimic  condi-
tion. (a) Normalized response of the hydrogel nanosensor (10
mg/L nanotubes in 5x5x3 mm3) as measured in the miniatur-
ized setup to various progesterone concentration introduced
at  t  =  0,  given  in  micromolars.  (b)  Representative  control
measurements.  (c)  Calibration  curve  of  the  hydrogel  na-
nosensor response. (d) Normalized response of the hydrogel
nanosensor for reversibility studies, where 100 µM progester-

one was introduced at t = 0 and the system was flushed with
buffer after t = 1800 sec.

Performance  Metrics  for  Miniaturized  Fluorescent
Tags  Sensor  SNR  and  power  consumption  are  two  im-
portant  metrics  for  field  deployment  of  fluorescent  tags.
Noise,  particularly  normalized  against  signal  strength,  is
the  principal  limiting  factor  for  measurement  accuracy.
The  normalized  noise  level  determines  the  ability  to  de-
tect fluorescent changes and can be related to the limit of
detection  using  the  experimentally  determined  calibra-
tion curve. Taking the limit of detection as 3x noise level
and  assessing  noise  levels  measured  in  various  experi-
ments (Fig. 6a), we find a tradeoff between those quanti-
ties.  Noise  levels  change  slightly  from  measurement  to
measurements,  probably  due  to  hydrogel  variations  and
mechanical  instabilities. Our results indicate that we can
successfully detect down to 100 nM of progesterone.

To  understand  the  energy  budget  to  operate  such  a
sensor in-field, we calculated the expected battery life for
a  standard  2000  mAh  battery  under  different  usage  fre-
quencies  (Fig.  6b).  Depending  on  the  measurement  fre-
quency that can range from once in 10 days to 10 times per
day,  the  battery  can  last  from  2000  days  to  10  days,  re-
spectively. Importantly, we note that reducing the average
measurement duration from 1000 sec to 100 sec increases
noise  by  only  20%,  suggesting  a  potential  for  extending
battery  life  with  minimal  impact  on  data  quality.  The
range  of  progesterone  levels  across  a  wide  variety  of  ma-
rine  organisms  is  between  0.32  nM  and  300  nM, 33–35,47–51
and  these  levels  can  fluctuate  over  periods  ranging  from
minutes  to  months.  The  sensitivity  of  our  sensor  system
overlaps with a substantial portion of this range.  For ex-
ample,  Gesto  et  al.50  measured  cortisol  levels  in  rainbow
trout and zebra fish, finding that the latter expressed 47.5
nM  in  the  control  group  but  298  nM  in  the  stressed  co-
hort.  The  former  value  is  below  the  detection  limit
demonstrated  in  this  work  by  a  factor  of  2  but  the  latter
case, of significant interest, is above by a factor of 3.  Simi-
larly,  Nouri  et  al.51  measured  steroid  hormones  in  Large-
mouth  bass,  LMB  (Micropterus  salmoides),  fathead  min-
now, FHM (Pimephales promelas), zebrafish (Danio rerio)
and  silverside  (Menidia  beryllina)  using  an  LC-MS/MS
technique  with  a  38.2  pM  instrument  detection  limit.
They measured a hormone concentration of 287.8 nM for
the  average  of  the  four  species.  The  sensor  system
demonstrated  in  this  work  may  also  find  use  in  studies
examining  the  uptake  of  hormone  additives  to  fish  farm
production.    Khatun  et  al.52  studied  testorsterone,  estro-
gen and progesterone addition to rui (Labeo rohita), catla
(Catla  catla),  and  monosex  tilapia  (Oreochromis  nilot-
icus), and found that progesterone levels in all three fish
types  ranged  from  100  nM  to  2326  nM.  Our  device  re-
quires  further  refinement  to  accurately  monitor  these
variations  with  precise  spatial  and  temporal  resolution.
For  extended  studies,  it  will  be  critical  to  enhance  the
nanosensors’ stability, improve reference corrections, and
implement measures to prevent biofouling.

solution before crosslinking, raw fluorescence emission spec-
tra of the nanosensor at different solution temperature, spec-
ifications  of  photodiode,  specifications  of  LEDs.  The  Sup-
porting  Information  is  available  free  of  charge  on  the  ACS
Publication website.

AUTHOR INFORMATION

Corresponding Author

* Email: <strano@mit.edu>

Author Contributions

The  manuscript  was  written  through  contributions  of  all
authors. All authors have given approval to the final version
of the manuscript.

Notes
The authors declare no competing financial interests.

ACKNOWLEDGMENT

This  work  was  supported  by  the  Innovasea  System  Inc
(Agrmt  dated  02/04/2021).  X.J.  acknowledges  support  from
Mathworks Inc. through the Mathworks Engineering Fellow-
ship.  The  authors  also  acknowledge  support  from  the  Na-
tional  Science  Foundation  (Award  no.  CBET-2124194)  for
nanoparticle spectroscopy and characterization. The collabo-
rative discussions on the biologging problem were supported
by King Abdullah University of Science & Technology (OSR-
2015  Sensors  2707).  The  Table  of  Contents  (ToC)  figure  was
created with Biorender.com.

ABBREVIATIONS

SWCNT,  single  walled  carbon  nanotube;  PEGDA,  PEGDA,
poly  (ethylene  glycol)  diacrylate;  GPS,  global  positioning
system;  GSD,  genotypic  sex  determination;  TSD,  tempera-
ture-dependent sex determination; near-infrared (nIR); LED,
light-emitting diode; HiPCO, High-Pressure Carbon Monox-
ide;  TEA,  trimethylamine;  THF,  tetrahydrofuran;  HCl,  hy-
drogen chloride; DCM, dichloromethane; MEHQ, Hydroqui-
none  monomethyl  ether;  InGaAs,  indium  gallium  arsenide;
SNR, signal-to-noise ratio; CoPhMore, corona phase molecu-
lar  recognition;  DMSO,  dimethylsulfoxide;  PBS,  phosphate
buffer saline; FFT, fast fourier transform analysis;

REFERENCES
(1)

Kaidarova,  A.;  Geraldi,  N.  R.;  Wilson,  R.  P.;  Kosel,  J.;
Meekan, M. G.;  Eguíluz, V. M.; Hussain, M. M.; Shamim,
A.;  Liao,  H.;  Srivastava,  M.;  Saha,  S.  S.;  Strano,  M.  S.;
Zhang, X.; Ooi, B. S.; Holton, M.; Hopkins, L. W.; Jin, X.;
Gong,  X.;  Quintana,  F.;  Tovasarov,  A.;  Tasmagambetova,
A.;  Duarte,  C.  M.  Wearable  Sensors  for  Monitoring  Ma-
rine  Environments  and  Their  Inhabitants.  Nature  Bio-
technology
1208–1220.
<https://doi.org/10.1038/s41587-023-01827-3>.
Chung,  H.;  Lee,  J.;  Lee,  W.  Y.  A  Review:  Marine  Bio-
Logging  of  Animal  Behaviour  and  Ocean  Environments.
Ocean
117–131.
56
<https://doi.org/10.1007/s12601-021-00015-1>.

Journal

Science

2023,

2021,

2023

41:9

(9),

(2),

41

(2)

(3)  Hussey,  N.  E.;  Kessel,  S.  T.;  Aarestrup,  K.;  Cooke,  S.  J.;
Cowley, P. D.; Fisk, A. T.; Harcourt, R. G.; Holland, K. N.;
Iverson, S. J.; Kocik, J. F.; Flemming, J. E. M.; Whoriskey,
F.  G.  Aquatic  Animal  Telemetry:  A  Panoramic  Window
into  the  Underwater  World.  Science  2015,  348  (6240),

Figure  6.  Performance  metrics.  (a)  Limit  of  detection  de-
pendence of the normalized noise limit with SNR=3 line ex-
tracted  from  the  calibration  curve  in  Fig.  4.  (b)  A  tradeoff
between  battery  life  and  measurement  frequency  for  2000
mAh  battery  averaging  a  signal  over  1000  sec  for  one  meas-
urement.

CONCLUSIONS AND FUTURE WORK

In  this  study,  we  engineered  a  miniaturized,  implanta-
ble fluorescent tag designed for continuous monitoring of
progesterone  in  marine  animals,  integrating  a  CoPh-
MoRe-based nanosensor within a biocompatible hydrogel
matrix. This tag, optimized to conform to  marine animal
dynamics,  provides  selective  and  reversible  responses  to
progesterone  across  physiologically  relevant  concentra-
tions.  Systematic  characterization  under  various  envi-
ronmental  conditions  confirmed  the  tag’s  robustness,
with  a  detection  limit  of  100  nM  and  a  dynamic  range
extending  to  200  μM.  Our  integrated  sensing  platform
demonstrated  exceptional  optoelectronic  customization
for  minimized  power  consumption  and  enhanced  signal-
to-noise  ratio,  proving  suitable  for  long-term  hormone
monitoring and deployment in marine environments. The
application  of  an  analytical  model  enables  predictive  as-
sessments of performance, guiding further device optimi-
zation.

This  work  represents  the  first  demonstration  of  a
SWCNT  nanosensor-enabled  implantable  platform  for
continuous  in  vivo  hormone  monitoring  in  marine  ani-
mals. The ability to track hormone levels with high spati-
otemporal resolution will open up new avenues for study-
ing  the  complex  interplay  between  animal  physiology,
behavior,  and  their  environment.  The  fundamental  ad-
vances in sensor design and performance realized here are
applicable  to  a  wide  range  of  analytes  and  ocean  sensing
scenarios.

Future  work  will  focus  on  further  miniaturization  and
packaging of the tag for field deployment, enabled by the
rapidly expanding toolbox of flexible electronics, wireless
power  transfer,  and  embedded  data  processing.  Incorpo-
rating  multi-modal  sensing  capabilities  and  orthogonal
sensors will enhance the information yield per animal and
provide a more holistic view of marine ecosystem dynam-
ics.  We  anticipate  that  this  new  sensing  paradigm  will
greatly  complement  and  expand  the  capabilities  of  con-
ventional  marine  biologging,  enabling  smarter  and  more
agile marine conservation and resource management.

ASSOCIATED CONTENT

Supporting  Information.  UV-Vis  absorption  spectrum  of
the progesterone sensor in buffer  condition and in hydrogel

1255642.
<https://doi.org/10.1126/SCIENCE.1255642/SUPPL_FILE/H>
USSEY.SM.PDF.

6

(JUN),

(4)  Harcourt,  R.;  Sequeira,  A.  M.  M.;  Zhang,  X.;  Roquet,  F.;
Komatsu,  K.;  Heupel,  M.;  McMahon,  C.;  Whoriskey,  F.;
Meekan,  M.;  Carroll,  G.;  Brodie,  S.;  Simpfendorfer,  C.;
Hindell,  M.;  Jonsen,  I.;  Costa,  D.  P.;  Block,  B.;  Muelbert,
M.;  Woodward,  B.;  Weise,  M.;  Aarestrup,  K.;  Biuw,  M.;
Boehme,  L.;  Bograd,  S.  J.;  Cazau,  D.;  Charrassin,  J.  B.;
Cooke,  S.  J.;  Cowley,  P.;  de  Bruyn,  P.  J.  N.;  Jeanniard  du
Dot, T.; Duarte, C.; Eguíluz, V. M.; Ferreira, L. C.; Fernán-
dez-Gracia,  J.;  Goetz,  K.;  Goto,  Y.;  Guinet,  C.;  Hammill,
M.; Hays, G. C.; Hazen, E. L.; Hückstädt, L. A.; Huveneers,
C.;  Iverson,  S.;  Jaaman,  S.  A.;  Kittiwattanawong,  K.;  Ko-
vacs,  K.  M.;  Lydersen,  C.;  Moltmann,  T.;  Naruoka,  M.;
Phillips, L.; Picard, B.; Queiroz, N.; Reverdin, G.; Sato, K.;
Sims, D. W.; Thorstad, E. B.; Thums, M.; Treasure, A. M.;
Trites, A. W.; Williams, G. D.; Yonehara, Y.; Fedak, M. A.
Animal-Borne  Telemetry:  An  Integral  Component  of  the
Ocean  Observing  Toolkit.  Frontiers  in  Marine  Science
2019,
436861.
<https://doi.org/10.3389/FMARS.2019.00326/BIBTEX>.
(5)  Watanabe,  Y.  Y.;  Papastamatiou,  Y.  P.  Biologging  and
Biotelemetry:  Tools for  Understanding  the  Lives  and  En-
vironments  of  Marine  Animals.  Annual  Review  of  Animal
Biosciences  2023,
11,  2023),  247–267.
(Volume
<https://doi.org/10.1146/ANNUREV-ANIMAL-050322->
073657/CITE/REFWORKS.
Roquet,  F.;  Boehme,  L.;  Fedak,  M.;  Block,  B.;  Charrassin,
J.-B.;  Costa,  D.;  Hückstädt,  L.;  Guinet,  C.;  Harcourt,  R.;
Hindell,  M.;  McMahon,  C.;  Woodward,  B.  Ocean  Obser-
vations  Using  Tagged  Animals.  Oceanography  2017,  30
(2), 139–139. <https://doi.org/10.5670/OCEANOG.2017.235>.
(7)  Hays, G. C.; Bailey, H.; Bograd, S. J.; Bowen, W. D.; Cam-
pagna,  C.;  Carmichael,  R.  H.;  Casale,  P.;  Chiaradia,  A.;
Costa, D. P.; Cuevas, E.; Nico de Bruyn, P. J.; Dias, M. P.;
Duarte,  C.  M.;  Dunn,  D.  C.;  Dutton,  P.  H.;  Esteban,  N.;
Friedlaender, A.; Goetz, K. T.; Godley, B. J.; Halpin, P. N.;
Hamann,  M.;  Hammerschlag,  N.;  Harcourt,  R.;  Harrison,
A. L.; Hazen, E. L.; Heupel, M. R.; Hoyt, E.; Humphries, N.
E.;  Kot,  C.  Y.;  Lea,  J.  S.  E.;  Marsh,  H.;  Maxwell,  S.  M.;
McMahon,  C.  R.;  Notarbartolo  di  Sciara,  G.;  Palacios,  D.
M.; Phillips, R. A.; Righton, D.; Schofield, G.; Seminoff, J.
A.; Simpfendorfer, C. A.; Sims, D. W.; Takahashi, A.; Tet-
ley, M. J.; Thums, M.; Trathan, P. N.; Villegas-Amtmann,
S.; Wells, R. S.; Whiting, S. D.; Wildermann, N. E.; Sequei-
ra, A. M. M. Translating Marine Animal Tracking Data in-
to Conservation Policy and Management. Trends in ecolo-
gy
459–473.
2019,
<https://doi.org/10.1016/J.TREE.2019.01.009>.

evolution

(5),

(6)

34

&

11

(8)  Wilson,  R.  P.;  Gómez-Laich,  A.;  Sala,  J.  E.;  Dell’Omo,  G.;
Holton,  M.  D.;  Quintana,  F.  Long  Necks  Enhance  and
Constrain Foraging Capacity in Aquatic Vertebrates.  Pro-
ceedings  of  the  Royal  Society  B:  Biological  Sciences  2017,
284 (1867). <https://doi.org/10.1098/RSPB.2017.2072>.
(9)  Hindell, M. A.; Reisinger, R. R.; Ropert-Coudert, Y.; Hück-
städt, L. A.; Trathan, P. N.; Bornemann, H.; Charrassin, J.
B.;  Chown,  S.  L.;  Costa,  D.  P.;  Danis,  B.;  Lea,  M.  A.;
Thompson,  D.;  Torres,  L.  G.;  Van  de  Putte,  A.  P.;  Alder-
man,  R.;  Andrews-Goff,  V.;  Arthur,  B.;  Ballard,  G.;
Bengtson, J.; Bester, M. N.; Blix, A. S.; Boehme, L.; Bost, C.
A.;  Boveng,  P.;  Cleeland,  J.;  Constantine,  R.;  Corney,  S.;
Crawford, R. J. M.;  Dalla Rosa, L.; de Bruyn, P. J. N.;  De-
lord, K.; Descamps, S.; Double, M.; Emmerson, L.; Fedak,
M.; Friedlaender, A.; Gales, N.; Goebel, M. E.; Goetz, K. T.;
Guinet, C.; Goldsworthy, S. D.; Harcourt, R.; Hinke, J. T.;
Jerosch, K.; Kato, A.; Kerry, K. R.; Kirkwood, R.; Kooyman,

G. L.; Kovacs, K. M.; Lawton, K.; Lowther, A. D.; Lydersen,
C.;  Lyver,  P.  O.  B.;  Makhado,  A.  B.;  Márquez,  M.  E.  I.;
McDonald,  B.  I.;  McMahon,  C.  R.;  Muelbert,  M.;  Nachts-
heim,  D.;  Nicholls,  K.  W.;  Nordøy,  E.  S.;  Olmastroni,  S.;
Phillips, R. A.; Pistorius, P.; Plötz, J.; Pütz, K.; Ratcliffe, N.;
Ryan,  P.  G.;  Santos,  M.;  Southwell,  C.;  Staniland,  I.;
Takahashi, A.; Tarroux, A.; Trivelpiece, W.; Wakefield, E.;
Weimerskirch,  H.;  Wienecke,  B.;  Xavier,  J.  C.;  Woth-
erspoon, S.; Jonsen, I. D.; Raymond, B. Tracking of Marine
Predators to Protect Southern Ocean Ecosystems. Nature
2020
87–92.
<https://doi.org/10.1038/s41586-020-2126-y>.

580:7801

(7801),

2020,

580

(10)  Barrionuevo, M.; Ciancio, J.; Steinfurth, A.; Frere, E. Geo-
location and Stable Isotopes Indicate Habitat Segregation
between Sexes in Magellanic Penguins during the Winter
Dispersion.  Journal  of  Avian  Biology  2020,  51  (2).
<https://doi.org/10.1111/JAV.02325>.

(11)  Wilmers,  C.  C.;  Nickel,  B.;  Bryce,  C.  M.;  Smith,  J.  A.;
Wheat, R. E.; Yovovich, V. The Golden Age of Bio-logging:
How  Animal-borne  Sensors  Are  Advancing  the  Frontiers
of
1741–1753.
2015,
<https://doi.org/10.1890/14-1401.1>.

Ecology.

Ecology

(7),

96

(12)  Block, B. A.; Jonsen, I. D.; Jorgensen, S. J.; Winship, A. J.;
Shaffer,  S.  A.;  Bograd,  S.  J.;  Hazen,  E.  L.;  Foley,  D.  G.;
Breed, G. A.; Harrison, A. L.; Ganong, J. E.; Swithenbank,
A.; Castleton, M.; Dewar, H.; Mate, B. R.; Shillinger, G. L.;
Schaefer, K. M.; Benson, S. R.; Weise, M. J.; Henry, R. W.;
Costa,  D.  P.  Tracking  Apex  Marine  Predator  Movements
in  a  Dynamic  Ocean.  Nature  2011,  475  (7354),  86–90.
<https://doi.org/10.1038/nature10082>.

(14)

(13)  Watanabe, Y. Y.; Goldbogen, J.  A. Too Big to Study? The
Biologging  Approach  to  Understanding  the  Behavioural
Energetics of Ocean  Giants.  Journal of  Experimental Biol-
ogy 2021, 224 (13). <https://doi.org/10.1242/jeb.202747>.
Jorgensen, S. J.; Reeb, C. A.; Chapple, T. K.; Anderson, S.;
Perle, C.; Van Sommeran, S. R.; Fritz-Cope, C.; Brown, A.
C.; Klimley, A. P.; Block, B. A. Philopatry and Migration of
Pacific  White  Sharks.  Proceedings  of  the  Royal  Society  B:
679.
277
2010,
Biological
<https://doi.org/10.1098/RSPB.2009.1155>.

Sciences

(1682),

(15)  Gleiss, A. C.; Jorgensen, S. J.; Liebsch, N.; Sala, J. E.; Nor-
man, B.; Hays, G. C.; Quintana, F.; Grundy, E.; Campagna,
C.;  Trites,  A.  W.;  Block,  B.  A.;  Wilson,  R.  P.  Convergent
Evolution  in  Locomotory  Patterns  of  Flying  and  Swim-
ming Animals. Nature Communications 2011 2:1 2011, 2 (1),
1–7. <https://doi.org/10.1038/ncomms1350>.

(16)  Cooke,  S.  J.;  Hinch,  S.  G.;  Wikelski,  M.;  Andrews,  R.  D.;
Kuchel,  L.  J.;  Wolcott,  T.  G.;  Butler,  P.  J.  Biotelemetry:  A
Mechanistic  Approach  to  Ecology.  Trends  in  Ecology  &
Evolution
334–343.
(6),
<https://doi.org/10.1016/J.TREE.2004.04.003>.

2004,

19

(17)  Meekan,  M.  G.;  Fuiman,  L.  A.;  Davis,  R.;  Berger,  Y.;
Thums,  M.  Swimming  Strategy  and  Body  Plan  of  the
World’s Largest Fish: Implications for Foraging Efficiency
and Thermoregulation. Frontiers in Marine Science 2015, 2
(SEP). <https://doi.org/10.3389/FMARS.2015.00064>.
(18)  Ripperger,  S.  P.;  Carter,  G.  G.;  Page  Supervision,  R.  A.;
Duda, N.; Koelpin, A.; Weigel, R.; Hartmann, M.; Nowak,
T.;  Thielecke,  J.;  Schadhauser,  M.;  Robert,  J.;  Herbst,  S.;
Meyer-Wegener,  K.;  Wägemann,  P.;  Preikschat,  W.  S.;
Cassens,  B.;  Kapitza,  R.;  Dressler,  F.;  Mayer,  F.  Thinking
Small:  Next-Generation  Sensor  Networks  Close  the  Size
Gap in Vertebrate Biologging. PLoS Biology 2020, 18 (4), 1–
25. <https://doi.org/10.1371/journal.pbio.3000655>.

(19)  Delord,  K.;  Barbraud,  C.;  Pinaud,  D.;  Letournel,  B.;
Jaugeon,  B.;  Goraguer,  H.;  Lazure,  P.;  Lormée,  H.  Move-
ments  of  Three  Alcid  Species  Breeding  Sympatrically  in

Saint Pierre and Miquelon, Northwestern Atlantic Ocean.
Journal  of  Ornithology
359–371.
<https://doi.org/10.1007/S10336-019-01725-Z/FIGURES/4>.

2020,

(2),

161

(20)  Ware,  C.;  Trites,  A.  W.;  Rosen,  D.  A.  S.;  Potvin,  J.  Aver-
aged Propulsive Body Acceleration (APBA) Can Be Calcu-
lated  from  Biologging  Tags  That  Incorporate  Gyroscopes
and  Accelerometers  to  Estimate  Swimming  Speed,  Hy-
drodynamic  Drag and Energy Expenditure for Steller Sea
Lions.
e0157326.
2016,
<https://doi.org/10.1371/JOURNAL.PONE.0157326>.

PLOS  ONE

(6),

11

(21)  Nassar, J. M.; Khan, S. M.; Velling, S. J.; Diaz-Gaxiola, A.;
Shaikh, S. F.; Geraldi, N. R.; Torres Sevilla, G. A.; Duarte,
C.  M.;  Hussain,  M.  M.  Compliant  Lightweight  Non-
Invasive  Standalone  “Marine  Skin”  Tagging  System.  npj
1–9.
2018,
Flexible  Electronics
<https://doi.org/10.1038/s41528-018-0025-1>.

2018

(1),

2:1

2

(22)  Lee,  M.  A.;  Duarte,  C.  M.;  Eguíluz,  V.  M.;  Heller,  D.  A.;
Langer,  R.;  Meekan,  M.  G.;  Sikes,  H.  D.;  Srivastava,  M.;
Strano,  M.  S.;  Wilson,  R.  P.  Can  Fish  and  Cell  Phones
Teach  Us  about  Our  Health?  ACS  Sensors  2019,  4  (10),
2566–2570. <https://doi.org/10.1021/acssensors.9b00947>.

(23)  Kaidarova,  A.;  Geraldi,  N.  R.;  Wilson,  R.  P.;  Kosel,  J.;
Meekan, M. G.; Eguíluz, V. M.; Hussain, M. M.; Shamim,
A.;  Liao,  H.;  Srivastava,  M.;  Saha,  S.  S.;  Strano,  M.  S.;
Zhang, X.; Ooi, B. S.; Holton, M.; Hopkins, L. W.; Jin, X.;
Gong,  X.;  Quintana,  F.;  Tovasarov,  A.;  Tasmagambetova,
A.;  Duarte,  C.  M.  Wearable  Sensors  for  Monitoring  Ma-
rine  Environments  and  Their  Inhabitants.  Nature  Bio-
1208–1220.
technology
<https://doi.org/10.1038/s41587-023-01827-3>.

2023,

2023

41:9

(9),

41

(24)  Cooke,  S.  J.;  Brownscombe,  J.  W.;  Raby,  G.  D.;  Broell,  F.;
Hinch, S. G.; Clark, T. D.; Semmens, J. M. Remote Bioen-
ergetics  Measurements  in  Wild  Fish:  Opportunities  and
Challenges.  Comparative  Biochemistry  and  Physiology  -
Part  A :  Molecular  and  Integrative  Physiology  2016,  202,
23–37. <https://doi.org/10.1016/j.cbpa.2016.03.022>.

(25)  Madliger,  C.  L.;  Love,  O.  P.;  Hultine,  K.  R.;  Cooke,  S.  J.
The Conservation Physiology Toolbox: Status and Oppor-
(1),  29.
tunities.  Conservation  Physiology  2018,  6
<https://doi.org/10.1093/CONPHYS/COY029>.

environment

(26)  Ojoghoro, J. O.; Scrimshaw, M. D.; Sumpter, J. P. Steroid
Hormones in the Aquatic Environment. The Science of the
792.
total
<https://doi.org/10.1016/J.SCITOTENV.2021.148306>.
(27)  Azizi-Lalabadi,  M.;  Pirsaheb,  M.  Investigation  of  Steroid
Hormone Residues in Fish: A Systematic Review.  Process
Safety  and  Environmental  Protection  2021,  152,  14–24.
<https://doi.org/10.1016/J.PSEP.2021.05.020>.

2021,

(28)  Bechshoft,  T.;  Wright,  A.  J.;  Styrishave,  B.;  Houser,  D.
Measuring  and  Validating  Concentrations  of  Steroid
Hormones  in  the  Skin  of  Bottlenose  Dolphins  (Tursiops
Truncatus).  Conservation  Physiology  2020,  8
(1).
<https://doi.org/10.1093/CONPHYS/COAA032>.

(29)  Ospina-Álvarez,  N.;  Piferrer,  F.  Temperature-Dependent
Sex Determination in Fish Revisited: Prevalence, a Single
Sex  Ratio  Response  Pattern,  and  Possible  Effects  of  Cli-
mate  Change.  PLOS  ONE  2008,  3
(7),  e2837.
<https://doi.org/10.1371/JOURNAL.PONE.0002837>.
(30)  Munday, P. L.; Buston, P. M.; Warner, R. R. Diversity and
Flexibility of Sex-Change Strategies in Animals. Trends in
ecology  &
89–95.
evolution
<https://doi.org/10.1016/J.TREE.2005.10.020>.

2006,

(2),

21

(31)  Guiguen, Y.; Fostier, A.; Piferrer, F.; Chang, C. F. Ovarian
Aromatase and Estrogens: A Pivotal Role for Gonadal Sex
Differentiation and Sex Change in Fish. General and com-
parative
352–366.
<https://doi.org/10.1016/J.YGCEN.2009.03.002>.

endocrinology

2010,

(3),

165

(32)  Castanheira, M. F.; Conceição, L. E. C.; Millot, S.; Rey, S.;
Bégout, M. L.; Damsgård, B.; Kristiansen, T.; Höglund, E.;
Øverli, Ø.; Martins, C. I. M. Coping Styles in Farmed Fish:
Consequences  for  Aquaculture.  Reviews  in  Aquaculture
2017, 9 (1), 23–41. <https://doi.org/10.1111/RAQ.12100>.
(33)  Atteke,  C.;  Vetillard,  A.;  Fostier,  A.;  Garnier,  D.-H.;  Jego,
P.; Bailhache, T. Effects of Progesterone and Estradiol on
the Repro-Ductive Axis in Immature Diploid and Triploid
Rainbow  Trout.  Comp.  Biochem.  Physiol.  A  Mol.  Integr.
Physiol 2003, 134, 693–705.

(34)  Robeck, T. R.; Steinman, K. J.; Parry, C. B.; Gomez, F. M.;
Jen-sen,  E.  D.  Comparisons  of  Serum  Progesterone  and
Progestagen  Concentrations  in  Normal  and  Abnormal
Bottlenose  Dolphin  (Tursiops  Truncatus)  Pregnancies.
Front. Mar. Sci 2021, 8, 630–563.

(35)  Orlando,  E.  F.;  Ellestad,  L.  E.;  Sources.  Concentrations,
and Exposure Effects of Environmental Gestagens on Fish
and Other Aquatic Wildlife, with an Emphasis on Repro-
duction. Gen Comp Endocrinol 2014, 203, 241–249.
(36)  Korpela,  J.;  Suzuki,  H.;  Matsumoto,  S.;  Mizutani,  Y.;
Samejima,  M.;  Maekawa,  T.;  Nakai,  J.;  Yoda,  K.  Machine
Learning  Enables  Improved  Runtime  and  Precision  for
Bio-Loggers on Seabirds. Communications Biology 2020 3:1
2020,  3  (1),  1–9. <https://doi.org/10.1038/s42003-020-01356->
8.
Sempionatto, J. R.; Lin, M.; Yin, L.; De la  paz, E.;  Pei, K.;
Sonsa-ard,  T.;  de  Loyola  Silva,  A.  N.;  Khorshed,  A.  A.;
Zhang,  F.;  Tostado,  N.;  Xu,  S.;  Wang,  J.  An  Epidermal
Patch for the Simultaneous Monitoring of Haemodynamic
and Metabolic Biomarkers. Nature Biomedical Engineering
2021
737–748.
(7),
<https://doi.org/10.1038/s41551-021-00685-1>.

2021,

(37)

5:7

5

(38)  Geng, Z.; Zhang, X.; Fan, Z.; Lv, X.; Su, Y.; Chen, H. Recent
Progress in Optical Biosensors Based on Smartphone Plat-
forms.  Sensors  2017,  Vol. 17,  Page  2449  2017,  17  (11), 2449.
<https://doi.org/10.3390/S17112449>.

(39)  O’Connell, M. J.; Bachilo, S. H.; Huffman, C. B.; Moore, V.
C.;  Strano,  M.  S.;  Haroz,  E.  H.;  Rialon,  K.  L.;  Boul,  P.  J.;
Noon, W. H.; Kittrell, C.; Ma, J.; Hauge, R. H.; Weisman,
R. B.; Smalley, R. E. Band Gap Fluorescence from Individ-
ual  Single-Walled  Carbon  Nanotubes.  Science  2002,  297
(5581),
593–596.
<https://doi.org/10.1126/SCIENCE.1072631/ASSET/67B598C>
0-C187-4745-B979-
D284272E029E/ASSETS/GRAPHIC/SE2920711004.JPEG.

(40)  Hong,  G.;  Diao,  S.;  Chang,  J.;  Antaris,  A.  L.;  Chen,  C.;
Zhang, B.; Zhao, S.; Atochin, D. N.; Huang, P. L.; Andreas-
son, K.  I.; Kuo, C. J.; Dai, H. Through-Skull  Fluorescence
Imaging of the Brain in a New near-Infrared Window. Na-
ture  Photonics  2014  8:9  2014,  8
(9),  723–730.
<https://doi.org/10.1038/nphoton.2014.166>.

(41)  Beyene,  A.  G.;  Delevich,  K.;  Del  Bonis-O’Donnell,  J.  T.;
Piekarski, D. J.; Lin, W. C.; Wren Thomas, A.; Yang, S. J.;
Kosillo, P.; Yang, D.; Prounis, G. S.; Wilbrecht, L.; Landry,
M. P. Imaging Striatal Dopamine Release Using a Nonge-
netically  Encoded  near  Infrared  Fluorescent  Catechola-
mine  Nanosensor.  Science  Advances  2019,  5
(7).
<https://doi.org/10.1126/SCIADV.AAW3108/SUPPL_FILE/A>
AW3108_SM.PDF.

(42)  Kruss, S.; Landry, M. P.; Vander Ende, E.; Lima, B. M. A. a;
Reuel, N. F.; Zhang, J.; Nelson, J.; Mu, B.; Hilmer, A.; Stra-
no,  M.  Neurotransmitter  Detection  Using  Corona  Phase
Molecular  Recognition  on  Fluorescent  Single-Walled
Carbon Nanotube Sensors. Journal of the American Chem-
ical
713–724.
<https://doi.org/10.1021/ja410433b>.

Society

2014,

(2),

136

(44)

2016,

(43)  Bisker,  G.;  Dong,  J.;  Park,  H.  D.;  Iverson,  N.  M.;  Ahn,  J.;
Nelson,  J.  T.;  Landry,  M.  P.;  Kruss,  S.;  Strano,  M.  S.  Pro-
tein-Targeted  Corona  Phase  Molecular  Recognition.  Na-
ture
1–14.
Communications
<https://doi.org/10.1038/ncomms10241>.
Jin, X.; Lee, M. A.; Gong, X.; Koman, V. B.; Lundberg, D. J.;
Wang,  S.;  Bakh,  N.  A.;  Park,  M.;  Dong,  J.  I.;  Kozawa,  D.;
Cho, S. Y.; Strano, M. S. Corona Phase Molecular Recogni-
tion of the Interleukin-6 (IL-6) Family of Cytokines Using
nIR  Fluorescent  Single-Walled  Carbon  Nanotubes.  ACS
Applied  Nano  Materials  2023,  6
(11),  9791–9804.
<https://doi.org/10.1021/acsanm.3c01525>.

7,

(45)  Lee,  M.  A.;  Wang,  S.;  Jin,  X.;  Bakh,  N.  A.;  Nguyen,  F.  T.;
Dong, J.;  Silmore, K.  S.; Gong, X.; Pham, C.; Jones, K.  K.;
Muthupalani,  S.;  Bisker,  G.;  Son,  M.;  Strano,  M.  S.  Im-
plantable  Nanosensors  for  Human  Steroid  Hormone
Sensing  In  Vivo  Using  a  Self-Templating  Corona  Phase
Molecular  Recognition.  Advanced  Healthcare  Materials
2000429.
2020,
<https://doi.org/10.1002/adhm.202000429>.

(21),

9

(46)  Zhang, J.; Landry, M. P.; Barone, P. W.; Kim, J.-H.; Lin, S.;
Ulissi, Z. W.; Lin, D.; Mu, B.; Boghossian, A. A.; Hilmer, A.
J.;  Rwei,  A.;  Hinckley,  A.  C.;  Kruss,  S.;  Shandell,  M.  A.;
Nair, N.; Blake, S.; Şen, F.; Şen, S.; Croy, R. G.; Li, D.; Yum,
K.;  Ahn,  J.-H.;  Jin,  H.;  Heller,  D.  A.;  Essigmann,  J.  M.;
Blankschtein, D.; Strano, M. S. Molecular Recognition Us-
ing Corona Phase Complexes Made of Synthetic Polymers
Adsorbed on Carbon Nanotubes. Nat. Nanotechnol 2013, 8
(12), 959.

(47)  Lowe, C. L.; Hunt, K. E.; Rogers, M. C.; Neilson, J. L.; Rob-
bins, J.; Gabriele, C. M.; Teerlink, S. S.; Seton, R.; Buck, C.
L.  Multi-Year  Progesterone  Profiles  During  Pregnancy  in
Baleen  of  Humpback  Whales  (Megaptera  Novaeangliae.
Conserv Physiol 2021, 9, 059 1-14.

(48)  Robeck, T. R.; Steinman, K. J.; O’Brien, J. K. Characteriza-
Tion  and  Longitudinal  Monitoring  of  Serum  Androgens
and  Glu-Cocorticoids  during  Normal  Pregnancy  in  the
Killer Whale (Or-Cinus Orca. Gen. Comp. Endocrinol 2017,
247, 116–129.

(49)  Pietraszek, J.; Atkinson, S. Concentrations of Estrone Sul-
Fate  and  Progesterone  in  Plasma  and  Saliva,  Vaginal  Cy-
tology, and Bioelectric Impedance during the Estrous Cy-
cle  of  the  Ha-Waiian  Monk  Seal  (Monachus  Schauins-
landi. Mar. Mammal Sci 1994, 10 (4), 430–441.

(50)  Gesto, M.; Hernández, J.; López-Patiño, M. A.; Soengas, J.
L.;  Míguez,  J.  M.  Is  Gill  Cortisol  Concentration  a  Good
Acute Stress Indicator in Fish? A Study in Rainbow Trout
and  Zebrafish.  Comparative  Biochemistry  and  Physiology
Part  A:  Molecular  &  Integrative  Physiology  2015,  188,  65–
69.

(51)  Nouri, M.-Z.; Kroll, K. J.; Webb, M.; Denslow, N. D. Quan-
tifi-Cation  of  Steroid  Hormones  in  Low  Volume  Plasma
and  Tissue  Homogenates  of  Fish  Using  LC-MS/MS.  Gen-
eral and Compara-tive Endocrinology 2020, 296, 113543.

(52)  Khatun, P.; Saha, P.; Islam, M. Z.; Islam, A.; Islam, M. A.;
Islam,  P. The  Reality  of  the  Use  of  Growth  Hormones  in
Fish. Current Research in Food Sci-ence 2024, 8, 100709.

Table of Contents Figure

13

Supporting Information

A Nanosensor Platform for Biologging in Marine Animals

Xiaojia  Jin1,  Ali  A.  Alizadehmojarad1,  Volodymyr  B.  Koman1,  Gabriel  Sánchez-Velázquez1,
Manki Son1, Rory Wilson2, Mark Meekan3, Carlos M. Duarte4, and Michael S. Strano1, *

1 77 Massachusetts Ave., Department of Chemical Engineering, Massachusetts Institute of Technology, Cambridge,

MA, 02139, USA

2Biosciences, College of Science, Swansea University, Singleton Park, Swansea SA2 8PP, United Kingdom

3Australian Institute of Marine Science, the Indian Ocean Marine Research Centre (IOMRC), The University of

Western Australia (M470), 35 Stirling Highway, 6009 Perth, Australia

4Red  Sea  Research  Center,  Division  of  Biological  and  Environmental  Sciences  and  Engineering,  King  Abdullah

University of Science and Technology, Thuwal 23955-6900, Saudi Arabia
*Corresponding author’s email address: <strano@mit.edu>

Table of Contents:

Figure  S1.  UV-Vis  absorption  spectrum  of  the  progesterone  sensor  in  buffer  condition  and  in
PEGDA hydrogel solution before crosslinking.

Figure S2. Raw fluorescence emission spectra of the nanosensor at different solution temperature.

Table S1. Photodiode specifications used for the study

Table S2. LED specifications used for the study

Figure  S1.  UV-Vis  absorption  spectrum  of  the  progesterone  sensor  in  buffer  condition  and  in
PEGDA hydrogel solution before crosslinking.

Figure S2. Raw fluorescence emission spectra of the nanosensor at different solution temperature.

900950100010501100115012001250020004000600080001000012000140001600018000Intensity (Abs.)Wavlength (nm) 5 °C 10 °C 15 °C 20 °C 25 °C 30 °C 35 °C 40 °C 45 °C 50 °C

Table S1. Photodiode specifications used for the study

Photodiode

FGA21

FGA10

FDGA05

Image

Wavelength range (nm)
Peak wavelength (nm)
Active area (mm2)
Rise / Fall time
Responsivity

800 - 1700
1590
3.1

900 – 1700
1550
0.79
25 ns / 25 ns  10 ns / 10 ns  2.5 ns / 2.5 ns
1.05 A/W

800 – 1700
1550
0.196

0.95 A/W

1.04 A/W

Table S2. LED specifications used for the study

LED 630L

LED 645L

LED 670L

22

20

22

LED
Spreading
angle (deg)

Emission
Spectrum

L-I-V
Characteristic
