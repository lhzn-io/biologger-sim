Received: 13 June 2022 |  Accepted: 7 October 2022
DOI: 10.1111/2041-210X.14019

R E V I E W

A review of supervised learning methods for classifying animal
behavioural states from environmental features

Silas Bergen1  |   Manuela M. Huso2,3  |   Adam E. Duerr4,5,6  |   Melissa A. Braham6  |
Sara Schmuecker7 |   Tricia A. Miller5,6  |   Todd E. Katzner8

1Department of Mathematics and Statistics, Winona State University, Winona, Minnesota, USA; 2U.S. Geological Survey, Forest and Rangeland Ecosystem
Science Center, Corvallis, Oregon, USA; 3Statistics Department, Oregon State University, Corvallis, Oregon, USA; 4Bloom Research Inc, Los Angeles, California,
USA; 5West Virginia University, Morgantown, West Virginia, USA; 6Conservation Science Global, Inc, West Cape May, New Jersey, USA; 7U.S. Fish and Wildlife
Service, Illinois- Iowa Field Office, Moline, Illinois, USA and 8U.S. Geological Survey, Forest and Rangeland Ecosystem Science Center, Boise, Idaho, USA

Correspondence
Silas Bergen
Email: <sbergen@winona.edu>

Funding information
American Eagle Foundation; American
Wind Wildlife Institute; Arconic
Foundation; Avian Power Line Interaction
Committee; ITC Holdings; Mid- American
Energy; U.S. Fish and Wildlife Service

Handling Editor: Res Altwegg

Abstract

1. Accurately predicting behavioural modes of animals in response to environmen-

tal features is important for ecology and conservation. Supervised learning (SL)

methods are increasingly common in animal movement ecology for classifying

behavioural modes. However, few examples exist of applying SL to classify poly-

tomous animal behaviour from environmental features especially in the context

of millions of animal observations.

2. We review SL methods (weighted k- nearest neighbours; neural nets; random for-

ests; and boosted classification trees with XGBoost) for classifying polytomous

animal behaviour from environmental predictors. We also describe tuning param-

eter selection and assessment strategies, approaches for visualizing relationships

between  predictors  and  class  outputs,  and  computational  considerations.  We

demonstrate these methods by predicting three categories of risk to bald eagles

from colliding with wind turbines using, as predictors, 12 environmental state fea-

tures associated with 1.7 million GPS telemetry data points from 57 eagles.

3. Of the SL methods we considered, XGBoost yielded the most accurate model

with 86.2% classification accuracy and pairwise- averaged area under the ROC

curve of 90.6. Computational time of XGBoost scaled better to large data than

any other SL method. We also show how SHAP values integrated in the R pack-

age (xgboost) facilitate investigation of variable relationships and importance.

4. For big data applications, XGBoost appears to provide superior classification ac-

curacy and computational efficiency. Our results suggest XGBoost should be con-

sidered as an early modelling option in situations where the intent is to classify

millions of animal behaviour observations from environmental predictors and to

understand  relationships  between  those  predictors  and  movement  behaviours.

We also offer a tutorial to assist researchers in implementing this method.

This is an open access article under the terms of the Creative Commons Attribution-NonCommercial License, which permits use, distribution and reproduction
in any medium, provided the original work is properly cited and is not used for commercial purposes.
© 2022 The Authors. Methods in Ecology and Evolution published by John Wiley & Sons Ltd on behalf of British Ecological Society. This article has been
contributed to by U.S. Government employees and their work is in the public domain in the USA.

Methods Ecol Evol. 2023;14:189–202.

wileyonlinelibrary.com/journal/mee3

 |  189

190 |   Methods in Ecology and Evolu(cid:13)on

K E Y W O R D S
behavioural classification, boosted classification tree, neural networks, random forest,
supervised learning, weighted k- nearest neighbour, XGBoost

1  |  I NTRO D U C TI O N

Boosted classification trees (BCTs) improve upon RFs by ‘boost-

ing’, wherein each new tree attempts to improve upon what has not

Understanding an animal's response to its environment and predict-

already  been  predicted  by  the  previous  trees.  Boosting  is  a  very

ing its behaviour with environmental features is a frequent goal in an-

powerful learning concept (Hastie et al., 2009) but computation time

imal movement ecology (Kays et al., 2015; Mercker et al., 2021) that

is still a concern when implementing BCTs, especially when there are

also  has  important  implications  for  conservation  (Sur  et  al.,  2021;

millions  of  observations  to  be  modelled— as  can  often  be  the  case

Wijeyakulasuriya et al., 2020). As advances in technology for study-

with animal movement data from biologgers. The eXtreme Gradient

ing animal movement have led to an increase in quantities of move-

Boosting  (xgboost)  package  (Chen  &  Guestrin,  2016)  is  a  recently

ment  data,  computational  feasibility  of  behavioural  classification

developed, state- of- the- art, open- source package available on mul-

tools is also an important consideration (Clarke et al., 2021).

tiple  platforms  that  implements  BCTs  in  a  manner  that  allows  for

Supervised  learning  (SL)  models  are  increasingly  common  in

modelling hundreds of millions of observations. XGBoost harnesses

behavioural  ecology  for  classification  of  behavioural  modes,  with

parallel and distributed computing, intelligent memory handling, and

especially wide application in movement studies using accelerome-

model  regularization  to  facilitate  efficient  fitting  on  desktop  com-

ters (e.g. Brandes et al., 2021; Yu et al., 2021). SL methods are typi-

cally capable of modelling complex nonlinear relationships between

puters. The XGBoost system is so efficient that it can run >10 times
faster  than  other  existing  BCT  packages  (Chen  &  Guestrin,  2016),

predictors  and  polytomous  behavioural  responses,  and  differ  with

resulting in a powerful and efficient machine learning method that

respect  to  computational  scalability,  interpretability  and  classifica-

can outperform RFs (Muñoz- Mas et al., 2019), offering great promise

tion  accuracy.  Popular  SL  approaches  for  animal  movement  stud-

for classifying large amounts of animal behaviour data.

ies  include  k- nearest  neighbours,  neural  networks  and  tree- based

Despite  the  plethora  of  studies  that  classify  animal  behaviour

methods  (Valletta  et  al.,  2017).  k- nearest  neighbours  and  its  ex-

and  the  importance  of  linking  animal  behaviour  to  variation  in  un-

tension  weighted  k- nearest  neighbours  (wKNN;  Hechenbichler  &

derlying environmental features, we know of no examples in which

Schliep, 2004) is a conceptually simple classification algorithm, but

SL was used to classify animal behaviour with predictors describing

it  does  not  facilitate  interpreting  relationships  between  predictors

those underlying environmental features. All the above- referenced

and response classes and may not be computationally feasible when

applications of SL in movement ecology use derived variables from

trying to classify millions of behaviour points.

accelerometer  or  GPS  data  to  classify  behaviour.  Furthermore,  we

Neural networks (NNs) model relationships between behaviours

are aware of only two applications of SL in movement ecology that

and predictors using hidden nodes. The relationship between each

used  XGBoost  (Leoni  et  al.,  2020;  Yu  et  al.,  2021).  However,  nei-

node and environmental predictors is modelled as a nonlinear trans-

ther  of  these  investigated  relationships  between  animal  behaviour

formation of a weighted sum of the predictors. The behaviour classes

and  underlying  predicting  features,  and  both  explored  relatively

are then modelled as a nonlinear transformation of a weighted sum

small datasets (tens of thousands of observations). Finally, only Yu

of  the  hidden  nodes.  The  result  is  a  complex  network  with  highly

et al. (2021) used XGBoost to classify polytomous behaviours.

nonlinear  relationships  between  predictors  and  behaviours.  NNs

Given  the  promise  of  SL  methods  for  classifying  polytomous

have  been  used  to  classify  animal  behaviour  from  accelerometer

animal  behaviour  from  its  environment  and  the  lack  of  literature

data (Patterson et al., 2019) and GPS data (Browning et al., 2018), but

describing  considerations  associated  with  large  data  applications,

as with wKNN, the sheer number of parameters to be estimated can

especially for the promising XGBoost method, a review of SL meth-

result in overfitting and extensive training times for large datasets.

ods  in  this  context  is  needed.  Accordingly,  we  present  a  review  of

Random  forests  (RFs)  are  a  tree- based  method  extensively

SL  methods  for  classifying  polytomous  animal  behaviour  classes

