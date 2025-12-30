Received: 20 October 2024 |  Accepted: 25 April 2025
DOI: 10.1111/1365-2656.70054

R E V I E W

Practical guidelines for validation of supervised machine
learning models in accelerometer- based animal behaviour
classification

Oakleigh Wilson  |   David Schoeman |   Andrew Bradley |   Christofer Clemente

University of the Sunshine Coast, Sippy
Downs, Queensland, Australia

Abstract

Correspondence
Oakleigh Wilson
Email: <oakleigh.wilson05@gmail.com>

1. Supervised  machine  learning  has  been  used  to  detect  fine- scale  animal  behav-

iour from accelerometer data, but a standardised protocol for implementing this

workflow is currently lacking. As the application of machine learning to ecological

Handling Editor: Francesca Cagnacci

problems expands, it is essential to establish technical protocols and validation

standards that align with those in other ‘big data’ fields.

2. Overfitting is a prevalent and often misunderstood challenge in machine learning.

Overfit models overly adapt to the training data to memorise specific instances

rather than to discern the underlying signal. Associated results can indicate high

performance on the training set, yet these models are unlikely to generalise to

new  data.  Overfitting  can  be  detected  through  rigorous  validation  using  inde-

pendent test sets.

3. Our systematic review of 119 studies using accelerometer- based supervised ma-

chine learning to classify animal behaviour reveals that 79% (94 papers) did not

validate  their  models  sufficiently  well  to  robustly  identify  potential  overfitting.

Although  this  does  not  inherently  imply  that  these  models  are  overfit,  the  ab-

sence of independent test sets limits the interpretability of their results.

4. To address these challenges, we provide a theoretical overview of overfitting in

the context of animal accelerometry and propose guidelines for optimal valida-

tion techniques. Our aim is to equip ecologists with the tools necessary to adapt

general machine learning validation theory to the specific requirements of biolog-

ging, facilitating reliable overfitting detection and advancing the field.

K E Y W O R D S
biologging, cross- validation, IMU, movement ecology, overfitting

This is an open access article under the terms of the Creative Commons Attribution License, which permits use, distribution and reproduction in any medium,
provided the original work is properly cited.
© 2025 The Author(s). Journal of Animal Ecology published by John Wiley & Sons Ltd on behalf of British Ecological Society.

1322 |

wileyonlinelibrary.com/journal/jane

J Anim Ecol. 2025;94:1322–1334.

    |  1323

1  |  I NTRO D U C TI O N

1.1  |  The golden age of machine learning in
biologging

omitting semi- supervised and unsupervised models as they typically

do not ‘validate’ in the traditional sense and are not yet as popular as

supervised models (Sur et al., 2023).

ML  is  rapidly  enhancing  the  scope  of  biological  research,  with

an exponential acceleration in ML utilisation across fields (Greener

Biologging,  particularly  animal- borne  accelerometry,  has  enabled

et  al.,  2022;  Jones,  2019).  Despite  this  technology's  increased  ac-

unprecedented insights into the secret lives of wild animals, allowing

cessibility,  it  remains  a  technical  specialisation  that  requires  cor-

biologists  to  track  activity  levels  (Brown  et  al.,  2013),  energy

rect  application  to  avoid  misleading  results  (Greener  et  al.,  2022;

expenditure  (Wilson  et  al.,  2020)  and  even  fine- scale  behaviours

Jones, 2019; Quinn et al., 2021). Biological fields with a history of

(Brown  et  al.,  2013;  Sur  et  al.,  2023)  across  hundreds  of  species.

‘big- data’  computation,  such  as  genomics  and  bioinformatics,  have

Accelerometers  record  sequences  of  instantaneous  acceleration

addressed the need for standardised protocols and reporting guide-

which  can  be  linked  to  corresponding  causal  behaviours.  Machine

lines, with the publication of discipline- specific introductions to ML

learning (ML) models can then be trained to identify similar patterns

(Greener  et  al.,  2022;  Jones,  2019)  and  the  development  of  stan-

in new data from unobserved individuals, for which behaviours are

dardised reporting checklists (Walsh et al., 2021). More traditional

not known (Figure 1; Brown et al., 2013; Sur et al., 2023). ML in this

branches  of  ecology,  however,  have  yet  to  adopt  this  level  of  ML

field can be broadly classified into supervised learning, which relies

training  and  standardisation,  with  ecologists  often  independently

on labelled examples to train the ML model, unsupervised learning,

learning to navigate technical terminology (jargon) and critical design

which  operates  without  labelled  examples,  and  semi- supervised

choices without formal training in ML theory or practice (Campbell

learning  which  combines  elements  of  both  techniques.  Here,

et al., 2013; McClintock et al., 2014). Advocates for the development

we  analyse  validation  methods  for  supervised  models  (Figure  1),

of  user- accessible  ML  protocols  for  behaviour  recognition  abound

F I G U R E   1 Overview of the stages involved in developing a supervised machine learning model for animal accelerometry. In the model
development phase, a machine learning architecture is trained to recognise patterns in labelled training data. The training data are made up
of ‘windows’ (discrete units of time- series data). While deep learning systems autonomously generate features from raw data, traditional
machine learning approaches require feature extraction, where summary statistics (e.g. mean, maximum, minimum) are computed for each
window. These features reduce the high dimensionality of the raw data, facilitating easier classification for smaller models. Each window
is associated with behaviour labels, such as ‘sleeping’, ‘running’ or ‘feeding’. Evaluation comprises two stages. Model hyperparameters are
tuned using a validation set composed of independent windows. The final model's performance is then calculated on a separate test set,
which assesses the model's ability to classify new, unseen data not included during training. This process allows for the assessment of
performance in novel scenarios. Behavioural labels can then be predicted for unseen data using the trained model.

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1324 |

(Ferdinandy et al., 2020; Garde et al., 2022; Yu et al., 2023), but pub-

scenarios that differ from the training set (Chicco, 2017; Goodfellow

lished  efforts  have  focused  mainly  on  hardware  and  sampling—for

et al., 2016).

example, device positioning (Garde et al., 2022; Gleiss et al., 2011;

Overfitting is an inherent risk in all fitting algorithms but is more

Kölzsch et al., 2016), sampling frequency (Hounslow et al., 2019; Yu

common in larger models with more free parameters and especially

et al., 2023) and window length (Putra & Vesilo, 2017)—with focus

problematic  for  high- dimensional,  non- statistically  based  mod-

on theoretical implementation emerging more recently (Ferdinandy

els  such  as  deep  learning  neural  networks  (Hosseini  et  al.,  2020).

et  al.,  2020).  Specifically,  a  unified  method  for  model  verification

Overfitting can be prevented with various techniques, mostly aim-

has yet to be identified within the animal accelerometery research

ing to intentionally limit the model's ability to memorise the training

community.

data (Chicco, 2017). To properly implement these controls, however,

Before progress can be made on developing more powerful mod-

overfitting must first be detected.

els,  it  is  critical  to  determine  how  best  these  should  be  validated.

A tell- tale sign of overfitting is a significant drop in performance

Validation is the process of predicting model performance onto an

between the training set and an independent test set, indicating that

unseen portion of data and assessing how well the model performed.

the model has low generalisability to new datasets. This deteriora-

Validation  is  the  cornerstone  of  model  development  as  it  guides

tion  in  performance,  however,  is  frequently  obscured  by  incorrect

model  optimisation  and  enables  us  to  distinguish  high- performing

validation procedures. Common practices in ML validation that may

models  from  low- performing  models  (Cawley  &  Talbot,  2010).

mask overfitting include (i) a lack of independence of the testing set,

Without robust validation, we do not know whether our model ef-

(ii)  non- representative  selection  of  the  test  set,  (iii)  failure  to  tune

fectively generalises to new data or is hyperspecific to the training

model hyperparameters on a validation set and (iv) optimisation on

data. The importance of rigorous validation in animal accelerometry

an inappropriate performance metric (Greener et al., 2022; Hosseini

has been demonstrated experimentally (e.g. Aulsebrook et al., 2024;

et al., 2020). Our review of validation techniques used in supervised

Ferdinandy  et  al.,  2020),  but  here  we  aim  to  provide  a  theoreti-

ML, as applied to classification of animal behaviour using accelerom-

cal  foundation  for  researchers  to  develop  a  deeper  understand-

eter data, seeks to determine the potential scope of these practices

ing of how to identify and implement rigorous validation in animal

in this field and to suggest guidelines for avoiding common pitfalls

accelerometry.

in future studies.

1.2  |  Leakage and overfitting

2  |  M ATE R I A L S A N D M E TH O DS

Overfitting  is  among  the  most  commonly  encountered,  yet  least-

To  explore  the  extent  of  overfitting  in  the  animal  accelerometer

recognised risks of ML (Chicco, 2017; Yates et al., 2023). Overfitting

literature,  we  conducted  a  systematic  review  under  the  Preferred

occurs when the model's complexity approaches or surpasses that of

Reporting

Items  for  Systematic  reviews  and  Meta- Analyses

the data (Figure 2). This causes the model to overadapt to the context

(PRISMA)  standard  (Page  et  al.,  2021).  The  PRISMA  standard  was

of the training set, essentially ‘memorising’ specific nuances in the

