Review
Advancements in Sensor Fusion for Underwater SLAM:
A Review on Enhanced Navigation and
Environmental Perception

Fomekong Fomekong Rachel Merveille 1

, Baozhu Jia 1,*

, Zhizun Xu 2

and Bissih Fred 3

1

2

School of Naval Architecture and Maritime, Guangdong Ocean University, Zhanjiang 524000, China;
<marvelous@stu.gdou.edu.cn>
School of Engineering, Newcastle University, Newcastle upon Tyne NE1 7RU, UK; <zhizun@gdou.edu.cn>
3 College of Fisheries, Guangdong Ocean University, Zhanjiang 524088, China; <1252201246@stu.gdou.edu.cn>

* Correspondence: <jiabzh@gdou.edu.cn>; Tel.: +86-1864114229

Abstract: Underwater simultaneous localization and mapping (SLAM) has significant challenges due
to the complexities of underwater environments, marked by limited visibility, variable conditions,
and restricted global positioning system (GPS) availability. This study provides a comprehensive
analysis of sensor fusion techniques in underwater SLAM, highlighting the amalgamation of pro-
prioceptive and exteroceptive sensors to improve UUV navigational accuracy and system resilience.
Essential sensor applications, including inertial measurement units (IMUs), Doppler velocity logs
(DVLs), cameras, sonar, and LiDAR (light detection and ranging), are examined for their contribu-
tions to navigation and perception. Fusion methodologies, such as Kalman filters, particle filters,
and graph-based SLAM, are evaluated for their benefits, limitations, and computational demands.
Additionally, innovative technologies like quantum sensors and AI-driven filtering techniques are
examined for their potential to enhance SLAM precision and adaptability. Case studies demonstrate
practical applications, analyzing the compromises between accuracy, computational requirements,
and adaptability to environmental changes. This paper proceeds to emphasize future directions,
stressing the need for advanced filtering and machine learning to address sensor drift, noise, and en-
vironmental unpredictability, hence improving autonomous underwater navigation through reliable
sensor fusion.

Keywords: underwater simultaneous localization and mapping (SLAM); sensor fusion; unmanned
underwater vehicles (UUVs); Kalman filter; particle filter; graph-based SLAM; quantum sensors;
AI-driven filtering; deep learning

Citation: Merveille, F.F.R.; Jia, B.; Xu,

Z.; Fred, B. Advancements in Sensor

Fusion for Underwater SLAM: A

Review on Enhanced Navigation and

Environmental Perception. Sensors

2024, 24, 7490. <https://doi.org/>

10.3390/s24237490

Academic Editor: Udo Frese

1. Introduction

Received: 6 October 2024

Revised: 21 November 2024

Accepted: 22 November 2024

Published: 24 November 2024

Copyright: © 2024 by the authors.

Licensee MDPI, Basel, Switzerland.

This article is an open access article

distributed under the terms and

conditions of the Creative Commons

Attribution (CC BY) license (https://

creativecommons.org/licenses/by/

4.0/).

The oceans encompass over 71% of the Earth’s surface, serving a vital function in sci-
entific, environmental, and industrial domains, including oceanographic research, marine
ecosystem surveillance, and subsea infrastructure evaluation [1–6]. The intricate character-
istics of underwater settings pose distinct problems for UUVs [7,8], especially in attaining
dependable navigation and mapping. In contrast to terrestrial surroundings, underwater
settings exhibit low visibility, swift signal degradation, and a lack of GPS, all of which
impede precise localization and mapping [9,10]. Light and sound, vital for vision-based and
sonar systems, deteriorate markedly due to water dispersion, absorption, and reflection,
leading to degraded sensor data. Moreover, dynamic environmental factors—such as fluc-
tuating currents, changing salinity, and turbidity—complicate the operational challenges
for UUVs [11,12].

Recent research has increasingly concentrated on sensor fusion to address these prob-
lems, integrating data from several sensor modalities to improve the resilience and accuracy
of SLAM systems [13–16]. Sensor fusion facilitates the amalgamation of proprioceptive

Sensors 2024, 24, 7490. <https://doi.org/10.3390/s24237490>

<https://www.mdpi.com/journal/sensors>

Sensors 2024, 24, 7490

2 of 31

sensors, such as inertial measurement units (IMUs) that convey data regarding the UUV’s
internal condition, with exteroceptive sensors, including sonar, cameras, and LiDAR, which
acquire environmental information for mapping and object recognition [17–19]. This amal-
gamation of sensors mitigates the limitations of individual sensors, resulting in enhanced
precision and dependability in navigation.

This paper conducts a thorough evaluation of current research on sensor fusion in
underwater SLAM, chosen for its relevance, novelty, and methodological rigor [17,20–22].
Emphasis is placed on research concerning noise, drift, and sensor degradation in under-
water environments, particularly focusing on current advancements in deep learning and
AI-based sensor fusion methodologies [23–27]. This review emphasizes contemporary diffi-
culties and progress, offering insights into the strengths and weaknesses of current research
while proposing avenues for improving UUV navigation in intricate underwater settings.
Notwithstanding significant advancements, existing SLAM systems encounter con-
siderable obstacles in dynamic, GPS-denied settings characterized by restricted visibility
and frequent signal loss [28–30]. Contemporary research frequently focuses on individ-
ual sensor modalities, such as compass, Doppler Velocity Logs (DVL), sonar, LiDAR, or
visual SLAM, each with intrinsic constraints. For example, vision-based SLAM has dif-
ficulties in murky seas, sonar is limited by resolution, and IMUs are susceptible to drift
over time [31–33]. Although certain sensor fusion techniques are integrated, these systems
frequently struggle to achieve a balance between computing burden and real-time accuracy,
particularly in intricate underwater environments characterized by fluctuating turbidity
and illumination [8,34–38].

Conventional fusion methods, such as Kalman filters and particle filters, while ef-
ficient, face scalability challenges when including numerous sensors in nonlinear and
unpredictable underwater environments [39–41]. This study delineates three primary
research gaps: (1) insufficient real-time sensor fusion in dynamic, turbid environments;
(2) computational difficulties in integrating multiple sensor types under complex under-
water conditions; and (3) the necessity for sophisticated filtering techniques and machine
learning models to improve real-time fusion by alleviating sensor drift, noise, and environ-
mental variability [27,42].

This paper presents a fresh and comprehensive taxonomy of sensor fusion algorithms,
categorized by mathematical principles, underwater [43] efficacy, and computing trade-
offs. This categorization offers a sophisticated framework for assessing sensor fusion
algorithms designed for underwater applications. This review contrasts previous research
by examining established methods like Kalman and particle filters while also exploring
novel breakthroughs in AI-driven and quantum sensor fusion techniques.

This work offers a comparative review of sensor fusion methodologies, including
Kalman filters, Extended Kalman filters [44], particle filters [45,46], and graph-based
SLAM [47,48], emphasizing their efficacy in mitigating difficulties such as drift, signal
degradation, and noise. We evaluate contemporary multimodal sensor fusion techniques
that include IMUs, Doppler velocity logs, sonar, cameras, and LiDAR, providing improved
resilience and precision in practical applications. Innovations in quantum sensing and
artificial intelligence (AI)-driven [49–53] adaptation filtering, including reinforcement learn-
ing and deep learning, are examined as potential transformative solutions for real-time
adaptability in underwater environments.

The organized study on underwater SLAM with sensor fusion approaches, advanced
computational frameworks, and new technologies like quantum sensors and AI describes
current and future underwater navigation advances. The Introduction discusses underwa-
ter obstacles like low visibility and no GPS and how sensor fusion improves SLAM accuracy.
Proprioceptive and exteroceptive sensors are crucial to underwater SLAM, as discussed in
Section 2. Section 3 discusses the pros and cons of multiple sensor integration in SLAM
odometry. Section 4 compares Kalman filters, particle filters, and graph-based SLAM
for sensor fusion, including computing requirements, accuracy, and optimal applications.
Section 5 examines computational efficiency, optimizing processing speed and memory for

Sensors 2024, 24, 7490

3 of 31

real-time underwater SLAM. In Section 6, case studies present experimental outcomes from
military, industrial, and environmental studies. Future directions include hybrid quantum–
AI models, deep learning, and computational optimizations for resilient, adaptable SLAMs
in complicated underwater environments. The Conclusion concludes that sensor fusion
and AI-driven SLAM technology can transform UUV underwater exploration.

The following section discusses SLAM sensors and how proprioceptive and exterocep-
tive technologies enable navigation and mapping in complicated aquatic settings to handle
underwater issues.

2. Essential Underwater Sensors and Their Function in Facilitating Improved
SLAM Systems

Underwater sensors are specialized instruments designed to monitor various physical
and environmental characteristics, enabling effective data collecting and navigation in intri-
cate and dynamic underwater environments. These sensors are essential for underwater
exploration, facilitating autonomous underwater vehicles (AUVs) and remotely operated
vehicles (ROVs) to collect real-time data for navigation and mapping. The underwater
sensor systems are classified into proprioceptive sensors and exteroceptive sensors, as
detailed in the subsequent section.

2.1. Proprioceptive Sensors

Proprioceptive sensors like accelerometers [54], gyroscopes, and magnetometers mea-
sure location, velocity, acceleration, and rotation to reveal a system’s internal state and
motion. These sensors include accelerometers, gyroscopes, magnetometers, and others,
all of which play vital roles in UUV navigation and control systems. Underwater vehicles
require depth sensors, such as barometers, for navigation and measurement purposes.
Barometers, a category of pressure sensors, gauge depth by assessing the pressure im-
posed by the water column above the sensor. Precise depth measurements are essential for
sustaining the intended altitude during underwater operations.

DVL utilizes acoustic measurements to ascertain a UUV velocity concerning the
seafloor. They are essential for dead reckoning, supplying velocity and positional data
when GPS or alternative navigation signals are inaccessible, as in deep-sea exploration.
Inertial measurement units (IMUs) [55–59] combine accelerometers, gyroscopes, and mag-
netometers to measure linear acceleration, angular velocity, and orientation. These sensors
provide continuous feedback on the AUV’s movement, making them indispensable for
maintaining precise navigation and orientation in challenging environments. IMUs have
been extensively employed in aircraft navigation, mobile devices, and underwater robotics
due to their ability to operate independently of external signals.

Acoustic Doppler current profilers (ADCPs) measure water current velocities using
the Doppler effect. This information is essential for correcting navigation errors caused by
underwater currents and maintaining precise control of UUV motion. Inclinometer sensors
measure tilt or inclination angles, allowing UUVs to maintain balance and control in uneven
or rugged underwater terrain. Thermocouples used for temperature measurement play a
crucial role in environmental monitoring, helping AUVs navigate through thermoclines or
temperature gradients in the water column.

Figure 1 depicts the standard proprioceptive sensors utilized for underwater nav-
igation. The sensors comprise compasses (susceptible to magnetic field interference);
barometers (for depth assessment); DVLs for acoustic velocity evaluation; IMUs integrating
accelerometers, gyroscopes, and magnetometers; acoustic Doppler current profilers (AD-
CPs for current velocity measurement); inclinometers (for tilt detection); and thermocouples
(for temperature assessment). Every sensor enhances efficient underwater navigation and
environmental awareness.

Sensors 2024, 24, 7490

4 of 31

Figure 1. Proprioceptive sensors for aquatic navigation.

2.2. Exteroceptive Sensors

Exteroceptive sensors gather information from the environment, enabling UUVs to
sense and map their surroundings. These sensors include cameras, sonar, and LiDAR, each
contributing unique data points that help build a comprehensive understanding of the
underwater world.

Figure 2 provides a visual depiction of an underwater SLAM system architecture,
illustrating the sequential modules involved in feature tracking and environmental recon-
struction. The system commences with the Underwater Camera Sensors Module, succeeded
by the Underwater Front-End for feature tracking. The Back-End Module facilitates sup-
plementary feature tracking, while the Loop Closing Module enables mistake correction.
The procedure concludes with the Mapping Module, which is tasked with environment
reconstruction, facilitating precise underwater navigation.

Figure 2. The typical architecture of a visual SLAM system.

Sensors 2024, 24, 7490 4 of 32   integrating accelerometers, gyroscopes, and magnetometers; acoustic Doppler current proﬁlers (ADCPs for current velocity measurement); inclinometers (for tilt detection); and thermocouples (for temperature assessment). Every sensor enhances eﬃcient underwater navigation and environmental awareness.  Figure 1. Proprioceptive sensors for aquatic navigation. 2.2. Exteroceptive Sensors Exteroceptive sensors gather information from the environment, enabling UUVs to sense and map their surroundings. These sensors include cameras, sonar, and LiDAR, each contributing unique data points that help build a comprehensive understanding of the underwater world. Figure 2 provides a visual depiction of an underwater SLAM system architecture, illustrating the sequential modules involved in feature tracking and environmental reconstruction. The system commences with the Underwater Camera Sensors Module, succeeded by the Underwater Front-End for feature tracking. The Back-End Module facilitates supplementary feature tracking, while the Loop Closing Module enables mistake correction. The procedure concludes with the Mapping Module, which is tasked with environment reconstruction, facilitating precise underwater navigation. Visual SLAM uses numerous camera types [60,61] to perceive the surroundings. Monocular cameras [62,63] compute 3D structures from 2D input and set initial distances depending on relative motion [64]. Parallax depth calculations allow stereo cameras [65,66] to localize underwater accurately. They use novel topological representations for real-time processing [67]. RGB-D depth cameras estimate distances using structured light or time of ﬂight. They have limited range, high noise, and translucent material issues but require less processing power than software-based approaches [68]. Data transmission begins after UUV camera picture acquisition, as in Figure 3. Image processing improves visual clarity, removes noise, and corrects distortions in transmitted data. After processing, the photos are used for environmental analysis, which comprises recognizing impediments, identifying items, and mapping the investigated area. The data are used for navigation and decision making. Sensors 2024, 24, 7490 5 of 32    Figure 2. The typical architecture of a visual SLAM system.  Figure 3. UUV camera image processing ﬂowchart. Active and passive sonar sensors detect underwater sound waves. Active sonar searches and positions underwater, whereas passive sonar tracks target distances. Water turbidity does not alter single-beam sonar distance information over many meters. For high-resolution 3D mapping, multi-beam sonar measures bottom depth quickly and accurately using many beams. Wrecks and mines are often detected using side-scan sonar, which provides high-resolution seaﬂoor morphology images. Underwater camera sensors module Underwater front-end (feature tracking)Back-end module (feature tracking)Loop closing module (error correction)Mapping module (environment  reconstruction) UUV cameraImage acquisitionImage processingData transmissionVisual qualityEnvironment analysisRemove noiseDistortions correctionsAnalyze underwaterDetect obstaclesNavigation and decision makingObject identificcationMap of the explored areaYesoptimizatiionNoSensors 2024, 24, 7490

5 of 31

Visual SLAM uses numerous camera types [60,61] to perceive the surroundings.
Monocular cameras [62,63] compute 3D structures from 2D input and set initial distances
depending on relative motion [64].

Parallax depth calculations allow stereo cameras [65,66] to localize underwater accu-

rately. They use novel topological representations for real-time processing [67].

RGB-D depth cameras estimate distances using structured light or time of flight. They
have limited range, high noise, and translucent material issues but require less processing
power than software-based approaches [68].

Data transmission begins after UUV camera picture acquisition, as in Figure 3. Image
processing improves visual clarity, removes noise, and corrects distortions in transmitted
data. After processing, the photos are used for environmental analysis, which comprises
recognizing impediments, identifying items, and mapping the investigated area. The data
are used for navigation and decision making.

Figure 3. UUV camera image processing flowchart.

Active and passive sonar sensors detect underwater sound waves. Active sonar
searches and positions underwater, whereas passive sonar tracks target distances. Water
turbidity does not alter single-beam sonar distance information over many meters. For high-
resolution 3D mapping, multi-beam sonar measures bottom depth quickly and accurately
using many beams. Wrecks and mines are often detected using side-scan sonar, which
provides high-resolution seafloor morphology images.

Each sonar type possesses unique functions tailored to particular underwater appli-
cations. Active sonar transmits sound pulses to deliver accurate location and distance
information, rendering it suitable for extensive searches in diverse aquatic environments.
Conversely, passive sonar is undetected as it captures noises from moving objects, rendering
it invaluable for covert tracking.