used in animal movement studies (e.g. Brandes et al., 2021; Clarke

from environmental characteristics, strategies for parameter tuning,

et  al.,  2021;  Patterson  et  al.,  2019).  RFs  are  examples  of  ‘ensem-

model selection and model assessment, approaches for understand-

ble’  learning  methods  wherein  a  set  of  relatively  simple  classifiers

ing  predictor  variable  importance  and  visualizing  the  relationships

is formed and averaged to generate final predictions. The ‘random’

between behaviour and environment, and computational scalability.

aspect of RFs refers to the fact that each tree is built off a random

We demonstrate this framework with a case study to classify more

subset  of  the  available  predictor  variables  and,  potentially,  of  the

than 1.7 million GPS telemetry points collected from 57 bald eagles

training  data  as  well.  With  deep  trees,  these  methods  can  model

in flight. Our goal in the case study was to classify flight points into

complex  interactions  among  predictors.  Compared  to  wKNN  and

one of three different categories indicating varying risk of collision

NNs, RFs are computationally efficient. However, a limitation of RFs

with  industrial  wind  turbines.  To  aid  researchers  in  implementing

is there is no information shared between trees, which can lead to

XGBoost,  we  have  made  available  a  tutorial  using  a  subset  of  our

tree redundancy.

data (Bergen, 2022).

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License2  |  M E TH O D S

2.1  |  Overview of supervised learning classification
methods

In these sections we describe (1) popular SL methods that can be ap-

plied to behavioural classification; (2) strategies for model selection

and model assessment; and (3) ways to identify important predictor

variables and their relationships with the modelled class probabilities.

Throughout this section we will use training data to refer to a fraction

of the data (usually two- thirds or three- fourths) used to fit the model,

and test data as the remaining fraction for which the response was

predicted from the trained model under consideration.

}

{

xi1, xi2, … , xip

Before  proceeding  we  define  some  preliminary  notation.  Let
xi ≡
  represents  the  set  of p  predictor  variables  for
the ith observation in the training set; i = 1, … , n. Categorical vari-
ables may be included in xi by way of one- hot (dummy variable) en-
coding.  Of  interest  is  using  these  predictors  to  model  a  response
yi  with C  behavioural  modes.  Let
  represents  the C

- vector  of  indicator  functions  where  yic = I
  rep-
{
resents the modelled probability of observation i  belonging to class
c  given  predictors;  modelled  classes  are  then  typically  defined  as
̂yi = argmaxc
modelled probability.

;  that  is,  the  class  with  the  highest

yi1, yi2, … , yiC

.  Let  ̂pc

, … , ̂pC

yi = c
}

̂p1

xi

xi

xi

(

)

(

)

(

(

)

(

))

Methods in Ecology and Evolu(cid:13)on

    |  191

predicted class of x0 is the majority class of these k- nearest neighbours.
It is up to the analyst to specify the value of k; with k = 1 the predicted
class of x0 is just the class of the training set observation with the most
similar covariates to x0.

Weighted  k- nearest  neighbours  extends  this  approach  by

d

the

) × I(

1 − d2

triangular

exp
≤ 1);
�

× I(
d
≤ 1);
|

K(d) = (1 −
− d2
;
2
|
and
�

weighting  the  ‘votes’  of  the  nearest  neighbours  with  a  kernel.  The
kernel K(d)  is  a  function  of  distance  d,  with K(d) ≥ 0  for  all  d. K(d)
achieves  its  maximum  when  d = 0  and  is  monotone  decreasing  as
∣ d ∣  increases.  Kernels  available  in  the  kknn  R  package  (Schliep
et  al.,  2016)  include  the  rectangular  kernel  K(d) = 1
≤ 1) ;
2
d
the

kernel
K(d) = 1
Gaussian
kernel
2𝜋
kernel  K(d) = 3
⋅ I(
d
kernel
√
4
K(d) = 𝜋
≤ 1) (Figure 1). Given k and choice of kernel
)
4
K, let  x(1), … , x(k+1) represents the k + 1 nearest training set neigh-
bours  of  x0  ordered  from  nearest  to  farthest.  The (k + 1)st  nearest
neighbour  is  used  to  standardize  the  distances  from  x0  to  the  re-
maining k, so that dstd
≤ 1 for i ∈ 1, … , k. Weights
dstd
w(i) = K
ity of the test set defined as ̂p0c =
 with corresponding
predicted class ̂y0.The value of k and type of kernel are tuning pa-
rameters  that  must  be  specified  to  implement  weighted  k- nearest

 are then formed and predicted class probabil-
(

i=1 w(i)I(y(i) = c)
k
i=1 w(i)

|
Epanechnikov

d(x(i),x0)
d(x(k+1),x0)

|
cosine

the
|

x(i), x0

x(i), x0

× I(
(

the

cos

𝜋d
2

))

=

)

(

d

(

)

(

∑

∑

|

|

|

|

|

k

neighbours in the kknn package.

2.3  |  Neural networks

2.2  |  Weighted k- nearest neighbours

Neural networks are supervised learning models that are named

Weighted k- nearest neighbours (Hechenbichler & Schliep, 2004) de-

after the neurons found in the human brain (Figure 2). A neural

fines an algorithm, rather than a model, for classifying test set ob-

network is a two- stage classification model, where the predictors

servations. It is an extension of the k- nearest neighbour algorithm, a
simple method for classifying a polytomous yi. Given covariate val-
ues  x0 of a test set observation, its Minkowski distance from each
training set value is:

are  used  to  model  nodes  of  a  hidden  layer;  these  hidden  layer

nodes are then used to model the classified probabilities. Given
H  nodes  in  a  hidden  layer,  the  relationship  of  xi  with  node  h  is
given by:

d

xi, x0

=

(

)

(∑

p

j=1

xij − x0j

q

1∕q

.

|
|
|

)

|
|
|

When q = 2 this is Euclidean distance. Using this distance metric, the k

- nearest neighbours to x0 from the training set are identified, and the

wh

xi

= 𝜙

𝛽h0 +

p

j=1

𝛽hjxij

.

(

)

(

∑

)

The function 𝜙 is called an activation function and for classification is

typically set to be the logistic function, which maps the real numbers

to (0,1):

F I G U R E   1 Common kernels for weighted k - nearest neighbour

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License192 |   Methods in Ecology and Evolu(cid:13)on

F I G U R E   2 Diagram of a neural network with H = 4 hidden nodes for classifying a C = 3 level polytomous response. (a) Shows a neural
network without a skip layer, while (b) includes a skip layer which models the relationship between predictors xi and class probabilities
directly.

𝜙(z) =

1
1 + e−z

.

The relationship between node h and probability class c is sub-
sequently modelled as a transformed linear combination of the wh ,
specifically:

pc

xi

= 𝜙

𝛼0c +
(

H

h=1

𝛼hcwh

xi

.

∑
The collection of parameters 𝜃 are estimated to minimize the log- loss in

(

)

(

))

et al., 2002) can be used to fit neural nets. Required tuning parameters

are the number of hidden layers, whether or not to use a skip layer,

and the value of the decay parameter. Hastie et al. (2009) recommend

standardizing  all  predictors  to  have  mean  0  and  variance  1  prior  to

model fitting, as nonhomogenous scaling can have large effect on the

quality of the final solution.

2.4  |  Random forests

the training set, where the log- loss is given by:

Random forests are a type of ensemble model, wherein predictions

R(𝜃) = −

n

i=1

C

c=1

yiclog

̂pc

xi

.

∑

∑

(

(

))

The minimization is subject to the constraint that
all i.

C
c=1 ̂pc

xi

= 1 for

∑

�

�

Neural  networks  are  highly  parameterized,  and  regularization

can  be  used  to  avoid  overfitting.  In  the  case  of  a  neural  network
without a skip layer, this involves minimizing R(𝜃) + 𝜆J(𝜃) where:

J(𝜃) =

𝛽2
h0 +

𝛽2
hj +

h
∑

h,j
∑

𝛼2
0c +

𝛼2
hc

h
∑

.

)

