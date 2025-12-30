1
2
0
2

g
u
A
0
2

]
E
C
.
s
c
[

1
v
4
9
3
9
0
.
8
0
1
2
:
v
i
X
r
a

Beyond Tracking: Using Deep Learning to
Discover Novel Interactions in Biological Swarms

Taeyeong Choi1, Benjamin Pyenson2, Juergen Liebig2, and
Theodore P. Pavlic2,3,4

1 Lincoln Institute for Agri-food Technology, University of Lincoln, Riseholme Park,
Lincoln, UK
2 School of Life Sciences, Social Insect Research Group,
Arizona State University, Tempe, AZ 85281, USA
3 School of Computing, Informatics, and Decision Systems Engineering,
Arizona State University, Tempe, AZ 85281, USA
4 School of Sustainability, Arizona State University, Tempe, AZ 85281, USA
<tchoi@lincoln.ac.uk>, {bpyenson, jliebig, tpavlic}@asu.edu

Abstract. Most deep-learning frameworks for understanding biologi-
cal swarms are designed to ﬁt perceptive models of group behavior to
individual-level data (e.g., spatial coordinates of identiﬁed features of in-
dividuals) that have been separately gathered from video observations.
Despite considerable advances in automated tracking, these methods are
still very expensive or unreliable when tracking large numbers of animals
simultaneously. Moreover, this approach assumes that the human-chosen
features include suﬃcient features to explain important patterns in col-
lective behavior. To address these issues, we propose training deep net-
work models to predict system-level states directly from generic graph-
ical features from the entire view, which can be relatively inexpensive
to gather in a completely automated fashion. Because the resulting pre-
dictive models are not based on human-understood predictors, we use
explanatory modules (e.g., Grad-CAM) that combine information hid-
den in the latent variables of the deep-network model with the video data
itself to communicate to a human observer which aspects of observed in-
dividual behaviors are most informative in predicting group behavior.
This represents an example of augmented intelligence in behavioral ecol-
ogy – knowledge co-creation in a human–AI team. As proof of concept,
we utilize a 20-day video recording of a colony of over 50 Harpegnathos
saltator ants to showcase that, without any individual annotations pro-
vided, a trained model can generate an “importance map” across the
video frames to highlight regions of important behaviors, such as dueling
(which the AI has no a priori knowledge of), that play a role in the
resolution of reproductive-hierarchy re-formation. Based on the empiri-
cal results, we also discuss the potential use and current challenges to
further develop the proposed framework as a tool to discover behaviors
that have not yet been considered crucial to understand complex social
dynamics within biological collectives.

Keywords: Deep Learning in Behavioral Ecology, Swarm Behavior, Ex-
plainable AI, Augmented Intelligence, Knowledge Co-creation

2

Taeyeong Choi et al.

Fig. 1: Proposed usage of DCNNs, trained to predict global state of the swarm
system from the entire view to later reveal key local observations by using the
gradient between the learned local feature and the prediction output in the
model.

1

Introduction

Deep Convolutional Neural Networks (DCNNs) have been widely adopted as the
primary backbone of data-driven frameworks to solve complex problems in com-
puter vision including object classiﬁcation or detection and recognition of human
actions [10], [14], [15]. The nature of their multi-layer structure has a powerful
ability to automatically learn to identify key local features (e.g., edges) from raw
pixels of images and combine into more meaningful concepts (e.g., pointy ears)
to produce a ﬁnal prediction output (e.g., dog), as the data is processed from
the lowest layer through the higher ones [4]. In fact, this may imply that if the
target data contains global information of biological swarms, lower-level visual
properties such as locations, motions, and interactions of the entities could au-
tomatically be identiﬁed throughout the hierarchical layers during the training
process. However, deep learning in behavioral biology has mostly been limited
to building perceptive models to localize particular body parts of each entity
to generate another input to a subsequent analysis model to capture motional
concepts of individuals and perform a prediction for the entire swarm based on
them [2], [5], [8], [11].

There can be two main challenges in this approach: 1) obtaining the indi-
vidual feature labels can require a signiﬁcant amount of human eﬀort especially
when a large group of system is examined, and 2) the choice of features relies
heavily on prior knowledge of human experts in the biological system. To address
these issues, as visualized in Fig. 1, we here suggest training the deep-network
models to predict system-level states directly from generic graphical features
from the entire view, which can be relatively inexpensive to gather, and ex-
amine the salient behavioral regularities discovered in the trained intermediate
layers by using gradient-based explanation modules (e.g., Grad-CAM [13]). In
other words, our proposal is to make more use of the aforementioned poten-
tial of DCNN to automatically discover ﬁne-grained, individual-level motional

