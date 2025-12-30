Master of Science Thesis in Electrical Engineering
Department of Electrical Engineering, Linköping University, 2024

Automated animal behavior
analysis using
accelerometer activity tags

Jakob Ahokas

Master of Science Thesis in Electrical Engineering
Automated animal behavior analysis using accelerometer activity tags

Jakob Ahokas
LiTH-ISY-EX–24/5688–SE

Supervisor:

Jakob Åslund

isy, Linköpings universitet

Examiner:

Fredrik Gustafsson

isy, Linköpings universitet

Division of Automatic Control
Department of Electrical Engineering
Linköping University
SE-581 83 Linköping, Sweden

Copyright © 2024 Jakob Ahokas

Abstract

The agricultural sector relies heavily on livestock, and efficient management of
the animals is crucial not only for economic reasons but also for ensuring ani-
mal welfare and promoting sustainable farming practices. Traditional livestock
management methods such as manual supervision and remote cameras are labor-
intensive and costly, particularly with large or free-roaming herds.

This thesis explores the integration of collar-based accelerometer activity tags
with the use of machine learning models to automate the monitoring and anal-
ysis of livestock behavior, specifically focusing on cows and goats. The primary
goal is to develop a system that can accurately classify various animal behaviors
using data collected from 3-dimensional accelerometer sensors.

The methodology involves collecting accelerometer data from tagged animals,
which are processed and transformed into various representations for feature ex-
traction. A decision tree classifier, simplified from an original random forest
model, is trained on this feature set to recognize different behaviors.

The model implementation on the system-on-chip demonstrates the feasibility
of deploying these machine models on resource-constrained embedded systems.
The classifier developed in this study performs well across most basic behaviors,
demonstrating high accuracy in detecting activities such as eating, lying, and
standing. However, some underrepresented classes in the dataset showed lower
classification performance. To address this, the study uses data augmentation
techniques to balance the impact of underrepresented classes and improve the
model’s generalization across less frequent behaviors. The results show promise
as a way to modernize agriculture by offering an automated solution for livestock
monitoring, with significant implications for animal health, farm efficiency, and
overall welfare.

iii

Acknowledgments

I wish to thank all the people who made this thesis possible. Firstly, I would like
to thank the employees at Vreta utbildningscentrum for their help with handling
the animals for data collection. I would also like to thank my office mate Anton
Bossen and the other thesis students in the Qulinda group for the ability to dis-
cuss issues and to know that I was not the only one struggling.

Finally, I would like to thank my examiner Fredrik Gustafsson and supervisor
Jakob Åslund at Linköping University for the feedback and support during the
project.

Linköping, November 2024
J A

v

Contents

1 Introduction

1.1 Background . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1.2 Research questions
. . . . . . . . . . . . . . . . . . . . . . . . . . .
1.3 Delimitations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2 Theory

2.4 Machine learning models for behavior analysis

2.1 Related work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2.1.1 A review of studies using accelerometer data to automate
behavior analysis in livestock . . . . . . . . . . . . . . . . .
2.1.2 Anomalous situations and rare behavior detection . . . . .
2.1.3 Precision livestock technologies for animal welfare . . . . .
2.2 Embedded programming of accelerometer tags . . . . . . . . . . .
2.3 Accelerometer data analysis . . . . . . . . . . . . . . . . . . . . . .
2.3.1 Spectral analysis . . . . . . . . . . . . . . . . . . . . . . . . .
2.3.2 Jerk Filter for motion analysis . . . . . . . . . . . . . . . . .
2.3.3 Sensor positioning . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . .
2.4.1 Decision trees . . . . . . . . . . . . . . . . . . . . . . . . . .
2.4.2 Gini Impurity . . . . . . . . . . . . . . . . . . . . . . . . . .
2.4.3 Calculating Feature Importance Using Gini Impurity . . .
2.4.4 Random forests . . . . . . . . . . . . . . . . . . . . . . . . .
2.5 Synthetic Minority Oversampling Technique . . . . . . . . . . . . .
2.6 Evaluation Metrics . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2.6.1 Accuracy . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2.6.2 Precision . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2.6.3 Recall . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2.6.4 F1-Score . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

3 Methodology

3.1 Hardware description . . . . . . . . . . . . . . . . . . . . . . . . . .
3.1.1 System-on-chip nRF52840 . . . . . . . . . . . . . . . . . . .
3.1.2 Accelerometer LIS2DS12 . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . .

3.2 Method Validation using Goat dataset

1
2
2
2

5
5

5
6
6
6
7
8
9
10
11
11
13
13
14
16
17
17
17
18
18

19
20
20
21
21

vii

viii

Contents

3.3 Data collection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3.4 Data preprocessing and managing . . . . . . . . . . . . . . . . . . .
3.4.1 Feature calculation . . . . . . . . . . . . . . . . . . . . . . .
3.5 Data analysis techniques . . . . . . . . . . . . . . . . . . . . . . . .
3.6 Implementation on activity tag . . . . . . . . . . . . . . . . . . . .
3.6.1 Memory Impact of Code Integration on Activity Tag . . . .
. . . . . . . . . . . . .
3.6.2 Power consumption and battery life

4 Results

. . . . . . .
4.1 Random Forest model on the third-party Goat dataset
4.2 Random Forest model on Cattle dataset
. . . . . . . . . . . . . . .
4.3 Feature importance . . . . . . . . . . . . . . . . . . . . . . . . . . .
4.4 Random forest model without frequency features . . . . . . . . . .
4.5 Random forest with Synthetic Minority Oversampling . . . . . . .
4.6 Simplified decision tree model . . . . . . . . . . . . . . . . . . . . .

5 Discussion

5.1 Methodology discussion . . . . . . . . . . . . . . . . . . . . . . . .
5.1.1 Data collection and data set imbalance . . . . . . . . . . . .
5.1.2 Preprocessing and model choices . . . . . . . . . . . . . . .
5.1.3 Step count as a feature . . . . . . . . . . . . . . . . . . . . .
5.1.4 Multiple animal classification . . . . . . . . . . . . . . . . .
5.2 Results discussion . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5.2.1 Comparison of Model Performances
. . . . . . . . . . . . .
5.2.2 Comparison of window sizes . . . . . . . . . . . . . . . . . .
5.2.3 Performance on Underrepresented Classes . . . . . . . . . .
5.2.4 Effectiveness of Data Augmentation Techniques . . . . . . .
. . . . . . . . . . . . . .

5.3 Implications for Real-World Applications

6 Conclusion

A Feature importance per class

B Performance without DFT features using a 10-second window size.

C Feature thresholds of the decision tree

Bibliography

23
26
28
29
30
31
32

35
35
37
38
42
43
44

47
47
48
49
51
51
52
52
53
53
54
55

57

61

65

67

69

1

Introduction

The agricultural sector depends heavily on livestock, which is a critical compo-
nent of the global food supply and a key asset for farmers worldwide. Efficient
management of these animals is highly important, not only for the economic via-
bility of farms but also for ensuring animal welfare and sustainable agricultural
practices. Traditional methods of livestock management typically involve man-
ual supervision, either in the form of direct human observers or via remote cam-
eras. One challenge livestock farmers currently face is that round-the-clock mon-
itoring of each individual animal in a detailed way becomes too labor-intensive
and expensive. The problem becomes even more apparent with larger herd sizes
and, in recent times, increased demand for humane farming practices that re-
quire more detailed supervision.

This thesis explores the development of a method to automatically analyze an-
imal behavior using accelerometer activity tags, reducing the supervision bur-
den on farmers. The primary focus is on cows and goats, but the technology is
adaptable to other animals with similar builds, such as horses. By leveraging
accelerometer data, these tags provide detailed insights into activity levels and
physical behaviors, such as head positioning, thereby aiding in more efficient and
humane livestock management.

The integration of collar-based accelerometer activity tags with machine learn-
ing models in livestock management holds significant promise. These technolo-
gies hold the power to modernize current agricultural practices and to ensure
the well-being of livestock. Automated behavior monitoring can improve the
early detection of health issues, optimize feeding schedules, and enhance breed-
ing programs, all of which contribute to more sustainable and profitable farming
operations.

1

2

1 Introduction

1.1 Background

The use of accelerometers in farms to gather data has had significant success in
previous studies, and the data has been useful for detecting various behavioral
patterns [16] [21]. The potential of such tags is high and has many applications,
such as improving animal health monitoring, disease or injury detection, detec-
tion of theft or predator attacks, and more. This research is done in collabora-
tion with Qulinda AB, an animal conservation-focused tech company. Qulinda
is actively collaborating with the Kenya Wildlife Service (KWS) in an initiative
called Project Ngulia, working towards the conservation of animals such as the
endangered black rhino in Kenya’s national parks. An additional objective for the
accelerometer tags is their potential use by KWS park rangers for monitoring and
anti-poaching efforts of these endangered animals.

Deploying this technology in real-world scenarios presents several challenges,
one of the most significant being battery life. The tags must be compact and
lightweight to ensure animal comfort, yet they also need to have extended bat-
tery life to facilitate frequent data transmission and reduce the frequency of re-
placements. Battery or sensor replacements can be particularly challenging for
farmers with free-ranging animals covering large areas. Therefore, optimizing
battery life through efficient hardware and software development is crucial to the
practical deployment of these tags. The software running on these devices plays
a large role in optimizing energy consumption. Efficient algorithms and code
optimization can significantly extend the operational life of the tags, ensuring
continuous and reliable data collection. This research addresses these challenges
by developing and implementing resource-efficient machine learning models for
real-time behavior classification, ensuring that the technology is both effective
and sustainable in demanding environments.

1.2 Research questions

1. To what extent can data gathered from collar-based accelerometers alone
be used to accurately classify common physical behaviors of animals given
sufficient computational power?

2. How well do the simplified models implemented on the activity tags inter-

pret animal behavior from the data despite the hardware constraints?

1.3 Delimitations

The models and algorithms for behavioral and activity analysis are fine-tuned to
the animal species that exist in the data sets. Two data sets are used in this thesis,
a cow data set gathered on the farm at Vreta utbildningscentrum containing data
from the Swedish Red-and-White and Holstein dairy cattle. The cow data was
gathered while the cows were indoors, possibly altering the animals’ behavior.

1.3 Delimitations

3

The second data set contains data from domestic pygmy goats gathered from
two outdoor farms in the Netherlands [12]. This thesis will focus on detecting
behaviors commonly occurring in the datasets such as eating, lying, ruminating,
walking, and standing.

2

Theory

This section provides the necessary technical knowledge about the area and the
techniques used throughout the thesis. There will also be a study of related work,
discussing their contributions and conclusions.

2.1 Related work

There exists a long list of researchers who have approached the problem of using
accelerometers to analyze the behavior of animals. This section will highlight a
few of them and group similar works together while discussing their main con-
clusions and findings.

2.1.1 A review of studies using accelerometer data to automate

behavior analysis in livestock

Studies in this area often have very different methodologies and conclusions. It
can be quite difficult to know which methods produce the best results without
spending a great deal of time and effort. To help navigate this field, the authors
[19] L. Riaboff et al. composed a systematic review to help future studies decide
on a methodology. They concluded that all surveyed articles follow the same
main outline, (1) Data collection, (2) Data preprocessing, and (3) Model develop-
ment. They all do these steps differently, but each achieves a relatively good score
on their respective key metrics, with accuracy typically above 80% for common
behaviors. Expectedly, rarely observed behaviors such as transitional behaviors,
like standing up from a lying position, have poor accuracy in predictions. The au-
thors provide methodology recommendations based on the reviewed paper and
as many as possible of them will be utilized in this thesis. The first recommenda-
tion is to include as much variety as possible when collecting data. Recordings

5

6

2 Theory

from at least 25 different animals from two or more farms with continuous ob-
servations over at least 40 hours are preferred. The recommended sampling rate
of the sensors is between 10Hz to 20Hz segmented into between 3-second and
30-second window sizes. The suggested features are a combination of motion
intensity, orientation, and shape. The recommended models are supervised ma-
chine learning techniques like support vector machines, RFs, or convolutional
neural networks.

2.1.2 Anomalous situations and rare behavior detection

Areas of focus for studies using 3D accelerometers for behavior analysis are typ-
ically the classification of either regular behavior or anomalous behavior. Regu-
lar behavior can include grazing, ruminating, lying, and steady standing while
anomalous situations can include disease detection, predator attacks, or birthing
signals. Papers focusing on unusual behavior typically have a much lower de-
tection accuracy than regular behavior, usually due to a lack of data. Machine
learning models require many observations of a certain behavior in order to learn
how to detect it, something which is a large problem when it comes to irregular
behavior [7]. Animals in anomalous situations typically display more complex
behavior as well, for example, predator attacks could be identified by the cows
stopping grazing for extended periods of time and then moving away, and disease
could be shown by unusual resting behavior, abnormal walking, absence of neck
movement, and low overall activity. The complexity of the behaviors requires
even more data to accurately detect, furthering the issue of dataset limitations
[4]. Due to the limited data available, this thesis will focus on the regular behav-
iors that commonly occur in the collected dataset.

2.1.3 Precision livestock technologies for animal welfare

Schillings et al. [20] published a study in 2021 discussing the potential of pre-
cision livestock technologies to automate animal health monitoring and the wel-
fare status of farm animals. The study uses a Five Domains Model framework
to categorize technologies by type, development stage, species application, and
welfare impact. Body-mounted accelerometers are one of the technologies exam-
ined, and the results indicate a high potential for sensors to be useful for various
applications such as disease detection and birth. However, the study raises con-
cerns about these technologies being able to reduce the occurrence of negative
states, but not contribute to promoting positive welfare states. Risks involving
the human-animal relationship are also mentioned, cautioning that this technol-
ogy could reduce the frequency and quality of interaction between humans and
animals, ultimately reducing animal welfare .

