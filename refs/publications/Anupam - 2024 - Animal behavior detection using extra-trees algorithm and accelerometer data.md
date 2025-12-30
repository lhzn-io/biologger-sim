See discussions, stats, and author profiles for this publication at: <https://www.researchgate.net/publication/384294764>

Animal behavior detection using extra-trees algorithm and accelerometer
data

Preprint · September 2024

DOI: 10.13140/RG.2.2.18872.97284

CITATIONS
0

1 author:

Sagnik Anupam

University of Pennsylvania

10 PUBLICATIONS   118 CITATIONS

SEE PROFILE

READS
165

All content following this page was uploaded by Sagnik Anupam on 25 September 2024.

The user has requested enhancement of the downloaded file.

Animal behavior detection using extra-trees
algorithm and accelerometer data

Sagnik Anupam1*

1*Department of Electrical Engineering and Computer Science,
Massachusetts Institute of Technology, Cambridge, 02139, MA,
USA.

Corresponding author(s). E-mail(s): <sagnik@mit.edu>;

Abstract

Accelerometer data collected through bio-logging devices is a powerful
method for tracking animals in situations where direct observation may
not be feasible or may affect experiment outcomes. However, it is often
challenging to process and interpret large amounts of accelerometer data
and correlate it with animal behavior. Thus, machine learning algorithms
are used for animal behavior classification. This paper demonstrates
the application of a novel hybrid approach combining the Extra-Trees
(ET) classifier with the Tree-structured Parzen Estimators (TPE) algo-
rithm to the animal behavior classification domain. The model was
evaluated using publicly available data on two animal species: Holstein
dairy cows (Bos taurus) and the North American red squirrels (Tami-
asciurus hudsonicus). Its performance was compared to that of the
K-Nearest Neighbors (KNN) and Support Vector Machine (SVM) clas-
sifiers, which are standard machine-learning models that have achieved
high levels of accuracy in this domain. The TPE-optimized ET classifier
achieved mean accuracies of 96.99% on the North American red squir-
rel dataset, and 87.51% and 90.89% on the Holstein dairy cow dataset
on 1-minute and 5-minute intervals of data. The classifier consistently
outperformed the KNN (90.10%, 87.17%, and 88.08% respective mean
accuracies) and SVM (93.81%, 86.83%, 90.08% respective mean accu-
racies) classifiers on both mean accuracy as well as mean weighted F1
score metrics by a statistically significant amount. Thus, the results show
that the hybrid model performs better than the current state-of-the-art
models in the animal behavior classification domain. Thus, optimized
ET classification models are a useful tool for accurately monitoring the
behavioral states of subjects belonging to a wide variety of animal species.

1

2

Animal behavior detection using extra-trees algorithm and accelerometer data

Keywords: Animal Behavior, Accelerometer, Machine Learning, Extra Trees

1 Introduction

Although numerous methods have been developed for detecting, measuring,
and classifying animal behavior over the years, they may not be feasible in cer-
tain situations due to visibility constraints or due to the fear that the observer
may influence the subjects’ behavior (Martin & Bateson, 2007). To overcome
this problem, the usage of accelerometer data from bio-logging devices has
emerged as a powerful alternative method of tracking animal behavior in
recent years, especially in cases where it is difficult to directly observe animals
in the wild (Brown, Kays, Wikelski, Wilson, & Klimley, 2013). Additionally,
accelerometer data analysis has several diagnostic use cases, such as identifying
lameness in sheep (Barwick et al., 2018).

However, it is challenging to process, interpret and analyze accelerometer
signals manually, especially in species that display a wide range of behaviors.
Recently, researchers have utilized advances in machine learning to adopt a
range of diverse techniques for interpreting accelerometer data. Some of the
most prominent algorithms being used for accelerometer data analysis are
K-Nearest Neighbors (KNN) (Bidder et al., 2014), Support Vector Machines
(SVM) (Tatler, Cassey, & Prowse, 2018), and Random Forests (RF) (Wang,
2019).

Improvements in decision-tree-based machine-learning models (such as RF
models) have led to the development of Extra-Trees (ET) models, which have
been shown to display remarkable improvements in performance over RF mod-
els in supervised classification problems (Geurts, Ernst, & Wehenkel, 2006). ET
models have also been shown to outperform SVM and KNN models on certain
supervised classification problems (Abbas et al., 2021). ET models have been
used for identifying malware (Zhou, Pang, & Liang, 2017), classifying brain
tumors (Pinto, Pereira, Rasteiro, & Silva, 2018), recognizing human activity
from sensor data (Uddin & Uddiny, 2015), and other computer vision problems
in the medical subdomain (Mar´ee, Wehenkel, & Geurts, 2013). However, their
potential usage for animal behavior classification has so far not been explored,
especially their relative performance against non-decision tree methods such
as SVM and KNN models.

This paper seeks to evaluate the performance of ET models optimized
using Tree-structured Parzen Estimators (TPE) optimization algorithm for the
purposes of animal behavior classification using accelerometer data. Their per-
formance is then compared to state-of-the-art methods on the same datasets.
ET models were chosen for evaluation because of their success in human activ-
ity recognition (as well as other supervised classification problems) and since
they have been shown to outperform SVM and KNN models on certain clas-
sification problems (Abbas et al., 2021). The TPE algorithm was chosen for

Animal behavior detection using extra-trees algorithm and accelerometer data

3

its previous success in optimizing hyperparameters in deep belief networks
Bergstra, Bardenet, Bengio, and K´egl (2011). The models are evaluated on
two publicly accessible datasets containing accelerometer data – one for Hol-
stein dairy cows (Bos taurus) (dataset from (V´azquez Diosdado et al., 2015))
and one for North American red squirrels (Tamiasciurus hudsonicus) (dataset
from (Studd et al., 2019)).

This paper presents a novel hybrid approach that optimizes ET model
parameters using the TPE algorithm, as the optimization of ET hyperpa-
rameters using Bayesian approaches has not been explored in the literature.
Furthermore, this paper advances the state-of-the-art in the animal behav-
ior classification domain by demonstrating this hybrid approach’s improved
classification accuracies over the SVM and KNN models.

This paper is divided into different sections as follows: Section 2 discusses
various machine-learning approaches to accelerometer data analysis in both
animal behavior classification as well as other domains. It then discusses exist-
ing work on hyperparameter optimization, both in the context of ET models as
well as other machine-learning models. Section 3 explains the computational
methodology used in developing the ET-TPE hybrid classifier as well as the
KNN and SVM benchmark methods. Section 4 describes the metrics used for
evaluating the performance of all the classifiers and discusses the results thus
obtained, while 5 describes the conclusions of the study, practical applications,
and directions for future research.

2 Related Work

2.1 Accelerometer Data Analysis

