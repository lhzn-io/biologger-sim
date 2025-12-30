Received: 4 December 2024 |  Accepted: 25 February 2025
DOI: 10.1111/2041-210X.70025

R E S E A R C H   A R T I C L E

Improved order selection method for hidden Markov models:
A case study with movement data

Fanny Dupont1  |   Marianne Marcoux2 |   Nigel Hussey3  |   Marie Auger- Méthé1,4

1Department of Statistics, University
of British Columbia, Vancouver, British
Columbia, Canada

2Freshwater Institute, Fisheries and
Oceans Canada, Winnipeg, Manitoba,
Canada

3Department of Integrative Biology,
University of Windsor, Windsor, Ontario,
Canada

4Institute for the Oceans and Fisheries,
University of British Columbia, Vancouver,
British Columbia, Canada

Correspondence
Fanny Dupont
Email: <fanny.dupont@stat.ubc.ca>

Marie Auger-Méthé
Email: <Auger-methe@stat.ubc.ca>

Funding information
Canadian Research Chairs program, Tier
II; BC Knowledge Development Fund;
Canada Foundation for Innovation's John
R. Evans Leaders Fund, Grant/Award
Number: 37715; Canadian Network for
Research and Innovation in Machining
Technology, Natural Sciences and
Engineering Research Council of Canada,
Grant/Award Number: RGPNS 503527-
2017, RGPNS- 2024, RGPIN- 2017- 03867
and RGPIN- 2024- 03984

Abstract

1. Hidden  Markov  models  (HMMs)  are  a  versatile  statistical  framework  commonly

used in ecology to characterize behavioural patterns from animal movement data.

In HMMs, the observed data depend on a finite number of underlying hidden states,

generally interpreted as the animal's unobserved behaviour. The number of states

is a crucial hyperparameter, controlling the trade- off between the ecological inter-

pretability of behaviours (fewer states) and the goodness of fit of the model (more

states). Selecting the number of states, commonly referred to as order selection, is

notoriously challenging. Common model selection metrics, such as Akaike informa-

tion criterion (AIC) and Bayesian information criterion (BIC), often perform poorly in

determining the number of states, particularly when models are misspecified.

2. Building on existing methods for HMMs and mixture models, we propose a double

penalised maximum likelihood estimate (DPMLE) for the simultaneous estimation of

the number of states and parameters of non- stationary HMMs. The DPMLE differs

from traditional information criteria by using two penalty functions on the station-

ary probabilities and state- dependent parameters. For non- stationary HMMs, for-

ward and backward probabilities are used to approximate stationary probabilities.

3. Using a simulation study that includes scenarios with additional complexity in the

data, we compare the performance of our method with that of AIC and BIC. We

also illustrate how the DPMLE differs from AIC and BIC using narwhal (Monodon

monoceros) movement data.

4. The proposed method outperformed AIC and BIC in identifying the correct num-

Handling Editor: Chris Sutherland

ber of states under model misspecification. Furthermore, its capacity to handle

non- stationary dynamics allowed for more realistic modelling of complex move-

ment data, offering deeper insights into narwhal behaviour. Our method is a pow-

erful tool for order selection in non- stationary HMMs, with potential applications

extending beyond the field of ecology.

K E Y W O R D S
animal movement, double penalised maximum likelihood estimate (DPMLE), HMM,
information criteria, non- stationary, order selection, SCAD

This is an open access article under the terms of the Creative Commons Attribution License, which permits use, distribution and reproduction in any medium,
provided the original work is properly cited.
© 2025 The Author(s). Methods in Ecology and Evolution published by John Wiley & Sons Ltd on behalf of British Ecological Society.

Methods Ecol Evol. 2025;16:1215–1227.

wileyonlinelibrary.com/journal/mee3

 |  1215

1216 |

1  |  I NTRO D U C TI O N

model  selection  criteria  have  been  proposed.  The  integrated  com-

pleted likelihood criterion (ICL; Biernacki et al., 2000) is promising,

Understanding  animals'  movement  and  behaviour  is  crucial  for

but is too sensitive to the overlap between the state- dependent dis-

conservation  and  is  therefore  driving  the  rapid  development  of

tributions and tends to underestimate the order (Pohle et al., 2017).

animal movement modelling (Sutherland, 1998). One of the most

The cross- validated likelihood criterion circumvents the theoretical

popular modelling approaches is the hidden Markov model (HMM),

challenges associated with information criteria (Smyth, 2000), but is

a  versatile  statistical  tool  for  modelling  time  series  (McClintock

computationally  challenging  and  does  not  outperform  BIC  (Celeux

et  al.,  2020;  Patterson  et  al.,  2010).  Advances  in  tracking  tech-

& Durand, 2008).

nology  and  biologging  data  resolution  have  increased  HMMs'

Two- stage procedures described above can be computationally

popularity in movement ecology, and they are now widely used to

expensive,  particularly  as  model  complexity  and  sample  size  in-

infer animals' behaviour from telemetry data (Glennie et al., 2023;

crease. Such a situation is likely to arise with increasingly complex

Zucchini  et  al.,  2017).  HMMs  assume  that  the  observed  time  se-

animal  movement  data.  de  Chaumaray  et  al.  (2024)  introduced  a

ries  arises  from  a  sequence  of  unobserved  states,  evolving  in  a

one- stage  approach  for  order  selection  in  non- parametric  HMMs,

finite state space. The states usually carry information about the

avoiding  the  inefficiencies  and  computational  burden  of  a  two-

phenomenon of interests, such as the survival status (McClintock

stage  procedure.  However,  it  cannot  accommodate  models  with

et  al.,  2020)  or  the  behavioural  state  of  an  animal  (Morales

time- varying  covariates  (hence  non- stationary  HMMs).  Penalised

et  al.,  2004).  Movement  ecologists  commonly  seek  to  study  the

maximum  likelihood  estimators  are  alternative  one- stage  methods

environmental  conditions  that  may  trigger  switches  between

(Gassiat & Boucheron, 2003; Mackay, 2002). Chen and Khalili (2008)

these states (e.g. time of the day in Ngô et al., 2019).

argued  that  while  some  penalised  methods  for  order  selection  in

In  practice,  when  fitting  an  HMM  to  movement  data,  the  pa-

HMMs  prevent  overfitting  of  type  I  (i.e.  estimating  states  that  ani-

rameters for both the observation and the hidden processes, along

mals rarely occupy), they do not address overfitting of type II, where

with  the  number  of  hidden  states,  need  to  be  estimated.  While

component  densities  overlap.  They  proposed  a  method  using  the

HMMs can be applied to data using various inferential frameworks

smoothly clipped absolute deviation (SCAD; Fan & Li, 2001) function

(see  Auger- Méthé  et  al.,  2021;  Leos- Barajas  &  Michelot,  2018  for

to overcome both overfitting types in mixture models. However, no

Bayesian methods), maximum likelihood inference is the most used

methods exist for non- stationary models, highlighting the need for

approach  to  fit  HMMs  in  ecology  (McClintock,  2021;  Zucchini

a universal statistical method for order selection in non- stationary

et  al.,  2017) and, as such, is the focus of this paper. However, se-

HMMs.

lecting the number of states, known as order selection, remains no-

This paper introduces an intuitive double penalised maximum

toriously challenging (Pohle et al., 2017). Order selection is crucial

likelihood  estimate  (DPMLE)  for  the  simultaneous  estimation  of

to control the trade- off between interpretability and the goodness

the order and parameters of non- stationary HMMs. It is built on

of fit of the model. The lack of universal tools often leads research-

the  method  proposed  in  Chen  and  Khalili  (2008)  to  estimate  the

ers  to  rely  on  model  validation  techniques  or  their  own  expertise

order of mixture models. Hung et al. (2013) introduced it for sta-

to choose, sometimes arbitrarily, an appropriate number of states.

tionary  HMMs,  where  it  outperformed  AIC  and  BIC  in  selecting

Consequently, many practitioners choose a number of states that is

the right number of states. We go further by extending this frame-

easily interpretable (e.g. DeRuiter et al., 2017). This order selection

work  to  non- stationary  HMMs,  which  incorporate  time- varying

problem with HMMs is similar to the challenges associated with es-

covariates  in  the  hidden  process,  and  evaluate  its  performance

timating the number of components of finite mixture models (Chen

using a simulation study with misspecification, since these situa-

& Khalili, 2008).

tions are common with animal movement data (Li & Bolker, 2017;

When estimating the parameters by maximum likelihood, stan-

Pohle et al., 2017). Here, we develop a double penalised likelihood

dard  tools  to  choose  between  models  with  different  numbers  of

method for order selection for non- stationary HMMs and explore

