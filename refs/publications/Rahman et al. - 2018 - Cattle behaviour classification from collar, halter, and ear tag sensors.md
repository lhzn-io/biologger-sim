A v a i l a b l e a t w w w . s c i e n c e d i r e c t . c o m

INFORMATION PROCESSING IN AGRICULTURE 5 (2018) 124–133

j o u r n a l h o m e p a g e : w w w . e l s e v i e r . c o m / l o c a t e / i n p a

Cattle behaviour classiﬁcation from collar, halter,
and ear tag sensors

A. Rahman a,*, D.V. Smith a, B. Little b, A.B. Ingham b, P.L. Greenwood c,
G.J. Bishop-Hurley b

a Analytics Program, Data61, CSIRO, Australia
b Productive and Adaptive Livestock Systems, Agriculture and Food, CSIRO, Australia
c NSW Department of Primary Industries Beef Industry Centre, Australia

A R T I C L E I N F O

A B S T R A C T

Article history:

Received 21 June 2017

Received in revised form

17 October 2017

Accepted 18 October 2017

In this paper, we summarise the outcome of a set of experiments aimed at classifying cattle

behaviour based on sensor data. Each animal carried sensors generating time series

accelerometer data placed on a collar on the neck at the back of the head, on a halter posi-

tioned at the side of the head behind the mouth, or on the ear using a tag. The purpose of

the study was to determine how sensor data from different placement can classify a range

Available online 3 November 2017

of typical cattle behaviours. Data were collected and animal behaviours (grazing, standing

Keywords:

Sensor data analytics

Cattle behaviour classiﬁcation

Sensors for cattle behaviour tracking

or ruminating) were observed over a common time frame. Statistical features were com-

puted from the sensor data and machine learning algorithms were trained to classify each

behaviour. Classiﬁcation accuracies were computed on separate independent test sets. The

analysis based on behaviour classiﬁcation experiments revealed that different sensor

placement can achieve good classiﬁcation accuracy if the feature space (representing

motion patterns) between the training and test animal is similar. The paper will discuss

these analyses in detail and can act as a guide for future studies.

(cid:1) 2018 China Agricultural University. Publishing services by Elsevier B.V. This is an open
access article under the CC BY-NC-ND license (<http://creativecommons.org/licenses/by-nc->

nd/4.0/).

1.

Introduction

Animals alter their behaviour to enable them to deal with
stressors such as infection, satiety, or social and environmen-
tal changes. This behaviour is often consistent and pre-
dictable but cannot be measured at scale because of the
labour required to physically monitor large numbers of ani-
mals continuously. Wearable sensor technologies offer a pos-
sible solution to this problem enabling measurement at scale
but this can only be successful if sensor outputs can be

* Corresponding author.

interpreted accurately and in real time. Monitoring cattle
behaviour using wearable sensors is becoming an important
option for farm management and genetic selection programs
and a greater emphasis on individual wellbeing and perfor-
mance rather than a more traditional herd based approach.
Examples of precision agriculture (PA) management and
genetic improvement strategies are seen across the agricul-
tural spectrum including cropping [1,2], dairy/beef [3] and
the aquaculture industry [4–6].

In the livestock sector behaviour analysis can provide
insight into (i) Animal health: animal behaviour patterns
can be linked to animal health [9–13], an early detection of
sickness was identiﬁed when rumination and general activity
decreased below expected levels; (ii) Feed intake and satiety:

