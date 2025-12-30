Contents lists available at ScienceDirect

Information Fusion

journal homepage: <www.elsevier.com/locate/inffus>

Multi-sensor integrated navigation/positioning systems using data fusion:
From analytics-based to learning-based approaches✩
Yuan Zhuang a,b,c, Xiao Sun a, You Li a,∗, Jianzhu Huai a, Luchi Hua d, Xiansheng Yang a,
Xiaoxiang Cao a, Peng Zhang a, Yue Cao e, Longning Qi d, Jun Yang d, Nashwa El-Bendary f,
Naser El-Sheimy g, John Thompson h, Ruizhi Chen a
a State Key Laboratory of Information Engineering in Surveying, Mapping and Remote Sensing, Wuhan University, Wuhan, China
b Hubei Luojia Laboratory, Wuhan, China
c Wuhan Unversity Shenzhen Research Institute, Shenzhen, China
d National ASIC Center, Southeast University, Nanjing, China
e School of Cyber Science and Engineering, Wuhan University, Wuhan, China
f Arab Academy for Science, Technology, and Maritime Transport (AASTMT), Aswan, Egypt
g Department of Geomatics Engineering, University of Calgary, Calgary, Canada
h School of Engineering, University of Edinburgh, Edinburgh, UK

A R T I C L E I N F O

A B S T R A C T

Keywords:
Machine learning
Data fusion
Estimation
Integrated navigation system
Multi-sensor
Positioning

Navigation/positioning systems have become critical to many applications, such as autonomous driving,
Internet of Things (IoT), Unmanned Aerial Vehicle (UAV), and smart cities. However, it is difficult to provide
a robust, accurate, and seamless solution with single navigation/positioning technology. For example, the
Global Navigation Satellite System (GNSS) cannot perform satisfactorily indoors; consequently, multi-sensor
integrated systems provide the solution, as they compensate for the limitations of single technology by using
the complementary characteristics of different sensors. This article describes a thorough investigation into
multi-sensor data fusion, which over the last ten years has been used for integrated positioning/navigation
systems. In this article, different navigation/positioning systems are classified and elaborated upon from three
aspects: (1) sources, (2) algorithms and architectures, and (3) scenarios, which we further divide into two
categories: (i) analytics-based fusion and (ii) learning-based fusion. For analytics-based fusion, we discuss the
Kalman filter and its variants, graph optimization methods, and integrated schemes. For learning-based fusion,
several supervised, unsupervised, reinforcement learning, and deep learning techniques are illustrated in multi-
sensor integrated positioning/navigation systems. Design consideration of these integrated systems is discussed
in detail from several aspects and their application scenarios are categorized. Finally, future directions for their
research and implementation are discussed.

1. Introduction

In recent decades, navigation/positioning systems have become
essential parts of many applications, such as driverless cars, the In-
ternet of Things (IoT), Unmanned Aerial Vehicle (UAV), and smart
cities. The state-of-the-art navigation/positioning systems include In-
ertial Navigation [1], Global Navigation Satellite System (GNSS) [2],
including Global Positioning System (GPS), BeiDou Navigation Satel-
lite System (BDS), GLObal NAvigation Satellite System (GLONASS),
and Galileo, Visible Light Positioning (VLP) [3], WiFi [4], Bluetooth

[5], Radio-Frequency Identification (RFID) [6], Ultra-Wideband (UWB)
[7], Ultrasonic [8], Magnetic [9], Odometer [10], Vision [11], LiDAR
[12], and 5G [13]. Different kinds of sensors, such as inertial sensors,
GNSS receivers, photodiodes, wireless receivers, magnetometers, and
cameras, are used in these navigation/positioning systems.

It is difficult to use single-sensor-based navigation/positioning sys-
tems to provide robust, accurate, and seamless solution, due to their
limitations. For instance, the Inertial Navigation System (INS) is a
relative positioning technology and only provides an accurate solution

✩

This work was supported by Excellent Youth Foundation of Hubei Scientific Committee, China (2021CFA040), Guangdong Basic and Applied Basic Research
Foundation, China (2022B1515120067), Open Fund of Hubei Luojia Laboratory, China (220100037), and Knowledge Innovation Program of Wuhan-Shuguang
Project, China (WHKXJSJ013).
∗ Corresponding author.

E-mail address:

<liyou@whu.edu.cn> (Y. Li).

<https://doi.org/10.1016/j.inffus.2023.01.025>
Received 5 August 2022; Received in revised form 27 January 2023; Accepted 30 January 2023

