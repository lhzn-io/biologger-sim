Hindawi Publishing Corporation
EURASIP Journal on Advances in Signal Processing
Volume 2010, Article ID 732586, 6 pages
doi:10.1155/2010/732586

Research Article
A New Method to Calibrate Attachment Angles of Data Loggers in
Swimming Sharks

Shizuka Kawatsu,1 Katsufumi Sato,2 Yuuki Watanabe,3 Susumu Hyodo,1 Jason P. Breves,4
Bradley K. Fox,4 E. Gordon Grau,4 and Nobuyuki Miyazaki1

1 Ocean Research Institute, The University of Tokyo, 1-15-1 Minamidai, Nakano, Tokyo 164-0014, Japan
2 International Coastal Research Center, Ocean Research Institute, The University of Tokyo, 2-106-1 Akahama,
Otsuchi, Iwate 028-1102, Japan
3 National Institute of Polar Research, 10-3 Midorimachi, Tachikawa, Tokyo 190-8518, Japan
4 Hawaii Institute of Marine Biology, University of Hawaii, Kaneohe, HI 96744, USA

Correspondence should be addressed to Shizuka Kawatsu, <kawatsusame@ori.u-tokyo.ac.jp>

Received 2 May 2009; Accepted 7 August 2009

Academic Editor: Jo˜ao Manuel R. S. Tavares

Copyright © 2010 Shizuka Kawatsu et al. This is an open access article distributed under the Creative Commons Attribution
License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly
cited.

Recently, animal-borne accelerometers have been used to record the pitch angle of aquatic animals during swimming. When
evaluating pitch angle, it is necessary to consider a discrepancy between the angle of an accelerometer and the long axis of an
animal. In this study, we attached accelerometers to 17 free-ranging scalloped hammerhead shark (Sphyrna lewini) pups from
Kaneohe Bay, Hawaii. Although there are methods to calibrate attachment angles of accelerometers, we conﬁrmed that previous
methods were not applicable for hammerhead pups. According to raw data, some sharks ascended with a negative angle, which
diﬀers from tank observations of captive sharks. In turn, we developed a new method to account for this discrepancy in swimming
sharks by estimating the attachment angle from the relationship between vertical speed (m/s) and pitch angle obtained by each
accelerometer. The new method can be utilized for ﬁeld observation of a wide range of species.

1. Introduction

An accurate determination of pitch angle is critical to
gain detailed information about the diving and foraging
strategies of aquatic animals. For example, air-breathing
aquatic animals that forage underwater control pitch angle
and allocate their submerged time. In African penguins,
steeper ascent angles presumably occur when they have
depleted their oxygen stores and must return to the surface
more quickly to breathe [1]. In macaroni penguins, pitch
angle is signiﬁcantly correlated with time spent at the
bottom-phase of the dive [2]. A steep pitch angle during
ascent indicates that they encountered a prey patch and a
shallow pitch angle contributes to movement into a more
proﬁtable area in the following dive, due to increasing the
horizontal distance [2]. While in ﬁsh, Nakaya [3] said that
scalloped hammerhead sharks (Sphyrna lewini) have great
maneuverability due to a movable large plate on head. Based

on the observation of swimming behavior, it is apparent that
sharks make a sharp dorsal turn at the bottom, consume food
items, and swim away along the bottom [3]. In this sequence,
pitch angle is an important indicator of a feeding event.

Recent advances in the development of animal-borne
accelerometers (data loggers) make it possible for researchers
to monitor pitch angle of aquatic animals in situ by attaching
an acceleration sensor (accelerometer) along the longitudinal
axis of the body. When a data logger is positioned exactly
parallel to the longitudinal axis of an animal, the calculated
angle of the data logger is the same as the pitch angle of
the animal. Nonetheless, it is impossible to align the logger
exactly parallel to the longitudinal axis of an animal in
ﬁeld studies. A few methods have been previously described
to account for the discrepancy between the pitch angle of
data loggers and the longitudinal axis in ﬁeld studies. In
one instance, Watanuki et al. [4] designated the attachment
angle to the lower back of seabirds as 0◦ when they were

2

EURASIP Journal on Advances in Signal Processing