The usage of accelerometer data for animal behavior classification has its roots
in the studies conducted in the 1950s which examined changes in human phys-
ical activity, such as gait velocity and acceleration (C.-C. Yang & Hsu, 2010).
Over time, such studies have expanded to identify human behavioral modes in
the domain of human activity recognition, especially from smartphone sensor
data. Prior research has shown that KNN (Paul & George, 2015), RF (Thakur
& Biswas, 2022), and SVM (Ahmed, Rafiq, & Islam, 2020) models achieve high
accuracies in the human activity recognition domain as well. Both the SVM
and RF approaches used the same publicly-available UCI dataset for model
evaluation, although different feature selection mechanisms were employed–
Sequential Floating Forward Search (SFFS) for the SVM model (Ahmed et
al., 2020) and Guided Regularized Random Forest Feature Selection (GRRF)
(Thakur & Biswas, 2022) for the RF model. The KNN model used a sepa-
rate dataset collected by the authors via a mobile application where subjects
could modify sample rate of data collection prior to training the model and
evaluating its performance (Paul & George, 2015).

The usage of accelerometer data for animal behavior classification is a
relatively recent development, with a study of Adelie penguin (Pygoscelis
adeliae) behavior in 1999 (Yoda et al., 1999) considered to be one of the first

4

Animal behavior detection using extra-trees algorithm and accelerometer data

applications of the technique to free-ranging animals (Nathan et al., 2012).
Early studies in animal behavior classification relied on visual observation of
the accelerometer data (Yoda et al., 2001) or manually developed Decision
Trees (DTs) (G´omez Laich, Wilson, Quintana, & Shepard, 2009) for each
species, while more recently, there have been several statistical and machine-
learning approaches used for animal behavior classification from accelerometer
datasets. Some of the techniques explored by authors for accelerometer data
analysis include DT, RF, KNN, and SVM algorithms, as well as Hidden
Markov Models (HMMs) and Hidden Semi-Markov Models (HSMMs). Table 1
contains a brief overview of the species and the classification techniques used
for its behavior classification. Wherever multiple models or techniques are
listed, the primary algorithm described by the authors or the most accurate
method for behavior classification is listed first.

Species

Analysis
Model

Citation

Hebridean Sheep (Ovis aries)

Chacma Baboons (Papio ursinus)

RF

RF

Eurasian Badger (Meles meles)

KNN

California Horn Sharks (Heterodontus francisci)

KNN

Alpine Chipmunks (Tamias alpinus)
Lodgepole Chipmunks (Tamias speciosus)

Kalahari Meerkats (Suricata suricatta)

Holstein Dairy Cows (Bos taurus)

HSMM,
SVM

Linear-
Kernel
SVM

DT Algo-
rithm,
HMM,
SVM

North American Red Squirrels (Tamiasciurus hudsonicus) Manually

Created
DT

Kleanthous
et al.
(2020)

Fehlmann
et al.
(2017)

McClune
et al.
(2014)

Karan et
al. (2019)

Hammond
et al.
(2016)
Chakravarty
et al.
(2019)

V´azquez Dios-
dado et
al. (2015)

Studd et
al. (2018)

Imperial Cormorants (Phalacrocorax atriceps)

Manually
Created
DT

G´omez Laich
et al.
(2009)

Animal behavior detection using extra-trees algorithm and accelerometer data

5

Table 1: Table Comparing Accelerometer Data Analysis Techniques Used for
Different Species

Researchers have also explored using easily accessible surrogate species or
captive animals to build training datasets to identify similar behavioral modes
in other, harder-to-observe specimen. One approach trained RF models on
accelerometer data from captive polar bears (Ursus maritimus) and brown
bears (Ursus arctos) and evaluated the model’s performance on data from
free-ranging, wild polar bears (Pagano et al., 2017). Another approach used an
SVM classifier trained on data from a domestic dog (Canis lupus familiaris) to
classify behavior in species as diverse as Australian dingo (Canis lupus dingo),
a Eurasian badger (Meles meles), a Bengal tiger (Panthera tigris tigris), an
African cheetah (Acinonyx jubatus), an American alligator (Alligator mis-
sissippiensis), a hairy-nosed wombat (Lasiorhinus krefftii ), an Eastern grey
kangaroo (Macropus giganteus), and a short-beaked echidna (Tachyglossus
aculeatus) (Campbell, Gao, Bidder, Hunter, & Franklin, 2013). Studies using
this approach would be able to identify behavioral modes in species for whom
it is not possible to capture training data directly, but they require highly accu-
rate classification models that can extrapolate well from the surrogate species
or the captive individuals, necessitating machine-learning approaches.

Thus, similar to the human activity recognition domain, the state-of-the-art
algorithms used in the animal behavior classification domain seem to be pri-
marily decision-tree-based models, such as RF and DT models, as well as SVM
and KNN classification models. ET models have been shown to be systemati-
cally faster to train than other decision-tree-based models and have been shown
to outperform them on classification tasks (Geurts et al., 2006). Although there
is strong prior evidence that ET models can outperform traditional models on
some machine-learning tasks (Abbas et al., 2021), so far no study has been con-
ducted introducing these models in the animal behavior classification domain
and comparing them against the non-decision-tree-based state-of-the-art mod-
els. This paper hence seeks to compare the performance of the optimized ET
models with the current non-decision-tree-based state-of-the-art models in the
animal classification domain (SVM and KNN).

2.2 Hybrid Optimized Extra-Tree Models

There are many different optimization algorithms that have been used for
hyperparameter optimization for various machine-learning models over the
years. The most common approaches include Bayesian optimization algorithms
(such as Sequential-Model-Based Optimization (SMBO), Gaussian Processes,
and Tree-structured Parzen Estimators (TPE) (Bergstra, Yamins, & Cox,
2013)), evolutionary optimization algorithms (such as Genetic Algorithm (GA)
(Mitchell, 1998)) and swarm intelligence algorithms (such as Particle Swarm
Optimization (PSA) (Kennedy & Eberhart, 1995), Firefly Algorithm (FA) (X.-
S. Yang, 2009), Dwarf Mongoose Optimization Algorithm (DMO) (Agushaka,

6

Animal behavior detection using extra-trees algorithm and accelerometer data

Ezugwu, & Abualigah, 2022), and Reptile Search Algorithm (RSA) (Abuali-
gah, Elaziz, Sumari, Geem, & Gandomi, 2022)). These algorithms allow for
the construction of hybrid models that include an optimization algorithm
that optimizes the hyperparameters passed to a conventional machine-learning
model. Such hybrid approaches have been developed for several different mod-
els, such as convolutional neural networks (Strumberger et al., 2019), SVMs
(Anupam & Kar, 2021), and RFs (Huang, Sabri, Ulrikh, Ahmad, & Alsaffar,
2022).

However, hyperparameter optimization for applications of ET models has
so far been restricted primarily to grid search (Xie, Zhu, Hu, & Zhu, 2021) or
random search (Zainab, Ghrayeb, Houchati, Refaat, & Abu-Rub, 2020). While
hybrid models comprising of well-known optimization algorithms and ETs have
been proposed, they do not use optimization algorithms for hyperparameter
optimization but rather use them for feature selection on the training datasets
(Sharaff & Gupta, 2019). Thus, the hybrid model approach explored in this
paper is relatively novel, as a Bayesian optimization algorithm, TPE, is used
for the hyperparameter optimization of ETs. The hybrid model’s performance
is then evaluated relative to other standard machine-learning models in the
domain.

3 Methodology

3.1 Dataset Sources and Collection Methods