states  are  the  likelihood  ratio  test  and  information  criteria  (e.g.

for the first time the performance of such methods under model

Akaike information criterion—AIC, Bayesian information criterion—

misspecification.

BIC).  Existing  likelihood  ratio  methods  cannot  effectively  test  for

We illustrate the use of the DPMLE using movement data from

order selection in HMMs, leading many researchers to rely on infor-

narwhal  (Monodon  monoceros),  a  species  vulnerable  to  climate

mation criteria (Dannemann & Holzmann, 2008).

change, specifically by decreasing sea ice and associated increas-

The  conventional  approach  for  order  selection  in  HMMs  in-

ing predator presence and ship traffic (Breed et al., 2017; Pizzolato

volves a two- stage procedure: fitting models with varying numbers

et  al.,  2014).  Previous  studies  identified  ‘distance  to  shore’  as

of states and selecting the best- fitting model with model selection

an  important  covariate  for  narwhal  habitat  selection  (Kenyon

criteria (Celeux & Durand, 2008). AIC and BIC often perform poorly

et al., 2018; Ngô et al., 2019; Shuert et al., 2023). Thus, we inves-

in  selecting  the  order  of  HMMs,  particularly  when  applied  to  mis-

tigate  non- stationary  HMMs  that  include  distance  to  shore  and

specified models (i.e. the true generating process in not among the

compare  the  results  found  when  selecting  the  number  of  states

models compared; Li & Bolker, 2017; Pohle et al., 2017). Alternative

with our DPMLE method, AIC and BIC. To our knowledge, double

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons Licensepenalised likelihood methods have not yet been explored in animal

movement analyses.

2  |  M ATE R I A L S A N D M E TH O DS

2.1  |  Hidden Markov models

Consider  a  N⋆- state  HMM  describing  a  sequence  of  observations
Y ≔ Y 1:T =
 and its associated sequence of hidden states
  for  all  t ≤ T.  Transitions  be-
S1:T =
tween hidden states are driven by the N⋆ × N⋆ transition probability
)
matrix (t.p.m.) Γ =

Y 1, … , Y T
,  St ∈
)

S1, … , ST
(

1, 2, … , N⋆

}