Beyond Tracking

3

Fig. 2: Example of Grad-CAM in
which the key regions are high-
lighted for class “Elephant”[1].

Fig. 3: Colony of 59 H. saltator as
a testbed, with a foraging cham-
ber accessed by the south tunnel.

patterns highly associated with macroscopic swarm properties so that the pre-
dictive model can later be queried about what these patterns are without being
constrained by prior knowledge from human experts.

Speciﬁcally, in this paper, we propose the use of the explainable module
Grad-CAM (Fig. 2) for biological research. Extending our previous work [3], we
utilize a 20-day video recording of a colony of over 50 Harpegnathos saltator ants
to demonstrate that without any individual annotations provided as input, the
trained model can classify social stability of colonies while also generating an
“importance map” across video frames to selectively highlight regions of inter-
actions (e.g., dueling) as potentially important drivers of colony state.

2 Proposed Framework

Rather than training on small-scale features of individuals in videos, our ap-
proach trains a DCNN to predict coarse-grained, large-scale labels (y) from rep-
resentations of generic features from video data. Any discrete, large-scale prop-
erty can be used, such as whether a crowd [7] is about to riot. We use hierarchy
state y ∈ {Stable, U nstable} for a H. saltator colony [3]. Our n-layer classiﬁer
consists of m two-dimensional convolutional layers φ1≤(cid:96)≤m followed by other
types ψm+1≤(cid:96)(cid:48)≤n, such as recurrent or fully-connected layers. Convolutional lay-
ers are used as feature extractors in this architecture since each output fij at φ(cid:96)
can compactly encode the local observation in a larger region (“receptive ﬁeld”)
at previous layers φ(cid:96)(cid:48)(cid:48)<(cid:96); i.e., a change in fij can imply the ampliﬁcation or
decrease of the motion pattern observed in the corresponding region.

For explanation of what visual regions are most important to the predictive
model, Grad-CAM [13] is employed on K two-dimensional output feature maps,
each denoted as f k ∈ Rh×w, at a convolutional layer φ(cid:96) to ﬁnally calculate the
“importance map” M c over the original input for a particular class c. In the
technical aspect, φ(cid:96) can be an arbitrary layer satisfying (cid:96) ∈ {1, 2, ..., m}, but the
layer φ(cid:96) close to φm is typically chosen to access more abstract features with
wider receptive ﬁelds than the ones available at lower layers φ(cid:96)(cid:48)<(cid:96). For brevity,
we denote φ to be the chosen convolutional layer in the following descriptions.

4

Taeyeong Choi et al.

ij = ∂yc/∂f k

To generate the importance map M c, we ﬁrst obtain the gradient gc of the
output yc with respect to each feature map f k from φ, i.e., gc
ij. There-
fore, gc
ij > 0 implies that enhancing the observational pattern encoded by f k
ij
increases the predicted likelihood of class c – the discovered pattern is “salient”
for class c – and gc
ij ≤ 0 implies that the observation is considered irrelevant to
the prediction of class c. Then, for each feature map f k, Grad-CAM then uses
this quantity to gain the averaged importance ac
ij (where Z
is a normalization constant). Finally, the importance map M c is computed by
the weighted summation of feature maps:
(cid:18) (cid:88)