2.2 Embedded programming of accelerometer tags

This thesis aims to add to the functionality of the animal activity tags, and as
such, embedded programming of the tags themselves is required. Embedded

2.3 Accelerometer data analysis

7

programming refers to the practice of writing code for embedded systems, often
microcontrollers, that are part of a larger electronic system. Examples of embed-
ded systems are camera systems, digital watches, gaming consoles, and even cars
and other vehicles. The computing systems within the embedded systems are
typically very small, and as such, they often have limited computing, memory,
and storage. They often have to interact closely with integrated sensors and work
within tight time constraints.

Most existing works on animal behavior recognition are offline and centralized
approaches in which sensor data is stored on the tag and later transmitted wire-
lessly to be computed elsewhere. However, some solutions use local calculations
and a lightweight classification directly on the tags, which has been shown to
increase battery life as data processing is cheaper than data transmission [8].

2.3 Accelerometer data analysis

The use of accelerometers as a tool for collecting data for animal behavior anal-
ysis is becoming increasingly prevalent [22]. The strength of the technology lies
in the fact that it is a small, lightweight sensor that can always gather data, even
when direct observation is not possible. As machine learning techniques have
developed in the last decade, it has become easier and easier to sift through and
process the massive amount of data that an accelerometer can generate, especially
at higher resolutions and with up to three spatial dimensions. The main goal of
accelerometer data analysis is to identify patterns in the generated waveforms
and, in this case, to classify them with a known corresponding behavior or move-
ment of the animal [13].

Utilizing 3-dimensional accelerometer sensors requires effective analytical meth-
ods to accurately and reliably identify behaviors from raw data. The accelerom-
eter captures signals along three axes: the x-axis, y-axis, and z-axis. These mea-
surements are typically represented as a time series, with each acceleration value
corresponding to a specific recording time. By segmenting this time series, statis-
tical features can be extracted, providing a comprehensive representation of the
accelerometer data. These features are then used to predict the targeted behav-
iors accurately.

Preprocessing of data can vary in its specifics, but generally follows a consistent
framework. This typically involves the following steps: first, cleansing the raw
time-series data to eliminate any noise. Next, a generation of supplementary
time-series data is carried out. Then, the full time series is divided into smaller,
distinct time windows. The full data collection time can be several hours or even
days long, and this is converted into small windows, each being only a few sec-
onds long. The final step involves extracting features from each of these time win-
dows for further analysis. Typical features extracted from the time windows are
mean, standard deviation, minimums, and maximums for each axis, or frequency-

8

2 Theory

domain features like Fourier Transform representations [1].

2.3.1 Spectral analysis

Once the data has been divided into time windows, one useful way of analyzing
the signals is to use spectral analysis, which involves breaking down a complex
signal into its constituent frequencies to study its spectral content. Spectral anal-
ysis is an invaluable tool in signal processing, especially when trying to uncover
the frequency components of a time-domain signal. In essence, it allows us to
identify the different frequencies that make up the overall movement and activ-
ity pattern, which is especially pertinent for understanding complex animal be-
haviors. Spectral analysis is based on the principle that any signal or waveform
can be represented as a sum of sine and cosine waves with different frequencies,
amplitudes, and phases. One method is to use a Fourier transform to transform a
signal from its original domain, in this case, the time domain, into the frequency
domain. While the Fourier transform typically uses a continuous frequency vari-
able, we utilize the Discrete Fourier Transform (DFT) for computational purposes.
The DFT is discrete in both time and frequency and is applied to signals that have
been sampled discretely. To perform this type of transform on a computer we first
discretize the signal x by sampling it N times. The formal definition of the DFT
for a sequence of values x0, x1, . . . , xN −1 is given by:

X(k) =

N −1(cid:88)

n=0

−i2π nk
N

xn · e

(2.1)

The output sequence X(k) is a complex-valued function of the frequency index k,
where the magnitude |X(k)| gives the amplitude of the corresponding frequency
component, and the argument arg(X(k)) gives the phase offset. Essentially, the
operation takes one sequence of real numbers as input, typically sampled values
of a function at discrete time intervals, and turns them into another sequence
that represents the frequency domain of the input sequence. This can reveal un-
derlying structures and properties of the signal that are not immediately obvious
in the time domain.

The accelerometer signals can be processed in a combined way or for each of
the X, Y, and Z axes separately. Both methods have shown promising results with
this kind of data. However, recent studies in animal behavior analysis suggest
that processing the axes separately can be advantageous for detecting certain be-
haviors [14].

Using spectral analysis and Fourier transforms on accelerometer signals can be
highly useful for recognizing animal behavior. For example, in the paper by [4]
Cabezas et al., two of their models’ top five most important features come from
the frequency domain of their accelerometer signals when recognizing grazing
and standing.

2.3 Accelerometer data analysis

9

In computational applications, directly calculating the DFT as defined by Equa-
tion 2.1 can be computationally expensive, especially for large datasets, due to
its complexity of O(N 2). To address this, the Fast Fourier Transform (FFT), an
algorithm with a much lower computational complexity of O(N log N ), is used.
The FFT is a family of algorithms that utilizes trigonometric symmetries in in
the DFT to drastically reduce the number of arithmetic operations required. The
most common FFT algorithm is the Cooley-Tukey algorithm, which recursively
breaks down a DFT of any composite size N = n1n2 into many smaller DFTs of
sizes n1 and n2, taking advantage of the periodicity and symmetry properties of
the complex exponential functions. A mathematical representation of the FFT
can be written as follows:

X(k) =

N /2−1(cid:88)

m=0

−i2π mk

N /2 · x2m + e

−i2π k

N · e

−i2π mk

N /2 · x2m+1

e

(2.2)

This equation outlines the Cooley-Tukey FFT algorithm [6] for the case of even-
odd decomposition of the DFT. Here, x2m and x2m+1 represent the even and odd-
indexed samples of the original dataset, respectively.

At first, this equation may look more complicated than the original DFT pre-
sented in Equation 2.1, but computationally it is much cheaper. The reason for
this efficiency lies in breaking down a single N -point DFT into smaller DFT op-
erations, specifically into two N /2-point DFTs [9]. To understand the computa-
tional savings, consider the calculation cost of the original DFT, which requires
N 2 complex multiplications if calculated regularly. When applying the FFT algo-
rithm as shown in Equation 2.2, each recursion reduces the number of multiplica-
tions needed. Specifically, in each stage of the recursion, the number of complex
multiplications required is halved. The computation at each level involves N mul-
tiplications, and because the depth of the recursion is log2(N ), the total number
of complex multiplications sums up to N log2(N ). This is a significant reduction
from the N 2 operations required by the straightforward DFT computation. In
real world situations with realistic values of N , this difference is extremely im-
portant.
It can turn situations where millions of multiplications are required
into ones where only a couple thousand multiplications need to be performed. It
allows for rapid analysis of data in near real-time, and the benefit only gets larger
as the dataset grows larger.

2.3.2 Jerk Filter for motion analysis

In signal processing, the analysis of movement often involves filtering noise from
motion capture or sensor data. One important aspect of motion analysis is the
smoothness of movement, which can be quantified using the concept of jerk, the
rate of change of acceleration. Hämäläinen’s jerk filter [10] is a specific tech-
nique used to reduce noise in acceleration data by minimizing jerk, leading to
smoother and more interpretable results. The jerk filter focuses on reducing the
high-frequency components of jerk in the signal, which are often associated with

10

2 Theory

noise. Jerk is defined as the third derivative of position with respect to time. If
x(t) represents the position at time t then

j(t) =

d3x(t)
dt3

(2.3)

The implementation of Hämäläinen’s jerk filter typically involves numerical op-
timization techniques like gradient descent, where the goal is to minimize the
following cost function:

J =

T(cid:90)

(cid:16)

0

λ1

∥x(t) − xmeasured(t)∥2 + λ2

∥j(t)∥2(cid:17)

dt

(2.4)

where λ1 and λ2 are parameters to control the smoothness of the resulting signal.
However, this would likely be an unnecessarily complex computation to perform
on the activity tag. Instead, a simplified version of the jerk-filter is used in this
thesis using NumPy’s ”numpy.diff()” function to smooth the data by numerically
approximating the derivative.

2.3.3 Sensor positioning

Researchers have debated where the optimal location for an accelerometer should
be for livestock behavior analysis. There are several aspects to consider and bal-
ance, with one issue being the problem of animal comfort. The sensors need to be
small and positioned in a way that does not restrict the animal’s freedom of move-
ment. Another key issue is the problem of recording accurate and reliable data.
Typically, tracking sensors of this type are either fastened around the animals’
necks using a type of necklace, as an ear-tag, or attached around one of the legs
as a leg-band. Different sensor positions have varying strengths and weaknesses
when recording accelerometer data. A study using collar-based accelerometers by
[15] Martiskainen et al. found that certain behaviors, such as standing, lying, and
ruminating, had nearly an identical pattern when using an accelerometer in the
neck position. Another study by [10] Hämälainen et al. found success in detect-
ing rumination and eating using a necklace-based accelerometer. However, the
collar would at times move around, causing difficulty in measuring. Sudden head
movements would also cause a disturbance, making some behaviors difficult to
recognize. Other solutions include fastening the sensor as an ear tag. As shown
by [1] Barwick in 2017, an ear tag may be able to capture a wider range of animal
movements while also being easier to apply and remove as ear tag procedures
and tools already exist in the industry. However, ear tags must be much smaller
than collar-based sensors to prevent animal discomfort which heavily limits sen-
sor size and, in turn, battery size.

The collar solution is preferred over the leg band in this situation as it allows for
better accelerometer data from head movement. The legs could be completely
still while the head moves around, causing a potential loss of information. The
collar is also preferred over the ear tags due to the increased battery life. The neck

2.4 Machine learning models for behavior analysis

11

position is also recommended by L. Riaboff et al. for analyzing feeding behavior
and simple motion and resting positions [19].

2.4 Machine learning models for behavior analysis

For effective behavior classification using accelerometer data, it is crucial to de-
velop and train a suitable machine learning model. Given the wide variety of
available models and techniques, selecting the appropriate ones is pivotal, tak-
ing into consideration the specific characteristics of the data and the hardware
constraints of the activity tags. Broadly, these models can be categorized into
supervised and unsupervised learning approaches. Supervised learning models
rely on a dataset that is already labeled, meaning each piece of accelerometer data
is tagged with the correct behavior. This allows the model to learn from a vast col-
lection of such labeled data, enabling it to classify behaviors in new, unseen, and
unlabeled data. On the other hand, unsupervised learning models do not require
labeled datasets. Instead, they identify patterns within the data and group simi-
lar data points into classes. Given the objective of this project to classify specific
known behaviors, supervised learning models are identified as the most appro-
priate choice for this task. As for specific models, previous works have shown
good predictive performance on similar datasets using random forests (RF), and
while this method is relatively lightweight in complexity, it is likely too memory-
intensive to run well on a microcontroller such as the one on the activity tag [19].
For that reason, the choice is made to run the full RF model separately from the
activity tag and implement a simplified version of it on the tag itself. as a first
step toward creating a simplified model on the tag itself to provide reasonably
accurate results at a fraction of the computational cost.

2.4.1 Decision trees

A decision tree is a supervised machine learning model used for classification and
regression. They are known for their simplicity and versatility but can be prone
to overfitting the training data and perform poorly on unseen data [17]. Deci-
sion trees can be likened to a flowchart-type structure where one starts at the
root node which splits into different branches that represent various properties
of the data. The decision-making process is straightforward, a node asks a ques-
tion about the data and follows the branch that corresponds to the answer. This
repeats until the final node, the leaf node, is reached and provides the predicted
label for that data point. A simplified decision tree can be seen in Figure 2.1. In
the example tree, it takes in the features derived from a data point and makes two
decisions. One data point is all accelerometer data gathered in a single 10-second
time window. First, if the standard deviation of the data in the Z-axis is above 2.5
m/s2 it classifies the sample as walking. If not, the tree looks at whether the mean
of the acceleration in the X-axis is above -5.0 m/s2. If it is, the sample is classified
as standing, and if not, the sample is classified as lying. In real applications, the
trees would be more complex with many more nodes, but the example gives an

12

2 Theory

idea of how a decision tree can be used to classify activities using accelerometer
data.

Figure 2.1: Example of a simplified decision tree classifying animal behavior
using features of accelerometer data.

2.4 Machine learning models for behavior analysis

13

2.4.2 Gini Impurity

To determine how to make decision splits at each node, decision trees employ
metrics to measure the best split based on the purity of a node. One commonly
used metric is the Gini impurity [11], which is also the split metric of choice in
this thesis. Gini impurity is a measure of how often a randomly chosen element
from the dataset would be incorrectly labeled had it been randomly labeled ac-
cording to the label distribution present in the dataset. In other words, how well
the tree separates the classes. In its simplest form, the Gini impurity for a node
in the decision tree can be mathematically expressed as:

IG(p) = 1 −

J(cid:88)

i=1

p2
i ,

(2.5)

where pi is the proportion of samples of class i in the dataset and J is the total
number of classes. When building a decision tree, all possible splits are evalu-
ated for each feature, and the resulting Gini impurity is calculated from each
potential split. The objective is to find the split that results in the lowest possible
Gini impurity compared to the current node’s impurity. A potential split can be
evaluated using

∆IG = IG(parent) −

(cid:32) Nlef t
N

IG(lef t) +

Nright
N

(cid:33)

IG(right)

.

(2.6)