InformationFusion95(2023)62–90Availableonline3February20231566-2535/©2023TheAuthor(s).PublishedbyElsevierB.V.ThisisanopenaccessarticleundertheCCBY-NC-NDlicense(<http://creativecommons.org/licenses/by-nc-nd/4.0/>).Y. Zhuang et al.

Glossary

ADM
ANN
ANS
AOA
AP
ATEKF
AUV
BDS
BLE
CDKF
CNN
CSAC
CSI
DLL
DNN
DSRC
DVL
ECEF
EKF
EM
EnKF
FLAS
FKF
FLL
FOV
FPLL
GNN
GNSS
GPS
HAPS
IF
ISM
ISRUKF
IMM

Aircraft Dynamic Model
Artificial Neural Network
Autonomous Navigation System
Angle of Arrival
Access Point
Adaptive Two-stage EKF
Autonomous Underwater Vehicle
BeiDou Navigation Satellite System
Bluetooth Low Energy
Central Difference Kalman Filter
Convolutional Neural Network
Chip Scale Atomic Clock
Channel State Information
Delay Lock Loops
Deep Neural Networks
Dedicated Short-Range Communication
Doppler Velocity Log
Earth-Centered, Earth-Fixed
Extended Kalman Filter
Expectation–Maximization
Ensemble Kalman Filter
Fuzzy Logic Adaptive System
Federated Kalman Filter
Frequency Lock Loops
Field of View
Frequency-assisted Phase Locked Loop
Grey Neural Networks
Global Navigation Satellite System
Global Positioning System
High Attitude Platform Station
Intermediate Frequency
Industrial Scientific Medical
Iterated Square Root UKF
Interacting Multiple Module

for a limited time, as both inertial sensor errors and integration errors
will cause the solution to diverge. Thus, other absolute positioning
data sources, such as GNSS, are usually needed; however, although
they are accurate in open-sky environments, they suffer from signal
blockage and multipath in urban areas and other GNSS-challenging
environments. Other wireless positioning systems, such as WiFi and
Bluetooth, usually have some limitations, such as high dependency on
the distribution of Access Points (APs), noisy and unstable solutions,
labor costs for building databases, and the fluctuation of Received
Signal Strengths (RSS) indoors [14]. Magnetic positioning is usually
used indoors for local, as opposed to global positioning. Vision po-
sitioning, which often uses a camera to capture an object’s motion,
offers accurate localization at a relatively low cost [15]; however, it
has limitations, such as privacy issues, the extraction of features from
environments, and large computation load. It is difficult, therefore,
to achieve navigation/positioning goals while satisfying application
requirements, by using a single-sensor modality.

Consequently, to improve positioning performance, the advantages
of different kinds of sensors can be fully exploited to improve reliabil-
ity, robustness, and spatial and temporal coverage. Taking a GNSS/INS
integrated system as an example, GNSS provides the position and
velocity to aid inertial navigation by reducing cumulative errors, while
INS fills the gap in challenging environments by filtering its noise;
hence, integration reduces the limitations of both constituent parts.

IMU
IoT
INS
JDL
KF
kNN
LCI
LED
LiDAR
LIO
LS-SVM
LSTM
MAP
MEMS
MIMO
NCO
NLOS
PCA
PDR
PF
PLL
PnP
POS
PRN
PSOBPNN

PVA
PVT
RANSAC
RF
RFID
RFR
RISS
RMSE
RNN
RSS
RTK
SAE
SAR
SfM
SIG
SINS
SLAM

Inertial Measurement Unit
Internet of Things
Inertial Navigation System
Joint Directors of the Laboratories
Kalman Filter
k-Nearest Neighbor
Loosely-Coupled Integration
Light-Emitting Diode
Light Detection and Ranging
LiDAR-Inertial Odometry
Least Squares Support Vector Machine
Long Short Term Memory
Maximum A Posteriori
Micro Electromechanical Systems
Multiple-Input-Multiple-Output
Numerically-Controlled Oscillator
Non-Line-of-Sight
Principal Component Analysis
Pedestrian Dead Reckoning
Particle Filter
Phase Lock Loops
Perspective-n-Point
Position and Orientation System
Pseudo Random Noise
Particle Swarm Optimization Back Propaga-
tion Neural Network
Position, Velocity, and Attitude
Position, Velocity, and Time
Random Sample Consensus
Radio Frequency
Radio-Frequency Identification
Random forest regression
Reduced Inertial Sensor System
Root Mean Square Error
Recurrent Neural Network
Received Signal Strength
Real-Time Kinematic
Stacked Auto-Encoder
Synthetic Aperture Radar
Structure from Motion
Special Interest Group
Strapdown Inertial Navigation System
Simultaneous Localization and Mapping

Many similar positioning systems can be integrated with INS, such as
WiFi, Bluetooth, RFID, UWB, Ultrasonic, Magnetic, and Vision, which
can be divided into three categories: (i) Loosely-Coupled Integration
(LCI), (ii) Tightly-Coupled Integration (TCI), and (iii) Ultra-Tightly-
Coupled Integration (UTCI). LCI integrates different sources, based
on position and velocity levels, while TCI integrates sensor data in
ranging levels between transmitters and the receiver. Different from
LCI and TCI, UTCI integrates at a deeper level of raw measurements,
such as raw carrier phase and code phase, from a GNSS receiver.
Multi-sensor integrated systems can be used in many applications, such
as aircraft, underwater vessels, surface ships, spacecraft, cars, indoor
mobile robots, and UAVs.

Data fusion, which fuses diverse information from various sources,
is the most important part of integrated systems, a widely accepted
definition of which was provided by the Joint Directors of the Labo-
ratories (JDL) workshop [16]: ‘‘A multi-level process dealing with the

InformationFusion95(2023)62–9063Y. Zhuang et al.

SLFNs
STKF
STL
SVM
TDOA
TOA
TCI
TXCO

UAV
UHF
UKF
UPF
USBL
UTC
UTCI
UTP
UWB
VINS
VIO
VLC
VLP
VNS
VO
VTL
VTL_DI

WLAN
WSN
1DWF

Single-hidden Layer Feed-forward Networks
Strong Tracking Kalman Filter
Scalar Tracking Loop
Support Vector Machine
Time Difference of Arrival
Time of Arrival
Tightly-Coupled Integration
Temperature Compensated Crystal Oscilla-
tor
Unmanned Aerial Vehicle
Ultra-High Frequency
Unscented Kalman Filter
Unscented Particle Filter
Ultrashort Base Line
Coordinated Universal Time
Ultra-Tightly-Coupled Integration
Underwater Transponder Positioning
Ultra-Wideband
Visual-Inertial Navigation System
Visual-Inertial Odometry
Visible Light Communication
Visible Light Positioning
Visual Navigation System
Visual Odometry
Vector Tracking Loop
Vector Tracking Loops Based Deep Integra-
tion
Wireless Local Area Network
Wireless Sensor Network
One-Dimensional Wiener Filter

association, correlation, combination of data, and information from sin-
gle and multiple sources to achieve refined position, identify estimates
and complete and timely assessments of situations, threats, and their
significance’’. There are several categories of data fusion algorithms;
however, analytics-based and learning-based approaches are the most
widely used. An analytics-based approach uses an analytics function
to model system states and external measurements, which are called
‘estimations’ in the literature [17]. Many analytics-based methods are
widely used, such as Kalman Filter (KF) and Particle Filter (PF), while
several learning-based data fusion methods, such as Artificial Neural
Network (ANN), Fuzzy Logic, and Support Vector Machine (SVM)
are also used, since they can model systems without prior statistical
information about the process and measurement noise. Learning-based
methods sometimes perform better than analytics-based methods.

The literature relating to data fusion for integrated positioning/
navigation systems was investigated in [15,18–21]. Loebis et al. [18]
surveyed developments in Autonomous Underwater Vehicles (AUVs)
navigation and multi-sensor data fusion techniques to improve the
AUV’s navigation capability. Smith and Singh [19] covered the appli-
cations of various algorithms at different layers of the JDL model, and
highlighted the weaknesses and strengths of their applications. Ben-Afia
et al. [15] presented a classification of vision-based fusion techniques
in unknown environments. Yassin et al. [20] surveyed wireless-based
indoor positioning technologies and generally introduced hybrid sys-
tems combining inertial sensors, cameras, and map matching. Guo
et al. [21] presented fusion-based indoor positioning techniques and
systems bearing three fusion characteristics: source, algorithm, and
weight spaces.

A comparison of these surveys and our work is shown in Table 1.
The article [18] concentrated only on the navigation applications of

Fig. 1. The overall architecture of the whole system.

underwater vehicles with a limited range of sources. The survey [19] fo-
cused on the JDL framework but did not discuss positioning/navigation
sources and application scenarios. Moreover, both [18,19] are out of
date. The survey [15] only focused on vision-based positioning and did
not mention any learning-based methods. The article [20] systemati-
cally discussed wireless positioning but only introduced a small range
of sensor fusion indoors. The survey [21] discussed both analytics-
based and learning-based methods, and gave an in-depth survey on
integration sources. But their topic is limited to indoor positioning and
their discussions on algorithms and design consideration are not com-
prehensive. In addition, optimization-based methods and integration
scheme-based classifications were not explicitly discussed by either of
these surveys.

We organize the text from three layers: sensors, integration algo-
rithms and architectures, as well as application scenarios. The overall
architecture of the system is depicted in Fig. 1. The detailed layout of
this article is shown in Fig. 2. The main contributions are:

• Based on the sensor integration, we classified multi-sensor fusion
into (i) absolute/relative, (ii) relative/relative, and (iii) abso-
lute/absolute integration. Innovatively, we classify absolute po-
sitioning sources into five categories: (1) radio-based, (2) light-
based, (3) audio-based, (4) field-based, and (5) vision-based,
based on their physical properties. The three categories of multi-
sensor combinations are also subdivided in our article, which
expands the depth of Guo et al. [21].

• The focus here is on analytics-based and learning-based sys-
tems, grounded on data fusion algorithms. Most systems are
interdisciplinary and have been designed for multiple scenarios.
Specialized schemes such as Visual-Inertial Odometry (VIO) are
not discussed in detail. In addition, the algorithms and inte-
gration architectures of analytics-based systems have been sur-
veyed from three aspects: loosely-coupled, tightly-coupled, and
ultra-tightly-coupled.

• We further discuss the analytics-based algorithms and integration
architectures. Filtering-based navigation systems have dominated
in the past several decades; however, analytics-based algorithms
are not limited to filtering-based methods, but also to graph
optimization. We also subdivide the learning-based positioning
and navigation methods into supervised learning, unsupervised
learning, deep learning, and reinforcement learning.

• We classify application scenarios into six categories, each one
with a certain number of examples and analyses. Some hot topics,
e.g., automated driving and UAVs, are explicitly discussed.

InformationFusion95(2023)62–9064Y. Zhuang et al.

Fig. 2. Overall classification of this article with respect to integrated positioning/navigation systems.

Table 1
Comparison of previous works with ours.

Features

[18]

[19]

[15]

[20]

[21]

Ours

Published year
Classification of integrated navigation/positioning systems based on sources
Classification of analytics-based data fusion
Optimization-based algorithms
Classification of integration architectures
Classification of learning-based data fusion
Design consideration
Application scenarios
Future research directions

2002
Limited
General
NO
NO
NO
General
Underwater only
General

2006
NO
Limited
NO
NO
Limited
General
NO
General

2014
Limited
General
NO
General
NO
NO
NO
General

2017
Limited
General
NO
NO
General
General
Indoor only
Explicit

2020
Limited
Explicit
NO
NO
General
General
Indoor only
Explicit

–
In-Depth
Explicit
Explicit
Explicit
Explicit
Explicit
Wide coverage
Explicit

• We present a comprehensive tutorial on design consideration.
This section discusses the selection between analytics-based and
learning-based systems, state selection and observability, real
time consideration, scalability, time synchronization, and the ro-
bustness of outliers. We also give some future research directions
for the field of integrated navigation/positioning.

This article will discuss integrated positioning/navigation systems,
thus: Section 2 discusses inertial navigation systems, various wire-
less positioning systems, and systems that use different sources; Sec-
tion 3 presents analytics-based multi-sensor data fusion methods, and
Section 4, learning-based multi-sensor data fusion systems; Section 5
presents design consideration before a system is implemented; Section 6
presents and categorizes application scenarios of the various systems;
Section 7 discusses future directions for research and implementation;
Section 8 presents a summary of our work.

2. Positioning/navigation sources

In this

section, we present widely-used single positioning/
navigation systems and classify integrated positioning/navigation sys-
tems concerning source categories.

2.1. Single positioning/navigation systems

Here, we present some widely-used single positioning/navigation
systems, including INS, GNSS, Visible light communication, WiFi, Blue-
tooth, RFID, ultrasonic, magnetics, odometer, vision, LiDAR, and 5G.
Some future positioning technologies (e.g., Terahertz-band localization
for 6G) have not yet been used, thus they are not covered.

2.1.1. Inertial navigation

Inertial navigation was developed several decades ago for military
applications, such as missiles, aeroplanes, and ships, by using inertial
sensors, including accelerometers and gyroscopes [1]. Inertial sensors
can be navigation grade, tactical grade, auto grade, and low-cost grade
[22]; their performance and cost are significantly different. Inertial
navigation uses the measurements from accelerometers and gyroscopes
to estimate the position, velocity, and attitude of the platform through

algorithms, such as INS mechanization, Pedestrian Dead Reckoning
(PDR), and motion constraints [23]. Due to errors in inertial sensors
and integral computations, as used in inertial navigation algorithms,
their accuracy degrades accumulatively, depending on inertial sensor
errors [24]. By using self-contained inertial sensors, inertial navigation
is independent of any external information, so it is not affected by
external electromagnetic interference. Inertial navigation can be used
in many environments – sky, ground, and underwater – and applied to
both vehicles and pedestrians. It offers position, velocity, and attitude
solutions with a high update rate, short-term accuracy, and good sta-
bility; its drawback, though, is that navigational errors increase over
time, thus its long-term accuracy is poor [25].

2.1.2. Global navigation satellite system

GNSS was developed in the 1960s to provide a real-time, all-
weather, global, land/sea/air navigation service in intelligence gath-
ering, nuclear explosion monitoring, and emergency communications
[2], since it can measure the distance between satellite and receiver
by using Time of Arrival (TOA) combined with data from multiple
satellites, to estimate a location to an accuracy ranging from a few
meters to centimeters [26]. However, since GNSS is vulnerable to
interference from signal blockage, multipath, and electromagnetism
[27], it is not accurate in either urban canyons or indoors. To over-
come these disadvantages, it must be integrated with other positioning
technologies, such as INS [26,28–32], WiFi [33], and UWB [29,34–36].
INS is an ideal complementary data source since integration reduces
the disadvantages of inertial dead-reckoning and GNSS’s line of sight.
When a GNSS signal is interrupted, or blocked, the inertial sensor
enables the system to coast until it is re-established. The integration of
GNSS and INS improves the quality and integrity of each module and
also allows calibration of inertial instrument biases, while the inertial
sensors improve the performance of the GNSS receiver [37].

2.1.3. Visible light positioning

Visible Light Communication (VLC), which uses optical light instead
of radio waves to transmit data [38], is a relatively recent development
that has many advantages over other systems, such as high energy
efficiency, long lifetime, low heating, high data rate; it does not harm
the human body [39,40]. Consequently, it is now applied to positioning

InformationFusion95(2023)62–9065Y. Zhuang et al.

in the navigation field and realizes a new positioning technology called
VLP [3]. A practical VLP system usually includes Light-Emitting Diode
(LED) lamps as the transmitters, and a photodiode, or camera, as the
receiver. The optical signals can be interpreted in many modes [41],
such as RSS, TOA, Time Difference of Arrival (TDOA), and Angle of
Arrival (AOA). Recent studies have applied several positioning algo-
rithms, such as proximity [42], trilateration [43], multilateration [44],
and fingerprinting [45], for each mode. Accuracy of most VLP systems
is a few centimeters because the optical signal is not sensitive to fading,
severe multipath interference, and electromagnetic wave interference
[3]. However, VLP is affected by shadowing or blocking as the optical
signals cannot pass through opaque objects.

2.1.4. WiFi

Currently, WiFi is used almost everywhere, from IoT to Smart Cities,
which support several IEEE 802.11 protocols; it has been researched
for around twenty years [4] and its hardware usually includes WiFi
routers or APs as the transmitters and WiFi receivers as receivers.
Flight times, arrival angle, Channel State Information (CSI), and RSS are
common measurements in WiFi positioning systems. Many algorithms,
such as trilateration [4], fingerprinting [4], and Kalman filtering [46],
are commonly used in them. WiFi-based positioning systems have
the advantages of supporting smart devices, acceptable positioning
accuracy (1–10 m), and good portability; also, they do not require ad-
ditional infrastructure, and have both wide coverage and low cost [47].
However, WiFi signals are susceptible to interference from multipath,
signal blockages, AP distribution, measurement fluctuation [23], and
extensive labor costs for database building [48]. As for algorithms of
data fusion, analytics-based methods, such as Extended Kalman Filter
(EKF) [23] and optimization methods [49] have been used in the
WiFi/inertial system for indoor pedestrian and robot applications.

2.1.5. Bluetooth

Bluetooth is a short-range data exchanging technology that uses
short-wavelength Ultra High Frequency (UHF) radio waves in the In-
dustrial Scientific Medical (ISM) band from 2.400 to 2.485 GHz [50].
Managed by the Bluetooth Special Interest Group (SIG), it is widely
used in IoT applications due to its low power consumption. As with
WiFi positioning, the BLE system usually uses beacons as both transmit-
ters and receivers, while positioning uses RSS values as measurements.
The algorithm categories are: proximity [51–53], multilateration [5,52,
54], fingerprinting [5,52,55], and the integration of multilateration and
fingerprinting [5]. The BLE beacons have the advantages of being small,
lightweight, low cost, low dissipation, and they are widely supported by
smart devices. Compared to WiFi, BLE is less energy-hungry, has greater
smart-device support, is more flexible and is easier to deploy. However,
it has similar limitations to WiFi, such as high labor costs in fingerprint
database building, and performance degrades due to multipath, signal
blockages, and RSS fluctuation [5]. Furthermore, since BLE and WiFi
share the 2.4 GHz band, BLE systems are frequently disrupted by WiFi
and other BLE devices. The literature shows that BLE/INS integrated
navigation is mostly realized by RSS [14,56–58] and sometimes by ToA
[59]. Furthermore, since Bluetooth 5.1 protocols were released in 2019,
its Angle of Arrival (AOA) positioning accuracy has improved [60,61].

2.1.6. Radio frequency identification

Another popular technology for many IoT applications, RFID often
employs Radio Frequency (RF) RSS and AOA to indicate the distance
between transmitter and receiver. Its tags, such as active, passive, and
semi-active, can be selected for positioning, and its accuracy varies
from centimeter-level to room-level, depending on the distribution of
tags and the selection of positioning algorithms [6]. The desirable
features that have made it so attractive, include contactless commu-
nications, high data rate, high security, non-line-of-sight readability,
compactness, and low cost [62]. In this positioning method, the RFID
reader is attached to a tracked object while active and passive tags are
placed on the ceiling and floor [63]. Its potential application scenarios
are indoor positioning and pedestrian navigation.

2.1.7. Ultra-wideband

UWB wireless communications, which communicates with a pulse
in a very short time interval (>1 ns), and without using a carrier,
operates in three categories: communications, positioning, and radar
[7]. Its positioning algorithms can be categorized into four groups: TOA
[64,65], TDOA [66], AOA [67], and RSS [68]. Its high bandwidth and
extremely short pulse waveforms make it effective in Non-Line-Of-Sight
(NLOS) environments, reduces the effects of multipath, consumes less
energy, and achieves centimeter-level positioning accuracy [47,69].
However, extra infrastructure is needed and signals become disturbed
by liquids and metals; it can also be interfered with by other systems
operating in the ultra-wide spectrum due to misconfiguration [69].
Also, the extremely short pulses may cause longer synchronization
time.

2.1.8. Ultrasonic

Inspired by bats’ night navigation, ultrasonic systems, which have
been researched for several years, can be categorized into two groups,
(i) using a tag as a receiver mounted on the object, and multiple
transmitters installed on a wall or ceiling [8]; and (ii) using a tag as
a transmitter mounted on the object and multiple receivers installed
on a wall or ceiling [70]. Depending on the accuracy required and
the operator’s budget, ultrasonic positioning mainly adopts trilatera-
tion and proximity [8] to process the TOA or TDOA measurements
[8,70]. Ultrasonic can achieve centimeter-level accuracy with densely
distributed nodes and room-level accuracy with sparsely distributed
nodes. This system offers several advantages, including low system
cost, high reliability and scalability, high energy efficiency, and most
importantly, zero leakage between rooms [71]. However, its perfor-
mance may vary in different environments because the transmitting
speed of the sound in the air can easily be affected by humidity and
temperature. Furthermore, its performance may suffer from reflected
ultrasound signals and environmental noise [72].

2.1.9. Magnetics

Most applications of low-frequency quasi-static magnetic fields in
short-range position and orientation measurements are based on free-
space field geometry [73]. They provide a positioning solution with
an accuracy of several meters without the aid of other systems and
can compensate for some wireless-based positioning technology. In-
door artificial disturbances created by electrical currents in metal or
other conducting structures may disturb wireless-based positioning, but
magnetic abnormalities created by these interferences can be used as
fingerprints or landmarks [74,75]. However, magnetic solutions are
not universally applicable, as they can result in significant localization
errors.

2.1.10. Odometer

An odometer is an instrument used for measuring the rotation of
the wheels of a land vehicle and giving information on the traveled
speed and distance. Odometers have traditionally been fitted to the
transmission shaft; however, most recent vehicles have an odometer
on each wheel. Thus, an odometer is also known as a wheel speed
sensor. By differentiating left and right odometer measurements, the
yaw rate of the vehicle may be measured, which is a technique known
as differential odometry [24]. Please note that the odometer is different
from the word ‘odometry’, of which the latter is a method using data
from motion sensors (e.g., camera, LiDAR, odometer) to estimate the
change in position over time. Since odometers are commonly used on
land vehicles, plenty of works on GNSS/INS integration used the aid
of an odometer [10,76,77]. It is useful to improve the accuracy of
position, velocity, and attitude during long GNSS outages [76].

InformationFusion95(2023)62–9066Y. Zhuang et al.

2.1.11. Vision

Vision-based systems, using cameras installed on surveillance and
smart devices allowing images, or videos, to estimate an object’s posi-
tion, are more robust than wireless-based systems. They can be catego-
rized into two groups, (i) where cameras are placed in a fixed location
[11], and (ii) where cameras are placed on mobile devices [78]. In the
first group, image-based camera localization can be classified into two
categories [79]: with and without known environment. With known
environment, a camera’s absolute pose (position + orientation) can be
determined by features whose types can be points, geometric, semantic,
etc. [80], where points are most widely used, called Perspective-n-Point
(PnP) problem [79]. These methods in outdoor environment often need
prior information given from other sensors (GNSS [81,82] and magnet-
ics [80]). In unknown environment, that is a Simultaneous Localization
and Mapping (SLAM, real-time) or Structure from Motion (SfM, post-
time) problem [80]. SLAM’s typical positioning technologies are Visual
Odometry (VO) and Visual-Inertial Odometry (VIO), in which only
relative pose can be solved. The second group is also known as visual
tracking [83] and can be integrated with motion detection. Yan et al.
[11] used an installed camera monitoring a long corridor for visual
tracking to aid PDR.

Extensive research has been conducted on visual odometry and
mapping. Vision odometry (VO), which is a likely replacement for
traditional odometry, collects image data by a camera mounted on
the agent and performs pose estimation by associating homologous
points in different images. Well-known vision-based algorithms include
MonoSLAM [84], ORB-SLAM [85], DSO [86], OV2SLAM [87]. Readers
can refer to [88] for a survey of monocular SLAM, and [89] for a survey
of visual odometry and mapping approaches with deep learning as the
workhorse.

Motion estimation by fusing vision and Inertial Measurement Unit
(IMU) enables many applications in robotics. Considering the comple-
mentary characteristics of vision and inertial sensors, VIO is a good
inertial navigator, exemplified by a legged, or wheeled, robot working
in a factory, a field, or indoors. The literature on visual-inertial odom-
etry and mapping is extensive, and notable work includes MSCKF [90],
OKVIS [91], VINS-Mono [92], KSWF [93], OpenVINS [94], and ORB-
SLAM3 [95]. Readers can refer to [96] for a survey on visual-inertial
odometry and [89] a recent survey on it, based on deep learning.

2.1.12. LiDAR

3-D Light Detection and Ranging (LiDAR) sensor, which can provide
direct, dense, active, and accurate depth measurements of environ-
ments [12], has emerged as an essential sensor for vehicles [97–99],
such as self-driving cars and autonomous UAVs. LiDAR collect point
cloud data of surrounding objects with a high sampling rate (typically
10 Hz [12,100]); thus it is useful to determine the pose change of
the vehicle itself. LiDAR positioning is mostly a relative positioning
method and also named LiDAR odometry [12,100]. LOAM [101] is the
most classical real-time LiDAR odometry, which sequentially registers
extracted edge and planar features to an incrementally built global
map. On the basis of LOAM, there are further studies, e.g., LeGO-LOAM
[102], Fast-LOAM [103].

With the help of inertial sensors, LiDAR-inertial odometry (LIO)
can considerably increase the accuracy and robustness of the LiDAR
odometry by compensating for the motion distortion in a LiDAR scan
and providing a good initial pose [12]. LINS [100] introduced a tightly-
coupled iterative Kalman filter and robocentric formula into the LiDAR
pose optimization in the odometry. FAST-LIO2 [12] proposed a new
data structure ikd-Tree that supported incremental map updates at
every step and efficient inquiries. LIO-SAM [104] firstly formulated
LIO odometry as a factor graph, which allowed a multitude of relative
and absolute measurements, including loop closures, to be incorporated
from different sources as factors into the system. In self-driving applica-
tions, GNSS, IMU, LiDAR, camera, and radar can be fused to complete
multiple tasks [105,106].

2.1.13. 5G networks

5G (5th Generation Mobile Communication Technology) localiza-
tion is a technology using cellular networks [107]. Unlike 2G/3G/4G
localization with low accuracy, 5G has a potential to achieve a
centimeter-level ranging accuracy [20]. Besides, higher signal band-
widths, denser networks, and Multiple-Input–Multiple-Output (MIMO)
technologies also significantly increase the ranging accuracy for signal
propagation delay based positioning methods like TDOA [107]. The
frequencies allocated for the 5G include sub-6 GHz and mm-wave
bands, both of which can be used for localization [108]. Since it is
not long after 5G was put into use, researches on 5G positioning mostly
used simulated results, seldom with real tests [13,108,109]. Decurninge
et al. [109] measured Channel State Information (CSI) data using a
32 dual-polarized antenna array at the base station and used extreme
learning machines to estimate a single antenna’s position. Shamaei and
Kassas [108] used a software-defined receiver to extract pseudorange
measurements on 600 MHz bands and their ranging error was 1.19 m.
Recently, Chen et al. [13] achieved ToA ranging accuracy of 0.5 m in
indoor field tests using 5G new radio carrier phase measurements in
the sub-6-GHz.

Single positioning/navigation systems are summarized in Table 2.

2.2. Multi-sensor integrated positioning/navigation systems

Section 1 has given the definition of relative and absolute po-
sitioning. Based on this definition, this subsection classified multi-
sensor integrated systems into: (i) absolute/relative integration, (ii)
relative/relative integration, and (iii) absolute/absolute integration sys-
tems.

2.2.1. Absolute positioning sources

Absolute positioning, which determines the object’s position and
attitude in a fixed reference frame, can be categorized by five aspects:
(1) radio-based, (2) light-based, (3) audio-based, (4) field-based, and
(5) vision-based. Radio-based positioning is a large family that includes,
but not limits to, GNSS, WiFi, Bluetooth, RFID, UWB, and 5G. They
use man-made emission source to produce electromagnetic waves in
radio frequency bands for localization. VLP (refer to Section 2.1.3),
using LED lamps as transmitters, and a photodiode, or camera, as the
receiver, is the dominantly used light-based positioning. Audio-based
positioning technologies, including ultrasonic [8,9] and acoustic [111]
in the audible spectrum, are mainly used indoors. Both ultrasonic and
acoustic positioning can be integrated with INS [112,113]. Other types
of audio-based hybrid systems can be referred to Section 2.1.8. Field-
based positioning navigates by matching the database storing field
information. The commonly used field-based positioning sources in-
clude magnetics, gravity, and map. Magnetic-based positioning, which
is mainly used indoors, has been discussed in Section 2.1.9; gravity
matching can be used in underwater passive navigation systems to
overcome the INS error accumulation and on land with the terrain con-
tour matching [114]; map matching can aid other sensors with reliable
location constraints in indoor positioning [115,116] (in Section 6.2)
and is also available in urban environments [117]. Vision is capable of
both absolute and relative positioning. In addition, Synthetic Aperture
Radar (SAR), which uses active microwave imaging radar, is a kind of
generalized visual positioning technology [118].

2.2.2. Relative positioning sources

Relative positioning, which determines the object’s position and
attitude in a moving reference frame or only determines velocity and
angular rate, mainly includes (1) inertial sensors and (2) vision. Since
INS and vision have been discussed above in detail, we pay more
attention on another inertial system, Pedestrian Dead Reckoning (PDR),
here. PDR systems use inertial sensors, which are often combined
with domain-specific knowledge about walking, to track user move-
ments. Specific to pedestrians, PDR estimates 2D position by accruing

InformationFusion95(2023)62–9067Y. Zhuang et al.

Table 2
Single positioning systems.

Systems

Setup

Positioning methods

Accuracy

Advantages

Drawbacks

INS/PDR/Motion
constraints

Accuracy depends
on time

Self-contained,
anti-interference

Navigation error
accumulates over time

From centimeters
to meters

Wide coverage in the
whole world

Inertial
navigation
[1,22–25]

GNSS [2,26–37]

VLP [3,38–45]

Inertial sensors
(accelerometers,
gyroscopes)

GNSS satellites,
receivers

LED lamps and
photodiode or
camera

WiFi [4,23,46–49]

WiFi routers or
access points

Bluetooth
[5,14,50–60,110]

BLE beacons

TOA

RSS/TOA/
TDOA/AOA

Trilateration/
fingerprinting/
Kalman filtering

Proximity/
multilateration/
fingerprinting

Few centimeters

3–10 m

1–5 m

RFID [6,62,63]

RFID tags

RSS

0.1–2 m

UWB [7,47,64–69]

UWB tags

RSS/TOA/TDOA/AOA

Few centimeters

Ultrasonic
[8,70–72]

Ultrasonic tags

Trilatera-
tion/proximity

Accuracy depends
on the distribution
density of
infrastructures

Not sensitive to
severe multipath
interference and
electromagnetic
interference

No additional
infrastructure, low
price, wide coverage

Low cost, easy to
deploy

High data rate, high
security,
non-line-of-sight
readability,
compactness, low cost

Low energy cost and
insensitive to
multipath effect

Low system cost,
reliability, scalability,
high energy
efficiency, and zero
leakage between
rooms

Magnetic [73–75]

Magnetometers

Fingerprinting

Several meters

Low cost

Odometer
[10,76,77]

Odometers

Read from wheel
rotation

Accuracy depends
on time

Self-contained,
anti-interference

Vision
[11,78–93,96]

Cameras

Feature Detection and
Tracking

Accuracy depends
on time

LiDAR
[12,97–106]

LiDAR sensors

Feature Detection and
Tracking

Accuracy depends
on time

5G
[13,20,107–109]

5G base stations
and antennas

RSS/TOA/TDOA/
AOA/CSI

Submeters

Not sensitive to
multipath effect and
no extra
infrastructure needed

Precise laser ranging,
high time resolution,
not sensitive to
multipath effect

High ranging
accuracy, high
capacity, high
reliability

Potential
integrated sources

Almost all sources

Unstable in dense
urban canyons and
indoor environments

Signal blockages

INS, wireless
systems and
magnetics

Bluetooth and
PDR

Susceptible to signal
interference and
blockage

Performance degrade
by multipath effects
and signal blockage

Requires heavy
infrastructure for
accurate positioning

Signal blockage
caused by liquid and
metallic materials

Transmission speed
depends on
environment and the
performance may
suffer from the
environmental noise

Only work in a local
area

Only determine
forward and heading
changes

Need large
computational
resources

Inertial sensors,
magnetics and
Bluetooth

Inertial sensors
and WiFi

WSN and inertial
sensors

GNSS and inertial
sensors

RF signals, inertial
navigation and
magnetometer

GNSS, inertial
navigation and
WiFi

GNSS and inertial
navigation

UWB, GNSS and
inertial navigation

Large cost, susceptible
to the weather

GNSS, inertial,
and vision
navigation

Signal blockages and
multipath

GNSS

{distance, heading} vectors representing either steps or strides [119].
Through smartphone market penetration, inexpensive MEMS sensors
become ubiquitous and give rise to the wide use of PDR. To prevent
PDR from error accumulation, radio-based positioning technologies
that are available on smartphones (e.g., Wifi [46,120,121], BLE [122–
124], and UWB [125,126]) can be integrated with it.

2.2.3. Absolute/relative integration

Fusion of one absolute and one relative positioning systems is the
standard type of the integrated navigation/positioning system. Since
most hybrid systems have inertial sensors, we classify this one–one in-
tegration type into five categories: (1) radio/inertial, (2) light/inertial,
(3) audio/inertial, (4) field/inertial, and (5) vision-based fusion. These
inertial systems include INS and PDR. An integration system with rela-
tive positioning but without inertial systems are very rare, e.g., GPS/VO
[127].

These five categories differ physically, therefore, their usages and
advantages are different. Radio/inertial is the dominant integrated
navigation system, due to the extensive coverage of GNSS and the wide
usage of WiFi and BLE. This category can have wide coverage and sys-
tem capacity, but its accuracy is susceptible to multipath interference
and NLOS, especially indoors. Similar to radio, light-based positioning
uses light wave for positioning. VLP suffers more from signal blockages
and narrow coverage, but is not sensitive to fading, multipath, and
electromagnetic wave interference, and is more accurate in indoor
environments [3]. Audio’s propagation speed is much lower than that
of electromagnetic waves. Thus, it is much easier to measure the Time
of Flight (ToF). Audio-based positioning is accurate in ranging but is not
robust in the dynamic cases [111]. Different from the three categories
above, field-based positioning does not suffer from environmental in-
terference. On the contrary, complex scenes may contain more features
for localization (e.g., a capsule endoscope positioning system [128]),
which makes field matching an ideal technology to compensate for

InformationFusion95(2023)62–9068Y. Zhuang et al.

other absolute positioning systems. Vision-based fusion systems herein
do not cover VO and VIO, since vision here is absolute positioning.
Its fusion sources include GNSS [81,82], magnetics [80], BLE [129],
WiFi [130], and inertial sensors [11,130], which has been discussed in
2.1.11.

2.2.4. Relative/relative integration

Besides the typical absolute/relative integration, there are fusion
systems including two relative positioning systems, most of which
include inertial sensors. With the low cost of cameras and the devel-
opment of computer vision, vision is a common choice to aid INS to
retard the error accumulation [131–134], and thus, gives rise to Visual-
Inertial Odometry (VIO, discussed in Section 2.1.11). Visual-inertial
integration is applicable to a wide range of scenes, including indoor
[131], outdoor vehicles [133], surface ships [134], and outer space
[132]. To further restrain error accumulation, visual-inertial systems
can be aided with an absolute positioning source [131,132,134].

Other relative positioning technologies including odometer, speed
log, Doppler velocity log (DVL), PDR, and LiDAR can also aid INS,
depending on the application scenarios. The odometer and DVL are
all instruments that measure speed. Land vehicles are usually equipped
with odometers; thus, they are very convenient to be integrated with in-
ertial sensors [10,76,77]. Ships and Autonomous Underwater Vehicles
(AUVs) that are not equipped with odometers can use speed logs as an
alternative [135–137]. They measure velocities depending on Doppler
effects. Pedestrian users can use PDR to integrate with INS [138],
although they may share the same inertial sensors. The miniaturization
of LiDAR gives it a larger stage for land vehicle [97,98], especially
automated driving [99], which will be discussed in Section 6.1.

2.2.5. Absolute/absolute integration

Without relative positioning, there are also works using two ab-
solute positioning sources. Two radio-based systems, although shares
similar physical properties, can be integrated together to compen-
sate with each other. These works include WiFi/BLE [52,139,140],
RFID/Wireless Sensor Network (WSN) [141], and GNSS/5G [142,143].
Since radio can connect vehicles via communication channels, radio-
ranging-based positioning technologies, e.g., Dedicated Short-Range
Communication (DSRC) [144] and UWB [145], can be used to measure
the vehicle-to-vehicle distances for cooperative localization. But these
systems can hardly get velocity and attitude information as inertial
sensors do, and may suffer from low sample rates [139].

Due to the shortages of INS-free fusion systems, fusing two absolute
positioning sources with an inertial sensor is an alternative. GNSS
can hardly provide reliable positioning results in sheltered conditions
while other radio-based sources can if infrastructures are provided.
In this way, WiFi [33], RFID [146], BLE [59], and UWB [29,35,36]
can be integrated with the GNSS/INS system to further improve the
performances under GNSS-challenging conditions. Similarly, two radio-
based systems excluding GNSS can also be integrated with the inertial
sensors (e.g., RFID/UWB/PDR integration [125], WiFi/BLE/INS [14]).
Each absolute positioning category has its own physical properties,
thus, multi-categories fusion may better compensate for each other.
Radio-based and field-based positioning sources are the most com-
monly used, most of fusion systems with two absolute positioning cat-
egories include them. Radio-based systems are susceptible to signal oc-
clusion while field-based systems do not, thus they can compensate for
each other. There are works choosing radio/field integration, including
GPS/map [147], GPS/magnetics [148,149], UWB/magnetics [150],
Wifi/map [115,151,152], and Wifi/magnetics [75,153,154]. Since the
frequency bands of the radio differ much from light’s, radio-based
positioning aided VLP is applicable [155]. As for radio/vision fusion,
Gao et al. [118] proposed an INS/GPS/SAR system where GPS/INS in-
tegration provides pseudo ranges and their change rates while SAR pro-
vides azimuth and pitch. In addition, the works [9,112] used magnet-
ics/ultrasonic integration indoors where magnetics provides distances
and ultrasonic provides attitudes.

3. Analytics-based multi-sensor data fusion for integrated posi-
tioning/navigation

3.1. Classification based on algorithms

Estimation is extracting the value of a hidden quantity from indirect,
inaccurate, and uncertain measurements, the main goal to minimize the
state estimation error, while counteracting uncertainties and perturba-
tions [17]. To differentiate estimation approaches from learning-based
ones, they are defined as analytics-based methods. In integrated navi-
gation systems, the most widely used method is the KF, introduced by
Rudolf Kalman in 1960 [156], which is suitable for linear systems with
Gaussian noises. However, most real-world applications are nonlinear
and/or non-Gaussian, which limits KF. Consequently, some variants,
including the EKF and the Unscented Kalman Filter (UKF) are applied,
which are classified as linearization based filters, sigma point based
filters, and Monte Carlo based filters.

In the past decade, the PF has become an effective tool for solving
nonlinear analytic problems with a non-Gaussian noise distribution due
to increased computational power. More recently, graph optimization
has become popular among researchers, since it is globally designed
and makes full use of historical information. Fig. 3 shows a general clas-
sification of the main algorithms used for state estimation in integrated
navigation systems.

3.1.1. Kalman filter

Kalman filter is a recursive analytics-based method, using the es-
timation of the last state and the observation of the current state to
find the optimal estimate of the current state, which is widely used in
multi-sensor data fusion for integrated navigation systems. KF assumes
that variables and noises are Gaussian distributed, and the system is
linear. The KF process and its state is described in two variables:

• 𝐱𝑘 represents the system state at time 𝑘.
• 𝐏𝑘 represents the covariance matrix, showing the accuracy of the

estimate.

The KF operation consists of two phases: prediction and update.
In prediction, the filter uses an estimated previous state to estimate
current state.

𝐱−
𝑘 = 𝐀𝐱𝑘−1 + 𝐁𝐮𝑘
where 𝐱−
𝑘 is the prediction state at time 𝑘, 𝐀 is the state transition
matrix acting on 𝐱𝑘−1, 𝐁 is the control matrix and 𝐮𝑘 is the control
vector. The predicted covariance of 𝐱−

(1)

𝑘 is

𝑘 = 𝐀𝐏𝑘−1𝐀𝑇 + 𝐐
𝐏−

(2)

where 𝐐 is the covariance of noise. During the update phase, the filter
optimizes the predicted state using current observations to obtain a
more accurate new estimate. Both this estimate and its covariance
are obtained with a weighting strategy, whose weight is expressed as
Kalman gain 𝐊𝑘.

𝐱𝑘 = 𝐱−

𝑘 + 𝐊𝑘

(𝐳𝑘 − 𝐇𝐱−

𝑘

)

𝐊𝑘 = 𝐏−

𝑘 𝐇𝑇 (𝐇𝐏−

𝑘 𝐇𝑇 + 𝐑)−1

𝐏𝑘 =

(𝐈 − 𝐊𝑘𝐇) 𝐏−

𝑘

(3)

(4)

(5)

where 𝐇 is the design matrix that maps the state space to the obser-
vation space, 𝐳𝑘 is the measurement of time 𝑘, and 𝐑 is the covariance
matrix for measuring noise.

Since Kalman filter can only deal with linear functions, the fusion
systems should be linearly designed. In [157], a model combined
with strong tracking KF and wavelet neural network for INS error
compensation was proposed. Strong Tracking Kalman Filter (STKF) was

InformationFusion95(2023)62–9069Y. Zhuang et al.

Fig. 3. A general classification of main filters used for state estimation in integrated navigation systems.

used to establish a highly accurate model of when GPS works well and
to predict INS errors during GPS outages. KF was applied to integrate
INS and UWB in [158–160]. The tightly-coupled model of INS/UWB
was established in [159,160]. The work [122] fused the localization
results of the Bluetooth propagation model and PDR through the KF to
improve the standalone Bluetooth model, step counting, and step length
calculation.

3.1.2. Extended Kalman filter

When the system is a linear Gaussian model, the KF can give the
optimal estimation, but the actual navigation system always has non-
linearity. For nonlinear systems, one suitable method is the EKF, which
converts a nonlinear system into an approximate linear system by
linearization. The core idea is to expand the nonlinear function into
the Taylor series around the filter state estimate and ignore the second-
order and above terms to obtain an approximate linearization model.
The state transfer matrix 𝐀 and the design matrix 𝐇 in the KF are
replaced by the Jacobian matrices of the non-linear functions 𝑓 and
ℎ, which represent the state and observation, respectively..

𝐀 =

𝜕𝐟
𝜕𝐗

=

𝐇 =

𝜕𝐡
𝜕𝐗

=

𝜕𝑓1
𝜕𝑥1
⋮
𝜕𝑓𝑛
𝜕𝑥1
𝜕ℎ1
𝜕𝑥1
⋮
𝜕ℎ𝑛
𝜕𝑥1

⎡
⎢
⎢
⎢
⎢
⎣

⎡
⎢
⎢
⎢
⎢
⎣

⋯

⋱

⋯

⋯

⋱

⋯

𝜕𝑓1
𝜕𝑥𝑛
⋮
𝜕𝑓𝑛
𝜕𝑥𝑛
𝜕ℎ1
𝜕𝑥𝑛
⋮
𝜕ℎ𝑛
𝜕𝑥𝑛

⎤
⎥
⎥
⎥
⎥
⎦

⎤
⎥
⎥
⎥
⎥
⎦

(6)

(7)

With the above matrices, the EKF filtering process is the same as the
linear Kalman filtering process.

Many articles use EKF as an efficient algorithm for GNSS/inertial
integrated navigation systems [161–164]. To solve the problem of a
random bias, the authors of [163] proposed an Adaptive Two-stage EKF
(ATEKF). An unknown bias can be estimated using the ratio between
the calculated innovation covariance and the innovation covariance
estimated from a window of innovations. Xu et al. proposed an adaptive
iterated EKF [165] which used the noise statistics estimator to model
the measurement noise, and then IEKF was used to deal with the
nonlinear problem in the INS/WSN integrated navigation system. A
novel approach [166] combined IMU and UWB range measurements
by EKF. In [167], the distance between a reference node and the target
node and its change rate measured from UWB tags were firstly input to
the channel filter for the estimation of the distance. Then, the estimated
distance is input to the EKF. In the linearization process, the EKF
algorithm may diverge when the neglected higher-order terms in Taylor

expansion are significant. The EKF and the PF were used for sensor
fusion in pose estimation to minimize uncertainty in robot localization
[168].

Algorithm 1 gives an example of GNSS/INS integration to demon-
strate how EKF is implemented. The selection of state and measurement
vectors will be discussed in Section 3.2. More details concerning INS
mechanization and the calculation of matrix 𝐀, 𝐇, 𝐐, and 𝐑 can be
found in [24,169].

Algorithm 1 A GNSS/INS instance [24] showing the implementation
of Extended Kalman Filter.
Parameter Statements:
}

{𝐱𝑘, 𝐏𝑘
𝐳𝑘: differential measurement at time step 𝑘, using GNSS-observed

: differential state and its covariance at time step 𝑘.

and INS-predicted quantities.
Initialization:

𝐱0: zero vector.
𝐏0: based on the accuracy of initial position, velocity, attitude

(PVA), and IMU errors.
Iteration Steps:
(1) INS mechanization:

compute present PVA based on those of last time and IMU

outputs.
(2) Prediction:

generate the next state and covariance:
𝐱−
𝑘 = 𝐀𝐱𝑘−1
𝑘 = 𝐀𝐏𝑘−1𝐀𝑇 + 𝐐
𝐏−
where 𝐀 is the linearization form of the system model,
𝐐 is calculated based on IMU error characteristics.

(3) Update, if GNSS measurements 𝐳𝑘 come:

𝑘 𝐇𝑇 + 𝐑)−1
)