The data used in this project was taken from publicly available online sources
which had collected the data as part of previous research projects, one on
Holstein dairy cows (V´azquez Diosdado et al., 2015) and the other on North
American red squirrels (Studd et al., 2018). The methods and devices used in
data collection by the original researchers are provided below:

1. The tri-axial acceleration data in the dairy cow dataset was collected from
six housed dairy cows in a commercial Holstein dairy cattle farm in Essex,
UK by V´azquez Diosdado et al. (2015). The cows wore neck collars with tag
sensors from the Omnisense Series 500 Cluster Geolocation System. The
accelerometer recorded tri-axial acceleration continuously at 50 Hz, and the
data was collected continuously from each cow for 36 hours, with direct
visual observation of cows recorded for 33 hours and 25 minutes for valida-
tion purposes (V´azquez Diosdado et al., 2015). The study was conducted
with the approval of the Royal Veterinary College Ethics and Welfare Com-
mittee (reference number 2012 1223). The variables recorded in this dataset
were the mean of the static component of acceleration in the Y-axis (SCAY)
and the mean of the Vectorial Dynamic Body Acceleration (VeDBA) over
window sizes of 1-minute and 5-minutes. Direct visual observations of the
cows were also recorded for 33 h and 25 min for data validation purposes,
and the datapoints were classified into three categories - lying, standing
and feeding (V´azquez Diosdado et al., 2015). These observations were the

Animal behavior detection using extra-trees algorithm and accelerometer data

7

dependent variables which we used for prediction purposes to evaluate the
performance of our models. Ultimately, there were 2019 samples in the 1-
minute dataset and 604 samples in the 5-minute dataset which were used
in the experiments run in our paper.

2. The tri-axial acceleration data in the North American red squirrels dataset
was collected by Studd et al. (2019) from a population of free-ranging male
red squirrels in southwestern Yukon (61◦ N, 138◦ W) who were fitted with
collar comprising of a ventrally mounted VHF radio-transmitter (model
PD-2C, 4g, Holohil Systems Limited, Carp, ON, Canada) and a dorsally
mounted tri-axial accelerometer (model Axy2, 4g, Technosmart Europe).
The squirrels remained free-ranging until they were recaptured after 22 days
on average and their collar was removed. Data was collected between Febru-
ary and October 2014, with 37 accelerometers deployed on 20 individuals
during winter (February) and mating season (March), 25 accelerometers on
18 individuals in summer, 30 accelerometers on 30 individuals in autumn,
with a total of 1924 days of recording (Studd et al., 2019). The variables
recorded in this dataset were the raw acceleration data along the x, y, and
z axes from the accelerometer, recorded at 2-second intervals, and were
classified into eight classes on the basis of video observations: caching, clip-
ping cones, digging, feeding, grooming, running, slow travel, and vocalizing
(Studd et al., 2019). These classes were used as the predicted variable for the
purposes of evaluating our classifiers. Ultimately, there were 61738 samples
in the dataset which were used in the experiments run in our paper.

3.2 Machine-Learning Algorithms

3.2.1 Extra-Trees Algorithm

This paper uses the Extra Trees (ET) classifier to classify the behavior of var-
ious animals using the data collected from accelerometers. The ET algorithm
was developed to combat the problem of high cut-point variance in tree-based
models, such as Classification and Regression Trees (CART), well documented
in empirical studies from the 90s (Wehenkel, 1998). Optimal cut points, defined
as the point maximizing the score for a given problem and a given feature
at a particular decision node, were shown to be strongly dependent on the
specific learning samples used, and the cut-point variance of the tree-based
models was shown to be responsible for their error rates (Geurts, 2002). Boot-
strap aggregation or ”bagging”, which involves building multiple trees trained
on random samples drawn with replacement from the overall dataset, was a
technique proposed to reduce variance (Breiman, 1996). This was then incor-
porated into Random Forest (RF) models, which reduce the variance of the
classifier by randomly sampling both data points and features and providing
different samples to different trees, generating an ensemble model that either
takes a majority vote across all decision trees or averages the predictions of all
the decision trees to generate its final output.

8

Animal behavior detection using extra-trees algorithm and accelerometer data

Although trees produced by ensemble methods like RF use randomization
in their construction, they do not build totally random trees, and ET models
were developed to explore if higher degrees of randomization could further
improve the accuracy of tree-based models. ET models choose to train each tree
on all data points, and randomly sample features and splits instead (Geurts
et al., 2006). So for a given tree, at each node, the ET classifier randomly
picks K features from the feature vector, generates K random splits (one for
each feature), and then selects the feature that maximizes a score based on
the normalized Shannon information gain (Desir, Petitjean, Heutte, Salaun,
& Thiberville, 2012). This process occurs for M trees, which are used as an
ensemble classifier.

The ET classifier algorithm as defined by its original authors is presented

below (Geurts et al., 2006):

Animal behavior detection using extra-trees algorithm and accelerometer data

9

Algorithm 1 Extra-Trees Classifier (as described in Geurts et al. (2006))
1: procedure BuildEnsemble(S)
2:

Input: training set S, Output: Tree ensemble T = {t1, . . . , tM }
for i ← 1 to M do

3:

4:

5:

11:

12:

13:

14:

15:

16:

17:

18:

19:

25:

26:

27:

28:

29:

30:

31:

32:

33:

34:

ti ← BuildTree(S)

end for
return T

6:
7: end procedure
8:
9: procedure BuildTree(S)
10:

Input: training set S, Output: Tree t
if |S| < nmin or all candidate attributes are constant in S or output

variable is constant in S then
return Leaf

else

Randomly select K attributes {a1, . . . , aK} without replacement
from all candidate attributes non-constant in S
Generate K splits {s1, . . . , sK} where ∀ i = 1, . . . , K; si =RandomSplit(S, ai)
Select split s∗ such that Score(s∗, S) = maxi=1,...,KScore(si, S)
Split S into subsets Sl and Sr based on test s∗
tl ← BuildTree(Sl); tr ← BuildTree(Sr)
return tree t with root node having split s∗ with tl and tr as its left
and right subtrees

end if
20:
21: end procedure
22:
23: procedure RandomSplit(S, a)
24:

Input: training set S and attribute a, Output: split s
if a is numerical then

aS
min = minimum value of a in S; aS
Draw cut-point ac uniformly in [amin, amax]
return a < ac

max = maximum value of a in S

else

if a is categorical then let A denote its set of possible values

AS = subset of values appearing in S
Randomly draw proper non-empty subset A1 ⊂ AS and subset A2 ⊆
A \ AS
return a ∈ A1 ∪ A2

end if

end if
35:
36: end procedure

As a result, the model has three hyperparameters that can be used for
tuning it: K, which is the number of attributes selected at each node, nmin,

10

Animal behavior detection using extra-trees algorithm and accelerometer data

the minimum sample size for splitting a node, and M , the number of trees in
the ensemble classifier model. Two of these parameters were set to the default
values as recommended by the original authors of the algorithm, with nmin = 2
n (where n is the total number of features
to prevent overfitting, and K =
provided to the model) to filter out irrelevant examples and reduce variance
(Geurts et al., 2006).

