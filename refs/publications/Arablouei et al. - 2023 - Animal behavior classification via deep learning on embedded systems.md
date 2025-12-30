Contents lists available at ScienceDirect

Computers and Electronics in Agriculture

journal homepage: <www.elsevier.com/locate/compag>

Original papers

Animal behavior classification via deep learning on embedded systems
Reza Arablouei a,∗, Liang Wang b, Lachlan Currie a, Jodan Yates a, Flavio A.P. Alvarenga c,
Greg J. Bishop-Hurley b
a Data61, CSIRO, Pullenvale QLD 4069, Australia
b Agriculture and Food, CSIRO, St Lucia QLD 4067, Australia
c NSW Department of Primary Industries, Armidale NSW 2350, Australia

A R T I C L E I N F O

A B S T R A C T

Keywords:
Animal behavior classification
Artificial intelligence of things
Deep learning
Embedded machine learning
Embedded systems
Inertial measurements
Sensor network
Wearable artificial intelligence

We develop an end-to-end deep-neural-network-based algorithm for classifying animal behavior using ac-
celerometry data on the embedded system of an artificial intelligence of things (AIoT) device installed in a
wearable collar tag. The proposed algorithm jointly performs feature extraction and classification utilizing
a set of infinite-impulse-response (IIR) and finite-impulse-response (FIR) filters together with a multilayer
perceptron. The utilized IIR and FIR filters can be viewed as specific types of recurrent and convolutional
neural network layers, respectively. We evaluate the performance of the proposed algorithm via two real-world
datasets collected from total eighteen grazing beef cattle using collar tags. The results show that the proposed
algorithm offers good intra- and inter-dataset classification accuracy and outperforms its closest contenders
including two state-of-the-art convolutional-neural-network-based time-series classification algorithms, which
are significantly more complex. We implement the proposed algorithm on the embedded system of the utilized
collar tags’ AIoT device to perform in-situ classification of animal behavior. We achieve real-time in-situ
behavior inference from accelerometry data without imposing any strain on the available computational,
memory, or energy resources of the embedded system.

1. Introduction

The term behavior is commonly used by animal scientists to describe
what an animal does during its daily life. It defines the internally
coordinated responses of living organisms to internal or external stim-
uli (Levitis et al., 2009). Animal behavior, when considered over ap-
propriate periods of time, is an important indicator of health, welfare,
and productivity, particularly for livestock. It can also provide valuable
information about animals’ environment, social interactions, and herd
dynamics.

Manual observation and recording of animal behavior is laborious
and in some cases impractical. In addition, employing machine learning
algorithms based on computer vision or sound recognition to automate
animal behavior classification is challenging. That is because, apart
from the technical challenges involved, the limited coverage range of
typical fixed vision or sound sensors makes them unsuitable for mon-
itoring large numbers of animals spread over large areas. Therefore,
classifying animal behavior on wearable devices, such as small and
light smart tags, using inertial measurement data is highly desirable.
Micro-electro-mechanical accelerometers are compact and low-power
motion sensors that can measure acceleration on three orthogonal
spatial axes by sensing minute variations in the capacitance between

a fixed electrode and a proof mass due to any force applied to the
sensor. There is a vast body of literature around using accelerometry
data to classify various animal behaviors, e.g., see Williams et al.
(2019), Rahman et al. (2018), Smith et al. (2016), Mattachini et al.
(2016), Dutta et al. (2015), González et al. (2015), Vázquez Dios-
dado et al. (2015), Hamalainen et al. (2011), Andriamandroso et al.
(2016), Kamminga et al. (2018), Sakaia et al. (2019), Barker et al.
(2018), Haladjian et al. (2018), Brandes et al. (2021), Arablouei et al.
(2021), Busch et al. (2017), Kamminga et al. (2017b), Suresh et al.
(2018), le Roux et al. (2018), Kamminga et al. (2017a), Dominguez-
Morales et al. (2021), Gutierrez-Galan et al. (2018) and the references
therein. However, there is relatively little work reported on perform-
ing the behavior classification on the embedded system of the de-
vice containing the accelerometer, e.g., Arablouei et al. (2021), Busch
et al. (2017), Kamminga et al. (2017b), Suresh et al. (2018), le Roux
et al. (2018), Kamminga et al. (2017a), Dominguez-Morales et al.
(2021) and Gutierrez-Galan et al. (2018), as most of the processing is
conventionally done after collecting the data.

Collecting and storing raw accelerometry data for post-hoc process-
ing is inefficient and unscalable. Transferring the raw data via wireless

∗ Corresponding author.

E-mail address: <reza.arablouei@csiro.au> (R. Arablouei).

<https://doi.org/10.1016/j.compag.2023.107707>
Received 6 March 2022; Received in revised form 4 September 2022; Accepted 11 September 2022