designed  to  aid  the  transparent  reporting  of  systematic  reviews,

training  data  rather  than  learning  to  recognise  more  generalised

covering  motivation,  method  and  results  of  the  systematic  review

patterns  that  apply  beyond  the  training  data  (Chicco,  2017;

in clearly defined stages (Page et al., 2021). No ethical permits were

Goodfellow  et  al.,  2016;  Xu  &  Goodacre,  2018).  Despite  initially

required to undertake this review.

appearing highly accurate—even approaching perfect performance,

We defined eligibility criteria as ‘peer- reviewed primary research

on the training data—overfit models will often perform poorly on the

papers published in 2013 until present that use supervised machine

test set, and struggle when applied to new instances, individuals or

learning  to  identify  specific  behaviours  from  raw,  non- livestock

Under fit

Robust fit

Overfit

F I G U R E   2 Overfitting occurs when a model is too well adjusted to the specific noise of the training data. Such models often perform
deceptively well on the training data, but poorly on new data. More robust models are those that find underlying signals in the data and can
generalise to new instances. Figure adapted from Montesinos López et al. (2022).

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License100% accuracy

70% accuracy

Test data

Single validation

Cross validation

    |  1325

Overfitting to training
data

Independent validation
on new data

F I G U R E   3 Validation on new data not included in the training set enables overfitting to be detected. Left shows a model overfit to the
noise of the training data. When this model is applied to new data, the noise now provides a disadvantage, suggesting the model is overfit
(middle). This validation can be single, with a single division into training, validation and testing data. Alternatively, cross- validation shuffles
and redivides the data multiple times with new portions of the same data assigned to training, validation and testing for each iteration.

animal accelerometer data’. We elected to ignore the analysis of live-

unseen  by  the  model,  as  will  be  the  case  in  real- world  application

stock behaviour as agricultural methods often operate within differ-

(Ferdinandy et al., 2020; Greener et al., 2022; Roberts et al., 2017).

ent constraints to the analyses conducted on wild animals and this

‘Data  leakage’  arises  when  the  evaluation  set  has  not  been  kept

body of literature has mostly developed in isolation to wild animal

independent of the training set, allowing inadvertent incorporation

research. Our search was conducted on 27 September 2024. Initial

of  testing  information  into  the  training  process.  This  leakage

keyword  search  across  three  databases  (Google  Scholar,  PubMed

compromises the validity of the evaluation as the test data are more

and Scopus) yielded 249 unique papers. Papers outside of the search

similar to the training data than unseen data would be. The similarity

criteria—including hardware and software advances, non- ML analy-

between  training  and  test  sets  masks  the  effect  of  overfitting,

sis, insufficient accelerometry application (e.g. research focused on

causing an overestimation of model performance compared to true

other sensors with accelerometry providing minimal support), unsu-

performance on unseen data (Chicco, 2017; Ferdinandy et al., 2020;

pervised methods and research limited to activity intensity or active

Goodfellow et al., 2016). While this general concept is typically well

and inactive states—were excluded, resulting in 119 papers.

understood by researchers, the nuance and specifics of how exactly

Each of these selected papers was reviewed by a single reviewer

such data leakage arises can be misunderstood.

to manually extract key information on validation methods. The in-

Model validation largely falls into categories of singular validation

formation extracted from each of the included papers was as follows:

and k- fold cross- validation (Figure 3). In singular validation, the data

are split once, with the test data held in a ‘vault’ and not accessed

•  Study  system:  Species,  sample  size  and  whether  subjects  were

until the final evaluation of model performance. In cross- validation,

captive or free- roaming;

the data are segmented k times (i.e. k folds) and evaluation is repeated

•  Validation  methods:  Data  split  partitions,  data  split  method  and

for each of these folds (Yates et al., 2023). Alternatively, bootstrap-

validation technique (cross- validation or other);

ping,  a  resampling  method  where  samples  of  data  are  iteratively

•  Window settings: Overlap (as percentage);

extracted to form as the test set and then returned to the sample

•  Tuning: Hyperparameter tuning, feature selection and model se-

pool before the next sample is pulled can be implemented used for

lection (e.g. window length, sampling frequency);

estimating performance variance (Harrell, 2001; Montesinos López

•  Outcomes: Reported performance metrics.

et  al.,  2022).  Bootstrapping  appeared  infrequently  in  the  animal

Information from reviewed literature in supplementary materials

to cross- validation, except that individual samples may appear more

(Dryad  Digital  Repository  DOI:  10.5061/dryad.fxpnvx14d;  Wilson

than once, and others never appear (Montesinos López et al., 2022).

et al., 2025).

For each of these methods, the same risks apply.

accelerometer- based behaviour classification literature but is similar

3  |  D I S C U S S I O N

3.1  |  Non- independence of the test set masks
overfitting to the training data

Typically,  it  is  assumed  that  random  subsampling  will  elim-

inate  data  leakage  (Aulsebrook  et  al.,  2024;  Chicco,  2017),  but

this  assumption  does  not  hold  true  for  time- series  data,  such

as  biologging  data.  Because  biologging  data  are  collected  in  se-

quence,  temporally  adjacent  measurements  are  not  considered

independent,  which  is  especially  the  case  when  a  short  window

(Figure  1)  bisects  a  longer  behavioural  pattern,  turning  a  single

To evaluate a trained ML model's performance, labelled data must

continuous  sequence  into  multiple  similar  segments  (Aulsebrook

be divided into independent subsets for training and evaluation—the

et  al.,  2024;  Ferdinandy  et  al.,  2020 ;  Minasandra  et  al.,  2023;

critical  requirement  being  that  the  model  is  tested  on  data  totally

Roberts  et  al.,  2017 ).  Random  division  into  training  and  testing

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1326 |

Continuous time-series data

Split into discreet windows

Randomly stratified Time stratified

Individually stratified

F I G U R E   4 When continuous time-  series data are split into discreet ‘windows’, consecutive windows will be related to each other. When
then splitting these data into training and testing sets, splitting consecutive windows into different sets can result in overly similar sets
(known as ‘data leakage’) that can mask model overfitting. Randomly stratified windows can result in consecutive windows being separated
to training and testing sets. Time- stratified windows better separate consecutive windows, but retain some relation. Individual stratified sets
have no shared information between the training and test sets, with the lowest risk of data leakage and overfitting.

sets risks these related contiguous windows being split between

but  will  be  less  correlated  than  temporally  close  samples,  making

the  two  datasets,  epitomising  the  phenomenon  of  data  leakage

time  stratification  a  more  appropriate  choice  than  random  subsa-

(Mannini et al., 2013). In this case, the cross- contamination means

mpling when LOIO is not possible (Aulsebrook et al., 2024; Swihart

that  the  training  and  test  sets  are  correlated,  which  means  that

& Slade, 1997).

models overfit to the training data will have an unfair advantage

Of  the  papers  reviewed,  25%  (30  papers)  did  not  report  suffi-

when  assessed  against  the  test  data,  maintaining  high  perfor-

cient  information  for  us  to  determine  the  validation  method  used,

mance  on  the  non- independent  test  set  (Figure  3).  As  such,  ran-

47%  (56  papers)  reported  use  of  cross- validation,  23%  (28  papers)

dom subsampling artificially inflates accuracy estimates compared

used singular validation and 2% (3 papers) made use of both types.

to  true  performance  on  independent,  unseen,  data.  The  use  of

Combining all methods, 18.5% of studies (22 papers) did not report

overlapping  windows  (where  adjacent  windows  sample  from  the

the method used to split out the test data, 47% (56) validated solely

same  underlying  data)  further  exacerbates  non- independence,

on randomly split data, 19% (23) verified with LOIO splits and 10%

leading  to  explicit  data  duplication  between  testing  and  training

(12)  combined  random  sampling  with  an  alternative  independent

sets  (Dehghani  et  al.,  2019;  Mannini  et  al.,  2013).  The  apparent

validation method. Thus, nearly half of the studies drew conclusions

increase in accuracy associated with overlapping windows may be

based on randomly sampled test sets, masking potential overfitting

the  result  of  data  leakage  rather  than  a  true  increase  in  perfor-

to the training set. Trends over time indicate an increase in the pro-

mance (Dehghani et al., 2019).

portion of papers reporting validation methods, from 60% (20 of 30)

One  alternative  to  random  subsampling  is  a  subject- based  or

in 2013–2018 to 87% (74 of 85) in 2019–2024. However, the prac-

leave- one- individual- out  (LOIO)  approach,  where  the  model  is

tice of random data splitting has become more common, being used

trained on the full labelled dataset from some individuals, validated

in  40%  (12)  of  papers  published  from  2013  to  2018,  increasing  to

on the full set of others and tested on the complete set of a single (or

50% (43) in 2019–2024. The majority (56%; 9 of 16) of papers pub-

multiple) other individual(s), thereby ensuring total independence of

lished thus far in 2024 relied on random splitting.

the test set (Ferdinandy et al., 2020; Goodfellow et al., 2016). This

method  tests  the  performance  of  the  model  when  applied  to  new

data and individuals not contained within the training set, and it is

appropriate for situations where the model will ultimately be applied

3.2  |  Model selection and hyperparameter tuning
on the test set masks overfitting to the test set