In Equation 2.6, ∆IG represents the change in Gini impurity from a parent node
to its child nodes in the form of a weighted average. Here, N is the number of
samples at the parent node and Nlef t and Nright are the number of samples at
the left and right child nodes, respectively. The potential split that reduces the
the Gini impurity the most, i.e., the largest ∆IG is chosen for that node. There
are metrics other than Gini impurity that accomplish the same goal, but Gini
impurity is favored in this use case for its computational efficiency as it does not
involve logarithmic calculations like many other similar metrics do.

2.4.3 Calculating Feature Importance Using Gini Impurity

As a further benefit of calculating Gini impurities at each node, it can also be
used as a way to rank the importance of features in the tree. This is especially
beneficial in this thesis as the end goal is to make a very lightweight model with
only a small number of features. These features will be selected from the most
important features calculated from a larger model.

The process of computing feature importance using Gini impurity involves sev-
eral steps that aggregate the impurity decrease attributed to each feature across
all decision trees in the ensemble. First, whenever a feature is used to split a node,
the reduction in Gini impurity is calculated and stored. This reduction represents
how much the split helped in clarifying and separating the data. Next, these im-
purity decreases are weighted depending on how many samples reach the node in

14

2 Theory

question. This ensures that splits that affect larger parts of the dataset get ranked
more highly. Finally, if one is using multiple decision trees, the importance gets
averaged across all trees and normalized to sum up to one. The mathematical
expression for calculating the importance of a feature f can be represented as:

If =

1
T

T(cid:88)

(cid:88)

t=1

n∈Nf ,t

(Df ,n

× Pn,t),

(2.7)

where Df ,n is the decrease in Gini impurity at node n due to feature f ,
Pn,t is the proportion of samples reaching node n in tree t,
Nf ,t represents the set of nodes in tree t that split on feature f , and
T is the number of trees.

By quantifying the reduction in Gini impurity that each feature achieves, this
metric provides a robust measure of each feature’s relative importance within
the model. This calculation not only helps understand which features are most
predictive but also helps in interpreting the model by identifying the features
that significantly influence the target variable. This knowledge is invaluable in
both improving model performance and understanding the underlying patterns
in the data.

2.4.4 Random forests

The Random Forest classifier builds upon and improves the decision tree method
using ensemble learning. It operates by constructing many decision trees and
combining their individual predictions. The fundamental concept is that com-
bining many decision trees and taking the mean of their predictions will lead to
more stable and more accurate predictions. To further reduce the risk of over-
fitting that single decision trees had, RFs apply two techniques; bootstrap aggre-
gating and feature randomness [3]. In bootstrap aggregating, multiple different
subsets are created from the original dataset with replacement, meaning that sub-
sets can contain the same data point. Each decision tree is trained on one of these
subsets to introduce variety among the trees. During the construction of the trees,
when decision splits occur at a node, the feature choices are taken from only the
subset and not the full dataset. This is called feature randomness and further
introduces variety among the trees to reduce overfitting, leading to increased ac-
curacy on unseen data. The RF model is favored for its ability to produce accurate
results and its ability to handle large datasets of high-dimensional data efficiently.
These abilities make the algorithm highly applicable to the problem of classify-
ing animal behavior from accelerometer data, as the number of features can get
very large depending on how the preprocessing is done.

The classifier’s complexity, and in turn prediction ability, is dependent on the
number of trees in the forest. This is a key hyperparameter that must be tuned
to fit the needs of the specific problem. As the number of trees in the forest in-
creases, the variance of the model decreases, making the model more robust to

2.4 Machine learning models for behavior analysis

15

noise in the training data. However, beyond a certain point, adding more trees
yields diminishing returns in performance improvement and can unnecessarily
increase computational complexity and memory usage. This is, in theory, the
worst that can happen though, as RFs are designed not to overfit as the number
of trees increases. As more trees are added to the RF, the variability in the model’s
predictions decreases, and the generalization error P E stabilizes. This stabiliza-
tion occurs because the ensemble’s predictions become more robust due to the
averaging process over many trees. According to Breiman [3], the generalization
error of an RF converges to a limit due to the Strong Law of Large Numbers,
which ensures that the average prediction of a large number of independent trees
becomes stable.

Each tree hk(x) in the RF ensemble is trained on a different subset of the train-
ing data, randomly drawn from the distribution of feature vectors X and class
labels Y . The generalization error P E, which specifies the probability of a wrong
classification on new data is related to the difference that the forest correctly pre-
dicts class Y and the highest probability of incorrectly classifying it as j. The
relationship is expressed as:

(cid:32)

(cid:33)

P E = PX,Y

ρ(h(X, Θ) = Y ) − max
j(cid:44)Y

PΘ(h(X, Θ) = j) < 0

.

(2.8)

Here, P E is the probability of an incorrect classification by the ensemble. It is de-
fined as the difference between the probability that the ensemble predicts the cor-
rect class Y for a feature vector X, denoted by ρ(h(X, Θ) = Y ), and the maximum
probability of predicting any other incorrect class j, across all randomizations Θ
within the forest.

Breiman further elaborates that the generalization error P E of an RF is bounded
by:

P E ≤ P E

(cid:32)
1 −

s2
1 + s2(k − 1)

(cid:33)

,

(2.9)

where P E is the error rate of a single tree and s is the average accuracy of the
individual trees. This implies that as the number of trees k increases, the gener-
alization error is at most equal to the average error of a single tree.

In the scope of this thesis, random forests are used as an analysis method sep-
arate from the activity tag, due to memory constraints on the chip. By training
the RF on a separate computer, we get an accurate, in-depth analysis of the data
and learn suitable feature thresholds for the tag’s simpler model. This separate
model is allowed to have high complexity as it only has to run once on a much
more powerful machine than the embedded system on the tag.

16

2 Theory

2.5 Synthetic Minority Oversampling Technique

One common issue for many machine learning datasets is that they are often im-
balanced. Samples of each behavior class that make up the dataset do not show
up an equal number of times. There are typically more commonly occurring
classes and more rare classes. This can lead to problems when trying to classify
these underrepresented classes. For the cow dataset, the walking class was one
such underrepresented behavior. The deficit in data samples of this type caused
major problems for the models’ ability to correctly classify data windows of the
’Walking’ class for cows. This problem will be discussed further in the Results
chapter.

The simplest approach to address this problem is to simply duplicate examples
of the minority classes. However, while this can help with balancing the dataset,
it does not provide any new information to the model and typically does not
improve performance by much.
Instead, a better approach is to synthetically
generate new samples from existing ones by transforming them slightly. This is
known as data augmentation [24]. One commonly used method of data augmen-
tation is called Synthetic Minority Oversampling Technique (SMOTE) [5], which
is also the data augmentation method used in this thesis. SMOTE works by se-
lecting examples that are close in the feature space using the k-nearest neighbors
algorithm, then drawing a line between the examples in the feature space and
creating a new sample at a point along that line. This line, known as a feature
vector, is represented as an n-dimensional vector for a data point i, where n is the
number of features as

Xi = [xi1, xi2, ..., xin].

Essentially, it is an array containing all the values of each feature for one sample
in the dataset. Next, neighbors are calculated for these vectors by finding the
Euclidean distance. A new vector is then calculated as the difference between
the selected instance Sorig and its neighbor Sneigh. Finally, to create the synthetic
sample Snew, this difference vector is multiplied by a random number r, which
ranges between 0 and 1. The result of the multiplication is then added to the
feature vector of the original instance. Mathematically, it can be expressed simply
as

Snew = Sorig + (Sneigh

− Sorig ) · r

(2.10)

This method was used as a countermeasure to try to improve classification for
the underrepresented classes in this thesis, namely the ’Walking’ class for the
cows and the ’Lying’ class for the goats. This was implemented with the help of
the Python ’imblearn’ library. For the oversampling process, the parameter k in
the k-nearest neighbor algorithm was set to 5.

2.6 Evaluation Metrics

17

2.6 Evaluation Metrics

Evaluating the performance of machine learning models is crucial to understand-
ing how well the models are predicting the behaviors of interest and to guide
improvements in the model development process. This thesis uses four metrics
to evaluate the performance of the machine learning models: accuracy, preci-
sion, recall, and the F1-score. By utilizing these four metrics, this study aims
to provide a comprehensive evaluation of the machine learning models’ perfor-
mance and reliability. Each metric offers important insights into the model’s
performance, especially considering the imbalanced nature of the dataset. The
following subsections will define each metric and discuss its relevance to this
study. Each definition will be given in terms of true positive, true negative, false
positive, and false negative classifications (TP, TN, FP, and FN, respectively). If
the correct label on a data sample is T rue, and the model correctly classifies it
as T rue, it is a TP. On the other hand, if the correct label is T rue but the model
incorrectly classifies the sample as False, it is FN. The same pattern applies to
the False labels.

2.6.1 Accuracy

Accuracy is the most intuitive performance measure and it simply represents the
ratio of correctly predicted observations to the total observations. It is defined as:

Accuracy =

T P + T N
T P + FP + FN + T N

(2.11)

This is a metric that determines the overall prediction accuracy for the entire
dataset over every behavior class. While accuracy is a very straightforward metric,
it is not always the best indicator of performance in the context of imbalanced
datasets, as it can be skewed by the majority class. For instance, it is possible to
get a very good-looking overall accuracy on a model that is in reality only able to
accurately classify the frequently appearing classes in the dataset but performs
poorly on less frequently appearing classes. Despite its weaknesses, accuracy
can serve as a solid measure to get a quick understanding of the model’s overall
performance.

2.6.2 Precision

Precision, or the positive predictive value, measures the accuracy of the positive
predictions. It is a class-specific metric, meaning that each behavior category will
have its own precision value. Precision is a particularly useful metric in scenar-
ios where the cost of false positives is high. For example, if one is examining
the health status of an animal and the model incorrectly identifies an animal as
having an irregular walking pattern or lying down frequently, it could lead to un-
necessary medical examinations or treatments which could be costly. Precision is
defined as follows:

P recision =

T P
T P + FP

(2.12)

18

2 Theory

In the context of this study, high precision in detecting specific behaviors like
walking indicates a low rate of misclassification of other behaviors as walking,
which is essential for minimizing false alarms in behavior detection systems.

2.6.3 Recall

Recall, also known as sensitivity or the true positive rate, measures the model’s
ability to correctly identify all relevant instances. For behaviors that are crucial
to detect accurately for animal welfare or health monitoring, a high recall is desir-
able. Similarly to precision, recall is also a class-specific metric. It is calculated
as:

Recall =

T P
T P + FN

(2.13)

A high recall rate for rare behaviors such as walking or grazing indicates the
model’s effectiveness in identifying these behaviors when they occur, despite
their infrequent representation in the dataset.

2.6.4 F1-Score

The F1-score is the harmonic mean of precision and recall, providing a single
metric to assess the balance between them. Each individual class will also have
its own F1-score as it is based on the class’s individual precision and recall scores.
This metric is especially useful in situations of uneven class distributions. This
is an inevitable outcome when gathering live data from cows. Certain behaviors
such as walking occur much less frequently than lying down or eating. The F1-
score is defined as:

F1-Score = 2 ·

P recision × Recall
P recision + Recall

(2.14)

Given the imbalanced nature of the dataset, with certain behaviors being under-
represented, the F1-score becomes a critical metric for evaluating model perfor-
mance, offering a more balanced view than accuracy alone. It also serves as a
single metric that combines both precision and recall, as it is important to have a
high score in both of these metrics. The F1-score helps you understand how well
your model balances the need to identify all positive cases (recall) while minimiz-
ing incorrect positive predictions (precision).

For example, consider a scenario where there are 100 data samples of the walk-
ing category. One could get a precision of 100% for the walking class by simply
correctly classifying just 3 of these samples as walking and never classifying any-
thing else as walking. Conversely, one could get a recall score of 100% for the
walking class by simply classifying everything as walking. Of course, this would
lead to a very poor precision score and extremely poor performance for every
other class. For these reasons, it is important to consider the balance between
precision and recall, and that is the purpose of the F1-score.

3

Methodology

This chapter outlines the methodology used for examining animal activity via
accelerometer tags. Subsequent sections provide a detailed description of the
physical tags’ hardware, including the technical specifications and capabilities
of their internal components. Additionally, this chapter delves into the types of
data collected, the process of data collection, and the techniques used for data
preprocessing. Figure 3.1 provides an overview of the general workflow adopted
in this project, from the initial data collection through to the preprocessing and
final analysis stages. This figure serves as a guide to the detailed methodologies
that will be discussed in the following sections.

Figure 3.1: A structured outline of the project’s methodology divided into
three main components.

19

20

3 Methodology

3.1 Hardware description

The used activity tag model is a combination of two main components, the nRF52840
wireless system-on-chip (SoC), and the LIS2DS12 accelerometer, both of which
will be presented in this section.

3.1.1 System-on-chip nRF52840

The nRF52840 developed by Nordic Semiconductor [18], is an ultra-low power
2.4GHz wireless SoC highly suitable for handling complex wireless tasks.
Its
power efficiency, versatility, and Bluetooth low energy (BLE) communication ca-
pabilities make it an ideal choice for the animal activity tag. The technical speci-
fications of the chip can be seen in Table 3.1.

Specification
CPU
Flash Memory
RAM
Cache
Radio
Power Consumption
Size
Operating Temperature

Details
32-bit ARM Cortex-M4F @ 64 MHz
1 MB
256 KB
Integrated (size not specified)
BLE 5, ANT, 2.4 GHz proprietary
0.4 µA OFF mode, 1.5 µA ON mode @ 3V
7mm x 7mm x 0.675mm
-40°C to 85°C

Table 3.1: Technical Specifications of the nRF52840 SoC

3.2 Method Validation using Goat dataset

21

3.1.2 Accelerometer LIS2DS12

