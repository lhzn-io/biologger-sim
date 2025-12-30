4
2
0
2

y
a
M
2
2

]

G
L
.
s
c
[

1
v
2
0
0
4
1
.
5
0
4
2
:
v
i
X
r
a

Animal Behavior Analysis Methods Using Deep Learning: A Survey

EDOARDO FAZZARI, Sant’Anna School of Advanced Studies, Italy
DONATO ROMANO, Sant’Anna School of Advanced Studies, Italy
FABRIZIO FALCHI, Institute of Information Science and Technologies, National Research Council of Italy, Italy

and Sant’Anna School of Advanced Studies, Italy

CESARE STEFANINI, Sant’Anna School of Advanced Studies, Italy

Animal behavior serves as a reliable indicator of the adaptation of organisms to their environment and their overall well-being. Through

rigorous observation of animal actions and interactions, researchers and observers can glean valuable insights into diverse facets of

their lives, encompassing health, social dynamics, ecological relationships, and neuroethological dimensions. Although state-of-the-art

deep learning models have demonstrated remarkable accuracy in classifying various forms of animal data, their adoption in animal

behavior studies remains limited. This survey article endeavors to comprehensively explore deep learning architectures and strategies

applied to the identification of animal behavior, spanning auditory, visual, and audiovisual methodologies. Furthermore, the manuscript

scrutinizes extant animal behavior datasets, offering a detailed examination of the principal challenges confronting this research

domain. The article culminates in a comprehensive discussion of key research directions within deep learning that hold potential for

advancing the field of animal behavior studies.

CCS Concepts: • Computing methodologies → Machine learning; • Applied computing → Bioinformatics.

Additional Key Words and Phrases: Animal Behavior, Deep Learning, Pose Estimation, Object Detection, Bio-acoustics, Machine

Learning

ACM Reference Format:

Edoardo Fazzari, Donato Romano, Fabrizio Falchi, and Cesare Stefanini. 2023. Animal Behavior Analysis Methods Using Deep Learning:

A Survey. 1, 1 (May 2023), 28 pages. <https://doi.org/XXXXXXX.XXXXXXX>

1 INTRODUCTION

Animal behavior encompasses a spectrum of actions, reactions, and activity patterns demonstrated by animals in

response to their environment, fellow organisms, and internal stimuli [29]. This expansive field covers a diverse range

of behaviors, spanning from innate instincts and simple reflexes to intricate social interactions and learned conduct.

The study of animal behavior involves the observation, description, and comprehension of how animals engage with

one another and their surroundings. Presently, the landscape of animal behavior research is undergoing rapid evolution,

propelled by the continual introduction of innovative experimental methodologies and the advancement of sophisticated

Authors’ addresses: Edoardo Fazzari, <edoardo.fazzari@santannapisa.it>, Sant’Anna School of Advanced Studies, Piazza Martiri della Libertà, Pisa, Italy,
56127; Donato Romano, Sant’Anna School of Advanced Studies, Piazza Martiri della Libertà, Pisa, Italy, 56127, <donato.romano@santannapisa.it>; Fabrizio
Falchi, Institute of Information Science and Technologies, National Research Council of Italy, Via G. Moruzzi, Pisa, Italy, 56124 and Sant’Anna School of
Advanced Studies, Piazza Martiri della Libertà, Pisa, Italy, 56127, <fabrizio.falchi@cnr.it>; Cesare Stefanini, Sant’Anna School of Advanced Studies, Piazza
Martiri della Libertà, Pisa, Italy, 56127, <cesare.stefanini@santannapisa.it>.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not
made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components
of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to
redistribute to lists, requires prior specific permission and/or a fee. Request permissions from <permissions@acm.org>.

© 2023 Association for Computing Machinery.
Manuscript submitted to ACM

Manuscript submitted to ACM

1

2

Fazzari, et al.

behavior detection systems [190]. This progression holds particular significance in advancing our understanding of

neuroethological aspects, exemplified by the utilization of mice in exploring diseases like Alzheimer’s [149], and in

refining animal welfare practices within agriculture [128]. The impetus behind this surge in progress is the integration

of cutting-edge technologies, with deep learning standing out as a transformative force that reshapes the approaches

researchers employ to investigate and interpret animal behaviors[29].

Deep learning has emerged as a pivotal tool in the exploration of animal behavior. This advanced branch of

artificial intelligence empowers computers to autonomously discern patterns and features from extensive datasets. As

researchers amass increasingly intricate datasets through state-of-the-art monitoring technologies, including high-

resolution cameras, GPS tracking devices, and sensors, the capability of deep learning algorithms to extract meaningful

insights becomes indispensable [16, 94]. This not only expedites the analysis process but also reveals nuanced aspects

of animal behavior that were previously challenging to decipher. Furthermore, deep learning plays a crucial role

in the development of sophisticated behavior detection systems. These systems can automatically recognize and

classify various behaviors, allowing researchers to redirect their focus from laborious manual data annotation to the

interpretation of results [8]. This acceleration in data processing and behavior recognition enhances the scalability and

efficiency of animal behavior studies, ushering in a new era of discovery and understanding in this dynamic field.

1.1 Survey structure

The structure of our survey is systematically delineated as follows: In the initial section, we expound upon the underlying

motivation propelling the use of deep learning for examining animal behaviors, explaining the inherent limitations

therein. Concurrently, we articulate the research questions that our survey endeavors to address. Subsequently, a

comprehensive exposition of the methodological framework employed for conducting the survey is presented, which

includes a discerning analysis of the gathered data to elucidate discernible trends within the research domain. The

subsequent segmentation of the study into two distinct components is pivotal to the overarching architecture of this

article. These segments, namely pose estimation and non-pose estimation-based methods, constitute the primary

constituents of our investigation, elucidating the extraction of salient information pertinent to animal behavioral

analysis and its subsequent application in behavior identification. Following this delineation, we furnish a compendium

of publicly available datasets. In conclusion, we revisit the initially posited research questions, providing responses in

light of the findings expounded within the two principal segments of the article.

1.2 Contributions

This survey article makes a threefold contribution to the current understanding of the study of animal behavior through

deep learning:

• We provide a thorough examination of existing technologies and algorithms employed in the analysis of animal
behavior. This entails a detailed exploration of methodologies and approaches currently prevalent in this domain,

providing readers with a nuanced understanding of the technological landscape.

• We compile and present a comprehensive list of publicly available datasets relevant to the research field. This
compilation serves as a valuable resource for researchers and practitioners, facilitating access to essential data

for furthering investigations into animal behaviors through data-driven methodologies.

• We engage in a substantive discussion regarding potential directions for the evolution of the field. Emphasizing
the integration of deep learning techniques, our discourse aims to enhance the quality of existing technologies,

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

3

thereby advancing the understanding of animal behaviors. This forward-looking analysis provides insights into

potential avenues for improvement and innovation.

To the best of our knowledge, this survey is the only examination of the topic to date. The comprehensive overview,

dataset compilation, and forward-looking discussions collectively contribute to a nuanced understanding of current

advancements and lay the groundwork for future developments in the application of deep learning to the study of

animal behavior.

2 MOTIVATION AND PROBLEM STATEMENT

In this section, we expound upon the foundational motivations that underscore the study of animal behavior through deep

learning, articulating the diverse advantages and objectives inherent to this specialized research domain. Concurrently,

we meticulously scrutinize the principal limitations that characterize this field, recognizing the nuanced challenges that

arise from variations in research setups. Our intention is to furnish a comprehensive guide for prospective researchers,

endowing them with a thorough understanding of potential impediments prior to initiating investigations within this

domain. Concurrently, we underscore the myriad opportunities inherent in the study of animal behavior, fostering an

appreciation for the intricate dimensions of this research frontier.

Table 1. Summary of the limitations and objectives in studying animal behaviors. DL stands for Deep Learning

Limitations

Sensor-induced stress
Battery life
Data noise
Storage constraints
Labeling economics
Subjective annotation
Computational demands
Ethical considerations
In-field tracking
Environmental unpredictability

Objectives
Biodiversity conservation
Biodiversity preservation
Ecological insight
Health impact
Welfare optimization
Pest management
Social dynamics
Non-invasive (DL related)
Real-time applications (DL related)

2.1 Limitations in studying animal behaviors

The exploration of animal behavior is confronted by a multitude of challenges that intricately shape the effectiveness

and practicality of its applications. These challenges permeate the methodologies employed for data acquisition, the

intricacies of data analysis (both in terms of location and computational demands), and the nuanced process of data

annotation.

An integral aspect of animal behavior studies is the utilization of sensors for data collection. However, the attachment

of sensors to animals introduces a unique set of challenges. Notably, there is a risk of inducing stress responses and

altering normal behaviors [207]. This necessitates a profound reflection on the authenticity of the collected data, urging

researchers to question whether stress-induced behaviors accurately mirror natural patterns. Moreover, the task of

differentiating genuine behavioral signals from background noise in sensor data adds complexity to interpretation,

emphasizing the requirement for advanced algorithms capable of discerning meaningful patterns amidst the noise [88].

Beyond stress responses and noise challenges, sensor equipment grapples with limitations in battery life [126], impacting

Manuscript submitted to ACM

4

Fazzari, et al.

the duration and scope of behavioral studies, especially in scenarios requiring continuous data collection over extended

periods. Researchers are challenged to strike a balance between the need for comprehensive, continuous monitoring

and the practical constraints imposed by limited battery capacities.

Transitioning into the domain of mobile devices introduces another layer of complexity to the challenges encountered

in deep learning applications. The implementation of models on these devices confronts the persistent issue of storage

limitations [33]. Balancing robust object detection with efficient data compression becomes a paramount concern, with

techniques like Quantized-CNN [196] attempting to address this challenge. However, the ongoing quest is to achieve

this balance without compromising precision, a crucial consideration for the reliability of behavioral analyses.

A pivotal challenge arises in the realm of labeling and annotation, where economic and practical constraints hinder the

tagging of large datasets for each animal [20]. This bottleneck impedes the scalability of deep learning models, heavily

reliant on labeled datasets for effective training. The impracticality of manual labeling raises fundamental concerns

about the breadth and accuracy of behavioral datasets, impacting the reliability of subsequent analyses. Subjectivity

compounds these challenges, influencing the accuracy and consistency of behavioral annotations. Visual inspection,

often subjective, is limited in providing objective insights into complex animal behaviors [19]. Manual annotation, while

traditional, is labor-intensive and susceptible to inter-annotator disagreements [172, 209]. The inherent subjectivity

introduces variability, raising questions about the replicability and reliability of experiments [47, 74].

Moreover, these challenges extend to innovative techniques, such as multi-view recordings, which hold promise for

providing richer insights into animal behaviors [81]. However, challenges arise in correlating social behaviors from

different perspectives due to the lack of correspondence across data sources. Effectively coordinating information from

multiple viewpoints demands inventive approaches to ensure accuracy and reliability, representing a frontier where

deep learning methodologies can contribute significantly.

A major challenge surfaces when comparing laboratory studies, where challenges often revolve around the subjec-

tivity introduced by the controlled environment, with ethological studies conducted in the wild presenting a distinct set

of challenges, notably in-field tracking [119]. The diverse and unpredictable environments encountered in the wild

introduce complexities not found in controlled laboratory settings. Bridging the gap between these two disciplines ne-

cessitates adaptable detection and tracking algorithms that seamlessly operate in both environments. Robust algorithms

capable of handling varying animal sizes, changing appearances, clutter, occlusions, and unpredictable environments

are vital for extracting meaningful insights [65, 74, 98]. These challenges underscore the critical need for technological

innovation that aligns with the demands of both controlled and wild settings.

2.2 Objectives in studying animal behaviors

Studying animal behavior offers manifold advantages, enriching our comprehension of the natural world and presenting

practical applications across diverse domains, including neuroscience, pharmacology, medicine, agriculture, ecology,

and robotics. Six key advantages of studying animal behavior are identified:

(1) Biodiversity Conservation: Understanding animal behavior is crucial for the conservation of biodiversity [48,

74, 139, 156, 192]. Knowledge of behaviors such as migration patterns, feeding habits, and reproductive strategies

is essential for designing effective conservation strategies and protecting endangered species.

(2) Ecological Understanding: Animal behavior provides insights into the ecological dynamics of ecosystems [2, 63].

Behavioral studies help researchers understand how animals interact with their environment, including their

roles in nutrient cycling, seed dispersal, and predator-prey relationships [38, 134, 202].

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

5

(3) Human Health and Medicine: Studying animal behavior can have implications for human health and

medicine [60, 68, 115, 175]. For example, research on animal models helps in understanding certain diseases

and developing potential treatments. Behavioral studies on animals also contribute to our understanding of the

neurobiology and psychology that underlie human behavior [44, 123, 168].

(4) Animal Welfare and Husbandry: Knowledge of animal behavior is essential for promoting the welfare of

domesticated animals and optimizing their husbandry practices [13, 81]. Understanding how animals express

natural behaviors can inform the design of environments that support their physical and psychological well-

being [79, 117, 180].

(5) Pest Control and Agriculture: Although right now it is very limited to pest identification, understanding the

behavior of pest species can aid in the development of effective pest control strategies in agriculture [45, 83, 127].

This knowledge helps farmers manage crop damage and reduce the need for harmful pesticides [116, 181].

(6) Understanding Social Dynamics: Observing social behaviors in animals can provide insights into the principles

governing social structures and interactions [146, 197]. This knowledge can have applications in fields such as

sociology and psychology, contributing to our understanding of social dynamics in general [5, 97, 153].

In this context, deep learning plays a pivotal role and emerges as a major technology in advancing the field, opening

new opportunities. Addressing the limitations discussed in the previous section, we will now elaborate on the advantages

that deep learning and computational technologies bring to the study of animal behavior.

We previously emphasized the integral aspect of employing sensors for data collection in animal behavior studies,

which may induce stress and high noise levels. The use of multiple and diverse sensors for data acquisition, coupled

with advanced architectures incorporating fusion layers, has been shown to mitigate noise and enhance the precision of

analysis [114]. However, attaching sensors directly to animals may introduce bias, prompting researchers in livestock

health assessment and neuroscience to adopt computer vision. The ability of computer vision to provide real-time, non-

invasive, and accurate animal-level information through the use of cameras has gained popularity [142]. Nevertheless,

this approach is limited to setups within the camera frame, except for innovations like Haalck et al.’s [65] moving

camera that tracks animals, creating a dynamic map of their environment. In larger scenarios, such as meadows where

cows graze, sensors remain preferable. Nevertheless, collecting and analyzing sensor data from mobile devices on

animals proves challenging and time-consuming. To address this, Dang et al. [46] introduced Long Range Area Network

(LoRaWAN), where sensors attached to cows connect to gateways transmitting information to the cloud. This not

only overcomes the limitations of computational power associated with mobile devices but also ensures continuous,

real-time data analysis.

The efficacy of deep learning is contingent on annotated data, especially for supervised approaches. While manual

annotation remains unavoidable, in tasks such as pose estimation and classification, labeling can be iterative. This

involves annotating a small portion of the dataset, training a network, predicting on new images, correcting labels,

and repeating this process multiple times. This iterative approach accelerates the labeling process, as demonstrated by

Pereira et al. [151]. Another approach is to generate artificial labels [103].

Table 1 succinctly encapsulates a consolidated overview of both primary limitations and advantages, providing a

discerning reference for researchers navigating the sophisticated landscape of animal behavior studies.

2.3 Research questions

The survey aims to address the following research questions:

Manuscript submitted to ACM

6

Fazzari, et al.

RQ1 Which animal species are less considered and why?

This research question seeks to investigate overlooked or less studied animal species in the context of behavior analysis.

To address this question, the survey will explore existing literature and research to identify trends and biases in the

selection of animal subjects. The objective is to understand why certain species receive less attention and to gain

insights into potential gaps in knowledge, aiding the development of more comprehensive and inclusive research

strategies.

RQ2 What deep learning methods have been used in the literature for animal behavior analysis?

This research question focuses on summarizing and categorizing the existing deep learning methods employed in the

literature for animal behavior analysis. The survey will review a wide range of studies to identify and classify the

various deep learning techniques applied to analyze animal behavior. The objective is to analyze existing methodologies

to identify trends, strengths, and limitations of current approaches in the field.

RQ3 What are the differences between human and animal behavior analysis?

This research question aims to highlight the distinctions between the analysis of human behavior and that of other

animal species. The survey will compare methodologies, ethical considerations, and challenges specific to studying

human and animal behavior.

RQ4 What are the deep learning strategies that are suitable and could enhance this task, but are not yet exploited?

This research question looks forward, aiming to identify untapped potential in the application of deep learning to

animal behavior analysis. The survey will involve a comprehensive review of the current literature to identify gaps or

areas where deep learning strategies have not been extensively explored. This involves proposing novel applications of

existing techniques or suggesting modifications to adapt deep learning methods for more effective analysis of animal

behavior.

3 METHOD FOR LITERATURE SURVEY

In this section, we clarify the methodology applied in our survey. Our approach involved a thorough systematic review

to carefully select the pertinent studies considered in this article. Following this, we accurately analyzed the gathered

information, employing statistical methods to derive meaningful insights.

3.1 Search and selection strategies

This section delineates the methodologies employed for data collection and synthesis. Initially, data acquisition was

conducted through systematic searches on academic repositories, including Google Scholar, IEEE Xplore, and the

Springer Database. The formulated search queries were as follows:

animal behavior AND deep learning

(insect OR wild) AND behavior AND deep learning

The decision to employ distinct queries for insects and wild animals was necessitated by the observed paucity of

literature in these categories relative to studies involving farm animals and neuroethology, commonly focused on mice.

Thus, the formulation of specific queries was imperative to encompass a broader spectrum of animal species.

Subsequently, the acquired data underwent systematic tabulation based on features explicated in Table 2. These

features were derived from discerned patterns identified during a comprehensive analysis of the extant literature.

Synthesizing the outcomes of this analysis, Sections 4 and 5 encapsulate the aggregated findings, summarizing the

respective papers that expound upon solution methodologies grounded in pose estimation and those that do not.

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

7

Finally, a judicious filtering operation was executed to extract only those articles germane to the objectives of

this survey, resulting in 151 articles. Each article within this subset underwent thorough examination, and pertinent

references therein were scrutinized and subsequently incorporated into our survey to enrich its content.

Table 2. Features Extracted from Papers

Reference: Assigned identifier for each retrieved article.
Year: Publication year of the article.
Country: Geographical location where the authors are based, as required in Section 3.2.
Species: The specific species under investigation in the article.
Pose Estimation: Indicates whether the methodology incorporates pose estimation (True or False).
Behavior Analysis: Indicates whether the analysis considers an association between extracted features
and observed behaviors (True or False).
Feature Methodology: The approach employed to extract salient features in the study.
Behavior Methodology: The methodological framework used to correlate features with observed behav-
iors.
Authors’ research field: Indicates the research fields the authors mainly work on.

3.2 Comprehensive science mapping analysis

3.2.1 Annual scientific production. In the process of retrieving articles, our attention was exclusively directed towards

research publications spanning the temporal spectrum from 2020 to 2023. Figure 1a elucidates this distribution through

a histogram, illustrating the quantitative representation of papers across each respective year.

3.2.2

Scientific production based on animal considered. Figure 1b illustrates the distribution of percentages pertaining

to the various animal species under consideration in the selected articles. Evidently, a predominant emphasis is placed

on research concerning livestock, notably focusing on cows and pigs, as well as studies involving mice, related mostly

to neuroscience.

3.2.3 Research field of authors. Given that animal behavior analysis is an interdisciplinary and multidisciplinary field,

it becomes imperative to comprehend the research background of individuals engaged in this domain. Despite the

predominant focus on articles related to deep learning technologies, it is noteworthy that a considerable number

of non-artificial intelligence practitioners are actively entering this field, as illustrated in Figure 1c. Interestingly,

when combining "computer science" (encompassing computer engineering) and "artificial intelligence," they constitute

only 18% of the scholarly contributions. In contrast, bio-related fields, including biology, animal science, agriculture,

veterinary, and ecology, collectively contribute 30% to the research landscape. Noteworthy is the active participation of

various engineering fields, even those with a mechanical-electrical background, in the exploration of animal behavior.

Additionally, a compelling correlation is observed in the fields of neuroscience and psychology, where the majority of

articles are dedicated to the study of mice.

4 POSE ESTIMATION-BASED METHODS

Pose estimation, the process of identifying and locating the position and orientation of objects, is a fundamental

technique widely used in the examination of animal behaviors alongside object detection, as discussed in subsection 5.3.

Originating from Human Pose Estimation (HPE), the evolution into Animal Pose Estimation (APE) was spearheaded by

Mathis et al. through DeepLabCut [122] and Pereira et al. via LEAP [151], subsequently evolving into SLEAP [152].

Manuscript submitted to ACM

8

Fazzari, et al.

Fig. 1. a) illustrates a histogram depicting the distribution of research articles per year, focusing exclusively on papers obtained and
cataloged during the initial scavenging phase. b) presents a pie chart detailing the variety of animals utilized in behavioral studies
leveraging deep learning techniques. c) displays another pie chart showcasing the diverse research fields of the authors.