√

However, during the course of the project, it was discovered that changing
the value of M led to differences in performance, which is why the value of
M was determined using the Hyperopt library’s implementation of the Tree-
structured Parzen Estimators (TPE) algorithm (Bergstra et al., 2013), which
is described next.

3.2.2 Tree-Structured Parzen Estimators (TPE)

The Tree-Structured Parzen Estimators (TPE) algorithm was first described
in Bergstra et al. (2011). The optimization problem is defined as finding a
global minimum of the objective function, which is a function that returns the
validation loss when provided with the hyperparameter values as arguments.
This is effectively a black-box function from the optimization algorithm’s per-
spective as it does not receive any formal mathematical description of the
objective function. To limit calls to the objective function (which could be
time-consuming to compute), a surrogate function (or response surface) is con-
structed, which helps choose more optimal hyperparameters at each iteration,
prior to making a time-consuming call to the objective function.

This surrogate function is a probabilistic model denoted as p(y|x), where
y is the validation loss, and x denotes the hyperparameters being optimized
(Bergstra et al., 2011). In order to find optimal hyperparameters under the
(current) surrogate function prior to calling the objective function, the optimal
arguments to a selection function are determined. The selection function used
in this algorithm is the Expected Improvement (EI) function. Thus finding
the optimal hyperparameters under the surrogate function p(y|x) is equivalent
to finding the hyperparameters that maximize the EI function (Zhao & Li,
2018).

The TPE algorithm is a type of Sequential Model-Based Optimization
(SMBO) algorithm. The general algorithm is defined as follows, given an objec-
tive function f , a surrogate function modeling f at time t = 0 (M0), a selection
function S, and an observation history H:

Animal behavior detection using extra-trees algorithm and accelerometer data

11

Algorithm 2 SMBO Algorithm (as described in Bergstra et al. (2011))
1: procedure SMBO(f, M0, T, S)
2:

H ← ∅
for t ← 1 . . . T do

x∗ ← argminxS(x, Mt−1)
Compute f (x∗)
H ← H ∪ (x∗, f (x∗))
Fit Mt to H

3:

4:

5:

6:

7:

8:

end for
return H

9:
10: end procedure

The TPE algorithm, instead of directly constructing the surrogate func-
tion Mt = p(y|x), builds it by computing p(x|y) and p(y) using Bayes’ rule
(cid:16)
p(y|x) = p(x|y)·p(y)

. Then the algorithm computes p(x|y) as follows:

(cid:17)

p(x)

p(x|y) =

(cid:40)

l(x)
g(x)

if y < y∗
if y ≥ y∗

(1)

where l(x) and g(x) are probability distributions modeled using Parzen esti-
mators on existing data points such that p(y < y∗) = γ is some quantile γ of
existing values. l(x) and g(x) can be computed using Parzen estimators (Zhao
& Li, 2018).

The EI function is defined as follows:

EIy∗ (x) =

(cid:90) y∗

−∞

(y − y∗)p(y|x)dy =

(cid:90) y∗

−∞

(y − y∗)

p(x|y) · p(y)
p(x)

dy

(2)

By definition we have γ = p(y < y∗) and p(x) = (cid:82)
(1 − γ)g(x) (Bergstra et al., 2011) . This implies:

R p(x|y) · p(y)dy = γl(x) +

(cid:90) y∗

−∞

(y−y∗)·p(x|y)·p(y)dy = l(x)

(cid:90) y∗

−∞

(y−y∗)·p(y)dy = γy∗l(x)−l(x)

(cid:90) y∗

−∞

p(y)dy

(3)

This in turn implies the following (Zhao & Li, 2018):

EIy∗ =

γy∗l(x) − l(x) (cid:82) y∗

−∞ p(y)dy

γl(x) + (1 − γ)g(x)

(cid:18)

∝

γ +

g(x)
l(x)

(cid:19)−1

(1 − γ)

(4)

As a result, improvement is maximized by picking points x with a high
probability under l(x) and a low probability under g(x). By drawing many
candidates and evaluating them according to g(x)
l(x) , the algorithm returns can-
didates x∗ which have the greatest expected improvement at step 4 of each

12

Animal behavior detection using extra-trees algorithm and accelerometer data

iteration (Bergstra et al., 2011). In this manner, the TPE algorithm was used
in the hybrid ET-TPE model to optimize M (the number of trees) to maxi-
mize the mean of the F1 weighted-average scores of the ET model after k -fold
cross-validation had occurred.

3.3 Benchmark Algorithms

3.3.1 K-Nearest Neighbors Algorithm

The k-nearest neighbors algorithm is a machine-learning model which classifies
new points from the test set depending on which class its k-nearest neighbor-
ing points in the training set lie. The algorithm first selects the k number of
data points which have the smallest Euclidean distance to the new point, and
then calculates the probability of the new point belonging to any given class.
It is possible to set a threshold i.e. at least t of the new points’ k-nearest neigh-
bors must belong to one class in order for the new point to be assigned to
that class. As a result, classifications that surpass the threshold but prove to
be incorrectly classified become false positives, whereas classifications that are
correctly classified but failed to surpass the threshold become false negatives
(Bidder et al., 2014). As the k-nearest neighbors model is used for bench-
marking purposes, the value of k is set to 5, which is the value used in earlier
works for benchmarking the performance of other algorithms on accelerome-
ter datasets to that of the k-nearest neighbors algorithm (Chakravarty et al.,
2019).

3.3.2 Support Vector Machines

Support Vector Machines (SVMs) are machine-learning models that find opti-
mal hyperplanes that separate the training data into different classes (Cortes
& Vapnik, 1995). Let the predicted class of a data point x(i) be denoted as
y(i) = wT x(i) + b where w is the vector of coefficients and b is a constant such
that the optimal hyperplane is denoted by wT x + b. Then finding the optimal
hyperplane is equivalent to minimizing the following function:

1
2

wT w + C

n
(cid:88)

i=1

ξi

(5)

subject to the constraints ξi ≥ 0 and yi(wT w + b) > 1 − ξi ∀i = 1 . . . n. Here ξi
are the slack variables measuring the degree of misclassification of x(i) and C
is a positive regularization constant (Campbell et al., 2013). Using Lagrangian
multipliers to simplify the problem and converting the resulting form into its
dual, the problem is equivalent to minimizing the following function:

n
(cid:88)

i=1

αi −

1
2

n
(cid:88)

n
(cid:88)

i=1

j=1

yiyjαiαjK(xi, xj)

(6)

subject to (cid:80)n
i=1 yiαi = 0 and 0 ≤ αi ≤ C, where αi are the Lagrangian mul-
tipliers and K(u, v) is a kernel function denoting an inner product in feature

Animal behavior detection using extra-trees algorithm and accelerometer data

13

space. One of the commonly used kernel functions is the RBF kernel function,
defined as K(u, v) = exp(−γ∥u − v∥2).