at the water surface, a time in which they were essentially
horizontal before release. This methodology is well suited
for birds that can be maintained in a horizontal position at
the water surface. However, for animals that have a ﬂexible
body, it is diﬃcult to keep them positioned horizontally for
an extended period of time. In addition, this methodology
cannot be applied for obligate swimming ﬁsh because of fatal
risk for lack of adequate gill ventilation. Another approach
to account for the discrepancy between the pitch angle of
data loggers and the longitudinal axis was reported by Sato
et al. [5] in Weddell seal. In this study, the attachment
angle was calculated by using the data logger along with the
speed sensor. Sato et al. [5] used the data logger (UWE1000-
PD2GT: 22 mm diameter, 124 mm length; 80 g in air; Little
Leonardo Co., Tokyo, Japan) which contains a propeller and
reported that the attachment angle for a speciﬁc dive of
Weddell seal could be determined using equations including
the number of propeller rotations, surging acceleration
(m/s2), the acceleration of gravity (9.8 m/s2), and body angle
(degrees). This methodology can only be applied for large
animals due to the relatively large size of data loggers that
have a propeller. Furthermore, this method is only applicable
for diving animals that must come to the surface to breathe.
Lastly, in a third study, the attachment angle in ﬂatﬁsh was
assigned as 0◦ when they lay on the substrate as reported by
Kawabe et al. [6]. This method is only applicable for benthic
animals that remain on the bottom. There are currently no
reported methods to apply for continuous swimming ﬁsh.

The previously described methods are speciﬁc for partic-
ular species and we therefore anticipated that they might not
be suitable for use in hammerhead sharks. Scalloped ham-
merhead shark pups have ﬂexible bodies and are obligatory
swimmers [7]. In addition, their small body size allows only
for use of the smallest logger available for ﬁeld studies that
can only record depth, temperature and 2-axes accelerations,
but not speed. In this study, we attached data loggers to
17 free-ranging pups with the objective to establish a new
method for calibrating the attachment angle of loggers in
free-ranging sharks.

2. Materials and Methods

2.1. Field Work. Our ﬁeld studies occurred in Kaneohe Bay,
Hawaii (21.26◦N, 157.47◦W) in August and October, 2007,
and July/August, 2008. Kaneohe Bay is a nursery ground for
the scalloped hammerhead shark (Sphyrna lewini) during
summer months in which pups spend most of their time near
the bottom [8]. In this study, juvenile scalloped hammerhead
sharks were collected using hand lines with baited hooks.
Upon capture, sharks were immediately transferred to the
Hawaii Institute of Marine Biology, University of Hawaii,
and placed in 3 m diameter tanks with ﬂow-through seawater
for 2–3 days. Sharks were fed squid twice a day and usually
resumed feeding within 24 hours of capture. Release of the
sharks into the ﬁeld with data loggers did not occur until
they resumed feeding in captivity for at least 48 hours. At
this time, both total length (TL) and body mass (BM) were
measured. For some sharks, BM was estimated from the

relationship (R2 = 0.45) between TL and BM of 20 pups
from a previous experiment. Prior to release, a data logger
was attached immediately anterior to the ﬁrst dorsal ﬁn using
a plastic cable connected to a time-scheduled release system
[9]. This cable ran through the soft plastic netting (3 cm ×
5 cm) attached to the shark with dissolvable suture (Matsuda
Medical Kogyo Co., Tokyo, Japan). Techniques used to attach
the data loggers were done within a jet of seawater and
designed to minimize stress. The time required to attach the
data loggers was less than 5 minutes per individual and we let
sharks respire forcibly along the way. After which time sharks
were immediately released in the bay. All animal experiments
were conducted according to the Guideline for Care and
Use of Animals approved by the committees of University of
Tokyo and University of Hawaii.

2.2. Data Recovery. An automatic time-scheduled release
system that allows for loggers to be located and retrieved
using VHF radio signals was used because the recapture of
instrumented pups in Kaneohe Bay is not possible. The data
loggers were attached to a ﬂoat of copolymer foam (Nichiyu
Giken Kogyo Co., Saitama, Japan), in the top of which a
VHF radio transmitter with a 45 cm semirigid wire antenna
(Advanced Telemetry Systems Inc., Isanti, MN, USA) was
embedded. A plastic cable connected to a time-scheduled
release mechanism (Little Leonardo Co.) bound the tag to the
plastic netting which was attached to the pups. Tag retrieval
followed the method reported in Baikal seals [10]. Devices
were attached to 17 pups in total, of which we successfully
retrieved 16 loggers. Of the 16 loggers, one data logger was
released from a pup after 6 hours, 7 were released after 24
hours, 7 were released after 48 hours, and one was released
after 72 hours.