(

𝛾 ij

{
i,j∈[1,N⋆]×[1,N⋆]:
)

(

ℙ

St+1 = i

St = j

= 𝛾 ij,

(

)

|

𝛾 ij = 1,

N⋆

j = 1
∑

with

(1)

and  satisfy  the  Markov  property.  The  initial  state  distribution,

𝜹 =

ℙ

S1 = 1

, … , ℙ

S1 = N⋆

, satisfies

(

(

)

(

))
N⋆

i = 1
∑

𝛿i = 1.

(2)

S1:T is homogeneous (i.e. time- independent). If there exists a row
vector 𝜋 that satisfies 𝜋Γ = 𝜋, the chain is further said to be station-

    |  1217

N⋆

𝛼t(j) =

𝛼t−1(i)𝛾 i,jfj

yt; 𝜽j

,

t = 2, … T

and

𝛼1(j) = 𝛿ifj

y1; 𝜽j

.

i=1
∑

N⋆

𝛽t(j) =

𝛾 j,ifi

yt+1; 𝜽j

(
)
𝛽t+1(i),

i=1
∑

(

)

t = 1, … T − 1 and

𝛽T (i) = 1.

(

)

The model described by Equation (3) is a standard HMM that can

be further extended to incorporate covariates in both processes. In

animal  movement,  covariates  are  generally  included  in  the  hidden

process (non- homogeneous HMM; Leos- Barajas & Michelot, 2018)

via a multinomial logit link as follows:

𝛾 (t)
ij =

ij

ec(t)
ec(t)

ik

,

k
∑

𝛽ij
0+

C

c=1
�
0

𝛽ij
c𝜔(t)
c ,

fori ≠ j.

otherwise,

(5)

(6)

c(t)
ij = ⎧
⎪
⎪
⎨
⎪
⎪
⎩

  is  the  vector  of  the C  covariates  at  time  t  and

, … , 𝜔(t)
𝜔(t)
where
C
1
, … , 𝛽ij
𝛽ij
𝛽ij =
  is  the  vector  of  regression  coefficients  for  the
(
C
0
transition probability 𝛾 (t)
ij , t ≥ 0. The vector of parameters to estimate
(
becomes  Ψ = (𝜹, 𝛽, Θ).  Non- homogeneous  HMMs  are,  by  definition,

)

)

ary and we commonly set 𝜹 = 𝜋 (Zucchini et al., 2017). The stationary

non- stationary.

probability, 𝜋, can be interpreted as the proportion of time an individual
spends in each state and is entirely determined by the t.p.m. If St = i,
⋅ ; 𝜽i
the conditional density of Y t is fi
, where 𝜽i is a state- dependent
parameter describing the state- dependent (also called emission) distri-

(
bution. The observations are assumed independent given the states.

)

Key features of interest in animal movement modelling include

the  state- dependent  distributions,  which  describe  movement  pat-

terns (e.g. speed, tortuosity), and the temporal structure, reflected

in  the  t.p.m.  (e.g.  behavioural  persistence  from  diagonal  entries).

Time- varying covariates help explain movement patterns and envi-

The likelihood can be written as follows (Zucchini et al., 2017):

ronmental drivers of behavioural transitions (McKellar et al., 2015;

ℒ(Ψ

y) ≔ ℒ = 𝜹ΓP

y1

ΓP

y2

… ΓP

yT

1,

(3)

Zucchini et al., 2017).

|

(

)

(

)

yt

(
with  vector  of  model  parameters Ψ = (𝜹, Γ, Θ), Θ =
P

 a N⋆ × N⋆ diagonal matrix with (i, i)th entry fi
We  consider  a  frequentist  approach,  which  involves  obtaining
)
y).  We  use  the

(
maximum  likelihood  estimates  ̂Ψ =argmax Ψ
expectation–maximization  (EM)  algorithm  (Baum  et  al.,  1970).  An

(
ℒ(Ψ

)
𝜽1, … , 𝜽N⋆

  and

yt; 𝜽i
(

)

)

.

2.1.1  |  Model selection criteria

Model  selection  is  a  crucial  step  to  maximize  predictive  accuracy

and  understand  mechanisms  driving  behaviour.  We  focus  on  the  AIC

EM iteration consists of an expectation (E) step, and a maximization

|

(Akaike, 1974) and BIC (Schwarz, 1978) since they are commonly used by

(M) step. It is based on rewriting the likelihood in terms of forward
probabilities  𝛼t(i) = ℙ
𝛽t(i) = ℙ
ward  and  backward  probabilities,  we  can  efficiently  compute  the

  and  backward  probabilities
, for all t ≤ T, i ≤ N⋆. By combining for-

Y t+1:T = yt+1:T ; St = j

Y 1:t = y1:t; St = j

(

)

(

)

posterior  probability  of  being  in  a  specific  state  at  a  specific  time,

given  the  entire  observed  sequence.  Thus,  Equation ( 3)  can  be  re-

written as follows (Zucchini et al., 2017):

ℒ =

N⋆

i = 1
∑

𝛼t(i)𝛽t(i).

Both 𝛼t and 𝛽t can be computed recursively using the forward–back-
ward algorithm as follows:

ecologists (Auger- Méthé et al., 2021). Although they arise from different

approaches, they have similar formulae. AIC is defined as follows:

AIC = − 2 log ℒ

̂Ψ

y

+ 2k,

(7)

(

)

where k is the number of estimated parameters in the model, y is the
ℒ(Ψ
observed  data  and  ̂Ψ =argmax Ψ
y)  the  MLE.  BIC  can  be  com-
puted as follows:

|

|

(4)

BIC = − 2 log ℒ

̂Ψ

y

+ k log(n),

(8)

(
where n  is  the  number  of  observations.  Lower  values  for  AIC  and

)

|

BIC  indicate  a  better  model.  Both  criteria  penalise  the  number  of

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1218 |

parameters through the second term of the equations. Since its pen-

alty  function  increases  with  the  sample  size,  BIC  better  balances

The  penalty  term  on  the  left  is  used  to  prevent  the 𝜋j's  (i.e.  sta-
tionary  probabilities)  with  small  values,  thus  penalising  states  in

the trade- off between parsimony and fit compared to AIC. This be-

haviour arises in our simulation study (see Supporting Information).

Theoretical justifications for the use of AIC and BIC for order selec-

tion in HMMs have not been derived yet. HMMs violate the standard

which  the  process  spends  little  time.  The  penalty  term  on  the
right uses a non- negative function p𝜆 that shrinks small Δ𝜇k's to 0,
thus  preventing  the  occurrence  of  similar  states  (i.e.  overlapping
state- dependent distributions). When extending the DPMLE to M

assumptions underlying the derivation of both information criteria, mak-

independent time series, −

p𝜆

Δ𝜇j

 is replaced by − M

p𝜆

Δ𝜇j

ing them unreliable for order selection. For example, under overestima-
tion (�N > N⋆ = 2), the assumption of a unique MLE does not hold (Drton
& Plummer, 2017; Watanabe, 2013). Besides, both AIC and BIC rely on

to  ensure  that  the  penalty  increases  as  the  likelihood  increases
�
�
with M. In animal movement analyses, p𝜆 could be applied to the
mean parameter, as overfitting of type II generally concerns state-

�

�

N−1

j = 1
∑

N−1

j = 1
∑

the assumption of the true model being in the set of candidate models.

dependent  distributions  with  close  means,  rather  than  overlap-

This assumption is inherent in the derivation of AIC and necessary for

ping tails (see Hung et al. (2013) for an example of its use on 𝜎 on

BIC to achieve consistency (i.e. selecting the true model as the sample

Gaussian HMMs).

size  increases;  Aho  et al., 2014).  However,  when  this  is  violated,  both

criteria tend to select additional states to compensate for misspecified

The DPMLE requires p𝜆 to be constant outside a neighbourhood
of  0  (Chen  &  Khalili,  2008).  Thus,  we  use  the  SCAD  function  and

model structures (Li & Bolker, 2017; Pohle et al., 2017). This behaviour is

refer  to  Hung  et  al.  (2013)  for  consistency  properties  of  the  order

problematic in ecological studies, where systems often exhibit complex

and parameter estimates in stationary HMMs. The SCAD function is

patterns that are difficult to capture with simplified models.

characterized by its derivatives as follows:

2.2  |  Likelihood- based double penalised method
for order selection

𝜆(x) = 𝜆𝟙
p�

x≤𝜆 + 𝜆

(a𝜆 − x)+
(a − 1)𝜆

𝟙

x>𝜆,

x > 0,

(11)

where 𝟙(.) is the characteristic function, a is a constant > 2 and 𝜆 ≥ 0
is a hyperparameter (see Supporting Information for a comparison of

We  propose  a  double  penalised  maximum  likelihood  estimate

the SCAD function to common penalty functions). For the remainder

(DPMLE) of the number of hidden states, based on the method de-

of  this  work,  we  assume  the  regularity  conditions  necessary  for  the

veloped by Chen and Khalili (2008) and Hung et al. (2013), adapted

consistency of the stationary DPMLE are met although they are often

to non- stationary HMMs. The main idea of the DPMLE is to remove

violated in practice (Chen et al., 2008).

virtually  empty  states  (overfitting  of  type  I)  and  merge  duplicate

states together (overfitting of type II).

Consider a stationary N⋆- state HMM described by Equation (3).
The  true  number  of  states N⋆  is  unknown  and  must  be  estimated.
From the order's upper bound N > N⋆, the double penalised method

2.2.1  |  Estimation

Stationary Markov chain

estimates,  by  minimizing  two  penalty  functions,  a  lower  or  equal

For stationary HMMs, we use a slightly modified version of the EM

order by first clustering and then merging similar states together.

procedure of Hung et al. (2013). The double penalised log- likelihood

Without  loss  of  generality,  we  describe  the  double  penalised

function to maximize can be written as:

procedure with state- dependent distributions characterized by two
, i ≤ N.  The  double  penalised  log- likelihood
𝜇i, 𝜎i
parameters:  𝜽i =
function is defined as:

(

)

̃l(Ψ

y) = l(Ψ

y) + CN

|

|

log 𝜋j −

N

j = 1
∑

N−1

j = 1
∑

p𝜆

Δ𝜇j

,

(

)

(9)

with Δ𝜇j = 𝜇j+1 − 𝜇j, for  j > 1, 𝜇1 ≤ 𝜇2 ≤ … ≤ 𝜇N, CN a constant > 0,
l(Ψ

y) and p𝜆 a penalty function.

y) = log ℒ(Ψ

The double penalised maximum likelihood method penalises: (1)

|

|

stationary probabilities to prevent small values of stationary proba-

N

j=1
∑

N

T

N

uj(1) log 𝜋j + CN

log 𝜋j+

vij(t) log 𝛾 ij

T

N

j=1
∑

t=2
∑
N−1

j,i=1
∑

+

uj(t) log fj

yt; 𝜽j

−

p𝜆

Δ𝜇j

t=1
∑

j=1
∑

(

j=1
∑

)

(

)

(12)

with uj(t) = 1  if  and  only  if  st = j, t ≤ T,  and vjk(t) = 1  if  and  only  if
st = j, and st−1 = k, for t ∈ (2, … , T). The E- Step at iteration p + 1 re-
places ui(t) and vij(t) by their conditional expectations based on the
(p)
previous parameter estimates  ̂Ψ
 and the observations, allowing

us to perform the maximization step as if the states were known.

bilities (overfitting of type I); and (2) state- dependent parameters to

We derive:

penalise the overlap between the component distributions (overfit-

ting of type II). The DPMLE is then:

̂ΨDPMLE = argmax

l(Ψ

Ψ (

|
with ̂N = number of distinct values of

N

N−1

y) + CN

log 𝜋j −

p𝜆

Δ𝜇j

j=1
∑

j=1
∑
̂𝜇1, … , ̂𝜇N

(

)
.

{

}

,

)

(10)

̂u(p+1)
j
⎧
⎪
̂v(p+1)
⎪
jk
⎨
⎪
⎪
⎩

(t) = 𝔼

uj(t) ∣ ̂Ψ

(p)

, Y = y

=

�

�

(p)
t (j)

,

̂𝛼(p)
t (j)̂𝛽
ℒ
̂Ψ

(p)

y

(13)

(t) = 𝔼

vjk(t) ∣ ̂Ψ

(p)

, Y = y

�
�
t−1(j)̂𝛾 (p)
= ̂𝛼(p)
jk fk
�

�

�

(p)
̂𝛽
t (k).

(p)

yt; ̂𝜽
k
�

�

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
(p)

 and ̂𝜶(p)
t

The notations ̂𝜷
 indicate that the parameter estimates from
the pth iteration were used for the derivation. Equation (12) at iteration
p + 1 becomes:

t

N

̂u(p+1)
j

N

T

N

(1) log 𝜋j + CN

log 𝜋j+

̂v(p+1)
ij

(t) log 𝛾 ij

j=1
∑
⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟
(I)

j,i=1
∑

t=2
∑

j=1
∑

T

N

+

̂u(p+1)
j

(t) log fj

yt; 𝜽j

−

p𝜆

Δ𝜇j

.

N−1

j=1
∑

t=1
∑
)
(
⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟
(II)

j=1
∑

)

