Received: 1 April 2018  |  Accepted: 28 February 2019
DOI: 10.1111/2041-210X.13172

R E S E A R C H   A R T I C L E

A novel biomechanical approach for animal behaviour
recognition using accelerometers

Pritish Chakravarty1  |   Gabriele Cozzi2,3  |   Arpat Ozgul2,3  |   Kamiar Aminian1

1Interfaculty Institute of Bioengineering
(IBI-STI), Ecole Polytechnique Fédérale de
Lausanne, Lausanne, Switzerland

2Institute of Evolutionary Biology and
Environmental Studies, University of Zurich,
Zurich, Switzerland

3Kalahari Research Centre, Kuruman River
Reserve, Van Zylsrus, South Africa

Correspondence
Pritish Chakravarty
Email: <pritish.chakravarty@epfl.ch>

Handling Editor: Robert B. O’Hara

Abstract

1. Data from animal-borne inertial sensors are widely used to investigate several as-

pects of an animal's life, such as energy expenditure, daily activity patterns and be-

haviour. Accelerometer data used in conjunction with machine learning algorithms

have been the tool of choice for characterising animal behaviour. Although machine

learning models perform reasonably well, they may not rely on meaningful features,

nor lend themselves to physical interpretation of the classification rules. This lack of

interpretability  and  control  over  classification  outcomes  is  of  particular  concern

where different behaviours have different frequency of occurrence and duration, as

in  most  natural  systems,  and  calls  for  the  development  of  alternative  methods.

Biomechanical  approaches  to  human  activity  classification  could  overcome  these

shortcomings, yet their full potential remains untapped for animal studies.

2. We  propose  a  general  framework  for  behaviour  recognition  using  accelerometers,

and develop a hybrid model where (a) biomechanical features characterise movement

dynamics, and (b) a node-based hierarchical classification scheme employs simple ma-

chine learning algorithms at each node to find feature-value thresholds separating

different behaviours. Using triaxial accelerometer data collected on 10 wild Kalahari

meerkats, and annotated video recordings of each individual as groundtruth, this hy-

brid  model  was  validated  in  three  scenarios:  (a)  when  each  behaviour  was  equally

represented  (EQDIST),  (b)  when  naturally  imbalanced  datasets  were  considered

(STRAT) and (c) when data from new individuals were considered (LOIO).

3. A linear-kernel Support Vector Machine at each node of our classification scheme

yielded an overall accuracy of >95% for each scenario. Our hybrid approach had a

2.7% better average overall accuracy than top-performing classical machine learning

approaches. Further, we showed that not all models with high overall accuracy re-

turned  accurate  behaviour-specific  performance,  and  good  performance  during

EQDIST did not always generalise to STRAT and LOIO.

4. Our hybrid model took advantage of robust machine learning algorithms for auto-

matically estimating decision boundaries between behavioural classes. This not only

achieved high classification performance but also permitted biomechanical interpre-

tation  of  classification  outcomes.  The  framework  presented  here  provides  the

This is an open access article under the terms of the Creative Commons Attribution-NonCommercial License, which permits use, distribution and reproduction
in any medium, provided the original work is properly cited and is not used for commercial purposes.
© 2019 The Authors. Methods in Ecology and Evolution published by John Wiley & Sons Ltd on behalf of British Ecological Society
802  |  wileyonlinelibrary.com/journal/mee3

Methods Ecol Evol. 2019;10:802–814.

Methods in Ecology and Evolu(cid:13)on

    |  803

flexibility to adapt models to required levels of behavioural resolution, and has the

potential to facilitate meaningful model sharing between studies.

K E Y W O R D S

accelerometer, animal behaviour recognition, biomechanics, machine learning, meerkat,

movement intensity, movement periodicity, posture

1 |  INTRODUC TION

obtained  even  when  the  recognition  accuracy  of  under- represented

behaviours is poor (He & Garcia, 2009); the issue of imbalanced classes

An in- depth understanding of wild animal behaviour and movement

has even been called a ‘curse’ in machine learning literature (Lemaitre,

has assumed prime importance in recent years in light of an urgent

Nogueira, & Aridas, 2017). This occurs because machine learning algo-

need to augment our forecasting, conservation and management ca-

rithms typically seek to minimise the overall misclassification rate, and

pacities in the face of rapid environmental change. Since gathering

thus tend to optimise for the most frequent behaviours since they con-

data on wild animals in their natural habitats is often precluded by lo-

tribute  most  to  the  overall  accuracy—the  classification  performance

gistical difficulty, animal- borne sensor systems that offer the possi-

of rare behaviours may nevertheless remain poor. Examination of the

bility of continuously and remotely recording data as the animal goes

classification rules would help understand how to improve the recog-

about its daily life have been developed (Ropert- Coudert & Wilson,

nition of rarer behaviours. However, the use of many features, which

2005). Over the two decades since their first application to remote

is typical with machine learning approaches (>15: Nathan et al., 2012;

monitoring of animal behaviour (e.g. Sellers, Varley, & Waters, 1998),

Resheff et al., 2014; Wang et al., 2015), implies that the resulting clas-

animal- borne  accelerometers  have  been  employed  to  gain  insights

sification rules are a function of that many variables, and deciphering

into  the  life  histories  of  species  as  far  apart  in  size,  type  of  habi-

these  high- dimensional  complex  rules  and  pinpointing  the  reasons

tat,  speed  and  mode  of  locomotion  as  chipmunks  (Tamias  alpinus)

behind  misclassification  of  under- represented  (rarer)  but  important

(Hammond,  Springthorpe,  Walsh,  &  Berg- Kirkpatrick,  2016),  seals

behaviours quickly becomes intractable.

(Leptonychotes weddellii) (Naito, Bornemann, Takahashi, McIntyre, &

Confining  the  role  of  machine  learning  algorithms  to  threshold-

Plötz, 2010), African wild dogs (Lycaon pictus) and cheetahs (Acinonyx

finding  within  a  classification  scheme  predefined  on  the  basis  of

jubatus)  (Cozzi  et al.,  2012),  vultures  (Gyps  fulvus)  (Nathan  et al.,

biomechanical  knowledge  of  animal  movement  dynamics,  and  using

2012) and  blue  whales  (Balaenoptera  musculus)  (Goldbogen  et al.,

biomechanically  significant  movement  descriptors  (features)  within

2011). To keep pace with the increasing ubiquity of accelerometry,

the  scheme,  may  help  solve  these  difficulties.  Such  an  approach  is

developing methods applicable across species has become essential.

made possible by the fact that there are certain natural commonalities

For  instance,  general  methods  have  been  developed  to  infer  ani-

in  the  movement  biomechanics  of  any  animal:  different  behaviours

mal  energy  expenditure  from  recorded  acceleration  (Wilson  et al.,

may be carried out more or less intensely, in characteristic postures,

2006).  However,  despite  progress  in  recognising  animal  behaviour

erratically or in a periodic manner. Even though the actual names for

from recorded acceleration, there is as yet no single technique that

different animal behaviours will depend on the environment and ani-

combines  under  one  framework  the  virtues  of  easy- to- implement

mal's context, broad behavioural categories will still lend themselves

machine learning on the one hand, and the interpretability and ro-

to description through the biomechanical principles of intensity, pos-

bustness of biomechanically defined classification rules on the other.

ture and periodicity.

Machine  learning,  often  rather  unenviably  referred  to  as  a  black

Several studies have employed biomechanical considerations to

box  (e.g.  McClune  et al.,  2014),  has  been  widely  employed  to  infer

characterise behaviours central to an animal's life, such as foraging,

animal  behaviour  from  raw  acceleration  data  (Nathan  et al.,  2012;

locomotion and resting (e.g. Shepard et al. 2008); in these studies,

Grünewälder  et al.,  2012;  Gao,  Campbell,  Bidder,  &  Hunter,  2013;

a  majority  of  the  acceleration- derived  metrics  used  for  behaviour

Bidder  et al.,  2014;  Resheff,  Rotics,  Harel,  Spiegel,  &  Nathan,  2014;

recognition were aimed at quantifying the three biomechanical prin-

Wang  et al.,  2015).  Despite  the  power  and  ease  of  use  of  machine

ciples of intensity, posture and periodicity. For instance, one study

learning approaches, the need to develop behaviour recognition tools

that categorised acceleration data in Adélie penguins (Pygoscelis ade-

generalisable  across  species  has  brought  to  light  the  importance  of

liae) (Yoda et al., 2001) considered the division of behavioural classes

