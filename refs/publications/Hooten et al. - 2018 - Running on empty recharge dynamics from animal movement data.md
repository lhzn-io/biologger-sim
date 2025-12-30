Running on empty: Recharge dynamics
from animal movement data

Mevin B. Hooten
U.S. Geological Survey, Colorado Cooperative Fish and Wildlife Research Unit

Department of Fish, Wildlife, and Conservation and Department of Statistics

Colorado State University

<mevin.hooten@colostate.edu>
Henry R. Scharf
Department of Statistics, Colorado State University

<henry.scharf@colostate.edu>
Juan M. Morales
Grupo de Ecolog´ıa Cuantitativa, INIBIOMA, Universidad Nacional del Comahue, CONICET

<jm.morales@conicet.gov.ar>

February 3, 2020

Keywords: animal movement, animal physiology, continuous-time model, energetics
Corresponding Author: Mevin B. Hooten, 1484 Campus Delivery, Colorado State
University, Fort Collins, CO 80523. Phone: 970-491-1415, Email: <mevin.hooten@colostate.edu>

0
2
0
2

n
a
J

0
3

]
P
A

.
t
a
t
s
[

5
v
0
3
0
8
0
.
7
0
8
1
:
v
i
X
r
a

1

Abstract

Vital rates such as survival and recruitment have always been important in
the study of population and community ecology. At the individual level, physio-
logical processes such as energetics are critical in understanding biomechanics and
movement ecology and also scale up to inﬂuence food webs and trophic cascades.
Although vital rates and population-level characteristics are tied with individual-
level animal movement, most statistical models for telemetry data are not equipped
to provide inference about these relationships because they lack the explicit, mech-
anistic connection to physiological dynamics. We present a framework for mod-
eling telemetry data that explicitly includes an aggregated physiological process
associated with decision making and movement in heterogeneous environments.
Our framework accommodates a wide range of movement and physiological pro-
cess speciﬁcations. We illustrate a speciﬁc model formulation in continuous-time
to provide direct inference about gains and losses associated with physiological
processes based on movement. Our approach can also be extended to accommo-
date auxiliary data when available. We demonstrate our model to infer mountain
lion (Puma concolor ; in Colorado, USA) and African buﬀalo (Syncerus caﬀer ; in
Kruger National Park, South Africa) recharge dynamics.

2

1

Introduction

Energetics has been a dominant theme in ecological and biological science for cen-

turies (Zuntz, 1897; Nussbaum, 1978) because an improved understanding of metabolics

and energy acquisition provides insights about fundamental similarities and diﬀerences

among species (Taylor et al., 1982). An understanding of the connection between en-

ergetics and movement is critical for all aspects of biology and leads to improved man-

agement and conservation of wildlife because physiological processes and vital rates are

indicative of animal health (Nathan et al., 2008; Wilmers et al., 2017). Healthy wildlife

individuals and populations are an essential ecosystem service and have intrinsic anthro-

pogenic and ecosystem value (Ingraham and Foster, 2008).

While much research has focused primarily on the ties between energy and locomo-

tion, myriad other factors inﬂuence animal decision making processes (Alcock, 2009).

Decisions made by animals directly aﬀect their movement rates and hence indirectly af-

fect their energy as well as other physiological processes (Houston and McNamara, 1999;

Morales et al., 2005, 2010). In what follows, we use the term “recharge” as a general

reference to physiological processes that require replenishment for an organism to main-

tain its physical health and normal activities. The recharge concept is a simpliﬁcation of

complex physiological changes over time; it reduces the complexity enough that we can

account for aggregate physiological signals while inferring environmental inﬂuences on

animal movement given telemetry data. We describe examples of physiological processes

that may be connected with animal movement decisions and show how they accumu-

late in a recharge function that can be statistically inferred using tracking data. Our

approach to account for recharge dynamics relies on a long-memory statistical model

speciﬁed to mimic physiological processes and can be applied to animal tracking data to

test hypotheses about animal behavior as well as estimate parameters associated with

changes in physiological processes over time.

Many former studies of animal movement have used experimental laboratory ap-

proaches to measure oxygen intake and energy expenditure directly (Alexander, 2003;

Halsey, 2016). These studies provided a foundational kinematic understanding of ani-

3

mal movement in controlled environments (Full et al., 1990). More recent research has

examined connections between movement and energetics in natural settings (Karasov,

1992) and how terrain and environmental factors inﬂuence movement (e.g., Humphries

and Careau, 2011; Shepard et al., 2013; Williams et al., 2014). Biotelemetry technology

has facilitated regular measurement of movement and led to improved understanding of

individual-based physiological processes (e.g., Cooke et al., 2004; Green, 2011).

Improvements in high-quality animal tracking data are occurring at an increasing

rate (Cagnacci et al., 2010). Wildlife tracking devices have allowed researchers to col-

lect unprecedented data sets that contain valuable information about animal movement,

and hence energetics and other physiological processes that require recharge (Kays et

al., 2015; Wilmers et al., 2015). Statistical approaches have been developed to charac-

terize the variation within and among individual animal trajectories (Scharf et al., 2016;

Hooten and Johnson, 2019; Hooten et al., 2017; Scharf et al., 2018). These approaches

include the use of environmental information and methods to identify the portions of

animal trajectories that indicate distinctly diﬀerent patterns (e.g., Whoriskey et al.,

2017). For example, stochastic diﬀerential equations (SDEs; Brillinger, 2010) allow re-

searchers to make inference on the importance of environmental covariates on movement

in continuous time. Some discrete-time models also incorporate covariates and focus on

phenomenological clustering of movement processes that are linked to possible behav-

ioral changes over time (e.g., Morales et al., 2004; Langrock et al., 2012; McClintock et

al., 2012; McKellar et al., 2015).

Despite the proliferation of statistical animal movement models, few are based on

speciﬁc mechanisms related to physiology (e.g., Schick et al., 2013). By contrast, purely

mathematical animal movement models are almost always mechanistically motivated

(Turchin, 1998), but are often too complex to allow for statistical learning using location-

based telemetry data alone. Some statistical models have been used to make post hoc

inferences concerning physiological processes such as memory (e.g., Avgar et al., 2013;

Oliveira-Santos et al., 2016) and energetics (e.g., Merkle et al., 2017; Hooten et al.,

2018), including some that rely on auxiliary data from accelerometers (e.g., Wilson et al.,

2012). However, they often lack the mechanistic mathematical speciﬁcations to account

4

for recharge dynamics directly when inferring movement dynamics. Demographic models

based on capture-recapture data, such as Cormack-Jolly-Seber (CJS) models, explicitly

consider individual health and body condition when inferring vital rates (Lebreton et al.,

1992; Pollock, 1991), but are often focused on large spatial and temporal scales (Schick

et al., 2013).

In what follows, we broaden the current scope of “energy landscapes” (Wilson et al.,

2012; Shepard et al., 2013) and “landscapes of fear” (Laundr´e et al., 2001; Bleicher, 2017)

to include all physiological processes that require recharge. We consider accumulations

of these physiological landscapes that result in individual-based recharge functions and

link them to decision making processes of individual organisms as they move. We show

how to use telemetry data to make inference about both the decision and recharge

processes in heterogeneous environments and account for their eﬀect on movement. We

demonstrate our recharge movement model with case studies involving telemetry data

for a mountain lion (Puma concolor ) in Colorado, USA and African buﬀalo (Syncerus

caﬀer ) in South Africa. We also discuss possible ways to extend the model to account

for conspeciﬁc and allospeciﬁc interactions among individuals as well as accommodate

auxiliary data sources such as individual-level health and accelerometer data.

2 Material and Methods

2.1 Physiological Landscapes

Critical to our approach is the concept of recharge, a time-varying process involving

an individual physiological characteristic v. Physiological recharge can be expressed

as a function g(v, t) that increases (i.e., charges) and decreases (i.e., discharges) over

time depending on the decision making process of the individual, the resulting behavior,

and the environmental conditions it encounters. We refer to a combination of spatially

explicit covariates that aﬀect the recharge function g(v, t) over time as the “physiological

landscape.” For a physiological characteristic v, we deﬁne the physiological landscape

as w(cid:48)(µ)θ(v) for any location µ ≡ (µ1, µ2)(cid:48) in region D (e.g., the study area).

5

The coeﬃcients θ(v) ≡ (θ1(v), . . . , θp(v))(cid:48) appropriately weight each of the landscape
variables (e.g., elevation, land type, etc.) in w(µ) ≡ (w1(µ), . . . , wp(µ))(cid:48) so that they

combine to result in a surface that modulates the state of the physiological process v

as an individual moves throughout the space (Figure 1). For example, if v refers to

the energetic component of a larger suite of physiological processes, then w(cid:48)(µ(t))θ(v)

represents the physiological landscape value that inﬂuences the energy recharge dynamics

as the individual under study moves to position µ(t) at time t.

In fact, for a given individual trajectory µ(t) (for all t ∈ T in the study period),

the physiological landscape w(cid:48)(µ(t))θ(v) is accumulated as the individual moves. This

accumulation over time results in what we refer to as a physiological recharge function

that can be expressed as the line integral of the physiological landscape

g(v, t) = g0(v) +

(cid:90) t

0

w(cid:48)(µ(τ ))θ(v)dτ ,

(1)

where the lower limit (i.e., zero) on the integral in (1) corresponds to the beginning

of the study period. Figure 1c depicts the physiological recharge function as the line

integral associated with the trajectory. At times when g(v, t) is large, the individual

is in a charged state with respect to physiological process v. Conversely, when the

physiological recharge function g(v, t) is small, it indicates that the physiological process

v is discharged and the individual may alter its behavior in an attempt to recharge.

While energy is among the most commonly studied physiological characteristic (Wil-

son et al., 2012), there exists a large set of other individual-based physiological character-

istics (i.e., v ∈ V) that contribute to individual, population, community, and ecosystem

health and larger scale vital rates (Matthiopoulos et al., 2015). For example, in addition

to energy intake and expenditure (Spalinger and Hobbs, 1992; Stephens et al., 2007),

most animals require periodic hydration (e.g., Tshipa et al., 2017), sleep (Savage and

West, 2007), heat (Humphries and Careau, 2011), and shelter (Eggleston and Lipcius,

1992). Less obvious physiological processes requiring recharge that transcend the indi-

vidual level may include activities such as reproduction (Proaktor et al., 2008), care for

young (Dudek et al., 2018), and “security” in the context of landscapes of fear (Laundr´e

et al., 2001; Bleicher, 2017). Thus, we can express an aggregated physiological recharge

6

process as an integral over the set of all physiological processes V:

g(t) =

(cid:90)

V

g(v, t)dv ,

= g0 +

(cid:90) t

0

w(cid:48)(µ(τ ))θdτ ,

where we show that the initial aggregated charge is

g0 ≡

(cid:90)

V

g0(v)dv ,

and the aggregated recharge coeﬃcients are

θ ≡

(cid:90)

V

θ(v)dv

(2)

(3)

(4)

(5)

in Online Appendix A. As we describe in what follows, the aggregated recharge process

in (3) provides a fundamental mechanistic link between environmental characteristics

and the physiology and sociality of moving individuals as they seek to recharge — a

link that is missing in most other contemporary models for animal movement and one

that allows us to examine the evidence for physiological signals in animal movement

trajectories. Furthermore, in the absence of a strict connection to speciﬁc physiological

processes, the recharge function in (3) can be used to generalize movement models to

accommodate long-range temporal dependence that may go unaccounted for otherwise.

Finally, the recharge function we speciﬁed in (3) can be generalized easily to accom-

modate time varying coeﬃcients (i.e., θ(t)), nonlinearity in the physiological landscape,

and alternatives to the convolution form of aggregation (e.g., based on the principle of

limiting factors). For example, to account for optima in the environmental gradients

that comprise the physiological landscape, we can include polynomial transformations

of environmental variables w as we would in a conventional regression model.

2.2 Movement Decisions Based on Physiological Processes

2.2.1 General Framework

Most modern statistical models for animal trajectories account for both measurement er-

ror and movement dynamics using a hierarchical framework (Schick et al., 2008; Hooten

7

et al., 2017). Thus, we employ a hierarchical structure to build a general modeling

framework that reconciles animal trajectories and physiological processes while account-

ing for measurement error and uncertainty in movement dynamics (Figure 2). To develop

a general recharge-based movement modeling framework, we consider a model for the

telemetry data that depends on the true, underlying animal trajectory. Our movement

model characterizes the structure of the trajectory, and hence the perception of the land-

scape by the animal, depending on a binary decision process z(ti) of the animal over

time. This decision process arises stochastically according to a probability function that

depends on the underlying aggregated physiological process. For telemetry observations

s(ti) (for i = 1, . . . , n) and associated trajectory µ(ti) we formulate the hierarchical

model

s(ti) ∼ [s(ti)|µ(ti)] ,

µ(ti) ∼




M0

, z(ti) = 0 ,



M1

, z(ti) = 1 ,

(6)

(7)

for i = 1, . . . , n, where the bracket notation ‘[·]’ denotes a generic probability distribu-

tion (Gelfand and Smith, 1990) that may include additional parameters. We introduce

continuous-time models for M0 and M1 in the example speciﬁcation that follows.

The mixture movement model in (7) depends on a latent binary decision z(t) that

represents the individual’s choice to recharge when z(t) = 1 (where z(t) = 1 corresponds

to a discharged state and z(t) = 0 corresponds to a charged state). The instantaneous

probability of the decision to recharge (ρ(t)) can be related to the latent physiological

recharge process g(t) through an appropriate link function. Thus, in the case studies

that follow, we express z(t) ∼ Bern(ρ(t)) with ρ(t) = 1 − Φ(g(t)), where Φ(·) represents

the standard normal cumulative distribution function (i.e., the inverse probit function;

another option is the logit). This relationship between ρ(t) and g(t) implies that the de-

cision to recharge will increase in probability when the aggregated physiological process

g(t) decreases. For example, as an individual ventures far from resources that allow it

to recharge, g(t) will decline and the individual will eventually need to make an eﬀort to

8

replenish its physiological processes, hence increasing ρ(t) and changing its movement

behavior (Figure 2). By connecting an animal decision process z(t) with movement and

resources, our model formulation explicitly accounts for the relationship between stimuli

and motivation, which is a primary focus of ethology (Colgan, 1989).

2.2.2 A Continuous-Time Recharge-Based Movement Model

In the continuous-time setting, stochastic diﬀerential equation (SDE) models are a pop-

ular option to account for diﬀusion and drift across heterogeneous landscapes (Brillinger,

2010). Thus, we provide an example speciﬁcation using the hierarchical framework by

formulating the speciﬁc components of our recharge-based movement model in (6)–(7).

We consider Gaussian error for telemetry observations such that s(ti) ∼ N(µ(ti), σ2I)

(for i = 1, . . . , n) and a mixture SDE with components

dµ(t) =






σ0db0(t)

, z(t) = 0

,

(8)

− (cid:53) p(µ(t), β)dt + σ1db1(t)

, z(t) = 1

for the set of times in the study period t ∈ T , where, p represents a potential function

(so-called because of its connections to potential energy in physics; Preisler et al., 2013)

controlling the drift of the individual trajectory µ(t) based on landscape covariates and

associated coeﬃcients β. The diﬀusion aspects of the movement process are controlled

by the two Gaussian white noise terms db0(t) and db1(t) that are scaled by σ0 and σ1.

The movement process model in (8) can be interpreted in the following way. When

the decision to recharge is made (z(t) = 1) at time t, the individual will respond to

the environment as dictated by the potential function p(µ(t), β) by taking steps that

are aligned approximately with its gradient surface (i.e., downhill on the surface; M1

in Figure 2). Conversely, when z(t) = 0, the individual may roam freely without need-

ing to respond to the environment (M0 in Figure 2). Thus, in this particular model

speciﬁcation, we would obtain biased inference about the movement parameters β if the

individual was assumed to move according to the SDE with potential function p(µ(t), β)

without considering the underlying physiological process (i.e., z(t) = 1 always). Most

studies investigating resource selection assume only a single movement model. Thus,

9

the movement model speciﬁcation in (8) allows us to infer when a physiological signal

is present in our telemetry data (i.e., when z(t) switches between zero and one at some

point along the trajectory).

It is worth noting that our model formulation ﬁts into a broader class of models for

movement using the basis function approach proposed by Hooten and Johnson (2017a)

to connect the telemetry data to the underlying trajectory. This framework provides

opportunities to extend the model in future studies to accommodate other types of

smoothness and heterogeneity in the trajectory process (see Scharf et al., 2018 and

Hooten et al., 2018 for further details). Also, to ﬁt the model to data, we must solve the

SDE for µ(t) based on a discrete approximation. This solution is more intuitive than

the SDE itself because it assumes a discrete-time form where the process components

of the model for µ(tj) in (7) can be written as M0 = N(µ(tj−1), σ2
N(µ(tj−1) − (cid:53)p(x(cid:48)(µ(tj−1))β)∆t, σ2

0I∆t) and M1 =
1I∆t) for a ﬁne grid of time points, t1, . . . , tm, spaced
∆t apart, using an Euler-Maruyama discretization scheme (Kloeden and Platen, 1992).

As a result of our speciﬁcations for the hierarchical model, the full parameter set

includes the latent position process µ(tj) for all j = 1, . . . , m, as well as 3 sets of

state g0 and recharge coeﬃcients θ, and 3) the variance parameters σ2