ComputersandElectronicsinAgriculture207(2023)107707Availableonline16February20230168-1699/©2023TheAuthor(s).PublishedbyElsevierB.V.ThisisanopenaccessarticleundertheCCBY-NC-NDlicense(<http://creativecommons.org/licenses/by-nc-nd/4.0/>).R. Arablouei et al.

communication is similarly disadvantageous. Therefore, it is important
to realize the classification of animal behavior in-situ and in real-
time on the embedded system of the wearable device that collect the
data. Doing so, only the inferred behavior classes need be stored or
communicated.

In this paper, we develop a deep-neural-network-based supervised
machine-learning algorithm to classify animal behavior using accelero-
metry data on the embedded system of a custom-built artificial intelli-
gence of things (AIoT) device that can be worn by cattle and similar
livestock as a collar tag. The proposed algorithm can effectively be
used for behavior inference on the embedded system of the AIoT device
without straining its computational, memory, or energy resources.

Most existing animal behavior classification algorithms are con-
ventional feature-engineering-based approaches that involve separate
feature extraction and classification processes. It is common to take
various time- and frequency-domain statistics and measures as features,
for example, mean, standard deviation, skewness, kurtosis, maximum
value, minimum value, autocorrelation, median, median absolute de-
viation, dominant frequency, and entropy. Some other rather ad-hoc
values, such as the so-called overall dynamic body acceleration and
vectorial dynamic body acceleration (Nathan et al., 2012), have also
been used as features. The main drawback of such approaches is that
the features are pre-defined regardless of the classifier used and need
be carefully engineered and hand-picked possibly through a suitable
feature selection method. The engineered features are also often limited
in flexibility and utility.

Our new animal behavior classification algorithm is composed of
two main processes that can be viewed as performing feature calcu-
lation and classification. However, it enjoys end-to-end learning since
the feature calculation process contains learnable parameters that are
trained jointly with the parameters of the classifier. Therefore, the
algorithm does not rely on any hand-engineering of the features as it
learns them directly from the data.

The proposed algorithm extracts meaningful and computationally
efficient features that facilitate classification of animal behavior in-situ
and in real-time on the embedded system of the collar tag’s AIoT device.
To this end, in the proposed algorithm, we use a set of first-order
infinite-impulse-response (IIR) Butterworth high-pass filters and a set of
nonlinear filters composed of two linear finite-impulse-response (FIR)
filters joined by tangent hyperbolic nonlinear activation. To enable
end-to-end learning of the deep neural network model defining the
proposed algorithm, we make the parameters of the utilized IIR and
FIR filters learnable. We design the proposed algorithm with the aim
of performing inference using the learned models on the embedded
system of the collar tag’s AIoT device. Therefore, we take into account
the computational, memory, and energy constraints of the embedded
system.

We carry out model training on a suitable computing device using
a deep-learning library where we implement the IIR and FIR filters
employed for feature calculation as specific recurrent and convolutional
neural networks, respectively. We then deploy the learned model on
the embedded system using a library provided by the microcontroller
manufacturer.

We evaluate the performance of the proposed algorithm using
two real-world datasets containing accelerometry data collected from
grazing beef cattle and annotated manually. The proposed algorithm
exhibits excellent intra- and inter-dataset classification accuracy and
outperforms two state-of-the-art convolutional-neural-network(CNN)-
based algorithms recently proposed for end-to-end classification of
time-series with a considerably smaller time and memory complexity.
We also provide some insights into how the proposed algorithm
works by analyzing the statistical and spectral properties of the ac-
celerometry data and the characteristics of the extracted features.

Table 1
Weather summary statistics during the experiments at Armidale NSW.

condition

time

August 2018

March 2020

average maximum temperature
average minimum temperature
highest maximum temperature
lowest minimum temperature

maximum relative humidity
minimum relative humidity

15.7 ◦C
−1.9 ◦C
20.6 ◦C
−7.6 ◦C

89%
48%

22.3 ◦C
11.5 ◦C
28.6 ◦C
3.6 ◦C

91%
55%

average pressure

1018 mbar

1017 mbar

average daily rainfall
average daily pan evaporation

0.9 mm
2.3 mm

1.9 mm
2.9 mm

overall

2. Data

dry, sunny, and
frosty with cool
days and cold nights

warm, cloudy, and
damp with mostly
light falls of rain

In this section, we describe the procedures and tools used to gen-
erate two datasets that we consider in this work, i.e., data collection
experiments, utilized hardware, annotation process, and data segmen-
tation.

2.1. Experiments

We have obtained our datasets from grazing beef cattle of Angus
breed during two data collection experiments ran in August 2018
and March 2020. The first experiment took place in August 2018
for 28 days at the Commonwealth Scientific and Industrial Research
Organisation (CSIRO) FD McMaster Laboratory Pasture Intake Facil-
ity (Greenwood et al., 2014), Chiswick NSW, Australia (30◦36′28.17′′S,
151◦32′39.12′′E). The accelerometry data was collected from ten steers
wearing collar tags called eGrazor.1 The steers were 23 to 35 months
of age and weighed 530 to 816 kg. We refer to the associated dataset
as Arm18. Another experiment was conducted in March 2020 for eight
days at the same facility while the accelerometry data was recorded
from eight heifers wearing the eGrazor collar tags. The heifers were
19 months old and weighed 283 to 354 kg. We refer to the associated
dataset as Arm20. In Table 1, we provide summary statistics of the
weather conditions for the periods that the experiments took place at
Armidale, NSW, Australia.2

In both experiments, the cattle wore the collar tags uninterruptedly.
Therefore, the eGrazor collar tags logged the accelerometry data con-
tinuously for the entire duration of the experiments. At the conclusion
of each experiment, we retrieved the SD flash memory cards, which
stored the logged data, from the tags. There was no concern around the
storage capacity as, with a sampling rate of 50 readings per second, a
32 GB memory card can accommodate the IMU data of about 400 days.
Fig. 1(a) shows the paddock and the cattle used for the experiment
that produced the Arm20 dataset. Fig. 1(b) shows cattle wearing the
eGrazor collar tags. The experiments were approved by the CSIRO
FD McMaster Laboratory Chiswick Animal Ethics Committee with the
animal research authority numbers 17/20 and 19/18.

2.2. eGrazor

During the experiments, we fitted the cattle with our eGrazor collar
tags that are purpose-built to capture, log, and process various sensor
data including inertial measurement, temperature, pressure, and geo-
location using the global navigation satellite system (GNSS). The tag,

1 <https://www.csiro.au/en/research/animals/livestock/egrazor-measuring->

cattle-pasture-intake

2 <http://www.weatherarmidale.com/>

ComputersandElectronicsinAgriculture207(2023)1077072R. Arablouei et al.

shown in Fig. 1(c), houses an artificial intelligence of things (AIoT)
device called Loci, a battery pack, and six photovoltaic modules for
harvesting solar energy. We place the tag on top of the animal’s neck
and secure it with a strap and a counterweight.

Loci, shown in Fig. 1(d), contains a wealth of sensing and communi-
cation capabilities. It has a Texas Instruments CC2650F128 system-on-
chip that consists of an Arm Cortex-M3 CPU running at 48 MHz with
28 KB of random access memory (RAM), 128 KB of read-only memory
(ROM), and a 802.15.4 radio module. Loci also has an MPU9250 9-axis
micro-electro-mechanical (MEMS) inertial measurement unit (IMU) in-
cluding a tri-axial accelerometer sensor that measures acceleration in
three orthogonal spatial directions (axes) as shown in Fig. 1(b). The 𝑥
axis corresponds to the antero-posterior (forward/backward) direction,
the 𝑦 axis to the medio-lateral (horizontal/sideways) direction, and
the 𝑧 axis to the dorso-ventral (upward/downward) direction. The
IMU chip outputs the tri-axial accelerometer readings as 12-bit signed
integers at a rate set to 50 samples per second. The raw accelerometer
readings can be processed by the on-board microcontroller or recorded
on an external flash memory card.

The power to Loci is supplied by the 3.6 V, 13.4 Ah Lithium-ion
battery pack that is recharged via six solar panels installed on the
exterior of the tag case. Loci draws a maximum current of 30 mA even
when the CPU and all other main components including the GNSS
receiver runs continuously. Therefore, the tag can operate normally for
at least 18 days using the battery pack’s full capacity with no recharge.
In practice, the battery pack is recharged for several hours almost every
day with solar panels providing up to 300 mA in total.

2.3. Annotations

We have annotated parts of the collected accelerometry data by
monitoring the behavior of the cattle on the field during the 2018
experiment and viewing the video recordings of the 2020 experiment.
We use the annotations to create our labeled datasets called Arm18
and Arm20 corresponding to the respective data collection experiments
as detailed above. We consider six mutually-exclusive behaviors of
grazing, walking, ruminating, resting, drinking, and other in the Arm18
dataset. We consider the same behaviors in the Arm20 dataset except
for combining the ruminating and resting behaviors to a single behavior
class referred to as ruminating/resting. We combine the ruminating and
resting behaviors to a single behavior class in the Arm20 dataset as it
is hard to clearly distinguish these behaviors in the recorded videos.
The other behavior class is the collection of all behaviors other than
the considered ones, i.e., grazing, walking, ruminating, resting, and
drinking.

We consider the above cattle behaviors as they are the most im-
portant behaviors from the perspective of evaluating and monitoring
productivity, feed efficiency, energetic dynamics, health, and welfare of
grazing cattle. For example, the knowledge of the times and durations
of a cattle’s grazing is crucial for determining its herbage dry matter
intake from the pasture (Smith et al., 2021). knowing when and for
how long a cattle ruminates or rests can also help understand the health
and well-being state of the animal (Schirmann et al., 2012). Monitoring
the walking behavior can be useful for measuring the animal’s energy
expenditure while identifying the drinking behavior is essential to
ascertain the animal’s access to water and hence compliance with
associated regulations. It is also important to note that grazing cattle,
particularly beef cattle, spend vast majority of their lives performing
the considered behaviors.

We have produced our annotations partially via observing the ani-
mals during the trials and partially via reviewing the recorded videos.
Annotating animal behavior is generally arduous and challenging. Par-
ticularly, it is not uncommon to overlook some instances of rare be-
haviors such as drinking, even for a domain expert, as they happen
occasionally and in short durations. Differentiating some behaviors
such as ruminating and resting can also be difficult.

Fig. 1. The experiment paddock containing cattle wearing eGrazor collar tags and
images of eGrazor and its AIoT device, Loci, used for collecting accelerometry data
corresponding to cattle behavior.

ComputersandElectronicsinAgriculture207(2023)1077073R. Arablouei et al.

Table 2
The number of labeled 256-sample segments (datapoints) in the considered datasets for
each behavior class.

dataset

Arm18

6588
65
2502
3126
104
178

12563

Arm20

6156
910

4080

594
222

11962

total

12744
975

9708

698
400

24525

behavior

grazing
walking
ruminating
resting
drinking
other

total

2.4. Datasets

We create the labeled Arm18 and Arm20 datasets by dividing the
relevant annotated accelerometry data into non-overlapping segments
each containing 256 consecutive triaxial readings, which are unique to
the segment. The segment size of 256 readings corresponds to about
5.12 s. Table 2 shows the number of segments (datapoints) for each
behavior class in each dataset.

To determine the optimal segment size, we experimented with vari-
ous values. The results show that the segment size of 256 accelerometer
readings (5.12 s) leads to a good balance between different competing
aspects of performance, i.e., classification accuracy and time/space
complexity. Larger segment sizes correspond to finer resolution in
the frequency domain that may help better recognize subtle differ-
ences between the classes through IIR/FIR filtering. In addition, as the
accelerometer readings are considerably noisy, calculating statistical
features aggregated over longer segments can help filter out the un-
certainty induced by noise more effectively. However, larger segment
sizes result in fewer datapoints being available for training as well as
higher computational and memory complexity of performing inference
on each datapoint.

3. Algorithm

We take an end-to-end learning approach in developing our animal
behavior classification algorithm. The conventional feature-engineer-
ing-based approaches involve separate feature engineering and classifi-
cation processes. However, to achieve end-to-end learning, we propose
an algorithm that calculates relevant features and performs classifica-
tion in conjunction. The algorithm uses trainable parameters for both
feature calculation and classification, which can be optimized jointly
during training.

Since we aim to realize animal behavior inference on the embedded
system of Loci, we take into consideration its resource limitations in
designing the underlying model of our animal behavior classification
algorithm that maps triaxial accelerometry data to animal behavior
classes. In Fig. 2, we sketch the architecture of our proposed end-to-end
animal behavior classification model. The input to the model consists
of 256 contiguous triaxial accelerometer readings and the output is the
predicted animal behavior class, when performing inference. During
training, the argmax operator in Fig. 2 is replaced with the sof tmax
operator, whose output is used to calculate the associated cross-entropy
loss.

The proposed model has two major parts, namely feature calcula-
tion and behavior classification. The main components of the feature
calculation part are a set of linear high-pass IIR filters, a set of nonlinear
filters each composed of two FIR filters and an element-wise hyperbolic
tangent (tanh) activation function, and corresponding mean and mean-
absolute aggregation functions, which we will elaborate on in the
following. The behavior classification part is made of a multilayer
perceptron (MLP).

3.1. Normalization

We stack the triaxial accelerometer

into three 𝑁-
dimensional vectors, denoted by 𝐚𝑥, 𝐚𝑦, and 𝐚𝑧. Recall that, in this
work, we set 𝑁 = 256. Each vector contains the accelerometer readings
pertaining to one spatial axis, i.e., 𝑥, 𝑦, or 𝑧, as signified by the
associated index.

readings

During training, we calculate the mean and standard-deviation of
the accelerometer readings for each axis using the entire training
data. We then normalize the accelerometer readings of each axis by
subtracting the corresponding mean from them and dividing the result
by the corresponding standard-deviation during both training and infer-
ence. Therefore, we express the normalized values of the accelerometer
readings as

̄𝐚𝑑 = 𝑠𝑑

(𝐚𝑑 − 𝑚𝑑 𝟏) , 𝑑 ∈ {𝑥, 𝑦, 𝑧}

where 𝑚𝑑 and 𝑠𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, are the means and the inverse standard-
deviations, respectively.

3.2. Calculation of features

We average the entries of ̄𝐚𝑑 for each axis 𝑑 ∈ {𝑥, 𝑦, 𝑧} to produce

three features, i.e., the mean features, as

𝑓1𝑑 =

1
𝑁

𝟏⊺ ̄𝐚𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}

