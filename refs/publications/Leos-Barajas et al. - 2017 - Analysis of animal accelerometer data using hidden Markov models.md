Methods in Ecology and Evolution 2017, 8, 161–173

doi: 10.1111/2041-210X.12657

Analysis of animal accelerometer data using hidden
Markov models

Vianey Leos-Barajas1,*, Theoni Photopoulou2,3, Roland Langrock4, Toby A. Patterson5, Yuuki
Y. Watanabe6,7, Megan Murgatroyd8,9 and Yannis P. Papastamatiou10,11

1Department of Statistics, Iowa State University, Snedecor Hall, Ames, IA 50011, USA; 2Department of Statistical Sciences,
Centre for Statistics in Ecology, Environment and Conservation, University of Cape Town, Cape Town, Rondebosch 7701,
South Africa; 3Department of Zoology, Institute for Coastal and Marine Research, Nelson Mandela Metropolitan University,
Port Elizabeth 6031, South Africa; 4Department of Business Administration and Economics, Bielefeld University, Postfach
100131, 33501 Bielefeld, Germany; 5CSIRO Oceans and Atmosphere, PO Box 1538, Hobart, Tas. 7000, Australia;
6National Institute of Polar Research, 10-3, Midori-cho, Tachikawa, Tokyo 190-8518, Japan; 7SOKENDAI (The Graduate
University for Advanced Studies), 10-3, Midori-cho, Tachikawa, Tokyo 190-8518, Japan; 8Animal Demography Unit,
Department of Biological Sciences, University of Cape Town, Cape Town, Rondebosch 7701, South Africa; 9Percy
FitzPatrick Institute of African Ornithology, Department of Biological Sciences, University of Cape Town, Cape Town,
Rondebosch 7701, South Africa; 10School of Biology, Scottish Oceans Institute, University of St Andrews, St Andrews KY16
8LB, UK; and 11Department of Biological Sciences, Florida International University, 3000 NE 151st, MSB 350, North Miami, FL
33181, USA

Summary

1. Use of accelerometers is now widespread within animal biologging as they provide a means of measuring an
animal’s activity in a meaningful and quantitative way where direct observation is not possible. In sequential
acceleration data, there is a natural dependence between observations of behaviour, a fact that has been largely
ignored in most analyses.
2. Analyses of acceleration data where serial dependence has been explicitly modelled have largely relied on hid-
den Markov models (HMMs). Depending on the aim of an analysis, an HMM can be used for state prediction
or to make inferences about drivers of behaviour. For state prediction, a supervised learning approach can be
applied. That is, an HMM is trained to classify unlabelled acceleration data into a ﬁnite set of pre-speciﬁed cate-
gories. An unsupervised learning approach can be used to infer new aspects of animal behaviour when biologi-
cally meaningful response variables are used, with the caveat that the states may not map to speciﬁc behaviours.
3. We provide the details necessary to implement and assess an HMM in both the supervised and unsupervised
learning context and discuss the data requirements of each case. We outline two applications to marine and aerial
systems (shark and eagle) taking the unsupervised learning approach, which is more readily applicable to animal
activity measured in the ﬁeld. HMMs were used to infer the eﬀects of temporal, atmospheric and tidal inputs on
animal behaviour.
4. Animal accelerometer data allow ecologists to identify important correlates and drivers of animal activity
(and hence behaviour). The HMM framework is well suited to deal with the main features commonly observed
in accelerometer data and can easily be extended to suit a wide range of types of animal activity data. The ability
to combine direct observations of animal activity with statistical models, which account for the features of
accelerometer data, oﬀers a new way to quantify animal behaviour and energetic expenditure and to deepen our
insights into individual behaviour as a constituent of populations and ecosystems.

Key-words: activity recognition, animal behaviour, latent states, serial correlation, time series

Introduction

Accelerometers are becoming more prevalent in the ﬁelds of
animal and human biologging (Bao & Intille 2004; Ravi et al.
2005; Shepard et al. 2008; Altun, Barshan & Tunc(cid:1)el 2010).
The potential of accelerometers lies in the fact that they pro-
vide a means of measuring activity in a meaningful and

*Correspondence author. E-mail: <vianey@iastate.edu>

quantitative way where direct observation is not possible
(Shepard et al. 2008; Nathan et al. 2012; Brown et al. 2013).
While these instruments are cheap and compact, recording
acceleration at a high temporal resolution and in up to three
dimensions quickly results in terabytes of data that present var-
ious challenges regarding transmission, storage, processing
and statistical modelling.

Much of the focus in the analysis of acceleration data has
been on identifying patterns in the observed waveforms that

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society

162 V. Leos-Barajas et al.

correspond to a known behaviour or movement mode. This
can be achieved by employing statistical classiﬁcation methods
and can entail observing the animal, manually assigning labels
corresponding to behaviours to segments of the data and train-
ing a model using the labelled data in order to subsequently
classify remaining unlabelled data. Many studies have shown
the eﬀectiveness of various machine learning algorithms for
classiﬁcation of human acceleration data (Bao & Intille 2004;
Ravi et al. 2005; Altun, Barshan & Tunc(cid:1)el 2010; Mannini &
Sabatini 2010). Algorithms such as support vector machines
(SVM), classiﬁcation trees, random forests, among others,
have also recently been used for classiﬁcation of animal accel-
eration data (Nathan et al. 2012; Carroll et al. 2014; Graf
et al. 2015). For example, Nathan et al. (2012) compared the
eﬀectiveness of ﬁve machine learning algorithms to distinguish
between eating, running, standing, active ﬂight, passive ﬂight,
general preening and lying down, for griﬀon vultures.

Most machine learning algorithms assume independence
between individual observations. However, in sequential accel-
eration data there is a natural dependence between observa-
tions of behaviour – once initiated, particular animal
behaviours often last for periods longer than the sampling fre-
quency. This fact has been largely ignored in most applications
of classiﬁcation approaches. The studies where serial depen-
dence has been explicitly modelled have mostly relied on hid-
den Markov models (HMMs; Ward et al. 2006; He, Li & Tan
2007; Mannini & Sabatini 2010, 2011). HMMs are stochastic
time-series models which assume that the observed time series,
the so-called state-dependent process, is driven by an unob-
servable state process. In this scenario, the former corresponds
to the acceleration data and the latter to the behavioural
classes. Typically, and in common with the aforementioned
machine learning approaches, in the training stage, the states
of the HMM were known a priori, requiring corresponding
data derived from direct observations.

There are two main diﬃculties with such a supervised learn-
ing approach. First, while there has been much success in clas-
siﬁcation of human acceleration data, where training data can
usually be obtained with minimal eﬀort, this may not be feasi-
ble for some animals. Humans can easily be observed in a labo-
ratory setting, given instructions or monitored in more realistic
settings, such as walking outdoors or in their home (Leenders,
Sherman & Nagaraja 2000). In certain cases, animals can also
be monitored in a laboratory setting (Wilson, Shepard & Lieb-
sch 2008), but movement patterns recorded in the laboratory
from free-ranging animals may not appear exactly the same as
in data collected while in more natural settings. Conversely,
many behaviours can only be observed in natural settings,
although there has been success in using surrogate species for
classiﬁcation of behavioural modes (Shepard et al. 2008;
Nathan et al. 2012; Brown et al. 2013; Campbell et al. 2014).

Secondly, human acceleration data have commonly been
used as a tool for health monitoring and other situations where
the focus is on (state) prediction, as opposed to learning how
external factors drive the behaviours. Classiﬁcation of beha-
viours alone, while certainly of interest in many scenarios, may
lead to biologically interesting inference. Once the
not

classiﬁcation has been done, the task of relating these states to
environmental (and other) covariates in order to identify dri-
vers in behaviours remains. Moreover, it is diﬃcult to make
appropriate inferential statements as the classiﬁcations are not
without error, propagating the state uncertainty through to the
modelled eﬀect of the covariates.

