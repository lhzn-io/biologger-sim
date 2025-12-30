Received: 19 July 2017

Accepted: 9 May 2018

DOI: 10.1111/jfb.13652

R E G U L A R P A P E R

FISH

Estimating fish swimming metrics and metabolic rates with
accelerometers: the influence of sampling frequency

Jacob W. Brownscombe1

| Robert J. Lennox1

| Andy J. Danylchuk2 | Steven J. Cooke1

1Fish Ecology and Conservation Physiology
Laboratory, Ottawa-Carleton Institute for
Biology, Carleton University, Ottawa, Canada

2Department of Environmental Conservation,
University of Massachusetts Amherst,
Amherst, Massachusetts

Correspondence
Jacob W. Brownscombe, Fish Ecology and
Conservation Physiology Laboratory, Ottawa-
Carleton Institute for Biology, Carleton
University, 1125 Colonel By Dr., Ottawa, ON
K1S 5B6 Canada.
Email: <jakebrownscombe@gmail.com>

Funding information
This work was funded by a Natural Sciences
and Engineering Research Council of Canada
Discovery Grant (SJC). The swim tunnel was
purchased with support from the Canada
Foundation for Innovation and the Ontario
Ministry of Research and Innovation.
Brownscombe is supported by Bonefish &
Tarpon Trust and Carleton University.
Danylchuk is a Bonefish & Tarpon Trust
Research Fellow.

1 |

INT RODUC TI ON

Accelerometry is growing in popularity for remotely measuring fish swimming metrics, but

appropriate sampling frequencies for accurately measuring these metrics are not well studied.
This research examined the influence of sampling frequency (1–25 Hz) with tri-axial accelerom-

eter biologgers on estimates of overall dynamic body acceleration (ODBA), tail-beat frequency,

swimming speed and metabolic rate of bonefish Albula vulpes in a swim-tunnel respirometer and
free-swimming in a wetland mesocosm. In the swim tunnel, sampling frequencies of ≥ 5 Hz

were sufficient to establish strong relationships between ODBA, swimming speed and metabolic

rate. However,

in free-swimming bonefish, estimates of metabolic rate were more variable

below 10 Hz. Sampling frequencies should be at least twice the maximum tail-beat frequency to

estimate this metric effectively, which is generally higher than those required to estimate

ODBA, swimming speed and metabolic rate. While optimal sampling frequency probably varies

among species due to tail-beat frequency and swimming style, this study provides a reference

point with a medium body-sized sub-carangiform teleost fish, enabling researchers to measure

these metrics effectively and maximize study duration.

K E Y W O R D S

accelerometer, Albula vulpes, biologging, bonefish, metabolism, swimming speed

activity levels (Gleiss et al., 2011), as well as finer scale behaviours

including individual strides, fin or wing beats, or more general behav-

Characterizing how animals behave and expend energy in the wild in

iours such as mating or foraging (Brown et al., 2013). With appropriate

relation to ecological factors and anthropogenic stressors plays an

respirometric calibrations, accelerometers can also be used to esti-

important role in both fundamental biology and applied conservation

mate the active metabolism of animals based on movement (Gleiss

(Buchholz, 2007; Cooke et al., 2014; Sutherland, 1998). Historically,

et al., 2011; King et al., 2004; Wilson et al., 2006). In particular, overall

fish expenditure was typically estimated in relation to swimming

dynamic body acceleration (ODBA) is a highly consistent proxy for

speed and tail-beat frequency in laboratory settings due to the conve-

movement speed and metabolic rate (Brownscombe et al. 2014; Gleiss

niences of quantifying these metrics with cameras (Bainbridge, 1958;

et al. 2011; Halsey et al. 2009; Wright et al. 2014). Given that active

Krohn and Boisdair, 1994). Recent advances in biologging and biote-

metabolism represents a major component of a fish's energy budget

lemetry technologies are now enabling unprecedented insight into

(Boisclair & Leggett, 1989; Jobling, 1994) and can be highly variable in

animal behaviour and bioenergetics in natural environments (Cooke

the wild due to environmental factors,

it is a valuable metric for

et al., 2016; Hussey et al., 2015; Wilmers et al., 2015). Accelerometer

understanding fish ecology and deriving estimates for bioenergetics

tags (transmitters or biologgers) are being increasingly employed to

models (Brodie et al., 2016; Brownscombe et al., 2017).

measure animal behaviour and energetics both in the wild and in cap-

tivity (see Brown et al., 2013; Cooke et al., 2016). Tri-axial accelerom-

eters are most commonly used, which quantify both animal

To capture the range of motion exhibited by animals, accelerome-
ters are typically programmed to sample data multiple times s−1 in all
three axes (note that it is also possible to sample only 1 or 2 axes but

movement (dynamic acceleration) and body posture (static accelera-

this limits ability to detect a full range of activities). A review of animal

tion due to gravity) in three dimensions. This is useful for quantifying

accelerometry across all taxa by Brown et al. (2013) identified the

© 2018 The Fisheries Society of the British Isles

J Fish Biol. 2018;93:207–214.

wileyonlinelibrary.com/journal/jfb

207

208

FISH

BROWNSCOMBE ET AL.

most common sampling frequencies cited in ecological literature to be

Ohlberger et al., 2007). While accelerometers are being increasingly