(1)

where 𝟏 stands for a column vector of appropriate size with all entries
being one. As the accelerometers sense the gravity of earth, the mean
features contain information about the orientation of the collar tag or
equivalently the pose of animal’s head.

To eliminate the effect of gravity after calculating the mean features,
we filter the normalized values of the accelerometer readings of each
axis using a first-order high-pass Butterworth filter that has a single
adjustable parameter 𝛾𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}. These IIR filters remove the
low-frequency components of the normalized accelerometer readings
of each axis to the extent determined by the value of 𝛾𝑑 . We denote the
application of the utilized IIR filters by

[

1, −𝛾𝑑

]⊺

∗ ̃𝐚𝑑 = [1, −1]⊺ ∗ ̄𝐚𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}

(2)

where ̃𝐚𝑑 is the filter output and ∗ denotes the linear convolution oper-
ation. Although this notation is somewhat unorthodox, it a meaningful
time-domain representation of a first-order high-pass Butterworth filter
that highlights its recurrent nature and hence infinite impulse response
without relying on any frequency-domain notation. The convolution
on the left hand-side represents the recurrence and is required for
the equality to hold. In practice, the entries of ̃𝐚𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, are
calculated through recursive operations as described in Arablouei et al.
(2021).

We compute the second set of features by averaging the absolute
values of the high-pass-filtered accelerometer readings for each axis,
i.e.,

𝑓2𝑑 =

1
𝑁

𝟏⊺

|̃𝐚𝑑 |, 𝑑 ∈ {𝑥, 𝑦, 𝑧}.

(3)

These features contain information about the intensity of the animal’s
body movements. We use the mean-absolute value as a surrogate for
the standard-deviation since it is more computationally-efficient and
robust to noise or outliers.

The features 𝑓1𝑑 and 𝑓2𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, are similar to the ones used
in Arablouei et al. (2021) but are different in two major aspects. First,
here, the IIR filter parameters 𝛾𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, are specific to each axis
while, in Arablouei et al. (2021), the same parameter is used for all
axes. Second, unlike in Arablouei et al. (2021) where the parameter of
the IIR filters is treated as a hyperparameter, in this work, we consider
𝛾𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, to be trainable parameters whose optimal values can
be learned from the data via training.

ComputersandElectronicsinAgriculture207(2023)1077074R. Arablouei et al.

Fig. 2. The architecture of the model underlying the proposed animal behavior classification algorithm when performing inference. During training, the argmax operator is replaced
with the sof tmax operator.

To enhance the discriminative power of the proposed model, we
extract three additional features from the high-pass-filtered accelerom-
eter readings ̃𝐚𝑑 . Thus, we pass them through a set of nonlinear filters
each consisting of two tandem FIR filters with an element-wise tanh
activation function in between. We then calculate the mean-absolute
of the nonlinear filter outputs as the third set of features, i.e.,

performing inference with any trained model using the proposed algo-
rithm, we choose the behavior class that has the highest corresponding
MLP output.

We summarize the procedure of performing inference using the pro-
posed algorithm together with the involved parameters and variables
in Algorithm 1.

𝑓3𝑑 =

1
𝑁

𝟏⊺

| tanh

(̃𝐚𝑑 ∗ 𝐡1𝑑

)

∗ 𝐡2𝑑 |, 𝑑 ∈ {𝑥, 𝑦, 𝑧}

(4)

4. Evaluation

where 𝐡1𝑑 ∈ R𝐾1×1 and 𝐡2𝑑 ∈ R𝐾2×1 represent the impulse responses of
the utilized FIR filters for each axis 𝑑 ∈ {𝑥, 𝑦, 𝑧} with lengths 𝐾1 and 𝐾2,
respectively. We treat these impulse responses as trainable parameter
vectors.

Similar to the second set of features 𝑓2𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, the third set
of features 𝑓3𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, also contain information regarding the
intensity of animal’s body movements that are sensed by the accelerom-
eters. However, the movements whose intensity is captured through
𝑓3𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, relate to specific parts of the frequency spectrum
ascertained by the FIR filter coefficients, which are learned directly
from the data. Here, we consider a single set of nonlinear filters and
consequently one set of the associated features. However, extending
the proposed algorithm to include more nonlinear filters in parallel and
thus more features is straightforward.

We stack the calculated features, i.e., 𝑓𝑖,𝑑 , 𝑖 ∈ {1, 2, 3} & 𝑑 ∈ {𝑥, 𝑦, 𝑧},

in the feature vector denote by 𝐟.

3.3. Classification

We feed the feature vector 𝐟 into to an MLP that outputs 𝐶 numbers
each corresponding to one behavior class. The employed MLP classifier
has one hidden layer that is followed by the rectified linear unit (ReLU)
activation function. Therefore, the output layer produces

𝐖2 max

(𝟎, 𝐖1𝐟 + 𝐛1

)

+ 𝐛2

(5)