In the supervised learning context, that is, when classiﬁca-
tion is the main purpose of an analysis, we train the HMM to
recognize speciﬁc behaviours. Alternatively, HMMs can also
be used in an unsupervised learning context, that is, when there
are no labelled data. In an unsupervised learning context, the
states are not pre-deﬁned to represent a speciﬁc behaviour.
Instead, the states are allocated such that the model captures
as much as possible of the marginal distribution of the observa-
tions, that is, the distribution of an observation at a randomly
chosen time point, not conditional on the previous history of
the process, as well as their correlation structure. If biologically
meaningful response variables from the acceleration data are
considered, then the HMM states usually represent inter-
pretable activity levels or even proxies of behavioural modes.
Being data-driven, the states can be as, if not more, informative
in the unsupervised learning setting than the alternatives. We
can then incorporate exogenous or, where available, endoge-
nous variable(s) of interest, to make inferential statements.
HMMs and related state-switching models, in particular state-
space models, have successfully been implemented to identify
drivers of movement based on tracking data (Patterson et al.
2009) and can similarly be applied in the context of accelerom-
eter data. For example, Phillips et al. (2015) applied HMMs in
an unsupervised learning context to understand the behaviour
of free swimming tuna from vertical movement data collected
by data storage tags. We implement an unsupervised learning
approach for another diﬃcult to observe marine species, the
blacktip reef shark and a volant species, the black eagle.

In this paper, we review HMM-based approaches to the
analysis of animal accelerometer data. In section ‘Accelerome-
ter data’, we provide an overview of accelerometer data and
connect
the data processing step to the HMM-based
approaches described in section ‘Analysis of accelerometer
data’. We refer to the term behavioural class, rather than diﬀer-
entiate between identiﬁcation of speciﬁc movements (e.g. wing
ﬂapping) and behaviours (e.g. foraging). In section ‘Real data
examples’, we demonstrate the use of HMMs with real data
examples from marine and aerial systems.

Accelerometer data

Accelerometer devices measure up to three axes, which can be
described relative to the body of the animal: longitudinal
(surge), lateral (sway) and dorsoventral (heave). Acceleration
recorded along one or two axes can be used to measure move-
ment in parts of the body, for example, the mandible (Suzuki
et al. 2009; Naito et al. 2010; Iwata et al. 2015), or aspects of
whole body acceleration, for example,
longitudinal surge
(Sakamoto et al. 2009). Currently, acceleration is most com-
monly recorded in three axes and, to a lesser degree, in two
axes (Brown et al. 2013), to measure locomotion.

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseD A T A P R O C E S S I N G F O R C L A S S I F I C A T I O N

While the observed acceleration data can be used to identify
speciﬁc movements in animals, HMMs and other machine
learning algorithms require more information to accurately
classify the unlabelled data. These methods require appropri-
ate features, that is, summary statistics, from a window (or slid-
ing window) of observations. The derived features should be
driven by the classes of movements that have been deﬁned and
chosen in such a way to accentuate the diﬀerences in observed
acceleration measurements. There are many commonalities
between the features used in applications of classiﬁcation of
acceleration data, though naturally no one optimal set exists
(Bao & Intille 2004; Martiskainen et al. 2009; Nathan et al.
2012; Brown et al. 2013). For instance, Nathan et al. (2012)
used 38 features in order to distinguish between eating, run-
ning, standing, active ﬂight, passive ﬂight, general preening
and lying down, for griﬀon vultures, while Graf et al. (2015)
used eight features to distinguish between standing, walking,
swimming, feeding, diving and grooming of Eurasian beavers.
In each case, means and variances of each of the three axes are
used, as well as overall dynamic body acceleration (ODBA),
the sum of dynamic body acceleration from the three axes,
among others.

C O N N E C T I N G M E A S U R E S T O B E H A V I O U R S

When the aim is to classify the acceleration data, data pro-
cessing is driven by identifying a set of features that can
be used to distinguish between speciﬁc behaviours, even if
those features are not themselves interpretable as a speciﬁc
behaviour when considered on their own. However, there
are metrics derived from accelerometer data that, on their
own, can be used as proxies for behaviour and as input to
an HMM. Repeating patterns in at least one axis tend to
arise from behaviours such as stroking (Sakamoto et al.
2009), ﬂapping, running or walking (Shepard et al. 2008),
whereas sudden changes, corresponding to bursts of accel-
eration, are often associated with prey pursuits or capture
(Suzuki et al. 2009; Simon, Johnson & Madsen 2012;
Watanabe & Takahashi 2013; Heerah et al. 2014; Ydesen
et al. 2014), as well as predator avoidance or conﬂict.

In addition to behaviour, several measures can be used to
summarize eﬀort or exertion and relate acceleration to activity
levels, such as ODBA (Wilson et al. 2006; Gleiss, Wilson &
Shepard 2011; Elliott et al. 2013; Gleiss et al. 2013) and vecto-
rial dynamic body acceleration (Qasem et al. 2012). Minimum
speciﬁc acceleration (MSA; Simon, Johnson & Madsen 2012)
can be used to disentangle the gravitational component of
acceleration (static acceleration) from the movement signal or
speciﬁc acceleration (also dynamic acceleration). One of the
simplest and most unambiguous interpretations of static accel-
eration data is body posture, which in many cases can be
directly interpreted as a speciﬁc behaviour (Shepard et al.
2008; Wilson, Shepard & Liebsch 2008).

Both ODBA and MSA are used to reduce the dimensional-
ity of three-dimensional acceleration data while retaining

Hidden Markov models for accelerometer data 163

important information (Wilson, Shepard & Liebsch 2008;
Simon, Johnson & Madsen 2012). They remove the gravita-
tional component from the acceleration signature and produce
an overall value of the dynamic acceleration experienced by
the animal. ODBA is derived by smoothing over a time period,
for example, 1 s, making it useful for continuous data, whereas
MSA is calculated pointwise (as the norm of the three vectors
minus 1 for the eﬀect of gravity) and is more suited to lower
resolution acceleration data.

Analysis of accelerometer data

We ﬁrst provide a brief overview of the HMM framework (sec-
tion ‘Hidden Markov Models’). Subsequently, in section ‘State
Prediction’, we review how HMMs can be used for state pre-
diction, that is, classiﬁcation of animal accelerometer data. In
section ‘Inference’, we focus on the implementation of HMMs
in a setting where the meaning of the states is driven entirely by
the data and the focus lies on general inference rather than clas-
siﬁcation only.

H I D D E N M A R K O V M O D E L S

An HMM is a stochastic time-series model involving two lay-
ers: an observable state-dependent process, denoted by fYtgT
t¼1
(in the univariate case), and an unobservable state process,
denoted by fCtgT
t¼1. The state-dependent process models the
observations, while the state process is a latent factor inﬂuenc-
ing the distribution of the observations. In our case, the obser-
vations are the accelerometer metrics considered, and the
latent states are closely related to the animal’s behavioural
state. More speciﬁcally, the state process {Ct} takes on a ﬁnite
number of possible values, 1,. . .,M, and its value at time t, ct,
selects which of M possible component distributions generates
observation yt. The Markov property is assumed for {Ct}, that
is, the (behavioural) state at time t only depends on the (be-
havioural) state at time t (cid:2) 1, such that evolution of the pro-
cess over time is completely characterized by the one-step state
transition probabilities. These models are natural and intuitive
candidates for modelling animal accelerometer data, for two
reasons: (i) they directly account for the fact that any corre-
sponding observation will be driven by the underlying beha-
vioural state, or general activity level, of the animal, and (ii)
they accommodate serial correlation in the time series by
allowing states to be persistent. HMMs seek to capture the
strong autocorrelation in accelerometer data in a mechanistic
way, rather than either neglecting this feature completely or
only including it in a nuisance error term. HMMs can therefore
be used for inference on complex temporal patterns, including
the behavioural state-switching dynamics and how these are
driven by environmental variables (Patterson et al. 2009;
McKellar et al. 2015).

To complete the basic HMM formulation, we ﬁrst summa-
rize the probabilities of transitions between the diﬀerent states
in the M 9 M transition probability matrix (t.p.m.) C ¼ ðcijÞ,
where cij ¼ PrðCtþ1 ¼ jjCt ¼ iÞ (for any t), i; j ¼ 1; . . .; M.
Note that here we are assuming that the state transition

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License164 V. Leos-Barajas et al.

probabilities are constant over time; this assumption is relaxed
in section ‘Inference’. The initial state probabilities are summa-
rized in the row vector d, where di ¼ PrðC1 ¼ iÞ, i ¼ 1; . . .; M.
Secondly, we need to specify state-dependent distributions
(sometimes called emission distributions), pðytjCt ¼ mÞ, or
more succinctly pmðytÞ, for m ¼ 1; . . .; M. These distributions
can be discrete or continuous, and possibly also multivariate
(in which case we write yt ¼ ðy1t; . . .; yRtÞ). Usually, the same
parametric distribution is assigned to all M states, such that
each state diﬀers in terms of its associated values of the param-
eters. Selection is driven by the data itself, for example, count
data or continuous observations.