Thus, for training an SVM model, it is required to define the kernel function
as well as the regularization cost parameter C. If the kernel function used is
the RBF kernel function, it also becomes necessary to define the γ parameter.
In previous research, four SVM model configurations have been shown to be
optimal configurations for animal behavior classification: one using a linear
kernel, one using a polynomial kernel, and two using the RBF kernel (Brennan,
Johnson, & Olson, 2021). The linear and polynomial kernel SVMs failed to
converge on our datasets. Of the two RBF kernel configurations presented,
the configuration with hyperparameter values C = 100 and γ = 1 is used for
benchmarking purposes as this configuration had the higher mean F1 score of
the two on our datasets.

4 Results and Discussions

The accelerometer data from the two species under study were used as the
input for the model, and the ET classifiers were trained on this data. A K-
Nearest Neighbors (KNN) classifier with k = 5 and an SVM model using the
RBF kernel function with C = 100 and γ = 1 was used for comparison with the
performance of the ET model. For both models, 10-fold cross-validation was
conducted to examine the performance of the models with different samples
of data used for training and testing. In 10-fold cross-validation, the dataset
was randomly divided into ten equal subsets, or ’folds’, of which one fold is
retained as a test set and the others serve as the training set. This procedure
was repeated ten times, with a different fold used as the test set each time,
after which the mean accuracy metric was computed from all ten trials. For
classification, each dataset was provided to three algorithms: the ET-TPE
model and the benchmark KNN and SVM models. For each dataset, the TPE
algorithm returned the optimal hyperparameter M for maximizing the mean
F1 score computed from cross-validation. This optimal hyperparameter M was
then used to build the ET model and determine its classification accuracy. The
trials were conducted on a 16-inch 2019 MacBook Pro with a 2.6 GHz 6-Core
Intel Core i7 processor and 16 GB 2667 MHz DDR4 RAM.

Two measures of accuracy were used for evaluating the performance of the
model. The first was the mean classification accuracy of the model across all
10 cross-validations, which was simply the mean of the percentage of samples
the model classified accurately. The second was the mean weighted F1 score of
the model across all 10 validations, where the overall F1 score of the classifier
was computed by taking the weighted average of the F1 scores of the multiple
classes according to the number of samples in each class (Pedregosa et al.,
2011).

The resulting mean accuracies and mean F1 scores post-cross-validation
are presented in 2. The ET-TPE algorithm outperformed the SVM and
KNN models in all metrics across all three datasets - the North American

14

Animal behavior detection using extra-trees algorithm and accelerometer data

red squirrels (Tamiasciurus hudsonicus) dataset with the accelerometer data
recorded in 2-second intervals, the Holstein dairy cows (Bos taurus) dataset
with the accelerometer data recorded in one-minute windows and the dairy
cow dataset with the accelerometer data recorded in five-minute windows.

Algorithm Dairy Cows (1 Minute) Dairy Cows (5 Minutes)

Red Squirrels

Mean
Accu-
racy

Mean
F1
Score

ET-TPE 87.51
87.17
86.83

KNN
SVM

0.8720
0.8664
0.8558

Mean
Accu-
racy

90.89
88.08
90.08

Mean
F1
Score

0.9112
0.8772
89.85

Mean
Accu-
racy

96.99
90.10
93.81

Mean
F1
Score

0.9697
0.8968
0.9369

Table 2: Mean Accuracies and Mean F1 Scores of Algorithms Across Datasets

To ensure that the differences were statistically significant, two one-way
repeated measures ANOVA tests were conducted. The first one-way repeated
measures ANOVA test was conducted on 30 test-train splits (3 datasets,
10 splits per dataset for k-fold cross-validation) to examine the effect that
three different algorithms had on accuracy. The results showed that the
type of algorithm used led to statistically significant differences in accu-
racy (F (2, 58) = 20.3488, p < 0.001).The second one-way repeated measures
ANOVA test was conducted on 30 test-train splits to examine the effect that
three different algorithms had on F1 scores. The results showed that the
type of algorithm used led to statistically significant differences in accuracy
(F (2, 58) = 25.4852, p < 0.001). Thus in both cases, we reject the null hypoth-
esis, and thus the choice of algorithm has a statistically significant effect on
the accuracy and F1 scores of the model.

This demonstrates that the TPE-optimized ET classifier model provides a
statistically significant improvement in the domain of animal behavior classifi-
cation as compared to the standard KNN and SVM models. Thus, the system
can be used for tracking the behaviors of diverse ranges of species due to its
generalizability and efficiency. Given that the ET classifier outperformed the
KNN and SVM classifiers on both metrics and on datasets of differing sizes,
the results also show that the TPE-optimized ET classifier is more versatile
and adaptable to datasets of varying size and differing features.

The results of this paper can potentially reduce researchers’ dependency
on having to manually identify animal behavior from large amounts of data
that need to be accurately transmitted by accelerometers. It can also open a
pathway for accelerometer data to be used more often for investigating under-
lying causes of changes in animal behavioral patterns and lead to a greater
understanding of animal behavior in the wild. Behavioral assessment through
accelerometers has many benefits if it were to be done on larger scales, such as
the analysis of human-animal conflict and the development of inferences about

Animal behavior detection using extra-trees algorithm and accelerometer data

15

animal ecology and the ways in which animals interact with their environments
(Fehlmann et al., 2017).

5 Conclusions

Determining activity budgets for different animals is important for studying a
wide range of problems in animal behavior, but the uncertainty about deciding
which tools to use for classifying accelerometer data has been a hindrance to
widespread adoption of this technique (Patterson, Gilchrist, Chivers, Hatch,
& Elliott, 2019). By conducting a comparative study on the performance of
different machine-learning models on different datasets, this project aims to
help future researchers make informed decisions when it comes to the numerous
classification models available for classifying accelerometer data.

Machine-learning methods for accelerometer data classification have a wide
variety of use cases, especially when the behaviors identified by the model devi-
ate from normal patterns observed in other instances. This can be especially
helpful in diagnosing physical conditions in the subjects, such as lameness and
differences in gait (Barwick et al., 2018). In other cases, identifying differ-
ences in activity budgets of animals can help measure the impact of various
disturbances in their environment on their behavioral patterns (Christiansen,
Rasmussen, & Lusseau, 2013).

However, there are several directions for future research to explore. In our
case, for the Holstein cow dataset, we obtained more accurate results for low-
frequency data as opposed to high-frequency data, a finding consistent with
previous studies (Studd et al., 2019). However, this in turn may lead to difficul-
ties while using machine-learning models to identify behavior only observable
for short bursts of time, resulting in a trade-off between documenting long-term
behavioral patterns continuously across large periods of time or recording fine-
scale behavior at millisecond sampling rates. Using a single machine-learning
model to identify both may prove to be challenging, and may even require the
utilization of different summary statistics variables and sampling techniques
(Studd et al., 2019). Further research is also needed to ensure that model pre-
dictions remain accurate when applied to different kinds of animals as well
as across different types of plants, especially when using machine learning to
monitor behavior such as grazing (Brennan et al., 2021).

In the future, widespread adoption of accelerometer data for the calcula-
tion of activity budgets, bout durations, and transitions between states can aid
in studies in a diverse variety of fields ranging from precision livestock farming
to animal ecology (V´azquez Diosdado et al., 2015). Additionally, maintain-
ing an online activity recognition system and integrating it with GPS-based
position-tracking systems can improve animal welfare and management sys-
tems (Kleanthous et al., 2020). The ability to record and classify behavioral
habits independent of light and weather conditions can now help answer a
broader range of questions about how species interact with their ever-changing
environments (Studd et al., 2019).