where 𝟎 denotes a vector of appropriate size with all zero entries,
𝐖1 ∈ R𝐿×𝐹 and 𝐛1 ∈ R𝐿×1 are the weight matrix and the bias vector of
the hidden layer, 𝐖2 ∈ R𝐶×𝐿 and 𝐛2 ∈ R𝐶×1 are the weight matrix and
the bias vector of the output layer, 𝐹 is the number of features, 𝐿 is the
dimension of the hidden layer output, and 𝐶 is the number of classes.
During training, we use the sof tmax operator to transform the output
of the MLP to the pseudo-likelihoods of the considered behavior classes,
which are used to calculate the associated cross-entropy loss. When

We evaluate both intra-dataset and inter-dataset classification per-
formance of the proposed algorithm using our labeled datasets and
appropriate cross-validation schemes. We also tune the hyperparame-
ters of the proposed algorithm in each scenario through cross-validation
and a greedy method.

We use the Matthews correlation coefficient (MCC) (Matthews,
1975) for evaluating the classification accuracy. The MCC takes into
account true and false positives and negatives and is known to be a
meaningful measure even when the dataset is highly imbalanced. It
falls between −1 and +1 where +1 is perfect prediction, 0 no better
than random prediction, and −1 perfect inverse prediction.

We jointly optimize the feature calculation parameters (the IIR and
FIR filter coefficients), i.e., 𝛾𝑑 , 𝐡𝑑1, and 𝐡𝑑2, 𝑑 ∈ {𝑥, 𝑦, 𝑧}, and the MLP
classifier parameters, i.e., 𝐖1, 𝐛1, 𝐖2, and 𝐛2. To this end, we imple-
ment the proposed model and train it using the PyTorch library.3 We
use an approach similar to the one taken in Kuznetsov et al. (2020) to
implement the IIR filters with differentiable parameters. To implement
the FIR filters, we use one-dimensional convolution operations with no
bias or padding and set the stride to one and the number of groups to
the number of input channels, i.e., three.

4.1. Intra-dataset accuracy

We consider three datasets for evaluating the intra-dataset clas-
sification accuracy of the proposed algorithm. They are the original
six-class Arm18 and five-class Arm20 datasets plus a five-class version
of the Arm18 dataset. We create the five-class Arm18 dataset by
combining the ruminating and resting behavior classes of the original
dataset into a single ruminating/resting behavior class. Hence, we
make a version of the Arm18 dataset that has the same behavior

3 <https://pytorch.org/>

ComputersandElectronicsinAgriculture207(2023)1077075R. Arablouei et al.

Algorithm 1: The inference procedure using the proposed algorithm and
the involved parameters and variables.

Table 3
The model and training hyperparameters of the proposed algorithm and their values
used with each considered dataset.

input, ∀𝑑 ∈ {𝑥, 𝑦, 𝑧}:

𝐚𝑑 ∈ R𝑁×1

output:

vectors of accelerometer readings

hyperparameter

𝑐 ∈ {0, … , 𝐶 − 1}

predicted behavior class index

parameters, ∀𝑑 ∈ {𝑥, 𝑦, 𝑧}:

𝑁 ∈ Z+
𝐾1, 𝐾2 ∈ Z+
𝐹 ∈ Z+
𝐿 ∈ Z+
𝐶 ∈ Z+
𝑚𝑑 ∈ R
𝑠𝑑 ∈ R+
0 ≤ 𝛾𝑑 ∈ R+ ≤ 1
𝐡1𝑑 ∈ R𝐾1×1, 𝐡2𝑑 ∈ R𝐾2×1
𝐖1 ∈ R𝐿×𝐹 , 𝐖2 ∈ R𝐶×𝐿
𝐛1 ∈ R𝐿×1, 𝐛2 ∈ R𝐶×1

variables:
𝐟 ∈ R𝐹 ×1

segment length
FIR filter lengths
number of features
hidden layer dimension
number of classes
normalization means
normal. inverse standard-deviations
IIR filter coefficients
FIR filter impulse responses
MLP weights
MLP biases

features

inference procedure:

normalize, ∀𝑑 ∈ {𝑥, 𝑦, 𝑧}:

̄𝐚𝑑 = 𝑠𝑑

(𝐚𝑑 − 𝑚𝑑 𝟏)
calculate features, ∀𝑑 ∈ {𝑥, 𝑦, 𝑧}:

𝟏⊺ ̄𝐚𝑑

𝑓1𝑑 = 1
𝑁
∗ ̃𝐚𝑑 = [1, −1]⊺ ∗ ̄𝐚𝑑
𝑓2𝑑 = 1
𝟏⊺
𝑓3𝑑 = 1

|̃𝐚𝑑 |

| tanh

𝟏⊺

𝑁

𝑁

(̃𝐚𝑑 ∗ 𝐡1𝑑

)

∗ 𝐡2𝑑 |

[

1, −𝛾𝑑

]⊺

classify:

𝑐 = arg max

(𝐖2 max

(𝟎, 𝐖1𝐟 + 𝐛1

)

+ 𝐛2

)

classes as the Arm20 dataset. This facilitates performance evaluation
and comparison, especially, in the next subsection where we perform
inter-class performance accuracy evaluation.

To evaluate the classification accuracy of the proposed algorithm
with each considered dataset, we use a leave-one-animal-out cross-
validation scheme. In each cross-validation fold of this scheme, we
use the data of one animal for validation and the data of the other
animals for training. We aggregate the results of all folds to calculate
the cross-validated results.

We compare the accuracy of the proposed algorithm with those of
four other algorithms, namely, a variant of the proposed algorithm that
uses a set of linear FIR filters to calculate 𝑓3𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, i.e.,

1st FIR filter length, 𝐾1
2nd FIR filter length, 𝐾2
hidden layer dimension, 𝐿

learning rate
weight decay
batch size
number of training iterations

dataset

Arm18
6 classes

8
8
7

0.0005
0.004
1024
40,000

Arm18
5 classes

8
8
6

0.0002
0.002
1024
60,000

Arm20

8
8
6

0.0002
0.002
1024
60,000

Table 4
The leave-one-animal-out cross-validated MCC values of the proposed algorithm and its
contenders, evaluated using the considered datasets.

algorithm

proposed
proposed with linear filters
Arablouei et al. (2021)
FCN
ResNet

dataset

Arm18
6 classes

0.9097
0.9014
0.8713
0.8804
0.9028

Arm18
5 classes

0.9568
0.9467
0.9466
0.9415
0.9478

Arm20

0.8762
0.8681
0.8662
0.8713
0.8728

Table 5
The leave-one-animal-out cross-validated MCC values of the proposed algorithm for
each behavior class and each considered dataset.

behavior

grazing
walking
ruminating
resting
drinking
other

overall

dataset

Arm18
6 classes

0.9802
0.6897
0.8906
0.8826
0.5962
0.3721

0.9097

Arm18
5 classes

0.9780
0.7280

0.9758

0.5556
0.4075

0.9568

Arm20

0.9118
0.8485

0.9099

0.7166
0.4038

0.8762

we use the hyperparameter values prescribed in Fawaz et al. (2019),
which are shown to be almost optimal.

In Table 4, we present the cross-validated MCC results for all
considered algorithms and datasets. As evident in Table 4, the pro-
posed algorithm yields the highest MCC values compared to the other
algorithms for all considered datasets. In Table 5, we provide the cross-
validated MCC values of the proposed algorithm for each behavior class
and dataset. Fig. 3 shows the confusion matrices associated with the
proposed algorithm and all considered datasets.

𝑓3𝑑 =

1
𝑁

𝟏⊺

|̃𝐚𝑑 ∗ 𝐡𝑑 |, 𝑑 ∈ {𝑥, 𝑦, 𝑧},

(6)

4.2. Inter-dataset accuracy

the MLP-based algorithm of Arablouei et al. (2021), and two CNN-
based time-series classification algorithms proposed in Wang et al.
(2017) and called the fully convolutional network (FCN) and the resid-
ual network (ResNet). It is shown in Fawaz et al. (2019) that FCN and
ResNet are among the most accurate existing time-series classification
algorithms, specifically those based on deep learning.

We utilize the Adam algorithm (Kingma and Ba, 2015) to opti-
mize the cross-entropy loss associated with the multiclass classification
problem. We tune the model and training hyperparameters of the
proposed algorithm for each dataset in conjunction with our leave-
one-animal-out cross-validation procedure. We list the hyperparameters
and their tuned values for each dataset in Table 3. We use the same
hyperparameter values as in Table 3 for the variant of the proposed
algorithm with linear FIR filters. For the FCN and ResNet algorithms,