parameters: 1) the drift coeﬃcients in the potential function, β, 2) the initial recharge
0, and σ2
1.
To estimate the parameters and make inference, we can ﬁt the model using maximum

s , σ2

likelihood if we are able to derive the integrated likelihood, or we can use Bayesian

methods. In what follows, we use a Bayesian approach that allows us to specify priors

for the three sets of parameters described above (Online Appendix C) and obtain a

Markov chain Monte Carlo (MCMC) sample from the posterior distribution

[{µ(tj), for j = 1, . . . , m}, β, g0, θ, σ2

s , σ2

0, σ2

1|{s(ti), i = 1, . . . , n}] ∝

n
(cid:89)

[s(ti)|µ(ti), σ2
s ]

m
(cid:89)

[µ(tj)|µ(tj−1), σ2

0]1−z(tj )[µ(tj)|µ(tj−1), β, σ2

1]z[tj ](z(tj)|g0, θ)×

i=1

j=1

[β][g0][θ][σ2

s ][σ2

0][σ2

1] ,

(9)

for a ﬁne discretization of the latent position process µ(tj) at times t1, . . . , tm and where

10

we have suppressed notation for the position process in the conditional distribution for

z(tj) to streamline the expression.

We applied speciﬁc formulations of our hierarchical movement model to infer recharge

dynamics based on telemetry data for two contrasting species: a mountain lion in the

Front Range of the Rocky Mountains in Colorado, USA and an African buﬀalo in Kruger

National Park, South Africa (Figure 3). Also, for illustration, we demonstrate the

approach based on simulated data in Online Appendix B. Using simulated data, we

showed that the modeling framework allows us to recover parameters and identify the

data generating model compared to a set of alternatives that consider only M0 and M1