𝑘 𝐇𝑇 (𝐇𝐏−
𝑘 + 𝐊𝑘
(𝐈 − 𝐊𝑘𝐇) 𝐏−

compute Kalman gain, update state and covariance:
𝐊𝑘 = 𝐏−
𝐱𝑘 = 𝐱−
𝐏𝑘 =
where 𝐇 is the linearization form of the measurement model,
𝐑 is calculated based on GNSS error characteristics.

(𝐳𝑘 − 𝐇𝐱−

𝑘

𝑘

(4) If it is necessary to output:

compute PVA based on INS mechanization results and the state

𝐱𝑘.

3.1.3. Unscented Kalman filter

The UKF belongs to the class of sigma point Kalman filters, which
sample a special set of sigma points of the state. Compared to the

InformationFusion95(2023)62–9070Y. Zhuang et al.

traditional EKF, UKF has better performance at the expense of comput-
ing time because it considers a large number of working points. The
most important process of UKF is the unscented transformation where
the sigma points are propagated through the nonlinear function and
then weighted and resampled into a Gaussian distribution. After the
unscented transformation, the sigma points create a vector in the N-
dimensional state space. Similar to KF, UKF has two phases, prediction
and update. In prediction, sigma points are propagated through the
system function for a given control input. For the update step, a new
set of sigma points needs to be calculated based on current prediction
through the unscented transformation. The detailed algorithm can be
referred to in [170,171].

Many papers adopted UKF in an integrated system [170–176]. A
variant of UKF, square-root UKF, was implemented in [177–179]. The
article [180] proposed a pulsar/CNS integrated navigation method
based on federated UKF. The federated filter was used for its stronger
fault tolerance and its ability to deal with different sampling periods.
For dynamic systems, an Interacting Multiple Module (IMM)-based UKF
was proposed [181]. Two IMM-UKFs were executed in parallel when
GNSS was available. One fused the information of low-cost GNSS, in-
vehicle sensors, and Reduced Inertial Sensor System (RISS), while the
other fused only in-vehicle Micro Electromechanical Systems (MEMS)
sensors. In [182], a new interacting multiple filter containing sim-
plified UKF-based subfilters with different heading initializations was
proposed. It had the same structure as the IMM filter.

Researchers also worked on the modification of UKF. For example,
in [183], a computationally efficient refinement of the UKF, called
marginalized UKF, was investigated to incorporate the linear substruc-
ture in the nonlinear function, i.e., the function was nonlinear only
in some of the state elements while the remaining part was linearly
mapped to the functional values. Also to reduce the computational
burden, in [184], UKF was modified based on the idea that the change
of probability distribution for the state variables between measurement
updates was small. Another work [185] constructed a nonlinear mea-
surement equation by including the second-order term in the Taylor
series of the pseudo-range measurements. To overcome the computa-
tional burden, the derivative UKF had the same form as the KF in
the prediction step. In the update step, the predicted measurement,
measurement covariance, and cross-correlation covariance were ap-
proximated by the statistics of chosen sigma points and the transformed
sigma points yielded through the nonlinear measurement equation,
thus enabling the filtering to retain the nonlinearity of pseudo-range
measurements.

3.1.4. Ensemble Kalman filter

The sample points of the previously mentioned sigma-point Kalman
filters (i.e., UKF, and Central Difference Kalman Filter (CDKF)) are cho-
sen deterministically. The number of sample points in the sigma-point
Kalman filters are of the same order as the dimension of the nonlinear
system. However, Ensemble Kalman Filter (EnKF) uses a stochastic
sampling algorithm based on the Monte Carlo method, which can better
reflect the states of the extremely high order and nonlinear systems.
EnKF samples a certain number of points randomly to realize the nu-
merical computation of the state covariance matrix. Such computation
not only reduces the computational complexity of calculating the state
covariance matrix in KF, but also achieves better performance. Similar
to other KF-derived methods, the EnKF also contains a prediction phase
and an update phase.

EnKF has also been widely used in integrated navigation systems.
In [186], the EnKF was used to estimate the position of the AUV,
and the performance of the EnKF with different ensemble members
was evaluated. A method of combing EnKF and PF was proposed in
[187]. The posterior probability density in EnKF that accounted for the
latest observation information was used as the proposal distribution for
particles.

Table 3
Comparison Among KF, EKF, UKF, EnKF, and PF.

Deal with non-linear functions
Deal with non-Gaussian noises
Computational complexity

KF

Poor
No
Low

EKF

Fair
No
Low

UKF

EnKF

Good
No
Medium

Good
No
Medium

PF

Good
Yes
High

3.1.5. Particle filter

𝑘

The PF is a recursive filter that uses the Monte Carlo method. A set
of weighted random samples (i.e., particles) is used to represent the
posterior probability of a random event. Different from the KF, which
is built on linear state space and Gaussian distributed noises, PF can
model any state. Given the particles of the previous state, predicted
particles can be obtained from the state transition equation plus the
control input. After the observation 𝐳𝑘 is obtained, the conditional
)
probability 𝑝 (𝐳𝑘 ∣ 𝐱𝑖
, for particles is computed, which represents the
probability of observing 𝐳𝑘 when the state 𝐱 (𝑡) takes the 𝑖th particle 𝐱𝑖.
After several recursions, the weights of many particles become small
enough to be negligible, leaving only a few particles with large weights.
This phenomenon wastes a lot of calculations on particles that have
a weak effect. Thus, the estimation performance is degraded. 𝑁 eff is
defined as the number of effective particles. If 𝑁 eff is less than a
certain threshold, re-sampling will slow down the degradation problem.
The concept of resampling is to remove particles with small weights
and focus on those with larger weights. A typical realization of PF
fusion GNSS/INS is given in Algorithm 2. The observation likelihood
𝑝 (𝐳𝑘 ∣ 𝐱𝑖
is specified by measurement model 𝐳𝑘 = ℎ(𝐱𝑘, 𝐯𝑘) [10], where
𝐯𝑘 is the measurement noise. The resampling algorithm can be found
in [188].

)

𝑘

PF is widely used in integrated navigation and has many variants.
Woodman and Harle developed a tracking system [189] that used
a foot-mounted inertial sensor, a building model, and a PF to track
the person and achieved 1 m accuracy. In [190], a Single-hidden
Layer Feed-forward Networks (SLFNs) was used to model multiple
fingerprinting probabilities and improve the PF performance. A new
initialization algorithm using Random Sample Consensus (RANSAC)
was presented to reduce the convergence time. In the paper [191],
a hybrid extended particle filter was developed as an alternative to
the EKF to achieve better navigation accuracy for low-cost MEMS
sensors. An adaptive joint observation model was developed to fuse
different observations according to the accuracy and reliability of the
corresponding sensors. Moreover, an enhanced version of the PF was
employed in the paper [10]. It sampled particles from both the prior
importance density and the observation likelihood, leading to improved
performance.

3.1.6. Summary of filtering methods

A general classification of the above filtering methods can be given
in Fig. 3. KF is only capable of dealing with linear functions, so it
has limited applications. EKF uses Taylor expansion to linearize the
nonlinear functions. Due to the errors introduced by the linearization,
the EKF is a sub-optimal and biased estimator, and calculating the
Jacobian matrix is always a very difficult and error-prone process. UKF,
EnKF, and PF share a similar principle: they use multiple sigma points
or particles to fit the nonlinear function without the need of calculating
the Jacobian matrix. But their computational cost is much larger. In
real applications, the selection of these methods should consider both
performance and complexity, which has been summarized in Table 3.

InformationFusion95(2023)62–9071Y. Zhuang et al.

Algorithm 2 A GNSS/INS instance [10] showing the implementation
of Particle Filter.

Parameter Statements:
}

𝑘, 𝜔𝑖

{𝐱𝑖
𝐳𝑘: GNSS measurement at time step 𝑘.

: 𝑖𝑡ℎ particle and its weight at time step 𝑘.

𝑘

Initialization:

𝐱𝑖
0: generated based on initial state’s probability distribution
𝑝(𝐱0).
0: 1
𝜔𝑖
𝑁
Iteration Steps:
(1) for each particle 𝐱𝑖

, where 𝑁 is the number of particles.

generate the new particle 𝐱𝑖

𝑘 using the system model 𝐱𝑖

𝑘 =

𝑘−1:

, 𝐰𝑖

𝑓 (𝐱𝑖
(2) for each new particle 𝐱𝑖
𝑘:

𝑘−1), where 𝐰𝑖

𝑘−1

𝑘−1 is the process noise.

compute the new weight using the observation likelihood,
𝑘 = 𝜔𝑖
𝜔𝑖

𝑝 (𝐳𝑘 ∣ 𝐱𝑖

)
.

𝑘

𝑘−1

(3) Normalize the new weight

𝜔𝑖

𝑘 =

𝜔𝑖
𝑘

.

𝑁
∑

𝑗=1

𝜔𝑗
𝑘

(4) Resample, if
1
𝑁 eff =
(𝜔𝑖
𝑘

𝑁
∑

𝑖=1

< 𝑁 T, where 𝑁 T is a threshold.

)2

(5) If it is necessary to output:

calculate the weighted mean of particles 𝐱𝑘 =

𝑁
∑

𝑖=1

𝑘𝐱𝑖
𝜔𝑖
𝑘.

3.1.7. Graph optimization

Apart from filtering-based algorithms, some works adopt nonlinear
optimization methods for integrated positioning systems. A graph with
state variables as vertices and observation factors as edges is used to
describe the inner relationships within the navigation systems through
graph-based optimization. Optimization methods were originally used
in vision-inertial simultaneous localization and mapping (SLAM) prob-
lems [85,86,91,92]. In recent years, they have also been widely used
among other positioning/navigation frames, including LiDAR-inertial
[104], GNSS/INS [192,193], GNSS/INS/vision [194–196], VLP/INS
[197], WiFi/PDR [49], UWB/INS [198], and BLE/PDR [123,124]. Com-
pared with filtering-based algorithms, optimization methods make full
use of historical information, thereby achieving better positioning ac-
curacy, although through additional calculations.

Optimization methods are very suitable for sensor fusion, of which
the key lies in designing an effective cost function to process multi-
sensor data. Generally, a cost function is the sum of the Mahalanobis
norm of residuals, which are calculated based on states and measure-
ments. In an integrated navigation/positioning system, each sensor’s
data can construct at least one type of residuals. For instance, IMU mea-
surements can construct IMU residuals [91,193], PDR residuals [123],
or pre-integration residuals [92,195]; image data can construct visual
residuals [92,95]. Since batch graph optimization is time-consuming,
strategies, such as sliding-window [192,194,197], are needed to reduce
the computational cost to realize real-time estimation. In particular,
many researches [86,91,92,195] marginalized old measurements out-
side the sliding window as prior information, which can construct
marginalization residuals [92,195]. Also, with effective incremental
optimization, GTSAM can conduct real-time localization without a
sliding window [193], but the memory consumption is incremental
over time. Most researchers choose popular libraries for optimization
tasks, including Ceres solver [49,194,197], g2o [123], and GTSAM
[192,193].

To estimate the optimal states based on a cost function, effective
optimization algorithms are needed. Optimization algorithms can be
divided into two major categories, (i) trust region approaches, and

(ii) line search approaches [199]. The Levenberg–Marquardt algorithm
[200], a trust region approach, is the most widely used for solving
graph optimization problems [49,123,197].

We take VLP/INS integration as an example to demonstrate the
implementation. The IMU preintegration, IMU measurement residual,
and LED projection residual can be referred to [197].

Algorithm 3 A VLP/INS instance [197] showing the implementation of
graph optimization.

Parameter Statements:
]
[𝐱0, 𝐱1, … , 𝐱𝑛−1

 =

: the full state vector in a sliding window

with a width 𝑛.

: IMU preintegration between the frames at the time step 𝑘

̂𝐳𝑏𝑘
𝑏𝑘+1
and 𝑘 + 1.
̂𝐮𝑐𝑘
𝑙 : LED 𝑙’s projection point in the image plane at the time step

𝑘.

𝐏𝑊
𝑙

: LED 𝑙’s prior coordinate in a local reference frame W.

Initialization:

𝐱0: initial position, velocity, attitude (PVA), and IMU errors.

Iteration Steps:
(1) IMU preintegration:

integrate the IMU measurements within the time interval

[𝑡𝑘−1, 𝑡𝑘] to represent the state transition ̂𝐳𝑏𝑘
𝑏𝑘+1
(2) Construct the cost function within a sliding window whose width
is 𝑛:

.

⎧
⎪
⎨
⎪
⎩

min


(

𝑛−1
∑

𝑘=0

𝐫

‖
‖
‖
‖

̂𝐳𝑏𝑘
𝑏𝑘+1

, 

2
)‖
‖
‖
𝛴
‖

𝑏𝑘
𝑏𝑘+1

+

𝑛−1
∑

𝑚−1
∑

𝑘=0

𝑙=0

𝐫

‖
‖
‖

(̂𝐮𝑐𝑘
𝑙

, 𝐏𝑊
𝑙

2
, )‖
‖
𝛴
‖

𝑐𝑘
𝑙

where 𝐫 (⋅) is IMU measurement residual with the covariance

⎫
⎪
⎬
⎪
⎭

matrix 𝛴𝑏𝑘
𝑏𝑘+1

,

𝐫 (⋅) is LED projection residual with the covariance matrix 𝛴𝑐𝑘
𝑙

.

(3) Optimize using the Levenberg–Marquardt method [200] to obtain
the optimal state vector .
(4) If it is necessary to output:

compute PVA based on the state vector .

3.2. Classification based on integration architecture

Recently, the literature has proposed various types of integration
architectures. The level of integration partly depends on whether the
architecture is a new system or a retrofit to another system [1]. The
three main integration architectures are, (i) loosely-coupled systems,
(ii) tightly-coupled systems, and (iii) ultra-tightly-coupled systems. The
most popular are GNSS/INS, because they are complementary to each
other and they overcome their individual limitations [201].

In integrated systems, filters, such as EKF and PF, are usually used to
fuse data from different sensors. In these filters, INS measurements are
often used for state prediction; other sensors’ observations usually serve
as updates to optimize the states. The three types of integration ar-
chitectures often share similar dynamic equations, but the observation
equations are different. A comparison of them are shown in Table 4.

3.2.1. Loosely-coupled integration

The most popular and earliest implemented integration scheme is
the loosely-coupled approach, also known as decentralized or cascaded
filtering. A Loosely-Coupled Integration (LCI) system uses one system’s
navigation outputs each time, which often are Position, Velocity, and
Time (PVT) rather than raw observations, to update the system states.
We first introduce a general formulation that suits all estimation
methods and positioning sources. Similar as the formerly mentioned
filtering and optimization-based methods, 𝐱𝑘 represents the system

InformationFusion95(2023)62–9072Y. Zhuang et al.

Table 4
Comparison among three integration architectures.

Architectures

Features

Advantages

Drawbacks

Loosely-coupled
Integration

Tightly-coupled
Integration

Integrate in the area of PVT,
also called decentralized or
cascaded filtering.

Integrate in the area of
observations, also called
centralized filtering.

Ultra-tightly-coupled
Integration

Integrate in the physical layer,
also centralized.

LCI is a simple and flexible approach.

It has smaller filter size than the centralized
approach.

All the single positioning systems need to
independently give solutions.

LCI is less accurate than other schemes.

TCI only needs one system to give independent
solutions.

Only one filter is implemented, thus TCI is more
complex than LCI.

It can detect and reject poor observations.

UTCI has the best performance on signal tracking
and anti-jamming capability.

As UTCI can largely improve the receivers’
performance, it is theoretically more accurate.

Systematic errors (e.g., cycle slips in GNSS) should
be eliminated before filtering.

It is not flexible and needs to design when sensors
are manufactured. Once made, the architecture can
hardly be changed.

The structure is more complex than LCI and TCI.

state at time 𝑘. We assume there were one dead-reckoning-based posi-
tioning source and 𝑁 other types of positioning sources. Their residuals
calculated by observations and the estimated state are marked as
𝐫 (⋅) and 𝐫 (⋅), respectively. We use the dead reckoning source as
the principle to predict the system state ̂𝐱𝑘∣𝑘−1 at time 𝑘 using the
sensor’s measurements and the last state 𝐱𝑘−1. The covariance of the
dead reckoning positioning residual 𝛴𝑅𝑘
are
calculated based on the uncertainty of observations and current state.
The positioning problem is to minimize the function,

and the 𝑖th source 𝛴𝑂𝑖

𝑘

{

‖
‖
‖

min
𝐱𝑘

𝐫

( ̂𝐱𝑘∣𝑘−1, 𝐱𝑘

)‖
‖
‖

2

𝛴𝑅𝑘

+

𝑁
∑

𝑖=1

𝐫

‖
‖
‖

(𝐳𝑖

𝑘, 𝐱𝑘

2
)‖
‖
𝛴
‖

𝑂𝑖
𝑘

}

(8)

In the loosely-coupled integration architecture, 𝐳𝑖
𝑘 is one or several
components of the state vector and is calculated by the estimator of the
positioning source 𝑖 at time 𝑘. To solve this problem, each algorithm has
its own optimization criteria: KF, EKF, and graph optimization need to
calculate the Jacobian matrix to deal with nonlinear functions, while
UKF, EnKF, and PF use particles to fit them.

Specifically, we take the GNSS/INS integration using EKF as an
example (Fig. 4), in which the positions and velocities derived from
the GNSS estimator, together with their covariance matrices, are em-
ployed as updates for the navigation EKF [169]. The construction of
transition matrix Φ can be found in [169]. The state vector of EKF
typically contains positions, velocities, attitudes, accelerometer errors,
and gyroscope errors, which can be written as:

𝛿𝐱 = [𝛿𝐫, 𝛿𝐯, 𝛿𝐀, 𝛿𝝎, 𝛿𝐟]𝑇

(9)

The observation equation of a discrete-time EKF is represented as,

𝐳𝑘 = 𝐇𝑘𝐱𝑘 + 𝐯𝑘

(10)

For the case using only GNSS-derived positions, they are expressed
in Earth-Centered, Earth-Fixed (ECEF) coordinates; therefore, 𝐳𝑘 and 𝐇𝑘
are expressed as,

𝐳𝑘 =

[𝐿GNSS − 𝐿INS, 𝜆GNSS − 𝜆INS, ℎGNSS − ℎINS

]𝑇

𝐇𝑘 =

[

𝐈

𝟎

𝟎

𝟎

]
𝟎

(11)

(12)

For the case considering both GNSS-derived positions and velocities,

the observation vector and design matrix are given as,

𝐳𝑘 =

[𝐿GNSS − 𝐿INS, 𝜆GNSS − 𝜆INS, ℎGNSS − ℎINS,

𝑣E,GNSS − 𝑣E,INS, 𝑣N,GNSS − 𝑣N,INS, 𝑣U,GNSS − 𝑣U,INS

]𝑇

𝐇𝑘 =

[

𝐈

𝐈

𝟎

𝟎

]
𝟎

(13)

(14)

An example on GNSS/INS integration is given in Algorithm 1.

Fig. 4. Loosely-Coupled GNSS/INS integration [169].

between GPS and RISS. Furthermore, Dusha and Mejias [127] inte-
grated a monocular visual odometry with GPS to improve navigation
performance.

Additionally, the article [132] proposed a navigation system that
integrates INS, VNS, CNS for deep space exploration. The article [180]
designed a Pulsar/CNS integrated navigation method for planetary
rovers using UKF. Furthermore, Li et al. [202] integrated miniature
coherent altimeter and velocimeter and IMU for Mars landing and Mars
based missions in 2010. Besides, Li and Peng [203] proposed the Radio
Beacons/IMU integration for Mars entry navigation.

In scenarios without GNSS, loosely-coupled integrated navigation
systems are usually implemented through the integration of inertial
sensors and other aids, such as UWB [150], magnetometer [204], and
WiFi [75,138,205–210]. For instance, WiFi provides several types of
observations, including fingerprints [205,209], ToF [208], and propa-
gation model [206,207]. Also, some works employed the integration
of velocity-based measurements and inertial sensors. Geng et al. [136]
used such integration for AUV navigation. Zhou et al. used the same
technique for road driving [211]. While Huh et al. [212] used the
Simultaneous Localization and Mapping (SLAM) algorithm to integrate
a camera with a gimbaled laser sensor for UAV navigation.

3.2.2. Tightly-coupled integration

Tightly-Coupled Integration (TCI) is also known as the centralized
approach [169]. Different from LCI, TCI uses raw observations (in-
cluding TOA, RSS, AOA, etc.) to update the system states; thus, its
number of estimators is fewer [169]. Similar to LCI, TCI also uses
the formulation (8) to present the problem. The difference is that 𝐳𝑖
𝑘
is no longer one or several components of the state vector but raw
observations of the positioning source 𝑖. Thus, the function 𝐫 (⋅) is
more complicated and needs to be established based on the positioning
system’s principle.

Apart from EKF, other filtering algorithms, such as PF, can also
be used [191]. Similarly, Georgy et al. [77] utilized both position
and velocity observations for KF and PF in their proposed integration

Specifically, we take the GNSS/INS integration using EKF as an ex-
ample (Fig. 5), where only one centralized filter is used to integrate the
GNSS-derived pseudo ranges, carrier phases, and Doppler frequencies

InformationFusion95(2023)62–9073Y. Zhuang et al.

Fig. 5. Tightly-Coupled GNSS/INS integration [169].

Fig. 6. Block diagram of the STL and VTL of GNSS receiver [224].

with INS-derived Position, Velocity, and Attitude (PVA) [213]. With
such a design, GNSS contributes to the integration solution, even when
fewer than four satellites are observable.

When designing the tightly-coupled GNSS/INS integrated system,
the clock bias and drift errors that affect the GNSS receiver should also
be included. The state vector is presented as [214],

𝛿𝐱 = [𝛿𝐫, 𝛿𝐯, 𝛿𝐀, 𝛿𝝎, 𝛿𝐟, 𝛿𝐛]𝑇

(15)

where 𝛿𝐛 usually includes receiver’s clock bias 𝛿𝑡 and clock drift error
𝛿𝑡′, however, some studies only considered the clock drift error 𝛿𝑡′
[215], while some also included the gyro and accelerometer scale
factors [169]. For a system without carrier phase measurements, the
observation vector 𝐳𝑘 is defined as,

𝐳𝐤 = 𝝇sat,𝑘 − ̂𝝇𝑘

(16)

]𝑇

]𝑇

𝝆′
𝑘

𝝆′
𝑘