Here we further assess how well a model learned using the proposed
algorithm is generalizable to unseen data, i.e., data on which the model
is not trained. Therefore, we evaluate the inter-dataset classification
accuracy of the proposed algorithm using the five-class Arm18 and
Arm20 datasets. We use the proposed algorithm to learn a behavior
classification model from one dataset and evaluate it on the other
dataset.

In Table 6, we give the overall MCC values as well as those corre-
sponding to each behavior for both cases of (1) training the proposed
model on the Arm20 dataset and evaluating it on the five-class Arm18
dataset and (2) training the proposed model on the five-class Arm18
dataset and evaluating it on the Arm20 dataset. We use the same
hyperparameter values as in Table 3, which are in fact the same for
both cases.

ComputersandElectronicsinAgriculture207(2023)1077076R. Arablouei et al.

Table 6
The cross-dataset MCC values of the proposed algorithm, overall and for each behavior
class, using the five-class Arm18 and Arm20 datasets.

MCC

training dataset, test dataset

Arm20, Arm18

Arm18, Arm20

grazing
walking
ruminating/resting
drinking
other

overall

0.9688
0.6866
0.9588
0.5285
0.2921

0.9393

0.8820
0.6423
0.8620
0.5903
0.3408

0.8034

Fig. 4 shows the confusion matrices corresponding to the cross-
dataset evaluation of the proposed algorithm using the five-class Arm18
and Arm20 datasets.

Inspecting the results in Tables 5 and 6 shows that the models
learned from both datasets generalize well to the other dataset. How-
ever, the model learned from the Arm20 dataset appears to perform
better on the five-class Arm18 dataset, as opposed to the alternative.
This can be due to a few factors.

First, the proportion of the less frequent classes, specifically the
walking and drinking behavior classes, are significantly higher in the
Arm20 dataset. Therefore, a model learned from the Arm20 dataset
is expectedly more effective in classifying these behavior classes com-
pared to a model learned from the Arm18 dataset. As seen, the clas-
sification accuracy of the walking and drinking behavior classes in
the Arm20 dataset degrades considerably when a model learned from
the five-class Arm18 dataset is used compared to when inter-dataset
cross-validation is performed.

Second, accurate classification of the behavior classes in the Arm20
dataset appears to be more challenging compared with the five-class
Arm18 dataset. This is evident from the intra-class results. Thus, classi-
fying the Arm20 dataset using a model learned from a different dataset
leads to a more noticeable loss in accuracy compared to classifying the
five-class Arm18 dataset using an inter-dataset model.

4.3. Complexity

To perform in-situ classification of cattle behavior in real time, we
implement the proposed algorithm on the embedded system of Loci
using the Digital Signal Processing software library of Arm’s Com-
mon Microcontroller Software Interface Standard (CMSIS). CMSIS is
a vendor-independent hardware abstraction layer for microcontrollers
that are based on Arm Cortex processors.4 Particularly, we make use
of the arm_biquad_cascade_df1_f32 and arm_fir_f32 func-
tions to respectively implement the IIR and FIR filters of the proposed
model. In Table 7, we give the number of parameters for the main parts
of the proposed animal behavior classification algorithm, i.e., normal-
ization, feature calculation, and classification. In addition, in Table 7,
we provide the number of different arithmetic/mathematical opera-
tions required for performing inference using the proposed algorithm
on a single datapoint (accelerometer readings of an 𝑁-sample time
window). The table also includes the total tally for each row when
𝑁 = 256, 𝐾1 = 𝐾2 = 8, 𝐹 = 9, 𝐿 = 7, and 𝐶 = 6.

We provide the numbers related to the actual runtime complexity
of performing inference on a single datapoint using the proposed
algorithm in Table 8. In this table, “text” and “rodata” refer to the
ROM space occupied by the algorithm code and the model parameters,
respectively. In addition, “stack” refers to the RAM space required to
store all variables when running the algorithm.

As shown in Table 8, performing inference using the proposed
animal behavior classification algorithm takes 85 ms of the CPU time.

Fig. 3. The confusion matrices resulting from the leave-one-animal-out cross-validated
evaluation of the proposed algorithm with each considered dataset.

4 <https://developer.arm.com/tools-and-software/embedded/cmsis>

ComputersandElectronicsinAgriculture207(2023)1077077R. Arablouei et al.

Table 7
The number of parameters and the number of different operations required for performing inference on a single datapoint using the proposed animal behavior classification
algorithm. The total values are for when 𝑁 = 256, 𝐾1 = 𝐾2 = 8, 𝐹 = 9, 𝐿 = 7, and 𝐶 = 6.

complexity

parameters

additions/subtractions
absolute value calculations
multiplications
tanh evaluations
ReLU operations
argmax operations

stage

normalization

feature calculation

6

3𝑁
0
3𝑁
0
0
0

3(𝐾1 + 𝐾2 + 1)

9𝑁 + 3(𝑁 − 𝐾1 + 2)𝐾1 + 3(𝑁 − 𝐾1 − 𝐾2 + 2)𝐾2 − 18
3(2𝑁 − 𝐾1 − 𝐾2 + 2)
3𝑁 + 3(𝑁 − 𝐾1 + 1)𝐾1 + 3(𝑁 − 𝐾1 − 𝐾2 + 2)𝐾2 + 6
3(𝑁 − 𝐾1 + 1)
0
0

classification

𝐿(𝐹 + 𝐶) + 𝐶 + 𝐿

𝐿𝐹 + 𝐶𝐿
0
𝐿𝐹 + 𝐶𝐿
0
𝐿
1

total

175

14,967
1494
13,431
747
7
1

ROM and 10 KB of RAM while the microcontroller of Loci has access
to 128 KB of flash ROM and 28 KB of RAM. Therefore, the memory
requirements can be easily met.

We have verified our implementation of the proposed animal be-
havior classification algorithm on the embedded system of Loci using
models trained on the Arm18 and Arm20 datasets during a small-scale
field trial conducted with Angus beef cows in February 2022. The
proposed algorithm ran smoothly in real time predicting the behavior
of the cattle with a classification accuracy similar to those presented in
Table 6.

At inference time, i.e., when using the proposed algorithm to clas-
sify cattle behavior in situ, we infer the animal behavior for every
window of 256 consecutive accelerometer readings (5.12 s) that slides
forward for 64 values (1.28 s) as the new readings arrive. Therefore,
the algorithm outputs the predicated behavior class every 1.28 s for the
last 5.12 s. We count the inferred instances of each behavior class over
a period of about five and half minutes (256 by 1.28 s or 327.68 s).
We then transmit these count numbers for all behaviors to a gateway
from each collar tag. This way, we avoid the costly transmission of the
raw data when only the summary knowledge of animal behavior over
a given time is of interest.

Each collar tag directly communicated with a gateway using a
Semtech SX12725 long-range low-power LoRa6 modem. The communi-
cation takes place at the frequency band of 916 MHz with a bandwidth
of 125 kHz and an effective range of about 3 km. In most related
application scenarios, the cattle are usually within less than 3 km of a
gateway. The gateway is also a Loci bundled with a BeagleBone7 single-
board computer that is connected to a remote server via a suitable
wired or wireless link.

The payload at each round of communication that occurs every
327.68 s includes six bytes for the behavior inference counts, four byte
for the timestamp, and two bytes for the node ID number. Transmitting
this information takes up to 1.3189 s while the LoRa modem draws a
current of 125 mA. With a duty cycle of around 0.4%, due to operating
for 1.3189 s every 327.68 s, this amounts to an average current draw
of about 0.5 mA.

We aggregate the number of inferred instances for each behavior
class over every 327.68 s to optimize the efficiency of the communi-
cation. It is the longest period for which the inference counts for each
behavior class can fit into a single byte. A shorter period will require
more frequent communication while a longer period will entail a larger
communication payload because of requiring the transmission of two or
more bytes for each behavior inference count.