16

Animal behavior detection using extra-trees algorithm and accelerometer data

Competing Interests

The authors declare that they have no competing interests.

Ethical Statement

The authors declare that no work involving any animal subjects was con-
ducted as a part of this project, and only publicly available data collected by
authors of other studies was used to compare model performance. The rele-
vant datasets were developed with the approval of the following organizations:
the Royal Veterinary College Ethics and Welfare Committee (reference num-
ber 2012 1223) (V´azquez Diosdado et al., 2015) and the Kluane Red Squirrel
Project (Studd et al., 2019).

References

Abbas, S., Jalil, Z., Javed, A.R., Batool, I., Khan, M.Z., Noorwali, A.,
. . . Akbar, A.
(2021, March). BCD-WERT: a novel approach for
breast cancer detection using whale optimization based efficient features
and extremely randomized tree algorithm. PeerJ Computer Science,
7 , e390. Retrieved 2022-12-25, from <https://peerj.com/articles/cs-390>
(Publisher: PeerJ Inc.)

10.7717/peerj-cs.390

(2022, April).

Abualigah, L., Elaziz, M.A., Sumari, P., Geem, Z.W., Gandomi,
Reptile Search Algorithm (RSA): A
A.H.
Systems
nature-inspired meta-heuristic
with Applications, 191 ,
from
<https://www.sciencedirect.com/science/article/pii/S0957417421014810>

Retrieved 2022-12-26,

optimizer.

116158.

Expert

10.1016/j.eswa.2021.116158

Agushaka, J.O., Ezugwu, A.E., Abualigah, L.

(2022, March). Dwarf
Mongoose Optimization Algorithm. Computer Methods in Applied
Mechanics and Engineering, 391 , 114570. Retrieved 2022-12-26, from
<https://www.sciencedirect.com/science/article/pii/S0045782522000019>

10.1016/j.cma.2022.114570

Ahmed, N., Rafiq, J.I., Islam, M.R. (2020, January). Enhanced Human Activ-
ity Recognition Based on Smartphone Sensor Data Using Hybrid Feature
Sensors, 20 (1), 317. Retrieved 2022-12-26, from
Selection Model.

Animal behavior detection using extra-trees algorithm and accelerometer data

17

<https://www.mdpi.com/1424-8220/20/1/317>
Multidisciplinary Digital Publishing Institute)

(Number: 1 Publisher:

10.3390/s20010317

Anupam, S., & Kar, A.K. (2021, January). Phishing website detection using
support vector machines and nature-inspired optimization algorithms.
Telecommunication Systems, 76 (1), 17–32. Retrieved 2022-12-26, from
<https://doi.org/10.1007/s11235-020-00739-w>

10.1007/s11235-020-00739-w

Barwick, J., Lamb, D., Dobos, R., Schneider, D., Welch, M., Trotter, M.
(2018, January). Predicting Lameness in Sheep Activity Using Tri-Axial
Acceleration Signals. Animals, 8 (1), 12. Retrieved 2021-03-22, from
<http://www.mdpi.com/2076-2615/8/1/12>

10.3390/ani8010012

(2011, December). Algo-
Bergstra, J., Bardenet, R., Bengio, Y., K´egl, B.
rithms for Hyper-Parameter Optimization.
(Vol. 24). Neural Infor-
mation Processing Systems Foundation. Retrieved 2021-06-18, from
<https://hal.inria.fr/hal-00642998>

Bergstra, J., Yamins, D., Cox, D.

(2013, February). Making a Sci-
ence of Model Search: Hyperparameter Optimization in Hundreds of
Dimensions for Vision Architectures.
International Conference on
Machine Learning (pp. 115–123). PMLR. Retrieved 2021-06-16, from
<http://proceedings.mlr.press/v28/bergstra13.html> (ISSN: 1938-7228)

Bidder, O.R., Campbell, H.A., G´omez-Laich, A., Urg´e, P., Walker, J., Cai,
Y., . . . Wilson, R.P. (2014, February). Love Thy Neighbour: Automatic
Animal Behavioural Classification of Acceleration Data Using the K-
Nearest Neighbour Algorithm. PLoS ONE , 9 (2), e88609. Retrieved
2021-03-22, from <https://dx.plos.org/10.1371/journal.pone.0088609>

10.1371/journal.pone.0088609

Breiman, L.

(1996, August).
123–140.
24 (2),

Learning,
<https://doi.org/10.1007/BF00058655>

Bagging predictors.

Retrieved

2022-12-28,

Machine
from

10.1007/BF00058655

Brennan, J., Johnson, P., Olson, K.

Classify-
ing season long livestock grazing behavior with the use of a

(2021, February).

18

Animal behavior detection using extra-trees algorithm and accelerometer data

Computers and Electron-
low-cost GPS and accelerometer.
ics
from
in Agriculture, 181 , 105957.
<https://www.sciencedirect.com/science/article/pii/S0168169920331628>

Retrieved 2022-12-26,

10.1016/j.compag.2020.105957

Brown, D.D., Kays, R., Wikelski, M., Wilson, R., Klimley, A.

(2013).
Observing the unwatchable through acceleration logging of animal
behavior. Animal Biotelemetry, 1 (1), 20. Retrieved 2021-03-22, from
<http://animalbiotelemetry.biomedcentral.com/articles/10.1186/2050->
3385-1-20

10.1186/2050-3385-1-20

Campbell, H.A., Gao, L., Bidder, O.R., Hunter, J., Franklin, C.E.

(2013,
December). Creating a behavioural classification module for acceleration
data: using a captive surrogate for difficult to observe species. Journal of
Experimental Biology, 216 (24), 4501–4506. Retrieved 2021-03-22, from
<http://jeb.biologists.org/cgi/doi/10.1242/jeb.089805>

10.1242/jeb.089805

Chakravarty, P., Cozzi, G., Ozgul, A., Aminian, K.

(2019,
A novel biomechanical approach for animal behaviour
and
from

June).
recognition
Evolution,
<https://onlinelibrary.wiley.com/doi/abs/10.1111/2041-210X.13172>

in Ecology
2021-03-22,

accelerometers.

using
10 (6),

Retrieved

802–814.

Methods

10.1111/2041-210X.13172

Christiansen, F., Rasmussen, M.H., Lusseau, D. (2013, November). Inferring
activity budgets in wild animals to estimate the consequences of distur-
bances. Behavioral Ecology, 24 (6), 1415–1425. Retrieved 2021-08-19,
from <https://doi.org/10.1093/beheco/art086>

10.1093/beheco/art086

Cortes, C., & Vapnik, V.

Support-vector net-
works. Machine Learning, 20 (3), 273–297. Retrieved 2023-01-01, from
<https://doi.org/10.1007/BF00994018>

(1995, September).

10.1007/BF00994018

Desir, C., Petitjean, C., Heutte, L., Salaun, M., Thiberville, L.

(2012,
September). Classification of Endomicroscopic Images of the Lung
Based on Random Subwindows and Extra-Trees. IEEE Transactions on

Animal behavior detection using extra-trees algorithm and accelerometer data

19

Biomedical Engineering, 59 (9), 2677–2683.
Transactions on Biomedical Engineering)

