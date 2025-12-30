Contents lists available at ScienceDirect

Computers and Electronics in Agriculture

journal homepage: <www.elsevier.com/locate/compag>

Original papers

Classifying animal behavior from accelerometry data via recurrent neural
networks
Liang Wang a, Reza Arablouei b,∗, Flavio A.P. Alvarenga c, Greg J. Bishop-Hurley a
a Agriculture and Food, CSIRO, St Lucia QLD 4067, Australia
b Data61, CSIRO, Pullenvale QLD 4069, Australia
c NSW Department of Primary Industries, Armidale NSW 2350, Australia

A R T I C L E I N F O

A B S T R A C T

Keywords:
Deep learning
Edge computing
Gated recurrent unit
Long short-time memory
Time-series classification

We study the classification of animal behavior from accelerometry data using various recurrent neural network
(RNN) models. RNNs have extensively been employed to classify time-series data in various applications.
However, their utilization for classifying animal behavior from wearable sensor data, particularly accelerometry
data, as well as the underlying accuracy-complexity trade-offs is rather under-explored. We use four triaxial
accelerometry datasets acquired from grazing cattle via collar tags or ear tags to evaluate the classification
performance and complexity of the considered RNN models, which feature long short-time memory (LSTM)
or gated recurrent unit (GRU) architectures with varying depths and widths. In the evaluations, we also
include two state-of-the-art convolutional neural network (CNN)-based time-series classification models.
The results show that the considered RNN-based models can achieve similar or higher animal behavior
classification accuracy compared to the CNN-based models while having smaller computational and memory
requirements. We also observe that the GRU-based models generally outperform the LSTM-based ones in terms
of classification accuracy despite being less complex. A single-layer uni-directional GRU model with 64 hidden
units appears to offer a good balance between accuracy and complexity making it suitable for implementation
on edge/embedded devices.

1. Introduction

Monitoring the behavior of livestock is crucial for their effective
management. Accurate knowledge of behavior and the associated short-
and long-term trends and variations can provide valuable insights into
the productivity, health, and welfare of animals. However, monitoring
animal behavior manually is time-consuming, labor-intensive, error-
prone, and may disturb the animals. Therefore, automatic classification
of animal behavior from wearable sensor data is of practical impor-
tance. Most animal behaviors are recognizable through body movement
patterns and intensity that can be sensed by accelerometers.

Early approaches that use accelerometry data to classify animal
behavior rely on hand-tuned thresholds in conjunction with standard
statistical features in time or frequency domain. In Williams et al.
(2019), the drinking behavior is identified using the mean of ac-
celerometer readings in the 𝑧 (front-to-back) axis and the variance of
accelerometer readings in the 𝑥 (vertical) axis. The results show that the
proposed method can distinguish drinking from other behaviors with
good accuracy. Busch et al. (2017) extract some statistical features from
triaxial accelerometry data collected by collar tags fitted on dairy cattle

and calculate the relevant thresholds to distinguish lying from standing
with good accuracy. In this work, the threshold values are computed
manually based on the analysis of the available data.

Triaxial accelerometer readings are multivariate time-series data.
Several time-series classification algorithms have been proposed in re-
cent years (Bagnall et al., 2017). The most popular ones are the nearest-
neighbor methods coupled with parametric distance functions (Lines
and Bagnall, 2015) and the ensemble methods (Bagnall et al., 2015;
Bostrom and Bagnall, 2015; Schäfer, 2015; Kate, 2016) including ran-
dom forest (Baydogan et al., 2013; Deng et al., 2013). Rahman et al.
(2018) use several time- and frequency-domain statistical features to
train a random forest classifier that can differentiate three cattle be-
haviors of grazing, standing, and ruminating. Smith et al. (2016) utilize
a set of binary classifiers, including support vector machine (SVM),
naive Bayes, 𝑘-nearest neighbors, logistic regression, and random for-
est, for animal behavior classification. They use standard time- and
frequency-domain statistical features together with some information-
theoretic features. The results show that the collection of binary classi-
fiers can improve classification accuracy compared to the correspond-
ing multiclass classifiers. Arablouei et al. (2021) devise a small set of

∗ Corresponding author.

E-mail address: <reza.arablouei@csiro.au> (R. Arablouei).

<https://doi.org/10.1016/j.compag.2023.107647>
Received 15 September 2021; Received in revised form 20 September 2022; Accepted 10 January 2023