This section delves into an in-depth analysis of these two methodologies juxtaposed with emerging trends within the

field of research. Given the primary focus of our survey on animal behavior analysis, subsequent to the introduction

of these predominant approaches, we elucidate the utilization of pose estimation outputs for behavior analysis and

classification. For a more comprehensive understanding of animal pose estimation, we recommend perusing the survey

conducted by Jiang et al. [78], published in 2022.

LEAP [151] is a single-animal pose estimation model employing convolutional layers culminating in confidence

maps that delineate the probability distribution for each distinct body keypoint. This architectural design, depicted

in Figure 2, is characterized by its simplicity, featuring three sets of convolutional layers. The initial two sets are

terminated by max pooling to alleviate computational complexity. Subsequently, transposed convolution is applied to

restore the original dimensions of the images, yet with a depth corresponding to the number of keypoints, thereby

Manuscript submitted to ACM

a)2020202120222023 (ongoing)YearsNumber of articles51015202530b)c)FliesCricketsGoatsFishCowsBirdsOtherOtherVeterinaryMechanical Eng.NeuroscienceTechnologyPsychologyPhysicsMathematicsSheepChickensHorsesMiceInsectsPigsEcologyBiologyAgricultureAnimal ScienceArtiﬁcial IntelligenceElectrical EngineeringEngineeringLife SciencesComputer ScienceAnimal Behavior Analysis Methods Using Deep Learning: A Survey

9

generating a confidence map for each. Despite its simplicity, the LEAP model encounters challenges in non-laboratory

settings due to issues such as occlusion, prompting the introduction of T-LEAP [166]. T-LEAP preserves the architecture

of LEAP but diverges in its use of 3D convolution instead of 2D convolution. The input to T-LEAP comprises four

consecutive frames extracted from videos, enhancing the model’s robustness. Notably, T-LEAP maintains a focus on

single-animal pose estimation, as elucidated in Figure 2. Subsequently, the author of LEAP introduced a refined version

known as Social LEAP (SLEAP) [152], designed to proficiently address the challenges associated with multi-animal

pose estimation through the integration of both bottom-up [145] and top-down strategies [138]. In the top-down

strategy, SLEAP first identifies individuals and subsequently detects their respective body parts. Unlike LEAP, SLEAP

seamlessly incorporates this approach without the need for an additional object detection architecture. On the other

hand, the bottom-up strategy in SLEAP involves detecting individual body parts and subsequently grouping them into

individuals based on their connectivity. A key advantage of this dual-strategy framework is its efficiency, requiring

only a single pass through the neural network. The output of this strategy produces multi-part confidence maps and

part affinity fields (PAFs) [34], constituting vector fields that intricately represent spatial relationships between pairs

of body parts. Additionally, SLEAP undergoes a structural enhancement by transitioning from LEAP’s backbone to a

more intricate U-Net architecture [164], thereby significantly improving accuracy in the realm of multi-animal pose

estimation scenarios.

Fig. 2. a) shows the architecture of LEAP [151]; b) the one exploited in T-LEAP [166]

Similarly, DeepLabCut (DLC) [122] has evolved significantly over time. Initially designed as a single-animal pose

estimation method, it utilizes a pretrained ResNet-50 [70] backbone with subsequent deconvolutional layers to generate

confidence maps for keypoints. This approach, taking advantage of Imagenet pretrained weights, allowed DLC to

effectively estimate skeletons with minimal data. The model’s capabilities were later expanded to include 3D pose

estimation through the use of multiple cameras [135]. Each camera view was trained independently, and sophisticated

camera calibration techniques were employed to derive 3D locations. A subsequent milestone in DLC’s development

involved addressing the challenges of multi-animal pose estimation [98]. This evolution introduced DLCRNet, a structural

modification that replaced the ResNet backbone. DLCRNet employs a bottom-up multi-animal pose estimation approach,

featuring a multi-fusion architecture and a multi-stage decoder. The decoder utilizes multiple stages of score maps

and PAFs [34] to predict keypoints for each animal. Further innovation is exemplified by SuperAnimal [205], which

introduced transformer layers into the model architecture.

While DLC [122] and SLEAP [152] currently stand as the predominant pose estimation methodologies in behavior

analysis for animal behavior classification, it is imperative to acknowledge recent advancements in animal pose

estimation architectures. Several notable methodologies have been introduced:

Manuscript submitted to ACM

Input Imageh x w x 3Conv643 x 31 x 1Pool2 x 22 x 2Conv1283 x 31 x 1Pool2 x 22 x 2Conv2563 x 31 x 1Pool2 x 22 x 2Conv5123 x 31 x 1TConv2563 x 32 x 2Conv2563 x 31 x 1TConv1283 x 32 x 2Conv1283 x 31 x 1TConvk3 x 32 x 2Confidence mapsh x w x kEncoderDecoderInput sequencet x h x w x 3EncoderConv3d643x3x31x1x1Pool3Dt/2x2x2t/2x2x2Conv3d1283x3x31x1x1Pool3D2x2x22x2x2Conv3d2563x3x31x1x1Pool3D1x2x21x2x2Conv3d5121x3x31x1x1DecoderTConv3d641x3x31x2x2Conv3d2561x3x31x1x1TConv3d641x3x31x2x2Conv3d1281x3x31x1x1TConv3dk1x3x31x2x2Confidence mapsh x w x ka)b)10

Fazzari, et al.

• OptiFlex [110] is a video-based animal pose estimation method that, given a skip ratio 𝑠 and a frame range 𝑓 ,
assembles a sequence of 2𝑓 + 1 images with indices ranging from 𝑡 − 𝑠 × 𝑓 to 𝑡 + 𝑠 × 𝑓 . This sequence is input
to a model based on residual blocks with intermediate supervision, generating predictions for each image and

producing a sequence of heatmap tensors. These tensors are then fed into an OpticalFlow model, ultimately
yielding the final heatmap prediction for index 𝑡. OptiFlex has demonstrated superior accuracy compared to
DeepLabCut [122], LEAP [151], and DeepPoseKit [64].

• SemiMultiPose [23] introduces a semi-supervised multi-animal pose estimation approach, building upon
DeepGraphPose [195] and DirectPose [183]. Taking both labeled and unlabeled frames as input, the method

processes them using a ResNet [70] backbone, generating a compact representation fed into three branches: one

for detecting keypoint heatmaps (B1), one for bounding box heatmaps (B2), and a third for keypoint detection

(B3). SemiMultiPose aims to generate pseudo keypoint coordinates from B2 and B3 for the self-supervised

branch, contributing to B1. The network has shown improved accuracy compared to SLEAP [152]. However, the

authors note that in cases of abundant labeled data, their method may not significantly outperform others, and

for single-animal pose estimation with unlabeled frames from a sequential video, DeepGraphPose [195] might

outperform SemiMultiPose [23], benefiting from the consideration of spatial and temporal information.

• Lightning Pose [21] exploits spatiotemporal statistics of unlabeled videos in two ways. Firstly, it introduces
unsupervised training objectives penalizing the network for predictions violating the smoothness of physical

motion, multiple-view geometry, or departing from a low-dimensional subspace of plausible body configurations.

Secondly, it proposes a novel network architecture predicting poses for a given frame using temporal context

from surrounding unlabeled frames. The resulting pose estimation networks exhibit superior performance with

fewer labels, generalize effectively to unseen videos, and provide smoother and more reliable pose trajectories

for downstream analysis (e.g., neural decoding analyses) compared to previously mentioned approaches.

• Bhattacharya et al. [20] introduced a novel model for recognizing the pose of multiple animals from unlabeled
data. The approach involves the removal of background information from each image and the application of an

edge detection algorithm to the body of the animal. Subsequently, the motion of the edge pixels is tracked, and

agglomerative clustering is performed to segment body parts. In a departure from previous methods, the end

result is not specific keypoints but rather the segmentation of body parts. To achieve this, the authors utilized

contrastive learning to discourage the grouping of distant body parts together.

After obtaining the skeletal representation of each animal in every frame, whether from videos or images, the

subsequent step involves processing the data to discern specific behaviors. The trajectories derived from pose estimation

can be effectively analyzed through statistical methods. Weber et al. [191] utilized DeepLabCut predictions [122] and

ANOVA [87] to conduct behavioral profiling of rodents, with a focus on studying stroke recovery. In a similar vein, Lee

et al. [101], employing DLC [122], investigated the behavior of non-tethered fruit flies. Their study involved predicting

locomotion patterns and identifying the centroid of the animals’ legs.

Machine learning for analyzing pose estimation trajectories becomes crucial when classifying postures and relating

them to specific behaviors. One of the simplest approaches is to use a Nearest-Neighbor classifier. Saleh et al. [168]

tested this method to classify mouse behaviors such as crossing and rearing in an open-field experiment, achieving 97%

accuracy. Other machine learning approaches were employed by Fang et al. [53] and Nilsson et al. [139]. The former used

a naive Bayesian classifier to identify eating, preening, resting, walking, standing, and running behaviors for poultry

analysis, providing a disease warning system. The latter introduced the SimBa toolkit, importing DeepLabCut [122] or

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

11

DeepPoseKit [64] projects to create classifiers using RandomForest [28] and extracting features like velocities and total