being able to physically interpret classification rules, even at the cost

into  static  and  dynamic  categories,  discriminated  between  static

of  small  gains  in  classification  accuracy  (Nathan  et al.,  2012).  Model

behaviours  based  on  posture  and  identified  locomotion  as  being

interpretability  becomes  particularly  significant  when  accurately

periodic. The use of periodicity metrics may help tease apart even

recognising  relatively  rarer  behaviours  is  important.  When  machine

highly  context- ,  environment-   and  mode- of- locomotion- dependent

learning approaches are applied to datasets that are heavily skewed

behaviours  such  as  locomotion  and  foraging.  For  instance,  peri-

in  the  frequency  and  duration  of  different  behaviours  (Watanabe,

odicity  metrics  have  since  been  used  to  characterise  locomotor

Izawa, Kato, Ropert- Coudert, & Naito, 2005; Grünewälder et al., 2012;

movement across avian (Laich, Wilson, Quintana, & Shepard, 2008),

Resheff et al., 2014; Wang et al., 2015), large overall accuracies may be

marine  (Kawabe  et al.  2003)  and  terrestrial  (Soltis  et al.,  2012)

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License804  |    Methods in Ecology and Evolu(cid:13)on

species;  the  aperiodicity  of  foraging  has  been  alluded  to  for  Little

Penguins (Eudyptula minor) diving for unpredictably located and mo-

N  triaxial  acceleration  values  recorded  along  the  surge  (asurge),  sway
(asway) and heave (aheave) axes as follows.

bile prey (Ropert- Coudert, Kato, Wilson, & Cannell, 2006; Watanabe

& Takahashi, 2013). Despite extensive use of such biomechanically

Posture

significant parameters in their behaviour recognition schemes, pre-

Common  measures  of  posture  involve  estimating  how  the  sensor

vious methods leave room for improvement—parameter thresholds

is oriented with respect to Earth's gravity. Computation is done by

for  building  classification  rules  were  manually  chosen  (Laich  et al.

averaging acceleration recorded along each axis of the accelerom-

2008), and training data used for creating the model came only from

eter,  assuming  that  acceleration  due  to  dynamic  bodily  movement

a few captive animals (McClune et al., 2014; Soltis et al., 2012).

shows up as oscillations around a constant, static value correspond-

In this study, we present a general behaviour recognition frame-

ing to Earth's gravity (e.g. Yoda et al., 2001). For instance, the mean

work  in  the  form  of  a  hybrid  model  that  combines  general  biome-

of surge acceleration in window w, asurge,w, may be computed as:

chanical principles on the one hand, and machine learning tools on

the other. The proposed hybrid model consists of a tree- like classi-

fication  framework  predefined  on  the  basis  of  biomechanical  con-

Intensity

meanSurgew

= ∑N

𝛼

surge,w
N

(1)

siderations,  where  specific  combinations  of  acceleration- derived

biomechanical  descriptors  capturing  movement  biomechanics  of

behavioural categories studied across a range of species are used in

conjunction with robust machine learning algorithms at each node of

the tree. The use of biomechanics to instruct the classification makes

the  model  interpretable,  and  the  use  of  machine  learning  at  each

node of the tree completely automates the search for optimal metric

Contrary  to  posture  estimation,  movement  intensity  is  commonly

characterised by quantifying dynamic acceleration, which is obtained

by removing static acceleration corresponding to Earth's gravity from

total  recorded  acceleration.  For  this,  we  considered  the  use  of  std-