The LIS2DS12, developed by STMicroelectronics [23], is the accelerometer of
choice for the activity tag. It is a three-axis ultra-low power accelerometer de-
signed for high-resolution motion detection and equipped with a built-in step
Its compact size and power efficiency make it a popular choice for
counter.
portable applications such as the tags used in this study. Key features and techni-
cal specifications of the accelerometer are listed in Table 3.2. For this project, the
accelerometer will be configured to ±2g sensitivity with 25Hz sampling rate, the
minimum required output rate of the built-in step counter.

Specification
Sensing Axes
Sensitivity
Output Data Rates (ODR)
Resolution
FIFO Buffer
Power Consumption
Communication
Size
Operating Temperature

Details
3-axis (X, Y, Z)
Selectable from ±2/4/6/16g
From 1 Hz to 6.4 kHz
Up to 16 bits
256 samples
2.5-8 µA (1-50Hz), 0.7 µA in power down mode
I2C/SPI digital interface
2mm x 2mm x 0.65mm
-40°C to +85°C

Table 3.2: Technical Specifications of the LIS2DS12 Accelerometer

3.2 Method Validation using Goat dataset

Prior to the main data collection and analysis, the methodologies developed for
this study were initially tested on an independent dataset involving goats [12].
The structure of the dataset is similar to the one collected and created during
this thesis, with a few notable differences. The data was gathered using 3-axis
accelerometers with a sensitivity of ±8g fastened to the collars of goats with a
sample rate of 100Hz, but this was downsampled to 25Hz before testing the
methods by simply only using every fourth row in the dataset. The authors of
the goat dataset also experimented with multiple sensors in several different po-
sitions, and the dataset is split into different files corresponding to these different
positions. To more closely follow the methodology of the data collection of the
cow dataset, only one of these files was used, as the cow will only have one sensor
in one position. There was also gyroscope and magnetometer data available but
those were discarded and not used for any of the features. However, the main
difference is the sheer size of the dataset. The goat data was gathered over many
days, and on 5 goats simultaneously, which was possible as there were multiple
human observers working on the project. In total there is over 200 hours of goat
data, but only about 50 hours of this data was used, as the rest was with different
sensor positions.

22

3 Methodology

The number of samples per class in the goat dataset can be seen in Table 3.3
and Figure 3.2. From this, we can see that the ’Lying’ class is severely underrep-
resented. The goat data was only collected during the daytime and the animals
seemed to be quite active during this time, skewing the behavior to the other be-
haviors, resulting in an unbalanced dataset. One point of interest compared to

Figure 3.2: Pie chart showing the distribution of behavior classes within the
goat dataset.

Table 3.3: Number of samples per behavior class for the goat dataset using a
window size of 2.4 seconds.

Behavior Number of Data Samples
Standing
Walking
Eating
Lying
Grazing

5131
2558
2950
104
3686

the cattle dataset is that the goat dataset does not have a label for ruminating.
Instead, the authors chose to separate ’Eating’ and ’Grazing’. The separation in
these two behaviors is described in the documentation to be that grazing is when
the animal is pulling fresh grass out of the ground while eating is when the ani-
mal is consuming hay from a pile, twigs from the ground, or fed pellets from a
human. [12]. This separation could not be made in the cattle dataset as it was
recorded during winter and early spring when the cows are fully indoors and

3.3 Data collection

23

there is no grass to graze from.

Aside from ruminating and grazing, the behaviors recorded are directly compa-
rable to those recorded in the cattle dataset. This allows for a direct assessment
of how well the methodologies transfer across different species. Although goats
and cows have distinct behavioral and physiological differences, their fundamen-
tal behaviors have enough similarity to make the goat dataset a valuable proof of
concept for the methods developed. Successfully predicting behaviors in goats
demonstrates the potential of these methods to be generalized across different
species. This cross-species validation is particularly important given the broader
goal of Qulinda AB to eventually adapt the activity tags for use on rhinos, in col-
laboration with Kenya Wildlife Service, and various animal sanctuaries in Africa.
The ability to generalize across species shows the robustness of the methodolo-
gies, which can give confidence in their applicability to other animal behavior
classification use cases.

3.3 Data collection

The data collection for this study was conducted at Vreta utbildningscentrum, a
large farm and education center located in Östergötland. As the data collection
was done during winter and early spring, the cows were indoors during the whole
process, possibly limiting the display of certain behaviors such as walking. The
data was collected using the animal activity tag composed of the hardware dis-
cussed in Section 3.1.1 and Section 3.1.2. The tags were set to sample data at a
frequency of 25Hz with a sensitivity of ±2g. The methodology used for data col-
lection was twofold, combining direct behavioral observations with accelerome-
ter data capturing. Each cow was equipped with an activity tag fastened securely
to its neck collar, ensuring that the accelerometer data accurately reflected the
cow’s movements without causing discomfort or hindrance to its natural behav-
iors. Figure 3.3 shows a cow of the Swedish Red-and-White breed wearing a collar
with the attached activity tag to monitor movement.

Data was collected over a period of six hours on three separate cows of the breeds
Swedish Red-and-White and Holstein Friesian (Bos taurus taurus). Data was only
captured from one animal at a time, each for around two hours per animal. This
was to allow the observer to follow and video capture the animal during the en-
tire collection period. Additionally, specific effort was made to ensure that the
targeted cows displayed a variety of behaviors. One of the selected cows was
relatively active and spent time eating and moving around the enclosure, while
another was comparatively calm and mostly laid down ruminating. Capturing
varying behaviors results in a richer dataset and a more comprehensive classifi-
cation model. In parallel with the accelerometer data collection, the cow’s behav-
iors were documented through continuous video recording. This simultaneous
recording allowed for the precise annotation of the accelerometer data after data
collection, taking note of the observed behaviors at corresponding timestamps.

24

3 Methodology

Figure 3.3: A Swedish Red-and-White breed cow wearing the animal activity
tag, attached with a neckband.

The video recordings served as a critical reference, enabling accurate categoriza-
tion of the displayed behaviors relevant to the study. Segments of data were
excluded from the dataset when the activity of the cow for that segment could
not clearly be recognized in the video (e.g. when the cow has moved behind an
obstacle or other animals). Additionally, outlying behaviors that did not fall into
one of the predetermined behaviors, such as grooming or using the scratching
pole, were labeled unknown and eventually discarded from the dataset. These
were behaviors that did not occur frequently enough to predict accurately so in-
cluding them would only damage the model’s performance.

Once the recordings were fully examined and behavior was documented for the
full video length, a script was made to match the labels with the accelerometer
data, matching the annotated timestamps and behaviors to each data window’s
UNIX timestamp. The result was then a fully annotated dataset ready for sub-
sequent processing and analysis. If a data window spanned across a behavior
transition, for example, if part of the 2.4-second data window was spent stand-

3.3 Data collection

25

ing still and the other part was spent walking, the sample was labeled transition.

The raw dataset itself was never used directly on the activity tag or its SoC. In-
stead, the dataset was only used for a separate analysis using an RF model to
calculate node split thresholds and determine relevant features to use on the tag
to perform inference.

The recording duration was 6 hours long and the documented behaviors were:
standing, walking, eating, lying, ruminating while lying down, and ruminating
while standing. The choice was made to separate ruminating into two categories
as it could be relevant to extract certain behavioral information. If one wants to
calculate a total time spent ruminating, it could easily be done by adding the two
categories. If they were to be combined into a single ruminating class, the user
would not know how much time was spent standing or lying down, which could
be relevant to assessing the animal’s welfare. Excessive amounts of time spent
lying down could indicate injury or sickness. A breakdown of the behaviors and
how often they occur in the dataset can be seen in Table 3.4 and Figure 3.4. Each
data sample corresponds to a full 2.4-second accelerometer data window com-
prised of 180 individual acceleration measurements (60 for each of the X, Y, and
Z axes).

Figure 3.4: Pie chart showing the distribution of behavior classes within the
cattle dataset.

At a glance, it can be seen that there are very few occurrences of the walking and
lying without ruminating classes. There are also quite few transition samples,
but that is not as much of an issue as transition is not likely to be a behavior of
interest. The class could however be included into the training set to make the
models more robust and generalizable. Countermeasures to remedy this dataset
imbalance will need to be applied to try to improve the scores on the underrepre-

26

3 Methodology

Table 3.4: Breakdown of behaviors and their occurrences in the cattle dataset
using a window size of 2.4 seconds.

Behavior
Ruminating (Standing)
Standing
Eating
Ruminating (Lying Down)
Walking
Transition
Lying

Number of Data Samples
1554
1549
1200
1102
261
178
136

sented classes, especially walking as it is the more complex and harder to identify
behavior.

3.4 Data preprocessing and managing

Once data has been collected and labeled, the next step in the pipeline is pre-
processing. This step is composed of several key processes: the initial storage of
accelerometer data, its subsequent transformation into a more analyzable form,
and the derivation of features from the transformed data. Given that the process-
ing and analysis tasks will be executed directly on the System on Chip (SoC) with
its limited memory, careful consideration is required in the selection of features
to compute. The SoC’s capabilities are significantly constrained not just in terms
of storage capacity, but also regarding the complexity of computational models
it can efficiently manage, such as decision trees. Using too many features in a
shallow decision tree can lead to underperformance due to underfitting and com-
promise the model’s interpretability [2]. To combat these limitations, only the
most relevant and important data features can be selected and used for the SoC
model. This refined subset of features is derived from a more comprehensive ma-
chine learning model, which is trained externally to the SoC environment. The
model of choice for the more complex external mode is a Random Forest, which
is the natural upgrade of a decision tree as it is simply an ensemble of multiple
decision trees working together.

This strategy ensures that the SoC operates efficiently without compromising the
accuracy and effectiveness of the behavioral classification task. It also allows the
model to focus on high-impact features, significantly enhancing the efficiency of
data processing and analysis on the SoC while ensuring that critical information
is neither lost nor overlooked. Performing this type of analysis directly on a small
embedded system or microcontroller is always a fine balancing act between com-
putational efficiency due to hardware constraints and obtaining accurate results.

The preprocessing phase involves transforming the data into various represen-
tations suitable for feature extraction. An outline of the preprocessing workflow

3.4 Data preprocessing and managing

27

is illustrated in Figure 3.5.

Figure 3.5: Preprocessing and feature extraction workflow for the ac-
celerometer data.

In the first step, time signals are divided into consecutive, non-overlapping time
intervals or time windows. This task is performed directly on the activity tag,
with a hyperparameter to control the window size. The window size is controlled
by specifying a maximum buffer size, M. The SoC transmits the buffered data to
the scanner once the buffer is full. As mentioned previously, the internal maxi-
mum buffer size was set to 180 during data collection, containing 60 values for
each axis (X, Y, Z). From this, the time window size can easily be calculated using

Twindow =

f
M

.

(3.1)

The sampling frequency f was set to 25Hz, and as such, the window size for the
data collection was 2.4 seconds. While on the lower end, this window size is in
line with the recommendation from Riaboff et al. of using 2 - 15 second windows
[19]. However, windows can easily be stitched together during preprocessing to
allow for experimentation with other window sizes for the separate analysis. A
10-second window size was also tested and will be presented in the Results sec-
tion. Studies such as those by Walton et al. and Cabezas et al. have demonstrated
the effectiveness of using a 10-second window, inclining tests with this larger size
in our analysis despite the increased memory usage. Additionally, an intermedi-
ate window size of 5 seconds was explored, though it did not notably improve
outcomes compared to the 2.4-second window, so it was not continued with any
further.

Figure 3.6 illustrates the result from this step, dividing the original signal (in
this case, for the X-axis) in 4 different time windows, spanning adjacent intervals
of 2.4 seconds. Once divided into windows, the data is separated by axis, treat-
ing the X, Y, and Z axes independently. This approach allows for the extraction
of features from each axis individually, which is beneficial as different types of
animal behaviors may be more pronounced along one axis than the others. By

28

3 Methodology

Figure 3.6: Time windows extracted from the original, unprocessed signal
in the X-axis divided into 4 windows.

analyzing each axis separately, it is possible to capture unique movement charac-
teristics that might be diluted or overlooked in a combined analysis. Once data
has been received by the tag and separated by axis, the next step is to calculate
features directly from the raw acceleration values without transforming them.
Subsequently, the raw data is transformed using Hämäläinen et al.’s jerk-based
filter [10] to extract the dynamic components of the data. Several related stud-
ies have demonstrated success using different variations of this step [4] [1] [19],
but despite differences in specifics, it shows the importance of having some form
of filter or transformation to isolate the dynamic or alternating components of
the accelerometer data. Additional features will be calculated from this dynamic
represenation before further transforming it into the final form, the frequency
domain representation, using DFT computations. In the frequency domain, the
data will be represented as a spectrogram in 6 different frequency bands the span
of 0Hz to 5Hz. The final features will be calculated from these frequency bands.
Features extracted from these three signal representations are used to train a su-
pervised machine learning algorithm for behavioural pattern classification. From
this machine learning model, feature importance can be ranked, and node thresh-
olds can be extracted for use in a simplified decision tree directly on the activity
tag’s SoC. Details on the analysis and machine learning models are provided in
Section 3.5.

3.4.1 Feature calculation

Once the accelerometer data has been converted into the various forms described
in Section 3.2, it is time to further transform the data into a feature representa-
tion of the time windows. The machine learning models do not interact or learn
from the time windows themselves, but instead only the features that describe
the windows, such as the mean or the maximum accelerations of each window.
As previously mentioned, these are calculated from the raw time domain, the
dynamic component, and the frequency domain representations. Many different
features were tested and experimented with in the separate analysis in order to
determine the most impactful features to implement on the activity tag. In to-

3.5 Data analysis techniques

29