movements. McKenzie-Smith et al. [125] used trajectories obtained with SLEAP [152] to identify stereotyped behaviors

such as grooming, proboscis extension, and locomotion in Drosophila melanogaster, using resulting ethograms provided

by MotionMapper [18] to explore how flies’ behavior varies across time of day and days, finding distinct circadian

patterns in all stereotyped behaviors.

Other authors opted for recurrent and convolutional neural networks, with simple approaches such as using Long

Short-Term Memory (LSTM) [72] and 1D convolutional neural networks to process trajectories for drawing behavioral

conclusions. Examples include detecting lameness in horses [4] and determining chemical interactions experienced

by crickets [54]. More complex approaches include Wittek et al. [193]’s use of InceptionTime [76], an ensemble of

deep convolutional neural network models, to classify seven distinct behaviors in birds. Some authors simplified

the classification process by introducing a non-linear clustering phase to improve the feature space, followed by

classification using Multilayer Perceptrons (MLP), demonstrating advantages in classification [171, 205].

A recent emerging trend involves the utilization of unsupervised learning techniques in the analysis of animal behavior.

Luxer et al. [113] have innovatively proposed a methodology for processing trajectories derived from DeepLabCut [122]

by employing a Variational Auto-Encoder (VAE) [89]. Subsequently, they apply a Hidden Markov Model (HMM) [157]

to the new representation of trajectories to discern underlying motifs. Following a comprehensive analysis of motif

usage, the authors iteratively employ HMM, limiting the number of motifs to those surpassing a 1% usage threshold in

the previous analysis. The refined motifs were attributed to specific behavior exhibited by the mice, such as exploration,

rearing, grooming, pausing, or walking. Notably, this methodological approach outperforms conventional techniques,

such as Auto-Regressive HMM (AR-HMM) or MotionMapper [18], when applied directly to the motion sequences.

Motion trajectories extend their utility beyond predicting the behavior of individual animals; in multi-animal scenarios,

they can also be applied to unravel the intricate web of social interactions among them. Segalin et al. [172] introduced

the Mouse Action Recognition System (MARS), a sophisticated automated pipeline tailored for pose estimation and

behavior quantification in pairs of freely interacting mice. MARS adeptly discerns three specific social behaviors: close

investigation, mounting, and attack. On a different note, Zhou et al. [209] proposed the Cross-Skeleton Interaction

Graph Aggregation Network (CS-IGANet), a groundbreaking framework designed to capture the diverse dynamics of

freely interacting mice. CS-IGANet successfully identifies a spectrum of behaviors, including approaching, attacking,

chasing, copulation, walking away from another mouse, sniffing, and many others.

Trajectories not only serve as a means to identify specific behaviors but are also instrumental in anomaly detection.

For instance, Fujimori et al. [59] employed OneClassSVM [26] and IsolationForest [109] to detect outlier behaviors

in domestic cats. Similarly, Gnanasekar et al. [60] utilized pose estimation data to predict abnormal behavior in mice

undergoing opioid withdrawal, employing pretrained convolutional neural networks for the classification of shaking

behaviors.

5 NON POSE ESTIMATION-BASED METHODS

In this section, we expound upon methodologies employed in the investigation of animal behaviors without recourse

to pose estimation techniques. To enhance clarity and systematic presentation, we have delineated subsections corre-

sponding to each methodology.

Manuscript submitted to ACM

12

5.1 Sensor based approaches

Fazzari, et al.

Sensor-generated data, typically originating from accelerometers or gyroscopes, has been extensively explored in

the literature, as comprehensively in [91, 136] surveys. These surveys delve into the application of classical machine

learning methods in modern animal farming and the study of animal behavior. More recently, a shift towards leveraging

deep learning approaches has been observed. Arablouei et al. [8] utilized a wearable collar tag equipped with an

accelerometer to collect data from grazing beef cattle. They applied a Multi-Layer Perceptron to classify behaviors such

as grazing, walking, ruminating, resting, and drinking. Similarly, Eerdekens et al. [49] employed tri-axial accelerometers

on horses, strategically positioned at the two front legs’ lateral side. They proposed a Convolutional Neural Network to

detect behaviors like standing, walking, trotting, cantering, rolling, pawing, and flank-watching based on the acquired

data. Mekruksavanich et al. [126], instead, segmented accelerometer data into 2-second windows and exploited a

pre-trained ResNet model [70] to perform sheep activity recognition. Dang et al. [46] introduced the integration of

multiple sensors, collecting environmental data (e.g., temperature, humidity) alongside cow behavior information

obtained from accelerometers and gyroscopes. They preprocessed this information using a 1D-convolutional neural

network and LSTM networks for classifying walking, feeding, lying, and standing. In a recent study, Pan et al. [144]

introduced four novel Convolutional Neural Network architectures tailored for Animal Action Recognition (AAR).

These architectures, namely one-channel temporal (OCT), one-channel spatial (OCS), OCT and spatial (OCTS), and

two-channel temporal and spatial (TCTS) networks, leverage data from 3D accelerometers and 3D gyroscopes. The

core objective of their research was to mscrupulously identify behaviors such as movement, drinking, eating, nursing,

sleeping, and lying in lactating sows.

In addition to accelerometer and gyroscope data, GNSS (Global Navigation Satellite System) data emerges as a

valuable tool for understanding animal behavior. Arablouei et al. [9] explored this avenue by employing GNSS to

extract pertinent information about cattle behavior, including metrics like distance from water points, median speed,

and median estimated horizontal position error. Integrating this GNSS data with accelerometry information, the

researchers pursued two distinct approaches. The first involved concatenating features from both sensor datasets into a

comprehensive feature vector, subsequently fed into a MLP classifier. Alternatively, the second approach centered on

fusing the posterior probabilities predicted by two separate MLP classifiers. These methodologies enabled the accurate

detection of behaviors such as grazing, walking, resting, and drinking.

5.2 Bioacoustics

While bioacoustics offers a captivating glimpse into animal behavior [177], given the integral role of sound in animal

activities such as communication, mating, navigation, and territorial defense [35], the current landscape of published

articles predominantly emphasizes animal identification [27, 187, 198] and sound event detection [133, 140]. Notably, the

existing literature reveals a scarcity of research endeavors combining acoustics and deep learning for the identification

of animal behaviors. Wang et al. [189] stand out as pioneers in this domain, as they endeavored to classify sheep

behaviors, including chewing, biting, chewing-biting, and ruminating sounds. This was accomplished using a recording

device positioned proximal to the animal’s face, with a placebo class designated as noise. The acquired wavelet data

were leveraged for classification tasks through both a feed-forward neural network and a recurrent neural network.

Additionally, the information was further processed by transforming it into a log-scaled Mel-spectrogram, serving as

input for a convolutional neural network. The findings underscore that while the recurrent neural network exhibited

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

13

superior performance, the convolutional neural network outperformed the feed-forward approach, attributing its

success to the enhanced signal representation offered by the Mel-spectrogram.

5.3 Object Detection

In conjunction with pose estimation techniques, object detection stands out as a widely employed deep learning

methodology for analyzing animal behavior. Its prevalence may be attributed to its established utility in animal

recognition and detection [12, 37, 181], prompting researchers to redirect their focus toward studying animal welfare

and activity.

Among the leading architectures for animal behavior identification, Faster R-CNN [160] and particularly YOLO [159]

are frequently employed. Nonetheless, alternative architectures have been proposed. For instance, Samsudin et al. [169]

utilized SSD MobileNetv2 [170] to detect abnormal and normal zebrafish larvae behaviors for examining the effects of

neurotoxins. McIntosh et al. [124] introduced TempNet, incorporating an encoder bridge and residual blocks with a

two-staged spatial-temporal encoder, to detect startle event in fish.

Object detection serves a dual role, encompassing instantaneous behavior detection through image or video frame

analysis, as well as the quantification and tracking of specific behaviors. The accurate analysis of single frames, counting,

and frame-by-frame examination enable researchers to quantify both the duration and frequency of distinct actions. For

instance, the application of YOLO in the study by Alameer et al. [5] facilitated the quantification of contact frequency

among pigs, allowing the identification of peculiar behaviors such as rear snorting and tail-biting. In the context of

cows and pigs, a crucial aspect involves quantifying movement and aggressive behavior [5, 141]. Furthermore, efforts to

discern rank relationships based on fighting behavior in animals like cows are of crucial importance [185]. Importantly,

for tasks demanding prolonged animal identification, tracking is conventionally executed using DeepSort [51, 194].

Efficient instant detection can be accomplished by conducting a single analysis on the animal and directly classifying

its behavior through a single image. In this context, deep learning object detection models prove instrumental in directly

identifying behaviors such as positional activities (e.g., mating, standing, feeding, spreading, fighting, drinking) for the

comprehensive analysis of animal health and stress behaviors [117, 161, 188]. These models also find application in disease

identification, such as the detection of wryneck [50], and in studying behavioral adaptations to new environments [105].

Furthermore, object detection models can be extended to operate with thermal and infrared images. For example, Xudong

et al. [201] utilized thermal images for the automatic recognition of dairy cow mastitis, introducing the EFMYOLOv3

model. Similarly, Lei et al. employed infrared images to discern feeding, resting, moving, and socializing behaviors in

slow animals [102].

Beyond these applications, notable approaches utilizing object detection include Fuentes et al. [58], who integrated

YOLO and Optical Flow to detect actions in cows. Additionally, some researchers employ object detection solely

for localizing the animal within the image or video. They subsequently crop that region and use it in other models,

leveraging 2D pretrained networks or introducing 3D convolutional neural networks for video analysis [57, 182].

5.4 Others

Several research endeavors have employed unique deep learning methodologies, distinct from those discussed in the

preceding section. Due to the relative scarcity of deep learning strategies for evaluating animal behavior in the existing

literature using the aforementioned approaches, we endeavored to compile a comprehensive assortment of ideas. To

achieve this, we have identified and categorized five distinct approaches:

Manuscript submitted to ACM

14

Fazzari, et al.

• Convolutional Classification on Raw Data. Alameer et al. [6] employed a GoogLeNet-like architecture[178] to
discern between feeding and non-nutritive visits to a manger in pig recordings. In a similar vein, Ayadi et al. [11]

utilized VGG19 [176] to determine whether cows were ruminating or not. This network architecture was also

applied to identify various behaviors in mice, such as grooming, licking the abdomen, squatting, resting, circling,

wandering, climbing, and searching [190]. Similarly leveraging pre-trained networks, Andresen et al. [7] developed

a fully automated system for surveilling post-surgical and post-anesthetic effects in mice facial expressions,

employing InceptionV3 [179] for pain identification. Notably, Bohnslav et al. [25] introduced DeepEthogram, a

software tested for predicting mice and flies behaviors. The approach involves using a sequence of 11 frames,

where the last frame is the target for prediction. Optical flow frames are generated using MotionNet [210]. These

frames, along with the target frame, are fed into a feature extractor (ResNet architectures [67, 70]) to extract

both flow and spatial features. Subsequently, the features are concatenated, and Temporal Guassian Mixture

(TGM) model [155] is applied for classification. Han et al. [66] employed a simpler approach, superimposing the

frame to be predicted with computationally generated optical flow from the subsequent frame. The resulting

image is then classified using a convolutional neural network to categorize behaviors in fish shoals, including

normal state, group stimulated, individual disturbed, feeding, anoxic, and starvation state.

• Segmentation. Xiao et al.[197] employed Mask R-CNN [69] to segment birds within a 3D space, facilitating
the analysis of their interactions based on distinct social actions: approach, stay, leave, and sing to. In contrast,

other researchers have devised innovative pipelines to investigate animal behavior. EthoFlow[19] is a software

grounded in segmentation, enabling the tracking and behavioral analysis of organisms (validated on bee datasets).

On a different note, SIPEC [118] constitutes a pipeline leveraging an Xception network [42] to extract features

from frames. These features are subsequently processed over time using a Temporal Convolutional Network

(TCN) [99] to classify the animal’s behavior in each frame. While SIPEC abstains from segmentation in the case

of single animal classification, it seamlessly incorporates segmentation for multi-animal behavior classification.
• Self-Supervised Learning. Jia et al. [77] proposed an innovative self-supervised learning approach known as
Selfee, designed for extracting comprehensive and discriminative features directly from raw video recordings

of animal behaviors. Selfee utilizes a pair of Siamese convolutional neural networks[93], trained explicitly to

generate discriminative representations for live frames.

• Explainability. To the best of our knowledge, Choi et al. [40] stands as the sole contributor employing Explainable
Artificial Intelligence (XAI). In their study, they harnessed Grad-CAM [173] to delve into the decision-making

process of a neural network designed to distinguish between unstable and stable ant swarms. The investigation

aimed to ascertain the network’s capacity to comprehend intricate behaviors such as dueling and dominance

biting, shedding light on the explainability of its predictions.

• Behavior identification in clips. Li et al. [104] undertook the task of categorizing significant pig behaviors,
such as feeding, lying, motoring, scratching, and mounting. Their approach involved the development of Pig’s

Multi-Behavior recognition (PMB-SCN), a sophisticated architecture built upon the SlowFast framework [56]

and leveraging spatio-temporal convolution. PMB-SCN comprised two distinct SlowFast pathways with varying

temporal speeds. The slow pathway utilized a larger temporal stride when processing input frames (e.g., 8,

considering a clip with a length of 64 frames), while the fast pathway employed a smaller temporal stride (e.g., 2).

The features extracted by these pathways were interconnected through lateral connections [108], enhancing

the model’s ability to capture complex spatio-temporal patterns. The final phase of the methodology involved

classification, where the fused features were utilized to discern and categorize various pig behaviors effectively.

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

15

6 PUBLICLY AVAILABLE DATASETS

This section meticulously enumerates publicly accessible datasets featured or referenced in the articles identified

through our systematic search. Table 3 presents details on each dataset, including the article of introduction, authorship,

targeted species, data type (e.g., images, videos, audio signals, sensor data), the specific tasks for which they were

utilized and the content of the datasets. Noteworthy is the incorporation of references indicating the dual usage of

datasets—initially introduced for a specific task and subsequently repurposed, signified by citations in the Application

column. Regrettably, several articles utilized private datasets, although some authors may offer dataset-sharing options.

We recommend consulting the corresponding articles to explore potential data access avenues.

A number of key considerations can be gleaned from Table 3, as follows:

• In the context of datasets tailored for pose estimation, a salient observation is the standardization of skeletal
structures when deployed across diverse animal species [32, 137, 206]. This standardization facilitates the training

of a singular network, avoiding the need for species-specific networks. Conversely, datasets exclusive to individual

animal species exhibit intricate skeletal configurations tailored to the anatomical nuances of that species. For

instance, precision in detecting the distal and proximal ends of crickets’ antennae may be achievable [55], but

such granularity may not translate to not insect species like horses.

• The inclination of animals like goats and birds to move in open fields compels researchers to rely on sensor data
or alternative methods, such as audio recordings, for event and action detection. This approach is significantly

more manageable than tracking the animals with cameras. However, the utilization of sensors is constrained by

the availability and affordability of these devices, directly impacting the number of individuals involved and the