[𝝆𝑘
where 𝝇sat,𝑘 =
represents the vector of corrected pseudo
ranges 𝝆𝑘 and pseudo-range rates 𝝆′
̂𝝇𝑘 =
[𝝆𝑘
represents the vector of predicted pseudo ranges and pseudo
range rates, which is computed from the current estimate of the target
trajectory [214]. Please note Eqs. (15) and (16) only hold in non-
differenced GNSS algorithms, which do not difference measurements
as the Real-Time Kinematic (RTK) does.

𝑘 at the time instant 𝑡𝑘;

The observation matrix is time-varying and depends on the number
of visible satellites 𝑁 [214]. The observation matrix 𝐇𝑘 is expressed
by,

In scenarios without GNSS signals, wireless systems can provide
range information for the TCI with inertial sensors, where differences
between wireless-based ranges and inertial-based ranges serve as obser-
vations. Zhuang and El-Sheimy [23] integrated WiFi, INS, and PDR for
pedestrian navigation using an EKF. The observation vector was derived
from the difference between WiFi-based and MEMS-based ranging,
while RSS bias was also put in the state vector. A similar technique was
used for the integration of inertial sensors with RFID [63] and BLE [14].
A UWB system can be tightly integrated with an INS to estimate the
indoor position and orientation [218] for indoor pedestrian navigation
[167]. Gao et al. [118] integrated SAR tightly with the GPS/INS system
to correct INS errors and provide speed-changing information. Also,
Gao et al. [98] compared LCI and TCI performance when integrating
LiDAR and GNSS with INS.

Alongside range-based technologies, visual-inertial integration sys-
tems have been developed recently. Qin et al. [92] designed a monoc-
ular Visual-Inertial Navigation System (VINS) for state estimation in
various environments, while Visual landmarks and IMU observations
were used for optimization. Cui et al. [219] used a tightly-coupled
integrated system for Mars exploration, i.e., X-ray pulsars/Doppler
system with TOA and velocity measurements. OpenVINS [94] used an
EKF-based sliding window visual-inertial estimator for state estimation
and camera calibration simultaneously. In recent years, ORB-SLAM3
[95], which fully relied on maximum a posteriori (MAP) estimation,
was proposed to fuse monocular, stereo, and RGB-D cameras with
inertial sensors.

(17)

3.2.3. Ultra-tightly-coupled integration

𝐇𝑘 =

[𝐇𝑁×3
𝟎𝑁×3
𝟎𝑁×3 𝐇𝑁×3

]

𝟎𝑁×6
𝐏𝑁×2
𝟎𝑁×6 𝐐𝑁×2

where 𝐇𝑁×3 is the Jacobian matrix of the nonlinear relationship be-
tween the user’s position and pseudo ranges 𝜌1, … , 𝜌𝑛. 𝐇𝑁×3, 𝐏𝑁×2,
𝐐𝑁×2 are given in [214] as follows

𝐇𝑁×3 =

̆𝑥 − 𝑥1
𝑑1
̆𝑥 − 𝑥2
𝑑2
⋮

⎡
⎢
⎢
⎢
⎢
⎣

̆𝑦 − 𝑦1
𝑑1
̆𝑦 − 𝑦2
𝑑2
⋮

̆𝑧 − 𝑧1
𝑑1
̆𝑧 − 𝑧2
𝑑2
⋮

⎤
⎥
⎥
⎥
⎥
⎦

𝐏𝑁×2 =

1
⎡
1
⎢
⎢
⋮
⎣

0
0
⋮

⎤
⎥
⎥
⎦

, 𝐐𝑁×2 =

0
⎡
0
⎢
⎢
⋮
⎣

1
⎤
1
⎥
⎥
⋮
⎦

(18)

]

[𝑥 − 𝑥𝑗

where 𝑑𝑗
[ ̆𝑥
̆𝑧]
̆𝑦
integration is given in Algorithm 1.

is the norm of the vector
and
is the estimated receiver position. An example on GNSS/INS

𝑧 − 𝑧𝑗

𝑦 − 𝑦𝑗

Regarding GNSS carrier phase measurements, it is necessary to
establish the relationship between time differenced carrier phase 𝝋𝑘 −
𝝋𝑘−1 and the state vector. The TCI is actually more computationally
efficient than the LCI when the ambiguities are fixed [216]. With the
development of rapid ambiguity resolution, Li et al. [217] proposed
a single-frequency multi-GNSS RTK/MEMS-IMU integration model for
positioning in urban environment.

Ultra-Tightly-Coupled Integration (UTCI), also called deep integra-
tion, has been used for applications via GNSS/INS systems, combining
GNSS signal tracking and GNSS/INS integration into a single KF. UTCI
integrates in the physical layer, rather than the data layer as LCI and
TCI do, thus, it is more tightly designed. This method can achieve the
best performance for signal tracking and anti-jamming [220,221].

As shown in Fig. 6, the GNSS receiver often has two different archi-
tectures: Scalar Tracking Loop (STL) and Vector Tracking Loop (VTL).
STL receives Intermediate Frequency (IF) signals, generates errors of
pseudo-range, pseudo-range rate, frequency, and carrier phase, and
then estimates the Position, Velocity, and Time (PVT) of the receiver.
Feedbacks driving the carrier and code Numerically-Controlled Oscilla-
tors (NCOs) are obtained from the discriminators directly, while VTL
combines two receiver tasks – signal tracking and PVT estimation –
into a single algorithm [222]. In vector tracking, receiver feedback is
obtained from the navigator to the tracking channels [223], enabling
VTL for GNSS/INS deep integration.

Based on the tracking loop algorithm, VTL falls into two groups:
coherent [224–226] and non-coherent [149] systems. In a non-coherent
system, the discriminator outputs directly determine the code phase
and carrier frequency errors. As the carrier phase is not locked [149],
the non-coherent system improves performance in weak signal condi-
tions and dynamic environments. Conversely, in a coherent tracking

InformationFusion95(2023)62–9074Y. Zhuang et al.

receiver, the Doppler estimate of the carrier loop is fed into the code
loop to aid in code tracking as an additional range-rate [227]. A Delay
Lock Loop (DLL) employs code tracking and Phase or Frequency Lock
Loops (PLL/FLL) to perform carrier phase/frequency tracking [225].
There are also combined Frequency-assisted Phase Locked Loop (FPLL)
[223]. Also, a coherent Vector Delay/Frequency Lock Loop (VDFLL)
[222,225,228] architecture uses the central filter to track the Pseudo-
Random Noise (PRN) code phases and the carrier frequencies, which
can be used for dynamic weak signal tracking.

In a typical ultra-tightly-coupled system, the observation updates
are directly based on In-Phase (I) and Quadrature-Phase (Q) values
generated by correlators. The observation equation is based on the
correlation values 𝑅𝑖 [221] and expressed as follows.

𝐳 =

𝑅1
⎡
⎢
𝑅2
⎢
⋮
⎢
⎢
𝑅𝑁
⎣

⎤
⎥
⎥
⎥
⎥
⎦

= 𝐇

𝛿𝑥
⎤
𝛿𝑦
⎥
⎥
𝛿𝑧
⎦

⎡
⎢
⎢
⎣

+ 𝐧

𝐇 =

(0)

√

2𝑃1𝐷1𝑅′′
1
0
⋮
0

−

⎡
⎢
⎢
⎢
⎣

√

−

0
2𝑃2𝐷2𝑅′′
2
⋮
0

0

0

(0) 0
⋮
0 −

√

0
⋮
2𝑃𝑁 𝐷𝑁 𝑅′′

𝑁 (0)

𝜕𝜏1
𝜕𝑥
𝜕𝜏2
𝜕𝑥
⋮
𝜕𝜏𝑁
𝜕𝑥

⎡
⎢
⎢
⎢
⎢
⎢
⎣

⎤
⎥
⎥
⎥
⎦

𝜕𝜏1
𝜕𝑦
𝜕𝜏2
𝜕𝑦
⋮
𝜕𝜏𝑁
𝜕𝑦

𝜕𝜏1
𝜕𝑧
𝜕𝜏2
𝜕𝑧
⋮
𝜕𝜏𝑁
𝜕𝑧

⎤
⎥
⎥
⎥
⎥
⎥
⎦

(19)

(20)

where, 𝑃𝑁 is the signal power, 𝐷𝑁 is navigation data, 𝜏𝑁 is the
propagation delay and 𝑅′′
𝑁 (0) can be calculated by pseudo-random
coarse/acquisition code.

Recent research used a Chip Scale Atomic Clock (CSAC) to substi-
tute for Temperature Compensated Crystal Oscillator (TXCO) in the
VTL-based deep integration to obtain a precise timing reference, in
which only three satellites were needed for navigation [229]. A Vector
Tracking Loop Based Deep Integration (VTL-DI) system used vector-
form pseudo-range errors and pseudo-range rate errors as observations
[229].

Many advanced systems, based on deeply integrated GNSS/INS
systems, have been developed. Langer et al. [149] proposed a deep
integration for GPS and pedestrian navigation system, which used the
step-length update to aid the deeply-coupled GPS/INS system. Fernán-
dez [97] used the LiDAR system to help GNSS/INS deep integration.
Apart from the GNSS-based deep integration, there was an application
of SINS (Strap-down Inertial Navigation System)/CNS [230,231]. He
et al. [230] integrated SINS and CNS to determine the rover’s position
and attitude.

4. Learning-based multi-sensor data fusion for integrated posi-
tioning/navigation

This section introduces a general categorization of the learning-
based methods (Fig. 7) used in integrated navigation systems. They
are generally summarized into two categories, (1) aiding analytical
methods to estimate parameters and (2) positioning end-to-end. It is
important to note that most novel contributions are based on the
combination of several learning based algorithms.

4.1. Supervised learning

Machine learning algorithms are traditionally classified into su-
pervised learning and unsupervised learning, according to whether
they require manual data labeling. Supervised learning is a task-driven
mechanism focusing on data classification or regression that requires
manually labeled data for model training. The most popular super-
vised learning algorithms used for classification in integrated position-
ing/navigation systems are SVM and Random Forest. We will discuss
several supervised learning algorithms used in integrated position-
ing/navigation as follows.

Fig. 7. A general classification of learning-based algorithms is available for most
applications. Only the algorithms discussed in this article are included in the
classification.

4.1.1. Artificial neural network

The inertial-aided integrated navigation is often affected by uncer-
tain noises [232]. Although UKF and PF have shown their great per-
formance in nonlinear systems, they have the limitations that need the
prior probability of the process and measurement noise. Learning-based
methods have attracted researchers’ interests due to their capability
to model and predict in nonlinear systems; hence, many studies have
applied neural networks in integrated positioning systems.

In the GNSS/INS integrated systems, ANN can be used to predict
positions or INS errors during GNSS outages. In the study [181], two
IMM-UKFs were executed in parallel when GNSS was available. One
fused the data of low-cost GNSS, in-vehicle sensors, and Reduced Iner-
tial Sensor System (RISS), while the other fused only in-vehicle sensors
and MEMS RISS. The differences between the state vectors of the two
IMM-UKFs were considered as training data of a Grey Neural Networks
(GNN) module to predict and compensate position errors when GNSS
signals were blocked. The study [233] mimicked the vehicle dynamics
and predicted its position during GPS outages. The method utilized
wavelet analysis to analyze and compare the INS and GPS outputs at
different resolution levels and then processed the signals by an ANN
module based on radial basis function. In [157], a strong tracking KF
(STKF) was combined with a wavelet neural network for INS error
compensation. The STKF was used to establish a highly accurate model
when GPS worked well and to predict INS errors during GPS outages.
In [234], Li et al. proposed a single hidden layer feedforward ANN to
predict and correct the INS position error during GPS outages. They
used the de-noised INS data and the outputs of interactive multi-model
EKF to train the learning model.

In addition, ANN is capable of end-to-end integrated navigation.
Magrin and Todt [235] fused data from a sonar octagon, a digital
compass, and wireless network signal strength measurements to de-
termine the position of an autonomous mobile robot. Almassri et al.
[236] designed a neural network to combine UWB and INS data with
a motion capture system to guarantee the positioning accuracy of a
moving robot.

ANNs have the following advantages. (1) It fuses sensor data for
positioning without using the system model, (2) it can predict in com-
plex nonlinear systems without prior knowledge such as characteristics
[157], and (3) it is able to deal with massive data efficiently. The
challenges of ANNs include: (1) they are black boxes, which cannot
explain how each variable affects the navigation system, (2) it usu-
ally requires a large number of training data, leading to over-fitting
and poor generalization [237], and (3) it is difficult to provide the
uncertainty of positioning results.

InformationFusion95(2023)62–9075Y. Zhuang et al.

4.1.2. Fuzzy logic

Standard KF assumes that the process and measurement noises
are zero-mean white Gaussian with known covariances. However, in
practical systems, it is difficult to model them accurately, which may
cause the filter to underperform and diverge. Applying fuzzy logic to
implement an adaptive filter is a way to solve these problems, where
the system is called Fuzzy Logic Adaptive System (FLAS). In a FLAS,
the residual between actual measurements and measurement predic-
tions by the internal model is monitored. Fuzzy logic allows flexibility
by using heuristics and avoids the need for accurate knowledge of
the process and measurement noise [238]. A typical FLAS consists
of three modules: fuzzification, fuzzy reasoning, and defuzzification.
The fuzzification module converts a crisp input value into a fuzzy
value. Afterward, the fuzzy-reasoning module is responsible for the
calculation by using the knowledge base. Finally, the defuzzification
module converts the fuzzy actions into a crisp action [239].

Fuzzy logic adaptive KF has been widely used for integrated naviga-
tion systems [238–240], where a FLAS was used to adjust measurement
noise and process noise covariances of the filter to prevent it from
divergence. Authors of [35] calculated the position differences by using
the fuzzy neural network. In [170], ultra-tight integration of GNSS
and INS was achieved by the fuzzy adaptive strong tracking of UKF.
The FLAS was able to tune the softening factor online according to
fuzzy rules, leading to performance enhancement in terms of both
tracking capability and estimation precision. In [241], the authors
proposed a novel fuzzy neural network (FNN) function approximator
to model unknown nonlinear systems with real-time implementation
for an adaptive fuzzy neuro-observer (AFNO) in low-cost INS/GPS
integrated positioning systems.

There are also GNSS-free applications, e.g., for underwater vehi-
cles [242] and UWB/INS fusion systems [243]. Shaukat et al. [242]
designed the fuzzy calibration logic to revise the measurement noise
covariance matrix for a better fusion of IMU, DVL, compass, and
pressure sensor. Gao and Li [243] designed a fuzzy adaption factor
to evaluate UWB measurement errors to effectively mitigate NLOS and
multipath interferences.

The advantages of fuzzy logic include, (1) it can model process
and measurements noise without the need of their probability char-
acteristics [240], (2) the system is simple and justifiable, (3) it takes
in expert knowledge and is good at handling nonlinearity and non-
Gaussian outliers [242]. The challenges include, (1) its rationale is not
constantly accurate, the results are perceived based on assumptions, so
it may not be widely accepted, (2) approval and verification of a fuzzy
information-based framework need broad equipment-based tests.

4.1.3. Support vector machine

The widely used neural network-based methods demand the quality
and quantity of training data, which can be restrictive and limits real-
world applications. By contrast, the principle of the SVM is structural
risk minimization, rather than empirical error minimization, which is
typical for neural networks. SVM also avoids local minima and overfit-
ting in neural networks [237]; hence, it achieves higher performance in
certain situations. Authors of [237] explored the Least Squares Support
Vector Machine (LS-SVM) to aid GPS/INS integrated systems, especially
during GPS outages. The hybrid method consisted of two working
modes: the LS-SVM/KF hybrid and the LS-SVM-based prediction during
GPS outages. In [172], SVM was trained with the INS data during
GPS outage when simulated annealing was applied to optimize the
parameters of the kernel and penalty functions. In [137], SVM was
used for the navigation of an Autonomous Underwater Vehicle (AUV),
which consists of a SINS and DVL. The SVM models the SINS error
and makes AUV navigation possible during the long-term DVL outage.
Using differently, Song et al. [244] designed two least square SVMs
to estimate the distances using RFID inputs and recognize the motion
pattern of a vehicle, respectively.

Fig. 8. A typical random forests architecture.

The advantages of SVM include, (1) it has high generalization ability
and strong adaptability for different navigation environments [244],
(2) it can effectively deal with high-dimensional data, such as wireless
fingerprint data, (3) it avoids local minima and overfitting [137,237],
and (4) it works well with a small number of training data [137].
The challenges are, (1) time consumption increases obviously on kernel
function with a large dataset, (2) its positioning performance decreases
significantly if the data has more noise.

4.1.4. Random forest

Random forest is based on decision trees and implemented with
three steps, (i) sub-sampling, (ii) decision tree training, and (iii) pre-
diction. In the first step, a fixed number of sub-samples are randomly
selected, each of which contains a fixed number of randomly selected
features. In the second step, those selected sub-samples are used to
train the decision trees. In the last step, all decision trees vote for
estimated results. Fig. 8 shows a schematic diagram of the random
forest algorithm.

Random forest and its variant, Random Forest Regression (RFR), can
both be used for integrated navigation/positioning. Random forest is a
classification method, which is be used for human activity recognition
[245,246] to fuse PDR with radio-based positioning systems. Besides,
the research [247] used the random forest to classify the GNSS posi-
tioning accuracy based on GNSS features. RFR is a regression method,
which can effectively model the highly nonlinear INS errors due to its
generalization capability. In GPS outages, the developed model offers
an INS error estimate, thereby improving the continuity and accuracy.
Authors of [248] predicted position changes of the target by providing
motion information, such as speed and heading angle, into the random
forest. The study [249] used a Principal Component Regression (PCR)-
RFR hybrid approach to the data containing both linear and nonlinear
components, thereby increasing the prediction accuracy.

The advantages of random forest are, (1) it is not sensitive to
abnormal data in training, (2) it handles the high dimensional sensor
data effectively [248], and (3) it avoids data overfitting [246,248]. The
challenges are, (1) in a complex task, many decision trees are needed
[245], thus, calculation efficiency is low, and (2) the interpretability of
the forest becomes weak when the scale of the forest reaches a certain
extent [245].

4.2. Unsupervised learning

Unsupervised learning is a data-driven method and does not rely
on manual labeling of data, which uses unknown patterns in features
to find the relationships among data samples. In this article, we present

InformationFusion95(2023)62–9076Y. Zhuang et al.

k-means [250], Expectation–Maximization (EM) algorithm [251,252],
and Principal Component Analysis (PCA) [247]. Since unsupervised
learning algorithms are seldom used in integrated navigation systems,
we only give them a brief introduction.

K-means is a clustering algorithm to partition observations into 𝑘
clusters. In the integrated navigation, k-means aids KF to estimate the
parameters, such as significant GNSS accuracy-related features [250].
Laskar et al. [253] revised the EKF states by avoiding the clustered
obstacles and finding suitable positions.

The EM algorithm is an iterative method of estimating latent vari-
ables in statistical models. Huang et al. [252] proposed the EM-EKF
algorithm, which combined the EM algorithm with the EKF algorithm,
to estimate the positioning information and unknown noise character-
istics. The EM algorithm can also be used to combine with UKF [251]
and Federated Kalman Filter (FKF) [254] to replace the prediction and
update process of KF. Chen et al. [255] proposed an adaptive Student’s
t-based Kalman filter to integrate GNSS and INS. In these researches,
noise is not assumed Gaussian distribution.

PCA is used to reduce the dimensionality of large data sets by
transforming a large set of variables into a smaller one that retains the
principal information to reduce machine-learning algorithms’ parame-
ters. Zhang and Hsu [247] used PCA to identify and discard transient in-
terference in a GNSS/INS integration system. Grejner-Brzezinska et al.
[256] used the PCA to reduce ANN training parameters to integrate
GPS, IMU, barometer, and other sensors.

Fig. 9. A typical deep reinforcement learning algorithm architecture.

fingerprinting, including Wi-Fi, Bluetooth, and geomagnetic data, to
obtain more stable and richer fingerprint characteristics. Belmonte-
Hernàndez et al. [266] proposed a deep neural network to fuse XBee,
Bluetooth, and WiFi fingerprints. Song et al. [267] proposed a hybrid
CNN-based indoor localization system (CNNLoc) with WiFi fingerprints
for multi-building and multi-floor localization.

4.3. Deep learning

4.4. Reinforcement learning

Deep learning belongs to a broad family of machine learning meth-
ods based on Artificial Neural Networks, consisting of three or more
layers of neural networks. The most representative models of deep
learning are the Convolutional Neural Network (CNN) and the Recur-
rent Neural Network (RNN). CNNs are powerful for dealing with image
and point cloud data, therefore they are mainly used in vision [257,
258] and laser [259] localization. RNNs allow feedback connections
into the same, or previous, layers in order to maintain the memory
of past inputs and model problems in time. Since data in integrated
navigation/positioning are always sequential, an RNN is an ideal tool.
Unlike other learning-based methods, deep learning is more used
for end-to-end integrated navigation problems. In this article, we only
explored two papers [257,260] that are used to aid analytical methods.
In [257], Siamese CapsNet was proposed for vision positioning, whose
results were then fused with UWB for capsule endoscopic localization.
In [260], a CNN network was used for walking pattern recognition; and
then a regular PDR is adopted, using IMU and magnetometer data.

End-to-end fusion of deep learning can be used in VIO [261–
263], PDR [264], vision/magnetic fusion [258], laser/INS fusion [259],
and multi-sensor fingerprinting [265–267]. Long Short Term Memory
(LSTM), an RNN capable of learning and storing long-term input trends,
deals well with time series data and is widely used in VIO [261–263].
VINet [262] used an LSTM to extract IMU data features, which were
integrated with image features by another LSTM network. To further
improve accuracy, Chen et al. [261] selectively combined image and
IMU features, using a two-layer bi-directional LSTM to extract inertial
features. By using LSTMs to deal with IMU inputs, Kim et al. [263]
designed an unsupervised loss to fuse vision and IMU data. Besides,
the work [89] presented a survey of visual odometry and mapping
approaches with deep learning. Similar with VIO, Li et al. [259] fused
laser and inertial data with a recurrent convolutional neural network
composed of a CNN-based point cloud feature extraction, an LSTM-
based IMU registration, and an LSTM-based data fusion. In the field
of PDR, L-IONet [264], a deep neural networks (DNN) framework, was
used to predict poses with the IMU and magnetometer data, which can
replace the traditional PDR framework. Deep learning is also capable
of fusing multi-sensor fingerprinting data to determine the locations
[265–267]. Gan et al. [265] used a deep belief network for multi-sensor

Reinforcement Learning (RL) is a basic machine learning paradigm,
which, together with both supervised and unsupervised learning, is
concerned with exploration of the space of possible control actions
to maximize the notion of cumulative reward. Accordingly, a set of
actions resulting in good performance were rewarded, while actions
resulting in poor performance were penalized [268]. Combined with
deep learning, Deep Reinforcement Learning (DRL), as the core of Al-
phaGo, has been widely studied in recent years. Deep learning provides
a learning mechanism, while reinforcement learning offers a learning
goal. Fig. 9 is a schematic diagram of the DRL algorithm structure. A
neural network decides actions for an Artificial Intelligence (AI) system,
while the environment informs whether to reward or punish in order
to adjust the parameters of the neural network.

RL has been successfully applied in path planning, collision avoid-
ance [274], and action games, and is now being applied to wireless
positioning [269–271] and vehicle tracking [272,273]. Study [269]
used RL to adjust the navigation parameters including IMU bias stan-
dard deviation. RL provided intelligent solutions by using a combina-
tion of dynamic programming and trial-and-error exploration to find
a set of optimal parameters. Similarly, Gao et al. [271] adaptively
estimated the process noise covariance matrix using a DRL approach,
where a deep deterministic policy gradient was introduced to obtain
an optimal state. With respect to vehicle tracking, Cao et al. [272] pro-
posed a reinforcement-learning-based Gaussian mixture model to fuse
millimeter-wave radars, LiDARs, and cameras in autonomous driving
applications. Rangesh and Trivedi [273] presented a modular frame-
work using the reinforcement learning paradigm for multi-object track-
ing, capable of a variable number of sensors including cameras and
LiDARs.

The main usages, advantages, and drawbacks of the learning-based
fusion methods surveyed in this paper are summarized in Table 5. The
advantages of RL include, (1) it has decision-making ability, which suits
well with vehicle tracking, (2) it has a strong automatic exploitation
ability, so the learned parameters can keep the validity for a certain
period of time [271]. The challenges of RL include, (1) it needs addi-
tional storage in navigation applications [271], (2) for DRL, the amount
of calculation and the complexity of the reward definition is large.

InformationFusion95(2023)62–9077Y. Zhuang et al.

Table 5
Learning-based multi-sensor data fusion.

Algorithms

Usages

Advantages

Drawbacks

Predict positions during GNSS
outages.

It fuses sensor data for positioning without
using the system model.

ANNs are black boxes, which cannot explain how
each variable affects the navigation system.

Artificial neural
network
[157,181,233–236]

End-to-end positioning.

Fuzzy logic
[35,170,238–241]

Adjust measurement
and process noise
covariance matrices.

Support vector machine
[137,172,237,244]

Predict in the fusion
systems during sensors’
outages.

Deep learning
[257–267]

Model the high nonlinear INS
errors.

End-to-end positioning.

Process camera and
laser data.

Reinforcement
learning [268–274]

Adjust the navigation
parameters.

Vehicle tracking.

It can predict in complex nonlinear systems
without prior knowledge such as characteristics
[157].

It is able to deal with massive data efficiently.

It usually requires a large number of training data,
leading to over-fitting and poor generalization [237].

It is difficult to provide the uncertainty of position-ing
results.

It can model process and measurements noise
without the need of their probability
characteristics [240].

The fuzzy rationale is not constantly accurate. The
results are perceived based on assumptions, so it may
not be widely accepted.

The system is simple and justifiable.

It takes in expert knowledge and is good at
handling nonlinearity and non-Gaussian outliers
[242].

It has high generalization ability and strong
adaptability for different navigation
environments [244].

It can effectively deal with high-dimensional
data, such as wireless fingerprint data.

It avoids local minima and overfitting
[137,237].

It works well with a small number of training
data [137].

Approval and verification of a fuzzy
information-based framework need broad
equipment-based tests.

Time consumption increases obviously on kernel
function with a large dataset.

Its positioning performance decreases
significantly if the data has more noise.

In a complex task, many decision trees are needed
[245]

The interpretability of the forest becomes weak
when the scale of the forest reaches a certain
extent [245].

Deep learning is suitable to model data with a
large number of inputs including images and
time-varying sensor data.

It is a black box, which cannot explain the
contribution of each positioning source to the final
navigation solution.

It can learn complicated features and
relationships from sensor data, which is
difficult for hand-crafted methods [261].

With massive training data, the positioning
accuracy can significantly surpass other
learning-based algorithms.

It requires to train with huge computing resources
and massive data.

A large amount of human resources are needed to
label the training data.

It is difficult to provide the uncertainty of position-ing
results.

It has decision-making ability, which suits well
with vehicle tracking.

It needs additional storage in navigation applications
[271].

It has a strong automatic exploitation ability,
so the learned parameters can keep the validity
for a certain period of time [271].

For DRL, the amount of calculation and the
complexity of the reward definition is large.

Recognize human activity.

It is not sensitive to abnormal data in training.

Random forest
[245–249]

Evaluate the quality of GNSS
positioning.

It handles the high dimensional sensor data
effectively [248].

It avoids data overfitting [246,248].

5. Design considerations

5.1. Metrics of navigation/positioning applications

When designing a navigation/positioning application, several met-
rics should be considered based on users’ requirements, which generally
include:

(a) accuracy: this is always the most important metric. It mainly
depends on the used sensors, which is summarized in Table 2.
During the selection of sensors, designers need to consider a
tradeoff between accuracy and cost. In addition, accuracy can
be evaluated by metrics including mean error and Root Mean
Square Error (RMSE) [23].

(b) coverage: the layout of facilities for navigation should be de-
signed based on the required coverage. For the coverage of
wireless-based positioning systems, signal coverage and Field Of
View (FOV) should also be taken into consideration.

(c) navigation update rate: the requirement for data rate depends
partly on users’ moving speed. Meanwhile, it is a tradeoff be-
tween the update rate and the system burden.

(d) real time consideration: will be discussed in Section 5.4.
(e) scalability: depend on the user scale. It will be discussed in

Section 5.5.

(f) availability and reliability: availability indicates the proportion
of time when a navigation system can be used, while relia-
bility indicates whether a system can alert users when facing
large errors. Both availability and reliability are relevant with
the system’s robustness to outliers, which will be discussed in
Section 5.7.

Apart from these metrics, other software and hardware design con-
siderations are needed to maintain high positioning/navigation perfor-
mance: analytics-based or learning-based systems (Section 5.2), state
selection and observability (Section 5.3), and time synchronization
(Section 5.6). Application cases are presented in Section 5.8.

InformationFusion95(2023)62–9078Y. Zhuang et al.

Table 6
Analytics-based versus learning-based systems.

Analytics-based
systems

Pros

Cons

Do not need training data.

Needs fewer computational
resources.

System and observation
model should be
well-studied.

Adaptive to multiple
scenarios.

Poorer ability in nonlinear
and non-Gaussian systems.

Learning-based
systems

Good to deal with
non-linear and
non-Gaussian systems.

Usually need massive training
data and large computational
resources.

Do not need to study the
internal mechanism of the
system.

Generalization capability is
questionable.

5.2. Analytics-based or learning-based systems?

The model-driven analytics-based systems are widely used in indus-
try and have been well tested in practice. However, in this big data
era, data-driven learning-based systems become popular and challenge
traditional methods for accuracy and robustness; consequently, how to
choose between them is a practical question.

Learning-based systems can evolve with more data, which con-
versely means large computational and data collection costs. However,
if not properly trained, learning methods may lead to low generalized
ability, i.e., a model trained on one scene may not be transferable
[275]. In real applications, the selection between analytics-based and
learning-based systems depends on data and computation resources,
the maturity of existing positioning models, and the complexity of the
positioning task. A comparison of them is summarized in Table 6.

5.3. State selection and observability

In analytics-based navigation systems, the integration system model
depends firstly on state selection. This statement is true not only for
filtering-based systems, but also for most optimization-based systems
[49,192,193]. In this subsection, we mainly discuss the state selection
of filtering-based systems, which have been widely used and tested in
industry.

Since navigation systems are always nonlinear, it is a common prac-
tice to use the error states [24] as expressed in Eqs. (9) and (15), rather
than the original states, to describe a system. Most integration systems
choose INS or PDR as the main system and design with the error states
based on their dynamics. Most integration systems involving INS choose
the position and velocity errors in the error states. Attitude errors,
accelerometer, and gyroscope biases are usually estimated, the first two
can cause a linear growth in velocity error, while gyroscope biases
cause quadratic growth. In contrast, most PDR-relevant integration
systems choose the position and heading errors in the error states; they
seldom choose velocity errors since the position is reckoned by steps,
rather than velocities.

Once the state variables are selected, it is essential to take observ-
ability into consideration as it can influence the convergence rate in
a filtering-based system. The KF measurement model is analogous to
a set of equations where the states are the unknown and the mea-
surements are the known quantities. As measurements accumulate over
time, there is a set of observation vectors 𝐳1, 𝐳2, … , 𝐳𝑘. The linearized
measurement model relative to the initial state 𝐱1 is [24]

where 𝐱1 is the state vector and 𝐰𝑘 is the noise vector. The observation
matrix 𝐎1∶𝑘 is defined as

𝐎1∶𝑘 =

𝐇1
⎛
⎜
𝐇2Φ1
⎜
⋮
⎜
⎜
𝐇𝑘Φ𝑘−1 ⋯ Φ2Φ1
⎝

⎞
⎟
⎟
⎟
⎟
⎠

(22)

The rank of matrix 𝐎1∶𝑘 is defined as 𝑚 and the length of the
state vector 𝐱1 is defined as 𝑛. The states are locally observable when
𝑚 = 𝑛 and partially observable when 𝑚 < 𝑛. The observability of
many parameters is dynamically dependent. For example, the attitude
errors and accelerometer biases of an INS are both unobservable at
constant attitude, but they both become observable after a change in
attitude, as this changes the relationship among the states in the system
model [24]. Moreover, eigenvalues of the error covariance matrix can
be used to evaluate the degree of observability [276]. Observability
analysis can also be used to solve the inconsistency problem that real-
time estimators, e.g., filters, fixed-lag smoothers, may output falsely
optimistic covariance inconsistent to the actual state error [277].

When the state vector is observable, the rate of convergence of a
KF state depends on the measurement sampling rate, the measurement
noise, and the system noise. This is known as stochastic observability
[24]. System and measurement noise can mask the state vector that
only has a small impact on the measurements, making those states
effectively unobservable. For those stochastically unobservable states,
their uncertainties can be equal, or even larger, than the initial ones
when the other state variables converge.

In real applications, the states with strong observability should be
selected. The choice of inertial instrument errors to estimate depends on
their effect on the position, velocity, and attitude solution [24]. An ob-
servable IMU error has a significant impact on navigation accuracy and
its impact should be no less than that of the random noise. Accelerom-
eter and gyro scale factors and cross-coupling errors are seldom chosen
for estimations, since these errors are often unobservable, except in
highly dynamic applications [24]. Besides scale factors and cross-
coupling errors, the observability of many parameters is dynamically
dependent [278,279]. Three instances are given as follows. The attitude
errors and accelerometer biases of an INS are not separately observable
at constant attitude, but they are after the attitude change [24]. In the
vision-aided INS, constant motions (e.g., pure translation and constant
acceleration) can lead to additional unobservable directions [278]. In
addition, constant accelerometer and gyro measurements can make
camera time offset weakly unobservable [279].

The state selection of sensors other than IMU, such as GNSS, WiFi,
etc., depends on the integration architecture, as discussed in Sec-
tion 3.2. In loosely coupled integration, only inertial states are esti-
mated; however, in tightly, or ultra-tightly, coupled integration, param-
eters of other sensors must be estimated. In GNSS/INS tightly-coupled
integration systems, it is common practice to estimate the clock bias
and drift errors, as shown in Eq. (15), since they are observable and
have a strong impact on the navigation performance. In ultra-tightly-
coupled systems, the reference-signal carrier phase offsets 𝛿𝜌𝑖,𝑘, for
each satellite 𝑖 and channel 𝑘 tracked, and carrier frequency tracking
errors 𝛿𝑓𝑖,𝑘, etc., may also be estimated [224]. In other tightly coupled
integration systems, such as WiFi/MEMS, RSS bias can also be put into
the state vector [23]. Furthermore, TOA and its time derivatives can be
estimated in a UWB/INS system [218]. Consequently, it is necessary to
analyze the system observability, architecture, and application scenario
before composing the state.

5.4. Real time considerations

𝐳1
⎛
⎜
𝐳2
⎜
⋮
⎜
⎜
𝐳𝑘
⎝

⎞
⎟
⎟
⎟
⎟
⎠

= 𝐎1∶𝑘𝐱1 +

𝐰1
⎛
⎜
𝐰2
⎜
⋮
⎜
⎜
𝐰𝑘
⎝

⎞
⎟
⎟
⎟
⎟
⎠

(21)

Before designing the positioning or navigation systems, real time
consideration is an essential factor that depends on application scenar-
ios. For applications such as car navigation and logistics delivery, real
time operation is a hard demand. In applications such as surveying and

InformationFusion95(2023)62–9079Y. Zhuang et al.

geo-referencing, a navigation solution is required for analysis offline.
Generally, real-time requirements will lead to lower robustness and
accuracy.

approach utilizes time-tagging by both the hardware and software ap-
proaches, which are low-cost, flexible, and reliable, but more involved
[286].

In analytics-based systems, real time processing is often realized
by filtering. Some optimization-based approaches can also offer real-
time solutions with a sliding window [192,197] structure. For post-
processing systems, optimization methods can achieve a global optimal.
Alternatively, Kalman filters can be transformed to Kalman smoothers,
of which there are three kinds, (i) fixed-interval, (ii) fixed-point, and
(iii) fixed-lag [280,281].

Learning-based systems are also capable of real-time navigation/
positioning. Most traditional learning methods, other than deep learn-
ing, are hybrids where KF-relevant methods predict the states [35,233,
237,249], estimate noise covariances [157,238,239], and other param-
eters [269]. Since KF is a real-time estimator, most of these methods
navigate in real time. Deep learning algorithms are usually designed
independently with KF and require high computing resources. With a
strong processing unit, they can also achieve real-time positioning in
vision-based [258], point cloud based [259], and fingerprint [266] data
fusion systems.

5.5. Scalability

Scalability is the metric whether a localization technique can be
applied to a large number of users over a large geographical area. Since
GNSS is based on broadcasting navigation messages globally and has
taken the dominant role in outdoor navigation, it is easy to achieve
high scalability in outdoor navigation systems using GNSS technologies,
such as network RTK. However, in an indoor environment, positioning
infrastructure must be deployed in advance, which may lead to high
cost and poorer scalability. A system with good scalability should
require less a priori information including calibration [282,283], less
infrastructure, and lower cost, thus, there is always a trade-off be-
tween scalability and accuracy. Infrastructure dependent technologies
for high-accuracy indoor positioning is usually more costly; hence,
when considering large-scale deployment, it is better to choose technol-
ogy with less calibration and infrastructure modification. For example,
in a fingerprinting system, reducing the offline calibration process by
utilizing crowd-sourced data, is an option [283].

5.6. Time synchronization

Multi-sensor data should be timestamped consistently, otherwise,
they may interfere with each other. Time synchronization is mostly
an engineering problem and is especially important for high-precision
positioning, or highly dynamic scenarios [24]. The selection of a syn-
chronized approach depends on whether the sensors can be triggered
with an external time Ref. [284]. Some sensors, such as a GNSS
receiver, can provide Coordinated Universal Time (UTC) timestamps as
a reference, while others, such as radars, are free-running and cannot
give absolute time references; in such cases, a sensor should give times
offsets relative to other sensors [284,285]. For instance, Lei et al. [285]
use UWB timestamps to integrate with IMU and camera. GNSS is an
important source of accurate timing and includes UTC timestamps.
Hence, GNSS-aided integrated navigation/positioning systems usually
suffer less from time synchronization problems.

To date, most studies of time synchronization involve GNSS/INS
integration, which can be classified into [286,287], (i) hard (hardware-
based), (ii) soft (software-based), and (iii) a hybrid of both. In the
hardware approach, the one pulse-per-second signal (1PPS) output
from a GNSS receiver is used as input, requiring a specific triggering
design, which is unlikely suitable to alternative sensor combinations.
The software approach falls into two further categories, (i) the aug-
mented Kalman filter method [287], and (ii) the controlled trajectory
method [288]. The performances of both these implicitly relate to state
observability and strongly depend on the vehicle trajectory. The hybrid

Apart from GNSS, clocks inside a PC or another sensor can also be
used to generate triggers for synchronization. Jeong et al. [289] used
the system clocks of the three PCs to synchronize LiDAR, camera, and
GPS/INS systems. Choi et al. [290] used the pulse generated by the
clock inside a thermal camera to synchronize other cameras while other
sensors (LiDAR and GPS/IMU) are synchronized by software. Similar
methods may also be used in GNSS-denied environments.

5.7. Robustness to outliers

Multi-sensor integrated systems are more prone to errors than a
single-sensor system. If the unexpected data, such as un-modeled dy-
namics or data distribution, are not correctly recognized, they will lead
to a reduce in overall positioning accuracy, and may even cause the
navigation system to diverge. In a robust navigation system, outliers
should either be restrained or removed. The most well-known outlier
detection algorithm is the RANdom SAmple Consensus (RANSAC).
In [291], mismatched points in feature extraction of vision position-
ing were removed based on the RANSAC method. Some learning ap-
proaches, such as the EM algorithm, can also be effective [292]. The
methods discussed above deal with outliers in the pre-processing. It is
also capable of restraining or removing outliers in the fusion process. In
optimization-based approaches, a loss function can be used to reduce
the influence of outliers [199]. In filtering-based approaches, when
outliers are detected, a robust KF can reduce the Kalman gain and
modify the measurement noise covariance matrix [293,294].

5.8. Application cases

In this subsection, we take autonomous driving for instance [105,
106,295–297] to analyze the design considerations mentioned above.
To safely navigate on the road, centimeter-level accuracy with high
reliability is required [295]. Autonomous driving always needs wide
coverage on road; thus, positioning systems that support global cover-
age (e.g., GNSS, INS, vision, and LiDAR) are adopted. These positioning
systems also allow good scalability. The navigation system must be
strictly real-time and needs a high update rate (>10 Hz [105,295])
since autonomous driving is very sensitive to time. To achieve this,
accurate time synchronization (10-ms level [289,290]) is required.
Availability, reliability, and robustness are all essential, which means
the navigation system should deal well with outliers [296,298]. The
navigation algorithm can use the combination of both analytic and
learning based methods, e.g., deep learning [105,106,295] is used to
deal with vision data while filtering [296] and optimization [297,298]
methods are used for state estimation in a fusion system. Additionally,
position, velocity, and attitude are all essential when selecting a state.

6. Application scenarios

Multi-sensor integration has been applied for diverse scenarios. The
following is a review of typical applications that are classified by
navigation platforms. These applications include land vehicles, indoor
localization, air vehicles, surface ships, underwater vessels, and outer
space, which are presented in Fig. 10.

6.1. Land vehicles

Land vehicles, including cars, motorcycles, vans, mobile robots, etc.,
have great demands on localization and navigation. In this subsection,
we select car and mobile robots as representatives.

Car navigation, which is the most common navigation applica-
tion, has attracted many researchers. Currently, GNSS/INS integrated
navigation [28,30,157,181,182,191,237,239,271] is the most popular

InformationFusion95(2023)62–9080Y. Zhuang et al.

Fig. 10. Application scenarios.

positioning system. In some environments (e.g., urban areas) where
GNSS suffers much from multipath, odometers [10,76,77], vision [194,
272,299], LiDAR [97,98,296], ultrasonics [300], map matching [117],
and UWB [243,301] can be used to aid it to produce a precise and
robust navigation system. In recent years, LiDAR and vision become
hot in car navigation.

Recently, autonomous driving has attracted huge industry invest-
ment. Different from car navigation systems, its tasks include not only
localization, but also perception, path planning, and control [295],
where localization plays a key role in other tasks. Since autonomous
driving is a multi-task process, there are three primary approaches for
combining sensory data based on interdependence between the follow-
ing [106]: high-level, mid-level, and low-level fusion. Autonomous ve-
hicles, which primarily use the camera, millimeter-wave radar, GNSS,
IMU, and LiDAR, mainly fuse data from a combination of camera-
LiDAR, camera-radar, or camera-radar-LiDAR [105,106], with the aid
of GNSS and IMU. In the work [296], a pre-built map was used for
LiDAR localization, and multi-sensor data helped with the ambiguity
resolution of GNSS RTK. The system made vehicles fully autonomous
in crowded city streets. Shao et al. [297] combined GNSS/INS solu-
tion with LiDAR scan matching and visual odometry to optimize the
poses; then the pose and the LiDAR scan measurements were utilized
to build a two-dimensional (2D) probability map. Besides, the track-
ing of surrounding vehicles is essential for many tasks (e.g., obstacle
avoidance, path planning, and intent recognition) and crucial to truly
autonomous driving [273]. Research [272,273] used LiDAR and camera
to track multiple objects due to their complementary capabilities of
environment perception. Multi-sensor fusion in automated driving was
reviewed in [105,106].

Localization and navigation are basic requirements when building
an autonomous mobile robot system. In outdoor environments, a com-
bination of GNSS, vision-based, and LiDAR-based systems is widely
used, while indoors, vision, RF-based, and acoustic systems are popular.
Integrating GNSS, RF-based and acoustic systems for mobile robot lo-
calization is well established. Compared to visual sensors, sonar is more
credible when the robot enters a dark environment. Ultrasonic signals
were integrated with inertial sensors [112,302] and wireless network
[165,235] to provide localization for an indoor robot. Furthermore, in
an indoor environment, RF signals, such as UWB [158,159,236,303],
WiFi [304], and WSN [165], can be added to the localized system.

In the past decade, the rapid development of Simultaneous Lo-
calization and Mapping (SLAM) [80] has driven camera-based and
LiDAR-based mobile robot navigation in an unknown environment.
Plenty of VIO and LIO systems including VINS-Mono [92] and FAST-
LIO2 [12] have been established for robotic navigation tasks. In [133],
the vision-based navigation method was integrated with a low-cost
reduced inertial sensor system by EKF to bridge the navigation gap

during GPS outages by using IMUs and wheel speed sensors. Tang et al.
[195] presented IC-GVINS for wheeled robots, fully utilizing the precise
INS in both the state estimation and visual process. Details on vision
and LiDAR have been explored in Section 2.1.

6.2. Indoor localization

For indoor localization, the five main positioning systems are, (i)
ultrasonic, (ii) RF, (iii) inertial, (iv) magnetic, and (v) vision-based.
However, a single positioning system is inaccurate; therefore, indoors,
an integrated system is imperative. Usually, a combination of wire-
less and inertial sensors is commonly used. In [46,116,120,121,138,
153,208,305,306], WiFi/PDR navigation systems were improved by
introducing estimation filters. WiFi signals can also be integrated with
INS [23,33,151,152,189,205,207,307]. Since most buildings have WiFi
APs, localization systems do not need additional infrastructure, but
power consumption is high. Bluetooth has lower power consumption
than WiFi [110]; hence, in [58,306], Bluetooth plus inertial sensors
were proposed. By using mobile phones, neither WiFi nor Bluetooth
need additional hardware, but they have low accuracy.

Other combinations used RFID [63,125], UWB [126,160,166,167]
and WLAN [115,190] to integrate with either INS or PDR. These kinds
of systems require additional positioning hardware. An emerging di-
rection of indoor localization is by introducing Visible Light Positioning
into the positioning system [3,308,309]. Positioning accuracy is usually
better than 0.1 m, outperforming the systems mentioned above. Also,
map information [116,151,152,310] and landmarks [305,310] can be
utilized for navigation systems, although their construction takes labor
and time. Geomagnetic information was used to aid inertial sensors in
[74,120,153,311].

6.3. Air vehicles

Air vehicles, including aircraft, guided missiles, UAVs, High Attitude
Platform Station (HAPS), etc., can hardly use non-GNSS radio-based
positioning sources and map information as land vehicles do. In this
subsection, we select aircraft and UAVs as representatives. When multi-
sensor integrated navigation systems are applied, GNSS/INS integration
is the most popular, for both aircraft [162,163,174,185,312–316] and
UAVs [161,164,173,215,317].

An integrated system comprising a SINS and GNSS has become
the main method to derive aircraft trajectory information for airborne
earth observation [314]. In [312], a sigma-point filter was applied to
GPS/INS integration. Attitude was represented by a three-dimensional
vector of generalized Rodrigues parameters, which reduced the size of
the covariance matrix. An iterated KF was proposed for INS/GPS inte-
gration [162] and was applied to SAR motion compensation. Authors
of [174] investigated the in-motion alignment of a SINS/GPS integrated
system using the UKF and CDKF. In [316], an INS aided by an aircraft
dynamic model was presented to manage the absence of GPS signals. A
fast-update Aircraft Dynamic Model (ADM) made it possible to utilize
a direct filtering method by employing nonlinear INS dynamics as
system equations and a nonlinear ADM as observation equations, which
substituted for indirect filtering based on linearized error equations.
The work [179] addressed the attitude and position estimation of a
small-size unmanned helicopter tethered to a moving platform by using
a multi-sensor data fusion algorithm based on a Square-Root UKF. The
state prediction was performed using a kinematic process model driven
by measurements of the inertial sensors onboard the helicopter, while
the subsequent correction used information from additional sensors,
such as a magnetometer, a barometric altimeter, a LiDAR altimeter, and
magnetic encoders that measured the tether orientation relative to the
helicopter.

To better utilize UAVs to save effort, time, and human life with
the assigned tasks, the UAV requires an accurate, precise, and robust
navigation system. In [164], the typical repeated dynamic patterns of

InformationFusion95(2023)62–9081Y. Zhuang et al.

UAVs offered useful information for estimating the UAV navigation
states. Machine learning classifiers were employed to detect the re-
peated dynamic patterns; then an appropriate constraint/update was
performed through EKF to obtain a better estimate of the UAV states.
Apart from filters, smoothers have also been used in UAV navigation
systems. Online and offline UAV position estimation, together with
their velocity and orientation, were presented in [317]. For off-line
estimation, a fixed-interval smoothing algorithm was applied. Online
estimation was accomplished with a fixed-lag smoothing algorithm. To
compensate for the GNSS signal outage in an indoor environment, RF
signals could be utilized, such as UWB signals [318,319]. The authors
of [131] studied the indoor localization of a small, low-cost UAV by
using the UbiSense UWB Real-Time Localization System and low-cost
IMU in conjunction with an EKF to improve position accuracy. The
camera was another widely used sensor during GNSS signal outages
[320]. However, vision-based systems suffer in low-textured or low-
illumination areas. In [171], a magnetometer was integrated with an
IMU for an accurate heading estimation of an indoor UAV.

6.4. Surface ships

In surface ship navigation systems, the GNSS system is an impor-
tant component as it is often integrated with other sensor modalities
to improve navigation performance, such as in GNSS/INS integrated
systems [321,322], a GNSS/Laser Gyro INS integrated system [323],
and a GPS/IMU/speed log integrated system [135]. However, GNSS
signals suffer from many issues, such as spoofs and interceptions [324].
Therefore, many researchers have investigated alternatives, such as the
Star Sensor and Radar. To negate outside interference, Star Sensors can
work independently and are at the cutting-edge of CNS [325]. The work
[326] proposed an algorithm based on a One-Dimensional Wiener Filter
(1DWF) to resolve the restoration of the Blurred Star image under high
dynamic conditions, by applying it to an integrated SINS/CNS system.
The work [325] used an INS/CNS integrated navigation method based
on Particle Swarm Optimization Back Propagation Neural Network
(PSOBPNN) to resolve CNS’s invalidity in cloudy weather.

Currently, autonomous ship navigation is in great demand, with
collision avoidance one of its important responsibilities [327]. To this
end, radar systems are often integrated with INS or GNSS [327,328].
Moreover, vision-based navigation provides massive amounts of infor-
mation, does not need wireless devices, and is now hotly debated in
the field of surface ship navigation. A ship navigation system has used
Vision/Radar/INS integration to measure the baseline between ship and
a UAV [134]. The work [329] used a high sampling rate of vision-based
navigation to achieve a Shipboard-Relative GPS/INS/Vision integrated
system. By fusing INS and Ultrashort Base Line (USBL) in a tightly
coupled scheme and without the aid of GNSS, the work [293] achieved
promising results. Since trajectories of surface ships are, approximately,
within a plane, research [324–326,330] adopted a two degrees of
freedom controller.

6.5. Underwater vessels

GNSS signals cannot be used with underwater vessels; consequently,
Doppler sonar, inertial sensors, and bathometers are the most common
sensors used in navigation [136,137]. Using Kalman filtering to merge
data received from an acoustic positioning system, a bathometer and
a DVL, a navigation system [331] was developed and implemented
in both simulation and in an actual submarine; while authors [332]
discussed Underwater Transponder Positioning (UTP), which required
only one transponder due to tight coupling with the INS. In [242], USBL
is integrated with IMU, DVL, compass, and pressure sensor, which is
designed for use in underwater seabed mapping applications for ocean
exploration.

6.6. Outer space

There are two main types of integrated navigation systems in outer
space, (i) autonomous satellite, and (ii) spacecraft. For the former, CNS
is one of the best, since it is low-cost and passive. A satellite’s position is
estimated by applying the state estimation method considering the mea-
sured celestial body positions. Its position error is independent of time
and has a strong anti-interference capability; however, it suffers from
the low accuracy of the horizon sensor. Another emerging technology is
the X-ray pulsar, which compares the pulse TOA observed by the X-ray
sensors at the satellite, and predicted by pulse timing [333]. Like CNS,
its anti-interference capability is strong and, because it has only one
single pulsar, its navigation state is unobservable. Therefore, in [180],
a pulsar/CNS integrated navigation method, based on a federated UKF
was proposed, and achieved velocity accuracy greater than 0.1 m/s,
improved position accuracy, and decreased both cost and failure risk.
In [334], a UKF-based information fusion method was proposed for
directly sensing horizon by using an earth sensor, and indirectly sensing
horizon by observing starlight atmospheric refraction.

For spacecraft navigation systems, some measurements have been
used, including geocentric vector, geocentric distance of earth sensor,
and star sensor’s outputs [335]. The astronavigation system has been
widely used in space missions, including CNS and the Doppler mea-
surement. In [238], KF was adapted to integrate data produced by
SINS sensor suites and external aiding, such as Autonomous Navigation
System (ANS) for guided vehicles to provide optimal estimates of
position and attitude. A filtering algorithm, Iterated Square Root UKF
(ISRUKF), and a switch-mode information fusion filter based on ISRUKF
and EKF were proposed in [335]. This method can fuse geocentric
vector and distance measured by a navigation sensor with starlight
angular distance and adapt measurement noise covariance matrices
online to approximate the actual system. In [336], vision-based relative
navigation of two spacecraft was addressed by using the sparse-grid
quadrature filter, which provided the estimates of relative orbit and
relative attitude together with the gyro biases.

7. Future research directions

Research to date has explored various types of integrated navigation
systems, including both analytics-based and learning-based schemes.
However, issues and challenges still exist in this field. Here we give
some suggestions for future research.

(a) Accuracy evaluation and error mitigation: accuracy evaluation is
always difficult for localization, especially in some complex indoor
environments, such as retail shops, shop floors and offices, because
ground truth is often difficult, or even impossible, to obtain. Crowded
environments create too much interference, which makes it hard to
evaluate errors through external assistance. Multipath and NLoS prob-
lems severely affect the accuracy of wireless-based localization. Future
work may focus on the detection and mitigation of these problems in
integrated systems. Using multiple sensors can help with the detec-
tion of multipath and NLoS [223], which can be realized either by
environment sensing, or training the historical dataset.
(b) Collaborative localization and crowdsource-based positioning: while
millions of users and devices are connected by IoT, massive amounts
of data are collected in real time. Hence, collaborative localization and
crowdsourcing using data from existing public infrastructures is a trend
for low-cost mass-market IoT applications. Under the crowdsourcing
framework, location users become also location providers; hence, in a
fingerprinting positioning algorithm [154], time and labor to build the
database are largely saved.
(c) Broader use of optimization methods: analytics-based approaches
are mainly KF-relevant estimation methods. However, graph optimiza-
tion is highly likely to deal with nonlinear problems; also, it is easy
to design an optimization architecture for fusing multi-sensor data.

InformationFusion95(2023)62–9082Y. Zhuang et al.

With a sliding window design, it can also support real-time posi-
tion/navigation. In the future, we anticipate seeing more applications
with graph optimization approaches.
(d) Theoretical aspects of sensor fusion:
for instance, the core goal of
both analytics-based and learning-based systems is to minimize errors;
however, most algorithms are easy to fall into local minima rather
than global optimization. Therefore, how to transfer from a non-convex
problem into a convex one remains to be explored, especially for
optimization-based approaches.
(e) INS-free filtering model:
in KF-relevant systems, INS error is com-
monly used as the state model, which makes INS an indispensable part
of an integrated navigation system [132]. The state model, without
having to depend on INS, and INS-free integrated navigation, should
be explored in future studies. This will help to ensure that navigation
systems will still work in the event of accelerometer or gyro failure. For
that model, observability (demonstrated in Section 5) should be fully
analyzed.
(f) Comprehensive comparisons between learning-based and analytics-
based approaches:
learning-based navigation systems perform better
when dealing with calibration errors and faulty sensors. However, most
research does not thoroughly differentiate between learning-based and
analytics-based methods, in that they always discuss the accuracy, but
they neglect other qualities, such as reliability and cost; this make
it hard to select the most effective localization scheme. A general
comparison between these two methods is presented in Section 5. We
urge future researchers to concentrate more on method selection for the
various integrated systems. In addition, some learning-based methods,
such as RL, should receive more attention.
(g) Positioning with new sensors: modern technology has given rise
to many new sensors, of which many are capable of positioning in a
certain scenario. For instance, in urban areas, an event-based camera
can capture moving objects, thereby calculating their kinematic charac-
teristics; the 6G communication, together with high-resolution imaging
and sensing, will provide 10 cm level indoor positioning [337].
(h) Interpretability of learning-based methods:
learning-based methods
are black boxes [282] and their mechanisms cannot be easily inter-
preted, especially for deep learning. Poor interpretability means that
navigation users will not trust the robustness of a training model; con-
sequently, an integrated navigation system that is short on robustness,
may lead to serious accidents. Therefore, a potential research direction
is to investigate how deep neural networks learn when they are used
for multi-sensor fusion.
(i) Data variety for indoor localization:
in the era of big data, research
on multi-sensor positioning/navigation should not be limited to the
positioning algorithm, but also pay attention to data variety, especially
for indoor localization. People spend 80% of their time indoors, which
enables us to train huge data resources with deep learning algorithms.
For instance, pedestrian-based localization plays an important role in
LBS applications. However, existing PDR methods usually considered
simple walking patterns (forward walking, backward walking, right
lateral walking, left lateral walking, and running) [260]. To obtain
more accurate location-based services, more walking patterns, such as
jumping, jogging, sprinting, ascending and descending stairs, crouch
walking, and stair climbing, we expect will be considered in future
work. For pedestrian-based applications, we also hope to include more
IoT devices, such as smartwatches, wristbands, and smart earphones,
to extend the potential applications of the existing research.
(j) Integrity monitoring: a navigation system can occasionally produce
output errors much larger than the uncertainty bounds specified for, or
indicated by it. This may be due to hardware or software failures, or
unusual operating conditions. Integrity monitoring systems detect these
faults and protect overall navigation solutions. Integrity, together with
accuracy, continuity, and availability, are the most required navigation
qualities [24]. However, to our knowledge, most studies of integrity
discuss filtering-based GNSS/INS systems. Other navigation systems
and algorithms have not been fully studied. To build a secure multi-
sensor navigation system, more attention should be paid to integrity
monitoring in future work.

(k) Positioning privacy: Existing studies usually provide the same level
of privacy protection. However, users need different levels of privacy
protection for different times, different locations, and different data.
For example, the user requires a higher level of privacy protection at
the point of interest. On the contrary, the user requires a lower level of
privacy protection at unimportant locations. Therefore, a personalized
location privacy protection is a research hotspot. Secondly, existing
solutions ignore the trust evaluation of privacy-preserving systems,
leading to misevaluation of the privacy protection degree provided
by a privacy-preserving system. Additionally, it is still a challenge to
put forward indicators that can correctly measure privacy protection
technology. Thirdly, existing researches are inflexible and lack the
ability to adaptively select privacy protection strategies for different
scenarios. More importantly, with the maturity of technologies such as
edge computing and blockchain, it is still difficult to balance privacy
protection and utility when applying the above technologies to privacy
protection. Finally, with the development of quantum computer, the
traditional privacy protection methods based on cryptography cannot
resist the computing power of quantum computer. Therefore, location
privacy protection against quantum attacks is a hot research topic in
the future.

The next decade will almost certainly witness the continued prolif-
eration of integration architectures with further improvement in cost,
integration, and performance.

8. Conclusions

This article presented a wide-ranging survey of multi-sensor inte-
grated navigation/positioning systems, which gives a comprehensive
understanding to practitioners and researchers. To thoroughly review
integrated systems, we explored the literature and discussed many
widely-used single positioning and navigation systems. We then classi-
fied integrated navigation systems concerning categories of (1) sources,
(2) algorithms and architectures, and (3) scenarios. To go into a deeper
study, we classified the integrated navigation/positioning systems into
two categories based on integration algorithms, (i) analytics-based
fusion, and (ii) learning-based fusion. Analytics-based fusion originated
from the well-known Kalman filter, therefore it can be classified fur-
ther, based either on algorithms or integration levels. There has been
very little academic discussion regarding learning-based fusion, there-
fore, we selected several algorithms to both demonstrate and compare
with each other: ANN, fuzzy logic, SVM, random forest, deep learning,
and reinforcement learning. We have given a comprehensive tutorial
on the consideration of design before implementing an application. We
have also given a detailed introduction to the applications of integrated
navigation/positioning based on application scenarios. Furthermore,
we have suggested future research directions in order to trigger readers’
thinking about this crucial subject. Finally, we look forward to seeing
more breakthroughs of integrated navigation/positioning, and more
valuable applications in areas such as IoT.

CRediT authorship contribution statement

Yuan Zhuang: Conceptualization, Project administration, Writing
– review & editing. Xiao Sun: Investigation, Writing – original draft,
Writing – review & editing. You Li: Writing – review & editing. Jianzhu
Huai: Writing – review & editing. Luchi Hua: Investigation, Writing –
original draft. Xiansheng Yang: Writing – review & editing. Xiaoxiang
Cao: Writing – review & editing. Peng Zhang: Writing – review &
editing. Yue Cao: Writing – review & editing. Longning Qi: Writing
– review & editing. Jun Yang: Writing – review & editing. Nashwa
El-Bendary: Writing – review & editing. Naser El-Sheimy: Writing –
review & editing. John Thompson: Writing – review & editing. Ruizhi
Chen: Writing – review & editing.

InformationFusion95(2023)62–9083Y. Zhuang et al.

Declaration of competing interest

The authors declare that they have no known competing finan-
cial interests or personal relationships that could have appeared to
influence the work reported in this paper.

Data availability

No data was used for the research described in the article.

References

[1] D.H. Titterton, J.L. Weston, Strapdown Inertial Navigation Technology, second

ed., Institution of Engineering and Technology, 2004.

[2] M.S. Grewal, L.R. Weill, A.P. Andrews, Global Positioning Systems, Inertial
Navigation, and Integration, second ed., Wiley-Interscience, Hoboken, N.J,
2007.

[3] Y. Zhuang, L. Hua, L. Qi, J. Yang, P. Cao, Y. Cao, Y. Wu, J. Thompson, H.
Haas, A survey of positioning systems using visible LED lights, IEEE Commun.
Surv. Tutor. 20 (3) (2018) 1963–1988.

[4] Y. Zhuang, Z. Syed, Y. Li, N. El-Sheimy, Evaluation of two WiFi positioning
systems based on autonomous crowdsourcing of handheld devices for indoor
navigation, IEEE Trans. Mob. Comput. 15 (8) (2016) 1982–1995.

[5] Y. Zhuang, J. Yang, Y. Li, L. Qi, N. El-Sheimy, Smartphone-based indoor

localization with bluetooth low energy beacons, Sensors 16 (5) (2016) 596.

[6] J. Zhou, J. Shi, RFID localization algorithms and applications-a review, J. Intell.

Manuf. 20 (6) (2009) 695.

[7] K. Siwiak, D. McKeown, Ultra-Wideband Radio Technology, John Wiley & Sons,

2005.

[8] N.B. Priyantha, A. Chakraborty, H. Balakrishnan, The cricket location-support
system, in: Proceedings of the 6th Annual International Conference on Mobile
Computing and Networking, ACM, 2000, pp. 32–43.

[9] W. Qiuying, G. Zheng, Z. Minghui, C. Xufei, W. Hui, J. Li, Research on
pedestrian location based on dual MIMU/magnetometer/ultrasonic module, in:
Position, Location and Navigation Symposium (PLANS), 2018 IEEE/ION, IEEE,
2018, pp. 565–570.

[10] J. Georgy, T. Karamat, U.

Iqbal, A. Noureldin, Enhanced MEMS-
IMU/odometer/GPS integration using mixture particle filter, GPS Solut.
15 (3) (2011) 239–252.

[11] J. Yan, G. He, A. Basiri, C. Hancock, Vision-aided indoor pedestrian dead
Instrumentation and Measurement

reckoning,
in: 2018 IEEE International
Technology Conference (I2MTC), IEEE, 2018, pp. 1–6.

[12] W. Xu, Y. Cai, D. He, J. Lin, F. Zhang, FAST-LIO2: Fast direct LiDAR-inertial

odometry, IEEE Trans. Robot. 38 (4) (2022) 2053–2073.

[13] L. Chen, X. Zhou, F. Chen, L.L. Yang, R. Chen, Carrier phase ranging for
indoor positioning with 5G NR signals, IEEE Internet Things J. 9 (13) (2022)
10908–10919.

[14] Y. Zhuang, J. Yang, L. Qi, Y. Li, Y. Cao, N. El-Sheimy, A pervasive integration
platform of low-cost MEMS sensors and wireless signals for indoor localization,
IEEE Internet Things J. 5 (6) (2018) 4616–4631.

[15] A. Ben-Afia, L. Deambrogio, D. Salos, A.-C. Escher, C. Macabiau, L. Soulier, V.
Gay-Bellile, Review and classification of vision-based localisation techniques in
unknown environments, IET Radar Sonar Navig. 8 (9) (2014) 1059–1072.
[16] F.E. White, Data Fusion Lexicon, Report, Joint Directors of Labs Washington

DC, 1991.

[17] H.H. Afshari, S.A. Gadsden, S. Habibi, Gaussian filters for parameter and state
estimation: A general review of theory and recent trends, Signal Process. 135
(2017) 218–238.

[18] D. Loebis, R. Sutton, J. Chudley, Review of multisensor data fusion techniques
and their application to autonomous underwater vehicle navigation, J. Mar.
Eng. Technol. 1 (1) (2002) 3–14.

[19] D. Smith, S. Singh, Approaches to multisensor data fusion in target tracking: A

survey, IEEE Trans. Knowl. Data Eng. 18 (12) (2006) 1696–1710.

[20] A. Yassin, Y. Nasser, M. Awad, A. Al-Dubai, R. Liu, C. Yuen, R. Raulefs,
E. Aboutanios, Recent advances in indoor localization: A survey on theoret-
ical approaches and applications, IEEE Commun. Surv. Tutor. 19 (2) (2017)
1327–1346.

[21] X. Guo, N. Ansari, F. Hu, Y. Shao, N.R. Elikplim, L. Li, A survey on fusion-based
indoor positioning, IEEE Commun. Surv. Tutor. 22 (1) (2020) 566–594.

[22] N. El-Sheimy,

Inertial Techniques

and INS/DGPS Integration, Report,

Department of Geomatics Engineering, University of Calgary, 2006.

[23] Y. Zhuang, N. El-Sheimy, Tightly-coupled integration of WiFi and MEMS sensors
on handheld devices for indoor pedestrian navigation, IEEE Sens. J. 16 (1)
(2016) 224–234.

[24] P. Groves, Principles of GNSS, Inertial, and Multi-Sensor Integrated Navigation

Systems, Artech House, 2008.

[25] J. Farrell, M. Barth, The Global Positioning System and Inertial Navigation,

McGraw-Hill, New York, 1999.

[26] Z. Gao, Y. Li, Y. Zhuang, H. Yang, Y. Pan, H. Zhang, Robust Kalman filter aided

GEO/IGSO/GPS raw-PPP/INS tight integration, Sensors 19 (2) (2019) 417.

[27] I. Skog, P. Handel, In-car positioning and navigation technologies—A survey,

IEEE Trans. Intell. Transp. Syst. 10 (1) (2009) 4–21.

[28] K. Feng, J. Li, X. Zhang, X. Zhang, C. Shen, H. Cao, Y. Yang, J. Liu, An improved
strong tracking Cubature Kalman filter for GPS/INS integrated navigation
systems, Sensors (Basel, Switzerland) 18 (6) (2018).

[29] Z. Li, G. Chang, J. Gao, J. Wang, A. Hernandez, GPS/UWB/MEMS-IMU tightly
coupled navigation with improved robust Kalman filter, Adv. Space Res. 58
(11) (2016) 2424–2434.

[30] Y. Liu, X. Fan, C. Lv, J. Wu, L. Li, D. Ding, An innovative information
fusion method with adaptive Kalman filter for integrated INS/GPS navigation
of autonomous vehicles, Mech. Syst. Signal Process. 100 (2018) 605–616.
[31] F. Shen, S. Hao, X. Wu, C. Guo, INS/GPS tightly integrated algorithm with
reduced square-root Cubature Kalman filter, in: Control Conference (CCC), 2016
35th Chinese, IEEE, 2016, pp. 5547–5550.

[32] Y. Zhuang, H.W. Chang, N. El-Sheimy, A MEMS multi-sensors system for
pedestrian navigation, in: China Satellite Navigation Conference (CSNC) 2013
Proceedings, Springer, 2013, pp. 651–660.

[33] J. Cheng, L. Yang, Y. Li, W. Zhang, Seamless outdoor/indoor navigation with
WIFI/GPS aided low cost inertial navigation system, Phys. Commun. 13 (2014)
31–43.

[34] K. Gryte, J.M. Hansen, T. Johansen, T.I. Fossen, Robust navigation of UAV using
inertial sensors aided by UWB and RTK GPS, in: AIAA Guidance, Navigation,
and Control Conference, 2017, p. 1035.

[35] Z. Li, R. Wang, J. Gao, J. Wang, An approach to improve the positioning
performance of GPS/INS/UWB integrated system with two-step filter, Remote
Sens. 10 (1) (2017) 19.

[36] J. Wang, Y. Gao, Z. Li, X. Meng, C.M. Hancock, A tightly-coupled GPS/INS/UWB
cooperative positioning sensors system supported by V2I communication,
Sensors 16 (7) (2016) 944.

[37] A.M. Hasan, K. Samsudin, A.R. Ramli, R.S. Azmir, S.A. Ismaeel, A review of
navigation systems (integration and algorithms), Aust. J. Basic Appl. Sci. 3 (2)
(2009) 943–959.

[38] A. Sevincer, A. Bhattarai, M. Bilgi, M. Yuksel, N. Pala, LIGHTNETs: Smart
LIGHTing and mobile optical wireless NETworks—A survey, IEEE Commun.
Surv. Tutor. 15 (4) (2013) 1620–1641.

[39] L. Hua, Y. Zhuang, L. Qi, J. Yang, L. Shi, Noise analysis and modeling in visible
light communication using Allan variance, IEEE Access 6 (2018) 74320–74327.
[40] D. Karunatilaka, F. Zafar, V. Kalavally, R. Parthiban, LED based indoor visible
light communications: State of the art, IEEE Commun. Surv. Tutor. 17 (3)
(2015) 1649–1678.

[41] X. Sun, Y. Zhuang, J. Huai, L. Hua, D. Chen, Y. Li, Y. Cao, R. Chen, RSS-based
visible light positioning using nonlinear optimization, IEEE Internet Things J.
9 (15) (2022) 14137–14150.

[42] P. Lou, H. Zhang, X. Zhang, M. Yao, Z. Xu, Fundamental analysis for indoor
in: Communications in China Workshops

visible light positioning system,
(ICCC), 2012 1st IEEE International Conference on, IEEE, 2012, pp. 59–63.

[43] H.-S. Kim, D.-R. Kim, S.-H. Yang, Y.-H. Son, S.-K. Han, An indoor visible light
communication positioning system using a RF carrier allocation technique, J.
Lightwave Technol. 31 (1) (2013) 134–144.

[44] S.Y. Jung, S. Hann, C.S. Park, TDOA-based optical wireless indoor localiza-
tion using LED ceiling lamps, IEEE Trans. Consum. Electron. 57 (4) (2011)
1592–1597.

[45] J. Vongkulbhisal, B. Chantaramolee, Y. Zhao, W.S. Mohammed, A
fingerprinting-based indoor localization system using intensity modulation
of light emitting diodes, Microw. Opt. Technol. Lett. 54 (5) (2012) 1218–1227.
[46] M. Bachtler, J. Carrera, T. Braun, Kalman Filter Supported WiFi and PDR Based
Indoor Positioning System, Vol. 12, University of Bern, Bern, Switzerland, 2018,
pp. 23–30, (2).

[47] H. Liu, H. Darabi, P. Banerjee, J. Liu, Survey of wireless indoor positioning
techniques and systems, IEEE Trans. Syst. Man Cybern. C (Appl. Rev.) 37 (6)
(2007) 1067–1080.

[48] Y. Zhuang, Y. Li, Z. Syed, H. Lan, N. El-Sheimy, Wireless access point
localization and propagation parameter determination using nonlinear least
squares and multi-level quality control, IEEE Wirel. Commun. Lett. (2015).

[49] J. Tan, X. Fan, S. Wang, Y. Ren, Optimization-based Wi-Fi radio map construc-
tion for indoor positioning using only smart phones, Sensors (Basel) 18 (9)
(2018).

[50] Y. Zhuang, C. Zhang, J. Huai, Y. Li, L. Chen, R. Chen, Bluetooth localization
technology: Principles, applications, and future trends, IEEE Internet Things J.
9 (23) (2022) 23506–23524.

[51] F. Yin, Y. Zhao, F. Gunnarsson, Proximity report triggering threshold optimiza-
tion for network-based indoor positioning, in: Information Fusion (Fusion), 2015
18th International Conference on, 2015, pp. 1061–1069.

[52] E.S. Lohan, J. Talvitie, P. Figueiredo e Silva, H. Nurminen, S. Ali-Loytty,
R. Piche, Received signal strength models for WLAN and BLE-based indoor
positioning in multi-floor buildings, in: Localization and GNSS (ICL-GNSS), 2015
International Conference on, 2015, pp. 1–6.

InformationFusion95(2023)62–9084Y. Zhuang et al.

[53] Y. Zhao, F. Yin, F. Gunnarsson, M. Amirijoo, E. Özkan, F. Gustafsson, Particle
filtering for positioning based on proximity reports, in: Information Fusion
(Fusion), 2015 18th International Conference on, 2015, pp. 1046–1052.
[54] A. Thaljaoui, T. Val, N. Nasri, D. Brulin, BLE localization using RSSI measure-
ments and iRingLA, in: Industrial Technology (ICIT), 2015 IEEE International
Conference on, 2015, pp. 2178–2183.

[55] Z. Li, L. Xiao, S. Jie, C. Gurrin, Z. Zhiliang, A comprehensive study of blue-
tooth fingerprinting-based algorithms for localization, in: Advanced Information
Networking and Applications Workshops (WAINA), 2013 27th International
Conference on, 2013, pp. 300–305.

[56] A. Arvanitopoulos, J. Gialelis, S. Koubias, Energy efficient indoor localization
utilizing BT 4.0 strapdown inertial navigation system, in: Proceedings of the
2014 IEEE Emerging Technology and Factory Automation, ETFA, IEEE, 2014,
pp. 1–5.

[57] J. Li, M. Guo, S. Li, An indoor localization system by fusing smartphone
inertial sensors and bluetooth low energy beacons, in: 2017 2nd International
Conference on Frontiers of Sensors Technologies,
IEEE, 2017, pp.
317–321.

ICFST,

[58] P.K. Yoon, S. Zihajehzadeh, B.-S. Kang, E.J. Park, Adaptive Kalman filter for
indoor localization using Bluetooth Low Energy and inertial measurement unit,
in: Engineering in Medicine and Biology Society (EMBC), 2015 37th Annual
International Conference of the IEEE, IEEE, 2015, pp. 825–828.

[59] H.S. Maghdid, A. Al-Sherbaz, N. Aljawad, I.A. Lami, UNILS: Unconstrained
indoors localization scheme based on cooperative smartphones networking with
onboard inertial, Bluetooth and GNSS devices, in: 2016 IEEE/ION Position,
Location and Navigation Symposium, PLANS, IEEE, 2016, pp. 129–136.
[60] N.B. Suryavanshi, K.V. Reddy, V.R. Chandrika, Direction finding capabil-
International Conference on Ubiquitous

ity in bluetooth 5.1 standard,
in:
Communications and Network Computing, Springer, 2019, pp. 53–65.

[61] C. Huang, Y. Zhuang, H. Liu, J. Li, W. Wang, A performance evaluation
framework for direction finding using BLE AoA/AoD receivers, IEEE Internet
Things J. 8 (5) (2021) 3331–3345.

[62] T. Sanpechuda, L. Kovavisaruch, A review of RFID localization: Applications
and techniques, in: Electrical Engineering/Electronics, Computer, Telecommu-
nications and Information Technology, 2008. ECTI-CON 2008. 5th International
Conference on, Vol. 2, IEEE, 2008, pp. 769–772.

[63] A.R.J. Ruiz, F.S. Granja, J.C.P. Honorato, J.I.G. Rosas, Accurate pedestrian in-
door navigation by tightly coupling foot-mounted IMU and RFID measurements,
IEEE Trans. Instrum. Meas. 61 (1) (2012) 178–189.

[64] R. Bharadwaj, S. Swaisaenyakorn, C.G. Parini, J. Batchelor, A. Alomainy, Lo-
calization of wearable ultrawideband antennas for motion capture applications,
IEEE Antennas Wirel. Propag. Lett. 13 (2014) 507–510.

[65] M. Kok, J.D. Hol, T.B. Schön, Indoor positioning using ultrawideband and

inertial measurements, IEEE Trans. Veh. Technol. 64 (4) (2015) 1293–1303.

[66] D. Yang, H. Li, Z. Zhang, G.D. Peterson, Compressive sensing based sub-
mm accuracy UWB positioning systems: A space–time approach, Digit. Signal
Process. 23 (1) (2013) 340–354.

[67] T. Deißler, M. Janson, R. Zetik, J. Thielecke, Infrastructureless indoor mapping
in: Systems, Signals and Image Processing

using a mobile antenna array,
(IWSSIP), 2012 19th International Conference on, IEEE, 2012, pp. 36–39.
[68] E. Leitinger, M. Fröhle, P. Meissner, K. Witrisal, Multipath-assisted maximum-
likelihood indoor positioning using UWB signals, in: Communications Work-
shops
IEEE, 2014, pp.
170–175.

(ICC), 2014 IEEE International Conference on,

[69] A. Alarifi, A. Al-Salman, M. Alsaleh, A. Alnafessah, S. Al-Hadhrami, M.A.
Al-Ammar, H.S. Al-Khalifa, Ultra wideband indoor positioning technologies:
Analysis and recent advances, Sensors 16 (5) (2016) 707.

[70] A. Ward, A. Jones, A. Hopper, A new location technique for the active office,

IEEE Pers. Commun. 4 (5) (1997) 42–47.

[71] F. Ijaz, H.K. Yang, A.W. Ahmad, C. Lee, Indoor positioning: A review of
indoor ultrasonic positioning systems, in: Advanced Communication Technology
(ICACT), 2013 15th International Conference on, IEEE, 2013, pp. 1146–1150.
[72] H.-S. Kim, J.-S. Choi, Advanced indoor localization using ultrasonic sensor
and digital compass, in: Control, Automation and Systems, 2008. ICCAS 2008.
International Conference on, IEEE, 2008, pp. 223–226.

[73] F.H. Raab, E.B. Blood, T.O. Steiner, H.R. Jones, Magnetic position and
orientation tracking system, IEEE Trans. Aerosp. Electron. Syst. (5) (1979)
709–718.

[74] Y. Li, Y. Zhuang, H. Lan, P. Zhang, X. Niu, N. El-Sheimy, Self-contained indoor
pedestrian navigation using smartphone sensors and magnetic features, IEEE
Sens. J. 16 (19) (2016) 7173–7182.

[75] Y. Li, Y. Zhuang, P. Zhang, H. Lan, X. Niu, N. El-Sheimy, An improved
inertial/wifi/magnetic fusion structure for indoor navigation, Inf. Fusion 34
(2017) 101–119.

[76] Z. Li, J. Wang, B. Li, J. Gao, X. Tan, GPS/INS/Odometer integrated system
using fuzzy neural network for land vehicle navigation applications, J. Navig.
67 (6) (2014) 967–983.

[77] J. Georgy, A. Noureldin, M.J. Korenberg, M.M. Bayoumi, Modeling the
stochastic drift of a MEMS-based gyroscope in gyro/odometer/GPS integrated
navigation, IEEE Trans. Intell. Transp. Syst. 11 (4) (2010) 856–872.

[78] J.J. Rodriguez, J. Aggarwal, Matching aerial images to 3-D terrain maps, IEEE

Trans. Pattern Anal. Mach. Intell. 12 (12) (1990) 1138–1149.

[79] Y. Wu, F. Tang, H. Li, Image-based camera localization: an overview, Vis.

Comput. Ind. Biomed. Art 1 (1) (2018) 8.

[80] N. Piasco, D. Sidibé, C. Demonceaux, V. Gouet-Brunet, A survey on Visual-Based
Localization: On the benefit of heterogeneous data, Pattern Recognit. 74 (2018)
90–109.

[81] D.M. Chen, G. Baatz, K. Köser, S.S. Tsai, R. Vedantham, T. Pylvänäinen, K.
Roimela, X. Chen, J. Bach, M. Pollefeys, B. Girod, R. Grzeszczuk, City-scale
landmark identification on mobile devices, in: CVPR 2011, 2011, pp. 737–744.
[82] B. Zeisl, T. Sattler, M. Pollefeys, Camera pose voting for large-scale image-based
localization, in: 2015 IEEE International Conference on Computer Vision (ICCV),
2015, pp. 2704–2712.

[83] A. Dutta, A. Mondal, N. Dey, S. Sen, L. Moraru, A.E. Hassanien, Vision tracking:

A survey of the state-of-the-art, SN Comput. Sci. 1 (1) (2020) 57.

[84] A.J. Davison, I.D. Reid, N.D. Molton, O. Stasse, MonoSLAM: Real-time single
camera SLAM, IEEE Trans. Pattern Anal. Mach. Intell. 29 (6) (2007) 1052–1067.
[85] R. Mur-Artal, J.M.M. Montiel, J.D. Tardos, ORB-SLAM: a versatile and accurate
monocular SLAM system, IEEE Trans. Robot. 31 (5) (2015) 1147–1163.
[86] J. Engel, V. Koltun, D. Cremers, Direct sparse odometry, IEEE Trans. Pattern

Anal. Mach. Intell. 40 (3) (2017) 611–625.

[87] M. Ferrera, A. Eudes, J. Moras, M. Sanfourche, G. Le Besnerais, Ov2SLAM: A
fully online and versatile visual SLAM for real-time applications, IEEE Robot.
Autom. Lett. 6 (2) (2021) 1399–1406.

[88] G. Younes, D. Asmar, E. Shammas, J. Zelek, Keyframe-based monocular SLAM:

design, survey, and future directions, Robot. Auton. Syst. 98 (2017) 67–88.

[89] C. Chen, B. Wang, C.X. Lu, N. Trigoni, A. Markham, A survey on deep learning
for localization and mapping: Towards the age of spatial machine intelligence,
2020, arXiv preprint arXiv:2006.12567.

[90] A.I. Mourikis, S.I. Roumeliotis, A multi-state constraint Kalman filter for vision-
aided inertial navigation, in: Proceedings 2007 IEEE International Conference
on Robotics and Automation, IEEE, 2007, pp. 3565–3572.

[91] S. Leutenegger, S. Lynen, M. Bosse, R. Siegwart, P. Furgale, Keyframe-based
visual–inertial odometry using nonlinear optimization, Int. J. Robot. Res. 34
(3) (2015) 314–334.

[92] T. Qin, P. Li, S. Shen, Vins-mono: A robust and versatile monocular

visual-inertial state estimator, IEEE Trans. Robot. 34 (4) (2018) 1004–1020.

[93] J. Huai, C.K. Toth, D.A. Grejner-Brzezinska, Stereo-inertial odometry using
in: Proceedings of the 28th International Technical
nonlinear optimization,
Meeting of the Satellite Division of the Institute of Navigation (ION GNSS+
2015), 2015, pp. 2087–2097.

[94] P. Geneva, K. Eckenhoff, W. Lee, Y. Yang, G. Huang, OpenVINS: A research
platform for visual-inertial estimation, in: 2020 IEEE International Conference
on Robotics and Automation, ICRA, 2020, pp. 4666–4672.

[95] C. Campos, R. Elvira, J.J.G. Rodríguez, J.M.M. Montiel, J.D. Tardós, ORB-
SLAM3: An accurate open-source library for visual, visual–inertial, and
multimap SLAM, IEEE Trans. Robot. 37 (6) (2021) 1874–1890.

[96] C. Cadena, L. Carlone, H. Carrillo, Y. Latif, D. Scaramuzza, J. Neira, I. Reid, J.J.
Leonard, Past, present, and future of simultaneous localization and mapping:
Toward the robust-perception age, IEEE Trans. Robot. 32 (6) (2016) 1309–1332.
[97] A. Fernández, J. Diez, D. d. Castro, P.F. Silva, I. Colomina, F. Dovis, P. Friess, M.
Wis, J. Lindenberger, I. Fernández, ATENEA: Advanced techniques for deeply
integrated GNSS/INS/LiDAR navigation, in: 2010 5th ESA Workshop on Satellite
Navigation Technologies and European Workshop on GNSS Signals and Signal
Processing, NAVITEC, 2010, pp. 1–8.

[98] Y. Gao, S. Liu, M.M. Atia, A. Noureldin, INS/GPS/LiDAR integrated naviga-
tion system for urban and indoor environments using hybrid scan matching
algorithm, Sensors 15 (9) (2015).

[99] M.M. Atia, S. Liu, H. Nematallah, T.B. Karamat, A. Noureldin, Integrated
indoor navigation system for ground vehicles with automatic 3-D alignment and
position initialization, IEEE Trans. Veh. Technol. 64 (4) (2015) 1279–1292.

[100] C. Qin, H. Ye, C.E. Pranata, J. Han, S. Zhang, M. Liu, LINS: A lidar-inertial
state estimator for robust and efficient navigation, in: 2020 IEEE International
Conference on Robotics and Automation, ICRA, pp. 8899–8906.

[101] J. Zhang, S. Singh, LOAM: Lidar odometry and mapping in real-time,

in:

Robotics: Science and Systems, Vol. 2, Berkeley, CA, pp. 1–9.

[102] T. Shan, B. Englot, LeGO-LOAM: Lightweight and ground-optimized lidar
odometry and mapping on variable terrain, in: 2018 IEEE/RSJ International
Conference on Intelligent Robots and Systems, IROS, 2018, pp. 4758–4765.

[103] H. Wang, C. Wang, C.-L. Chen, L. Xie, F-LOAM : Fast LiDAR odometry and
mapping, in: 2021 IEEE/RSJ International Conference on Intelligent Robots and
Systems, IROS, 2021, pp. 4390–4396.

[104] T. Shan, B. Englot, D. Meyers, W. Wang, C. Ratti, D. Rus, Lio-sam: Tightly-
coupled lidar inertial odometry via smoothing and mapping, in: 2020 IEEE/RSJ
International Conference on Intelligent Robots and Systems, IROS, IEEE, pp.
5135–5142.

[105] Z. Wang, Y. Wu, Q. Niu, Multi-sensor fusion in automated driving: A survey,

IEEE Access 8 (2020) 2847–2868.

[106] D.J. Yeong, G. Velasco-Hernandez, J. Barry, J. Walsh, Sensor and sensor fusion

technology in autonomous vehicles: A review, Sensors 21 (6) (2021) 2140.

InformationFusion95(2023)62–9085Y. Zhuang et al.

[107] C. Laoudias, A. Moreira, S. Kim, S. Lee, L. Wirola, C. Fischione, A survey of
enabling technologies for network localization, tracking, and navigation, IEEE
Commun. Surv. Tutor. 20 (4) (2018) 3607–3644.

[136] Y. Geng, R. Martins, J. Sousa, Accuracy analysis of DVL/IMU/magnetometer
integrated navigation system using different IMUs in AUV, in: IEEE ICCA 2010,
2010, pp. 516–521.

[108] K. Shamaei, Z.M. Kassas, Receiver design and time of arrival estimation for
opportunistic localization with 5G signals, IEEE Trans. Wireless Commun. 20
(7) (2021) 4716–4731.

[109] A. Decurninge, L.G. Ordóñez, P. Ferrand, H. Gaoning, L. Bojie, Z. Wei, M.
Guillaud, CSI-based outdoor localization for massive MIMO: Experiments with
a learning approach,
in: 2018 15th International Symposium on Wireless
Communication Systems, ISWCS, 2018, pp. 1–6.

[110] R. Faragher, R. Harle, Location fingerprinting with bluetooth low energy

beacons, IEEE J. Sel. Areas Commun. 33 (11) (2015) 2418–2428.

[111] R. Chen, Z. Li, F. Ye, G. Guo, S. Xu, L. Qian, Z. Liu, L. Huang, Precise indoor
positioning based on acoustic ranging in smartphone, IEEE Trans. Instrum.
Meas. 70 (2021) 1–12.

[112] H. Zhao, Z. Wang, Motion measurement using inertial sensors, ultrasonic
sensors, and magnetometers with extended kalman filter for data fusion, IEEE
Sens. J. 12 (5) (2012) 943–953.

[113] H. Yang, R. Zhang, J. Bordoy, F. Höflinger, W. Li, C. Schindelhauer, L. Reindl,
Smartphone-based indoor localization system using inertial sensor and acoustic
transmitter/receiver, IEEE Sens. J. 16 (22) (2016) 8051–8061.

[114] L. Wu, H. Wang, H. Chai, L. Zhang, H. Hsu, Y. Wang, Performance evaluation

and analysis for gravity matching aided navigation, Sensors 17 (4) (2017).

[115] H. Leppäkoski, J. Collin, J. Takala, Pedestrian navigation based on inertial
sensors, indoor map, and WLAN signals, J. Signal Process. Syst. 71 (3) (2013)
287–296.

[116] C. Yu, H. Lan, F. Gu, F. Yu, N. El-Sheimy, A map/INS/Wi-Fi integrated system

for indoor location-based service applications, Sensors 17 (6) (2017) 1272.

[117] Y. Cui, S.S. Ge, Autonomous vehicle positioning with GPS in urban canyon

environments, IEEE Trans. Robot. Autom. 19 (1) (2003) 15–25.

[118] S. Gao, Y. Zhong, X. Zhang, B. Shirinzadeh, Multi-sensor optimal data fusion
for INS/GPS/SAR integrated navigation system, Aerosp. Sci. Technol. 13 (4)
(2009) 232–237.

[119] R. Harle, A survey of indoor inertial positioning systems for pedestrians, IEEE

Commun. Surv. Tutor. 15 (3) (2013) 1281–1293.

[120] X. Guo, W. Shao, F. Zhao, Q. Wang, D. Li, H. Luo, WiMag: Multimode fusion
localization system based on Magnetic/WiFi/PDR, in: Indoor Positioning and
Indoor Navigation (IPIN), 2016 International Conference on, IEEE, 2016, pp.
1–8.

[121] Z.-g. Wu, Z.-l. Deng, L. Wen, Simulation of fusion localization based on a single
WiFi AP and PDR, DEStech Trans. Comput. Sci. Eng. (Mmsta) (2017).
[122] N. Yu, X. Zhan, S. Zhao, Y. Wu, R. Feng, A precise dead reckoning algorithm
based on bluetooth and multiple sensors, IEEE Internet Things J. 5 (1) (2018)
336–351.

[123] Z. Zuo, L. Liu, L. Zhang, Y. Fang, Indoor positioning based on bluetooth
low-energy beacons adopting graph optimization, Sensors (Basel) 18 (11)
(2018).

[124] X. Wang, Y. Zhuang, Z. Zhang, X. Cao, F. Qin, X. Yang, X. Sun, M. Shi, Z.
Wang, Tightly-coupled integration of pedestrian dead reckoning and bluetooth
based on filter and optimizer, IEEE Internet Things J. (2022) 1.

[125] F. Zampella, F. Seco, Robust indoor positioning fusing PDR and RF technologies:
The RFID and UWB case, in: Indoor Positioning and Indoor Navigation (IPIN),
2013 International Conference on, IEEE, 2013, pp. 1–10.

[126] P. Chen, Y. Kuang, X. Chen, A UWB/improved PDR integration algorithm
applied to dynamic indoor positioning for pedestrians, Sensors 17 (9) (2017)
2065.

[127] D. Dusha, L. Mejias, Error analysis and attitude observability of a monocular
GPS/visual odometry integrated navigation filter, Int. J. Robot. Res. 31 (6)
(2012) 714–737.

[128] P. Zhang, Y. Xu, R. Chen, W. Dong, Y. Li, R. Yu, M. Dong, Z. Liu, Y. Zhuang,
J. Kuang, A multimagnetometer array and inner IMU-based capsule endoscope
positioning system, IEEE Internet Things J. 9 (21) (2022) 21194–21203.
[129] J. Kunhoth, A. Karkar, S. Al-Maadeed, A. Al-Attiyah, Comparative analysis of
computer-vision and BLE technology based indoor navigation systems for people
with visual impairments, Int. J. Health Geogr. 18 (1) (2019) 29.

[130] J. Dong, M. Noreikis, Y. Xiao, A. Ylä-Jääski, ViNav: A vision-based indoor
navigation system for smartphones, IEEE Trans. Mob. Comput. 18 (6) (2019)
1461–1475.

[131] A. Benini, A. Mancini, S. Longhi, An imu/uwb/vision-based extended kalman
filter for mini-uav localization in indoor environment using 802.15.4a wireless
sensor network, J. Intell. Robot. Syst. 70 (1–4) (2013) 461–476.

[132] X. Ning, M. Gui, Y. Xu, X. Bai, J. Fang, INS/VNS/CNS integrated navigation
method for planetary rovers, Aerosp. Sci. Technol. 48 (2016) 102–114.
[133] T.B. Karamat, R.G. Lins, S.N. Givigi, A. Noureldin, Novel EKF-based vi-
sion/inertial system integration for improved navigation, IEEE Trans. Instrum.
Meas. 67 (1) (2018) 116–125.

[134] Y. Meng, W. Wang, H. Han, M. Zhang, A vision/radar/INS integrated guidance
Ind. Electron. 66 (11) (2019)

IEEE Trans.

method for shipboard landing,
8803–8810.

[135] C. Zhang, C. Guo, D. Zhang, Ship navigation via GPS/IMU/LOG integration
using adaptive fission particle filter, Ocean Eng. 156 (2018) 435–445.

[137] D. Wang, X. Xu, Y. Yao, T. Zhang, Virtual DVL reconstruction method for
an integrated navigation system based on DS-LSSVM algorithm, IEEE Trans.
Instrum. Meas. 70 (2021) 1–13.

[138] Y. Zhuang, H. Lan, Y. Li, N. El-Sheimy, PDR/INS/WiFi integration based on
handheld devices for indoor pedestrian navigation, Micromachines 6 (6) (2015)
793.

[139] L. Kanaris, A. Kokkinis, A. Liotta, S. Stavrou, Fusing bluetooth beacon data with
Wi-Fi radiomaps for improved indoor localization, Sensors 17 (4) (2017) 812.
[140] H.-K. Su, Z.-X. Lıao, C.-H. Lin, T.-M. Lin, A hybrid indoor-position mechanism
based on bluetooth and WiFi communications for smart mobile devices, in: 2015
International Symposium on Bioelectronics and Bioinformatics, ISBB, IEEE,
2015, pp. 188–191.

[141] Z. Xiong, F. Sottile, M.A. Spirito, R. Garello, Hybrid indoor positioning ap-
proaches based on WSN and RFID, in: New Technologies, Mobility and Security
(NTMS), 2011 4th IFIP International Conference on, IEEE, 2011, pp. 1–5.

[142] L. Bai, C. Sun, A.G. Dempster, H. Zhao, J.W. Cheong, W. Feng, GNSS-5G
hybrid positioning based on multi-rate measurements fusion and proactive
measurement uncertainty prediction, IEEE Trans. Instrum. Meas. 71 (2022)
1–15.

[143] F. Li, R. Tu, J. Hong, S. Zhang, P. Zhang, X. Lu, Combined positioning
algorithm based on BeiDou navigation satellite system and raw 5G observations,
Measurement 190 (2022) (2000) 110763.

[144] J. Liu, B. Cai, J. Wang, Cooperative localization of connected vehicles: Inte-
grating GNSS with DSRC using a robust Cubature Kalman filter, IEEE Trans.
Intell. Transp. Syst. 18 (8) (2017) 2111–2125.

[145] G.M. Hoangt, B. Denis, J. Häirri, D. Slock, Cooperative localization in VANETs:
An experimental proof-of-concept combining GPS, IR-UWB ranging and V2V
communications,
in: 2018 15th Workshop on Positioning, Navigation and
Communications, WPNC, 2018, pp. 1–6.

[146] Z. Wei, S. Ma, Z. Hua, H. Jia, Z. Zhao, Train integrated positioning method
based on GPS/ins/RFID, in: 2016 35th Chinese Control Conference, CCC, IEEE,
2016, pp. 5858–5862.

[147] J. Georgy, A. Noureldin, C. Goodall, Vehicle navigator using a mixture particle
IEEE Trans.

filter for inertial sensors/odometer/map data/GPS integration,
Consum. Electron. 58 (2) (2012) 544–552.

[148] Y. Hao, Z. Zhang, Q. Xia, Research on data fusion for SINS/GPS/magnetometer
integrated navigation based on modified CDKF, in: Progress in Informatics and
Computing (PIC), 2010 IEEE International Conference on, Vol. 2, IEEE, 2010,
pp. 1215–1219.

[149] M. Langer, S. Kiesel, C. Ascher, G.F. Trommer, Deeply coupled GPS/INS
integration in pedestrian navigation systems in weak signal conditions, in: 2012
International Conference on Indoor Positioning and Indoor Navigation, IPIN,
2012, pp. 1–7.

[150] S. Zihajehzadeh, P.K. Yoon, B. Kang, E.J. Park, UWB-aided inertial motion
capture for lower body 3-D dynamic activity and trajectory tracking, IEEE
Trans. Instrum. Meas. 64 (12) (2015) 3577–3587.

[151] J.A. Herrera, A. Hinkenjann, P. Ploger, J. Maiero, Robust indoor localization
using optimal fusion filter for sensors and map layout information, in: Indoor
Positioning and Indoor Navigation (IPIN), 2013 International Conference on,
IEEE, 2013, pp. 1–8.

[152] M.I. Khan, J. Syrjarinne, Investigating effective methods for integration of
building’s map with low cost inertial sensors and wifi-based positioning, in:
Indoor Positioning and Indoor Navigation (IPIN), 2013 International Conference
on, IEEE, 2013, pp. 1–8.

[153] Y. Li, Y. Zhuang, H. Lan, Q. Zhou, X. Niu, N. El-Sheimy, A hybrid WiFi/magnetic
matching/PDR approach for indoor navigation with smartphone sensors, IEEE
Commun. Lett. 20 (1) (2016) 169–172.

[154] Y. Li, Z. He, Z. Gao, Y. Zhuang, C. Shi, N. El-Sheimy, Toward robust
crowdsourcing-based localization: A fingerprinting accuracy indicator enhanced
wireless/magnetic/inertial integration approach, IEEE Internet Things J. 6 (2)
(2019) 3585–3600.

[155] Z. Luo, W. Zhang, G. Zhou, Improved spring model-based collaborative indoor

visible light positioning, Opt. Rev. 23 (3) (2016) 479–486.

[156] R.E. Kalman, Contributions to the theory of optimal control, Bol. Soc. Mat.

Mexicana 5 (2) (1960) 102–119.

[157] X. Chen, C. Shen, W.-b. Zhang, M. Tomizuka, Y. Xu, K. Chiu, Novel hybrid of
strong tracking Kalman filter and wavelet neural network for GPS/INS during
GPS outages, Measurement 46 (10) (2013) 3847–3854.

[158] Q. Fan, B. Sun, Y. Sun, X. Zhuang, Performance enhancement of MEMS-based
INS/UWB integration for indoor navigation applications, IEEE Sens. J. (99)
(2017) 1.

[159] F. Qigao, S. Biwen, W. Yaheng, Tightly coupled model for indoor positioning
based on uwb/ins, Int. J. Comput. Sci. Issues (IJCSI) 12 (4) (2015) 11.
[160] L. Zwirello, X. Li, T. Zwick, C. Ascher, S. Werling, G.F. Trommer, Sensor data
fusion in UWB-supported inertial navigation systems for indoor navigation, in:
Robotics and Automation (ICRA), 2013 IEEE International Conference on, IEEE,
2013, pp. 3154–3159.

InformationFusion95(2023)62–9086Y. Zhuang et al.

[161] G. Falco, M.C.-C. Gutiérrez, E. Serna, F. Zacchello, S. Bories, Low-cost real-time
tightly-coupled GNSS/INS navigation system based on carrier-phase double-
differences for UAV applications,
in: Proceedings of the 27th International
Technical Meeting of the Satellite Division of the Institute of Navigation (ION
GNSS 2014), Tampa, FL, USA, Vol. 812, 2014, 841857.

[162] J. Fang, X. Gong, Predictive iterated Kalman filter for INS/GPS integration and
its application to SAR motion compensation, IEEE Trans. Instrum. Meas. 59 (4)
(2010) 909–915.

[163] K.H. Kim, J.G. Lee, C.G. Park, Adaptive two-stage extended Kalman filter for
a fault-tolerant INS-GPS loosely coupled system, IEEE Trans. Aerosp. Electron.
Syst. 45 (1) (2009) 125–137.

[164] S. Zahran, A. Moussa, N. El-Sheimy, Enhanced UAV navigation in GNSS
denied environment using repeated dynamics pattern recognition, in: Position,
Location and Navigation Symposium (PLANS), 2018 IEEE/ION, IEEE, 2018, pp.
1135–1142.

[165] Y. Xu, X. Chen, Q. Li, Adaptive iterated extended kalman filter and its
application to autonomous integrated navigation for indoor robot, Sci. World
J. 2014 (2014).

[166] Z. Zeng, S. Liu, W. Wang, L. Wang,

Infrastructure-free indoor pedestrian
tracking based on foot mounted UWB/IMU sensor fusion, in: Signal Processing
and Communication Systems (ICSPCS), 2017 11th International Conference on,
IEEE, 2017, pp. 1–7.

[167] Y. Xu, X. Chen, J. Cheng, Q. Zhao, Y. Wang,

Improving tightly-coupled
model for indoor pedestrian navigation using foot-mounted IMU and UWB
measurements, in: Instrumentation and Measurement Technology Conference
Proceedings (I2MTC), 2016 IEEE International, IEEE, 2016, pp. 1–5.

[168] N. Ganganath, H. Leung, Mobile robot

localization using odometry and
kinect sensor, in: Emerging Signal Processing Applications (ESPA), 2012 IEEE
International Conference on, IEEE, 2012, pp. 91–94.

[169] P. Aggarwal, MEMS-Based Integrated Navigation, Artech House, 2010.
[170] D.-J. Jwo, C.-F. Yang, C.-H. Chuang, T.-Y. Lee, Performance enhancement for
ultra-tight GPS/INS integration using a fuzzy adaptive strong tracking unscented
Kalman filter, Nonlinear Dynam. 73 (1–2) (2013) 377–395.

[171] X. Yuan, S. Yu, S. Zhang, G. Wang, S. Liu, Quaternion-based unscented kalman
filter for accurate indoor heading estimation using wearable multi-sensor
system, Sensors 15 (5) (2015) 10872–10890.

[172] Z. Jiang, C. Liu, G. Zhang, Y. Wang, C. Huang, J. Liang, GPS/INS integrated
navigation based on UKF and simulated annealing optimized SVM, in: Vehicular
Technology Conference (VTC Fall), 2013 IEEE 78th, IEEE, 2013, pp. 1–5.

[173] M. Rhudy, Y. Gu, J. Gross, M.R. Napolitano, Evaluation of matrix square root
operations for UKF within a UAV GPS/INS sensor fusion application, Int. J.
Navig. Obs. 2011 (2011).

[174] Q. Wang, Y. Li, C. Rizos, S. Li, The UKF and CDKF for low-cost SDINS/GPS
in-motion alignment, in: Proceedings of International Symposium on GPS/GNSS,
2008, pp. 441–448.

[175] Q. Zou, W. Xia, Y. Zhu, J. Zhang, B. Huang, F. Yan, L. Shen, A VLC and
IMU integration indoor positioning algorithm with weighted unscented Kalman
filter, in: Computer and Communications (ICCC), 2017 3rd IEEE International
Conference on, IEEE, 2017, pp. 887–891.

[176] D. Feng, C. Wang, C. He, Y. Zhuang, X.-G. Xia, Kalman-filter-based integration
of IMU and UWB for high-accuracy indoor positioning and navigation, IEEE
Internet Things J. 7 (4) (2020) 3133–3146.

[177] J. Kong, X. Mao, S. Li, BDS/GPS dual systems positioning based on the modified

SR-UKF algorithm, Sensors 16 (5) (2016) 635.

[178] L.-H. Ma, Z.-B. Feng, B. Ying, Z.-Y. Wang, Application of fixed matrix square
root UKF in the ultra-tightly coupled integrated GPS/SINS navigation system,
ICIC Express Lett. B 6 (1) (2015) 175–180.

[179] L.A. Sandino, M. Bejar, K. Kondak, A. Ollero, Multi-sensor data fusion for
a tethered unmanned helicopter using a square-root unscented Kalman filter,
Unmanned Syst. 4 (04) (2016) 273–287.

[180] J. Liu, J. Ma, J. Tian, Pulsar/CNS integrated navigation based on federated

UKF, J. Syst. Eng. Electron. 21 (4) (2010) 675–681.

[181] Q. Xu, X. Li, C.-Y. Chan, A cost-effective vehicle localization solution using an
interacting multiple model- unscented Kalman filters (IMM-UKF) algorithm and
grey neural network, Sensors 17 (6) (2017) 1431.

[182] S.Y. Cho, IM-filter for INS/GPS-integrated navigation system containing low-cost

gyros, IEEE Trans. Aerosp. Electron. Syst. 50 (4) (2014) 2619–2629.

[183] G. Chang, Loosely coupled INS/GPS integration with constant lever arm using

marginal unscented Kalman filter, J. Navig. 67 (3) (2014) 419–436.

[184] M. Enkhtur, S.Y. Cho, K. Kim, Modified unscented Kalman filter for a multirate
INS/GPS integrated navigation system, Etri J. 35 (5) (2013) 943–946.
[185] G. Hu, S. Gao, Y. Zhong, A derivative UKF for tightly coupled INS/GPS

integrated navigation, ISA Trans. 56 (2015) 135–144.

[188] M.S. Arulampalam, S. Maskell, N. Gordon, T. Clapp, A tutorial on particle
filters for online nonlinear/non-Gaussian Bayesian tracking, IEEE Trans. Signal
Process. 50 (2) (2002) 174–188.

[189] O. Woodman, R. Harle, Pedestrian localisation for indoor environments, in:
Proceedings of the 10th International Conference on Ubiquitous Computing,
ACM, 2008, pp. 114–123.

[190] Z. Wu, E. Jedari, R. Muscedere, R. Rashidzadeh, Improved particle filter based
on WLAN RSSI fingerprinting and smart sensors for indoor localization, Comput.
Commun. 83 (2016) 64–71.

[191] P. Aggarwal, Z. Syed, N. El-Sheimy, Hybrid extended particle filter (HEPF)
for integrated civilian navigation system, in: Position, Location and Navigation
Symposium, 2008 IEEE/ION, IEEE, 2008, pp. 984–992.

[192] S. Zhao, Y. Chen, J.A. Farrell, High-precision vehicle navigation in urban
environments using an MEM’s IMU and single-frequency GPS receiver, IEEE
Trans. Intell. Transp. Syst. 17 (10) (2016) 2854–2867.

[193] W. Wen, X. Bai, Y.C. Kan, L. Hsu, Tightly coupled GNSS/INS integration via
factor graph and aided by fish-eye camera, IEEE Trans. Veh. Technol. 68 (11)
(2019) 10651–10662.

[194] X. Li, X. Wang, J. Liao, X. Li, S. Li, H. Lyu, Semi-tightly coupled integration
of multi-GNSS PPP and S-VINS for precise positioning in GNSS-challenged
environments, Satell. Navig. 2 (1) (2021) 1.

[195] X. Niu, H. Tang, T. Zhang, J. Fan, J. Liu, IC-GVINS: A robust, real-time, INS-
centric GNSS-visual-inertial navigation system, IEEE Robot. Autom. Lett. 8 (1)
(2023) 216–223.

[196] S. Cao, X. Lu, S. Shen, GVINS: Tightly coupled GNSS–Visual–Inertial fusion
for smooth and consistent state estimation, IEEE Trans. Robot. 38 (4) (2022)
2004–2021.

[197] C. Qin, X. Zhan, VLIP: Tightly coupled visible-light/inertial positioning system
to cope with intermittent outage, IEEE Photonics Technol. Lett. 31 (2) (2018)
129–132.

[198] Q. Meng, Y. Song, S. ying Li, Y. Zhuang, Resilient tightly coupled INS/UWB
integration method for indoor UAV navigation under challenging scenarios, Def.
Technol. (2022).

[199] S. Agarwal, K. Mierle, T.C.S. Team, Ceres solver, 2022.
[200] H. Yu, B.M. Wilamowski, Levenberg–Marquardt Training, CRC Press, 2018,

12–1–12–16.

[201] H. Liu, S. Nassar, N. El-Sheimy, Two-filter smoothing for accurate INS/GPS land-
vehicle navigation in urban centers, IEEE Trans. Veh. Technol. 59 (9) (2010)
4256–4267.

[202] S. Li, Y. Peng, Y. Lu, L. Zhang, Y. Liu, MCAV/IMU integrated navigation for the
powered descent phase of Mars EDL, Adv. Space Res. 46 (5) (2010) 557–570.
[203] S. Li, Y. Peng, Radio beacons/IMU integrated navigation for Mars entry, Adv.

Space Res. 47 (7) (2011) 1265–1279.

[204] S. Zihajehzadeh, P.K. Yoon, E.J. Park, A magnetometer-free indoor human
localization based on loosely coupled IMU/UWB fusion, in: 2015 37th Annual
International Conference of the IEEE Engineering in Medicine and Biology
Society, EMBC, 2015, pp. 3141–3144.

[205] F. Evennou, F. Marx, Advanced integration of WiFi and inertial navigation
systems for indoor mobile positioning, Eurasip J. Appl. Signal Process. 2006
(2006) 164.

[206] T. Iwase, R. Shibasaki, Infra-free indoor positioning using only smartphone sen-
sors, in: International Conference on Indoor Positioning and Indoor Navigation,
2013, pp. 1–8.

[207] W.W. Li, R.A. Iltis, M.Z. Win, A smartphone localization algorithm using RSSI
and inertial sensor measurement fusion, in: 2013 IEEE Global Communications
Conference, GLOBECOM, 2013, pp. 3335–3340.

[208] U. Schatzberg, L. Banin, Y. Amizur, Enhanced WiFi ToF indoor positioning
system with MEMS-based INS and pedometric information, in: Position, Lo-
cation and Navigation Symposium-PLANS 2014, 2014 IEEE/ION, IEEE, 2014,
pp. 185–192.

[209] W. Xiao, W. Ni, Y.K. Toh, Integrated Wi-Fi fingerprinting and inertial sensing
for indoor positioning, in: 2011 International Conference on Indoor Positioning
and Indoor Navigation, 2011, pp. 1–6.

[210] Y. Zhuang, Y. Li, L. Qi, H. Lan, J. Yang, N. El-Sheimy, A two-filter integration
of MEMS sensors and WiFi fingerprinting for indoor positioning, IEEE Sens. J.
16 (13) (2016) 5125–5126.

[211] J. Zhou, X. Nie, J. Lin, A novel laser Doppler velocimeter and its integrated
navigation system with strapdown inertial navigation, Opt. Laser Technol. 64
(2014) 319–323.

[212] S. Huh, D.H. Shim, J. Kim, Integrated navigation system using camera and
gimbaled laser scanner for indoor and outdoor autonomous flight of UAVs,
in: 2013 IEEE/RSJ International Conference on Intelligent Robots and Systems,
2013, pp. 3158–3163.

[186] Ngatini, E. Apriliani, H. Nurhadi, Ensemble and fuzzy Kalman filter for position
estimation of an autonomous underwater vehicle based on dynamical system
of AUV motion, Expert Syst. Appl. 68 (2017) 29–35.

[213] S. Godha, Performance Evaluation of Low Cost MEMS-Based IMU Integration
with GPS for Land Vehicle Navigation Application (Thesis), University of
Calgary, 2006.

[187] X. Lin, H. Sun, Y. Wang, Dynamic positioning particle filtering method based on
the EnKF, in: Mechatronics and Automation (ICMA), 2017 IEEE International
Conference on, IEEE, 2017, pp. 1871–1876.

[214] G. Falco, M. Pini, G. Marucco, Loose and tight GNSS/INS integrations: Com-
parison of performance assessed in real urban scenarios, Sensors 17 (2) (2017)
255.

InformationFusion95(2023)62–9087Y. Zhuang et al.

[215] M. George, S. Sukkarieh, Tightly coupled INS/GPS with bias estimation for
UAV applications, in: Proceedings of Australiasian Conference on Robotics and
Automation, ACRA, 2005.

[216] M.G. Petovello, Real-Time Integration of a Tactical-Grade IMU and GPS for
High-Accuracy Positioning and Navigation (Thesis), University of Calgary, 2003.
[217] T. Li, H. Zhang, Z. Gao, Q. Chen, X. Niu, High-accuracy positioning in urban
environments using single-frequency multi-GNSS RTK/MEMS-IMU integration,
Remote Sens. 10 (2) (2018) 205.

[244] X. Song, X. Li, W. Tang, W. Zhang, A fusion strategy for reliable vehicle
positioning utilizing RFID and in-vehicle sensors, Inf. Fusion 31 (2016) 76–86.
[245] Y. Yuan, X. Sun, Z. Liu, Y. Li, X. Guan, Approach of personnel location in
roadway environment based on multi-sensor fusion and activity classification,
Comput. Netw. 148 (2019) 34–45.

[246] L. Cong, J. Tian, H. Qin, A practical floor localization algorithm based on
multifeature motion mode recognition utilizing FM radio signals and inertial
sensors, IEEE Sens. J. 20 (15) (2020) 8806–8819.

[218] J.D. Hol, F. Dijkstra, H. Luinge, T.B. Schon, Tightly coupled UWB/IMU pose
estimation, in: 2009 IEEE International Conference on Ultra-Wideband, 2009,
pp. 688–692.

[247] G. Zhang, L.-T. Hsu, Intelligent GNSS/INS integrated navigation system for
a commercial UAV flight control system, Aerosp. Sci. Technol. 80 (2018)
368–380.

[219] P. Cui, S. Wang, A. Gao, Z. Yu, X-ray pulsars/Doppler integrated navigation for

mars final approach, Adv. Space Res. 57 (9) (2016) 1889–1900.

[220] D.B. Hwang, D.W. Lim, S.L. Cho, S.J. Lee, Unified approach to ultra-tightly-
coupled GPS/INS integrated navigation system, IEEE Aerosp. Electron. Syst.
Mag. 26 (3) (2011) 30–38.

[221] J.W. Kim, D.-H. Hwang, S.J. Lee, A deeply coupled GPS/INS integrated Kalman
filter design using a linearized correlator output, in: 2006 IEEE/ION Position,
Location, and Navigation Symposium, IEEE, 2006, pp. 300–305.

[222] M. Lashley, D.M. Bevly, J.Y. Hung, A valid comparison of vector and scalar
tracking loops, in: IEEE/ION Position, Location and Navigation Symposium,
2010, pp. 464–474.

[223] E. Amani, Scalar and Vector Tracking Algorithms with Fault Detection and
Exclusion for GNSS Receivers: Design and Performance Evaluation (Thesis),
Paris Est, 2017.

[224] J. Dou, B. Xu, L. Dou, Performance assessment of GNSS scalar and vector

frequency tracking loops, Optik 202 (2020) 163552.

[225] M. Wu, J. Ding, Z. Luo, L. Zhao, The coherent vector tracking loop design
with FDE algorithm for BDS signals,
in: 2016 IEEE Advanced Information
Management, Communicates, Electronic and Automation Control Conference,
IMCEC, 2016, pp. 835–840.

[226] M. Petovello, C. O’Driscoll, G. Lachapelle, Weak signal carrier tracking using
extended coherent integration with an ultra-tight GNSS/IMU receiver, in: Proc.
ENC-GNSS 2008, 2008.

[227] J.D. Gautier, GPS/INS Generalized Evaluation Tool (GIGET) for the Design and

Testing of Integrated Navigation Systems, Stanford University, 2003.

[228] J. Liu, X. Cui, M. Lu, Z. Feng, Vector tracking loops in GNSS receivers for
dynamic weak signals, J. Syst. Eng. Electron. 24 (3) (2013) 349–364.
[229] C. Jiang, S. Chen, Y. Chen, Y. Bo, Research on a chip scale atomic clock driven
GNSS/SINS deeply coupled navigation system for augmented performance, IET
Radar Sonar Navig. 13 (2) (2019) 326–331.

[230] Z. He, X. Wang, J. Fang, An innovative high-precision SINS/CNS deep integrated
navigation scheme for the mars rover, Aerosp. Sci. Technol. 39 (2014) 559–566.
[231] W. Xiaojuan, W. Xinlong, A SINS/CNS deep integrated navigation method based
on mathematical horizon reference, Aircr. Eng. Aerosp. Technol. 83 (1) (2011)
26–34.

[232] A.G. Quinchia, G. Falco, E. Falletti, F. Dovis, C. Ferrer, A comparison between
different error modeling of MEMS applied to GPS/INS integrated systems,
Sensors 13 (8) (2013) 9549–9588.

[233] R. Sharaf, A. Noureldin, A. Osman, N. El-Sheimy, Online INS/GPS integration
with a radial basis function neural network, IEEE Aerosp. Electron. Syst. Mag.
20 (3) (2005) 8–14.

[234] D. Li, X. Jia, J. Zhao, A novel hybrid fusion algorithm for low-cost GPS/INS
IEEE Access 8 (2020)

integrated navigation system during GPS outages,
53984–53996.

[235] C.E. Magrin, E. Todt, Multi-sensor fusion method based on artificial neural
network for mobile robot self-localization, in: 2019 Latin American Robotics
Symposium (LARS), 2019 Brazilian Symposium on Robotics (SBR) and 2019
Workshop on Robotics in Education, WRE, pp. 138–143.

[236] A.M.M. Almassri, N. Shirasawa, A. Purev, K. Uehara, W. Oshiumi, S. Mishima,
H. Wagatsuma, Artificial neural network approach to guarantee the positioning
accuracy of moving robots by using the integration of IMU/UWB with motion
capture system data fusion, Sensors 22 (15) (2022).

[237] Z. Xu, Y. Li, C. Rizos, X. Xu, Novel hybrid of LS-SVM and Kalman filter for

GPS/INS integration, J. Navig. 63 (2) (2010) 289–299.

[238] J. Ali, Strapdown inertial navigation system/astronavigation system data syn-
thesis using innovation-based fuzzy adaptive Kalman filtering, IET Sci. Meas.
Technol. 4 (5) (2010) 246–255.

[239] C.-H. Tseng, S.-F. Lin, D.-J. Jwo, Fuzzy adaptive cubature Kalman filter for

integrated navigation systems, Sensors 16 (8) (2016) 1167.

[240] P.J. Escamilla-Ambrosio, N. Mort, Multi-sensor data fusion architecture based on
adaptive Kalman filters and fuzzy logic performance assessment, in: Information
Fusion, 2002. Proceedings of the Fifth International Conference on, Vol. 2, IEEE,
2002, pp. 1542–1549.

[241] N. Musavi, J. Keighobadi, Adaptive fuzzy neuro-observer applied to low cost

INS/GPS, Appl. Soft Comput. 29 (2015) 82–94.

[242] N. Shaukat, M. Moinuddin, P. Otero, Underwater vehicle positioning by

correntropy-based fuzzy multi-sensor fusion, Sensors 21 (18) (2021).

[243] H. Gao, X. Li, Tightly-Coupled Vehicle Positioning Method at Intersections

Aided by UWB, Sensors 19 (13) (2019).

[248] S. Adusumilli, D. Bhatt, H. Wang, P. Bhattacharya, V. Devabhaktuni, A low-cost
INS/GPS integration methodology based on random forest regression, Expert
Syst. Appl. 40 (11) (2013) 4653–4659.

[249] S. Adusumilli, D. Bhatt, H. Wang, V. Devabhaktuni, P. Bhattacharya, A novel
hybrid approach utilizing principal component regression and random forest
regression to bridge the period of GPS outages, Neurocomputing 166 (2015)
185–192.

[250] C. Rui, K-means aided Kalman filter noise estimation calibration for integrated
in: 2016 IEEE International Conference on Intelligent

GPS/INS navigation,
Transportation Engineering, ICITE, 2016, pp. 156–161.

[251] Y. Li, S.S. Gao, Y. Yang, A novel adaptive UKF and its application in the

SINS/GPS integrated navigation, Appl. Mech. Mater. 597 (2014) 521–524.

[252] D. Huang, H. Leung, E.-S. N, Expectation maximization based GPS/INS inte-
gration for land-vehicle navigation, IEEE Trans. Aerosp. Electron. Syst. 43 (3)
(2007) 1168–1177.

[253] M.N.U. Laskar, M.N.A. Tawhid, T. Chung, Extended Kalman Filter (EKF) and K-
means clustering approach for state space decomposition of autonomous mobile
robots,
in: 2012 7th International Conference on Electrical and Computer
Engineering, IEEE, 2012, pp. 113–116.

[254] G. Liu, H. Zhu, EM-FKF approach to an integrated navigation system, J. Aerosp.

Eng. 27 (3) (2014) 621–630.

[255] Y. Chen, W. Li, Y. Wang, A robust adaptive indirect in-motion coarse alignment
method for GPS/SINS integrated navigation system, Measurement 172 (2021)
108834.

[256] D. Grejner-Brzezinska, C. Toth, S. Moafipoor, J. Kwon, Design and calibration
of a neural network-based adaptive knowledge system for multi-sensor personal
navigation, in: Proceedings of the 5 Th International Symposium on Mobil
Mapping Technology MMT’07, 2007.

[257] P. Narmatha, V. Thangavel, D.S. Vidhya, A hybrid RF and vision aware fusion
scheme for multi-sensor wireless capsule endoscopic localization, Wirel. Pers.
Commun. (2021).

[258] M. Turan, J. Shabbir, H. Araujo, E. Konukoglu, M. Sitti, A deep learning based
fusion of RGB camera information and magnetic localization information for
endoscopic capsule robots, Int. J. Intell. Robot. Appl. 1 (4) (2017) 442–450.

[259] C. Li, S. Wang, Y. Zhuang, F. Yan, Deep sensor fusion between 2D laser scanner
and IMU for mobile robot localization, IEEE Sens. J. 21 (6) (2021) 8501–8509.
[260] Q. Wang, H. Luo, H. Xiong, A. Men, F. Zhao, M. Xia, C. Ou, Pedestrian dead
reckoning based on walking pattern recognition and online magnetic fingerprint
trajectory calibration, IEEE Internet Things J. (2020).

[261] C. Chen, S. Rosa, Y. Miao, C.X. Lu, W. Wu, A. Markham, N. Trigoni,
Selective sensor fusion for neural visual-inertial odometry, in: Proceedings of
the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2019,
pp. 10542–10551.

[262] R. Clark, S. Wang, H. Wen, A. Markham, N. Trigoni, Vinet: Visual-inertial
odometry as a sequence-to-sequence learning problem, in: Proceedings of the
AAAI Conference on Artificial Intelligence, Vol. 31, 2017.

[263] Y. Kim, S. Yoon, S. Kim, A. Kim, Unsupervised balanced covariance learning for

visual-inertial sensor fusion, IEEE Robot. Autom. Lett. 6 (2) (2021) 819–826.

[264] C. Chen, P. Zhao, C.X. Lu, W. Wang, A. Markham, N. Trigoni, Deep-learning-
based pedestrian inertial navigation: Methods, data set, and on-device inference,
IEEE Internet Things J. 7 (5) (2020) 4431–4441.

[265] X. Gan, B. Yu, L. Huang, Y. Li, Deep learning for weights training and indoor
positioning using multi-sensor fingerprint, in: 2017 International Conference on
Indoor Positioning and Indoor Navigation, IPIN, IEEE, 2017, pp. 1–7.
[266] A. Belmonte-Hernández, G. Hernández-Peñaloza, D.M. Gutiérrez, F. Álvarez,
SWiBluX: Multi-sensor deep learning fingerprint for precise real-time indoor
tracking, IEEE Sens. J. 19 (9) (2019) 3473–3486.

[267] X. Song, X. Fan, X. He, C. Xiang, Q. Ye, X. Huang, G. Fang, L.L. Chen, J.
Qin, Z. Wang, CNNLoc: Deep-learning based indoor localization with WiFi
fingerprinting, in: 2019 IEEE SmartWorld, Ubiquitous Intelligence & Comput-
ing, Advanced & Trusted Computing, Scalable Computing & Communications,
Cloud & Big Data Computing, Internet of People and Smart City Innovation
(SmartWorld/SCALCOM/UIC/ATC/CBDCom/IOP/SCI), 2019, pp. 589–595.

[268] W.M. Van Buijtenen, G. Schram, R. Babuska, H.B. Verbruggen, Adaptive fuzzy
control of satellite attitude by reinforcement learning, IEEE Trans. Fuzzy Syst.
6 (2) (1998) 185–194.

[269] C. Goodall, N. El-Sheimy, Intelligent tuning of a Kalman filter using low-cost
in: Proceedings of 5th International Symposium on

MEMS inertial sensors,
Mobile Mapping Technology (MMT’07), Padua, Italy, 2007, pp. 1–8.

InformationFusion95(2023)62–9088Y. Zhuang et al.

[270] Y. Li, X. Hu, Y. Zhuang, Z. Gao, P. Zhang, N. El-Sheimy, Deep reinforcement
learning (DRL): Another perspective for unsupervised wireless localization, IEEE
Internet Things J. (2019).

[271] X. Gao, H. Luo, B. Ning, F. Zhao, L. Bao, Y. Gong, Y. Xiao, J. Jiang, RL-AKF: An
Adaptive Kalman Filter Navigation Algorithm Based on Reinforcement Learning
for Ground Vehicles, Remote Sens. 12 (11) (2020).

[272] M. Cao, J. Chen, J. Wang, A novel vehicle tracking method for cross-area sensor
fusion with reinforcement learning based GMM, in: 2020 American Control
Conference, ACC, pp. 442–447.

[273] A. Rangesh, M.M. Trivedi, No blind spots: Full-surround multi-object tracking
for autonomous vehicles using cameras and LiDARs, IEEE Trans. Intell. Veh. 4
(4) (2019) 588–599.

[274] X. Huang, H. Deng, W. Zhang, R. Song, Y. Li, Towards multi-modal perception-
based navigation: A deep reinforcement learning method, IEEE Robot. Autom.
Lett. 6 (3) (2021) 4986–4993.

[275] X. Cao, Y. Zhuang, X. Yang, X. Sun, X. Wang, A universal Wi-Fi fingerprint
localization method based on machine learning and sample differences, Satell.
Navig. 2 (1) (2021) 27.

[276] F.M. Ham, R.G. Brown, Observability, eigenvalues, and Kalman filtering, IEEE

Trans. Aerosp. Electron. Syst. AES-19 (2) (1983) 269–273.

[277] J. Huai, Y. Lin, Y. Zhuang, M. Shi, Consistent right-invariant fixed-lag smoother
with application to visual inertial SLAM, in: Proceedings of the AAAI Conference
on Artificial Intelligence, Vol. 35, 2021, pp. 6084–6092, (7).

[278] Y. Yang, G. Huang, Observability analysis of aided INS with heterogeneous
IEEE Trans. Robot. 35 (6) (2019)

lines, and planes,

features of points,
1399–1418.

[279] J. Huai, Y. Lin, Y. Zhuang, C.K. Toth, D. Chen, Observability analysis and
keyframe-based filtering for visual inertial odometry with full self-calibration,
IEEE Trans. Robot. 38 (5) (2022) 3219–3237.

[280] Y. Zhuang, Q. Wang, M. Shi, P. Cao, L. Qi, J. Yang, Low-cost localization for
indoor mobile robots based on ensemble Kalman smoother using received signal
strength, IEEE Internet Things J. (2019).

[281] S. Nassar, Improving the Inertial Navigation System (INS) Error Model for INS

and INS/DGPS Applications (Thesis), University of Calgary, 2003.

[282] Y. Li, R. Chen, X. Niu, Y. Zhuang, Z. Gao, X. Hu, N. El-Sheimy, Inertial sensing
meets machine learning: Opportunity or challenge? IEEE Trans. Intell. Transp.
Syst. (2021) 1–17.

[283] Y. Zhao, W.C. Wong, T. Feng, H.K. Garg, Efficient and scalable calibration-
free indoor positioning using crowdsourced data, IEEE Internet Things J. 7 (1)
(2020) 160–175.

[284] T. Huck, A. Westenberger, M. Fritzsche, T. Schwarz, K. Dietmayer, Precise
timestamping and temporal synchronization in multi-sensor fusion, in: 2011
IEEE Intelligent Vehicles Symposium, IV, 2011, pp. 242–247.

[285] P. Lei, Z. Li, B. Xue, H. Zhang, X. Zou, Hybsync: Nanosecond wireless position
and clock synchronization based on UWB communication with multisensors, J.
Sensors 2021 (2021) 9920567.

[286] B. Li, C. Rizos, H.K. Lee, H.K. Lee, A GPS-slaved time synchronization system

for hybrid navigation, GPS Solut. 10 (3) (2006) 207–217.

[287] I. Skog, P. Handel, Time synchronization errors in loosely coupled GPS-aided
inertial navigation systems, IEEE Trans. Intell. Transp. Syst. 12 (4) (2011)
1014–1023.

[288] H.K. Lee, J.G. Lee, G.-I. Jee, Calibration of measurement delay in global
positioning system/strapdown inertial navigation system, J. Guid. Control Dyn.
25 (2) (2002) 240–247.

[289] J. Jeong, Y. Cho, Y.-S. Shin, H. Roh, A. Kim, Complex urban dataset with
multi-level sensors from highly diverse urban environments, Int. J. Robot. Res.
38 (6) (2019) 642–657.

[290] Y. Choi, N. Kim, S. Hwang, K. Park, J.S. Yoon, K. An, I.S. Kweon, KAIST multi-
spectral day/night data set for autonomous and assisted driving, IEEE Trans.
Intell. Transp. Syst. 19 (3) (2018) 934–948.

[291] Q. Sun, Y. Zhang, J. Wang, W. Gao, An improved FAST feature extraction
based on RANSAC method of vision/SINS integrated navigation system in
GNSS-denied environments, Adv. Space Res. 60 (12) (2017) 2660–2671.
[292] J.N. Ash, R.L. Moses, Outlier compensation in sensor network self-localization
via the EM algorithm, in: Proceedings.(ICASSP’05). IEEE International Confer-
ence on Acoustics, Speech, and Signal Processing, 2005. Vol. 4, IEEE, 2005, pp.
iv/749–iv/752.

[293] T. Zhang, J. Wang, L. Zhang, L. Guo, A student’s T-based measurement
uncertainty filter for SINS/USBL tightly integration navigation system, IEEE
Trans. Veh. Technol. 70 (9) (2021) 8627–8638.

[294] Y. Hao, A. Xu, X. Sui, Y. Wang, A modified extended Kalman filter for a

two-antenna GPS/INS vehicular navigation system, Sensors 18 (11) (2018).

[298] C. Merfels, C. Stachniss, Sensor fusion for self-localisation of automated vehicles,

PFG – J. Photogramm. Remote Sens. Geoinf. Sci. 85 (2) (2017) 113–126.

[299] J.-P. Tardif, M. George, M. Laverne, A. Kelly, A. Stentz, A new approach to
vision-aided inertial navigation, in: Intelligent Robots and Systems (IROS), 2010
IEEE/RSJ International Conference on, IEEE, 2010, pp. 4161–4168.

[300] M. Moussa, A. Moussa, N. El-Sheimy, Multiple ultrasonic aiding system for car
navigation in GNSS denied environment, in: Position, Location and Navigation
Symposium (PLANS), 2018 IEEE/ION, IEEE, 2018, pp. 133–140.

[301] K. Dierenbach, S. Ostrowski, G. Jozkow, C. Toth, D. Grejner-Brzezinska,
in:
Z. Koppanyi, UWB for navigation in GNSS compromised environments,
Proceedings of the 28th International Technical Meeting of the Satellite Division
of the Institute of Navigation (ION GNSS+ 2015), Tampa, FL, USA, 2015, pp.
14–18.

[302] D. Ruiz, E. García, J. Ureña, D. de Diego, D. Gualda, J.C. García, Extensive
ultrasonic local positioning system for navigating with mobile robots,
in:
Positioning Navigation and Communication (WPNC), 2013 10th Workshop on,
IEEE, 2013, pp. 1–6.

[303] Q. Fan, B. Sun, Y. Sun, Y. Wu, X. Zhuang, Data fusion for indoor mobile
robot positioning based on tightly coupled INS/UWB, J. Navig. 70 (5) (2017)
1079–1097.

[304] J. Biswas, M. Veloso, Wifi localization and navigation for autonomous indoor
mobile robots, in: Robotics and Automation (ICRA), 2010 IEEE International
Conference on, IEEE, 2010, pp. 4379–4384.

[305] Z. Chen, H. Zou, H. Jiang, Q. Zhu, Y.C. Soh, L. Xie, Fusion of WiFi, smartphone
sensors and landmarks using the Kalman filter for indoor localization, Sensors
15 (1) (2015) 715–732.

[306] S.-J. Yu, S.-S. Jan, D.S. De Lorenzo, Indoor navigation using Wi-Fi fingerprinting
combined with pedestrian dead reckoning, in: Position, Location and Navigation
Symposium (PLANS), 2018 IEEE/ION, IEEE, 2018, pp. 246–253.

[307] M. Atia, A. Noureldin,

J. Georgy, M. Korenberg, Bayesian filtering
based WiFi/INS integrated navigation solution for GPS-denied environments,
Navigation 58 (2) (2011) 111–125.

[308] Z. Li, L. Feng, A. Yang, Fusion based on visible light positioning and inertial
navigation using extended Kalman filters, Sensors 17 (5) (2017) 1093.
[309] Z. Li, A. Yang, H. Lv, L. Feng, W. Song, Fusion of visible light indoor positioning
and inertial navigation based on particle filter, IEEE Photonics J. 9 (5) (2017)
1–13.

[310] J. Wang, A. Hu, C. Liu, X. Li, A floor-map-aided WiFi/pseudo-odometry
integration algorithm for an indoor positioning system, Sensors 15 (4) (2015)
7096–7124.

[311] S.-E. Kim, Y. Kim, J. Yoon, E.S. Kim, Indoor positioning system using geomag-
netic anomalies for smartphones, in: Indoor Positioning and Indoor Navigation
(IPIN), 2012 International Conference on, IEEE, 2012, pp. 1–5.

[312] J.L. Crassidis, Sigma-point Kalman filtering for integrated GPS and inertial
navigation, IEEE Trans. Aerosp. Electron. Syst. 42 (2) (2006) 750–756.
[313] B. Cui, X. Chen, X. Tang, Improved cubature Kalman filter for GNSS/INS based
on transformation of posterior sigma-points error, IEEE Trans. Signal Process.
65 (11) (2017) 2975–2987.

[314] X. Gong, T. Qin, Airborne earth observation positioning and orientation by
SINS/GPS integration using CD RTS smoothing, J. Navig. 67 (2) (2014)
211–225.

[315] X. Liu, H. Qu, J. Zhao, P. Yue, Maximum correntropy square-root cubature
Kalman filter with application to SINS/GPS integrated systems, ISA Trans.
(2018).

[316] J. Shen, Y. Su, Q. Liang, X. Zhu, Model aided airborne integrated navigation
system based on an improved square-root unscented H∞ filter, Trans. Inst.
Meas. Control (2018) 1–11.

[317] P. Kaniewski, R. Gil, S. Konatowski, Estimation of UAV position with use of

smoothing algorithms, Metrol. Meas. Syst. 24 (1) (2017) 127–142.

[318] K. Li, C. Wang, S. Huang, G. Liang, X. Wu, Y. Liao, Self-positioning for UAV
indoor navigation based on 3D laser scanner, UWB and INS, in: Information
and Automation (ICIA), 2016 IEEE International Conference on, IEEE, 2016,
pp. 498–503.

[319] Y. Xu, Y.S. Shmaliy, C.K. Ahn, T. Shen, Y. Zhuang, Tightly coupled integration
INS and UWB using fixed-lag extended UFIR smoothing for quadrotor

of
localization, IEEE Internet Things J. 8 (3) (2021) 1716–1727.

[320] C. Chen, X. Wang, W. Qin, N. Cui, Vision-based relative navigation using

cubature huber-based filtering, Aircr. Eng. Aerosp. Technol. (2018).

[321] C. Zhang, C. Guo, D. Zhang, Data fusion based on adaptive interacting multiple
model for GPS/INS integrated navigation system, Appl. Sci. 8 (9) (2018) 1682.
[322] C. Zhang, T. Li, C. Guo, GPS/INS integration based on adaptive interacting

[295] S. Liu, L. Li, J. Tang, S. Wu, J.-L. Gaudiot, Creating autonomous vehicle systems,

multiple model, J. Eng. 2019 (15) (2019) 561–565.

Synth. Lect. Comput. Sci. 6 (1) (2017) i–186.

[296] G. Wan, X. Yang, R. Cai, H. Li, Y. Zhou, H. Wang, S. Song, Robust and precise
vehicle localization based on multi-sensor fusion in diverse city scenes, in:
2018 IEEE International Conference on Robotics and Automation, ICRA, pp.
4670–4677.

[323] D. Wu, Y. Jia, L. Wang, Y. Sun, Ship hull flexure measurement based on

integrated GNSS/LINS, Front. Optoelectron. 12 (3) (2019) 332–340.

[324] M. Zhang, Q. Wang, Z. Guo, Research on integrated navigation of strap-down
inertial navigation system and star sensor, in: 2017 Forum on Cooperative
Positioning and Service, CPGPS, IEEE, 2017, pp. 11–15.

[297] Y. Shao, C.K. Toth, D.A. Grejner-Brzezinska, L.B. Strange, High-accuracy vehicle
localization using a pre-built probability map, in: ASPRS Imaging and Geospatial
Technology Forum IGTF 2017, Baltimore, Maryland, 2017.

[325] Q. Wang, Y. Li, M. Diao, W. Gao, Z. Qi, Performance enhancement of INS/CNS
integration navigation system based on particle swarm optimization back
propagation neural network, Ocean Eng. 108 (2015) 33–45.

InformationFusion95(2023)62–9089Y. Zhuang et al.

[326] X. Ma, X. Xia, Z. Zhang, G. Wang, H. Qian, Star image processing of SINS/CNS
integrated navigation system based on 1DWF under high dynamic conditions,
in: 2016 IEEE/ION Position, Location and Navigation Symposium, PLANS, IEEE,
2016, pp. 514–518.

[332] O. Hegrenas, K. Gade, O.K. Hagen, P.E. Hagen, Underwater transponder
positioning and navigation of autonomous underwater vehicles, in: OCEANS
2009, MTS/IEEE Biloxi-Marine Technology for Our Future: Global and Local
Challenges, IEEE, 2009, pp. 1–7.

[327] T. Statheros, G. Howells, K.M. Maier, Autonomous ship collision avoidance
navigation concepts, technologies and techniques, J. Navig. 61 (1) (2008)
129–142.

[333] S.I. Sheikh, D.J. Pines, P.S. Ray, K.S. Wood, M.N. Lovellette, M.T. Wolff, The
use of X-ray pulsars for spacecraft navigation, Adv. Astronaut. Sci. 119 (1)
(2005) 105–119.

[328] B. Svilicic, I. Rudan, A. Jugović, D. Zec, A study on cyber security threats in a
shipboard integrated navigational system, J. Mar. Sci. Eng. 7 (10) (2019) 364.
[329] D. Tang, Y. Jiao, J. Chen, On Automatic Landing System for carrier plane
based on integration of INS, GPS and vision, in: 2016 IEEE Chinese Guidance,
Navigation and Control Conference, CGNCC, IEEE, 2016, pp. 2260–2264.
[330] M. Kurowski, S. Roy, J.J. Gehrt, R. Damerius, C. Buskens, D. Abel, T. Jein-
sch, Multi-vehicle guidance, navigation and control towards autonomous ship
maneuvering in confined waters, in: 2019 18th European Control Conference,
IEEE, New York, 2019.

[331] M. Blain, S. Lemieux, R. Houde, Implementation of a ROV navigation sys-
tem using acoustic/Doppler sensors and Kalman filtering, in: OCEANS 2003.
Proceedings, Vol. 3, IEEE, 2003, pp. 1255–1260.

[334] X. Ning, J. Fang, An autonomous celestial navigation method for LEO satellite
based on unscented Kalman filter and information fusion, Aerosp. Sci. Technol.
11 (2–3) (2007) 222–228.

[335] W. Yang, S. Li, N. Li, A switch-mode information fusion filter based on ISRUKF
for autonomous navigation of spacecraft, Inf. Fusion 18 (2014) 33–42.
[336] B. Jia, M. Xin, Vision-based spacecraft relative navigation using sparse-grid
quadrature filter, IEEE Trans. Control Syst. Technol. 21 (5) (2013) 1595–1606.
[337] M. Latva-aho, K. Leppänen, F. Clazzer, A. Munari, Key Drivers and Research
Challenges for 6G Ubiquitous Wireless Intelligence (White Paper), Tech. rep.,
University of Oulu, 2019.

InformationFusion95(2023)62–9090