Normw,  the  standard  deviation  of  the  Euclidean  norm  of  the  triaxial
⃗aw|
), which is equivalent to computing Vectorial
acceleration vector (
|
|
|

Dynamic Body Acceleration (VeDBA, McGregor, Busa, Yaggie, & Bollt,

thresholds separating different behaviours. We showcase the appli-

2009):

cation and benefits of this hybrid behaviour recognition framework

on  data  collected  on  wild  meerkats  (Suricata  suricatta),  where  the

classification of their main activities such as vigilance, foraging, rest-

Periodicity

stdNormw = std (
|
|

⃗aw|
|

)

(2)

ing and running is essential for characterising their social and individ-

To  quantify  movement  periodicity,  we  analysed  the  frequency  con-

ual behaviour. We validated this hybrid model against synchronised,

tent of the signal through the use of the Fourier transform (FT). The

annotated video camera footage considered as the groundtruth, and

FT of aperiodic signals such as acceleration recorded during foraging

compared its performance with benchmark measures obtained with

will be relatively flat, whereas that computed for periodic signals such

alternative classification methods based entirely on classical machine

as those recorded during locomotion will be marked by the presence

learning.

2 |  MATERIAL AND ME THODS

2.1 | Biomechanically driven behaviour recognition
and validation

2.1.1 | Quantifying movement biomechanics through
acceleration- derived features

of  a  clear,  tall  peak,  usually  at  a  characteristic  frequency.  This  peak

height  was  considered  as  a  measure  of  signal  periodicity,  and  may

be  computed  as  follows.  For  each window  w,  the  acceleration  signal

from  each  of  the  three  axes  recorded  at  a  sampling  frequency  of  Fs
may  be:  (a)  normalised  (zero  mean  and  unit  energy);  (b)  low- pass  fil-

tered; (c) zero- padded and windowed; and (d) FT- ed with a resolution

of U Hz (corresponding to FT computation at L = Fs/U equally spaced
frequencies  between  0  and  Fs).  From  the  FT  of  acceleration  along
each  axis,  the  square  of  the  magnitude  of  each  Fourier  coefficient
(c2
, i ∈ 1 … L), corresponding to the power of the

, c2

, c2

fi,w,sway

fi,w,surge

fi,w,heave

Raw  triaxial  acceleration  data  may  be  summarised  in  the  form  of

quantifiable biomechanical descriptors of movement, which can then

be used as features capable of discriminating between different be-

havioural  categories.  The  features  to  be  developed  will  be  strongly

signal at frequency fi, may be computed and averaged over the three
axes. Finally, from this axis- averaged FT, the maximum power obtained
across all frequencies fi (i ∈ 1 … L) may be chosen as a measure of the
periodicity of the signal. This feature will henceforth be referred to as

dependent on the desired ethogram; here we shall consider an arche-

fftPeakPowerAvg.

typal, general ethogram consisting of three common behaviours—lo-

comotion, resting and foraging. We focused on three biomechanical

principles  to  characterise  these  behaviours:  posture,  movement  in-

fftPeakPowerAvgw

= max
L

c2
fi,w,sway

+ c2

fi,w,surge
3

+ c2

fi,w,heave

(3)

tensity and periodicity. These principles have been previously used to

Note that actual values of the signal processing parameters, such

discriminate between behaviours for a range of species; we aim to syn-

as type, order and cut- off frequency of the low- pass filter, length of

thesise and combine these existing but scattered principles within one

zero- padding, type of window and U, will depend on the characteris-

biomechanically defined classification framework. We quantify these

tics of the recorded acceleration signal, such as signal bandwidth and

three descriptors for each fixed- duration sliding window w containing

sampling frequency.

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMethods in Ecology and Evolu(cid:13)on

    |  805

2.1.2 | A biomechanically defined hierarchical
classification scheme with automated feature-
threshold computation

2.1.3 | Model validation

To test the utility of a behaviour recognition method, one needs to

validate the predictions made by it against groundtruthed data—the

The  proposed  approach  involves  predefining  a  hierarchical  tree- like

latter typically coming from direct observation or video annotation

scheme that classifies broader behavioural categories into increasingly

of  the  behaviours  of  interest.  Typically,  a  video  camera  synchro-

specific ones up to the desired level of behavioural resolution. Each

nised  with  the  animal- borne  accelerometer  is  used  to  film  the  ani-

node of this tree uses one or more features tailored to the classifica-

mal  while  the  accelerometer  records  data;  the  groundtruth  is  then

tion at that node. A predefined hierarchical scheme has two interest-

obtained by having an expert assign behaviour labels to sections of

ing characteristics that make it more advantageous over the common

the video based on a suitably defined ethogram. This process is then

classical machine learning approach of directly classifying behaviours

repeated  for  multiple  individuals  to  capture  inter- individual  varia-

at their highest resolution. The first advantage concerns the ease of

tion  in  behaviours.  Finally,  windows  of  acceleration  corresponding

dealing with imbalanced classes. It is quite probable that when spe-

to observed behaviours of interest are extracted from the continu-

cific behaviours are grouped into compound categories at the higher

ous acceleration data stream to obtain bouts of labelled behaviour

placed nodes of the tree, a relatively rarer behaviour gets clubbed into

of fixed duration. To evaluate the effect of imbalanced datasets and

the same compound category with a more frequent behaviour. As a

inter- individual  variability  on  model  classification,  we  discuss  three

result, the problem of imbalanced classes is not encountered at the

different forms of cross- validation.

higher placed node, and is deferred to a lower node where the rare

behaviour can no longer be grouped into a compound category with

Equally distributed behaviour 10- fold cross- validation (EQDIST)

the more frequent behaviour. Thus, if poor recognition accuracy of a

EQDIST evaluates model performance when the dataset has an equal

rare behaviour is encountered, one can precisely identify the node at

number of bouts of each behaviour. It involves conducting standard

which the misclassification occurs. Moreover, since the input features

10- fold  cross- validation  on  subsampled  datasets  where  the  sample

are tailored to each node, one can understand which features to add

size for each behaviour is made equal. This is done by first pooling data

or modify at the culprit node to improve classification. This process of

from  all  individuals  together,  and  then  randomly  selecting  as  many

optimising the model for each individual behaviour may be very dif-

bouts from each behaviour as the one with the least number of bouts.

ficult to do with machine learning approaches that classify directly up

to the finest behaviour resolution level using classification rules which

Stratified 10- fold cross- validation (STRAT)

are a function of many (>15) features. Secondly, when higher behav-

STRAT  evaluates  model  performance  when  some  behaviours  may

ioural resolution is desirable, specific behaviours themselves can be

be under- represented or rarer in the dataset than others. It involves

considered as compound categories and separated into finer behav-

pooling data from all individuals together and then dividing the pooled

iours by adding nodes below them. For instance, adding a node below

dataset into 10 equal parts in such a way that the proportion of bouts

‘locomotion’ could distinguish between slow and fast locomotion. In

from each type of behaviour in each fold is equal to that in the entire,

classical machine learning, if behavioural classes are added retrospec-

unmodified dataset.

tively, the entire model would have to be built anew.

The precise form of the classification tree for a specific application

Leave- one- individual- out cross- validation (LOIO)

will depend on the ethogram of interest, so will the features to be given

LOIO evaluates model performance when inter- individual variation is

as inputs to each node. Here we demonstrate the construction of a clas-

taken into account. It involves training a model using data pooled over

sification tree for the archetypal ethogram considered in Section 2.1.1

all individuals except one, and then testing this model on data from the

consisting of locomotion, resting and foraging. For the classification of

individual left out. This process is repeated until each individual has

these behaviours, the first node would separate the static (resting) and

been the ‘test’ individual once.

dynamic (locomotion and foraging) behavioural categories. At the sec-

We used confusion matrix- based metrics to evaluate and com-

ond  stage  of  this  tree,  one  node  below  the  dynamic  category  would

pare  model  performance.  These  performance  statistics  included

separate the two dynamic behaviours: locomotion and foraging. In this

three  behaviour- specific  metrics  (sensitivity,  precision  and  speci-

scheme, each node divides a parent behavioural category into exactly

ficity), and overall model accuracy (see Appendix S1 for definitions).

two daughter behavioural types. To accomplish this binary classification

at each node, appropriate user- chosen biomechanically significant fea-

tures (cf. Section 2.1.1) may be given as inputs to commonly employed

binary machine learning algorithms (such as Support Vector Machines

(SVM)) to obtain optimal feature- value thresholds in a completely auto-

2.2 | Case Study: Kalahari Meerkats

2.2.1 | Data collection and groundtruthing

mated fashion. For instance, at the first node of the classification tree

Fieldwork was conducted at the Kalahari Meerkat Project, a long- term

described  here,  stdNorm,  a  measure  of  movement  intensity,  may  be

study of wild meerkats in the South African Kalahari Desert (Clutton-

used as a single- feature input to an SVM that will separate behaviours

Brock, Gaynor, & McIlrath, 1999). Eleven data- recording sessions were

into the static and dynamic behavioural categories.

done  on  10  adult  meerkats  (seven  males,  three  females,  body  mass

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License806  |    Methods in Ecology and Evolu(cid:13)on

667 ± 98  grams,  age  24 ± 15 months);  one  of  the  individuals  was  re-

corded twice. For each individual, data were collected over 3 hr in the

morning, which corresponds to the duration of normal morning meer-

kat activity (meerkats become inactive as temperatures soar around the

midday hours). Individuals were captured using methodology described

in Jordan, Cherry & Manser, 2007 and fitted with a collar equipped with

an  inertial  measurement  unit  (IMU)  (adapted  version  of  Physilog  IV,

GaitUp SA, Switzerland) of size 35 mm × 29 mm × 19 mm and meas-

uring triaxial acceleration at 100 Hz/axis with a range of ± 156.96 m/
s2 (corresponding to ± 16 times the acceleration due to Earth's gravity)

with  16- bit  resolution. The  overall  collar weight was  <25 g;  collars  of

this size and weight have been shown not to affect meerkat behaviour

(Golabek, Jordan, & Clutton- Brock, 2008). The collar was positioned so

that the axes of the accelerometer were oriented as shown in Figure 1.

The accelerometer was calibrated prior to each capture according to a

standard  procedure  (Ferraris,  Grimaldi,  &  Parvis,  1995). After  release,

the collared animal was filmed using a handheld video camera record-

ing at 25 frames/second and synchronised electronically with the IMU

system. All videos were annotated using Solomon Coder (Version: beta

17.03.22). This video annotation served as the groundtruthing for our

behaviour recognition scheme.

2.2.2 | Meerkat behaviours and hierarchical
classification scheme

Four different behaviours (Figure 2) were considered for the ethogram

based on their biological significance:

F I G U R E   1  Sensor axes orientation. The image shows the animal
displaying typical bipedal vigilance behaviour

the animal's torso is typically upright during vigilance, it is flat during

•  Vigilance: representative of the animal's general stress or alertness

resting.  At  the  third  node,  movement  intensity  (stdNorm)  and  peri-

level. The meerkat is stationary and lifts its head and torso up to

odicity  (fftPeakPowerAvg)  were  used  to  separate  foraging  from  run-

survey its surroundings.

ning—running was observed to involve faster and more periodic limb

•  Foraging: can help derive proxies for body condition, which could, in

movements compared to foraging. At each node, a separate machine

turn, play a role in determining the animals’ survival and social sta-

learning algorithm (M1, M2 and M3 in Figure 2) was chosen from four

tus (Hodge, Manica, Flower, & Clutton-Brock, 2008). Most meerkat

candidates:  Naïve- Bayes  (NB),  Linear  Discriminant  Analysis  (LDA),

prey live underground; foraging involves scanning the ground, dig-

Logistic  Regression  (LR)  and  linear- kernel  Support  Vector  Machine

ging, and handling and ingesting prey.

(SVM). We shall henceforth refer to each such M1- M2- M3 combina-

•  Running:  high-speed  locomotion  from  one  point  to  another  with

tion as one ‘hybrid model’. Thus, since four candidates were possible at

presumably high energy expenditure. Prolonged running events are

each of the three nodes, a total of 4 × 4 × 4 = 64 hybrid models were

rare and typically mark important events such as aggressive inter-

tested  to  find  the  best  one.  Scikit- learn  (Pedregosa,  2011,  version

actions with rival meerkat groups.

•  Resting: periods of inactivity, mainly due to fatigue or excessive heat.

Typically, the meerkat lies down with its body flat on the ground.

0.19.0) was used to implement all machine learning models (using their
default configurations) in Python.

Video  clips  of  each  behaviour  are  provided  as  Supplementary

2.2.3 | Feature computation

Information.  Social  context- dependent  meerkat  behaviours  such  as

A sliding window w of size two seconds was considered for feature com-

grooming and territory marking were excluded from the ethogram.

putation; this provided sufficient temporal resolution of behaviour and

Based  on  the  description  of  the  behaviours  of  interest  here  and

was short enough to capture bouts of running, the behaviour with the

the  framework  presented  in  Section 2.1,  a  three- node  hierarchi-

shortest duration. Successive windows had an overlap of 50%. Windows

cal  scheme  was  devised  to  classify  meerkat  behaviour,  as  shown  in

containing  transitions  between  different  behaviours  were  excluded;

Figure 2. Movement intensity (stdNorm) and posture (meanSurge) were

each window thus contained acceleration data corresponding to exactly

used to separate static (vigilance and resting) and dynamic (foraging

one video- labelled behaviour.

and running) behaviours in the first node. At the second node, pos-

ture (meanSurge) was used to distinguish vigilance from resting—while

For each window w, acceleration along the surge axis (asurge,w) only
was  averaged  (meanSurgew)  and  used  to  estimate  neck  inclination

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMethods in Ecology and Evolu(cid:13)on

    |  807

(Equation 1), as values along this axis are least susceptible to changes

test fold were added together to produce an aggregated confusion ma-

due to possible rotations of the collar around the axis of the meerkat's

trix from which performance statistics were calculated. LOIO was done

cylindrical  neck.  For  fftPeakPowerAvg  computation  (cf.  Section 2.1.1

for individuals for which all four behaviours were recorded. Performance

under ‘Periodicity’), the parameters used were: Fs = 100 Hz, U = 0.01 Hz,
L = 10000. The low- pass filter was a fourth- order Butterworth filter with

a cut- off frequency of 10 Hz. The length of zero- padding was 1 s, and

the Blackman–Harris windowing function was used. All feature compu-
tations  were  done  using  MATLAB  R2016b.  MATLAB  code  to  compute
fftPeakPowerAvg is supplied in Supplementary Information.

2.2.4 | Model validation

statistics for each individual were computed separately, and their mean

and standard deviation across individuals were reported.

2.2.5 | Alternative classification methods:
benchmarking against classical machine learning
approaches

To  benchmark  our  hybrid  model's  results  against  those  obtained with

alternative  classification  methods  based  entirely  on  classical  machine

For EQDIST, 10 synthetically equalised datasets were generated using

learning, four commonly employed algorithms were considered: Naïve-

the Imbalanced- learn (Lemaitre et al., 2017, version 0.3.0) package in

Bayes (NB), K- Nearest Neighbours (KNN, with K = 5), Random Forest (RF,

Python. STRAT was implemented using Scikit- learn (Pedregosa, 2011).

with 10 trees) and Support Vector Machine (SVM) with a linear kernel.

For both EQDIST and STRAT, confusion matrices obtained from each

Features presented in a recent review of animal behaviour recognition

F I G U R E   2  Biomechanically
informed behaviour recognition
scheme. (a) Workflow showing feature
extraction from triaxial acceleration;
(b) At each of the three nodes of the
classification scheme, a separate machine
learning algorithm (M1, M2, M3) is
trained with specific biomechanical
features encapsulating information
on posture (meanSurge), movement
intensity (stdNorm) and periodicity
(fftPeakPowerAvg)

TA B L E   1  Summary of data collected.
Data were collected on 10 unique
individuals; data from recording session
numbers 4 and 7 were collected on the
same individual. A bout refers to a
window w of two seconds containing one
video- labelled behaviour

Recording session
number

Vigilance

Resting

Foraging

Running

Bouts per
recording session

1

2

3

4

5

6

7

8

9

10

11

4,594

3,896

1,453

5,221

1,890

1,639

4,785

71

4,283

1,906

1,782

Bouts per activity

31,520

2,114

120

0

0

0

744

156

0

0

0

661

3,795

1,562

5,315

6,278

2,823

6,134

4,438

3,498

4,841

1,713

4,407

5,398

69

29

38

161

169

98

40

20

43

84

77

8,339

9,360

7,769

8,205

8,193

6,919

8,479

4,932

6,039

6,397

7,918

4,6407

828

82,550
(total bouts)

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License808  |    Methods in Ecology and Evolu(cid:13)on

(Nathan et al., 2012) were considered as input to these machine learning

Section 2.2.2)—these  bouts  were  excluded  from  the  dataset.  The  re-

algorithms. They considered statistical features—mean, standard devia-

maining 82550 bouts corresponded to the four behaviours of interest,

tion, skewness, kurtosis, maximum and minimum—computed from data

as presented in Table 1. Foraging (56.2% of retained bouts) and vigilance

from each accelerometer axis as well as the acceleration norm. For con-

(38.2%) were the most common behaviours, whereas running (1%) was

sistency, we retained only those features that either used only the surge

the  rarest.  Typical  signals  recorded  for  each  behaviour  are  shown  in

axis or all three axes together—16 such features were identified. Further,

Figure 3.

to  meaningfully  compare  results with  our  three- feature  hybrid  model,

we selected the top three features from this set of 16, thereby ensur-

ing that both approaches would have the same complexity in terms of

3.2 | Performance evaluation

feature- space dimensionality. Further details on feature selection can be

Out of the 64 possible combinations for the M1- M2- M3 hybrid model,

found in Appendix S2.

3 |  RE SULTS

3.1 | Observed behaviour

we  found  that  SVM- SVM- SVM  performed  the  best  across  all  three

cross- validation methods. The linear- kernel SVM not only fully auto-

mated the search for robust feature- value thresholds but also yielded

simple  linear  decision  boundaries,  thereby  rendering  classification

rules transparent and intuitive, as shown in Figure 4. The next three

subsections give details on the performance of the SVM- SVM- SVM

A total of 105,604 2- s bouts of video- labelled behaviour were collected.

hybrid model for each cross- validation method tested, and benchmark

About 12.3% of these bouts contained transitions from one observed

them  against  results  obtained  with  classical  machine  learning  using

behaviour  to  another,  in  6.2%  of  them  the  animal was  not  caught  on

the same number of features. Results obtained with classical machine

camera  and  3.3%  contained  social  behaviour  such  as  grooming  (cf.

learning using all 16 features are provided in Appendix S3.

F I G U R E   3  Five-  second snapshots of the four behaviours of interest for a typical individual (dataset #1). During vigilance, the meerkat is
still; short perturbations in the signal occur when the head turns to scan the surroundings. During resting, the meerkat remains still and the
surge signal has a different intercept compared to that during vigilance. Foraging produces erratically varying signals due to site- dependent
digging and manoeuvring. Running is a fast, rhythmic activity marked by a highly periodic signal

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMethods in Ecology and Evolu(cid:13)on

    |  809

3.2.1 | EQDIST

metrics for LOIO with data from the five retained recording sessions

(corresponding  to  five  unique  individuals)  are  shown  in  Table 4.  For

Results for EQDIST in Table 2 show that for behaviour- specific met-

behaviour- specific  metrics,  the  best  hybrid  model  (SVM- SVM- SVM)

rics,  the  best  hybrid  model  (SVM- SVM- SVM)  performed  better  in

performed  better  in  terms  of  mean  sensitivity  (average  1.1%  across

terms  of  sensitivity  (average  3.5%  across  the  four  behaviours),  pre-

the four behaviours), mean precision (average 4.3%) and mean speci-

cision (average 3.3%) and specificity (average 1.1%) compared to the

ficity  (average  1.3%)  compared  to  the  best  machine  learning  model

best machine learning model (K- Nearest Neighbours).

(Random Forest).

3.2.2 | STRAT

4 |  DISCUSSION

Results for STRAT in Table 3 show that for behaviour- specific metrics,

the best hybrid model (SVM- SVM- SVM) performed better in terms of

We presented a physically intuitive behaviour recognition framework

sensitivity (average 5.1% across the four behaviours), precision (aver-

based on a hybrid model that combines movement biomechanics and

age 3.1%) and specificity (average 0.7%) compared to the best machine

robust machine learning. We showed that with our biomechanically de-

learning model (K- Nearest Neighbours).

fined node- based hierarchical classification framework, acceleration-

3.2.3 | LOIO

derived features summarising movement biomechanics could be used

in  conjunction  with  existing  machine  learning  algorithms  to  recog-

nise  behaviour  from  triaxial  acceleration  data.  Using  data  collected

For  LOIO,  data  from  recording  sessions  numbered  3,  4,  5,  8,  9  and

on  10  wild  meerkats,  we  demonstrated  the  efficacy  of  our  hybrid

10 (see Table 1) were discarded since they did not contain any rest-

model in scenarios where one or more behaviours are rarer or under-

ing  behaviour.  The  mean  and  standard  deviation  of  all  performance

represented  in  the  dataset  compared  to  others,  and  when  there  is

F I G U R E   4  Transparent classification. Linear decision boundaries ( l1, l2 and l3) found by the SVM- SVM- SVM hybrid model (for data used
during EQDIST) render the classification scheme transparent and physically intuitive

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License810  |    Methods in Ecology and Evolu(cid:13)on

l
l

a
r
e
v
O

g
n

i

n
n
u
R

g
n

i

g
a
r
o
F

g
n

i
t
s
e
R

e
c
n
a

l
i

i

g
V

)

%

(
y
c
a
r
u
c
c
a

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

l

e
d
o
M

h
c
a
o
r
p
p
A

.

7
5
9

.

5
1
8

2

.

2
9

2
9

4
8

.

9
7
9

.

5
6
9

.

9
7
9

2

.

8
9

2

.

8
9

.

3
9
9

8

.

8
9

.

3
9
9

.

4
9
9

.

4
9
9

.

7
6
9

.

8
7
9

.

9
7
9

.

5
7
9

.

7
7
9

.

3
4
9

.

6
2
9

.

9
3
9

.

2
4
9

.

8
2
9

.

5
7
9

.

9
7
9

.

5
7
9

8
9

8
9

.

7
5
9

.

9
6
9

.

7
6
9

.

3
7
9

7
9

.

8
5
9

.

6
2
6

.

8
1
9

.

1
7
6

3
9

.

6
8
9

.

3
2
8

.

9
7
9

.

5
7
9

.

7
5
8

.

7
3
9

.

9
8
8

.

7
2
8

.

3
3
8

.

6
7
8

.

7
4
9

.

6
1
8

.

6
4
8

.

3
4
8

.

3
2
8

2

.

8
9

.

7
6
9

.

5
4
9

.

4
4
9

2

.

6
9

.

2
5
9

M
V
 S
-

M
V
 S
-

M
V
S

d
i
r
b
y
H

.

5
3
4

.

3
1
9

.

5
0
9

.

6
3
5

N
N
K

M
V
S

F
R

i

e
n
h
c
a
M

i

g
n
n
r
a
e
L

B
N

l

a
c
i
s
s
a
C

l

i

g
n
n
r
a
e

l

i

e
n
h
c
a
m

l

a
c
i
s
s
a

l

c

f
o
t
a
h
t

i

t
s
n
a
g
a
d
e
k
r
a
m
h
c
n
e
b
s
i

l

e
d
o
m
d
i
r
b
y
h
M
V
 S
-

M
V
 S
-

M
V
S
e
h
t

f
o
e
c
n
a
m
r
o
f
r
e
p
e
h
T

.
s
t
l
u
s
e
r
n
o
i
t
a
d

i
l

a
 v
-

s
s
o
r
c
T
S
I
D
Q
E

2

E
L
B
A
T

.

i

e
n
h
c
a
M

r
o
t
c
e
V
t
r
o
p
p
u
S

,

M
V
S

;
t
s
e
r
o
F
m
o
d
n
a
R

,

F
R

;
s
r
u
o
b
h
g

i

e
N

t
s
e
r
a
e
 N
-

K

,

N
N
K

;
s
e
y
a
 B
-

e
v

ï

a
N

,

B
N

l
l

a
r
e
v
O

g
n

i

n
n
u
R

g
n

i

g
a
r
o
F

g
n

i
t
s
e
R

e
c
n
a

l
i

i

g
V

)

%

(
y
c
a
r
u
c
c
a

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

l

e
d
o
M

h
c
a
o
r
p
p
A

.

7
7
9

.

9
2
9

6
9

.

9
5
9

.

6
3
9

.

1
2
9

.

1
8
5

.

4
9
8

.

7
0
9

.

3
1
9

.

9
9
9

.

3
9
9

.

9
9
9

.

9
9
9

.

9
9
9

.

9
5
8

.

7
4
9

.

4
8
8

.

7
6
8

.

6
2
8

.

3
8
9

.

3
7
9

.

1
8
9

.

4
7
9

8
9

.

8
7
9

.

6
6
9

.

4
7
9

.

5
7
9

.

6
6
9

.

3
9
9

8
9

8

.

8
9

8

.

8
9

.

2
9
9

.

1
7
8

0

.

4
1
8

2

.

0
8

0

.

4
9
9

0
0
1

.

3
9
9

.

2
9
9

0
0
1

5
8

0

.

1
4
6

.

7
4
6

0

.

1
8
9

2

.

8
8

.

5
4
9

.

4
4
9

.

4
8
8

8

.

8
9

2
9

.

6
6
9

5

.

6
9

.

1
2
9

.

1
7
9

M
V
 S
-

M
V
 S
-

M
V
S

d
i
r
b
y
H

.

4
6
9

.

8
5
9

.

7
5
9

.

8
6
9

N
N
K

M
V
S

F
R

i

e
n
h
c
a
M

i

g
n
n
r
a
e
L

B
N

l

a
c
i
s
s
a
C

l

i

g
n
n
r
a
e

l

i

e
n
h
c
a
m

l

a
c
i
s
s
a

l

c

f
o
t
a
h
t

i

t
s
n
a
g
a
d
e
k
r
a
m
h
c
n
e
b
s
i

l

e
d
o
m
d
i
r
b
y
h
M
V
 S
-

M
V
 S
-

M
V
S
e
h
t

f
o
e
c
n
a
m
r
o
f
r
e
p
e
h
T

.
s
t
l
u
s
e
r
n
o
i
t
a
d

i
l

a
 v
-

s
s
o
r
c
T
A
R
T
S

3

E
L
B
A
T

.

i

e
n
h
c
a
M

r
o
t
c
e
V
t
r
o
p
p
u
S

,

M
V
S

;
t
s
e
r
o
F
m
o
d
n
a
R

,

F
R

;
s
r
u
o
b
h
g

i

e
N

t
s
e
r
a
e
 N
-

K

,

N
N
K

;
s
e
y
a
 B
-

e
v

ï

a
N

,

B
N

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

l

l

d
e
t
a
u
c
a
c
e
r
e
w
s
c
i
r
t
e
m
e
c
n
a
m
r
o
f
r
e
P

.

i

g
n
n
r
a
e

l

i

e
n
h
c
a
m

l

l

a
c
i
s
s
a
c
f
o
t
a
h
t

i

t
s
n
a
g
a
d
e
k
r
a
m
h
c
n
e
b
s
i

l

e
d
o
m
d
i
r
b
y
h
M
V
 S
-

M
V
 S
-

M
V
S
e
h
t

f
o
e
c
n
a
m
r
o
f
r
e
p
e
h
T

.
s
t
l
u
s
e
r
n
o
i
t
a
d

i
l

a
 v
-

s
s
o
r
c
O
O
L

I

4

E
L
B
A
T

e
r
e
h
n
w
o
h
s
e
r
a
s
l
a
u
d
v
d
n

i

i

i

t
s
e
t

i

s
s
o
r
c
a
n
o
i
t
a
v
e
d
d
r
a
d
n
a
t
s
d
n
a
n
a
e
m

r
i
e
h
t
d
n
a

l

i

a
u
d
v
d
n

i

i

t
s
e
t
h
c
a
e
r
o
f
y
e
t
a
r
a
p
e
s

l

l
l

a
r
e
v
O

g
n

i

n
n
u
R

g
n

i

g
a
r
o
F

g
n

i
t
s
e
R

e
c
n
a

l
i

i

g
V

)

%

(
y
c
a
r
u
c
c
a

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

)

%

(

.

c
e
r
P

)

%

(

.

c
e
p
S

)

%

(

.

n
e
S

l

e
d
o
M

h
c
a
o
r
p
p
A

.

8
1
±
5

.

6
9

2

.

8
±
9
8
7

.

8

.

2
±
1
3
9

.

.

4
2
±
6
3
9

.

.

1
1
1
±
1
9
8

.

.

1
0
±
9
9
9

.

2

.

3
1
±
3

.

6
8

.

0
7
±
3
5
9

.

.

6
0
2
±
9
1
6

.

.

1
0
1
±
7
0
9

.

.

7
1
1
±
4
1
9

.

.

8
0
±
3
9
9

.

.

0
2
±
6
8
9

.

.

6
6
±
4
4
9

.

2

.

0
±
9
9
9

.

5

.

2
1
±
2

.

0
9

.

5
4
±
2

.

6
9

2

.

0
±
9
9
9

.

.

0
2
1
±
8

.

8
8

8

.

3
±
6
6
9

.

5

.

0
1
±
2

.

8
8

.

4
9
±
8
0
9

.

.

1
0
±
9
9
9

.

.

0
2
1
±
8
4
8

.

5

.

6
±
5
4
9

.

.

5
1
±
4
7
9

.

.

0
1
±
8

.

8
9

.

0
8
2
±
1
1
8

.

2

.

1
±
9
8
9

.

.

6
3
2
±
4
1
7

.

.

5
4
±
4
6
9

.

.

8
1
±
1
6
9

.

.

0
1
±
3
7
9

.

.

9
2
±
1
2

.

.

7
2
1
±
9
0
9

.

.

5
5
4
±
7
1
3

.

.

4
4
1
±
7
8
7

.

2

.

1
±
4
8
9

.

8

.

2
±
8
5
9

.

M
V
 S
-

M
V
 S
-

M
V
S

d

i
r
b
y
H

3

.

2
2
±
6
2
8

.

.

4
2
2
±
8

.

6
7

B
N

l

a
c
i
s
s
a
C

l

.

1
1
±
4
7
9

.

.

9
0
±
2

.

8
9

.

8
9
2
±
4
3
6

.

.

8
0
±
3

.

8
9

.

4
8
1
±
6
2
6

.

.

6
8
±
8

.

8
8

2

.

6
±
1
3
9

.

.

6
2
±
5

.

2
9

.

1
1
±
6
7
9

.

.

0
1
±
0
8
9

.

.

4
8
2
±
9
6
6

.

.

0
1
±
4
8
9

.

.

8
7
1
±
5

.

8
6

.

3
7
±
7
9
8

.

.

5
5
±
7
3
9

.

2

.

3
±
7
2
9

.

.

8
1
±
1
6
9

.

.

0
1
±
7
8
9

.

0

0
0
1

0

.

8
4
1
±
3
9
7

.

.

8
1
2
±
0
2
8

.

.

6
2
±
5
5
9

.

N
N
K

M
V
S

F
R

e
n

i

h
c
a
M

g
n

i

n
r
a
e
L

Methods in Ecology and Evolu(cid:13)on

    |  811

inter- individual variability. We showed that our hybrid model's predic-

tions were more accurate than those obtained with alternative clas-

sification methods based on classical machine learning using the same

number of features.

Our results shed light on the complex interplay of several factors

involved in behaviour recognition: feature selection, class imbalance,

class  separability,  model  selection  and  persistent  misclassification.

While the feature selection methods used in classical machine learning

found measures of movement intensity (stdNorm, stdSurge; Appendix

S2), they failed to select a measure of posture. This proved to be es-

pecially problematic for distinguishing the two static behaviours, vig-

ilance and resting, since they primarily differ in posture. Consistently

poorer resting and vigilance detection performance resulted when a

measure  of  posture  was  excluded  (classical  machine  learning)  com-

pared to when it was included (meanSurge in the hybrid model) even

in EQDIST, where matters are not yet complicated by class imbalance.

The effect of not including a measure of posture gets amplified when

naturally occurring class imbalance is introduced in STRAT: the classi-

cal machine learning models NB and SVM completely miss the much

rarer  resting  behaviour  (vigilance  bouts  outnumber  resting  bouts

8.3:1),  whereas  for  KNN  and  RF,  resting  detection  sensitivity  plum-

mets to below 65% and precision to below 82%. Model response to

class  imbalance  may  vary  unpredictably:  classical  machine  learning

with  KNN  and  RF  yields  fair  performance  across  EQDIST,  STRAT

and  LOIO;  SVM,  on  the  other  hand,  first  recognises  resting  during

EQDIST  (albeit  poorly)  despite  the  absence  of  a  feature  describing

posture, then completely misses resting behaviour during STRAT and

LOIO (even though overall model accuracy still remains high: 93.6%

and 88.2% respectively), and then performs well when all 16 features

are  included  (Appendix  S3).  This  indicates  the  difficulty  of  general-

ising model behaviour across datasets when feature choice is left to

an automatic algorithm. However, the hybrid model, where the SVM

algorithm  was  only  used  to  find  feature- value  thresholds  within  a

biomechanically  predefined  tree- like  classification  structure  with

task- specific  features  (i.e.  biomechanically  appropriate  features  for

each node in the classification tree), consistently performs well across

EQDIST, STRAT and LOIO. Class imbalance may be less problematic

when class separability is high. Running, despite being the rarest class

in our dataset (foraging instances outnumber running instances 56:1)

is  recognised  fairly  accurately  across  EQDIST,  STRAT  and  LOIO  for

the KNN, RF and SVM classical machine learning models, and the hy-

brid model. This might be because measures of intensity (stdNorm, std-

Surge) were particularly effective at separating foraging and running:

this can be seen from Figure 4, where the magnitude of <1 of the slope

of the decision boundary l3 implies that the feature on the vertical axis
(stdNorm) is more discriminating than the one on the horizontal axis

(fftPeakPowerAvg).

In addition to exponentially greater model complexity, perhaps the

greatest disadvantage of increasing the number of features in classical

machine  learning  is  the  loss  of  ability  to  understand  why  misclassi-

fications  persist.  The  performance  of  classical  machine  learning  be-

comes comparable to that of the hybrid model when all 16 features are

used (Appendix S3), yet even with a fivefold increase in the number

.

i

e
n
h
c
a
M

r
o
t
c
e
V
t
r
o
p
p
u
S

,

M
V
S

;
t
s
e
r
o
F
m
o
d
n
a
R

,

F
R

;
s
r
u
o
b
h
g

i

e
N

t
s
e
r
a
e
 N
-

K

,

N
N
K

;
s
e
y
a
 B
-

e
v

ï

a
N

,

B
N

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

812  |    Methods in Ecology and Evolu(cid:13)on

of features (from 3 to 16), resting detection performance still remains

been achieved. This high- resolution model may then be made available

poor. Examination of the classification rules to understand the source

for future studies on that species.

of misclassification is rendered unmanageable by the fact that, for 16

Choosing  appropriate  sensor  parameters  may  be  a  crucial  com-

features,  16- dimensional  space  will  need  to  be  analysed.  With  the

ponent  of  achieving  accurate  behaviour  classification.  Even  though

hybrid model, however, due to the hierarchical nature of the classifi-

Gao  et al.,  2013  followed  a  hierarchical  classification  scheme  em-

cation scheme, it is easy to pinpoint where and why resting misclassi-

ploying  SVMs,  the  web- based  system  they  developed  limited  the

fication occurs. The rarer resting behaviour is clubbed with a frequent

input  sampling  frequency  to  only  1 Hz  which,  they  found  for  some

behaviour, vigilance, into the static behavioural category, and the rarer

species, was insufficient to extract meaningful information from the

running  behaviour  is  clubbed  with  a  frequent  behaviour,  foraging,

frequency- domain features they used. In our meerkat study, requisite

(foraging bouts outnumber running bouts 56:1) into the dynamic cat-

signal  processing  techniques  employed  to  compute  movement  peri-

egory. Thereafter, since the static and dynamic behavioural categories

odicity through fftPeakPowerAvg might have played an important role

are separated accurately (Table S7), it is easy to see that the primary

in successfully distinguishing meerkat running from foraging despite

deterioration  of  resting  recognition  accuracy  must  occur  at  the  M2

high  class  imbalance.  This  was  due,  in  part,  to  the  choice  of  a  suffi-

node. This node employs an SVM which uses only one feature as input,

ciently  high  sampling  frequency  of  100 Hz.  We  found  that  meerkat

meanSurge  (measure  of  posture)—this  thus  indicated  that  there  may

running  had  a  characteristic  frequency  of  around  4 Hz,  and  a  good

have been limitations to our hypothesis about posture during resting

rule- of- thumb is to oversample by about 20 times when using a noisy

and/or vigilance. Indeed, re- consulting the groundtruthing video data,

sensor  (Boyd,  Sundaram,  &  Shrivastava,  2010),  although  the  sam-

we discovered that the major source of erroneous resting detection

pling  frequency  could  theoretically  be  reduced  to  the  Nyquist  limit

was the disproportionately large contribution of an additional unex-

of  twice  the  maximum  frequency  of  interest.  Finally,  while  stdNorm

pected  curled- up  resting  posture  (different  from  the  belly- flat  posi-

and fftPeakPowerAvg, used in foraging vs. running classification, make

tion typically observed) of a single individual (see Appendix S4). Thus,

no assumptions about sensor orientation with respect to the animal,

new insight into the groundtruthing data itself was obtained because

meanSurge, used in vigilance vs. resting classification, assumes knowl-

of the interpretability offered by our hybrid model; this is in contrast

edge of sensor placement around the meerkat's neck. Higher running

to  machine  learning  approaches,  which  have  to  rely  completely  on

classification accuracy (compared to that for resting) might thus indi-

groundtruthing data.

cate that if the features used are independent of sensor orientation

Our behaviour recognition framework offers two other key advan-

with respect to the animal, classification may be more robust for some

tages  over  existing  methods.  Firstly,  in  our  hybrid  model,  robust  ma-

species, since sensor fixation will inevitably be slightly different across

chine learning algorithms were tasked with searching for feature- value

individuals or species (e.g. collars in mammals and back- packs in birds).

thresholds, thus making the mechanism of decision boundary selection

Studies on energy expenditure (e.g. Gleiss, Wilson, & Shepard, 2011)

automatic,  general,  clear  and  easy  to  implement.  In  the  tree- based

also suggested that when accelerometers cannot be accurately placed

classification model presented by McClune et al., 2014, analyses were

on  the  animal,  using  information  from  all  axes  together  (Vectorial

based on data from a single, tame individual, and it was not clear how

Dynamic  Body  Acceleration)  may  perform  better  than  treating  each

their iterative feature- threshold selection method could be extended to

axis independently (Overall Dynamic Body Acceleration).

data from more individuals. Secondly, our classification scheme has the

Through the use of general biomechanical principles characterising

potential to enable meaningful model sharing across studies by offering

animal movement, our conceptually simple, robust classification method

the added advantage of being adaptable to desired levels of behavioural

may  be  applicable  across  a  range  of  species, with  different  behaviour

resolution. For studies where coarse behavioural resolution is sufficient,

labels depending on the species’ specific context. The biomechanically

our hybrid model can be used to simply determine when the animal was

defined  node- based  hierarchical  format  permitting  model  adaptation

static or dynamic. For studies requiring higher behavioural resolution,

to  coarser  or  finer  behavioural  resolution  makes  it  apt  for  meaningful

our scheme may be used as a template upon which new nodes, possibly

model sharing between studies on a given species. The advantage and

using  additional  biomechanically  derived  features,  may  be  added  fur-

novelty of our method is that it allows a high classification performance

ther down the tree to accommodate new behaviours when needed. For

and, at the same time, a physical and biomechanical interpretation of the

the meerkat ethogram chosen for this study, three biomechanically in-

terpretable features proved to be enough but, for instance, if one were

interested  in  characterising  meerkat  foraging  effort,  one  could  add

an additional node below ‘foraging’ and split it into ‘digging’ and ‘non-

digging’  through  a  peak- detection- based  metric  indicating  front- paw

swipes made during digging. In a classical machine learning approach,

classification outcomes. The incorporation of common machine learning
algorithms found in all popular, existing packages in Python, MatLab
and R makes this method simple and accessible.

ACK N OWLE D G E M E NT S

the  whole  model  would  need  to  be  rebuilt  from  scratch  if  new  be-

We thank the Northern Cape Conservation Authority for permission

haviours were to be added; in our approach, adding higher behavioural

to conduct this research, and the farmers neighbouring the KRC for

resolution to a given ‘coarser’ model will not impact the existing model

granting us access to their private land. We thank the Trustees of the

parameters. This could enable separate studies on the same species to

KRC  for  access  to  research  facilities  in  the  Kuruman  River  Reserve

add upon a single model until the required behavioural resolution has

and the Directors of the KMP for access to habituated animals with

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons Licenseknown life histories. During the period of our project, the long- term

research on meerkats was supported by a European Research Council

Advanced  Grant  (No.  294494)  to  Tim  Clutton- Brock,  the  University

of  Zurich  and  the  Mammal  Research  Institute  at  the  University  of

Pretoria. We thank the field managers, collaborators and assistants for

facilitating field work and helping with data collection, and in particu-

lar David Gaynor, Tim Vink, Ana Morales González and Héctor Ruiz

Villar.  Special  thanks  to  Nino  Maag  for  helping  with  developing  the

conceptual  framework  of  the  project,  definition  of  meerkat  behav-

iours and data collection. We thank Selin Ersoy for annotating all vid-

eos, and Pascal Morel for adapting the Physilog IV for this study. This

project was supported by the Swiss National Science Foundation (re-

search grant no. CR32I*_159743) to Arpat Ozgul and Kamiar Aminian.

We thank the three anonymous reviewers, associate editor and han-

dling  editor  for  their  thoughtful  comments  that  helped  improve  the

presentation and clarity of the manuscript.

AUTH O R S ’ CO NTR I B UTI O N S

K.A.  and  P.C.  developed  the  research  idea,  and  G.C.  and A.O con-

tributed to refinements. P.C. and G.C. supervised the fieldwork. P.C.

performed  data  analyses  and  led  the  writing  of  the  manuscript.  All

authors contributed critically to the drafts and gave final approval for

publication.

DATA ACCE S S I B I LIT Y

Data  deposited

in  the  Dryad  Digital  Repository  <https://doi>.

org/10.5061/dryad.7q294p8 (Chakravarty et al. 2019).

O RCI D

Pritish Chakravarty

 <https://orcid.org/0000-0002-2975-6253>

Gabriele Cozzi

 <https://orcid.org/0000-0002-1744-1940>

Arpat Ozgul

 <https://orcid.org/0000-0001-7477-2642>

Kamiar Aminian

 <https://orcid.org/0000-0002-6582-5375>

R E FE R E N C E S

Bidder,  O.  R.,  Campbell,  H.  A.,  Gómez-Laich,  A.,  Urgé,  P.,  Walker,  J.,  &
Cai, Y., … Wilson, R. P. (2014). Love thy neighbour: Automatic animal
 behavioural  classification  of  acceleration  data  using  the  k- nearest
neighbour algorithm. PLoS ONE, 9(2), e88609. <https://doi.org/10.1371/>
journal.pone.0088609

Boyd, J., Sundaram, H., & Shrivastava, A. (2010). Power-accuracy tradeoffs
in human activity transition detection. In Proceedings of the Conference
on  Design,  Automation  and  Test  in  Europe  (pp.  1524–1529).  European
Design and Automation Association.

Chakravarty,  P.,  Cozzi,  G.,  Ozgul,  A.,  &  Aminian,  K.  (2019).  Data  from:  A
novel biomechanical approach for animal behaviour recognition using
accelerometers. Dryad Digital Repository,  <https://doi.org/10.5061/>
dryad. 7q294p8

Clutton-Brock,  T.  H.,  Gaynor,  D.,  McIlrath,  G.  M.,  Maccoll,  A.  D.  C.,
Kansky,  R.,  Chadwick,  P.,  …  Brotherton,  P.  N.  M.  (1999).  Predation,
group  size  and  mortality  in  a  cooperative  mongoose,  Suricata

Methods in Ecology and Evolu(cid:13)on

    |  813

suricatta.  Journal  of  Animal  Ecology,  68(4),  672–683.  <https://doi>.
org/10.1046/j.1365-2656.1999.00317.x

Cozzi, G., Broekhuis, F., McNutt, J. W., Turnbull, L. A., Macdonald, D. W., &
Schmid, B. (2012). Fear of the dark or dinner by moonlight? Reduced
temporal partitioning among Africa's large carnivores. Ecology, 93(12),
2590–2599. <https://doi.org/10.1890/12-0017.1>

Ferraris, F., Grimaldi, U., & Parvis, M. (1995). Procedure for effortless in-
field  calibration  of  three- axial  rate  gyro  and  accelerometers.  Sensors
and Materials, 7(5), 311–330.

Gao, L., Campbell, H. A., Bidder, O. R., & Hunter, J. (2013). A Web- based se-
mantic tagging and activity recognition system for species’ accelerom-
etry data. Ecological Informatics, 13, 47–56. <https://doi.org/10.1016/j>.
ecoinf.2012.09.003

Gleiss, A. C., Wilson, R. P., & Shepard, E. L. (2011). Making overall dynamic
body acceleration work: On the theory of acceleration as a proxy for
energy  expenditure.  Methods  in  Ecology  and  Evolution,  2(1),  23–33.
<https://doi.org/10.1111/j.2041-210X.2010.00057.x>

Golabek,  K.  A.,  Jordan,  N.  R.,  &  Clutton-Brock,  T.  H.

(2008).
Radiocollars  do  not  affect  the  survival  or  foraging  behaviour  of
wild  meerkats.  Journal  of  Zoology,  274(3),  248–253.  <https://doi>.
org/10.1111/j.1469-7998.2007.00377.x

Goldbogen, J. A., Calambokidis, J., Oleson, E., Potvin, J., Pyenson, N. D.,
Schorr,  G.,  &  Shadwick,  R.  E.  (2011).  Mechanics,  hydrodynamics  and
energetics of blue whale lunge feeding: Efficiency dependence on krill
density.  Journal  of  Experimental  Biology,  214(1),  131–146.  <https://doi>.
org/10.1242/jeb.048157

Grünewälder, S., Broekhuis, F., Macdonald, D. W., Wilson, A. M., McNutt, J.
W., Shawe-Taylor, J., & Hailes, S. (2012). Movement activity based clas-
sification of animal behaviour with an application to data from cheetah
(Acinonyx jubatus). PLoS ONE, 7(11), e49120. <https://doi.org/10.1371/>
journal.pone.0049120

Hammond,  T.  T.,  Springthorpe,  D.,  Walsh,  R.  E.,  &  Berg-Kirkpatrick,  T.
(2016). Using accelerometers to remotely and automatically character-
ize behavior in small animals. Journal of Experimental Biology, 219(11),
1618–1624. <https://doi.org/10.1242/jeb.136135>

He,  H.,  &  Garcia,  E.  A.  (2009).  Learning  from  imbalanced  data.  IEEE
Transactions on Knowledge and Data Engineering, 21(9), 1263–1284.
Hodge,  S.  J.,  Manica,  A.,  Flower,  T.  P.,  &  Clutton-Brock,  T.  H.  (2008).
Determinants  of
female
meerkats.  Journal  of  Animal  Ecology,  77(1),  92–102.  <https://doi>.
org/10.1111/j.1365-2656.2007.01318.x

in  dominant

reproductive

success

Jordan, N. R., Cherry, M. I., & Manser, M. B. (2007). Latrine distribution and
patterns of use by wild meerkats: Implications for territory and mate
defence. Animal Behaviour, 73(4), 613–662.

Kawabe, R., Kawano, T., Nakano, N., Yamashita, N., Hiraishi, T.,& Naito,
Y.  (2003).  Simultaneous  measurement  of  swimming  speed  and
tail  beat  activity  of  free-swimming  rainbow  trout  Oncorhynchus
mykiss  using  an  acceleration  data-logger.  Fisheries  science,  69(5),
959–965.

Laich, A. G., Wilson, R. P., Quintana, F., & Shepard, E. L. (2008). Identification
of imperial cormorant Phalacrocorax atriceps behaviour using acceler-
ometers. Endangered species research, 10, 29–37.

Lemaitre, G., Nogueira, F., & Aridas, C. K. (2017). Imbalanced- learn: A py-
thon  toolbox  to  tackle  the  curse  of  imbalanced  datasets  in  machine
learning. Journal of Machine Learning Research, 18(17), 1–5.

McClune, D. W., Marks, N. J., Wilson, R. P., Houghton, J. D., Montgomery,
I. W., & McGowan, N. E., … Scantlebury, M. (2014). Tri- axial accelerom-
eters quantify behaviour in the Eurasian badger (Meles meles): Towards
an automated interpretation of field data. Animal Biotelemetry, 2(1), 5.
<https://doi.org/10.1186/2050-3385-2-5>

McGregor, S. J., Busa, M. A., Yaggie, J. A., & Bollt, E. M. (2009). High res-
olution MEMS accelerometers to estimate VO2 and compare running
mechanics  between  highly  trained  inter- collegiate  and  untrained
runners.  PLoS  ONE,  4(10),  e7355.  <https://doi.org/10.1371/journal>.
pone.0007355

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License814  |    Methods in Ecology and Evolu(cid:13)on

Naito,  Y.,  Bornemann,  H.,  Takahashi,  A.,  McIntyre,  T.,  &  Plötz,  J.  (2010).
Fine- scale feeding behavior of Weddell seals revealed by a mandible
accelerometer. Polar Science, 4(2), 309–316. <https://doi.org/10.1016/j>.
polar.2010.05.009

Nathan, R., Spiegel, O., Fortmann-Roe, S., Harel, R., Wikelski, M., & Getz,
W.  M.  (2012).  Using  tri- axial  acceleration  data  to  identify  behavioral
modes of free- ranging animals: General concepts and tools illustrated
for griffon vultures. Journal of Experimental Biology, 215(6), 986–996.
<https://doi.org/10.1242/jeb.058602>

Pedregosa, , et al. (2011). Scikit- learn: Machine learning in python. JMLR,

12, 2825–2830.

Resheff,  Y.  S.,  Rotics,  S.,  Harel,  R.,  Spiegel,  O.,  &  Nathan,  R.  (2014).
AcceleRater: A web application for supervised learning of behavioral
modes  from  acceleration  measurements.  Movement  Ecology,  2(1),  27.
<https://doi.org/10.1186/s40462-014-0027-0>

Ropert-Coudert, Y., Kato, A., Wilson, R. P., & Cannell, B. (2006). Foraging
strategies and prey encounter rate of free- ranging Little Penguins. Marine
Biology, 149(2), 139. <https://doi.org/10.1007/s00227-005-0188-x>
Ropert-Coudert,  Y.,  &  Wilson,  R.  P.  (2005).  Trends  and  perspectives
in  animal- attached  remote  sensing.  Frontiers  in  Ecology  and  the
Environment, 3(8), 437–444. <https://doi.org/10.1890/1540-9295(200>
5)003[0437:TAPIAR]2.0.CO;2

Sellers,  W.  I.,  Varley,  J.  S.,  &  Waters,  S.  S.  (1998).  Remote  monitoring  of
locomotion  using  accelerometers:  A  pilot  study.  Folia  Primatologica,
69(Suppl. 1), 82–85. <https://doi.org/10.1159/000052700>

Shepard,  E.  L.,  Wilson,  R.  P.,  Quintana,  F.,  Laich,  A.  G.,  Liebsch,  N.,  &
Albareda, D. A., … Newman, C. (2008). Identification of animal move-
ment  patterns  using  tri- axial  accelerometry.  Endangered  Species
Research, 10, 47–60. <https://doi.org/10.3354/esr00084>

Soltis,  J.,  Wilson,  R.  P.,  Douglas-Hamilton,  I.,  Vollrath,  F.,  King,  L.  E.,  &
Savage, A. (2012). Accelerometers in collars identify behavioral states
in  captive  African  elephants  Loxodonta  africana.  Endangered  Species
Research, 18(3), 255–263. <https://doi.org/10.3354/esr00452>

Wang,  Y.,  Nickel,  B.,  Rutishauser,  M.,  Bryce,  C.  M.,  Williams,  T.  M.,
Elkaim,  G.,  &  Wilmers,  C.  C.  (2015).  Movement,  resting,  and

attack behaviors of wild pumas are revealed by tri- axial accelerome-
ter measurements. Movement Ecology, 3(1), 2. <https://doi.org/10.1186/>
s40462-015-0030-0

Watanabe,  S.,  Izawa,  M.,  Kato,  A.,  Ropert-Coudert,  Y.,  &  Naito,  Y.
(2005).  A  new  technique  for  monitoring  the  detailed  behaviour
of  terrestrial  animals:  A  case  study  with  the  domestic  cat.  Applied
Animal  Behaviour  Science,  94(1),  117–131.  <https://doi.org/10.1016/j>.
applanim.2005.01.010

Watanabe,  Y.  Y.,  &  Takahashi,  A.  (2013).  Linking  animal- borne  video
to  accelerometers  reveals  prey  capture  variability.  Proceedings  of
the  National  Academy  of  Sciences,  110(6),  2199–2204.  <https://doi>.
org/10.1073/pnas.1216244110

Wilson, R. P., White, C. R., Quintana, F., Halsey, L. G., Liebsch, N., Martin,
G. R., & Butler, P. J. (2006). Moving towards acceleration for estimates
of  activity- specific  metabolic  rate  in  free- living  animals:  The  case  of
the cormorant. Journal of Animal Ecology, 75(5), 1081–1090. <https://doi>.
org/10.1111/j.1365-2656.2006.01127.x

Yoda,  K.,  Naito,  Y.,  Sato,  K.,  Takahashi,  A.,  Nishikawa,  J.,  &  Ropert-
Coudert, Y., … Le Maho, Y. (2001). A new technique for monitoring
the behaviour of free- ranging Adelie penguins. Journal of Experimental
Biology, 204(4), 685–690.

S U P P O R T I N G I N FO R M AT I O N

Additional  supporting  information  may  be  found  online  in  the

Supporting Information section at the end of the article.

How to cite this article: Chakravarty P, Cozzi G, Ozgul A,

Aminian K. A novel biomechanical approach for animal

behaviour recognition using accelerometers. Methods Ecol Evol.

2019;10:802–814. <https://doi.org/10.1111/2041-210X.13172>

CHAKRAVARTY eT Al. 2041210x, 2019, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13172> by Test, Wiley Online Library on [03/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
