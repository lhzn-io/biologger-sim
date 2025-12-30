royalsocietypublishing.org/journal/rstb

Review

Cite this article: Holton MD, Wilson RP,
Teilmann J, Siebert U. 2021 Animal tag
technology keeps coming of age: an
engineering perspective. Phil. Trans. R. Soc. B
376: 20200229.
<https://doi.org/10.1098/rstb.2020.0229>

Accepted: 3 December 2020

One contribution of 10 to a theme issue
‘Measuring physiology in free-living animals
(Part II)’.

Subject Areas:
behaviour, ecology, environmental science

Keywords:
tagging, behaviour, technology, movement,
logger, biologging

Authors for correspondence:
Mark D. Holton
e-mail: <m.d.holton@swansea.ac.uk>
Rory P. Wilson
e-mail: <r.p.wilson@swansea.ac.uk>

†These authors contributed equally to the
study.

Animal tag technology keeps coming
of age: an engineering perspective

Mark D. Holton1,†, Rory P. Wilson1,†, Jonas Teilmann2 and Ursula Siebert3

1Biosciences, Swansea University, Singleton Park, Swansea SA2 8PP, UK
2Marine Mammal Research, Department of Bioscience, Aarhus University, Frederiksborgvej 399, 4000 Roskilde,
Denmark
3Institute for Terrestrial and Aquatic Wildlife Research, University of Veterinary Medicine Hannover, Bischofsholer
Damm 15, 30173 Hannover, Germany

RPW, 0000-0003-3177-0107; JT, 0000-0002-4376-4700

Animal-borne tags (biologgers) have now become extremely sophisticated,
recording data from multiple sensors at high frequencies for long periods
and, as such, have become a powerful tool for behavioural ecologists and
physiologists studying wild animals. But the design and implementation
of these tags is not trivial because engineers have to maximize performance
and ability to function under onerous conditions while minimizing tag mass
and volume (footprint) to maximize the wellbeing of the animal carriers. We
present some of the major issues faced by tag engineers and show how tag
designers must accept compromises while maintaining systems that can
answer the questions being posed. We also argue that basic understanding
of engineering issues in tag design by biologists will help feedback to
engineers to better tag construction but also reduce the likelihood that
tag-deploying biologists will misunderstand their own results. Finally, we
technology together
suggest
with new approaches will lead to further step changes in our understanding
of wild-animal biology using smart tags.

that proper consideration of conventional

This article is part of the theme issue ‘Measuring physiology in free-

living animals (Part II)’.

1. Introduction
Data logging technology these days is ubiquitous due to current vehicle and
mobile phone technology, logging data either within localized memory storage
or transmitting-on-request,
(accelerometer)
information to a distant server for processing.

location (GPS) and movement

Animal-borne tags recording information have, however, been around for
over 4 decades now, collecting many different types of information, not
unlike mobile phone technology, including, but not limited to, GPS location
[1], acceleration [2], magnetic field strength [3], temperature [4], pressure [5],
heart rate [6], ambient light levels [7], conductivity [8] etc., and have trans-
formed our understanding of wild-animal physiology [9–11], ecology [12]
and behaviour [13] and, as such, play a major role in informing conservation
[14]. By combining some, or all, of these sensors, one can ‘see’ what an
animal is doing, where it is doing it and potentially, what the environmental
(and terrain) conditions are, and so generate a second-by-second diary of the
animal’s behaviour in three-dimensional space, and subsequently, poten-
tially determine if the behaviour is borne from environmental effects or
something else.

The development of these tags has been extraordinary, primarily as a result
of developments in the solid-state industry, driven by consumers. Alone within
the data logger (aka biologgers) community, data storage is now as high as
64 GB [15], sensor count may exceed 9 (e.g. [16]) with deployment periods ran-
ging to years [17] and recording frequencies of now up to greater than 180 kHz
[18] on animals as diverse as small bats [18] and 100 ton blue whales [19,20]. As
a result of recent advances in semiconductor technology, storage capacity is no

© 2021 The Author(s) Published by the Royal Society. All rights reserved.

 Downloaded from <https://royalsocietypublishing.org/> on 04 September 2025 2

r
o
y
a
l
s
o
c
i

e
t
y
p
u
b

i

.

l
i
s
h
n
g
o
r
g
/
j
o
u
r
n
a
l
/
r
s
t
b

P
h

i
l
.

T
r
a
n
s
.

R

.

S
o
c
.

B

3
7
6

:

2
0
2
0
0
2
2
9