k = (1/Z) (cid:80)

j gc

(cid:80)

(cid:19)

i

M c = Γ

k (cid:12) f k
ac

(1)

k

where (cid:12) is the element-wise multiplication, and Γ (a) = a for a > 0 and Γ (a) = 0
otherwise. In Section 4, we also introduce a more restrictive Γ (cid:48) that gates only
the top 5% values so as to strictly verify whether key behaviors are eﬀectively
highlighted with the highest level of conﬁdence. Also, M c can be spatially up-
sampled to ﬁt the original image of a desired size for visualization purpose.

3 Testbed Design with H. saltator

As in [3], a colony of H. saltator is utilized as a testbed to validate whether our
proposed framework can reveal salient behavioral patterns. A conspicuous “un-
stable” state can be induced in this system through the removal of identiﬁed egg
layers (“gamergates”) [9] that triggers a hierarchy reformation process. During
this process, aggressive interactions such as dueling [12] can be readily observed
for several weeks until several mated workers activate their ovaries and start to
lay eggs as the new gamergates, causing the colony to return to its nominal sta-
ble state [6]. We apply our framework to this system by building a binary-state
classiﬁer on the stability of the colony. We use the resulting deep-network model
to identify important behaviors of interest and validate whether dueling (Fig. 4a)
is discovered without a priori knowledge of it. Other behaviors identiﬁed by the
system may then warrant further investigation by human researchers.

3.1 Video Data from Colonies Undergoing Stabilization

As shown in Fig. 3, each 20-day video was taken with an overhead camera to
observe 59 H. saltator ants in plaster nests covered with glass. Due to a foraging
chamber outside the view of the camera, not all ants are necessarily visible at
all times, and some paralyzed crickets can be carried into the view. We arti-
ﬁcially disturbed the reproductive hierarchy by removing all four preidentiﬁed
gamergates after the second day of recording and further observed the process
of hierarchy reformation until aggressive interactions almost disappeared in the
last several days. Therefore, the video frames of the ﬁrst 2 days are annotated
with y = Stable, while the later ones of 18 days are all with y = U nstable.

Beyond Tracking

5

(a)

(b)

Fig. 4: (a) Example of two consecutive RGB frames cropped around a dueling
interaction in yellow circle for visibility; (b) Horizontal and vertical optical ﬂow
vectors generated from (a), in each of which red (blue) are the regions of move-
ment in the positive (negative) direction along the corresponding axis.

We follow the preprocessing method in [3] to extract from consecutive frames
their optical ﬂow, for which a pair of vectors encodes the horizontal and vertical
transient movements from the input sequence (e.g., Fig. 4) [7]. Two optical ﬂows
in spatial resolution of 64 × 64 were computed every two minutes to use as an
input x to the model, as each was obtained from two consecutive RGB frames
0.5 seconds apart in times. More details of the dataset are available online5.

3.2 Deployed DCNNs with Grad-CAM

We use a classiﬁer from our previous work [3] for the one-class classiﬁcation
task of predicting colony state. That colony-state classiﬁer has an overall perfor-
mance of 0.786 in the Area Under the Curve (AUC) of the Receiver Operating
Characteristic (ROC) while only taking two consecutive optical ﬂows as input.
Moreover, colony-state predictions during the early period of ﬁrst 6 days after
the reproductive hierarchy is disturbed have higher AUC scores than 0.900 in
average [3], indicating that the micro-scale graphical features identiﬁed by the
deep network may be strong predictors of macro-scale state dynamics.

More speciﬁcally, the classiﬁer we use has four 2D convolutional layers φ1:4
with 2D max pooling between consecutive layers, and six other types of lay-
ers ψ5:10 follow to produce the estimated likelihood of unstable colony state. As
described in Section 2, we then employ Grad-CAM on the feature maps from
φ4. For each generated importance map M c, bicubic interpolation is applied to
match the size of the frame image to overlay.

4 Results and Model Validation