to  unlabelled  data  from  new  individuals,  as  is  the  ultimate  aim  in

most instances for animal accelerometer research. Because the test

Hyperparameters  are  variables  that  cannot  be  learned  by  the  ML

data  are  independent  from  the  training  data,  overfit  models  incur

model during training but are set prior to training (Yu & Hong, 2020).

no advantage, and reported performance more closely mimics true

Examples include model- specific settings such as the algorithm type,

performance on the unseen data (Figure 4).

learning  rate  or  ‘size’  of  the  model,  as  well  as  preprocessing  deci-

Alternatively,  when  labelled  data  are  available  only  from  the

sions, for example, the window length, degree of overlap between

same individuals as the unlabelled target data and there are too few

windows and which features are used to develop the training data

individuals  for  LOIO  validation,  a  time- stratified  method  could  be

in statistical models. These decisions tailor the model to the specific

used to minimise the impact of overfitting (Aulsebrook et al., 2024).

learning  problems  it  is  presented  with.  Given  the  diversity  in  data

This  involves  splitting  data  chronologically,  often  using  the  initial

quality,  quantity  and  the  complexity  of  classification  tasks  varying

portion of an individual's data for training and the subsequent por-

between  different  datasets,  no  single  ML  model  will  be  appropri-

tions  for  validation  and  testing,  ensuring  independent  sequences

ate  for  all  contexts  (Greener  et  al.,  2022).  Each  ML  architecture  is

appear in each set. Application of this method is common in other

based  on  unique  assumptions,  aligning  most  effectively  with  data

areas of time- series analyses, such as finance and weather predic-

that meet those assumptions, so there is no optimal set of hyperpa-

tion  (Nielsen,  2017).  Because  animal  behaviour  is  deterministic,

rameters, but rather a set of hyperparameters that is most appropri-

temporally  distant  instances  will  not  be  completely  independent,

ate for the problem at hand.

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseSingle validation

Nested cross validation

    |  1327

Cross validation

1

1

2

3

1

2

3

A

B

A

B

A

B

F I G U R E   6 Single validation versus nested cross-  validation. In
single validation, the data are divided once into training, validation
and testing portions. In cross- validation, each portion of data is
iteratively assigned to the training, validation and testing roles. In
nested cross- validation, there is both an outer loop (each portion
of data iteratively assigned to the testing role) as well as an inner
loop (each portion of remaining data iterates between training and
validation). Colours indicate partitions of data that are shuffled in
each cross- validation.

Model selection on
validation data

Independent test
on new data

F I G U R E   5 How tuning of hyperparameters can overfit to the
validation set. Many potential models are generated using the
training data and evaluated on the validation data. Given enough
free parameters and possible iterations, by chance, one of the
models may fit the evaluation data (orange line). Final evaluation
using additional independent test data prevents overestimation of
accuracy due to overfitting to the tuning set.

Hyperparameter  tuning  typically  involves  training  models  with  a

et  al.,  2020; Yates et  al.,  2023). Each time a model is evaluated on a

range of possible parameters and evaluating the performance of each

dataset, the performance provides information about that dataset. As

model variant on an evaluation set to identify the parameters associated

tuning is part of the training (not testing) phase of model development,

with best performance. These potential parameters can be identified

tuning by calculating performance on the test set compromises the in-

using grid search (exhaustively trialling possible combinations), random

dependence of the test set—information about the test set has been

selection (a random selection of possible options), Bayesian estimation

used  to  inform  the  training  process,  which  is  a  form  of  data  leakage

(incrementally  searching  for  global  optima)  or  algorithms  based  on

(Fannjiang et al., 2019a; Quinn et al., 2021; Xu & Goodacre, 2018). To

population  or  evolutionary  dynamics  (Chandrashekar  &  Sahin,  2014;

overcome this limitation, nested cross- validation can be used, where

Yu & Hong, 2020). Hyperparameter tuning typically involves selecting

an inner loop tunes the hyperparameters and an outer loop evaluates

a set of hyperparameters as found by the search algorithm, training a

the  model  (Figure  6;  Cawley  &  Talbot,  2010;  Hosseini  et  al.,  2020;

model according to these parameters and then evaluating model per-

Yates et al., 2023). Although this repeated loop of validation is compu-

formance on a new evaluation set. The hyperparameter combination

tationally expensive, this level of robust validation is necessary to ad-

with the best classification performance is then selected as the final

equately detect overfitting during model tuning and to prevent overfit

model. It is critical, however, that this optimal hyperparameter perfor-

models from incurring unfair advantage. While this method has been

mance is not mistaken for the generalised performance.

found to be overkill in scenarios with few tuneable parameters (Wainer

As the number of free model parameters and iterations among

& Cawley, 2021), the degree to which this may or may not be necessary

these parameters increases, so does the likelihood that one of the

for animal accelerometry remains to be investigated.

possible  model  parameter  sets  will  be  overfit  to  the  evaluation

In the animal accelerometry literature, a review of the prevalence

data.  Analogously  to  ‘p- hacking’—where  running  enough  statisti-

of  hyperparameter  tuning  approaches  (e.g.  costs,  weights,  depth)

cal  tests  eventually  yields  a  seemingly  significant  result—tweaking

found  that  this  stage  of  model  development  was  infrequently  re-

a model until evaluation reports high accuracy makes it difficult to

ported.  Including  feature  selection—selecting  a  subset  of  promising

know  whether  the  model  genuinely  represents  the  signal  or  has

features for use in model development in statistical- based ML models

simply  overfitted  to  the  evaluation  set  by  chance  (Figure  5;  Quinn

(Aulsebrook  et al., 2024;  Demircioğlu, 2021)—and  other  elements  of

et  al.,  2021).  To  distinguish  between  genuine  model  performance

model selection, such as trialling a number of window lengths and sam-

and  overfitting,  a  third  independent  dataset  is  necessary.  This  is

pling frequencies in tuning procedures, 57% (68) papers reported on

known as the ‘validation’ set and is used to fine- tune hyperparame-

model tuning. Of these, 14% (10) assessed performance on a dedicated

ters while safeguarding against overfitting before evaluating on the

validation set and a further 13% (9) performed inner cross- validation

final evaluation (test) data (Cawley & Talbot, 2010).

within the training set; 48% (33) did not implement tuning on any kind

This  validation  set  is  necessary  for  hyperparameter  tuning  pro-

of  validation  set  (predominantly  implementing  default  parameters),

cedures,  whether  in  a  simple  train–validation–test  split  or  within  a

with a further 23% (16) not reporting the number of data portions the

cross- validation  procedure.  While  cross- validation  (which  alternates

labelled set was split into. Use of a validation set, but one that is not

between training and testing splits) is often thought to mitigate over-

independent  from  the  training  and  testing  data  (see  section  above),

fitting, it does not eliminate the risk entirely when used for model se-

risks masking overfitting as well, and the method of dataset division

lection and hyperparameter tuning (Cawley & Talbot, 2010; Hosseini

should also be considered when assessing test set independence. Of

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1328 |

the 68 papers that reported model tuning, 10% (7) validated on data

that could be considered meaningfully independent from the training

(TP + FP))  assesses  the  recognition  of  positive  classes.  While  each
of these metrics is more easily interpreted in the binary context (as

and testing sets (i.e. not randomly split).

one- vs- all  in  the  multi- class  scenario),  macro- averaging  the  scores

The impact of information leakage through overfitting hyperpa-

from each class provides multi- class performance estimates (Kautz

rameters  to  the  test  set  is  often  underappreciated  and  frequently

et  al.,  2017).  These  scores,  however,  are  also  similarly  sensitive  to

overlooked,  even  in  long- established  ML  research  (Cawley  &

class imbalance and, used alone, should be interpreted with caution

Talbot,  2010;  Hosseini  et  al.,  2020).  While  our  review  cannot  de-

(Kautz et al., 2017).

finitively  confirm  overfitting  to  the  test  set,  it  shows  that  current

Compound metrics, such as the F1- Score or Matthews Correlation

validation protocols are insufficient to detect the phenomenon. It is

Coefficient  (MCC),  are  said  to  be  more  robust  to  class  imbalance

nevertheless  reasonable  to  infer  that  overfitting  likely  occurred  in

because they draw from multiple elements of the confusion matrix

much of the animal accelerometry literature, as has been common in

(Chicco,  2017).  F1- Score  balances  precision  and  recall  by  calculat-

other fields during early ML adoption.

ing  their  harmonic  mean,  providing  a  single  metric  that  accounts

3.3  |  Inappropriate performance metrics prevent
meaningful model optimisation

for  both  false  positives  and  false  negatives  (2 × Precision × Recall/
(Precision + Recall)). MCC improves upon this balance by further in-
corporating  all  four  categories  (TP,  TN,  FP,  FN)  to  provide  a  more

holistic  performance  overview  ((TP × TN − FP × FN)/sqrt((TP + FP)
(TP + FN)(TN + FP)(TN + FN))).

The  performance  of  supervised  classification  models  is  typically

All above- mentioned metrics rely on the selection of a specific

evaluated  using  a  confusion  matrix,  where  known  true  categories

threshold, which determines the class assigned to a prediction based

are  organised  as  rows  and  predicted  categories  as  columns.  Each