longer an issue; microSD cards are now available with 1 TB of
data storage. This is an extraordinary amount of storage
−1),
space. For example, a data logger storing: time (at 40 B s
tri-axial acceleration (6 B at 40 Hz), tri-axial magnetometry
(6 B at 13 Hz), temperature and pressure (both using 3 B at
−1. At that rate, it would
4 Hz), equates to just under 512 B s
take about 7 years to fill a 64 GB card and over a hundred
years to fill a single 1 TB card.

fundamental element of all. That

The changing range of animals used as a function of the
time over which the technology has been developed reflects
perhaps the most
tag
‘size’ affects animals, and what this means to the engineer
[21]. Animal-associated tags affect animals in a suite of
ways ranging from increased energy expenditure [22] to
increased mortality [23], and it is clear that larger tags are
expected to lead to greater detriment (but see [22]), so biol-
ogists should be striving to reduce the size of the tags,
almost whatever the size of the carrier. Coupled with this,
though, is the reasonable expectation that ever smaller tags
can be deployed on ever smaller animals [24], which opens
up the potential of tag technology insights on an increasing
range of species because most animals are small.

This is the major challenge for the tag engineer because
high performance measuring systems that operate under
challenging conditions can be constructed relatively easily if
they are not size limited. But beyond that, these tags, and
their deployment protocols, need to be fool-proof so that
when tags are being deployed under the onerous conditions
that typify much fieldwork, no pilot errors [25] are made.
Finally, assuming the tag, or at least the data, can be recov-
ered, it is useful if there is software that allows the biologist
to see what she/he has got. Indeed, rapid repeat deploy-
ments in the field should rely on confirmation of quality
before tags are redeployed.

This article takes an engineering perspective to detail
some of the important consideration in the design of biolog-
gers, rather than systems that also, or uniquely, incorporate
transmission telemetry. Cognizance of this is not just for
the engineers because if the design and decision-making pro-
cess is understood by biologists, judgements can be made in
the field about how to programme the tags, for example, to
get the best (duration, resolution, sensor activation, duty-
cycling etc.) from the data. Finally, this paper will muse
over where the future might take animal tagging, which is
rapidly becoming a mainstream discipline in its own right.

2. Animals first
There is an increasing number of publications which show the
detrimental effect of tags on their carriers [22,26,27] such as
changes in behaviour and increased energy uses, and, in the
interests of ethically, morally and otherwise good science, we
need to be working to minimize these effects [28]. This not
only requires that workers consider tag placement on their
study animals [29] but also that they minimize tag mass [30],
because this creates forces that can lead to sores and even
death [31], minimize the tag-animal footprint for inter alia
heat loss reasons [32], maximize streamlining [33] and even
consider tag colour [34] and electronic blinking lights that
may cause behavioural changes of predator, prey or conspeci-
fics. Most of these issues are the province of engineers. This is
because, on the one hand, it is linked to the physicality of tag

effects [35] where techniques like flow visualization [36] and
computer fluid dynamics can help minimize detriment [33],
but, on the other, the miniaturization and precise layout of
the tag components define the physical form of the tags. Tag
design engineers, therefore, have to work under severe con-
straints, which are further complicated since an optimized
tag design for one species will not necessarily be right for
another. The niceties of this are not covered here but will be
reflected in an important drive for engineers to reduce tag
size in general, so minimization of tag size underpins the
rest of this paper.

the environment,

3. Hardware
(a) Sensors
The number of sensors is extraordinary [37], with researchers
now measuring everything from internal physiological par-
ameters such as heart rate [38,39] and stomach pH [40]
through sensors that work both internally and externally
such as respiration rate sensors [41], accelerometers [42] and
magnetometers [3] to transducers that interrogate the external
environment for, e.g. pressure, salinity or temperature [43].
Generally, the quality of data retrieved from larger sensors
is better than smaller sensors so that, other things being
equal, we expect smaller animals to be served by lower qual-
ity sensor data. However, the exception to this is where
sensors are required to react rapidly, for example, tempera-
ture sensors [44], because larger mass sensors have greater
thermal inertia, which makes response times sluggish, a pro-
cess exacerbated when sensors have to be covered (e.g. with
resin) to protect them (cf. [45]). Users, therefore, have to
decide on the trade-off between the value of rapid against
accurate temperature measurement, something that will
depend on the heterogeneity of
the
sampling rate (see below) and precise questions being
asked. Within biologging, sensors are still remarkably small
[16], and many are combined in single chips, such as the iner-
tial measurement unit (IMU) chips used for dead-reckoning,
which have tri-axial accelerometers, tri-axial gyro meters and
tri-axial magnetic field intensity sensors and are a couple of
millimetres in external dimensions. From a sensor size per-
spective, this tempts researchers into wanting increasing
numbers of sensor types within one tag [16,46] and there is
certainly a case for aspiring to have the ‘most complete moni-
toring possible’ of the study animal. Although this would
seem to go against rigorous hypothesis-testing science [47],
even hypothesis-testing science is formed on observations
and biologgers do exactly that. But even small sensors require
current to function, and so impose a cost on size that goes
beyond their physical presence and is reflected in the battery
size or deployment duration. An important determinant of
power drain and, therefore, battery size, is the resolution at
which the sensors are required to operate. To achieve
higher resolutions, noise may make it difficult to directly
measure small changes in signal, and so it may be necessary
to oversample and average, i.e. collect more samples at a
higher rate and then average, to improve the signal-to-noise
ratio. All this assumes that biologists have unfettered choice
about their ideal resolution for their study question, even
though the ‘allowable’ questions also depend on what is
possible. A good example of this is the measurement of
depth, which has, over the last 4 decades, seen resolutions

 Downloaded from <https://royalsocietypublishing.org/> on 04 September 2025 of pressure move between 8 and 16 bit [48]. This translates
the sensor measurement range into between 256 and 65 536
steps, respectively. Thus, a depth sensor that operates over
a range of 0–500 m, for example, will have depth resolution
steps between 1.95 m and 7.6 mm, respectively. Assuming
appropriate sampling frequency, this has a profound effect
on the way results are interpreted, and even the extent to
which we are presented information with serendipitous
potential. For example, low depth resolution is the likely
reason why many studies on penguin diving dismiss dives
to less than 1–2 m [49], even though most commuting and
some feeding behaviour occurs in this range for many
species. Beyond that, as an example of high-resolution-
enhanced serendipity, the use of high-resolution depth data
indicates that porpoises Phocoena phocoena may use short,
shallow dives to help them re-oxygenate their tissues by
increasing the oxygen partial pressure difference between
their lungs and their blood (figure 1), something that is
otherwise unlikely to be considered.

swimming horizontally within the water

We have used a variety of commercial depth sensors that
specify their accuracy to be between 1 cm (Keller AG, <www>.
keller-druck.com) and 50 cm (TE Connectivity Ltd, <www.te>.
com) and so choice of which sensor to use as well as the tem-
poral and bit resolution to apply obviously affects the
‘quality’ of data recorded. The use of the most accurate
depth sensor sampled at 40 Hz has allowed us to determine,
for example, that Magellanic penguins Spheniscus magellani-
cus
column
actually oscillate in depth around 23 mm due to the beating
of their flippers which causes movement in the heave axis.
This can help inform biomechanical studies but is unlikely
to be ecologically relevant. Above all,
it is important to
choose the correct sensor for the likely quantity to be
measured, i.e. for depth, a sensor that exceeds the range of
the animal under study, but not overly so, as this will
reduce the depth resolution and will impact on the ability
to study fine movements in the water column. Similarly,
selecting the likely g-range tri-axial accelerometers is very
important as fine-scale movement at the milli-g range will
be lost when the sensor itself is scaled to ±16 g, compared
to ±2 g.

The frequency with which the sensors are interrogated
also affects power consumption as an approximately linear
function of sampling frequency and,
therefore, battery
capacity and ultimately size (figure 2). In a manner similar
to that illustrated for the porpoise above, if sampling frequen-
cies are to define particular waveforms, then data need to be
sampled at a rate at least two times the highest frequency
component in that waveform. Elephants are capable of gener-
ating infrasonic calls [51] with frequencies below 50 Hz being
possible, and lasting for several seconds [52]. In this case, an
accelerometer would need to record at twice the highest fre-
quency of an elephant’s vocalization range to detect/record
the sound [53], assuming that the ensuing vibration can be
sensed by accelerometers. In fact, by sampling acceleration
at 320 Hz on African elephants Loxodonta africana, we have
detected clear pulsed waveforms at 19 Hz, which we
assumed were due to infrasound.

(b) Memory
A key element of biologgers is that they store, rather than
transmit, data [54]. This has power and practicality

i

.

l
i
s
h
n
g
o
r
g
/
j
o
u
r
n
a
l
/
r
s
t
b

P
h

i
l
.

T
r
a
n
s
.

R

.

S
o
c
.

B

3
7
6

:

2
0
2
0
0
2
2
9

0

10

20

30

40

50

time (s)

3

r
o
y
a
l
s
o
c
i

e
t
y
p
u
b

)

m