tal, X features were calculated and tested. X from the raw time domain, X from
the dynamic component, and X from the frequency domain. Features were calcu-
lated from each accelerometer axis separately, meaning each category of feature
is calculated several times. For example, the accelerometer mean is divided into
mean_x, mean_y, and mean_z. In the time domain and for the dynamic compo-
nent, each feature category becomes 3 features. In the frequency domain, each
feature is also calculated for each of the 6 frequency bands from 0 to 5Hz, as
well as for each axis. Here, each feature category becomes 18 features. The root
mean square (RMS) in the frequency domain becomes rms_x_0H z, rms_x_1H z,
and so on. In total, with all categories, axes, and bands, there are 114 features
used to describe the accelerometer data. Table 3.5 presents the features that are
extracted for each data representation as well as their abbreviated name used in
later graphs.

Table 3.5: Summary of features used in the model, categorized into raw time
domain, dynamic component, and frequency domain features with their ab-
breviations.

mean_axis
std_axis
max_axis
min_axis
Q5_axis
Q95_axis

Raw Time Domain Features Abbreviation
Mean
Standard Deviation
Max
Min
5th Percentile
95th Percentile
Dynamic Component Features
Mean
Standard Deviation
Max
Min
5th Percentile
95th Percentile
Kurtosis
Skewness
Frequency Domain Features
DFT Min Freqency
DFT Peak Frequency
DFT Mean Frequency
DFT Standard Deviation

ac_mean_axis
ac_std_axis
ac_max_axis
ac_min_axis
ac_Q5_axis
ac_Q95_axis
kurt_ac_axis
skew_ac_axis

min_ac_axis_band
max_ac_axis_band
rms_ac_axis_band
std_ac_axis_band

3.5 Data analysis techniques

When the data windows have been converted into features the analysis and ma-
chine learning models can be applied. Two similar, but different, models are used
in this thesis. An RF model is used for the separate analysis and a single decision

30

3 Methodology

tree is used as a classifier directly on the tag, with thresholds and structure de-
rived from the RF. The RF uses all 114 available features, while the simplified
decision tree only uses the 20 most impactful features. The RF decides and reg-
ulates its thresholds, structure, and feature importance rankings using the tech-
niques described in the Theory chapter.

For the separate, in-depth analysis of the accelerometer data, an RF model was
developed using the Python ’scikit-learn’ library. At this stage, the dataset is com-
prised of the feature representation of the time windows and the corresponding
correct label for the displayed animal behavior at that time. The labels are then
encoded, turning string-based categorical labels into a numerical format, neces-
sary for the mathematical computations involved in machine learning algorithms.
Following this, the dataset is divided into training and test sets, to be able to accu-
rately assess the model’s performance. As an additional step, sklearn’s Standard-
Scaler was used to standardize the features to bring them onto the same scale.
If this step is not done, features of larger numerical magnitude risk dominating
smaller ones during the learning process. The RF model was then trained with
200 estimators. No class weights were initially specified, allowing the model to
treat each class equally during the learning process. Experimentation was later
done with increasing the class weight of underrepresented classes in the dataset
such as the ’walking’ class. Finally, the model’s predictive accuracy was evalu-
ated against the test set, providing a quantitative measure of its performance.
The model learns patterns from the training set, and once sufficiently trained it
tries to classify previously unseen data from the test set. This serves as a fair in-
dicator of how well the model performs.

As an additional analysis tool, a classification report is then generated, offering
detailed insights into the model’s precision, recall, and F1 scores across the dif-
ferent behavioral categories. These metrics give deeper insight into the model’s
strengths and weaknesses than accuracy alone can provide. As a final step, the
model’s feature importance is calculated from the Gini impurity used to construct
the tree. The normalized average decrease in impurity for each feature is taken
as its importance score. Features that lead to larger decreases in impurity are con-
sidered more important because they provide better splits that more effectively
classify the dataset.

3.6 Implementation on activity tag

The implementation of the behavior classification system on the activity tag is
based on the main methodology described throughout this chapter. The first step
is sensor data acquisition, which is followed by data transformation and feature
extraction, and finally the classification using a decision tree model.

The core of the implementation is written in C, leveraging the nRF52840 SoC
from Nordic Semiconductor and the LIS2DS12 accelerometer from STMicroelec-

3.6 Implementation on activity tag

31

tronics. The SoC handles the collection and processing of accelerometer data in
real-time, using the the accelerometer’s built-in capabilities. The accelerometer
collects data at a frequency of 25Hz, storing acceleration measurements along
the X, Y, and Z axes. The raw sensor data’s individual components is separated
by axis, which is then processed to calculate the various statistical features de-
scribed in Section 3.4.1 for behavior classification.

The decision tree model, derived from the original RF model, utilizes a series
of decision nodes to classify behavior based on extracted features. These decision
nodes are implemented as a C structure, where each node contains a threshold,
a feature index, and the indices of the subsequent nodes to visit depending on
whether the feature value is above or below the threshold. This structure, though
similar to a linked list, optimizes the decision-making process by avoiding un-
necessary if-statements for each case, thus conserving computational resources.
The decision-making flow continues until a leaf node is reached, representing a
specific behavior. This classification process occurs in real-time with each new
accelerometer data window. The classification results are then transmitted via
BLE for further analysis or storage, depending on the application.

3.6.1 Memory Impact of Code Integration on Activity Tag

The nRF52840 SoC used in the activity tag has 1 MB of flash memory, which
stores the firmware, BLE communication protocols, and the behavior classifica-
tion model. Integrating a larger machine learning model poses a risk of excessive
memory usage, potentially hindering regular operation. For that reason, a very
computationally efficient methodology was chosen. However, it is still essential
to evaluate the memory footprint to ensure there is sufficient space for the code,
data storage, and future updates.

• Initial firmware size: 214.8 KB

• Firmware size after integration: 225.7 KB

• Increase in flash memory usage: 10.9 KB

• Percentage of total flash memory used: 22.0%

Additionally, the nRF52840 SoC is equipped with 256 KB of RAM, utilized for
dynamic data storage during runtime. Adding the behavior classification code af-
fects RAM usage, as it requires space for storing the accelerometer data, extracted
features, and the decision tree nodes.

• Initial RAM usage: 33.5 KB

• RAM usage after integration: 35.7 KB

• Increase in RAM usage: 4.2 KB

• Percentage of total RAM used: 13.9%

32

3 Methodology

While exact figures for the computational load require runtime profiling, prelim-
inary testing indicates that the decision tree model operates efficiently within the
SoC’s processing capabilities. The average processing time per sample is minimal,
ensuring that BLE communication and other real-time tasks are not negatively af-
fected.

3.6.2 Power consumption and battery life

The power consumption of the activity tag is directly influenced by the compu-
tational load and memory usage. Increased processing and memory access can
lead to higher power consumption, affecting the battery life which can lead to
farmers having to replace the battery more often. This can be a hassle, especially
for free-ranging and less cooperative animals. The current setup uses a SAFT LS
14250 lithium battery with a capacity of approximately 1200 mAh. The numbers
presented below are estimations taken from the nRF52840 data sheet [18]. The
power consumption breakdown is as follows:

• nRF52840 SoC:

– Sleep mode (with RTC running): 1.5 µA
– CPU running (processing features and classifier): 5 mA

– BLE transmission: 10 mA

• LIS2DS12 Accelerometer:

– Active mode (25 Hz sampling): 8 µA

• Average current consumption:

– CPU active time per data window (2.4 seconds): 0.2 seconds

– BLE transmission time per data window: 2 ms

– Sleep time per data window: 2.1 seconds

We can then estimate an average current battery consumption as

(5 mA × 0.2 s) + (10 mA × 0.002 s) + (1.5 µA × 2.1 s) + (8 µA × 2.4 s)
2.4 s

Cavg =

=

1042.35 µAs
2.4 s

≈ 434 µA

As mentioned, the battery capacity is 1200 mAh (or 1,200,000 µAh) and we esti-
mated the average current consumption to be 434 µA, so we get

Battery life (in hours) =

Battery life (in days) =

1, 200, 000 µAh
434 µA

≈ 2766 hours

2766
24

≈ 115.25 days

3.6 Implementation on activity tag

33

It is important to note that this is a lower bound for the battery life. The calcu-
lation assumes constant BLE transmission. Without BLE transmission, we can
follow a similar calculation and find that average current consumption drops to
426 µA, and the battery life is extended to approximately 117.4 days. However,
in practice, the tag will utilize clever use of power-saving modes, duty sampling,
and other techniques to reduce power consumption during periods of low activ-
ity which significantly increases battery life.

4

Results

This section will present the results of the analysis and work done with the aim
of answering the research questions. The results of the machine learning models
will be in focus from the perspective of various performance metrics. First, the
methodology discussed in the previous chapter will be put to the test on the
third-party goat data set. These results indicate if the methodology is sound
and can give insight into the performance of the models on the cattle data set.
Next, results from the separate analyses with the larger models trained on the
cattle data set are presented along with various experiments to try to improve the
performance and their outcomes. Feature importance is also ranked to transition
into the simplified, single-tree model with fewer features. Finally, the results
from the simplified model that is implemented on the activity tag are presented
along with relevant discussion.

4.1 Random Forest model on the third-party Goat

dataset

As a first step in validating the methodologies developed in this study, the models
were applied to the third-party dataset comprised of accelerometer data collected
from goats. This data set served as an initial test bed to evaluate the effectiveness
of the analysis techniques across different species. The same preprocessing struc-
ture and features were used for all experiments with this data set, but various
hyperparameters of the model were changed and evaluated to find an optimal
setup. Most of the changed hyperparameters gave a minimal difference in results
and will not be included in this report. However, the most impactful hyperpa-
rameter to change was the window size, which controls how many acceleration
values are included in each time window used to calculate the features. Each time

35

36

4 Results

window gets reduced to single values that represent the entire window, such as
the mean of the X-axis during the entire time window. Consequently, a larger
window size gives the model more information per window but also reduces the
number of windows available to train on, as the data set is divided into larger
chunks. In essence, altering the window size becomes a trade-off between the
quality and quantity of the time windows.

The performance metrics presented below are derived from using the two win-
dow sizes on otherwise the same RF model with 200 decision trees. The trees use
Gini impurity as the function to determine when to split nodes, the max depth
was not specified, meaning that the nodes are expanded until all leaf nodes are
pure. The data was preprocessed as described in Section 3.4 and the features
used were the same ones seen in Table 3.5. The results of the models’ predictions
on the unseen test data can be seen in Table 4.1. Looking at the performance met-

Table 4.1: Comparison of RF model performance with different window
sizes on accelerometer data from goats.

2.4-second Window Results

Behavior Class Window Size Precision Recall
0.96
Standing
0.94
Walking
0.75
Eating
0.30
Laying
0.85
Grazing

0.95
0.90
0.75
1.00
0.87

2.4s
2.4s
2.4s
2.4s
2.4s

F1-Score
0.96
0.92
0.75
0.47
0.86

Standing
Walking
Eating
Laying
Grazing

Overall Model Accuracy: 88.11%

10-second Window Results

10s
10s
10s
10s
10s

0.97
0.99
0.83
1.00
0.94

0.99
0.97
0.87
0.33
0.89

0.98
0.98
0.85
0.50
0.91

Overall Model Accuracy: 93.69%

rics precision, recall, and F1-score for each class we can gain an understanding of
the model’s strengths and potential areas for improvement. Overall, from Table
4.1 we can see that the model is mostly able to distinguish between several key
behaviors typically observed in both goats and cattle. Notably, the ’Laying’, class
performs relatively poorly compared to the other behavior classes. Both models
have a perfect 1.0 precision score for the ’Laying’ class but a very poor recall, re-
sulting in a substandard F1-score. In practice, this means that when the models
classified a sample as ’Laying’ it was always correct, but there were many sam-
ples that should have been classified as ’Laying’ that were incorrectly classified
as something else instead.

4.2 Random Forest model on Cattle dataset

37

4.2 Random Forest model on Cattle dataset

Building upon the initial validation conducted with the goat dataset, this section
delves into the core analysis using the cattle dataset collected at Vreta utbildnings-
centrum. This dataset was collected from dairy cows during indoor conditions.
The behavior classes will mostly be the same as in the goat dataset, with ’Grazing’
being switched out for ’Ruminating’. The ’Ruminating’ category will also be split
into two separate behaviors, ’Standing ruminating’ and ’Laying ruminating’, de-
pending on if the animal was standing up or lying down while ruminating. For a
fair comparison, the same window sizes and other hyperparameters will be used
for these models as for the goat models. The results from the RF models on the
cattle data set are presented in Table 4.2.

Table 4.2: Comparison of RF model performance with different window
sizes on accelerometer data from cows.

2.4-second Window Results

Behavior Class
Standing
Walking
Eating
Laying
Standing ruminating
Laying ruminating

Window Size Precision Recall
0.90
0.02
0.91
0.96
0.84
0.87

0.75
1.00
0.89
1.00
0.86
0.93

2.4s
2.4s
2.4s
2.4s
2.4s
2.4s

F1-Score
0.82
0.04
0.90
0.98
0.85
0.90

Overall Model Accuracy: 84.67%

10-second Window Results

Standing
Walking
Eating
Laying
Standing ruminating
Laying ruminating

10s
10s
10s
10s
10s
10s

0.73
1.00
0.81
1.00
0.90
0.92

0.88
0.05
0.94
0.88
0.80
0.92

0.80
0.10
0.87
0.93
0.85
0.92

Overall Model Accuracy: 82.41%

Evidently, the overall performance of the models on the cattle data set is worse
than the goat dataset. Despite its limited size, the cattle set produces respectable
results for all classes except ’Walking’, which seems to be a problematic class
for this data set. The model got a high score in the precision metric but a very
low recall, which indicates that the model is very hesitant to classify samples as
’Walking’ and misses almost all of them. The very few samples it did classify as
’Walking’ were correct, though.