ComputersandElectronicsinAgriculture206(2023)107647Availableonline20January20230168-1699/©2023TheAuthor(s).PublishedbyElsevierB.V.ThisisanopenaccessarticleundertheCCBY-NC-NDlicense(<http://creativecommons.org/licenses/by-nc-nd/4.0/>).L. Wang et al.

Fig. 1. Cattle on paddock during the experiment leading to the Arm20c and Arm20e datasets.

Fig. 2. Angus heifers wearing collar (b) and ear (c) tags used for data collection.

computationally-efficient and informative features based on examining
the statistical and spectral properties of the relevant accelerometry
data. Their cross-validated results show that, using the proposed fea-
tures, resource-efficient discriminative models can yield good classifi-
cation accuracy.

The above-mentioned machine-learning-based approaches to animal
behavior classification require careful feature engineering to achieve
satisfactory results. The features used in Rahman et al. (2018) and
Smith et al. (2016) stem from domain knowledge and intuition, hence
do not necessarily represent the internal structure of the data. In
addition, such methods require the extraction of the features to be
accomplished before training any classification model. As a result, the
feature extraction and classification stages are disjoint.

End-to-end deep neural networks (DNNs) have demonstrated
promising performance in classification tasks involving complex input
data, such as image classification (LeCun et al., 2015), where feature
engineering is inherently difficult. Therefore, substantial research has
been conducted on using various DNN models for classifying time-series
data (Wang et al., 2017; Fawaz et al., 2019).

Rahman et al. (2016) use an auto-encoder to learn useful feature
representations for accelerometer time-series data in an unsupervised
way. An SVM classifier trained with the learned features is shown
to outperform the one trained with hand-crafted features. This work
achieves data-driven feature engineering while feature calculation and
behavior classification are still separate steps.

Kasfi et al. (2016) introduce an end-to-end cattle behavior classifi-
cation algorithm that utilizes a convolutional neural network (CNN)
model. In this model, the parameters of the feature extraction and
classification parts are estimated jointly. The algorithm’s accuracy is
similar to that of the one proposed in Rahman et al. (2016), albeit it is
more efficient. Peng et al. (2019) use a long short-time memory (LSTM)
recurrent neural network (RNN) model to classify cattle behavior. The
model is trained to classify cattle behavior considering three different
time-window sizes of 3.2s, 6.4s, and 12.8s. The results show that the
utilized LSTM classifier is superior to a simple CNN classifier and the
best performance is achieved when the window size is 3.2s. Following
up this work, Peng et al. (2020) use a similar LSTM model to detect

ComputersandElectronicsinAgriculture206(2023)1076472L. Wang et al.

Fig. 3. The PCB of the ear tag used for data collection (a) and the block diagram of its main components (b).

calving-related behaviors from accelerometry data. Unfortunately, the
authors of Peng et al. (2019, 2020) do not provide any further detail
regarding the specifications of their models.

were approved by the CSIRO FD McMaster Laboratory Chiswick Animal
Ethics Committee with the animal research authority numbers 19/18
and 17/20.

In this paper, we examine the performance of RNN models in clas-
sifying animal behavior from accelerometry data. We consider several
RNN models based on LSTM and gated recurrent unit (GRU) architec-
tures with various numbers of hidden layers and units. We characterize
the performance of the considered models as well as the underlying
trade-offs between model complexity and accuracy. Understanding the
interplay between model complexity and classification accuracy is crit-
ical when the behavior classification is to be performed on devices with
limited computational, memory, or energy resources. By characterizing
the accuracy-complexity trade-off for RNN-based classifiers, we assess
the feasibility of their implementation on edge or embedded devices
and identify the most suitable models that help balance accuracy and
complexity effectively.

2. Datasets

In this section, we describe the specifications of the datasets that we
utilize to evaluate the proposed animal behavior classification models
as well as the processes of their generation.

We have conducted several data collection experiments with grazing
beef cattle wearing collar tags or ear tags. The first experiment took
place in August 2018 at the Commonwealth Scientific and Industrial
Research Organisation (CSIRO) FD McMaster Laboratory Chiswick,
near Armidale, NSW, Australia (30◦36’28.17"S, 151◦32’39.12"E). There
is a detailed description of the experiment and the equipment used
including the collar tags in Arablouei et al. (2021). The accelerometry
data was collected from ten steers of Angus breed wearing collar tags.
We refer to the associated dataset as Arm18. Another experiment was
conducted in March 2020 at the same facility while the accelerometry
data was collected from eight cattle of Angus breed wearing collar tags,
six of which also wore ear tags. We refer to the associated datasets as
Arm20c and Arm20e where the former relates to the collar tag data
and the latter to the ear tag data. A similar experiment was run at
CSIRO’s Lansdown Research Station, Woodstock, Queensland, Australia
(19◦39’26.41"S, 146◦50’5.88"E) in September 2019 with nineteen cattle
wearing collar tags. The animals in this experiments were heifers and
steers of Brangus and Droughtmaster breeds. We refer to the associated
dataset as Lan19.

Fig. 1 shows the paddock and the cattle used for the experiment
that produced the Arm20c and Arm20e datasets. Figs. 2(a) and 2(b)
show cattle wearing the utilized collar and ear tags. The experiments

The smart ear tag used for data collection, specifically the Arm20e
dataset, is a purpose-built sensor node jointly developed by CSIRO and
a commercial partner, Ceres Tag,1 to serve both research and industrial
applications. It houses a wealth of sensors and communication capabil-
ities. Its main components are microcontroller, triaxial accelerometer,
satellite communication interface, on-board memory, solar panel, and
battery. The microcontroller is a Nordic nRF528402 system-on-chip
with a 64 MHz ARM Cortex-M4F processor, 1 MB of flash memory,
256 kB of RAM, a floating-point unit, and Bluetooth 5 interface. The
accelerometer is a Bosch Sensortec BMA4003 micro electromechani-
cal system (MEMS) device with an ultra-low power consumption of
maximum 14 μA. It measures the instantaneous acceleration in three
orthogonal spatial axes. On each axis, it senses minuscule changes in
the capacitance between a fixed electrode and a proof mass that is
displaced by any force applied to the device’s supporting frame.

The ear tag is powered by a 3.2 V, 170 mAh battery pack that is
recharged using a solar panel installed on the tag’s case. The operating
system running on the microcontroller is Zephyr.4 As the on-board
memory of the ear tag is limited, to log the accelerometry data, we
stream the data via a generic attribute profile (GATT) Bluetooth link
to the collar tag installed on the same animal. Fig. 3(a) contains the
pictures of both sides of the ear tag’s printed circuit board (PCB) and
Fig. 3(b) depicts the block diagram of the ear tag’s main components.
In all data collection experiments, the tags recorded triaxial ac-
celerometer readings. The accelerometer sample rate was 50 Hz for
the collar tags and 62.5 Hz for the ear tags. We manually annotated
sections of the accelerometry data by observing the behavior of the
cattle. The behaviors are mutually exclusive. In the Arm18 dataset,
there are four behavior classes of interest, grazing, ruminating, resting,
and other. In the Lan19 dataset, four behavior classes of interest are
grazing, walking, ruminating/resting, and other. In the Arm20c and
Arm20e datasets, there are three behavior classes of interest, grazing,
ruminating/resting, and other. In the Arm18, Arm20c, and Arm20e
datasets, the other behavior class is the collection of all behaviors other

1 <https://cerestag.com/>
2 <https://www.nordicsemi.com/products/nrf52840>
3 <https://www.bosch-sensortec.com/products/motion-sensors/>

accelerometers/bma400/

4 <https://www.zephyrproject.org/>

ComputersandElectronicsinAgriculture206(2023)1076473L. Wang et al.

Table 1
The number of datapoints corresponding to each behavior class in the considered
datasets.

Behavior

Grazing
Walking
Ruminating
Resting
Other

Total

Dataset

Arm18

7109
–
2482
2909
735

Lan19

70 402
16 700

53 760

10 616

Arm20c

Arm20e

6156
–

4080

1726

6047
–

3640

1575

13 235

151 478

11 962

11 262

Table 2
The MCC values of
the proposed RNN-based and the state-of-the-art CNN-based
classifiers evaluated using the considered datasets. The highest three MCC values for
each dataset are shown in green, blue, and red.

Model

bi-LSTM-2–128
bi-LSTM-2–64
bi-LSTM-2–32
bi-LSTM-1–128
bi-LSTM-1–64
bi-LSTM-1–32
uni-LSTM-2–128
uni-LSTM-2–64
uni-LSTM-2–32
uni-LSTM-1–128
uni-LSTM-1–64
uni-LSTM-1–32

bi-GRU-2–128
bi-GRU-2–64
bi-GRU-2–32
bi-GRU-1–128
bi-GRU-1–64
bi-GRU-1–32
uni-GRU-2–128
uni-GRU-2–64
uni-GRU-2–32
uni-GRU-1–128
uni-GRU-1–64
uni-GRU-1–32

FCN
ResNet

Dataset

Arm18

0.891
0.888
0.778
0.858
0.772
0.754
0.879
0.856
0.829
0.854
0.777
0.734

0.910
0.891
0.883
0.886
0.857
0.757
0.908
0.900
0.857
0.898
0.879
0.723

0.880
0.907

Lan19

Arm20c

Arm20e

0.826
0.803
0.755
0.787
0.751
0.721
0.806
0.757
0.746
0.793
0.741
0.729

0.811
0.800
0.753
0.789
0.766
0.738
0.810
0.776
0.714
0.789
0.755
0.732

0.783
0.791

0.880
0.875
0.857
0.870
0.864
0.847
0.806
0.868
0.852
0.872
0.861
0.829

0.895
0.884
0.876
0.884
0.871
0.851
0.891
0.877
0.851
0.885
0.873
0.858

0.873
0.874

0.789
0.774
0.751
0.777
0.760
0.653
0.789
0.753
0.446
0.791
0.739
0.665

0.800
0.797
0.759
0.779
0.776
0.747
0.789
0.774
0.738
0.777
0.787
0.750

0.794
0.809

than grazing, resting, and ruminating. In the Lan19 dataset, the other
behavior class represents all behaviors except grazing, walking, resting,
and ruminating.

We divide the annotated accelerometry data into non-overlapping
segments each containing 256 consecutive triaxial readings. The seg-
ment size of 256 corresponds to about 5.12s for collar tag data and
about 4.1s for ear tag data. The accelerometer readings of each dataset
can be arranged into a three-way tensor of dimensions (𝑁, 256, 3) where
𝑁 is the total number of segments. Table 1 shows the number of
segments (datapoints) of each behavior class in each dataset.

3. Model

In this section, we provide an architectural overview of the proposed
RNN classifiers, discuss the choice of values for the related hyper-
parameters, and outline the relevant learning and evaluation processes
as well as the utilized performance metrics.

3.1. Architecture

RNNs are artificial neural networks with their neurons organized
into successive layers of input layer, hidden layer, and output layer.

Each connection between neurons has a corresponding trainable
weight. RNNs differ from feed-forward neural networks in that their
hidden layer neurons are connected to themselves in a recurrent
manner resembling a feedback loop. Therefore, the values of the hidden
layer neurons at any time step 𝑡, namely, the hidden state denoted by 𝐡𝑡,
are dependent on their values at the previous time step 𝑡−1, namely, the
previous hidden state denoted by 𝐡𝑡−1, and the current input denoted
by 𝐱𝑡. This relationship can be expressed as

𝐡𝑡 = 𝐟(𝐱𝑡, 𝐡𝑡−1).

(1)

This in-built recurrence enables RNNs to learn and recognize patterns
over input sequences, extract meaningful features from sequential ob-
servations, and map the learned features to discriminate the underlying
classes in sequential data.

Fig. 4 depicts the architecture of the RNN-based animal behavior
classification algorithm that we consider in this work. The input module
is a perceptron that augments the dimension of the input data from
three to the hidden-state dimension, which is a model hyper-parameter.
The output of the input module is fed to the recurrent module, which
learns a non-linear encoding of the input sequences. The output module
takes the encoding produced by the recurrent module as input and
shrinks its dimension down to the number of classes. If the recurrent
module is bi-directional, two encoding vectors corresponding to the
forward and backward directions are concatenated and fed into the
output module. In the perceptrons of both input and output modules,
we use the rectified linear unit (ReLU) activate function except for the
last layer of the output module where we use the softmax activation
function to predict the pseudo-probability of each class.

3.2. Hyper-parameters

As the simple Elman/Jordan RNN often suffers from the vanish-
ing/exploding gradient problem when dealing with long input se-
quences, gated RNN variants are more commonly used in practice.
Therefore, the first structural hyper-parameter of our RNN-based clas-
sifiers is the utilized gated variant, that is, long short-term mem-
ory (LSTM) (Hochreiter and Schmidhuber, 1997) or gated recurrent
unit (GRU) (Cho et al., 2014). LSTM comprises a memory cell, an input
gate, a forget gate, and an output gate. The memory cell accumulates
the information extracted from the input sequences and the gates
modulate the inward and outward flux of the information. GRU is
similar to LSTM but does not have any output gate. Thus, it has fewer
parameters and is computationally less demanding compared to LSTM.
The bidirectional RNNs use an additional hidden layer to accu-
mulate sequential information in the backward direction. This can
enable more flexible processing of the information within the input
sequence. The number of directions, that is, the network being uni- or
bi-directional, is another structural hyper-parameter. The other struc-
tural hyper-parameters are the number of stacked RNN layers and the
number of neurons in each hidden layer. We consider the number of
RNN layers to be either one or two and the number of hidden-layer
neurons to be 32, 64, or 128. We name the models corresponding to
different combinations of considered structural hyper-parameters by
hyphenating the number of directions (bi or uni), the RNN variant
(LSTM or GRU), the number of layers (1 or 2), and the number of
hidden-layer neurons (32, 64 or 128) as shown in Table 2.

3.3. Evaluation

We compare the performance of the considered RNN-based mod-
els with that of two CNN-based time-series classification algorithms,
proposed in Wang et al. (2017) and called fully-convolutional network
(FCN) and residual network (ResNet), in terms of both classification
accuracy and model complexity. As shown in Fawaz et al. (2019),
these algorithms are among the most accurate existing time-series
classification algorithms.

ComputersandElectronicsinAgriculture206(2023)1076474L. Wang et al.

Fig. 4. The architecture of the considered RNN classifier. Blue circles represent the neurons of their respective perceptrons with ReLU activation functions and blue rectangles
represent the RNN cells at each time step.

We evaluate the performance of all considered models using
four datasets described in Section 2 via a leave-one-animal-out cross-
validation (CV) scheme. In every CV fold, we train each model using
the data of all animals but one and evaluate the trained model using
the data of the animal whose data was left out in training. We then ag-
gregate the evaluation results of all folds to obtain our cross-validated

accuracy results. We carry out a limited tuning of the algorithmic
hyper-parameters of the proposed models, which are, the learning
rate, weight decay, batch size, and number of training iterations, and
use the same values for all models except for the number of training
iterations that is specific to each model. For FCN and ResNet, we use
the hyper-parameter values prescribed in Fawaz et al. (2019).

ComputersandElectronicsinAgriculture206(2023)1076475L. Wang et al.

Fig. 5. The confusion matrices corresponding to the best performing model for each dataset, top left: bi-GRU-2-128 for Arm18, top right: bi-LSTM-2-128 for Lan19, bottom left:
bi-GRU-2-128 for Arm20c, bottom right: ResNet for Arm20e.

We use the Matthews correlation coefficient (MCC) as the metric
for classification accuracy since it is suitable for unbalanced multiclass
classification problems (Gorodkin, 2004). MCC takes into account the
true and false positives and negatives and is generally regarded as a
balanced accuracy measure that can be used even if the classes are of
vastly different sizes.

We quantify the complexity of each model using three metrics,
namely, the number of parameters, the amount of memory occupied,
and the number of multiplication operations required to perform in-
ference on a single datapoint (256 consecutive triaxial accelerometer
readings). We calculate the memory usage of each model utilizing the
PyTorch Model Size Estimator tool5 and count the number of required
multiplication operations by examining the tensor operations involved
in performing inference via each model.

The basic building blocks of all considered RNN- and CNN-based
models are perceptron, LSTM, GRU, or convolution modules whose

required multiplication counts are given by

𝑀perc = 𝐷in × 𝐷out × 𝐿
𝑀LSTM = (𝐷2
𝑀GRU = (𝐷2
𝑀conv = 𝐾 × 𝐶in × (𝐿 − 𝐾 + 1) × 𝐶out

h × 8 + 𝐷h × 3) × 𝐿
h × 6 + 𝐷h × 3) × 𝐿

(2)

(3)

(4)

(5)

where 𝐿 is the length of the input time-series, 𝐷in and 𝐷out are the
dimensions of the input and output layers in the input/output percep-
trons, respectively, 𝐷h is the dimension of the hidden layer in the RNN
modules, 𝐾 is the size of the convolution kernel, and 𝐶in and 𝐶out are
the numbers of the input and output channels in any convolutional
layer, respectively.

We implement all models using the PyTorch library6 for Python and

train them on CSIRO’s high-performance computing clusters.

5 <https://github.com/jacobkimmel/pytorch_modelsize>

6 <https://pytorch.org/>

ComputersandElectronicsinAgriculture206(2023)1076476L. Wang et al.

Fig. 6. The confusion matrices corresponding to the uni-GRU-1-64 model for each datasets, top left: Arm18, top right: Lan19, bottom left: Arm20c, bottom right: Arm20e.

4. Results

In this section, we present the evaluation results of classification

accuracy and model complexity for all considered models.

4.1. Accuracy

Table 2 shows the MCC values representing the classification accu-
racy of the proposed RNN-based models and the considered state-of-
the-art CNN-based models for each dataset. In Figs. 5 and 6, for each
considered dataset, we present the confusion matrices corresponding to
the best performing model and the uni-GRU-1-64 model, respectively.
We will explain the reason for choosing this model later in this section.
To facilitate a visual comparison, we plot the values of the MCC against
the dimension of the hidden layer for each dataset and all RNN-based
models in Fig. 7.

The results show that the largest considered RNN-based models,
namely, bi-LSTM-2-128 and bi-GRU-2-128, yield superior or similar
performance to the CNN-based models. The GRU-based models are in

general more accurate than the LSTM-based ones, although the differ-
ence is small. The accuracy of the RNN-based models decreases as the
number of directions, layers, or neurons in each hidden layer decreases.
However, the number of neurons appears to affect the accuracy more
significantly compared to the number of directions or layers. Therefore,
the MCC values of the uni-GRU-1-128 are close to those of the best-
overall-performing model that is bi-GRU-2-128. The ResNet model is
slightly more accurate than the FCN model. This is consistent with
the results reported in Fawaz et al. (2019) for multivariate time-series
classification using various datasets.

4.2. Complexity

In Table 3, we present the values of the model complexity metrics,
viz. the number of multiplication operations required to perform infer-
ence on a single datapoint, the number of trainable parameters, and the
memory usage, for the proposed RNN-based and the considered state-
of-the-art CNN-based classifiers. We calculate the values assuming the
number of classes to be four.

ComputersandElectronicsinAgriculture206(2023)1076477L. Wang et al.

Fig. 7. The MCC value versus the hidden layer dimension for all considered RNN-based classification models and datasets.

Table 3
The values of
the number of multiplication
operations, the number of parameters, and the required memory, for the proposed
RNN-based and the state-of-the-art CNN-based classifiers.

the model complexity metrics, viz.

Model

Operations (M)

Parameters (K)

Memory (MB)

bi-LSTM-2–128
bi-LSTM-2–64
bi-LSTM-2–32
bi-LSTM-1–128
bi-LSTM-1–64
bi-LSTM-1–32
uni-LSTM-2–128
uni-LSTM-2–64
uni-LSTM-2–32
uni-LSTM-1–128
uni-LSTM-1–64
uni-LSTM-1–32

bi-GRU-2–128
bi-GRU-2–64
bi-GRU-2–32
bi-GRU-1–128
bi-GRU-1–64
bi-GRU-1–32
uni-GRU-2–128
uni-GRU-2–64
uni-GRU-2–32
uni-GRU-1–128
uni-GRU-1–64
uni-GRU-1–32

FCN
ResNet

134.7
33.8
8.5
67.4
16.9
4.3
67.4
16.9
4.3
33.8
8.5
2.1

101.2
25.4
6.4
50.6
12.7
3.2
50.7
12.7
3.2
25.4
6.4
1.6

67.9
132.6

661
166.7
42.3
265.7
67.3
17.3
265.2
67.1
17.2
133.1
33.8
8.7

496.1
125.2
31.9
199.7
50.7
13.1
199.2
50.4
12.9
100.1
25.5
6.6

267.3
520.2

3.3
1.0
0.4
1.8
0.7
0.3
1.5
0.5
0.2
1.0
0.4
0.2

2.7
0.9
0.3
1.5
0.6
0.3
1.3
0.5
0.2
0.9
0.4
0.2

3.0
4.6

To provide a visual representation of the accuracy-complexity trade-
off underlying the examined models, we plot the values of MCC against

the memory usage and the number of required multiplications for all
models and datasets in Figs. 8 and 9, respectively. In these figures, the
points with the same shape and color correspond to the models that
only vary in the hidden layer dimension. The larger the dimension,
the higher the memory usage and multiplication count. Note that
the complexity of performing inference using each model is almost
independent of the dataset used since, in all considered datasets, the
datapoints have the same size and the numbers of classes are similar,
specifically, three or four.

Among all models, bi-LSTM-2-128 is the most complex one in terms
of the number of parameters and multiplication operations. Its memory
usage is also the highest among the RNN-based models. The bi-GRU-
2-128 model is almost three-fourths as complex as the bi-LSTM-2-128
model in terms of all complexity metrics despite having better accuracy.
Unidirectional models are significantly less complex compared to their
bidirectional counterparts as their complexity metric values are less
than half of those of the corresponding bidirectional models. However,
this does not come at the expense of any significant loss of accuracy. We
observe a similar trend when examining the models with one hidden
layer versus the corresponding models with two hidden layers.

The complexity difference in models that only differ in the number
of hidden layer neurons (hidden layer dimension) is more pronounced
as going from 128 to 64 reduces the complexity metrics by almost four
folds. In general, the models with 64 neurons in their hidden layers
are only slightly less accurate compared to their corresponding ones
with 128 neurons. However, reducing the hidden layer dimension to 32
results in a more noticeable decrease in accuracy. Therefore, the uni-
GRU-1-64 model appears to strike a good balance between accuracy
and performance. When contrasted to the state-of-the-art CNN-based
models, FCN and ResNet, the uni-GRU-1-64 has a comparable accuracy
but is substantially less complex as the values of its complexity metrics
are more than an order of magnitude smaller than those of the FCN and
ResNet models.

ComputersandElectronicsinAgriculture206(2023)1076478L. Wang et al.

Fig. 8. The MCC value versus the memory usage for all considered animal behavior classification models and datasets.

5. Discussion

A main feature of the classification models that we have studied
in this work is their ability to be trained and perform inference in an
end-to-end manner. Specifically, they take the multivariate time-series
data of triaxial accelerometer readings as the input and produce the
predicted animal behavior class as the output. The conventional models
commonly adopted prior to the introduction of the DNN-based end-to-
end models require scrupulous feature engineering in conjunction with
expert domain knowledge. The input to the classification model in such
approaches is the extracted features and not the raw data. The raw data
is fed to a prior processing stage called feature extraction that calculates
the features. This approach involves two separate stages. The first stage
is to determine the best features to extract from the data and the second
stage is to find the best classification model that maps the extracted
features to the desirable output.

In the RNN- and CNN-based models studied in this work, the RNN
modules or the CNN layers can be viewed as playing the role of feature
extraction. However, the parameters (weights) of the RNN/CNN layers
are trainable. This means the features are learned jointly with the
discriminator (classifier) in an efficient way. This is the key to superior
performance of end-to-end DNN models and their wide acceptance in
recent years to tackle many problems in various applications.

Our proposed RNN-based models exhibit favorable performance
when evaluated using the considered performance metrics and con-
trasted with the state-of-the-art CNN-based models. However, they
suffer from a fundamental limitation that is inherent to all RNN-based
models. The recurrent operations of an RNN are performed sequentially
and may not be executed in parallel. On the other hand, feed-forward
neural networks, including the CNNs, predominantly involve arithmetic
operations over tensors, which can be performed in parallel given suit-
able compute capability. Therefore, RNN-based models can in general

benefit less from parallelization compared with the CNN-based models.
Nonetheless, parallel processors that can accelerate tensor operations
are resource-hungry and still rarely integrated into edge devices or
embedded systems. This means the sequential nature of the RNNs
does not pose any substantial disadvantage to our proposed RNN-based
models when the target platform is an edge or embedded device.

To evaluate the performance of our proposed models, we used four
datasets, three of which are collected using collar tags and one using ear
tags. The datasets are also collected at two different research facilities,
three datasets at one facility and one dataset at another. The locations
of the two research facilities are more than 1,300 km apart. This has
resulted in a significant diversity among the datasets for the following
reasons. First, the utilized collar tags and ear tags are placed on or
attached to distinct parts of cattle’s body hence their accelerometers
are subject to significantly different acceleration patterns when animals
exhibit various considered behaviors. The type of the accelerometers
used and their sample rates are also different in the collar tags and ear
tags. In addition, the impact of earth’s gravity on the accelerometer
readings of the two devices is different as the orientation of the collar
tags and ear tags correlate with each considered behavior in distinct
ways. Second, the dimensions of the area in which the experiments
took place as well as the climate, pasture type and quality, and terrain
characteristics are considerably different in the two utilized research
facilities. We have also used several different breeds of cattle in the
data collection experiments. The important observation here is that
the proposed models perform well with all four datasets despite their
diversity. Therefore, the proposed algorithms are robust to a broad
range of variations in the data.

6. Conclusion

Our examination of the utility of different RNN models for animal
behavior classification from triaxial accelerometry data indicated that

ComputersandElectronicsinAgriculture206(2023)1076479L. Wang et al.

Fig. 9. The MCC value versus the number of multiplication operations required for inference (a single forward pass) for all considered animal behavior classification models and
datasets.

the GRU-based models yield better classification accuracy compared
to the LSTM-based models, despite their lower complexity. We also
observed that the unidirectional models with a single hidden layer
are only slightly less accurate than their bidirectional or dual-layer
counterparts. Both accuracy and complexity were more sensitive to the
dimension of the hidden layers. Overall, a unidirectional GRU-based
model with one hidden layer of size 64 appeared to offer the best bal-
ance between accuracy and complexity given all considered datasets.
This model is nearly as accurate as the state-of-the-art CNN-based
FCN and ResNet models but has substantially reduced computational
and memory complexity. This makes it suitable for implementation
on resource-constrained edge devices or embedded systems. In future
work, we will explore implementing the proposed models on the em-
bedded systems of our collar tags and ear tags and examine their
on-device performance and the associated trade-offs.

CRediT authorship contribution statement

Liang Wang: Methodology, Software, Writing. Reza Arablouei:
Methodology, Software, Writing. Flavio A.P. Alvarenga: Data collec-
tion. Greg J. Bishop-Hurley: Conceptualization, Project administra-
tion.

Declaration of competing interest

The authors declare that they have no known competing finan-
cial interests or personal relationships that could have appeared to
influence the work reported in this paper.

Data availability

Data will be made available on request.

Acknowledgments

This research was undertaken with strategic investment funding
from the CSIRO, Australia and NSW Department of Primary Indus-
tries, Australia. We would like to thank the following technical staff
who were involved in the research at CSIRO FD McMaster Laboratory
Chiswick: Alistair Donaldson and Reg Woodgate with NSW Department
of Primary Industries, and Jody McNally and Troy Kalinowski with
CSIRO Agriculture and Food. In addition, we acknowledge the CSIRO
staff who have contributed to the research projects at Lansdown Re-
search Station that have produced one of the datasets used in this
paper, especially Mel Matthews, Holly Reid, Wayne Flintham, and Steve
Austin. We also recognize the contributions of the CSIRO Data61 staff
who have designed and built the devices used for data collection,
specifically, Lachlan Currie, John Scolaro, Jordan Yates, Leslie Overs,
and Stephen Brosnan.

References

Arablouei, R., Currie, L., Kusy, B., Ingham, A., Greenwood, P.L., Bishop-Hurley, G.,
2021. In-situ classification of cattle behavior using accelerometry data. Comput.
Electron. Agric. 183, 106045.

Bagnall, A., Lines, J., Bostrom, A., Large, J., Keogh, E., 2017. The great time series
classification bake off: A review and experimental evaluation of recent algorithmic
advances. Data Min. Knowl. Discov. 31 (3), 606–660.

Bagnall, A., Lines, J., Hills, J., Bostrom, A., 2015. Time-series classification with COTE:
The collective of transformation-based ensembles. IEEE Trans. Knowl. Data Eng. 27
(9), 2522–2535.

Baydogan, M.G., Runger, G., Tuv, E., 2013. A bag-of-features framework to classify

time series. IEEE Trans. Pattern Anal. Mach. Intell. 35 (11), 2796–2802.

Bostrom, A., Bagnall, A., 2015. Binary shapelet transform for multiclass time series
classification. In: International Conference on Big Data Analytics and Knowledge
Discovery. Springer, pp. 257–269.

ComputersandElectronicsinAgriculture206(2023)10764710L. Wang et al.

Busch, P., Ewald, H., Stüpmann, F., 2017. Determination of standing-time of dairy
cows using 3D-accelerometer data from collars. In: 2017 Eleventh International
Conference on Sensing Technology. ICST, IEEE, pp. 1–4.

Cho, K., Van Merriënboer, B., Bahdanau, D., Bengio, Y., 2014. On the properties
of neural machine translation: Encoder-decoder approaches. arXiv preprint arXiv:
1409.1259.

Deng, H., Runger, G., Tuv, E., Vladimir, M., 2013. A time series forest for classification

and feature extraction. Inform. Sci. 239, 142–153.

Peng, Y., Kondo, N., Fujiura, T., Suzuki, T., Yoshioka, H., Itoyama, E., et al., 2019.
Classification of multiple cattle behavior patterns using a recurrent neural network
with long short-term memory and inertial measurement units. Comput. Electron.
Agric. 157, 247–253.

Rahman, A., Smith, D., Hills, J., Bishop-Hurley, G., Henry, D., Rawnsley, R., 2016. A
comparison of autoencoder and statistical features for cattle behaviour classifica-
tion. In: 2016 International Joint Conference on Neural Networks. IJCNN, IEEE,
pp. 2954–2960.

Fawaz, H.I., Forestier, G., Weber, J., Idoumghar, L., Muller, P.-A., 2019. Deep learning
for time series classification: A review. Data Min. Knowl. Discov. 33 (4), 917–963.
Gorodkin, J., 2004. Comparing two K-category assignments by a K-category correlation

Rahman, A., Smith, D., Little, B., Ingham, A., Greenwood, P., Bishop-Hurley, G., 2018.
Cattle behaviour classification from collar, halter, and ear tag sensors. Inform.
Process. Agric. 5 (1), 124–133.

coefficient. Comput. Biol. Chem. 28 (5–6), 367–374.

Schäfer, P., 2015. The BOSS is concerned with time series classification in the presence

Hochreiter, S., Schmidhuber, J., 1997. Long short-term memory. Neural Comput. 9 (8),

of noise. Data Min. Knowl. Discov. 29 (6), 1505–1530.

1735–1780.

Kasfi, K.T., Hellicar, A., Rahman, A., 2016. Convolutional neural network for time
series cattle behaviour classification. In: Proceedings of the Workshop on Time
Series Analytics and Applications. pp. 8–12.

Kate, R.J., 2016. Using dynamic time warping distances as features for improved time

series classification. Data Min. Knowl. Discov. 30 (2), 283–312.

LeCun, Y., Bengio, Y., Hinton, G., 2015. Deep learning. Nature 521 (7553), 436–444.
Lines, J., Bagnall, A., 2015. Time series classification with ensembles of elastic distance

measures. Data Min. Knowl. Discov. 29 (3), 565–592.

Peng, Y., Kondo, N., Fujiura, T., Suzuki, T., Ouma, S., Yoshioka, H., Itoyama, E., et
al., 2020. Dam behavior patterns in Japanese black beef cattle prior to calving:
Automated detection using LSTM-RNN. Comput. Electron. Agric. 169, 105178.

Smith, D., Rahman, A., Bishop-Hurley, G.J., Hills, J., Shahriar, S., Henry, D.,
Rawnsley, R., 2016. Behavior classification of cows fitted with motion collars:
Decomposing multi-class classification into a set of binary problems. Comput.
Electron. Agric. 131, 40–50.

Wang, Z., Yan, W., Oates, T., 2017. Time series classification from scratch with deep
neural networks: A strong baseline. In: 2017 International Joint Conference on
Neural Networks. IJCNN, IEEE, pp. 1578–1585.

Williams, L.R., Bishop-Hurley, G.J., Anderson, A.E., Swain, D.L., 2019. Application of
accelerometers to record drinking behaviour of beef cattle. Animal Prod. Sci. 59
(1), 122–132.

ComputersandElectronicsinAgriculture206(2023)10764711
