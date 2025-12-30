UC Santa Cruz
UC Santa Cruz Previously Published Works

Title
Building use‐inspired species distribution models: Using multiple data types to examine
and improve model performance

Permalink
<https://escholarship.org/uc/item/26z2v9fx>

Journal
Ecological Applications, 33(6)

ISSN
1051-0761

Authors
Braun, Camrin D
Arostegui, Martin C
Farchadi, Nima
et al.

Publication Date
2023-09-01

DOI
10.1002/eap.2893

Peer reviewed

eScholarship.org

Powered by the California Digital Library
University of California

Received: 1 February 2023

Accepted: 22 May 2023

DOI: 10.1002/eap.2893

A R T I C L E

Building use-inspired species distribution models: Using
multiple data types to examine and improve model
performance

Camrin D. Braun 1
Michael Alexander 3
Stephanie Brodie 6,7
Tobey H. Curtis 10
Nerea Lezama-Ochoa 6,7
Nuno Queiroz 11,12
David W. Sims 12,15
Riley Young-Morse 5

| Martin C. Arostegui 1
| Pedro Afonso 1,4
| Daniel P. Crear 8
| Elliott L. Hazen 6,7

| Nima Farchadi 2

|

| Andrew Allyn 5
| Emmett F. Culhane 1,9

| Alex Kerney 5

|

| Katherine E. Mills 5

| Dylan Pugh 5

James D. Scott 3,13
|
| Simon R. Thorrold 1
| Rebecca Lewison 2

| Gregory B. Skomal 14
| Heather Welch 6,7

|

|

|

|

| Steven J. Bograd 6

|

1Biology Department, Woods Hole Oceanographic Institution, Woods Hole, Massachusetts, USA

2Institute for Ecological Monitoring and Management, San Diego State University, San Diego, California, USA

3NOAA Earth System Research Laboratory, Boulder, Colorado, USA

4Okeanos and Institute of Marine Research, University of the Azores, Horta, Portugal

5Gulf of Maine Research Institute, Portland, Maine, USA

6Environmental Research Division, Southwest Fisheries Science Center, National Oceanic and Atmospheric Administration, Monterey, California, USA

7Institute of Marine Sciences, University of California, Santa Cruz, California, USA

8ECS Federal, in Support of National Marine Fisheries Service, Atlantic Highly Migratory Species Management Division, Silver Spring,
Maryland, USA

9Massachusetts Institute of Technology–Woods Hole Oceanographic Institution Joint Program in Oceanography-Applied Ocean Science and
Engineering, Cambridge, Massachusetts, USA

10National Marine Fisheries Service, Atlantic Highly Migratory Species Management Division, Gloucester, Massachusetts, USA
11Research Network in Biodiversity and Evolutionary Biology, Universidade do Porto, Vair˜ao, Portugal

12Marine Biological Association of the United Kingdom, The Laboratory, Plymouth, UK

13Cooperative Institute for Research in Environmental Sciences, University of Colorado Boulder, Boulder, Colorado, USA

14Massachusetts Division of Marine Fisheries, New Bedford, Massachusetts, USA

15Ocean and Earth Science, National Oceanography Centre Southampton, University of Southampton, Southampton, UK

Correspondence
Camrin D. Braun
Email: <cbraun@whoi.edu>

Funding information
National Aeronautics and Space
Administration, Grant/Award Number:
80NSSC19K0187; NASA Earth and Space
Science and Technology, Grant/Award
Number: 80NSSC22K1549

Abstract
Species distribution models (SDMs) are becoming an important tool for marine
conservation and management. Yet while there is an increasing diversity and

volume of marine biodiversity data for training SDMs, little practical guidance
is available on how to leverage distinct data types to build robust models. We

explored the effect of different data types on the fit, performance and predictive

ability of SDMs by comparing models trained with four data types for a heavily

Ecological Applications. 2023;e2893.
<https://doi.org/10.1002/eap.2893>

<https://onlinelibrary.wiley.com/r/eap>

© 2023 The Ecological Society of America.

1 of 20

2 of 20

Handling Editor: Brice X. Semmens

INTRODUCTION

BRAUN ET AL.

exploited pelagic fish, the blue shark (Prionace glauca),
in the Northwest
Atlantic: two fishery dependent (conventional mark-recapture tags, fisheries

observer records) and two fishery independent (satellite-linked electronic tags,
pop-up archival tags). We found that all four data types can result in robust

models, but differences among spatial predictions highlighted the need to con-
sider ecological realism in model selection and interpretation regardless of data

type. Differences among models were primarily attributed to biases in how each

data type, and the associated representation of absences, sampled the environ-
ment and summarized the resulting species distributions. Outputs from model

ensembles and a model trained on all pooled data both proved effective for com-
bining inferences across data types and provided more ecologically realistic pre-

dictions than individual models. Our results provide valuable guidance for

practitioners developing SDMs. With increasing access to diverse data sources,
future work should further develop truly integrative modeling approaches that

can explicitly leverage the strengths of individual data types while statistically
accounting for limitations, such as sampling biases.

K E Y W O R D S
climate change, ecological forecasting, highly migratory species, prediction, spatial ecology,
species distribution models

tool

Species distribution models (SDMs) are an increasingly
common tool used to understand species distributions
and to predict species responses to changing environ-
mental conditions (Araújo et al., 2019; Elith et al.,
2008; Guisan & Thuiller, 2005). In the marine envi-
for
ronment, SDMs have become an important
studying biophysical drivers of habitat use that can be
readily applied for conservation, spatial planning and
(Araújo et al., 2019; Crear
fisheries management
et al., 2021; Robinson et al., 2017). While SDMs for
marine species are often built using single data types
(Grüss et al., 2019), there are some fishery-dependent
and fishery-independent data sources that can be used
scale of
to expand the scope and spatiotemporal
(Erauskin-Extramiana et al., 2019;
modeling efforts
Sequeira et al., 2013). Building robust SDMs is partic-
ularly important when faced with limited data,
the
need to understand how species will respond to a
changing ocean, and to accurately assess exposure to
various
fisheries
exploitation, habitat degradation, and energy develop-
ment. Increasing human use of marine resources, cli-
mate variability and change, and limitations in data
availability and scope require exploring best practices
for leveraging multiple data types in marine conserva-
tion and management.

anthropogenic

including

stressors

In addition to the typical fisheries datasets, such as
vessel
logbooks and fishery observers, some fishery-
independent datasets have been developed that capture
marine species occurrence, primarily as a product of
targeted research or management
efforts. Fishery-
independent datasets include specific survey efforts, such
as aerial or shipboard transect or trawl surveys (Abrahms
et al., 2019; Becker et al., 2019; Di Sciara et al., 2015;
Friedland et al., 2021), as well as electronic telemetry tags
that track animal movement (e.g., Block et al., 2011;
Queiroz et al., 2019). Electronic tags, in particular, repre-
sent species’ habitat use independent of fishing effort
and are thus useful for representing the unbiased habi-
tat use and environmental niche of tracked individuals.
Despite the relatively high cost and low sample sizes,
these datasets are growing and becoming increasingly
available (Hussey et al., 2015), but guidance on best
practices for building SDMs across disparate data types
is lacking.

Here we develop a use-inspired comparison of SDMs
built with four types of fishery-dependent and fishery-
independent occurrence data using a heavily exploited
pelagic fish, the blue shark (Prionace glauca), as a model
species to inform spatial management measures in a
changing ocean. We use conventional marker tag, fishery
observer, satellite-linked electronic tag, and pop-up archi-
val tag data to fit data-specific SDMs in a comparative
framework to inform important decisions in the model

ECOLOGICAL APPLICATIONS

3 of 20

development process and identify trade-offs associated
with each data type. In addition to understanding differ-
ences among SDMs using a suite of validation and perfor-
mance metrics, we tested the impact of data pooling and
generating model ensembles for maximizing model util-
ity and prioritizing model development in real-world
applications.

METHODS

Model species

Blue sharks occupy productive nearshore habitats in the
North Atlantic Ocean during summer and fall (Carey &
Scharold, 1990) and make extensive offshore migrations
into the Gulf Stream and subtropical waters during
(Braun et al., 2019; Campana et al., 2011;
winter
Kohler & Turner, 2018; Queiroz et al., 2019; Vandeperre
et al., 2014). Blue sharks are typically caught as bycatch
in longline fisheries that target swordfish and tunas, as
well as recreational fisheries for large pelagic species
(Aires-da Silva & Gallucci, 2007; Kohler & Turner, 2018).
This species is also the target of a number of research
efforts using electronic tags to study behavior and ecology
across multiple ecosystems (e.g., Braun et al., 2019;
Vandeperre et al., 2014). The relative abundance and
widespread distribution of blue sharks results in a diverse
set of occurrence data available for species distribution
modeling (Druon et al., 2022), thus enabling the evalua-
tion of the data types and the associated model develop-
ment process.

Fisheries-dependent datasets

Marker tag