Sensors 2024, 24, 7490 5 of 32    Figure 2. The typical architecture of a visual SLAM system.  Figure 3. UUV camera image processing ﬂowchart. Active and passive sonar sensors detect underwater sound waves. Active sonar searches and positions underwater, whereas passive sonar tracks target distances. Water turbidity does not alter single-beam sonar distance information over many meters. For high-resolution 3D mapping, multi-beam sonar measures bottom depth quickly and accurately using many beams. Wrecks and mines are often detected using side-scan sonar, which provides high-resolution seaﬂoor morphology images. Underwater camera sensors module Underwater front-end (feature tracking)Back-end module (feature tracking)Loop closing module (error correction)Mapping module (environment  reconstruction) UUV cameraImage acquisitionImage processingData transmissionVisual qualityEnvironment analysisRemove noiseDistortions correctionsAnalyze underwaterDetect obstaclesNavigation and decision makingObject identificcationMap of the explored areaYesoptimizatiionNoSensors 2024, 24, 7490

6 of 31

Specialized sonar types are essential: single-beam sonar provides accurate distance
readings in murky seas, facilitating long-range detection. Multi-beam sonar excels at three-
dimensional mapping by acquiring intricate depth data across vast regions using numerous
beams. Side-scan sonar provides high-resolution views of seafloor morphology, facilitating
structural analysis for environmental evaluations and danger identification.

Figure 4 depicts the conversion of electrical energy into mechanical energy via sonar
transducers, resulting in the transmission of sound waves underwater. The interaction of
these waves with subaqueous objects and marine organisms leads to scattering, refraction,
and reflection. Reflected waves are subsequently received as echoes, analyzed, and utilized
for data implementation, so concluding the sonar operational cycle.

Figure 4. Sonar system in UUV navigation.

2.3. LiDAR Technology

Even in harsh underwater environments, LiDAR sensors provide reliable, high-
frequency range data. The high 3D data resolution in texture-limited underwater sceneries
includes point cloud data for SLAM systems. LiDAR improves navigational maps by
developing 3D models and detecting items on the bottom [69,70].

Figure 5 shows the underwater LiDAR system’s sequential operation. Laser systems
are emitted, propagate through water, interact with an underwater object, and then are
used for navigation and mapping. The LiDAR sensor detects and analyzes reflections to
provide a 3D representation and navigational outputs.

Sensors 2024, 24, 7490 6 of 32   Each sonar type possesses unique functions tailored to particular underwater applications. Active sonar transmits sound pulses to deliver accurate location and distance information, rendering it suitable for extensive searches in diverse aquatic environments. Conversely, passive sonar is undetected as it captures noises from moving objects, rendering it invaluable for covert tracking. Specialized sonar types are essential: single-beam sonar provides accurate distance readings in murky seas, facilitating long-range detection. Multi-beam sonar excels at three-dimensional mapping by acquiring intricate depth data across vast regions using numerous beams. Side-scan sonar provides high-resolution views of seaﬂoor morphology, facilitating structural analysis for environmental evaluations and danger identiﬁcation. Figure 4 depicts the conversion of electrical energy into mechanical energy via sonar transducers, resulting in the transmission of sound waves underwater. The interaction of these waves with subaqueous objects and marine organisms leads to scattering, refraction, and reﬂection. Reﬂected waves are subsequently received as echoes, analyzed, and utilized for data implementation, so concluding the sonar operational cycle.  Figure 4. Sonar system in UUV navigation. 2.3. LiDAR Technology Even in harsh underwater environments, LiDAR sensors provide reliable, high-frequency range data. The high 3D data resolution in texture-limited underwater sceneries SonarSonar traducersElectrical energyMechanical energyPropagation of sound waves Underwater structures, marine life etc..ScatteringRefractionReflectionEcho receptionSignal processingData implementa-tionSensors 2024, 24, 7490

7 of 31

Figure 5. Underwater LiDAR system.

This graphic in Figure 6 classifies several types of exteroceptive sensors utilized in
underwater settings. Visual sensors, sonar sensors, and LiDAR technology yield several
data types, encompassing optical imaging, range measurements, and three-dimensional
mapping. Hydrophones facilitate passive acoustic monitoring, whereas laser line scanners
assist in high-resolution mapping and imaging. Each sensor type fulfills a distinct function
in improving environmental awareness for underwater applications.

Figure 6. Exteroceptive sensor overview.

Sensors 2024, 24, 7490 7 of 32   includes point cloud data for SLAM systems. LiDAR improves navigational maps by developing 3D models and detecting items on the bottom [69,70]. Figure 5 shows the underwater LiDAR system’s sequential operation. Laser systems are emitted, propagate through water, interact with an underwater object, and then are used for navigation and mapping. The LiDAR sensor detects and analyzes reﬂections to provide a 3D representation and navigational outputs. LiDAR sensorEmission of laser pulsesPropagation trough waterUnderwater objectReflection from the objectPoint cloud processing3D representationNavigation and mappingDetection of return pulses Figure 5. Underwater LiDAR system. This graphic in Figure 6 classiﬁes several types of exteroceptive sensors utilized in underwater settings. Visual sensors, sonar sensors, and LiDAR technology yield several data types, encompassing optical imaging, range measurements, and three-dimensional mapping. Hydrophones facilitate passive acoustic monitoring, whereas laser line scanners assist in high-resolution mapping and imaging. Each sensor type fulﬁlls a distinct function in improving environmental awareness for underwater applications. The previous section covered underwater SLAM sensors’ types, capabilities, and applications in complex situations. On this basis, the next part discusses how integrating numerous sensors improves SLAM accuracy, resilience, and ﬂexibility in harsh underwater circumstances. Sensors 2024, 24, 7490 8 of 32    Figure 6. Exteroceptive sensor overview. 3. Multiple Sensor Integration in SLAM Odometry: Strengths and Weaknesses Numerous scientiﬁc investigations indicate that SLAM odometry beneﬁts from incorporating many sensors, providing notable advantages and certain limitations. A signiﬁcant advantage is the improved durability and precision in a wide range of challenging and intricate settings. Integrating LiDAR with inertial measurement units (IMUs) and optical sensors dramatically enhances the accuracy of mapping and localization, particularly in dynamic environments with ﬂuctuating elements such as pedestrians and cars [71]. In outdoor contexts, incorporating geometric and textural data from LiDAR, IMU, wheel encoder, GPS, and road network data improves localization and mapping accuracy. In interior locations where budget constraints prohibit 3D LiDAR use, a multisensor fusion system employing 2D LiDAR, IMU, and wheel odometry can handle motion degeneracy and geometrically comparable environments, improving robustness and precision [72]. Tightly coupled systems integrating LiDAR, inertial, and visual data use error state iterative Kalman ﬁlters and factor graph optimization for real-time error correction and accurate transformation estimate [73]. Multiple LiDAR sensors, including solid-state and spinning LiDARs, improve the robot’s perception by acquiring a high robot ‘station map and accomplishing low-drift ego estimation in featureless interior environments. The complementarity of sensors, such as IMUs’ high-frequency output for rapid handling and cameras’ feature tracking to counter cameras’ drift, makes SLAM systems more robust and able to adapt to unexpected and dynamic surroundings [74]. The complexity and processing eﬀort required to integrate and fuse data from numerous sources are drawbacks of multisensor integration [75]. Using a magnetometer, odometer, and IMU data to improve LiDAR-based SLAM systems in feature-sparse settings requires complex algorithms [76] and factor graph optimization, which can be computationally intensive [77]. Multi-camera [78,79] systems provide rich environmental information and improved feature matching, but dynamic content and changing illumination conditions require advanced techniques like semantic-guided synthetic aperture imaging to maintain accuracy [80]. Multisensor integration [81] in SLAM odometry improves robustness and precision but requires careful computational resources and algorithmic complexity management. Researchers fuse sensors to improve underwater SLAM systems’ accuracy and robustness. The system method improves underwater SLAM precision and resilience. Vision-Inertial [82], Laser-Vision, and multisensor SLAM are standard approaches [83,84,85]. Multisensor fusion [86,87] has three fusion layers: data, feature, and decision. Sensors 2024, 24, 7490

8 of 31

The previous section covered underwater SLAM sensors’ types, capabilities, and
applications in complex situations. On this basis, the next part discusses how integrating
numerous sensors improves SLAM accuracy, resilience, and flexibility in harsh underwa-
ter circumstances.

3. Multiple Sensor Integration in SLAM Odometry: Strengths and Weaknesses

Numerous scientific investigations indicate that SLAM odometry benefits from incor-
porating many sensors, providing notable advantages and certain limitations. A significant
advantage is the improved durability and precision in a wide range of challenging and
intricate settings. Integrating LiDAR with inertial measurement units (IMUs) and optical
sensors dramatically enhances the accuracy of mapping and localization, particularly in
dynamic environments with fluctuating elements such as pedestrians and cars [71]. In
outdoor contexts, incorporating geometric and textural data from LiDAR, IMU, wheel
encoder, GPS, and road network data improves localization and mapping accuracy. In
interior locations where budget constraints prohibit 3D LiDAR use, a multisensor fusion
system employing 2D LiDAR, IMU, and wheel odometry can handle motion degeneracy
and geometrically comparable environments, improving robustness and precision [72].
Tightly coupled systems integrating LiDAR, inertial, and visual data use error state iterative
Kalman filters and factor graph optimization for real-time error correction and accurate
transformation estimate [73]. Multiple LiDAR sensors, including solid-state and spinning
LiDARs, improve the robot’s perception by acquiring a high robot ‘station map and accom-
plishing low-drift ego estimation in featureless interior environments. The complementarity
of sensors, such as IMUs’ high-frequency output for rapid handling and cameras’ feature
tracking to counter cameras’ drift, makes SLAM systems more robust and able to adapt to
unexpected and dynamic surroundings [74].

The complexity and processing effort required to integrate and fuse data from nu-
merous sources are drawbacks of multisensor integration [75]. Using a magnetometer,
odometer, and IMU data to improve LiDAR-based SLAM systems in feature-sparse settings
requires complex algorithms [76] and factor graph optimization, which can be computation-
ally intensive [77]. Multi-camera [78,79] systems provide rich environmental information
and improved feature matching, but dynamic content and changing illumination con-
ditions require advanced techniques like semantic-guided synthetic aperture imaging
to maintain accuracy [80]. Multisensor integration [81] in SLAM odometry improves
robustness and precision but requires careful computational resources and algorithmic
complexity management.

Researchers fuse sensors to improve underwater SLAM systems’ accuracy and robust-
ness. The system method improves underwater SLAM precision and resilience. Vision-
Inertial [82], Laser-Vision, and multisensor SLAM are standard approaches [83–85]. Mul-
tisensor fusion [86,87] has three fusion layers: data, feature, and decision. Although
visual SLAM algorithms have improved, they still struggle with low-quality images from
rapid camera motions and changing light. Compared to odometers, IMU-assisted sensors
improve angular velocity and local location precision, improving SLAM performance
cost-effectively. Loosely coupled visual-inertial fusion approaches estimate IMU and cam-
era [88] motions separately and subsequently fuse them, while tightly coupled methods
establish motion and observation equations before state estimation.

The data gathered from these sensors are processed and merged through sophisticated
sensor fusion techniques, yielding actionable information for underwater SLAM applica-
tions. The fusion system integrates data types such as motion, range, 3D mapping [89],
visual data, velocity, depth, temperature, and auditory data, guaranteeing precise and
dependable navigation in real time. The subsequent session will cover the fundamental
fusion techniques employed in underwater multisensor fusion [90].

After discussing the pros and cons of combining many sensors in SLAM odom-
etry, we will examine the fusion methods and computational strategies that enable it.
Section 4 analyses Kalman filters, particle filters, graph-based SLAM, and other sensor fu-

Sensors 2024, 24, 7490

9 of 31

sion approaches, including their mathematical foundations, computational trade-offs, and
applicability for underwater environments. This foundation allows us to assess how quan-
tum sensors and AI-driven fusion improve SLAM accuracy and resilience in complicated
underwater environments.

4. Assessing Sensor Fusion Techniques: Efficacy, Intricacy, and Enhancement in
Underwater SLAM
4.1. Sensor Fusion Methodologies

Sensor fusion integrates input from several sensors to enhance the accuracy and
dependability of state estimates in SLAM systems [91]. In a SLAM system, the state denotes
the collection of variables that encapsulate the system’s comprehension of its position,
orientation, velocity, and environmental map [92]. The states can be classified into two
categories: navigation state and map state.

The navigation state encompasses the system’s position, velocity, and orientation—
parameters that delineate the vehicle or robot’s location and movement within space. In
underwater SLAM, the navigation state encompasses the coordinates of an underwater
vehicle, its orientation (often represented as a rotation matrix or quaternion), and its velocity.
The navigation state is often compact and updated in real time as the system progresses.

Conversely, the map state encompasses the characteristics or landmarks in the environ-
ment that the system has detected. In underwater SLAM, this may pertain to the locations
of sonar-detected entities or keyframe orientations. The map state is generally far larger
than the navigation state and expands over time as additional characteristics are identified
or the system investigates new regions. The intricacy of the map state may fluctuate based
on the system and setting; nevertheless, it often necessitates more advanced methodologies
for estimation, especially as the map expands.

Sensor fusion methodologies are utilized to ascertain the two states—navigation and
mapping—by synthesizing data from diverse sensors, including IMUs (inertial measure-
ment units), sonar, DVLs (Doppler velocity logs), and cameras. The difficulty in sensor
fusion is integrating data from several sensors while considering their specific errors,
noise, and biases. Four principal sensor fusion methods employed in SLAM systems are
Kalman filters (KFs), extended Kalman filters (EKFs), particle filters (PFs), and Graph-
SLAM. Each method possesses distinct advantages and disadvantages, contingent upon
the characteristics of the system dynamics, the nature of the sensor data, and the surround-
ing environment.

a. Kalman Filters

KF are among the most prevalent sensor fusion methodologies, particularly when
both the system dynamics and sensor models exhibit linearity, as well as when the noise
inside the system is Gaussian [93]. The Kalman filter is frequently employed to assess
the navigation state, including position, velocity, and orientation, through the recursive
refinement of the state estimate utilizing new sensor data. The KF algorithm functions
by forecasting the system’s condition at each time interval and subsequently refining that
forecast upon receiving additional data.

The principal benefit of the KF lies in its capacity to integrate predictions with observa-
tions in a statistically optimal fashion. In underwater SLAMs, for instance, the Kalman filter
may integrate input from sensors such as IMUs, sonar, and DVLs to ascertain the position
and velocity of an underwater vehicle [94–96]. This is effective when the system adheres to
linear dynamics and the measurements are affected by Gaussian noise [40,97–100].

The KF algorithm operates in two primary phases: prediction and updating.
Prediction: The Kalman filter predicts the state at time t using the previous state xt−1

and control input ut:

where

xt is the state at time t;

xt = Ftxt−1+Btut + wt

(1)

Sensors 2024, 24, 7490

10 of 31

Ft is the state transition matrix;
Bt is the control input matrix;
ut is the control input;
wt is the process noise (assumed to be Gaussian).

Update: Upon the availability of new sensor measurements zt, the filter revises the
anticipated state. The update phase integrates the Kalman gain Kt, which reconciles the
forecast with the measurement:

Kt= P−

t HT

t (HtP−

t HT
(cid:0)zt − Htx−

t +R)−1
(cid:1)

t

xt= x−

t + Kt

where

Kt is the Kalman gain;
P−
is the predicted covariance;
t
Ht is the measurement matrix;
R is the measurement noise covariance;
x−
t

is the predicted state estimate.

(2)

(3)

This iterative procedure enables the Kalman filter to perpetually enhance the system’s

state estimation by utilizing new information.

b.

Extended Kalman Filters

The EKF augments the Kalman filter to accommodate non-linear system dynamics and
measurement models. Although the KF presumes that both the system and measurement
models are linear, the EKF can linearize these models based on the current state estima-
tion [101,102]. The EKF is appropriate for intricate, non-linear systems frequently found
in real-world SLAM applications, including underwater or aerial vehicles with dynamic
motion models and non-linear sensor readings [103,104].

The EKF operates analogously to the KF, with a principal distinction: it linearizes the

system and measurement models utilizing Jacobian matrices at each time increment.

Forecast of state: The state prediction in the EKF adheres to a similar structure as in

the KF, while incorporating non-linear system dynamics.

xt = f(xt−1,ut)+wt

(4)

where f(xt−1,ut) is the non-linear state transition function.

Jacobian matrices: To linearize the system, the EKF calculates the Jacobian matrices of

the state transition and measurement functions.

Ft =

∂f(xt−1,ut)
∂xt−1

Ht=

∂h(x t)
∂xt

(5)

(6)

where ft and ht are the non-linear state transition and measurement functions, and Ft and
Ht are their Jacobians.