The CPU and all other major components of Loci including the LoRa
modem draw at most 30 mA on average. Therefore, the battery pack of
the eGrazor collar tag with a nominal capacity of 13.4 Ah can power
Loci for several weeks before needing to be recharged by the solar pan-
els, which can provide up to 300 mA. Therefore, running the classifier
and transmitting the summary knowledge of the inferred behaviors do
not impose any significant burden on the available resources of Loci’s
embedded system.

Fig. 4. The confusion matrices resulting from the cross-dataset evaluation of the
proposed algorithm for both considered cases.

This means the inference can be conveniently executed every one

second. In addition, the total required memory is less than 12 KB of

5 <https://www.semtech.com/products/wireless-rf/lora-core/sx1272>
6 <https://lora-alliance.org/>
7 <https://beagleboard.org/bone>

ComputersandElectronicsinAgriculture207(2023)1077078R. Arablouei et al.

Table 8
The actual memory and time complexity of the proposed animal behavior classification
algorithm running on the embedded system of Loci, the eGrazor collar tag’s AIoT
device.

text

10,880 bytes

rodata

708 bytes

stack

9,550 bytes

CPU time

85 ms

Note that the memory and time complexity of performing inference
using the FCN and ResNet algorithms on a single datapoint is a few
orders of magnitude larger compared with that of the proposed al-
gorithm. For example, the FCN models whose MCC results are given
in Section 4.1 have a few hundred thousand parameters taking up
several megabyte of memory. In addition, a forward pass of the FCN
algorithm to perform inference on a single datapoint requires around
68 million multiplication operations. The memory and time complexity
of performing inference using the ResNet algorithm is more than double
that of the FCN algorithm.

5. Interpretation

We provide some insights into the proposed animal behavior clas-
sification algorithm, particularly, the features that it extracts from the
triaxial accelerometer readings in an end-to-end manner by analyzing
the statistical and spectral properties of the data and their relationships
with the features. We choose the Arm20 dataset for this purpose as it
is less unbalanced compared with the Arm18 dataset in terms of the
prevalence of different behavior classes.

5.1. Features

In Fig. 5, we plot the histograms of the normalized accelerometer
readings, i.e., ̄𝐚𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, for each behavior class and spatial
axis. Each dashed vertical line in Fig. 5 indicates the mean value of
its corresponding behavior class with the same color.

We observe in Fig. 5 that the means corresponding to different
behavior classes, especially those for the 𝑥 axis, are rather distinct.
Therefore, they can be useful for discriminating the behavior classes.
The mean values are directly related to the orientation of the tag and
hence the head pose of the animal wearing the tag. Considering the
behaviors of interest, the head pose can carry significant information
in regards to the animal’s behavior. The mean features, i.e., 𝑓1𝑑 , 𝑑 ∈
{𝑥, 𝑦, 𝑧}, are meant to capture this information.

In Fig. 6, we plot the amplitude spectral density (ASD) functions
of the normalized and IIR-filtered accelerometer readings, i.e., ̃𝐚𝑑 , 𝑑 ∈
{𝑥, 𝑦, 𝑧}, for all behavior classes and spatial axes. The ASDs are averaged
over all datapoints (𝑁-sample segments) of the Arm20 dataset. The
ASD function is the square-root of the power spectral density function.
It represents how the power of the accelerometer readings within the
𝑁-sample segments are on-average distributed over the spectral range
of zero to 25 Hz (the Nyquist frequency that is half of the sampling
frequency) for each behavior class and axis.

Fig. 6 shows that the overall power of the IIR-filtered accelerometer
readings (with the effect of gravity/head pose removed) can be a good
distinguishing factor for most behavior classes. We use the features 𝑓2𝑑 ,
𝑑 ∈ {𝑥, 𝑦, 𝑧}, to capture this information that relates to the intensity of
animal’s body movements. We use the mean-absolute value instead of
the standard deviation to quantify the power because of its superior
numerical properties such as being less computationally demanding
and more robust to noise and outliers.

In Fig. 7, we plot the ASD of the nonlinear-filtered accelerometer

readings that are used to calculate 𝑓3𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, i.e.,

̌𝐚𝑑 = tanh

(̃𝐚𝑑 ∗ 𝐡1𝑑

)

∗ 𝐡2𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧},

Fig. 5. The histograms of the normalized accelerometer readings of the Arm20 dataset
for each class and spatial axis.

(7)

for all behavior classes and spatial axes when the model parameters are
learned for the Arm20 dataset.

ComputersandElectronicsinAgriculture207(2023)1077079R. Arablouei et al.

Fig. 6. The amplitude density functions of the normalized and IIR-filtered accelerom-
eter readings for all behavior classes and spatial axes, averaged over all datapoints of
the Arm20 dataset.

We make two major observations from Fig. 7. First, the ruminat-
ing/resting and drinking behavior classes have similar overall powers
in the 𝑧 axis for pre-nonlinear-filtered accelerometer readings as seen
in Fig. 6(c), specifically in comparison with the other classes. However,
after the nonlinear filtering, as shown in Fig. 7(c), the filtered values
associated with the two behavior classes have substantially different
total powers. This means 𝑓3𝑧 can help distinguish the drinking behavior
from the ruminating/resting behavior and consequently from the other
behaviors. Note that drinking is a relatively rare behavior and gen-
erally hard to classify accurately. Second, the high-frequency spectral
components of the accelerometer readings, i.e., over 10 Hz, appear to
be mostly suppressed by the nonlinear filters trained on the Arm20
dataset to classify animal behavior. This is justifiably beneficial as the
considered cattle behaviors are expected to have acceleration signa-
tures that predominately fall in the frequency range lower than 10 Hz.
The higher-frequency components are most likely due to observational
noise/error.

In Fig. 8, we plot the frequency responses of the learned FIR filters,
i.e., 𝐡1𝑑 and 𝐡2𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}. The inclusion of these plots is only
for the sake of illustration as the FIR filters in the proposed algorithm
form a set of nonlinear filters together with the utilized element-wise
tanh activation function. Frequency response is undefined for these
nonlinear filters, which result in the filtered values with the ASD
functions shown in Fig. 7.

5.2. Feature space

To gain more insights into the inner-workings of the proposed
algorithm, we visualize the feature space associated with the Arm20
dataset in two embedding dimensions using the 𝑡-distributed stochastic
neighbor embedding (tSNE) algorithm (van der Maaten and Hinton,
2008). To this end, we calculate the features, i.e., 𝑓𝑖,𝑑 , 𝑖 ∈ {1, 2, 3} &
𝑑 ∈ {𝑥, 𝑦, 𝑧}, for the entire Arm20 dataset using the parameters of a
model trained on the same dataset to classify its behavior classes. The
tSNE algorithm preserves the local structure of the subspace constituted
by the features while projecting it onto a lower-dimensional space. It
does not necessarily preserve the global structure of the data.

Fig. 9(a) is a visualization of the feature space of the Arm20 dataset
using all nine features while Fig. 9(b) is another visualization using
only the first six features, i.e., 𝑓1𝑑 , 𝑓2𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}. Each dot in Fig. 9
represents a datapoint and is colored according to its corresponding
behavior class. It is clear from Figs. 9(a) and 9(b) that the additional
three features, i.e., 𝑓3𝑑 , 𝑑 ∈ {𝑥, 𝑦, 𝑧}, help datapoints belonging to
the same class cluster around each other better hence facilitate the
classification and improve accuracy. This is more prominent for the less
frequent behavior classes, i.e., walking, drinking, and other.

In Fig. 9(c), we visualize the feature space of the Arm20 dataset
when the nine features are calculated using a model trained on the
Arm18 dataset. The clusters corresponding to different behavior classes
are similarly distinguishable in Figs. 9(a) and 9(c). This can partially
explain the favorable inter-dataset generalizability of the proposed
model observed in Section 4.2.

6. Discussion

The work presented in this paper is a continuation of our previous
work in Arablouei et al. (2021) that improves it in several aspects.
First and foremost, our approach here is based on end-to-end learning
where the feature extractor parameters are optimized jointly with the
classifier parameters. In Arablouei et al. (2021), feature extraction and
classification are done separately. Moreover, in this work, we use three
new features that help enhance performance, particularly by facilitating
the classification of less frequent behaviors such as drinking. Unlike
in Arablouei et al. (2021), here, we also normalize the accelerometer
readings before calculating the features using them. This improves the
classification accuracy as well as the training speed.