E-mail address: <ashfaqur.rahman@data61.csiro.au> (A. Rahman).
Peer review under responsibility of China Agricultural University.
<https://doi.org/10.1016/j.inpa.2017.10.001>
2214-3173 (cid:1) 2018 China Agricultural University. Publishing services by Elsevier B.V.
This is an open access article under the CC BY-NC-ND license (<http://creativecommons.org/licenses/by-nc-nd/4.0/>).

I n f o r m a t i o n P r o c e s s i n g i n A g r i c u l t u r e 5 ( 2 0 1 8 ) 1 2 4 – 1 3 3

125

behaviours like grazing, chewing and feeding are indicators of
feed intake. Percentage of time spent on grazing related beha-
viours can assist in understanding the amount of feed intake
compared to amount of pasture or supplements offered, ani-
mal preference and satiety state [14–16];
(iii) Heat/Estrus
event: this refers to the period of sexual receptivity and fertil-
ity in female mammals. The heat event has been shown to be
detectable through changes in restlessness (activity) [12]. The
detection of periods indicate the appropriate time for artiﬁcial
insemination.

Commercial and research systems presented in [9–21] con-
tinuously and automatically monitor the rumination time [9–
11], grazing time [10] and activity intensity [9–13] of individual
animals. Current behaviour monitoring systems are com-
monly comprised of: (a) an individual sensor or combination
of sensors that are ﬁtted to each animal (Fig. 1) - these sensors
can include accelerometers, magnetometer, gyroscope, com-
pass, GPS, pressure and microphone; (b) a sensor node to pro-
cess, store and transmit sensor observations; and (c) a model
or set of models [17,18] to infer an animal’s behaviour from
the raw sensor observations.

Sensors can be placed on different parts of the animal and
it is not known if, or how, location might inﬂuence classiﬁca-
tion accuracy. We therefore devised an experiment to better
understand how sensor placement inﬂuences behaviour clas-
siﬁcation accuracy? In this study, we collected data simulta-
neously from accelerometers placed on three different parts
of the animal body: neck (collar), head (halter) and ear (using
an ear tag). We developed separate behaviour classiﬁcation
models based on sensor data from these three locations. We
utilised two different testing approaches: (i) Training on data
from a set of animals and testing models on data from ani-
mals that are not part of the training process and (ii) Mix data
from all the animals, training on data on part of mixed data
set and testing models on data are not part of the training
process. Analysis results reveal that feature distribution

Fig. 1 – Collar, halter and ear tag sensors used for cattle
behaviour monitoring.

between training and test data is an important factor for
accurate behaviour classiﬁcation for any sensor placement.

2.

Feature extraction for classiﬁcation

In previous studies, machine learning based cattle behaviour
classiﬁers [17,18] employed a standard approach to model
development without considering the potential value of state
of the art classiﬁers and feature representations. The stan-
dard workﬂow (Fig. 2)
in developing behaviour models
involves partitioning time series data into short time win-
dows, and for each window, extracting a small set of statisti-
cal features (i.e. ﬁrst to fourth order statistical moments). The
combination of statistical features and corresponding beha-
viour annotations were used to train a classiﬁer. A set of sta-
tistical features were computed from the time series sensor
data in [19–21] and showed potential to classify cattle beha-
viour with high accuracy. In this study we computed statisti-
cal features only for classiﬁcation experiments.

An important step in a classiﬁcation framework (Fig.2) is
feature extraction. For the experiments conducted as part of
this study, a set of statistical features were computed from
the time and frequency representations associated with each
window of the input series. Frequency domain representa-
tions of the time series data were obtained using Discrete
Fourier Transformation (DFT). Let xt be the t(cid:1) th element of
the time series. In DFT k(cid:1) th element of the frequency
domain representation is obtained as:

¼

f k

Xn(cid:1)1

xte(cid:1)2pitk=n

t¼0

ð1Þ

where n is the length of the vector. The interpretation is that x
represents the signal level at various points in time and f rep-
resents the signal level at various frequencies. The DC com-
the DFT (f 0: component corresponding to 0
ponent of
frequency) is retained as a feature. The remaining statistical
features are then computed from the spectrum after its DC
component has been removed. The statistical features used
include the mean, standard deviation, skewness, and kurtosis
as presented in Table 1.

We also used minimum and maximum of the series xt and
f k as features (with k > 0). The standard deviation, minimum
and maximum features were used to represent the motion
intensity. Along with these features, the period of the signal
within each time window was computed in time domain
using the method presented in [6]. The period feature is
included because some behaviours, such as grazing, walking
and ruminating, have repetition within their motion patterns.
A total of fourteen statistical features were computed.

3.

Sensors for data collection

The results presented here are based on trial data collected at
FD McMaster Laboratory in Armidale, NSW, Australia in
November 2014. Accelerometer sensors were placed in a col-
lar, ear tag, and halter at the same time and data from these
three different sources. A video camera recorded the animal’s
behaviours. A domain expert coded the videos to identify a
range of time-stamped data from the three sources were

126

I n f o r m a t i o n P r o c e s s i n g i n A g r i c u l t u r e 5 ( 2 0 1 8 ) 1 2 4 – 1 3 3

Fig. 2 – Cattle behaviour classiﬁcation framework.

Table 1 – Features Computed from time and frequency domain representation of the signal.

Features

Mean

Standard Deviation

rT ¼

Skewness

Kurtosis

c

T

b

T

Time Domain
P

l

T

¼

q

t

xt
ﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ
P
ðxt (cid:1) l
Þ2
1
T
n
P
ﬃﬃﬃﬃﬃﬃﬃ
ðxt(cid:1)l
n(cid:1)1
P
T
t
ð
Þ2
ðxt(cid:1)l
P
T
ðxt(cid:1)l
P
T
t
ð
Þ2
ðxt(cid:1)l
T

Þ3
Þ3=2

t

t

Þ4
Þ2

¼ nðnþ1Þðn(cid:1)1Þ
ðn(cid:1)2Þðn(cid:1)3Þ

¼ n

p

n(cid:1)2

Frequency Domain

P

q

l
F

¼

rF ¼

p

¼ n

n(cid:1)2

k>0f k
ﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ
P
Þ2
ðf k
1
n
ﬃﬃﬃﬃﬃﬃﬃ
n(cid:1)1

(cid:1) l
F

k>0
P

(cid:1)l
F

(cid:3)
P

Þ3
(cid:4)
3=2

c
F

b
F

¼ nðnþ1Þðn(cid:1)1Þ
ðn(cid:1)2Þðn(cid:1)3Þ

ðf k
k>0
ðf k
(cid:1)l
P
P

k>0
(cid:3)

k>0

k>0

F

Þ2
ðf k
ðf k

(cid:1)l
F

Þ4
(cid:4)

2

(cid:1)l
F

Þ2

aligned to these behaviour labels and three different labelled
data sets were produced.

The devices deployed in this experiment were designed by
engineers within CSIRO’s Sensor Technology Group. Two
models were deployed. The ﬁrst model was the ‘‘Camazotz”
devices with two deployed on each animal, one on a halter
and the other in an ear tag. A detailed description of the
devices can be found in [7]. For this study, the accelerometers
(STMicroelectronics LSM303 3-axis accelerometer/magne-
tometer) were sampled at a frequency of 30 Hz. An ear tag
housing was 3D printed to hold the Camazotz and attached
to the left ear of the animal using industry standard tools.
For the halter mounted sensor, a housing was also printed
using a 3D printer and attached to the cheek strap of the hal-
ter using cable ties. The third, a Fleck device was housed in a
box attached to each animal by a collar. The accelerometer in
the CSIRO monitoring collars ([8]) was a piezoelectric micro-
electromechanical system (MEMS) chip containing a 3-axis
sensor
accelerometer and a 3-axis magneto-resistive
(HMC6343 Honeywell, Plymouth, MN).

The accelerometer chip was programmed to collect data at
a frequency of 12 Hz. The box containing the electronics was
located under the animal’s neck. The resulting data was
logged to an on board MicroSD card. At completion of the ﬁeld
experiment, all the devices were removed from the animals
and the MicroSD cards removed. The SD Cards were copied
to a computer and the stored data converted from binary for-
mat to ‘‘CSV” ﬁles, which include variables for date, time and
X/Y/Z accelerometer – referred to henceforth as the ‘‘Data Log
File” (DLF). A second data ﬁle, ‘‘Annotation File” (AF), was cre-
ated from ﬁeld observations of the animal behaviour while
wearing the devices. The AF ﬁle can also be created by a cus-
tom application (the AF APP) that allows an operator to code

behaviours while viewing video of the animal recorded in
the ﬁeld. Finally, the AF and the DLF are read by the machine
learning software to create the windows of data for each
behaviour type.

4.

Experimental setup

q

as:

computed

ﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ
þ acc2
þ acc2
acc2
z
y
x

Sensor data obtained from the accelerometer were utilised in
this experiment. The squared acceleration magnitude (accm)
accm ¼
, where
was
accx; accyandaccz are the three axes of the accelerometer. The
accm series was the only time series used to compute features.
Our previous study [?] on other cattle behaviour data sets
indicates that the squared acceleration magnitude is sufﬁ-
cient to pull to good classiﬁcation accuracy on the behaviours
studied in the paper. Hence we used squared acceleration
magnitude and computed features from that series.

Six behaviour classes were recorded during the ﬁeld trial:
Grazing, Resting, Walking, and Standing, Ruminating and
Other. Fig.3 summarises the distribution of different classes
from the three different sources. Note that Walking, Resting
and Other class have a small representation. We thus concen-
trated and developed classiﬁers on the Grazing, Standing and Rumi-
nating classes only. The accm series was partitioned into
windows of 200 samples and statistical
features were
extracted from each time window. Windows were extracted
20 samples apart along the time series. Fourteen statistical
features were computed from each time window. The fea-
tures were used to train the Random Forest [22] Classiﬁer that
produced best classiﬁcation results for our dataset. A random
forest is a collection of decision tree classiﬁers. Each decision
tree is generated from a random subset of the features. Given

I n f o r m a t i o n P r o c e s s i n g i n A g r i c u l t u r e 5 ( 2 0 1 8 ) 1 2 4 – 1 3 3

127

Fig. 3 – Class distribution from the data sets [collated from all animals] collected from sensors placed at collar, halter and ear tag.

a test sample, each decision tree in the forest produces a class
decision that are fused into a single decision using majority
voting. We used the WEKA [23] implementation. All experi-
ments were conducted in MATLAB.

A set of three binary classiﬁers were trained such that each
target behaviour was classiﬁed against a combined class of all
remaining behaviour classes. The classiﬁcation accuracies are
reported for each target class separately in the results section.
Binary classiﬁers are developed as often only one behaviour
class needs to be inferred for a particular management prac-
tice, and hence, multi-class classiﬁers are not always
required. If multiple behaviours need to be classiﬁed for a par-
ticular application, the corresponding set of binary classiﬁers
can be combined.

and

recall ¼

true positive
true positive þ false negative

ð4Þ

Replacing precision and recall in F-Score deﬁnition gives

us

F1 ¼ 2 (cid:3)

true positive
true positiveþfalse positive
true positive
true positiveþfalse positive

(cid:3)

þ

true positive
true positiveþfalse negative
true positive
true positiveþfalse negative

¼ 2 (cid:3)

true positive
2 (cid:3) true positive þ false negative þ false positive

ð5Þ

We used the above formula to compute the classiﬁcation

performance of the binary classiﬁers.

We measured the classiﬁcation accuracy using FScore.

5.

Results and analysis

FScore is deﬁned as:
F1 ¼ 2 (cid:3) precision (cid:3) recall
precision þ recall

precision and recall are deﬁned as:

precision ¼

true positive
true positive þ false positive

ð2Þ

ð3Þ

We conducted a series of experiments to ﬁnd an answer to the
research question posed in this paper. We tried to understand
how effectively different behaviours can be classiﬁed using
the statistical features computed from devices attached to
different locations on the animals head. We developed a
machine learning model for each behaviour separately i.e.

128

I n f o r m a t i o n P r o c e s s i n g i n A g r i c u l t u r e 5 ( 2 0 1 8 ) 1 2 4 – 1 3 3

we developed a binary classiﬁer for each behaviour where the
target behaviour became one class and the remaining beha-
viours combine into the other class. For all possible sensor
placements, we conducted two approaches to evaluate the
classiﬁcation performance:

(i) we conducted a second experiment using the N Fold
Stratiﬁed Cross Validation (SCV) approach. For each
data source, we combined the data from all the ani-
mals. We then split the data into N folds so that the
class distribution of the folds remain close to that of
the combined data set. After that, each fold becomes
a test set and the remaining folds combine into one
training set. The process was repeated where each fold
becomes a test set by turn and classiﬁcation accuracy
(FScore) is computed on each test set; and

(ii) Leave–Out–One–Animal

(LOOA) validation approach
where data from one animal becomes the test set and
data from the remaining animals combine into the
training set. Each animal becomes a test animal in turn
and classiﬁcation accuracy is computed on each test
set.

SCV enforces similarity between training and test set. The
idea behind the LOOA approach is to see how well such sim-
ilarity is maintained between the training–test set in a more
realistic environment and how it inﬂuences the classiﬁcation
accuracy.

We ﬁrst evaluated the performance of the binary classiﬁers
using the SCV approach. We computed the average accuracy
(FScore) over the folds. Table 2 presents the average FScore
computed on three different behaviours from different data
sources using SCV approach. We can observe two things:

(a) In general, halter data was classiﬁed with higher accu-

racy compared to collar and ear tag data.

(b) Classiﬁcation accuracy (FScore) is in general high.

We also evaluated the performance of the binary classi-
ﬁers using the LOOA validation approach. The average accu-
racy (FScore) was computed over the test sets. Table 3
presents the average FScore computed for three behaviours
from different devices using LOOA approach. We can observe
two things:

(a) In general halter data is classiﬁed with better accuracy

compared against collar and ear tag data.

(b) Classiﬁcation accuracy (FScore) is in general low.

Overall, classiﬁcation accuracy using the SCV approach
was better than the LOOA approach. To understand the differ-
ence in performance between the SCV and LOOA approaches,
we analysed a number of results. As data from halter showed
relatively better performance than from collar and ear tag
devices, we will conﬁne the discussion to the halter data
and the conclusions from the halter is applicable to the other
device locations.

Class distribution differences between training and test
sets across multiple folds was investigated ﬁrst. Fig.4 presents
the Training set and Test set class distribution between the tar-
get and other class while validating using the LOOA approach.
In general, the class distribution between training and test set
do not match very well. Also, note that the Training set class
distribution for Standing and Ruminating class is imbalanced.
As concluded in [24], classiﬁcation accuracy measures like
FScore can be biased if there is a mismatch between class dis-
tribution between training and test data set. This becomes
even more critical if the class distribution is imbalanced
[24]. This partly explains the poor performance of the LOOA
approach. The class distribution between training and test
set is almost the same when using the SCV approach (Fig.5).
This explains one of the possible reasons for the performance
difference between the SCV and LOOA approach.

The second issue we investigated is how the feature space
distributions of the training and test sets vary using the SCV
and LOOA approaches. Fig.6 and Fig.7 present the Bhat-
tacharya distance [25] between the training and test distribu-
tions across the fourteen features using LOOA and SCV
approaches, respectively. It is clear that feature distributions
match very closely between training and test data in SCV
leading to a low Bhattacharya distance (Fig.7). There is a
higher mismatch between the training and test set feature
distribution when using LOOA leading to a higher Bhat-
tacharya distance (Fig.6). Generally, machine learning models
require training and test feature distributions to be similarly
distributed in order for classiﬁcation to be successful. Conse-
quently, the greater mismatch in the feature space distribu-
the LOOA approach (compared with the SCV
tions of
approach)
classiﬁcation
performance.

contributes

poorer

its

to

To ﬁnd out what can be done to improve the classiﬁcation
accuracy of the LOOA approach and what happens under an
identical situation with the SCV approach, another set of
experiments were conducted. For each training–test scenario,
a learning curve was constructed. A learning curve reveals the
classiﬁcation performance relationship between the training
and test data set as more training samples are added for

Table 2 – FScore Summary using Stratiﬁed Cross Validation.

Collar
Halter
Ear Tag

Grazing

0.809
0.914
0.805

Standing

0.874
0.89
0.86

Ruminating

0.913
0.932
0.895

I n f o r m a t i o n P r o c e s s i n g i n A g r i c u l t u r e 5 ( 2 0 1 8 ) 1 2 4 – 1 3 3

129

Table 3 – FScore Summary using Leave Out One Animal validation.

Collar
Halter
Ear Tag

Grazing

0.3596
0.7967
0.4808

Standing

0.4342
0.5096
0.3675

Ruminating

0.149
0.6211
0.1704

Fig. 4 – Class Distribution between training and test animals while using LOOA approach on Halter data stream. Here Cxxx
represents the ID of the test animal.

Fig. 5 – Class Distribution between training and test animals while using SCV approach on Halter data stream.

model generation. The learning curve provides insight into
the model’s suitability for a classiﬁcation task, in particular,
if the model is suffering from bias (under ﬁtting) or variance
(over ﬁtting). This informs the developer what needs to be
done to improve the model. We ﬁrst construct a learning

curve for the model developed with the SCV approach. Fig.8
presents the learning curve of a representative fold using
the Halter data set. Note that under identical class distribu-
tion, the training error is very low across all sample sizes,
while the test error is monotically decreasing with training

130

I n f o r m a t i o n P r o c e s s i n g i n A g r i c u l t u r e 5 ( 2 0 1 8 ) 1 2 4 – 1 3 3

Fig. 6 – Feature distribution difference between training and test set for different behaviour classes using the LOOA approach.
In the 2D histograms, the x–axis presents the 14 features and y-axis presents the 10 bins for each feature. Each feature is
normalised in the range of 0–1 and are split in 10 equal range bins [0–0.1], [0.1–0.2],. . ., [0.9–1]. Each bin in the y–axis
represents the concentration of values of a feature in that bin w.r.t. other bins for that feature. The concentrations are
displayed using a heat map and the colour code on the right of each histogram donates the level of concentration. The
Bhattacharyya distance between the training and test 2D histograms are presented at the bottom for each behaviour.

Fig. 7 – Feature distribution difference between training and test set for different behaviour classes using the SCV approach.
In the 2D histograms, the x–axis presents the 14 features and y-axis presents the 10 bins for each feature. Each feature is
normalised in the range of 0–1 and are split in 10 equal range bins [0–0.1], [0.1–0.2],. . ., [0.9–1]. Each bin in the y–axis
represents the concentration of values of a feature in that bin w.r.t. other bins for that feature. The concentrations are
displayed using a heat map and the colour code on the right of each histogram donates the level of concentration. The
Bhattacharyya distance between the training and test 2D histograms are presented at the bottom for each behaviour.

I n f o r m a t i o n P r o c e s s i n g i n A g r i c u l t u r e 5 ( 2 0 1 8 ) 1 2 4 – 1 3 3

131

Fig. 8 – Learning curve on Fold 1 (representative fold) using the SCV approach on Halter data.

sample size. The test error often approaches zero as more
training samples are added. This suggests the classiﬁer is well
behaved and does not require modiﬁcation.

While using LOOA validation, Fig.9 presents the learning
curves for some folds (animals) while using the Halter data
set. Note that as we add more training data there is a big
gap between training and test data set error when compared
against Fig.8. This suggests the model is suffering from a vari-
ance problem. The possible reasons are:

(a) The machine learning models have been over-trained

(suffering from overﬁtting problem),

(b) The feature set is not representative of the particular

classiﬁcation problem.

If we compare the learning curve of the SCV approach that
has been developed under an identical scenario (i.e. same
type of model and feature set) the classiﬁcation error of the
SVC appears to be signiﬁcantly smaller than the LOOA
approach with an identical numbers of training samples.
The SVC based classiﬁer is both accurate and well behaved
suggesting that (i) the model has not overﬁt the classiﬁcation
problem and (ii) its feature set is representative of the classi-
ﬁcation problem. This suggests when motion data from the
same steer are included in both the training and test sets,
the feature set is representative. However, when the training
and test sets consist of different cattle, as in the case of the

LOOA validation, the feature set does not appear to generalise
between cattle. The source of motion pattern (as represented
by the features) variation between the cattle can be
attributed to differences in the physical movement of
individuals and minor differences in IMU positioning
(whether this occurs during deployment or the IMU shifts
position after deployment).

In summary, when comparing the classiﬁcation perfor-
mance of different sensor placements, the key issue is the
similarity of feature space distribution between training and
test animals. When tested on a different animal (LOOA valida-
tion), the feature spaces are not similar between training and
test set resulting in poor classiﬁcation performance for all
sensor placements. When feature space distribution is
enforced using SCV approach, classiﬁcation performance on
test set was very high for all sensor placements. Note that sta-
tistical features were good enough to secure high classiﬁca-
tion accuracy with SCV approach. Thus simple features can
do well if the feature space is similar between training and
test set for any sensor placement (i.e. collar, halter, and ear
tag).

6.

Conclusions

In this paper, we studied cattle behaviour classiﬁcation using
machine learning algorithms from collar, halter and ear tag
sensor data. We conducted a series of experiments using

132

I n f o r m a t i o n P r o c e s s i n g i n A g r i c u l t u r e 5 ( 2 0 1 8 ) 1 2 4 – 1 3 3

Fig. 9 – Learning Curve on some folds (i.e. animals) using the LOOA approach on Halter data. Here C xxx represents the animal
ID of the individual animal. A missing square means no test data was available for that animal.

two validation approaches under the same model develop-
ment conditions; Leave–Out–One–Animal (LOOA) and Strati-
ﬁed Cross Validation (SCV). In LOOA the class and feature
distribution between the training and test data sets were
found to be quite dissimilar resulting in poor behaviour clas-
siﬁcation performance. With SCV, both the class and feature
distribution between the training and test data sets were
quite similar resulting in a far higher classiﬁcation accuracy.
The source of the performance difference between the SCV
and LOOA based classiﬁers was related to the motion varia-
tions across different cattle for the same behaviour.

From the results obtained in this study (Table 3), none of
the sensor placements revealed high classiﬁcation accuracy
because of lack of correspondence between feature space of
training and test set (in a practical setup with LOOA). How-
ever, when feature space correspondence is enforced (using
the SCV), all sensor placements lead to high classiﬁcation
accuracy (Table 2). This suggests that the performance of
machine learning based behaviour models improve if there
is similarity in cattle motion distribution (i.e. feature space)
for any sensor placement (i.e. collar, halter, and ear tag).

In a practical deployment of cattle behaviour models, the
LOOA is likely to be the most realistic validation approach.
It is expected that we would develop models based on histor-
ical data collected from a set of animals and then test them
on a different set of animals in a new trial. To deal with the

feature distribution variance that degrade performance when
applying classiﬁer to new animals, alternative/reduced fea-
ture representation and Transfer Learning approaches need
to be investigated. Transfer learning is an active research area
in machine learning [26–29] that involves algorithm develop-
ment for the improvement of learning in a new task through
the transfer of knowledge from a related task that has already
been learned. In future, we will investigate such approaches
to attempt to reduce the discrepancy between training and
test distributions by learning feature representations that
offer greater invariance across different cattle (domain
adaptation).

R E F E R E N C E S

[1] Seelan SK, Laguette S, Casady G, Seielstad G. Remote sensing
applications for precision agriculture: a learning community
approach. Remote Sensing Environ 2003;88(12):157–69.

[2] McBratney AB, Whelan BM, Shatar T. Variability and

uncertainty in spatial, temporal and spatio-temporal crop
yield and related data. In: Lake JV, Bock GR, Goode JA, editors.
Precision agriculture: spatial and temporal variability of
environmental quality. England: Wiley & Sons; 1997. p.
141–60.

[3] Berckmans D. Automatic on-line monitoring of animals by
precision livestock farming. In: Proc. ISAH Conference on

I n f o r m a t i o n P r o c e s s i n g i n A g r i c u l t u r e 5 ( 2 0 1 8 ) 1 2 4 – 1 3 3

133

Animal Production in Europe: The Way Forward in a
Changing World. Saint-Malo, France; 2004. p. 27–31.
[4] Mallekh R, Lagarde JP, Eneau JP, Clotour C. An acoustic

detector of turbot feeding activity. Aquaculture 2003;221(1–
4):481–9.

[5] Rahman A, Shahriar MS, D’Este C, Smith G, McCulloch J,

Timms G. Time–series prediction of shellﬁsh farm closure: a
comparison of alternatives. Elsevier Inform Process Agric
2014;1(1):42–51.

[6] Hellicar A, Rahman A, Smith D, Smith G, McCulloch J,
Andrewartha S, et al. An algorithm for the automatic
detection of heart rate and variability for an oyster sensor.
IEEE Sens J 2015;15(8):4480–7.

[7] Jurdak R, Kusy B, Sommer P, Kottege N, Crossman V,

McKeown A, et al. Camazotz: multimodal activity-based GPS
sampling. In: Proc. 12th International Conference on
Information Processing in Sensor Networks (IPSN).
Philadelphia, USA; 2013. p. 67–78.

[8] Gonza´ lez LA, Bishop-Hurley G, Handcock RN, Crossman C.
Behavioural classiﬁcation of data from collars containing
motion sensors in grazing cattle. Comput Electron Agric
2015;110:91–102.

[9] Allﬂex. Cow Intelligence. link: <<http://www>.

scrdairy.com/cow-intelligence>; 2016.

[10] CowManager. The Cow Manager System. link: <https://

<www.cowmanager.com/en-us/>>; 2017.

[11] Dairymaster. Moo Monitor. link: <http://

<www.dairymaster.com/heat-detection/>>; 2017.

[12] Shahriar MS, Smith D, Rahman A, Freeman M, Hills J,

Rawnsley R, et al. Detecting heat events in dairy cows using
accelerometers and unsupervised learning. Elsevier Comput
Electron Agric 2016;128:20–6.

[13] iCEROROTiCS. CowAlert. link: <<http://www.icerobotics.com/>

products/#cowalert>; 2017.

[14] Greenwood PL, Valencia P, Overs L, Paull DR, Purvis IW. New
ways of measuring intake, efﬁciency and behaviour of
grazing livestock. Animal Prod Sci 2014;54:1796–804.

[15] Greenwood PL, Bishop-Hurley GJ, Gonzalez LA, Ingham AB.
Development and application of a livestock phenomics
platform to enhance productivity and efﬁciency at pasture.
Animal Prod Sci 2016;56:1299–311.

[16] Greenwood PL, Paull DR, McNally J, Kalinowski T, Ebert D,
Little B, et al. Use of sensor-determined behaviours to
develop algorithms for pasture intake by individual grazing
cattle. Crop Pasture Sci 2016. <https://doi.org/10.1071/CP16383>.

[17] Robert JB, White B, Renter D, Larson R. Evaluation of three-

dimensional accelerometers to monitor and classify
behaviour patterns in cattle. Comput Electron Agric 2009;67
(1–2):80–4.

[18] Gonzalez LA, Bishop-Hurley GJ, Handcock R, Crossman C.
Behavioural classiﬁcation of data from collars containing
motion data. Comput Electron Agric 2015;110:91–102.

[19] Smith D, Dutta R, Hellicar A, Bishop-Hurley GJ, Rawnsley R,
Henry D, et al. Bag of Class Posteriors, a new multi-variate
time series classiﬁer applied to animal behaviour
identiﬁcation. Expert Syst Appl 2015;42(7):3774–84.
[20] Smith D, Little B, Greenwood PL, Valencia P, Rahman A,

Ingham AB, et al. A study of sensor derived features in cattle
behaviour classiﬁcation models. In: Proc. IEEE Sensors.
Busan, Korea; 2015, doi: <https://doi.org/10.1109/ICSENS.2015>.
7370529.

[21] Rahman A, Smith D, Henry D. Rawnsley R. A comparison of
autoencoder and statistical features for cattle behaviour
classiﬁcation. In: Proc. IEEE Joint International Conference on
Neural Networks (IJCNN). Vancouver, Canada; 2016. p. 2954–
60.

[22] Breiman L. Random Forests. Mach Learn 2001;45(1):5–32.
[23] Hall M, Frank E, Holmes G, Pfahringer B, Reutemann P, Witten

IH. The WEKA data mining software: an update. ACM
SIGKDD Explorat Newsl 2009;11(1):10–8.

[24] Forman G, Scholz M. Apples-to-apples in cross-validation

studies: pitfalls in classiﬁer performance measurement. ACM
SIGKDD Explorat Newsl 2010;12(1):49–57.

[25] Derpanis KG. The bhattacharyya measure. Link: <http://
<www.cse.yorku.ca/~kosta/CompVis_Notes/bhattacharyya>.
pdf>; 2017.

[26] Ben-David S, Blitzer J, Cramer K, Pereira F. Analysis of

representations for domain adaptation. In: Proc Conference
on Neural Information Processing Systems (NIPS).
Cambridge; 2007. p. 137–44.

[27] Bengio Y, Courville A, Vincent P. Representation learning: a
review and new perspectives. IEEE Trans Pattern Anal Mach
Intell 2013;35(8):1798–828.

[28] Glorot X, Bordes A, Bengio Y. Domain adaptation for large-

scale sentiment classiﬁcation: a deep learning approach. In:
Proc. International Conference on Machine Learning (ICML).
Belluvue, Washington; 2011. p. 97–110.

[29] Pan SJ, Yang Q. A survey on transfer learning. IEEE Trans

Knowl Data Eng 2010;22(10):1345–59.