on  the  model's  confidence  score.  In  contrast,  rank- based  metrics

cell in the matrix contains counts of observations, with the diagonal

evaluate  model  performance  across  a  range  of  thresholds  (Ferri

indicating correct classifications. While confusion matrices provide

et  al.,  2009).  Two  common  rank- based  metrics  are  the  area  under

comprehensive insights into model performance, they can become

the receiver operating characteristic curve (AUC- ROC) and the area

challenging  to  interpret  in  multi- class  scenarios.  Consequently,

under the precision- recall curve (PR- AUC) (Cook & Ramadas, 2020).

performance  evaluation  often  relies  on  a  more  manageable  set  of

AUC- ROC measures the trade- off between sensitivity and specific-

metrics. The appropriate choice of these test metrics is critical for

ity at various thresholds, providing insights into the model's ability

model  validation,  as  it  is  through  these  metrics  the  performance

to  distinguish  between  classes.  PR- AUC  focuses  on  the  trade- off

of  the  model  can  be  understood  and  the  most  appropriate  model

between precision and recall, highlighting the model's performance

optimised  for  (Ferri  et  al.,  2009).  There  is  no  universal  ‘best’

on the positive class, which is particularly helpful when the positive

metric,  but  rather  many  possible  metrics,  each  of  which  reports

class is in the minority (Cook & Ramadas, 2020). While these meth-

different  elements  of  performance  from  the  confusion  matrix

ods are calculated for binary classes, they can be generalised to the

(Ferri  et  al.,  2009;  Lovell  et  al.,  2023).  Selecting  the  appropriate

multi- class by macro- averaging one- vs- all scores for each class.

set  involves  careful  consideration  of  the  goals  of  the  optimisation

In our review, we found that 74% (88) of papers reported model

balanced against the ‘blind spots’ of the metrics.

accuracy,  with  26%  (31)  citing  accuracy  as  the  sole  performance

Accuracy is the most commonly referenced performance metric

metric. 40% (48) of the studies reported an accuracy exceeding 90%,

in classification tasks. Defined as the proportion of correct predic-

while  70%  (83)  reported  accuracy  above  80%.  The  next- most  fre-

tions  made  by  a  model,  this  metric  provides  valuable  insights  into

quently reported metrics were recall (54 papers) and precision (52),

model performance, but it is often insufficient, particularly for im-

followed  by  specificity  and  F1- score  (both  reported  in  25  papers).

balanced datasets (Ferri et al., 2009; Sur et al., 2023). In situations

Other metrics, including AUC, PR- curve, MCC and Kappa (accuracy

characterised by class imbalance, accuracy can be inflated by models

accounting for chance baseline; Ferri et al., 2009) each individually

that predominantly predict the majority class (e.g. in a dataset with

appeared infrequently. It is not yet clear which of these metrics or

a high proportion of sleeping data, if 80% of instances are ‘sleeping’,

combinations  of  metrics  are  the  most  appropriate  for  validation  in

a model that predicts sleeping for all instances will achieve an accu-

animal accelerometry, and until a dedicated study is undertaken, it

racy of 80%; Goodfellow et al., 2016). Relying solely on accuracy can

remains up to the author to justify the metric/s they present. Such a

obscure a model's true performance, so the inclusion of additional

dedicated study, either a simulation study with case- study data or a

performance metrics is recommended.

review of metrics implemented in other fields and their advantages

Recall measures the proportion of correctly identified positives

and trade- offs, may be sufficient to solve this challenge. However, as

(true  positives,  TP)  out  of  all  actual  positives  (TP + false  negatives,
FN),  providing  insight  into  the  model's  effectiveness  in  capturing

currently, no definitive guidelines can be given, present best practice

would  be  to  consider  a  range  of  metrics  in  context  of  the  study's

positive instances. Specificity measures the proportion of true neg-

goals  as  well  as  reporting  the  upper  and  lower  bounds  of  perfor-

atives  (TN)  out  of  all  TN + false  positives  (FP),  reflecting  the  mod-
el's  ability  to  accurately  identify  negative  classes.  Precision  (TP/

mance  between  cross- validation  folds  (i.e.  the  uncertainty)  where

cross- validation has been performed (Lovell et al., 2023).

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License    |  1329

3.4  |  Unnatural test sets optimise for
unnatural models

et  al.,  2013)—other  research  suggests  that  captive  surrogacy  is

ineffective,  in  some  cases,  even  when  the  surrogate  is  from  the

same  species  (e.g.  Pagano  et  al.,  2017).  In  these  instances,  data

The  essential  goal  of  machine  learning  is  to  generalise  beyond  the

from captive individuals may not sufficiently represent their free-

training  set  to  new,  unseen  data  (Domingos,  2012).  It  is  possible

roaming  counterparts  due  to  constraints  of  enclosures  or  ethi-

to  report  the  performance  of  ML  models  against  the  test  set,  but

cal  considerations  leading  to  unnatural  movements  (Dickinson

not how appropriate the test set was for the problem. To general-

et  al.,  2020 ;  Pagano  et  al.,  2017).  Similarly,  human  biologging

ise well, the test data must, as much as possible, mimic the unseen

research  consistently  reports  a  20–30%  decrease  in  model  per-

target data in terms of behavioural stratification, environment and

formance when laboratory- trained models are deployed on free-

types of individuals (Dickinson et al., 2020; Ferdinandy et al., 2020;

roaming people (Farrahi et al., 2019). While not ‘overfitting’ in the

Yu  et  al.,  2022).  It  is  the  responsibility  of  the  researcher  to  deter-

traditional sense, this limitation nevertheless results in an optimis-

mine how similar the test set is to the real data and decide whether

tic performance estimate, potentially not generalising to the true

the  calculated  performance  metrics  are  generalisable  to  the  final

performance in the wild (sample of papers compared in Table 1).

application.

Similarly,  when  only  a  limited  set  of  behaviours  are  collected,  or

‘Gold- standard’  validation  would  be  to  collect  labelled  training

only  clean  examples  included  (i.e.  ‘other’  classes  removed  and

data from multiple individuals of similar status (i.e. environment, size,

transitions between behaviours eliminated), a highly tailored and

behaviours) to the ultimate unseen research individuals and validate

unnaturally simplistic dataset is developed (Resheff et  al.,  2024).

the  model  with  appropriately  partitioned  LOIO  methods  on  these

Despite high accuracy on this curated dataset, the model's prac-

labelled  individuals.  Animal  research,  however,  often  poses  logis-

tical  value  diminishes  when  this  fails  to  represent  the  true  be-

tical, practical and ethical challenges that can limit data collection,

havioural range (Resheff et al., 2024).

placing  the  ‘gold  standard’  beyond  reach  (Lenth,  2001;  Patterson

Although the accuracy of models could not be assessed for free-

et al., 2019).

roaming  individuals  due  to  the  absence  of  ground- truthed  data,

Implementing  hold- out  test  data  for  validation  ensures  final

models trained on captive specimens often failed to reliably detect

evaluation is on truly unseen data, providing a fair estimate of true

free- roaming behaviours. To expand the use of accelerometry in wild

model performance, provided that the test data are drawn from the

populations, the development of effective methods for transferring

same distribution as the training data (Hastie et al., 2010). In cases

captive- trained models to free- roaming individuals is a priority.

of limited sample size, implementing a hold- out test set containing

only a single individual can be risky, as this single individual may in-

troduce biases, or exhibit individual idiosyncrasies to the degree that

3.5  |  Uncertain reporting obscures methods

it  may  render  the  individual  unrepresentative  of  the  population  in

general (Chimienti, 2022). Where there are sufficient data to provide

A limitation of this systematic review was the inability to automate

a test set composed of multiple individuals, hold- out data are pref-

key  data  extraction  due  to  inconsistent  reporting  across  stud-

erable, but where such data are insufficient, LOIO cross- validation

ies,  a  well- recognised  and  long- standing  issue  in  this  field  (Brown

can mitigate risks of biased test individuals. By iteratively calculating

et al., 2013; Campbell et al., 2013). For instance, the well- established

cross- validated  test  performance  on  each  of  the  individuals,  LOIO

ML term ‘windows’ was inconsistently referred to as segments, in-

cross- validation provides an average performance to account for the

crements, periods or epochs—the latter having an alternative specific

bias of any one individual, as well as an additional metric of ‘uncer-

meaning in ML as ‘data presentations’ for training neural networks

tainty’ (how the performance changes among individuals) which can

(Goodfellow et al., 2016). The overlap between windows was often

be used to choose between models, balancing both average perfor-

vaguely  described with terms like ‘rolling’, ‘sliding’  or ‘moving’, and

mance and the performance range. The final model, built on the data

even  the  term  ‘cross- validation’  was  sometimes  used  ambiguously,

from all individuals, is assumed to have performance approximately

making it unclear whether it referred to a single or multiple valida-

equal  to  the  average  performance  from  each  of  the  folds  (Hastie

tion folds. This inconsistency also hampered the qualitative assess-

et al., 2010).

ment of missing information, making it unclear whether omissions,

Capturing the full behavioural range of a species is often also

such as the absence of hyperparameter tuning details, were inten-

impractical if not impossible (Campbell et al., 2013). Free- roaming

tional null values or simply incompletely reported.