individually (Online Appendix B).

3 Results

3.1 Mountain Lion

In the western USA, mountain lions (Puma concolor ) are apex predators that mostly

seek mule deer (Odocoileus hemionus) as prey. In the Front Range of the Rocky Moun-

tains in Colorado, USA (Figure 3), many approaches have been used to model the

individual-based movement of mountain lions (e.g., Hanks et al., 2015; Hooten and

Johnson, 2017a; Buderman et al., 2018), but none have modeled connections between

physiological dynamics and movement. Front Range mountain lions navigate a matrix

of public and privately owned land comprised of wildland-urban interface, roads, and

trail systems (Blecha, 2015; Buderman et al., 2018). Previous research has shown that

prey availability and cached carcasses are important factors inﬂuencing mountain lion

movement (Husseman et al., 2003; Blake and Gese, 2016). Thus, we speciﬁed a recharge-

based movement model for the telemetry data (global positioning system [GPS] with 3

hr ﬁxes; n=150) from an adult male mountain lion in Colorado during April 25, 2011 –

May 17, 2011 (Figure 3).

This particular trajectory includes a period at the beginning and end of the time

interval where the individual occupied a prey kill area (top center of blown up region

11

in Figure 3; using methods to identify kills sites described by Knopﬀ et al., 2009).

On approximately May 1, 2011, the individual mountain lion left the prey kill area to

traverse a large loop to the south before returning to the prey kill area. After a few more

days at the prey kill area, the individual left again to traverse a small loop to the north.

We hypothesized that the mountain lion individual recharged at the prey kill area and

mostly discharged otherwise.

We used the same movement model structure as speciﬁed in the previous section,

with M0 implying no drift when charged and p(µ(t), β) = x(cid:48)(µ(t))β to account for drift

when discharged. To formulate the recharge component of the full model, we used an

intercept (θ0), and six spatial covariates: presence in the prey kill area, elevation, slope,

sine and cosine of aspect, and the interaction of elevation and slope. For movement

covariates in the full model, we used ﬁve: elevation, slope, sine and cosine of aspect, and

distance to prey kill area.

We ﬁt the full recharge-based movement model to the mountain lion telemetry data

shown in Figure 3. The set of priors and hyperparameter settings, as well as pseudocode

and computational details to ﬁt the recharge-based movement model, are provided in

Online Appendix C. We also examined a set of simpler models including model M0 and

M1 separately as well as the recharge-based model with only prey kill area covariates

and the associated submodel M1 with only the prey kill area covariates. We scored

each of the models using the negative log posterior predictive score based on cross-

validation (Online Appendix C) and found the recharge-based model with only prey

kill area covariates was the best predictive model. The associated marginal posterior

distributions for the model parameters β1 (coeﬃcient for distance to prey kill area), θ0

(recharge intercept coeﬃcient), and θ1 (coeﬃcient for inside prey kill area) are shown in

Figure 4.

In this case, the left half of Figure 4 (labeled “behavior”) indicates that there is

evidence for the individual to move toward the prey kill area when the decision to

recharge is made (because of the negative coeﬃcient associated with distance to prey

kill area) and the recharge function itself (and hence the decision to recharge) increased

with the individual’s presence in the prey kill area (i.e., convex polygon with 1 km buﬀer

12

from kill site clusters).

In terms of the estimated recharge function for the individual mountain lion, the

posterior median for g(t) is shown superimposed on the trajectory in Figure 5. The

results of ﬁtting the recharge-based movement model to the mountain lion telemetry

data indicate that the individual is charged (blue) when near the prey kill area (green

region) and discharges as it moves farther from the kill area, both to the south and the

north (Figure 5a).

Visualized longitudinally, the posterior marginal trajectories as well as posterior me-

dian for g(t) and ρ(t) are shown in Figure 5. The posterior inference indicates that the

mountain lion individual we analyzed was mostly recharging during the early portion of

the study period (April 25, 2011 — May 1, 2011). However, as the recharge function g(t)

exceeded a value of approximately three, the individual left the prey kill area. During

the week that the individual was away from the prey kill area, our analysis shows that

the aggregated physiological process discharged until the behavioral decision process was

dominated by z(t) = 1, at which point the individual actively sought to recharge. This

decision process was characterized largely by a tendency of the individual to orient back

toward the prey kill area on May 9, 2011 (Figure 5). Then, after another few days of

recharging at the original prey kill area, the individual left the prey kill area again (this

time to the north) and its physiological process began to discharge again until near the

end of the study period when the individual returned to the prey kill area (Figure 5).

3.2 African Buﬀalo

In contrast to the western hemisphere predator we described in the previous section,

the African buﬀalo is a large grazing ungulate that ranges throughout sub-Saharan

Africa (Sinclair, 1977). In Kruger National Park, South Africa, the African buﬀalo is an

important species because it ﬁlls a niche in terms of tall and coarse grazing preference

(Corn´elis et al., 2014), is a source of prey for lions (Panthera leo; Sinclair, 1977; Prins,

1996; Radloﬀ and DuToit, 2004), and is one of the desirable species for tourism in the

region. African buﬀalo are strongly water dependent because they lack the capacity

to subsist on the moisture available from their forage alone (Prins and Sinclair, 2013).

13

Previous studies of the movement of African buﬀalo found that water resources can

strongly inﬂuence their space use (Redfern et al., 2003). In some cases, African buﬀalo

may undergo large interseasonal movements when resources are limited (e.g., Naidoo

et al., 2012), but there is variability in dry versus wet season movement characteristics

across regions (Ryan et al., 2006; Corn´elis et al., 2014). Repetitive use of areas is

common among African buﬀalo and some of these patterns in space use may be a result

of maintaining physiological balance among resources (Bar-David et al., 2009).

We used the same movement model (8) that we applied to the mountain lion data

(but with diﬀerent environmental variables) to analyze a set of telemetry data arising

from an adult female African buﬀalo in southern Kruger National Park (Getz et al.,

2007) obtained using hourly GPS ﬁxes (n=361) and spanning the period from October

1, 2005 – October 14, 2005 (Figure 3). The transition from dry to wet season typically

occurs during late September and October in South Africa, and the year 2005 had

slightly more rainfall than the climate average for Kruger National Park (MacFadyen et

al., 2018). The African buﬀalo movement data we analyzed indicates that the individual

mostly occupied the northern and western extent of the region during the two week time

period, but traveled approximately 15 km between major surface water sources to the

southeastern portion of the region during October 7–9, 2005.

We speciﬁed the recharge function to include an intercept (θ0) and covariates for

elevation, slope, surface water proximity (< 0.5 km buﬀer to nearest surface water),

and an interaction for elevation×slope to examine the evidence for an eﬀect of water

and other resources for which topography may serve as a surrogate on physiological

recharge during a time when it is diﬃcult to predict the widespread availability of water

and forage during the transition from dry to wet season in this region. For movement

covariates, we used elevation, slope, and distance to nearest surface water.

We ﬁt recharge-based hierarchical movement models to the African buﬀalo telemetry

data shown in Figure 3. The full set of priors and hyperparameter settings, as well as

pseudocode and computational details to ﬁt the full recharge-based movement model,

are provided in Online Appendix C. As in the mountain lion data analysis, we also

examined a set of simpler models, including hierarchical models that incorporate M0

14

and M1 separately with all covariates as well as M1 with only surface water covariates

both together with M0 and separately.

Similar to our mountain lion results, the reduced recharge model based only on

surface water covariates had a better predictive score than the other models we ﬁt (Online

Appendix C). The left half of Figure 6 (labeled “behavior”), which shows the marginal

posterior distribution for the movement parameter, indicates that the African buﬀalo

orients toward surface water when it makes the decision to recharge during this time

period. Furthermore, the right half of Figure 6 indicates that surface water proximity

increased the recharge function itself. These results agree with previous ﬁndings (e.g.,

Redfern et al., 2003) that surface water in this region is an important predictor of African

buﬀalo movement.

Displayed in the same way as the mountain lion results, Figure 7 shows the posterior

marginal trajectories as well as posterior median for g(t) and ρ(t) for the African buﬀalo.

The posterior inference indicates that the African buﬀalo individual we analyzed needed

to recharge regularly throughout the time period based on the large values for ρ(t)

overall. However, brief and fairly regular periods where the posterior mean for z(t)

dropped below 0.5 in Figure 7e indicate short forays away from water resources. One

such period where the decision process was not dominated by z(t) = 1 occurred when the

individual looped to the southeast of the study area (October 7–8, 2005). Our analysis

shows that the recharge function started high (near zero) and then mostly decreased

as the individual ventured farther from surface water until eventually looping back to

the north at which point the recharge function increased again (Figure 7a,d). In fact,

Figure 7a shows the areas associated with increases in the recharge function in green.

This spatially-explicit inference indicates that low lying areas near the Sabie River and

tributaries are associated with recharge for the African buﬀalo individual we analyzed

(Figure 7a). Furthermore, the fact that the recharge model including surface water

proximity covariates had a better predictive score than the simpler models (M0 and

M1) ﬁt separately, suggests that a physiological recharge signal related to the covariates

is present in the movement trajectory for the African buﬀalo.

15

4 Discussion

Our example data analyses provided evidence that both the mountain lion and African

buﬀalo data sets contained a physiological signal whose variation is at least partially ex-

plained by environmental features. In the case of the mountain lion, a model comparison

indicated that proximity to prey kill area was the primary factor inﬂuencing the recharge

and movement processes. This result agrees with other recent studies (i.e., Buderman et

al., 2018) that mountain lion movement patterns are strongly inﬂuenced by predatory

behavior. Our analysis of the African buﬀalo data suggested that recharge-based dy-

