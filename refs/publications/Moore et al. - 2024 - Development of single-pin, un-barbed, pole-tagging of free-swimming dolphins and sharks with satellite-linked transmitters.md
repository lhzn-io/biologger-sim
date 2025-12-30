Moore et al. Animal Biotelemetry  (2024) 12:6
<https://doi.org/10.1186/s40317-024-00364-3>

Animal Biotelemetry

METHODOLOGY

Open Access

Development of single-pin, un-barbed,
pole-tagging of free-swimming dolphins
and sharks with satellite-linked transmitters
Michael J. Moore1*, Thomas M. Lanagan2, Randall S. Wells3, Jason Kapit2, Aaron A. Barleycorn3, Jason B. Allen3,
Robin W. Baird4, Camrin D. Braun1, Gregory B. Skomal5 and Simon R. Thorrold1

Abstract
Background  To tag large marine vertebrates, without the need to catch them, avoiding using barbs for tag retention,
and precisely controlling tag location, the remote Tag Attachment Device on a pole (TADpole) was developed. This
allows single-pin tags (Finmount, Wildlife Computers) to be attached to the dorsal fins of free-swimming large marine
vertebrates.

Results  TADpole comprises a pole-mounted holster that carries a tag. It uses compressed air, and a micro-controller,
to rapidly insert a stainless-steel pin through a corrodible metal retaining ring in the first tag attachment wing,
the animal’s dorsal fin, and then a press fit Delrin retaining ring in the tag wing on the other side of the fin. Tag-
ging only occurs when the trailing edge of the dorsal fin touches a trigger bar in the holster, ensuring optimal pin
placement. It was developed using fins from cadavers, then trialed on briefly restrained coastal dolphins that could
be followed in successive days and weeks, and then on free-swimming animals in the field. The latter showed very
short touch/response intervals and highlighted the need for several iterative revisions of the pneumatic system.
This resulted in reducing the total time from triggering to tag application to ~ 20 ms. Subsequent efforts expanded
the TADpole’s applicability to sharks. One free-swimming Atlantic spotted dolphin, two white sharks, and one whale
shark were then tagged using the TADpole.

Conclusions  Being able to tag free-swimming dolphins and sharks remotely and precisely with satellite-linked
telemetry devices may contribute to solving conservation challenges. Sharks were easier to tag than dolphins. Dol-
phin touch-to-response times were 28 ms or less. Delphinid skin has unique polymodal axon bundles that project
into the epidermis, perhaps a factor in their uniquely fast response, which is 10 × faster than humans. Their primary
reaction to tagging is to abduct the flippers and roll the fin out of the TADpole holster. This device has the potential
to deliver high-quality tag data from large vertebrates with dorsal fins without the stress and logistics associated
with catch-and-release, and without the trauma of tags that use barbs for retention. It also collects a dorsal fin biopsy
core.

Keywords  Tags, SPOT, SPLASH, Touch response interval, White shark, Whale shark, Dolphin, Tag attachment

*Correspondence:
Michael J. Moore
<mmoore@whoi.edu>
Full list of author information is available at the end of the article