As discussed in Section 3, we validate our approach by conﬁrming that dueling
behavior between ants is identiﬁed by the AI as strongly related to the unstable
colony state. A model that can detect dueling with no prior knowledge of the be-
havior may identify other behavioral patterns that warrant further investigation.

5 <https://github.com/ctyeong/OpticalFlows> HsAnts

6

Taeyeong Choi et al.

(a)

(c)

(b)

(d)

Fig. 5: (a): Heatmaps from Grad-CAM at two arbitrary times; (b), (c), (d): Three
dueling examples captured by the top 5% impactful regions of red. Each pair
shows two consecutive frames cropped around the interaction for clarity.

Figure 5a displays the heatmaps produced by the initial application of Grad-
CAM with rectiﬁer Γ . Grad-CAM identiﬁes that the central area is more critical
than the boundaries, and this general pattern is consistent over time despite
changes in ant behaviors. This visualization indicates that, for the purpose of
identifying changes in colony hierarchical state, the neural network has learned
to ignore interactions near boundaries and instead focuses on interactions in
the center of the area. Although this pattern matches intuition from human
observations of these ants, it is too coarse to identify important behaviors.

We thus applied a ﬁltered rectiﬁer Γ (cid:48) to only visualize regions of the top-
5% positive gradients to identify the most dramatic responses in the generated
heatmap to the ant motions, which resulted in more reﬁned identiﬁcations of
regions of importance. Figures 5b, 5c, and 5d show examples of dueling inter-
actions detected by these highest gradients. Given that the deep network was
not provided coordinates of the ants nor prior behavioral models of dueling, it is
not surprising that the highlighted regions do not precisely identify speciﬁc ants
in the interactions. Nevertheless, the network identiﬁes general regions in close
proximity to important behaviors. In particular, in Fig. 5c and 5d, more than
two ants were engaged in dueling, but the detection region dynamically moved
around them while they actively participated. These results support that the
trained model has not overﬁt trivial attributes such as brightness or contrast of
video but learned from ant behaviors themselves.

Figure 6a also shows the case where two duelers are captured as intended
while other active ants who are simply showing swift turns nearby each other
without direct interaction are ignored by our model. This indicates that the

Beyond Tracking

7

(a)

(b)

Fig. 6: Two examples in which dueling ants are detected (yellow dash line) while
other active ones are ignored (white dash line).

DCNN classiﬁer does not blindly take any type of movement into account for
prediction; only relevant patterns are prioritized as features to utilize. Similarly,
in Fig. 6b, two dueling ants are detected among a group of other non-dueling
neighbors that are presenting rapid changes in motion and orientation. This
example also demonstrates the ability of our trained model to ﬁlter out unim-
portant motion patterns even when a high degree of motion ﬂow is present.

5 Summary, Discussion, & Future Work

We have proposed a deep-learning pipeline as a tool to uncover salient inter-
actions among individuals in a swarm without requiring prior human knowl-
edge about the behaviors or signiﬁcant preprocessing eﬀort devoted to individual
tracking and behavioral coding. Our experimental results show that a trained
classiﬁer integrated with Grad-CAM can localize regions of key individual-scale
interactions used by the classiﬁer to make its colony-scale predictions. Validating
our approach, identiﬁed behaviors, such as dueling, are the same behaviors that
have been identiﬁed previously by human researchers without the aid of machine
learning; however, our classiﬁer discovered them without any prior guidance from
humans. Thus, the library of other highlighted patterns from our pipeline can
be used to generate new testable hypotheses of individual-to-colony emergence.
Our proposed approach greatly reduces human annotation eﬀort as only
macro-scale, swarm-level annotations are used in training. Signiﬁcant eﬀort is
currently being used to develop machine-learning models for the subtask of
tracking alone. Our approach suggests that tracking may, in many cases, be
an unnecessary step that wastes both computational and human resources. Fur-
thermore, our proposed approach reduces the risk of introducing human bias in
the pre-processing of individual-level observations. Consequently, our example
is a model of how human–AI observational teams can engage in knowledge co-
creation – each providing complementary strengths and ultimately realizing the
vision of augmented, as opposed to purely artiﬁcial, intelligence.