(

h
t
p
e
d

0

0.2

0.4

0.6

0.8

1.0

1.2

1.4

Figure 1. Sequential dives by a harbour porpoise P. phocoena, with pressure
measured at 5 Hz and resolved at 16 bit, immediately following a single deep
(22 m), long (165 s) dive. The short (3–13 s), shallow (0.21–1.2 m) dives with
rapid surface periods (0.6 s) are easily discernible and may indicate how the
animal could briefly flush the lungs [50] during the surface period and then
use the water pressure to enhance the differential between lung and tissue
oxygen partial pressures to facilitate the reoxygenation process.

to the number of sensors,

transmission
advantages for many studies since signal
requires that
the device use power to transmit. In any
event, some studies require data from animals that operate
in environments where signal attenuation prohibits useful
transmission telemetry (e.g. [55]). There is also the large
quantity of data that are collected with such devices, that
would require a significant amount of power. As a partial sol-
ution to this, some hybrid devices may collect and store
internally high-frequency data, and transmit either snippets,
or summary information of the animal’s recent, notable,
behaviours. The disadvantage of biologging is, however,
that the devices have to be recovered to access the data (but
see [56]), which is almost impossible in marine species that
cannot be relocated and where telemetry signals become
essential for tag recovery. Unsurprisingly, writing sensor
data to a memory requires power, with overall power require-
ment being proportional
the
sampling frequency of those sensors and the deployment
duration. Additionally, the type of memory used is also
important. Flash memory, of which there are several types,
can be written to rapidly, but does require high peak current
for short periods of time while the data are written into the
store, with peak current reaching up to 50 mA or more.
This can have a detrimental effect on the battery itself if it
is not capable of delivering those currents and can result in
diminished overall capacity. Moreover, the ambient tempera-
ture at which the batteries are both stored and used when
deployed can more dramatically affect the resulting capacity,
with recommended operating temperatures typically within
the range −20 to +60°C. At the higher extreme, the loss of
capacity occurs along with increased internal resistance
[57], while at the lower extreme, chemical reactions slow to
such an extent that in some applications, the battery becomes
useless [58]. One of the most power-demanding memories is
the microSD Flash cards which, for a single sized package,
can have capacities from a few MB to 100s of GB. This is
more than sufficient capacity for year-long deployments on
animals with high sampling rates, provided that the animal
can carry the necessarily larger battery to interrogate the sen-
sors and power the processor (see below), in addition to
writing the data to the card. Additionally, we have found
that the longer the deployment period, the more likely the

 Downloaded from <https://royalsocietypublishing.org/> on 04 September 2025
4

r
o
y
a
l
s
o
c
i

e
t
y
p
u
b

i

.

l
i
s
h
n
g
o
r
g
/
j
o
u
r
n
a
l
/
r
s
t
b

P
h

i
l
.

T
r
a
n
s
.

R

.

S
o
c
.

B

3
7
6

:

2
0
2
0
0
2
2
9

cards are to be corrupted, making data access difficult or
impossible to recover. The precise reasons for this are unclear
because large memory microSD cards can be used in cameras
for many months without problem. However, we believe that
this is likely down to one or more scenarios, such as power
being constantly applied for several days/weeks/months,
in addition to potentially large temperature swings due to
local environmental conditions. Of the memory chips, vola-
tile RAM, or dynamic RAM (DRAM), requires the least
current, but these systems require more complex circuitry to
refresh the stored data repeatedly, which either means an
additional battery in the logger or the researcher taking a
risk by using one battery both to power the tag and safeguard
the data. Non-volatile static RAM (NVSRAM) is yet another
storage medium that is typically faster than Flash due to
not requiring data to be written back upon reading, as is
the case with DRAM. NVSRAM, however, is more costly
than Flash due to the high number of transistors required
per data bit (typically six or more) and is, therefore, generally
manufactured at lower capacity. It can be used in conjunction
with other storage media as a temporary buffer in prep-
aration for a burst-write of a more significant quantity of
data to the primary store. These days, biologgers generally
use Flash RAM for its capacity, where the data, once written,
are stored without requiring additional power.

Flash storage mechanisms generally require data to be
written into a ‘page buffer’ on the chip of a fixed size,
perhaps 256 B. Once the processor has completed the transfer,
this page of data is then copied into the main Flash storage
array. The larger the overall Flash capacity, the larger this
page capacity may be. Flash chip controllers normally allow
any number of bytes within the page to be written to, i.e. a
transfer can be any number of bytes up to the maximum
size of the page. If the processor is only buffering/transfer-
ring 256 B of sensor data, and the Flash chip has a page
size of 4096 B, then, once the 256 B have been written into
the page (of 4096 size), all 4096 B are written back into the
main Flash area. This is obviously a waste of power as 3840
extra, unused bytes are being stored back to the main array.
Note that before data can be written to Flash memory,
‘blocks’ must first be erased, whereby all bits are set to the
equivalent of a ‘1’. When writing to Flash, a ‘1’ can be set to
a ‘0’, but not the other way round. If data have been written
once, the only means of changing data in the main storage
array is to first erase blocks, which are generally larger than
a page size. Ideally, the processor’s internal memory store
should at least match that of the Flash page size or be able
to use an external buffer and stream data to the Flash page
in one storage session. If the latter, then the processor must
communicate with the external buffer simultaneously, requir-
ing separate communication lines, further complicating the
design.

sensor to the memory store. This includes fitting more data
points per ‘page’ of memory due to the reduced bit-count
per sensor. Specifically, for a data logger repeatedly request-
ing data from a sensor, possibly 40 times a second, any
reduction in bytes transferred is power saved as the
processor can return to sleep mode quicker (40 times a
second). Many operate at 3.3–5 V, while manufacturers also
offer 1.8–2.0 V varieties, allowing for significant power
savings. Lithium batteries,
either non-rechargeable or
rechargeable, having an on-load voltage of between 3.6 and
4.2 V at full charge, can be efficiently ‘chopped up’ with
some judicious dc–dc converter techniques (buck converters)
and dropped to the required 1.8–2.0 V range, almost halving
the power consumption. The same can be said for a lot of sen-
sors such as accelerometers, magnetometers, gyroscopes, etc.
that have a wide operating voltage range, from 5.0 V down to
as little as 1.8 V. Low voltage will equate to lower current
draw and, therefore, lower power usage overall as power
can be equated to voltage×current drawmean. If all com-
ponents can operate at this lower voltage then this will be
the optimal solution, while hybrid systems that use both
lower and higher voltages can coexist at the expense of a
potentially higher component count.

Ideally, processors should be active for the minimum
amount of time, sleeping where possible to minimize current
draw. Different processors have varying abilities to power
down sufficiently,
typically to nW levels, and quickly
enough to warrant the transition. The time taken to wake
the processor up and for a timing crystal or resonator to
stabilize before computations can commence is important
and can add to the energy budget. Thus, minimizing the
number of times the processor wakes up can increase effi-
typically have different
ciency significantly. Processors
‘levels’ of sleep and can power down unused internal mod-
ules/circuits to reduce overall power consumption. Some
can drop to nA current draw levels during deep-sleep
modes, but these often have a significantly longer switch-on
time. To mitigate this, many sensor chips such as acceler-
ometers, magnetometers, etc. have buffers and internal
clocking mechanisms enabling the automated timed collec-
tion and storage of multiple sensor readings. When its
buffer is full, the sensor signals the processor to wake-up
and transfer the sensor’s data buffer. This allows the pro-
cessor to minimize power, only waking to coordinate data
transfers between sensors and storage.

The clocking speed of the processor can also be very
important. Processor current draw will
increase approxi-
mately linearly with its clocking frequency, equating to the
number of instructions it can process per second. Minimizing
clock speed to reduce current draw may result in longer times
to complete data transfers, but with some protocols current
consumption may also increase.

(c) Processors
Everything costs power. Processors used in data loggers are
typically either 8 or 16 bit for the low sensor sampling
frequency (few 10s of Hz) devices. Overall, reduced bit resol-
ution and reduced sampling frequency (assuming the
biological questions being asked of
the system can be
answered with those resolutions—see above) can improve
efficiency because there is less ‘work done’ by both the
sensor and the processor in transferring data from the

(d) Logging duration and batteries
The length of time that a tag will log information depends on
the power draw of the complete system for its logging proto-
col and the battery capacity. Nominally, if a tag draws an
effective continuous current of Y mA and the battery has a
capacity of Z mA hours, the system will work for Z/Y
hours. This is a simplistic view, however, because the theore-
tical maximum capacity of the battery can be compromised if
the pulsed current exceeds the battery’s specified rating [59].

 Downloaded from <https://royalsocietypublishing.org/> on 04 September 2025 5

r
o
y
a
l
s
o
c
i

e
t
y
p
u
b

i

.

l
i
s
h
n
g
o
r
g
/
j
o
u
r
n
a
l
/
r
s
t
b

P
h

i
l
.

T
r
a
n
s
.

R

.

S
o
c
.

B

3
7
6

:

2
0
2
0
0
2
2
9

hardware

user’s choice

operating
voltage

sensor
number

sensor
size

processor and
memory size

sampling
frequency

sensor
resolution

amount of
internal
processing

frequency of
writing data
to memory

duty
cycling

power
consumption

battery
capacity

battery
size

tag size

projected
logging
duration

protection of
electronics
(housing)

Figure 2. Interaction of various parameters within animal tag construction and operation that ultimately affect tag size. (Online version in colour.)

This can also be exacerbated by low temperatures. For
example, we have found that a ‘Daily Diary’ tag [60] that
draws a mean current of 1.5 mA (with much higher peak cur-
rents), deployed on penguins swimming in 14°C water,
operates for between about 2 and 6 days even though it is
powered by a 750 mAh lithium cell (Eve EF651625), which
should last for approximately 21 days. Importantly, there is
also appreciable variation even within specified cells pro-
duced by any one manufacturer, but also variation in the
ability of the battery to provide the requisite current without
breaking down. In any event, not all batteries are created
equal and while bigger batteries in general have greater
capacity, and can withstand higher currents without breaking
down, the different battery types have different qualities. The
two most commonly used in biologgers are non-rechargeable
lithium thionyl chloride (LTC) and rechargeable lithium-ion
polymer. LTC cells have a higher energy density and so can
theoretically power devices for longer for a given volume.
This would seem to make them better for animal tags, but
that assumes that the cells are operating well within their
specified current limits. In contrast with rechargeable bat-
teries, LTC cells are, however, especially for the lower
volume devices, less able to provide higher currents, either
continuously or more importantly in pulses, and so may
not be able to power the circuit at all or only do so for a frac-
tion of the intended duration. This is particularly relevant for
GPS systems, which may draw 30 mA or more continuously
for a number of seconds to calculate every fix due to the
highly complex calculations required to triangulate the
logger’s position in three-dimensional space [59,61].

(i) Topping batteries up
Any measure that can provide power to a rechargeable bat-
tery in a tag can increase operational life or allow a tag to
have more sensors (see figure 2). Importantly, trickle-charging
can be pivotal for study success, and not just because it may
allow the unit to operate ‘indefinitely’, as is the aspiration of
many users, such as those who transmit logger data rather
than relying on tag recovery. Importantly, and perhaps more
realistically, trickle-charging it can extend the operational life

1000

100

10

)
s
y
a
d
(

e
f
i
l

l
a
n
o
i
t
a
r
e
p
o

1

0

20

40

60

80

100

% power provided by energy harvesting

Figure 3. The theoretical operational life of a 100 mAh−1 battery required to
provide a continuous current of 1 mA for a biologger while also being pro-
vided with power by an energy harvesting system. Note the nonlinear
response (the y-axis is a log scale) and how small
increases in inputted
power produce a disproportionate extension of the operational life.

of the tag disproportionately in a predetermined manner
that is analogous to the package actually having a markedly
larger battery (figure 3).

Trickle-charging is likely to become more topical, given
the diversity of miniature energy harvesting systems avail-
able today, which range from mechano-harvesters [62]
through thermo-electric generators [63] to radio-wave har-
vesters [64]. Wireless energy harvesting devices typically
comprise a coil(s)/shaped antenna with dimensions typically
designed for specific ranges of the radiofrequencies to be
absorbed, to achieve maximum power transfer. However,
the substantial attenuation of radio waves by saline environ-
ments (such as body tissues) and very reduced recovered
energy anyway compared to the mean power usage of
many data loggers storing to Flash memory makes this
power source currently impractical. Solar cells (photovoltaics—
PVs) absorb energy from the visible region of the electromag-
netic spectrum, a different range to radio waves. Because of
the wavelength of the visible spectrum, electron excitation
through photon absorption generates free electrons, which can
be stored either in a capacitor or rechargeable cell. It is surprising
that biologgers today either have no topping-up system in place

 Downloaded from <https://royalsocietypublishing.org/> on 04 September 2025

6

r
o
y
a
l
s
o
c
i

e
t
y
p
u
b

i

.

l
i
s
h
n
g
o
r
g
/
j
o
u
r
n
a
l
/
r
s
t
b

P
h

i
l
.

T
r
a
n
s
.

R

.

S
o
c
.

B

3
7
6

:

2
0
2
0
0
2
2
9

low

low

nocturnal

closed

movement vigour

% time spent moving

period active

habitat shading

high

high

diurnal

open

kinetic energy harvester

solar cell (PV) harvester

homogeneous

environmental temperature

heterogeneous

thermo-electric generator

low (remote)

radio-wave density

high (urban)

wireless energy harvester

Figure 4. Schematic diagram to show how animal behaviour and space/time use affects the viability of different energy harvesting mechanisms that might be
employed to supply power to a biologger. The dashed lines crossing the left-hand panels show illustrative examples from a pelagic shark (blue) and an urban bat
(black). (Online version in colour.)

or those that do only use solar power [65]. Which energy har-
vesting system(s) is best suited for the study animal depends
on the animal’s lifestyle (figure 4) and also, critically, on whether
the tag is implanted or external. Internal tags, especially in
homeotherms, have little choice in energy harvesters since
thermo-electric generators require a temperature difference to
create a charge, while ambient energies such as electromagnetic
radiation,
including radio waves, cannot be perceived (see
above) and so must operate with kinetic energy harvesters or
none at all.

Animal ecology and behaviour change, however, with
season,
so movement-based power harvesting systems
which might work for a migrating bird may fail post-
migration, so consideration also needs to be given to animal
habits as well as the changes in available ambient energy
(such as daylight length in solar cell systems). Finally, smart
programming can also help extend the life of tags by duty-
cycling or simply not recording data when the animal is
quiescent [66].

As tags get smaller, and batteries become an increasingly
important percentage of the overall tag volume and mass, we
predict that interest in power generating systems for biolog-
gers will increase. Smart phones will undoubtedly have a
role in catalysing this process of technological advancement,
as they have for sensors and memory.

galvanic corrosion if there are dissimilar metals at the water
interface), temperature extremes that may be below zero
and/or be as high as 50°C, pressures as high as 200 bar
[69] and have sensors that can be rapidly challenged by bio-
fouling [70]. Sensors and data access ports that have to
interact with the environment can, therefore, be problematic,
not least because, even if the device is potted in resin, there is
a line of weakness between them and the resin. This can lead
to hairline cracks if the environment has large temperature
fluctuations and there is differential
thermal expansion
between resin and them. Such large temperature fluctuations
are prevalent in temperate penguins where, for example, in
Magellanic penguins S. magellanicus, the temperature of the
outside surface of the tag may range between 11 and 35°C
with every dive cycle due to cold water and high insolation.
Almost all marine tags that have to operate at depths exceed-
ing 100 m are potted in resin, although at lesser depths, some
companies use O-rings and air-filled systems. Any air in a tag
(even as bubbles in resin) creates a weak spot since the
pressure on it to compress ( potentially causing cracks in the
housing) goes up linearly with depth: at the surface, atmos-
−2, but this goes up to
pheric pressure is about 68.8 kg m
−2
1.13 × 105 kg m
at 1 km. Thus,
deep-diving animals is critical.