Interestingly, unlike the goat data set, the 10-second window size model performs
worse than the 2.4-second window size when using the cattle data set. However,

38

4 Results

the difference in results from the two window sizes is comparatively small for the
cattle dataset. Most behavior classes obtain a similar, or slightly worse, score in
all metrics. The ’Lying’ class no longer performs poorly using this data set and
achieves an F1-score of above 90% for both window sizes, despite being under-
represented. The model is even able to separate ’Lying’ and ’Lying ruminating’
to a large degree.

From these results, the choice was made to continue using the 2.4-second win-
dow sizes for the simplified SoC model. While the goat model shows that the
10-second windows can perform better with sufficient data samples, the differ-
ence was deemed not great enough to restructure the code on the SoC to handle
the increased computational load of using 10-second windows.

4.3 Feature importance

Following the initial RF models, careful analysis of the features used by the mod-
els is required to effectively perform the next step of simplifying the model. The
feature importance was calculated and ranked from each of the models presented
above using the method presented in Section 2.4.3.

The feature rankings vary based on the specific behaviors included in the clas-
sification task, but in most cases, the classifier operates with all six behaviors
considered simultaneously. Therefore, the feature importance rankings provided
below reflect the scenario where all behaviors are included in the classification
analysis simultaneously. An overview of the feature ranking for the cow data set
can be seen in Figure 4.1. This graph of the complete feature set gives an idea
of the distribution of the model’s feature importance. Specific numbers and fea-
ture names can be disregarded. Feature importance for each individual behavior
can be found in Appendix A. A complementary table detailing the top 20 most
important features can be seen in Table 4.3.

Figure 4.1: Feature importance ranked in descending order for an RF model
trained on the cow data set.

4.3 Feature importance

39

Table 4.3: Feature importances from the top 20 most important features of
the RF Model trained on the cow data set with all behaviors.

Importance
0.0394
0.0331
0.0305
0.0301
0.0289
0.0266
0.0251
0.0236
0.0229
0.0229
0.0227
0.0193
0.0181
0.0179
0.0177
0.0167
0.0165
0.0160
0.0151
0.0141

Feature
kurt_acx
mean_acc_x
Q5_x
skew_acx
mean_acc_y
Q5_y
Q95_x
Q5_ac_x
kurt_ac_z
min_acc_x
min_acc_y
max_acc_y
Q95_ac_x
mean_ac_y
Q5_ac_z
Q95_y
Q95_ac_z
std_acc_y
skew_ac_z
max_acc_x
Total Raw acc:
Total Dynamic:
Total DFT:

Source
Dynamic
Raw acc
Raw acc
Dynamic
Raw acc
Raw acc
Raw acc
Dynamic
Dynamic
Raw acc
Raw acc
Raw acc
Dynamic
Dynamic
Dynamic
Raw acc
Dynamic
Raw acc
Dynamic
Raw acc
11
9
0

One key takeaway from Figure 4.1 is that not all features carry the same weight in
classification power. There are a number of highly relevant features, but the ma-
jority are not very useful. Almost all of the features derived from the frequency
domain are gathered in the long tail of the distribution, signifying that they do
not carry a lot of relevance for the overall classification process. In 4.3 not a sin-
gle frequency feature derived from the DFT process made it into the top 20 most
impactful features for the cow data set. Both raw accelerometer data and the iso-
lated dynamic component are of similar importance in the top 20 rankings. We
also see that motion in all three axes (X, Y, Z) is important, with the X-axis being
the most impactful.

Looking at the output from the RF model trained on the goat data set in Fig-
ure 4.2, we see a similar-looking feature distribution amplified even further. The
impactful features on the left side of the x-axis are even more impactful, and the
ones on the right side are even less impactful than for the cow data set. We also
see a similar result where the vast majority of the features derived from the fre-
quency domain by the DFT are typically not very relevant. However, there are a
few outliers. For example, in Table 4.4 we see that four frequency features from

40

4 Results

the DFT are actually highly relevant and can be found in the top 20 list. Instead,
the dynamic features are dominant for the goats. We also observe that the fea-
tures derived from the X-axis are most important for classifying cow behavior,
while the Y-axis features are most important for classifying goat behavior. The
features from the Z-axis give the least impactful information for both animals.

Figure 4.2: Feature importance ranked in descending order for a RF model
trained on the goat data set.

4.3 Feature importance

41

Table 4.4: Feature importances from the top 20 most important features of
the RF Model trained on the goat data set with all behaviors.

Importance
0.04793
0.04750
0.04104
0.04082
0.03714
0.03475
0.03250
0.03033
0.02928
0.02818
0.02628
0.02377
0.02312
0.02257
0.02253
0.02229
0.02091
0.02088
0.020099
0.01984

Feature
Q95_y
Q5_ac_y
Q5_ac_x
Q95_ac_y
mean_acc_y
rms_ac_ay_band2
Q5_x
mean_acc_x
Q95_ac_z
std_ac_z
Q95_ac_x
rms_ac_ay_band5
std_ac_x
min_acc_x
std_ac_y
rms_ac_ay_band3
kurt_acy
rms_ac_ay_band4
Q5_ac_z
skew_acy
Total Raw acc:
Total Dynamic:
Total DFT:

Source
Raw acc
Dynamic
Dynamic
Dynamic
Raw acc
DFT
Raw acc
Raw acc
Dynamic
Dynamic
Dynamic
DFT
Dynamic
Raw acc
Dynamic
DFT
Dynamic
DFT
Dynamic
Dynamic
4
10
6

These results indicate that overall, features derived from the frequency domain
using the Fourier Transform are typically not very impactful. Similar results
were found from various configurations of the DFT using different resolutions,
window sizes, window functions, and overlaps. These findings led to the exclu-
sion of Fourier Transform features from further analysis with consideration for
computational efficiency and the negligible impact of DFT features on model per-
formance. While some DFT features can clearly be of relevance, as seen in Table
4.4, it was deemed not worth the increased computational cost to transform the
entire data window into the frequency domain for a very marginal increase in
performance.

42

4 Results

4.4 Random forest model without frequency features

With the insight gained from inspecting the feature importance of both the goat
and cow models, new RF models were created and trained without using any
features derived from the frequency domain. Only the 2.4-second window size
models are presented here, as the 10-second window size did not give enough
of an improvement to warrant the extra memory and computation time given
the small data set. The results of the models are shown in Table 4.5. The 10-
second window size models without DFT features are presented in Appendix
B. The results of these models predictions show that frequency features derived

Table 4.5: RF model performance on both data sets without the use of fre-
quency features using a window size of 2.4 seconds.

Cow Data set

Behavior Class
Standing
Walking
Eating
Laying
Standing ruminating
Laying ruminating

Precision Recall
0.87
0.02
0.90
0.96
0.86
0.88

0.76
1.00
0.88
1.00
0.85
0.93

F1-Score
0.81
0.04
0.89
0.98
0.86
0.91

Overall Model Accuracy: 84.75%

Standing
Walking
Eating
Laying
Grazing

Goat Data set

0.95
0.92
0.73
1.00
0.88

0.96
0.93
0.76
0.42
0.85

0.96
0.92
0.74
0.59
0.86

Overall Model Accuracy: 88.05%

by the DFT are indeed not very impactful. The cow data set’s overall accuracy
remains essentially unchanged, going from 84.67% to 84.75%. The goat data
set also produced very similar results with or without DFT features, going from
88.11% to 88.05% overall accuracy.

4.5 Random forest with Synthetic Minority Oversampling

43

4.5 Random forest with Synthetic Minority

Oversampling

The main issue with all of the models presented so far is that one underrepre-
sented class sticks out as being a clear underperformer. For models using the
goat data set, it is the "Laying" class, and for the cow models, it is the "Walking"
class. These two behaviors are both severely underrepresented in their respective
data sets. SMOTE was implemented in an effort to increase predictive perfor-
mance for these two behavior classes, as discussed in Section 3.5.1. The results of
using SMOTE are shown in Table 4.6.

Table 4.6: RF model performance on both data sets with SMOTE for balanc-
ing the data set with a window size of 2.4 seconds.

Cow Data set

Behavior Class
Standing
Walking
Eating
Laying
Standing ruminating
Laying ruminating

Precision Recall
0.83
0.23
0.91
0.96
0.81
0.88

0.76
0.23
0.89
0.92
0.87
0.91

F1-Score
0.79
0.23
0.90
0.94
0.84
0.90

Overall Model Accuracy: 83.11%

Standing
Walking
Eating
Laying
Grazing

Goat Data set

0.96
0.91
0.73
0.75
0.90

0.95
0.95
0.80
0.47
0.83

0.95
0.93
0.77
0.58
0.87

Overall Model Accuracy: 88.60%

The use of SMOTE proved to be quite effective for improving the performance of
both ’Walking’ for cows and ’Laying’ for goats and producing a more balanced
result across the various behaviors. Both classes are still clearly the worst per-
forming classes in their respective models, but significant gains can be seen par-
ticularly in recall which also results in a better F1-score. However, comparing
the results with their 2.4-second window counterpart models that did not em-
ploy SMOTE, we can note a slight decrease in overall accuracy for the cow data
set. Without SMOTE, an accuracy of 84.67% was achieved, and with SMOTE an
accuracy of 83.11% was reached. The loss mostly comes from a slight reduction
in performance for the ’Standing’ and ’Laying’ classes. The goat model saw an
increase in overall accuracy, going from 88.11% to 88.60%, with the most signifi-
cant gains coming from the underperforming ’Laying’ class.

44

4 Results

4.6 Simplified decision tree model

As discussed in Section 3.5, the final model versions implemented on the activity
tags to do classification in real-time use a single decision tree with only 20 fea-
tures. Results from the single decision tree from both the cow and goat data sets
using a 2.4-second window can be found in Table 4.7. The goat and cow models
presented below are two separate models, each using their respective top 20 most
important features shown in Table 4.3 and 4.4. Using the same model for both
animals would not be possible with the current setup as they do not have the
behaviors in their data sets. Clearly, this simplified model performs worse than

Table 4.7: Results of the final simplified model implemented on the activity
tags.

Cow Data set

Behavior Class
Standing
Walking
Eating
Laying
Standing ruminating
Laying ruminating

Precision Recall
0.86
0.00
0.82
0.75
0.82
0.73

0.69
0.00
0.87
1.00
0.75
0.90

F1-Score
0.76
0.00
0.84
0.86
0.78
0.81

Overall Model Accuracy: 78.07%

Standing
Walking
Eating
Laying
Grazing

Goat Data set

0.92
0.84
0.61
0.17
0.87

0.94
0.87
0.71
0.05
0.73

0.93
0.86
0.66
0.08
0.79

Overall Model Accuracy: 81.91%

the RF model for both data sets, which is an expected result. There is a slight
reduction in predictive capabilities across all behavior classes. No class performs
very differently in the simplified version versus the full RF. The goat model still
struggles with the "Laying" class, while the cow model struggles with identifying
’Walking’.

Surprisingly, while the use of SMOTE did show its merits for the RF model, it
proved to be outright detrimental for this simplified decision tree model. The
overall accuracy for the cow data set was reduced from 78.07% down to 69.25%.
For the sake of brevity, the entire performance metric table will not be shown
here. The main takeaway from the SMOTE results on the simplified model is
that the ’Standing’ class, the most frequent behavior, was heavily reduced in both
precision and recall, causing poor results. The results for the goat data set went

4.6 Simplified decision tree model

45

from a 81.91% overall accuracy to a 78.69% accuracy. The recall of the problem-
atic class, ’Laying’, saw a large increase going from 0.05 to 0.71, but this came
at a cost of recall in other behaviors. The ’Standing’ class in particular saw re-
duced performance, going from 0.94 to 0.82 in recall, a significant loss given that
’Standing’ is the by far the most frequently appearing class in the goat data set.

5

Discussion

This chapter examines the experimental findings from the study, which explored
accelerometer data for monitoring animal behaviors. It evaluates how well the
results address the research questions and integrates these findings with the the-
oretical frameworks and methodologies used throughout the study. The discus-
sion also highlights the limitations of current methods, potential improvements,
and the broader impact of these technologies on livestock management and ani-
mal welfare.

Overall, the methodology developed through this thesis was comprehensive and
considered the challenges of real-time, on-device machine learning. It was a tes-
tament to the iterative nature of model development, where each phase of testing
and adjustment brought the system closer to an ideal balance of accuracy, effi-
ciency, and practical utility in a real-world agricultural setting. This approach
highlighted the potential of wearable technology in livestock management and
set a foundation for future enhancements and refinements.

5.1 Methodology discussion

The methodology adopted in this thesis was aimed at developing a robust and ef-
ficient way of classifying animal behaviors using the accelerometer data gathered
with wearable activity tags. As the classification needs to happen in real-time, on-
device, without transmitting the data, significant focus was placed on optimizing
the process to suit the limited computational resources available on the SoC.

47

48

5 Discussion

5.1.1 Data collection and data set imbalance

Two different data sets were used in this thesis to answer the research questions
posed in Section 1.2, a goat data set and a cow data set. While the goat data set
was found fully annotated and ready from an online source [12], gathering a new
data set for the cows from scratch came with its own set of challenges. As with
many machine learning tasks, the quality and quantity of the data is everything.
The easiest way of improving the models is to get more high-quality data. Col-
lecting and annotating data is very time-consuming, especially as this thesis work
was carried out by only one person. Creating the cow data set used in this thesis
took a lot of effort to do alone. Most of the data sets used by the related works
mentioned in this thesis have been collected by teams of researchers, which al-
lows them to gather a substantial amount more data. The animals from which
data is collected need to be observed and video-recorded at all times during the
collection process. At Vreta utbildningscentrum where the cow data set was col-
lected, this had to be done manually.