2.3. Instruments. Acceleration data loggers (M190L-D2GT;
Little Leonardo Co., Tokyo, Japan) were used to examine
swimming behavior of pups. Each logger was 15 mm in
diameter, 53 mm in length, had a mass of 18 g and recorded
depth (1 Hz), 2-axes accelerations (for detecting caudal ﬁn
movement and pitch, 32 Hz for eight individuals and 16 Hz
for eight individuals), and temperature (1 Hz). The total
weight of the instruments deployed on pups,
including
devices for data recovery (such as ﬂoat and VHF transmit-
ter), was 50 g with a slight positive buoyancy in seawater.
The measuring range for acceleration along two axes was
±29.4 m/s2. Values recorded by the accelerometers were
converted into acceleration (m/s2) with linear regression
equations. To obtain the calibration equations, relative values
recorded by each logger at 90◦and −90◦ from the horizontal
level were regressed against the corresponding acceleration
(9.8 m/s2 and −9.8 m/s2, resp.).

2.4. Data Analysis. Two of the sixteen retrieved data loggers
were not included in our analyses due to incomplete data
records. Loggers were positioned so as to detect longitu-
dinal (surging) and lateral (swaying) accelerations. Loggers
attached on the animals measured both dynamic acceleration
(such as tail beating activities) and static acceleration (such

EURASIP Journal on Advances in Signal Processing

3

Data logger

+θ

−θ

γ > 0◦

γ < 0◦

0◦

γ

α

θ

+

θ
−

Data logger
Y +

g

γ

γ

g

Data logger

Y −

γ

α

Ascent [θ > 0◦, Y > 0 (ms)−2, γ > 0◦, α < 0◦]

Descent [θ < 0◦, Y < 0 (ms)−2, γ < 0◦, α < 0◦]

Figure 1: Attachment of a data-logger to the dorsal side of a hammerhead shark. Diagram shows the direction of surging acceleration Y ,
recorded by a D2GT logger placed on a shark, and gravity g (= 9.8 ms−2), angle of surge axis of the logger to horizon (γ), that of longitudinal
axis to horizon (θ) deﬁned as pitch angle (negative as the shark descends), and logger attachment angle (α).

as gravity). The acceleration sensor along the longitudinal
body axis can measure acceleration in response to changes
in the movements of animals such as stroking and change
in pitch angle. High-frequency ﬂuctuations in the surging
acceleration records are believed to be caused by caudal ﬁn
movements. When the animal is still or moving at a constant
speed, the gravity vector will change in response to pitch
angle. Together, low-frequency ﬂuctuations in the acceler-
ation along the longitudinal axis (surging acceleration) are
used to calculate the pitch angle [5, 11].

To remove the high-frequency component of acceleration
caused by the tail beating, we extracted the low-frequency
signals on surging accelerations of sharks with a ﬁlter in
the IGOR Pro software (Wave Metrics Inc., USA; see also
[5, 11]). Then, the low-frequency component of longitudinal
acceleration (Y ) was converted to angle of the data-logger
relative to the horizon (γ ranging from −90◦ to 90◦) as
follows:

γ = a sin

(cid:2)

(cid:3)
.

Y
9.8

(1)

Following Sato et al. [5], the body angle of pups against

the water surface (θ, Figure 1) can be expressed by

θ = γ − α,

(2)

where γ is the angle of surge axis of the logger to horizon
(degrees), and α is the attachment angle of the logger
against the longitudinal axis (degrees). θ and γ while pups
were descending (the data logger was tilting in a clockwise
direction) were regarded as negative, and when ascending
(the data logger was tilting in a counterclockwise direction),
θ and γ were regarded as positive.

At ﬁrst, we estimated an attachment angle (α1) using a
previously reported method [4]. We corrected the values of
body angle recorded in a holding tank horizontally for 10–
20 seconds to 0◦. We held a pup for 10–20 seconds with its

)

m