S T A T E P R E D I C T I O N

Hidden Markov models provide a solid framework for the
classiﬁcation of data with strong serial dependence, such as
sequential acceleration data, which are often processed to rep-
resent movements over a few seconds, or less, at a time (Ward
et al. 2006; He, Li & Tan 2007; Mannini & Sabatini 2010). In
this section, we cover the implementation and testing of an
HMM when the focus of the analysis is state prediction. A full
example and R code implementing this approach is provided in
the Appendix S1 (Supporting Information).

State prediction can be accomplished in three manners, com-
monly referred to as supervised, semi-supervised or unsuper-
vised learning. We discuss the implementation of an HMM in
the supervised learning case, such that each state corresponds
to one behaviour of interest, and brieﬂy comment on the other
two cases at the end of the section. Hastie, Tibshirani & Fried-
man (2001) detail how to split the labelled time series into train-
ing, validation and testing data, in order to estimate the
prediction error. Other approaches to estimating prediction
error, such as a leave-one-out cross-validation (here treating a
time series as an observation), are also provided in detail.

Since the states are known, the maximum likelihood esti-
mates (MLEs) of the HMM parameters are obtained by maxi-
mizing the complete-data likelihood, which conveniently splits
into several independent parts, each of which is fairly straight-
forward to maximize (details provided in the Appendix S3).
First, the mth entry of ^d is simply the proportion of the time
series that start in state m. Secondly, the entries of the t.p.m.,
are estimated by

^cij ¼

# transitions from state i to state j

total # transitions from state i

;

for i; j ¼ 1; . . .; M. (Note this is the MLE conditional on the
initial state, c1.) Finally, for each m ¼ 1; . . .; M, the parameters
of the state-dependent distribution given state m are estimated
using only the observations allocated to state m. As a multi-
variate normal distribution (MVN) is a common choice in
these cases, we cover the steps to ﬁt the HMM with MVN
in the Appendix S3 and
state-dependent distributions
Supporting Information. Given a ﬁtted HMM, we can use the
Viterbi algorithm to decode the most likely state sequence,
thereby assigning each observation to a state, at low computa-
tional eﬀort. Full details for state decoding are provided in

Zucchini, MacDonald & Langrock (2016). The state predic-
tions can be compared to the known states, and the proportion
of correctly decoded states serves as an estimate of the predic-
tion accuracy.

As mentioned previously, there are two other approaches to
state prediction: semi-supervised and unsupervised learning. In
a semi-supervised approach, classes are pre-deﬁned, as in the
supervised learning context, but there is additional ﬂexibility
provided in that the data do not have to be assigned to one of
the pre-deﬁned classes. Instead, multiple additional states can
be estimated from the data. In an unsupervised learning
approach, classes are not pre-deﬁned in any manner. In these
two cases, one objective can be to identify the number of dis-
tinct movement patterns exhibited by the animal, with the
resulting estimated HMM states depending on the features
selected for interpretation. However, as multiple movement
modes can correspond to the same behaviour (e.g. foraging),
interpretation of the estimated states should be made with cau-
tion. In the next section, we detail the implementation of the
unsupervised learning approach where the focus is to construct
biologically relevant classes of animal behaviour in order to
make inferential statements.

I N F E R E N C E

So far, we have mostly focused on the case where there is a
training sample, that is, acceleration data together with the
associated behavioural states. Corresponding analyses involve
training the HMM based on such labelled data and then using
that HMM to categorize incoming new, unlabelled data. While
certainly of interest in some settings, in practice, more often
than not, labelled data will not be available but only the
accelerometer data. In such unsupervised learning settings, the
HMM framework can be equally useful, but is typically
applied for diﬀerent purposes than in classiﬁcation. More
speciﬁcally, the meaning of the states in such cases is often not
of interest per se. Instead, an HMM is used simply as an
approximate representation of the real data-generating pro-
cess, and this may or may not entail that the nominal HMM
states are biologically meaningful. (However, metrics derived
from the accelerometer data, as described in section
‘Accelerometer data’, have been shown to provide insight into
activity levels or correspond to classes of behaviours, such that
when used as response variables in the HMM, these can lead
to biologically interpretable states.) Unsupervised learning of
HMMs for accelerometer data has the advantage that the
states are estimated in a data-driven manner. In particular, for
many of the metrics described in section ‘Accelerometer data’
that are connected to behaviours, assignment of classes is diﬃ-
cult, to say the least, especially for animals where behaviours
are not well deﬁned. These include animals which cannot be
directly observed for long periods such as aquatic organisms.

There are three diﬀerent possible purposes of having an
approximate representation of the real process: (i) a mathemat-
ical description of the dynamics of the system (e.g. in order to
have a concise description of how accelerometer measurements
evolve over time, in terms of a small number of interpretable

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons Licenseparameters and associated stochastic distributions); (ii) extrac-
tion of information (e.g. a hypothesis test on whether or not
some environmental covariate increases the probability of an
animal switching to a particular behavioural state); and (iii)
prediction of future or missing values (e.g. behavioural state
prediction given accelerometer data; Konishi & Kitagawa
2008). In the ecological literature on animal movement mod-
elling, HMMs are used primarily to address (i) and (ii), the for-
mer in the sense that concise descriptions of movement
patterns are sought and the latter in the sense that inference on
the interaction of animals with their environment is drawn. In
general, the ability to make inferential statements provides an
avenue to answer questions about the behavioural processes,
movement patterns and transitions between behaviours under
diﬀerent conditions or in relation to other covariates.

Addressing a research question related to aim (ii) usually
involves the incorporation of covariates into the statistical
model. In the HMM setting, this is commonly done at the level
of the hidden states. For the general case of time-varying
covariates, we deﬁne the corresponding time-dependent t.p.m.
CðtÞ ¼ ðcðtÞ
ij ¼ PrðCtþ1 ¼ jjCt ¼ iÞ. The transition
probabilities at time t, cðtÞ
ij , can then be related to a vector of
environmental (or other) covariates, ðxðtÞ
p Þ, via the
1
multinomial logit link:

ij Þ, where cðtÞ

; . . .; xðtÞ