quantity of sequences that can be compiled for the dataset.

• For identifying static positions, such as whether an animal is lying down or standing, still images suffice. However,
capturing and analyzing videos, or more precisely, short video clips, is crucial for recognizing dynamic actions

and behaviors. These clips are intentionally brief to focus solely on the relevant action event, ensuring accurate

classification using deep learning techniques. This approach effectively eliminates extraneous or unrelated

behaviors that may interfere with the identification of the specific behavioral instance. This is the rationale

behind Yang et al.’s decision to utilize 15 frames for each video clip [204].

• Unfortunately, publicly available collective and social behavior prediction and analysis datasets are currently
limited to mice and fish, even though we discussed a study in this survey that utilized explainable artificial

intelligence to analyze ant behavior. This innovative research methodology relies heavily on video data, pre-

senting a computational challenge that demands substantial processing efforts. The intricate nature of this

approach necessitates a considerable investment of time for meticulous frame and event labeling, thereby slightly

diminishing its overall research appeal and popularity.

• An essential consideration pertains to the primary focus of many databases, which primarily aim at identification,
detection, pose estimation, and tracking. Despite this orientation, it is crucial to acknowledge that several datasets

have been instrumental in behavioral analysis, even if not explicitly designed for such purposes. Researchers are

strongly encouraged not to overlook animal datasets merely because they do not pertain to specific behaviors.

Valuable insights can be gleaned from these datasets, and their broader applicability should be explored beyond

their initially intended scope.

Manuscript submitted to ACM

16

Fazzari, et al.

Table 3. Datasets Information useful for Animal Behavior Analysis

Species

Introduced by

Type

Applications

Dimensions

Akçay [2]
Birds
Morfi et al. [131]
Birds
Knight et al. [92]
Birds
Shamoun-Baranes et al. [174]
Birds
Arablouei et al. [9]
Cattle
Barnard et al. [14]
Dogs
Kamminga et al. [84]
Goats
Kleanthous et al. [90]
Goats
Kamminga et al. [85]
Horses
Mathis et al. [121]
Horses
Mathis et al. [122]
Fish
McIntosh et al. [124]
Fish
Papaspyros et al. [146]
Fish
Rahman et al. [158]
Fish
Tucker et al. [184]
Fish
Bjerge et al. [22]
Insects
Fazzari et al. [54]
Insects
Modlmeier et al. [129]
Insects
Pereira et al. [152]
Insects
Pham et al. [154]
Insects
Ullah et al. [186]
Insects
Martin et al. [120]
Jellyfish
Burgos et al. [31]
Mice
Jiang et al. [81]
Mice
Jiang et al. [80]
Mice
Mathis et al. [122]
Mice
Pereira et al. [152]
Mice
Segalin et al. [172]
Mice
Cao et al. [32]
Multiple, 5
Yang et al. [204]
Multiple, 30
Multiple, 54
Yu et al. [206]
Multiple, 850 Ng et al. [137]
Pigs
Tigers
Monkeys

Rielert et al. [161]
Li et al. [106]
Labuguen et al. [96]

Images
Audio
Audio
Sensor data
Sensor data
Images
Sensor data
Sensor data
Videos
Images
Videos
Videos
Videos
Videos
Videos
Images
Videos
Images
Videos
Sequences
Images
Images
Videos
Videos
Videos
Videos
Videos
Videos
Images
Images/Videos
Images
Images/Videos
Images
Images
Images

Detection
Recognition [27]
Event detection [112]
Movement prediction [192]
Behavior classification
Pose Estimation
Action recognition (also [24])
Action recognition (also [24, 126])
Pose estimation, Action recognition [24]
Pose Estimation
Pose estimation
Behavior classification
Collective Behavior Prediction
Action recognition [62]
Tracking, Chemical response analysis [62]
Detection
Tracking, Chemical response analysis
Movement prediction [192]
Pose estimation
Locomotion classification
Recognition
Detection
Pose estimation, Social behavior analysis [81]
Social behavior analysis
Detection, Tracking
Pose estimation
Pose estimation
Pose estimation, Behavior classification
Pose Estimation
Pose Estimation
Pose Estimation
Pose Estimation, Action recognition
Position classification
Pose estimation
Pose estimation

3436 images
687 recording, 87 classes
64 recording, 5 classes
19 sequences
11962 labeled datapoints (arm20c), 10879 labeled datapoints (arm20e)
22479 images
177.8 hours of sequence data, 5 individuals
2 sequences
8144 frames
608550 images
100 frames
892 clips
three 16-hour trajectory datasets
95 clips
3 hours for each of the 384 individuals
29960 images
5 minutes clip for 69 individuals
14400 frames (4 hours)
30 videos, 2000 labels
258 traces
1686 images
842 images
237 videos and over 8M frames
12*3 annotated videos, 216,000*3 frames in total
10 videos, each video lasts 3 min, 4000 frames annotated
161 frames
1000 frames, 2950 instances & 1474 frames, 2948 instances
3.3M labels for pose annotation, 14 hours of behavior annotation
4666 images
2.4K video clips with 15 frames for each video, resulting in 36K frames
10015 images
50 hours of annotated videos, 30K video sequences for AAR, 33K frames for APE
7277 images
8076 images
13083 images

7 DISCUSSION ABOUT RESEARCH QUESTIONS

In concluding our extensive survey, we undertake the task of responding to the research questions outlined in subsec-

tion 2.3, drawing upon the insights gleaned from the studies expounded upon earlier. These responses aim to offer

readers practical guidance in navigating the dynamic trends discerned from the comprehensive examination of the

state-of-the-art literature. Their purpose is to serve as a compass for readers, facilitating a deeper comprehension of

emerging patterns and fostering the implementation of advancements in the field of animal behavior.

RQ1 (Which animal species are less considered and why?): In the context of animal behavior analysis employing

deep learning, farm animals take center stage, as illustrated in Figure 1. Pigs and cows emerge as prominent subjects,

while mice claim a noteworthy position owing to their significance in neuroscience research [30]. Despite chickens

being the most widely farmed animals globally, surpassing even cows, sheep, and goats [162], their consideration in

behavior analysis appears relatively subdued. This discrepancy may be attributed to the limited nature of chicken

behavior, encompassing mostly activities such as sleeping, moving, and eating. They are predominantly analyzed for

welfare-related assessments [82, 130].

Goats and sheep, less scrutinized in behavioral studies, likely owe their lower visibility to their outdoor grazing habits,

which hinder the feasibility of employing image processing techniques. Unlike pigs, which are often studied within

confined spaces, the vast open areas in which goats and sheep are typically raised limit the practicality of utilizing

image processing, even with occasional drone deployment [3]. Birds face a similar challenge, requiring continuous

tracking or data collection from sensors for comprehensive analysis [17].

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

17

For aquatic creatures like fishes, a distinct hurdle arises from the difficulty in training neural networks on underwater

images. These images often suffer from poor quality due to distortion and color/contrast loss in water, necessitating an

image enhancement phase for meaningful analysis [167].

A notable observation is the limited consideration given to domestic animals in this research context [36, 41, 86, 100].

This may stem from the scarcity of veterinary professionals engaged in this evolving field or ethical concerns surrounding

the study of domestic animals.

RQ2 (What deep learning methods have been used in the literature for animal behavior analysis?):

Throughout this survey, we delineate two distinct methodologies employed for the analysis of animal behaviors: pose

estimation and non-pose estimation methods. Pose estimation-based approaches hinge on the analysis of trajectories

traced by keypoints, with subsequent utilization of various machine and deep learning techniques to scrutinize behavior.

Predominantly, recurrent neural networks and 1D convolutional neural networks are the favored deep learning methods,

though recent applications have also embraced variational auto-encoders for unsupervised motif identification [89, 113]

and convolutional graph networks for interaction analysis [209]. However, a prevalent trend emerges wherein data is

often processed through statistical analysis or traditional machine learning methods [53, 125, 139, 168]. This inclination

may stem from the fact that many researchers are not inherently engaged in artificial intelligence or data science, as

mentioned earlier (see subsection 3.2), or it could be influenced by the volume of available data, given the heightened

data requirements of deep learning [143]. Despite the migration of classification tasks and behavior discovery to

deep learning, certain aspects, such as behavior outlier detection, persist in employing classical machine learning

approaches like OneClassSVM [26] and IsolationForest [109]. On the other hand, non-pose estimation encompasses

diverse applications, categorized based on the type of data: sensors, audio and video, and image data. Sensor data

commonly undergoes processing through (1D)-convolutional or recurrent neural networks [46, 49, 126, 144], and in

some cases, multi-layer perceptron classifiers [8], particularly when sensor data is transformed into features like velocity,

angles, humidity, location, among others [9]. In the domain of bioacoustics, recurrent neural networks or pre-trained

convolutional neural networks on spectrogram images are frequently applied [189]. For images and videos, processing

methods vary according to the task at hand. They may be employed for object detection, where identification extends

beyond the animal to encompass specific behaviors, typically achieved through frameworks such as YOLO [159] and

Faster R-CNN [160]. Alternatively, pre-trained neural networks or segmentation techniques, with subsequent analysis

of the segmentation mask, are utilized [197]. Figure 3 and Figure 4 encapsulate and illustrate the summarized pose and

non-pose estimation methods for behavior analysis expounded in this survey.

RQ3 (What are the differences between human and animal behavior analysis?): Deep learning for animal

behavior analysis draws inspiration from and translates methodologies used in human applications. While similarities

exist in predicting final classification outputs, notable differences emerge in data handling, particularly with sensor data.

Moreover, a distinct gap is evident in pose estimation methods. In the following list, we highlight these divergences

that present opportunities for leveraging deep learning in animal behavior analysis:

• Pose estimation (regression). In animal pose estimation, regression-based methodologies have not garnered
widespread acclaim as observed in human applications. This divergence in popularity can likely be attributed to

their utilization predating the ascendancy of heatmap-based techniques [208]. Conversely, within the human

context, these regression approaches have demonstrated noteworthy success, particularly when seamlessly

integrated with multi-task learning techniques [165]. By facilitating the exchange of information between

interconnected tasks, such as pose estimation and pose-based action recognition, models can enhance their

Manuscript submitted to ACM

18

Fazzari, et al.

Fig. 3. Comprehensive schema illustrating the pose estimation architectures covered in this survey, accompanied by detailed
methodologies for accurate classification of predictions into distinct behavioral classes.

Fig. 4. Comprehensive schema illustrating the non-pose estimation architectures covered in this survey. To improve readability we
divided them into blocks using the same structure employed in the survey.

generalization capabilities. For example, Fan et al. [52] introduced an innovative dual-source convolutional neural

network, employing both image patches and complete images for two distinct tasks: joint detection, responsible

for discerning whether a patch contains a body joint, and joint localization, aimed at pinpointing the precise

location of the joint within the patch. Each task is associated with its dedicated loss function, and the synergistic

combination of these tasks yields notable improvements in overall performance.

Manuscript submitted to ACM

Pose EstimationLEAPSLEAPT-LEAPDeepLabCutOptiFlexSemiMultiPoseLightning PoseArchitecturesPredictions are input toStatistical Analysis (e.g. ANOVA)Nearest-NeighborsClassifierNaive BayesianClassifierSimBatoolkitMotionMapperMulti LayerPerceptronRecurrent Neural Networks (e.g., LSTM)1D Convolutional Neural Networks(AR-)Hidden Markov ModelVariational Auto-Encoder (VAE)Mouse Action Recognition System (MARS)Cross-Skeleton Interaction Graph Aggregation NetworkOneClassSVMIsolationForestNon Pose EstimationMulti-Layer PerceptronOne\Two-Channel Temporal/Spatial/bothSensors-basedRecurrent Neural NetworksConvolutional Neural Networks on Mel-SpectrogramBioacousticYOLOFaster R-CNNSSD MobileNetv2TempNetEFMYOLOv3Object DetectionVGGConvolutional on Raw DataMask R-CNNSegmentationSelfeeSelf-Supervised LearningGrad-CAMExplainabilityPig’s Multi-Behavior Recognition (PMB-SCN)Using ClipsEthoFlowSIPECGoogLeNetInceptionV3DeepEthogramTemporal Gaussian Mixture (TGM)(1D-)Convolutional Neural Networks (e.g ResNet)Animal Behavior Analysis Methods Using Deep Learning: A Survey

19

• Pose estimation (heatmap). While these approaches find application in the realm of animal behavior, we
believe that leveraging the following methods employed in human pose estimation could significantly augment

this field:

Using pre-trained an general models based on transformers. Xu et al. [200] introduced VitPose++, an extension

of the VitPose model [199], specifically designed for generic body pose estimation. This innovative framework

utilizes vision transformers and distinguishes itself by not only focusing on human subjects but also extending its

application to animals. The training process incorporates the AP-10K [? ] and APT36K [204] datasets, ensuring a

comprehensive understanding of both human and animal poses. We believe that fine-tuning pre-trained models

of this kind may improve animal pose estimation results.

Using Generative Adversarial Networks (GANs) [61]. The benefit can be twofold. GANs are explored in human

pose estimation to generate biologically plausible pose configurations and to discriminate the predictions with

high confidence from those with low confidence, which could infer the poses of the occluded body parts [39, 43]. A

valuable aspect that could be used also in our task, solving possible occlusion issue in open-field research. Another

usage is to perform adversarial data augmentation treating the pose estimation network as a discriminator and

using augmentation networks as a generator to perform adversarial augmentations [150].

• Smart handling of sensor data. The significance of detecting human behaviors through sensor technologies
has grown significantly in recent years [71, 75, 147]. This has prompted researchers to critically evaluate the

relevance of various sensors employed in behavior classification through deep learning techniques. The central

question revolves around the necessity of each sensor in contributing to accurate behavior identification and

whether a contribution significance analysis can be effectively employed in this context. Addressing this concern,

Li et al. [107] introduced a novel method aimed at optimizing sensor selection. Their approach involves assessing
the self-information brought by the jth sensor concerning the occurrence of a specific activity 𝐴𝑖 and multiplying
it by the universality of the same sensor j during instances of the same activity 𝐴𝑖 . This innovative strategy
proved to be highly effective, resulting in improved recognition rates and reduced time consumption, thanks to

the elimination of redundant and noisy data.

• Quantifying data scarcity. As highlighted in the limitations section (refer to subsection 2.1), the collection
of behavior data is frequently a laborious and resource-intensive process. Consequently, estimating dataset

size has garnered attention in the field of Human Action Recognition (HAR) as an integral component of data

collection planning. The objective is to mitigate the time and effort invested in behavior data collection while

ensuring precise estimates of model parameters. For example, Hossain et al. [73] introduced a method grounded

in Uncertainty Quantification (UQ) [1] to determine the optimal amount of behavior data required for obtaining

accurate estimates of model parameters when modeling human behaviors as a Markov Decision Process [15].

Technologies of this nature have the potential to expedite research endeavors by facilitating more efficient

workflows.

RQ4 (What are the deep learning strategies that are suitable and could enhance this task, but are not yet

exploited?): Exploring animal behavior through deep learning is just one facet of the multifaceted study in ethology

and neuroscience. Beyond mere identification, understanding the decision-making processes and the emergence of