ComputersandElectronicsinAgriculture207(2023)10770710R. Arablouei et al.

Fig. 8. The frequency responses of the FIR filters associated with all spatial axes in
the proposed algorithm, learned from the Arm20 dataset.

We use a single set of IIR and nonlinear filters to calculate the
features in the proposed algorithm. However, it is straightforward to ex-
tend the proposed algorithm to calculate more features using multiple
sets of filters. In our experiments with the considered datasets, we did
not find any significant improvement in classification accuracy when
using more filters. We did not observe any benefit in using nonlinear
filters that have more than two FIR filters in tandem either. Nor did we
witness any benefit in having more than one hidden layer in the MLP
classifier.

In the proposed algorithm, we treat the accelerometer readings of
three spatial axes independently; hence, the FIR filters are akin to
depthwise convolutions with no bias. We have considered using two-
dimensional convolutions or adding pointwise convolutions to take
into account possible inter-channel information. However, despite the
significant increase in complexity, there was no gain in classification
accuracy. Addition of bias to the FIR filters was not beneficial either.
We have considered using batch normalization, dropout regulariza-
tion, and skip connections in the model underpinning the proposed

Fig. 7. The amplitude density functions of the normalized and filtered accelerometer
readings for all classes and axes, averaged over all datapoints of the Arm20 dataset.

ComputersandElectronicsinAgriculture207(2023)10770711R. Arablouei et al.

Fig. 9. Visualization of the Arm20 dataset in the feature space using the tSNE
algorithm.

algorithm or its training. However, none led to any improvement in
the classification accuracy.

The tanh activation function used within the nonlinear filters of
the proposed algorithm results in substantially higher classification
accuracy compared with using ReLU or sigmoid (logistic) activation
functions. However, its implementation on embedded systems is re-
source intensive. In future work, we will consider replacing it with
a less complex approximation or implementing it more efficiently
without incurring any significant loss of accuracy.

The proposed algorithm does not show any sign of overfitting to
the considered datasets when using the hyperparameter values given
in Table 3. On the other hand, the FCN and ResNet algorithms overfit
in every scenario regardless of the choice of the hyperparameter values
as they are large enough to memorize the uninformative and irrelevant
patterns in the training data that are likely due to noise or nuisance
factors. Therefore, when training these CNN-based model, we treat
the number of training iterations as a hyperparameter and tune it
through cross-validation. We do not need to limit the number of the
training iterations of the proposed model to prevent it from overfitting
the training set in our experiments with the considered datasets. The
iteration numbers in Table 3 indicate when the convergence occurs and
further training does not reduce the aggregate cross-entropy loss.

Modularity and flexibility of the modern deep neural networks,
enabled by their layered structure that can incorporate nonlinear func-
tions and transformations, have led to their widespread successful
use in several applications that demand learning approximations to
complex nonlinear mapping functions. However, the advantages of
the deep neural networks come at the expense of high nonlinearity
and nonconvexity of the associated optimization objective functions.
This has made it practically impossible to analyze the performance of
deep learning models theoretically or predict their accuracy from an
analytical point of view (Goodfellow et al., 2016). Interpreting deep
learning models and explaining their performance are areas of active
research (Molnar, 2020).

In Section 5, we attempt to interpret the underlying deep neural
networks architecture of the proposed algorithm and explain how
works. Explaining alternate architectures that are outperformed by the
proposed algorithm and why that is the case is hard if possible at all.
Therefore, we only present and examine the performance of the pro-
posed algorithm and suffice with mentioning some notable alternatives,
which we have investigated, in the above paragraphs. Architectural
hyperparameters, such as the number of layers, the number of filters
in each layer, and the type of activation functions, are generally de-
termined through cross-validation and limited, often greedy, search in
the space of feasible hyperparameter values. Finding the optimal values
for the hyperparameters is impractical as it requires combinatorial
optimization with typically prohibitive time and space complexity.

Learning animal behavior classification models that perform well
on rare behavior classes such as drinking is intrinsically challenging.
This is mainly because the amount of training data available for such
behaviors is limited. The annotation of these behaviors is also hard
as they may be overlooked or mistaken due to occurring sporadically
and in short intervals. Some grazing cattle may not drink water from
any water trough for several days depending on the circumstances.
When a classifier is learned from data that does not represent the entire
subspace corresponding to some classes, its accuracy and confidence
will inevitably be affected adversely, particularly, with respect to the
inadequately characterized classes.

Paucity of data for uncommon behavior classes makes the training
dataset highly imbalanced. This is certainly unideal. However, in our
experience, the class imbalance is not the main culprit for inferior ac-
curacy of classifying the rare behaviors. Rather, the scarcity of training
data for these behavior classes is to be blamed. We have explored
using various methods for balancing our datasets, such as undersam-
pling, oversampling, weighting the datapoints by the inverse of the
frequency of their associated classes, and synthesizing new datapoints

ComputersandElectronicsinAgriculture207(2023)10770712R. Arablouei et al.

using the synthetic minority oversampling technique (Chawla et al.,
2002). However, we have not observed any meaningful improvement
in classification accuracy using models learned from the resultant ar-
tificially balanced datasets. Learning accurate classification models for
rare behaviors is a subject of our ongoing research.

In our current implementation of the proposed algorithm on the
embedded system of Loci, we use 32-bit floating-point parameters and
variables and performs all the required mathematical operations with
these numbers using the corresponding floating-point operations. In
future work, we will consider using quantization to reduce the number
of floating-point operations and consequently accelerate the in-situ
inference procedure.

In our annotated datasets, each datapoint belongs to only one
behavior class for the entirety of its temporal dimension. On the other
hand, at inference time, during every consecutive 256 accelerometry
readings or 5.12 s, the animal may not necessarily exhibit a single
behavior as it inevitably switches between behaviors at arbitrary oc-
casions. The ratio of time segments over which inference is performed
while more than one behavior occur can be decreased using a smaller
segment size. However, in practice, such instances cannot be eliminated
for being a fundamental limitation of performing inference on segments
of any time-series data. One potential way to tackle this limitation is
to use running statistics instead of time-windowed statistics. Another
possible way is through running an online time-series change detec-
tion algorithm alongside the behavior classification algorithm. We will
study these possible alternative solutions and the associated challenges
and opportunities in our future research.

7. Conclusion

We developed a new algorithm for animal behavior classification
using triaxial accelerometry data. The proposed model can be trained
in an end-to-end manner and implemented on the embedded system of
our purpose-built AIoT device to perform animal behavior classification
in situ and in real time. The proposed algorithm computes three sets
of features that capture information from triaxial accelerometry data
regarding the animal behavior in insightful ways. It uses an MLP to
classify the calculated features. When evaluated using two datasets
collected via real-world animal trials, the proposed algorithm delivers
classification accuracy that is superior to that of two state-of-the-art
CNN-based classifiers while it incurs substantially lower memory and
time complexity.

CRediT authorship contribution statement

Reza Arablouei: Methodology, Software, Writing. Liang Wang:
Software. Lachlan Currie: Software, Data collection. Jodan Yates:
Software, Data collection. Flavio A.P. Alvarenga: Data collection.
Greg J. Bishop-Hurley: Conceptualization, Project administration.

Declaration of competing interest

The authors declare that they have no known competing finan-
cial interests or personal relationships that could have appeared to
influence the work reported in this paper.

Data availability

Data will be made available on request.

Acknowledgment

This research was undertaken with strategic investment funding
from the CSIRO and NSW Department of Primary Industries. We would
like to thank the following technical staff who were involved in the re-
search at CSIRO FD McMaster Laboratory Chiswick: Alistair Donaldson
and Reg Woodgate with NSW Department of Primary Industries, and
Jody McNally and Troy Kalinowski with CSIRO Agriculture and Food.

References

Andriamandroso, A., Bindelle, J., Mercatoris, B., Lebeau, F., 2016. A review on the use
of sensors to monitor cattle jaw movements and behavior when grazing. Biotechnol.
Agron. Soc. Environ. 20 (S1), 273–286.

Arablouei, R., et al., 2021. In-situ classification of cattle behavior using accelerometry