© The Author(s) 2024, corrected publication 2024. Open Access  This article is licensed under a Creative Commons Attribution 4.0
International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you
give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes
were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated
otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not
permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To
view a copy of this licence, visit http:// creat iveco mmons. org/ licen ses/ by/4. 0/. The Creative Commons Public Domain Dedication waiver
(http:// creat iveco mmons. org/ publi cdoma in/ zero/1. 0/) applies to the data made available in this article, unless otherwise stated in a
credit line to the data.

Moore et al. Animal Biotelemetry  (2024) 12:6

Page 2 of 16

Background
Tracking movements of animals has long been a primary
tool  of  wildlife  biologists.  The  ability  to  deploy  tracking
tags  remotely,  without  having  to  capture  individuals  for
manual attachment, and avoiding barbed or intramuscu-
lar  implants  [1,  2],  has  many  potential  benefits,  includ-
ing reduced stress and tissue trauma during and after tag
attachment,  decreased  risks  to  animals  and  people,  and
simplified logistics and costs.

In  cetaceans,  high-resolution  short-duration  archival
tags  such  as  the  DTAG  are  typically  attached  with  suc-
tion  cups  [3].  Satellite-linked  radio  transmitting  (SLRT)
tags allow for the collection of near-real-time geolocation
data over broader time scales. To achieve longer attach-
ment  duration  with  this  technology,  barbed  LIMPET
(Wildlife Computers, Redmond, WA USA) tags attached
via rifle, crossbow, or lance into the dorsal fin or base of
the fin have been used. Attachments on small cetaceans
are  typically  short.  For  SPLASH  tags  on  rough-toothed
dolphins (Steno bredanensis), mean duration was 13 days
(maximum  17)  [4].  Durations  of  up  to  three  months
were obtained for Cuvier’s beaked whales (Ziphius cavi-
rostris) [5] and false killer whales (Pseudorca crassidens)
[6].  Longer  durations  have  been  achieved  with  remotely
attached  transdermal  intramuscular  tags  [1],  but  they
have  the  potential  for  significant  tissue  trauma  [7–9].
Dedicated  tests  and  analyses  of  prior  tagging  data  have
demonstrated  that  a  single-pin  attachment  of  tags  to
the  dolphin  dorsal  fin  is  minimally  traumatic,  without
adverse impacts to health or behavior (e.g., FINMOUNT
SPLASH tag,) [10–13]. However, use of this approach has
been  limited  to  attachment  on  small  cetaceans  caught
briefly for tagging or for other interventions [11, 14–21].
The  median  tag  durations  of  single-pin  dorsal  fin  tags
on bottlenose dolphins (Tursiops truncatus) for a recent
study was 117–163 days [19], depending on the tag con-
figuration. With a safe and effective tag now available, a
means  of  safely  attaching  the  tag  to  dorsal  fins  without
the need for capture was desired.

In  sharks,  the  use  of  satellite-linked  tagging  to  exam-
ine  and  quantify  distribution,  habitat  use,  and  move-
ment  ecology  has  increased  dramatically  over  the  last
two decades [2]. The two most common technologies are
pop-up satellite-linked archival transmitting (PSAT; e.g.,
MiniPAT, Wildlife Computers) and SLRT (e.g., SPOT and
SPLASH tags) tags. The former are typically tethered to
an intramuscular dart inserted into the base of the dorsal
fin; PSAT tags can be programmed to detach (and trans-
mit  archived  data)  after  a  deployment  duration  of  up  to
one year. In contrast, SLRT tags transmit near real-time
data  when  the  shark  is  at  the  surface,  but  they  must  be
affixed to the apex of the shark’s dorsal fin. To do so, the
shark is captured, restrained and/or lifted from the water,

and the tag is usually attached by drilling four small holes
through  the  fin  and  securing  it  with  plastic  bolts. These
tags provide more accurate geolocations than PSAT tags
and have been successfully deployed for up to seven years
[22].  However,  unlike  air-breathing  mammals,  sharks
are  not  obligated  to  spend  time  at  the  surface,  and  the
amount  of  location  data  can  vary  within  and  between
species.  Moreover,  sharks  tagged  using  this  method  can
be  exposed  to  physiological  stress  and  physical  trauma
associated  with  capture,  handling,  and  tagging,  which
can impact post-release behavior [23] and cause perma-
nent gross deformation of the fin [24]. As noted above for
marine mammals, a single-pin tag that minimizes trauma
to  the  fin  and  can  be  applied  to  free-swimming  sharks
would be of value.

Thus, if off-the-shelf single-pin tags could be routinely
attached  to  free-swimming  cetaceans  and  sharks  that
have suitable dorsal fins, without the need to catch them,
there could be major improvement of medium-term tag
attachment  durations,  reduced  risk  of  injury  to  the  ani-
mals  and  people,  simplified  logistics,  reduced  expense,
and greatly increased deployment opportunities.

Methods
Overall approach

The design and development of a pole-based Tag Attach-
ment  Device  (TADpole)  evolved  through  iterative  steps
involving  biologists,  veterinarians,  and  engineers,  work-
ing  in  the  lab  and  in  the  field.  While  the  TADpole  was
conceived in the early 2000s, and initial designs proposed
in  2014,  work  to  develop  a  prototype  began  in  earnest
when  funding  was  first  obtained  in  2017.  Field  trials  on
dolphins  spanned  2018–2023.  In  2020,  the  device  was
tested  off  the  bow  of  a  small  vessel  off  Massachusetts,
USA  tagging  white  sharks  (Carcharodon  carcharias).  In
2022, the device was tested with an in-water approach to
tagging  whale  sharks  (Rhincodon  typus)  off  Massachu-
setts, USA. In 2023 a bow-riding (Stenella frontalis) dol-
phin was tagged west of Sarasota, Florida, USA.

Specifications

The initial intent of the TADpole was for a pole-mounted
apparatus  to  apply  a  single  attachment  pin  SPLASH  or
SPOT tag onto free-swimming dolphins while riding the
bow wave of a small boat. There were several design con-
siderations.  The  system  should  collect  a  biopsy  sample
simultaneous  with  tagging  to  allow  for  genetic  analyses
to confirm species and sex of the animal and assist with
genetic stock structure determinations. Similarly, the tag
attachment system was also required to have a corrodible
link  for  releasing  the  device  from  the  animal  following
battery exhaustion. The tag pin location relative to the fin
must enable the vee of the tag wings to be snug, but not

Moore et al. Animal Biotelemetry  (2024) 12:6

Page 3 of 16

compress the trailing edge of the dorsal fin, to minimize
abrasion of the tag on the fin. The distance from the trail-
ing edge of the fin to the tag attachment pin (38 mm) was
established  from  examination  of  the  relative  success  of
previous  tag  attachments,  and  with  the  intent  to  reduce
the  potential  of  injury  from  tag  pin  migration  to  be  no
more serious than injuries dolphins and sharks inflict on
one  another  [12,  25].  The  design  allowed  for  tagging  a
dorsal fin up to 26 mm wide at the pin location, being the
maximum width of dorsal fin samples of common bottle-
nose dolphin dorsal fins measured at that position.

Design

Before  embarking  on  a  detailed  design,  a  brief  field  test
was  conducted  in  April  2015  off  Sarasota,  FL,  with  a
mock-up  tool,  a  Y-shaped  pole-end  fitting,  to  ensure
that it was indeed possible to place it around the caudal
aspect  of  the  dorsal  fin  of  a  bow-riding  bottlenose  dol-
phin. The initial tests were successful, and the design pro-
gressed into a conceptual design phase.

The  initial,  manual,  catch-and-release  approach  for
applying SPOT and SPLASH tags used a sharpened cork-
borer to make a hole in the dorsal fin [10]. This was done
by hand and estimated to require approximately 23 kg (50
lbs)  of  force.  A  cordless  drill  with  a  sharpened  tube  can
also be used. Significantly more force would be required
to  rapidly  tag  a  moving  dolphin  during  the  brief  time  it
surfaces to breathe. Springs or compressed air were con-
sidered as a source of this force. With the requirement to
recover a biopsy sample from the animal, a reciprocating
linear motion was preferable.

Figure 1 illustrates the overall design. Design drawings,
specifications,  dimensions,  and  operating  instructions
are archived at the Woods Hole Open Access Server [26].
Microcontroller  code  is  archived  on  GitHub  [27].  A  tag
is  inserted  into  the  Y-shaped  TADpole  holster,  which
is  mounted  on  the  base  of  a  hollow,  telescoping  carbon
fiber  pole.  The  TADpole  is  deployed  by  an  operator  on
the  bow  of  a  small  vessel,  ideally  equipped  with  a  bow
platform  or  pulpit  to  provide  a  better  view  of  bow-rid-
ing dolphins and allow a free range of movement of the
TADpole  system  in  front  of  the  bow. The  pole  length  is
adjustable, 2–4 m long and 5 cm in diameter. The system
weighs  3.6  kg  (holster  2.1  kg,  poles  1.5  kg).  The  opera-
tor maneuvers the holster behind the trailing edge of the
dorsal  fin  of  a  bow-riding  or  surface-swimming  animal
(Fig.  2).  The  TADpole  is  configured  as  follows.  The  tag
holster  is  attached  to  a  valve  housing  at  the  base  of  the
pole (Figs. 1 and 2). The tag is provided by the manufac-
turer with V-shaped wings that wrap around the fin from
behind, with a mounting hole in each wing to secure the
tag  to  a  restrained  animal’s  dorsal  fin.  For  the  TADpole
application,  these  holes  are  enlarged  using  a  punch  to

2

1

7

6

5

3

4

4

1. Valve housing
2. Pneumatic cylinder
3. Tag wings with pin through metal ring, above Delrin ring
4. Delrin guides
5. Left tag wing with Delrin ring
6. Holster
7. Tag body

Fig. 1  TADpole configuration used for dolphin and shark trials
viewed from below. The aluminum holster has Delrin guides
to position it around the dorsal fin (Fig. 2). The pole has a valve
cylinder at its base, attached to the holster. A pneumatic cylinder
is mounted to the holster with its piston in line with the Delrin
and metal rings press fit into the tag wings. A pusher, sleeved
by a dart, is threaded into the piston. When the trailing edge
of the dorsal fin is surrounded by the tag wings, it triggers the piston
to push a dart through the rings and the dorsal fin (insert). The dart
is retained by a press fit into the Delrin ring. The piston retracts
the pusher, leaving the animal free to swim off with the tag

1. Dorsal fin
2. Trigger
3. Valve chamber
4. Antenna
5. Holster
6. Tag
7. Microswitch
8. Tag wings
9. Guide
10. Pneumatic cylinder

3

4

1

2

10

9

5

7

6

8

Fig. 2  Schematic drawing of the TADpole, positioned on a dorsal fin
ready to apply a tag. The valve in the housing delivers compressed
air to the cylinder to actuate the tagging cycle when triggered. The
Delrin guides shown in Fig. 1 are not shown here

 Moore et al. Animal Biotelemetry  (2024) 12:6

Page 4 of 16

enable  retaining  rings  to  press  fit  into  each  wing  (Fig.  1
inset).  The  ring  inserted  in  the  right  tag  wing  (looking
down on the upper, antenna side of the tag) is corrodible
(magnesium or aluminum), while the ring inserted in the
left tag wing is Delrin (Fig. 1 inset) [26]. The rings in the
tag wings are secured in U-shaped retaining clips on each
side of the holster, with the holes in line with the axis of a
pneumatic piston in an aluminum cylinder (Fig. 1) on the
right side of the holster.

The  tagging  actuation  cycle  shown  schematically  in
Fig. 3, involves a hollow pin, sleeved over a hollow pusher
threaded  into  the  piston  (Figs.  4  and  5).  The  pusher
passes  the  pin  through  the  corrodible  ring,  with  a  loose
fit. It then takes a biopsy core through the dorsal fin, and
finally pushes the shouldered, beveled pin tip with a press
fit through the Delrin ring (Figs. 4, 5 and 6). The base of
the  pin  also  has  a  shoulder  that  seats  on  the  corrodible
ring, and hence holds the right tag wing against the right
side of the dorsal fin (Fig. 6). The press fit pin head in the
Delrin ring holds it and the left tag wing against the left
side of the fin. Once the pin, and hence tag and retaining
rings,  are  attached  to  the  dorsal  fin,  the  piston  rod  and
pusher retract (Fig. 7) with the biopsy retained by a small

barb  protruding  into  the  hollow  pusher.  The  swimming
force  of  the  animal  pulls  both  retaining  rings  out  of  the
clips on the holster, and the tagged animal swims free.

The  actuation  cycle  is  only  triggered  after  turning  on
the controller power and pressurizing the solenoid valve,
when  the  operator  thrusts  the  holster  forward  immedi-
ately behind the trailing edge of the dorsal fin of a bow-
riding  animal,  to  the  point  that  the  dorsal  fin  depresses
a  horizontal  metal  trigger  bar  at  the  base  of  the  holster
vee  (Fig.  2).  This  can  only  happen  when  the  vee  of  the
tag  wings  is  snug  against  the  trailing  edge  of  the  dorsal
fin,  a  location  previously  shown  to  be  optimal  for  sin-
gle-pin  dorsal  fin  tags  [10,  13].  Trigger  depression  acti-
vates  a  micro-controller  coded  sequence  of  commands
to  the  pneumatic  valve  to  extend  and  retract  the  piston
at  defined  intervals,  to  successfully  attach  the  tag  as
described above. The actuation cycle  is optimal at 20 ms
(adjustable).  The  system’s  working  pressure  is  1517  Pa
(220  psi),  using  a  regulated  supply  from  a  20,685  kPa
(3000 psi) capacity dive cylinder.

The tag remains attached to the fin until the corrodible
ring  has  lost  sufficient  material  that  its  inside  diameter
exceeds the outside diameter of the shoulder at the base

Fig. 3  Flowchart for TADpole operation. Pneumatic cylinder, trigger and micro-switch are on holster (Figs. 1 and 2), valve in valve chamber at base
of pole, to which holster is attached. Controller, batteries (2 × 12 V in series), and relays are in a control box on deck. Wiring from control box,
and hose from dive cylinder pass inside pole to valve chamber and then holster

Moore et al. Animal Biotelemetry  (2024) 12:6

Page 5 of 16

1

2

3

4

5

7

1. Pneumatic cylinder
2. Piston
3. Pusher
4. Metal retaining ring
5. Hollow pin
6. Dorsal fin
7. Delrin retaining ring

6

Fig. 4  Deployment mechanism—exploded view from below. Pusher threads onto cylinder piston rod. Tag dart slides over pusher. Dielectric grease
on base of pusher shaft holds dart in place until deployed. Ring on left is corrodible metal and right is Delrin

1. Piston rod
2. Pusher
3. Pin inserted over pusher
4. Metal retaining ring
5. Dorsal fin
6. Delrin retaining ring

1. Piston rod
2. Pusher
3. Pin inserted through fin and rings
4. Metal retaining ring
5. Dorsal fin
6. Delrin retaining ring

1

2

3

4

5

6

1

2

3

Fig. 5  Actuation cycle step 1: armed configuration of tag dart
deployment system. The hollow dart, inserted onto the pusher, ready
to be extended by the piston through the corrodible ring, the dorsal
fin and then press fit into the second, Delrin ring

Fig. 6  Actuation cycle step 2: hollow tag dart pusher extended, dart
engaged in retaining rings and dorsal fin. The pusher can have a small
barb on its inner wall to retain the resulting biopsy core

4

5

6

of  the  pin.  At  that  point  the  right  tag  wing  will  detach
from the fin, and the ensuing asymmetric drag on the tag
will work the pin back out of the tag attachment hole and
release the tag, leaving no foreign body in the fin, allow-
ing repair/healing to ensue.

The  micro-controller  and  batteries  to  power  the  con-
troller and valve are in a customized, waterproof Pelican
case  secured  to  the  deck  of  the  vessel.  The  cable  con-
necting the holster micro-switch and valve to the micro-
controller, and the air hose from the compressed air tank
to  the  valve  pass  down  the  hollow  pole.  To  control  the
cylinder’s actuation with millisecond time resolution, an

Arduino  Uno  micro-controller  (https:// store- usa. ardui
no. cc/ produ cts/ ardui no- uno- rev3),  a  waterproof  MIL
spec  micro-switch  (https:// <www>. mcmas ter. com/ 7517K
33/),  and  a  5-way  solenoid  valve  were  selected  (https://
<www>. autom ation direct. com/ adc/ shopp ing/ catal og/
pneum atic_compo nents/ direc  tional_ contr ol_solen oid_
valves/ solen oid_ valves/ avs- 5121- 24d). For low-cost com-
pressed air, a portable air compressor capable of 1138 kPa
(165 psi) max was used at first. Subsequent iterations of
the design used a standard SCUBA compressed air tank
with  a  single  stage  regulator.  The  exhaust  air  from  the
valve  chamber  is  discharged  via  a  1  m  air  hose  extend-
ing up the pole to avoid sea water ingress into the valve

Moore et al. Animal Biotelemetry  (2024) 12:6

Page 6 of 16

1. Piston rod
2. Retracted pusher
3. Pin engaged in both tag rings
4. Dorsal fin

1

2

3

4

Fig. 7  Actuation cycle step 3: pusher and piston retracted
with biopsy inside pusher barrel, leaving the tag attached
to the dorsal fin, and the retaining rings to disconnect from the clips
on the tag holster as the animal swims off

assembly.  Corrodible  rings  for  tag  release  were  made  of
magnesium for short-term initial testing, with a plan for
using  aluminum  for  longer  deployments.  The  current
design is illustrated and detailed in Figs. 1, 2, 3, 4, 5 and
6. The holster is loosely tethered to the vessel by a 6 mm
diameter  Dyneema
(https:// <www>. appli ed- fiber. com/)
braided line, to retain the holster in the event of a failure
of  the  pusher  to  retract  during  the  actuation  cycle,  or  a
fracture of the pole/holster connection.

Laboratory testing

Best practice guidelines for cetacean tagging [1] encour-
age  refinement  of  tags  and  attachment  techniques,  with
suitable testing on carcass tissue, to achieve effective and
consistent  operation  before  use  on  live  animals.  Frozen
cadaver bottlenose dolphin dorsal fin samples from beach
stranding mortalities were thawed, and the TADpole sys-
tem  iteratively  tested  to  ensure  complete  tagging  cycles
occurred,  with  minimum  actuation  cycle  time.  Tests  in
the lab and in the field were documented through video
recordings,  allowing  frame-by-frame  analysis.  Success
with lab tests led to field tests on dolphins during 2018–
2023, and tests with white sharks in November 2020, and
whale sharks in September 2022 with each field test lead-
ing to further refinements and lab testing.

cylinder  sizes  and  pressure  capacities  were  tested. The
specifications  for  the  current  system  components  are
available  [26].  Step-by-step  detailed  instructions  for
use  of  the  TADpole,  and  description  of  the  hardware
and  software  are  provided  in  the  TADpole  Operations
Manual.  The  operational  pressure  for  the  system  is
1517 kPa (220 psi), being the upper functional limit for
the solenoid valve.

Pin sterilization and handling

Pins  were  autoclaved  prior  to  field  trials  and  then  han-
dled  using  sterile  gloves.  A  small  amount  of  electrical
insulating  compound  #4  (Dow  Corning)  was  applied  to
the base of the pin before inserting it on to the pusher to
avoid it sliding down the pusher shaft while the holster is
being maneuvered to the dorsal fin.

Field testing

Once consistent results were obtained in the laboratory,
dolphin field trials were undertaken off Sarasota, Florida,
U.S.A.,  during  April–June  2018,  June  2019,  May  2021,
October  2022,  May  2023,  and  August  2023,  and  off  the
island  of  Hawai‘i,  U.S.A.,  during  November  2018.  The
vessel was operated near dolphins. If they chose to bow
ride,  a  tagging  attempt  was  made  if  feasible.  Trials  with
white  sharks  were  undertaken  east  of  Chatham,  Mas-
sachusetts,  U.S.A.,  in  November  2020.  Trials  with  the
whale  shark  were  undertaken  south  of  Martha’s  Vine-
yard, Massachusetts, USA, in September 2022. All these
tests except the whale shark used the system on a hand-
held pole as described above. The whale shark trial vessel
was incompatible with the pole approach, so the control
system (in a waterproof enclosure), and the air tank were
mounted  on  a  small  raft  pushed  by  a  swimmer  follow-
ing behind the tagging swimmer with hoses and control
cable between them. The whale shark’s dorsal fin was too
compliant for triggering the tag on its trailing edge, so the
tag was manually placed and then triggered by the swim-
mer’s finger on the trigger.

Video analysis

Iterative modifications

During  laboratory  cadaver  sample  tests,  to  minimize
the  delay  in  the  pneumatic  system,  the  valve  that  was
initially  located  in  the  deck  control  box  was  moved
to  the  valve  chamber  at  the  base  of  the  pole  (Fig.  2).
Higher  flow  and  pressure  valves  were  tested,  pres-
sure  was  increased  from  896  kPa  (130  psi)  with  a  bat-
tery  powered  air  compressor,  to  a  SCUBA  tank,  with
pressure options up to 20,685 kPa (3000 psi). Different

Videos  of  dolphin  trials  in  the  field  and  laboratory  were
acquired  using  a  GoPro  Hero6  Black  camera  (https://
gopro. com/). Then, using Final Cut Pro X 10.4.1 (https://
apps. apple. com/) to scroll through frames to identify sig-
nificant  events—the  numbers  of  frames  between  events
were  converted  to  elapsed  time  using  frame  per  second
recorded. Events included: first touch, behavioral changes
such  as  bubble  streams,  roll,  flipper  movement,  pump
tail, and accelerate.

Moore et al. Animal Biotelemetry  (2024) 12:6

Page 7 of 16

Results
Laboratory testing

As the hardware and software evolved, iterative lab tests
were  critical  to  ensure  that  the  system  was  reliably  tag-
ging cadaver fins. However, the absence of the dynamics
of sea state and animal behavior made successive field tri-
als essential and informative.

Dolphin tagging efficiency in field

Days spent in the field to test the TADpole varied widely
in terms of sea state and availability of potential tagging
candidates.  Table  1  summarizes  the  field  sites,  and  spe-
cies  involved  in  tagging  attempts  at  each  site,  including
bottlenose,  pantropical  spotted  (Stenella  attenuata),
Atlantic  spotted,  and  rough-toothed  dolphins  (Steno
bredanensis),  and  melon-headed  whales  (Peponocephala
electra). Thirty-one individual dorsal fins were contacted
over 22 days at sea. On 17 occasions, the device triggered,
but  the  pin  did  not  fully  penetrate  through  the  fin,  and
therefore failed to press fit into the second retaining ring
to  complete  the  tag  attachment.  On  one  occasion  a  tag
was successfully attached and is described in detail below
(Fig.  8).  On  four  occasions,  a  partial  biopsy  sample  was
obtained  from  the  pin  dragging  across  the  dorsal  fin  as
the animal rolled out of the holster before the actuation
cycle could be completed.

Assessment of restrained, tagged Sarasota Bay bottlenose
dolphins

As  part  of  Sarasota  Dolphin  Research  Program  bottle-
nose dolphin health assessments, during a brief restraint
onboard a vessel, two dolphins were tagged in 2022 using
the  TADpole  device,  using  magnesium  corrodible  rings.
On  May  18th,  2022,  dolphin  F293  was  tagged.  The  tag

Fig. 8  Dorsal view of Wildlife Computers SPLASH10 tag attached
to dorsal fin of Atlantic spotted dolphin, August 15th, 2023

continued to transmit through June 22nd, 2022. On July
6th, 2022, the animal was observed without the tag, with
a small healing hole at the tag site. The tag was attached
for 35–49 days. A second dolphin, F322 was tagged May
19th,  2022.  The  tag  continued  to  transmit  through  June
10th,  2022,  and  then  was  observed  on  June  14th,  2022,
with the tag off with no evidence of tag trauma except the
small hole made by the pin (Fig. 9). The tag was attached
for  22–26  days.  Both  dolphins  were  observed  after  tag
loss, and the tag holes have fully healed without compli-
cations (Figs. 10 and 11).

In  May  2023,  two  restrained  dolphins  were  tagged  by
the  TADpole  during  Sarasota  Dolphin  Research  Pro-
gram  bottlenose  dolphin  health  assessments,  using  alu-
minum  corrodible  links  to  test  their  durability.  On  May
11th,  2023,  dolphin  F292  was  tagged  (Fig.  12).  The  ani-
mal was first seen after tagging, without the tag, on May
23rd, 2023. Transmissions ceased on May 15th, 2023, so
the  dolphin  lost  the  tag  within  4–12  days  of  tagging.  A
small  hole  remained  at  the  tag  attachment  site  on  May

Table 1  Summary of TADpole field trial events with dolphins

Start date

Field days

Field site

Vessel

Species (no. of attempts)

Contact,
no trigger

Trigger

Tag

2018 Apr 09

2018 May 16

2018 Jun 02

2018 Jun 10

2018 Nov 10

2019 Jun 27

2021 May 24

2022 Oct 17

2023 May 15

2023 Aug 15

1

2

1

1

8

3

3

1

1

1

Sarasota Bay

Sarasota—offshore,
Sarasota Bay, Tampa Bay

Egmont Key—offshore

Stump Pass—offshore
Hawaiʻi

Nai’a

Nai’a

Nai’a

Nai’a

Cascadia

Tursiops truncatus (0)

Tursiops truncatus (2)

Tursiops truncatus (2)

Tursiops truncatus (1)

Tursiops truncatus (2), Stenella attenuata
(12), Peponocephala electra (2)

Sarasota—offshore

R/V WR Mote

Stenella frontalis (5)

Sarasota—offshore

R/V Eugenie Clark

Tursiops truncatus (1), Stenella frontalis (1),
Steno bredanensis (5)

Sarasota—offshore

R/V Eugenie Clark

Steno bredanensis (4)

Sarasota—offshore

R/V Eugenie Clark

Tursiops truncatus (1)

Sarasota—offshore

R/V Eugenie Clark

Tursiops truncatus (1), Stenella frontalis (9)

0

2

1

1

12

3

3

4

1

4

0

0

0

0

4

2

4

1

1

6

EVENT TOTAL

22

48

31

18

0

0

0

0

0

0

0

0

0

1

1

 Moore et al. Animal Biotelemetry  (2024) 12:6

Page 8 of 16

Fig. 10  F293 healing after tag loss. a July 5th, 2022. b September 6th,
2023

Fig. 9  Bottlenose dolphin tag F322. a Tag being applied using
the TADpole during temporary restraint, May 19th, 2022. b Tag
attached to F322, May 19th, 2022. c Individual sighted on June 8th,
2022. This individual was sighted again June 14th, with the tag gone,
and the tag area looked ‘clean’, but no adequate photographs were
available

23rd. On May 12th, 2023, dolphin F326 was tagged. The
animal was last reported with the tag on September 5th,
2023,  after  transmissions  had  ceased,  and  was  first  seen
without  the  tag  on  September  12th,  2023,  indicating  a
tag attachment duration of 115–123 days, as desired. Fig-
ure 13 shows the tag site on September 12th, November
7th, 2023, and January 15th, 2024. In both cases, the tags
came off the fin as designed leaving a small hole, and by
August and November 2023, respectively, both fins were

Fig. 11  F322 healing after tag loss. a July 5th, 2022. b December 5th,
2022. c March 22nd, 2023

Moore et al. Animal Biotelemetry  (2024) 12:6

Page 9 of 16

Fig. 12  F292 healing after tag loss. a March 23, 2023. b August 4th,
2023

well-healed (Figs. 12 and 13). The reason for the short tag
attachment  duration  for  F292  is  not  known,  but  it  was
too brief to have been the result of corrosion. The attach-
ment duration for F326 suggests that aluminum is a rea-
sonable choice for the corrodible retaining ring.

Behavioral responses by dolphins

For  each  restrained  animal,  a  single  startle/jerk  reaction
was observed as the pin passed through the fin. For bow-
riding animals, the commonest response of a dolphin to
the tool touching the dorsal fin was to quickly abduct the
flippers and roll laterally, often to as much as 90 degrees.
In some cases, forward acceleration or dropping in eleva-
tion was observed. When the initial designs of the device
triggered,  the  animals  usually  reacted  faster  than  the
device could complete its task. This led to various adjust-
ments to the hardware and software. These included min-
imizing the length of air hose between the valve and the
cylinder,  maximizing  the  working  air  pressure,  reducing
the wall thickness of the pin from 1.82 mm to 1.02 mm,
and ensuring its cutting tip was freshly sharpened.

Video analysis of touch‑to‑response times

We  used  the  video  data  from  the  2021  season  to  evalu-
ate the device. Table 2 shows that the touch-to-response
time ranged from 3 to 28 ms. In one case the video also
showed the movement of the trigger, and the pusher/pin
assembly.  The  biggest  delay  was  from  the  first  touch  to
when the trigger began to move. To establish the deploy-
ment  timing  of  the  TADpole  device  in  the  laboratory,

Fig. 13  F326 healing after tag loss. a September 12th, 2023. b
November 7th, 2023. c January 15th, 2024

videos  were  taken  of  the  device  triggering  without  any
dorsal  fin  in  the  holster.  For  three  consecutive  trials,
the  time  from  triggering  to  extension  ranged  from  9  to
15 ms, and from triggering to retraction was 20–26 ms.

Free‑swimming dolphin tagging

A  bow-riding  presumed  adult  female  Atlantic  spotted
dolphin  was  tagged  on  August  15th,  2023,  85  km  off-
shore  of  Sarasota,  Florida  (Figs.  8  and  14).  The  tag  was
deployed  from  a  custom  bow  pulpit  on  Mote  Marine
Laboratory’s 14-m R/V Eugenie Clark with the tag opera-
tor’s feet 0.5 m above the sea surface. The standard Wild-
life  Computers  SPLASH10  Finmount  tag  was  attached.
To  minimize  the  actuation  cycle  duration  there  was  no
biopsy retaining barb in the pusher. Despite this, a full fin
core sample was retained. The corrodible ring was made
of  aluminum.  Conditions  were  nearly  ideal—calm  seas
and  slow-moving,  persistently  bow-riding  dolphins.  The
angle of the holster relative to the pole was altered to be

 Moore et al. Animal Biotelemetry  (2024) 12:6

Page 10 of 16

Table 2  Summary of TADpole touch to behavioral response times

Date

Set

Touch to response

Touch to
trigger

Trigger to fire

Trigger to fin

Result

May 24 2021

May 27 2021

May 27 2021

May 27 2021

May 27 2021

May 27 2021

1

1

2

3

4

5

20–28

14

16

13

8 to 19

3 to 12 (prior bubble stream,
possibly wary)

18

6

10

None

Triggered

Triggered

None

Biopsy

Triggered and Biopsy

Time in milliseconds (ms) in six common bottlenose dolphins attempts in May 2021, offshore Sarasota, FL, from video frame time analysis. May 27 set 1 was the only
event with a video record of the trigger/ pusher/ pin movements. No tags were successfully attached in this series. However grazing biopsies were obtained on two
occasions. Based on these data the wall thickness of the pin was reduced

more  acute,  in  response  to  dolphins  riding  close  to  the
bow  of  the  vessel,  facilitating  trigger  contact  by  the  fin
when the tool was in appropriate position. Two previous
contacts on other dolphins earlier in the day with a more
obtuse  angle  as  would  be  required  for  dolphins  farther
ahead  of  the  bow  had  resulted  in  premature  triggering,
before the tag was in place on the fin. The dolphin leaped
repeatedly immediately after tagging, but returned to the
bow multiple times, affording good views of the attached
tag (Fig. 8). The tag transmitted for 31 days, as the animal
ranged  through  waters  frequented  by  Atlantic  spotted
dolphins  (Fig.  15).  Transmissions  ceased  due  to  battery
exhaustion.

Shark tagging

Two  white  sharks,  approximately  3.7  and  4.4  m  in  total
length, were tagged with SPOT tags from the 3.4 m-long
bow  pulpit  of  a  7.3  m  vessel  off  Chatham,  MA  on  7
November  2020.  Both  sharks  were  free-swimming < 1  m
below  the  surface  when  tagged  and  reacted  by  moving
slowly  away  from  the  tagging  vessel.  An  overhead  view
of  shark  tagging  is  shown  in  Fig.  16  and  an  image  of  a

Fig. 14  Atlantic spotted dolphin with tag remotely applied using
the TADpole while bow-riding August 15th, 2023

successfully  tagged  shark  is  shown  in  Fig.  17.  No  loca-
tions  were  reported  from  either  of  these  tags.  However,
one of the tags reported intermittently over the next five
months until 17 April 2021; unfortunately, tag communi-
cation with the satellite was not long enough to calculate
a  position.  When  this  shark  was  resighted  after  2  years
(28  November  2022),  the  tag  was  gone,  and  the  fin  was
well-healed.  One  whale  shark  was  successfully  tagged
by a swimmer as described above (Fig. 18), a second tag
attempt  was  triggered,  but  the  pin  did  not  fully  press
into the Delrin ring, so the tag swimmer removed the tag
manually.  This  resulted  from  inadequate  air  pressure  in
the small volume scuba cylinder that was used to power
the system. The resulting tag data are shown in Fig. 19.

Discussion
The  TADpole  has  potential  for  conservation  research
with  dolphins,  and  white  and  whale  sharks.  The  funda-
mental  method  appears  to  have  value,  but  to  enhance
efficiency,  especially  for  using  it  with  small  cetaceans,
there are some matters to consider.

Dolphin evasive behavior

During the dolphin field trials, the biggest challenge was
to complete the actuation cycle before the animal evaded
the attempt by rolling, as described above. The dolphins
were  acutely  sensitive  to  touch  by  the  TADpole,  and
adept at avoiding it once sensed. Earlier studies of human
reaction  times  (mean ± SEM  milliseconds)  to  painful
stimuli to the hand were 387 ± 20 ms whereas reaction to
tactile  stimulation  was  361 ± 25  ms  [28].  From  a  review
by Caldwell et al. [29]: “Human tactile, perceptual mean
reaction times from one study in untrained, healthy vol-
unteers have been found to vary between 210 and 400 ms
[30],  but  can  range  down  to  140–150  ms  with  practice
for certain individuals [31]. Reaction times for individu-
als  tend  to  stay  relatively  constant  between  ages  25  and
60”.  Thus,  from  the  data  in  Table  2,  dolphins  seem  to

Moore et al. Animal Biotelemetry  (2024) 12:6

Page 11 of 16

Fig. 15  Locations obtained of tagged Atlantic spotted dolphin over a one-month period

react to touch an order of magnitude faster than humans,
although we cannot say for sure that they were not pre-
alerted  by  visual  or  acoustic  stimuli  before  the  tool  first
touched  the  dolphin,  or  that  the  very  act  of  bow  riding
puts  them  on  high  alert.  But  tactile  stimulus  reaction
times in the teens for dolphins vs. hundreds of millisec-
onds in humans is striking.

In  the  skin  of  bottlenose  dolphins,  Palmer  et  al.  [32]
described  richer,  more  elaborate  and  specialized  neural
structures than in humans. These tunneled into the rete
peg base terminating in unique papillary wall complexes,
some of which penetrated the epidermis up to three cell
layers  from  the  surface.  Eldridge  et  al.  [33]  described
how humpback whale (Megaptera novaeangliae) skin has

 Moore et al. Animal Biotelemetry  (2024) 12:6

Page 12 of 16

Fig. 16  Aerial view of white shark TADpole tagging event November
8th, 2020

Fig. 17  SPOT tag attached to white shark dorsal fin using
the TADpole tool. November 8th, 2020

been  shaped  by  the  aquatic  environment  to  sense  flow,
turbulence,  and  boundary  layers  as  well  as  touch  and
noxious  stimuli.  Visualizing  afferent  neural  structures
immunochemically,  they  described  unique  threadlike
heterogenous axon bundles in humpback whale skin, that
divided  into  smaller  bundles  without  structural  endings
at the dermal/epidermal junction, with ‘an exceptionally
dense low threshold mechanosensory system innervation
most likely adapted for sensing hydrodynamic stimuli’. If
proven relevant to all cetaceans, these observations may
be the basis for the remarkably rapid dolphin touch reflex
observed in our study. One might speculate that the dol-
phins’  rapid  rolling  reaction  evolved  at  least  in  part  in

Fig. 18  SPOT tag attached to whale shark dorsal fin using
the TADpole —September 4th, 2022

response  to  predation  attempts  by  sharks,  as  evidenced
by frequent observations of shark bite wounds exhibiting
scraping marks from teeth in one jaw as the dolphin pre-
sumably rolled out of its mouth (Fig. 20).

Tagging efficiency

Success of the tagging effort was predicated on the abil-
ity  to  place  the  tool  where  it  would  trigger  an  event,
the  duration  of  the  consequent  actuation  cycle,  and  the
ability  of  the  pin  to  penetrate  the  dorsal  fin  efficiently
and  press  fit  through  the  Delrin  ring  before  the  animal
was able to react and evade the attempt. Data in Table 2
showing  the  collection  of  biopsies  from  the  pin  tip  as
dolphins dropped and rolled out of the TADpole holster
reflect  events  where  the  tool  fell  short  of  completing  its
task.  This  resulted  in  changes  being  made  to  the  pneu-
matic  system  such  as  minimizing  the  length  of  the  air
hoses between the valve and the cylinder, optimizing the
size of the cylinder, maximizing the cutting efficiency of
the  pin,  minimizing  any  mechanical  latency  in  the  trig-
ger mechanics, optimizing the ergonomics of the angle of
the  tool  relative  to  the  pole,  adjusting  the  angle  relative
to the distance of the dolphin from the bow of the boat,
and  positioning  of  the  tagger  relative  to  where  the  dol-
phin swam.

Metal retaining rings

We initially considered magnesium, zinc, and aluminum.
We decided to do the initial attachment trials with mag-
nesium  to  generate  maximum  corrosion,  and  thence,
short attachment times. The two tags remained attached
for about a month from the Sarasota Bay follow-up obser-
vations.  We  did  this  in  case  there  were  any  unforeseen
health  impacts  from  the  tag  attachment.  We  observed
none. Longer attachments could be attained with a metal
lower in the galvanic series, such as aluminum or brass.

Moore et al. Animal Biotelemetry  (2024) 12:6

Page 13 of 16

Fig. 19  Locations of whale shark over a 19-day period

Fig. 20  Fresh shark bite on 2-year-old female bottlenose dolphin
“2094” in Sarasota Bay, Florida, in April 2023, suggestive of rolling
out of the shark’s jaws. Tooth scrape marks on a right and b left, side
of the peduncle

Subsequent  tests  in  Sarasota  Bay  used  aluminum,  and
this  was  also  used  for  the  offshore  tagging  of  the  free-
ranging  dolphin.  No  adverse  health  effects  were  noted
for the Sarasota Bay dolphins. One tag with an aluminum
ring came off the dorsal fin of an inshore dolphin within
4–12  days  of  tagging  for  unknown  reasons  probably
unrelated to the metal of the ring. The tag on the offshore
dolphin ceased transmitting after 31 days due to battery
failure,  so  the  full  duration  of  attachment  could  not  be
documented, and the other inshore dolphin retained the
tag  for  115–123  days,  a  reasonable  amount  of  time  for
tracking SPLASH tags.

Biopsy

During  the  trials  to  minimize  the  TADpole  actuation
cycle, we elected to remove the biopsy retaining barb in
the pusher as we were concerned it might slow down the
extension  phase.  Once  we  have  more  experience  with
successful dolphin tagging events, using that barb should
be  a  consideration.  Future  shark  tagging  efforts  should
use barbed pushers.

Pin length

When single-pin tags are attached to restrained animals,
the width of the fin can be measured, and the pin length

 Moore et al. Animal Biotelemetry  (2024) 12:6

Page 14 of 16

cut  to  match  the  fin  width.  Obviously,  this  cannot  be
done  on  a  bow-riding  animal.  Thus,  we  opted  to  design
the  TADpole  for  the  likely  maximum  width  of  most
dolphin dorsal fins at the point where the pin was to be
inserted. Hence our choice to design the TADpole to be
able to penetrate up to 26 mm of fin width. The tool will
certainly tag narrower fins, however the drawback of this
is  that  the  pin/rings  complex  is  not  fully  flush  with  the
dorsal fin in smaller animals. This will lead to the poten-
tial  for  marginally  more  drag,  and  possibly  increased
snagging  of  debris  and  active  fishing  lines.  Only  once  a
significant  number  of  deployments  have  been  under-
taken  in  areas  where  follow-up  observations  are  likely
will  the  extent  of  this  concern  be  apparent.  We  have
actively discussed a pin that could dynamically adjust to
the fin width, to overcome this concern, but there was no
obvious way to do this.

Tag placement

The design of the holster provides an absolute limit of the
distance the tag pin can be from the trailing edge of the
dorsal fin. The major vessels in the fin are anterior to this
position.  This  distance  from  the  trailing  edge  of  the  fin
and vertical positioning was established through experi-
ence  tagging  77  dolphins  with  single-pin  radiotags,  and
designed to minimize the potential for dorsal fin damage
[13].  Thus,  despite  our  inability  to  closely  examine  the
dorsal fin as one can with a restrained animal, the risk of
the pin passing through a large vessel is very low.

Sharks

The  use  of  the  TADpole  on  white  and  whale  sharks
raises some questions about how to optimize the design
for  those  two  species.  The  white  shark  tagger  found  it
possible  to  use  the  tool  deeper  in  the  water.  Unfortu-
nately,  no  positions  were  derived  from  these  two  tags.
Upon consultation with the tag manufacturer, we con-
clude  that  the  tags  were  placed  too  low  on  the  dorsal
fin.  For  this  tag  design  (i.e.,  horizontal  single  point),
virtually the entire tag must clear the water before the
wet/dry  sensor  initiates  transmission.  Therefore,  we
recommend that the tags be placed much closer to the
apex  of  the  dorsal  fin,  as  was  the  case  with  the  whale
shark. The whale shark tagging protocol departed from
the deck-based tagger and used swimmers instead. Both
shark  events  flooded  the  valve  via  the ~ 2  m  exhaust
tube, a design constraint that was implemented to min-
imize  the  vent  tube  length  and,  presumably,  minimize
pneumatic drag. A one-way exhaust valve (e.g., https://
<www>. mcmas ter. com/ 7933K 27/)  should  be  considered
for  shark  tagging.  While  it  will  prolong  the  actuation
cycle,  minimizing  its  duration  does  not  appear  to  be  a
concern in the sharks where touch reactions seem to be

less  of  an  issue  in  our  field  trials,  given  the  high  suc-
cess rate compared to that of the dolphins. Our results
suggest that additional trials with large, free-swimming
sharks are a promising future avenue for tagging with-
out capture and handling of the animal.

Conclusions
The  TADpole
characteristics:

tagging

tool  has

the

following

•  Enables  tagging  of  free-swimming  dolphins  and

sharks.

•  Avoids  the  stress  of  capture/restraint  to  manually
attach tags. Animals that are tagged while bow riding
approach and leave the boat at will.

•  Trauma  from  the  tag  and  attachment  is  compara-
ble  to  that  of  single-pin  dorsal  fin  tags,  and  hence
provides  the  potential  for  longer  tag  durations  than
reported for remotely deployed, barb-retained tags.
•  Requires  a  smaller  team  and  less  expense  than  a

catch-and-release expedition for tagging.

Future steps should include:

•  Further  use  of  the  TADpole  tool  with  resident  dol-
phin  populations  to  undertake  post-tagging  follow-
up  observations  of  tag  attachment  sites  before  and
after tag loss.

•  More  development  of  the  TADpole  hardware  and
software  specific  for  the  requirements  of  different
dolphin and shark species, especially to enhance the
efficiency of dolphin tag application.

•  Use of the tool to tag offshore dolphins without the
need for restraint, to establish the potential value of
this novel technique.

•  Use  of  aluminum  or  brass  rings  to  optimize  tag

attachment duration relative to tag battery life.

•  Development  of  the  capability  of  retaining  a  biopsy
(skin) sample during tagging, for genetic sample col-
lection  for  sex  determination,  population  structure
studies, and epigenetic assessments of age and health.

Acknowledgements
Jay Sweeney and Rae Stone enabled critical initial support from Dolphin
Quest. Gretchen Lovewell, Misty Niemeyer, and William McLellan collected
and supplied dolphin cadaver dorsal fins from stranded, deceased dolphins.
Michael Scott, Brian Balmer, Teri Rowles, Lori Schwacke, Cynthia Smith, and
Andrew Westgate contributed to the project. We thank the Mote Marine
Laboratory Marine Operations staff for field support. White shark tagging
was funded by the Atlantic White Sharks Conservancy and conducted off the
F/V Aleutian Dream with the assistance of John King. Brian Hanson, Megan
Winton, and spotter pilot Wayne Davis. Whale shark tagging was conducted
off the F/V Endurance and made possible by Eric Savetsky and Dr. Tom Burns,
DVM. We thank Krystan Wilkinson for tracking map preparation.

Moore et al. Animal Biotelemetry  (2024) 12:6

Page 15 of 16

Author contributions
MJM coordinated the tool development process, assisted with field testing,
and drafted the manuscript. TML led the design, engineering and itera-
tive development of the hardware and software. RSW conceived of the
tool, secured initial funding, recruited the team, and led the field testing.
JK oversaw the engineering project and provided critical input as to how
to evolve and enhance the system. AAB and JBA operated the tag tool and
worked with the Mote Marine Laboratory staff to enable the dolphin field
tests. RWB enabled and supported the field tests in Hawaiʻi. CDB conceived
of and undertook the whale shark tagging. GBS conceived of and undertook
the white shark tagging. SRT supported the planning for both shark tagging
projects. All authors read and approved the final manuscript.

Funding
Funding for initial TADpole development and testing was provided to WHOI
by Dolphin Quest, Inc. Support for refinements and further testing was pro-
vided by Dolphin Biology Research Institute, Mote Scientific Foundation and
the NOAA RESTORE Program via WHOI CINAR NA19OAR4320074. Fieldwork
in Hawaiʻi was supported by a grant from the Tides Foundation to Cascadia
Research Collective. White shark tagging was supported by the Atlantic
White Shark Conservancy and the Massachusetts Division of Marine Fisheries.
Whale shark tagging was supported by internal funding at WHOI. Support for
preparation of the manuscript was provided by the Independent Research &
Development Program at WHOI and the NOAA RESTORE program.

Availability of data and materials
The design, operating protocol, components specifications are available in the
Woods Hole Open Access Server repository https:// hdl. handle. net/ 1912/ 67505
and TADpole Arduino code for the microcontroller is available at https://
github. com/ WHOItp/ TADpo le. git.

Declarations

Ethics approval and consent to participate
Dolphin field tests in Florida were conducted under National Marine Fisheries
Service Scientific Research Permits No. 15543, 20455, and 26622, and under
annually renewed IACUC approvals from Mote Marine Laboratory, issued to
Wells. Field tests in Hawaiʻi were conducted under National Marine Fisheries
Service Scientific Research Permit No. 20605, issued to Baird, and under IACUC
approval from Cascadia Research Collective. Sharks were tagged under IACUC
approval from the Woods Hole Oceanographic Institution.

Consent for publication
Not applicable.

Competing interests
None.

Author details
1 Department of Biology Woods Hole Oceanographic Institution, Woods Hole,
MA 02543, USA. 2 Department of Applied Ocean Physics and Ocean Engineer-
ing, Woods Hole Oceanographic Institution, Woods Hole, MA, USA. 3 Sarasota
Dolphin Research Program, Brookfield Zoo Chicago, c/o Mote Marine Labora-
tory, Sarasota, FL, USA. 4 Cascadia Research Collective, Olympia, WA, USA. 5 Mas-
sachusetts Division of Marine Fisheries, New Bedford, MA, USA.

Received: 18 February 2024   Accepted: 2 April 2024
Published: 15 April 2024

References

 1. Andrews RD, Baird RW, Calambokidis J, Goertz CE, Gulland F, Heide-

Jorgensen M-P, Hooker SK, Johnson M, Mate B, Mitani Y. Best practice
guidelines for cetacean tagging. J Cetacean Res Manag. 2019;20:27–66.
https:// doi. org/ 10. 47536/ jcrm. v20i1. 237.

 2. Renshaw S, Hammerschlag N, Gallagher AJ, Lubitz N, Sims DW. Global
tracking of shark movements, behaviour and ecology: a review of the

 3.

 4.

 5.

renaissance years of satellite tagging studies, 2010–2020. J Exp Mar Biol
Ecol. 2023;560:151841. https:// doi. org/ 10. 1016/j. jembe. 2022. 151841.
Johnson M, Tyack P. A digital acoustic recording tag for measuring
the response of wild marine mammals to sound. IEEE J Ocean Eng.
2003;28:3–12.
Shaff JF, Baird RW. Diel and lunar variation in diving behavior of rough-
toothed dolphins (Steno bredanensis) off Kauaʻi Hawaiʻi. Mar Mamm Sci.
2021;37:1261–76. https:// doi. org/ 10. 1111/ mms. 12811.
Schorr GS, Falcone EA, Moretti DJ, Andrews RD. First long-term behavioral
records from Cuvier’s beaked whales (Ziphius cavirostris) reveal record-
breaking dives. PLoS ONE. 2014;9: e92633. https:// doi. org/ 10. 1371/ journ
al. pone. 00926 33.

 6. Baird RW, Hanson MB, Schorr GS, Webster DL, McSweeney DJ, Gorgone

AM, Mahaffy SD, Holzer DM, Oleson EM, Andrews RD. Range and primary
habitats of Hawaiian insular false killer whales: informing determination
of critical habitat. Endanger Spec Res. 2012;18:47–61. https:// doi. org/ 10.
3354/ esr00 435.

 7. Moore MJ, Zerbini AN. Dolphin blubber/axial muscle shear: implications
for rigid trans-dermal intra-muscular tracking tag trauma in whales. J Exp
Biol. 2017;220:3717–23. https:// doi. org/ 10. 1242/ jeb. 165282.

 8. Norman SA, Flynn KR, Zerbini AN, Gulland F, Moore MJ, Raverty S, Rotstein
DS, Mate BR, Hayslip C, Gendron D. Assessment of wound healing of
tagged gray (Eschrichtius robustus) and blue (Balaenoptera musculus)
whales in the eastern North Pacific using long-term series of photo-
graphs. Mar Mamm Sci. 2018;34:27–53. https:// doi. org/ 10. 1111/ mms.
 12443.

 9. Gendron D, Martinez Serrano I, de Ugalde la Cruz A, Calambokidis J, Mate
B. Long-term individual sighting history database: an effective tool to
monitor satellite tag effects on cetaceans. Endang Spec Res. 2015;26:235–
41. https:// doi. org/ 10. 3354/ esr00 644.

10. Balmer BC, Wells RS, Schwacke LH, Rowles TK, Hunter C, Zolman ES,

Townsend FI, Danielson B, Westgate AJ, McLellan WA. Evaluation of a
single-pin, satellite-linked transmitter deployed on bottlenose dolphins
(Tursiops truncatus) along the coast of Georgia, USA. Aquat Mamm.
2011;37:187–92.

 11. Wells RS, Fougeres EM, Cooper AG, Stevens RO, Brodsky M, Lingenfelser R,

Dold C, Douglas DC. Movements and dive patterns of short-finned pilot
whales (Globicephala macrorhynchus) released from a mass stranding in
the Florida Keys. Aquat Mamm. 2013;39:61–72. https:// doi. org/ 10. 1578/
AM. 39.1. 2013. 61.

 12. Balmer BC, Schwacke LH, Wells RS. Linking dive behavior to satellite-

linked tag condition for a bottlenose dolphin (Tursiops truncatus) along
Florida’s Northern Gulf of Mexico Coast. Aquat Mamm. 2010. https:// doi.
org/ 10. 1578/ AM. 36.1. 2010.1.

 13. Balmer BC, Wells RS, Howle LE, Barleycorn AA, McLellan WA, Ann Pabst D,
Rowles TK, Schwacke LH, Townsend FI, Westgate AJ. Advances in ceta-
cean telemetry: a review of single-pin transmitter attachment techniques
on small cetaceans and development of a new satellite-linked transmitter
design. Mar Mamm Sci. 2014;30:656–73. https:// doi. org/ 10. 1111/ mms.
 12072.

 14. Deming AC, Wingers NL, Moore DP, Rotstein D, Wells RS, Ewing R, Hodan-

bosi MR, Carmichael RH. Health impacts and recovery from prolonged
freshwater exposure in a common bottlenose dolphin (Tursiops trunca-
tus). Front Vet Sci. 2020;7:235. https:// doi. org/ 10. 3389/ fvets. 2020. 00235.

 15. Dunn C, Claridge D, Herzing D, Volker C, Melillo-Sweeting K, Wells RS,

Turner T, O’Sullivan K. Satellite-linked telemetry study of a rehabilitated
and released Atlantic spotted dolphin in the Bahamas provides insights
into broader ranging patterns and conservation needs. Aquat Mamm.
2020;46:633–9. https:// doi. org/ 10. 1578/ AM. 46.6. 2020. 633.

 16. Moore RBT, Douglas DC, Nollens HH, Croft L, Wells RS. Post-release

monitoring of a stranded and rehabilitated short-finned pilot whale (Glo-
bicephala macrorhynchus) reveals current-assisted travel. Aquat Mamm.
2020;46:200–14. https:// doi. org/ 10. 1578/ AM. 46.2. 2020. 200.

 17. Wells RS: Evaluation of tag attachments on small cetaceans. Final Report

to the Office of Naval Research for Award Number: N000141210391. 5 pp.
2013

 18. Wells RS, Fauquier DA, Gulland FMD, Townsend FI, DiGiovanni RA. Evaluat-
ing postintervention survival of free-ranging odontocete cetaceans. Mar
Mamm Sci. 2013;29:E463–83. https:// doi. org/ 10. 1111/ mms. 12007.
 19. Wells RS, Schwacke LH, Rowles TK, Balmer BC, Zolman E, Speakman T,

Townsend FI, Tumlin MC, Barleycorn A, Wilkinson KA. Ranging patterns

 Moore et al. Animal Biotelemetry  (2024) 12:6

Page 16 of 16

of common bottlenose dolphins Tursiops truncatus in Barataria Bay,
Louisiana, following the Deepwater Horizon oil spill. Endanger Spec Res.
2017;33:159–80. https:// doi. org/ 10. 3354/ esr00 732.

 20. Pulis E, Wells RS, Schorr GS, Douglas DC, Samuelson MM, Solangi M.

Movements and dive patterns of pygmy killer whales (Feresa attenuata)
released in the Gulf of Mexico following rehabilitation. Aquat Mamm.
2018;44:555–67. https:// doi. org/ 10. 1578/ AM. 44.5. 2018. 555.

 21. Wells RS, Cremer MJ, Berninsone LG, Albareda D, Wilkinson KA, Stamper
MA, Paitach RL, Bordino P. Tagging, ranging patterns, and behavior of
franciscana dolphins (Pontoporia blainvillei) off Argentina and Brazil: con-
siderations for conservation. Mar Mamm Sci. 2022;38:571–605. https://
doi. org/ 10. 1111/ mms. 12879.

 22. Nasby-Lucas N, Domeier ML. Impact of satellite linked radio transmit-
ting (SLRT) tags on the dorsal fin of subadult and adult white sharks
(Carcharodon carcharias). Bull Mar Sci. 2020;96:23–30. https:// doi. org/ 10.
5343/ bms. 2019. 0019.

 23. Skomal G. Evaluating the physiological and physical consequences of

capture on post-release survivorship in large pelagic fishes. Fish Manage
Ecol. 2007;14:81–9. https:// doi. org/ 10. 1111/j. 1365- 2400. 2007. 00528.x.
 24.  Jewell OJ, Wcisel MA, Gennari E, Towner AV, Bester MN, Johnson RL, Singh

S. Effects of smart position only (SPOT) tag deployment on white sharks
Carcharodon carcharias in South Africa. PLoS ONE. 2011;6: e27242. https://
doi. org/ 10. 1371/ journ al. pone. 00272 42.

 25. Chin A, Mourier J, Rummer JL. Blacktip reef sharks (Carcharhinus melano-

pterus) show high capacity for wound healing and recovery following
injury. Conserv Physiol. 2015;3:cov062. https:// doi. org/ 10. 1093/ conph ys/
cov062.

 26. TADpole—CAD drawings of a device to tag dolphins, parts list, and

operating instructions. https:// doi. org/ 10. 26025/ 1912/ 67505 [https:// hdl.
handle. net/ 1912/ 67505]. Accesed 9 Apr 2024.

 27. TADpole—Arduino code for TADpole. [https:// github. com/ WHOItp/

TADpo le. git]. Accesed 9 Apr 2024.

 28. Ploner M, Gross J, Timmermann L, Schnitzler A. Pain processing is faster

than tactile processing in the human brain. J Neurosci. 2006;26:10879–82.
https:// doi. org/ 10. 1523/ JNEUR OSCI. 2386- 06. 2006.

 29. Caldwell DJ, Cronin JA, Wu J, Weaver KE, Ko AL, Rao RPN, Ojemann JG.
Direct stimulation of somatosensory cortex results in slower reaction
times compared to peripheral touch in humans. Sci Rep. 2019;9:3292.
https:// doi. org/ 10. 1038/ s41598- 019- 38619-2.

 30. Lele P, Sinclair D, Weddell G. The reaction time to touch. J physiol.
1954;123:187. https:// doi. org/ 10. 1113/ jphys iol. 1954. sp005 042.

 31. Woodworth RS, Barber B, Schlosberg H. Experimental psychology. Oxford:

Oxford and IBH Publishing; 1954.

 32. Palmer E, Weddell G. The relationship between structure, innervation and

function of the skin of the bottle nose dolphin (Tursiops truncatus). Proc
Zool Soc Lond. 1964;143:553-568 557. https:// doi. org/ 10. 1111/. 1469-
7998. 1964. tb038 81.x.

 33. Eldridge S, Mortazavi F, Rosene D. The hydrodynamic sensory system

in the skin of cetaceans. FASEB J. 2020;34:1–1. https:// doi. org/ 10. 1096/
fasebj. 2020. 34. s1. 00356.

Publisher’s Note
Springer Nature remains neutral with regard to jurisdictional claims in pub-
lished maps and institutional affiliations.