new behaviors in animals is of paramount importance [95]. This survey focuses on methodologies primarily centered

around detecting behavioral classes or, in the case of unsupervised learning, identifying behavioral motifs. These motifs

are then grouped into behavioral classes based on similarity, often with the assistance of human experts. However,

Manuscript submitted to ACM

20

Fazzari, et al.

animals, much like humans, exhibit dynamic changes in their behavior over time There is a growing need for methods

that can efficiently capture these trial-to-trial changes, breaking them down into a learning component and a noise

component [10]. This is where reinforcement learning plays a pivotal role. Not only does it allow the perception of shifts

in animal behavior and provide examples of biological learning algorithms, but it also enables the emulation of animal

movements. This emulation has given rise to digital twins [111], providing a valuable tool for a more comprehensive

study of animal behavior thanks to the ease of data acquisition. The convergence of deep learning strategies and

reinforcement learning opens up exciting possibilities, paving the way for the development of interactive simulacra of

animal behavior, akin to advancements already achieved in human behavior studies [148]. This innovative approach

empowers researchers to simulate how animals might adapt their behavior in diverse environments while interacting

with various agents, be they other animals, humans, or even robots [132, 163, 203]. Ultimately, the fusion of deep

learning and reinforcement learning holds the promise of creating dynamic, interactive simulations that significantly

deepen our understanding of the nuances of animal behavior across a spectrum of contexts.

8 CONCLUSIONS

In summary, this survey rigorously examined the manifold benefits associated with the application of deep learning

methodologies in the identification of animal behavior. Commencing with a detailed elucidation of the underlying

motivations, limitations, objectives, and pertinent research inquiries steering the integration of deep learning within

this domain, we established a robust contextual framework. Subsequently, our scrutiny extended to a thorough review

of contemporary techniques, systematically categorized into pose and non-pose estimation methodologies. Within these

delineations, we expounded upon a spectrum of methodologies, encompassing sequence processing in pose estimation

and biocoustics, direct classification utilizing convolutional neural networks, outliers detection, convolutional graph

neural networks, object detection, segmentation strategies, self-supervised learning, explainability, and unsupervised

learning. Moreover, we curated a comprehensive table of publicly available datasets relevant to animal behavior,

thereby augmenting the practical utility of deep learning applications. Our discourse on the subject and prospective

considerations has pinpointed extant challenges within the literature, proffering a roadmap for potential research

trajectories conducive to the advancement of the field. In essence, this survey serves as an invaluable compendium for

researchers spanning diverse domains, with particular relevance to ethologists and neuroscientists. We believe that this

survey will function as a guiding beacon, steering forthcoming research initiatives and fostering advancements in the

intricate domain of animal behavior studies using deep learning.

REFERENCES

[1] Moloud Abdar, Farhad Pourpanah, Sadiq Hussain, Dana Rezazadegan, Li Liu, Mohammad Ghavamzadeh, Paul Fieguth, Xiaochun Cao, Abbas
Khosravi, U Rajendra Acharya, et al. 2021. A review of uncertainty quantification in deep learning: Techniques, applications and challenges.
Information fusion 76 (2021), 243–297.

[2] Hüseyin Gökhan Akçay, Bekir Kabasakal, Duygugül Aksu, Nusret Demir, Melih Öz, and Ali Erdoğan. 2020. Automated bird counting with deep

learning for regional bird distribution mapping. Animals 10, 7 (2020), 1207.

[3] Najla Al-Thani, Alreem Albuainain, Fatima Alnaimi, and Nizar Zorba. 2020. Drones for sheep livestock monitoring. In 2020 IEEE 20th Mediterranean

Electrotechnical Conference (MELECON). IEEE, 672–676.

[4] Mohammed Alagele and Remzi Yildirim. 2022. ANIMAL GAIT IDENTIFICATION USING A DEEP LEARNING METHOD. In 2022 International

Symposium on Multidisciplinary Studies and Innovative Technologies (ISMSIT). IEEE, 540–542.

[5] Ali Alameer, Stephanie Buijs, Niamh O’Connell, Luke Dalton, Mona Larsen, Lene Pedersen, and Ilias Kyriazakis. 2022. Automated detection and

quantification of contact behaviour in pigs using deep learning. biosystems engineering 224 (2022), 118–130.

[6] Ali Alameer, Ilias Kyriazakis, Hillary A Dalton, Amy L Miller, and Jaume Bacardit. 2020. Automatic recognition of feeding and foraging behaviour

in pigs using deep learning. Biosystems engineering 197 (2020), 91–104.

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

21

[7] Niek Andresen, Manuel Wöllhaf, Katharina Hohlbaum, Lars Lewejohann, Olaf Hellwich, Christa Thöne-Reineke, and Vitaly Belik. 2020. Towards a
fully automated surveillance of well-being status in laboratory mice using deep learning: Starting with facial expression analysis. PLoS One 15, 4
(2020), e0228059.

[8] Reza Arablouei, Liang Wang, Lachlan Currie, Jodan Yates, Flavio AP Alvarenga, and Greg J Bishop-Hurley. 2023. Animal behavior classification via

deep learning on embedded systems. Computers and Electronics in Agriculture 207 (2023), 107707.

[9] Reza Arablouei, Ziwei Wang, Greg J Bishop-Hurley, and Jiajun Liu. 2023. Multimodal sensor data fusion for in-situ classification of animal behavior

using accelerometry and GNSS data. Smart Agricultural Technology 4 (2023), 100163.

[10] Zoe Ashwood, Nicholas A Roy, Ji Hyun Bak, and Jonathan W Pillow. 2020. Inferring learning rules from animal decision-making. Advances in

Neural Information Processing Systems 33 (2020), 3442–3453.

[11] Safa Ayadi, Ahmed Ben Said, Rateb Jabbar, Chafik Aloulou, Achraf Chabbouh, and Ahmed Ben Achballah. 2020. Dairy cow rumination detection:
A deep learning approach. In Distributed Computing for Emerging Smart Networks: Second International Workshop, DiCES-N 2020, Bizerte, Tunisia,
December 18, 2020, Proceedings 2. Springer, 123–139.

[12] Shoubhik Chandan Banerjee, Khursheed Ahmad Khan, and Rati Sharma. 2023. Deep-worm-tracker: Deep learning methods for accurate detection

and tracking for behavioral studies in C. elegans. Applied Animal Behaviour Science 266 (2023), 106024.

[13] Jun Bao and Qiuju Xie. 2022. Artificial intelligence in animal farming: A systematic literature review. Journal of Cleaner Production 331 (2022),

129956.

[14] Shanis Barnard, Simone Calderara, Simone Pistocchi, Rita Cucchiara, Michele Podaliri-Vulpiani, Stefano Messori, and Nicola Ferri. 2016. Quick,

accurate, smart: 3D computer vision technology helps assessing confined animals’ behaviour. PloS one 11, 7 (2016), e0158748.

[15] Richard Bellman. 1957. A Markovian Decision Process. Journal of Mathematics and Mechanics 6, 5 (1957), 679–684. <http://www.jstor.org/stable/>

24900506

[16] S Benaissa, FAM Tuyttens, D Plets, L Martens, L Vandaele, W Joseph, and B Sonck. 2023. Improved cattle behaviour monitoring by combining

Ultra-Wideband location and accelerometer data. animal 17, 4 (2023), 100730.

[17] Silas Bergen, Manuela M Huso, Adam E Duerr, Melissa A Braham, Todd E Katzner, Sara Schmuecker, and Tricia A Miller. 2022. Classifying behavior

from short-interval biologging data: An example with GPS tracking of birds. Ecology and Evolution 12, 2 (2022), e08395.

[18] Gordon J Berman, Daniel M Choi, William Bialek, and Joshua W Shaevitz. 2014. Mapping the stereotyped behaviour of freely moving fruit flies.

Journal of The Royal Society Interface 11, 99 (2014), 20140672.

[19] Rodrigo Cupertino Bernardes, Maria Augusta Pereira Lima, Raul Narciso Carvalho Guedes, Clíssia Barboza da Silva, and Gustavo Ferreira Martins.

2021. Ethoflow: computer vision and artificial intelligence-based software for automatic behavior analysis. Sensors 21, 9 (2021), 3237.

[20] Samayan Bhattacharya and Sk Shahnawaz. 2021. Pose recognition in the wild: Animal pose estimation using agglomerative clustering and

contrastive learning. arXiv preprint arXiv:2111.08259 (2021).

[21] Dan Biderman, Matthew R Whiteway, Cole Hurwitz, Nicholas Greenspan, Robert S Lee, Ankit Vishnubhotla, Richard Warren, Federico Pedraja,
Dillon Noone, Michael Schartner, et al. 2023. Lightning Pose: improved animal pose estimation via semi-supervised learning, Bayesian ensembling,
and cloud-native open-source tools. bioRxiv (2023).

[22] Kim Bjerge, Jamie Alison, Mads Dyrmann, Carsten Eie Frigaard, Hjalte MR Mann, and Toke Thomas Høye. 2023. Accurate detection and

identification of insects from camera trap images with deep learning. PLOS Sustainability and Transformation 2, 3 (2023), e0000051.

[23] Ari Blau, Christoph Gebhardt, Andres Bendesky, Liam Paninski, and Anqi Wu. 2022. SemiMultiPose: A Semi-supervised Multi-animal Pose

Estimation Framework. arXiv preprint arXiv:2204.07072 (2022).

[24] Enkeleda Bocaj, Dimitris Uzunidis, Panagiotis Kasnesis, and Charalampos Z Patrikakis. 2020. On the benefits of deep convolutional neural networks

on animal activity recognition. In 2020 International Conference on Smart Systems and Technologies (SST). IEEE, 83–88.

[25] James P Bohnslav, Nivanthika K Wimalasena, Kelsey J Clausing, Yu Y Dai, David A Yarmolinsky, Tomás Cruz, Adam D Kashlan, M Eugenia Chiappe,
Lauren L Orefice, Clifford J Woolf, et al. 2021. DeepEthogram, a machine learning pipeline for supervised behavior classification from raw pixels.
Elife 10 (2021), e63377.

[26] Bernhard E Boser, Isabelle M Guyon, and Vladimir N Vapnik. 1992. A training algorithm for optimal margin classifiers. In Proceedings of the fifth

annual workshop on Computational learning theory. 144–152.

[27] Francisco J Bravo Sanchez, Md Rahat Hossain, Nathan B English, and Steven T Moore. 2021. Bioacoustic classification of avian calls from raw

sound waveforms with an open-source deep learning architecture. Scientific Reports 11, 1 (2021), 15733.

[28] Leo Breiman. 2001. Random forests. Machine learning 45 (2001), 5–32.
[29] André EX Brown and Benjamin de Bivort. 2017. The study of animal behaviour as a physical science. bioRxiv (2017). <https://doi.org/10.1101/220855>

arXiv:<https://www.biorxiv.org/content/early/2017/11/17/220855.full.pdf>

[30] Elizabeth C Bryda. 2013. The Mighty Mouse: the impact of rodents on advances in biomedical research. Missouri medicine 110, 3 (2013), 207.
[31] Xavier P Burgos-Artizzu, Piotr Dollár, Dayu Lin, David J Anderson, and Pietro Perona. 2012. Social behavior recognition in continuous video. In

2012 IEEE conference on computer vision and pattern recognition. IEEE, 1322–1329.

[32] Jinkun Cao, Hongyang Tang, Hao-Shu Fang, Xiaoyong Shen, Cewu Lu, and Yu-Wing Tai. 2019. Cross-domain adaptation for animal pose estimation.

In Proceedings of the IEEE/CVF international conference on computer vision. 9498–9507.

[33] Shuo Cao, Dean Zhao, Xiaoyang Liu, and Yueping Sun. 2020. Real-time robust detector for underwater live crabs based on deep learning. Computers

and Electronics in Agriculture 172 (2020), 105339.

Manuscript submitted to ACM

22

Fazzari, et al.

[34] Zhe Cao, Tomas Simon, Shih-En Wei, and Yaser Sheikh. 2017. Realtime multi-person 2d pose estimation using part affinity fields. In Proceedings of

the IEEE conference on computer vision and pattern recognition. 7291–7299.

[35] Carl Chalmers, Paul Fergus, S Wich, and SN Longmore. 2021. Modelling Animal Biodiversity Using Acoustic Monitoring and Deep Learning. In

2021 International Joint Conference on Neural Networks (IJCNN). IEEE, 1–7.

[36] Robert D Chambers, Nathanael C Yoder, Aletha B Carson, Christian Junge, David E Allen, Laura M Prescott, Sophie Bradley, Garrett Wymore, Kevin
Lloyd, and Scott Lyle. 2021. Deep learning classification of canine behavior using a single collar-mounted accelerometer: Real-world validation.
Animals 11, 6 (2021), 1549.

[37] Chen Chen, Weixing Zhu, and Tomas Norton. 2021. Behaviour recognition of pigs and cattle: Journey from computer vision to deep learning.

Computers and Electronics in Agriculture 187 (2021), 106255.

[38] Chen Chen, Weixing Zhu, Juan Steibel, Janice Siegford, Junjie Han, and Tomas Norton. 2020. Recognition of feeding behaviour of pigs and

determination of feeding time of each pig by a video-based deep learning method. Computers and Electronics in Agriculture 176 (2020), 105642.

[39] Yu Chen, Chunhua Shen, Xiu-Shen Wei, Lingqiao Liu, and Jian Yang. 2017. Adversarial posenet: A structure-aware convolutional network for

human pose estimation. In Proceedings of the IEEE international conference on computer vision. 1212–1221.

[40] Taeyeong Choi, Benjamin Pyenson, Juergen Liebig, and Theodore P Pavlic. 2022. Beyond tracking: using deep learning to discover novel interactions

in biological swarms. Artificial Life and Robotics 27, 2 (2022), 393–400.

[41] Yoona Choi, Heechan Chae, Jonguk Lee, Daihee Park, and Yongwha Chung. 2021. Cat Monitoring and Disease Diagnosis System based on Deep

Learning. Journal of Korea Multimedia Society 24, 2 (2021), 233–244.

[42] François Chollet. 2017. Xception: Deep learning with depthwise separable convolutions. In Proceedings of the IEEE conference on computer vision

and pattern recognition. 1251–1258.

[43] Chia-Jung Chou, Jui-Ting Chien, and Hwann-Tzong Chen. 2018. Self adversarial training for human pose estimation. In 2018 Asia-Pacific Signal

and Information Processing Association Annual Summit and Conference (APSIPA ASC). IEEE, 17–30.

[44] Genaro A Coria-Avila, James G Pfaus, Agustín Orihuela, Adriana Domínguez-Oliva, Nancy José-Pérez, Laura Astrid Hernández, and Daniel

Mota-Rojas. 2022. The neurobiology of behavior and its applicability for animal welfare: A review. Animals 12, 7 (2022), 928.

[45] Solemane Coulibaly, Bernard Kamsu-Foguem, Dantouma Kamissoko, and Daouda Traore. 2022. Explainable deep convolutional neural networks

for insect pest recognition. Journal of Cleaner Production 371 (2022), 133638.