data. Comput. Electron. Agric. 183, 106045.

Barker, Z., Vázquez Diosdado, J., Codling, E., Bell, N., Hodges, H., Croft, D., Amory, J.,
2018. Use of novel sensors combining local positioning and acceleration to measure
feeding behavior differences associated with lameness in dairy cattle. J. Dairy Sci.
101, 6310–6321.

Brandes, S., Sicks, F., Berger, A., 2021. Behaviour classification on giraffes (giraffa
camelopardalis) using machine learning algorithms on triaxial acceleration data of
two commonly used GPS devices and its possible application for their management
and conservation. Sensors 21, 002229.

Busch, P., Ewald, H., Stüpmann, F., 2017. Determination of standing-time of dairy
cows using 3D-accelerometer data from collars. In: Proceeding of International
Conference on Sensing Technology. Sydney, Australia.

Chawla, N., Bowyer, K., Hall, L., Kegelmeyer, W., 2002. SMOTE: Synthetic minority

over-sampling technique. J. Artificial Intelligence Res. 16, 321–357.

Dominguez-Morales, J., Duran-Lopez, L., Gutierrez-Galan, D., Rios-Navarro, A., Linares-
Barranco, A., Jimenez-Fernandez, A., 2021. Wildlife monitoring on the edge: A
performance evaluation of embedded neural networks on microcontrollers for
animal behavior classification. Sensors 21, 2975.

Dutta, R., Smith, D., Rawnsley, R., Bishop-Hurley, G., Hills, J., Timms, G., Henry, D.,
2015. Dynamic cattle behavioral classification using supervised ensemble classifiers.
Comput. Electron. Agric. 111, 18–28.

Fawaz, H., Forestier, G., Weber, J., Idoumghar, L., Muller, P., 2019. Deep learning for
time series classification: a review. Data Min. Knowl. Discov. 33 (4), 917–963.
González, L., Bishop-Hurley, G., Handcock, R., Crossman, C., 2015. Behavioral classi-
fication of data from collars containing motion sensors in grazing cattle. Comput.
Electron. Agric. 110, 91–102.

Goodfellow, I., Bengio, Y., Courville, A., 2016. Deep Learning. MIT Press.
Greenwood, P., Valencia, P., Overs, L., Paull, D., Purvis, I., 2014. New ways of
measuring intake, efficiency and behaviour of grazing livestock. Anim. Prod. Sci.
54, 1796–1804.

Gutierrez-Galan, D., Dominguez-Morales, J., Cerezuela-Escudero, E., Rios-Navarro, A.,
Tapiador-Morales, R., Rivas-Perez, M., Dominguez-Morales, M.,
Jimenez-
Fernandez, A., Linares-Barranco, A., 2018. Embedded neural network for real-time
animal behavior classification. Neurocomputing 272, 17–26.

Haladjian, J., Haug, J., Nüske, S., Bruegge, B., 2018. A wearable sensor system for

lameness detection in dairy cattle. Multimodal Technol. Interact. 2, 27.

Hamalainen, W., Jarvinen, M., Martiskainen, P., Mononen, J., 2011. Jerk-based feature
extraction for robust activity recognition from acceleration data. In: Proceedings of
International Conference on Intelligent Systems Design and Applications. Cordoba,
Spain, pp. 831–836.

Kamminga, J., Bisby, H., Le, D., Meratnia, N., Havinga, P., 2017a. Generic online animal
activity recognition on collar tags. In: Proc. ACM Int. Joint Conf. on Pervasive and
Ubiquitous Computing and Symposium on Wearable Computers. pp. 597–606.
Kamminga, J., Le, D., Meijers, J., Bisby, H., Meratnia, N., Havinga, P., 2018. Robust
sensor-orientation-independent feature selection for animal activity recognition on
collar tags. Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. 2 (1), 15.
Kamminga, J., Meratnia, N., Bisby, H., Havinga, P., Le, D., 2017b. Generic online animal
activity recognition on collar tags. In: UbiComp/ISWC’17 Adjunct. Maui, HI, USA,
pp. 597–606.

Kingma, D., Ba, J., 2015. Adam: A method for stochastic optimization. In: International

Conference for Learning Representations. San Diego, CA, USA.

Kuznetsov, B., Parker, J., Esqueda, F., 2020. Differentiable IIR filters for machine
learning applications. In: Proceedings of the International Conference on Digital
Audio Effects. Vienna, Austria, pp. 297–303.

Levitis, D., Lidicker, W., Freund, G., 2009. Behavioural biologists do not agree on what

constitutes behaviour. Anim. Behav. 78 (1), 103–110.

van der Maaten, L., Hinton, G., 2008. Visualizing high-dimensional data using t-SNE.

J. Mach. Learn. Res. 9, 2579–2605.

Mattachini, G., Riva, E., Perazzolo, F., Naldi, E., Provolo, G., 2016. Monitoring feeding
behaviour of dairy cows using accelerometers. J. Agric. Eng. XLVII 498, 54–58.
Matthews, B., 1975. Comparison of the predicted and observed secondary structure of
T4 phage lysozyme. Biochim. Biophys. Acta (BBA) - Protein Struct. 405, 442–451.
Molnar, C., 2020. Interpretable machine learning: A guide for making black box models
explainable. Available online: <https://christophm.github.io/interpretable-ml-book/>.
Nathan, R., Spiegel, O., Fortmann-Roe, S., Harel, R., Wikelski, M., Getz, W., 2012. Using
tri-axial acceleration data to identify behavioral modes of free-ranging animals:
general concepts and tools illustrated for griffon vultures. J. Exp. Biol. 215,
986–996.

Rahman, A., Smith, D., Little, B., Ingham, A., Greenwood, P., Bishop-Hurley, G., 2018.
Cattle behaviour classification from collar, halter, and ear tag sensors. Inf. Process.
Agric. 5, 124–133.

le Roux, S., Wolhuter, R., Stevens, N., Niesler, T., 2018. Reduced energy and
memory requirements by on-board behavior classification for animal-borne sensor
applications. IEEE Sens. J. 18 (10), 4261–4268.

ComputersandElectronicsinAgriculture207(2023)10770713R. Arablouei et al.

Sakaia, K., Oishia, K., Miwab, M., Kumagaia, H., Hirookaa, H., 2019. Behavior
classification of goats using 9-axis multi sensors: The effect of imbalanced datasets
on classification performance. Comput. Electron. Agric. 166, 105027.

Suresh, V., Sidhu, R., Karkare, P., Patil, A., Lei, Z., Basu, A., 2018. Powering the IoT
through embedded machine learning and LoRa. In: Proceedings of IEEE World
Forum on Internet of Things. Singapore, pp. 349–354.

Schirmann, K., Chapinal, N., Weary, D., Heuwieser, W., von Keyserlingk, M., 2012.
Rumination and its relationship to feeding and lying behavior in holstein dairy
cows. J. Dairy Sci. 95 (6), 3212–3217.

Vázquez Diosdado, J., Barker, Z., Hodges, H., Amory, J., Croft, D., Bell, N.,
Codling, E., 2015. Classification of behaviour in housed dairy cows using an
accelerometer-based activity monitoring system. Anim. Biotelemetry 3, 15.

Smith, W., Galyean, M., Kallenbach, R., Greenwood, P., Scholljegerdes, E., 2021.
Understanding intake on pastures: how, why, and a way forward. J. Anim. Sci.
99 (6), skab062.

Wang, Z., Yan, W., Oates, T., 2017. Time series classification from scratch with deep
neural networks: A strong baseline. In: International Joint Conference on Neural
Networks. pp. 1578–1585.

Smith, D., Rahman, A., Bishop-Hurley, G., Hills, J., Shahriar, S., Henry, D.,
Rawnsley, R., 2016. Behavior classification of cows fitted with motion collars:
Decomposing multi-class classification into a set of binary problems. Comput.
Electron. Agric. 131, 40–50.

Williams, L., Bishop-Hurley, G., Anderson, A., Swain, D., 2019. Application of ac-
celerometers to record drinking behaviour of beef cattle. Anim. Prod. Sci. 59,
122–132.

ComputersandElectronicsinAgriculture207(2023)10770714