P
(

expðgijÞ
N
k¼1 expðgikÞ
P
bðijÞ
0 þ

cðtÞ
ij ¼

gij ¼

; where

l xðtÞ

l

p

l¼1 bðijÞ
0

if i 6¼ j;
otherwise:

Essentially, there is one multinomial logit link speciﬁcation
for each row of the matrix CðtÞ, and the entries on the diagonal
of the matrix serve as reference categories.

is

the

the

density

observations

While with labelled data the likelihood of interest is the com-
plete-data likelihood, for unlabelled data the likelihood of
only,
of
interest
L ¼ pðy1; . . .; yT Þ, the evaluation of which requires the consid-
eration of all possible state sequences that might have given rise
to these data. The powerful forward algorithm, detailed in the
Appendix S3, can be applied to accomplish this, opening up a
straightforward and usually feasible avenue to MLEs, namely
direct numerical maximization of the likelihood. In practice,
one needs to consider multiple starting values in order to make
sure to have found the global maximum. The expectation–
maximization algorithm provides a popular alternative route
to MLEs, despite being much more technically involved and
having no clear practical advantages (MacDonald 2014). Since
it is our view that users are better oﬀ focusing on the simpler
direct maximization approach, it is only this approach that we
present in detail in the Appendix S3 and Supporting Informa-
tion (for a more comprehensive introduction to maximum like-
lihood estimation for HMMs, see Zucchini, MacDonald &
Langrock 2016).

Model selection techniques, in particular information crite-
ria, can be used to choose an adequate family of state-depen-
dent distributions, to select an appropriate number of states
or to determine whether or not a covariate should be included

Hidden Markov models for accelerometer data 165

in the model. However, users should not blindly follow such
information criteria, especially with regard to the selection of
the number of states. For animal behaviour data, it is our
experience that such formal model selection approaches tend
to favour models with more states than would be expected
based on biological intuition, often to an extent such that
selected models become near-impossible to interpret and very
diﬃcult to work with in practice (Langrock et al. 2015). One
explanation for this is that often additional states are included
to compensate for a model formulation that ignores some
pattern in the data. These patterns can be due to the inﬂuence
of an unobserved covariate, within-day variation or individ-
ual heterogeneity which is not accounted for, a violation of
the Markov assumption or outliers – which usually cannot be
avoided in data structures as complex as those studied here,
and which may not be pertinent to the ultimate aim of the
study. Further, accelerometer data are directly connected to
the movement of an animal, such that an HMM with a large
number of states may reﬂect multiple movement modes, or
general classes of movement, connected to the same beha-
vioural class, for example, foraging or active behaviour. In
such cases, a healthy dose of pragmatism is required. If the
choice of the number of states turns out to be diﬃcult, then it
is often useful to carefully examine all plausible models (with
lower and higher numbers of states), for example, using
model checking tools, in order to understand what exactly it
is that the more complex models capture that is not already
captured by the simpler models. Langrock et al. (2015) dis-
cuss this issue in detail, demonstrating many of the points
made above in a real data example.

The HMM framework encompasses various other useful
tools for drawing inference. In particular, incorporating ran-
dom eﬀects into the model formulation is crucial when there is
substantial heterogeneity across multiple individuals observed.
There are various ways in which this can be accomplished
within the class of HMMs – see McKellar et al. (2015) and
Chapter 13 in Zucchini, MacDonald & Langrock (2016) for
comprehensive overviews, including discussions on the impor-
tance of acknowledging any potential heterogeneity. Further-
more, the dependence structure can be modiﬁed in various
ways, for example, allowing for more complex memory in the
state process without losing the ability to eﬃciently calculate
the likelihood using the forward algorithm (Langrock et al.
2012). Assessment of the model adequacy, that is, model
checking, is commonly done using (pseudo)residuals, which
can reveal any notable lack of ﬁt (Zucchini, MacDonald &
Langrock 2016).

Real data examples

M O D E L L I N G A C T I V I T Y I N A S O A R I N G R A P T O R

Large soaring birds, like raptors, depend on favourable meteo-
rological conditions, as well as the underlying topography, for
generation of updrafts required for low-energy ﬂight (Penny-
cuick 2008). Lift availability is known to be driven largely by
wind speed and temperature, as well as their interaction with

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License166 V. Leos-Barajas et al.

the underlying topography, though other factors also con-
tribute. Lift adequate for soaring ﬂight is generated by two
mechanisms: (i) by upward thermal convection of air warmed
by solar radiation ( (cid:2)Akos et al. 2010) (thermal soaring) and (ii)
by the movement of air over slopes and ridges in the landscape
(orographic or ridge soaring).

Recently, empirical studies relating bird activity patterns to
weather conditions have become possible due to advances in
biologging technology that allows for collection of high-resolu-
tion movement (e.g. acceleration) data. In particular, accelera-
tion data can be used to distinguish between diﬀerent
movement modes or, more simply, as a proxy of overall activ-
ity level, even if they do not correspond clearly to diﬀerent
behaviours (Williams et al. 2015).

An adult Verreaux’s eagle Aquila verreauxii was instrumented
with a remotely downloadable multisensor data-logger (UvA-
BiTS, University of Amsterdam, the Netherlands; Bouten et al.
2013) in the Western Cape, South Africa, in 2013. The data-log-
ger recorded three-dimensional acceleration (at 20 Hz) for 1 s
directly after recording GPS location. The GPS location sam-
pling rate depended on the solar-powered battery charge and
thus was higher during the midday. Data were collected over
nine consecutive days, with a variable amount of acceleration
data sampled each day and none collected overnight.

We were primarily interested in identifying potential drivers
of activity level. As such, we extracted the MSA, which serves
as an index of activity, over each 1-second sample of accelera-
tion data recorded. On average, each day produced approxi-
mately 135 observations (s.e., 23(cid:3)32). Before ﬁtting an HMM
to the time series of MSA values, we ﬁrst needed to resolve the
irregular sampling of the acceleration data, as this is a clear vio-
lation of the HMM assumptions. The time series of MSA
across days were taken to be independent and, within a day,
the acceleration data were subsampled to produce one value of
MSA every 112 s (Fig. 1). Only one consecutive missing value
was allowed before splitting the daily MSA time series into two
or more segments.

The histogram of MSA values revealed two peaks close to
zero, which may reﬂect general low-active behaviours such as
roosting and preening. As we did not wish to discriminate
between these two general types of behaviours, we ﬁt a two-
state HMM with state 1 represented by a mixture of gamma

MSA values for 16 to 24 April

distributions and a gamma distribution for state 2. The ﬁtted
state-dependent densities are shown in Fig. 2, which we post
hoc interpreted as low-activity and high-activity behaviour.
Although we do not connect state 2 to a speciﬁc ﬂight beha-
viour, such as orographic soaring, we expect that behaviours
requiring more energy are reﬂected by larger MSA values.

In order to examine the eﬀect of wind speed and temperature
on the state-switching dynamics between the two activity
levels, we obtained hourly observations from the South Afri-
can Weather Services (Lambert’s Bay Station). The station is
approximately 30 km from the general area in which the eagle
was tracked, which lead to a slight spatial and temporal mis-
match between the available weather data and the conditions
actually experienced by the eagle. The range of temperatures
and wind speeds experienced by the eagle during the study per-
iod was between 12(cid:3)3 and 31(cid:3)5 °C and 0 and 7(cid:3)4 m/s, respec-
tively. We allowed the entries of the t.p.m. to be a function of
wind speed, temperature and their interaction. The wind-only
model is written as logitðcijðtÞÞ ¼ b0i þ b1ix1t, for i ¼ 1; 2,
j 6¼ i, t ¼ 1; . . .; T, with the intercept term b0;i reﬂecting the
t.p.m., when wind speed is at 0 m/s. The model including wind
speed alone was favoured by the Bayesian information crite-
rion (BIC) and the full model, with temperature and the inter-
action term, favoured by the Akaike information criterion
(AIC) (Table 1). After examination of the (pseudo)residuals of
the models selected by AIC and BIC, we selected the model
favoured by BIC as there was a similar lack-of-ﬁt evident in
both models. Further, we may not have captured a large
enough range of temperatures in order to make general infer-
ences about its eﬀect on the activity levels of the eagle and as
such were cautious of overﬁtting or overinterpreting the model
results. We present conﬁdence intervals and a plot of the
(pseudo)residuals for assessment of goodness-of-ﬁt in the
Appendix S3 for the model with only wind speed included. R
code to simulate MSA data and ﬁt a two-state HMM with the
t.p.m., entries as functions of wind speed is included in the Sup-
porting Information.

The estimated state transition probabilities suggest that,
as wind speed increases, (i) the eagle has a very slightly
increased chance of switching to the high-activity state
when in the low-activity state and (ii) spends much longer
in the active state. As a
periods of time, on average,

A
S
M

A
S
M

3

2

1

0

3

2

1

0

17 Apr

18 Apr

19 Apr

20 Apr

21 Apr

22 Apr

23 Apr

24 Apr

Date

MSA values for 21 April

07:00

11:00

15:00

19:00

Time of day

Fig. 1. Minimum speciﬁc acceleration values
derived from three-axis acceleration data from
a Verreaux’s eagle collected over 9 days, 16–
24 July 2013 (top). Minimum speciﬁc accelera-
tion values
21st of April,
corresponding to the shaded area in the upper
plot (bottom).

from the

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMarginal MSA density

State−dependent MSA densities

Hidden Markov models for accelerometer data 167

y
t
i
s
n
e
D

40

30

20

10

0

Densities
Marginal
State 1
State 2

y
t
i
s
n
e
D

60

40

20

0

0·0

0·0

0·5

1·0

1·5

2·0

Minimum specific acceleration (MSA)

y
t
i
s
n
e
D

8e−04
4e−04

1·5
0·5
Minimum specific acceleration (MSA)
Tail behaviour of densities

1·0

2·0

2·00

2·25

3·00
Minimum specific acceleration (MSA)

2·75

2·50

Fig. 2. Histogram of minimum speciﬁc acceleration (MSA) from a Verreaux’s eagle, truncated at MSA = 2, with marginal density (the distribution
of observations not conditional on process history) and state-dependent densities weighted according to the proportion of observations assigned to
each state (left). Unweighted state-dependent densities (top right) and close-up of the tail behaviour of the densities (bottom right). A square root
coordinate transformation for the x-axis was used in all plots and for the y-axis only for the tail behaviour plot.

Table 1. Model ﬁtting results for the Ver-
reaux’s eagle

Model

Log likelihood

AIC

ΔAIC

BIC

ΔBIC

No covariates
Temperature
Wind speed
Wind speed, temperature
Wind speed, temperature,
wind speed 9 temperature

2000(cid:3)2
2001(cid:3)9
2010(cid:3)4
2011(cid:3)6
2017(cid:3)0

(cid:2)3980(cid:3)4
(cid:2)3979(cid:3)9
(cid:2)3996(cid:3)9
(cid:2)3995(cid:3)2
(cid:2)4002(cid:3)0

21(cid:3)6
22(cid:3)1
5(cid:3)1
6(cid:3)8
0

(cid:2)3929(cid:3)4
(cid:2)3918(cid:3)6
(cid:2)3935(cid:3)6
(cid:2)3923(cid:3)7
(cid:2)3920(cid:3)3

21(cid:3)6
17(cid:3)0
0
11(cid:3)9
15(cid:3)3

Based on the AIC, the model selected is the full model including wind speed, temperature and
their interaction. Based on the BIC, the model selected includes only wind speed.
AIC, Akaike information criterion; BIC, Bayesian information criterion.

State–dwell probabilities

Stationary distribution

1·00

0·75

0·50

0·25

0·00

y
t
i
l
i

b
a
b
o
r
P

y
t
i
l
i

b
a
b
o
r
P

1·00

0·75

0·50

0·25

0·00

State 1 −> state 1

State 2 −> state 2

State 1

State 2

0

2
Wind speed (m s–1)

4

6

0

2
Wind speed (m s–1)

4

6

Fig. 3. For the Verreaux’s eagle example, estimated state-dwell probabilities (probability of remaining in a state) as a function of wind speed (left)
and estimated equilibrium state probabilities (marginal probability of a state at a ﬁxed value of the covariate) as a function of wind speed (right).

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License168 V. Leos-Barajas et al.

ODBA Values for 13 July 2013

A
B
D
O

8

6

4

2

0

13 Jul 00:00

13 Jul 06:00

13 Jul 12:00
Time of day

13 Jul 18:00

13 Jul 24:00

Fig. 4. Overall dynamic body acceleration
values from a blacktip reef shark, averaged
over 1-second intervals, for 13 July 2013.

consequence, the equilibrium (stationary) distribution for
ﬁxed wind speeds (Patterson et al. 2009) indicates that the
eagle spends more time in the active state overall as wind
speed increases (Fig. 3). Windier conditions favour oro-
graphic soaring, as demonstrated by studies on migrating
golden eagles Aquila chrysaetos, which is a more active
behaviour (Lanzone et al. 2012). There is also theoretical
evidence to suggest that, in general, ﬂying is more energeti-
cally demanding in high winds (Pennycuick 1972).

D I E L A C T I V I T Y C H A N G E S I N A R E E F - A S S O C I A T E D

S H A R K

Many species of shark are upper trophic level predators, which
may serve an important role in marine ecosystems. However,
determining the intensity of their predatory behaviour requires
modelling the temporal component as their activity levels are
likely to follow a diel and/or tidal cycle (Gleiss et al. 2013;
Papastamatiou et al. 2015). Acceleration sensors provide a
direct measure of activity; however, many species of shark
swim continuously making it diﬃcult to deﬁne speciﬁc beha-
viours (e.g. they are never truly at rest), making conventional
classiﬁcation methods problematic. HMMs can identify
changes in behavioural states and how these may be related to
time of day, tidal state, swimming depth or water temperature.
To demonstrate this, we applied HMMs to accelerometry data
obtained from a free-ranging blacktip reef shark Carcharhinus
melanopterus at Palmyra Atoll in the central Paciﬁc Ocean
(data taken from Papastamatiou et al. 2015). A multisensor
package was attached to the dorsal ﬁn of a 117-cm female
shark. The multisensor data-logger (ORI400-D3GT, Little
Leonardo, Tokyo, Japan) recorded three-dimensional acceler-
ation (at 20 Hz), depth and water temperature (at 1 Hz) and
was embedded in a foam ﬂoat which detached from the shark
after 4 days (Papastamatiou et al. 2015). The package also
contained a VHF transmitter allowing recovery at the surface
after detachment.

In order to examine active behaviour, we calculated the
average ODBA of the shark over 1-second intervals, which
resulted in 321 815 observations (after removing the ﬁrst four
hours of data). Figure 4 displays the ODBA time series of
1 day. Compared to metrics such as tail-beat frequency,
ODBA has the advantage of measuring change in behaviour in
all axes. For example, if the shark is nose down at the seaﬂoor,
attempting to capture prey, its tail-beat frequency may be low
but it is still active (Watanabe et al. 2012). As we are interested
in the times of day the shark was more active, as well as tide
eﬀects, we applied a two-state HMM with one state post hoc

interpreted as representing less active behaviour and the other
more active behaviour.

Although there are clear spikes in ODBA that point to
higher energetic activities, various combinations of parametric
distributions for state 1 and 2 led to vastly diﬀerent state-
dependent densities. Further, the ODBA values had many
extreme values that needed to be accommodated, which fur-
ther increased the diﬃculties of selecting appropriate state-
dependent distributions. As ODBA is not a metric that can
easily be divided into active/inactive behaviours in sharks, we
estimated the state-dependent densities nonparametrically, in
both states, in order to minimize the bias introduced by assign-
ing inadequate parametric distributions (Fig. 5; Langrock
et al. 2015).

To examine potential diel and tide eﬀects on activity levels,
we let the entries of the t.p.m., be functions of up to two covari-
ates: time of day and tide level (ebb, ﬂood, low and high). Tide
data were obtained from the NOAA tides and currents website
for Palmyra Atoll and was processed by denoting high or low
tide as (cid:4)1 h from reported high or low tide times. Time of day
is represented by two trigonometric functions with period 24 h,
cos(2pt/86 400) and sin(2pt/86 400) (86 400 is the number of
seconds in a day). We use three indicator variables, x1t; x2t and
x3t, for tide levels high, ﬂood and ebb, respectively, such that
x1t ¼ 1 when tide level is high and x1t ¼ 0 otherwise, and so
on, which gives the entries of the t.p.m., the following form

logitðcijðtÞÞ ¼ b0i þ b1i cosð2pt=86 400Þ

þ b2i sinð2pt=86 400Þ þ b3ix1t þ b4ix2t þ b5ix3t

for i ¼ 1; 2, j 6¼ i, t ¼ 1; . . .; 86 400. The intercept term b0;i
corresponds to low tide.

Based on the selected model (Table 2), with conﬁdence
intervals and (pseudo)residuals provided in the Appendix S3,
the shark’s activity levels were, on average,
lowest from
approximately 9:00–13:00 and highest from 21:00–1:00. In
Fig. 6, we see that the shark was more active during high tide
in general when compared to ﬂood, low or ebb tide. While the
equilibrium (or stationary) distribution associated with low
and ebb tide overlaps, the state-dwell probabilities, that is, the
diagonal entries of the t.p.m. corresponding to the probability
of remaining in the same state, are higher during ebb tide than
in low tide. Naturally in a short time series, the tide levels are
correlated with certain times of the day, but a longer time series
or a joint modelling of multiple time series, with tide levels
observed during all times of day, can provide robust estimates
of the eﬀect of tide on activity level using the HMM formula-
tion provided here.

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMarginal ODBA density

State−dependent ODBA densities

Hidden Markov models for accelerometer data 169

Density

State 1
State 2
Marginal

10

y
t
i
s
n
e
D

5

0

0·0

0·5

1·0

1·5

2·0

Overall dynamic body acceleration (ODBA)

y
t
i
s
n
e
D

15

10

5

0

y
t
i
s
n
e
D

1e−03

5e−04

0e+00

0·0

0·5

1·0

1·5

2·0

Overall dynamic body acceleration

Tail behaviour of densities

2

4

6

8

10

Overall dynamic body acceleration

Fig. 5. Histogram of overall dynamic body acceleration (ODBA) from a blacktip reef shark, truncated at ODBA = 2, with marginal density and
state-dependent densities weighted according to the proportion of observations assigned to each state. (left). Unweighted state-dependent densities
(top right) and close-up of the tail behaviour of the densities (bottom right). A square root coordinate transformation for the x-axis was used in all
plots and for the y-axis only for the tail behaviour plot.

Table 2. Model ﬁtting results for a blacktip reef shark

Stationary distribution for state 2

Log
likelihood AIC

ΔAIC BIC

ΔBIC

639 299(cid:3)2 (cid:2)1 278 370

779

(cid:2)1 277 178

692

639 558(cid:3)1 (cid:2)1 278 872
639 657(cid:3)6 (cid:2)1 279 063
639 695(cid:3)2 (cid:2)1 279 130

277(cid:3)2 (cid:2)1 277 645
86(cid:3)2 (cid:2)1 277 819
(cid:2)1 277 869
19

225
51
1

639 708(cid:3)7 (cid:2)1 279 149

0

(cid:2)1 277 870

0

Model

No

covariates

Time
Time, high
Time, high,

ﬂood

Time, high,
ﬂood, ebb

Based on the AIC and BIC, the model selected includes time of day and
includes diﬀerences in activity levels based on all categories of tide
levels.
AIC, Akaike information criterion; BIC, Bayesian information crite-
rion.

Using the Viterbi algorithm, we decoded the optimal
state sequence to underlie the ODBA time series. To fur-
ther understand the eﬀect of vertical habitat on behaviour,
we related the decoded state sequence to a grid of depth
and temperature values, shown in Fig. 7. The shark spent
most of its time over the nearly ﬁve-day period in depths
of about 3–6 m and between 28 and 29 °C, with some
higher counts also in shallower waters, which is reﬂected
in the state 2 counts. However, the percentages of state 2
the shark was generally more
observations reveal
active when near the surface in waters of 28–29 °C. There
was generally less active behaviour exhibited when the indi-
vidual was in very shallow warm water (>29 °C).

that

)
2
e
t
a
t
S