10, 16 and 32 Hz, but devices can have the capacity to measure up to

applied to study fish behaviour and energetics, few studies have iden-

300 Hz (Broell et al., 2013). In previous applications in fish, the major-

tified optimal sampling frequencies to capture metrics of interest [but

ity of sampling frequencies ranged from 5 to 25 Hz (Brownscombe

see Halsey et al., (2009) for an example with birds]. Broell et al., (2013)

et al., 2014, 2017; Tsuda et al., 2006; O'Toole et al., 2010; Whitney

examined the influence of sampling frequency on identifying fine scale

et al., 2010; Wilson et al., 2013; Wright et al., 2014). While electing

behaviours of great sculpin Myoxocephalus polyacanthocephalus (Pallas

for higher sampling frequencies provides greater temporal resolution

1814), including feeding strikes and escape events. The authors gener-

and more dependable measures of behaviour and energy expenditure,

ally advocated for relatively high frequencies (> 30 Hz) for identifica-

it also limits tag battery life. To some extent this can be offset by

tion of these fine-scale behaviours. Optimal sampling frequencies for

increasing battery size, but this also increases tag burden and restricts

estimating other metrics such as general activity levels, tail-beat fre-

the applications of the tag to only larger animals (Jepsen et al., 2005).

quencies, swimming speeds and metabolic rates are still unclear.

Another consequence of high frequency sampling is that it can result

This study aimed to identify optimal accelerometer sampling fre-

in excessive data beyond what are necessary to address the research

quencies for measuring swimming metrics and metabolic rates with a

question, complicating analysis and increasing computation times.

Identifying optimal sampling frequencies for specific research ques-

tropical marine teleost fish, the bonefish Albula vulpes (L. 1758).
Firstly, the influence of sampling rate (1–25 Hz) on estimates ODBA,

tions is therefore highly relevant to developing best practices for

fish swimming speeds and metabolic rates in a swim-tunnel respirom-

accelerometry.

eter were examined. Secondly, variation in estimates of these metrics

Accelerometer tags have been applied to diverse fish species to

due to sampling frequency was measured with free-swimming

address a range of fundamental and applied research questions, from

A. vulpes in a wetland mesocosm.

general activity to fine scale behaviours and energetics (Broell et al.,

2013; Brownscombe et al., 2013, 2014, 2017; Gleiss et al., 2010;

Murchie et al., 2011; O'Toole et al., 2010; Tsuda et al., 2006; Whitney

et al., 2007, 2010). Oscillations in sway-axis acceleration are also a

2 | M A T E R I A L S A N D M ET H O D S

reliable proxy for tail-beat frequencies (Brownscombe et al., 2013;

2.1 | Fish capture and holding

Sakamoto et al., 2009), which are metrics that historically have been