(
h
t
p
e
D

0
0.5
1
1.5

23 : 08
2007/10/24

23 : 09

23 : 10

23 : 11

23 : 12

Time on 24 October 2007

(a)

)

m

(
h
t
p
e
D

−0.5
0.5
1.5
2.5

20
0
−20
−40

e
l
g
n
a
h
c
t
i
P

)
g
e
d
(

20
0
−20
−40

e
l
g
n
a
h
c
t
i
P

)
g
e
d
(

23 : 09 : 50
2007/10/24

23 : 09 : 55 23 : 10 : 00 23 : 10 : 05

Time on 24 October 2007

(b)

Figure 2: (a) An example of swimming depth (blue line) adjusted
pitch angle by new method (green line) and by previous method
(red line) of an individual pup (HI0703). (b) Enlarged part of
Figure 2 shows that the adjusted pitch angle (green line) changed
from a negative to positive value at the moment of ascent.

body level to the water surface and recorded the time. We
assumed the pitch angle during previous recording periods
to be ﬂat (0◦). Then, we subtracted the recorded angle during
previous periods from each individual’s pitch angle data over
the period of logger deployment. Next, we obtained another
attachment angle (α2) using a new method that estimated
the attachment angle from the relationship between vertical

4

EURASIP Journal on Advances in Signal Processing

Table 1: Morphological information and attachment angles of loggers derived from a previous method (α1) and that following adjustment
by a new method (α2) for each shark.

Shark ID Sex
HI0702
F
M
HI0703
F
HI0704
HI0705
F
M
HI0706
F
HI0707
M
HI0709
F
HI0801
HI0802
F
—
HI0803
—
HI0804
—
HI0805
M
HI0807
F
HI0808
∗Data length (h) is not necessarily consistent with total recorded hours.

Total length (cm)
54.5
58
54
56
55
56
54
54
54
58
58
57
54
57

Body mass (g)
727
870
935
760
750
780
745
575
575
717
717
681
575
681

α1 (degrees)
−19.6
−12.5
−2.2
−18.0
−13.3
−12.0
−6.9
−31.2
−19.3
−23.1
−24.9
−26.1
−15.8
−21.7

α2 (degrees)
−43.6
−24.3
−20.5
−36.4
−25.3
−23.9
−19.9
−31.9
−22.7
−40.1
−44.1
−55.2
−40.4
−17.3

Correlation coeﬃcient
−0.72
−0.88
−0.71
−0.79
−0.57
−0.77
−0.56
−0.78
−0.83
−0.72
−0.74
−0.60
−0.72
−0.71

Data length (h)∗
6
24
48
48
28
24
20
2
2
19
24
17
17
44

60

40

20

0

−20

−40

−60

−80

n
o
i
t
c
e
r
r
o
c

e
r
o
f
e
b
e
l
g
n
a
h
c
t
i
P

)
g
e
d
(

To conﬁrm the utility of this new method, we observed
instrumented banded dogﬁsh (Triakis scyllium) in an exper-
imental tank using a video camera. We attached a data
logger (UWE190PD2GT: 22 mm diameter, 124 mm length;
80 g in air; Little Leonardo Co., Tokyo, Japan) using the
same method as used for hammerhead pups. After the
experiment, we compared the adjusted angle calculated from
our new method with the adjusted angle obtained from video
observations.

−0.8 −0.6 −0.4 −0.2

0

0.2

0.4

Vertical speed (m/s)

3. Results

Figure 3: Example of the relationship between raw pitch angle (γ)
and vertical speed from an individual pup (HI0702). A negative
vertical speed indicates ascent and a positive value indicates descent.

speed (m/s) and body angle. We compared raw pitch angle
(γ) with vertical speed per second to ﬁnd a linear regression
from each pup. There are indications that negatively buoyant
ﬁshes, such as sharks and sturgeon, may assume a positive
pitch tilt during steady horizontal swimming as a behavioral
mechanism to increase the total body area generating lift
[12, 13]. Nonetheless, it can be assumed that the body axis
of an animal is parallel to the direction of movement when
the animal swims at a constant speed. With this assumption,
we expected a descending pup to have a negative pitch angle
while the pitch angle of an ascending pup would be positive.
If a pup swims horizontally, the instantaneous pitch angle
would be zero. When we analyzed the relationships between
raw pitch angle and vertical speed per second, we found a
linear regression from each pup. This regression line should
pass through the origin coordinate if the logger angle is
parallel to the longitudinal axis of the body. We considered
the intercept of the regression line to be the attachment angle
(α2 degrees).

As expected, we could not use previously reported methods
to adjust pitch angle. Thus, we needed to develop a new
method to calculate the attachment angle for hammerhead
pups. A modulation of the pitch angle of a swimming shark
is expected to correspond to ﬂuctuations in the vertical
speed rate (depth changes per second). The depth parameter
therefore has the potential to provide information for the
correction of pitch angle.

The ﬁrst method reported by Watanuki et al. [4] provided
us an estimated attachment angle (α1) from 16 pups that
varied between −40.9◦ and −2.2◦ (Table 1). When we applied
this attachment angle to each pup, some individuals showed
a negative angle when they ascended (Figure 2, red line). All
the scatter plots made from the pitch angle before adjustment
and the vertical speed provided a linear regression. A
regression line was produced for each pup (Figure 3) with
correlation coeﬃcient (absolute value) higher than 0.56
(Table 1). The intercept of the regression line (adjustment
angle α2) varied from −55.2◦ to −17.3◦ (Table 1). α1 and
α2 were regarded as negative when the data logger was tilting
in a clockwise direction and positive when the data logger
was tilting in a counterclockwise direction. As a result, all the
data loggers attached to pups showed negative attachment
angles.

EURASIP Journal on Advances in Signal Processing

5

the animal does not need to be ﬁxed ﬂat, but it cannot be
applied to smaller animals such as hammerhead shark pups,
because a data logger including a speed sensor is too large
and would likely impact behavior.

In conclusion, we developed a new method of analysis
that enabled us to correct the pitch angle of hammerhead
sharks equipped with a small accelerometer. For ﬁsh that
display changes in pitch angle when making movements
up and down in the water column, this new method to
correct pitch angle in juvenile sharks can be applied for the
acquisition of information in a wider range of species.

Acknowledgments

The authors would like to thank the following people for
their cooperation: Dr. Darren T. Lerner, Dr. Nicholas M.
Whitney, and Dr. Tetsuya Hirano, University of Hawaii,
Yoko Yamaguchi, Shin Takaki, and Souichirou Takabe, ORI
for their assistance with the ﬁeldwork, and Sho Tanaka,
Fumitaka Noguchi, and Genjiro Nishi, Tokai University, for
their assistance of aquarium investigations. This study was
supported by the Sasakawa Scientiﬁc Research Grant from
The Japan Science Society to S. K., the Pauley Foundation
Summer Program 2008 at Hawaii Institute of Marine Biology
to E. G. G., Japan-USA Research Cooperative Program from
the Japan Society for the Promotion of Science to S. H., Grant
in Aid from JSPS (19255001) to K. S., and program “Bio-
Logging Science of the University of Tokyo (UTBLS)” led by
N. M.

References

[1] R. P. Wilson and M.-P. Wilson, “The foraging behaviour of
the African penguin Spheniscus demersus,” in The Penguins:
Ecology and Management, pp. 244–265, Surrey Beatty and
Sons, Sidney, Australia, 1995.

[2] K. Sato, J.-B. Charrassin, C.-A. Bost, and Y. Naito, “Why do
macaroni penguins choose shallow body angles that result in
longer descent and ascent durations?” Journal of Experimental
Biology, vol. 207, no. 23, pp. 4057–4065, 2004.

[3] K. Nakaya, “Hydrodynamic function of the head in the
hammerhead sharks (Elasmobranchii: Sphyrnidae),” Copeia,
pp. 330–336, 1995.

[4] Y. Watanuki, Y. Niizuma, G. W. Gabrielsen, K. Sato, and
Y. Naito, “Stroke and glide of wing-propelled divers: deep
diving seabirds adjust surge frequency to buoyancy change
with depth,” Proceedings of the Royal Society B, vol. 270, no.
1514, pp. 483–488, 2003.

[5] K. Sato, Y. Mitani, M. F. Cameron, D. B. Siniﬀ, and Y.
Naito, “Factors aﬀecting stroking patterns and body angle
in diving Weddell seals under natural conditions,” Journal of
Experimental Biology, vol. 206, no. 9, pp. 1461–1470, 2003.
[6] R. Kawabe, Y. Naito, K. Sato, K. Miyashita, and N. Yamashita,
“Direct measurement of the swimming speed, tailbeat, and
body angle of Japanese ﬂounder (Paralichthys olivaceus),” ICES
Journal of Marine Science, vol. 61, no. 7, pp. 1080–1087, 2004.
[7] C. G. Lowe, “Kinematics and critical swimming speed of juve-
nile scalloped hammerhead sharks,” Journal of Experimental
Biology, vol. 199, no. 12, pp. 2605–2610, 1996.

Figure 4: An attachment angle of the data logger on the banded
dogﬁsh was 14◦ from visual analysis and 13.7◦ from the regression
line method.

The attachment angles obtained from our new method
diﬀered from values obtained from the ﬁrst method
(Table 1). For example, an attachment angle of one individ-
ual (HI0702) from the ﬁrst method was −19.6◦ while the
new method yielded an angle of −43.6◦. Both corrected pitch
angles using the above values are indicated in Figure 2. The
corrected pitch angle using the new methodology showed
that the diving proﬁle became negative during descent and
positive during ascent (Figure 2(b)). Even considering the
pitch tilt previously cited [12, 13], a negative pitch angle
during ascent does not correctly represent the pitch angle of
a pup. We concluded that the new methodology corresponds
well with the diving proﬁle. In banded dogﬁsh held in an
aquarium, the adjustment angle from the regression line
method was 13.7◦, while the observed tilt angle of the
data logger was 14◦ when analyzed from video observations
(Figure 4).

4. Discussion

The new regression line method we report has three
advantages over previously described methods. First, the
new method provides more accurate information about the
correction angle since the corrected pitch angle using the
new methodology corresponds well with the diving proﬁle.
It is diﬃcult to ﬁx sharks on their ﬂat pitch angle because
their bodies are ﬂexible and a seemingly ﬂat angle out of
water is not necessarily the same as the rigid ﬂat angle.
Indeed, banded dogﬁsh orient their heads slightly upward
when resting at the bottom of an aquarium when compared
with when they are held out of water. Second, the new
method is considerably less invasive than the method that
requires holding sharks level at the water surface. Our new
method accounts for the fact that hammerhead shark pups
are obligate swimmers that can only respire while swimming
[7]. Third, it is possible to adjust the pitch angle without
speed data. Sato et al. [5] developed another adjustment
technique for a logger that contained a propeller so as to
record speed in addition to depth, 2-axes accelerations, and
temperature in the data logger we used. With this technique,

6

EURASIP Journal on Advances in Signal Processing

[8] K. N. Holland, B. M. Wetherbee, J. D. Peterson, and C. G.
Lowe, “Movements and distribution of hammerhead shark
pups on their natal grounds,” Copeia, pp. 495–502, 1993.
[9] Y. Watanabe, E. A. Baranov, K. Sato, Y. Naito, and N. Miyazaki,
“Foraging tactics of Baikal seals diﬀer between day and night,”
Marine Ecology Progress Series, vol. 279, pp. 283–289, 2004.
[10] Y. Watanabe, E. A. Baranov, K. Sato, Y. Naito, and N. Miyazaki,
“Body density aﬀects stroke patterns in Baikal seals,” Journal of
Experimental Biology, vol. 209, no. 17, pp. 3269–3280, 2006.

[11] H. Tanaka, Y. Takagi, and Y. Naito, “Swimming speeds and
buoyancy compensation of migrating adult chum salmon
Oncorhynchus keta revealed by speed/depth/acceleration data
logger,” Journal of Experimental Biology, vol. 204, no. 22, pp.
3895–3904, 2001.

[12] P. He and C. S. Wardle, “Tilting behavior of the Atlantic mack-
erel, Scomber scombrus, at low swimming speeds,” Journal of
Fish Biology, vol. 29, pp. 223–232, 1986.

[13] C. D. Wilga and G. V. Lauder, “Functional morphology of
the pectoral ﬁns in bamboo sharks, Chiloscyllium plagiosum:
benthic vs. pelagic station-holding,” Journal of Morphology,
vol. 249, no. 3, pp. 195–209, 2001.