(

    |  1219

log ̃𝜋j

(p)
̂𝜹

, 𝜷, ̂𝝁(p), ̂𝝈(p)

,

(

)
(17)

̂v(p)
ij (t) log 𝛾 (t)

(p+1)

̂𝜷

= argmax𝜷 T ̂
t=2
∑

T

N

j,i=1
∑

̃𝜋j(Ψ) =

1
T

ℙ

St = j

Y = y

=

1
Tℒ

t=1
∑

[

]

|

ij + CNN ̂
j=1
∑

T

𝛼t(j)𝛽t(j),

t=1
∑

where  the  parameters  to  estimate  are Ψ = (𝜹, 𝜷, 𝝁, 𝝈).  Importantly,  ̃𝝅

(14)

is only used during the maximization over 𝜷, where it is derived condi-

tionally on the observation parameters estimated at the current step.

Therefore, we maintain independent penalties for the observation and

state processes.

Since  non- stationary  HMMs,  by  definition,  do  not  have  sta-

j = 1
∑

(I) and (II) can be maximized separately since they depend on differ-

tionary  distributions,  various  methods  may  be  used  to  replace  𝝅.

ent parameters. We start by maximizing (I) with respect to Γ under

The  derivation  of  ̃𝝅  in  Equation ( 17)  is  motivated  by  the  fact  that

N

the constraint

𝜋j = 1. We improve the algorithm proposed by Hung

Hung et al. (2013) use the penalty on the stationary distribution to

et al. (2013) by using the fact that estimating 𝜋 essentially consists of

estimating Γ and derive 𝜋 as follows:

𝝅 = 1

IN − Γ + U

−1

,

(15)

(
with U the N × N matrix of ones.

)

ensure  that  no  state  is  empty.  Therefore,  we  use  estimates  of  the

proportion  of  time  spent  in  each  state  as  substitutes  for  station-

ary probabilities. This method is convenient since a gradient can be

computed. The number of operations involved in computing ̃𝝅(Ψ) is
of order TN2 (Zucchini et al., 2017). The Viterbi algorithm could po-
tentially  be  used  to  derive  ̃𝝅  (see  Supporting  Information),  but  the

Any non- penalised parameter (e.g. 𝝈) uses the classic EM algo-

gradient cannot be computed, limiting the use of gradient- descent

rithm, which usually requires numerical methods. We then maxi-
p+ 1
mize (II) with respect to Θ. Let ̂Ψ
2
(

, ̂𝝁(p), ̂𝝈(p+1)

̂𝝅(p+1), ̂Γ

(p+1)

 be

=

)

the vector of all updated parameters up to this point, at iteration
p + 1 . To obtain ̂𝝁(p+1) =
̂𝜇(p+1)
, we maximize a local ap-
1
proximation of the SCAD penalty evaluated in ̂Ψ
) with respect
(
(
to 𝜇 . This circumvents the non- smoothness of the SCAD penalty

(
, … , ̂𝜇(p+1)

p+ 1
2

)

)

N

methods to fit the model, and thus is not considered further. Other
𝜹ΓT and de-
approaches could be considered, such as using 𝝅 = lim
T → ∞
riving ̂𝝅 = 𝜹Γ(0)Γ(1) … Γ(T), but this would come with a higher compu-
tational complexity of at least O(TN2.37).

Manole  and  Khalili  (2021)  propose  the  Group- Sort- Fuse  (GSF)

procedure to adapt the DPMLE to the multivariate case (i.e. penalty

(Zou & Li,  2008). The maximization problem can then be written

applied to a multidimensional parameter). The GSF generalizes the

as follows:

argmax𝜇

T

N

t=2
�

j=1
�

p+ 1
2

̂u�
j

(t) log fj

�

yt; 𝜇j, ̂𝜎(p+1)
�

j

�

N−1

(16)

−

j=1
�

+ p�
𝜆

Δ̂𝜇(p)
j
�

Δ𝜇j − Δ̂𝜇(p)
Δ̂𝜇(p)
⎤
p𝜆
j
⎥
⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟
⎥
�
�
⎥
Δ𝜇j ;Δ̂𝜇(p)
⎥
�
⎥
⎥
with Δ̂𝜇j = ̂𝜇j+1 − ̂𝜇j, for  j > 1, 𝜇1 ≤ 𝜇2 ≤ … ≤ 𝜇N. Equation (16) can
⎦
be maximized with regular maximization algorithms. The approxima-

⎡
⎢
⎢
⎢
⎢
⎢
⎢
⎣

��

�

̃p𝜆

�

.

j

j

tion  guarantees  the  descent  property  of  the  EM- algorithm  (Zou  &

Li, 2008).

Non- stationary Markov chain by means of covariates

When  time- varying  covariates  are  included  in  the  hidden  process,

the  assumption  of  stationarity  no  longer  holds  since  the  model  is

time- dependent  and  the  stationary  DPMLE  described  cannot  be

applied. As such, the penalty to prevent overfitting of type I is ad-

justed, while the rest of the DPMLE and estimation of parameters,

except  for  𝜷,  remain  unchanged.  The  stationary  distribution  is  re-

placed by an estimate of the proportion of time spent in each states

̃𝝅, computed using forward and backward probabilities. At iteration
p + 1, ̂𝜷

 is updated as follows:

(p+1)

𝝁1, … , 𝝁N
natural ordering of 𝝁 =
ate space, using l2- norms, and cluster ordering 𝜏 as follows:

 on the real line to the multivari-

(

)

𝝁𝜏(1) = argmin𝝁i:i=1…N

𝝁i

2

𝝁𝜏(k) = argmin𝝁j ≠𝝁𝜏(i)∀i

𝝁j − 𝝁𝜏(k−1)
‖
‖

‖
‖

.

2

(18)

p𝜆  is  then  applied  to  the  difference  in  l2  norms  of  the  clustered
parameters.

‖
‖
‖

‖
‖
‖

The  choice  of  the  hyperparameters 𝜆  and CN  is  important  to  en-
sure  that  the  method  performs  well.  As  Hung  et  al.  (2013),  we  set
a = 3.7. 𝜆 and CN are chosen from a discrete set by a BIC- type criterion,
BICDPMLE, which follows the procedure by Wang et al. (2009) and Lin
and Song (2022) to select the pair of hyperparameters that minimize

− 2 log ℒ

̂ΨDPMLE
(

y

+ k log(n),

)

(19)

where  ̂ΨDPMLE ≠ ̂ΨMLE  is  the  vector  of  parameter  estimates  after  the
DPMLE procedure. The number of parameters k can be derived as follows:

|

k = dim

𝜽1

̂N + ̂N

̂N − 1

,

(

)

(

)

(20)

𝜽1

where dim

  corresponds  to  the  dimension  of 𝜽1  (i.e.  the  num-
ber of state- dependent parameters estimated for each state). 𝜆 is
expected to increase with the sample size and the choice of CN is

(

)

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1220 |

not expected to be crucial (Chen & Khalili,  2008). BICDPMLE could
potentially share the same limitations as BIC, such as overfitting
(i.e.  selecting 𝜆  and CN  close  to  0).  However,  under  misspecifica-
tion,  the  issue  lies  with  the  likelihood,  that  grows  with  the  num-

distributions),  commonly  used  to  model  step

lengths

(e.g.

McClintock,  2021;  Pohle  et  al.,  2017),  across  all  scenarios.  The

baseline  model  used  is  a  stationary  gamma- HMM,  to  which  ad-

ditional  structure  (under  different  scenarios)  is  incorporated

ber of states (Cai et al., 2021), and often faster than BIC's penalty

(Figure  1).  Scenarios  1,  2  and  6  generate  the  time  series  of  only

as  shown  in  our  simulations.  DPMLE  specifically  targets  overfit-

one individual, while scenarios 3, 4 and 5 use the same parameters

ting  in  likelihoods  during  order  selection  (i.e.  penalising  virtually
empty or duplicate states). By combining it with BICDPMLE through
 and ̂N, we directly address overfitting with too many
ℒ
states and enable BICDPMLE to better balance model parsimony and
)
fit when selecting hyperparameters.

̂ΨDPMLE