(Conference Name: IEEE

10.1109/TBME.2012.2204747

Fehlmann, G., O’Riain, M.J., Hopkins, P.W., O’Sullivan, J., Holton,
Identi-
M.D., Shepard, E.L.C., King, A.J.
fication of behaviours
from accelerometer data in a wild social
primate. Animal Biotelemetry, 5 (1), 6. Retrieved 2021-03-22, from
<http://animalbiotelemetry.biomedcentral.com/articles/10.1186/s40317->
017-0121-3

(2017, December).

10.1186/s40317-017-0121-3

Geurts, P.

(2002, May). Contributions to decision tree induction: bias/-
variance tradeoff and time series classification. Retrieved 2022-12-28,
(Publisher: ULi`ege -
from https://orbi.uliege.be/handle/2268/25737
Universit´e de Li`ege)

Geurts, P., Ernst, D., Wehenkel, L.

(2006, April). Extremely randomized
trees. Machine Learning, 63 (1), 3–42. Retrieved 2021-03-22, from
<http://link.springer.com/10.1007/s10994-006-6226-1>

10.1007/s10994-006-6226-1

G´omez Laich, A., Wilson, R., Quintana, F., Shepard, E. (2009, May). Iden-
tification of imperial cormorant Phalacrocorax atriceps behaviour using
accelerometers. Endangered Species Research, 10 , 29–37. Retrieved
2021-03-22, from <http://www.int-res.com/abstracts/esr/v10/p29-37/>

10.3354/esr00091

Hammond, T.T., Springthorpe, D., Walsh, R.E., Berg-Kirkpatrick, T.
(2016, June). Using accelerometers to remotely and automatically
The Journal of Experi-
characterize behavior in small animals.
mental Biology, 219 (11), 1618–1624.
from
<http://jeb.biologists.org/lookup/doi/10.1242/jeb.136135>

Retrieved 2021-03-22,

10.1242/jeb.136135

Huang, J., Sabri, M.M.S., Ulrikh, D.V., Ahmad, M., Alsaffar, K.A.M. (2022,
January). Predicting the Compressive Strength of the Cement-Fly
Ash–Slag Ternary Concrete Using the Firefly Algorithm (FA) and
Random Forest (RF) Hybrid Machine-Learning Method. Materials,

20

Animal behavior detection using extra-trees algorithm and accelerometer data

15 (12), 4193. Retrieved 2022-12-26, from <https://www.mdpi.com/1996->
1944/15/12/4193
(Number: 12 Publisher: Multidisciplinary Digital
Publishing Institute)

10.3390/ma15124193

Karan, S., Meese, E.N., Yang, Y., Yeh, H.-G., Lowe, C.G., Zhang, W.
(2019, November). Classification of Shark Behaviors using K-Nearest
Neighbors. 2019 IEEE Green Energy and Smart Systems Conference
(IGESSC) (pp. 1–6). (ISSN: 2640-0138)
10.1109/IGESSC47875.2019
.9042395

Kennedy, J., & Eberhart, R. (1995). Particle swarm optimization. Proceed-
ings of ICNN’95-international conference on neural networks (Vol. 4, pp.
1942–1948). IEEE.

Kleanthous, N., Hussain, A., Khan, W., Sneddon, J., Mason, A. (2020). Fea-
ture Extraction and Random Forest to Identify Sheep Behavior from
Accelerometer Data. D.-S. Huang & P. Premaratne (Eds.), Intelligent
Computing Methodologies (pp. 408–419). Cham: Springer International
Publishing. 10.1007/978-3-030-60796-8 35

Martin, P., & Bateson, P.P.G. (2007). Measuring behaviour: an introductory
guide (3rd Edition ed.). Cambridge: Cambridge University Press.

Mar´ee, R., Wehenkel, L., Geurts, P.

(2013).

Extremely Random-
ized Trees and Random Subwindows for Image Classification, Anno-
tation, and Retrieval.
A. Criminisi & J. Shotton (Eds.), Deci-
sion Forests for Computer Vision and Medical Image Analysis (pp.
from
125–141).
<http://link.springer.com/10.1007/978-1-4471-4929-310>
10.1007/978-1
-4471-4929-3 10

London: Springer London. Retrieved 2021-03-24,

McClune, D.W., Marks, N.J., Wilson, R.P., Houghton, J.D., Montgomery,
(2014, March). Tri-axial
I.W., McGowan, N.E., . . . Scantlebury, M.
accelerometers quantify behaviour in the Eurasian badger (Meles meles):
towards an automated interpretation of field data. Animal Biotelemetry,
2 (1), 5. Retrieved 2022-12-26, from <https://doi.org/10.1186/2050-3385->
2-5

10.1186/2050-3385-2-5

Mitchell, M. (1998). An introduction to genetic algorithms. MIT Press.

Nathan, R., Spiegel, O., Fortmann-Roe, S., Harel, R., Wikelski, M.,
Using tri-axial acceleration data

(2012, March).

Getz, W.M.

Animal behavior detection using extra-trees algorithm and accelerometer data

21

to identify behavioral modes of
cepts and tools illustrated for griffon vultures.
imental Biology, 215 (6), 986–996.
<http://jeb.biologists.org/cgi/doi/10.1242/jeb.058602>

free-ranging animals: general con-
Journal of Exper-
from

Retrieved 2021-03-22,

10.1242/jeb.058602

Pagano, A., Rode, K., Cutting, A., Owen, M., Jensen, S., Ware, J.,
Using tri-axial accelerome-
Endangered Species
from <http://www.int->

. . . Williams, T.
ters to identify wild polar bear behaviors.
Research, 32 , 19–33. Retrieved 2021-03-22,
res.com/abstracts/esr/v32/p19-33/

(2017, January).

10.3354/esr00779

Patterson, A., Gilchrist, H.G., Chivers, L., Hatch, S., Elliott, K.
(2019, March). A comparison of techniques for classifying behav-
Ecology
ior
and Evolution, 9 (6), 3030–3045.
from
<https://onlinelibrary.wiley.com/doi/abs/10.1002/ece3.4740>

Retrieved 2021-03-22,

from accelerometers

two species of

seabird.

for

10.1002/ece3.4740

Paul, P., & George, T.

(2015, March). An effective approach for human
activity recognition on smartphone. 2015 IEEE International Confer-
ence on Engineering and Technology (ICETECH) (pp. 1–3). 10.1109/
ICETECH.2015.7275024

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel,
O., . . . Duchesnay, (2011). Scikit-learn: Machine Learning in Python.
Journal of Machine Learning Research, 12 (85), 2825–2830. Retrieved
2021-07-07, from <http://jmlr.org/papers/v12/pedregosa11a.html>

Pinto, A., Pereira, S., Rasteiro, D., Silva, C.A.

(2018, October). Hier-
archical brain tumour
segmentation using extremely randomized
trees. Pattern Recognition, 82 , 105–117. Retrieved 2021-03-24, from
<https://www.sciencedirect.com/science/article/pii/S0031320318301699>

10.1016/j.patcog.2018.05.006

Sharaff, A., & Gupta, H. (2019). Extra-Tree Classifier with Metaheuristics
Approach for Email Classification. S.K. Bhatia, S. Tiwari, K.K. Mishra,
& M.C. Trivedi (Eds.), Advances in Computer Communication and Com-
putational Sciences (pp. 189–197).
10.1007/
978-981-13-6861-5 17

Singapore: Springer.

22

Animal behavior detection using extra-trees algorithm and accelerometer data

Strumberger, I., Tuba, E., Bacanin, N., Zivkovic, M., Beko, M., Tuba, M.
(2019, May). Designing Convolutional Neural Network Architecture
by the Firefly Algorithm. 2019 International Young Engineers Forum
(YEF-ECE) (pp. 59–65). 10.1109/YEF-ECE.2019.8740818

Studd, E.K., Landry-Cuerrier, M., Menzies, A.K., Boutin, S., McAdam,
A.G., Lane, J.E., Humphries, M.M.
(2018). Data from: Behavioral
classification of low frequency acceleration and temperature data from
a free ranging small mammal. Dryad. Retrieved 2021-07-06, from
<http://datadryad.org/stash/dataset/doi:10.5061/dryad.1s1m8r7>
(Art-
work Size: 93622442 bytes Pages: 93622442 bytes Version Number: 1
Type: dataset) 10.5061/DRYAD.1S1M8R7

Studd, E.K., Landry-Cuerrier, M., Menzies, A.K., Boutin, S., McAdam, A.G.,
Lane, J.E., Humphries, M.M. (2019). Behavioral classification of low-
frequency acceleration and temperature data from a free-ranging small
mammal. Ecology and Evolution, 9 (1), 619–630. Retrieved 2021-
07-02, from <https://onlinelibrary.wiley.com/doi/abs/10.1002/ece3.4786>
( eprint: <https://onlinelibrary.wiley.com/doi/pdf/10.1002/ece3.4786>)

10.1002/ece3.4786

Tatler, J., Cassey, P., Prowse, T.A.A. (2018, December). High accuracy at low
frequency: detailed behavioural classification from accelerometer data.
Journal of Experimental Biology, 221 (23). Retrieved 2021-04-02, from
(Publisher: The
<https://jeb.biologists.org/content/221/23/jeb184085>
Company of Biologists Ltd Section: Research Article)

10.1242/jeb.184085

Thakur, D., & Biswas, S.

(2022, May). Guided regularized random for-
est feature selection for smartphone based human activity recognition.
Journal of Ambient Intelligence and Humanized Computing. Retrieved
2022-12-26, from <https://doi.org/10.1007/s12652-022-03862-5>

10.1007/s12652-022-03862-5

Uddin, M.T., & Uddiny, M.A. (2015, May). Human activity recognition from
wearable sensors using extremely randomized trees. 2015 International
Conference on Electrical Engineering and Information Communication
Technology (ICEEICT) (pp. 1–6). 10.1109/ICEEICT.2015.7307384

V´azquez Diosdado, J.A., Barker, Z.E., Hodges, H.R., Amory, J.R., Croft, D.P.,
Bell, N.J., Codling, E.A. (2015, December). Classification of behaviour
in housed dairy cows using an accelerometer-based activity monitoring
system. Animal Biotelemetry, 3 (1), 15. Retrieved 2021-03-22, from

Animal behavior detection using extra-trees algorithm and accelerometer data

23

<http://www.animalbiotelemetry.com/content/3/1/15>

10.1186/s40317-015-0045-8

Wang, G.

(2019,
animal behavior
logical
Retrieved 2021-03-22,
69–76.
<https://linkinghub.elsevier.com/retrieve/pii/S1574954118302036>

for
Machine
January).
from location and movement data.

Informatics,

learning

49 ,

inferring
Eco-
from

10.1016/j.ecoinf.2018.12.002

Wehenkel, L.A.

(1998). Automatic learning techniques in power systems

(No. 429). Springer Science & Business Media.

Xie, Y., Zhu, C., Hu, R., Zhu, Z. (2021, July). A Coarse-to-Fine Approach for
Intelligent Logging Lithology Identification with Extremely Randomized
Trees. Mathematical Geosciences, 53 (5), 859–876. Retrieved 2022-12-26,
from <https://doi.org/10.1007/s11004-020-09885-y>

10.1007/s11004-020-09885-y

Yang, C.-C., & Hsu, Y.-L.

(2010, August). A Review of Accelerometry-
Based Wearable Motion Detectors for Physical Activity Monitor-
ing.
from
Sensors, 10 (8), 7772–7788.
<https://www.mdpi.com/1424-8220/10/8/7772>
(Number: 8 Publisher:
Molecular Diversity Preservation International)

Retrieved 2022-12-27,

10.3390/s100807772

Yang, X.-S.

(2009).

Firefly Algorithms for Multimodal Optimization.
O. Watanabe & T. Zeugmann (Eds.), Stochastic Algorithms: Founda-
tions and Applications (pp. 169–178). Berlin, Heidelberg: Springer.
10.1007/978-3-642-04944-6 14

Yoda, K., Naito, Y., Sato, K., Takahashi, A., Nishikawa, J., Ropert-Coudert,
(2001, February). A new technique for mon-
Y., . . . Le Maho, Y.
itoring the behaviour of
Journal of
Experimental Biology, 204 (4), 685–690. Retrieved 2022-12-27, from
<https://doi.org/10.1242/jeb.204.4.685>

free-ranging Adelie penguins.

10.1242/jeb.204.4.685

Yoda, K., Sato, K., Niizuma, Y., Kurita, M., Bost, C., Le Maho, Y., Naito,
Y.
(1999, November). Precise monitoring of porpoising behaviour of
Adelie penguins determined using acceleration data loggers. Journal of
Experimental Biology, 202 (22), 3121–3126. Retrieved 2022-12-27, from
<https://doi.org/10.1242/jeb.202.22.3121>

24

Animal behavior detection using extra-trees algorithm and accelerometer data

10.1242/jeb.202.22.3121

Zainab, A., Ghrayeb, A., Houchati, M., Refaat, S.S., Abu-Rub, H.

(2020,
December). Performance Evaluation of Tree-based Models for Big Data
Load Forecasting using Randomized Hyperparameter Tuning.
2020
IEEE International Conference on Big Data (Big Data) (pp. 5332–5339).
10.1109/BigData50022.2020.9378423

Zhao, M., & Li, J. (2018, March). Tuning the hyper-parameters of CMA-
ES with tree-structured Parzen estimators. 2018 Tenth International
Conference on Advanced Computational Intelligence (ICACI) (pp. 613–
618). 10.1109/ICACI.2018.8377530

Zhou, X., Pang, J., Liang, G. (2017, October). Image classification for malware
detection using extremely randomized trees. 2017 11th IEEE Inter-
national Conference on Anti-counterfeiting, Security, and Identification
(ASID) (pp. 54–59). (ISSN: 2163-5056) 10.1109/ICASID.2017.8285743

View publication stats