c (
∑

The parameter 𝜆 is often referred to as a decay parameter and penal-

izes large linear weights. Larger values of 𝜆 yield a more conservative
model. Setting 𝜆 = 0 results in no model regularization.

are formed by averaging across many separate classification trees.
Let  fj( ⋅ )  represent  a  tree  in  a  ‘forest’  of T  trees,  for  j = 1, … , T.  fj
has  a  depth  of M  with Lj  leaves  (sometimes  referred  to  as  ‘nodes’).
The parameter M controls the depth of the tree and complexity of
predictor  variable  interactions.  Higher  M  allows  for  deeper  trees,

higher- order  interactions  and  more  nonlinear  univariate  relation-
ships. Every data point is assigned to a leaf in tree  j by following a
series of binary splits; each split defined by one of the p predictor

variables (Figure 3).

For  a  single  classification  tree  f   that  maps  xi  to  leaf  l ,  the
= 1
 modelled probabilities are ̂pc
, that is, the pro-
Nl
portion of training points in the same leaf as  xi belonging to class
cl measures the impurity of leaf  l , with
c. The Gini index 1 −
Gini indices of 0 indicating a pure leaf (all training observations in

c=1 ̂p2

yi = c

i∈lI

∑

xi

�

�

�

�

C

∑

the leaf belong to the same class). Each split in the tree is chosen

A skip layer can be included in which case weights are included

to minimize the Gini index. Random forests (Breiman, 2001) are a

that directly model the relationship between the class probabilities

collection  of  de- correlated  trees  where  the  de- correlation  occurs

and the predictors (Figure 2b). In this case the model becomes:

pc

xi

= 𝜙

𝛾 0 +

p

j=1

𝛾 jxij + 𝛼0c +

H

h=1

𝛼hcwh

xi

.

(

)

(

∑

∑

(

))

by  bagging  (subsampling  the  training  rows)  and  subsampling  the
available predictors to grow each tree. For each of t = 1, … , T, the

random forest algorithm:

Regularization  can  also  be  used  with  skip  layers  in  which  case  J(𝜃)
is  extended  to  include 𝛾 0  and  the 𝛾 j.The  nnet  package  in  r  (Venables

1. Draws  a  bootstrap  sample  of  size  nb  and  randomly  selects  m

variables  from  the  p  available.

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMethods in Ecology and Evolu(cid:13)on

    |  193

F I G U R E   3 Two example trees, both of depth M = 3 (the shaded regions) where tree (a) has L1 = 6 leaves (circles with scores w11, …, w16)
and tree (b) has L2 = 5 leaves (circles with scores w21, …, w25). Each tree maps data point i  to one of Lj leaf scores wjl for j ∈ {1, 2} and
l ∈
predictor variable could be used in more than one branch of the tree (xi1 in a) or not at all, and while two trees could have the same depth M,
the number of leaves might differ depending on how splits were defined.

 by following a series of binary splits, each split defined by one of p = 4 predictor variables

. Note that any one

xi1, xi2, xi3, xi4

1, … , Lj

{

}

{

}

2. Grows a classification tree ft to the bootstrapped data using the
m variables until either all nodes are pure or a specified maximum

number of nodes has been reached, whichever comes first.

3. Outputs the T trees.

Let x0 represent covariates of a test set observation, then ̂ptc
is formed for each tree t and the predicted random forest probability
)
formed by averaging across trees: ̂pc

x0

x0

x0

(

.

T
t=1 ̂ptc

= 1
T

Random forests are relatively simple to train and tune and often
�

�

�

�

∑

leaf l  are assigned a score wjl for l ∈
tree- based mapping from xi to its leaf score. The modelled logit ̂p
is found by summing t trees:

1, … , Lj

. Thus fj

xi

}

{

(

)

= wjl is the

xi

)

(

(t) =

̂yi

t

j=1

fj

xi

.

∑

(

)

Boosted  trees  are  grown  sequentially  with  each  new  tree  grown  to

best  predict  what  has  not  already  been  modelled  by  previous  trees.
Specifically, for each boosting iteration t, the optimal ‘next tree’ is the

yield  accurate  predictions  (Hastie  et  al.,  2009).  Because  each  tree

one that minimizes the objective function:

branch  is  a  binary  split  on  one  of  the  predictor  variables,  it  is  not

important for the variables to be on the same scale or to be symmet-

ric. Random forests can be implemented in R with the randomForest
package  (Liaw  &  Wiener,  2002).  The  tuning  parameters  are T,  the
number of trees to grow, the maximum number of leaves Lj for each
tree,  the  proportion  of  rows  to  subsample  for  each  tree  (RSP)  and

the proportion of predictor variable columns to sample for each tree

(CSP).

2.5  |  Boosted classification trees and XGBoost

Whereas  random  forests  grow  de- correlated  trees,  boosted  clas-

sification  trees  are  grown  sequentially  with  each  tree  optimized

to  explain  that  which  has  not  already  been  modelled  by  previous
trees.  For  now,  to  simplify  notation,  let  yi  be  binary  and  redefine
. Once again let fj( ⋅ ) rep-
̂yi = logit
resents a tree with a depth of M that has Lj leaves. All data points in
)

 where logit(p) = log

p
1 − p

xi

̂p

(

(

(

))

(t) =

n

i=1

l

yi, ̂y(t)

i

,

∑

(

)

where l( ⋅ ) is a loss function which for binary classification is:

l

yi, ̂y(t)

i

(

)

= yilog

̂p

xi

+

1 − yi

log

1 − ̂p

xi

.

t−1
j=1 fj

xi

- ft

(

xi

(
(
))
= ̂y(t−1)
i

- ft

)

(

(

))

xi

 the objective can be re-

∑

�

�

�

�

�

�

Since ̂y(t)
i =
written as:

(t) =

n

i=1

∑

l

yi, ̂y(t−1)
(

i

- ft

xi

.

(

))

(1)

The optimal next tree in the boosting sequence is the ft that min-
imizes (t) and can be found by gradient descent, where both the
decrease  in  (t)  associated  with  each  possible  split  and  the  leaf

scores depend on both the gradient and the Hessian of the loss

function. Chen and Guestrin (2016), Friedman (2001) and Hastie

et al. (2009) provide full details on the mathematical form of the

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

194 |   Methods in Ecology and Evolu(cid:13)on

scores and algorithms for finding splits. From Equation 1 it is ap-

parent  that  the  optimal  next  tree  in  the  boosting  sequence  de-
pends  explicitly  upon  the  previous  t − 1  trees  and  is  chosen  to

improve upon what has not already been explained by the trees

grown before it.

It  is  possible  for  boosted  trees  to  overfit  the  training  data  by

learning  ‘too  fast’.  One  way  to  prevent  this  is  to  slow  the  learning
rate with a learning rate parameter 𝜂, such that ̂y(t)
The smaller the learning rate parameter 𝜂, the more the contribution
)
of each new tree is diminished. This results in slower learning, which

i = ̂y(t−1)

- 𝜂ft

xi

.

(

i

proportions; the maximum depth of each tree (M); the shrinkage pa-
rameter 𝜂; and the regularization parameters 𝜆 and 𝛾. The number of
boosting  iterations  t  is  also  a  tuning  parameter,  but  xgboost  imple-
ments an ‘early stopping rule’ for choosing t whereby boosting contin-

ues until an evaluation metric (such as the log- loss) has not improved

on the test set for a user- specified number of iterations. This avoids
having to perform a tuning parameter grid search involving t as the op-
timal t is selected given specification of the other tuning parameters.

also requires more trees (Friedman, 2001).

2.6  |  Model selection and assessment

Another way to improve predictive accuracy is to introduce ran-

domness into each tree, reducing the correlation between trees so

Tuning the parameters to optimize predictive accuracy is a crucial as-

that new trees are adding more ‘new’ information. Like random for-

pect of supervised learning. A common approach is to perform a grid

ests, a subset of rows and/or columns may be sampled at random at

search over a combination of tuning parameters and choose the model

each boosting iteration. In addition to ensuring the training data are

that  optimizes  misclassification  error  in  the  test  set.  After  selecting

not overfit, adding stochasticity to each tree also has the advantage

the  best  model  its  predictive  ability  must  be  assessed.  K- fold  cross-

of speeding up the algorithm. Subsampling columns is thought to be

validation  more  accurately  represents  true  out- of- sample  predictive

more effective at preventing overfitting than is the more traditional

ability than using the accuracy from the same test set used to select

row subsampling (Chen & Guestrin, 2016).

the model, which can provide an overly optimistic representation of a

The XGBoost algorithm developed by Chen and Guestrin (2016)

model's true out- of- sample predictive ability (Hastie et al., 2009).

modifies (1) slightly by including regularization terms on the depth of

Overall performance can be assessed with the overall accuracy

the tree and the leaf scores. Specifically, (1) becomes:

rate (per cent of correctly classified points). Overall accuracy is best

(t) =

n

i=1

l

yi, ̂y(t−1)

i

- ft

xi

- 𝛾

t

j=1

Lj +

1
2

𝜆

t

j=1

Lj
l=1

w2
jl .

∑

(

(

))

∑

∑

∑

Thus  (t)  is  small  when  the  additive  loss  is  small,  but  also  when

the  number  of  leaves  and  scores  assigned  to  each  leaf  are  also

small. 𝛾  sets  the  minimum  loss  reduction  required  for  each  addi-

tional split in the tree by penalizing the number of leaves and thus

can be considered a ‘pruning’ parameter since increasing it prunes

back leaves that add little predictive value. 𝜆 penalizes large leaf

compared  to  the  ‘no- information  rate’,  equal  to  the  prevalence  of

the  majority  class,  as  a  measure  of  how  well  the  model  improves

upon a noninformative model that simply assigns each point to the

majority class. The model's ability to separate the predicted proba-
bilities of class ci from cj can be measured by the pairwise area under
the ROC curve (auROC). An auROC of 1 indicates perfect separation

between these probabilities while an auROC of 0.5 indicates perfect
overlap and complete failure to distinguish class ci from cj. An ‘overall
auROC’ can be formed to measure overall performance by averaging

weights  and  can  be  considered  a  ‘shrinkage’  parameter  since  in-

the pairwise auROC (Hand & Till, 2001). This yields an estimate of

creasing  𝜆  shrinks  the  leaf  weights  towards  0.  Increasing  𝜆  or  𝛾

the overall auROC that is not sensitive to the distribution of points

results  in  a  more  conservative  model  (ensuring  the  training  data

among classes:

are not overfit).

For  classification  of  a  C- level  response  variable  where  C > 2,

yi1, … , yiC
function generalizes to:
{
}

 is a C- vector of indicators with yic = I

yi = c

. The loss

(

)

l

yi, ̂yi

= −

C

c=1

yiclog

̂pc(xi)

,

(

)

∑

(

)

where the ̂pc
referred to as the softmax function:

xi

(

)

 are guaranteed to sum to 1 using what is sometimes

̂pc

xi

=

�

�

exp

t
j=1 fjc

xi

�∑
C
c=1 exp

�
t
j=1 fjc

��
xi

.

∑

�∑

�

��

auROCoverall =

2
C(C − 1)

auROC

ci, cj

.

(2)

i,j∈{1,…,C}:i<j
∑

(

)

The  auROCoverall  represents  the  overall  separation  of  the  predicted
probabilities of the C classes.

2.7  |  Variable relationships and importance

“[A]  single  metric,  such  as  classification  accuracy,  is  an  incomplete

description  of  most  real- world  tasks.”  (Doshi- Velez  &  Kim,  2017).

After finding an SL method that accurately classifies behaviour from

environmental features it is likely that researchers will want insight

Thus, at each of the t boosting iterations, C trees are grown, with

into which environmental predictors were most important, and how

the constraint

C
c=1 fjc

xi

= 0 ∀ j typically imposed for identifiability.

those  predictors  are  used  in  the  SL  model  to  classify  behaviour.

The boosted classification tree tuning parameters in the r package

Global explanation methods seek to describe the average behaviour

∑

�

�

xgboost (Chen et al., 2022) include the row and column subsampling

of a SL model while local methods seek to describe how predictors

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons Licenseexplain  individual  predictions  (Molnar,  2022).  In  this  section,  let
̂f(x) be a fitted SL model that maps predictor xi =
prediction,  for  example,  a  class  probability  or  logit  probability.  For
classification of polytomous behaviours there are likely C such func-

xi1, … , xip

 to a

}

{

tions, one for each class; for simplicity of notation in this section we

will only consider one function (i.e. binary classification). The meth-

ods that follow can then be easily extended to >2 classes by applying
the method multiple times, one for each class.

2.8  |  Individual conditional expectation and partial
dependence plots

A model- agnostic approach to local explanation is the independent

conditional expectation (ICE) plot, to which the partial dependence

plot  (PDP)  is  the  global  analogue.  ICE  and  PDP  plots  are  model-

agnostic  explanation  methods  in  the  sense  that  they  are  defined

apart from the SL model (Molnar, 2022) and can thus be applied to
an  array  of  SL  models.  Let  xis  be  the  predictor  of  interest,  and  xis′
the remaining predictors. Then for a grid of values
along the range of xis, the individual conditional expectation is given
}
by:

, … , xism

, xis2

xis1

{

(i)
̂f
s =

̂f

xis1

, xis�

,̂f

xis2

, xis�

, … ,̂f

xism

, xis�

.

{

)

(

(

)
(i)
A single line on an ICE plot, ̂f
s , shows how the predictions for the ith
training  instance  vary  for  changes  in  the  predictor  of  interest  xis,  by
replacing xis with values from the grid and making predictions at each
value, keeping all other predictors constant at their observed values.

(

)}

Methods in Ecology and Evolu(cid:13)on

    |  195

suite of predictors. ‘SHAP’ (SHapley Additive exPlanations) is a com-

putationally efficient implementation of Shapley theory developed

by Lundberg and Lee (2017). As with PDPs and ICE plots, SHAP val-

ues are model agnostic and can be defined for any SL model. SHAP
values arise from defining the prediction ̂f  as a linear combination of
contributions 𝜙j, such that:

̂f

xi

= 𝜙0 +

p

j=1

𝜙j

xij

.

∑

)

(

(

)

(

xij

)
 is the contribution of variable xij to the
The interpretation of each 𝜙j
prediction of instance i, relative to the average prediction for the data-
set 𝜙0. For more detail and an excellent, intuitive description of SHAP
values the reader is referred to sections 9.5– 9.6 of Molnar (2022). Each
training instance has p SHAP values 𝜙j, one for each predictor. Plotting
 versus xij for many training instances i provides
the SHAP values 𝜙j
insight into how different xij contribute to the predictions. Variability in
 for equivalent xij indicates interaction with other xij′, which
the 𝜙j
can simply be added as a third dimension to the plot (via colour or size)

xij

xij

(

)

(

)

or faceted upon to illustrate interaction relationships. This makes in-

teractions easier to investigate with SHAP values than with ICE and

PDP plots.

An advantage to SHAP values is that they can be used to inform

global variable importance, by averaging the absolute SHAP values
for a predictor. 𝜙j = 1
xij
ant’ variables and small for variables that contribute little to predic-
�
tions. Ordering the variables by 𝜙j provides a more consistent and
accurate representation of variable importance than the commonly

∣ will be large for more ‘import-

n
i=1 ∣ 𝜙j

∑

�

n

used  relative  gain.  For  tree- based  methods,  the  gain  of  a  variable

measures  the  total  improvement  in  the  objective  function  for  all

The partial dependence ̂f s is simply the average of all individual

splits  involving  that  variable  across  all  trees.  The  relative  gain  of  a

conditional expectations:

̂f s =

1
n

n

i=1

(i)
̂f
s .

∑
Thus, an ICE plot visualizes the dependence of the prediction on a fea-

variable is the fractional contribution of its gain to the total gain of

all the variables. As pointed out by Lundberg and Lee (2017), relative

gain is biased to attribute more importance to variables used in splits
lower  in  the  tree,  whereas  ordering  by  𝜙j  more  directly  measures
each variable's actual contribution to predictions.

ture for each training instance separately, one line per instance, while a

A  disadvantage  to  SHAP  values  for  explaining  relationships  is

PDP averages over these to produce one overall line.

that they are somewhat more difficult to interpret than an individ-

An  advantage  to  PDPs  and  ICE  plots  are  their  interpretability,

ual  conditional  expectation,  as  they  are  contributions  to  an  obser-

as  it  is  possible  to  plot  the  partial  dependence  of  the  class  prob-

vation's  prediction  relative to  the  average  prediction.  Furthermore,

abilities  versus  each  predictor.  A  drawback  of  these  plots  is  that

these contributions are on the raw scale (e.g. logit probability), and

if  the  predictors  are  correlated,  the  partial  dependence  of  class

no transformation of the raw contributions to the more interpreta-

probabilities evaluated along the sequence of an individual predic-

ble probability scale contributions exists.

tor  may  average  across  sparse  data  for  some  of  the  values  in  the

sequence.  Additionally,  visualizing  interactions  between  variables

with PDPs is not straightforward as it requires creating ICEs along a

3  |  C A S E S T U DY

two- dimensional grid of variable pairs and averaging. This becomes

tedious if many predictors are involved.

3.1  |  Data

2.9  |  SHAP values

Shapley  values  are  derived  from  coalitional  game  theory  and  indi-

flight behaviour of soaring birds has been modelled, predicting the

cate how to fairly assign contributions to a modelled output from a

relationship between land features and risk of collision with wind

Bald  eagles  are  at  risk  of  collision  with  wind  turbines.  Although

3.1.1  |  Eagle flight data

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
196 |   Methods in Ecology and Evolu(cid:13)on

turbines is an important conservation goal that can inform place-

we scaled all continuous predictors. We used the kknn package in r

ment  of  future  wind  energy  developments.  Some  of  the  highest

(Schliep et al., 2016) to implement wKNN.

turbine- caused mortality rates of this species have been reported

For  the  NNs  we  trained  to  a  grid  combining  hidden

in  the  Midwestern  United  States,  where  eagles  use  both  ripar-

ian  habitats  and  the  upland  areas  where  wind  turbines  are  often

built (Schmuecker et al., 2020). Data from GPS telemetry devices

sizes  H ∈ {2, 4, 6, … , 18, 20},

layer
parameters  of
𝜆 ∈ {0,0.001, 0.01, 0.1, 0.5}  and  skip  layers  ∈ {TRUE, FALSE}  for  a
total of 10 × 5 × 2 = 100 tuning combinations. Prior to implementing

decay

on eagles can be used to describe eagle flight behaviour (Bergen

NNs we scaled all continuous predictors. We used the nnet package

et al., 2022), and certain flight behaviours are likely to be associ-

in r (Venables et al., 2002) to implement the NNs.

ated with higher collision risk. If risky behaviours can be associated

with underlying landscape features, there is the potential to iden-

tify landscapes where collision risk is relatively more or less likely,

thus providing important information to guide turbine siting. This

For  the  RFs  we  trained  to  a  grid  combining  number  of
trees  T ∈ {50,100, … , 250, 300},  row  sampling  per  cent  RSP
∈ {0.6, 0.7, 0.8, 0.9, 1}  and  CSP  ∈ {0.6, 0.7, 0.8, 0.9, 1}  for  a  total  of
6 × 5 × 5 = 150 combinations. Trees were grown until all nodes were

objective  of  identifying  landscapes  with  increased  collision  risk

pure. We used the randomForest package in r (Liaw & Wiener, 2002)

motivated us to use SL to predict bald eagle risk of collision with

to implement the RFs.

wind  turbines  from  underlying  land  features.  We  used  1,765,935

We  used  XGBoost  as  implemented  in  the  xgboost  r  package

in- flight GPS points from bald eagles in Iowa. Consecutive points

(Chen  et  al.,  2022)  to  fit  the  BCTs.  Since  XGBoost  involves  many

were between 1 and 11 s apart. Each GPS point belonged to one

more tuning parameters than any of the other methods we consid-

of three risk levels from wind turbines: high risk, moderate risk and

ered,  searching  a  grid  involving  all  tuning  parameters  potentially

low  risk,  defined  by  a  combination  of  the  flight  characteristics

could  have  yielded  thousands  of  tuning  parameter  combinations.

and elevation. Low- risk GPS points were all ≥250 m above- ground

Accordingly,  we  searched  a  parameter  grid  in  two  stages.  In  the

level. Moderate-  and high- risk GPS points were all <250 m above-
ground  level,  but  moderate- risk  points  were  less  tortuous  than

high- risk points. For more details on definition of the risk levels see

first stage we searched over combinations of maximum tree depths
M ∈ {16, 18, … , 28, 30}, and both RSP and CSP ∈ {0.6,0.7,0.8,0.9,1}
for  a  total  of 13 × 5 × 5 = 325  combinations.  For  these  we  set  the

Appendix S1. Of the 1,765,935 GPS points, 60.5% were defined as

shrinkage parameter 𝜂 and the regularization parameters 𝛾 and 𝜆 to

high risk, 7.8% as moderate risk and 31.7% as low risk of collision

their respective default values of 0.3, 0 and 1. The optimal number

with wind turbines.

3.1.2  |  Environmental predictors

We  associated  each  classified  GPS  telemetry  datum  with  a  set  of

environmental predictors that are known to be associated with eagle

of boosting iterations for each parameter combination was chosen

using  an  early  stopping  rule:  boosting  continued  until  the  test  set

log- loss did not improve for 10 consecutive iterations. After search-

ing the first grid, we chose the top three combinations of {M, CSP,

RSP}  using  the  lowest  test  set  misclassification  error  and  we  com-
bined them with a new grid involving 𝜂 ∈ {0.1, 0.2, 0.3}, 𝛾 ∈ {0, 1, 2}
and  𝜆 ∈ {0, 1, 2},  for  a  total  of  3 × 3 × 3 × 3 = 81  second- stage

behaviour. Accordingly, we identified a series of environmental pre-

combinations.

dictors  that  we  felt  would  be  useful  to  describe  bald  eagle  flight

For  each  SL  method  (wKNN,  NN,  RF,  XGBoost)  we  selected  the

behaviour  in  Iowa.  Our  features  included  six  predictors  describing

tuning parameter combination with the lowest test set misclassifica-

distance to features relevant to eagles, four topographic predictors

tion error and subsequently carried out five-fold cross- validation with

and two categorical state predictors. For details on these variables

that combination. We then calculated overall and by- class assessment

see Appendix S2.

metrics to assess each method's out- of- sample predictive ability.

3.2  |  Supervised learning

3.2.2  |  Computation time

3.2.1  |  Model training

For all SL methods we measured the time it took to train the model

and classify the test set. To investigate how well the best SL mod-

To train the SL methods we randomly divided the data into a training

els scaled as size of the training set increased, we further evaluated

set  of  1,177,690  GPS  points  (67%)  and  a  test  set  of  the  remaining

training  time  of  the  best  NN,  RF  and  XGBoost  models  as  a  func-

588,245  points  (33%).  We  trained  four  types  of  models,  including

tion of sample size. From our entire dataset of 1,177,690 GPS points

wKNNs, NNs, RFs and BCTs and we classified the test set with each

we  sampled  {1000;  5000;  10,000;  50,000;  100,000;  500,000;

model type.

1,000,000} points without replacement and we trained each model

For  the  wKNNs  we  trained  over  a  grid  of k ∈ {5, 6, … , 19, 20}

to the subsampled data, measuring the training time for each. We did

using rectangular, triangular, Epanechnikov and gaussian kernels, for

not consider wKNN in this analysis, as computational time for that

a  total  of  16 × 4  =  64  combinations.  Prior  to  implementing  wKNN

method depends not only on the size of the training set but also the

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMethods in Ecology and Evolu(cid:13)on

    |  197

size of the test set. All computation times were measured on a desk-

misclassification  rate.  The  best  NN  combination  had  20  hidden

top computer with a Windows 10 operating system and 3.7GHz Intel

nodes,  a  decay  parameter  of  0.01  and  included  a  skip  layer;  this

Xeon W- 2145 processor with 8 cores and 128 (8 × 16) GB of RAM.

combination had a 32.1% test set misclassification rate. The best RF

tuning  parameter  combination  was  300  trees,  with  a  70%  column

and 100% row subsampling per cent and had a 14.5% misclassifica-

3.2.3  |  Variable relationships and importance

tion rate. See Appendix S3 for details on tuning parameter searches

For  the  best- performing  supervised  learning  method  we  created

ICE, PDP and SHAP plots, and we investigated variable importance

as measured by averaged absolute SHAP values for each predictor

4.2  |  Model assessment

and risk class. To avoid over- plotting, the ICE, PDP and SHAP plots

for all methods.

were created for a subsample of GPS points.

Following five-fold cross- validation, the best XGBoost model yielded

4  |  R E S U LT S

4.1  |  Model selection

86.2% overall correct classification of points (Table 1). Compared to

a noninformative accuracy rate of 60.5% (the prevalence of the ma-

jority  ‘high- risk’  class),  the  best  XGBoost  model  resulted  in  a  42%

improvement upon a noninformative model. The overall auROC was

high  (90.6%),  driven  by  especially  accurate  pairwise  classification

of  low- risk  flight  versus  the  other  two  risk  categories.  The  model

Of the SL methods we considered, NNs performed the worst, with

was  somewhat  less  accurate  at  distinguishing  high  risk  from  mod-

median misclassification rate of 33.1% (Figure 4a). wKNN performed

erate  risk,  but  still  had  a  relatively  high  pairwise  auROC  between

better  than  NNs,  with  a  20.0%  median  misclassification  rate.  The

these  two  classes.  The  best  RF  model  had  an  overall  performance

tree- based methods were the most accurate. RFs had a 14.7% me-

that was very close to the best XGBoost model with an overall five-

dian  misclassification  rate,  slightly  better  than  the  first  XGBoost

fold cross- validation accuracy of 86.1% (slightly worse than the best

tuning parameter search which yielded a 15.3% median misclassifi-

XGBoost  model)  and  overall  auROC  of  90.7%.  The  overall  auROC

cation rate. Refining the XGBoost grid search by reducing the shrink-

from the best random forest model was slightly better than the best

age  parameter  improved  the  XGBoost  performance  and  yielded  a

XGBoost model, which was entirely driven by a better moderate ver-

14.8% median misclassification rate.

sus  high  auROC  for  the  RF;  the  other  two  pairwise  auROCs  were

The lowest misclassification rate of the test set came from the

worse for RF than for XGBoost. There was a moderate drop- off in

second  XGBoost  grid  search,  with  a  14.4%  misclassification  rate
resulting  from  tuning  parameters  combination M = 26;  CSP  =  0.9;
RSP  =  1.0;  𝜂 = 0.1;  𝛾 = 0;  and 𝜆 = 2.  The  best  wKNN  combination
was a triangular kernel with k = 10 which yielded a 19.0% test set

performance between the tree- based methods and wKNN and NNs

performed drastically worse than any other method we considered.

For more details on the by- class performance of the best XGBoost

model, see Appendix S4.

F I G U R E   4 Results of tuning parameter grid searches. Each dot represents one tuning parameter combination. Red lines indicate median
values across parameter combinations.

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License198 |   Methods in Ecology and Evolu(cid:13)on

Model

Accuracy (%)

auROCoverall
(%)

XGBoost

RF

wKNN

NN

86.2

86.1

81.8

67.8

90.6

90.7

82.6

71.3

Pairwise auROC (%)

L v M L v H

M v H

96.0

95.4

83.6

73.1

97.7

97.5

94.5

78.6

78.1

79.3

69.7

62.2

Training
time
(minutes)

22.7

52.0

108.3

141.8

Abbreviations: L v M, low versus moderate risk; L v H, low versus high risk; M v H, moderate versus
high risk.

TA B L E   1 Comparison of classification
accuracy and training time of methods
used to classify risk of collision for bald
eagles with wind turbines in Iowa, USA.
Accuracies and auROCs are assessed via
five- fold cross- validation. auROCoverall
is computed by averaging the pairwise
auROCs (see Equation 2). ‘Training time’
refers to the time needed to train the
model on 2/3 and classify the remaining
1/3 of the data.

4.3  |  Computation time

The  wKNN  combinations  had  the  longest  median  training  time  at

111 min (Figure 4b), followed by the NNs at 61 min. However, there

was  much  variability  in  the  NN  training  times,  with  some  of  them

taking  over  3 h  to  train.  RFs  were  more  efficient  than  wKNN  and

NNs  with  a  median  training  time  of  30 min.  The  first  XGBoost  pa-

rameter combinations were relatively very fast, with a median train-

ing time of only 8.5 min. The second XGBoost searches were slower,

given the decreased 𝜂 and hence increased number of boosting itera-

tions  relative  to  the  first  search  (Figure  S2.E).  Nevertheless,  these

still had a median training time of only 17 min, faster than the median

for any non- XGBoost method.

Of  the  best  parameter  combinations  from  each  method,  the

best  XGBoost  method  was  significantly  faster  to  train  than  any  of

the other methods, at only 22.7 min (Table 1). The best RF method

took over twice as long at 52.0 min. The best wKNN and NN meth-

F I G U R E   5 Computational time of best SL models for various
subsample sizes. Subsamples were drawn without replacement
from the >1.7 GPS points. NN, neural net; RF, random forest.

ods were even more computationally demanding, taking 108.3 and

In general as d2 water increased, there were higher contributions to

141.8 min  to  train  respectively.  Finally,  as  the  subsample  size  in-

low- risk  outputs  whereas  for  small  values  of  d2  water  there  were

creased, the training time for the best NN and RF increased much

very large contributions to high- risk outputs (Figure 6b). Accordingly,

more drastically than for the best XGBoost model, with the training

the shape of the relationship of the modelled class outputs with d2

time for NN appearing to initially increase almost quadratically with

water was very similar for ICE, PDP and SHAP plots.

subsample size (Figure 5).

The partial dependence of multiple class probabilities can be over-

laid  on  the  same  plot  to  provide  a  clearer  interpretation  of  marginal

relationships with predicted classes (Figure S4). This approach worked

4.4  |  Variable importance and relationships

especially well for visualizing relationships with categorical predictors;

for  example,  Figure  S4  shows  that  high- risk  flight  was  more  preva-

Given that the XGBoost model described in Section 4.1 resulted in the

lent in the winter than summer months. Further exploration of SHAP

most accurate test set predictions, we further investigated the variable

values  provided  important  insight  into  interactions  among  variables

relationships and importance with this model fit to the entire dataset.

(Figure  7).  Here,  the  SHAP  contributions  to  the  high- risk  class  out-

Of  the  10  environmental  and  two  state  predictors,  d2  water  and  d2

puts for d2 landfill are plotted versus the observed d2 landfill values.

landfill were the two most important quantitative modelling variables

A  marginal  relationship  of  the  high- risk  outputs  with  d2 landfill  does

as determined by averaging the absolute SHAP values across all risk

not provide much insight into this relationship, whereas faceting the

classes  for  a  subsample  of  10,000  GPS  points  (Figure  S3).  TPI  and

observations by month illustrates that the relationship of high- risk out-

northness were the least impactful quantitative variables. Given that

put with d2 landfill varies somewhat by month; for example in June the

one- hot encoding of the factor variables month and stage results in as

closer to landfills, the lower the contributions to high- risk output.

many encodings as there are levels of each variable, directly comparing

overall contributions of the factor and quantitative variables is difficult.

PDP, ICE and SHAP plots suggested that as d2 water increases,

5  |  D I S C U S S I O N

the predicted probability of high- risk flight decreased while the pre-

dicted probability of low- risk flight decreases (Figure 6a). The pre-

We  have  presented  a  review  of  SL  methods  for  classifying  an  ani-

dicted probabilities of moderate- risk flight were relatively constant.

mal's  polytomous  behaviour  from  environmental  features,  and  we

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMethods in Ecology and Evolu(cid:13)on

    |  199

F I G U R E   6 Visualizations of the relationship between: (a) modelled class probabilities and distance to water ( d2 water), using individual
conditional expectations (ICEs) and partial dependence plots (PDPs); (b) contributions to class outputs (SHAP values) and distance to water.
ICE plots use a sample of 5000 and SHAP plots a sample of 10,000 GPS points. Vertical lines at base of plots represent deciles of d2 water
distribution. In (a), each grey line is one GPS point, predicted at a fixed sequence along the range of d2 water while holding all other variables
measured at that GPS point constant at their observed values. The yellow line indicates the partial dependence of each class probability on
d2 water (the average of the individual lines). In (b), each individual point is a GPS point, and the y- axes are the contributions to the modelled
class outputs given that GPS point's d2 water value relative to the average. The yellow line is a scatterplot smoother. In both plots, variability
in the individual lines or points represents interactions with other predictor variables.

illustrate these approaches using a case study of nearly two million

that  beat  the  best  RFs,  while  still  requiring  only  a  fraction  of  the

GPS  data  points.  While  weighted  k- nearest  neighbours  performed

computation  times  of  the  RFs.  XGBoost  also  affords  its  users  the

reasonably  well  from  the  standpoint  of  predictive  accuracy,  be-

ability  to  investigate  relationships  between  class  predictions  and

cause this method lacks a model with which to define predictions,

predictors, either with ICE/PDP plots or SHAP plots. The built- in in-

it is impossible with this tool to investigate variable importance and

tegration of SHAP value computation in the xgboost r package adds

relationships. Of the modelling approaches, our results point to tree-

to the appeal of this method.

based  methods  (RFs  and  boosted  trees  via  XGBoost)  as  the  most

It is important to emphasize that any effective SL model for clas-

accurate and scalable with large datasets. Tree- based methods also

sifying animal behaviour from land features should only be used to

offer the possibility  of  subsequent  investigation  of  variable impor-

predict behaviour in similar geographies as those used to train the

tance and relationships.

model. New geographies, with potentially new distributions of land

Of  the  tree- based  methods,  XGBoost  clearly  offers  the  most

features, will require separate SL methods. This again reiterates the

promise  for  animal  behaviour  classification  with  large  datasets.

benefit of XGBoost, which makes it computationally feasible to train

While we initially wanted to include more than 300 trees in our RF

new models on these new geographies.

grid  search,  doing  so  resulted  in  computational  failure  given  the

One limitation of SL methods in general is they do not explicitly

size  of  our  training  set. While  our  first  parameter  search  involving

account  for  correlation  between  observations.  In  our  case  study,

XGBoost did not quite beat out RFs for test set classification accu-

there is certainly strong temporal autocorrelation in the GPS points.

racy, its much faster computational time allowed us to hone- in on a

While it is very likely that including the lagged behavioural state of

reasonable first- grid parameter combination. Subsequent reduction

previous  GPS  points  to  predict  current  behaviour  would  improve

of the learning rate parameter resulted in several XGBoost models

prediction  accuracy,  it  would  render  the  models  unusable  from  a

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License200 |   Methods in Ecology and Evolu(cid:13)on

F I G U R E   7 High-  risk class SHAP values, plotted by distance to landfill (d2 landfill), for a subsample of 10,000 GPS points. (a) The overall
relationship is plotted; (b) the relationships are faceted by month. In each plot, the lines represent scatterplot smooths. Vertical lines at base
of plots represent deciles of d2 landfill distribution.

conservation  standpoint.  Since  the  overarching  goal  of  our  mod-

in  these  situations.  We  offer  a  tutorial  to  assist  researchers  inter-

els  was  to  use  land  features  to  predict  animal  behaviour  in  order

ested in implementing this powerful method (Bergen, 2022).

to determine land types where birds are at greater risk from wind

turbines,  including  animal- level  data  in  our  models  would  make  it

AU T H O R C O N T R I B U T I O N S

impossible to predict these behaviours using land features alone. It

All  authors  jointly  developed  the  concept  for  this  research,  raised

is also important to note that accounting for temporal autocorrela-

funding to support the study. Silas Bergen led conceptualization and

tion is not essential in SL applications where the goal is optimized

implementation of supervised learning models, with assistance from

prediction accuracy rather than well- calibrated inference (the goal

Manuela M. Huso and other coauthors. Silas Bergen led writing of

of more traditional modelling situations). That said, SL applications

the  manuscript  with  assistance  from  all  other  coauthors.  Tricia  A.

where land predictors do not need to be separated from other po-

Miller  and  Sara  Schmuecker  led  fund  raising  for  and  collection  of

tential animal- based predictors could very well improve prediction

field data, with assistance from Silas Bergen, Melissa A. Braham and

accuracy  by  using  lagged  behavioural  states  to  classify  current

Todd  E.  Katzner.  Melissa  A.  Braham  led  management  of  telemetry

ones.

data, with assistance from Tricia A. Miller.

In our case study, all SL models had the most difficulty separat-

ing the high-  from moderate- risk classes. Both of these behaviours

AC K N OW L E D G E M E N T S

occurred  at  low  elevations  (<250 m  above- ground  level)  and  dif-
fered only in their membership in one of three behavioural modes

A large number of people assisted with data collection or provided

some type of logistical support for this project. These include D.

identified by k- means clustering (see Appendix S1). Given that many

Becker, M.J. Lanzone, T.A. Miller, J. J. Goodman, T. Goodman, V.

points  on  cluster  boundaries  may  be  quite  similar  to  each  other

Goodman,  J.  Slater  and  family,  B.  Massey,  S.  Hawks,  R.  Watson,

while  assigned  to  different  clusters,  this  uncertainty  may  result  in

C.  McClure,  J.  Haas,  J.  Cancilla,  S.  Shepherd,  Jeff  Cooper,  Teryl

the relatively poorer performance of our SL models in separating the

Grubb,  Russ  Horton,  Meghan  Judkins,  Iowa  Tribe,  Oklahoma

high-  from moderate- risk GPS points.

Department of Wildlife Conservation, World Bird Sanctuary, The

Our work is important to concept development because of the

Peregrine  Fund,  Excelon  Quad  Cities  Generating  Station,  Origin

paucity  of  ‘big  data’  animal  movement  studies  in  which  millions  of

Wind  Energy,  LLC,  MacBride  Raptor  Center,  Iowa  Department

polytomous behaviours have been successfully predicted from en-

of  Natural  Resources,  USFWS  Michigan  Ecological  Services

vironmental  features  with  subsequent  exploration  of  relationships

Field  Office,  USFWS  La  Crosse  Fish  and  Wildlife  Conservation

between  the  behaviours  and  environmental  features.  Our  results

Office,  USFWS  Columbia  Fish  and  Wildlife  Conservation  Office,

suggest XGBoost should be considered as an early modelling option

Port  Louisa  National  Wildlife  Refuge,  Upper  Mississippi  River

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseNational  Wildlife  and  Fish  Refuge,  Savanna  District  and  the  en-

Breiman,  L.  (2001).  Random  forests.  Machine  Learning,  45(1),  5– 32.

Methods in Ecology and Evolu(cid:13)on

    |  201

tire  staff  of  the  USFWS  Illinois- Iowa  Ecological  Services  Field

Office. Funding for data collection was provided by the American

Eagle Foundation, Mid- American Energy, American Wind Wildlife

Institute,  Avian  Power  Line  Interaction  Committee,  ITC  Holdings

Corporation,  the  Arconic  Foundation,  the  USFWS  Minnesota-

Wisconsin  Ecological  Services  Field  Office,  USFWS  Region  3

Migratory Birds Program and the authors' organizations. Funding

for the analysis was provided by the American Eagle Foundation

and  the  authors'  organizations.  Any  use  of  trade,  firm,  or  prod-

uct  names  is  for  descriptive  purposes  only  and  does  not  imply

endorsement  by  the  U.S.  Government.  Findings  and  conclusions

in this article are those of the authors and do not necessarily rep-

resent the views of the USFWS.

C O N FL I C T O F I N T E R E S T

None.

P E E R R E V I E W

The peer review history for this article is available at <https://publo>

ns.com/publo n/10.1111/2041- 210X.14019.

DATA  AVA I L A B I L I T Y S TAT E M E N T

Full  data  available  from  USGS  Survey  Data  Release  (Braham

et al., 2021). An R Markdown tutorial demonstrating implementation

of  XGBoost  including  model  selection,  assessment,  interpretation

and plotting using a subset of 10,000 GPS points is also available in

a Zenodo repository (Bergen, 2022).

O R C I D

Silas Bergen

 <https://orcid.org/0000-0003-3257-4415>

Manuela M. Huso

 <https://orcid.org/0000-0003-4687-6625>

Adam E. Duerr

 <https://orcid.org/0000-0002-6145-8897>

Melissa A. Braham

 <https://orcid.org/0000-0001-7917-1889>

Tricia A. Miller

 <https://orcid.org/0000-0001-5152-9789>

Todd E. Katzner

 <https://orcid.org/0000-0003-4503-8435>

R E F E R E N C E S

Bergen,  S.  (2022).  Tutorial  for  implementing  XGBoost  to  classify  poly-
tomous  animal  behavior  from  environmental  features  (v1.0.0).
Zenodo, <https://doi.org/10.5281/zenodo.7126770>

Bergen,  S.,  Huso,  M.  M.,  Duerr,  A.  E.,  Braham,  M.  A.,  Katzner,  T.  E.,
Schmuecker,  S.,  &  Miller,  T.  A.  (2022).  Classifying  behavior  from
short- interval  biologging  data:  An  example  with  GPS  tracking  of
birds. Ecology and Evolution, 12, e08395. <https://doi.org/10.1002/>
ece3.8395

Braham,  M.  A.,  Miller,  T.  A.,  Schmuecker,  S.  J.,  Duerr,  A.  E.,  Bergen,  S.,
& Katzner, T. E. (2021). Data derived from GPS tracking of free- flying
bald eagles (Haliaeetus leucocephalus). U.S. Geological Survey Data
Release. <https://doi.org/10.5066/P9HZZZ26>

Brandes,  S.,  Sicks,  F.,  &  Berger,  A.  (2021).  Behaviour  classification
on giraffes (Giraffa camelopardalis) using machine learning algo-
rithms on triaxial acceleration data of two commonly used GPS
devices  and  its  possible  application  for  their  management  and
conservation.  Sensors,  21(6),  2229.  <https://doi.org/10.3390/>
s2106 2229

<https://doi.org/10.1023/A:10109> 33404324

Browning, E., Bolton, M., Owen, E., Shoji, A., Guilford, T., & Freeman,
R.
learn-
(2018).  Predicting  animal  behaviour  using  deep
ing:  GPS  data  alone  accurately  predict  diving  in  seabirds.
Methods  in  Ecology  and  Evolution,  9(3),  681– 692.  <https://doi>.
org/10.1111/2041- 210X.12926

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting sys-
tem. Proceedings of the 22nd ACM SIGKDD international conference
on  knowledge  discovery  and  data  mining,  785– 794.  <https://doi>.
org/10.1145/29396 72.2939785

Chen, T., He, T., Benesty, M., Khotilovich, V., Tang, Y., Cho, H., Kailong, C.,
Mitchell, R., Cano, I., Zhou, T., Li, M., Xie, J., Lin, M., Geng, Y., Yutian,
L.,  &  Yuan,  J.  (2022).  xgboost:  Extreme  gradient  boosting.  https://
CRAN.R- proje ct.org/packa ge=xgboost

Clarke, T. M., Whitmarsh, S. K., Hounslow, J. L., Gleiss, A. C., Payne, N.
L.,  &  Huveneers,  C.  (2021).  Using  tri- axial  accelerometer  loggers
to  identify  spawning  behaviours  of  large  pelagic  fish.  Movement
Ecology, 9(1), 26. <https://doi.org/10.1186/s4046> 2- 021- 00248 - 8

Doshi- Velez, F., & Kim, B. (2017). Towards a rigorous science of interpreta-
ble machine learning. <https://doi.org/10.48550/> arXiv.1702.08608

Friedman,  J.  H.  (2001).  Greedy  function  approximation:  A  gradient
boosting machine. The Annals of Statistics, 29(5), 1189– 1232.
Hand, D. J., & Till, R. J. (2001). A simple generalisation of the area under
the ROC curve for multiple class classification problems. Machine
<https://doi.org/10.1023/A:10109>
Learning,
20819831

171– 186.

45(2),

Hastie, T., Tibshirani, R., & Friedman, J. H. (2009). The elements of statisti-
cal learning: Data mining, inference, and prediction (2nd ed.). Springer.
Hechenbichler,  K.,  &  Schliep,  K.  (2004).  Weighted  k- nearest- neighbor
techniques and ordinal classification. Sonderforschungsbereich 386,
Paper 399.

Kays, R., Crofoot, M. C., Jetz, W., & Wikelski, M. (2015). Terrestrial animal
tracking  as  an  eye  on  life  and  planet.  Science,  348(6240).  https://
doi.org/10.1126/scien ce.aaa2478

Leoni, J., Tanelli, M., Strada, S. C., & Berger- Wolf, T. (2020). Ethogram-
based  automatic  wild  animal  monitoring  through  inertial  sen-
sors  and  GPS  data.  Ecological  Informatics,  59,  101112.  <https://doi>.
org/10.1016/j.ecoinf.2020.101112

Liaw, A., & Wiener, M. (2002). Classification and regression by random-

Forest. R News, 2(3), 18– 22.

Lundberg,  S.,  &  Lee,  S.  I.  (2017).  A  unified  approach  to  interpreting
model  predictions.  arXiv,  1705.07874.  <https://doi.org/10.48550/>
arXiv.1705.07874

Mercker, M., Schwemmer, P., Peschko, V., Enners, L., & Garthe, S. (2021).
Analysis of local habitat selection and large- scale attraction/avoid-
ance based on animal tracking data: Is there a single best method?
Movement  Ecology,  9(1),  20.  <https://doi.org/10.1186/s4046> 2- 021-
00260 - y

Molnar, C. (2022). Interpretable Machine Learning: A guide for making black
box models explainable (2nd ed.). <https://chris> tophm.github.io/inter
preta ble- ml- book/

Muñoz- Mas,  R.,  Gil- Martínez,  E.,  Oliva- Paterna,  F.  J.,  Belda,  E.  J.,  &
Martínez- Capel,  F.  (2019).  Tree- based  ensembles  unveil  the  mi-
crohabitat  suitability  for  the  invasive  bleak  (Alburnus  alburnus  L.)
and  pumpkinseed  (Lepomis  gibbosus  L.):  Introducing  XGBoost  to
eco- informatics.  Ecological  Informatics,  53,  100974.  <https://doi>.
org/10.1016/j.ecoinf.2019.100974

Patterson, A., Gilchrist, H. G., Chivers, L., Hatch, S., & Elliott, K. (2019). A
comparison of techniques for classifying behavior from accelerom-
eters for two species of seabird. Ecology and Evolution, 9(6), 3030–
3045. <https://doi.org/10.1002/ece3.4740>

Schliep, K., Hechenbichler, K., & Lizee, A. (2016). kknn: Weighted k- nearest
[Computer  software].  <https://CRAN.R-> proje

neighbors
ct.org/packa ge=kknn

(1.3.1)

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License202 |   Methods in Ecology and Evolu(cid:13)on

Schmuecker,  S.  J.,  Becker,  D.  A.,  Lanzone,  M.  J.,  Fogg,  B.,  Romano,  S.
P., Katzner, T. E., & Miller, T. A. (2020). Use of upland and riparian
areas  by  wintering  bald  eagles  and  implications  for  wind  energy.
The Journal of Wildlife Management, 84(8), 1578– 1589. <https://doi>.
org/10.1002/jwmg.21927

Sur, M., Woodbridge, B., Esque, T. C., Belthoff, J. R., Bloom, P. H., Fisher,
R.  N.,  Longshore,  K.,  Nussear,  K.  E.,  Tracey,  J.  A.,  Braham,  M.  A.,
&  Katzner,  T.  E.  (2021).  Linking  behavioral  states  to  landscape
features  for  improved  conservation  management.  Ecology  and
Evolution, 11(12), 7905– 7916. <https://doi.org/10.1002/ece3.7621>

Valletta, J. J., Torney, C., Kings, M., Thornton, A., & Madden, J. (2017).
Applications  of  machine  learning  in  animal  behaviour  studies.
Animal  Behaviour,  124,  203– 220.  <https://doi.org/10.1016/j.anbeh>
av.2016.12.005

Venables, W. N., Ripley, B. D., & Venables, W. N. (2002). Modern applied

statistics with S (4th ed.). Springer.

Wijeyakulasuriya, D. A., Eisenhauer, E. W., Shaby, B. A., & Hanks, E. M.
(2020). Machine learning for modeling animal movement. PLoS ONE,
15(7), e0235750. <https://doi.org/10.1371/journ> al.pone.0235750

Yu, H., Deng, J., Nathan, R., Kröschel, M., Pekarsky, S., Li, G., & Klaassen,
M.  (2021).  An  evaluation  of  machine  learning  classifiers  for

next- generation,  continuous- ethogram  smart  trackers.  Movement
Ecology, 9(1), 15. <https://doi.org/10.1186/s4046> 2- 021- 00245 - x

S U P P O R T I N G I N FO R M AT I O N

Additional  supporting  information  can  be  found  online  in  the

Supporting Information section at the end of this article.

How to cite this article: Bergen, S., Huso, M. M., Duerr, A. E.,

Braham, M. A., Schmuecker, S., Miller, T. A., & Katzner, T. E.

(2023). A review of supervised learning methods for classifying

animal behavioural states from environmental features.

Methods in Ecology and Evolution, 14, 189–202. <https://doi>.

org/10.1111/2041-210X.14019

BERGEN et al. 2041210x, 2023, 1, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14019> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