The collection process can be improved in many ways. First, there needs to be
a way of gathering data from several animals at once. This not only helps with
the collection speed but having more animals also introduces more diversity into
the data set. Outside of having more people to collect data, one way of achieving
this is to have some form of video surveillance setup in place. This way, footage
can also be recorded over a longer time period. It would be preferable to have a
much larger data set, possibly several days, which would be hard to do manually.

If more data is to be collected, a further improvement is to conduct the data
collection when the cows are outside. This provides a more natural behavior bal-
ance, particularly when it comes to eating and grazing. Having to move around
to graze on new patches of grass would likely also help with the problem that the
cows remained very static and which caused the ’Walking’ class to become very
underrepresented.

The annotation process could also be streamlined. The way it was done in this
thesis was very manual and slow. After recording, the video footage had to be
watched back, some parts many times, to get an accurate behavior label of what
the cow was doing at each timestamp. An Excel sheet was used to write down
what behavior the animal was displaying as well as the start and end times in the
video timestamps. These video timestamps were then converted to UNIX times-
tamps and the noted behavior was labeled to the data set for each data window
via a Python script. This process was not optimal and a lot of this could stand
to be improved. A preferable way of doing this task would likely involve having
some type of specialized video player that could easily annotate the behaviors
and what timestamps they occurred by using a graphical user interface. The out-
put could be saved in a CSV format to then be used with the Python script, which
would drastically cut down the manual work and effort involved. Creating a tool
like this was considered for this thesis, but for the amount of data available, it

5.1 Methodology discussion

49

would ultimately take more time than just annotating it manually.

One major problem with both data sets is that they are heavily imbalanced. This
is an unavoidable outcome as the animals will not display each behavior for an
equal amount of time and some behaviors are naturally rare. These cannot be dis-
carded though, as these behaviors that occur infrequently are often important for
the welfare and management of the animals. Unbalance in the data set means that
some classes will be underrepresented, which typically means that they will per-
form worse than their overrepresented counterparts. The easiest way of tackling
this issue is to simply gather more data from those underrepresented behaviors.
There are other ways to handle this problem, such as using SMOTE to syntheti-
cally generate new samples as was used in this thesis. However, as can be seen
in Table 4.6, this helped improve model performance for these behaviors. While
effective to a degree, the underrepresented ’Walking’ class for cows and ’Lying’
still perform quite poorly. Balancing the dataset in this way often also affected
the precision and recall of the more prevalent behaviors.

5.1.2 Preprocessing and model choices

The analytic part of the methodology was aimed at answering the first research
question of learning to what degree collar-based accelerometer data provides
enough information to accurately classify the behaviors of animals. The second
research question regarding what methods can be used to analyze the data also
had to be answered in order to answer the first question. Related works was
studied extensively in order to learn possible analytic approaches, with the extra
condition that the calculations had to be simple enough to fit on the activity tag
itself.

Ultimately, the use of Random Forests and decision trees formed the core of the
analytic approach. These methods were chosen for their effectiveness in handling
high-dimensional data and their capacity to model complex behaviors through
simple decision rules. These can easily be translated into a format the processor
on the SoC can handle, without external libraries or heavy calculations. While
a neural network could likely outperform the RF given sufficient computational
resources and a large enough data set, it would not be feasible to implement it
in a way that outperforms the RF given the existing setup. Other solutions could
also be worth looking into. One consideration is to implement the use of Markov
models with some form of transition matrix that contains probabilities for tran-
sitions between states. For example, it is unlikely that the cow goes from ’Lying’
to ’Walking’ directly without first standing up, but it is very likely to go from ly-
ing to lying and ruminating. These transitions are currently not considered and
could be used to improve the models markedly.

Another main point of the methodology was the preprocessing and feature se-
lection. Good preprocessing and features are extremely central for getting the
best results out of the RF model. As mentioned, there is a lot of related work in

50

5 Discussion

this area, some of which is outlined in Section 2.1. Most of these works use dif-
ferent techniques, features, and data set processing methods at the core of their
classification. As such, it was difficult to figure out the best strategy to tackle this
problem. However, these related works do not have to worry about adhering to
the computational constraints of a small SoC as they all do their classification
on an external computer. The central idea for the preprocessing and feature se-
lection of this thesis was to start broad, rank the best methods and features, and
then narrow down and simplify the model enough to the point that the activity
tag’s SoC can handle it smoothly. The process of determining the most impactful
features involved analyzing feature importance derived from the initial RF mod-
els. The 20 most impactful features across all behaviors were then selected to
be used in the simplified model. Following this analysis, an entire group of fea-
tures could be eliminated from further analysis. The frequency-based features
derived from the Discrete Fourier Transform of the accelerometer signals proved
to be relatively underperforming across all behaviors with none of them making
it into the overall top 20 most impactful features for cows. It was concluded to
not be worth the computational cost of transforming the entire signal into the
frequency domain just to derive a few underwhelming features that barely im-
proved the result for either data set. This result was mostly in line with findings
in other related works. The use of features from the frequency domain can also be
seen in [4] Cabezas et al., where they found a similar result of frequency features
not being very dominant. The only behavior where they were very impactful was
for their ’Steady standing’ class. This result diverges from the findings seen in
Appendix A, where frequency features were not very impactful for ’Standing’.
Instead, ’Walking’ was the cow behavior that most relied on frequency features
in this thesis. However, the classification results for ’Walking’ in cows turned
out very poor, so these findings are not very reliable. Frequency features in the
goat data set proved to be a bit more impactful, with 4 of them making it into
the top 20 overall most important features list. However, these features seem
relatively replaceable by other features, as the model’s overall accuracy only de-
creased from 88.11% to 88.05% after eliminating all 72 frequency-based features.

The simplification of the model to fit the SoC’s capabilities involved compromises,
particularly in the granularity and number of features used. This was a delicate
balance to find, as too much simplification could strip the model of its ability to
accurately predict complex behaviors. The decision to use a single decision tree
and limit the feature set was driven by these considerations, aiming to create a
model that was both efficient and effective under the constraints imposed by the
hardware. However, the size and memory impact of the simplified model were
overestimated and only took up a small fraction of the available capacity. Given
more time, either a deeper tree, more features, or some sort of ensemble solution
with a small number of trees working together would likely have been feasible to
implement and performed better.

5.1 Methodology discussion

51

5.1.3 Step count as a feature

One intended step in the methodology that proved unsuccessful was to include
the use of the LIS2DS12 accelerometer’s built-in step counter as a feature. The
idea was to examine differences in step count between two consecutive data win-
dows as an easy feature to determine if the animal was walking. The step counter
is not foolproof and sometimes misregisters steps, but it could still likely be a
very impactful feature. In practice, however, the use of the step counter turned
out to not work very well. Upon closer inspection of the data, it turns out that the
step counter was updated very inconsistently. Most of the time, the step count
was updated in chunks of 5-10 steps at once between windows. This could be
worked around, but the main issue was when the steps were reported. Typically,
if there were 4 consecutive walking-windows, the step count would only be up-
dated a couple of windows after the walking was done. This offset was not con-
sistent either, and would often come anywhere between 1 and 5 windows later.

An attempt was made near the end of the project to build an alternative step-
counting function by using a bandpass filter on the norm of the acceleration and
filter for a chosen step frequency interval somewhere in the range of 0.25 to 4
steps per second. A step would then be counted every time a chosen threshold
is exceeded. While this showed some promise, it could not be implemented well
enough in the small remaining time-frame.

5.1.4 Multiple animal classification

Another idea with the activity tag by the mission provider Qulinda AB was that
these tags were to be used on a variety of animals. This concept was also tested
in this thesis by using data sets from both goats and cows. However, the results
found that the models prioritized quite different features for these two animals.
What features are important for classifying animal behavior from accelerometer
data seems to vary greatly between animal species. As observed in Section 4.2.1,
not many of the same features appear in both top 20 lists. There are some gen-
erally important features like the mean of the X-axis and percentiles of various
axes (represented as Q95_axis and Q5_axis in Table 4.3 and Table 4.4), but the
models otherwise value quite different features. This suggests that a one-model
approach for all animals may not be the best strategy and yield suboptimal clas-
sification performance. Instead, the better solution is to use a model trained for
that specific animal. If both animals’ behavior needs to be classifiable on the same
tag, the model needs to be more complex and handle a larger number of features
for accurate classification. Depending on how good the classification needs to
be, this may at some point hinder the other functionality of the tag and reduce
battery life enough that a hardware upgrade may be necessary.

52

5 Discussion

5.2 Results discussion

In this section, we discuss the results obtained from the experimental application
of accelerometer-based models for animal behavior classification. The discussion
focuses on answering the third research question of how well the implemented
models classify the animal’s behavior. Several critical aspects of the results are
analyzed, such as the performance of the models on underrepresented classes to
the practical implications of deploying such technologies in real-world scenarios.

5.2.1 Comparison of Model Performances

The effectiveness of various models’ ability to analyze accelerometer data and
classify animal behavior has been a significant focus of this study, with results
presented in Chapter 4 showing a range of performances. The comparison of
these models provides valuable insights into their relative strengths and limita-
tions, guiding further development in the area.

The performance of the various RF models on both the cow and the goat data
sets demonstrates strong classification capabilities across most behaviors, with
particular success noted in more frequent behaviors such as ’Eating’ and ’Stand-
ing’. However, its effectiveness diminishes significantly when dealing with under-
represented classes like ’Walking’ in cows and ’Laying’ in goats, which highlights
a common challenge in machine learning, the difficulty of handling class imbal-
ance. Across all models, we also note that the models perform better on the goat
data set than the cow data set, but this is an expected result, given that the goat
data set is several times larger than the cow data set. To answer the first research
question, an RF given only the signals from a collar-based accelerometer was able
to score an overall accuracy upwards of 93.69% for the goats and 84.67% for the
cows across all behaviors. Clearly, this shows the potential of the methodologies
and that accelerometer data alone is sufficient to classify the basic activities con-
sidered in this thesis, see Table 3.3 and 3.4.

Once the RF model was simplified into its single decision tree form, the classi-
fication accuracy also saw a significant decrease. This was, of course, also an
expected outcome. However, the performance of the simplified model was better
than first hypothesized. Going from 200 decision trees in an RF down to a single
decision tree while also only using a fraction of the features at first seemed like it
would completely decimate the classification accuracy. In practice, it turned out
to not be as drastic of a decrease. The cow model saw a reduction from 84.75%
overall accuracy with its best model down to 78.07%, while the goat model went
from 93.69% to 81.91%.

To answer the third research question of how well the implemented models re-
liably interpret animal behavior we only have to look at Table 4.7. For most
behaviors, the accuracy is quite satisfactory. Having around 80% accuracy on the
simplified model is a decent result given the initial constraints, but it could defi-
nitely be improved on. Especially the two minority classes ’Walking’ for cows and

5.2 Results discussion

53

’Lying’ for goats. Unsurprisingly, if these two behaviors are not included in the
classification, the overall performance gets drastically improved, as seen in Ap-
pendix B. However, further effort should be put into improving the performance
of these two classes instead of discarding them. These behaviors are very core
to any animal monitoring application and should be included in any real-world
situation using accelerometer activity tags. The result can be compared with sim-
ilar studies using accelerometer data to classify animal behavior. For instance,
unconstrained by having to perform the classification on the tag itself, the RF
model by [4] Cabezas et al in 2022 saw a 91% overall accuracy on cow data, and
[8] González et al. achieved a 90.5% accuracy in 2015 on cow data using decision
trees.

5.2.2 Comparison of window sizes

Clearly, the results demonstrate that the 10-second window leads to a notable
improvement in the classification of most behavior classes compared to the 2.4-
second windows for the goat data set. Significant gains are observed in the walk-
ing, eating, and grazing behaviors, whereas the classification results for ’Laying’
remain similar and relatively poor. These results are consistent with the find-
ings of [19] Riaboff et al., where window sizes of 10 seconds and more are better
able to capture high motion variability found in activities with a complex de-
scription, such as walking and grazing. However, the main problem with larger
window sizes is that the number of time windows gets reduced. However, a ma-
jor drawback of using larger window sizes is the consequent reduction in the
number of available time windows. This issue is further amplified by the likeli-
hood of encountering windows that span multiple behaviors, which are typically
excluded from the dataset. The longer the window, the greater the number of
multi-behavior spans, leading to even fewer time windows available for training
and validation.

5.2.3 Performance on Underrepresented Classes

The imbalance of the data sets posed a huge challenge throughout the thesis
work. As evidenced by the various tables in Chapter 4, the models struggled
heavily with classifying these behaviors accurately, primarily due to their sparse
representation in the training data. The underrepresentation of certain behav-
iors, such as "lying" in goats and "walking" in cows, likely arises from the natural
behavior patterns and environmental conditions in which the data was collected.
Goats are typically more active and curious animals compared to cows. They
tend to spend more time standing and exploring, which could be a reason why ly-
ing down is rare in goats. Cows typically have less dynamic and varied behavior
patterns compared to goats. In many farming environments, especially during
winter or in indoor settings, cows spend much of their time standing, lying down,
or feeding rather than walking. This could be due to the lack of stimulus or space
to promote walking. An easy improvement over the current data collection is to
collect data from cows outdoors.

54

5 Discussion

One curious result seen with the cow models is that while ’Walking’ performed
poorly, ’Lying’ performed very well for the cows, despite also being an underrep-
resented class. The model was even able to separate regular lying and ruminat-
ing while lying down surprisingly well. Lying down might have more distinctive
movement signatures that are easier to detect via accelerometers, making it easier
for the model to learn and recognize this behavior despite fewer instances. Walk-
ing may be much harder to detect for the accelerometer, as it is a much more
complex behavior that can look very different from step to step.