[46] Thai-Ha Dang, Ngoc-Hai Dang, Viet-Thang Tran, and Wan-Young Chung. 2022. A LoRaWAN-Based Smart Sensor Tag for Cow Behavior Monitoring.

In 2022 IEEE Sensors. IEEE, 1–4.

[47] Anthony I Dell, John A Bender, Kristin Branson, Iain D Couzin, Gonzalo G de Polavieja, Lucas PJJ Noldus, Alfonso Pérez-Escudero, Pietro Perona,
Andrew D Straw, Martin Wikelski, et al. 2014. Automated image-based tracking and its application in ecology. Trends in ecology & evolution 29, 7
(2014), 417–428.

[48] Ellen M Ditria, Sebastian Lopez-Marcano, Michael Sievers, Eric L Jinks, Christopher J Brown, and Rod M Connolly. 2020. Automating the analysis

of fish abundance using object detection: optimizing animal ecology with deep learning. Frontiers in Marine Science (2020), 429.

[49] Anniek Eerdekens, Margot Deruyck, Jaron Fontaine, Luc Martens, Eli De Poorter, David Plets, and Wout Joseph. 2020. Resampling and data
augmentation for equines’ behaviour classification based on wearable sensor accelerometer data using a convolutional neural network. In 2020
International Conference on Omni-layer Intelligent Systems (COINS). IEEE, 1–6.

[50] Abdullah Magdy Elbarrany, Abdallah Mohialdin, and Ayman Atia. 2023. The Use of Pose Estimation for Abnormal Behavior Analysis in Poultry

Farms. In 2023 5th Novel Intelligent and Leading Emerging Sciences Conference (NILES). IEEE, 33–36.

[51] Ivan Roy S Evangelista, Ronnie Concepcion, Maria Gemel B Palconit, Argel A Bandala, and Elmer P Dadios. 2022. YOLOv7 and DeepSORT for
Intelligent Quail Behavioral Activities Monitoring. In 2022 IEEE 14th International Conference on Humanoid, Nanotechnology, Information Technology,
Communication and Control, Environment, and Management (HNICEM). IEEE, 1–5.

[52] Xiaochuan Fan, Kang Zheng, Yuewei Lin, and Song Wang. 2015. Combining local appearance and holistic view: Dual-source deep neural networks

for human pose estimation. In Proceedings of the IEEE conference on computer vision and pattern recognition. 1347–1355.

[53] Cheng Fang, Tiemin Zhang, Haikun Zheng, Junduan Huang, and Kaixuan Cuan. 2021. Pose estimation and behavior classification of broiler

chickens based on deep neural networks. Computers and Electronics in Agriculture 180 (2021), 105863.

[54] Edoardo Fazzari, Fabio Carrara, Fabrizio Falchi, Cesare Stefanini, and Donato Romano. 2023. Using AI to decode the behavioral responses of an
insect to chemical stimuli: towards machine-animal computational technologies. International Journal of Machine Learning and Cybernetics (2023).
<https://doi.org/10.1007/s13042-023-02009-y>

[55] Edoardo Fazzari, Fabio Carrara, Fabrizio Falchi, Cesare Stefanini, Donato Romano, et al. 2022. A Workflow for Developing Biohybrid Intelligent

Sensing Systems. (2022).

[56] Christoph Feichtenhofer, Haoqi Fan, Jitendra Malik, and Kaiming He. 2019. Slowfast networks for video recognition. In Proceedings of the IEEE/CVF

international conference on computer vision. 6202–6211.

[57] Marcelo Feighelstein, Yamit Ehrlich, Li Naftaly, Miriam Alpin, Shenhav Nadir, Ilan Shimshoni, Renata H Pinho, Stelio PL Luna, and Anna Zamansky.

2023. Deep learning for video-based automated pain recognition in rabbits. Scientific Reports 13, 1 (2023), 14679.

[58] Alvaro Fuentes, Sook Yoon, Jongbin Park, and Dong Sun Park. 2020. Deep learning-based hierarchical cattle behavior recognition with spatio-

temporal information. Computers and Electronics in Agriculture 177 (2020), 105627.

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

23

[59] Shiori Fujimori, Takaaki Ishikawa, and Hiroshi Watanabe. 2020. Animal behavior classification using DeepLabCut. In 2020 IEEE 9th Global

Conference on Consumer Electronics (GCCE). IEEE, 254–257.

[60] Sudarsini Tekkam Gnanasekar, Svetlana Yanushkevich, Nynke J Van den Hoogen, and Tuan Trang. 2022. Rodent Tracking and Abnormal Behavior
Classification in Live Video using Deep Neural Networks. In 2022 IEEE Symposium Series on Computational Intelligence (SSCI). IEEE, 830–837.
[61] Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. 2014. Generative

adversarial nets. Advances in neural information processing systems 27 (2014).

[62] Sayali V Gore, Rohit Kakodkar, Thaís Del Rosario Hernández, Sara Tucker Edmister, and Robbert Creton. 2023. Zebrafish Larvae Position Tracker
(Z-LaP Tracker): a high-throughput deep-learning behavioral approach for the identification of calcineurin pathway-modulating drugs using
zebrafish larvae. Scientific Reports 13, 1 (2023), 3174.

[63] Kiyoko M Gotanda, Damien R Farine, Claudius F Kratochwil, Kate L Laskowski, and Pierre-Olivier Montiglio. 2019. Animal behavior facilitates

eco-evolutionary dynamics. arXiv preprint arXiv:1912.09505 (2019).

[64] Jacob M Graving, Daniel Chae, Hemal Naik, Liang Li, Benjamin Koger, Blair R Costelloe, and Iain D Couzin. 2019. DeepPoseKit, a software toolkit

for fast and robust animal pose estimation using deep learning. Elife 8 (2019), e47994.

[65] Lars Haalck, Michael Mangan, Barbara Webb, and Benjamin Risse. 2020. Towards image-based animal tracking in natural environments using a

freely moving camera. Journal of neuroscience methods 330 (2020), 108455.

[66] Fangfang Han, Junchao Zhu, Bin Liu, Baofeng Zhang, and Fuhua Xie. 2020. Fish shoals behavior detection based on convolutional neural network

and spatiotemporal information. IEEE Access 8 (2020), 126907–126926.

[67] Kensho Hara, Hirokatsu Kataoka, and Yutaka Satoh. 2018. Can spatiotemporal 3d cnns retrace the history of 2d cnns and imagenet?. In Proceedings

of the IEEE conference on Computer Vision and Pattern Recognition. 6546–6555.

[68] Benjamin L Hart. 2011. Behavioural defences in animals against pathogens and parasites: parallels with the pillars of medicine in humans.

Philosophical Transactions of the Royal Society B: Biological Sciences 366, 1583 (2011), 3406–3417.

[69] Kaiming He, Georgia Gkioxari, Piotr Dollár, and Ross Girshick. 2017. Mask r-cnn. In Proceedings of the IEEE international conference on computer

vision. 2961–2969.

[70] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. 2016. Identity mappings in deep residual networks. In Computer Vision–ECCV 2016: 14th

European Conference, Amsterdam, The Netherlands, October 11–14, 2016, Proceedings, Part IV 14. Springer, 630–645.

[71] Ahmed M Helmi, Mohammed AA Al-qaness, Abdelghani Dahou, and Mohamed Abd Elaziz. 2023. Human activity recognition using marine

predators algorithm with deep learning. Future Generation Computer Systems 142 (2023), 340–350.

[72] Sepp Hochreiter and Jürgen Schmidhuber. 1997. Long short-term memory. Neural computation 9, 8 (1997), 1735–1780.
[73] Tahera Hossain, Wanggang Shen, Anindya Antar, Snehal Prabhudesai, Sozo Inoue, Xun Huan, and Nikola Banovic. 2023. A Bayesian approach for
quantifying data scarcity when modeling human behavior via inverse reinforcement learning. ACM Transactions on Computer-Human Interaction
30, 1 (2023), 1–27.

[74] Jin Hou, Yuxin He, Hongbo Yang, Thomas Connor, Jie Gao, Yujun Wang, Yichao Zeng, Jindong Zhang, Jinyan Huang, Bochuan Zheng, et al. 2020.

Identification of animal individuals using deep learning: A case study of giant panda. Biological Conservation 242 (2020), 108414.

[75] Md Milon Islam, Sheikh Nooruddin, Fakhri Karray, and Ghulam Muhammad. 2023. Multi-level feature fusion for multimodal human activity

recognition in Internet of Healthcare Things. Information Fusion 94 (2023), 17–31.

[76] Hassan Ismail Fawaz, Benjamin Lucas, Germain Forestier, Charlotte Pelletier, Daniel F Schmidt, Jonathan Weber, Geoffrey I Webb, Lhassane
Idoumghar, Pierre-Alain Muller, and François Petitjean. 2020. Inceptiontime: Finding alexnet for time series classification. Data Mining and
Knowledge Discovery 34, 6 (2020), 1936–1962.

[77] Yinjun Jia, Shuaishuai Li, Xuan Guo, Bo Lei, Junqiang Hu, Xiao-Hong Xu, and Wei Zhang. 2022. Selfee, self-supervised features extraction of

animal behaviors. Elife 11 (2022), e76218.

[78] Le Jiang, Caleb Lee, Divyang Teotia, and Sarah Ostadabbas. 2022. Animal pose estimation: A closer look at the state-of-the-art, existing gaps and

opportunities. Computer Vision and Image Understanding (2022), 103483.

[79] Min Jiang, Yuan Rao, Jingyao Zhang, and Yiming Shen. 2020. Automatic behavior recognition of group-housed goats using deep learning. Computers

and Electronics in Agriculture 177 (2020), 105706.

[80] Zheheng Jiang, Zhihua Liu, Long Chen, Lei Tong, Xiangrong Zhang, Xiangyuan Lan, Danny Crookes, Ming-Hsuan Yang, and Huiyu Zhou. 2022.
Detecting and tracking of multiple mice using part proposal networks. IEEE Transactions on Neural Networks and Learning Systems (2022).
[81] Zheheng Jiang, Feixiang Zhou, Aite Zhao, Xin Li, Ling Li, Dacheng Tao, Xuelong Li, and Huiyu Zhou. 2021. Multi-view mouse social behaviour

recognition with deep graphic model. IEEE Transactions on Image Processing 30 (2021), 5490–5504.

[82] Kevin Hyekang Joo, Shiyuan Duan, Shawna L Weimer, and Mohammad Nayeem Teli. 2022. Birds’ Eye View: Measuring Behavior and Posture of

Chickens as a Metric for Their Well-Being. arXiv preprint arXiv:2205.00069 (2022).

[83] Telmo De Cesaro Júnior and Rafael Rieder. 2020. Automatic identification of insects from digital images: A survey. Computers and Electronics in

Agriculture 178 (2020), 105784.

[84] Jacob W Kamminga, Duc V Le, Jan Pieter Meijers, Helena Bisby, Nirvana Meratnia, and Paul JM Havinga. 2018. Robust sensor-orientation-
independent feature selection for animal activity recognition on collar tags. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous
Technologies 2, 1 (2018), 1–27.

Manuscript submitted to ACM

24

Fazzari, et al.

[85] Jacob W Kamminga, Nirvana Meratnia, and Paul JM Havinga. 2019. Dataset: Horse movement data and analysis of its potential for activity

recognition. In Proceedings of the 2nd Workshop on Data Acquisition To Analysis. 22–25.

[86] Panagiotis Kasnesis, Vasileios Doulgerakis, Dimitris Uzunidis, Dimitris G Kogias, Susana I Funcia, Marta B González, Christos Giannousis, and
Charalampos Z Patrikakis. 2022. Deep learning empowered wearable-based behavior recognition for search and rescue dogs. Sensors 22, 3 (2022),
993.

[87] Jörg Kaufmann and AG Schering. 2014. Analysis of Variance ANOVA. John Wiley & Sons, Ltd. <https://doi.org/10.1002/9781118445112.stat06938>

arXiv:<https://onlinelibrary.wiley.com/doi/pdf/10.1002/9781118445112.stat06938>

[88] AT Kavlak, M Pastell, and P Uimari. 2023. Disease detection in pigs based on feeding behaviour traits using machine learning. biosystems engineering

226 (2023), 132–143.

[89] Diederik P Kingma and Max Welling. 2013. Auto-encoding variational bayes. arXiv preprint arXiv:1312.6114 (2013).
[90] Natasa Kleanthous, Abir Hussain, Wasiq Khan, Jennifer Sneddon, and Panos Liatsis. 2022. Deep transfer learning in sheep activity recognition

using accelerometer data. Expert Systems with Applications 207 (2022), 117925.

[91] Natasa Kleanthous, Abir Jaafar Hussain, Wasiq Khan, Jennifer Sneddon, Ahmed Al-Shamma’a, and Panos Liatsis. 2022. A survey of machine

learning approaches in animal behaviour. Neurocomputing 491 (2022), 442–463.

[92] Elly C Knight and Erin M Bayne. 2019. Classification threshold and training data affect the quality and utility of focal species data processed with

automated audio-recognition software. Bioacoustics 28, 6 (2019), 539–554.

[93] Gregory Koch, Richard Zemel, Ruslan Salakhutdinov, et al. 2015. Siamese neural networks for one-shot image recognition. In ICML deep learning

workshop, Vol. 2. Lille.

[94] Benjamin Koger, Adwait Deshpande, Jeffrey T Kerby, Jacob M Graving, Blair R Costelloe, and Iain D Couzin. 2023. Quantifying the movement,

behaviour and environmental context of group-living animals using drones and computer vision. Journal of Animal Ecology (2023).

[95] International Brain Laboratory, Valeria Aguillon-Rodriguez, Dora Angelaki, Hannah Bayer, Niccolò Bonacchi, Matteo Carandini, Fanny Cazettes,
Gaelle Chapuis, Anne K Churchland, Yang Dan, et al. 2021. Standardized and reproducible measurement of decision-making in mice. Elife 10
(2021), e63711.

[96] Rollyn Labuguen, Jumpei Matsumoto, Salvador Blanco Negrete, Hiroshi Nishimaru, Hisao Nishijo, Masahiko Takada, Yasuhiro Go, Ken-ichi Inoue,
and Tomohiro Shibata. 2021. MacaquePose: a novel “in the wild” macaque monkey pose dataset for markerless motion capture. Frontiers in
behavioral neuroscience 14 (2021), 581154.

[97] Tim Landgraf, Gregor HW Gebhardt, David Bierbach, Pawel Romanczuk, Lea Musiolek, Verena V Hafner, and Jens Krause. 2021. Animal-in-the-loop:
using interactive robotic conspecifics to study social behavior in animal groups. Annual Review of Control, Robotics, and Autonomous Systems 4
(2021), 487–507.

[98] Jessy Lauer, Mu Zhou, Shaokai Ye, William Menegas, Steffen Schneider, Tanmay Nath, Mohammed Mostafizur Rahman, Valentina Di Santo, Daniel
Soberanes, Guoping Feng, et al. 2022. Multi-animal pose estimation, identification and tracking with DeepLabCut. Nature Methods 19, 4 (2022),
496–504.