namics were important because the simpler models that do not directly account for an

underlying physiological process had worse predictive scores. In the case of the African

buﬀalo data we analyzed, the inferred spatial pattern associated with recharge in Fig-

ure 7a indicated a clear relationship between probable surface water and recharge and

this was conﬁrmed by the posterior distributions for movement and recharge parameters

(Figure 6). Previous studies of African buﬀalo indicate that, while movement is largely

driven by water resources, other factors such as forage, social dynamics, and cover may

also inﬂuence space use (Ryan et al., 2006; Winnie et al., 2008). These additional factors

could be examined in more detailed studies that combine recharge and social dynamics

with plant ecology and energetics.

In general, the feedback between animal decision making, physiology, and movement

is a complex process that involves both intrinsic and extrinsic factors (Morales et al.,

2005; Nathan at al., 2008; Morales et al., 2010). For example, connections between en-

ergetics, memory, and movement directly inﬂuence the way we infer animal home ranges

(B¨orger et al., 2008). Despite calls for more thoughtful frameworks to model movement

that consider mechanisms explicitly, many modern approaches to modeling animal tra-

jectories are still purely phenomenological. Recent advances in biotelemetry technology

have given rise to massive repositories of high-resolution individual-based data (“aux-

iliary data”) that often accompany more conventional position-based telemetry data

(Brown et al., 2013). These auxiliary data are collected to measure characteristics of

individual ﬁtness and behavior (e.g., Elliot et al., 2013; Leos-Barajas et al., 2017) and

16

may provide a more direct link to understand physiological recharge.

Leveraging the hierarchical modeling framework to combine data sources (Hobbs and

Hooten, 2015), we can integrate auxiliary data into the recharge-based animal movement

model (Online Appendix E). Such model structures have become common in population

and community ecology where they are referred to as “integrated population models”

(Schaub and Abadi, 2011). When we have auxiliary accelerometer data, it may be

possible to connect the ﬁne-scale measurements of micro-movement to the change in

position directly (Wilson et al., 1991). In that case, it is sensible to let the auxiliary

data inform both the trajectory process and the physiological recharge process directly.

In situations where multiple forms of auxiliary data are recorded (e.g., accelerometer and

body condition measurements), we can augment the integrated movement model with

additional data models that are connected to the latent model components, partitioning

the recharge functions further as needed (Online Appendix E).

Overall, the framework we present allows researchers to connect the mechanisms re-

lated to known physiological characteristics with more conventional telemetry data to

account for latent physiological and individual-based decision processes. Our approach is

ﬂexible and allows for modiﬁcations to the form of both movement (6)–(7) and recharge

functions (1) and (3). As with any mixture model, some structure allows the data to bet-

ter separate model components so that parameters are identiﬁable. In our case studies,

we speciﬁed the movement model such that one term (M0) represents random diﬀusive

movement and the other term (M1) captures movement in response to environmental

variables. This helps us learn about the recharge function in a way that corresponds to

our preexisting knowledge about the physiology of these species. In Online Appendix

E, we show how to extend the recharge-based movement model to accommodate vari-

ous sources of auxiliary data to better recognize and estimate the physiological process

components depending on available data.

For some species, it may be appropriate to consider additional stochasticity in the

recharge process because of unobservable interactions with conspeciﬁcs, allospeciﬁcs,

or other dynamic environmental conditions. Our framework can readily accommodate

these sources of overdispersion by specifying the recharge functions g(v, t) as SDEs (in

17

addition to the movement process). Statistical inference in these settings relies on our

ability to observe enough data to successfully estimate the various sources of uncertainty

in the model. Auxiliary data, such as those described above, may be helpful to partition

and estimate parameters in these more general models.

We formulated the recharge-based movement models in continuous time for our appli-

cations to account for irregular telemetry and auxiliary data when available, but, like all

continuous-time models that require numerical solutions, our model is ﬁt using an intu-

itive discrete time approximation. In cases where the telemetry data are high-resolution

and temporally regular, the movement models (i.e., M0 and M1) themselves can be

formulated directly in discrete time using either the velocity vectors (e.g., Jonsen et al.,

2005) or polar coordinates associated with discrete moves (e.g., Morales et al., 2004;

Langrock et al., 2012; McClintock et al., 2012). In this setting, the movement process

and physiological recharge function are limited to the chosen temporal resolution and

the associated inference is resolution-dependent.

While our recharge-based movement modeling framework facilitates the inclusion of

mechanisms related to physiology, it can also be used as a way to accommodate latent

sources of dependence. The physiological recharge functions we speciﬁed in (1) and (3)

impart a type of long memory in the stochastic process models that we exploit to learn

about the inﬂuences of landscape and other spatial features on movement. However, time

series analyses have relied on long-memory processes to account for dependence in data

for many other applications (Beran, 1994). In terms of animal memory explicitly, its

inﬂuence on movement has been investigated separately (e.g., Fagan et al., 2013; Avgar

et al., 2013; Bracis et al., 2015; Bracis and Mueller, 2017; Merkle et al., 2017), but it

has not been accommodated in the way we describe herein, especially in the context of

physiological processes.

Acknowledgements

The authors thank the editors and three anonymous reviewers whose comments helped

improve this work. The authors also thank Jake Ivan, Mat Alldredge, Ephraim Hanks,

18

Franny Buderman, Devin Johnson, Daisy Chung, and Brett McClintock for numerous

helpful discussions and previous research in this area. This research was funded by NSF

DMS 1614392 (MBH) and PICT 2015 0815 (JMM). Any use of trade, ﬁrm, or product

names is for descriptive purposes only and does not imply endorsement by the U.S.

Government. Data and computer code are available at:

<https://github.com/henryrscharf/Hooten_et_al_EL_2018>.

References

Alcock, J. 2009. Animal Behavior: An Evolutionary Approach. Sinauer. Sunderland,

Massachusetts, USA.

Alexander, R.M. 2003. Principles of Animal Locomotion. Princeton University Press.

Princeton, New Jersey, USA.

Avgar, T., R. Deardon, and J.M. Fryxell. (2013). An empirically parameterized individ-

ual based model of animal movement, perception, and memory. Ecological Modeling,

251: 158-172.

Bar-David, S., I. Bar-David, P.C. Cross, S.J. Ryan, C.U. Knechtel, and W.M. Getz.

(2009). Methods for assessing movement path recursion with application to African

buﬀalo in South Africa. Ecology, 90: 2467-2479.

Bracis, C., E. Gurarie, B. Van Moorter, and R.A. Goodwin. (2015). Memory eﬀects on

movement behavior in animal foraging. PloS One, 10: e0136057.

Bracis, C. and T. Mueller. (2017). Memory, not just perception, plays an important

role in terrestrial mammalian migration. Proceedings of the Royal Society B, 284:

20170449.

Beran, J. (1994). Statistics for Long-Memory Processes. Chapman & Hall/CRC.

Blake, L.W. and E.M. Gese. (2016). Resource selection by cougars: Inﬂuence of behav-

ioral state and season. The Journal of Wildlife Management, 80: 1205-1217.

19

Blecha, K.A. (2015). Risk-reward tradeoﬀs in the foraging strategy of cougar (Puma

concolor): Prey distribution, anthropogenic development, and patch selection. Thesis,

Colorado State University, Fort Collins, CO.

Bleicher, S.S. (2017). The landscape of fear conceptual framework: Deﬁnition and review

of current applications and misuses. PeerJ, 5: e3772.

B¨orger, L., B.D. Dalziel, and J.M. Fryxell. (2008). Are there general mechanisms of

animal home range behaviour? A review and prospects for future research. Ecology

Letters, 11: 637-650.

Brown, D., R. Kays, M. Wikelski, R. Wilson, R., and A.P. Klimley. (2013). Observing

the unwatchable through acceleration logging of animal behavior. Animal Bioteleme-

try, 1: 1-16.

Buderman, F.E., M.B. Hooten, M. Aldredge, and J.S. Ivan.

(2018). Time-varying

predatory behavior is primary predictor of ﬁne-scale movement of wildland-urban

cougars. Movement Ecology, 6: 22.

Brillinger, D.R. (2010). Modeling spatial trajectories. In Gelfand, A. E., P. J. Diggle,

M. Fuentes, and P. Guttorp, editors, Handbook of Spatial Statistics, chapter 26, pages

463-475. Chapman & Hall/CRC, Boca Raton, Florida, USA.

Cagnacci, F., L. Boitani, R.A. Powell, and M.S. Boyce. (2010). Animal ecology meetings

GPS-based radiotelemetry: A perfect storm of opportunities and challenges. Philo-

sophical Transactions of the Royal Society of London B: Biological Sciences, 365:

2157-2162.

Colgan, P. (1989). Animal Motivation. Springer Netherlands.

Cooke, S.J., S.G. Hinch, M. Wikelski, R.D. Andrews, L.J. Kuchel, T.G. Wolcott, and

P.J. Butler.

(2004). Biotelemetry: a mechanistic approach to ecology. Trends in

Ecology and Evolution, 19: 334-343.

Cornelis, D., M. Melletti, L. Korte, S.J. Ryan, M. Mirabile, T. Prin, and H.H.T. Prins.

(2014). African Buﬀalo Syncerus caﬀer.

In: Ecology, Evolution and Behaviour of

20

Wild Cattle. Melletti, M. and J. Burton (eds.). Cambridge University Press.

Dudeck, B.P., M. Clinchy, M.C. Allen, and L.Y. Zanette. (2018). Fear aﬀects parental

care, which predicts juvenile survival and exacerbates the total cost of fear on demog-

raphy. Ecology, 99: 127-135.