(

y

|

2.3  |  Simulation study

We

implemented  a  simulation  framework  based  on  Pohle

et  al.  (2017).  We  use  similar  scenarios,  each  exploring  a  type  of

complexity commonly found in animal movement data: (1) bench-

mark  (no  misspecification),  (2)  outliers,  (3)  individual  heteroge-

neity  in  the  hidden  process,  (4)  individual  heterogeneity  in  the

to generate a time series for 10 independent individuals. We ex-
plore two sample sizes: T ∈ {5000, 12,000} .

Scenario 1 aims to show the performance of the methods with-

out  misspecification  (Figure  1a).  The  data  are  generated  follow-

ing  a  standard  three- state  stationary  gamma–HMM  with  means
= (1.5, 4, 12). The t.p.m.
𝜇1, 𝜇2, 𝜇3
is
(

= (1, 3, 5.5) and shapes

s1, s2, s3

)

(

)

0.8 0.1 0.1

.

Γ = ⎛
0.1 0.8 0.1
⎜
⎜
0.1 0.1 0.8
⎜
⎜
⎜
⎝

⎞
⎟
⎟
⎟
⎟
⎟
⎠

These mean and shape values were selected because the ICL cri-

observed  process,  (5)  violation  of  the  conditional  independence

terion  outperforms  BIC  and  AIC  for  most  scenarios,  but  performs

assumption and (6) temporal variation in the hidden process. We

poorly in selecting the right number of states under this setting (Pohle

simulate  three- state  gamma- HMMs  (i.e.  gamma  state- dependent

et al., 2017). Scenario 2 incorporates outliers in the observations by

(a)

(b)

(c)

(d)

(e)

(f)

F I G U R E   1 Simulation scenarios: State 1 (orange), state 2 (blue) and state 3 (green).

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License    |  1221

adding uniformly distributed random errors from the interval

10, 20

to  0.5%  of  the  data  simulated  with  the  framework  of  scenario  1
]
(Pohle et al., 2017). To include inter- individual differences (e.g. male/

[

female), scenario 3 adds discrete random effects in the hidden pro-
cess. We simulate M = 10 individuals with equal time- series length T

. Discrete random effects in the hidden process assume that the time
series  are  clustered  in K > 1  components,  where  each  component

for efficient convergence despite the reduced exploration. We use
random search with BICDPMLE to select hyperparameters, exploring
50 uniform values of 𝜆 and CN within log M𝜆 ∈
.
We do not explore CN in the log scale since the penalised likelihood
]
method  is  not  sensitive  to  the  choice  of CN  (Chen  &  Khalili,  2008;
Hung et al., 2013).

 and CN ∈

1, 5

1, 5

[

]

[

For each scenario and sample size, 100 datasets are generated,

has its t.p.m. and the members of the same component share a com-

and the success rates (percentage (%) of correctly estimated number

mon set of parameters (DeRuiter et al., 2017; McClintock, 2021). We
consider K = 2 with likelihood:

M

K

ℒ

mix =

𝛿(k)Γ(k)P

ym
1

Γ(k)P

ym
2

… Γ(k)P

ym
T

1𝜈(k),

(21)

m = 1
∏

k = 1
∑

(

)

(

)

(

)

of states) of each method are compared. Each simulation run corre-

sponds to a specific dataset, scenario and sample size, resulting in a

total of 100 datasets × 6 scenarios × 2 sample sizes = 1200 simula-
tion  runs.  The  upper  bound  for  the  number  of  states  across  every
method is set to N = 4 for computational feasibility of the simulation

framework.

with  Γ(1)  as  in  scenario  1  and  Γ(2) = ⎛
⎜
⎜
⎜
⎜
⎜
⎝

𝜈(1), 𝜈(2)

𝜈 =

0.1 0.1 0.8

0.1 0.8 0.1

0.1 0.1 0.8

⎞
⎟
⎟
⎟
⎟
⎟
⎠

,  where

2.4  |  Narwhal case study

= (0.5, 0.5)  is  the  vector  of  mixture  probabilities.

Scenario  4  includes  individual  heterogeneity  in  the  observa-

(

)

We demonstrate the use of our method on a narwhal case study.

The main goal is to estimate the number of behavioural states given

tion  process  (e.g.  juveniles  may  be  slower  than  adults;  DeMars

narwhal  movement  patterns  and  understand  their  relationship

et al., 2013). We follow the procedure defined by Pohle et al. (2017)

with environmental covariates. The study focuses on the region of

and generate the individual means of the gamma state- dependent

Qikiqtaaluk (Baffin) in Nunavut, Canada. During the summer 2017,

distribution  within  the  third  state  (Figure  1d)  with  a  log- normal
distribution  with  mean  and  variance  parameters  (log(5.5), 0.15).

Scenario 5 includes additional correlation in the observation pro-

18 narwhal were equipped with electronic tags in Tremblay Sound

(72°30′ N,  80°45′ W).  All  capture  and  tagging  protocols  were  ap-
proved  by  the  Fisheries  and  Oceans  Animal  Care  Committee  and

cess. We generate individuals with time- varying mean parameters

a  Licence  for  Scientific  Purposes  was  granted  (permit  #AUP  40,

for state 1 (Figure 1e), simulated using an auto- regressive process

S- 17/18- 1017- NU; protocols for narwhal's capture and tagging are

of order 1 with persistence 0.85. Scenario 6 incorporates tempo-

described in Shuert et al., 2022). We demonstrate the performance

ral  variation  in  the  transition  probabilities  (e.g.  foraging  is  more

of the proposed method for order selection using location data only

likely at night) with the cosinor function and a resolution of 15 min

for eight narwhal with FastLoc GPS data for a period of 2 months

(Figure 1f).

with  a  temporal  resolution  of  one  location  per  hour  (Figure  2).

Most  scenarios  (see  code  attached)  are  simulated  with  the

More details regarding data processing can be found in Supporting

simData  function  from  the  momentuHMM  package  (McClintock  &

Information.  Latitude  and  longitude  were  converted  into  step

Michelot, 2018) in R (R Core Team, 2021). We fit both stationary and

length and turning angle. Step lengths were modelled with gamma

non- stationary approaches, using ‘time of day’ as a covariate in the

distributions  and  turning  angles  with  von  Mises  distributions.  We

non- stationary methods, leading to a total of eight models. To intro-

used the GSF procedure to apply the DPMLE on multivariate state-

duce misspecification, the covariate ‘time of day’ in non- stationary

dependent  parameters  (i.e.  overlapping  states  were  characterized

methods  is  modelled  linearly  (1–96)  rather  than  with  the  periodic

by  vectors  of  mean  step  length  and  turning  angle  concentrations

functions  used  to  simulate  scenario  6.  For  consistency,  we  used  it

‘close’ to each other).

when fitting non- stationary approaches across all scenarios.

We  did  not  expect  the  number  of  states N⋆  to  exceed  4  (Ngô

To select the best model according to AIC and BIC, we fit HMMs

with  2,  3  and  4  states  to  each  simulated  dataset.  For  each  model,

we  follow  Pohle  et  al.  (2017)  and  explore  150  random  initial  pa-

rameter  values  for  the  optimization  procedure.  Finally,  we  com-

pare  the  fitted  models  across  the  different  numbers  of  states  and

et  al.,  2019;  Pohle  et  al.,  2017);  thus,  we  set  the  upper  bound  to
be N = 8 to allow N > N⋆. We explored 100 pairs of randomly sam-
pled  hyperparameters  𝜆  and  CN  and  selected  the  best  pair  with
BICDPMLE. We set a = 3.7. As highlighted in previous studies (Kenyon
et al., 2018; Ngô et al., 2019; Shuert et al., 2023), ‘distance to shore’

select  the  one  that  minimizes  each  criterion  (AIC  or  BIC).  For  the

has been identified as a key factor influencing narwhal habitat selec-

DPMLE methods, we use MLE estimates from random positions that

tion. To explore its role further, we investigated it as a covariate in the

maximized  the  likelihood  of  a  standard  HMM  as  initial  values  and

hidden process of non- stationary HMMs. We fitted standard HMMs

explore nine random initial values. Fewer random initial values are

using 30 random starting values and initialized both DPMLE meth-

explored compared to AIC and BIC since the method takes longer to

ods with MLE estimates. Due to computational constraints, only 10

converge  and  has  MLE  estimates  for  starting  parameters,  allowing

random starting values were explored for the DPMLE methods.

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
1222 |

F I G U R E   2 Location data for eight narwhals tracked from August to October 2017, after data cleaning, with one colour per individual.

3  |  R E S U LT S

3.1  |  Simulated data

states. The t.p.m. for merged states can be estimated by averaging

the state- transition probabilities (see Supporting Information). Both

DPMLE methods tended to slightly underestimate the means of the

last  two  states  under  scenarios  2  and  3,  with  accuracy  improving

Both DPMLE methods outperformed BIC and AIC and had a success

as  the  sample  size  increased  (see  Supporting  Information).  Non-

rate higher than 99% for more than half of the scenarios (Figure 3). The

stationary DPMLE mean estimates under scenario 6 outperformed

non- stationary  DPMLE  was  consistently  among  the  best- performing

the stationary estimates as the sample size increased.

methods and had more than 85% success rate for 10 of the 12 simula-

In scenarios 4 and 5 with sample size of 5000, BIC with covari-

tion settings explored. The mean estimates of both DPMLE methods

ates  performed  better  than  both  DPMLEs.  However,  its  perfor-

closely aligned with the simulated values (see Supporting Information).

mance was halved when the sample size increased to 12,000. This

BIC performed well for some scenarios and performed better than the

suggests that the inclusion of covariates improves the performance

DPMLE in two cases (scenarios 4 and 5 with covariates with a sample

of BIC through the increase of its penalty value, leading to the se-

size of 5000; Figure 3). However, its performance was significantly re-

lection of fewer states. As the sample size increases, the likelihood

duced when applied to a large sample size (12,000). The performance

becomes  the  dominant  factor,  which  explains  the  decrease  in  per-

of the non- stationary DPMLE was generally much higher and was less

formance (i.e. increase in overfitting) observed with higher sample

affected by an increase in sample size than AIC and BIC.

sizes.  A  similar  behaviour  arose  with  both  DPMLEs  for  the  same

Under  scenario  2  (presence  of  outliers),  both  DPMLEs  identi-

scenarios.  However,  the  decrease  in  performance  was  only  dras-

fied  the correct  number  of  states  with  a 100%  success  rate,  while

tic  for  the  stationary  method,  and  the  non- stationary  DPMLE  still

BIC  and  AIC  consistently  overestimated  the  number  of  states  (see

performed  reasonably  well  under  scenario  5  with  an  85%  success

Supporting Information). The DPMLEs also exhibited strong perfor-

rate for a sample size of 12,000. Under scenario 5, AIC selected an

mance under scenarios 3 (heterogeneity in the t.p.m.) and 6 (temporal

additional state between state 2 and 3 to incorporate the misspec-

variation in t.p.m.) with more than 90% success rates for both sam-

ification. BIC behaved similarly 53% of the time for a sample size of

ple sizes, which is likely because the misspecification is in the t.p.m.

12,000. The non- stationary DPMLE method was less subject to this

rather  than  the  state- dependent  distributions.  Both  double  penal-
ised  likelihood  methods  estimate  N(N − 1)  transition  probabilities
and can therefore incorporate the misspecification in the additional

behaviour.  Instead,  it  slightly  underestimated  the  mean  estimates

(see Supporting Information) and incorporated some of the temporal

variation in the temporal covariate.

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License3.2  |  Narwhal movement data

The  agreement  between  both  DPMLE  methods  provided  strong

evidence that narwhal movement in the summer is best explained by

Both DPMLE procedures selected two states, whereas model selection

two behavioural states. Movement of type 1 (Figure 4) estimated by the

criteria  selected  more  than  four  states.  The  non- stationary  DPMLE

two- state non- stationary DPMLE was slow and with little directional

was selected as the best- performing DPMLE model. BIC identified the

persistence,  thus  interpreted  as  area- restricted  searching  behaviour,

five- state HMM without covariate as the best- performing model. As

which is typically characterized by the ability to adjust movement adap-

expected from the simulations, AIC selected the most complex model

tively (Dorfman et al., 2022). This state can cover different behaviours

available: eight states with covariate ‘distance to shore’.

such as foraging, resting and socializing activities. Movement of type 2

    |  1223

F I G U R E   3 Success rate in estimating the correct number of states (i.e. three) across scenarios and sample sizes. ‘cov’ refers to models
fitted with the linear covariate ‘time of day’.

(a)

(b)

(c)

F I G U R E   4 Estimates from the HMM of narwhal movement data obtained with the non-  stationary DPMLE, with the two estimated states
(in blue and orange).

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1224 |

was faster and with strong directional persistence which likely reflected

a transiting behaviour. This interpretation was corroborated by the de-

coded states obtained from the forward- backward algorithm (Figure 5).

Information). Only one state could be identified as a transiting behaviour
(blue). States 4 and 5 had very low persistence (𝛾 11 = 0.17 , 𝛾 55 = 0.25)
and seemed unstable (Figure 5c). Thus, they were difficult to interpret as

Extreme turning angle values falling outside the estimated distribution

distinct and well- defined behaviours. Strong oscillations between states

were interpreted as location errors (Figure 4; Hurford, 2009). The states

could indicate the presence of additional and unnecessary states (Celeux

of the two- state HMM were stable, as shown by their high persistence

& Durand, 2008). In contrast, two- state HMMs differentiating between

and the decoded state sequence (Figure 5d). On average, both states

a resident (i.e. area- restricted search) and a transiting (fast and directed)

exhibited high persistence (0.88 and 0.81). From Figure 4, time spent in

movement are very common in animal movement analyses (Whoriskey

slow movement increased further from the shoreline, while time spent

et al., 2017). Movement associated with the turquoise, orange and green

in  the  directed  state  increased  as  narwhal  approach  the  shoreline.

states from the 5- state HMM (see Supporting Information) could cor-

Narwhal typically feed on deep- water prey, which could explain the as-

respond to area- restricted searching behaviour estimated by the two-

sociation between deeper waters (i.e. areas far from the shoreline) and

state  HMM  (characterized  by  low  directional  persistence  and  slower

increased time spent in area- restricted searching behaviour, as these

movement) and the other two states to transiting.

areas are likely rich in food resources (Watt & Ferguson, 2015). In con-

trast, the increased time spent in the directed state near the shoreline

may represent an adaptive anti- predatory response to the rising threat

4  |  D I S C U S S I O N

of killer whale predation in the Arctic (Breed et al., 2017).

In  the  five- state  model,  states  did  not  have  a  clear  interpretation

We  proposed  a  double  penalised  maximum  likelihood  estimate  to

and  exhibited  overlapping  step  length  distributions  (see  Supporting

perform simultaneous parameter estimation and order selection in

F I G U R E   5 Narwhal locations coloured by state from HMM model selected by BIC (a) and non-  stationary DPMLE (b) with associated state
time series (c and d, respectively).

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License    |  1225

non- stationary  HMMs  that  overcame  most  of  the  problems  asso-

&  Li,  2001;  Wang  et  al.,  2007).  Cross- validation  could  be  used  for

ciated  with  AIC  and  BIC.  In  the  simulation  study,  our  method  sig-

hyperparameter  selection  method,  but  the  computational  costs  of

nificantly outperformed both criteria. Our narwhal movement case

the DPMLE currently make this option impractical. Additionally, the

study demonstrated that, unlike AIC and BIC, our proposed method

potential overfitting issues highlighted by Wang et al. (2007) warrant

identified  two  behavioural  states  that  closely  aligned  with  the  ex-

further investigation.

pected  movement  behaviour  for  this  species  (Breed  et  al.,  2017;

We have introduced a DPMLE that, for the first time, provides

Shuert et al., 2023; Watt & Ferguson, 2015), further demonstrating

a  flexible  framework  for  handling  non- stationary  HMMs,  thereby

its  usefulness  in  ecology.  The  non- stationary  DPMLE  has  demon-

expanding  its  use  to  a  wider  range  of  real- life  scenarios  compared

strated  greater  efficiency  in  handling  the  narwhal  movement  data

to other methods. This framework could be further extended to in-

compared to the stationary DPMLE and allowed us to model a rela-

corporate random effects, allowing it to capture individual variation

tionship with an important environmental covariate.

(McClintock,  2021)  and  broadening  its  applicability  to  multilevel

DPMLE  is  particularly  effective  at  handling  misspecification  in

data  structures.  While  it  is  important  to  minimize  misspecification

the hidden process (scenarios 3 and 6) because it estimates a large

by  modelling  as  much  relevant  information  as  possible,  movement

t.p.m. that can accommodate model misspecification. With a higher

ecologists  rarely  have  the  data  or  knowledge  needed  to  create  a

upper bound, the method is expected to handle greater levels of mis-

fully specified model. Due to its improved performance in the simu-

specification. However, merged states may exhibit distinct transition

lation study and when applied to real- world data, the non- stationary

probabilities, which must not be overlooked. DPMLE cannot handle

DPMLE provides a good surrogate for standard information criteria

large levels of heterogeneity in state- dependent distributions (23%–
67% success rate in scenario 4 with T = 12,000) likely because such
heterogeneity creates distinct means that are ascribed to different

to perform order selection and parameter inference simultaneously

while handling the remaining misspecifications in the data.

states.  Individual  variation  in  movement  between  animals  is  inher-

AU T H O R C O N T R I B U T I O N S

ent in nature but we would expect the performance of both DPMLE

Fanny Dupont and Marie Auger- Méthé conceived the ideas and de-

methods  to  improve  as  differences  between  individuals  decrease.

signed  the  methodology;  Marianne  Marcoux  contributed  in  ensur-

One possible solution to circumvent this inherent problem is to fit

ing the accurate application of the method in the case study; Nigel

one  model  per  individual.  Several  misspecifications  were  not  ex-

Hussey and Marianne Marcoux conducted fieldwork; Fanny Dupont

plored here, such as those arising from inadequate state- dependent

conducted  the  analyses  and  prepared  the  manuscript.  Marianne

distributions (de Chaumaray et al., 2024).

Marcoux, Marie Auger- Méthé and Nigel Hussey contributed to fund

Information criteria are unreliable for order selection in HMMs

the study, and Marianne Marcoux and Marie Auger- Méthé contrib-

applied to complex real- world data. AIC consistently overestimated

uted to the supervision. All co- authors provided constructive feed-

the number of states, while BIC showed better performance under

back on written drafts. Our study engaged with the community of

certain  conditions.  However,  for  most  misspecified  scenarios,  BIC

Mittimatalik (Pond Inlet) and involved the Mittimatalik Hunter and

tended  to  favour  models  with  too  many  states.  In  the  case  of  the

Trapper Organization in field and tagging operations. Local individu-

narwhal  dataset,  both  criteria  selected  many  states  that  were  dif-

als played key roles in leading these efforts. While Inuit individuals

ficult to interpret, further illustrating their limitations when applied

were  involved  in  data  collection  for  the  case  study,  none  were  in-

to  complex  real- world  data  and  in  agreement  with  the  findings  of

volved in the development of the statistical analysis that is the focus

previous studies (Li & Bolker, 2017; Pohle et al., 2017).

of this paper.

While the simulation results show the good performance of the

proposed  method  with  various  sample  sizes,  the  non- stationary

AC K N OW L E D G E M E N T S

DPMLE is computationally expensive (see Supporting Information).

I acknowledge the support of the Natural Sciences and Engineering

However, the optimization procedure can be parallelized over two key

Research Council of Canada (NSERC), the Canadian Research Chairs

dimensions: (1) initial values and (2) hyperparameters. In our study,

program, BC Knowledge Development Fund and Canada Foundation

we  only  parallelized  over  hyperparameters,  which  should  be  con-

for Innovation's John R. Evans Leaders Fund, the Canadian Statistical

sidered when interpreting the runtimes provided in the Supporting

Sciences Institute (CANSSI) as well as the support of Fisheries and

Information.  Parallelization  over  initial  values  is  straightforward  to

Oceans Canada (DFO). I thank the community of Mittimatalik (Pond

implement and would greatly reduce computational costs. However,

Inlet) for its support in tagging operations and the devoted people

future work could investigate derivative- free optimizers, or efficient

who  led  operations  in  the  field.  Fieldwork  was  supported  by  the

programming languages along with automatic differentiation frame-

Polar Continental Shelf Program, Fisheries and Oceans Canada, the

works. Strategies to improve hyperparameter search efficiency (e.g.

Nunavut Wildlife Management Board, the Nunavut Implementation

quasi- random  sequences)  could  also  be  explored.  Another  natural

Fund, and World Wildlife Fund Canada. This research was enabled

direction  for  future  work  would  be  to  formally  assess  the  asymp-
totic properties of the non- stationary DPMLE. Note that BICDPMLE is
a BIC- type criterion that relies on the effective number of parame-

by support provided by Compute Canada (<www>. compu tecan ada. ca).

I  am  grateful  to  Dr.  Daniel  J.  McDonald,  as  well  as  my  committee

members Dr. Matías Salibián- Barrera and Dr. Nancy E. Heckman for

ters, which has only been rigorously derived in Gaussian models (Fan

the constructive suggestions and discussions.

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License1226 |

C O N F L I C T O F  I N T E R E S T S TAT E M E N T

Marie  Auger- Méthé  is  an  Associate  Editor  on  Methods  in  Ecology

and Evolution, but played no role in the handling or reviewing of the

manuscript.

P E E R R E V I E W

The peer review history for this article is available at https:// www.

webof scien ce. com/ api/ gatew ay/ wos/ peer-  review/ 10. 1111/ 2041-

210X. 70025 .

DATA  AVA I L A B I L I T Y S TAT E M E N T

Supporting  data  and  code  for  simulation  and  the  narwhal  tracking

data  are  available  on  GitHub,  versioned  and  archived  on  Zenodo

https:// doi. org/ 10. 5281/ zenodo. 14942003 (Dupont, 2025).

O R C I D

Fanny Dupont

 <https://orcid.org/0009-0003-4633-3484>

Nigel Hussey

 <https://orcid.org/0000-0002-9050-6077>

Marie Auger- Méthé

 <https://orcid.org/0000-0003-3550-4930>

R E F E R E N C E S

Aho, K., Derryberry, D., & Peterson, T. (2014). Model selection for ecolo-
gists: The worldviews of AIC and BIC. Ecology, 95(3), 631–636.
Akaike, H. (1974). A new look at the statistical model identification. IEEE
Transactions on Automatic Control, 19(6), 716–723. https:// doi. org/
10. 1109/ TAC. 1974. 1100705

Auger- Méthé, M., Newman, K., Cole, D., Empacher, F., Gryba, R., King,
A. A., Leos- Barajas, V., Mills Flemming, J., Nielsen, A., Petris, G., &
Thomas, L.  (2021). A  guide  to state–space  modeling  of  ecological
time series. Ecological Monographs, 91(4), e01470. https:// doi. org/
10. 1002/ ecm. 1470

Baum,  L.  E.,  Petrie,  T.,  Soules,  G.,  &  Weiss,  N.  (1970).  A  maximization
technique occurring in the statistical analysis of probabilistic func-
tions of Markov chains. The Annals of Mathematical Statistics, 41(1),
164–171. https:// doi. org/ 10. 1214/ aoms/ 11776 97196

Biernacki,  C.,  Celeux,  G.,  &  Govaert,  G.  (2000).  Assessing  a  mixture
model for clustering with the integrated completed likelihood. IEEE
Transactions on Pattern Analysis and Machine Intelligence, 22(7), 719–
725. https:// doi. org/ 10. 1109/ 34. 865189

Breed,  G.  A.,  Matthews,  C.  J.  D.,  Marcoux,  M.,  Higdon,  J.  W.,  LeBlanc,
B.,  Petersen,  S.  D.,  Orr,  J.,  Reinhart,  N.  R.,  &  Ferguson,  S.  H.
(2017).  Sustained  disruption  of  narwhal  habitat  use  and  behavior
in the presence of Arctic killer whales. Proceedings of the National
Academy of Sciences, 114(10), 2628–2633. https:// doi. org/ 10. 1073/
pnas. 16117 07114

Cai, D., Campbell, T., & Broderick, T. (2021). Finite mixture models do not
reliably  learn  the  number  of  components.  In  International  confer-
ence on machine learning (pp. 1158–1169). PMLR.

Celeux, G., & Durand, J. B. (2008). Selecting hidden Markov model state
number  with  cross- validated  likelihood.  Computational  Statistics,
23(4), 541–564. https:// doi. org/ 10. 1007/ s0018 0-  007-  0097-  1
Chen,  J.,  &  Khalili,  A.  (2008).  Order  selection  in  finite  mixture  mod-
els  with  a  nonsmooth  penalty.  Journal  of  the  American  Statistical
Association,  103(484),  1674–1683.  https:// doi. org/ 10. 1198/ 01621
45080 00001075

Chen, J., Tan, X., & Zhang, R. (2008). Consistency of penalized MLE for nor-
mal mixtures in mean and variance. Statistica Sinica, 18, 443–465.
Dannemann, J., & Holzmann, H. (2008). Testing for two states in a hid-
den  Markov  model.  Canadian Journal of Statistics,  36(4),  505–520.
https:// doi. org/ 10. 1002/ cjs. 55503 60402

de Chaumaray, M. D. R., Kolei, S. E., Etienne, M. P., & Marbac, M. (2024).
Estimation of the order of non- parametric hidden Markov models
using the singular values of an integral operator. Journal of Machine
Learning Research, 25(415), 1–37.

DeMars,  C.  A.,  Auger- Méthé,  M.,  Schlägel,  U.  E.,  &  Boutin,  S.  (2013).
Inferring parturition and neonate survival from movement patterns
of female ungulates: A case study using woodland caribou. Ecology
and Evolution, 3(12), 4149–4160. https:// doi. org/ 10. 1002/ ece3. 785
DeRuiter, S. L., Langrock, R., Skirbutas, T., Goldbogen, J. A., Calambokidis,
J., Friedlaender, A. S., & Southall, B. L. (2017). A multivariate mixed
hidden Markov model for blue whale behaviour and responses to
sound  exposure.  The  Annals  of  Applied  Statistics,  11(1),  362–392.
https:// doi. org/ 10. 1214/ 16-  AOAS1008

Dorfman,  A.,  Hills,  T.  T.,  &  Scharf,  I.  (2022).  A  guide  to  area- restricted
search: A foundational foraging behaviour. Biological Reviews, 97(6),
2076–2089.

Drton,  M.,  &  Plummer,  M.  (2017).  A  Bayesian  information  criterion  for
singular  models.  Journal  of  the  Royal  Statistical  Society,  Series  B:
Statistical Methodology, 79(2), 323–380.

Dupont, F. (2025). Fanny- Dupont/DPMLE: DPMLE_v1 (DPMLE). Zenodo.
Fan, J., & Li, R. (2001). Variable selection via nonconcave penalized like-
lihood and its oracle properties. Journal of the American Statistical
Association,  96(456),  1348–1360.  https:// doi. org/ 10. 1198/ 01621
45017 53382273

Gassiat, E., & Boucheron, S. (2003). Optimal error exponents in hidden
Markov models order  estimation. IEEE Transactions on Information
Theory, 49(4), 964–980. https:// doi. org/ 10. 1109/ TIT. 2003. 809574
Glennie, R., Adam, T., Leos- Barajas, V., Michelot, T., Photopoulou, T., &
McClintock,  B.  T.  (2023).  Hidden  Markov  models:  Pitfalls  and  op-
portunities in ecology. Methods in Ecology and Evolution, 14(1), 43–
56. https:// doi. org/ 10. 1111/ 2041-  210X. 13801

Hung, Y., Wang, Y., Zarnitsyna, V., Zhu, C., & Wu, C. F. J. (2013). Hidden
Markov  models  with  applications  in  cell  adhesion  experiments.
Journal of the American Statistical Association, 108(504), 1469–1479.
https:// doi. org/ 10. 1080/ 01621 459. 2013. 836973

Hurford, A. (2009). GPS measurement error gives rise to spurious 180° turn-
ing angles and strong directional biases in animal movement data. PLoS
One, 4(5), e5632. https:// doi. org/ 10. 1371/ journ al. pone. 0005632
Kenyon,  K.  A.,  Yurkowski,  D.  J.,  Orr,  J.,  Barber,  D.,  &  Ferguson,  S.  H.
(2018).  Baffin  Bay  narwhal  (Monodon  monoceros)  select  bathym-
etry  over  sea  ice  during  winter.  Polar  Biology,  41(10),  2053–2063.
https:// doi. org/ 10. 1007/ s0030 0-  018-  2345-  y

Leos- Barajas, V., & Michelot, T. (2018). An introduction to animal move-
ment modeling with hidden Markov models using Stan for Bayesian
inference.  arXiv  preprint  arXiv:180610639.  https:// doi. org/ 10.
48550/  arXiv. 1806. 10639

Li, M., & Bolker, B. M. (2017). Incorporating periodic variability in hidden
Markov  models  for  animal  movement.  Movement  Ecology,  5(1),  1.
https:// doi. org/ 10. 1186/ s4046 2-  016-  0093-  6

Lin,  Y.,  &  Song,  X.  (2022).  Order  selection  for  regression- based  hid-
den  Markov  model.  Journal  of  Multivariate  Analysis,  192,  105061.
https:// doi. org/ 10. 1016/j. jmva. 2022. 105061

Mackay,  R.  J.  (2002).  Estimating  the  order  of  a  hidden  Markov  model.
Canadian  Journal  of  Statistics,  30(4),  573–589.  https:// doi. org/ 10.
2307/ 3316097

Manole, T., & Khalili, A. (2021). Estimating the number of components in
finite mixture models via the group- sort- fuse procedure. The Annals
of Statistics, 49(6), 3043–3069.

McClintock,  B.  T.  (2021).  Worth  the  effort?  A  practical  examination  of
random effects in hidden Markov models for animal telemetry data.
Methods in Ecology and Evolution, 12(8), 1475–1497. https:// doi. org/
10. 1111/ 2041-  210X. 13619

McClintock,  B.  T.,  Langrock,  R.,  Gimenez,  O.,  Cam,  E.,  Borchers,  D.  L.,
Glennie, R., & Patterson, T. A. (2020). Uncovering ecological state
dynamics  with  hidden  Markov  models.  Ecology  Letters,  23(12),
1878–1903. https:// doi. org/ 10. 1111/ ele. 13610

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMcClintock,  B.  T.,  &  Michelot,  T.  (2018).  momentuHMM:  package  for
generalized hidden Markov models of animal movement. Methods
in Ecology and Evolution, 9(6), 1518–1530. https:// doi. org/ 10. 1111/
2041-  210X. 12995

McKellar, A. E., Langrock, R., Walters, J. R., & Kesler, D. C. (2015). Using
mixed  hidden  Markov  models  to  examine  behavioral  states  in  a
cooperatively  breeding  bird.  Behavioral  Ecology,  26(1),  148–157.
https:// doi. org/ 10. 1093/ beheco/ aru171

Morales,  J.  M.,  Haydon,  D.  T.,  Frair,  J.,  Holsinger,  K.  E.,  &  Fryxell,  J.  M.
(2004). Extracting more out of relocation data: Building movement
models  as  mixtures  of  random  walks.  Ecology,  85(9),  2436–2445.
https:// doi. org/ 10. 1890/ 03-  0269

Ngô, M. C., Heide- Jørgensen, M. P., & Ditlevsen, S. (2019). Understanding
narwhal  diving  behaviour  using  hidden  Markov  models  with  de-
pendent  state  distributions  and  long  range  dependence.  PLoS
Computational  Biology,  15(3),  e1006425.  https:// doi. org/ 10. 1371/
journ al. pcbi. 1006425

Patterson,  T.  A.,  McConnell,  B.  J.,  Fedak,  M.  A.,  Bravington,  M.  V.,  &
Hindell, M. A. (2010). Using GPS data to evaluate the accuracy of
state–space  methods  for  correction  of  Argos  satellite  telemetry
error. Ecology, 91(1), 273–285. https:// doi. org/ 10. 1890/ 08-  1480. 1

Pizzolato, L., Howell, S. E. L., Derksen, C., Dawson, J., & Copland, L. (2014).
Changing sea ice conditions and marine transportation activity in
Canadian Arctic waters between 1990 and 2012. Climatic Change,
123(2), 161–173. https:// doi. org/ 10. 1007/ s1058 4-  013-  1038-  3
Pohle,  J.,  Langrock,  R.,  Van  Beest,  F.  M.,  &  Schmidt,  N.  M.  (2017).
Selecting the number of states in hidden Markov models: Pragmatic
solutions illustrated using animal movement. Journal of Agricultural,
Biological and Environmental Statistics, 22, 270–293.

R Core Team. (2021). R: A language and environment for statistical comput-

ing. R Foundation for Statistical Computing.

Schwarz, G. (1978). Estimating the dimension of a model. The Annals of
Statistics, 6(2), 461–464. https:// doi. org/ 10. 1214/ aos/ 11763 44136
Shuert, C. R., Hussey, N. E., Marcoux, M., Heide- Jørgensen, M. P., Dietz,
R.,  &  Auger- Méthé,  M.  (2023).  Divergent  migration  routes  reveal
contrasting  energy- minimization  strategies  to  deal  with  differing
resource  predictability.  Movement  Ecology,  11(1),  31.  https:// doi.
org/ 10. 1186/ s4046 2-  023-  00397 -  y

Shuert, C. R., Marcoux, M., Hussey, N. E., Heide- Jørgensen, M. P., Dietz,
R.,  &  Auger- Méthé,  M.  (2022).  Decadal  migration  phenology  of  a
long- lived Arctic icon keeps pace with climate change. Proceedings
of the National Academy of Sciences of the United States of America,
119(45), e2121092119. https:// doi. org/ 10. 1073/ pnas. 21210 92119
Smyth, P. (2000). Model selection for probabilistic clustering using cross-

validated likelihood. Statistics and Computing, 10(1), 63–72.

    |  1227

Sutherland, W. J. (1998). The importance of behavioural studies in con-
servation  biology.  Animal  Behaviour,  56(4),  801–809.  https:// doi.
org/ 10. 1006/ anbe. 1998. 0896

Wang,  H.,  Li,  B.,  &  Leng,  C.  (2009).  Shrinkage  tuning  parameter  selec-
tion  with  a  diverging  number  of  parameters.  Journal  of  the  Royal
Statistical Society, Series B: Statistical Methodology, 71(3), 671–683.
https:// doi. org/ 10. 1111/j. 1467-  9868. 2008. 00693. x

Wang, H., Li, R., & Tsai, C. L. (2007). Tuning parameter selectors for the
smoothly  clipped  absolute  deviation  method.  Biometrika,  94(3),
553–568. https:// doi. org/ 10. 1093/ biomet/ asm053

Watanabe, S. (2013). A widely applicable Bayesian information criterion.

The Journal of Machine Learning Research, 14(1), 867–897.

Watt, C. A., & Ferguson, S. H. (2015). Fatty acids and stable isotopes (13C
and 15N) reveal temporal changes in narwhal (Monodon monoceros)
diet  linked  to  migration  patterns.  Marine  Mammal  Science,  31(1),
21–44. https:// doi. org/ 10. 1111/ mms. 12131

Whoriskey,  K.,  Auger- Méthé,  M.,  Albertsen,  C.  M.,  Whoriskey,  F.  G.,
Binder, T. R., Krueger, C. C., & Mills Flemming, J. (2017). A hidden
Markov movement model for rapidly identifying behavioral states
from animal tracks. Ecology and Evolution, 7(7), 2112–2121. https://
doi. org/ 10. 1002/ ece3. 2795

Zou, H., & Li, R. (2008). One- step sparse estimates in nonconcave penal-
ized  likelihood  models.  The  Annals  of  Statistics,  36(4),  1509–1533.
https:// doi. org/ 10. 1214/ 00905 36070 00000802

Zucchini,  W.,  MacDonald,  I.  L.,  &  Langrock,  R.  (2017).  Hidden  Markov

models for time series: An introduction using R. CRC Press.

S U P P O R T I N G I N FO R M AT I O N

Additional  supporting  information  can  be  found  online  in  the

Supporting Information section at the end of this article.

Appendix S1: Supporting Information.

How to cite this article: Dupont, F., Marcoux, M., Hussey, N., &

Auger- Méthé, M. (2025). Improved order selection method for

hidden Markov models: A case study with movement data.

Methods in Ecology and Evolution, 16, 1215–1227. <https://doi>.

org/10.1111/2041-210X.70025

DUPONT et al. 2041210x, 2025, 6, Downloaded from <https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.70025> by Test, Wiley Online Library on [04/09/2025]. See the Terms and Conditions (<https://onlinelibrary.wiley.com/terms-and-conditions>) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