Update: The update phase in the EKF resembles that of the KF but utilizes lin-

earized models.

Kt= P−
xt= x−

t HT
t + Kt

t (HtP−

t HT
(cid:0)zt − h(cid:0)x−

t +R)−1
(cid:1) (cid:1)

t

(7)

(8)

Jacobian matrices enable the Extended Kalman filter to manage non-linearities; how-
ever, this introduces increased computational complexity and the risk of inferior perfor-
mance if the linearization inadequately approximates the actual non-linearity.

c.

Particle Filters

Sensors 2024, 24, 7490

11 of 31

PFs, or sequential Monte Carlo (SMC) approaches, are an effective technique for
predicting the state of systems characterized by non-linear dynamics and non-Gaussian
noise. Particle filtering is especially advantageous when the system’s state distribution is
multimodal, complicating approximation using a singular Gaussian distribution as utilized
in Kalman filtering and extended Kalman filtering [105].

In PFs, the state is shown by a collection of particles, with each particle symbolizing a
potential state of the system [106]. The filter operates by advancing the particles through
time according to the system’s dynamics and adjusting their weights in response to sensor
measurements [107].

Forecast: Each particle is advanced according to the system’s dynamics and control input.

(cid:16)

(i)
t = f

x

x

(i)
t−1,

ut

(cid:17)

+w

(i)
t

(9)

where w

(i)
t

is the process noise for particle i.

Update: The weight of each particle is adjusted according to the probability of the

measurement relative to the particle’s anticipated state:

w

(i)
t = w

(i)
t−1 ∗ p(zt|x

(i)
t )

(10)

where p(zt|x

(i)
t

(i)
) is the likelihood of the measurement zt given the predicted state x
t

.

After the adjustment of particle weights, the system executes resampling to produce a

fresh collection of particles, emphasizing those with elevated weights.

d. Graph-SLAM

Graph-SLAM is a global optimization method for SLAM that constructs a graph of
robot poses and observed landmarks. This method utilizes graph vertices to denote the
robot’s poses, encompassing its positions and orientations at various time intervals, as well
as the landmarks, which are features or observable items inside the environment [108–110].
The edges signify the constraints between these postures and landmarks, usually obtained
from sensor data (e.g., range, bearing) or odometry.

The objective of Graph-SLAM is to determine the arrangement of poses and landmarks
that optimize the likelihood of the observed data while adhering to the limitations [111,112].
This procedure often entails optimizing a nonlinear least-squares cost function, which
modifies the postures and landmarks to reduce the discrepancy between predicted and
observed sensor values [108,109,113].

The optimization problem is articulated as follows:

min
x

∑
i,j

||h(xi , xj) − zij||2

(11)

where