Eggleston, D.B. and R.N. Lipcius.

(1992). Shelter selection by spiny lobster under

variable predation risk, social conditions, and shelter size. Ecology, 73: 992-1011.

Elliott, K.H., M. Le Vaillant, A. Kato, J.R. Speakman, and Y. Ropert-Coudert. (2013).

Accelerometry predicts daily energy expenditure in a bird with high activity levels.

Biology Letters, 9: 20120919.

Fagan, W.F., M.A. Lewis, M. AugerM´eth´e, T. Avgar, S. Benhamou, G. Breed, L.

LaDage, U.E. Schlgel, W.W. Tang, Y.P. Papastamatiou, and J. Forester.

(2013).

Spatial memory and animal movement. Ecology Letters, 16: 1316-1329.

Full, R., D. Zuccarello, and A. Tullis. (1990). Eﬀect of variation in form on the cost of

terrestrial locomotion. Journal of Experimental Biology, 150: 233-246.

Gelfand, A.E. and A.F. Smith.

(1990). Sampling-based approaches to calculating

marginal densities. Journal of the American Statistical Association, 85: 398-409.

Getz, W.M., S. Fortmann-Roe, P.C. Cross, A.J. Lyons, S.J. Ryan, and C.C. Wilmers.

(2007). LoCoH: nonparameteric kernel methods for constructing home ranges and

utilization distributions.PloS one,2(2), e207.

Green, J.A. (2011). The heart rate method for estimating metabolic rate: review and

recommendations. Comparative Biochemistry and Physiology Part A: Molecular and

Integrative Physiology, 158: 287-304.

Halsey, L.G. (2016). Terrestrial movement energetics: Current knowledge and its appli-

cation to the optimising animal. Journal of Experimental Biology, 219: 1424-1431.

Hanks, E.M., M.B. Hooten, and M. Alldredge. (2015). Continuous-time discrete-space

models for animal movement. Annals of Applied Statistics, 9: 145-165.

21

Hobbs, N.T. and M.B. Hooten.

(2015). Bayesian Models: A Statistical Primer for

Ecologists. Princeton University Press.

Hooten, M.B. and N.T. Hobbs. (2015). A guide to Bayesian model selection for ecolo-

gists. Ecological Monographs, 85: 3-28.

Hooten, M.B. and D.S. Johnson. (2017a). Basis function models for animal movement.

Journal of the American Statistical Association, 112: 578-589.

Hooten, M.B. and D.S. Johnson. (2019). Modeling Animal Movement. Gelfand, A.E.,

M. Fuentes, and J.A. Hoeting (eds). In Handbook of Environmental and Ecological

Statistics. Chapman and Hall/CRC.

Hooten, M.B., D.S. Johnson, B.T. McClintock, and J.M. Morales.

(2017). Animal

Movement: Statistical Models for Telemetry Data. Chapman and Hall/CRC.

Hooten, M.B., H.R. Scharf, T.J. Heﬂey, A. Pearse, and M. Weegman. (2018). Animal

movement models for migratory individuals and groups. Methods in Ecology and

Evolution, 9: 1692-1705.

Houston A.I. and J.M. McNamara. (1999). Models of Adaptive Behaviour. Cambridge

University Press. Cambridge, United Kingdom.

Humphries, M.M. and V. Careau. (2011). Heat for nothing or activity for free? Ev-

idence and implications of activity-thermoregulatory heat substitution.

Integrative

and Comparative Biology, 51: 419-431.

Husseman, J.S., D.L. Murray, G. Power, C. Mack, C. Wenger, and H. Quigley. (2003).

Assessing diﬀerential prey selection patterns between two sympatric large carnivores.

Oikos, 101: 591-601.

Ingraham, M.W. and S.G. Foster, S.G. (2008). The value of ecosystem services pro-

vided by the US National Wildlife Refuge System in the contiguous US. Ecological

Economics, 67: 608-618.

Jonsen, I.D., J.M. Flemming, and R.A. Myers. (2005). Robust statespace modeling of

animal movement data. Ecology, 86: 2874-2880.

22

Karasov, W.H. (1992). Daily energy expenditure and the cost of activity in mammals.

American Zoology, 32: 238248.

Kays, R., M. Crofoot, W. Jetz, and M. Wikelski. (2015). Terrestrial animal tracking as

an eye on life and planet. Science, 384(6240): aaa2478.

Kloeden, P.E. and E. Platen.

(1992). Numerical Solution of Stochastic Diﬀerential

Equations. Springer, Berlin.

Knopﬀ, K. H., A. A. Knopﬀ, M. B. Warren, and M. S. Boyce. (2009). Evaluating global

positioning system telemetry techniques for estimating cougar predation parameters.

Journal of Wildlife Management, 73: 586-597.

Langrock, R., R. King, J. Matthiopoulos, L. Thomas, D. Fortin, and J. Morales. (2012).

Flexible and practical modeling of animal telemetry data: Hidden Markov models and

extensions. Ecology, 93: 2336-2342.

Laundr´e, J.W., L. Hern´andez, and K.B. Altendorf.

(2001). Wolves, elk, and bison:

Reestablishing the “landscape of fear” in Yellowstone National Park. Canadian Jour-

nal of Zoology, 79: 1401-1409.

Lebreton, J.D., K.P. Burnham, J. Clobert, and D.R. Anderson.

(1992). Modeling

survival and testing biological hypotheses using marked animals: a uniﬁed approach

with case studies. Ecological Monographs, 62: 67-118.

Leos-Barajas, V., T. Photopoulou, R. Langrock, T.A. Patterson, Y.Y. Watanabe, M.

Murgatroyd, and Y.P. Papastamatiou. (2017). Analysis of animal accelerometer data

using hidden Markov models. Methods in Ecology and Evolution, 8: 161-173.

Matthiopoulos, J., J. Fieberg, G. Aarts, H.L. Beyer, J.M. Morales, and D.T. Haydon.

(2015). Establishing the link between habitat selection and animal population dy-

namics. Ecological Monographs, 85: 413-436.

McClintock, B.T., R. King, L. Thomas, J. Matthiopoulos, B.J. McConnell, and J.M.

Morales. (2012). A general discrete-time modeling framework for animal movement

using multistate random walks. Ecological Monographs, 82: 335-349.

23

MacFadyen, S., N. Zambatis, A.J. Van Teeﬀelen, and C. Hui. (2018). Long-term rainfall

regression surfaces for the Kruger National Park, South Africa: A spatiotemporal

review of patterns from 1981 to 2015. International Journal of Climatology, 38: 2506-

2519.

McKellar, A.E., R. Langrock, J.R. Walters, and D.C. Kesler.

(2015). Using mixed

hidden Markov models to examine behavioral states in a cooperatively breeding

bird.Behavioral Ecology,26: 148-157.

Merkle, J.A., J.R. Potts, and D. Fortin. (2017). Energy beneﬁts and emergent space

use patterns of an empirically parameterized model of memory-based patch selection.

Oikos, 126: 185-195.

Morales, J.M., D.T. Haydon, J. Frair, K.E. Holsinger, and J.M. Fryxell. (2004). Extract-

ing more out of relocation data: Building movement models as mixtures of random

walks. Ecology, 85: 2436-2445.

Morales J.M., D. Fortin, J. Frair and E. Merrill. (2005). Adaptive models for large

herbivore movements in heterogeneous landscapes. Landscape Ecology, 20: 301-316.

Morales J.M., P.R. Moorcroft, J. Matthiopoulos, J.L. Frair, J.K. Kie, R.A. Powell, E.H.

Merrill, and D.T. Haydon. (2010). Building the bridge between animal movements

and population dynamics. Philosophical Transactions of the Royal Society, Series B,

365: 2289-2301.

Naidoo, R., P. Du Preez, G. Stuart-Hill, M. Jago, and M. Wegmann. (2012). Home

on the range:

factors explaining partial migration of African buﬀalo in a tropical

environment.PLoS one,7(5), e36527.

Nathan, R., W.M. Getz, E. Revilla, M. Holyoak, R. Kadmon, D. Saltz, and P.E. Smouse.

(2008). A movement ecology paradigm for unifying organismal movement research.

Proceedings of the National Academy of Sciences, 105: 19052-19059.

Nussbaum, M. (1978). Aristotle’s De Motu Animalium: Text with Translation, Com-

mentary, and Interpretive Essays. Princeton University Press, Princeton, New Jersey,

24

USA.

Oliveira-Santos, L.G.R., J.D. Forester, U. Piovezan, W.M. Tomas, and F.A. Fernandez.

(2016). Incorporating animal spatial memory in step selection functions. Journal of

Animal Ecology, 85: 516-524.

Pollock, K.H. (1991). Modeling capture, recapture, and removal statistics for estimation

of demographic parameters for ﬁsh and wildlife populations: Past, present, and future.

Journal of the American Statistical Association, 86: 225-238.

Preisler, H.K., A.A. Ager, and M.J. Wisdom.

(2013). Analyzing animal movement

patterns using potential functions. Ecosphere, 4: 1-13.

Prins, H.H.T. (1996). Ecology and Behaviour of the African Buﬀalo: Social Inequality

and Decision Making. London: Chapman & Hall.

Prins, H.H.T. and A.R.E. Sinclair. (2013). Syncerus caﬀer. In: The Mammals of Africa.

Kingdon, J.S. and M. Hoﬀmann (eds.). Amsterdam: Academic Press.

Proaktor, G., T. Coulson, and E.J. Milner-Gulland. (2008). The demographic conse-

quences of the cost of reproduction in ungulates. Ecology, 89: 2604-2611.

Radloﬀ, F.G. and J.T. Du Toit. (2004). Large predators and their prey in a southern