[99] Colin Lea, Rene Vidal, Austin Reiter, and Gregory D Hager. 2016. Temporal convolutional networks: A unified approach to action segmentation. In
Computer Vision–ECCV 2016 Workshops: Amsterdam, The Netherlands, October 8-10 and 15-16, 2016, Proceedings, Part III 14. Springer, 47–54.
[100] Charly G Lecomte, Johannie Audet, Jonathan Harnie, and Alain Frigon. 2021. A validation of supervised deep learning for gait analysis in the cat.

Frontiers in Neuroinformatics 15 (2021), 712623.

[101] Sanghoon Lee, Brayden Waugh, Garret O’Dell, Xiji Zhao, Wook-Sung Yoo, and Dal Hyung Kim. 2021. Predicting Fruit Fly Behaviour using TOLC

device and DeepLabCut. In 2021 IEEE 21st International Conference on Bioinformatics and Bioengineering (BIBE). IEEE, 1–6.

[102] Yujie Lei, Pengmei Dong, Yan Guan, Ying Xiang, Meng Xie, Jiong Mu, Yongzhao Wang, and Qingyong Ni. 2022. Postural behavior recognition of

captive nocturnal animals based on deep learning: a case study of Bengal slow loris. Scientific Reports 12, 1 (2022), 7738.

[103] Chen Li and Gim Hee Lee. 2023. ScarceNet: Animal Pose Estimation with Scarce Annotations. In Proceedings of the IEEE/CVF Conference on

Computer Vision and Pattern Recognition. 17174–17183.

[104] Dan Li, Kaifeng Zhang, Zhenbo Li, and Yifei Chen. 2020. A spatiotemporal convolutional network for multi-behavior recognition of pigs. Sensors

20, 8 (2020), 2381.

[105] Juan Li, Chen Xu, Lingxu Jiang, Ying Xiao, Limiao Deng, and Zhongzhi Han. 2019. Detection and analysis of behavior trajectory for sea cucumbers

based on deep learning. Ieee Access 8 (2019), 18832–18840.

[106] Shuyuan Li, Jianguo Li, Hanlin Tang, Rui Qian, and Weiyao Lin. 2019. ATRW: a benchmark for Amur tiger re-identification in the wild. arXiv

preprint arXiv:1906.05586 (2019).

[107] Yang Li, Guanci Yang, Zhidong Su, Shaobo Li, and Yang Wang. 2023. Human activity recognition based on multienvironment sensor data.

Information Fusion 91 (2023), 47–63.

[108] Tsung-Yi Lin, Piotr Dollár, Ross Girshick, Kaiming He, Bharath Hariharan, and Serge Belongie. 2017. Feature pyramid networks for object detection.

In Proceedings of the IEEE conference on computer vision and pattern recognition. 2117–2125.

[109] Fei Tony Liu, Kai Ming Ting, and Zhi-Hua Zhou. 2008. Isolation forest. In 2008 eighth ieee international conference on data mining. IEEE, 413–422.
[110] XiaoLe Liu, Si-yang Yu, Nico Flierman, Sebastian Loyola, Maarten Kamermans, Tycho M Hoogland, and Chris I De Zeeuw. 2020. OptiFlex:

video-based animal pose estimation using deep learning enhanced by optical flow. BioRxiv (2020), 2020–04.

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

25

[111] Yongkui Liu, He Xu, Ding Liu, and Lihui Wang. 2022. A digital twin-based sim-to-real transfer for deep reinforcement learning-enabled industrial

robot grasping. Robotics and Computer-Integrated Manufacturing 78 (2022), 102365.

[112] Vincent Lostanlen, Kaitlin Palmer, Elly Knight, Christopher Clark, Holger Klinck, Andrew Farnsworth, Tina Wong, Jason Cramer, and Juan Pablo
Bello. 2019. Long-distance detection of bioacoustic events with per-channel energy normalization. arXiv preprint arXiv:1911.00417 (2019).
[113] Kevin Luxem, Petra Mocellin, Falko Fuhrmann, Johannes Kürsch, Stephanie R Miller, Jorge J Palop, Stefan Remy, and Pavol Bauer. 2022. Identifying

behavioral structure from deep variational embeddings of animal motion. Communications Biology 5, 1 (2022), 1267.

[114] Md Sultan Mahmud, Azlan Zahid, Anup Kumar Das, Muhammad Muzammil, and Muhammad Usman Khan. 2021. A systematic literature review

on deep learning applications for precision cattle farming. Computers and Electronics in Agriculture 187 (2021), 106313.

[115] Gianluca Manduca, Valeria Zeni, Sara Moccia, Beatrice A Milano, Angelo Canale, Giovanni Benelli, Cesare Stefanini, and Donato Romano. 2023.

Learning algorithms estimate pose and detect motor anomalies in flies exposed to minimal doses of a toxicant. Iscience 26, 12 (2023).

[116] Richard Mankin, David Hagstrum, Min Guo, Panagiotis Eliopoulos, and Anastasia Njoroge. 2021. Automated applications of acoustics for stored

product insect detection, monitoring, and management. Insects 12, 3 (2021), 259.

[117] Dr Samuel Manoharan. 2020. Embedded imaging system based behavior analysis of dairy cow. Journal of Electronics and Informatics 2, 2 (2020),

148–154.

[118] Markus Marks, Qiuhan Jin, Oliver Sturman, Lukas von Ziegler, Sepp Kollmorgen, Wolfger von der Behrens, Valerio Mante, Johannes Bohacek, and
Mehmet Fatih Yanik. 2022. Deep-learning-based identification, tracking, pose estimation and behaviour classification of interacting primates and
mice in complex environments. Nature machine intelligence 4, 4 (2022), 331–340.

[119] Jesse D Marshall, Tianqing Li, Joshua H Wu, and Timothy W Dunn. 2022. Leaving flatland: Advances in 3D behavioral measurement. Current

Opinion in Neurobiology 73 (2022), 102522.

[120] Miguel Martin-Abadal, Ana Ruiz-Frau, Hilmar Hinz, and Yolanda Gonzalez-Cid. 2020. Jellytoring: real-time jellyfish monitoring based on deep

learning object detection. Sensors 20, 6 (2020), 1708.

[121] Alexander Mathis, Thomas Biasi, Steffen Schneider, Mert Yuksekgonul, Byron Rogers, Matthias Bethge, and Mackenzie W Mathis. 2021. Pretraining
boosts out-of-domain robustness for pose estimation. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision.
1859–1868.

[122] Alexander Mathis, Pranav Mamidanna, Kevin M Cury, Taiga Abe, Venkatesh N Murthy, Mackenzie Weygandt Mathis, and Matthias Bethge. 2018.

DeepLabCut: markerless pose estimation of user-defined body parts with deep learning. Nature neuroscience 21, 9 (2018), 1281–1289.

[123] Mackenzie Weygandt Mathis and Alexander Mathis. 2020. Deep learning tools for the measurement of animal behavior in neuroscience. Current

opinion in neurobiology 60 (2020), 1–11.

[124] Declan McIntosh, Tunai Porto Marques, Alexandra Branzan Albu, Rodney Rountree, and Fabio De Leo. 2020. Movement tracks for the automatic

detection of fish behavior in videos. arXiv preprint arXiv:2011.14070 (2020).

[125] Grace C McKenzie-Smith, Scott W Wolf, Julien F Ayroles, and Joshua W Shaevitz. 2023. Capturing continuous, long timescale behavioral changes

in Drosophila melanogaster postural data. arXiv preprint arXiv:2309.04044 (2023).

[126] Sakorn Mekruksavanich, Ponnipa Jantawong, and Anuchit Jitpattanakul. 2022. ResNet-based Deep Neural Network using Transfer Learning for

Animal Activity Recognition. In 2022 6th International Conference on Information Technology (InCIT). IEEE, 445–449.

[127] Querriel Arvy Mendoza, Lester Pordesimo, Mitchell Neilsen, Paul Armstrong, James Campbell, and Princess Tiffany Mendoza. 2023. Application of

Machine Learning for Insect Monitoring in Grain Facilities. AI 4, 1 (2023), 348–360.

[128] Shailendra Mishra and Sunil Kumar Sharma. 2023. Advanced contribution of IoT in agricultural production for the development of smart livestock

environments. Internet of Things 22 (2023), 100724.

[129] Andreas P Modlmeier, Ewan Colman, Ephraim M Hanks, Ryan Bringenberg, Shweta Bansal, and David P Hughes. 2019. Ant colonies maintain

social homeostasis in the face of decreased density. Elife 8 (2019), e38473.

[130] Abdallah Mohamed Mohialdin, Abdullah Magdy Elbarrany, and Ayman Atia. 2023. Chicken Behavior Analysis for Surveillance in Poultry Farms.

(2023).

[131] Veronica Morfi, Yves Bas, Hanna Pamuła, Hervé Glotin, and Dan Stowell. 2019. NIPS4Bplus: a richly annotated birdsong audio dataset. PeerJ

Computer Science 5 (2019), e223.

[132] Keita Mori, Naohiro Yamauchi, Haoyu Wang, Ken Sato, Yu Toyoshima, and Yuichi Iino. 2022. Probabilistic generative modeling and reinforcement

learning extract the intrinsic features of animal behavior. Neural Networks 145 (2022), 107–120.

[133] Ilyass Moummad, Romain Serizel, and Nicolas Farrugia. 2023. Regularized Contrastive Pre-training for Few-shot Bioacoustic Sound Detection.

arXiv preprint arXiv:2309.08971 (2023).

[134] Amin Nasiri, Ahmad Amirivojdan, Yang Zhao, and Hao Gan. 2023. Estimating the Feeding Time of Individual Broilers via Convolutional Neural

Network and Image Processing. Animals 13, 15 (2023), 2428.

[135] Tanmay Nath, Alexander Mathis, An Chi Chen, Amir Patel, Matthias Bethge, and Mackenzie Weygandt Mathis. 2019. Using DeepLabCut for 3D

markerless pose estimation across species and behaviors. Nature protocols 14, 7 (2019), 2152–2176.

[136] Suresh Neethirajan. 2020. The role of sensors, big data and machine learning in modern animal farming. Sensing and Bio-Sensing Research 29

(2020), 100367.

[137] Xun Long Ng, Kian Eng Ong, Qichen Zheng, Yun Ni, Si Yong Yeo, and Jun Liu. 2022. Animal kingdom: A large and diverse dataset for animal

behavior understanding. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 19023–19034.

Manuscript submitted to ACM

26

Fazzari, et al.

[138] Thong Duy Nguyen and Milan Kresovic. 2022. A survey of top-down approaches for human pose estimation. arXiv preprint arXiv:2202.02656

(2022).

[139] Simon RO Nilsson, Nastacia L Goodwin, Jia Jie Choong, Sophia Hwang, Hayden R Wright, Zane C Norville, Xiaoyu Tong, Dayu Lin, Brandon S
Bentzley, Neir Eshel, et al. 2020. Simple Behavioral Analysis (SimBA)–an open source toolkit for computer classification of complex social behaviors
in experimental animals. BioRxiv (2020), 2020–04.

[140] Inês Nolasco, Shubhr Singh, Veronica Morfi, Vincent Lostanlen, Ariana Strandburg-Peshkin, Ester Vidaña-Vila, Lisa Gill, Hanna Pamuła, Helen

Whitehead, Ivan Kiskin, et al. 2023. Learning to detect an animal sound from five examples. Ecological Informatics 77 (2023), 102258.

[141] Anicetus Odo, Ramon Muns, Laura Boyle, and Ilias Kyriazakis. 2023. Video Analysis using Deep Learning for Automatic Quantification of Ear

Biting in Pigs. IEEE Access (2023).

[142] Dario Augusto Borges Oliveira, Luiz Gustavo Ribeiro Pereira, Tiago Bresolin, Rafael Ehrich Pontes Ferreira, and Joao Ricardo Reboucas Dorea.

2021. A review of deep learning algorithms for computer vision systems in livestock. Livestock Science 253 (2021), 104700.

[143] Mehmet Batuhan Özdaş, Fatih Uysal, and Fırat Hardalaç. 2023. Classification of Retinal Diseases in Optical Coherence Tomography Images Using

Artificial Intelligence and Firefly Algorithm. Diagnostics 13, 3 (2023), 433.

[144] Zhixin Pan, Huihui Chen, Weizhao Zhong, Aiguo Wang, and Chundi Zheng. 2023. A CNN-Based Animal Behavior Recognition Algorithm for

Wearable Devices. IEEE Sensors Journal 23, 5 (2023), 5156–5164.

[145] George Papandreou, Tyler Zhu, Liang-Chieh Chen, Spyros Gidaris, Jonathan Tompson, and Kevin Murphy. 2018. PersonLab: Person Pose Estimation
and Instance Segmentation with a Bottom-Up, Part-Based, Geometric Embedding Model. In Proceedings of the European Conference on Computer
Vision (ECCV).

[146] Vaios Papaspyros, Ramón Escobedo, Alexandre Alahi, Guy Theraulaz, Clément Sire, and Francesco Mondada. 2023. Predicting long-term collective

animal behavior with deep learning. bioRxiv (2023), 2023–02.

[147] Hyunseo Park, Nakyoung Kim, Gyeong Ho Lee, and Jun Kyun Choi. 2023. MultiCNN-FilterLSTM: Resource-efficient sensor-based human activity

recognition in IoT applications. Future Generation Computer Systems 139 (2023), 196–209.

[148] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. 2023. Generative agents: Interactive

simulacra of human behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology. 1–22.

[149] Ward A Pedersen, Pamela J McMillan, J Jacob Kulstad, James B Leverenz, Suzanne Craft, and Gleb R Haynatzki. 2006. Rosiglitazone attenuates

learning and memory deficits in Tg2576 Alzheimer mice. Experimental neurology 199, 2 (2006), 265–273.

[150] Xi Peng, Zhiqiang Tang, Fei Yang, Rogerio S Feris, and Dimitris Metaxas. 2018. Jointly optimize data augmentation and network training: Adversarial
data augmentation in human pose estimation. In Proceedings of the IEEE conference on computer vision and pattern recognition. 2226–2234.
[151] Talmo D Pereira, Diego E Aldarondo, Lindsay Willmore, Mikhail Kislin, Samuel S-H Wang, Mala Murthy, and Joshua W Shaevitz. 2019. Fast animal

pose estimation using deep neural networks. Nature methods 16, 1 (2019), 117–125.

[152] Talmo D Pereira, Nathaniel Tabris, Arie Matsliah, David M Turner, Junyu Li, Shruthi Ravindranath, Eleni S Papadoyannis, Edna Normand, David S
Deutsch, Z Yan Wang, et al. 2022. SLEAP: A deep learning system for multi-animal pose tracking. Nature methods 19, 4 (2022), 486–495.
[153] Michael Perez and Corey Toler-Franklin. 2023. CNN-Based Action Recognition and Pose Estimation for Classifying Animal Behavior from Videos:

A Survey. arXiv preprint arXiv:2301.06187 (2023).

[154] Tuan D Pham. 2022. Classification of Caenorhabditis Elegans Locomotion Behaviors With Eigenfeature-Enhanced Long Short-Term Memory

Networks. IEEE/ACM Transactions on Computational Biology and Bioinformatics 20, 1 (2022), 206–216.