xi, xj represent the robot poses at time steps i and j, h(x i, xj

(cid:1) is a function that predicts
the relative measurement between two poses, and zij is the actual measurement between
the poses.

The sum is over all pairs of poses i and j that are connected by a measurement constraint.
In Graph-SLAM, the relative measurements zij are often derived from sensor data
(cid:1) captures
(such as laser range finders, sonar, or stereo cameras). The function h(x i, xj
the expected measurement based on the relative poses xi and xj. The optimization aims
to reduce the discrepancy between predicted and actual measurements for all pairs of
interconnected poses and landmarks.

Graph-SLAM is very advantageous for extensive mapping settings and prolonged
robotic operations. It can process substantial volumes of sensor data and measurements,
facilitating a comprehensive optimization of the robot’s course and the map. This method
necessitates substantial processing resources for optimization, particularly as the number
of postures and landmarks increases [114–116].

Sensors 2024, 24, 7490

12 of 31

The optimization procedure frequently employs techniques such as Gauss–Newton or
Levenberg–Marquardt to iteratively enhance the robot’s trajectory and the environmental
map. The algorithm optimizes the poses and landmarks by minimizing the nonlinear
least-squares error, iteratively refining the configuration until convergence is achieved.

4.2. Comparative Analysis of Sensor Fusion Techniques and Emerging Technologies for
Underwater SLAM

The graphic in Figure 7 depicts a graph-based [47,48,117,118] SLAM representation,
with each node representing a pose of the UUV throughout its course. The edges connecting
nodes signify relative pose restrictions obtained from sensor data, like sonar or LiDAR,
utilized for localization and mapping [119,120]. The graph structure illustrates how sensor
fusion in SLAM amalgamates spatial links between successive UUV points to create an
optimized map. These correlations mitigate drift and enhance accuracy in demanding un-
derwater conditions where GPS signals are inaccessible. This visual depiction underscores
the essential function of graph-based SLAM in ensuring reliable navigation and precise
mapping over extended missions.

Figure 7. Graph representation of pose constraints.

a. Complexity analysis and quantitative evaluation

The computing complexity as detailed in Table 1 of each approach varies considerably
depending on the environment and the quantity of integrated sensor modalities. The
following table delineates the trade-offs among various methods:

Table 1. Comparative analysis of sensor fusion methods for SLAM: Benefits, drawbacks, and
applications.

Method

Advantages

Disadvantages

Computational
Complexity

Optimal Application
Scenario

KF

EKF

PF

Effective for Gaussian
noise linear systems

Addresses non-linearities
in sensor data

Problems with
non-linearities and
non-Gaussian noise

Resource-intensive owing
to the computation of the
Jacobian

O(n2)

O(n3)

Effectively functions in
non-Gaussian, nonlinear
contexts

Necessitates numerous
particles; computationally
intensive

O(N·M)

Low sensor noise, relatively
stable settings [22,27,95,116]

Nonlinear environments
characterized by moderate
dynamics [44]

Underwater dynamics and
uncertainty [45]

Sensors 2024, 24, 7490 12 of 32   min(cid:2934)(cid:3533)||h (cid:4666)x(cid:2919)(cid:2919),(cid:2920),x(cid:2920)(cid:4667) (cid:3398) z(cid:2919)(cid:2920)||(cid:2870)  (11)where x(cid:2919),x(cid:2920) represent the robot poses at time steps i and j, h(cid:4666)x(cid:2919),x(cid:2920)(cid:4667) is a function that predicts the relative measurement between two poses, and z(cid:2919)(cid:2920) is the actual measurement between the poses. The sum is over all pairs of poses i and j that are connected by a measurement constraint. In Graph-SLAM, the relative measurements z(cid:2919)(cid:2920) are often derived from sensor data (such as laser range ﬁnders, sonar, or stereo cameras). The function h(cid:4666)x(cid:2919),x(cid:2920)(cid:4667) captures the expected measurement based on the relative poses x(cid:2919) and x(cid:2920) . The optimization aims to reduce the discrepancy between predicted and actual measurements for all pairs of interconnected poses and landmarks. Graph-SLAM is very advantageous for extensive mapping settings and prolonged robotic operations. It can process substantial volumes of sensor data and measurements, facilitating a comprehensive optimization of the robot’s course and the map. This method necessitates substantial processing resources for optimization, particularly as the number of postures and landmarks increases [114,115,116]. The optimization procedure frequently employs techniques such as Gauss–Newton or Levenberg–Marquardt to iteratively enhance the robot’s trajectory and the environmental map. The algorithm optimizes the poses and landmarks by minimizing the nonlinear least-squares error, iteratively reﬁning the conﬁguration until convergence is achieved. 4.2. Comparative Analysis of Sensor Fusion Techniques and Emerging Technologies for Underwater SLAM The graphic in Figure 7 depicts a graph-based [47,48,117,118] SLAM representation, with each node representing a pose of the UUV throughout its course. The edges connecting nodes signify relative pose restrictions obtained from sensor data, like sonar or LiDAR, utilized for localization and mapping [119,120]. The graph structure illustrates how sensor fusion in SLAM amalgamates spatial links between successive UUV points to create an optimized map. These correlations mitigate drift and enhance accuracy in demanding underwater conditions where GPS signals are inaccessible. This visual depiction underscores the essential function of graph-based SLAM in ensuring reliable navigation and precise mapping over extended missions.  Figure 7. Graph representation of pose constraints. Sensors 2024, 24, 7490

13 of 31

Table 1. Cont.

Method

Advantages

Disadvantages

Computational
Complexity

Optimal Application
Scenario

Graph-based SLAM

Very accurate large-scale
mapping, especially loop
closure

CPU-intensive for real-time
operation

O(n3) to O(n4)

Hybrid methods

Integrates the advantages
of many filters

Augmented complexity
and possible overhead

Variable

Deep learning
approaches

Ability to learn complex
sensor data
representations

Ability to learn complex
sensor data representations

Variable

Large-scale settings needing
precise long-term mapping
[47,48]

Environments characterized
by fluctuating dynamics and
uncertainty [121–125]

Underwater environments
that are complex and
data-rich [126–128]

b. Quantitative evaluation of sensor fusion techniques

In assessing the practical efficacy of diverse sensor fusion methodologies for underwa-
ter SLAM, several critical metrics can be employed to gauge their usefulness, including
error rate (RMSE), computational load, and drift over time. These measurements offer
insights into the compromises among accuracy, computational complexity, and practical
usefulness. The table below consolidates data from many case studies, emphasizing promi-
nent sensor fusion techniques’ comparative advantages and disadvantages, including KF,
EKF, particle filters, and graph-based SLAM [129]. Each method is evaluated according to
its standard performance in simulated and real-world contexts.

Note: Figures 8–12 are artistic depictions derived from a synthesis of literature findings.
These figures are not based on genuine experimental data or particular calculations. They
function as conceptual summaries of overarching trends and attributes documented in prior
research, providing visual insight into the relative strengths and weaknesses of diverse
sensor fusion methodologies across varying environmental situations.

Figure 8. Accuracy of sensor fusion techniques in subaqueous environments.

This graphic in Figure 9 displays a comparative evaluation of the robustness of four
sensor fusion approaches. Robustness is evaluated on a scale from 1 to 5, with elevated
values indicating enhanced resilience to environmental disruptions, including reduced visi-
bility and turbulence. This image is an example overview synthesized from the literature,
not based on real experimental data.

Sensors 2024, 24, 7490 14 of 32    Figure 8. Accuracy of sensor fusion techniques in subaqueous environments. This graphic in Figure 9 displays a comparative evaluation of the robustness of four sensor fusion approaches. Robustness is evaluated on a scale from 1 to 5, with elevated values indicating enhanced resilience to environmental disruptions, including reduced visibility and turbulence. This image is an example overview synthesized from the literature, not based on real experimental data.  Figure 9. Assessment of the robustness of sensor fusion techniques. Recent works have examined Kalman ﬁlters, particle ﬁlters, and graph-based SLAM approaches to handle the unique problems of dynamic underwater settings. Due to environmental factors such as ﬂuctuating currents and turbidity and the lack of GPS, these old methods are limited in adaptability and accuracy. In real-time applications, where quick and adaptable decision making is crucial, these methods are computationally intensive. This ﬁgure is a synthesis of literature ﬁndings that serve as an illustrative summary and are not derived from original experimental data. Sensors 2024, 24, 7490

14 of 31

Figure 9. Assessment of the robustness of sensor fusion techniques.

Figure 10. Comparing the performance of AI-driven and conventional sensor fusion techniques for
underwater SLAM systems. Not obtained from actual experimental data, this chart is an indicative
summary based on a synthesis of literary results.

Figure 11. Localization drift in GPS-disabled environments: comparing quantum and conventional
sensors. This image is an illustrative summary based on a synthesis of published findings rather than
original experimental data.

Sensors 2024, 24, 7490 14 of 32    Figure 8. Accuracy of sensor fusion techniques in subaqueous environments. This graphic in Figure 9 displays a comparative evaluation of the robustness of four sensor fusion approaches. Robustness is evaluated on a scale from 1 to 5, with elevated values indicating enhanced resilience to environmental disruptions, including reduced visibility and turbulence. This image is an example overview synthesized from the literature, not based on real experimental data.  Figure 9. Assessment of the robustness of sensor fusion techniques. Recent works have examined Kalman ﬁlters, particle ﬁlters, and graph-based SLAM approaches to handle the unique problems of dynamic underwater settings. Due to environmental factors such as ﬂuctuating currents and turbidity and the lack of GPS, these old methods are limited in adaptability and accuracy. In real-time applications, where quick and adaptable decision making is crucial, these methods are computationally intensive. This ﬁgure is a synthesis of literature ﬁndings that serve as an illustrative summary and are not derived from original experimental data. Sensors 2024, 24, 7490 15 of 32 Figure 10. Comparing the performance of AI-driven and conventional sensor fusion techniques for underwater SLAM systems. Not obtained from actual experimental data, this chart is an indicative summary based on a synthesis of literary results. Figure 11. Localization drift in GPS-disabled environments: comparing quantum and conventional sensors. This image is an illustrative summary based on a synthesis of published ﬁndings rather than original experimental data. Figure 12. Comparison of the mapping precision of single and multisensor fusion for SLAM systems. This graphic shows a literature synthesis, not experimental data. Sensors 2024, 24, 7490 15 of 32 Figure 10. Comparing the performance of AI-driven and conventional sensor fusion techniques for underwater SLAM systems. Not obtained from actual experimental data, this chart is an indicative summary based on a synthesis of literary results. Figure 11. Localization drift in GPS-disabled environments: comparing quantum and conventional sensors. This image is an illustrative summary based on a synthesis of published ﬁndings rather than original experimental data. Figure 12. Comparison of the mapping precision of single and multisensor fusion for SLAM systems. This graphic shows a literature synthesis, not experimental data. Sensors 2024, 24, 7490

15 of 31

Figure 12. Comparison of the mapping precision of single and multisensor fusion for SLAM systems.
This graphic shows a literature synthesis, not experimental data.

Recent works have examined Kalman filters, particle filters, and graph-based SLAM
approaches to handle the unique problems of dynamic underwater settings. Due to envi-
ronmental factors such as fluctuating currents and turbidity and the lack of GPS, these old
methods are limited in adaptability and accuracy. In real-time applications, where quick
and adaptable decision making is crucial, these methods are computationally intensive.
This figure is a synthesis of literature findings that serve as an illustrative summary and are
not derived from original experimental data.

4.3. Integration of Quantum Sensors, Deep Learning, and AI-Driven Techniques for Improved
Underwater SLAM

Quantum sensors offer unmatched sensitivity to environmental changes, while AI-
based methods enable real-time adaptability in data fusion strategies, together providing
transformative advantages for reliable and flexible SLAM in complex underwater conditions.
Quantum sensors, which are based on the principles of quantum physics, are ex-
tremely sensitive to even minute changes in their surroundings, such as variations in the
gravitational and magnetic fields. They are essential for underwater conditions, where
typical sensor performance is hindered by turbidity, pressure, and electromagnetic wave
attenuation [130]. This sensitivity makes it possible to achieve excellent precision, which
is essential for underwater environments. Because of their great stability and minimal
drift, they are an important tool for extended missions in places where GPS is not available,
which can present substantial issues due to accumulated inaccuracies. Quantum magne-
tometers, for example, can detect fluctuations in the geomagnetic field. These variations
can be used to infer changes in position, therefore providing an alternative navigational
cue in situations where traditional signals are not available [131].

Increasing the resilience of SLAM frameworks by integrating quantum sensors is
particularly beneficial for situations such as deep-sea exploration, where traditional sensors
may not be able to provide accurate results. On the other hand, integrating and miniatur-
izing quantum sensors within UUVs presents challenges related to power consumption,
sensor fusion complexities, and environmental interference [132]. All of these challenges
require further development to accommodate practical deployment in real-world scenar-
ios. Moreover, these sensors are being linked with artificial-intelligence-driven filtering
algorithms to manage the high-dimensional data that they generate. This allows for the
optimization of SLAM processing and accuracy, even in situations that are turbulent and
have a limited amount of data [133,134]

Deep learning, especially CNNs, helps process underwater visual and auditory data,
addressing issues including picture quality, color distortion, and item dimensions. YOLOv8
and Faster R-CNN accurately identify underwater features for coral reef imaging and
AUV operations in low visibility [135,136]. These models improve underwater imaging

Sensors 2024, 24, 7490 15 of 32 Figure 10. Comparing the performance of AI-driven and conventional sensor fusion techniques for underwater SLAM systems. Not obtained from actual experimental data, this chart is an indicative summary based on a synthesis of literary results. Figure 11. Localization drift in GPS-disabled environments: comparing quantum and conventional sensors. This image is an illustrative summary based on a synthesis of published ﬁndings rather than original experimental data. Figure 12. Comparison of the mapping precision of single and multisensor fusion for SLAM systems. This graphic shows a literature synthesis, not experimental data. Sensors 2024, 24, 7490

16 of 31

clarity for biodiversity monitoring and infrastructure inspections by minimizing noise and
color distortions.

Sensor fusion improves SLAM systems’ localization and mapping by combining sonar,
LiDAR, and camera data with deep learning. Dynamic sensor prioritization—using LiDAR
in clear water and sonar in muddy water—improves obstacle recognition, allowing AUVs
to navigate complicated terrains without human supervision (Merveille et al., 2024). In
complicated underwater environments, deep learning models and sensor fusion improve
mapping and localization.

Both supervised and unsupervised deep learning techniques use visual and LiDAR
data to improve SLAM. Supervised posture estimation is accurate, but unsupervised
methods reduce rotation and translation errors without labeled data [137]. Hierarchical
feature encoding and attention techniques improve multi-sensor synthesis pose estimation
precision [138]. Laser radar, IMUs, and other data are fused to overcome laser-based SLAM
drift with algorithms like EKF for exact environmental mapping. Stable multi-sensor
fusion approaches like GNSS simulation provide exact location and velocity data even with
malfunctioning sensors.

Deep-learning-based sensor fusion improves underwater mapping by enabling se-
mantic scene understanding in SLAM systems [139]. In dynamic situations, reinforcement
learning (RL) improves sensor localization data integration and SLAM stability [140]. Tradi-
tional SLAM systems struggle with moving objects, but recent deep learning enhancements
identify and compensate for such dynamic aspects. In low-visibility conditions, non-optical
sensors like mm Wave radar improve dependability. Due to sensor integration and deep
learning problems, underwater SLAM for UUVs needs more research.

IMU, sonar, and LiDAR data processing in real time needs large computational re-
sources, especially in quickly changing surroundings [106,141–143]. Distributed computing
systems minimize computational load, while GPUs and FPGAs enable parallel processing
to reduce latency [144–146].

Additionally, dependability issues in UUV operations, such as sensor failures or
environmental disruptions, can be mitigated using redundancy and machine-learning-
based filtering methods to improve resilience and system efficacy.

The Y-axis in Figure 10 shows the equivalent mapping accuracy (%). In contrast, the
X-axis shows the sensor quality. The Y-axis represents equal mapping accuracy (%). In
contrast, the sensor quality index (X-axis) displays the sensor system’s ability to collect
precise, noise-resistant data (arbitrary units). Traditional methods (solid blue line) enhance
mapping accuracy as sensor quality improves, but they cannot reach high accuracy levels.
Even with moderate sensor quality, AI-driven approaches (dashed orange line) produce
near-optimal mapping accuracy, demonstrating more robust and consistent performance
across all sensor quality levels. This shows how AI-driven solutions might improve SLAM
in complex underwater environments.

X in Figure 11 represents mission time (hours), and Y represents localization drift
(arbitrary units). Traditional sensors (solid blue line) wander exponentially due to error
accumulation without GPS correction. Quantum sensors (dashed green line) have a smaller
localization drift, allowing them to navigate more accurately in GPS-denied areas during
long missions.

Integrating deep learning models with sensor fusion and quantum sensing promotes
underwater SLAM by augmenting mapping and localization accuracy in difficult, GPS-
denied situations. Recent advancements in model compression, edge computing, and
AI-driven filtering enhance the capabilities of autonomous underwater navigation. The
subsequent part analyzes experimental data to illustrate the efficacy of these fusion tech-
niques in SLAM applications.

Conventional SLAM techniques, such as KF and particle filters, mitigate drift, noise,
and processing constraints but frequently encounter substantial drift and erratic alter-
ations in low-visibility settings [40,104]. Research conducted by Bucci et al. and Techap-

Sensors 2024, 24, 7490

17 of 31

attaraporn et al. demonstrated the efficacy of Kalman filtering; however, it is deficient in
adaptability in dynamic conditions [40,104].

Quantum sensors, as analyzed by Sambataro et al., utilize quantum state discrimi-
nation to enhance sensitivity and precision in GPS-denied environments, with quantum
sensor networks (QSN) attaining meter-level accuracy, essential for prolonged underwater
operations [147,148].

AI-driven methodologies provide real-time adaptability, as demonstrated by researchers
by combining noisy and heterogeneous sensor data to improve localization stability in
dynamic situations while requiring less processing power than static filters [149].
In
contrast to conventional methodologies, AI and deep learning [150] techniques enhance
responsiveness and precision in underwater SLAM.

We have examined sensor fusion methods and their performance in underwater
SLAM applications. Now, we must consider computing complexity. Real-time SLAM
processing demands and optimization solutions for underwater navigation are examined
in Section 5. Each fusion method balances processing performance and memory utilization.
In resource-constrained situations, hierarchical fusion and distributed processing enable
efficient deployment.

5. Enhancing Computing Efficiency in Sensor Fusion for Real-Time Underwater SLAM

Sensor fusion enhances underwater SLAM navigation accuracy and resilience, but
each technique needs different computational demands that affect processing time and
memory. Real-time underwater SLAM requires managing these demands, especially when
computational tasks might be shared across UUVs or offloaded to surface stations. Essential
sensor fusion approaches’ computation needs and optimization methods for underwater
accuracy and real-time performance are discussed in this section.

5.1. Kalman Filter Efficiency and Variants

The computationally efficient Kalman filter is appropriate for real-time applications
with O(n2) complexity scaling, where n is the number of state variables [40,151]. It effi-
ciently processes high-frequency, linear IMU and DVL data streams. State linearization
and sigma-point sampling make the EKF and UKF more computationally intensive, but
they are suggested for non-linear scenarios [104]. To maintain performance and reduce
processing burden, adaptive filtering adapts state space to environmental stability [40].
Further optimization may involve dynamically changing filter types based on environ-
mental complexity, utilizing simpler models for stable settings and advanced filters for
difficult ones.

5.2. Particle Filter Complexity and Adaptations

The particle filter can handle non-linear, non-Gaussian environments; however, its
complexity scaling is O(NM), where N is the particle count and M is the state space dimen-
sionality. Reduced particle numbers simplify processing but may lower dynamic accuracy.
GPU-based parallel processing and adaptive resampling, which adjust particle count
based on environmental stability, enable real-time particle filters [152]. In stable, resource-
constrained underwater environments, event-based sampling reduces duplicate processing
by updating particles only when significant environmental changes occur [153,154].

5.3. Computational Challenges and Solutions

Real-time applications cannot use particle filters since they are computationally expen-
sive but versatile. With particle count, computing load grows since each particle represents
a potential state and requires processing. Recent hardware acceleration and adaptive
techniques have helped [155]. Software-only particle filter processing on conventional
processors like the Cortex-M1 core takes two orders of magnitude longer than hardware
accelerators, making real-time SLAM easier in limited situations [155,156].

Sensors 2024, 24, 7490

18 of 31

Particle weights can be changed to save computation [152]. Particle filters can improve
state estimations with exponential weight adjustments in noisy sensor environments.
Adaptive weight adjustment and selective resampling keep particles representative of high-
likelihood states without using too many particles in computationally limited underwater
SLAM applications.

Particle filters are beneficial in non-linear and non-Gaussian conditions, but their com-
puting needs limit real-time applications. However, hardware acceleration and adaptive
resampling make them more viable. Particle filters and implementation strategies can
increase underwater SLAM performance even in tough conditions. Optimizing particle
filter algorithms and hardware implementations may make this resilient technology more
accessible and efficient for underwater SLAM applications [157].

5.4. Graph-Based SLAM Computational Efficiency and Parallelism

Real-time applications must compute graph-based SLAM. SLAM can be used in
real-time on low-power platforms due to data parallelism and GPU acceleration [158]. Col-
lective SLAM systems increase efficiency by dividing computational tasks across multiple
players. These frameworks allow low-processing bots to interact and perform SLAM using
measurement algebra [159]. This cooperative approach makes SLAM viable for smaller
autonomous robots with less computational resources.

Although graph-based SLAM has high mapping precision, computing requirements
must be balanced. GPU acceleration, graph sparsification, and multi-sensor fusion mini-
mize computational load but complicate implementation. Integrating dynamic and past
information into SLAM enhances mapping accuracy but requires careful data processing to
avoid inaccuracy [158]. Further research is needed to optimize graph-based SLAM for real-
world applications to balance precision advances with computationally feasible methods.

5.5. Deep Learning Models and Computational Considerations

Deep learning for underwater SLAM, specifically feature extraction and object recog-
nition, is popular yet computationally expensive, especially during training [160]. Model
reduction, pruning, and quantization minimize these requirements for embedded UUV
deployment [161,162]. Deep learning for feature extraction and Kalman filtering for sensor
fusion balance computational efficiency and data fusion. Knowledge distillation, where a
large model trains a smaller one to perform specific tasks, is another novel strategy that
reduces processing overhead without losing accuracy.

5.6. Event-Driven and Energy-Efficient Processing

Long-term operations in low-energy underwater environments require energy-efficient
processing. Event-driven processing decreases computing load and power consumption in
steady situations by processing data only when significant sensor changes occur [163,164].
Neuromorphic computers, which mimic brain-like processing for sensor fusion, conserve
energy and speed up SLAM processing [165].

5.7. Optimization Strategies for Real-Time Performance

Real-time underwater SLAM in resource-constrained environments involves compu-
tational complexity control for accuracy and efficiency. Hierarchical sensor fusion inter-
mittently analyses complex, low-frequency sensors like sonar or cameras and continually
incorporates feedback from high-frequency, low-complexity sensors like IMUs to balance
accuracy and computing load [166]. Multi-core CPUs and GPUs can reduce latency and
enable real-time particle filter and deep learning model execution [167]. In multi-UUV sys-
tems, distributed processing decreases UUV workload and enhances system responsiveness
by outsourcing computation to surface stations or dividing it between vehicles.

Sensors 2024, 24, 7490

19 of 31

5.8. Balancing Accuracy with Computational Efficiency

Sensor fusion is computationally expensive for underwater SLAMs. Particle filters
and deep learning models outperform Kalman filtering in complex scenarios but require
more computer resources. Hierarchical fusion, parallel processing, and event-driven
sampling help SLAM implementations balance these trade-offs and operate in challenging
underwater conditions in real time [168].

The graph in Figure 12 contrasts the computing requirements of the four techniques
regarding processing load. Reduced values indicate enhanced efficiency, underscoring the
real-time relevance of each method in underwater navigation activities. Our subsequent in-
terest is directed to the successful sensor fusion case studies and algorithm implementations
in UUV SLAM.

Based on the computational challenges of SLAM sensor fusion, the next section dis-
cusses applied case studies of multisensor fusion methods in underwater environments. In
Section 6, major experimental results from SLAM investigations in military operations and
deep-sea research show how these fusion methods improve localization precision, visibility
adaptability, and environmental noise robustness. The assessments show the strengths
and weaknesses of different strategies and reveal when certain sensor fusion techniques
work well.

6. Practical Implementations of Sophisticated Sensor Fusion in Underwater SLAM for
Military, Industrial, and Research Endeavors
6.1. A Few Case Studies of Successful Sensor Fusion

Military activities, oil and gas development, and deep-sea research require UUVs.
Advanced sensor fusion systems integrate sonar, LiDAR, and inertial sensors for covert
navigation, enabling underwater surveillance, mine detection, and reconnaissance in GPS-
denied areas in the military [169]. In the oil and gas industry, UUVs check pipelines and
undersea infrastructure for leaks, even in low visibility. Despite tremendous pressure and
low visibility, they construct high-resolution 3D images of unknown locations for deep-sea
research [104,170–174].

Incorporating vision-based methodologies, such as feature extraction methods like
SIFT, with topological maps improves SLAM efficacy under many environmental condi-
tions, including variations in illumination and noise. This method enhances localization
and mapping accuracy, especially in underwater environments where optical and acoustic
imaging diverge markedly [175]. Furthermore, feature-based SLAM systems that integrate
semantic information enhance robustness by linking feature points to semantic labels,
resulting in improved feature-matching precision and loop closure detection [176].

Frameworks such as ORB-SLAM2, when integrated with deep learning for intersection
recognition, improve the precision for environmental representations, hence augmenting
the overall reliability of SLAM [177]. Incorporating multisensor systems, including LiDAR-
inertial odometry and visual-inertial odometry, enhances the resilience of SLAM in intricate
situations. Furthermore, real-time location algorithms integrating point-line features with
IMU data have demonstrated improved trajectory accuracy and reduced matching er-
rors [178].

Notwithstanding these developments, SLAM systems [179,180] encounter difficul-
ties in dynamic underwater environments. Conventional methods exhibit deficiencies in
robustness and accuracy when addressing moving objects; however, contemporary tech-
niques utilizing deep learning and semantic segmentation present potential alternatives.
These methodologies emphasize eliminating dynamic feature points while prioritizing
static environmental components, enhancing the precision of pose estimation and trajectory
mapping. Current research seeks to create algorithms that can manage static and dynamic
components in real time, with integrated methods demonstrating the potential for addi-
tional error reduction [181]. Integrating deep learning with sensor fusion for underwater
SLAM has also shown promising results.

Sensors 2024, 24, 7490

20 of 31

In summary, the selection and integration of appropriate sensor fusion methodolo-
gies are pivotal in overcoming the unique challenges posed by underwater environments,
where factors such as sensor noise, computational complexity, and variable environmental
conditions demand a careful balance between accuracy and efficiency. As advancements in
sensor technology and computational techniques continue, these methodologies promise to
enhance the accuracy, robustness, and real-time performance of SLAM systems in increas-
ingly complex underwater applications. The following section delves into case studies of
successful sensor fusion implementations in underwater SLAM, illustrating the real-world
applicability and outcomes of these approaches across various operational environments.

6.2. A Few Key Experimental Results from Existing Studies in UUV SLAM

These studies focus on different multisensor fusion approaches, addressing fundamen-

tal challenges like visibility, localization precision, and environmental adaptability.

SLAM accuracy depends on underwater picture enhancement and low-visibility fea-
ture detection. Liang et al. [168] developed a multisensor system that improves visual
quality and contrast by using hybrid attention mechanisms, generative adversarial net-
works (GANs), and DVL compared to other approaches; the strategy improves feature
point detection by 68.18% in MAE and 44.44% in STD. These findings demonstrate the
system’s low-visibility AUV performance. Bucci et al. [129] integrated pose-graph SLAM
with maximum a posteriori (MAP) estimate using a monocular camera and DVL data.
Optimized with an inbuilt reset mechanism to accommodate the computational load, this
technique was robust and accurate around Stromboli Island. Li et al. [182] used LiDAR
data with EKF in a Rao-Blackwellized Particle Filter (RBPF)-SLAM architecture to improve
map clarity and pose accuracy in high drift-risk environments. Techapattaraporn et al. [40]
showed that an error-state Kalman filter (ESKF) reduced computing effort by estimating
error states instead of full states, improving localization stability. Bucci et al. [104] validated
centralized and decentralized UKF techniques in dynamic, low-visibility situations. Both
filtering methods are resilient and efficient, essential for underwater navigation.

Underwater SLAM systems using particle filtering efficiently address sensor noise
and environmental uncertainty. In their 2021 study, Martínez-Barberá et al. [183] used a
sequential Monte Carlo (SMC) architecture with particle filters to manage noise in pipelines
using sonar and camera data. Applications demanding great localization reliability benefit
from this method. Wang and Qiu [184] used LiDAR and camera data in a multi-modal
SLAM framework to achieve 98.9% mapping accuracy and 1.1% error, useful for resource
extraction. Vargas et al. [185] used DVL data with visual signals to improve posture
prediction and robustness in low-visibility environments, outperforming ORB-SLAM2.
Rahman et al. [20] introduced the SVIn2 system, which uses sonar, visual, inertial, and
water-pressure data for adaptive, reliable localization in underwater trials. Table 2 provides
more details.

Table 2. Experimental results from the reviewed literature.

Study

Sensors Used

Environment

Fusion Technique

Key Results

Liang et al. [168]

Camera, DVL

Low visibility

GAN with attention
mechanisms

MAE reduced by 68.18%; STD
reduced by 44.44%

Bucci et al. [129]

Techapattaraporn
et al. [40]

Martínez-Barberá
et al. [183]

Monocular camera,
DVL

Sea trials

MAP with pose-graph
SLAM

Comprehensive mapping with
enhanced localization precision

INS, DVL

Simulation

ESKF

Outperformed EKF and INS
under DVL loss

Camera, range sensor

Real-world

Particle filter

Improved localization reliability

Wang and Qiu [184]

LiDAR, camera

Real-world

Multi-modal fusion

98.9% accuracy, 1.1% error rate

Sensors 2024, 24, 7490

21 of 31

Table 2. Cont.

Study

Sensors Used

Environment

Fusion Technique

Key Results

Rahman et al. [20]

Sonar, visual, inertial,
water-pressure

Benchmarks

Keyframe-based SLAM

Vargas et al. [185]

Camera, acoustic
sensor

Experimental
trials

Acoustic-visual SLAM

Li et al. [182]

LiDAR, EKF

Various

RBPF-SLAM with EKF

Robust initialization, loop
closure, and relocalization

Enhanced robustness compared
to ORB-SLAM2

Enhanced map delineations,
enhanced pose precision

Bucci et al. [104]

Various, UKF

Sea trials

Centralized/decentralized
unscented Kalman filter

Improved resilience, reduced
measurement impacts

6.3. Analysis and Limitations of Experimental Results

The reviewed research continuously emphasizes the significance of multisensor fusion
in attaining superior localization precision and mapping accuracy in difficult underwater
environments. The integration of sensors like DVL, sonar, and cameras alleviates the
constraints of single-sensor SLAM methods, improving system adaptability in intricate
underwater settings. Nonetheless, specific high-precision fusion techniques, such as particle
filters, are computationally intensive, hence constraining their real-time use in resource-
limited environments. These trade-offs highlight the necessity for balanced solutions that
preserve accuracy while ensuring operational efficiency.

Multisensor fusion methods show promise; however, they frequently use proprietary
datasets from controlled contexts, limiting deep-sea application scalability. The computa-
tional load of some other advanced algorithms is a major obstacle for real-time applications.
Expanding freely available datasets to cover real-world conditions like high turbidity and
strong currents would help the community test and assess SLAM algorithms.

6.4. Datasets Used in Reviewed Experiments

Most reviews use proprietary or controlled-environment datasets. Public datasets
encompassing a range of marine conditions (e.g., high turbidity, deep-sea pressure) are
needed to improve benchmarking among multisensor SLAM approaches and encourage
field cross-validation and repeatability.

Section 8 synthesizes recent multisensor fusion studies on underwater SLAM, high-
lighting significant gains in robustness, precision, and adaptability in autonomous underwa-
ter vehicles. Innovative advances in image augmentation, probabilistic estimation, Kalman
filtering, particle filtering, multi-modal SLAM, and sonar-based applications are presented
per theme. Each area highlights visibility, localization, and environmental adaptation
improvements, with tables and numbers for a complete picture.

Section 7 discusses how hybrid quantum–AI models, deep learning, and optimized
computational frameworks could improve underwater SLAM’s precision and adaptability
after reviewing sensor fusion experiments and their effects. These advances aim to let
UUVs autonomously explore and map complicated aquatic environments in real time, even
without GPS and fluctuating visibility. The next generation of SLAM systems will improve
resilience, computing efficiency, and responsiveness by incorporating quantum sensors
and AI, enabling disruptive underwater exploration and monitoring applications.

7. Future Directions

To overcome underwater obstacles, underwater SLAM systems must integrate quan-
tum sensors and deep learning. These technologies promise to improve underwater SLAM
by improving precision, adaptability, and robustness, allowing UUVs to traverse and map
complicated aquatic terrain autonomously.

Future SLAM systems may incorporate specialized quantum sensors, such as quan-
tum magnetometers, quantum gravimeters, and atomic clocks, to negotiate underwater

Sensors 2024, 24, 7490

22 of 31

obstacles. Atomic clocks provide remarkable timing precision, essential for reducing lo-
calization drift over prolonged durations in environments without a GPS. Atomic clocks
offer consistent and accurate timing, enabling the synchronization of data from several
sensors and minimizing cumulative errors in positioning and trajectory precision [186,187].
Quantum sensors markedly boost the stability of UUV positioning, whereas atomic clocks
substantially improve timing precision, a critical factor in complex underwater navigation.
Future SLAM systems may incorporate quantum sensing alongside AI-driven filtering
and reinforcement learning (RL) to facilitate real-time flexibility. For instance, UUVs
outfitted with quantum magnetometers and artificial intelligence algorithms might adjust to
fluctuating underwater conditions, including currents and turbidity, even in the absence of
a GPS. In this configuration, quantum sensors would deliver high-precision data, while AI
algorithms would dynamically modify SLAM settings according to real-time environmental
inputs [147]. This combination would be particularly advantageous for prolonged missions,
such as deep-sea exploration and marine ecosystem surveillance.

Deep learning models, including convolutional neural networks (CNNs) and reinforce-
ment learning, enable unmanned underwater vehicles (UUVs) to analyze intricate sensor
data and modify simultaneous localization and mapping (SLAM) settings in real-time.
Convolutional neural networks (CNNs) facilitate the identification of essential underwater
characteristics by unmanned underwater vehicles (UUVs), whereas reinforcement learning
(RL) permits the dynamic adjustment of sensor fusion methodologies in response to real-
time environmental data [136,188]. This adaptability can improve navigational precision in
situations with obstacles and variable visibility.

Future SLAM systems may integrate quantum sensor data with deep learning al-
gorithms to obtain precise environmental assessments and adaptive decision making.
Quantum gravimetric data can improve localization precision, but deep learning can aid in
semantic mapping and obstacle detection. This combination allows UUVs to identify and
react to environmental changes with exceptional precision, enhancing localization accuracy
and navigational safety.

Hybrid SLAM models integrating quantum sensing with deep learning necessitate
substantial computational resources owing to the intricacy of processing quantum sensor
data and AI-driven adaptation. Future SLAM systems must prioritize computational frame-
works that enhance processing efficiency while maintaining accuracy. Possible solutions
encompass hierarchical sensor fusion, distributed processing inside multi-UUV networks,
and the utilization of GPU or neuromorphic processor acceleration to diminish latency and
facilitate real-time processing in demanding underwater environments [106,152].

To implement SLAM on resource-limited UUVs, lightweight AI models like MobileNet
and SqueezeNet, along with model compression approaches, can support the deployment
of quantum-enhanced SLAM. Distributed processing inside UUV networks may enhance
operational capabilities by facilitating computational task-sharing in extensive, intricate
underwater environments [189].

As SLAM technology advances, comprehensive and varied datasets are crucial for
testing hybrid SLAM models. To guarantee thorough testing, researchers might utilize
datasets encompassing a variety of underwater settings, ranging from shallow coastal areas
to deep-sea regions. Publicly accessible datasets will expedite development and enable
cross-validation among universities and sectors, fostering collaboration and resilience in
SLAM models [190].

Deep learning models, specifically CNNs and GANs, can augment SLAM by facilitat-
ing UUVs in executing semantic mapping and identifying underwater characteristics in
real time. These models enable UUVs to categorize seafloor entities such as coral, sand, and
rock formations, thereby improving navigation precision and operational safety. The incor-
poration of deep learning into SLAM enhances contextual awareness, which is beneficial
for applications including marine biodiversity monitoring, subsea infrastructure inspection,
and archeological research. Nonetheless, lightweight and real-time deep learning models
are essential for UUV deployment to guarantee efficiency and responsiveness [191].

Sensors 2024, 24, 7490

23 of 31

8. Conclusions

This paper emphasizes significant breakthroughs in sensor fusion for UUV SLAM,
highlighting the revolutionary impact of quantum sensors and AI-driven methodologies in
tackling intricate underwater issues. This review’s key contributions are (1) a comprehen-
sive examination of quantum sensors, illustrating their capacity to reduce localization drift
and improve SLAM accuracy in GPS-denied environments, and (2) an emphasis on AI-
driven filtering techniques, which provide real-time adaptability and resilience in dynamic
underwater contexts. This paper distinguishes itself from prior assessments that focus
on conventional fusion methods by highlighting the distinctive benefits and prospects
of emerging technology. Progressing requires addressing obstacles such as computing
needs and data integration, as well as enhancing energy efficiency and system reliability, to
advance underwater SLAM. Quantum and AI-driven technologies, emphasizing redun-
dancy, failure detection, and adaptive capabilities, offer considerable potential for scalable,
efficient, and resilient UUV operations in intricate marine settings.

Author Contributions: Conceptualization F.F.R.M. and B.J.; methodology, F.F.R.M. and B.J.; software,
F.F.R.M.; validation, B.J., B.F., and Z.X.; formal analysis, F.F.R.M. and B.J.; investigation, B.F.; resources,
B.J.; data curation, Z.X.; writing—original draft preparation, B.F.; writing—review and editing, Z.X.;
visualization, F.F.R.M.; supervision, B.J. and Z.X; project administration, F.F.R.M.; funding acquisition,
B.J. All authors have read and agreed to the published version of the manuscript.

Funding: This research was funded by the National Natural Science Foundation of China, grant
number: 52071090.

Data Availability Statement: Not applicable.

Conflicts of Interest: The authors declare no conflicts of interest.

References

1.

2.

Evans, K.; Chiba, S.; Bebianno, M.J.; Garcia-Soto, C.; Ojaveer, H.; Park, C.; Ruwa, R.; Simcock, A.J.; Vu, C.T.; Zielinski, T. The
Global Integrated World Ocean Assessment: Linking Observations to Science and Policy Across Multiple Scales. Front. Mar. Sci.
2019, 6, 298. [CrossRef]
Seymour, J.R. A sea of microbes: The diversity and activity of marine microorganisms. Microbiol. Aust. 2014, 35, 183–187.
[CrossRef]

3. Hatje, V.; da Costa, M.F.; da Cunha, L.C. Oceanografia e Química: Unindo conhecimentos em prol dos oceanos e da sociedade.

4.

5.

Quimica Nova 2013, 36, 1497–1508. [CrossRef]
Liu, C.; Jiang, B.; Wang, X.; Zhang, Y.; Xie, S. Event-Based Distributed Secure Control of Unmanned Surface Vehicles With DoS
Attacks. IEEE Trans. Syst. Man, Cybern. Syst. 2024, 54, 2159–2170. [CrossRef]
Zhang, G.; Yin, S.; Huang, C.; Zhang, W.; Li, J. Structure Synchronized Dynamic Event-Triggered Control for Marine Ranching
AMVs via the Multi-Task Switching Guidance. IEEE Trans. Intell. Transp. Syst. 2024, 1–14. [CrossRef]

6. Wang, X.; Zhang, H.; Wang, Y.; Wang, Y.; Dong, H.; Li, J. Data-Based Guaranteed Trajectory Estimation for Unmanned Surface

7.

8.

9.

Vehicles. IEEE Trans. Ind. Inform. 2024, 20, 9793–9802. [CrossRef]
Sands, T.; Bollino, K.; Kaminer, I.; Healey, A. Autonomous Minimum Safe Distance Maintenance from Submersed Obstacles in
Ocean Currents. J. Mar. Sci. Eng. 2018, 6, 98. [CrossRef]
Reis, G.M. Augmented Terrain-Based Navigation to Enable Persistent Autonomy for Underwater Vehicles in GPS-Denied
Environments. Master’s Thesis, Florida International University, Miami, FL, USA, 2018. [CrossRef]
Saeed, N.; Celik, A.; Alouini, M.-S.; Al-Naffouri, T.Y. Analysis of 3D localization in underwater optical wireless networks with
uncertain anchor positions. Sci. China Inf. Sci. 2020, 63, 202305. [CrossRef]

10. Diamant, R.; Lampe, L. Underwater localization with time-synchronization and propagation speed uncertainties. In Proceedings
of the 2011 8th Workshop on Positioning, Navigation and Communication, Dresden, Germany, 7–8 April 2011; IEEE: Piscataway,
NJ, USA, 2011; pp. 100–105. [CrossRef]

11. Holliday, D.V.; Donaghay, P.L.; Greenlaw, C.F.; Napp, J.M.; Sullivan, J.M. High-frequency acoustics and bio-optics in ecosystems

research. ICES J. Mar. Sci. 2009, 66, 974–980. [CrossRef]

12. Kalyan, B.; Balasuriya, A.; Ura, T.; Wijesoma, S. Sonar and vision based navigation schemes for autonomous underwater vehicles.
In Proceedings of the 8th Control, Automation, Robotics and Vision Conference ICARCV 2004, Kunming, China, 6–9 December
2004; pp. 437–442. [CrossRef]

13. Ali, U.; Muhammad, W.; Irshad, M.J.; Manzoor, S. Multi-sensor fusion for underwater robot self-localization using PC/BC-DIM

neural network. Sens. Rev. 2021, 41, 449–457. [CrossRef]

Sensors 2024, 24, 7490

24 of 31

14.

Joe, H.; Cho, H.; Sung, M.; Kim, J.; Yu, S.C. Sensor fusion of two sonar devices for underwater 3D mapping with an AUV. Auton.
Robot. 2021, 45, 543–560. [CrossRef]

15. Emter, T.; Petereit, J. Integrated multi-sensor fusion for mapping and localization in outdoor environments for mobile robots.

SPIE Sens. Technol. Appl. 2014, 9121, 194–203. [CrossRef]

16. Choi, W.S.; Hoang, N.M.; Jung, J.H.; Lee, J.M. Navigation System Development of the Underwater Vehicles Using the GPS/INS
Sensor Fusion. In Proceedings of the Intelligent Robotics and Applications: 7th International Conference ICIRA 2014, Guangzhou,
China, 17–20 December 2014; Springer International Publishing: New York, NY, USA, 2014; pp. 491–497. [CrossRef]

17. Yeong, D.J.; Velasco-Hernandez, G.; Barry, J.; Walsh, J. Sensor and Sensor Fusion Technology in Autonomous Vehicles: A Review.

Sensors 2021, 21, 2140. [CrossRef] [PubMed]

18. Chen, C.; Rosa, S.; Miao, Y.; Lu, C.X.; Wu, W.; Markham, A.; Trigoni, N. Selective Sensor Fusion for Neural Visual-Inertial
Odometry. In Proceedings of the 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), Long Beach,
CA, USA, 15–20 June 2019; IEEE: Piscataway, NJ, USA, 2019; pp. 10534–10543. [CrossRef]

19. Butt, F.A.; Chattha, J.N.; Ahmad, J.; Zia, M.U.; Rizwan, M.; Naqvi, I.H. On the Integration of Enabling Wireless Technologies and
Sensor Fusion for Next-Generation Connected and Autonomous Vehicles. IEEE Access 2022, 10, 14643–14668. [CrossRef]
20. Rahman, S.; Li, A.Q.; Rekleitis, I. SVIn2: A multi-sensor fusion-based underwater SLAM system. Int. J. Rob. Res. 2022, 41,

1022–1042. [CrossRef]

21. Dang, X.; Rong, Z.; Liang, X. Sensor Fusion-Based Approach to Eliminating Moving Objects for SLAM in Dynamic Environments.

Sensors 2021, 21, 230. [CrossRef]

22. Drolet, L.; Michaud, F.; Cote, J. Adaptable sensor fusion using multiple Kalman filters. In Proceedings of the 2000 IEEE/RSJ
International Conference on Intelligent Robots and Systems (IROS 2000), (Cat. No.00CH37113). Takamatsu, Japan, 31 October–5
November 2000; IEEE: Piscataway, NJ, USA, 2000; pp. 1434–1439. [CrossRef]
Feng, M.; Yi, X.; Wang, K.; Cheng, Z. Multi-sensor fusion visual SLAM for uncertain observations. In Proceedings of the 2024
5th International Conference on Computer Vision, Image and Deep Learning (CVIDL), Zhuhai, China, 19–21 April 2024; IEEE:
Piscataway, NJ, USA, 2024; pp. 1151–1155. [CrossRef]

23.

24. Zeng, X.; Martinez, T. A noise filtering method using neural networks. In Proceedings of the IEEE International Workshop on Soft
Computing Techniques in Instrumentation, Measurement and Related Applications (SCIMA 2003), Provo, UT, USA, 17 May 2003;
IEEE: Piscataway, NJ, USA, 2003; pp. 26–31. [CrossRef]

25. Zhang, S.; Gong, S.; Zhang, G.; Pan, F.; Li, H. SLAM Algorithm Based on Variational Bayesian Noise Adaptive Kalman. In
Proceedings of the 2023 China Automation Congress (CAC), Chongqing, China, 17–19 November 2023; IEEE: Piscataway, NJ,
USA, 2023; pp. 3669–3674. [CrossRef]

26. Vasyukov, S.; Macovey, A.; Tronnikov, A. Impulsive Noise from the Optional Equipment on In-Vehicle Power Lines. In Proceedings
of the 2021 International Russian Automation Conference (RusAutoCon), Sochi, Russia, 5–11 September 2021; pp. 238–243.
[CrossRef]

27. Zhang, Q.; Wu, H.; Liang, L.; Mei, X.; Xian, J.; Zhang, Y. A Robust Sparse Sensor Placement Strategy Based on Indicators of Noise

for Ocean Monitoring. J. Mar. Sci. Eng. 2024, 12, 1220. [CrossRef]

29.

28. Hammond, M.; Rock, S.M. A SLAM-based approach for underwater mapping using AUVs with poor inertial information.
In Proceedings of the 2014 IEEE/OES Autonomous Underwater Vehicles (AUV), Oxford, MS, USA, 6–9 October 2014; IEEE:
Piscataway, NJ, USA, 2014; pp. 1–8. [CrossRef]
Fallon, M.F.; Johannsson, H.; Kaess, M.; Folkesson, J.; McClelland, H.; Englot, B.J.; Leonard, J.J. Simultaneous Localization and
Mapping in Marine Environments. In Marine Robot Autonomy; Springer: New York, NY, USA, 2013; pp. 329–372. [CrossRef]
Jiang, M.; Song, S.; Li, Y.; Jin, W.; Liu, J.; Feng, X. A Survey of Underwater Acoustic SLAM System. In Proceedings of the
Intelligent Robotics and Applications: 12th International Conference, ICIRA 2019, Shenyang, China, 8–11 August 2019; Springer
International Publishing: New York, NY, USA, 2019; pp. 159–170. [CrossRef]

30.

31. Xu, C.; Liu, Z.; Li, Z. Robust Visual-Inertial Navigation System for Low Precision Sensors under Indoor and Outdoor Environments.

32.

Remote Sens. 2021, 13, 772. [CrossRef]
Santos, J.M.; Couceiro, M.S.; Portugal, D.; Rocha, R.P. A Sensor Fusion Layer to Cope with Reduced Visibility in SLAM. J. Intell.
Robot. Syst. 2015, 80, 401–422. [CrossRef]

33. Hao, L.; Li, H.; Zhang, Q.; Hu, X.; Cheng, J. LMVI-SLAM: Robust Low-Light Monocular Visual-Inertial Simultaneous Localization
and Mapping. In Proceedings of the 2019 IEEE International Conference on Robotics and Biomimetics (ROBIO), Dali, China, 6–8
December 2019; IEEE: Piscataway, NJ, USA, 2019; pp. 272–277. [CrossRef]

34. Xing, H.; Liu, Y.; Guo, S.; Shi, L.; Hou, X.; Liu, W.; Zhao, Y. A Multi-Sensor Fusion Self-Localization System of a Miniature

Underwater Robot in Structured and GPS-Denied Environments. IEEE Sens. J. 2021, 21, 27136–27146. [CrossRef]

35. Trevathan, J.; Read, W.; Schmidtke, S. Towards the Development of an Affordable and Practical Light Attenuation Turbidity

Sensor for Remote Near Real-Time Aquatic Monitoring. Sensors 2020, 20, 1993. [CrossRef] [PubMed]

36. Mohamed, K.M.; Natarajan, E.; Said, W.Z.B.W.; Khan, M.A. Intelligent Water Turbidity System Using IoT. In Proceedings of the
2023 International Conference on Intelligent Sensing and Industrial Automation, Virtual, 9–10 December 2023; Association for
Computing Machinery: New York, NY, USA, 2023; pp. 1–5. [CrossRef]

37. Trejo-Zúñiga, I.; Moreno, M.; Santana-Cruz, R.F.; Meléndez-Vázquez, F. Deep-Learning-Driven Turbidity Level Classification. Big

Data Cogn. Comput. 2024, 8, 89. [CrossRef]

Sensors 2024, 24, 7490

25 of 31

38. Antonini, G.; Pearce, J.M.; Berruti, F.; Santoro, D. A novel camera-based sensor for real-time wastewater quality monitoring.

39.

Water Pract. Technol. 2024, 19, 3778–3793. [CrossRef]
Scheiber, M.; Cardaillac, A.; Brommer, C.; Weiss, S.; Ludvigsen, M. Modular Multi-Sensor Fusion for Underwater Localization
for Autonomous ROV Operations. In Proceedings of the OCEANS 2022, Hampton Roads, VA, USA, 17–20 October 2022; IEEE:
Piscataway, NJ, USA, 2022; pp. 1–5. [CrossRef]

40. Techapattaraporn, A.; Siriyakorn, V.; Sanposh, P.; Tipsuwan, Y.; Kasetkasem, T.; Charubhun, W. Sensor Fusion Using Error-State
Kalman Filter to Improve Localization of Autonomous Underwater Vehicle Under DVL Signal Loss. In Proceedings of the
TENCON 2023—2023 IEEE Region 10 Conference (TENCON), Chiang Mai, Thailand, 31 October–3 November 2023; IEEE:
Piscataway, NJ, USA, 2023; pp. 893–898. [CrossRef]
Song, J.; Mei, W.; Xu, Y.; Fu, Q.; Bu, L. Practical Implementation of KalmanNet for Accurate Data Fusion in Integrated Navigation.
IEEE Signal Process. Lett. 2024, 31, 1890–1894. [CrossRef]

41.

42. Albekairi, M. A Comprehensive Mutable Analytics Approach to Distinguish Sensor Data on the Internet of Underwater Things.

IEEE Access 2024, 12, 95007–95019. [CrossRef]

43. Xu, Z.; Haroutunian, M.; Murphy, A.J.; Neasham, J.; Norman, R. An Integrated Visual Odometry System for Underwater Vehicles.

IEEE J. Ocean. Eng. 2020, 46, 848–863. [CrossRef]

44. Wang, W.; Cheng, B. Augmented EKF based SLAM system with a side scan sonar. In Proceedings of the 2020 12th International
Conference on Intelligent Human-Machine Systems and Cybernetics (IHMSC 2020), Hangzhou, China, 22–23 November 2020;
IEEE: Piscataway, NJ, USA, 2020; pp. 71–74. [CrossRef]

45. Grisetti, G.; Stachniss, C.; Burgard, W. Improved techniques for grid mapping with Rao-Blackwellized particle filters. IEEE Trans.

Robot. 2007, 23, 34–46. [CrossRef]

46. Nilakantan, J.M.; Ponnambalam, S.G.; Nielsen, P. Application of Particle Swarm Optimization to Solve Robotic Assembly Line
Balancing Problems. In Handbook of Neural Computation; Academic Press: Cambridge, MA, USA, 2017; pp. 239–267. [CrossRef]

47. Grisetti, G.; Kummerle, R.; Stachniss, C.; Burgard, W. A tutorial on graph-based SLAM. IEEE Intell. Transp. Syst. Mag. 2010, 2,

31–43. [CrossRef]

48. Chang, S.; Zhang, D.; Zhang, L.; Zou, G.; Wan, C.; Ma, W.; Zhou, Q. A Joint Graph-Based Approach for Simultaneous Underwater
Localization and Mapping for AUV Navigation Fusing Bathymetric and Magnetic-Beacon-Observation Data. J. Mar. Sci. Eng.
2024, 12, 954. [CrossRef]

49. Lanzagorta, M.; Uhlmann, J.; Venegas-Andraca, S.E. Quantum sensing in the maritime environment. In Proceedings of the
OCEANS 2015—MTS/IEEE Washington, Washington, DC, USA, 19–22 October 2015; IEEE: Piscataway, NJ, USA, 2015; pp. 1–9.
[CrossRef]

50. Tariq, S.; Khalid, U.; Arfeto, B.E.; Duong, T.Q.; Shin, H. Integrating Sustainable Big AI: Quantum Anonymous Semantic Broadcast.

51.

IEEE Wirel. Commun. 2024, 31, 86–99. [CrossRef]
Selvan, C.P.; Ramanujam, S.K.; Jasim, A.S.; Hussain, M.J.M.; Selvan, C.P.; Ramanujam, S.K.; Jasim, A.S.; Hussain, M.J.M.
Enhancing Robotic Navigation in Dynamic Environments. Int. J. Comput. Math. Comput. Sci. 2024. [CrossRef]

52. Zou, D.; Tan, P. CoSLAM: Collaborative visual SLAM in dynamic environments. IEEE Trans. Pattern Anal. Mach. Intell. 2012, 35,

354–366. [CrossRef] [PubMed]

53. Liu, B. Research on Visual SLAM Method Based on Deep Learning in Dynamic Environments. In Proceedings of the 2024 IEEE
6th Advanced Information Management, Communicates, Electronic and Automation Control Conference (IMCEC), Chongqing,
China, 24–26 May 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 1645–1649. [CrossRef]

54. Paull, L.; Saeedi, S.; Seto, M.; Li, H. AUV navigation and localization: A review. IEEE J. Ocean. Eng. 2013, 39, 131–149. [CrossRef]
55. Chen, W.; Wang, X.; Gao, S.; Shang, G.; Zhou, C.; Li, Z.; Xu, C.; Hu, K. Overview of Multi-Robot Collaborative SLAM from the

Perspective of Data Fusion. Machines 2023, 11, 653. [CrossRef]

56. Yin, J.; Wang, Y.; Lv, J.; Ma, J. Study on Underwater Simultaneous Localization and Mapping Based on Different Sensors. In
Proceedings of the 2021 IEEE 10th Data Driven Control and Learning Systems Conference, DDCLS 2021, Suzhou, China, 14–16
May 2021; IEEE: Piscataway, NJ, USA, 2021; pp. 728–733. [CrossRef]
Sun, K.; Cui, W.; Chen, C. Review of underwater sensing technologies and applications. Sensors 2021, 21, 7849. [CrossRef]
57.
58. Huy, D.Q.; Sadjoli, N.; Azam, A.B.; Elhadidi, B.; Cai, Y.; Seet, G. Object perception in underwater environments: A survey on

sensors and sensing methodologies. Ocean. Eng. 2023, 267, 113202. [CrossRef]

59. Kim, A.; Eustice, R.M. Real-time visual SLAM for autonomous underwater hull inspection using visual saliency. IEEE Trans.

Robot. 2013, 29, 719–733. [CrossRef]

60. Zhang, S.; Zhao, S.; An, D.; Liu, J.; Wang, H.; Feng, Y.; Li, D.; Zhao, R. Visual SLAM for underwater vehicles: A survey. Comput.

Sci. Rev. 2022, 46, 100510. [CrossRef]

61. Kazerouni, I.A.; Fitzgerald, L.; Dooly, G.; Toal, D. A survey of state-of-the-art on visual SLAM. Expert Syst. Appl. 2022, 205, 117734.

[CrossRef]

62. Zhang, Y.; Zhou, L.; Li, H.; Zhu, J.; Du, W. Marine Application Evaluation of Monocular SLAM for Underwater Robots. Sensors

2022, 22, 4657. [CrossRef]

63. Zheng, Z.; Xin, Z.; Yu, Z.; Yeung, S.K. Real-time GAN-based image enhancement for robust underwater monocular SLAM. Front.

Mar. Sci. 2023, 10, 1161399. [CrossRef]
Scaramuzza, D.; Fraundorfer, F. Tutorial: Visual odometry. IEEE Robot. Autom. Mag. 2011, 18, 80–92. [CrossRef]

64.

Sensors 2024, 24, 7490

26 of 31

65. Cheng, J.; Zhang, L.; Chen, Q.; Hu, X.; Cai, J. A review of visual SLAM methods for autonomous driving vehicles. Eng. Appl.

Artif. Intell. 2022, 114, 104992. [CrossRef]

66. Xu, Z.; Haroutunian, M.; Murphy, A.J.; Neasham, J.; Norman, R. An Integrated Visual Odometry System With Stereo Camera for

67.

Unmanned Underwater Vehicles. IEEE Access 2022, 10, 71329–71343. [CrossRef]
Javed, Z.; Kim, G.W. PanoVILD: A challenging panoramic vision, inertial and LiDAR dataset for simultaneous localization and
mapping. J. Supercomput. 2022, 78, 8247–8267. [CrossRef]

68. Chong, T.J.; Tang, X.J.; Leng, C.H.; Yogeswaran, M.; Ng, O.; Chong, Y.Z. Sensor Technologies and Simultaneous Localization and

Mapping (SLAM). Procedia Comput. Sci. 2015, 76, 174–179. [CrossRef]

69. Estrada, D.C.; Dalgleish, F.R.; Ouden, C.J.D.; Ramos, B.; Li, Y.; Ouyang, B. Underwater LiDAR Image Enhancement Using a GAN

Based Machine Learning Technique. IEEE Sens. J. 2022, 22, 4438–4451. [CrossRef]

70. Debeunne, C.; Vivet, D. A review of visual-lidar fusion based simultaneous localization and mapping. Sensors 2020, 20, 2068.

[CrossRef]

71. Cai, Y.; Ou, Y.; Qin, T. Improving SLAM Techniques with Integrated Multi-Sensor Fusion for 3D Reconstruction. Sensors 2024,

24, 2033. [CrossRef]

72. Zhang, B.; Peng, Z.; Zeng, B.; Lu, J. 2DLIW-SLAM:2D LiDAR-inertial-wheel odometry with real-time loop closure. Meas. Sci.

Technol. 2024, 35, 075205. [CrossRef]

73. Yu, C.; Chao, Z.; Xie, H.; Hua, Y.; Wu, W. An Enhanced Multi-Sensor Simultaneous Localization and Mapping (SLAM) Framework
with Coarse-to-Fine Loop Closure Detection Based on a Tightly Coupled Error State Iterative Kalman Filter. Robotics 2023, 13, 2.
[CrossRef]

74. Peng, G.; Lam, T.L.; Hu, C.; Yao, Y.; Liu, J.; Yang, F. SLAM Based on Multi-Sensor. In Introduction to Intelligent Robot System Design;

Springer Nature: Singapore, 2023; pp. 273–305. [CrossRef]

75. Wang, X.; Fan, X.; Shi, P.; Ni, J.; Zhou, Z. An Overview of Key SLAM Technologies for Underwater Scenes. Remote. Sens. 2023,

15, 2496. [CrossRef]

76. Chen, D.; Neusypin, K.A.; Selezneva, M.S. Correction Algorithm for the Navigation System of an Autonomous Unmanned

Underwater Vehicle. Sensors 2020, 20, 2365. [CrossRef] [PubMed]

77. Zhang, F.; Zhang, B.; Sun, C. A Robust Lidar SLAM System Based on Multi-Sensor Fusion. In Proceedings of the 2022 11th
International Conference on Control, Automation and Information Sciences (ICCAIS), Hanoi, Vietnam, 21–24 November; IEEE:
Piscataway, NJ, USA, 2022; pp. 130–135. [CrossRef]

78. Chaudhuri, R.; Deb, S.; Das, H. Noble Approach on Sensor Fused Bio Intelligent Path Optimisation and Single Stage Obstacle

Recognition in Customized Mobile Agent. Procedia Comput. Sci. 2023, 218, 778–787. [CrossRef]

79. Nicosevici, T.; Garcia, R.; Carreras, M.; Villanueva, M. A Review of Sensor Fusion Techniques for Underwater Vehicle Navigation.
In Proceedings of the Oceans’04 MTS/IEEE Techno-Ocean’04, (IEEE Cat. No. 04CH37600). Kobe, Japan, 9–12 November 2004;
IEEE: Piscataway, NJ, USA, 2004; pp. 1600–1605.

80. Kaveti, P. Multi-camera sensing for robust perception in robotics. Master’s Thesis, Northeastern University, Boston, MA,

USA, 2022. [CrossRef]

81. Li, C.; Guo, S. Characteristic evaluation via multi-sensor information fusion strategy for spherical underwater robots. Inf. Fusion

2023, 95, 199–214. [CrossRef]

82. Ma, S.; Bai, X.; Wang, Y.; Fang, R. Robust Stereo Visual-Inertial Odometry Using Nonlinear Optimization. Sensors 2019, 19, 3747.

[CrossRef]

83. Xing, K.; Zhang, X.; Lin, Y.; Ci, W.; Dong, W. Simultaneous Localization and Mapping Algorithm Based on the Asynchronous

Fusion of Laser and Vision Sensors. Front. Neurorobot. 2022, 16, 866294. [CrossRef]

84. Balemans, N.; Hellinckx, P.; Latre, S.; Reiter, P.; Steckel, J. S2L-SLAM: Sensor Fusion Driven SLAM using Sonar, LiDAR and Deep
Neural Networks. In Proceedings of the IEEE Sensors, Sydney, Australia, 31 October–3 November 2021; IEEE: Piscataway, NJ,
USA, 2021; pp. 1–4. [CrossRef]
Sang, I.C.; Norris, W.R. An Autonomous Underwater Vehicle Simulation with Fuzzy Sensor Fusion for Pipeline Inspection. IEEE
Sens. J. 2023, 23, 8941–8951. [CrossRef]

85.

86. Wang, C.; Cheng, C.; Yang, D.; Pan, G.; Zhang, F. Underwater AUV Navigation Dataset in Natural Scenarios. Electronics 2023,

87.

12, 3788. [CrossRef]
Feng, C.Q.; Li, B.L.; Liu, Y.F.; Zhang, F.; Yue, Y.; Fan, J.S. Crack assessment using multi-sensor fusion simultaneous localization
and mapping (SLAM) and image super-resolution for bridge inspection. Autom. Constr. 2023, 155, 105047. [CrossRef]

88. Chen, W.; Zhou, C.; Shang, G.; Wang, X.; Li, Z.; Xu, C.; Hu, K. SLAM Overview: From Single Sensor to Heterogeneous Fusion.

Remote Sens. 2022, 14, 6033. [CrossRef]

89. Xu, X.; Zhang, L.; Yang, J.; Cao, C.; Wang, W.; Ran, Y.; Tan, Z.; Luo, M. A Review of Multi-Sensor Fusion SLAM Systems Based on

3D LIDAR. Remote Sens. 2022, 14, 2835. [CrossRef]

90. Bescos, B.; Facil, J.M.; Civera, J.; Neira, J. DynaSLAM: Tracking, Mapping and Inpainting in Dynamic Scenes. IEEE Robot. Autom.

Lett. 2018, 3, 4076–4083. [CrossRef]

91. Rahman, S. A Multi-Sensor Fusion-Based Underwater Slam System. Available online: <https://scholarcommons.sc.edu/etd/5987/>

(accessed on 21 November 2024).

Sensors 2024, 24, 7490

27 of 31

92. Dou, J.; Xu, C.; Tang, Z. SLAM Algorithm Based on Heterogeneous Sensor Data Fusion. In Proceedings of the 2024 36th Chinese
Control and Decision Conference (CCDC), Xi’an, China, 25–27 May 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 1435–1442.
[CrossRef]

93. Kotsuki, S.; Miyoshi, T.; Kondo, K.; Potthast, R. A local particle filter and its Gaussian mixture extension implemented with minor

modifications to the LETKF. Geosci. Model Dev. 2022, 15, 8325–8348. [CrossRef]

94. Kusuma, P.W.; Habaebi, M.H.; Hakim, G.P.N.; Muwardi, R.; Islam, R. Kalman Filter for tracking a noisy cosinusoidal signal with
constant amplitude. In Proceedings of the 2023 9th International Conference on Computer and Communication Engineering
(ICCCE), Kuala Lumpur, Malaysia, 15–16 August 2023; IEEE: Piscataway, NJ, USA, 2023; pp. 383–387. [CrossRef]
Setoodeh, P.; Habibi, S.; Haykin, S. (Eds.) Kalman Filter. In Nonlinear Filters; Wiley: Hoboken, NJ, USA, 2022; pp. 49–70. [CrossRef]
95.
96. Wang, B.; Sun, Z.; Jiang, X.; Zeng, J.; Liu, R. Kalman Filter and Its Application in Data Assimilation. Atmosphere 2023, 14, 1319.

97.

[CrossRef]
Jin, K.; Chai, H.; Su, C.; Xiang, M. A performance-enhanced DVL/SINS integrated navigation system based on data-driven
approach. Meas. Sci. Technol. 2023, 34, 095120. [CrossRef]

98. Zhai, X.; Qi, F.; Zhang, H.; Xu, H. Application of Unscented Kalman Filter in GPS /INS. In Proceedings of the 2012 Symposium
on Photonics and Optoelectronics, Shanghai, China, 21–23 May 2012; IEEE: Piscataway, NJ, USA, 2012; pp. 1–3. [CrossRef]
99. Zhang, S.; Zhang, T.; Zhong, L.; Hu, B. A SINS/DVL Integrated Navigation Method Based on EIMM-ARCKF Algorithm. IEEE

Sens. J. 2024, 24, 22733–22744. [CrossRef]

100. Paterson, J.; Adorno, B.V.; Lennox, B.; Groves, K. A Nonlinear Estimator for Dead Reckoning of Aquatic Surface Vehicles Using
an IMU and a Doppler Velocity Log. In Proceedings of the 2024 IEEE International Conference on Robotics and Automation
(ICRA), Yokohama, Japan, 13–17 May 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 11941–11947. [CrossRef]

101. Cai, X. The application of extended kalman filtering based on SLAM. Appl. Comput. Eng. 2023, 12, 46–51. [CrossRef]
102. Yan, L.; Zhao, L. An approach on advanced unscented kalman filter from mobile robot-slam. Int. Arch. Photogramm. Remote Sens.

Spat. Inf. Sci. 2020, 43, 381–389. [CrossRef]

103. Ding, L.; Wen, C. High-Order Extended Kalman Filter for State Estimation of Nonlinear Systems. Symmetry 2024, 16, 617.

[CrossRef]

104. Bucci, A.; Franchi, M.; Ridolfi, A.; Secciani, N.; Allotta, B. Evaluation of UKF-Based Fusion Strategies for Autonomous Underwater

Vehicles Multisensor Navigation. IEEE J. Ocean. Eng. 2022, 48, 1–26. [CrossRef]

105. Kuptametee, C.; Aunsri, N. Sequential Abruptly Changing Hidden States Estimation using Adaptive Particle Impoverishment
Mitigation Scheme. In Proceedings of the 2023 Joint International Conference on Digital Arts, Media and Technology with ECTI
Northern Section Conference on Electrical, Electronics, Computer and Telecommunications Engineering (ECTI DAMT & NCON),
Phuket, Thailand, 22–25 March 2023; IEEE: Piscataway, NJ, USA, 2023; pp. 302–307. [CrossRef]

106. Venugopal, V.; Kannan, S. Accelerating real-time LiDAR data processing using GPUs. In Proceedings of the 2013 IEEE 56th
International Midwest Symposium on Circuits and Systems (MWSCAS), Columbus, OH, USA, 4–7 August 2013; IEEE: Piscataway,
NJ, USA, 2013; pp. 1168–1171. [CrossRef]

107. Chen, X.; Läbe, T.; Milioto, A.; Röhling, T.; Vysotska, O.; Haag, A.; Behley, J.; Stachniss, C. OverlapNet: Loop Closing for
LiDAR-based SLAM. In Proceedings of the 16th Robotics: Science and Systems XVI, Robotics: Science and Systems Foundation,
Online, 12–16 July 2020. [CrossRef]

108. Prados Sesmero, C.; Villanueva Lorente, S.; Di Castro, M. Graph SLAM Built over Point Clouds Matching for Robot Localization

in Tunnels. Sensors 2021, 21, 5340. [CrossRef] [PubMed]

109. Juric, A.; Kendes, F.; Markovic, I.; Petrovic, I. A Comparison of Graph Optimization Approaches for Pose Estimation in SLAM. In
Proceedings of the 2021 44th International Convention on Information, Communication and Electronic Technology (MIPRO),
Opatija, Croatia, 27 September–1 November 2021; IEEE: Piscataway, NJ, USA, 2021; pp. 1113–1118. [CrossRef]

110. Guo, X.; Hu, J.; Chen, J.; Deng, F.; Lam, T.L. Semantic Histogram Based Graph Matching for Real-Time Multi-Robot Global

Localization in Large Scale Environment. IEEE Robot. Autom. Lett. 2021, 6, 8349–8356. [CrossRef]

111. Lu, G. SLAM Based on Camera-2D LiDAR Fusion. In Proceedings of the 2024 IEEE International Conference on Robotics and

Automation (ICRA), Yokohama, Japan, 13–17 May 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 16818–16825. [CrossRef]

112. Chen, Z.; Zhu, H.; Yu, B.; Fu, X.; Jiang, C.; Zhang, S. Robust Multi-Sensor Fusion SLAM Based on Road Network and Reflectivity
Enhancement. In Proceedings of the 2024 7th International Conference on Advanced Algorithms and Control Engineering
(ICAACE), Shanghai, China, 21–23 March 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 1434–1439. [CrossRef]

113. Carrasco, P.L.N.; Bonin-Font, F.; Codina, G.O. Stereo Graph-SLAM for Autonomous Underwater Vehicles. In Intelligent Au-
tonomous Systems 13: Proceedings of the 13th International Conference IAS-13; Springer International Publishing: New York, NY, USA,
2016; pp. 351–360. [CrossRef]

114. Bai, D.; Wang, C.; Zhang, B.; Yi, X.; Tang, Y. Matching-range-constrained real-time loop closure detection with CNNs features.

Robot. Biomimetics 2016, 3, 15. [CrossRef]

115. Funabiki, N.; Morrell, B.; Nash, J.; Agha-Mohammadi, A.A. Range-Aided Pose-Graph-Based SLAM: Applications of Deployable

Ranging Beacons for Unknown Environment Exploration. IEEE Robot. Autom. Lett. 2020, 6, 48–55. [CrossRef]

116. Potokar, E.R.; Norman, K.; Mangelson, J.G. Invariant Extended Kalman Filtering for Underwater Navigation. IEEE Robot. Autom.

Lett. 2021, 6, 5792–5799. [CrossRef]

Sensors 2024, 24, 7490

28 of 31

117. Naphade, K.S.; Storer, R.H.; Wu, S.D. Graph theoretic generation of assembly plans, Part i: Correct generation of precedence

graphs. 1999, accompanied paper.

118. Chaves, S.M.; Galceran, E.; Ozog, P.; Walls, J.M.; Eustice, R.M. Pose-Graph SLAM for Underwater Navigation. In Sensing and
Control for Autonomous Vehicles: Applications to Land, Water and Air Vehicles; Springer: Cham, Switzerland, 2017; pp. 143–160.
119. Cao, B.; Mendoza, R.C.; Philipp, A.; Gohring, D. LiDAR-Based Object-Level SLAM for Autonomous Vehicles. In Proceedings of
the IEEE International Conference on Intelligent Robots and Systems, Abu Dhabi, United Arab Emirates, 14–18 October; IEEE:
Piscataway, NJ, USA, 2021; pp. 4397–4404. [CrossRef]

120. He, W.; Li, R.; Liu, T.; Yu, Y. LiDAR-based SLAM pose estimation via GNSS graph optimization algorithm. Meas. Sci. Technol.

2024, 35, 096304. [CrossRef]

121. Abdelaziz, N.; El-Rabbany, A. Deep Learning-Aided Inertial/Visual/LiDAR Integration for GNSS-Challenging Environments.

Sensors 2023, 23, 6019. [CrossRef]

122. Ni, P.; Zhang, C.; Ji, Y. A hybrid method for short-term sensor data forecasting in Internet of Things. In Proceedings of the 2014
11th International Conference on Fuzzy Systems and Knowledge Discovery (FSKD), Xiamen, China, 19–21 August 2014; IEEE:
Piscataway, NJ, USA, 2014; pp. 369–373. [CrossRef]

123. Beck, S.; Deuser, L.; Still, R.; Whiteley, J. A hybrid neural network classifier of short duration acoustic signals. In Proceedings of
the IJCNN-91-Seattle International Joint Conference on Neural Networks, Seattle, WA, USA, 8–12 July 1991; IEEE: Piscataway, NJ,
USA, 1991; pp. 119–124. [CrossRef]

124. Howell, B.P.; Wood, S. Passive sonar recognition and analysis using hybrid neural networks. In Proceedings of the Oceans 2003.
Celebrating the Past... Teaming Toward the Future, (IEEE Cat. No.03CH37492). San Diego, CA, USA, 22–26 September 2003;
IEEE: Piscataway, NJ, USA, 2003; Volume 4, pp. 1917–1924. [CrossRef]

125. Slivinski, L.; Spiller, E.; Apte, A.; Sandstede, B. A Hybrid Particle–Ensemble Kalman Filter for Lagrangian Data Assimilation.

Mon. Weather. Rev. 2015, 143, 195–211. [CrossRef]

126. Haq, K.R.A.; Harigovindan, V.P. Water Quality Prediction for Smart Aquaculture Using Hybrid Deep Learning Models. IEEE

Access 2022, 10, 60078–60098. [CrossRef]

127. Salakhutdinov, R. Deep learning. In Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery

and Data Mining, New York, NY, USA, 24–27 August 2014; p. 1973. [CrossRef]

128. Goodwin, M.; Halvorsen, K.T.; Jiao, L.; Knausgård, K.M.; Martin, A.H.; Moyano, M.; A Oomen, R.; Rasmussen, J.H.; Sørdalen,
T.K.; Thorbjørnsen, S.H. Unlocking the potential of deep learning for marine ecology: Overview, applications, and outlook. ICES
J. Mar. Sci. 2022, 79, 319–336. [CrossRef]

129. Bucci, A.; Ridolfi, A.; Allotta, B. Pose-graph underwater simultaneous localization and mapping for autonomous monitoring and

3D reconstruction by means of optical and acoustic sensors. J. Field Robot. 2024, 41, 2543–2563. [CrossRef]

130. Christensen, L.; Fernández, J.d.G.; Hildebrandt, M.; Koch, C.E.S.; Wehbe, B. Recent Advances in AI for Navigation and Control of

Underwater Robots. Curr. Robot. Rep. 2022, 3, 165–175. [CrossRef]

131. Loseto, G.; Scioscia, F.; Ruta, M.; Gramegna, F.; Ieva, S.; Fasciano, C.; Bilenchi, I.; Loconte, D.; Di Sciascio, E. A Cloud-Edge
Artificial Intelligence Framework for Sensor Networks. In Proceedings of the 2023 9th International Workshop on Advances in
Sensors and Interfaces (IWASI), Monopoli, Italy, 8–9 June 2023; IEEE: Piscataway, NJ, USA, 2023; pp. 149–154. [CrossRef]
132. Weber, D.; Guhmann, C.; Seel, T. Neural Networks Versus Conventional Filters for Inertial-Sensor-based Attitude Estimation. In
Proceedings of the 2020 IEEE 23rd International Conference on Information Fusion (FUSION), Rustenburg, South Africa, 6–9 July
2020; IEEE: Piscataway, NJ, USA, 2020; pp. 1–8. [CrossRef]

133. Peng, Y.; Jiang, F.; Dong, L.; Wang, K.; Yang, K. Personalized Federated Learning for Generative AI-Assisted Semantic Communi-

cations. arXiv 2024, arXiv:2410.02450.

134. Niemeyer, M.; Arkenau, J.; Pütz, S.; Hertzberg, J. Streamlined Acquisition of Large Sensor Data for Autonomous Mobile Robots
to Enable Efficient Creation and Analysis of Datasets. In Proceedings of the 2024 IEEE International Conference on Robotics and
Automation (ICRA), Yokohama, Japan, 13–17 May 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 15804–15810. [CrossRef]

135. Pan, W.; Lv, B.; Peng, L. Research on AUV navigation state prediction method using multihead attention mechanism in a
CNN-BiLSTM model. In Proceedings of the 2024 7th International Conference on Advanced Electronic Materials, Computers and
Software Engineering (AEMCSE 2024), Nanchang, China, 10–12 May 2024; Yang, L., Ed.; SPIE: Cergy-Pontoise, France, 2024;
p. 105. [CrossRef]

136. Amarasinghe, C.; Ratnaweera, A.; Maitripala, S. UW Deep SLAM-CNN Assisted Underwater SLAM. Appl. Comput. Syst. 2023, 28,

100–113. [CrossRef]

137. An, Y.; Shi, J.; Gu, D.; Liu, Q. Visual-LiDAR SLAM Based on Unsupervised Multi-channel Deep Neural Networks. Cogn. Comput.

2022, 14, 1496–1508. [CrossRef]

138. An, Y.; Sun, Z.; Zhang, C.; Yue, H.; Zhi, Y.; Xu, H. Visual-LIDAR SLAM Based on Supervised Hierarchical Deep Neural Networks.
In Proceedings of the 2024 39th Youth Academic Annual Conference of Chinese Association of Automation (YAC), Dalian, China,
7–9 June 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 1371–1378. [CrossRef]

139. Lai, T. A Review on Visual-SLAM: Advancements from Geometric Modelling to Learning-Based Semantic Scene Understanding

Using Multi-Modal Sensor Fusion. Sensors 2022, 22, 7265. [CrossRef]

140. Wong, C.-C.; Feng, H.-M.; Kuo, K.-L. Multi-Sensor Fusion Simultaneous Localization Mapping Based on Deep Reinforcement

Learning and Multi-Model Adaptive Estimation. Sensors 2023, 24, 48. [CrossRef]

Sensors 2024, 24, 7490

29 of 31

141. Massari, G.; Albani, Y.; Cavallini, F.; Marras, C.; Spaccini, D.; Petrioli, C. Enabling Underwater Internet of Things. In Proceedings

of the Offshore Technology Conference, Houston, TX, USA, 9 May 2024; OTC: Houston, TX, USA, 2024. [CrossRef]

142. Oskard, D.N.; Hong, T.H.; Shaffer, C.A. Real-time algorithms and data structures for underwater mapping. IEEE Trans. Syst. Man

Cybern. 1990, 20, 1469–1475. [CrossRef]

143. Kang, K.D.; Chen, L.; Yi, H.; Wang, B.; Sha, M. Real-Time Information Derivation from Big Sensor Data via Edge Computing. Big

Data Cogn. Comput. 2017, 1, 5. [CrossRef]

144. Liu, X.; Jiang, C.; Yang, S.; Zhu, B.; Zhao, Z. Design and Implementation of Real-time Signal Processing Heterogeneous System
for Unmanned Platform. In Proceedings of the 2023 8th International Conference on Intelligent Computing and Signal Processing
(ICSP), Xi’an, China, 21 April 2023; IEEE: Piscataway, NJ, USA, 2023; pp. 340–345. [CrossRef]

145. Thomas, K.A.; Poddar, S.; Ghosh, M.; Nag, A. Real-Time Object Detection for Unmanned Underwater Vehicles Using Movidius
Neural Compute Stick. In Proceedings of the International Conference on Science, Technology and Engineering, Manipur, India,
17–18 February 2024; Springer: Berlin/Heidelberg, Germany, 2024; pp. 547–553. [CrossRef]

146. Jain, P.; Pateria, N.; Anjum, G.; Tiwari, A.; Tiwari, A. Edge AI and On-Device Machine Learning for Real Time Processing. Int. J.

Innov. Res. Comput. Commun. Eng. 2023, 12, 8137–8146. [CrossRef]

147. Sambataro, O.; Costanzi, R.; Alves, J.; Caiti, A.; Paglierani, P.; Petroccia, R.; Munafo, A. Current Trends and Advances in Quantum

Navigation for Maritime Applications: A Comprehensive Review. arXiv 2023, arXiv:2310.04729. [CrossRef]

148. Zhan, C.; Gupta, H. Quantum Sensor Network Algorithms for Transmitter Localization. In Proceedings of the 2023 IEEE
International Conference on Quantum Computing and Engineering (QCE), Bellevue, WA, USA, 17–22 September 2023; IEEE:
Piscataway, NJ, USA, 2023; pp. 659–669. [CrossRef]

149. Fuentes, J.; Bobadilla, L.; Smith, R.N. Localization in Seemingly Sensory-Denied Environments through Spatio-Temporal Varying
Fields. In Proceedings of the 2022 Sixth IEEE International Conference on Robotic Computing (IRC), Naples, Italy, 5–7 December
2022; IEEE: Piscataway, NJ, USA, 2022; pp. 142–147. [CrossRef]

150. Merveille, F.F.R.; Jia, B.; Xu, Z.; Fred, B. Enhancing Underwater SLAM Navigation and Perception: A Comprehensive Review of

Deep Learning Integration. Sensors 2024, 24, 7034. [CrossRef]

151. Souza, L.F.; Frutuoso, A.; Silva, D.C.; De Barros, E.A. Real-Time INS/DVL/PS fusion applied to the navigation of Autonomous
Underwater Vehicles. In Proceedings of the 2022 Latin American Robotics Symposium (LARS), 2022 Brazilian Symposium on
Robotics (SBR), and 2022 Workshop on Robotics in Education (WRE), São Paulo, Brazil, 18–21 October 2022; IEEE: Piscataway, NJ,
USA, 2022; pp. 1–6. [CrossRef]

152. Hong, K.W.; Kim, Y.; Bang, H. A New Parallel Resampling Algorithm for GPU-Accelerated Particle Filter. In Proceedings of the
AIAA SCITECH 2023 Forum, Oxon Hill, MD, USA, 23–27 January 2023; American Institute of Aeronautics and Astronautics:
Reston, VA, USA, 2023. [CrossRef]

153. Liu, S.; Xie, M.; Ng, H.-C.; Guo, H.; Li, X. Improving Particle Filters with Adaptive Bayesian Resampling for Real-Time Filtering.
In Proceedings of the 2023 8th International Conference on Signal and Image Processing (ICSIP), Wuxi, China, 8–10 July 2023;
IEEE: Piscataway, NJ, USA, 2023; pp. 521–526. [CrossRef]

154. Jiang, C.; Zhu, D.; Li, H.; Xu, X.; Li, D. Improving the particle filter for data assimilation in hydraulic modeling by using a Cauchy

likelihood function. J. Hydrol. 2023, 617, 129050. [CrossRef]

155. Kundrata, J.; Tomic, D.; Maretic, I.; Baric, A. Particle filter implemented as a hardware accelerator in Cortex-M core periphery. In
Proceedings of the 2021 44th International Convention on Information, Communication and Electronic Technology (MIPRO),
Opatija, Croatia, 24–28 May 2021; IEEE: Piscataway, NJ, USA, 2021; pp. 154–159. [CrossRef]

156. Ramachandran, B.; Mayberry, S.T.; Zhang, F. Acoustic Localization of Underwater Robots: A Time of Arrival-Based Particle
Filter Approach Using Asynchronous Beacon Pinging. In Proceedings of the 2023 8th International Conference on Automation,
Control and Robotics Engineering (CACRE), Guangzhou, China, 13–15 July 2023; IEEE: Piscataway, NJ, USA, 2023; pp. 294–299.
[CrossRef]

157. Cheng, Y.; Ren, W.; Xiu, C.; Li, Y. Improved Particle Filter Algorithm for Multi-Target Detection and Tracking. Sensors 2024,

24, 4708. [CrossRef]

158. Zhu, Y.; An, H.; Wang, H.; Xu, R.; Sun, Z.; Lu, K. DOT-SLAM: A Stereo Visual Simultaneous Localization and Mapping (SLAM)

System with Dynamic Object Tracking Based on Graph Optimization. Sensors 2024, 24, 4676. [CrossRef]

159. Wei, K.; Zheng, X.; Wei, W.; Song, M.; Zhang, J.; Gan, H.; Guo, Y.; Zhang, J. An algorithm of simultaneous localization and
mapping for mobile robots based on graph optimization. In Proceedings of the International Conference on Remote Sensing,
Mapping, and Image Processing (RSMIP 2024), Xiamen, China, 19–21 January 2024; Bilas Pachori, R., Chen, L., Eds.; SPIE:
Cergy-Pontoise, France, 2024; pp. 157–168. [CrossRef]

160. Zhou, H.; Kong, M.; Yuan, H.; Pan, Y.; Wang, X.; Chen, R.; Lu, W.; Wang, R.; Yang, Q. Real-time underwater object detection

technology for complex underwater environments based on deep learning. Ecol. Inform. 2024, 82, 102680. [CrossRef]

161. Ojha, A.K. Deep Learning Techniques for Enhanced Underwater Remote Sensing: Applications in Marine Biodiversity and

Infrastructure Inspection. J. Image Process. Intell. Remote. Sens. 2021, 4, 11–22. [CrossRef]

162. Wang, G.; Lin, H.; Wang, Q. Research on underwater target tracking method combining deep learning and kernel correlation
filtering. In Proceedings of the 2024 5th International Conference on Computer Vision, Image and Deep Learning (CVIDL),
Zhuhai, China, 19–21 April 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 1458–1461. [CrossRef]

Sensors 2024, 24, 7490

30 of 31

163. Sambath Kumar, R.; Sivaradje, G. A QoS-Aware Energy-Efficient Chimp Optimization Routing Protocol with Efficient Sensor

Node Deployment Strategy in Underwater Acoustic Sensor Network. J. Commun. 2023, 18, 665. [CrossRef]

164. Khan, S.; Singh, Y.V.; Yadav, P.S.; Sharma, V.; Lin, C.-C.; Jung, K.-H. An Intelligent Bio-Inspired Autonomous Surveillance System

Using Underwater Sensor Networks. Sensors 2023, 23, 7839. [CrossRef]

165. Arunodhayam, T.P.P.; Vadde, A.R.; Kumar, T.P.; Silas, S.; Gandu, S.P.; Kumar, C.H. Sustainable Energy Efficient Routing Protocol
using Chimp algorithm and SOM for Underwater Wireless Sensor Networks. In Proceedings of the 2023 International Conference
on Recent Advances in Science and Engineering Technology (ICRASET), Nagara, India, 23–24 November 2023; IEEE: Piscataway,
NJ, USA, 2023; pp. 1–4. [CrossRef]

166. Wang, F.; Zhao, L.; Xu, Z.; Liang, H.; Zhang, Q. LDVI-SLAM: A lightweight monocular visual-inertial SLAM system for dynamic

environments based on motion constraints. Meas. Sci. Technol. 2024, 35, 126301. [CrossRef]

167. Hansen, T.; Birk, A. An Open-Source Solution for Fast and Accurate Underwater Mapping with a Low-Cost Mechanical Scanning
Sonar. In Proceedings of the 2024 IEEE International Conference on Robotics and Automation (ICRA), Yokohama, Japan, 13–17
May 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 9968–9975. [CrossRef]

168. Liang, Z.; Wang, K.; Zhang, J.; Zhang, F. An Underwater Multisensor Fusion Simultaneous Localization and Mapping System

Based on Image Enhancement. J. Mar. Sci. Eng. 2024, 12, 1170. [CrossRef]

169. Nainggolan, J.H.P. Military Application of Unmanned Underwater Vehicles: In Quest of a New Legal Regime? Indones. J. Int. Law

2018, 16, 61–83. [CrossRef]

170. sub Song, K.; Chu, P.C. Conceptual Design of Future Undersea Unmanned Vehicle (UUV) System for Mine Disposal. IEEE Syst. J.

2012, 8, 43–51. [CrossRef]

171. Yang, Z.; Zou, Z. Multi-sensor data fusion method based on FPGA. In Proceedings of the 2023 2nd International Conference on
Artificial Intelligence and Computer Information Technology (AICIT), Yichang, China, 15–17 September 2023; IEEE: Piscataway,
NJ, USA, 2023; pp. 1–4. [CrossRef]

172. Yang, K.; Zhang, Z.; Cui, R.; Yan, W. Acoustic-optic assisted multisensor navigation for autonomous underwater vehicles. Ocean

Eng. 2024, 297, 117139. [CrossRef]

173. Wang, D.; Wang, B.; Huang, H.; Zhang, H. A Multisensor Fusion Method Based on Strict Velocity for Underwater Navigation

System. IEEE Sens. J. 2023, 23, 18587–18598. [CrossRef]

174. Wang, D.; Xu, X.; Yao, Y.; Zhang, T.; Zhu, Y. A novel SINS/DVL tightly integrated navigation method for complex environment.

IEEE Trans. Instrum. Meas. 2019, 69, 5183–5196. [CrossRef]

175. Oliveira, A.J.; Ferreira, B.M.; Cruz, N.A. Feature Extraction Towards Underwater SLAM using Imaging Sonar. In Proceedings of

the OCEANS 2023—Limerick, Limerick, Ireland, 5–8 June 2023 ; IEEE: Piscataway, NJ, USA, 2023; pp. 1–7. [CrossRef]

176. Ma, S.; Liang, H.; Wang, H.; Xu, T. An Improved Feature-Based Visual Slam Using Semantic Information. In Proceedings of the
2023 IEEE 6th Information Technology, Networking, Electronic and Automation Control Conference (ITNEC), Chongqing, China,
24–26 February 2023; IEEE: Piscataway, NJ, USA, 2023; pp. 559–564. [CrossRef]

177. Li, W.; Yi, F.; Peng, Y.; Zhang, M.; Liu, J. Construction of Topological Navigation Map Based on Model Fusion. In Proceedings of
the 2023 4th International Conference on Intelligent Computing and Human-Computer Interaction (ICHCI), Guangzhou, China,
4–6 August 2023; IEEE: Piscataway, NJ, USA, 2023; pp. 311–316. [CrossRef]

178. Guan, L.; Jin, R.; Li, D.; Li, J.; Lu, Y. A Real-Time Robot Location Algorithm Based on Improved Point-Line Feature Fusion. In
Proceedings of the 2023 International Conference on Advanced Robotics and Mechatronics (ICARM), Sanya, China, 8–10 July
2023; IEEE: Piscataway, NJ, USA, 2023; pp. 534–538. [CrossRef]

179. Xu, Z.; Haroutunian, M.; Murphy, A.J.; Neasham, J.; Norman, R. An underwater visual navigation method based on multiple

aruco markers. J. Mar. Sci. Eng. 2021, 9, 1432. [CrossRef]

180. Guth, F.A.; Silveira, L.; Amaral, M.; Botelho, S.; Drews, P. Underwater visual 3D SLAM using a bio-inspired system. In Proceedings
of the 2013 Symposium on Computing and Automation for Offshore Shipbuilding (NAVCOMP 2013), Rio Grande, Brazil, 14–15
March 2013; IEEE Computer Society: Washington, DC, USA, 2013; pp. 87–92. [CrossRef]

181. Shen, D.; Fang, H.; Li, Q.; Liu, J.; Guo, S. Increasing the localization accuracy of visual SLAM with semantic segmentation and

motion consistency detection in dynamic scenes1. J. Intell. Fuzzy Syst. 2023, 44, 7501–7512. [CrossRef]

182. Li, N.; Zhou, F.; Yao, K.; Hu, X.; Wang, R. Multisensor Fusion SLAM Research Based on Improved RBPF-SLAM Algorithm. J.

Sens. 2023, 2023, 3100646. [CrossRef]

183. Martínez-Barberá, H.; Bernal-Polo, P.; Herrero-Pérez, D. Sensor Modeling for Underwater Localization Using a Particle Filter.

Sensors 2021, 21, 1549. [CrossRef] [PubMed]

184. Wang, C.; Qiu, Y. Electronic Sensor Multi-Modal Slam Algorithm Based on Information Fusion Technology. In Proceedings of the
2023 International Conference on Ambient Intelligence, Knowledge Informatics and Industrial Electronics (AIKIIE), Ballari, India,
2–3 November 2023; IEEE: Piscataway, NJ, USA, 2023; pp. 1–6. [CrossRef]

185. Vargas, E.; Scona, R.; Willners, J.S.; Luczynski, T.; Cao, Y.; Wang, S.; Petillot, Y.R. Robust Underwater Visual SLAM Fusing
Acoustic Sensing. In Proceedings of the 2021 IEEE International Conference on Robotics and Automation (ICRA), Xi’an, China, 30
May–5 June 2021; IEEE: Piscataway, NJ, USA, 2021; pp. 2140–2146. [CrossRef]

186. Gschwendtner, M.; Bormuth, Y.; Soller, H.; Stein, A.; Walsworth, R.L. Quantum Sensing Can Already Make a Difference. But

Where? J. Innov. Manag. 2024, 12, 1–11. [CrossRef]

Sensors 2024, 24, 7490

31 of 31

187. Kantsepolsky, B.; Aviv, I. Quantum Sensing for the Cities of the Future. Int. Arch. Photogramm. Remote Sens. Spat. Inf. Sci. 2024, 48,

93–100. [CrossRef]

188. Merveille, F.F.R.; Jia, B.; Xu, Z. Advancements in Underwater Navigation: Integrating Deep Learning and Sensor Technologies for

Unmanned Underwater Vehicles. Preprints, 2024. [CrossRef]

189. Hadap, S.; Patil, M. Quantum Computing in Artificial Intelligence: A Paradigm Shift. Int. J. Adv. Res. Sci. Commun. Technol. 2024,

530–534. [CrossRef]

190. Meng, H.; Lu, H. A Survey of Deep Learning Technology in Visual SLAM. In Proceedings of the 2024 International Wireless
Communications and Mobile Computing (IWCMC), Ayia Napa, Cyprus, 27–31 May 2024; IEEE: Piscataway, NJ, USA, 2024;
pp. 0037–0042. [CrossRef]

191. Fekry, A.; Kamel, A.M.; Elhalwagy, Y.; Abosekeen, A. Deep Learning-Based Strategies for Integrated Autonomous Navigation: A
Review. In Proceedings of the 2024 International Telecommunications Conference (ITC-Egypt), Kafr El Dawwar, Egypt, 22–25
July 2024; IEEE: Piscataway, NJ, USA, 2024; pp. 692–697. [CrossRef]

Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual
author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to
people or property resulting from any ideas, methods, instructions or products referred to in the content.