African savanna: a predator’s size determines its prey size range. Journal of Animal

Ecology 73: 410-423.

Redfern, J.V., R. Grant, H. Biggs, and W.M. Getz. (2003). Surfacewater constraints on

herbivore foraging in the Kruger National Park, South Africa. Ecology, 84: 2092-2107.

Ryan, S.J., C.U. Knechtel, and W.M. Getz. (2006). Range and habitat selection of

African buﬀalo in South Africa. The Journal of Wildlife Management, 70: 764-776.

Savage, V.M. and G.B. West. (2007). A quantitative, theoretical framework for under-

standing mammalian sleep. Proceedings of the National Academy of Sciences, 104:

1051-1056.

Scharf, H.R., M.B. Hooten, B.K. Fosdick, D.S. Johnson, J.M. London, and J.W. Durban.

25

(2016). Dynamic social networks based on movement. Annals of Applied Statistics,

10: 2182-2202.

Scharf, H.R., M.B. Hooten, D.S. Johnson, and J.W. Durban. (2018). Process convolu-

tion approaches for modeling interacting trajectories. Environmetrics, e2487.

Schaub, M. and F. Abadi.

(2011).

Integrated population models: A novel analysis

framework for deeper insights into population dynamics. Journal of Ornithology, 152:

227-237.

Schick, R.S., S.R. Loarie, F. Colchero, B.D. Best, A. Boustany, D.A. Conde, P.N. Halpin,

L.N. Joppa, C.M. McClellan, and J.S. Clark. (2008). Understanding movement data

and movement processes: Current and emerging directions. Ecology Letters, 11:

1338-1350.

Schick, R.S., S.D. Kraus, R.M. Rolland, A.R. Knowlton, P.K. Hamilton, H.M. Pettis,

R.D. Kenney, and J.S. Clark. (2013). Using hierarchical Bayes to understand move-

ment, health, and survival in the endangered North Atlantic right whale. PloS one,

8: e64166.

Shepard, E.L.C., R.P. Wilson, W.G. Rees, E. Grundy, S.A. Lambertucci, and S.B.

Vosper. (2013). Energy landscapes shape animal movement ecology. American Nat-

uralist, 182: 298-312.

Sinclair, A.R.E. (1977). The African Buﬀalo: A Study of Resource Limitation of Popu-

lations. University of Chicago Press. Chicago, IL, USA.

Spalinger, D.E. and N.T. Hobbs. (1992). Mechanisms of foraging in mammalian herbi-

vores: New models of functional response. The American Naturalist, 140: 325-348.

Stephens, D.W., J.S. Brown, and R. Ydenberg. (2007). Foraging Behavior and Ecology.

University of Chicago Press. Chicago, IL, USA.

Taylor, C.R., N.C. Heglund, and G.M. Maloiy. (1982). Energetics and mechanics of

terrestrial locomotion. I. Metabolic energy consumption as a function of speed and

body size in birds and mammals. Journal of Experimental Biology, 97: 1-21.

26

Tshipa, A., H. Valls-Fox, H. Fritz, K. Collins, L. Sebele, P. Mundy, and S. Chamaill´e-

Jammes. (2017). Partial migration links local surface-water management to large-

scale elephant conservation in the world’s largest transfrontier conservation area. Bi-

ological Conservation, 215: 46-50.

Turchin, P. (1998). Quantitative Analysis of Movement: Measuring and Modeling Pop-

ulation Redistribution in Animals and Plants. Sinauer. Sunderland, Massachusetts,

USA.

Williams, T. M., L. Wolfe, T. Davis, T. Kendall, B. Richter, Y. Wang, C. Bryce, G.H.

Elkaim, and C.C. Wilmers.

(2014).

Instantaneous energetics of puma kills reveal

advantage of felid sneak attacks. Science, 346: 81-85.

Wilmers, C.C., B. Nickel, C.M. Bryce, J.A. Smith, R.E. Wheat, and V. Yovovich. (2015).

The golden age of biologging: How animalborne sensors are advancing the frontiers

of ecology. Ecology, 96: 1741-1753.

Wilmers, C.C., L.A. Isbell, J.P. Suraci, and T.M. Williams. (2017). Energetics-informed

behavioral states reveal the drive to kill in African leopards. Ecosphere, 8: e01850.

Wilson, R.P., M.P.T. Wilson, R. Link, H. Mempel, and N.J. Adams. (1991). Determina-

tion of movements of African penguins Spheniscus demersus using a compass system:

Dead reckoning may be an alternative to telemetry. Journal of Experimental Biology,

157: 557-564.

Wilson, R., F. Quintana, and V. Hobson. (2012). Construction of energy landscapes

can clarify the movement and distribution of foraging animals. Proceedings of the

Royal Society, Series B, 279: 975-980.

Winnie, J.A., P. Cross, and W. Getz. (2008). Habitat quality and heterogeneity in-

ﬂuence distribution and behavior in African buﬀalo (Syncerus caﬀer ). Ecology, 89:

1457-1468.

Whoriskey, K., M. Auger-M´eth´e, C.M. Albertsen, F.G. Whoriskey, T.R. Binder, C.C.

Krueger, and J. Mills Flemming.

(2017). A hidden Markov movement model for

27

rapidly identifying behavioral states from animal tracks. Ecology and Evolution, 7:

2112-2121.

Zuntz, N. (1897). Uber den Stoﬀverbrauch des Hundes bei Muskelarbeit. Pﬂugers

Archiv, 68: 191-211.

28

Figure 1: a) The simulated environmental covariates w(µ) that may inﬂuence the

recharge function (left: large scale spatial process, middle: small scale spatial pro-

cess, right: patch; b) an example physiological landscape based on the environmental

covariates with example individual trajectory (µ(t), for all t ∈ T ) shown as solid

line beginning at solid point and ending at the arrow; c) The physiological recharge

function arising from the path integral of the physiological landscape associated with

trajectory. Numbered circles represent time points at which the simulated individual

is charged (red) and discharged (green).

29

Figure 2: Schematic of recharge and movement model components. The observed telemetry data (s(ti),
red and green points along trajectory) at time ti are measurements (with error) of the true positions µ(ti)

(blue triangle, left, for a given observation time ti). The underlying continuous-time trajectory µ(t) is

shown as the solid blue line and is conditionally modeled based on the movement dynamics (incorporated

in models M0 and M1) and possibly changes in the environment (incorporated in model M1). In this

example, the brown circle in the middle of the study area represents a recharge region or patch where the

individual may recharge its energy (e.g., a prey kill area). The binary decision z(t) to recharge indicates

when the individual responds to the underlying landscape (in this case, it may be attracted to the recharge

region). While z(t) is represented as a continuous-time binary process in our model, this ﬁgure shows the

subset of decisions associated with the observed telemetry data (numbered points in bottom plot). In the

ﬁgure, decisions to recharge (z(t) = 1) are green and are otherwise shown in red (z(t) = 0). The stochastic

binary decision process is governed by the probability function ρ(t) (shown as solid black line in bottom

plot), which is, in turn, a function of the recharge process g(t) (not shown).

30

Figure 3: World map depicting the regions where the telemetry data in our examples

arise from a GPS collared mountain lion and African buﬀalo. Telemetry data

are shown as black points on blown up maps, with elevation shown as background

shading; high (relative) elevations shown as lighter shading.

31

Figure 4: Marginal posterior violin plots for the mountain lion model parameters a)

β and b) θ.

32

−2000001000020000bbehaviordist. to kill areaa)−2−1012qrechargeintercept<1km to kill areab)Figure 5: Posterior median associated with the mountain lion data analysis for the a) recharge function
g(t) shown as color on top of the posterior mean trajectory µ(t). Prey kill area (i.e., convex polygon with

1 km buﬀer from prey kill site clusters) shown as green region indicating area associated with recharge.

Distance to prey kill area is shown in the background for reference (with small distances indicated by darker

shades). Map in (a) oriented such that north is up. Posterior median trajectories (b, c) and d) recharge

function g(t) and e) decision probability ρ(t) with 95% credible intervals shown in gray with posterior mean

for the decision z(t) shown as black points. Color corresponds to the value of the recharge function. Proﬁle

of distance to prey kill area shown as gray line in (b) and (c) for reference. Green rug at the bottom of

(b) represents times when recharge occurred.

33

445460easting [km]llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll43554380northing [km]llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll−22timegr0.00.51.0llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll2011−04−252011−05−012011−05−062011−05−112011−05−17a)b)c)d)e)xg(t)3.56−1.350Figure 6: Marginal posterior violin plots for the African buﬀalo model parameters a)

β and b) θ.

34

−200−1000100200bbehaviordist. to surface watera)−0.1−0.0500.050.1qrechargeintercept<0.5km to surface waterb)Figure 7: Posterior median associated with the African buﬀalo data analysis for the a) recharge function
g(t) shown as color on top of the posterior mean trajectory µ(t). Distance to surface water is shown in the

background for reference (with small distances indicated by darker shades) and green indicating inferred

areas associated with recharge. Map in (a) oriented such that north is up. Posterior median trajectories

(b, c) and d) recharge function g(t) and e) decision probability ρ(t) with 95% credible intervals shown in

gray with posterior mean for the decision z(t) shown as black points. Color corresponds to the value of

the recharge function. Distance to surface water proﬁle shown as gray line in (b) and (c) for reference.

Green rug at the bottom of (b) represents times when the recharge function is increasing.

35

385395easting [km]llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll−2780−2760northing [km]llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll−2.00.0timegr0.00.51.0lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll2005−10−012005−10−052005−10−102005−10−15a)b)c)d)e)xg(t)−0.446−1.62Appendix A: Derivation of Aggregated Recharge Pro-