−2 at 100 m depth, and 1.04 × 106 kg m

the design and construction of

tags for

(e) Tag construction
Biologgers have to work in a diverse range of environments.
The most accommodating are perhaps when they are
implanted into the gentle, relatively stable insides of animals
[67], although even there they may be subject to substantial
changing pressure [68]. This contrasts to externally mounted
options where the tags may have to operate in corrosive and
in
conductive seawater environments (which can result

(f ) Data recovery
Transmission of data is energetically costly but then so is
recovery of the whole tag, especially if it is implanted.
Today, a great many biologgers have to be recovered to
acquire the data, a process which ranges from the trivial to
extremely onerous [5]. In larger animals that can carry
larger tags, a VHF or Argos location transmitter may be
in tag recovery success [15]. Data transmission,
essential

 Downloaded from <https://royalsocietypublishing.org/> on 04 September 2025 7

r
o
y
a
l
s
o
c
i

e
t
y
p
u
b

i

.

l
i
s
h
n
g
o
r
g
/
j
o
u
r
n
a
l
/
r
s
t
b

P
h

i
l
.

T
r
a
n
s
.

R

.

S
o
c
.

B

3
7
6

:

2
0
2
0
0
2
2
9

where it can occur (because, for example, salt water does not
allow the passage of radio waves), generally uses VHF sys-
tems (e.g. [71]), which is only viable for externally mounted
tags. Transmission requires a link between the tag and a
receiver that lasts long enough for a respectable amount of
data to be transferred, and it requires that the tag have
enough extra power to transmit. For both these reasons,
most biologgers transmitting data cannot transmit continu-
ous data recorded at high rates. Rather, they provide, for
example, 3 s bursts of data for every minute of operation,
which allows a reasonable snapshot of the animal’s biology
[72] while accepting the holes in information that this entails.
Ultimately,
this approach depends on the
questions being asked.

the utility of

(g) Software
(i) Tag programming
A logger with fixed logging frequency and sensor options
will have a known power requirement and a reasonably
well-defined projected run time. Against this, having smart
logging protocols has a great potential for biologists to save
power while acquiring the most useful data for their ques-
tions. For example, not powering up all sensors saves
power, it gives the processor less data to collect, and sub-
sequently less data to store, and so the primary data
storage can be accessed less frequently. Additionally, not all
sensors need to be sampled at the same frequency. For
instance, acceleration might have sensors sampled at the
highest frequency to enhance behaviour classification [73],
while magnetometry may often be sampled at lower rates
as it primarily provides heading metrics (e.g. [74]) and can
easily be interpolated, while temperature measurements, for
example, will likely have an inherent lag due to sensor encap-
sulation [44] so high-frequency measurements would be of
little benefit. Overly complex programming options have
the disadvantage of increasing the chances that the biologist
in the field may make a mistake, something that is not trivial,
given the difficulties of putting tags on animals in the
first place.

(ii) Quick inspection of tag data in the field
Many tag deployments are made after careful preparation in
the laboratory and are ‘single shot’ events. Equally, many
studies deploy tags repeatedly over time in the field, with
researchers having to make tag-programming decisions
based on the data they receive from deployments over
time. This calls for proper inspection of recovered tag data
to inform the next protocols. There is often poor appreci-
ation of the importance of data inspection under such
conditions. At its most base level, workers need to ascertain
the correct functioning of all the sensors—without outliers
and operating within the prescribed range—before re-
deployment. This requires that software be available in the
field to allow the workers to inspect all of their recorded
parameters as a function of time. Sadly, many do not do
this, and may return from expeditions with poor, or no,
data, which is a waste of time and resources and has impor-
tant
tag
manufacturers should provide such software, even if it is
primitive, showing little more than sensor outputs over
this may have
Indeed, provision of
time graphically.
changed field studies considerably.

[75]. We believe

implications

ethical

that

4. Common mistakes in data interpretation
Linked to the above point is more comprehensive under-
standing of sensor metrics, either direct or derived. The
vast array of machine-learning programmes [76] makes it
easy to collect data and, with little more than cursory inspec-
tion, analyse it within a programming ‘black box’. No
biologist would take the mass of an animal without
understanding what it means, but many today using accel-
erometry metrics, for example, are unclear what the values
presented mean. This is particularly important when the be-
haviour-identifying programme relies on ‘validated’ data
from an animal observed to behave in a particular manner
while wearing a tag [77]. For instance, a study species ‘vali-
dated’
terrain will produce markedly different
acceleration offsets if it normally lives in mountains because
body pitch (manifest through the surge static acceleration
values (cf. [73]) is rarely around zero. Similarly, proper under-
standing of the meaning of sensor data will help workers
identify behaviours that are not observed in captivity and,
therefore, cannot be ‘validated’ in the conventional sense.
Some simple code can easily be constructed using either R
or MatLab to allow the worker to visualize sample data
while in the field and some tag manufacturers provide soft-
ware that does this. There are numerous R packages
available for deconstructing animal logger data, including
using Boolean approaches for defining data [78], and visua-
lizing this in two or more dimensions, including overlaying
movement paths onto textured mapping technologies.

in level

5. Conclusion
Although current biologgers are incredibly potent with
respect to the information that they can gather, and thereby
in their capacity to elucidate the behaviour, ecology and
physiology of the study species, poor understanding of tag
capacities and limitations can lead to misinterpretation.
Basic knowledge of tag design and mode of operation,
including issues such as resolution, sampling rate and
power draw, should not be the province of the tag engineer
alone. Indeed, proper understanding of such matters by
scientists would, at once, ensure that the data taken rep-
resent what
they are supposed to, and reduce the
likelihood that the tag will underperform. Beyond this, the
most comprehensive data on aspects of an animal’s biology
may be of little value if the tag itself causes aberrations in
animal biology. We, therefore, need to be particularly vigi-
lant with respect to potential tag detriment, understanding
that good science and the wellbeing of the animals that
carry the tags both depend on biological and engineering
expertise operating together.

Data accessibility. This article has no additional data.
Authors’ contributions. M.D.H.: conception or design of the work; drafting
the article; critical revision of the article throughout; final approval of
the version. R.P.W.: conception or design of the work; drafting the
article; critical revision of the article throughout; final approval of
the version. J.T.: critical revision of the article throughout; final
approval of the version. U.S.: critical revision of the article throughout;
final approval of the version.
Competing interests. We declare we have no competing interests.
Funding. This research contributes to the CAASE project funded by
King Abdullah University of Science and Technology (KAUST)
under the KAUST Sensor Initiative.

 Downloaded from <https://royalsocietypublishing.org/> on 04 September 2025 References

1.

Hebblewhite M, Haydon DT. 2010 Distinguishing
technology from biology: a critical review of the use
of GPS telemetry data in ecology. Phil. Trans. R. Soc.
B 365, 2303–2312. (doi:10.1098/rstb.2010.0087)
Brown DD, Kays R, Wikelski M, Wilson R, Klimley AP.
2013 Observing the unwatchable through
acceleration logging of animal behavior. Anim.
Biotelemetry 1, 20. (doi:10.1186/2050-3385-1-20)
3. Williams HJ et al. 2017 Identification of animal

2.

4.

movement patterns using tri-axial magnetometry.
Mov. Ecol. 5, 6. (doi:10.1186/s40462-017-0097-x)
Godyń D, Herbut P, Angrecka S. 2019 Measurements
of peripheral and deep body temperature in
cattle—a review. J. Therm. Biol. 79, 42–49.
(doi:10.1016/j.jtherbio.2018.11.011)

5. Williams H, Shepard E, Holton MD, Alarcón P,

Wilson R, Lambertucci S. 2020 Physical limits of
flight performance in the heaviest soaring bird.
Proc. Natl Acad. Sci. USA 117, 17 884–17 890.
(doi:10.1073/pnas.1907360117)
Green JA. 2011 The heart rate method for
estimating metabolic rate: review and
recommendations. Comp. Biochem. Physiol. A 158,
287–304. (doi:10.1016/j.cbpa.2010.09.011)
Bridge ES, Kelly JF, Contina A, Gabrielson RM,
MacCurdy RB, Winkler DW. 2013 Advances in
tracking small migratory birds: a technical review of
light-level geolocation. J. Field Ornithol. 84,
121–137. (doi:10.1111/jofo.12011)
Teilmann J, Agersted MD, Heide-Jørgensen MP.
2020 A comparison of CTD satellite-linked tags for
large cetaceans—bowhead whales as real-time
autonomous sampling platforms. Deep Sea Res. Part I
157, 103213. (doi:10.1016/j.dsr.2020.103213)
Block BA. 2005 Physiological ecology in the 21st
century: advancements in biologging science.
Integr. Comp. Biol. 45, 305–320. (doi:10.1093/icb/
45.2.305)

6.

7.

8.

9.

10. Bishop CM et al. 2015 The roller coaster flight
strategy of bar-headed geese conserves energy
during Himalayan migrations. Science 347,
250–254. (doi:10.1126/science.1258732)

11. Meir JU, York JM, Chua BA, Jardine W, Hawkes LA,

23.

Milsom WK. 2019 Reduced metabolism supports
hypoxic flight in the high-flying bar-headed goose
(Anser indicus). eLife 8, e44986. (doi:10.7554/eLife.
44986)

12. Block BA et al. 2001 Migratory movements, depth
preferences, and thermal biology of Atlantic bluefin
tuna. Science 293, 1310–1314. (doi:10.1126/
science.1061197)
Toledo S, Shohami D, Schiffner I, Lourie E, Orchan Y,
Bartan Y, Nathan R. 2020 Cognitive map-based
navigation in wild bats revealed by a new high-
throughput tracking system. Science 369, 188–193.
(doi:10.1126/science.aax6904)

13.

14. Bograd SJ, Block BA, Costa DP, Godley BJ. 2010

Biologging technologies: new tools for conservation.
Endanger. Species Res. 10, 1–7. (doi:10.3354/
esr00269)

27. Bodey TW, Cleasby IR, Bell F, Parr N, Schultz A,

Votier SC, Bearhop S. 2018 A phylogenetically
controlled meta-analysis of biologging device
effects on birds: deleterious effects and a call for
more standardized reporting of study data. Methods
Ecol. Evol. 9, 946–955. (doi:10.1111/2041-210X.
12934)

28. Hawkins P. 2004 Bio-logging and animal welfare:
practical refinements. Mem. Natl Inst. Polar Res. 58,
58–68.

29. Vandenabeele SP, Grundy E, Friswell MI, Grogan A,
Votier SC, Wilson RP. 2014 Excess baggage for birds:
inappropriate placement of tags on gannets
changes flight patterns. PLoS ONE 9, e92657.
(doi:10.1371/journal.pone.0092657)

30. Gillies N et al. 2020 Short-term behavioural impact

contrasts with long-term fitness consequences of
biologging in a long-lived seabird. Sci. Rep. 10,
1–10. (doi:10.1038/s41598-020-72199-w)

31. Rasiulis AL, Festa-Bianchet M, Couturier S, Côté SD.
2014 The effect of radio-collar weight on survival of
migratory caribou. J. Wildl. Manag. 78, 953–956.
(doi:10.1002/jwmg.722)

32. McCafferty DJ, Currie J, Sparling CE. 2007 The effect

8

r
o
y
a
l
s
o
c
i

e
t
y
p
u
b

i

.

l
i
s
h
n
g
o
r
g
/
j
o
u
r
n
a
l
/
r
s
t
b

P
h

i
l
.

T
r
a
n
s
.

R

.

S
o
c
.

B

3
7
6

:

2
0
2
0
0
2
2
9

15. Mikkelsen L, Johnson M, Wisniewska DM, van Neer
A, Siebert U, Madsen PT, Teilmann J. 2019 Long-
term sound and movement recording tags to study
natural behavior and reaction to ship noise of seals.
Ecol. Evol. 9, 2588–2601. (doi:10.1002/ece3.4923)
Johnson MP, Tyack PL. 2003 A digital acoustic
recording tag for measuring the response of wild
marine mammals to sound. IEEE J. Oceanic Eng. 28,
3–12. (doi:10.1109/JOE.2002.808212)

16.

17. Nielsen NH, Teilmann J, Sveegaard S, Hansen RG,
Sinding M-HS, Dietz R, Heide-Jørgensen MP. 2018
Oceanic movements, site fidelity and deep diving in
harbour porpoises from Greenland show limited
similarities to animals from the North Sea. Mar.
Ecol. Prog. Ser. 597, 259–272. (doi:10.3354/
meps12588)
Stidsholt L, Johnson M, Beedholm K, Jakobsen L,
Kugler K, Brinkløv S, Salles A, Moss CF, Madsen PT.
2019 A 2.6-g sound and movement tag for studying
the acoustic scene and kinematics of echolocating
bats. Methods Ecol. Evol. 10, 48–58. (doi:10.1111/
2041-210X.13108)

18.

19. DeRuiter SL, Langrock R, Skirbutas T, Goldbogen JA,
Chalambokidis J, Friedlaender AS, Southall BL. 2016
A multivariate mixed hidden Markov model to
analyze blue whale diving behaviour during
controlled sound exposures. arXiv preprint.
(doi:10.1038/arXiv:1602.06570)

20. Abrahms B et al. 2019 Memory and resource

of instrument attachment on the surface
temperature of juvenile grey seals (Halichoerus
grypus) as measured by infrared thermography.
Deep Sea Res. Part II 54, 424–436. (doi:10.1016/j.
dsr2.2006.11.019)
Kay WP et al. 2019 Minimizing the impact of
biologging devices: using computational fluid
dynamics for optimizing tag design and positioning.
Methods Ecol. Evol. 10, 1222–1233. (doi:10.1111/
2041-210X.13216)

35.

34. Wilson RP, Spairani HJ, Coria NR, Culik BM, Adelung
D. 1990 Packages for attachment to seabirds: what
color do Adelie penguins dislike least? J. Wildl.
Manag. 54, 447–451. (doi:10.2307/3809657)
Jones TT et al. 2011 Determining transmitter drag and
best-practice attachment procedures for sea turtle
biotelemetry. National Oceanographic and Atmospheric
Administration Technical Memorandum 480, https://
repository.library.noaa.gov/view/noaa/4512.

36. Bannasch R, Wilson RP, Culik B. 1994 Hydrodynamic
aspects of design and attachment of a back-
mounted device in penguins. J. Exp. Biol. 194,
83–96. (doi:10.1242/jeb.194.1.83)

37. Whitford M, Klimley AP. 2019 An overview of

38.

behavioral, physiological, and environmental
sensors used in animal biotelemetry and biologging
studies. Anim. Biotelemetry 7, 1–24. (doi:10.1186/
s40317-019-0189-z)
Clark TD, Sandblom E, Hinch S, Patterson D, Frappell
P, Farrell A. 2010 Simultaneous biologging of heart
rate and acceleration, and their relationships with
energy expenditure in free-swimming sockeye
salmon (Oncorhynchus nerka). J. Comp. Physiol. B
180, 673–684. (doi:10.1007/s00360-009-0442-5)
39. Williams TM, Blackwell SB, Richter B, Sinding M-HS,
Heide-Jørgensen MP. 2017 Paradoxical escape

tracking drive blue whale migrations. Proc. Natl
Acad. Sci. USA 116, 5582–5587. (doi:10.1073/pnas.
1819031116)

33.

21. Ripperger SP et al. 2020 Thinking small: next-

22.

24.

25.

generation sensor networks close the size gap in
vertebrate biologging. PLoS Biol. 18, e3000655.
(doi:10.1371/journal.pbio.3000655)
Pennycuick C, Fast PL, Ballerstädt N, Rattenborg N.
2012 The effect of an external transmitter on the
drag coefficient of a bird’s body, and hence on
migration range, and energy reserves after
migration. J. Ornithol. 153, 633–644. (doi:10.1007/
s10336-011-0781-3)
Saraux C et al. 2011 Reliability of flipper-banded
penguins as indicators of climate change. Nature
469, 203–206. (doi:10.1038/nature09630)
Portugal SJ, White CR. 2018 Miniaturization of
biologgers is not alleviating the 5% rule. Methods
Ecol. Evol. 9, 1662–1666. (doi:10.1111/2041-210X.
13013)
Stanton NA, Salmon P, Harris D, Marshall A,
Demagalski J, Young MS, Waldmann T, Dekker S.
2009 Predicting pilot error: testing a new
methodology and a multi-methods and analysts
approach. Appl. Ergon. 40, 464–471. (doi:10.1016/j.
apergo.2008.10.005)

26. White CR, Cassey P, Schimpf NG, Halsey LG, Green
JA, Portugal SJ. 2013 Implantation reduces the
negative effects of bio-logging devices on birds.
J. Exp. Biol. 216, 537–542. (doi:10.1242/jeb.

076554)

 Downloaded from <https://royalsocietypublishing.org/> on 04 September 2025 9

r
o
y
a
l
s
o
c
i

e
t
y
p
u
b

i

.

l
i
s
h
n
g
o
r
g
/
j
o
u
r
n
a
l
/
r
s
t
b

P
h

i
l
.

T
r
a
n
s
.

R

.

S
o
c
.

B

3
7
6

:

2
0
2
0
0
2
2
9

40.

responses by narwhals (Monodon monoceros).
Science 358, 1328–1331. (doi:10.1126/science.
aao2740)
Thouzeau C, Peters G, Le Bohec C, Le Maho Y. 2004
Adjustments of gastric pH, motility and temperature
during long-term preservation of stomach contents
in free-ranging incubating king penguins. J. Exp.
Biol. 207, 2715–2724. (doi:10.1242/jeb.01074)
41. Wilson RP, Simeone A, Luna-Jorquera G, Steinfurth
A, Jackson S, Fahlman A. 2003 Patterns of
respiration in diving penguins: is the last gasp an
inspired tactic? J. Exp. Biol. 206, 1751–1763.
(doi:10.1242/jeb.00341)
Yoda K, Sato K, Niizuma Y, Kurita M, Bost C, Le Maho
Y, Naito Y. 1999 Precise monitoring of porpoising
behaviour of Adelie penguins determined using
acceleration data loggers. J. Exp. Biol. 202,
3121–3126. (doi:10.1242/jeb.202.22.3121)

42.

43. Wilmers CC, Nickel B, Bryce CM, Smith JA, Wheat
RE, Yovovich V. 2015 The golden age of bio-logging:
how animal-borne sensors are advancing the
frontiers of ecology. Ecology 96, 1741–1753.
(doi:10.1890/14-1401.1)

44. Wilson RP et al. 2002 Remote-sensing systems and
seabirds: their use, abuse and potential for
measuring marine environmental variables. Mar.
Ecol. Prog. Ser. 228, 241–261. (doi:10.3354/
meps228241)

45. Weimerskirch H, Wilson RP, Guinet C, Koudil M.
1995 Use of seabirds to monitor sea-surface
temperatures and to validate satellite remote-
sensing measurements in the Southern Ocean. Mar.
Ecol. Prog. Ser. 126, 299–303. (doi:10.3354/
meps126299)

46. Ropert-Coudert Y, Wilson RP. 2005 Trends and
perspectives in animal-attached remote sensing.
Front. Ecol. Environ. 3, 437–444. (doi:10.1890/1540-
9295(2005)003[0437:TAPIAR]2.0.CO;2)
Popper K. 1978 The myth of inductive hypothesis
generation. Conjectures and refutations. London, UK:
Routledge & Kegan Paul.

47.

49.

48. Wilson RP, Culik BM, Bannash R, Driesen H. 1992
Monitoring penguins at sea using data loggers. In
Proc. Biotelemetry XII, 31 August–5 September,
Ancona, Italy, pp. 205–214.
Sutton G, Pichegru L, Botha JA, Kouzani AZ, Adams
S, Bost CA, Arnould JP. 2020 Multi-predator
assemblages, dive type, bathymetry and sex
influence foraging success and efficiency in African
penguins. PeerJ 8, e9380. (doi:10.7717/peerj.9380)
Kooyman GL, Cornell LH. 1981 Physiological zoology.
Chicago, IL: University of Chicago Press.

50.

51. Herbst CT, Stoeger AS, Frey R, Lohscheller J, Titze IR,
Gumpenberger M, Fitch WT. 2012 How low can you
go? Physical production mechanism of elephant
infrasonic vocalizations. Science 337, 595–599.
(doi:10.1126/science.1219712)

52. Günther RH, O’Connell-Rodwell CE, Klemperer SL.
2004 Seismic waves from elephant vocalizations: a

possible communication mode? Geophys. Res. Lett.
31, L11602. (doi:10.1029/2004GL019671)

53. Hedlin MA, Walker KT. 2013 A study of infrasonic
anisotropy and multipathing in the atmosphere
using seismic networks. Phil. Trans. R. Soc. A 371,
20110542. (doi:10.1098/rsta.2011.0542)

54. Naito Y. 2004 New steps in bio-logging science.

Mem. Natl Inst. Polar Res. 58, 50–57.

56.

55. Andrzejaczek S, Gleiss AC, Lear KO, Pattiaratchi CB,
Chapple TK, Meekan MG. 2019 Biologging tags
reveal links between fine-scale horizontal and
vertical movement behaviors in tiger sharks
(Galeocerdo cuvier). Front. Mar. Sci. 6, 229. (doi:10.
3389/fmars.2019.00229)
Flack A, Nagy M, Fiedler W, Couzin ID, Wikelski M.
2018 From local collective behavior to global
migratory patterns in white storks. Science 360,
911–914. (doi:10.1126/science.aap7781)
57. Ning G, Haran B, Popov BN. 2003 Capacity fade
study of lithium-ion batteries cycled at high
discharge rates. J. Power Sources 117, 160–169.
(doi:10.1016/S0378-7753(03)00029-6)

59.

58. Belt JR, Ho CD, Motloch CG, Miller TJ, Duong TQ.
2003 A capacity and power fade study of Li-ion cells
during life cycle testing. J. Power Sources 123,
241–246. (doi:10.1016/S0378-7753(03)00537-8)
Savoye F, Venet P, Millet M, Groot J. 2011 Impact of
periodic current pulses on Li-ion battery
performance. IEEE Trans. Ind. Electron. 59,
3481–3488. (doi:10.1109/TIE.2011.2172172)
60. Wilson RP, Shepard E, Liebsch N. 2008 Prying into
the intimate details of animal lives: use of a daily
diary on animals. Endanger. Species Res. 4,
123–137. (doi:10.3354/esr00064)
El-naggar AM. 2012 New method of GPS orbit
determination from GCPS network for the purpose
of DOP calculations. Alexandria Eng. J. 51, 129–136.
(doi:10.1016/j.aej.2012.06.002)

61.

64.

63.

62. Niroomand M, Foroughi HR. 2016 A rotary
electromagnetic microgenerator for energy
harvesting from human motions. J. Appl. Res.
Technol. 14, 259–267. (doi:10.1016/j.jart.2016.
06.002)
Lund A, Tian Y, Darabi S, Müller C. 2020 A polymer-
based textile thermoelectric generator for wearable
energy harvesting. J. Power Sources 480, 228836.
(doi:10.1016/j.jpowsour.2020.228836)
Song C, Huang Y, Zhou J, Carter P, Yuan S, Xu Q, Fei
Z. 2016 Matching network elimination in broadband
rectennas for high-efficiency wireless power transfer
and energy harvesting. IEEE Trans. Ind. Electron. 64,
3950–3961. (doi:10.1109/TIE.2016.2645505)
Saha CR, Huda MN, Mumtaz A, Debnath A, Thomas
S, Jinks R. 2020 Photovoltaic (PV) and thermo-
electric energy harvesters for charging applications.
Microelectron. J. 96, 104685. (doi:10.1016/j.mejo.
2019.104685)
Korpela JM, Suzuki H, Matsumoto S, Mizutani Y,
Samejima M, Maekawa T, Nakai J, Yoda K.

65.

66.

2019 AI on animals: AI-assisted animal-borne
logger never misses the moments that
biologists want. bioRxiv 630053. (doi:10.1038/
bioRxiv:630053)

67. Grémillet D, Kuntz G, Gilbert C, Woakes AJ, Butler
PJ, Yl M. 2005 Cormorants dive through the Polar
night. Biol. Lett. 1, 469–471. (doi:10.1098/rsbl.
2005.0356)

68. Green J, Butler P, Woakes A, Boyd I. 2003 Energetics
of diving in macaroni penguins. J. Exp. Biol. 206,
43–57. (doi:10.1242/jeb.00059)
Tyack PL, Johnson M, Soto NA, Sturlese A,
Madsen PT. 2006 Extreme diving of beaked whales.
J. Exp. Biol. 209, 4238–4253. (doi:10.1242/
jeb.02505)

69.

70. Hammerschlag N, Cooke SJ, Gallagher AJ, Godley BJ.
2014 Considering the fate of electronic tags:
interactions with stakeholders and user
responsibility when encountering tagged aquatic
animals. Methods Ecol. Evol. 5, 1147–1153. (doi:10.
1111/2041-210X.12248)

71. Rock P, Camphuysen C, Shamoun-Baranes J, Ross-
Smith VH, Vaughan IP. 2016 Results from the first
GPS tracking of roof-nesting herring gulls Larus
argentatus in the UK. Ringing Migr. 31, 47–62.
(doi:10.1080/03078698.2016.1197698)

72. Mayer M, Fog Bjerre DH, Sunde P. 2020 Better safe

73.

than sorry: the response to a simulated predator
and unfamiliar scent by the European hare.
Ethology 126, 704–715. (doi:10.1111/eth.13019)
Shepard EL et al. 2008 Identification of animal
movement patterns using tri-axial accelerometry.
Endanger. Species Res. 10, 47–60. (doi:10.3354/
esr00084)

74. Walker JS et al. 2015 Prying into the intimate

secrets of animal lives; software beyond hardware for
comprehensive annotation in ‘Daily Diary’ tags. Mov.
Ecol. 3, 1–16. (doi:10.1186/s40462-015-0056-3)
75. Bidder O, Arandjelović O, Almutairi F, Shepard E,
Lambertucci SA, Qasem L, Wilson R. 2014 A risky
business or a safe BET? A Fuzzy Set Event Tree for
estimating hazard in biotelemetry studies. Anim.
Behav. 93, 143–150. (doi:10.1016/j.anbehav.2014.
04.025)

77.

76. Valletta JJ, Torney C, Kings M, Thornton A, Madden
J. 2017 Applications of machine learning in animal
behaviour studies. Anim. Behav. 124, 203–220.
(doi:10.1016/j.anbehav.2016.12.005)
Campbell HA, Gao L, Bidder OR, Hunter J, Franklin
CE. 2013 Creating a behavioural classification
module for acceleration data: using a captive
surrogate for difficult to observe species.
J. Exp. Biol. 216, 4501–4506. (doi:10.1242/jeb.

089805)

78. Wilson RP et al. 2018 Give the machine a hand:
a Boolean time-based decision-tree template for
rapidly finding animal behaviours in
multisensor data. Methods Ecol. Evol. 9, 2206–2215.
(doi:10.1111/2041-210X.13069)

 Downloaded from <https://royalsocietypublishing.org/> on 04 September 2025