[155] AJ Piergiovanni and Michael Ryoo. 2019. Temporal gaussian mixture layer for videos. In International Conference on Machine learning. PMLR,

5152–5161.

[156] Rudresh Pillai, Rupesh Gupta, Neha Sharma, and Rajesh Kumar Bansal. 2023. A Deep Learning Approach for Detection and Classification of Ten

Species of Monkeys. In 2023 International Conference on Smart Systems for applications in Electrical Sciences (ICSSES). IEEE, 1–6.

[157] Lawrence Rabiner and Biinghwang Juang. 1986. An introduction to hidden Markov models. ieee assp magazine 3, 1 (1986), 4–16.
[158] Shah Atiqur Rahman, Insu Song, M.K.H. Leung, Ickjai Lee, and Kyungmi Lee. 2014. Fast action recognition using negative space features. Expert

Systems with Applications 41, 2 (2014), 574–587. <https://doi.org/10.1016/j.eswa.2013.07.082>

[159] Joseph Redmon, Santosh Divvala, Ross Girshick, and Ali Farhadi. 2016. You only look once: Unified, real-time object detection. In Proceedings of the

IEEE conference on computer vision and pattern recognition. 779–788.

[160] Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun. 2015. Faster r-cnn: Towards real-time object detection with region proposal networks.

Advances in neural information processing systems 28 (2015).

[161] Martin Riekert, Achim Klein, Felix Adrion, Christa Hoffmann, and Eva Gallmann. 2020. Automatically detecting pig position and posture by 2D

camera imaging and deep learning. Computers and Electronics in Agriculture 174 (2020), 105391. <https://doi.org/10.1016/j.compag.2020.105391>

[162] Timothy P Robinson, GR William Wint, Giulia Conchedda, Thomas P Van Boeckel, Valentina Ercoli, Elisa Palamara, Giuseppina Cinardi, Laura

D’Aietti, Simon I Hay, and Marius Gilbert. 2014. Mapping the global distribution of livestock. PloS one 9, 5 (2014), e96084.

[163] Donato Romano and Cesare Stefanini (Eds.). 2021. Biological Cybernetics. 115, issue 6 Animal-robot interaction and biohybrid organisms (2021).
[164] Olaf Ronneberger, Philipp Fischer, and Thomas Brox. 2015. U-net: Convolutional networks for biomedical image segmentation. In Medical Image
Computing and Computer-Assisted Intervention–MICCAI 2015: 18th International Conference, Munich, Germany, October 5-9, 2015, Proceedings, Part III
18. Springer, 234–241.

[165] Sebastian Ruder. 2017. An overview of multi-task learning in deep neural networks. arXiv preprint arXiv:1706.05098 (2017).

Manuscript submitted to ACM

Animal Behavior Analysis Methods Using Deep Learning: A Survey

27

[166] Helena Russello, Rik van der Tol, and Gert Kootstra. 2022. T-LEAP: Occlusion-robust pose estimation of walking cows using temporal information.

Computers and Electronics in Agriculture 192 (2022), 106559.

[167] Alzayat Saleh, Marcus Sheaves, Dean Jerry, and Mostafa Rahimi Azghadi. 2022. Adaptive uncertainty distribution in deep learning for unsupervised

underwater image enhancement. arXiv preprint arXiv:2212.08983 (2022).

[168] Dema Saleh, Moemen Ahmed, Mai Zaafan, Yasmine Farouk, and Ayman Atia. 2023. A Pharmacology Toolkit for Animal Pose Estimation, Tracking

and Analysis. In 2023 International Mobile, Intelligent, and Ubiquitous Computing Conference (MIUCC). IEEE, 1–7.

[169] W Samsudin, MZ Harizan, MZ Ibrahim, RA Karim, and W Ibrahim. 2022. Zebrafish larvae locomotor activity detection using Convolutional Neural

Network (CNN). (2022).

[170] Mark Sandler, Andrew Howard, Menglong Zhu, Andrey Zhmoginov, and Liang-Chieh Chen. 2018. Mobilenetv2: Inverted residuals and linear

bottlenecks. In Proceedings of the IEEE conference on computer vision and pattern recognition. 4510–4520.

[171] Steffen Schneider, Jin Hwa Lee, and Mackenzie Weygandt Mathis. 2023. Learnable latent embeddings for joint behavioural and neural analysis.

Nature (2023), 1–9.

[172] Cristina Segalin, Jalani Williams, Tomomi Karigo, May Hui, Moriel Zelikowsky, Jennifer J Sun, Pietro Perona, David J Anderson, and Ann Kennedy.
2021. The Mouse Action Recognition System (MARS) software pipeline for automated analysis of social behaviors in mice. Elife 10 (2021), e63720.
[173] Ramprasaath R Selvaraju, Abhishek Das, Ramakrishna Vedantam, Michael Cogswell, Devi Parikh, and Dhruv Batra. 2016. Grad-CAM: Why did

you say that? arXiv preprint arXiv:1611.07450 (2016).

[174] Judy Shamoun-Baranes, Joseph B Burant, E Emiel van Loon, Willem Bouten, and CJ Camphuysen. 2017. Short distance migrants travel as far as

long distance migrants in lesser black-backed gulls Larus fuscus. Journal of Avian Biology 48, 1 (2017), 49–57.

[175] Julie K Shaw and Sarah Lahrman. 2023. The human–animal bond–a brief look at its richness and complexities. Canine and Feline Behavior for

Veterinary Technicians and Nurses (2023), 88–105.

[176] Karen Simonyan and Andrew Zisserman. 2014. Very deep convolutional networks for large-scale image recognition. arXiv preprint arXiv:1409.1556

(2014).

[177] Dan Stowell. 2022. Computational bioacoustics with deep learning: a review and roadmap. PeerJ 10 (2022), e13152.
[178] Christian Szegedy, Wei Liu, Yangqing Jia, Pierre Sermanet, Scott Reed, Dragomir Anguelov, Dumitru Erhan, Vincent Vanhoucke, and Andrew
Rabinovich. 2015. Going deeper with convolutions. In Proceedings of the IEEE conference on computer vision and pattern recognition. 1–9.
[179] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jon Shlens, and Zbigniew Wojna. 2016. Rethinking the inception architecture for computer

vision. In Proceedings of the IEEE conference on computer vision and pattern recognition. 2818–2826.

[180] Patrizia Tassinari, Marco Bovo, Stefano Benni, Simone Franzoni, Matteo Poggi, Ludovica Maria Eugenia Mammi, Stefano Mattoccia, Luigi Di Stefano,
Filippo Bonora, Alberto Barbaresi, et al. 2021. A computer vision approach based on deep learning for the detection of dairy cows in free stall barn.
Computers and Electronics in Agriculture 182 (2021), 106030.

[181] Ana Cláudia Teixeira, José Ribeiro, Raul Morais, Joaquim J Sousa, and António Cunha. 2023. A Systematic Review on Automatic Insect Detection

Using Deep Learning. Agriculture 13, 3 (2023), 713.

[182] Vu Quang Thanh and Chayakorn Netramai. 2022. Deep learning-based monitoring system for distress on mice using behavior analysis. In 2022

International Electrical Engineering Congress (iEECON). IEEE, 1–4.

[183] Zhi Tian, Hao Chen, and Chunhua Shen. 2019. Directpose: Direct end-to-end multi-person pose estimation. arXiv preprint arXiv:1911.07451 (2019).
[184] Sara Tucker Edmister, Thaís Del Rosario Hernández, Rahma Ibrahim, Cameron A Brown, Sayali V Gore, Rohit Kakodkar, Jill A Kreiling, and
Robbert Creton. 2022. Novel use of FDA-approved drugs identified by cluster analysis of behavioral profiles. Scientific Reports 12, 1 (2022), 6120.
[185] Tom Uchino and Hayato Ohwada. 2021. Individual identification model and method for estimating social rank among herd of dairy cows using

YOLOv5. In 2021 IEEE 20th International Conference on Cognitive Informatics & Cognitive Computing (ICCI* CC). IEEE, 235–241.

[186] Naeem Ullah, Javed Ali Khan, Lubna Abdulaziz Alharbi, Asaf Raza, Wahab Khan, and Ijaz Ahmad. 2022. An efficient approach for crops pests

recognition and classification based on novel DeepPestNet deep learning model. IEEE Access 10 (2022), 73019–73032.

[187] Alluri LSV Siddhartha Varma, Vishal Bateshwar, Anubuthi Rathi, and Anurag Singh. 2021. Acoustic Classification of Insects using Signal Processing
and Deep Learning Approaches. In 2021 8th International Conference on Signal Processing and Integrated Networks (SPIN). IEEE, 1048–1052.
[188] Juan Wang, Nan Wang, Lihua Li, and Zhenhui Ren. 2020. Real-time behavior detection and judgment of egg breeders based on YOLO v3. Neural

Computing and Applications 32 (2020), 5471–5481.

[189] Kui Wang, Pei Wu, Hongmei Cui, Chuanzhong Xuan, and He Su. 2021. Identification and classification for sheep foraging behavior based on

acoustic signal and deep learning. Computers and Electronics in Agriculture 187 (2021), 106275.

[190] Xingqi Wang, Chen Du, Ying Wang, Sheng Hu, and Yuliang Zhao. 2021. Behavioral Recognition of Mice Based on a Deep Network. In 2021 IEEE

11th Annual International Conference on CYBER Technology in Automation, Control, and Intelligent Systems (CYBER). IEEE, 840–844.

[191] Rebecca Z Weber, Geertje Mulders, Julia Kaiser, Christian Tackenberg, and Ruslan Rust. 2022. Deep learning-based behavioral profiling of rodent

stroke recovery. BMC biology 20, 1 (2022), 1–19.

[192] Dhanushi A Wijeyakulasuriya, Elizabeth W Eisenhauer, Benjamin A Shaby, and Ephraim M Hanks. 2020. Machine learning for modeling animal

movement. Plos one 15, 7 (2020), e0235750.

[193] Neslihan Wittek, Kevin Wittek, Christopher Keibel, and Onur Güntürkün. 2023. Supervised machine learning aided behavior classification in

pigeons. Behavior Research Methods 55, 4 (2023), 1624–1640.

Manuscript submitted to ACM

28

Fazzari, et al.

[194] Nicolai Wojke, Alex Bewley, and Dietrich Paulus. 2017. Simple online and realtime tracking with a deep association metric. In 2017 IEEE international

conference on image processing (ICIP). IEEE, 3645–3649.

[195] Anqi Wu, Estefany Kelly Buchanan, Matthew Whiteway, Michael Schartner, Guido Meijer, Jean-Paul Noel, Erica Rodriguez, Claire Everett, Amy
Norovich, Evan Schaffer, et al. 2020. Deep Graph Pose: a semi-supervised deep graphical model for improved animal pose tracking. Advances in
Neural Information Processing Systems 33 (2020), 6040–6052.

[196] Jiaxiang Wu, Cong Leng, Yuhang Wang, Qinghao Hu, and Jian Cheng. 2016. Quantized convolutional neural networks for mobile devices. In

Proceedings of the IEEE conference on computer vision and pattern recognition. 4820–4828.

[197] Shiting Xiao, Yufu Wang, Ammon Perkes, Bernd Pfrommer, Marc Schmidt, Kostas Daniilidis, and Marc Badger. 2023. Multi-view Tracking, Re-ID,
and Social Network Analysis of a Flock of Visually Similar Birds in an Outdoor Aviary. International Journal of Computer Vision 131, 6 (2023),
1532–1549.

[198] Weitao Xu, Xiang Zhang, Lina Yao, Wanli Xue, and Bo Wei. 2020. A multi-view CNN-based acoustic classification system for automatic animal

species identification. Ad Hoc Networks 102 (2020), 102115.

[199] Yufei Xu, Jing Zhang, Qiming Zhang, and Dacheng Tao. 2022. Vitpose: Simple vision transformer baselines for human pose estimation. Advances

in Neural Information Processing Systems 35 (2022), 38571–38584.

[200] Yufei Xu, Jing Zhang, Qiming Zhang, and Dacheng Tao. 2023. ViTPose++: Vision Transformer for Generic Body Pose Estimation. IEEE Transactions

on Pattern Analysis and Machine Intelligence (2023).

[201] Zhang Xudong, Kang Xi, Feng Ningning, and Liu Gang. 2020. Automatic recognition of dairy cow mastitis from thermal images by a deep learning

detector. Computers and Electronics in Agriculture 178 (2020), 105754.

[202] Jun Yamada, John Shawe-Taylor, and Zafeirios Fountas. 2020. Evolution of a complex predator-prey ecosystem on large-scale multi-agent deep

reinforcement learning. In 2020 International Joint Conference on Neural Networks (IJCNN). IEEE, 1–8.

[203] Shoichiro Yamaguchi, Honda Naoki, Muneki Ikeda, Yuki Tsukada, Shunji Nakano, Ikue Mori, and Shin Ishii. 2018. Identification of animal behavioral

strategies by inverse reinforcement learning. PLoS computational biology 14, 5 (2018), e1006122.

[204] Yuxiang Yang, Junjie Yang, Yufei Xu, Jing Zhang, Long Lan, and Dacheng Tao. 2022. Apt-36k: A large-scale benchmark for animal pose estimation

and tracking. Advances in Neural Information Processing Systems 35 (2022), 17301–17313.

[205] Shaokai Ye, Anastasiia Filippova, Jessy Lauer, Maxime Vidal, Steffen Schneider, Tian Qiu, Alexander Mathis, and Mackenzie Weygandt Mathis.

2022. SuperAnimal models pretrained for plug-and-play analysis of animal behavior. arXiv preprint arXiv:2203.07436 (2022).

[206] Hang Yu, Yufei Xu, Jing Zhang, Wei Zhao, Ziyu Guan, and Dacheng Tao. 2021. AP-10K: A Benchmark for Animal Pose Estimation in the Wild.

arXiv:2108.12617 [cs.CV]

[207] Kaifeng Zhang, Dan Li, Jiayun Huang, and Yifei Chen. 2020. Automated video behavior recognition of pigs using two-stream convolutional

networks. Sensors 20, 4 (2020), 1085.

[208] Ce Zheng, Wenhan Wu, Chen Chen, Taojiannan Yang, Sijie Zhu, Ju Shen, Nasser Kehtarnavaz, and Mubarak Shah. 2023. Deep learning-based

human pose estimation: A survey. Comput. Surveys 56, 1 (2023), 1–37.

[209] Feixiang Zhou, Xinyu Yang, Fang Chen, Long Chen, Zheheng Jiang, Hui Zhu, Reiko Heckel, Haikuan Wang, Minrui Fei, and Huiyu Zhou. 2022.
Cross-Skeleton Interaction Graph Aggregation Network for Representation Learning of Mouse Social Behaviour. arXiv preprint arXiv:2208.03819
(2022).

[210] Yi Zhu, Zhenzhong Lan, Shawn Newsam, and Alexander Hauptmann. 2019. Hidden two-stream convolutional networks for action recognition. In
Computer Vision–ACCV 2018: 14th Asian Conference on Computer Vision, Perth, Australia, December 2–6, 2018, Revised Selected Papers, Part III 14.
Springer, 363–378.

Manuscript submitted to ACM