cess

In what follows, we show how to obtain the aggregated recharge process g(t) as a function

of the physiological recharge functions g(v, t). Consider the integral of g(v, t) over V

g(t) =

=

(cid:90)

V
(cid:90)

V

g(v, t)dv ,

g0(v) +

(cid:90)

(cid:90) t

V
(cid:90) t

0
(cid:90)

(cid:90) t

0

w(cid:48)(µ(τ ))θ(v)dτ dv ,

w(cid:48)(µ(τ ))θ(v)dτ dv ,

w(cid:48)(µ(τ ))θ(v)dvdτ ,

V

w(cid:48)(µ(τ ))θdτ ,

0
(cid:90) t

0

= g0 +

= g0 +

= g0 +

(10)

(11)

(12)

(13)

(14)

The key aspect of the derivation above in involves the use of Fubini’s theorem to change

the order of integration in (13) which yields the following results

g0 =

θ =

(cid:90)

V
(cid:90)

V

g0(v)dv ,

θ(v)dv .

(15)

(16)

Appendix B: Analysis of Simulated Data

To demonstrate the hierarchical movement model with recharge dynamics, we simulated

a set of telemetry data with n = 500 observations based on the following speciﬁcation

for the movement and recharge components of the model. The ﬁrst model component

M0, implies our simulated trajectory will arise as a random walk resembling nomadic

behavior when the individual is in a charged state. For the potential function associated

with the decision to recharge, we speciﬁed p(µ(t), β) = x(cid:48)(µ(t))β, implying that the

movement of the simulated individual may be inﬂuenced by the gradient of a linear

36

combination of our covariates x(µ). In our simulation, we considered a single spatial

covariate x(µ(t)) deﬁned as the Euclidean distance to a patch polygon in the study

area (Figure 8a; where the patch itself may be desirable to the individual because it

represents a central place, energy resource, etc). Thus, the potential function for our

recharge movement process simpliﬁes to p(µ(t), β) = βx(µ(t)) (with β = −55658.2

simulating a trajectory with drift toward the patch when the individual is discharged).

Note that there is no intercept in this potential function because it does not aﬀect the

gradient in the movement model.

We speciﬁed the recharge process based on the expression g(t) and using g0 = −1
and w(µ(t)) = (1, w(µ(t)))(cid:48) where w(µ(t)) = 1 if the individual is in the recharge patch

(green polygon in Figure 8a) at time t, and zero otherwise. For recharge coeﬃcients, we

used θ = (θ0, θ1)(cid:48) with θ0 = −1 and θ1 = 4. This formulation for the recharge function

g(t) implies a recharge rate that is three times as fast as the discharge rate, which may

be more realistic for certain types of recharge processes (e.g., energetics; Figure 8b).

The remaining parameters used to simulate data were speciﬁed as: σ2

0 =
1 = 0.03. For the hierarchical movement model based on recharge dynamics

s = 10−5, σ2

0.02, and σ2

ﬁt to simulated data, we speciﬁed priors for each of the model parameters as:

(cid:2)σ2

s

(cid:3) = IG(qs = 2.000122, rs = 3.000122 × 10−5)

Hyperparameters chosen so that mode of prior is 10−5 and variance is 10−2.

(cid:2)σ2

0

(cid:3) = IG(q0 = 2.003556, r0 = 0.06007113)

Hyperparameters chosen so that mode of prior is 0.02 and variance is 1.

(cid:2)σ2

1

(cid:3) = IG(q1 = 2.008019, r1 = 0.09024058)

Hyperparameters chosen so that mode of prior is 0.03 and variance is 1.

[β] = N(µβ, Σβ), µβ = 0, Σβ = 2.513

[g0] = N(µg0, σ2

g0), µg0 = 0, σ2

g0 = 1

[θ] = N(µθ, Σθ), µθ = 0, Σθ = 1000I2

37

(17)

(18)

(19)

(20)

(21)

(22)

Figure 8: a) Simulated trajectory µ(t) in two dimensions and b) associated recharge

(g(t)) and c) decision probability (ρ(t)). The green polygon shown in the middle of

(a) represents a patch that corresponds to recharge and the single covariate based on

distance to patch is shown in (a) as shading from light (near patch) to dark (far from

patch). The trajectory color corresponds to the time elapsed since the initial point

of the study period (increasing from dark blue to yellow). The simulated decision

process z(t) is shown as semitransparent points at the top (z(t) = 1) and bottom

(z(t) = 0) of the plot for ρ(t) in (c).

38

−202g0.00.40.8ra)b)c)05101520tThe temporal grid contained m = 1500 time points. We standardized all covariates so

that the mean slope along the trajectory was approximately 1. We then speciﬁed weakly

informative zero-mean normal priors for β with standard deviation 50, corresponding

to a belief that the contribution made by the covariate to the total displacement of

an individual should be less than about 100 spatial units per full temporal unit. On

the scale of the untransformed covariate, this corresponds to a standard deviation of

approximately 56. For θ, the prior standard deviation of 31.62 corresponds to a belief

that the individual will change from fully charged to fully depleted no more than about

50 times per whole time unit.

We ﬁt the recharge-based movement model to the simulated data shown in Figure 8.

We also ﬁt the simpler hierarchical models including only M1 (z(t) = 1 for all t) and M0

(z(t) = 0 for all t) and scored them to assess predictive ability using the approach de-

scribed in Appendix C. Cross-validation indicated that we were able to correctly identify

the recharge-based movement model as the data generating model when compared to the

simpler alternatives based only on M1 and M0. The marginal posterior distributions

for β and θ are shown in Figure 9.

Figure 9: Marginal posterior violin plots for a) β1 (left), and b) θ0 (center) and θ1

(right). True values used to simulate data shown as black points.

The model properly recovers the parameters, indicating that the simulated individual

39

l−2e+05−1e+0501e+052e+05bbehaviordist. to polygona)ll−8−4048qrechargeinterceptpolygonb)moves toward the patch when needing to recharge and then recharging inside the patch

at a faster rate than the discharge outside the patch. The associated posterior inference

for the recharge function g(t) and probability of decision to recharge ρ(t) are shown in

Figure 10.

The results shown in Figure 10 indicate that we are able to use the recharge-based

movement model to learn about an underlying physiological recharge function using

telemetry data alone. In fact, the posterior median recovers the pattern in the simulated

functions (Figure 10c–d) quite well, where the uncertainty increases appropriately when

the decision probability ρ(t) approaches one half.

Appendix C: Prior Speciﬁcations, Scoring, and Com-

puting Details

For the hierarchical movement model based on recharge dynamics ﬁt to the mountain

lion telemetry data, we speciﬁed priors for each of the model parameters as:

(cid:2)σ2

s

(cid:3) = IG(qs = 4.479787, rs = 54.79787)

Hyperparameters chosen so that mode of prior is 10 and variance is 100.

(cid:2)σ2

0

(cid:3) = IG(q0 = 4.479815, r0 = 21919260)

Hyperparameters chosen so that mode of prior is 4 × 106 and variance is 4 × 1012.

(cid:2)σ2

1

(cid:3) = IG(q1 = 4.479815, r1 = 21919260)

Hyperparameters chosen so that mode of prior is 4 × 106 and variance is 4 × 1012.

[β] = N(µβ, Σβ), µβ = 0, Σβ = 2.5 × 107I5
g0), µg0 = 0, σ2

[g0] = N(µg0, σ2

g0 =

[θ] = N(µθ, Σθ), µθ = 0, Σθ = 532I5

40

(23)

(24)

(25)

(26)

(27)

(28)

Figure 10: Telemetry data (points) and posterior mean trajectory (multicolored line)

for the a) easting and b) northing directions. Gray lines in (a) and (b) represent

the value of x(µ(t)) and green rug plot below (a) represents positions where the

recharge function is increasing. The posterior median c) recharge function g(t) and

d) associated probability ρ(t) of decision to recharge are shown as multicolored lines

with 95% credible intervals shown in gray (z(t) shown as black points). True values

of g(t) and ρ(t) are shown as red lines. The color associated with the estimates

indicates discharged when orange and charged when blue.

41

0.00.40.8xllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll0.40.60.81.0yllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll05101520−2024timegr0.00.51.0lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllla)b)c)d)The temporal grid contained m = 600 time points. We standardized all X covariates so

that the mean slope along the trajectory was approximately 1. We then speciﬁed weakly

informative zero-mean normal priors for β with standard deviation 5000, corresponding

to a belief that the contribution made by any given covariate to the total displacement

of an individual should be less than about 10 km per day. For θ, a standard deviation of

23.07 corresponds to a belief that the individual will change from fully charged to fully

depleted no more than about once per hour.

For the hierarchical movement model based on recharge dynamics ﬁt to the African

buﬀalo telemetry data, we speciﬁed priors for each of the model parameters as:

(cid:2)σ2

s

(cid:3) = IG(qs = 2.266181, rs = 3.266181)

Hyperparameters chosen so that mode of prior is 1 and variance is 25.

(cid:2)σ2

0

(cid:3) = IG(q0 = 4.479815, r0 = 493183.4)

Hyperparameters chosen so that mode of prior is 9 × 104 and variance is 9 × 108.

(cid:2)σ2

1

(cid:3) = IG(q1 = 4.479815, r1 = 493183.4)

Hyperparameters chosen so that mode of prior is 9 × 104 and variance is 9 × 108.

[β] = N(µβ, Σβ), µβ = 0, Σβ = 104I5

[g0] = N(µg0, σ2

g0), µg0 = 0, σ2

g0 = 1