animals  often  move  beyond  the  reach  of  researchers'  observa-

We informally observed that, compared to details on the study

tion,  while  captive  animals  may  exhibit  atypical  behaviours  or

system (e.g. species, sample size and data collection methods), vali-

only  a  narrow  range  of  their  natural  repertoire,  meaning  not  all

dation methods were reported less thoroughly. For instance, 18% of

behaviours  that  occur  in  the  unlabelled,  unseen  data  are  cap-

papers (22) lacked sufficient information to determine the method of

tured in the labelled set (Chimienti, 2022; Dickinson et al., 2020;

data splitting. In 38% (45) of papers, the portions of data used were

Ladds et al., 2016). While some literature recommends the use of

unspecified, making it unclear whether a validation set was included.

captive  surrogates  of  alternate  species—both  close  (Ferdinandy

In  25%  of  papers  (30),  it  was  not  possible  to  determine  whether

et  al.,  2020)  and  distant  phylogenetic  relations

(Campbell

cross- validation or single validation had been used.

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1330 |

TA B L E   1 Deploying captive-  trained models on free- roaming individuals. Despite achieving high accuracy on the captive set, the ML
model can display significant limitations when applied to the target free- roaming individuals, often being unable to detect realistic free-
roaming behaviours.

Reference

Species

Model

Captive accuracy

Free- roaming performance

Fannjiang et al. (2019b)

Jellyfish

Discriminant Analysis

0.99

Rast et al. (2020)

Fox

Random Forest

0.955

Support vector machine

0.8817

Neural network

0.9433

Pagano et al. (2017)

Polar bear

Random forest

Not assessed

Clarke et al. (2021)

Pelagic fish

Random forest

0.94

Harvey- Carroll
et al. (2024)

Pangolin

Random forest

0.85

Dunford et al. (2024)

Cat

Random forest

F = 0.96 (accuracy not
reported)

Unable to detect wild behaviours when
trained on only data from captive
individuals. Addition of in situ free-
roaming data improved classification
performance

Unable to detect wild behaviours using
Random Forest or Support Vector
Machine models (all samples were
classed as ‘grooming’). Able to detect
multiple behaviours only using the neural
network

The captive- trained model was able
to detect stationary behaviours only.
Only wild- trained models were able to
distinguish energetic behaviours

‘Swimming’ was not detected in 3
of 5 free- roaming individuals (likely
due to large fish size increasing signal
magnitude)

Observed to generate reasonable free-
roaming behavioural budgets

Despite achieving high test ‘accuracy’,
some models failed to identify grooming
and feeding in free- roaming cats. Other
models were able to identify these
behaviours

The  implementation  of  a  standardised  reporting  checklist  for

should  be  considered.  For  time- series  data,  random  subsampling

animal accelerometry ML studies would greatly enhance reproduc-

within  individuals  should  be  avoided,  and  LOIO  or  chronological

ibility and compatibility in this field. The Data Optimisation Model

splits  should  be  used  instead.  Exemplary  discussion  of  testing  set

Evaluation (DOME, Walsh et al., 2021) guideline is a field- agnostic,

independence is demonstrated (Aulsebrook et al., 2024; Ferdinandy

generalised,  biology- accessible  checklist  suggested  for  reporting

et al., 2020).

supervised  ML  analysis.  While  not  intended  to  be  exhaustive,  ad-

hering to this checklist could assist future biologging studies to en-

2. Hyperparameter  tuning  and  model  selection  on  the  test  set

sure  transparency  and  reproducibility,  facilitating  robust  scientific

masks  overfitting  to  the  test  set.

advancements.

Tuning  hyperparameters  is  an  important  stage  of  fine- tuning

models to specific traits in the dataset. This process must be com-

3.6  |  Best practices for detecting overfitting

pleted as part of the training process prior to evaluation of the final

model  on  the  test  set.  With  sufficient  data,  this  will  require  three

In light of these common challenges with machine learning validation,

separate and independent subsets of data and, for cross- validation

the following concepts should be considered to ensure best practice

workflows, a nested cross- validation (with an inner training/valida-

for detecting model overfitting:

tion cross- validation and then an outer test cross- validation) may be

implemented. An exemplary discussion of the importance of hyper-

1. Non- independence  of  the  testing  set  masks  overfitting  to  the

parameter tuning is found in Hosseini et al. (2020).

training  data.

3. Inappropriate  performance  metrics  prevent  meaningful  model

Labelled data should be split such that the testing data are inde-

optimisation.

pendent from the training data. With a sufficient sample size, data

can be split into three independent subsets (training, validating and

Performance  metrics  are  critical  for  guiding  the  optimisation

testing), or, when there are insufficient data, nested cross- validation

and  selection  of  models.  Selecting  a  limited  set  of  performance

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License    |  1331

metrics from a complete confusion matrix is necessarily reductive

4  |  CO N C LU S I O N

and each metric presents its own limitations and biases. Particularly

in the context of class imbalance, be wary of accuracy as a stand-

Combining the 18 papers that used independent training and testing

alone metric and consider multiple metrics and compound metrics

sets without model tuning and the seven papers that tuned models

in  evaluations.  When  using  cross- validation,  report  the  full  range

using  independent  validation  sets,  this  review  found  that  only  25

of performance variation across validation folds. Exemplary discus-

papers (21%) in the reviewed animal accelerometer- based behaviour

sion of performance metrics can be found (Ferri et al., 2009).

classification  literature  followed  ‘gold  standard’  ML  validation

4. Unnatural  test  sets  optimise  for  unnatural  models.

validate their models in a way that could reveal overfitting. Despite

methods.  The  remaining  79%  of  the  literature  (94  papers)  did  not

70% of the studies reporting model accuracy above 80%, our review

Ensure collected data capture real- world variability by including

suggests  that  inconsistent  validation  practices  may  be  concealing

a broad spectrum of individuals, behaviours and transitions, reflect-

overfitting in many, if not most, of these studies.

ing real- world model application as much as possible. Model predic-

Literature  review  alone  cannot  determine  the  actual  impact  of

tions are directly applicable only to the subpopulation, behaviours

this  potential  overfitting,  as  suboptimal  validation  does  not  inher-

and  context  contained  within  the  labelled  data.  Extrapolating  be-

ently  mean  that  a  model  is  overfit  or  that  performance  has  been

yond these constraints, or use of surrogates, should be carefully jus-

overstated. However, without gold standard validation, it is impossi-

tified, and results caveated and interpreted with caution. Exemplary

ble to determine whether overfitting or accuracy inflation occurred,

discussion  of  limits  to  generalisation  can  be  found  (Dickinson

leaving the results uncertain. In these situations, both the capacity

et al., 2021; Ladds et al., 2016).

of  a  model  to  generalise  and  the  ecological  conclusions  must  be

treated with caution. An example of the potential effect of masked

5. Adherence  to  the  DOME  reporting  guidelines  ensures  repro-

overfitting is available in a re- evaluation of past work by the pres-

ducible  ML.

ent  authors  using  Supervised  Self- Organising  Maps  to  classify  be-

haviours in various species (Annett et al., 2024; Galea et al., 2021;

Standardising  reporting  of  methods  across  the  literature  by

Gaschk  et  al.,  2023).  These  studies  used  random  data  splitting  for

use of the DOME guidelines (Walsh et al., 2021) for supervised ML

training and testing data, did not implement a validation set for hy-

would  ensure  that  future  research  can  more  easily  learn  from  re-

perparameter  tuning  and  prioritised  accuracy  in  imbalanced  class

search  in  the  past.  For  validating  accelerometer- based  animal  be-

scenarios.  Although  each  paper  reported  99%  classification  accu-

haviour  classification  models,  specifically,  the  following  should  be

racy, our re- analysis accounting for the aforementioned limitations

clearly and explicitly stated:

demonstrated that generalised model performance on an indepen-

dent  test  set  was  actually  only  around  50%,  indicating  substantial

•  Method of splitting (random, chronological, stratified, by individ-

overfitting in the original papers. While this is only one example of

ual, other—with justification);

the impact masked overfitting can have on the predictive power of

•  Portions of splitting (training/validation/testing, with proportions);

behaviour  classification  models,  it  is  possible  that  a  similar  impact

•  Method  of  validation

(single,  cross- validation,

inner  cross-

could be hidden across the literature.

validation with hold- out test set, other);

Overfitting is a persistent challenge across most ML implemen-

•  Performance  metrics  (a  range  of  metrics—with  justification—as

tations to which ecology is no exception (Ginzburg & Jensen, 2004;

well as performance range across folds);

Roberts  et  al.,  2017).  For  instance,  camera  trap  species  identifica-

6. Sanity  checks  and  control  conditions  in  the  ML  workflow  help

location  and  time  of  day  can  become  overfitted  to  specific  image

tion  models  trained  and  tested  on  images  from  the  same  camera

to  avoid  errors.

backgrounds and must be tested across a range of contexts before

deployment (Norouzzadeh et al., 2021). Similarly, acoustic detectors

Similar to the use of ecological baselines or null conditions in other eco-

can achieve high performance when trained and tested on samples

logical models, an ML control could train and evaluate the model on

from the same audio file but may fail to generalise beyond these sce-

a randomised dataset, where poor performance would be expected.

narios; their true performance must be validated across a range of

This  would  confirm  that  the  model  is  responding  to  real  conditions

independent recordings (Kershenbaum et al., 2025). Even non- ML-

rather  than  erroneous  code  or  leakage.  Critically,  we  encourage  this

based plant biomass estimation models have been shown to produce

developing  research  field  to  see  ML  as  more  than  a  tool,  but  an  ex-

overly optimistic predictions when validated on spatially correlated

periment in its own right. ML can be an incredibly powerful tool for

test data (Ploton et al., 2020; Yu et al., 2021). Thus, the guidelines

pattern recognition, but the onus is still on the ecologist to mistrust the

presented  in  this  paper,  while  developed  in  the  context  of  animal

results until rigour is proven, critically evaluating whether the reported

accelerometer- based behaviour classification, are relevant to the de-

results—particularly when performance is reported to be very high—

velopment of all predictive models across ecology, particularly those

are generalisable and trustworthy.

implementing time series and spatially correlated analyses.

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1332 |

Overfitting detection and prevention is a large, complex and rap-

idly evolving field, with best practices being continually refined. As

ecologists increasingly adopt ML into applied research, our protocols

and implementations similarly advance. Although a ‘one- size- fits- all’

validation method suitable for all ML applications is not possible, the

fundamental principles outlined in this paper are broadly applicable

across ecology. Ecologists considering implementing ML—or indeed

any  predictive  model—in  their  research  should  carefully  consider

and account for how biased validation practices may limit the gener-

alisability of their model results and remain vigilant to the possibility

of model overfitting.

AU T H O R  C O N T R I B U T I O N S

Oakleigh  Wilson  conceived  the  idea  for  the  paper,  collected

and  analysed  the  review  results  and  wrote  the  first  draft.  David

Schoeman,  Andrew  Bradley  and  Christofer  Clemente  contributed

ideas throughout the project and provided multiple rounds of review

for the manuscript. All authors gave final approval for submission.

AC K N OW L E D G E M E N T S

We  thank  J.  Eadie  for  additional  proof- reading.  Open  access

publishing  facilitated  by  University  of  the  Sunshine  Coast,  as  part

of the Wiley - University of the Sunshine Coast agreement via the

Council of Australian University Librarians.

C O N FL I C T O F I N T E R E S T S TAT E M E N T

The authors have no conflicts of interest to declare.

DATA  AVA I L A B I L I T Y S TAT E M E N T

Data  available  from  the  Dryad  Digital  Repository:  https:// doi. org/

10. 5061/ dryad. fxpnv x14d (Wilson et al., 2025).

S TAT E M E N T O N I N C LU S I O N

Our study was a global systematic review and was based on a meta-

analysis of secondary data rather than primary data. As such, there

was  no  local  data  collection.  Data  were  collected  systematically

without geographical considerations.

O R C I D

Oakleigh Wilson

 <https://orcid.org/0009-0004-9082-3664>

Christofer Clemente

 <https://orcid.org/0000-0001-8174-3890>

R E F E R E N C E S

Annett,  J.,  Gaschk,  J.,  &  Clemente,  C.  (2024).  Comparative  analysis  of
behavioural  repertoires  for  Mahogany  glider  and  Brushtail  pos-
sum using accelerometer loggers and machine learning algorithms.
Journal  of  Zoology,  322(1),  24–34.  https:// doi. org/ 10. 1111/ jzo.
13125

Aulsebrook,  A.  E.,  Jacques- Hamilton,  R.,  &  Kempenaers,  B.  (2024).
Quantifying  mating  behaviour  using  accelerometry  and  ma-
chine  learning:  Challenges  and  opportunities.  Animal  Behaviour,
207(January), 55–76. https:// doi. org/ 10. 1016/j. anbeh av. 2023. 10. 013
Brown, D. D., Kays, R., Wikelski, M., Wilson, R., & Klimley, A. P. (2013).
Observing the unwatchable through acceleration logging of animal

behavior.  Animal  Biotelemetry,  1,  1–16.  https:// doi. org/ 10. 1186/
2050-  3385-  1-  20

Campbell, H. A., Gao, L., Bidder, O. R., Hunter, J., & Franklin, C. E. (2013).
Creating a behavioural classification module for acceleration data:
Using  a  captive  surrogate  for  difficult  to  observe  species.  Journal
of  Experimental  Biology,  216(24),  4501–4506.  https:// doi. org/ 10.
1242/ jeb. 089805

Cawley, G. C., & Talbot, N. L. C. (2010). On over- fitting in model selec-
tion and subsequent selection bias in performance evaluation. The
Journal of Machine Learning Research, 11, 2079–2107.

Chandrashekar, G., & Sahin, F. (2014). A survey on feature selection meth-
ods. Computers and Electrical Engineering, 40(1), 16–28. https:// doi.
org/ 10. 1016/j. compe leceng. 2013. 11. 024

Chicco, D. (2017). Ten quick tips for machine learning in computational
biology. Methods in Ecology and Evolution, 10(6), 802–814. https://
doi. org/ 10. 1186/ s1304 0-  017-  0155-  3

Chimienti, M. (2022). The role of individual variability on the predictive
performance of machine learning applied to large bio- logging data-
sets. Scientific Reports, 12(1), 19737. https:// doi. org/ 10. 1038/ s4159
8-  022-  22258 -  1

Clarke, T. M., Whitmarsh, S. K., Hounslow, J. L., Gleiss, A. C., Payne, N.
L.,  &  Huveneers,  C.  (2021).  Using  tri- axial  accelerometer  loggers
to  identify  spawning  behaviours  of  large  pelagic  fish.  Movement
Ecology, 9(1), 26. https:// doi. org/ 10. 1186/ s4046 2-  021-  00248 -  8

Cook, J., & Ramadas, V. (2020). When to consult precision- recall curves.
The  Stata  Journal,  20(1),  131–148.  https:// doi. org/ 10. 1177/ 15368
67X20 909693

Dehghani, A., Sarbishei, O., Glatard, T., & Shihab, E. (2019). A quantita-
tive  comparison  of  overlapping  and  non- overlapping  sliding  win-
dows for human activity recognition using inertial sensors. Sensors,
19(22), 5026. https:// doi. org/ 10. 3390/ s1922 5026

Demircioğlu,  A.  (2021).  Measuring  the  bias  of  incorrect  application  of
feature selection when using cross- validation in radiomics. Insights
Into
Imaging,  12(1),  172.  https:// doi. org/ 10. 1186/ s1324 4-  021-
01115 -  1

Dickinson, E. R., Stephens, P. A., Marks, N. J., Wilson, R. P., & Scantlebury,
D. M. (2020). Best practice for collar deployment of tri- axial accel-
erometers on a terrestrial quadruped to provide accurate measure-
ment of body acceleration. Animal Biotelemetry, 8, 1–8. https:// doi.
org/ 10. 1186/ s4031 7-  020-  00198 -  9

Dickinson, E. R., Twining, J. P., Wilson, R., Stephens, P. A., Westander, J.,
Marks, N., & Scantlebury, D. M. (2021). Limitations of using surro-
gates  for  behaviour  classification  of  accelerometer  data:  Refining
methods using random forest models in caprids. Movement Ecology,
9(1), 28. https:// doi. org/ 10. 1186/ s4046 2-  021-  00265 -  7

Domingos, P. (2012). A few useful things to know about machine learn-
ing. Communications of the ACM, 55(10), 78–87. https:// doi. org/ 10.
1145/ 23477 36. 2347755

Dunford, C. E., Marks, N. J., Wilson, R. P., & Scantlebury, D. M. (2024).
Identifying animal behaviours from accelerometers: Improving pre-
dictive  accuracy  of  machine  learning  by  refining  the  variables  se-
lected, data frequency, and sample duration. Ecology and Evolution,
14(5), e11380. https:// doi. org/ 10. 1002/ ece3. 11380

Fannjiang, C., Mooney, T. A., Cones, S., Mann, D., Shorter, K. A., & Katija,
K. (2019a). Augmenting biologging with supervised machine learn-
ing  to  study  in  situ  behavior  of  the  medusa  Chrysaora  fuscescens.
Journal of Experimental Biology, 222(16), jeb207654. https:// doi. org/
10. 1242/ jeb. 207654

Fannjiang, C., Mooney, T. A., Cones, S., Mann, D., Shorter, K. A., & Katija,
K. (2019b). Augmenting biologging with supervised machine learn-
ing  to  study  in  situ  behavior  of  the  medusa  Chrysaora  fuscescens.
Movement Ecology, 9(1), 28. https:// doi. org/ 10. 1242/ jeb. 207654

Farrahi, V., Niemelä, M., Kangas, M., Korpelainen, R., & Jämsä, T. (2019).
Calibration  and  validation  of  accelerometer- based  activity  moni-
tors: A systematic review of machine- learning approaches. Gait &

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicensePosture,  68,  285–299.  https:// doi. org/ 10. 1016/j. gaitp ost. 2018. 12.
003

Ferdinandy, B., Gerencsér, L., Corrieri, L., Perez, P., Újváry, D., Csizmadia,
G.,  &  Miklósi,  Á.  (2020).  Challenges  of  machine  learning  model
validation  using  correlated  behaviour  data:  Evaluation  of  cross-
validation  strategies  and  accuracy  measures.  PLoS  One,  17(7),
e0236092. https:// doi. org/ 10. 1371/ journ al. pone. 0236092

Ferri,  C.,  Hernández- Orallo,  J.,  &  Modroiu,  R.  (2009).  An  experimental
comparison  of  performance  measures  for  classification.  Pattern
Recognition Letters, 30(1), 27–38. https:// doi. org/ 10. 1016/j. patrec.
2008. 08. 010

Galea, N., Murphy, F., Gaschk, J. L., Schoeman, D. S., & Clemente, C. J.
(2021).  Quantifying  finer- scale  behaviours  using  self- organising
maps  (SOMs)  to  link  accelerometery  signatures  with  behavioural
patterns in free- roaming terrestrial animals. Scientific Reports, 11(1),
13566. https:// doi. org/ 10. 1038/ s4159 8-  021-  92896 -  4

Garde,  B.,  Wilson,  R.  P.,  Fell,  A.,  Cole,  N.,  Tatayah,  V.,  Holton,  M.  D.,
Rose, K. A. R., Metcalfe, R. S., Robotka, H., Wikelski, M., Tremblay,
F., Whelan, S., Elliott, K. H., & Shepard, E. L. C. (2022). Ecological
inference using data from accelerometers needs careful protocols.
Methods  in  Ecology  and  Evolution,  13(4),  813–825.  https:// doi. org/
10. 1111/ 2041-  210X. 13804

Gaschk,  J.  L.,  Del  Simone,  K.,  Wilson,  R.  S.,  &  Clemente,  C.  J.  (2023).
Resting  disparity  in  quoll  semelparity:  Examining  the  sex- linked
behaviours  of  wild  roaming  northern  quolls  (Dasyurus  hallucatus)
during breeding season. Royal Society Open Science, 10(2), 221180.
https:// doi. org/ 10. 1098/ rsos. 221180

Ginzburg,  L.  R.,  &  Jensen,  C.  X.  J.  (2004).  Rules  of  thumb  for  judging
ecological  theories.  Trends  in  Ecology  &  Evolution,  19(3),  121–126.
https:// doi. org/ 10. 1016/j. tree. 2003. 11. 004

Gleiss,  A.  C.,  Wilson,  R.  P.,  &  Shepard,  E.  L.  C.  (2011).  Making  overall
dynamic body acceleration work: On the theory of acceleration as
a proxy for energy expenditure. Methods in Ecology and Evolution,
2(1), 23–33. https:// doi. org/ 10. 1111/j. 2041-  210X. 2010. 00057. x

Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning (Vol. 1).

MIT Press.

Greener, J. G., Kandathil, S. M., Moffat, L., & Jones, D. T. (2022). A guide to
machine learning for biologists. Nature Reviews Molecular Cell Biology,
23(1), 40–55. https:// doi. org/ 10. 1038/ s4158 0-  021-  00407 -  0
Harrell, F. E. (2001). Regression modeling strategies: With applications to lin-
ear models, logistic and ordinal regression, and survival analysis|Spring-
erLink (Vol. 608, Springer Series in Statistics). Springer. https:// link.
sprin ger. com/ book/ 10. 1007/ 978-  3-  319-  19425 -  7

Harvey- Carroll,  J.,  Carroll,  D.,  Trivella,  C.- M.,  &  Connelly,  E.  (2024).
Classification  of  African  ground  pangolin  behaviour  based  on  ac-
celerometer  readouts:  Validation  of  bio- logging  methods.  Animal
Biotelemetry, 12(1), 22. https:// doi. org/ 10. 1186/ s4031 7-  024-  00377 -  y
Hastie,  T.,  Tibshirani,  R.,  &  Friedman,  J.  (2010).  The elements of statisti-
cal learning: Data mining, inference, and prediction (Vol. 2). Springer.
https:// link. sprin ger. com/ book/ 10. 1007/ 978-  0-  387-  21606 -  5
Hosseini,  M.,  Powell,  M.,  Collins,  J.,  Callahan- Flintoft,  C.,  Jones,  W.,
Bowman,  H.,  &  Wyble,  B.  (2020).  I  tried  a  bunch  of  things:  The
dangers  of  unexpected  overfitting  in  classification  of  brain  data.
Neuroscience  &  Biobehavioral  Reviews,  119(December),  456–467.
https:// doi. org/ 10. 1016/j. neubi orev. 2020. 09. 036

Hounslow,  J.  L.,  Brewster,  L.  R.,  Lear,  K.  O.,  Guttridge,  T.  L.,  Daly,  R.,
Whitney,  N.  M.,  &  Gleiss,  A.  C.  (2019).  Assessing  the  effects  of
sampling frequency on behavioural classification of accelerometer
data. Journal of Experimental Marine Biology and Ecology, 512(March),
22–30. https:// doi. org/ 10. 1016/j. jembe. 2018. 12. 003

Jones, D. T. (2019). Setting the standards for machine learning in biology.
Nature Reviews Molecular Cell Biology, 20(11), 659–660. https:// doi.
org/ 10. 1038/ s4158 0-  019-  0176-  5

Kautz, T., Eskofier, B. M., & Pasluosta, C. F. (2017). Generic performance
measure for multiclass- classifiers. Pattern Recognition, 68(August),
111–125. https:// doi. org/ 10. 1016/j. patcog. 2017. 03. 008

    |  1333

Kershenbaum, A., Akçay, Ç., Babu- Saheer, L., Barnhill, A., Best, P., Cauzinille,
J.,  Clink,  D.,  Dassow,  A.,  Dufourq,  E.,  Growcott,  J.,  Markham,  A.,
Marti- Domken, B., Marxer, R., Muir, J., Reynolds, S., Root- Gutteridge,
H.,  Sadhukhan,  S.,  Schindler,  L.,  Smith,  B.  R.,  …  Dunn,  J.  C.  (2025).
Automatic detection for bioacoustic research: A practical guide from
and for biologists and computer scientists. Biological Reviews, 100(2),
620–646. https:// doi. org/ 10. 1111/ brv. 13155

Kölzsch,  A.,  Neefjes,  M.,  Barkway,  J.,  Müskens,  G.  J.  D.  M.,  van
Langevelde,  F.,  de  Boer,  W.  F.,  Prins,  H.  H.  T.,  Cresswell,  B.  H.,  &
Nolet, B. A. (2016). Neckband or backpack? Differences in tag de-
sign  and  their  effects  on  GPS/accelerometer  tracking  results  in
large Waterbirds. Animal Biotelemetry, 4(1), 13. https:// doi. org/ 10.
1186/ s4031 7-  016-  0104-  9

Ladds, M. A., Thompson, A. P., Slip, D. J., Hocking, D. P., & Harcourt, R. G.
(2016). Seeing it all: Evaluating supervised machine learning meth-
ods for the classification of diverse Otariid behaviours. PLoS One,
11(12), e0166898. https:// doi. org/ 10. 1371/ journ al. pone. 0166898
Lenth, R. V. (2001). Some practical guidelines for effective sample size
determination.  The  American  Statistician,  55(3),  187–193.  https://
doi. org/ 10. 1198/ 00031 30013 17098149

Montesinos  López,  O.  A.,  Montesinos  López,  A.,  &  Crossa,  J.  (2022).
Overfitting,  model  tuning,  and  evaluation  of  prediction  perfor-
mance.  In  O.  A.  Montesinos  López,  A.  Montesinos  López,  &  J.
Crossa  (Eds.),  Multivariate  statistical  machine  learning  methods  for
genomic prediction (pp. 109–139). Springer International Publishing.
https:// doi. org/ 10. 1007/ 978-  3-  030-  89010 -  0_ 4

Lovell,  D.,  Miller,  D.,  Capra,  J.,  &  Bradley,  A.  P.  (2023).  Never  mind  the
metrics- what  about  the  uncertainty?  Visualising  binary  confusion
matrix  metric  distributions  to  put  performance  in  perspective.  In
International Conference on Machine Learning. PMLR.

Mannini, A., Intille, S. S., Rosenberger, M., Sabatini, A. M., & Haskell, W.
(2013). Activity recognition using a single accelerometer placed at
the wrist or ankle. Medicine and Science in Sports and Exercise, 45(11),
2193–2203. https:// doi. org/ 10. 1249/ mss. 0b013 e3182 9736d6
McClintock,  B.  T.,  Johnson,  D.  S.,  Hooten,  M.  B.,  Ver  Hoef,  J.  M.,  &
Morales, J. M. (2014). When to Be discrete: The importance of time
formulation in understanding animal movement. Movement Ecology,
2(1), 1–14. https:// doi. org/ 10. 1186/ s4046 2-  014-  0021-  6

Minasandra, P., Jensen, F. H., Gersick, A. S., Holekamp, K. E., Strauss, E.
D., & Strandburg- Peshkin, A. (2023). Accelerometer- based predic-
tions of behaviour elucidate factors affecting the daily activity pat-
terns of spotted hyenas. Royal Society Open Science, 10(11), 230750.
https:// doi. org/ 10. 1098/ rsos. 230750

Nielsen, A. (2017). Practical time series analysis: Prediction with statistics

and machine learning (1st ed.). O'Reilly Media.

Norouzzadeh, M. S., Morris, D., Beery, S., Joshi, N., Jojic, N., & Clune, J.
(2021). A deep active learning system for species identification and
counting in camera trap images. Methods in Ecology and Evolution,
12(1), 150–161. https:// doi. org/ 10. 1111/ 2041-  210X. 13504

Pagano, A. M., Rode, K. D., Cutting, A., Owen, M. A., Jensen, S., Ware,
J.  V.,  Robbins,  C.  T.,  Durner,  G.  M.,  Atwood,  T.  C.,  Obbard,  M.  E.,
Middel,  K.  R.,  Thiemann,  G.  W.,  &  Williams,  T.  M.  (2017).  Using
tri- axial  accelerometers  to  identify  wild  polar  bear  behaviors.
Endangered  Species  Research,  32(January),  19–33.  https:// doi. org/
10. 3354/ esr00779

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C.,
Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S.
E.,  Chou,  R.,  Glanville,  J.,  Grimshaw,  J.  M.,  Hróbjartsson,  A.,  Lalu,
M. M., Li, T., Loder, E. W., Mayo- Wilson, E., McDonald, S., … Moher,
D. (2021). The PRISMA 2020 statement: An updated guideline for
reporting systematic reviews. Systematic Reviews, 10(1), 89. https://
doi. org/ 10. 1186/ s1364 3-  021-  01626 -  4

Patterson, A., Gilchrist, H. G., Chivers, L., Hatch, S., & Elliott, K. (2019).
A  comparison  of  techniques  for  classifying  behavior  from  accel-
erometers  for  two  species  of  seabird.  Ecology  and  Evolution,  9(6),
3030–3045. https:// doi. org/ 10. 1002/ ece3. 4740

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1334 |

Ploton, P., Mortier, F., Réjou- Méchain, M., Barbier, N., Picard, N., Rossi,
V.,  Dormann,  C.,  Cornu,  G.,  Viennois,  G.,  Bayol,  N.,  Lyapustin,  A.,
Gourlet- Fleury, S., & Pélissier, R. (2020). Spatial validation reveals
poor  predictive  performance  of  large- scale  ecological  mapping
models.  Nature  Communications,  11(1),  4540.  https:// doi. org/ 10.
1038/ s4146 7-  020-  18321 -  y

Putra,  I.  P.  E.  S.,  &  Vesilo,  R.  (2017).  Window- size  impact  on  detection
rate of wearable- sensor- based fall detection using supervised ma-
chine  learning.  In  2017  IEEE  Life  Sciences  Conference.  https:// doi.
org/ 10. 1109/ LSC. 2017. 8268134

Quinn, T. P., Le, V., & Cardilini, A. P. A. (2021). Test set verification is an
essential step in model building. Methods in Ecology and Evolution,
12(1), 127–129. https:// doi. org/ 10. 1111/ 2041-  210X. 13495
Rast,  W.,  Kimmig,  S.  E.,  Giese,  L.,  &  Berger,  A.  (2020).  Machine  learn-
ing goes wild: Using data from captive individuals to infer wildlife
behaviours.  PLoS  One,  15(5),  e0227317.  https:// doi. org/ 10. 1371/
journ al. pone. 0227317

Resheff,  Y.  S.,  Bensch,  H.  M.,  Zöttl,  M.,  Harel,  R.,  Matsumoto- Oda,  A.,
Crofoot,  M.  C.,  Gomez,  S.,  Börger,  L.,  &  Rotics,  S.  (2024).  How  to
treat mixed behavior segments in supervised machine learning of
behavioural  modes  from  inertial  measurement  data.  Movement
Ecology, 12(1), 44. https:// doi. org/ 10. 1186/ s4046 2-  024-  00485 -  7

Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera- Arroita,
G., Hauenstein, S., Lahoz- Monfort, J. J., Schröder, B., Thuiller, W.,
Warton,  D.  I.,  Wintle,  B.  A.,  Hartig,  F.,  &  Dormann,  C.  F.  (2017).
Cross- validation  strategies  for  data  with  temporal,  spatial,  hier-
archical,  or  phylogenetic  structure.  Ecography,  40(8),  913–929.
https:// doi. org/ 10. 1111/ ecog. 02881

Sur, M., Hall, J. C., Brandt, J., Astell, M., Poessel, S. A., & Katzner, T. E.
(2023).  Supervised  versus  unsupervised  approaches  to  classifica-
tion  of  accelerometry  data.  Ecology  and  Evolution,  13(5),  e10035.
https:// doi. org/ 10. 1002/ ece3. 10035

Swihart, R. K., & Slade, N. A. (1997). On testing for independence of ani-
mal movements. Journal of Agricultural, Biological, and Environmental
Statistics, 2, 48–63. https:// doi. org/ 10. 2307/ 1400640

Wainer, J., & Cawley, G. (2021). Nested cross- validation when selecting
classifiers  is  overzealous  for  most  practical  applications.  Expert
Systems with Applications, 182(November), 115222. https:// doi. org/
10. 1016/j. eswa. 2021. 115222

Walsh,  I.,  Fishman,  D.,  Garcia- Gasulla,  D.,  Titma,  T.,  Pollastri,  G.,
Capriotti,  E.,  Casadio,  R.,  Capella- Gutierrez,  S.,  Cirillo,  D.,  Del
Conte, A., Dimopoulos, A. C., Del Angel, V. D., Dopazo, J., Fariselli,
P.,  Fernández,  J.  M.,  Huber,  F.,  Kreshuk,  A.,  Lenaerts,  T.,  Martelli,
P. L., … Tosatto, S. C. E. (2021). DOME: Recommendations for su-
pervised  machine  learning  validation  in  biology.  Nature  Methods,
18(10), 1122–1127. https:// doi. org/ 10. 1038/ s4159 2-  021-  01205 -  4
Wilson,  O.  A.,  Schoeman,  D.  S.,  Bradley,  A.,  &  Clemente,  C.  J.  (2025).
Systematic  review  of  validation  of  supervised  machine  learning

models in accelerometer- based animal behaviour classification lit-
erature.  Dryad  Digital  Repository.  https:// doi. org/ 10. 5061/ dryad.
fxpnv x14d

Wilson,  R.  P.,  Börger,  L.,  Holton,  M.  D.,  Scantlebury,  D.  M.,  Gómez-
Laich, A., Quintana, F., Rosell, F., Graf, P. M., Williams, H., Gunner,
R., Hopkins, L., Marks, N., Geraldi, N. R., Duarte, C. M., Scott, R.,
Strano, M. S., Robotka, H., Eizaguirre, C., Fahlman, A., & Shepard, E.
L. C. (2020). Estimates for energy expenditure in free- living animals
using acceleration proxies: A reappraisal. Journal of Animal Ecology,
89(1), 161–172. https:// doi. org/ 10. 1111/ 1365-  2656. 13040

Xu,  Y.,  &  Goodacre,  R.  (2018).  On  splitting  training  and  validation  set:
A comparative study of cross- validation, bootstrap and systematic
sampling  for  estimating  the  generalization  performance  of  super-
vised learning. Journal of Analysis and Testing, 2(3), 249–262. https://
doi. org/ 10. 1007/ s4166 4-  018-  0068-  2

Yates,  L.  A.,  Aandahl,  Z.,  Richards,  S.  A.,  &  Brook,  B.  W.  (2023).  Cross
validation for model selection: A review with examples from ecol-
ogy. Ecological Monographs, 93(1), e1557. https:// doi. org/ 10. 1002/
ecm. 1557

Yu, H., Deng, J., Leen, T., Li, G., & Klaassen, M. (2022). Continuous on-
board  behaviour  classification  using  accelerometry:  A  case  study
with  a  new  GPS- 3G- Bluetooth  system  in  Pacific  black  ducks.
Methods in Ecology and Evolution, 13(7), 1429–1435. https:// doi. org/
10. 1111/ 2041-  210x. 13878

Yu, H., Muijres, F. T., te Lindert, J. S., Hedenström, A., & Henningsson,
P.  (2023).  Accelerometer  sampling  requirements  for  animal  be-
haviour classification and estimation of energy expenditure. Animal
Biotelemetry,  11(1),  28.  https:// doi. org/ 10. 1186/ s4031 7-  023-
00339 -  w

Yu, H., Wu, Y., Niu, L., Chai, Y., Feng, Q., Wang, W., & Liang, T. (2021).
A  method  to  avoid  spatial  overfitting  in  estimation  of  grassland
above- ground biomass on the Tibetan Plateau. Ecological Indicators,
125(June), 107450. https:// doi. org/ 10. 1016/j. ecoli nd. 2021. 107450
Yu,  T.,  &  Hong,  Z.  (2020).  Hyper- parameter  optimization:  A  review  of
algorithms and applications (preprint). arXiv. https:// arxiv. org/ abs/
2003. 05689

How to cite this article: Wilson, O., Schoeman, D., Bradley, A.,

& Clemente, C. (2025). Practical guidelines for validation of

supervised machine learning models in accelerometer- based

animal behaviour classification. Journal of Animal Ecology, 94,

1322–1334. <https://doi.org/10.1111/1365-2656.70054>

WILSON et al. 13652656, 2025, 7, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70054> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