We obtained marker tag data from the International
Commission for the Conservation of Atlantic Tunas
(ICCAT) Secretariat tag database (<https://iccat.int/en>) for
blue sharks in the Atlantic Ocean from 1959 to 2019.
These marker (e.g., conventional or “spaghetti”) tags are
attached to a fish upon release and may be recorded
again if the individual is later recaptured. This dataset
consisted of 101,714 blue sharks tagged and released
across a number of commercial and recreational fisheries.
In total,
tagged individuals were
recaptured, yielding a total of 115,367 blue shark daily
presence locations. The releases were dominated by three
main gear types: 66% (n = 67,085) were from rod and reel
fisheries, 19% (18,826) from unclassified gear codes and
13% (13,022) from longline fisheries. Five gear types

(~13%)

13,653

comprised the majority of marker tag recoveries: 34%
(n = 4558) from longline, 21% (n = 2872) from rod and
reel, 21% (n = 2806) from purse seine, 13% (n = 1728)
from baitboat and 9% (n = 1197) from unclassified gear
codes. These data were filtered to remove duplicate IDs
and points on land, and only one tag event was retained
for each day within a 0.01(cid:1) grid to reduce the autocorrela-
tion structure in the data (Brodie, Litherland, et al.,
2018). The filtering steps retained 36,840 combined
releases and recoveries in the North Atlantic during the
oceanographic model time period (1993–2019) and were
biased toward the Northeast US shelf (Figure 1a) during
summer. Significant releases and recoveries occurred
across the main footprint of the longline fleet in this
region, spanning the area of impact of the Gulf Stream
along the southeast USA and east of Cape Hatteras to the
Azores and northern Europe.

Fisheries observer

The US Atlantic pelagic longline fishery primarily targets
swordfish (Xiphias gladius) and yellowfin tuna (Thunnus
albacares). An at-sea observer program has been in place
for this fishery since the early 1990s whereby indepen-
dent observers catalog gear and catch information for
every set made on ~10%–15% of longline fishing trips
(Beerkircher et al., 2002; Crear et al., 2021). These
observer data were used to represent blue shark presence
(catch) and absence through the spatial extent of the fish-
ery concentrated in the northern Gulf of Mexico, along
the East Coast of the USA and along the southern and
eastern edges of the Grand Banks (Figure 1b). In total,
22,890 pelagic longline sets conducted between 1993 and
2019 were used in the analysis. A total of 8057 and 14,833
sets
and absence,
respectively.

shark presence

recorded blue

Fisheries-independent datasets

Satellite-linked electronic tag

Satellite-linked tags (model SPOT, Wildlife Computers)
were deployed on 70 individuals across a number of
study sites in the North Atlantic, resulting in 6430 unique
(2006–2018;
individual
tracking days over 12 years
Figure 1c). Tags were attached to the dorsal fin of blue
sharks in a manner similar to Braun et al. (2019). When
at the surface, a wet-dry switch on the tag activated trans-
mission to Argos
and a Doppler-based
geoposition was calculated for the shark with associated
location error (typically <10 km, Lopez et al., 2014).

satellites

4 of 20

BRAUN ET AL.

50

40

30

20

10

50

40

30

20

10

(a) Marker tags
N = 36,840

−100

−75

−50

−25

(b) Fishery observer
N = 8057
presences

N = 14,833
absences

6000

4000

2000

s
e
c
n
e
s
e
r
p

.
o
N

800

600

400

200

s
e
c
n
e
s
b
a

.
o
N

400

300

200

100

s
e
c
n
e
s
e
r
p

.
o
N

−100

−75

−50

−100

−75

(c) Satellite tags
N = 6430 locations
from 70 individuals

−100

−75

−50

−25

(d) Pop-up tags
N = 4913 locations
from 37 individuals

50

40

30

20

10

50

40

30

20

10

150

100

50

s
e
c
n
e
s
e
r
p

.
o
N

150

100

50

s
e
c
n
e
s
e
r
p

.
o
N

−100

−75

−50

−25

Presence locations for the marker tags (a),

F I G U R E 1
fishery observer data (b), and two types of electronic tags
(c, satellite and d, pop-up). Marker tags and observer data
are fishery dependent (a, b), and electronic tags are fishery independent
(c, d). Observer data (b) also contains “true” absence locations (but see
Discussion). Note that grid cells for the fishery observer locations
that contained <3 vessels were removed to protect confidentiality.
Orange triangles in (c) and (d) indicate the locations where tags
were deployed.

Resulting locations were then filtered using a speed filter
−1) to remove unrealistic locations and regularized
(10 ms
to daily location estimates by fitting a state-space model
and predicting daily time steps (R package foieGras,
Jonsen et al., 2019, 2020).

Pop-up satellite archival transmitting tag

Pop-up satellite archival transmitting (a.k.a. “PSAT”) tags
(models PAT and miniPAT, Wildlife Computers) were
deployed on 37 individuals in many of the same study
locations, resulting in 5136 unique individual tracking
days over 8 years (2009–2017; Figure 1d). Pop-up tags
archive depth, temperature and light level data that are
then used to estimate animal movements. However, tags
that rely on light level for geolocation often exhibit large
errors in daily position estimates (Braun et al., 2015; Niel-
sen & Sibert, 2007). We combined light and sea surface
temperature measurements using a likelihood framework
in a hidden Markov Model (Wildlife Computers “GPE3”
geolocation software) which has been shown to provide
realistic movement estimates to within <1(cid:1) longitude and
~1–2(cid:1) in latitude, particularly when datasets are high
quality and target species are surface-oriented (Braun,
Galuardi, & Thorrold, 2018). Fitted models provided daily
location estimates and associated uncertainty for each
tagged individual over the tag deployment period.

Environmental data

We included 10 environmental variables as potential pre-
dictor variables in the SDMs, which consisted of two
static variables, seven dynamic surface variables and one
dynamic subsurface variable to better represent
the
three-dimensional environment of this highly migratory
species through time (Brodie, Jacox, et al., 2018). The
dynamic environmental data were sourced from the Global
Ocean Physics Reanalysis (GLORYS, Copernicus Marine
Environmental Monitoring Service; Lellouche et al., 2018).
GLORYS is a global, data-assimilating ocean model with
daily outputs at 1/12(cid:1)
resolution
representing 50 vertical levels. The data-assimilating nature
of the model allows for regular data-driven updates to
model predictions from in situ platforms and remote sens-
ing observations that ensure realistic model outputs. The
seven dynamic surface variables included: (1) sea surface
temperature (SST; in degree Celsius) and (2) its spatial
standard deviation (SST_sd; calculated over a 0.25(cid:1)
square), (3) sea surface height (SSH; in meters) and (4) its
spatial standard deviation (SSH_sd; calculated over a

(~9 km) horizontal

ECOLOGICAL APPLICATIONS

5 of 20

0.25(cid:1) square), (5) sea surface salinity (SSS; in PSU) and
(6) its spatial standard deviation (SSS_sd; calculated over
a 0.25(cid:1) square) and (7) eddy kinetic energy (EKE; in
meters per square second). The dynamic subsurface vari-
able, mixed layer depth (MLD; in meters), was output
from the model and used here as an index of the water
column structure. The two static variables included
bathymetry (ETOPO1 obtained from <https://www.ngdc>.
noaa.gov/mgg/global/global.html, coarsened to 1=12(cid:1); in
meters) and rugosity (calculated as the spatial standard
deviation of bathymetry over a 0.25(cid:1) square; in meters).
Each corresponding environmental value extracted from
the
and
times for each data type was included in the final data
frame. All environmental grids used the GLORYS native
spatial (1/12(cid:1)) and temporal (daily) resolution.

presence/absence/pseudo-absence

locations

Species distribution models

The probability of species presence was modeled for each
data type as a function of environmental variables using
a boosted regression tree (BRT) framework (dismo R
package, Elith et al., 2006). BRTs are nonparametric and
use boosting (a numerical optimization technique) to
determine optimal partitioning of variance. One of the
advantages of using BRTs is their ability to handle corre-
lation and collinearity effects of the environmental vari-
ables so a priori assessment of predictor variables is not
needed (Elith et al., 2006). BRTs were fitted using a
Bernoulli family appropriate to the binary nature of the
response variable (presence/[pseudo-]absence) and a
fixed number of 2000 trees with a learning rate of 0.005,
a bag fraction of 0.75, and tree complexity of 5. Elith
et al. (2008) have presented a thorough discussion of
hyperparameter tuning. Therefore we fixed these param-
eters here to isolate the effects of the different data types
and our focal “treatments” (see below). The resulting
models described species-specific “habitat suitability” as
continuous values ranging from 0 to 1.

Exploratory treatments: Sample size,
spatial extent, absences

In any SDM application, practitioners are faced with a
number of decisions during model development that may
impact the resulting model skill and applicability to the
desired use case. We used the different data types to test
the impact of three important aspects of our model
framework: sample size, spatial extent, and representa-
tion of absences. To explore the effects of different sample
trained with the maximum
sizes, models were

sample size available for each data type and then subse-
quently subsampled to 4000 and 1000 presences for sub-
sequent model re-fitting.

for

We also explored how different

spatial extents
affected model fit and performance. For our example use
case, we sought to build SDMs that could be predicted
under climate change scenarios
the Northwest
Atlantic Ocean. Therefore, our spatial extent of interest
was the footprint of a downscaled global climate model
that spanned from the Caribbean to the Grand Banks
(Alexander et al., 2020), approximately equivalent to the
extent of
the fishery observer data and relatively
restricted compared with the widespread coverage across
the North Atlantic as represented by the other three data
types. For spatial extent treatments, a model was trained
for each data type with all available presence observa-
tions from the full spatial extent of each data type. Each
data type was then subset to a common, limited spatial
extent in the Northwest Atlantic within the spatial extent
of the climate model as an example use case. A second
set of models for this treatment was then trained with the
presence observations for each data type from this limited
spatial extent. We subsequently compared predictions
from the full extent and limited extent models within the
spatial extent of the downscaled climate model to under-
stand the potential impacts of including training data
from outside the study area.

A fundamental challenge of many data types for habi-
tat modeling is that they are presence only, and thus can-
not provide information on animal absence. A number of
techniques have been developed to simulate data
representing where individuals were likely absent, often
termed pseudo-absences (Barbet-Massin et al., 2012).
These approaches include simple background sampling
to more complex, biased sampling such as generating
simulated animal movement trajectories using null ani-
mal movement models (Hazen et al., 2021; Pinti et al.,
2022). For all datasets, we generated pseudo-absences
using background sampling methods. Background sam-
pling was performed by randomly drawing, without
replacement, from the spatial extent of a given individual
track from an electronic tag (background track sampling)
or from the extent of the full dataset (background extent
sampling). For electronic tags only, additional pseudo-
absences were generated using correlated random walk
simulations. To simulate realistic tracks and sample
pseudo-absence locations, we conducted 10 correlated
random walk simulations per individual in each elec-
tronic tag dataset following Hazen et al. (2021). The fish-
ery observer dataset does include observed fishing effort
when blue sharks were not detected, but many of the
fishing sets that recorded “absences” occurred in areas
that were likely to be suitable blue shark habitats despite

6 of 20

BRAUN ET AL.

no blue sharks being captured, presumably due to imper-
fect sampling as a function of gear-specific catchability.
Thus, we also simulated pseudo-absences using the back-
ground method for the model fitted with fishery observer
data to compare these with the “true” absences observed
in these data. In all cases, dates were assigned to pseudo-
absence locations by randomly drawing from the possible
dates in the corresponding presence dataset. Simulated
pseudo-absences were compared against all available
presence data from all data types to avoid generating
pseudo-absences for which a corresponding presence
occurred in that month (regardless of the year) and
0.1(cid:1) grid cell (~10 km). The resulting pseudo-absence
locations were randomly subsampled to generate a
1:1 presence/pseudo-absence dataset for each model
training application.

Finally, we also explored two methods for combining
data in SDMs. Pooling of data is common in species distribu-
tion modeling (Fletcher et al., 2019), especially when using
opportunistic, presence-only data collated from multiple
sources (Domisch et al., 2016). We created a pooled, all-data
model that was trained with all presences and associated
pseudo-absences (from background sampling) combined
across data types. Ensemble modeling techniques have been
also regularly applied to combine predictions across data
types or model frameworks (Araújo & New, 2007). Thus, we
also created an equal-weight, mean model ensemble that
averaged across the predictions from each of the four data-
specific models; in this case, each of the data-specific models
relied on background pseudo-absence generation.

Comparing model performance

We evaluated model performance across three dimen-
sions: explanatory power, predictive skill and ecological
realism. Explanatory power indicates a model’s ability to
explain the variability in a given dataset and was evalu-
ated using the percent explained deviance (R 2). Predictive
skill indicates how well a model prediction can discern
different actual outcomes (Norberg et al., 2019) and was
evaluated with Area Under the Receiver Operating Char-
acteristic Curve (AUC). These metrics were calculated
using 10-fold cross-validation (Abrahms et al., 2019).
We also calculated the sensitivity and specificity of each
model (caret package for R, Kuhn, 2015) that represent
the proportion of true presences and true absences,
respectively, correctly predicted by the model. Daily
model predictions were generated for the full spatial
extent of the data and predictions were classified as pre-
sent when predicted suitability was greater than the 75%
quantile of a given prediction surface and considered
25% quantile. We
than the
absent when less

quantitatively assessed ecological
realism for each
model against its training data (i.e., in-sample) using
median predicted habitat suitability at presences and
pseudo-absences and qualitatively assessed realism
using the expert opinion of an example daily prediction
for each model. The same quantitative approach was
used for assessing each model’s predictive capacity (and
thus ecological realism) against independent presence
data (i.e., all true presences) from the three other data
types (e.g., fisheries observer SDM used to predict pres-
ences from the three tagging datasets; repeated for all
SDMs). Finally, we used pairwise correlation to quantify
spatial variability among model predictions. We calcu-
lated Pearson’s correlation coefficient in each grid cell
by comparing monthly predictions (1993–2019; n = 324)
for each pair of data-specific models. For example, all
monthly predictions from the marker tag model in a
given grid cell were compared against all monthly pre-
dictions from the satellite tag model in the same grid
cell by calculating the correlation between model
predictions.

RESULTS

After quality control and temporal filtering (1993–2019)
to match available environmental data, we selected
56,240 presence observations for blue sharks in the North
Atlantic from the four data types (Figure 1). Our treat-
ments identified a spectrum of model sensitivity to the dif-
ferent manipulations. The impact of successive reductions
in sample sizes available for model training was minor
based on metrics representing explanatory power, predic-
tive skill and ecological realism (Table 1) and almost
indiscernible among most example predictions (Figure 2).
In spatial extent manipulations, metrics for explanatory
power, predictive skill, and ecological realism were rela-
tively invariant for the three datasets that spanned the
North Atlantic (marker, satellite and pop-up tags) and, in
some cases, suggested minor improvements in model per-
formance when the spatial extent of the training data was
limited to the Northwest Atlantic (Table 2, Figure 3). In
contrast, the performance of
fishery observer models
decreased across all metrics when comparing the full with
the limited spatial extent of training data.

Among the three treatments (sample size, spatial
extent, representation of absences), manipulations in
how absences were represented demonstrated the most
significant impact on data-specific model performance.
For both types of electronic tag data, pseudo-absences
were either drawn from correlated random walk (CRW)
simulations, randomly sampled from the extent of individ-
ual tracks (track extent) or randomly sampled from the

ECOLOGICAL APPLICATIONS

7 of 20

T A B L E 1

Summary of model statistics for sample size manipulations.

Explanatory
power
R 2

Predictive
skill
AUC

Median in-sample
prediction at
presences

Median in-sample
prediction at
pseudo-absences

Median prediction
at all true
presences

Figure
panel

Ecological realism

0.71

0.73

0.79

0.58

0.59

0.66

0.27

0.29

0.41

0.50

0.49

0.58

0.97

0.97

0.96

0.94

0.94

0.93

0.81

0.81

0.80

0.93

0.92

0.92

0.98

0.98

0.97

0.91

0.90

0.90

0.64

0.64

0.67

0.79

0.78

0.80

0.06

0.06

0.06

0.08

0.08

0.10

0.36

0.36

0.32

0.18

0.19

0.18

0.93

0.93

0.93

0.79

0.77

0.85

0.73

0.72

0.70

0.52

0.58

0.70

2a

2b

2c

2j

2k

2l

2d

2e

2f

2g

2h

2i

Data type

N

Marker

36,840

Observer

Satellite

Pop-up

4000

1000

8057

4000

1000

6430

4000

1000

4913

4000

1000

Note: For each data type, a “full” model was built with all available presence observations (first row of each data type) then randomly subsampled to smaller
sample sizes. For all metrics except prediction at pseudo-absences, higher values indicate better model performance.

extent of
individuals
the full dataset pooled across
(background extent). In both cases, sampling pseudo-
absences from the background extent resulted in the best
performing model across all metrics compared with the
track extent and CRW (Table 3). Among the two poorer
performing pseudo-absence methods for electronic tag
data (i.e., track extent and CRW), track extent pseudo-
absence sampling consistently resulted in better predictive
performance against all presence data across the four data
indicated slightly
types, but within-sample metrics
improved model performance using CRW-generated
pseudo-absences (Table 3). The example predictions for
the two electronic tag data types suggested that the three
pseudo-absence techniques resulted in significantly differ-
ent predicted habitat suitability, with background extent
sampling likely to result in the most realistic predictions
(Figure 4). The background sampling of pseudo-absences
also resulted in the most ecologically realistic predictions
compared with models fit with “true” absence data in the
observer dataset, despite the model performance metrics
being largely invariant across absence- and pseudo-
absence-based models for the observer data. For example,
“true” absence models for the fishery observer dataset
predicted high habitat suitability in the subpolar North
Atlantic and subtropical gyre for the example prediction
day which contrasted with the almost complete absence of
suitable habitat in these areas as predicted by the pseudo-
absence-based model (Figure 4). The observed divergence
across model predictions and, in some cases, between
model validation metrics and ecological realism of model

predictions (e.g., observer absence and pseudo-absence
models, Table 3 and Figure 4) highlighted the utility of
having experts assess the realism of model predictions in
addition to commonly used model validation metrics.

The model performance also varied across data-
specific models, with the marker tag model exhibiting the
highest explanatory power and best predictive skill met-
rics (Table 4). Both fishery-dependent models indicated
high-performance metrics relative to fishery-independent
models and resulted in spatially constrained suitability in
example predictions (Figure 5, Table 4). In contrast,
fishery-independent models predicted more widespread
suitable habitat during the example July prediction; how-
ever, both satellite tag and pop-up tag-based models dem-
onstrated better sensitivity when predicting independent,
out-of-sample presence data (Figure 6). The marker tag
model exhibited particularly high sensitivity in predicting
both types of fishery-dependent presence observations,
while the observer model indicated the lowest sensitivity
of any model-data combination when predicting the
marker tag dataset. In contrast, the models trained with
fishery-dependent data had a higher specificity when
predicting true absences in the observer data.

Pairwise linear correlations among each model’s pre-
diction highlighted where each pair of data-specific models
tended to agree and disagree (Figure 7). In general, there
was large-scale agreement among models throughout the
Slope Sea and along the US East Coast and Gulf of
Mexico. The most disagreement across models is apparent
in the subpolar North Atlantic (Figure 7a–c) and in

8 of 20

r
e
k
r
a
M

40° N

20° N

r
e
v
r
e
s
b
O

e
t
i
l
l
e
t
a
S

40° N

20° N

40° N

20° N

p
u
-

p
o
P

40° N

20° N

(a)

(d)

(g)

(j)

Full sample size

N = 4000

N = 1000

BRAUN ET AL.

(b)

(e)

(h)

(k)

N = 36,480

N = 8057

N = 6430

N = 4913

(c)

(f)

(i)

(l)

100° W

60° W

20° W

100° W

60° W

20° W

100° W

60° W

20° W

F I G U R E 2
models trained with each data type. Yellow indicates highly suitable habitat and blue indicates low suitability.

(a–l) Predicted habitat suitability for an example day (1 July 2019) showing the impact of sample size manipulations for

0

0.5
Habitat suitability

1

subtropical waters east of the Mid-Atlantic Ridge. Overall,
the model fitted to all available presence data and the
model ensemble (mean of each data-specific model predic-
tion) provided similar example predictions (Figure 5) and
sensitivity when predicting all available presence observa-
tions (Figure 6). However, the data-pooled model and
ensemble differed significantly in their in-sample predic-
tive performance (Table 4), likely to have been a product
of the ensemble predictions representing the mean suit-
ability prediction across four data-specific models that
were at times strongly divergent (Figure 7).

DISC USS I ON

Species distribution models are an important tool for
understanding how species relate and respond to chang-
ing ocean conditions. Using data from a wide-ranging

for

source

of marine

marine species, we found that inherent biases associated
with both fishery-dependent and fishery-independent
datasets, including spatial and temporal biases that arise
from disproportionate sampling (e.g., fishing or tagging
effort), must be considered when building models.
Fishery-dependent datasets can be an effective and large-
scale
species
observations
(e.g., Arostegui et al., 2022; Brodie, Litherland, et al.,
2018). Despite the broad spatial extent and temporal cov-
erage, models trained on these data are often influenced
by the nonrandom spatial and temporal distribution of
fishing effort (e.g., Kroodsma et al., 2018). While both the
marker tag and observer-based models were character-
ized by the highest model evaluation metrics, their per-
formance when predicting
fishery-independent
datasets was generally poor, presumably as a result of
heavily biased sampling relative to environmental gradi-
that
ents (Baker et al., 2022). These results suggest

the

ECOLOGICAL APPLICATIONS

9 of 20

T A B L E 2

Summary of model statistics for spatial extent manipulations.

Ecological realism

Data
type

Spatial
extent
of data

Explanatory
power
R 2

Predictive
skill
AUC

Median in-sample
prediction at
presences

Median in-sample
prediction at
pseudo-absences

Median prediction
at all true
presences

Figure
panel

N

Marker

Full

36,840

Limited

Observer Full

Limited

Satellite

Full

Limited

Pop-up

Full

Limited

8950

8057

2572

6430

2043

4913

1593

0.71

0.79

0.58

0.39

0.27

0.46

0.50

0.57

0.97

0.98

0.94

0.85

0.81

0.88

0.93

0.92

0.98

0.97

0.91

0.76

0.64

0.75

0.79

0.82

0.06

0.02

0.08

0.23

0.36

0.22

0.18

0.13

0.98

0.96

0.81

0.59

0.77

0.75

0.52

0.39

3a

3b

3c

3d

3e

3f

3g

3h

Note: For each data type, a model was built with all available presence observations from the full spatial extent of each data type (first row of each data type
and see Figure 1). Each data type was subset to a common, limited spatial extent in the Northwest Atlantic as an example study region of interest (second row
for each data type), in this case representing the spatial extent of a downscaled global climate model. For all metrics except prediction at pseudo-absences,
higher values indicate better model performance.

fishery-based models can reliably predict where blue
sharks interact with specific fisheries (Crear et al., 2021;
Stock et al., 2020). In contrast, the fishery-independent
models exhibited generally lower evaluation metrics but
were more broadly robust in their predictive performance
and ecological realism, suggesting they may more accu-
rately represent the realized environmental niche and
geographic distribution of blue sharks beyond the foot-
print of the fishery. This distinction regarding the relative
strengths of different data types may have even greater
relevance for model projections to understand how spe-
cies’ distributions and their interactions with fisheries
may shift under climate change (Karp et al., 2023).

In contrast with fisheries-dependent data, fisheries-
independent electronic tags are critical for species that are
rarely captured in fisheries or surveys and are otherwise
data limited with respect to their distribution. Archival,
pop-up tags rely on ad hoc methods to estimate the most
probable movements of tagged animals (accuracy ≥1(cid:1),
Braun et al., 2015; Braun, Skomal, & Thorrold, 2018;
Musyl et al., 2011; Nielsen & Sibert, 2007; Wilson et al.,
2007), whereas satellite-linked tags rely on communica-
tions to satellites at the surface, resulting in higher loca-
tion accuracy (±5 km, Jonsen et al., 2020). This difference
in accuracy between tag types suggests satellite-linked tags
may provide superior occurrence data for SDMs; however,
we found that the more error-prone observations from
pop-up tags improved model performance. For both types
of fishery-independent data, the environment was sampled
for each presence location as the mean over the area
encompassed by the estimated daily location ± the 95% CI

around that location. This approach explicitly accounts for
location uncertainty and results in some averaging of envi-
ronmental metrics over a broader area for the pop-up tags
(due to higher uncertainty) compared with the specific
environment sampled for the more accurate satellite tags.
The improved model performance in our results is likely,
in part, to be a product of smoothing the local environ-
ment to be more representative of regional scale environ-
mental variability, which has been shown to contribute
disproportionately to SDM-predictive performance (Brodie
et al., 2021). The potential for environmentally driven
changes to drive the likelihood of surfacing behavior
(e.g., Sepulveda et al., 2018), which is requisite for
satellite-linked tag transmission, is likely to be another
contributing factor to this data type exhibiting reduced
model performance relative to pop-up tags. Models trained
on satellite-linked tag data are biased to predict where the
focal species engages in surfacing behavior (Pinti et al.,
2022), akin to how fishery-based models are biased to pre-
dict where the focal species interacts with a fishery.
Together, these results highlight important considerations
for building SDMs with electronic tag data and suggest
that relatively error-prone locations from archival tags
may be suitable, or even superior in some applications, for
model development.

Treatments: Sample size

With nearly an order of magnitude range in sample
size across data types, we explored the impact of sample

10 of 20

BRAUN ET AL.

Full extent

Limit extent

(a)

(b)

r
e
k
r
a
M

r
e
v
r
e
s
b
O

e
t
i
l
l
e
t
a
S

p
u
-

p
o
P

40° N

30° N

20° N

40° N

30° N

20° N

40° N

30° N

20° N

40° N

30° N

20° N

(c)

(e)

(g)

N = 36,840

N = 8950

(d)

N = 8057

N = 1593

(f)

N = 6430

N = 2572

(h)

N = 4913

N = 2043

0

0.5
Habitat suitability

1

(a–h) Predicted habitat suitability for an example day (1 July 2019) showing the impact of spatial extent manipulations for

F I G U R E 3
each data type. The first column shows example predictions for data-specific models trained with the full spatial extent of each data type (see
Figure 1) and predicted to the extent of the downscaled climate model. The second column shows example predictions for models trained
with occurrence data only from within the spatial extent shown.

ECOLOGICAL APPLICATIONS

11 of 20

T A B L E 3

Summary of model statistics for “true” absence and pseudo-absence manipulations.

Ecological realism

Data
type

(Pseudo)
absence
method

Explanatory
power
R 2

Predictive
skill
AUC

Median in-sample
prediction at
presences

Median in-sample
prediction at
pseudo-absences

Median prediction
at all true
presences

Figure
panel

Observer True (all)

True (1:1)

Background extent

Satellite

CRW

Track extent

Background extent

Pop-up

CRW

Track extent

Background extent

0.57

0.58

0.62

0.15

0.13

0.24

0.17

0.14

0.49

0.94

0.94

0.95

0.73

0.70

0.81

0.74

0.70

0.92

0.85

0.91

0.93

0.57

0.53

0.64

0.58

0.54

0.79

0.05

0.08

0.09

0.46

0.45

0.35

0.45

0.47

0.18

0.70

0.79

0.12

0.61

0.71

0.73

0.53

0.65

0.66

4a

4b

4c

4d

4e

4f

4g

4h

4i

Note: Models based on observer data were fitted with all absences (n = 14,833; ~1:2 presence to absence ratio), subsampled true absences (to represent 1:1
presence to absence ratio) and pseudo-absences randomly sampled from the background extent of the dataset. The two types of electronic tag datasets (satellite
and pop-up) were each treated with three different pseudo-absence generation techniques: correlated random walk, sampling from the extent of individual
tracks and background sampling from the full spatial extent (see Methods). For all metrics except prediction at pseudo-absences, higher values indicate better
model performance.

True absences (all)

True absences (1:1)

Background pseudo-absences

(b)

(c)

(a)

r
e
v
r
e
s
b
O

40° N

20° N

100° W

60° W

20° W

100° W

60° W

20° W

100° W

60° W

20° W

CRW

Track extent

Background extent

(d)

(g)

e
t
i
l
l
e
t
a
S

40° N

20° N

p
u
-

p
o
P

40° N

20° N

(e)

(h)

(f)

(i)

100° W

60° W

20° W

100° W

60° W

20° W

100° W

60° W

20° W

0

0.5
Habitat suitability

1

Predicted habitat suitability for an example day (1 July 2019) showing the impact of absence and pseudo-absence

F I G U R E 4
manipulations for each data type. The observer data contain “true” absence locations that were all used for the first treatment (a; ~1:2
presence to absence ratio) and were subsampled to a 1:1 ratio for the second treatment (b). The third treatment (c) used pseudo-absences
sampled from the background extent of the observer data. The electronic tag datasets (satellite and pop-up) are presence only and thus
require pseudo-absence generation. Three methods were tested: correlated random walk (d, g), sampling from the extent of individual tracks
(e, h) and sampling from the background extent of the dataset (f, i).

12 of 20

T A B L E 4
ensemble.

Summary of model evaluation statistics for selected, final models for each data type and the all-data model and model

BRAUN ET AL.

Data type

Pseudo-absence
type

N

Marker tags

Background extent

36,840

Fishery

Background extent

8057

observer

Satellite tags

Background extent

Pop-up tags

Background extent

6430

4913

All data

Background extent

56,463

Ensemble

Background extent

56,463

NA

Ecological realism

Explanatory
power
R 2

Predictive
skill
AUC

Median
in-sample
prediction at
presences

Median
in-sample
prediction at
pseudo-absences

Median
prediction
at all true
presences

Figure
panel

0.71

0.62

0.27

0.50

0.52

0.97

0.95

0.81

0.93

0.93

0.92

0.98

0.93

0.64

0.79

0.93*

0.67*

0.06

0.09

0.36

0.18

0.14

0.20

0.93

0.12

0.73

0.68

0.93*

0.67*

5a

5b

5c

5d

5e

5f

Note: * indicates values report the same metric. For all metrics except prediction at pseudo-absences, higher values indicate better model performance.

size on model validation metrics and ecological realism.
Several efforts have demonstrated varying performances
of different modeling approaches at very small sample
sizes (<100; e.g., Hernandez et al., 2006; Wisz et al.,
2008). However, such small sample sizes are becoming
increasingly rare, particularly for marine species for
which practitioners can leverage fishery interaction data
and/or widespread tagging efforts (Hussey et al., 2015)
that rapidly yield datasets in the hundreds to thousands.
We demonstrate that the modeling framework used here
was largely insensitive to changes in the sample size in
the thousands, even compared with full sample sizes with
>36,000 occurrences. These results suggest that with the
proper approach to model development, sample size
should not inhibit habitat suitability models for most
marine species, including rare or infrequently observed
taxa (e.g., Lezama-Ochoa et al., 2020).

inhibit

when multiple, complementary, large-scale datasets exist,
as is common for highly migratory marine species. Our
results also corroborate previous findings that spatial
mismatch between training data and the desired model-
ing application may not
the development of
robust SDMs. For example, Abrahms et al. (2019) used
electronic
throughout
tag data from blue whales
>1,000,000 km2 of the California Current to build SDMs
that informed high collision risk areas and time periods
in the ~6000 km2 Santa Barbara Channel located therein.
While the authors did not explicitly test the impact of the
different spatial extent between the blue whale occur-
rence data and desired modeling outcome, their model
predictions were proved to be consistent with indepen-
dent sightings data and generally aligned with our results
that different spatial extent can be less important than
other factors in training robust SDMs.

Treatments: Spatial extent

Treatments: Absences

Information on species’ occurrence over large scales is a
fundamental need for basic and applied ecology studies.
However, it is often time-consuming and expensive to
develop survey-quality,
large-scale species distribution
datasets. Thus, practitioners often leverage opportunistic
datasets that are available on smaller scales than the
desired modeling application, when used with appropri-
ate caution, to develop SDMs that can predict outside the
original spatial extent (e.g., Stirling et al., 2016). While
some work has shown that “scaling up” relatively
small-scale, scientific survey data with opportunistic
citizen science data can result in improved accuracy and
spatial extent of SDMs (Robinson et al., 2020), our results
suggest that survey-quality data may not be necessary

The representation of absences proved the most impor-
tant manipulation we tested during model development.
Previous studies have indicated how critical pseudo-
absence generation can be for modeling with presence-
only data (Barbet-Massin et al., 2012; Hazen et al., 2021;
Pinti et al., 2022). Indeed, our findings align with sugges-
tions by Hazen et al. (2021) that using background sam-
pling to generate pseudo-absences results in the best
model validation metrics and predictive skill. However,
they also highlight that, at least for their study species
(blue whale), the expert opinion was that resulting model
predictions were not biologically realistic compared with
methods that leveraged important characteristics of ani-
mal movement (e.g., autocorrelated step length and turn

ECOLOGICAL APPLICATIONS

13 of 20

(a) Marker tags

(b) Fishery observer

40° N

20° N

40° N

20° N

40° N

20° N

(c) Satellite tags

(d) Pop-up tags

(e) All data

(f) Ensemble

100° W

60° W

20° W

100° W

60° W

20° W

0

0.5
Habitat suitability

1

Predicted habitat suitability for an example day (1 July 2019) using models fitted with each data type, the all-data model

F I G U R E 5
(e) and the ensemble of (a–d, f). Yellow indicates highly suitable habitat and blue indicates low suitability. The black grid cells indicate
where presence data are available during any July in each dataset.

angles) such as the CRW methods. In contrast, our blue
shark models
indicated that background sampling
resulted in the best model metrics and most realistic
models for this generalist species, highlighting the poten-
tial role of niche separation in the presence versus
pseudo-absence training data (O’Toole et al., 2021) and
suggesting that species-specific habitat specificity may be
an important topic for future study.

The improved performance of fishery observer models
trained with background pseudo-absences rather than
“true” absences highlighted the need to account for the
focal species when predicting
variable catchability of

their occurrence. Catchability is the efficiency of fishing
gear in sampling a species’ abundance and can change as
a result of varying environmental conditions and fishing
operational characteristics. Failing to account for catchability
can obscure patterns in occurrence (Maunder & Punt, 2004).
Most notably, the degree of vertical overlap between fishing
gear and a species’ habitat use modulates catchability.
The diel change in depth distribution of many highly
migratory marine species alters their susceptibility to
being captured at a given depth (Ward & Myers, 2005), as
does environmental variation in the water column that
restricts species to near-surface waters or facilitates their

14 of 20

(a) Sensitivity

predicting to

all presence
data

marker
tag data

fishery
observer
data

satellite
tag data

pop-up
tag data

0.94

0.98

0.91

0.71

0.75

0.55

0.39

0.98

0.69

0.67

BRAUN ET AL.

(b) Specificity

predicting to

fishery
observer
true absences

marker
tag model

0.79

fishery
observer
model

0.79

0.89

0.92

0.85

0.88

0.85

satellite
tag model

0.59

0.88

0.90

0.86

0.81

0.90

pop-up
tag model

0.64

0.95

0.98

0.95

0.77

0.82

model fit to
all data

0.77

0.95

0.97
0.97

0.95

0.82

0.86

model
ensemble

0.75

marker
tag model

fishery
observer
model

satellite
tag model

pop-up
tag model

model fit to
all data

model
ensemble

0

0.25

0.50

0.75

1

Proportion correct

Proportion of presences (sensitivity, a) and “true” absences from the observer data (specificity, b) correctly predicted by

F I G U R E 6
each selected model (Table 4) and dataset combination. Model predictions were considered “correct” when predicted suitability was greater
than the 75% quantile for presence observations and less than the 25% quantile for absences in the observer data. Model ensemble includes
the selected model for each data type (Table 4), excluding the all-data model (i.e., rows 1–4).

increased occupation of deeper waters (e.g., Arostegui
et al., 2022; Prince & Goodyear, 2006). Similarly, modifi-
cations in fishery operations (e.g., changed hook and/or
bait type) may also alter catchability (e.g., sea turtles and
common mola—Arostegui et al., 2020; Gilman et al.,
2006) and can impact sympatric species in different ways
(e.g., bigeye tuna versus porbeagle shark—Foster et al.,
2012). Presence/absence data from fishery catches is,
thus, more appropriately considered as detection/
nondetection data due to the imperfect nature of such
sampling (sensu MacKenzie et al., 2002). Models trained
on fishery observer (or other catch) data must standard-
ize for catchability when incorporating “true” absences
in their place. When
or using pseudo-absences

catchability bias is unknown, or variables contributing to
catchability are unavailable, a background pseudo-
absence approach (with filtering of pseudo-absences that
conflict with known presences, as used here) may yield
more realistic predictions.

Leveraging diverse data types

fishery-
While previous studies have suggested that
dependent and fishery-independent datasets can lead to
consistent estimates of species’ habitats (Karp et al., 2023;
Pennino et al., 2016), our results suggested that models
trained with heavily biased data may significantly diverge

ECOLOGICAL APPLICATIONS

15 of 20

(a) Marker : Satellite

(b) Marker : Pop-up

50° N

40° N

30° N

20° N

10° N

50° N

40° N

30° N

20° N

10° N

50° N

40° N

30° N

20° N

10° N

(c) Marker : Observer

(d) Satellite : Pop-up

(e) Satellite : Observer

(f) Pop-up : Observer

100° W

80° W

60° W

40° W

20° W

0°

100° W

80° W

60° W

40° W

20° W

0°

−1

−0.5

0
Correlation

.5

1

(a–f) Pairwise linear correlation of monthly predictions during the GLORYS period (1993–2019) for each data-specific

F I G U R E 7
model. High positive correlation (red) indicates similarity in model predictions. High negative correlation (blue) indicates model predictions
are in opposition.

the

such as

those collected
from less biased datasets,
with fishery-independent methods. Thus, we sought to
leverage the diversity among data types to explore how to
reconcile
among models.
apparent differences
Combining multiple data sources is becoming increasingly
common for model species distributions (Fletcher et al.,
2019), often to supplement limited data (Fletcher et al.,
2016) or to alleviate limitations of particular data types
(Dorazio, 2014). While our pooled, all-data model

demonstrated marginal performance from the perspective
of traditional evaluation of model skill and ecological real-
ism, the predictive performance to both fishery-dependent
and independent datasets was reasonable given the dispro-
portionate sample sizes among data types. Data pooling is
the most common method of combining datasets (Fletcher
et al., 2019), probably due to its simplicity, but it does not
account for the different assumptions and biases inherent
in each data type. Several studies have indicated empirical

16 of 20

BRAUN ET AL.

support for fitting independent models for distinct data
types that are then combined through ensemble tech-
niques (Araújo & New, 2007). Our approach to ensemble
models assumed that the resulting model would better
represent the spectrum of blue shark ecology from the
fishery-independent datasets, while still leveraging the sig-
nificantly larger sample size from the fishery-dependent
data. Indeed, our results suggested that even simple model
ensembles may be an acceptable way to combine data for
modeling species distribution, as has been shown for other
marine taxa (e.g., blue whale; Abrahms et al., 2019).
Together, our results suggested that ensembles of indepen-
dent models may be an appropriate compromise between:
(1) data-rich fishery datasets that reliably predict a species
fishery interaction probability but are not representative of
the full extent of a species’ distribution or habitat suitabil-
ity; and (2) more ecologically realistic predictions from
fishery-independent models that tend to be more limited
in spatial and temporal coverage.

relationships

species–environment

Despite the relative success of model ensembles and
data pooling shown here, some issues are apparent in this
approach, including the inability to explicitly account for
uncertainty across datasets, leverage species–environment
relationships across models, or incorporate spatial depen-
dencies. Recent advances have suggested that model-based
data integration may be the most appropriate way to com-
bine data (Fletcher et al., 2019) in order to retain the
strengths of each dataset, while explicitly accounting for
data-specific biases (Isaac et al., 2020). Given the flexibility
in these approaches, there are several opportunities for
explicitly linking inference across datasets such that, for
example,
can be
derived using joint likelihood across diverse data types
(Ahmad Suhaimi et al., 2021). Similarly, most SDMs—
including those in this study—are spatially implicit (and
simple), in that they do not formally incorporate spatial
dependencies in the data; although more complex in struc-
ture, spatially explicit SDMs achieve greater predictive per-
formance and are better suited to addressing management
and conservation issues given their enhanced ability to
local conditions (DeAngelis & Yurek, 2017;
represent
Domisch et al., 2019; Williamson et al., 2022). In applied
science (such as spatial planning of marine protected
areas), the ability to provide the most accurate species’
occurrence predictions and their associated uncertainty
(especially at local jurisdictional scales) is paramount; such
information ultimately is used by managers in how they
decide to balance the biological, economic, and social out-
comes of fisheries that have a real-world impact on fish
and fishers (Anderson et al., 2019; Arostegui et al., 2021).
As integrated and spatially explicit SDMs continue to
gain traction in basic ecology and applied management
(Zulian et al., 2021), practical guidance and best

practices will make these approaches increasingly accessi-
ble to practitioners.

Conclusion

As SDMs become foundational in ecology, questions of
how to use the ever-increasing volume of diverse data
sets remain. While significant changes in sample size and
spatial extent had relatively minor impacts on resulting
models, our results demonstrated that how absences are
represented in presence–absence models is a critical con-
sideration in model development that can lead to varying
model outcomes. Data-specific biases are inherent and, in
our results, were clearly manifested in model predictions;
these are integral considerations for modeling applica-
tions, particularly for models built with single data types.
If multiple data types are available, our results suggested,
at minimum, that a comparison across models may illu-
minate important similarities and/or differences that can
inform model utility for the desired application. We pre-
sent an ensemble approach that leverages the desired
strengths of the individual datasets while minimizing the
inherent biases of each data type and provides the appro-
priate balance of predictive performance and ecological
realism. In our use case, the divergence of the fishery
observer model from the models trained with other data
types, the variability among traditional model evaluation
fishery-
metrics, and the predictive performance of
independent models together suggest that an integrated
approach to model development is needed to generate
robust SDMs from diverse data types. While statistically
reconciling, and even leveraging, diverse data types
remains challenging for most practitioners, especially in
a spatially explicit model framework, increasing access to
diverse data sources suggests that explicit data integration
is an important area for future work (Isaac et al., 2020)
and will be instrumental in expanding and improving
efforts to better understand the impacts of climate change
on marine species.

A C K N OW L E D G M E N T S
We thank all those who supported tagging efforts, the
collection of observer program data, and those who con-
tributed to the ICCAT marker tag program, including the
NOAA Northeast Fisheries Science Center’s Cooperative
Shark Tagging Program. We thank the US Atlantic pelagic
longline fishery observers and data providers from the
including
NOAA Southeast Fisheries Science Center
L. Beerkircher and S. Cushner. We are grateful to the
numerous captains and crews who provided their expertise
and ship time and thank J. Suca for helpful comments on
an earlier version of this manuscript. This work was

ECOLOGICAL APPLICATIONS

17 of 20

(80NSSC19K0187) and NOAA’s

supported by a NASA Ecological Forecasting funded
project
Integrated
Ecosystem Assessment program. Martin C. Arostegui
was supported by the Postdoctoral Scholar Program
at Woods Hole Oceanographic
Institution with
funding provided by the Dr. George D. Grice Postdoc-
toral Scholarship Fund. Emmett F. Culhane was
supported by a Future Investigators in NASA Earth
and Space Science and Technology (FINESST) award
(80NSSC22K1549).

C O N F L I C T O F I N T E R E S T S T A T E M E N T
The authors declare no conflicts of interest.

D A T A A V A I L A B I L I T Y S T A T E M E N T
Code (Braun et al., 2023b) is available in Zenodo: https://
doi.org/10.5281/zenodo.7971532. The raw model training
datasets for the marker, pop-up, and satellite tag datasets
(Braun et al., 2023a) are available in Dryad: <https://doi>.
org/10.5061/dryad.h44j0zpr2. The marker tag data used
in this research are also publicly available from the Inter-
national Commission for the Conservation of Atlantic
Tunas (ICCAT) Secretariat tag database at <https://iccat>.
int/en/accesingdb.html, under “BSH” in the “Tagging”
section. The raw model training data for the fishery-
dependent observer dataset used in this study are consid-
ered confidential under the U.S. Magnuson-Stevens Act:
qualified researchers may request these data from the
NOAA Pelagic Observer Program office by contacting
<popobserver@noaa.gov>; we requested data representing
all pelagic longline sets between the years 1993 and 2019.

O R C I D
Elliott L. Hazen
Nerea Lezama-Ochoa
3106-1669
Heather Welch

<https://orcid.org/0000-0002-0412-7178>
<https://orcid.org/0000-0003->

<https://orcid.org/0000-0002-5464-1140>

R EF E RE N C E S
Abrahms, B., H. Welch, S. Brodie, M. G. Jacox, E. A. Becker, S. J.
Bograd, L. M. Irvine, D. M. Palacios, B. R. Mate, and E. L.
Hazen. 2019. “Dynamic Ensemble Models to Predict Distribu-
tions and Anthropogenic Risk Exposure for Highly Mobile
Species.” Diversity and Distributions 25(8): 1182–93.

Ahmad Suhaimi, S. S., G. S. Blair, and S. G. Jarvis. 2021. “Integrated
Species Distribution Models: A Comparison of Approaches
under Different Data Quality Scenarios.” Diversity and Distri-
butions 27(6): 1066–75.

Aires-da Silva, A. M., and V. F. Gallucci. 2007. “Demographic and
Risk Analyses Applied to Management and Conservation of
the Blue Shark (Prionace glauca) in the North Atlantic Ocean.”
Marine and Freshwater Research 58(6): 570–80.

Alexander, M. A., S. I. Shin, J. D. Scott, E. Curchitser, and C. Stock.
2020. “The Response of the Northwest Atlantic Ocean to
Climate Change.” Journal of Climate 33(2): 405–28.

Anderson, C. M., M. J. Krigbaum, M. C. Arostegui, M. L. Feddern,
J. Z. Koehn, P. T. Kuriyama, C. Morrisett, et al. 2019. “How
Commercial Fishing Effort Is Managed.” Fish and Fisheries
20(2): 268–85.

Araújo, M. B., R. P. Anderson, A. M(cid:2)arcia Barbosa, C. M. Beale,
C. F. Dormann, R. Early, R. A. Garcia, et al. 2019. “Standards
for Distribution Models in Biodiversity Assessments.” Science
Advances 5(1): eaat4858.

Araújo, M. B., and M. New. 2007. “Ensemble Forecasting of Species
Distributions.” Trends in Ecology & Evolution 22(1): 42–7.
Arostegui, M., C. Braun, P. Woodworth-Jefcoats, D. Kobayashi, and
P. Gaube. 2020. “Spatiotemporal Segregation of Ocean Sunfish
Species (Molidae) in the Eastern North Pacific.” Marine Ecol-
ogy Progress Series 654: 109–25.

Arostegui, M. C., C. M. Anderson, R. F. Benedict, C. Dailey, E. A.
Fiorenza, and A. R. Jahn. 2021. “Approaches to Regulating
Recreational Fisheries:(cid:3)abalancing Biology with Angler Satis-
faction.” Reviews in Fish Biology and Fisheries 31(3): 573–98.
Arostegui, M. C., P. Gaube, P. A. Woodworth-Jefcoats, D. R.
Kobayashi, and C. D. Braun. 2022. “Anticyclonic Eddies
Aggregate Pelagic Predators in a Subtropical Gyre.” Nature
609(7927): 535–40.

Baker, D. J., I. M. Maclean, M. Goodall, and K. J. Gaston. 2022.
“Correlations between Spatial Sampling Biases and Environ-
mental Niches Affect Species Distribution Models.” Global
Ecology and Biogeography 31(6): 1038–50.

Barbet-Massin, M., F. Jiguet, C. H. Albert, and W. Thuiller. 2012.
“Selecting Pseudo-Absences for Species Distribution Models:
How, where and how Many?” Methods in Ecology and Evolu-
tion 3(2): 327–38.

Becker, E. A., K. A. Forney, J. V. Redfern, J. Barlow, M. G. Jacox,
J. J. Roberts, and D. M. Palacios. 2019. “Predicting Cetacean
Abundance and Distribution in a Changing Climate.” Diversity
and Distributions 25(4): 626–43.

Beerkircher, L. R., E. Cortés, and M. Shivji. 2002. “Characteristics of
Shark Bycatch Observed on Pelagic Longlines off the Southeast-
ern United States, 1992–2000.” Marine Fisheries Review 64: 40–9.
Block, B. A., I. D. Jonsen, S. J. Jorgensen, A. J. Winship, S. A.
Shaffer, S. J. Bograd, E. L. Hazen, et al. 2011. “Tracking Apex
Marine Predator Movements in a Dynamic Ocean.” Nature
475(7354): 86–90.

Braun, C., M. Arostegui, N. Farchadi, M. Alexander, P. Afonso,
A. Allyn, S. Bograd, et al. 2023b. “Code for: Building Use-
Inspired Species Distribution Models: Using Multiple Data
Types to Examine and Improve Model Performance.” Zenodo.
<https://doi.org/10.5281/zenodo.7971532>.

Braun, C. D., M. C. Arostegui, N. Farchadi, M. Alexander, P.
Afonso, A. Allyn, S. J. Bograd, et al. 2023a. “Building
Use-Inspired Species Distribution Models: Using Multiple Data
Types to Examine and Improve Model Performance.” Dryad.
<https://doi.org/10.5061/dryad.h44j0zpr2>.

Braun, C. D., B. Galuardi, and S. R. Thorrold. 2018. “HMMoce: An
R Package for Improved Geolocation of Archival-Tagged
Fishes Using a Hidden Markov Method.” Methods in Ecology
and Evolution 9: 1212–20.

Braun, C. D., P. Gaube, T. H. Sinclair-Taylor, G. B. Skomal, and
S. R. Thorrold. 2019. “Mesoscale Eddies Release Pelagic Sharks
from Thermal Constraints to Foraging in the Ocean Twilight
Zone.” Proceedings of the National Academy of Sciences of the
United States of America 116(35): 17187–92.

18 of 20

BRAUN ET AL.

Braun, C. D., G. B. Skomal, and S. R. Thorrold. 2018. “Integrating
Archival Tag Data and a High-Resolution Oceanographic
Model to Estimate Basking Shark (Cetorhinus maximus) Move-
ments in the Western Atlantic.” Frontiers in Marine Science
5: 25.

Braun, C. D., G. B. Skomal, S. R. Thorrold, and M. L. Berumen.
2015. “Movements of the Reef Manta Ray (Manta alfredi) in
the Red Sea Using Satellite and Acoustic Telemetry.” Marine
Biology 162(12): 2351–62.

Brodie, S., B. Abrahms, S. J. Bograd, G. Carroll, E. L. Hazen, B. A.
Muhling, M. Pozo Buil, J. A. Smith, H. Welch, and M. G.
Jacox. 2021. “Exploring Timescales of Predictability in Species
Distributions.” Ecography 44(6): 832–44.

Brodie, S., M. G. Jacox, S. J. Bograd, H. Welch, H. Dewar, K. L.
Scales, S. M. Maxwell, et al. 2018. “Integrating Dynamic Sub-
surface Habitat Metrics into Species Distribution Models.”
Frontiers in Marine Science 5: 219.

Brodie, S., L. Litherland, J. Stewart, H. T. Schilling, J. G. Pepperell,
and I. M. Suthers. 2018. “Citizen Science Records Describe the
Distribution and Migratory Behaviour of a Piscivorous Preda-
tor, Pomatomus Saltatrix.” ICES Journal of Marine Science
75(5): 1573–82.

Campana, S. E., A. Dorey, M. Fowler, W. Joyce, Z. Wang,
D. Wright, and I. Yashayaev. 2011. “Migration Pathways,
Behavioural Thermoregulation and Overwintering Grounds of
Blue Sharks in the Northwest Atlantic.” PLoS One 6(2):
e16854.

Carey, F. G., and J. V. Scharold. 1990. “Movements of Blue Sharks
in Depth and Course.” Marine Biology

(Prionace glauca)
106(3): 329–42.

Crear, D. P., T. H. Curtis, S. J. Durkee, and J. K. Carlson. 2021.
“Highly Migratory Species Predictive Spatial Modeling
(PRiSM): An Analytical Framework for Assessing the Perfor-
mance of Spatial Fisheries Management.” Marine Biology
168(10): 1–17.

DeAngelis, D. L., and S. Yurek. 2017. “Spatially Explicit Modeling

in Ecology: A Review.” Ecosystems 20(2): 284–300.

Di Sciara, G. N., G. Lauriano, N. Pierantonio, A. Cañadas,
G. Donovan, and S. Panigada. 2015. “The Devil we don’t
Know: Investigating Habitat and Abundance of Endangered
Giant Devil Rays in the North-Western Mediterranean Sea.”
PLoS ONE 10(11): 1–17.

Domisch, S., M. Friedrichs, T. Hein, F. Borgwardt, A. Wetzig,
“Spatially
S. C.
Jähnig, and S. D. Langhans. 2019.
Explicit Species Distribution Models: A Missed Opportu-
nity in Conservation Planning?” Diversity and Distribu-
tions 25(5): 758–69.

Domisch, S., A. M. Wilson, and W. Jetz. 2016. “Modelbased Integra-
tion of Observed and Expertbased Information for Assessing
the Geographic and Environmental Distribution of Freshwater
Species.” Ecography 39(11): 1078–88.

Dorazio, R. M. 2014. “Accounting for Imperfect Detection and Sur-
vey Bias in Statistical Analysis of Presence-Only Data.” Global
Ecology and Biogeography 23(12): 1472–84.

Druon, J. N., S. Campana, F. Vandeperre, F. H. V. Hazin,
H. Bowlby, R. Coelho, N. Queiroz, et al. 2022. “Global-Scale
Environmental Niche and Habitat of Blue Shark (Prionace
glauca) by Size and Sex: A Pivotal Step to Improving Stock
Management.” Frontiers in Marine Science 9(4): 1–25.

Elith, J., C. H. Graham, R. P. Anderson, M. Dudík, S. Ferrier,
A. Guisan, R. J. Hijmans, et al. 2006. “Novel Methods Improve
Prediction of species’ Distributions from Occurrence Data.”
Ecography 29(2): 129–51.

Elith, J., J. R. Leathwick, and T. Hastie. 2008. “A working guide to
boosted regression trees.” Journal of Animal Ecology 77(4):
802–13.

Erauskin-Extramiana, M., H. Arrizabalaga, A. J. Hobday, A. Cabré,
L. Ibaibarriaga, I. Arregui, H. Murua, and G. Chust. 2019.
“Large-Scale Distribution of Tuna Species in a Warming
Ocean.” Global Change Biology 25(6): 2043–60.

Fletcher, R. J., T. J. Hefley, E. P. Robertson, B. Zuckerberg, R. A.
McCleery, and R. M. Dorazio. 2019. “A Practical Guide for
Combining Data to Model Species Distributions.” Ecology
100(6): 1–15.

Fletcher, R. J., R. A. McCleery, D. U. Greene, and C. A. Tye. 2016.
“Integrated Models that Unite Local and Regional Data Reveal
Larger-Scale Environmental Relationships and Improve Predic-
tions of Species Distributions.” Landscape Ecology 31(6): 1369–82.
Foster, D. G., S. P. Epperly, A. K. Shah, and J. W. Watson. 2012.
“Evaluation of Hook and Bait Type on the Catch Rates in the
Western North Atlantic Ocean Pelagic Longline Fishery.” Bul-
letin of Marine Science 88(3): 529–45.

Friedland, K. D., E. T. Methratta, A. B. Gill, S. K. Gaichas, T. H.
Curtis, E. M. Adams, J. L. Morano, D. P. Crear, M. C.
McManus, and D. C. Brady. 2021. “Resource Occurrence and
Productivity in Existing and Proposed Wind Energy Lease
Areas on the Northeast US Shelf.” Frontiers in Marine Science
8(4): 1–19.

Gilman, E., E. Zollett, S. Beverly, H. Nakano, K. Davis, D.
Shiode, P. Dalzell, and I. Kinan. 2006. “Reducing Sea Turtle
by-Catch in Pelagic Longline Fisheries.” Fish and Fisheries
7(1): 2–23.

Grüss, A., J. T. Thorson, and E. Jardim. 2019. “Developing Spatio-
Temporal Models Using Multiple Data Types for Evaluating
Population Trends and Habitat Usage.” ICES Journal of
Marine Science 76(6): 1748–61.

Guisan, A., and W. Thuiller. 2005. “Predicting Species Distribution:
Offering More than Simple Habitat Models.” Ecology letters
8(9): 993–1009.

Hazen, E. L., B. Abrahms, S. Brodie, G. Carroll, H. Welch, and
S. J. Bograd. 2021. “Where Did they Not Go? Considerations
for Generating Pseudo-Absences for Telemetry-Based Habi-
tat Models.” Movement Ecology 9(5): 1–13.

Hernandez, P. A., C. H. Graham, L. L. Master, and D. L. Albert.
2006. “The Effect of Sample Size and Species Characteristics
on Performance of Different Species Distribution Modeling
Methods.” Ecography 29(5): 773–85.

Hussey, N. E., S. T. Kessel, K. Aarestrup, S. J. Cooke, P. D. Cowley,
A. T. Fisk, R. G. Harcourt, et al. 2015. “Aquatic Animal Telem-
etry: A Panoramic Window into the Underwater World.”
Science 348(6240): 1255–642.

Isaac, N. J., M. A. Jarzyna, P. Keil, L. I. Dambly, P. H. Boersch-
Supan, E. Browning, S. N. Freeman, et al. 2020. “Data Integra-
tion for Large-Scale Models of Species Distributions.” Trends
in Ecology and Evolution 35(1): 56–67.

Jonsen, I. D., C. R. McMahon, T. A. Patterson, M. AugerMéthé,
R. Harcourt, M. A. Hindell, and S. Bestley. 2019. “Movement
Responses to Environment: Fast Inference of Variation among

ECOLOGICAL APPLICATIONS

19 of 20

Southern Elephant Seals with a Mixed Effects Model.” Ecology
100(1): e02566.

Jonsen, I. D., T. A. Patterson, D. P. Costa, P. D. Doherty, B. J.
Godley, W. J. Grecian, C. Guinet, et al. 2020. “A Continuous-
Time State-Space Model for Rapid Quality Control of Argos
Locations from Animal-Borne Tags.” Movement Ecology 8(1):
1–13.

Karp, M. A., S. Brodie, J. A. Smith, K. Richerson, R. L. Selden, O. R.
Liu, B. A. Muhling, et al. 2023. “Projecting Species Distribu-
tions Using Fishery-Dependent Data.” Fish and Fisheries 24(1):
71–92.

Kohler, N. E., and P. A. Turner. 2018. “Distributions and Move-
ments of Atlantic Shark Species: A 52-Year Retrospective Atlas
of Mark and Recapture Data.” Marine Fisheries Review 81(2):
1–93.

Kroodsma, D. A., J. Mayorga, T. Hochberg, N. A. Miller,
K. Boerder, F. Ferretti, A. Wilson, et al. 2018. “Tracking the
Global Footprint of Fisheries.” Science 359(6378): 904–8.
Kuhn, M. 2015. “Caret: Classification and Regression Training.”
Astrophysics Source Code Library, ascl–1505. <https://cran.r->
project.org/web/packages/caret/caret.pdf.

Lellouche, J.-M., E. Greiner, O. le Galloudec, G. Garric, C. Regnier,
M. Drevillon, M. Benkiran, et al. 2018. “Recent Updates to the
Copernicus Marine Service Global Ocean Monitoring and
Forecasting Real-Time 1/12 Degree High-Resolution System.”
Ocean Science 14(5): 1093–126.

Lezama-Ochoa, N., M. G. Pennino, M. A. Hall, J. Lopez, and
H. Murua. 2020. “Using a Bayesian Modelling Approach
(INLA-SPDE) to Predict the Occurrence of the Spinetail
Devil Ray (Mobular mobular).” Scientific Reports 10(1):
1–11.

Lopez, R., J.-P. Malarde, F. Royer, and P. Gaspar. 2014. “Improving
Argos Doppler Location Using Multiple-Model Kalman Filter-
ing.” IEEE Transactions on Geoscience and Remote Sensing
52(8): 4744–55.

MacKenzie, D. I., J. D. Nichols, G. B. Lachman, S. Droege, A. A.
Royle, and C. A. Langtimm. 2002. “Estimating Site Occupancy
Rates when Detection Probabilities Are Less than One.”
Ecology 83(8): 2248–55.

Maunder, M. N., and A. E. Punt. 2004. “Standardizing Catch and
Effort Data: A Review of Recent Approaches.” Fisheries
Research 70(2): 141–59.

Musyl, M. K., R. W. Brill, D. S. Curran, N. M. Fragoso, L. M.
McNaughton, A. Nielsen, B. S. Kikkawa, and C. D. Moyes. 2011.
“Postrelease Survival, Vertical and Horizontal Movements, and
Thermal Habitats of Five Species of Pelagic Sharks in the Cen-
tral Pacific Ocean.” Fishery Bulletin 109(4): 341–68.

Nielsen, A., and J. R. Sibert. 2007. “Statespace Model for Light-
Based Tracking of Marine Animals.” Canadian Journal of
Fisheries and Aquatic Sciences 64(8): 1055–68.

Norberg, A., N. Abrego, F. G. Blanchet, F. R. Adler, B. J. Anderson,
J. Anttila, M. B. Araújo, et al. 2019. “A Comprehensive Evalua-
tion of Predictive Performance of 33 Species Distribution
Models at Species and Community Levels.” Ecological Mono-
graphs 89(3): 1–24.

O’Toole, M., N. Queiroz, N. E. Humphries, D. W. Sims, and A. M.
Sequeira. 2021. “Quantifying Effects of Tracking Data Bias on
Species Distribution Models.” Methods in Ecology and Evolu-
tion 12(1): 170–81.

Pennino, M. G., D. Conesa, A. Lopez-Quilez, F. Munoz,
A. Fern(cid:2)andez, and J. M. Bellido. 2016. “Fishery-Dependent
and-Independent Data Lead to Consistent Estimations of
Essential Habitats.” ICES Journal of Marine Science 73(9):
2302–10.

Pinti, J., M. Shatley, A. Carlisle, B. A. Block, and M. J. Oliver. 2022.
“Using Pseudo-Absence Models to Test for Environmental
Selection in Marine Movement Ecology: The Importance of
Sample Size and Selection Strength.” Movement Ecology 10(1):
1–17.

Prince, E. D., and C. P. Goodyear. 2006. “Hypoxiabased Habitat
Compression of Tropical Pelagic Fishes.” Fisheries Oceanogra-
phy 15(6): 451–64.

Queiroz, N., N. E. Humphries, A. Couto, M. Vedor, I. da Costa,
A. M. M. Sequeira, G. Mucientes, et al. 2019. “Global Spatial
Risk Assessment of Sharks under the Footprint of Fisheries.”
Nature 572(7770): 461–6.

Robinson, N. M., W. A. Nelson, M. J. Costello, J. E. Sutherland, and
C. J. Lundquist. 2017. “A Systematic Review of Marine-Based
Species Distribution Models (SDMs) with Recommendations
for Best Practice.” Frontiers in Marine Science 4: 421.

Robinson, O. J., V. Ruiz-Gutierrez, M. D. Reynolds, G. H. Golet,
M. Strimas-Mackey, and D. Fink. 2020. “Integrating Citizen
Science Data with Expert Surveys Increases Accuracy and
Spatial Extent of Species Distribution Models.” Diversity and
Distributions 26(8): 976–86.

and

2018.

Sepulveda, C. A., S. A. Aalbers, C. Heberer, S. Kohin, and
“Movements
H. Dewar.
of
Swordfish Xiphias gladius in the United States Pacific Leather-
back Conservation Area.” Fisheries Oceanography 27(4): 381–94.
Sequeira, A. M. M., C. Mellin, M. G. Meekan, D. W. Sims, and
C. J. A. Bradshaw. 2013. “Inferred Global Connectivity of
Whale Shark Rhincodon Typus Populations.” Journal of Fish
Biology 82: 367–89.

Behaviors

Stirling, D. A., P. Boulcott, B. E. Scott, and P. J. Wright. 2016.
“Using Verified Species Distribution Models to Inform the
Conservation of a Rare Marine Species.” Diversity and Distribu-
tions 22(7): 808–22.

Stock, B. C., E. J. Ward, T. Eguchi, J. E. Jannot, J. T. Thorson, B. E.
Feist, and B. X. Semmens. 2020. “Comparing Predictions of
Fisheries Bycatch Using Multiple Spatiotemporal Species Dis-
tribution Model Frameworks.” Canadian Journal of Fisheries
and Aquatic Sciences 77(1): 146–63.

Vandeperre, F., A. Aires-da Silva, J. Fontes, M. Santos, R. Serr˜ao
Santos, and P. Afonso. 2014. “Movements of Blue Sharks
(Prionace glauca) across their Life History.” PloS one 9(8):
e103538.

Ward, P., and R. A. Myers. 2005. “Inferring the Depth Distribution
of Catchability for Pelagic Fishes and Correcting for Variations
in the Depth of Longline Fishing Gear.” Canadian Journal of
Fisheries and Aquatic Sciences 62(5): 1130–42.

Williamson, L. D., B. E. Scott, M. Laxton, J. B. Illian, V. L. Todd,
P. I. Miller, and K. L. Brookes. 2022. “Comparing Distribu-
tion of Harbour Porpoise Using Generalized Additive
Models and Hierarchical Bayesian Models with Integrated
Nested Laplace Approximation.” Ecological Modelling 470:
110011.

Wilson, S. G., B. S. Stewart, J. J. Polovina, M. G. Meekan, J. D.
Stevens, and B. Galuardi. 2007. “Accuracy and Precision of

20 of 20

BRAUN ET AL.

Archival Tag Data: A Multiple-Tagging Study Conducted on a
Whale Shark (Rhincodon typus) in the Indian Ocean.” Fisheries
Oceanography 16(6): 547–54.

Wisz, M. S., R. J. Hijmans, J. Li, A. T. Peterson, C. H. Graham,
A. Guisan, and NCEAS Predicting Species Distributions Work-
ing Group†. 2008. “Effects of Sample Size on the Performance
of Species Distribution Models.” Diversity and Distributions
14(5): 763–73.

Zulian, V., D. A. Miller, and G. Ferraz. 2021. “Integrating Citizen-
Science and Planned-Survey Data Improves Species Distribu-
tion Estimates.” Diversity and Distributions 27(12): 2498–509.

How to cite this article: Braun, Camrin D.,
Martin C. Arostegui, Nima Farchadi,
Michael Alexander, Pedro Afonso, Andrew Allyn,
Steven J. Bograd, et al. 2023. “Building
Use-Inspired Species Distribution Models: Using
Multiple Data Types to Examine and Improve
Model Performance.” Ecological Applications
e2893. <https://doi.org/10.1002/eap.2893>