Sensor positioning is another key factor when it comes to recognizing underrep-
resented behaviors. If the sensor had been fastened around a leg of the cow, it
likely would have been significantly easier to detect steps. This would come at
a cost though, as it would be very difficult, if not impossible, to separate other
behaviors such as ruminating.

5.2.4 Effectiveness of Data Augmentation Techniques

The application of data augmentation techniques, specifically the Synthetic Mi-
nority Oversampling Technique (SMOTE), played a key role in addressing the
class imbalance in our dataset. The goal of using SMOTE was to enhance the
model’s ability to generalize across less frequent behaviors by synthetically gen-
erating new samples from the existing data of underrepresented classes. For the
cow dataset, SMOTE was applied to the ’Walking’ behavior, which was notably
underrepresented. The results showed that SMOTE effectively increased the re-
call of the ’Walking’ class from 0.02 to 0.23, indicating that the model became bet-
ter at identifying walking instances. However, this improvement came at a slight
cost to the overall model accuracy, which decreased marginally from 84.67% to
83.11%.

Similarly, for the goat dataset, SMOTE was applied to the ’Lying’ behavior. The
recall for ’Lying’ improved significantly from 0.05 to 0.47, demonstrating that
SMOTE enabled the model to better recognize this underrepresented behavior.
However, the overall accuracy of the goat model remained relatively unchanged,
going from 88.11% to 88.60%. While this indicates a slight improvement, the
change in accuracy is minimal. This small increase may not be statistically sig-
nificant and could be due to random variation rather than the effect of SMOTE.
These findings suggest that while SMOTE can substantially enhance the detec-
tion of minority classes, its impact on overall model performance can vary de-
pending on the dataset. In practice, applying SMOTE requires consideration of
the specific behaviors and the context in which the model will be used. The im-
proved recall for underrepresented behaviors can be important for real-world
applications where accurately identifying such behaviors is more important than
marginal gains in overall accuracy.

5.3 Implications for Real-World Applications

55

5.3 Implications for Real-World Applications

The practical implications of these findings for real-world applications are many,
particularly in the context of livestock management and animal welfare. The
ability to classify behaviors and monitor animals without direct observation has
several potential benefits. First, farmers can be provided with valuable insights
into the health and well-being of their livestock. For instance, a cow that walks
significantly less than others may be experiencing health issues that require atten-
tion. Early detection of such anomalies through automated monitoring systems
can lead to timely interventions, potentially reducing veterinary costs and im-
proving animal welfare. Automated behavior monitoring can reduce the need for
constant human supervision, allowing farmers to spend their time and resources
more efficiently. The use of accelerometer activity tags can be particularly useful
in large farms where manual monitoring of each animal is impractical. However,
it is important to consider the possible downsides of this technology as well. If
farmers become too reliant on this type of device, it risks reducing the frequency
and quality of interaction between humans and animals, which can be a net neg-
ative in terms of welfare. Even if the occurrence of negative welfare states is re-
duced and responded to quickly, it is also important to promote positive welfare
states and to maintain personal relationships with the animals.

6

Conclusion

The integration of collar-based accelerometer activity tags with machine learn-
ing models in livestock management holds significant promise. This thesis has
demonstrated the feasibility of using accelerometer data to accurately classify a
variety of animal behaviors, providing valuable insights into the health and ac-
tivity patterns of livestock. The use of advanced data preprocessing techniques
and machine learning algorithms, such as RFs and decision trees, has proven
effective in extracting meaningful features from accelerometer signals, despite
data set imbalances. The results show that the best-performing unconstrained
RF model is able to classify basic animal behaviors with a 93.69% accuracy for
goats and 84.67% for cows. When the model is simplified into its decision tree
form for implementation on the activity tag, the accuracy gets lowered to 81.91%
for goats and 78.07% for cows. The general methodology shows promise and with
more data and additional refinements to the model, the activity tags can become
a helpful tool for farming in the future.

Automated behavior monitoring can reduce the need for constant human super-
vision, allowing for more efficient farm management. Early detection of health
issues through accurate behavior classification can lead to timely interventions,
improving animal welfare and reducing veterinary costs.

While challenges remain, especially in handling class imbalances and optimizing
model performance, the potential benefits for animal health and farm efficiency
are substantial. These technologies represent a step forward in modernizing farm-
ing practices and ensuring the well-being of livestock.

57

Appendix

A

Feature importance per class

Figure A.1: Feature importance for detection of eating behavior in cows.

61

62

A Feature importance per class

Figure A.2: Feature importance for detection of laying behavior in cows.

Figure A.3: Feature importance for detection of laying ruminating behavior
in cows.

63

Figure A.4: Feature importance for detection of standing behavior in cows.

Figure A.5: Feature importance for detection of standing ruminating behav-
ior in cows.

64

A Feature importance per class

Figure A.6: Feature importance for detection of walking behavior in cows.

B

Performance without DFT features
using a 10-second window size.

Table B.1: Random forest model performance on both data sets without the
use of frequency features using a window size of 10 seconds.

Cow Data set

Behavior Class
Eating
Laying
Laying ruminating
Standing
Standing ruminating
Walking
Overall Model Accuracy: 80.69%

Precision Recall
0.91
0.88
0.94
0.78
0.79
0.15

0.89
1.00
0.94
0.76
0.88
0.11

Goat Data set

Behavior Class
Eating
Grazing
Standing
Walking
Overall Model Accuracy: 93.31%

Precision Recall
0.88
0.90
0.98
0.93

0.80
0.95
0.98
0.97

F1-Score
0.90
0.93
0.94
0.77
0.83
0.12

F1-Score
0.84
0.92
0.98
0.95

65

C

Feature thresholds of the decision
tree

In the table below, the thresholds for each node of the decision tree is presented.
The order is the same order (depth first) that the implemented tree uses. Worth
noting is that the acceleration uses an encoding where the ±2g values are con-
verted into values in the range of -512 to 511, which is the range of a 10-bit
signed integer.

Threshold
40.7224
73.3000
-182.9750
-117.1333
37.5000
5.6708
47.7250
-61.1333
-147.4250
-9.5000
-67.1750
123.2578
-2.0583
11.2000
10.5476
123.0000
-188.8417
11.4899
40.0512
43.8482

Feature
KURT_DYN_Z
Q5_Y
Q5_X
MEAN_Y
MAX_Y
STD_Y
Q5_Y
MEAN_X
Q95_X
MIN_Y
Q5_Y
STD_X
MEAN_DYN_Y
Q95_DYN_X
STD_X
MAX_Y
MEAN_X
STD_Y
KURT_DYN_X
STD_Y

67

68

C Feature thresholds of the decision tree

5.2479
1.9917
-6.0815
-1.7828
217.7750
-0.1498
-7.1526
-174.0250
-8.1000
6.9816
6.5500
43.3602
-215.0750
-7.3601
38.5000
-14.5000
-132.9833
8.9750
73.5000
-147.9250
-137.9750
-143.0250
-4.5000
5.4711
-17.5500
-15.0250
63.5000
10.8779
-155.5000
55.2307
-131.4083
59.4417
-7.0250
8.5000
4.5335
62.5000

SKEW_DYN_Z
MEAN_DYN_Y
SKEW_DYN_X
SKEW_DYN_X
Q95_Y
SKEW_DYN_X
SKEW_DYN_X
Q5_X
Q5_DYN_X
SKEW_DYN_Z
Q95_DYN_X
KURT_DYN_Z
Q5_X
SKEW_DYN_X
MIN_Y
MAX_Y
MEAN_X
Q5_Y
MIN_Y
Q95_X
Q95_X
Q5_X
MIN_Y
STD_Y
Q5_Y
Q5_DYN_Z
MIN_Y
STD_Y
Q5_X
KURT_DYN_Z
MEAN_X
MEAN_Y
Q5_DYN_X
MAX_Y
STD_Y
MIN_Y

Bibliography

[1] J Barwick. On-animal motion sensing using accelerometers for sheep be-
haviour and health monitoring. Armidale (Australia): [Doctoral disserta-
tion, University of New England], 2017.

[2] Erin J. Bredensteiner and Kristin P. Bennett. Feature minimization within
decision trees. Computational Optimization and Applications, 10:111–126,
1998.

[3] Leo Breiman. Random forests. Machine learning, 45:5–32, 2001.

[4] Javier Cabezas, Roberto Yubero, Beatriz Visitación, Jorge Navarro-García,
María Jesús Algar, Emilio L Cano, and Felipe Ortega. Analysis of accelerom-
eter and gps data for cattle behaviour identification and anomalous events
detection. Entropy, 24(3):336, 2022.

[5] Nitesh V Chawla, Kevin W Bowyer, Lawrence O Hall, and W Philip
Kegelmeyer. Smote: synthetic minority over-sampling technique. Journal
of artificial intelligence research, 16:321–357, 2002.

[6] James W Cooley and John W Tukey. An algorithm for the machine calcu-
lation of complex fourier series. Mathematics of Computation, 19(90):297–
301, 1965.

[7] Eloise S Fogarty, David L Swain, Greg M Cronin, Luis E Moraes, and Mark
Trotter. Behaviour classification of extensively grazed sheep using machine
learning. Computers and Electronics in Agriculture, 169:105175, 2020.

[8] Luciano A González, GJ Bishop-Hurley, Rebecca N Handcock, and Christo-
pher Crossman. Behavioral classification of data from collars containing
motion sensors in grazing cattle. Computers and electronics in agriculture,
110:91–102, 2015.

[9] Fredrik Gustafsson, Lennart Ljung, and Mille Millnert. Signal Processing.

Studentlitteratur, 2010.

[10] W Hämäläinen, P Martiskainen, M Järvinen, J-P Skön, J Tiirikainen,
M Kolehmainen, and J Mononen. Computational challenges in deriving

69

70

Bibliography

dairy cows’ action patterns from accelerometer data. In Proceedings of the
22nd Nordic symposium of the International Society for Applied Ethology,
page 18. Finnish Society for Applied Ethology, 2010.

[11] Trevor Hastie, Robert Tibshirani, and Jerome Friedman. The Elements of
Statistical Learning: Data Mining, Inference, and Prediction. Springer Se-
ries in Statistics. Springer New York, New York, NY, 2009. ISBN 978-0-387-
84857-0.

[12] Jacob W. Kamminga, Duv V. Le, Jan Pieter Meijers, Helena C. Bisby, Nirvana
Meratnia, and Paul J.M. Havinga. Robust sensor-orientation-independent
feature selection for animal activity recognition on collar tags. Proc. ACM
Interact. Mob. Wearable Ubiquitous Technol., 2(1), March 2018. doi: 10.
1145/3191747.

[13] Vianey Leos-Barajas, Theoni Photopoulou, Roland Langrock, Toby A Patter-
son, Yuuki Y Watanabe, Megan Murgatroyd, and Yannis P Papastamatiou.
Analysis of animal accelerometer data using hidden markov models. Meth-
ods in Ecology and Evolution, 8(2):161–173, 2017.

[14] L Lush, S Ellwood, A Markham, AI Ward, and P Wheeler. Use of tri-axial
accelerometers to assess terrestrial mammal behaviour in the wild. Journal
of Zoology, 298(4):257–265, 2016.

[15] Paula Martiskainen, Mikko Järvinen, Jukka-Pekka Skön, Jarkko Tiirikainen,
Mikko Kolehmainen, and Jaakko Mononen. Cow behaviour pattern recogni-
tion using a three-dimensional accelerometer and support vector machines.
Applied animal behaviour science, 119(1-2):32–38, 2009.

[16] Gabriele Mattachini, Elisabetta Riva, Francesca Perazzolo, Ezio Naldi, and
Giorgio Provolo. Monitoring feeding behaviour of dairy cows using ac-
celerometers. Journal of Agricultural Engineering, 47(1):54–58, 2016.

[17] Arundhati Navada, Aamir Nizam Ansari, Siddharth Patil, and Balwant A
Sonkamble. Overview of use of decision tree algorithms in machine learning.
In 2011 IEEE control and system graduate research colloquium, pages 37–
42. IEEE, 2011.

[18] Nordic Semiconductor.

nRF52840 Product Specification, 2022. URL:

<https://www.nordicsemi.com/Products/nRF52840>.

[19] Lucile Riaboff, Laurence Shalloo, Alan F Smeaton, Sébastien Couvreur, Au-
rélien Madouasse, and Mark T Keane. Predicting livestock behaviour using
accelerometers: A systematic review of processing techniques for ruminant
behaviour prediction from raw accelerometer data. Computers and Elec-
tronics in Agriculture, 192:106610, 2022.

[20] Juliette Schillings, Richard Bennett, and David Christian Rose. Exploring
the potential of precision livestock farming technologies to help address
farm animal welfare. Frontiers in Animal Science, 2, 2021.

Bibliography

71

[21] Md Sumon Shahriar, Daniel Smith, Ashfaqur Rahman, Mark Freeman,
James Hills, Richard Rawnsley, Dave Henry, and Greg Bishop-Hurley. De-
tecting heat events in dairy cows using accelerometers and unsupervised
learning. Computers and electronics in agriculture, 128:20–26, 2016.

[22] Laurence Shalloo, T Byrne, L Leso, Elodie Ruelle, K Starsmore, A Geoghegan,
J Werner, and N O’Leary. A review of precision technologies in pasture-
based dairying systems. Irish Journal of Agricultural and Food Research, 59
(2):279–291, 2021.

[23] STMicroelectronics. LIS2DS12 Ultra-low-power high-performance three-
axis linear accelerometer, 2022. URL: <https://www.st.com/en/mems-and->
sensors/lis2ds12.html.

[24] David A Van Dyk and Xiao-Li Meng. The art of data augmentation. Journal

of Computational and Graphical Statistics, 10(1):1–50, 2001.