An important future direction is to further classify the highlighted patterns
automatically discovered by these pipelines. Human behavioral ecologists can
discriminate between peculiar interactions (e.g., dueling, dominance biting, and

8

Taeyeong Choi et al.

policing [12]) that all may occur during the most unstable phases of reproduc-
tive hierarchy formation in H. saltator ants. Our method may have the ability
to identify these behaviors, but it does not currently cluster similar identiﬁed
patterns together and generate generalizable stereotypes that would be instruc-
tive to human observers hoping to identify these behaviors in their own future
observations. Unsupervised learning methods could be adopted as a subsequent
module to perform clustering and dimensionality reduction to better communi-
cate common features of clusters, which may include patterns not yet appreciated
by human researchers that are apparently useful in predicting swarm behavior.

References

[1] Grad-CAM class activation visualization (2020). URL <https://keras.io/examples/>

vision/grad cam/

[2] Bozek, K., Hebert, L., Mikheyev, A.S., Stephens, G.J.: Towards dense object track-

ing in a 2D honeybee hive. In: Proc. IEEE CVPR 2018 (2018)

[3] Choi, T., Pyenson, B., Liebig, J., Pavlic, T.P.: Identiﬁcation of abnormal states in
videos of ants undergoing social phase change. In: Proc. AAAI 2021 (2021)
[4] Goodfellow, I., Bengio, Y., Courville, A., Bengio, Y.: Deep learning. MIT press

Cambridge (2016)

[5] Graving, J.M., Chae, D., Naik, H., Li, L., Koger, B., Costelloe, B.R., Couzin, I.D.:
Deepposekit, a software toolkit for fast and robust animal pose estimation using
deep learning. eLife 8 (2019)

[6] Liebig, J., Peeters, C., H¨olldobler, B.: Worker policing limits the number of repro-

ductives in a ponerine ant. Proc. R. Soc. B 266(1431) (1999)

[7] Mehran, R., Oyama, A., Shah, M.: Abnormal crowd behavior detection using

social force model. In: Proc. IEEE CVPR 2009 (2009)

[8] Nath, T., Mathis, A., Chen, A.C., Patel, A., Bethge, M., Mathis, M.W.: Using
deeplabcut for 3D markerless pose estimation across species and behaviors. Nat.
Protoc. 14(7) (2019)

[9] Peeters, C., Crewe, R.: Worker reproduction in the ponerine ant ophthalmopone
berthoudi: an alternative form of eusocial organization. Behav. Ecol. Sociobiol.
18(1) (1985)

[10] Redmon, J., Farhadi, A.: Yolov3: An incremental improvement. arXiv:1804.02767

(2018)

[11] Romero-Ferrero, F., Bergomi, M.G., Hinz, R.C., Heras, F.J., de Polavieja, G.G.:
Idtracker. ai: tracking all individuals in small or large collectives of unmarked
animals. Nat. Methods 16(2) (2019)

[12] Sasaki, T., Penick, C.A., Shaﬀer, Z., Haight, K.L., Pratt, S.C., Liebig, J.: A simple
behavioral model predicts the emergence of complex animal hierarchies. Am. Nat.
187(6) (2016)

[13] Selvaraju, R.R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., Batra, D.: Grad-
cam: Visual explanations from deep networks via gradient-based localization. In:
Proc. IEEE ICCV 2017, pp. 618–626 (2017)

[14] Simonyan, K., Zisserman, A.: Very deep convolutional networks for large-scale

image recognition. arXiv:1409.1556 (2014)

[15] Wang, L., Xiong, Y., Wang, Z., Qiao, Y., Lin, D., Tang, X., Van Gool, L.: Temporal
segment networks: Towards good practices for deep action recognition. In: Proc.
ECCV 2016. Springer (2016)