(

P

0·5

0·4

0·3

0·2

0·5

0·4

0·3

0·2

0·5

0·4

0·3

0·2

0·5

0·4

0·3

0·2

E
b
b

l

F
o
o
d

i

H
g
h

L
o
w

00:00

06:00

12:00
Time of day

18:00

24:00

Result

Estimate

Forecast

Fig. 6. Implied stationary distribution for state 2, the more active state,
by time of day and tide level for the blacktip reef shark example. For
tide levels, we distinguish between model estimates, such that the corre-
sponding tide level was observed at that time of day, and forecasts,
where we did not observe the tide level at that time of day.

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

170 V. Leos-Barajas et al.

No. of observations in state 2

% observations in state 2

)

m

(
h
t
p
e
D

0

2

4

6

8

10

Count

1500

1000

500

0

)

m

(
h
t
p
e
D

0

2

4

6

8

10

Percentage
1·00

0·75

0·50

0·25

0·00

28

29

30

31

32

33

28

29

30

31

32

33

Temperature (in Celsius)

Temperature (in Celsius)

Fig. 7. For the blacktip reef shark example,
the number of observations in each grid cell
that correspond to state 2. Zero counts appear
in white (left). Percentage of observations in
each cell that correspond to state 2 (right).

Discussion

We detailed two approaches for analysing animal accelerome-
ter data with HMMs: a supervised learning approach for state
prediction, such that classiﬁcation is of primary interest, and
an unsupervised learning approach, where the states reﬂect
biologically meaningful classes of behaviour, in order to infer
drivers of animal behaviour. The aim of a study and the type
of data available determine which of the two is to be preferred.
When the objective is to do classiﬁcation and there is a set of
pre-deﬁned behaviours of interest, then the model’s ability to
correctly predict and categorize behaviours is of main interest.
In this instance, a supervised learning approach may be
applied. One of the beneﬁts of such an approach is that the
behavioural classes are exactly deﬁned, making interpretation
relatively straightforward. Alternatively, if the objective is to
infer (or, colloquially speaking, to ‘learn’) new aspects of ani-
mal behaviour, then the unsupervised learning approach pro-
vides an excellent framework. The latter comes with the
implicit caveat that the states do not necessarily map directly
to speciﬁc animal behaviours. Any post hoc behavioural inter-
pretation of the estimated states is directly connected to the
metric(s) used and must draw from background biological
knowledge of the species of interest. In many cases, behaviours
such as foraging may not be exclusive to one state or another.
Nonetheless, if the model is able to identify bouts of behaviour
which consistently reappear, then it is often likely that these
signify something important in the animal’s behavioural reper-
toire and are worthy of further investigation.

Even when classiﬁcation is the goal of an analysis, there are
certainly practical scenarios which preclude the use of an
HMM, for example, if the training data do not reﬂect the

transitions between behaviours or if there are insuﬃcient data.
Moreover, multiple studies have shown that other machine
learning algorithms, for example, SVMs or random forests,
can work well for classiﬁcation of animal acceleration data
(Martiskainen et al. 2009; Nathan et al. 2012; Carroll et al.
2014; Graf et al. 2015). However, disregarding the serial
dependence in the acceleration data usually is an unrealistic
assumption, which often goes unmentioned or is treated as an
afterthought. Adopting the assumption of independence is
particularly risky if inferential statistics are applied to the out-
put of a machine learning algorithm. In these cases, secondar-
ily applied statistical tests implicitly assume that the machine
learning categorizations contain more information content
than is warranted, potentially leading to spurious results. This
is not just a statistical nuance and can be a crucial point. Such
tests are often applied as decision making tools to sort out
‘what matters’ and setting the direction for much further
research eﬀort. Also, in assuming independence, one allows for
classiﬁcations that may not be biologically realistic or must ﬁl-
ter the classiﬁcations to properly identify a speciﬁc behaviour.
For instance, Carroll et al. (2014) used a SVM where one of
the primary interests was to identify prey handling/capture for
penguins at sea. To conﬁrm a prey capture event, they ruled
that if the SVM classiﬁed three consecutive observations as
prey handling, this counted as a true prey capture. In contrast,
an HMM would have bypassed the need to ﬁlter through the
classiﬁcation results by accounting for the serial dependence in
observations corresponding to prey handling. In general, many
behaviours persist over longer stretches of time than those at
which the data are processed, also necessitating the use of a
model that can account for the serial dependence. It may be
diﬃcult for any machine learning algorithm that assumes

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

independence to properly classify a sequence of observations
into the same class, unless the boundaries between classes are
well deﬁned. In the context of recognition tasks, for example,
speech or pattern recognition, HMMs have proven to be extre-
mely successful tools for classiﬁcation precisely because they
do account for the serial dependence in the signal of interest
(Rabiner 1989).

In the literature, inference on behavioural state-switching
dynamics has sometimes been made using two-stage (or even
three-stage) analyses, where HMMs (or other machine learn-
ing algorithms) are used to decode the behaviours underlying
given observations, and subsequently a logistic regression is
conducted for relating the decoded behaviours to covariates
(Hart et al. 2010; Broekhuis et al. 2014). The appeal of such an
approach lies in the ease of implementation: fairly basic
HMMs, without covariates, are ﬁtted to the accelerometer
data and used to decode the states, and, subsequently, stan-
dard regression software packages can be used to conduct a
regression of the behavioural states on covariates. However, it
is our view that such a multistage analysis is less suited to relat-
ing accelerometer data to covariates than the joint modelling
approach presented in section ‘Inference’, for two reasons: (i)
in the multistage analyses, the uncertainty in state estimates is
usually not propagated through the diﬀerent stages of analysis,
and (ii) a regression analysis on decoded states needs to take
into account the high serial correlation in those states. Rather
than ignoring these issues or trying to address them within a
multistage analysis (which render such an approach technically
challenging), a direct joint modelling approach, where neither
of the problems arise, seems preferable.

Using a direct joint modelling approach in section ‘Real
data examples’, we were able to learn about the eﬀects that
atmospheric variables have on activity levels of a soaring rap-
tor, while for the blacktip reef shark we examined temporal
and tidal inputs eﬀects on its activity levels. The HMM pro-
duced similar temporal patterns of activity to a previous analy-
sis of the blacktip reef shark data set using generalized additive
mixed models (Papastamatiou et al. 2015). Both analytical
methods revealed crepuscular and/or nocturnal increases in
activity with a tidal component, with the shark most active at
the high tide or as tide was about to ebb. By incorporating
swimming depth and temperature, it was also revealed that
highest activity was seen when the shark was at the surface in
waters of 28–29 °C. More importantly, the analysis showed
that the shark was inactive when in very warm (>29 °C) shal-
low water or deeper water. These results agree with a previous
hypothesis that sharks are ‘hunting warm, and resting warmer’
and use warmer water (>29 °C) to increase the rate of some
physiological function such as digestion, and not for foraging
(Papastamatiou et al. 2015). The HMM in this case allows us
to explain the drivers of activity in the shark and move beyond
just describing its movements, but rather explain ‘why’ it may
be moving or selecting certain habitats. The HMM also pro-
vided a measure of the change in probability of the individual
being in active states. Although there was a clear temporal pat-
tern of activity, the HMM identiﬁed the shark as 30% more
likely to be in an active state during the late evening hours. For

Hidden Markov models for accelerometer data 171

the adult black eagle, the HMM provided a direct modelling
approach to examine the eﬀect of wind speed and temperature
on its activity level. The results suggests that the black eagle
spent more time in the relatively active state overall and was
more likely active in windier conditions. These results are in
line with theoretical (Pennycuick 1972) and empirical (Lan-
zone et al. 2012) studies.

We have covered the basic HMM framework here, but the
popularity of the HMM framework is due in part to its many
extensions. In particular, there are two HMM extensions that
have been proven useful in classiﬁcation of human activities:
the hidden semi-Markov model (HSMM) (Langrock & Zuc-
chini 2012) and the hierarchical HHMM (Fine, Singer &
Tishby 1998). The HSMM models the time spent within a state
by some probability distribution with support on the positive
real integers, thereby allowing for more complex state-dwell-
time distributions than can be provided by an HMM (namely
only geometric distributions). For instance, an HMM may not
model the time spent in a resting behaviour adequately if the
animal is known to rest for long periods of time. The HHMM
provides the framework necessary to identify composite beha-
viours. For instance, lunge feeding in baleen whales is a com-
posite behaviour made up of (i) initial increase in acceleration
with (ii) a positive pitch angle, as animals commonly approach
prey schools from below, followed by (iii) a rapid deceleration
after the whale opens its mouth increasing its drag (Owen et al.
2015). The HHMM models each composite behaviour as its
own HMM and models the transitions between composite
behaviours, that is, switches between HMMs.

Acknowledgements

Y.Y.W. was funded by Grants-in-Aid for Scientiﬁc Research from the Japan
Society for the Promotion of Science (grant reference 25850138). T.P. was sup-
ported by a South African National Research Foundation Scarce Skills Postdoc-
toral Research Fellowship, and T.P. and Y.P.P. received funding from the
MASTS pooling initiative (The Marine Alliance for Science and Technology for
Scotland) and their support is gratefully acknowledged. MASTS is funded by the
Scottish Funding Council (grant reference HR09011) and contributing institu-
tions. T.P. and M.M. gratefully acknowledge the hardware, software, support
and expertise contributed by Prof. Willem Bouten and his research group UvA-
BiTS (University of Amsterdam Bird Tracking System). Special thanks to J.
Caselle for supporting all ﬁeld work at Palmyra atoll. The authors are grateful to
Orr Spiegel, the Associate Editor and an anonymous referee for their useful com-
ments that substantially improved the manuscript.

Data accessibility

Data available from the Dryad Digital Repository <http://dx.doi.org/10.5061/>
dryad.6bm2c (Leos-Barajas et al. 2016).

References
(cid:2)Akos, Z., Nagy, M., Leven, S. & Vicsek, T. (2010) Thermal soaring ﬂight of birds

and unmanned aerial vehicles. Bioinspiration & Biomimetics, 5, 045003.

Altun, K., Barshan, B. & Tunc(cid:1)el, O. (2010) Comparative study on classifying
human activities with miniature inertial and magnetic sensors. Pattern Recog-
nition, 43, 3605–3620.

Bao, L. & Intille, S.S. (2004) Activity recognition from user annotated accelera-
tion data. Pervasive Computing (eds. A. Ferscha & F. Mattern), pp. 1–17.
Springer, Berlin, Heidelberg, Germany.

Bouten, W., Baaij, E.W., Shamoun-Baranes, J. & Camphuysen, K.C.J. (2013) A
ﬂexible GPS tracking system for studying bird behaviour at multiple scales.
Journal of Ornithology, 154, 571–580.

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License172 V. Leos-Barajas et al.

Broekhuis, F., Gr€unew€alder, S., McNutt, J.W. & Macdonald, D.W. (2014) Opti-
mal hunting conditions drive circalunar behavior of a diurnal carnivore.
Behavioral Ecology, 25, 1268–1275.

Brown, D., Kays, R., Wikelski, M., Wilson, R. & Klimley, A.P. (2013) Observing
the unwatchable through acceleration logging of animal behavior. Animal
Biotelemetry, 1, 1–16.

Campbell, H.A., Gao, L., Bidder, O.R., Hunter, J. & Franklin, C.E. (2014) Creat-
ing a behavioural classiﬁcation module for acceleration data: using a captive
surrogate for diﬃcult to observe species. Journal of Experimental Biology, 216,
4501–4506.

Carroll, G., Slip, D., Jonsen, I. & Harcout, R. (2014) Supervised accelerometry
analysis can identify prey capture by penguins at sea. Journal of Experimental
Biology, 217, 4295–4302.

Elliott, K.H., Le Vaillant, M., Kato, A., Speakman, J.R. & Ropert-Coudert, Y.
(2013) Accelerometry predicts daily energy expenditure in a bird with high
activity levels. Biology Letters, 9, 20120919.

Fine, S., Singer, Y. & Tishby, N. (1998) The hierarchical hidden Markov model:

analysis and applications. Machine Learning, 32, 41–62.

Gleiss, A.C., Wilson, R.P. & Shepard, E.L.C. (2011) Making overall dynamic
body acceleration work: on the theory of acceleration as a proxy for energy
expenditure. Methods in Ecology and Evolution, 2, 23–33.

Gleiss, A.C., Wright, S., Liebsch, N., Wilson, R.P. & Norman, B. (2013) Con-
trasting diel patterns in vertical movement and locomotor activity of whale
sharks at Ningaloo Reef. Marine Biology, 160, 2981–2992.

Graf, P.M., Wilson, R.P., Qasem, L., Hackl€ander, K. & Rosell, F. (2015) The use
of acceleration to code for animal behaviours; A case study in free-ranging
Eurasian beavers Castor ﬁber. PLoS One, 10, e0136751.

Hart, T., Mann, R., Coulson, T., Pettorelli, N. & Trathan, P.N. (2010)
Behavioural switching in a central place forager: patterns of diving behaviour
in the macaroni penguin (Eudyptes chrysolophus). Marine Biology, 157, 1543–
1553.

Hastie, T., Tibshirani, R. & Friedman, J. (2001) The Elements of Statistical Learn-

ing. Springer, New York, NY, USA.

He, J., Li, H. & Tan, J. (2007) Real-time daily activity classiﬁcation with wireless
sensor networks using hidden Markov model. 29th Annual International Con-
ference of the IEEE Engineering in Medicine and Biology Society, EMBC 2007,
pp. 3192–3195.

Heerah, K., Hindell, M., Guinet, C. & Charrassin, J.B. (2014) A new method to
quantify within dive foraging behaviour in marine predators. PLoS One, 9,
e99329.

Iwata, T., Sakamoto, K.Q., Edwards, E.W.J., Staniland, I.J., Trathan, P.N.,
Goto, Y., Sato, K., Naito, Y. & Takahashi, A. (2015) The inﬂuence of preced-
ing dive cycles on the foraging decisions of Antarctic fur seals. Biology Letters,
11, 20150227.

Konishi, S. & Kitagawa, G. (2008) Information Criteria and Statistical Modeling.

Springer, New York, NY, USA.

Langrock, R. & Zucchini, W. (2012) Hidden Markov models with arbitrary state
dwell-time distributions. Computational Statistics and Data Analysis, 55, 715–
724.

Langrock, R., King, R., Matthiopoulos, J., Thomas, L., Fortin, D. & Morales,
J.M. (2012) Flexible and practical modeling of animal telemetry data: hidden
Markov models and extensions. Ecology, 93, 2336–2342.

Langrock, R., Kneib, T., Sohn, A. & DeRuiter, S.L. (2015) Nonparametric infer-

ence in hidden Markov models using P-splines. Biometrics, 71, 520–528.

Lanzone, M.J., Miller, T.A., Turk, P. et al. (2012) Flight responses by a migra-
tory soaring raptor to changing meteorological conditions. Biology Letters, 8,
710–713.

Leenders, N.Y.J.M., Sherman, W.M. & Nagaraja, H.N. (2000) Comparisons of
four methods of estimating physical activity in adult women. Medicine &
Science in Sports & Exercise, 32, 1320–1326.

Leos-Barajas, V., Photopoulou, T., Langrock, R., Patterson, T.A., Watanabe,
Y.Y., Murtroyd, M. & Papastamatiou, Y. (2016) Data from: Analysis of ani-
mal accelerometer data using hidden Markov models. Methods in Ecology and
Evolution, <http://dx.doi.org/10.5061/dryad.6bm2c>

MacDonald, I.L. (2014) Numerical maximisation of likelihood: a neglected alter-

native to EM? International Statistical Review, 82, 296–308.

Mannini, A. & Sabatini, A.M. (2010) Machine learning methods for classifying
human physical activity from on-body accelerometers. Sensors, 10, 1154–1175.
Mannini, A. & Sabatini, A.M. (2011) Accelerometry-based classiﬁcation of
human activities using Markov modeling. Computational Intelligence and Neu-
roscience, 2011, 647858.

Martiskainen, P., J€arvinen, M., Sk€on, J., Tiirikainen, J., Kolehmainen, M. &
Mononen, J. (2009) Cow behaviour pattern recognition using a three-dimen-
sional accelerometer and support vector machines. Applied Animal Behaviour
Science, 119, 32–38.

McKellar, A.E., Langrock, R., Walters, J.R. & Kesler, D.C. (2015) Using mixed
hidden Markov models to examine behavioural states in a cooperatively breed-
ing bird. Behavioral Ecology, 26, 148–157.

Naito, Y., Bornemann, H., Takahashi, A., McIntyre, T. & Pl€otz, J. (2010) Fine-
scale feeding behavior of Weddell seals revealed by a mandible accelerometer.
Polar Science, 4, 309–316.

Nathan, R., Spiegel, O., Fortmann-Roe, S., Harel, R., Wikelski, M. & Getz, W.
(2012) Using tri-axial acceleration data to identify behavioral modes of free-
ranging animals: general concepts and tools illustrated for griﬀon vultures. The
Journal of Experimental Biology, 215, 986–996.

Owen, K., Dunlop, R.A., Monty, J.P., Chung, D., Noad, M.J., Donnelly, D.,
Golditzen, A.W. & Mackenzie, T. (2015) Detecting surface-feeding behavior
by rorqual whales in accelerometer data. Marine Mammal Science, 32, 327–
348.

Papastamatiou, Y.P., Watanabe, Y.Y., Bradley, D., Dee, L.E., Lowe, C.G. &
Caselle, J. (2015) Drivers of daily routines in an ectothermic marine predator:
hunt warm, rest warmer? PLoS One, 10, e0127807.

Patterson, T.A., Basson, M., Bravington, M.V. & Gunn, J.S. (2009) Classifying
movement behaviour in relation to environmental conditions using hidden
Markov models. Journal of Animal Ecology, 78, 1113–1123.

Pennycuick, C.J. (1972) Soaring behaviour and performance of some east african

birds, observed from a motor-glider. Ibis, 114, 178–218.

Pennycuick, C.J. (2008) Modelling the Flying Bird. Academic Press, Elsevier, Lon-

don, UK.

Phillips, J.S., Patterson, T.A., Leroy, B., Pilling, G.M. & Nicol, S.J. (2015) Objec-
tive classiﬁcation of latent behavioral states in bio-logging data using multi-
variate-normal hidden Markov models. Ecological Applications, 25(5), 1244–
1258.

Qasem, L., Cardew, A., Wilson, A., Griﬃths, I., Halsey, L.G., Shepard, E.L.C.,
Gleiss, A.C. & Wilson, R. (2012) Tri-axial dynamic acceleration as a proxy for
animal energy expenditure; Should we be summing values or calculating the
vector? PLoS One, 7, e31187.

Rabiner, L.R. (1989) A tutorial on hidden Markov models and selected applica-

tions in speech recognition. IEEE Proceedings, 77, 257–286.

Ravi, N., Dandekar, N., Mysore, P. & Littman, M.L. (2005) Activity recognition
from accelerometer data. American Association for Artiﬁcial Intelligence, 5,
1541–1546.

Sakamoto, K.Q., Sato, K., Ishizuka, M., Watanuki, Y., Takahashi, A., Daunt,
F. & Wanless, S. (2009) Can ethograms be automatically generated using body
acceleration data from free-ranging birds? PLoS One, 4, e5379.

Shepard, E.L.C., Wilson, R., Quintana, F. et al. (2008) Identiﬁcation of animal
movement patterns using tri-axial accelerometry. Endangered Species
Research, 10, 47–60.

Simon, M., Johnson, M. & Madsen, P.T. (2012) Keeping momentum with a
mouthful of water: behavior and kinematics of humpback whale lunge feeding.
The Journal of Experimental Biology, 215, 3786–3798.

Suzuki, I., Naito, Y., Folkow, L.P., Nobuyuki, M. & Blix, A.B. (2009) Validation
of a device for accurate timing of feeding events in marine animals. Polar Biol-
ogy, 32, 667–671.

Ward, J.A., Lukowicz, P., Troster, G. & Starner, T.E. (2006) Activity recognition
of assembly tasks using body-worn microphones and accelerometers. IEEE
Transactions on Pattern Analysis and Machine Intelligence, 28, 1553–1567.
Watanabe, Y.Y. & Takahashi, A. (2013) Linking animal-borne video to acceler-
ometers reveals prey capture variability. Proceedings of the National Academy
of Sciences of the United States of America, 110, 2199–2204.

Watanabe, Y.Y., Lydersen, C., Fisk, A.T. & Kovacs, K.M. (2012) The slowest
ﬁsh: swim speed and tail-beat frequency of Greenland sharks. Journal of
Experimental Marine Biology and Ecology, 426, 5–11.

Williams, H.J., Shepard, E.L.C., Duriez, O. & Lambertucci, S.A. (2015) Can
accelerometry be used to distinguish between ﬂight types in soaring birds? Ani-
mal Biotelemetry, 3, 1–11.

Wilson, R.P., Shepard, E.L.C. & Liebsch, N. (2008) Prying into the intimate
details of animal lives: use of a daily diary on animals. Endangered Species
Research, 4, 123–137.

Wilson, R.P., White, C.R., Quintana, F., Halsey, L.G., Liebsch, N., Martin,
G.R. & Butler, P.J. (2006) Moving towards acceleration for estimates of activ-
ity-speciﬁc metabolic rate in free-living animals: the case of the cormorant.
Journal of Animal Ecology, 75, 1081–1090.

Ydesen, K.S., Wisniewska, D.M., Hansen, J.D., Beedholm, K., Johnson, M. &
Madsen, P.T. (2014) What a jerk: prey engulfment revealed by high-rate,
super-cranial accelerometry on a harbour seal (Phoca vitulina). The Journal of
Experimental Biology, 217, 2239–2243.

Zucchini, W., MacDonald, I.L. & Langrock, R. (2016) Hidden Markov Models
for Time Series: An Introduction Using R, 2nd edn. Chapman & Hall/CRC,
Boca Raton, FL, USA.

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseReceived 21 June 2016; accepted 30 August 2016
Handling Editor: Robert B. O’Hara

Supporting Information

Additional Supporting Information may be found online in the support-
ing information tab for this article:

Appendix S1. R code for HMMs: Documented R code presented for
application of HMMs in both a supervised and unsupervised learning
approach.

Hidden Markov models for accelerometer data 173

Appendix S2. Comparing supervised learning approaches: A compar-
ison of four supervised learning approaches when there are varying
levels of autocorrelation present in the data.

Appendix S3. Further mathematical details for HMMs. (Pseudo)resid-
ual plots and model checking for both HMM applications presented in
manuscript.

© 2016 The Authors. Methods in Ecology and Evolution © 2016 British Ecological Society, Methods in Ecology and Evolution, 8, 161–173

 2041210x, 2017, 2, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.12657> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