[θ] = N(µθ, Σθ), µθ = 0, Σθ = 359I5

(29)

(30)

(31)

(32)

(33)

(34)

The temporal grid contained m = 1441 time points. We standardized all X covariates so

that the mean slope along the trajectory was approximately 1. We then speciﬁed weakly

informative zero-mean normal priors for β with standard deviation 100, corresponding

to a belief that the contribution made by any given covariate to the total displacement

of an individual should be less than about 200m per hour. For θ, a standard deviation

of 18.95, which corresponds to a belief that the individual will change from fully charged

to fully depleted no more than about once per hour.

42

Model

Score

Recharge full

15.45199

Recharge reduced 15.38224

M1,full

M1,reduced

M0

15.47527

15.44072

15.42810

Table 1: Predictive scores for mountain lion models (smaller scores indicate better

predictive models). Recharge full: recharge model including all covariates. Recharge

reduced: recharge model including only prey kill area covariates. M1,full: Hi-

erarchical model including all movement covariates assuming that all z(t) = 1.

M1,reduced: Hierarchical model including only prey kill area covariate, assuming

that all z(t) = 1. M0: Hierarchical model with no covariates, assuming that all

z(t) = 0.

We ﬁt the mountain lion and African buﬀalo models using 100000 MCMC iterations

(discarding the ﬁrst 50000 as burn-in and thinning the remainder at an interval of 10

iterations) which required approximately 20 hours for the most complex model on a

workstation with 3 Ghz 8-core Intel Xeon processor and 64 GB of RAM.

To score the models, we used the negative log posterior predictive density as a proper

predictive score computed using 8-fold cross-validation (Hooten and Hobbs, 2015). The

posterior predictive distribution is analytically intractable (along with the rest of the

posterior quantities of interest, as is typical in hierarchical Bayesian models), thus, we

estimated it using Monte Carlo integration based on a kernel density estimate of the

point-wise posterior predictive density evaluated at the hold out data. We averaged the

resulting quantities across equal-sized folds to arrive at the ﬁnal score for each model.

Smaller scores indicate better predictive performance.

The predictive scores for: 1) the mountain lion models are shown in Table 1, for the

African buﬀalo models are shown in Table 2, and 3) for the simulation models are shown

in Table 3.

43

Model

Score

Recharge full

13.34667

Recharge reduced 13.29791

M1,full

M1,reduced

M0

13.61633

13.59157

13.57993

Table 2: Predictive scores for African buﬀalo models (smaller scores indicate bet-

ter predictive models). Recharge full: Recharge model including all covariates.

Recharge reduced: recharge model including only surface water covariates. M1,full:

Hierarchical model including all movement covariates assuming that all z(t) = 1.

M1,reduced: Hierarchical model including only distance to surface water covariate,

assuming that all z(t) = 1. M0: Hierarchical model with no covariates, assuming

that all z(t) = 0.

Model

Score

Recharge

-5.458882

M1

M0

-5.447527

-5.443709

Table 3: Predictive scores for simulated data models (smaller scores indicate bet-

ter predictive models). Recharge: recharge model including recharge region covari-

ates. M1: Hierarchical model including recharge region covariates assuming that

all z(t) = 1. M0: Hierarchical model with no covariates assuming that all z(t) = 0.

44

Appendix D: Pseudo-code for obtaining draws from

posterior distribution

To ﬁt the model we used an MCMC algorithm with the following updates for model

parameters:

1. Update σ2

s ∼ [σ2

s |·] = IG(qs + n, rs + 1
2

(cid:80)n

i=1

(cid:80)2

d=1 (s(ti, d) − µ(ti, d))2) where d

indexes the two spatial dimensions (e.g., longitude and latitude).

2. Deﬁne a ﬁne grid of time points T over the study interval [0, T ] of size m such that

T ⊃ Tobs, where Tobs ≡ {t1, . . . , ti, . . . , tn} is the set of observation time points.

Let ∆tj = tj − tj−1.

(a) Update

µ(t1) ∼ [µ(t1)|·]

∝ (cid:2)µ(t2)|µ(t1), σ2

0, σ2

1, β, z(t2)(cid:3) (cid:2)s(t1)|µ(t1), σ2

s

(35)

(cid:3)1{t1∈Tobs}

m
(cid:89)

[z(tj)|g0, θ]

j=2

(36)

using a Metropolis random walk with an adaptively tuned bivariate Gaus-

sian proposal distribution. Note that we have suppressed notation for the

position process µ(t) in the conditional distribution for z(tj) to simplify the

expressions.

(b) For j = 2, . . . , m − 1 update

µ(tj) ∼ [µ(tj)|·] ∝

(cid:2)µ(tj+1)|µ(tj), σ2

0, σ2

1, β, z(tj+1)(cid:3) (cid:2)µ(tj)|µ(tj−1), σ2

0, σ2

1, β, z(tj)(cid:3)

× (cid:2)s(tj)|µ(tj), σ2

s

(cid:3)1{tj ∈Tobs}

m
(cid:89)

[z(tl)|g0, θ]

l=j+1

(37)

(38)

(39)

using a Metropolis random walk with an adaptively tuned bivariate Gaussian

proposal distribution.

45

(c) Update

µ(tm) ∼ [µ(tm)|·]

∝ (cid:2)µ(tm)|µ(tm−1), σ2

0, σ2

1, β, z(tm)(cid:3) (cid:2)s(tm)|µ(tm), σ2

s

(cid:3)1{tm∈Tobs}

(40)

(41)

using a Metropolis random walk with an adaptively tuned bivariate Gaussian

proposal distribution.

The conditional distributions for µ(tj+1) are given by

(cid:2)µ(tj+1)|µ(tj), σ2

0, σ2

1, β, z(tj+1)(cid:3) =

N(cid:0)µ(tj) − z(tj+1)∇x(cid:48) (µ(tj)) β∆tj+1, (cid:0)(1 − z(tj+1))σ2

0 + z(tj+1)σ2
1

3. For j = 1, . . . , m update

z(tj) ∼ [z(tj)|·] = Bern

(cid:33)

(cid:32)

π(1)
j
j + π(1)
π(0)

j

where

(42)
(cid:1) .

(cid:1) ∆tj+1I2

(43)

(44)

(45)

j = (1 − Φ(g(tj))) (cid:2)µ(tj+1)|µ(tj), σ2
π(1)
j = Φ(g(tj)) (cid:2)µ(tj+1)|µ(tj), σ2
π(0)

1, β, z(tj) = 0(cid:3) ,
where the recharge function is approximated as g(tj) = g0 + (cid:80)j−1
l=1 ∆tlw(cid:48)(µ(tl))θ.
Note that the full-conditional distributions for each z(tj) are conditionally inde-

0, σ2

(46)

0, σ2

1, β, z(tj) = 1(cid:3)

pendent. Therefore, these parameters need not be updated serially.

4. Update

0, σ2

1, β|·(cid:3)

0, σ2
σ2

1, β ∼ (cid:2)σ2
(cid:32) m
(cid:89)

∝

(cid:2)µ(tj)|µ(tj−1), σ2

0, σ2

(cid:33)
1, β, z(tj)(cid:3)

[β] (cid:2)σ2

0

(cid:3) (cid:2)σ2

1

(cid:3)

(47)

(48)

j=2

46

as a block using a Metropolis random walk with an adaptively tuned multivariate

Gaussian proposal distribution.

5. Update

g0, θ ∼ [g0, θ|·]

∝

m
(cid:89)

j=1

[z(tj)|g0, θ] [g0] [θ]

(49)

(50)

as a block using a Metropolis random walk with an adaptively tuned multivariate

Gaussian proposal distribution.

Appendix E: Model extension to include auxiliary

data

To incorporate auxiliary data in the hierarchical model framework, we retain the model

structure for the recharge-based movement model and assume we also have auxiliary data

represented by y(tl) at time tl for l = 1, . . . , L observations during the study period. For

example, the q × 1 vectors y(tl) could represent a set of q accelerometer measurements

recorded at time tl. Depending on the auxiliary data source and support, we formulate

the auxiliary data model generally as

y(tl) ∼ [y(tl)|g1(tl), γ] ,

(51)

for l = 1, . . . , L and where γ represents a set of auxiliary data parameters we seek to

learn about. The function g1(tl) represents the portion of the aggregated physiological

recharge function g(tl) that relates to the observed auxiliary data y(tl). Thus, the

aggregated physiological recharge function g(t) can be partitioned into two components

g(t) = g1(t) + g2(t), where g2(t) represents the remainder of physiological processes

not measured by g1(t). This recharge formulation implies that we have two aggregated

physiological recharge functions

47

g1(t) = g1,0 +

g2(t) = g2,0 +

(cid:90) t

0
(cid:90) t

0

w(cid:48)

1(µ(τ ))θ1dτ ,

w(cid:48)

2(µ(τ ))θ2dτ ,

(52)

(53)

associated with measured and unmeasured physiological space, respectively. Each ag-

gregated recharge function is comprised of its own set of parameters we may seek to

learn about. Thus, the full integrated movement model can be visualized by the di-

rected acyclic graph (DAG) shown in Figure 11. In the DAG, we indicate a possible

additional relationship between the auxiliary data (y) and movement process (µ) using

a gray arrow.

Figure 11: Directed acyclic graph (DAG) associated with the recharge-based move-

ment model based on both positional telemetry data (s) and auxiliary data (y). By

convention, solid arrows denote stochastic model dependencies and dashed arrows

represent deterministic relationships in the model. Note that the edge between y and

µ is shown in gray because it may or may not exist depending on how the model is

speciﬁed.

48

szg1g2✓1✓2 ygµ