used as a proxy for metabolic rates (Steinhausen et al., 2005;

Albula vulpes in both experiments described below were captured

from Kemps Creek, Eleuthera, The Bahamas, using a seine net and

then transported by boat to the wet laboratory facility at the Cape

Eleuthera Institute (as per methods described in Murchie et al., 2009).

Albula vulpes were held at the facility in circular holding tanks (3.7 m
diameter × 1.25 m height; 13,180 l) prior to experimentation and

were fed daily rations of chopped fish to satiation. All experiments

were conducted in accordance with the Canadian Council on Animal

Care as administered by the Carleton University Animal Care Commit-

tee (Protocol B10-06).

2.2 | Swim tunnel experiment

Swim-tunnel experiments took place between 0700 and 1000 h from

18 to January 27, 2013. The night prior to experimentation, A. vulpes
(n = 8; 48 (cid:1) 2.5 cm fork length, LF; 35–44 cm range) were tagged
with tri-axial accelerometers (model X8M-3, 500 mAh battery, 15 g in

air, 25 Hz recording frequency; Gulf Coast Data Concepts; www.

gcdataconcepts.com), secured to the A. vulpes externally through the

dorsal musculature to frontal and backing plates with 36 kg breaking

strength braided Dacron line (Figure 1; Brownscombe et al. 2014).

Albula vulpes were fasted for 24 h prior to swim-tunnel experiments

temperature was

and water
this period
(23.3 (cid:1) 0.9(cid:3)C S.D.). After tagging, A. vulpes were placed into a Blazka-
style recirculation swim tunnel (24.1 cm internal diameter × 116 cm
length, 2.1 m s−1 maximum flow rate; Nowell et al., 2015) to acclimate

consistent during

FIGURE 1

Photos of Albula vulpes tagged externally with a tri-axial

accelerometer biologger (a) in a swim-tunnel respirometer and
(b) swimming in a semi-natural wetland

In the swim tunnel, A. vulpes were subjected to a modified ramp-

Ucrit procedure (Jain et al., 1997) involving increases in water speed in
15 cm s−1 increments every 15 min until exhaustion (as per Nowell

over night.

BROWNSCOMBE ET AL.

FISH

209

et al., 2015). At each speed, water oxygen concentrations were mea-

mean and error of explained variance (R2) amongst sampling

sured over a 10 min period using an OxyGuard oxygen probe

frequencies.

(OxyGuard Handy Polaris 2, portable DO meter, Water Management

Technologies,

Inc.; <www.w-m-t.com>). The swim tunnel was then

flushed with fresh seawater directly from the ocean for a 5 min period

prior to increasing the water flow speed. Acceleration data at each

swimming speed were derived from a minimum of a 1 min period

when fish were visually observed maintaining position in the swim

tunnel (i.e. not falling back nor gaining position within the tunnel). This

approach may have incurred some biases due to variation in fish

movement throughout the entire 10 min respirometry period that was

not captured with the 1 min acceleration measurement period, yet

yielded a more accurate estimate of the relationship between acceler-

ation and swimming speed. After experimentation, accelerometers

were removed and fish were measured for body mass, total length

(LT), LF, WB and DB for calculations of blocking effect and metabolic
rate. Fish were then placed into a holding tank for 24 h prior to

release.

Measurements of water oxygen concentration in the swim tunnel

(cid:4)
O2; mg
were used to estimate A. vulpes oxygen consumption rate (M
(cid:4)
O2 = Δ[O2] υ(Mt)−1,
O2 min−1 kg−1) at each swimming speed using: M
where Δ[O2] is the change on oxygen concentration (mg l−1), v is the
swim tunnel volume (total volume minus the fish's volume; L), M is the

fish's mass (kg) and t is time (min). Albula vulpes swimming speeds

(SS) were corrected for the solid blocking effect (i.e.,the increase in

water velocity around the fish due to its presence in the tunnel) based
on Bell & Terhune (1970): SS = Vh1 + {0.4LF [0.5(M + DB)]−1}i [0.25 π
DBM(At)−1]1.5, where V is swim tunnel water velocity (cm s−1) and A is
swim tunnel cross-sectional area.

Tri-axial acceleration data consisted of acceleration ( g) in three

2.3 | Wetland mesocosm experiment

Albula vulpes (n = 8; mean (cid:1) S.D. LT = 38.8 (cid:1) 2.3 cm, 35–42 cm
range) were tagged with tri-axial accelerometer loggers in the same

manner as the swim-tunnel experiment and immediately placed in a c.
2,500 m2 semi-natural wetland mesocosm at the Cape Eleuthera Insti-

tute on January 18, 2015. The mesocosm is supplied with seawater

from the adjacent wet-lab facility and vegetated with red mangrove

Rhizophora mangle and black mangrove Avicennia germinans. This envi-

ronment is similar to A. vulpes habitats in the mangrove creeks of

nearshore Eleuthera, but it is disconnected from the ocean and not

influenced by tides. Previous work has shown that A. vulpes exhibit a

range of typical behaviours in this mesocosm, including regular forag-

ing (Brownscombe et al., 2014; Murchie et al., 2011). The data exam-
ined here were derived from a 4 h period, 1300–1700 hours on

January 19, 2015.

Albula vulpes wetland acceleration data were analyzed in the same

manner as the swim tunnel data and mean ODBA was calculated for

each second over the 4 h period. Swimming speeds and oxygen con-

sumption rates were then predicted using the models from the swim

tunnel experiment. Mean ODBA, swimming speed and metabolic rate

for each individual fish were compared between sampling frequencies

by fitting linear mixed effects models to each variable with sampling

frequency as a predictor and fish ID as a random intercept. Pairwise

comparisons were implemented using the glht function in the R pack-

age multcomp (Hothorn et al. 2008) to determine whether there were

significant differences between sampling frequencies.

axes (Ax = surge, Ay = heave, Az = sway in our fish attachment orien-
tation). These data were subset from the full dataset (25 Hz sampling

3 | RE SU LT S

frequency) to datasets of 1, 3, 5, 10, 15 and 20 Hz. This was accom-

plished by selecting every nth data row, where n = (full sampling fre-
quency)(subset sampling frequency)−1. To separate static (gravity)

from dynamic (fish movement) acceleration, a box smoother was

applied. The optimal smoothing interval was determined using the

method described in Shepard et al.

(2008) for each sampling fre-

quency. While a 2 s running mean was sufficient for sampling frequen-

cies of 3 Hz and higher, a 5 s running mean was applied to the 1 Hz

dataset. ODBA ( g) was calculated as the absolute sum of the dynamic

acceleration in all axes. Albula vulpes tail-beat frequency was calcu-

lated from Az-axis dynamic acceleration data using a short-term Fou-
rier transform with the dfreq function in the R package seewave

(Sueur et al., 2008).

Relationships between A. vulpes swimming speed, ODBA, tail-

beat frequency and metabolic rate in the swim tunnel were fit with a

series of linear mixed effects (LMM) models using the package nlme in

3.1 | Swim tunnel experiment

There was a significant positive relationship between A. vulpes swim-

ming speed and ODBA, as well as ODBA and metabolic rate in the

swim tunnel at all sampling frequencies (Figure 2(a),

(c) and

Table 1). However, there was no significant relationship between

swimming speed and tail-beat frequency at sampling frequencies of

< 10 Hz (Figure 2(b) and Table 1). The relationship between ODBA

and swimming speed, as well as ODBA and metabolic rate were both
highly consistent at sampling frequencies of ≥ 5 Hz, but more variable

at lower frequencies (Figure 3(a), (c) and Table 1). However, tail-beat

frequency was more consistent with swimming speed at sampling fre-
quencies of ≥10 Hz (Figure 3(b) and Table 1).

3.2 | Wetland mesocosm experiment

R (Pinheiro et al., 2015). At each sampling frequency, LMMs were fit

with ODBA as the response and swimming speed as the predictor,

Measurements of A. vulpes ODBA were very consistent at sampling
frequencies ≥ 3 Hz, but 1 Hz was significantly higher than other fre-

tail-beat frequency as the response and swimming speed as the pre-

quencies (Figure 4(a)). Owing to a combination of higher estimates of

dictor and O2 as the response and ODBA as the predictor. All models
included fish as a random intercept. In addition, linear models were fit

ODBA as well as variation in predictive-model coefficients from the

swim-tunnel experiment, estimates of A. vulpes swimming speeds in

to each individual fish for all of these relationships to compare the

the wetland were significantly higher at sampling frequencies of

210

(a)

)
g
(

A
B
D
O

1·00

0·75

0·50

0·25

0·00

1·00

0·75

0·50

0·25

0·00

1·00

0·75

0·50

0·25

0·00

1·00

0·75

0·50

0·25

0·00

1·00

0·75

0·50

0·25

0·00

1·00

0·75

0·50

0·25

0·00

1·00

0·75

0·50

0·25

0·00

FISH

BROWNSCOMBE ET AL.

(b)

(c)

12

)
z
H

(

F
B
T

6

4

2

0

6

4

2

0

6

4

2

0

6

4

2

0

6

4

2

0

6

4

2

0

6

4

2

0

)
1
–
n
m

i

1
–
g
k

2

O
g
m

(

2

O
Ṁ

9

6

3

0

12

9

6

3

0

12

9

6

3

0

12

9

6

3

0

12

9

6

3

0

12

9

6

3

0

12

9

6

3

0

1 Hz

3 Hz

5 Hz

10 Hz

y
c
n
e
u
q
e
r
f
g
n

i
l

p
m
a
S

15 Hz

20 Hz

25 Hz

0

20

40

60

80

0

20

40

60

80

0

20

40

60

80

Swimming speed (cm s–1)

Swimming speed (cm s–1)

FIGURE 2

The relationship between (a) swimming speed and overall dynamic body acceleration (ODBA), (b) swimming speed and tail beat
frequency (TBF), (c) ODBA and metabolic rate at a range of sampling frequencies measured in Albula vulpes in a swim-tunnel respirometer.
mean value for individual fish at each swimming speed. Where there is a significant relationship, the data were fitted with a linear mixed effect
model ( (cid:1)95% C.I.)

,

< 5 Hz than higher sampling frequencies (Figure 4(b)). Variation

frequency with tri-axial accelerometers on estimates of ODBA, swim-

amongst sampling frequencies was greatest in estimates of A. vulpes

ming speeds, tail-beat frequencies and metabolic rates in A. vulpes,

metabolic rate, where sampling frequencies of < 10 Hz were signifi-

with the goal of identifying minimum frequencies required to effec-

cantly different from those 10 Hz or higher (Figure 4(c)).

4 | D I S C U S S I O N

tively measure metrics that are relevant to fish ecology and bioener-

getics. To accomplish this we used a ramp-Ucrit procedure in a swim-
tunnel respirometer (Jain et al., 1997); an important limitation of this

approach is that anaerobic recruitment can occur at higher swimming

speeds, influencing the estimated relationship between aerobic meta-

Accelerometry is a valuable tool for studying both animal behaviour

bolic rate, acceleration and swimming speed. Importantly, this does

and ecological energetics (Brown et al., 2013; Cooke et al. 2016). With

not affect our assessment of the influence of accelerometer sampling

the rapid expansion in its application, it is important to develop best

frequency on estimates of

fish swimming metrics because our

practices for accelerometry that ensure research questions are

methods were consistent in both the swim tunnel and free-swimming

addressed effectively. Here we explored the influence of sampling

A. vulpes data.

BROWNSCOMBE ET AL.

FISH

211

TABLE 1

Linear mixed effects model outputs predicting overall dynamic body acceleration (ODBA) and tail-beat frequency (TBF) by swimming

O2) by ODBA at a range of sampling frequencies with Albula vulpes in a swim-tunnel respirometer. Individual was

(cid:4)
speed, and metabolic rate (M
included as a random effect

Model

Frequency (Hz)

Intercept

Value

S.E.

Marginal R2

Conditional R2

t

P

ODBA by swimming speed

1

3

5

10

15

20

25

TBF by swimming speed

1

3

5

10

15

20

25
(cid:4)
M

O2 by ODBA

1

3

5

10

15

20

25

0.018
−0.014
−0.004
−0.008
−0.010
−0.010
−0.010

0.37

0.78

1.97

1.23

1.30

1.17

1.30

3.64

4.07

3.75

3.81

3.82

3.83

3.82

0.008

0.009

0.010

0.010

0.010

0.010

0.010

0.0002

0.0005

−0.007

0.040

0.040

0.040

0.040

7.25

5.67

6.31

6.07

5.96

5.97

5.99

0.0006

0.0009

0.0008

0.0008

0.0008

0.0008

0.0008

0.0005

0.0020

0.0040

0.0040

0.0030

0.0030

0.0030

1.41

1.24

1.19

1.18

1.16

1.17

1.17

0.76

0.69

0.73

0.73

0.73

0.73

0.74

0.002

0.002

0.09

0.66

0.78

0.73

0.73

0.40

0.36

0.42

0.41

0.40

0.40

0.40

0.87

0.82

0.87

0.87

0.86

0.86

0.87

0.59

0.60

0.09

0.83

0.89

0.91

0.91

0.62

0.57

0.63

0.62

0.61

0.61

0.61

12.8

10.6

12.8

12.5

12.4

12.4

12.6

0.3

0.3
−1.7

10.6

14.5

15.5

15.4

5.1

4.6

5.3

5.1

5.1

5.1

5.1

<0.001

<0.001

<0.001

<0.001

<0.001

<0.001

<0.001

>0.05

>0.05

>0.05

<0.001

<0.001

<0.001

<0.001

<0.001

<0.001

<0.001

<0.001

<0.001

<0.001

<0.001

We found sampling frequencies of just 1 Hz were sufficient to

While higher sampling frequencies resulted in more accurate esti-

establish strong relationships between ODBA, swimming speed and

mates of A. vulpes swimming speeds and metabolic rates, sampling

metabolic rate. However, the variance in these relationships and lin-

rates as low as 1 Hz would still provide a measure of general activity

ear mixed effects model coefficients were more variable below

level. Conversely, for the measurement of finer scale behaviours,

5 Hz. Further,

in free swimming A. vulpes, estimates of metabolic

Broell et al.

(2013)

found relatively high sampling frequencies

rate were significantly different below 10 Hz. Given that higher

(> 30 Hz) were required to effectively identify rapid feeding strikes

sampling frequencies are most effective at accurately capturing the

and escape responses in M. polyacanthocephalus. It is intuitive that

full range of animal movement, which is directly related to move-

rapid behaviours would require higher sampling frequencies to be

ment speed and active metabolism, this variation reflects decreased

identified and discriminated.

In other work, Brownscombe et al.

accuracy in estimates of fish swimming speed and metabolic rate at

(2014) were able to identify benthic foraging in A. vulpes using 25 Hz,

lower sampling frequencies. Similarly, frequencies of < 10 Hz were

whereas Whitney et al. (2010) were able to identify nurse shark Gin-

ineffective at estimating A. vulpes tail-beat frequencies in the swim

glymostoma cirratum (Bonnaterre 1788) mating behaviours with only

tunnel. Given that the maximum A. vulpes tail-beat frequencies

5 Hz sampling frequencies. When choosing a sampling frequency for

observed in the swim tunnel were < 5 Hz, this is consistent with

accelerometer applications, it is important to consider the study objec-

signal processing theory, which suggests sampling must be at least

tives and relevant timeframes for metrics of interest.

twice as frequent as the highest frequency wave in a waveform

According to signal processing theory, sampling must be at least

(Brown et al., 2013; Yost et al., 1983). Because tail-beat frequencies

twice as frequent as the highest frequency wave in a waveform

of

free swimming A.

vulpes

reach a maximum of 9 Hz

(Brown et al., 2013; Yost et al., 1983). The sampling frequency will

(Brownscombe et al., 2014), sampling frequencies of > 18 Hz would

therefore depend to some extent on the species of interest, particu-

be required to estimate this metric effectively. While estimates of

larly given the allometric scaling of body movements, with an inverse

tail-beat frequency from accelerometer tags are valuable for com-

relationship between animal size and stroke frequency (Sato et al.,

parisons with previous fish swimming and bioenergetics research

2009). In fish, the body shape and swimming style must also be con-

(Cooke et al., 2016), higher sampling frequencies are required to

sidered because the wavelength of the swimming stroke influences

acquire accurate estimates of tail-beat frequency than ODBA, swim-

the frequency of the propulsion by tail beat. For example, the short

ming speed and metabolism.

wavelength tail-beat characteristic of

fast-swimming thunniform

212

(a)

FISH

ODBA by swimming speed

1·0

0·9

0·8

0·7

0·6

0·5

(b)

Tail beat frequency by swimming speed

1·00

0·75

2
R

0·50

(c)

0·25

0·00

1·00

0·75

0·50

0·25

0·00

Metabolic rate by ODBA

(c)

)
1
–
n
m

i

1
–
g
k

2

O
g
m

(

2

O
Ṁ

(a)

0·08

)
g
(

A
B
D
O

(b)

)
1
–
s
m
c
(

d
e
e
p
s
g
n
m
m
w
S

i

i

0·06

0·04

0·02

0·00

7·5

5·0

2·5

0·0

4·5

4·0

3·5

3·0

BROWNSCOMBE ET AL.

b

b

b

b

b

b

a

a

c

c

c

c

c

b

b

a

a

c

c

c

c

1

3

5

10
Sampling frequency (Hz)

15

20

25

0

5

10

15

20

25

Sampling frequency (Hz)

FIGURE 3 Mean ((cid:1)S.E.) explained variance (R2) in (a) overall dynamic
body acceleration (ODBA) by swimming speed, (b) tail-beat frequency
by swimming speed, and (c) metabolic rate by ODBA from linear
models fit to individual Albula vulpes in a swim tunnel

FIGURE 4 Mean ((cid:1)S.E.) estimates of (a) overall dynamic body
acceleration (ODBA), (b) swimming speed and (c) metabolic rate from
free-swimming Albula vulpes in a semi-natural wetland mesocosm over
a 4 h period. Different lower-case letters indicate significant
differences between sampling frequencies (Tukey's HSD post hoc
test, p < 0.05) on fitted linear mixed effects models

fishes are more frequent than those of slower swimming anguilliform

In recent applications, the majority of studies have employed

fishes with a longer swimming stoke whose wavelength travels farther

accelerometer transmitters with relatively low sampling frequencies

down the body [see Froese & Pauly (2016) for swimming styles of

(typically c. 5 Hz; Brownscombe et al., 2017; O'Toole et al., 2010;

fishes]. Albula vulpes have a subcarangiform swimming style and our

Payne et al., 2011; Wilson et al., 2013), which should suffice to pro-

findings suggest that sampling at 10 Hz should suffice for most accel-

vide accurate estimates of activity level (ODBA) and swimming speed,

erometer applications unless tail-beat frequency is of interest. Higher

although may incur some biases in estimating metabolic rate. Studies

frequencies would probably be required for smaller-bodied species,

employing data loggers generally utilize higher frequencies > 20 Hz

species with shorter movement wavelengths (e.g. thunniform swim-

that provide greater behavioural resolution, including for measuring

mers), or for identifying movements of shorter duration (Broell

tail-beat frequency (Broell et al., 2013; Brownscombe et al., 2013,

et al., 2013).

2014; Thiem et al., 2015). In some cases, this may be excessively high

BROWNSCOMBE ET AL.

if the goal is estimate swimming speed or metabolic rate and not to

identify fine scale behaviour or count tail-beat frequencies. There is

generally a tradeoff between sampling frequency and study duration,

but alternative approaches such as interval sampling can be used to

maintain high resolution of data while maintaining a longer period of

sampling if necessary (Dow et al., 2009). Advanced onboard proces-

sing of acceleration signals to automatic classification of behaviour

can also be programmed into tags to limit the onboard memory use

(Broell et al., 2013).

In conclusion, accelerometer tags are a valuable tool for remotely

measuring fish behaviour and metabolism, with diverse application for

understanding how ecological factors influence behaviour and energy

expenditure (Brown et al., 2013; Brownscombe et al., 2017; Gleiss

et al., 2011), as well as estimates of active metabolic rate for bioener-

getics models (Cooke et al., 2016). Identifying the minimum effective

sampling frequencies for measuring metrics of interest will ensure that

research questions are addressed effectively while also maximizing
data collection duration. We found sampling frequencies of ≥ 5 Hz

were sufficient to estimate swimming speed from accelerometer-
derived ODBA, while ≥ 10 Hz would be most accurate for estimating

metabolic rate and higher frequencies are required to estimate tail-

beat frequencies (at least twice the maximum TBF). Although lower

sampling frequencies provide general estimates of activity levels,

higher frequencies are often required to accurately identify finer scale

behaviours. Optimal sampling frequencies are certainly related to

study objective and metrics of interest, as well as species characteris-

tics, namely body size and swimming style.

ACKNOWLEDGEMEN TS

We thank the staff of the Cape Eleuthera Institute for providing facili-

ties and support for this research.

ORCID

Jacob W. Brownscombe

<http://orcid.org/0000-0003-2496-8764>

Robert J. Lennox

<http://orcid.org/0000-0003-1010-0577>

RE FE R ENC E S

Bainbridge, R. (1958). The speed of swimming of fish as related to size and
to the frequency and amplitude of the tail beat. Journal of Experimental
Biology., 35, 109–133.

Bell, W., & Terhune, L. (1970). Water tunnel design for fisheries research.

Fisheries Research Board of Canada Technical Report, 195, 1–169.

Boisclair, D., & Leggett, W. C. (1989). The importance of activity in bioen-
ergetics models applied to actively foraging fishes. Canadian Journal of
Fisheries and Aquatic Sciences, 46, 1859–1867.
Brodie, S., Taylor, M. D., Smith, J. A., Suthers,

I. M., Gray, C. A., &
Payne, N. L. (2016). Improving consumption rate estimates by incorpo-
rating wild activity into a bioenergetics model. Ecology and Evolution, 6,
2262–2274.

Broell, F., Noda, T., Wright, S., Domenici, P., Steffensen,

J. F.,
Auclair, J.-P., & Taggart, C. T. (2013). Accelerometer tags: Detecting
and identifying activities in fish and the effect of sampling frequency.
The Journal of Experimental Biology, 216, 1255–1264.

Brown, D. D., Kays, R., Wikelski, M., Wilson, R., & Klimley, A. P. (2013).
Observing the unwatchable through acceleration logging of animal
behavior.
<https://doi.org/10>.
1186/2050-3385-1-20

Biotelemetry,

Animal

20.

1,

FISH

213

Brownscombe, J. W., Thiem, J. D., Hatry, C., Cull, F., Haak, C. R.,
Danylchuk, A. J., & Cooke, S. J.
(2013). Recovery bags reduce
post-release impairments in locomotory activity and behavior of bone-
fish (Albula spp.) following exposure to angling-related stressors. Jour-
nal of Experimental Marine Biology and Ecology, 440, 207–215.

Brownscombe, J. W., Gutowsky, L. F. G., Danylchuk, A. J., & Cooke, S. J.
(2014). Foraging behaviour and activity of a marine benthivorous fish
estimated using tri-axial accelerometer biologgers. Marine Ecology Pro-
gress Series, 505, 241–251.

Brownscombe, J. W., Cooke, S. J., & Danylchuk, A. J. (2017). Spatiotempo-
ral drivers of energy expenditure in a coastal marine fish. Oecologia,
183, 689–699.

Buchholz, R. (2007). Behavioural biology: An effective and relevant conser-

vation tool. Trends in Ecology and Evolution, 22, 401–407.

Cooke, S. J., Blumstein, D. T., Buchholz, R., Caro, T., Fernández-Juricic, E.,
Franklin, C. E., … Wikelski, M. (2014). Physiology, behavior and conser-
vation. Physiological and Biochemical Zoology, 87, 1–14.

Cooke, S. J., Brownscombe, J. W., Raby, G. D., Broell, F., Hinch, S. G.,
Clark, T. D., & Semmens, J. M. (2016). Remote bioenergetics measure-
ments in wild fish: Opportunities and challenges. Comparative Biochem-
istry and Physiology A, 202, 23–37.

Dow, C., Michel, K. E., Love, M., & Brown, D. C. (2009). Evaluation of opti-
mal sampling interval for activity monitoring in companion dogs. Ameri-
can Journal of Veterinary Research, 70, 444–448.

Froese, R. & Pauly, D. (2016) FishBase. Retrieved from <www.fishbase.org/>

search.php

Gleiss, A. C., Dale, J. J., Holland, K. N., & Wilson, R. P. (2010). Accelerating
estimates of activity-specific metabolic rate in fishes: Testing the appli-
cability of acceleration data-loggers. Journal of Experimental Marine
Biology and Ecology, 385, 85–91.

Gleiss, A. C., Wilson, R. P., & Shepard, E. L. C. (2011). Making overall
dynamic body acceleration work: On the theory of acceleration as a
proxy for energy expenditure. Methods in Ecology and Evolution, 2,
23–33.

Halsey, L. G., Shepard, E. L. C., Quintana, F., Gomez Laich, A.,
Green, J. A., & Wilson, R. P. (2009). The relationship between oxygen
consumption and body acceleration in a range of species. Comparative
Biochemistry and Physiology A, 152, 197–202.

Hothorn, T., Bretz, F., & Westfall, P. (2008). Simultaneous inference in gen-

eral parametric models. Biometrical Journal, 50, 346–363.

Hussey, N. E., Kessel, S. T., Aarestrup, K., Cooke, S. J., Cowley, P. D.,
Fisk, A. T., … Whoriskey, F. G. (2015). Aquatic animal telemetry: A pan-
oramic window into the underwater world. Science, 348, 1255642.
Jain, K., Hamilton, J., & Farrell, A. (1997). Use of a ramp velocity test to
measure critical swimming speed in rainbow trout (Onchorhynchus
mykiss). Comparative Biochemistry and Physiology Part A: Physiology,
117, 441–444.

Jepsen, N., Schreck, C., & Clements, S. (2005). A brief discussion on the
2% tag/bodymass rule of thumb. In M. T. Lembo & G. Marmulla (Eds.),
Aquatic telemetry: Advances and applications (pp. 255–259). Rome,
Italy: FAO.

Jobling, M. (1994). Fish bioenergetics. London, England: Chapman and Hall.
King, A. M., Loiselle, D. S., & Kohl, P. (2004). Force generation for locomo-
tion of vertebrates: Skeletal muscle overview. IEEE Journal of Oceanic
Engineering, 29, 684–691.

Krohn, M. M., & Boisdair, D. (1994). Use of a stereo-video system to esti-
mate the energy expenditure of free-swimming fish. Canadian Journal
of Fisheries and Aquatic Sciences, 51, 1119–1127.

Murchie, K. J., Danylchuk, S. E., Pullen, C. E., Brooks, E., Shultz, A. D.,
Suski, C. D., … Cooke, S. J. (2009). Strategies for the capture and trans-
port of bonefish, Albula vulpes, from tidal creeks to a marine research
laboratory
40,
long-term holding. Aquaculture
1538–1550.

Research,

for

Murchie, K. J., Cooke, S. J., Danylchuk, A. J., & Suski, C. D. (2011). Esti-
mates of field activity and metabolic rates of bonefish (Albula vulpes) in
coastal marine habitats using acoustic tri-axial accelerometer transmit-
ters and intermittent-flow respirometry. Journal of Experimental Marine
Biology and Ecology, 396, 147–155.

Nowell, L. B., Brownscombe, J. W., Gutowsky, L. F. G., Murchie, K. J.,
Suski, C. D., Danylchuk, A. J., … Cooke, S. J. (2015). Swimming energet-
ics and thermal ecology of adult bonefish (Albula vulpes): A combined

214

FISH

laboratory and field study in Eleuthera, the Bahamas. Environmental
Biology of Fishes, 98, 2133–2146.

Ohlberger, J., Staaks, G., & Holker, F. (2007). Estimating the active meta-
bolic rate (AMR) in fish based on tail beat frequency (TBF) and body
mass. The Journal of Experimental Biology, 307A, 296–300.

Payne, N. L., Gillanders, B. M., Seymour, R. S., Webber, D. M.,
Snelling, E. P., & Semmens, J. M. (2011). Accelerometry estimates field
metabolic rate in giant australian cuttlefish Sepia Apama during breed-
ing. Journal of Animal Ecology, 80, 422–430.

Pinheiro, J., Bates, D., DebRoy, S., Sarkar, D. & Team, R. (2015) nlme: Linear
and nonlinear mixed effects models. R package version 3.1–120.
Retrieved from <www.CRAN.R-project.org/package=nlme>

Sakamoto, K. Q., Sato, K.,

Ishizuka, M., Watanuki, Y., Takahashi, A.,
Daunt, F., & Wanless, S. (2009). Can ethograms be automatically gen-
erated using body acceleration data from free-ranging birds? PLoS One,
4, e5379.

Sato, K., Sakamoto, K. Q., Watanuki, Y., Takahashi, A., Katsumata, N.,
Bost, C. A., & Weimerskirch, H. (2009). Scaling of soaring seabirds and
implications for flight abilities of giant pterosaurs. PLoS One, 4, e5400.

Shepard, E. L. C., Wilson, R. P., Halsey, L. G., Quintana, F., Laich, A. G.,
Gleiss, A. C., … Norman, B. (2008). Derivation of body motion via
appropriate smoothing of acceleration data. Aquatic Biology, 4,
235–241.

Steinhausen, M. F., Steffensen, J. F., & Andersen, N. G. (2005). Tail beat
frequency as a predictor of swimming speed and oxygen consumption
of saithe (Pollachius virens) and whiting (Merlangius merlangus) during
forced swimming. Marine Biology, 148, 197–204.

Sueur, J., Aubin, T., & Simonis, C. (2008). Seewave: A free modular tool for

sound analysis and synthesis. Bioacoustics, 18, 213–226.

Sutherland, W. (1998). The importance of behavioural studies in conserva-

tion biology. Animal Behaviour, 56, 801–809.

Thiem, J. D., Dawson, J. W., Gleiss, A. C., Martins, E. G., Haro, A.,
Castro-Santos, T., … Cooke, S. J. (2015). Accelerometer-derived activity
correlates with volitional swimming speed in lake sturgeon (Acipenser
fulvescens). Canadian Journal of Zoology, 93, 645–654.

O'Toole, A. C., Murchie, K. J., Pullen, C., Hanson, K. C., Suski, C. D.,
Danylchuk, A. J., & Cooke, S. J. (2010). Locomotory activity and depth
distribution of adult great barracuda (Sphyraena barracuda) in Bahamian
coastal habitats determined using acceleration and pressure bioteleme-
try transmitters. Marine and Freshwater Research, 61, 1446–1456.

BROWNSCOMBE ET AL.

Tsuda, Y., Kawabe, R., Tanaka, H., Mitsunaga, Y., Hiraishi, T.,
Yamamoto, K., & Nashimoto, K.
(2006). Monitoring the spawning
behaviour of chum salmon with an acceleration data logger. Ecology of
Freshwater Fish, 15, 264–274.

Whitney, N. M., Papastamatiou, Y. P., Holland, K. N., & Lowe, C. G. (2007).
Use of an acceleration data logger to measure diel activity patterns in
captive whitetip reef
sharks, Triaenodon obesus. Aquatic Living
Resources, 20, 299–305.

Whitney, N. M., Pratt, H. L., Pratt, T. C., & Carrier, J. C. (2010). Identifying
shark mating behaviour using three-dimensional acceleration loggers.
Endangered Species Research, 10, 71–82.

Wilmers, C. C., Nickel, B., Bryce, C. M., Smith, J. A., Wheat, R. E.,
Yovovich, V., & Hebblewhite, M. (2015). The golden age of bio-logging:
How animal-borne sensors are advancing the frontiers of ecology. Ecol-
ogy, 96, 1741–1753.

Wilson, R. P., White, C. R., Quintana, F., Halsey, L. G., Liebsch, N.,
Martin, G. R., & Butler, P. J. (2006). Moving towards acceleration for
estimates of activity-specific metabolic rate in free-living animals: The
case of the cormorant. Journal of Animal Ecology, 75, 1081–1090.
Wilson, S. M., Hinch, S. G., Eliason, E. J., Farrell, A. P., & Cooke, S. J. (2013).
Calibrating acoustic acceleration transmitters for estimating energy
use by wild adult Pacific salmon. Comparative Biochemistry and Physiol-
ogy A, 164, 491–498.

Wright, S., Metcalfe, J. D., Hetherington, S., & Wilson, R. (2014). Estimat-
ing activity-specific energy expenditure in a teleost fish, using acceler-
ometer loggers. Marine Ecology Progress Series, 496, 19–32.

Yost, M., Cooper, R. A., & Bremner, F. J. (1983). Fourier analyses: A mathe-
matical and geometric explanation. Behavior Research Methods & Instru-
mentation, 15, 258–261.

How to cite this article: Brownscombe JW, Lennox RJ,

Danylchuk AJ, Cooke SJ. Estimating fish swimming metrics

and metabolic rates with accelerometers: the influence of sam-
pling frequency. J Fish Biol. 2018;93:207–214. <https://doi.org/>

10.1111/jfb.13652
