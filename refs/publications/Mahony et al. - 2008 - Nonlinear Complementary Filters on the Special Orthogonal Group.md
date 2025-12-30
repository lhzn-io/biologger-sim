Nonlinear Complementary Filters on the Special
Orthogonal Group
R. Mahony, Tarek Hamel, Jean-Michel Pflimlin

To cite this version:

R. Mahony, Tarek Hamel, Jean-Michel Pflimlin. Nonlinear Complementary Filters on the Spe-
IEEE Transactions on Automatic Control, 2008, 53 (5), pp.1203-1217.
cial Orthogonal Group.
￿10.1109/TAC.2008.923738￿. ￿hal-00488376￿

HAL Id: hal-00488376

<https://hal.science/hal-00488376v1>

Submitted on 1 Jun 2010

HAL is a multi-disciplinary open access
archive for the deposit and dissemination of sci-
entific research documents, whether they are pub-
lished or not. The documents may come from
teaching and research institutions in France or
abroad, or from public or private research centers.

L’archive ouverte pluridisciplinaire HAL, est
destinée au dépôt et à la diffusion de documents
scientifiques de niveau recherche, publiés ou non,
émanant des établissements d’enseignement et de
recherche français ou étrangers, des laboratoires
publics ou privés.

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

1

Non-linear complementary ﬁlters on the special
orthogonal group

Robert Mahony, Member, IEEE, Tarek Hamel, Member, IEEE, and Jean-Michel Pﬂimlin, Member, IEEE

Abstract—This paper considers the problem of obtaining good
attitude estimates from measurements obtained from typical low
cost inertial measurement units. The outputs of such systems
are characterised by high noise levels and time varying additive
biases. We formulate the ﬁltering problem as deterministic
observer kinematics posed directly on the special orthogonal
group SO(3) driven by reconstructed attitude and angular ve-
locity measurements. Lyapunov analysis results for the proposed
observers are derived that ensure almost global stability of the
observer error. The approach taken leads to an observer that we
term the direct complementary ﬁlter. By exploiting the geometry
of the special orthogonal group a related observer, termed the
passive complementary ﬁlter, is derived that decouples the gyro
measurements from the reconstructed attitude in the observer
inputs. Both the direct and passive ﬁlters can be extended to
estimate gyro bias on-line. The passive ﬁlter is further developed
to provide a formulation in terms of the measurement error that
avoids any algebraic reconstruction of the attitude. This leads to
an observer on SO(3), termed the explicit complementary ﬁlter,
that requires only accelerometer and gyro outputs; is suitable
for implementation on embedded hardware; and provides good
attitude estimates as well as estimating the gyro biases on-line.
The performance of the observers are demonstrated with a set
of experiments performed on a robotic test-bed and a radio
controlled unmanned aerial vehicle.

Index Terms—Complementary ﬁlter, nonlinear observer, atti-

tude estimates, special orthogonal group.

I. INTRODUCTION

T HE recent proliferation of Micro-Electro-Mechanical

Systems (MEMS) components has lead to the devel-
inertial
opment of a range of low cost and light weight
measurement units. The low power,
light weight and po-
tential for low cost manufacture of these units opens up a
wide range of applications in areas such as virtual reality
and gaming systems, robotic toys, and low cost mini-aerial-
vehicles (MAVs) such as the Hovereye (Fig. 1). The signal
output of low cost IMU systems, however, is characterised
by low-resolution signals subject to high noise levels as well
as general time-varying bias terms. The raw signals must be
processed to reconstruct smoothed attitude estimates and bias-
corrected angular velocity measurements. For many of the
low cost applications considered the algorithms need to run
on embedded processors with low memory and processing
resources.

R. Mahony is with Department of Engineering, Australian National Uni-

versity, ACT, 0200, Australia. e-mail: <Robert.Mahony@anu.edu.au>.

T. Hamel

is with I3S-CNRS, Nice-Sophia Antipolis, France. e-mail:

<thamel@i3s.unice.fr>.
is
Saint

J.-M.
Dassault
<Jean-Michel.Pflimlin@dassault-aviation.com>.

Department
Paris.

Pﬂimlin
Aviation,

Cloud,

with

of
France.

Navigation,
e-mail:

Manuscript received November 08, 2006; revised August 03, 2007.

There is a considerable body of work on attitude recon-
struction for robotics and control applications (for example
[1]–[4]). A standard approach is to use extended stochastic
linear estimation techniques [5], [6]. An alternative is to use
deterministic complementary ﬁlter and non-linear observer
design techniques [7]–[9]. Recent work has focused on some
of the issues encountered for low cost IMU systems [9]–
[12] as well as observer design for partial attitude estimation
[13]–[15]. It is also worth mentioning the related problem of
fusing IMU and vision data that is receiving recent attention
[16]–[19] and the problem of fusing IMU and GPS data [9],
[20]. Parallel to the work in robotics and control there is
a signiﬁcant literature on attitude heading reference systems
(AHRS) for aerospace applications [21]. An excellent review
of attitude ﬁlters is given by Crassidis et al. [22]. The recent
interest in small low-cost aerial robotic vehicles has lead to a
renewed interest in lightweight embedded IMU systems [8],
[23]–[25]. For the low-cost light-weight systems considered,
linear ﬁltering techniques have proved extremely difﬁcult
to apply robustly [26] and linear single-input single-output
complementary ﬁlters are often used in practice [25], [27]. A
key issue is on-line identiﬁcation of gyro bias terms. This
problem is also important in IMU callibration for satellite
systems [5], [21], [28]–[31]. An important development that
came from early work on estimation and control of satellites
was the use of the quaternion representation for the attitude
kinematics [30], [32]–[34]. The non-linear observer designs
that are based on this work have strong robustness properties
and deal well with the bias estimation problem [9], [30].
However, apart from the earlier work of the authors [14],
[35], [36] and some recent work on invariant observers [37],
[38] there appears to be almost no work that considers the
formulation of non-linear attitude observers directly on the
matrix Lie-group representation of SO(3).

In this paper we study the design of non-linear attitude
observers on SO(3) in a general setting. We term the proposed
observers complementary ﬁlters because of the similarity of
the architecture to that of linear complementary ﬁlters (cf. Ap-
pendix A), although, for the non-linear case we do not have
a frequency domain interpretation. A general formulation of
the error criterion and observer structure is proposed based
on the Lie-group structure of SO(3). This formulation leads
us to propose two non-linear observers on SO(3), termed the
direct complementary ﬁlter and passive complementary ﬁlter.
The direct complementary ﬁlter is closely related to recent
work on invariant observers [37], [38] and corresponds (up
to some minor technical differences) to non-linear observers
proposed using the quaternion representation [9], [30], [32].

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

2

Fig. 1. The VTOL MAV HoverEye c(cid:176) of Bertin Technologies.

We do not know of a prior reference for the passive comple-
mentary ﬁlter. The passive complementary ﬁlter has several
practical advantages associated with implementation and low-
sensitivity to noise. In particular, we show that the ﬁlter can
be reformulated in terms of vectorial direction measurements
such as those obtained directly from an IMU system; a
formulation that we term the explicit complementary ﬁlter. The
explicit complementary ﬁlter does not require on-line algebraic
reconstruction of attitude, an implicit weakness in prior work
on non-linear attitude observers [22] due to the computational
overhead of the calculation and poor error characterisation of
the constructed attitude. As a result the observer is ideally
suited for implementation on embedded hardware platforms.
Furthermore, the relative contribution of different data can be
preferentially weighted in the observer response, a property
that allows the designer to adjust for application speciﬁc
noise characteristics. Finally, the explicit complementary ﬁlter
remains well deﬁned even if the data provided is insufﬁcient
to algebraically reconstruct the attitude. This is the case, for
example, for an IMU with only accelerometer and rate gyro
sensors. A comprehensive stability analysis is provided for
all three observers that proves local exponential and almost
global stability of the observer error dynamics, that is, a stable
linearisation for zero error along with global convergence
of the observer error for all initial conditions and system
trajectories other than on a set of measure zero. Although
the principal results of the paper are presented in the matrix
Lie group representation of SO(3), the equivalent quaternion
representation of the observers are presented in an appendix.
The authors recommend that the quaternion representations are
used for hardware implementation.

The body of paper consists of ﬁve sections followed by a
conclusion and two appendices. Section II provides a quick
overview of the sensor model, geometry of SO(3) and in-
troduces the notation used. Section III details the derivation
of the direct and passive complementary ﬁlters. The develop-
ment here is deliberately kept simple to be clear. Section IV
integrates on-line bias estimation into the observer design and
provides a detailed stability analysis. Section V develops the
explicit complementary ﬁlter, a reformulation of the passive
complementary ﬁlter directly in terms of error measurements.

A suite of experimental results, obtained during ﬂight tests
of the Hovereye (Fig. 1), are provided in Section VI that
demonstrate the performance of the proposed observers. In
addition to the conclusion (§VII) there is a short appendix on
linear complementary ﬁlter design and a second appendix that
provides the equivalent quaternion formulation of the proposed
observers.

II. PROBLEM FORMULATION AND NOTATION.

A. Notation and mathematical identities

The special orthogonal group is denoted SO(3). The asso-

ciated Lie-algebra is the set of anti-symmetric matrices

so(3) = {A ∈ R3×3 | A = −AT }

For any two matrices A, B ∈ Rn×n then the Lie-bracket (or
matrix commutator) is [A, B] = AB − BA. Let Ω ∈ R3 then
we deﬁne






Ω× =

0
Ω3
0
−Ω2 Ω1

−Ω3 Ω2
−Ω1
0




 .

For any v ∈ R3 then Ω×v = Ω × v is the vector cross product.
The operator vex : so(3) → R3 denotes the inverse of the Ω×
operator

vex (Ω×) = Ω,
vex(A)× = A,

Ω ∈ R3.
A ∈ so(3)

For any two matrices A, B ∈ Rn×n the Euclidean matrix

inner product and Frobenius norm are deﬁned

(cid:104)(cid:104)A, B(cid:105)(cid:105) = tr(AT B) =

n(cid:88)

AijBij

(cid:112)

||A|| =

(cid:104)(cid:104)A, A(cid:105)(cid:105) =

i,j=1
(cid:118)
(cid:117)
(cid:117)
(cid:116)

n(cid:88)

A2
ij

i,j=1

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

3

The following identities are used in the paper

(Rv)× = Rv×RT ,
(v × w)× = [v×, w×]

R ∈ SO(3), v ∈ R3
v, w ∈ R3

(cid:104)(cid:104)v×, w×(cid:105)(cid:105),

||v×||2,

vT w = (cid:104)v, w(cid:105) =

vT v = |v|2 =

1
2
1
2
(cid:104)(cid:104)A, v×(cid:105)(cid:105) = 0,
tr([A, B]) = 0,

v, w ∈ R3

v ∈ R3

A = AT ∈ R3, v ∈ R3
A, B ∈ R3×3

The following notation for frames of reference is used
• {A} denotes an inertial (ﬁxed) frame of reference.
• {B} denotes a body-ﬁxed-frame of reference.
• {E} denotes the estimator frame of reference.
Let Pa, Ps denote, respectively, the anti-symmetric and

symmetric projection operators in square matrix space

Pa(H) =

1
2

(H − H T ),

Ps(H) =

1
2

(H + H T ).

Let (θ, a) (|a| = 1) denote the angle-axis coordinates of

R ∈ SO(3). One has [39]:

R = exp(θa×),

log(R) = θa×

cos(θ) =

1
2

(tr(R) − 1),

Pa(R) = sin(θ)a×.

For any R ∈ SO(3) then 3 ≥ tr(R) ≥ −1. If tr(R) = 3 then
θ = 0 in angle-axis coordinates and R = I. If tr(R) = −1
then θ = ±π, R has real eigenvalues (1, −1, −1), and there
exists an orthogonal diagonalising transformation U ∈ SO(3)
such that U RU T = diag(1, −1, −1).

For any two signals x(t) : R → Mx, y(t) : R → My
are termed asymptotically dependent if there exists a non-
degenerate function ft : Mx × My → R and a time T such
that for any t > T

ft(x(t), y(t)) = 0.

By the term non-degenerate we mean that the Hessian of ft
at any point (x, y) is full rank. The two signals are termed
asymptotically independent if for any non-degenerate ft and
any T there exists t1 > T with ft(x(t1), y(t1)) (cid:54)= 0.

B. Measurements

The measurements available from a typical inertial mea-
surement unit are 3-axis rate gyros, 3-axis accelerometers and
3-axis magnetometers. The reference frame of the strap down
IMU is termed the body-ﬁxed-frame {B}. The inertial frame
is denoted {A}. The rotation R = A
BR denotes the relative
orientation of {B} with respect to {A}.
Rate Gyros: The rate gyro measures angular velocity of {B}
relative to {A} expressed in the body-ﬁxed-frame of
reference {B}. The error model used in this paper is

Ωy = Ω + b + µ ∈ R3

where Ω ∈ {B} denotes the true value, µ denotes
additive measurement noise and b denotes a constant (or
slowly time-varying) gyro bias.

Accelerometer: Denote the instantaneous linear acceleration
of {B} relative to {A}, expressed in {A}, by ˙v. An ideal
accelerometer, ‘strapped down’ to the body-ﬁxed-frame
{B}, measures the instantaneous linear acceleration of
{B} minus the (conservative) gravitational acceleration
ﬁeld g0 (where we consider g0 expressed in the inertial
frame {A}), and provides a measurement expressed in
the body-ﬁxed-frame {B}. In practice, the output a from
a MEMS component accelerometer has added bias and
noise,

a = RT ( ˙v − g0) + ba + µa,

where ba is a bias term and µa denotes additive measure-
ment noise. Normally, the gravitational ﬁeld g0 = |g0|e3
where |g0| ≈ 9.8 dominates the value of a for low
frequency response. Thus, it is common to use

va =

a
|a|

≈ −RT e3

as a low-frequency estimate of the inertial z-axis ex-
pressed in the body-ﬁxed-frame.

Magnetometer: The magnetometers provide measurements of

the magnetic ﬁeld

m = RT Am + Bm + µb

where Am is the Earths magnetic ﬁeld (expressed in
the inertial frame), Bm is a body-ﬁxed-frame expres-
sion for the local magnetic disturbance and µb denotes
measurement noise. The noise µb is usually quite low
for magnetometer readings, however, the local magnetic
disturbance can be very signiﬁcant, especially if the IMU
is strapped down to an MAV with electric motors. Only
the direction of the magnetometer output is relevant for
attitude estimation and we will use a vectorial measure-
ment

vm =

m
|m|

in the following development

The measured vectors va and vm can be used to construct
BR :

an instantaneous algebraic measurement of the rotation A
{B} → {A}

Ry = arg min

R∈SO(3)

(cid:161)
λ1|e3 − Rva|2 + λ2|v∗

m − Rvm|2(cid:162)

≈ A

BR

where v∗
m is the inertial direction of the magnetic ﬁeld in
the locality where data is acquired. The weights λ1 and λ2
are chosen depending on the relative conﬁdence in the sensor
outputs. Due to the computational complexity of solving an op-
timisation problem the reconstructed rotation is often obtained
in a suboptimal manner where the constraints are applied in
sequence; that is, two degrees of freedom in the rotation matrix
are resolved using the acceleration readings and the ﬁnal
degree of freedom is resolved using the magnetometer. As a
consequence, the error properties of the reconstructed attitude
Ry can be difﬁcult to characterise. Moreover, if either mag-
netometer or accelerometer readings are unavailable (due to
local magnetic disturbance or high acceleration manoeuvres)
then it is impossible to resolve the vectorial measurements into
a unique instantaneous algebraic measurement of attitude.

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

4

C. Error criteria for estimation on SO(3)

Let ˆR denote an estimate of the body-ﬁxed rotation matrix
BR. The rotation ˆR can be considered as coordinates
R = A
for the estimator frame of reference {E}. It is also associated
with the frame transformation

ˆR = A
E

ˆR : {E} → {A}.

The goal of attitude estimate is to drive ˆR → R. The
estimation error used is the relative rotation from body-ﬁxed-
frame {B} to the estimator frame {E}

˜R := ˆRT R,

˜R = E
B

˜R : {B} → {E}.

(1)

The proposed observer design is based on Lyapunov stabil-
ity analysis. The Lyapunov functions used are inspired by the
cost function

˙Etr = −

Etr :=

=

1
4

tr

(cid:107)I3 − ˜R(cid:107)2 =

1
4
1
tr(I3 − ˜R)
2

(cid:179)

(I3 − ˜R)T (I3 − ˜R)

(cid:180)

(2)

One has that

Etr =

1
2

tr(I − ˜R) = (1 − cos(θ)) = 2 sin(θ/2)2.

(3)

where θ is the angle associated with the rotation from {B} to
frame {E}. Thus, driving Eq. 2 to zero ensures that θ → 0.

III. COMPLEMENTARY FILTERS ON SO(3)

In this section, a general framework for non-linear comple-
mentary ﬁltering on the special orthogonal group is introduced.
The theory is ﬁrst developed for the idealised case where R(t)
and Ω(t) are assumed to be known and used to drive the ﬁlter
dynamics. Filter design for real world signals is considered in
later sections.

The goal of attitude estimation is to provide a set of
dynamics for an estimate ˆR(t) ∈ SO(3) to drive the error
rotation (Eq. 1) ˜R(t) → I3. The kinematics of the true system
are

˙R = RΩ× = (RΩ)×R

(4)

where Ω ∈ {B}. The proposed observer equation is posed
directly as a kinematic system for an attitude estimate ˆR on
SO(3). The observer kinematics include a prediction term
based on the Ω measurement and an innovation or correction
term ω := ω( ˜R) derived from the error ˜R. The general form
proposed for the observer is

ˆR(0) = ˆR0,

˙ˆR = (RΩ + kP ˆRω)× ˆR,

(5)
where kP > 0 is a positive gain. The term (RΩ + kP ˆRω) ∈
{A} is expressed in the inertial frame. The body-ﬁxed-frame
angular velocity is mapped back into the inertial frame AΩ =
RΩ. If no correction term is used (kP ω ≡ 0) then the error
rotation ˜R is constant,

˙˜R = ˆRT (RΩ)T

×R + ˆRT (RΩ)×R

= ˆRT (−(RΩ)× + (RΩ)×) R = 0.
The correction term ω := ω( ˜R) ∈ {E} is considered to
be in the estimator frame of reference. It can be thought of

(6)

as a non-linear approximation of the error between R and
ˆR as measured from the frame of reference associated with
ˆR. In practice, it will be implemented as an error between a
measured estimate Ry of R and the estimate ˆR.

The goal of the observer design is to ﬁnd a simple expres-
sion for ω that leads to robust convergence of ˜R → I. In prior
work [35], [36] the authors introduced the following correction
term

ω := vex(Pa( ˜R)) = vex(Pa( ˆRT Ry))

(7)

This choice leads to an elegant Lyapunov analysis of the
ﬁlter stability. Differentiating the storage function Eq. 2 along
trajectories of Eq. 5 yields
(cid:179)

(cid:180)

1
2

kP
2

tr

˜R

ωT
×

tr( ˙˜R) = −
(cid:105)
(cid:104)
kP
×(Ps( ˜R) + Pa( ˜R))
ωT
2
kP
2

(cid:104)(cid:104)ω×, Pa( ˜R)(cid:105)(cid:105) = −kP |ω|2

tr

= −

= −

= −

kP
2

(cid:105)
(cid:104)
×Pa( ˜R)
ωT

tr

(8)

In Mahony et al. [35] a local stability analysis of the ﬁlter
dynamics Eq. 5 is provided based on this derivation. In Section
IV a global stability analysis for these dynamics is provided.
We term the ﬁlter Eq. 5 a complementary ﬁlter on SO(3)
since it recaptures the block diagram structure of a classical
complementary ﬁlter (cf. Appendix A). In Figure 2: The ‘ ˆRT ’

Fig. 2. Block diagram of the general form of a complementary ﬁlter on
SO(3).

operation is an inverse operation on SO(3) and is equivalent to
a ‘−’ operation for a linear complementary ﬁlter. The ‘ ˆRT Ry’
operation is equivalent to generating the error term ‘y − ˆx’.
The two operations Pa( ˜R) and (RΩ)× are maps from error
space and velocity space into the tangent space of SO(3);
operations that are unnecessary on Euclidean space due to the
identiﬁcation TxRn ≡ Rn. The kinematic model is the Lie-
group equivalent of a ﬁrst order integrator.

To implement the complementary ﬁlter it is necessary to
map the body-ﬁxed-frame velocity Ω into the inertial frame. In
practice, the ‘true’ rotation R is not available and an estimate
of the rotation must be used. Two possibilities are considered:
direct complementary ﬁlter: The constructed attitude Ry is

used to map the velocity into the inertial frame

˙ˆR = (RyΩy + kP ˆRω)× ˆR.
A block diagram of this ﬁlter design is shown in Figure
3. This approach can be linked to observers documented

ˆRkˆRTRΩMapsangularvelocityMapsangularvelocity˜R++InverseoperationonSO(3)SystemMapserror˜RRR˙ˆR=AˆR(RΩ)×onSO(3)DifferenceoperationintocorrectframeofreferenceontoTISO(3).ontoTISO(3).kinematicsAˆRTRΩPa(˜R)IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

5

in earlier work [30], [32] (cf. Appendix B). The approach
has the advantage that it does not introduce an additional
feedback loop in the ﬁlter dynamics, however, high
frequency noise in the reconstructed attitude Ry will
enter into the feed-forward term of the ﬁlter.

the architecture shown in Figure 5. The passive complementary
ﬁlter avoids coupling the reconstructed attitude noise into the
predictive velocity term of the observer, has a strong Lyapunov
stability analysis, and provides a simple and elegant realisation
that will lead to the results in Section V.

Fig. 3. Block diagram of the direct complementary ﬁlter on SO(3).

passive complementary ﬁlter: The ﬁltered attitude ˆR is used

IV. STABILITY ANALYSIS

Fig. 5. Block diagram of the simpliﬁed form of the passive complementary
ﬁlter.

in the predictive velocity term

(9)

˙ˆR = ( ˆRΩy + kP ˆRω)× ˆR.
A block diagram of this architecture is shown in Figure 4.
The advantage lies in avoiding corrupting the predictive
angular velocity term with the noise in the reconstructed
pose. However,
the approach introduces a secondary
feedback loop in the ﬁlter and stability needs to be
proved.

In this section, the direct and passive complementary ﬁlters
on SO(3) are extended to provide on-line estimation of time-
varying bias terms in the gyroscope measurements and global
stability results are derived. Preliminary results were published
in [35], [36].

For the following work it is assumed that a reconstructed
rotation Ry and a biased measure of angular velocity Ωy are
available

Ry ≈ R,
Ωy ≈ Ω + b

valid for low frequencies,
for constant bias b.

(11a)

(11b)

The approach taken is to add an integrator to the compensator
term in the feedback equation of the complementary ﬁlter.

Let kP , kI > 0 be positive gains and deﬁne
Direct complementary ﬁlter with bias correction:

Ry(Ωy − ˆb) + kP ˆRω

(cid:180)

(cid:179)

˙ˆR =
˙ˆb = −kI ω,

ˆR,

ˆR(0) = ˆR0, (12a)

×

ˆb(0) = ˆb0,

(12b)
˜R = ˆRT Ry. (12c)

Fig. 4. Block diagram of the passive complementary ﬁlter on SO(3).

A key observation is that the Lyapunov stability analysis in

ω = vex(Pa( ˜R)),

Eq. 8 is still valid for Eq. 9, since

˙Etr = −

1
2

1
2

tr( ˙˜R) = −
1
2
that

= −

tr([ ˜R, Ω×]) −

tr(−(Ω + kP ω)× ˜R + ˜RΩ×)

kP
2

tr(ωT
×

˜R) = −kP |ω|2,

the trace of a commutator

using the fact
is zero,
tr([ ˜R, Ω×]) = 0. The ﬁlter is termed a passive complimentary
ﬁlter since the cross coupling between Ω and ˜R does not
contribute to the derivative of the Lyapunov function. A global
stability analysis is provided in Section IV.

There is no particular theoretical advantage to either the
direct or the passive ﬁlter architecture in the case where exact
measurements are assumed. However, it is straightforward to
see that the passive ﬁlter (Eq. 9) can be written

˙ˆR = ˆR(Ω× + kP Pa( ˜R)).
This formulation suppresses entirely the requirement to repre-
sent Ω and ω = kP Pa( ˜R) in the inertial frame and leads to

(10)

Passive complementary ﬁlter with bias correction:

(cid:180)

,

×

Ωy − ˆb + kP ω

(cid:179)

˙ˆR = ˆR
˙ˆb = −kI ω,
ω = vex(Pa( ˜R)),

ˆR(0) = ˆR0,

ˆb(0) = ˆb0,
˜R = ˆRT Ry.

(13a)

(13b)

(13c)

The non-linear stability analysis is based on the idea of an
adaptive estimate for the unknown bias value.

Theorem 4.1: [Direct complementary ﬁlter with bias
correction.] Consider the rotation kinematics Eq. 4 for a
time-varying R(t) ∈ SO(3) and with measurements given
by Eq. 11. Let ( ˆR(t), ˆb(t)) denote the solution of Eq. 12.
Deﬁne error variables ˜R = ˆRT R and ˜b = b − ˆb. Deﬁne
U ⊆ SO(3) × R3 by

(cid:110)
( ˜R, ˜b) tr( ˜R) = −1, Pa(˜b× ˜R) = 0

(cid:111)

.

(14)

U =

Then:

ˆRkˆRT++˙ˆR=AˆR(RyΩy)×AΩyRyRyΩy˜RˆRTRyPa(˜R)ˆRk++ˆRTRy˙ˆR=AˆRRyΩy˜R(ˆRΩy)×ˆRΩyˆRTAPa(˜R)˙ˆR=ˆRAˆRkΩyRyˆRTR(Ω)×ˆRTPa(˜R)IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

6

1) The set U is forward invariant and unstable with respect

to the dynamic system Eq. 12.

2) The error ( ˜R(t), ˜b(t)) is locally exponentially stable to

(I, 0).

3) For almost all initial conditions ( ˜R0, ˜b0) (cid:54)∈ U the trajec-
tory ( ˆR(t), ˆb(t)) converges to the trajectory (R(t), b).

Proof: Substituting for the error model (Eq. 11), Equation

12a becomes

˙ˆR =

(cid:179)
R(Ω + ˜b) + kP ˆRω

(cid:180)

×

ˆR.

Differentiating ˜R it is straightforward to verify that

˙˜R = −kP ω× ˜R − ˜b× ˜R.

(15)

Deﬁne a candidate Lyapunov function by

V =

1
2

tr(I3 − ˜R) +

1
2kI

|˜b|2 = Etr +

1
2kI

|˜b|2

(16)

Differentiating V one obtains

tr( ˙˜R) −
(cid:179)

˜bT ˙ˆb

1
kI

kP ω× ˜R + ˜b× ˜R

˙V = −

=

=

1
2
1
2
−kP
2

tr

(cid:180)

−

1
kI

(cid:104)˜b,

˙ˆb(cid:105)

(cid:104)(cid:104)ω×, Pa( ˜R) + Ps( ˜R)(cid:105)(cid:105)
1
2

(cid:104)(cid:104)˜b×, Pa( ˜R) + Ps( ˜R)(cid:105)(cid:105) −

−

(cid:104)˜b,

˙ˆb(cid:105)

1
kI

= −kP (cid:104)ω, vex(Pa( ˜R))(cid:105) − (cid:104)˜b, vex(Pa( ˜R)(cid:105) −

(cid:104)˜b,

˙ˆb(cid:105)

1
kI

Substituting for

˙ˆb and ω (Eqn’s 12b and 12c) one obtains

˙V = −kP |ω|2 = −kP |vexPa( ˜R)|2

(17)

√

Lyapunov’s direct method ensures that ω converges asymptoti-
cally to zero [40]. Recalling that ||Pa( ˜R)|| =
2 sin(θ), where
(θ, a) denotes the angle-axis coordinates of ˜R. It follows that
ω ≡ 0 implies either ˜R = I, or log( ˜R) = πa× for |a| = 1.
In the second case one has the condition tr( ˜R) = −1. Note
that ω = 0 is also equivalent to requiring ˜R = ˜RT to be
symmetric.

It is easily veriﬁed that (I, 0) is an isolated equilibrium of

the error dynamics Eq. 18.

From the deﬁnition of U one has that ω ≡ 0 on U. We will
prove that U is forward invariant under the ﬁlter dynamics
Eqn’s 12. Setting ω = 0 in Eq. 15 and Eq. 12b yields

˙˜R = −˜b× ˜R,

˙ˆb = 0.

(18)

For initial conditions ( ˜R0, ˜b0) = ( ˜R0, ˜b0) ∈ U the solution of
Eq. 18 is given by

˜R(t) = exp(−t˜b×) ˜R0,

˜b(t) = ˜b0,

( ˜R0, ˜b0) ∈ U.

(19)

We verify that Eq. 19 is also a general solution of Eqn’s 15
and 12b. Differentiating tr( ˜R) yields

d
dt

tr( ˜R) = −tr(˜b× exp(−t˜b×) ˜R0)

(cid:195)

= tr

exp(−t˜b×)

(˜b× ˜R0 + ˜R0

˜b×)

(cid:33)

2

(cid:179)
exp(−t˜b×)Pa(˜b× ˜R0)

(cid:180)

= 0,

= tr

where the second line follows since ˜b× commutes with
exp(˜b×) and the ﬁnal equality is due to the fact
that
Pa(˜b× ˜R0) = 0, a consequence of the choice of initial
conditions ( ˜R0, ˜b0) ∈ U. It follows that tr( ˜R(t)) = −1 on
solution of Eq. 19 and hence ω ≡ 0. Classical uniqueness
results verify that Eq. 19 is a solution of Eqn’s 15 and 12b. It
remains to show that such solutions remain in U for all time.
The condition on ˜R is proved above. To see that Pa(˜b× ˜R) ≡ 0
we compute

d
dt

Pa(˜b× ˜R) = −Pa(˜b2
×

˜R) = −Pa(˜b× ˜R˜bT

×) = 0

as ˜R = ˜RT . This proves that U is forward invariant.

Applying LaSalle’s principle to the solutions of Eq. 12 it
follows that either ( ˜R, ˜b) → (I, 0) asymptotically or ( ˜R, ˜b) →
( ˜R∗(t), ˜b0) where ( ˜R∗(t), ˜b0) ∈ U is a solution of Eq. 18.

To determine the local stability properties of the invariant
sets we compute the linearisation of the error dynamics. We
will prove exponential stability of the isolated equilibrium
point (I, 0) ﬁrst and then return to prove instability of the
set U. Deﬁne x, y ∈ R3 as the ﬁrst order approximations of
˜R and ˜b around (I, 0)

˜R ≈ (I + x×),
˜b = −y.

x× ∈ so(3)

(20a)

(20b)

The sign change in Eq. 20b simpliﬁes the analysis of the
˙˜b and dis-
linearisation. Substituting into Eq. 15, computing
carding all terms of quadratic or higher order in (x, y) yields

(cid:195)

d
dt

x

y

(cid:33)

(cid:195)

=

−kP I3
−kI I3

I3
0

(cid:33) (cid:195)

(cid:33)

x

y

(21)

For positive gains kP , kI > 0 the linearised error system is
strictly stable. This proves part ii) of the theorem statement.
To prove that U is unstable, we use the quaternion formu-
lation (see Appendix B). Using Eq. 49, the error dynamics of
the quaternion ˜q = (˜s, ˜v) associated to the rotation ˜R is given
by

(kP ˜s|˜v|2 + ˜vT ˜b),

1
2

˙˜s =
˙˜b = kI ˜s˜v,
˙˜v = −

1
2

(˜s(˜b + kP ˜s˜v) + ˜b × ˜v),

(22a)

(22b)

(22c)

It is straightforward to verify that the invariant set associated
to the error dynamics is characterised by

(cid:110)

(˜s, ˜v, ˜b) ˜s = 0, |˜v| = 1, ˜bT ˜v = 0

(cid:111)

U =

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

7

Deﬁne y = ˜bT ˜v, then an equivalent characterisation of U is
given by (˜s, y) = (0, 0). We study the stability properties
of the equilibrium (0, 0) of (˜s, y) evolving under the ﬁlter
dynamics Eq. 12. Combining Eq. 22c and 22b, one obtains
the following dynamics for ˙y
˙y = ˜vT ˙˜b + ˜bT ˙˜v
= kI ˜s|˜v|2 − 1

2 ˜s|˜b|2 − 1

2 kP ˜s2y

Linearising around small values of (˜s, y) one obtains

(cid:195)

(cid:33)

(cid:195)

˙˜s
˙y

=

1
2 kP
2 |˜b0|2
kI − 1

1
2
0

(cid:33) (cid:195)

(cid:33)

˜s

y

Since KP and KI are positive gains it follows that the lineari-
sation is unstable around the point (0, 0) and this completes
the proof of part i).

The linearisation of the dynamics around the unstable set is
either strongly unstable (for large values of |˜b0|2) or hyperbolic
(both positive and negative eigenvalues). Since ˜b0 depends on
the initial condition then there there will be trajectories that
converge to U along the stable centre manifold [40] associated
with the stable direction of the linearisation. From classical
centre manifold theory it is known that such trajectories are
measure zero in the overall space. Observing in addition that
U is measure zero in SO(3) × R3 proves part iii) and the full
proof is complete.

The direct complimentary ﬁlter is closely related to quater-
nion based attitude ﬁlters published over the last ﬁfteen years
[9], [30], [32]. Details of the similarities and differences is
given in Appendix B where we present quaternion versions of
the ﬁlters we propose in this paper. Apart from the formulation
directly on SO(3), the present paper extends earlier work
by proposing globally deﬁned observer dynamics and a full
global analysis. To the authors best understanding, all prior
published algorithms depend on a sgn(θ) term that is discon-
tinuous on U (Eq. 14). Given that the observers are not well
deﬁned on the set U the analysis for prior work is necessarily
non-global. However, having noted this, the recent work of
Thienel et al. [30] provides an elegant powerful analysis that
transforms the observer error dynamics into a linear time-
varying system (the transformation is only valid on a domain
on SO(3) × R3 − U) for which global asymptotic stability is
proved. This analysis provides a global exponential stability
under the assumption that the observer error trajectory does
not intersect U. In all practical situations the two approaches
are equivalent.

The remainder of the section is devoted to proving an anal-
ogous result to Theorem 4.1 for the passive complementary
is necessary to deal with
ﬁlter dynamics. In this case,
non-autonomous terms in the error dynamics due to passive
coupling of the driving term Ω into the ﬁlter error dynamics.
Interestingly, the non-autonomous term acts in our favour to
disturb the forward invariance properties of the set U (Eq. 14)
and reduce the size of the unstable invariant set.

it

Theorem 4.2: [Passive complementary ﬁlter with bias
correction.] Consider the rotation kinematics Eq. 4 for a
time-varying R(t) ∈ SO(3) and with measurements given by
Eq. 11. Let ( ˆR(t), ˆb(t)) denote the solution of Eq. 13. Deﬁne

error variables ˜R = ˆRT R and ˜b = b − ˆb. Assume that Ω(t) is
a bounded, absolutely continuous signal and that the pair of
signals (Ω(t), ˜R) are asymptotically independent (see §II-A).
Deﬁne U0 ⊆ SO(3) × R3 by

(cid:110)

(cid:111)

( ˜R, ˜b) tr( ˜R) = −1, ˜b = 0

.

(23)

U0 =

Then:

1) The set U0 is forward invariant and unstable with respect

to the dynamic system 13.

2) The error ( ˜R(t), ˜b(t)) is locally exponentially stable to

(I, 0).

3) For almost all initial conditions ( ˜R0, ˜b0) (cid:54)∈ U0 the tra-
jectory ( ˆR(t), ˆb(t)) converges to the trajectory (R(t), b).
Proof: Substituting for the error model (Eq. 11) in Eqn’s

13 and differentiating ˜R, it is straightforward to verify that
˙˜R = [ ˜R, Ω×] − kP ω× ˜R − ˜b× ˜R,
˙˜b = kI ω

(24a)

(24b)

The proof proceeds by differentiating the Lyapunov-like func-
tion Eq. 16 for solutions of Eq. 13. Following an analogous
derivation to that in Theorem 4.1, but additionally exploiting
the cancellation tr([ ˜R, Ω×]) = 0, it may be veriﬁed that

˙V = −kP |ω|2 = −kP |vex(Pa( ˜R))|2

where V is given by Eq. 16. This bounds V (t) ≤ V (0), and
it follows ˜b is bounded. LaSalle’s principle cannot be applied
directly since the dynamics Eq. 24a are not autonomous. The
function ˙V is uniformly continuous since the derivative

¨V = −kP Pa( ˜R)T

Pa([ ˜R, Ω×]) − Pa((kP ω − ˜b)×) ˜R

(cid:179)

(cid:180)

is uniformly bounded. Applying Barbalat’s lemma proves
asymptotic convergence of ω = vex(Pa( ˜R)) to zero.

Direct substitution shows that ( ˜R, ˜b) = (I, 0) is an equilib-
rium point of Eq. 24. Note that U0 ⊂ U (Eq. 14) and hence
ω ≡ 0 on U (Th. 4.1). For ( ˜R, ˜b) ∈ U0 the error dynamics
Eq. 24 become

˙˜R = [ ˜R, Ω×],

˙˜b = 0.

The solution of this ordinary differential equation is given by

˜R(t) = exp(−A(t)) ˜R0 exp(A(t)), A(t) =

(cid:90) t

Ω×dτ.

0

Since A(t) is anti-symmetric for all time then exp(−A(t)) is
orthogonal and since exp(−A(t)) = exp(A(t))T it follows ˜R
is symmetric for all time. It follows that U0 is forward invariant
under the ﬁlter dynamics Eq. 13. We prove by contradiction
that U0 ⊂ U is the largest forward invariant set of the closed-
loop dynamics Eq. 13 such that ω ≡ 0. Assume that there
exits ( ˜R0, ˜b0) ∈ U − U0 such that ( ˜R(t), ˜b(t)) remains in U
for all time. One has that Pa(˜b× ˜R) = 0 on this trajectory.
Consequently,

d
dt

Pa(˜b× ˜R) = Pa(˜b×[ ˜R, Ω×]) − P(˜b× ˜RbT
×)
= Pa(˜b×[ ˜R, Ω×])
(cid:179)

= −

(˜b × Ω)× ˜R + ˜R(˜b × Ω)×

1
2

(cid:180)

= 0,

(25)

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

8

,

vi = RT v0i + µi,

vi ∈ {B}

(29)

where we have used

2Pa(˜b× ˜R) = ˜b× ˜R + ˜R˜b× = 0,
several times in simplifying expressions. Since (Ω(t), ˜R(t))
are asymptotically independent then the relationship Eq. 25
must be degenerate. This implies that there exists a time T
such that for all t > T then ˜b(t) ≡ 0 and contradicts the
assumption.

(26)

It follows that either ( ˜R, ˜b) → (I, 0) asymptotically or

( ˜R, ˜b) → ( ˜R∗(t), 0) ∈ U0.

Analogously to Theorem 4.1 the linearisation of the error
dynamics (Eq. 24) at (I, 0) is computed. Let ˜R ≈ I + x×
and ˜b ≈ −y for x, y ∈ R3. The linearised dynamics are the
time-varying linear system

(cid:195)

(cid:33)

(cid:195)

d
dt

x

y

=

(cid:33) (cid:195)

(cid:33)

−kP I3 − Ω(t)× I3
0

−kI I3

x

y

Let |Ωmax| denote the magnitude bound on Ω and choose

α2 > 0, α1 >

α1 + kP α2
kI

< α3 <

α2(|Ωmax|2 + kI )
kP
α1 + kP α2
kI

+

|Ωmax|α2
kI

Set P, Q to be matrices

(cid:181)

P =

α1I3 −α2I3
α3I3
−α2I3

(cid:182)

(cid:181)

, Q =

kP α1 − α2kI −α2|Ωmax|

−α2|Ωmax|

α2

(cid:182)

(27)
It is straightforward to verify that P and Q are positive
deﬁnite matrices given the constraints on {α1, α2, α3}. Con-
sider the cost function W = 1
2 ξT P ξ, with ξ = (x, y)T .
Differentiating W yields

˙W = − (kP α1 − α2kI )|x|2 − α2|y|2

+ yT x(α1 + kP α2 − α3kI ) + α2yT (Ω × x)

(28)

It is straightforward to verify that

(cid:162)

ξT P ξ

(cid:161)

d
dt

≤ −2(|x|, |y|) Q

(cid:33)

(cid:195)

|x|

|y|

.

This proves exponential stability of the linearised system at
(I, 0).

The linearisation of the error dynamics on a trajectory in
U0 are also time varying and it is not possible to use the
argument from Theorem 4.1 to prove instability. However,
note that V ( ˜R∗, ˜b∗) = 2 for all ( ˜R∗, ˜b∗) ∈ U0. Moreover,
any neighbourhood of a point ( ˜R∗, ˜b∗) ∈ U0 within the set
SO(3) × R3 contains points ( ˜R, ˜b) such the V ( ˜R, ˜b) < 2.
Trajectories with these initial conditions cannot converge to U0
due to the decrease condition derived earlier, and it follows that
U0 is unstable. Analogous to Theorem 4.1 it is still possible
that a set of measure zero initial conditions, along with very
speciﬁc trajectories Ω(t), such that the resulting trajectories
converge to to U0. This proves part iii) and completes the
proof.

Apart from the expected conditions inherited from Theo-
rem 4.1 the key assumption in Theorem 4.2 is the indepen-
dence of Ω(t) from the error signal ˜R. The perturbation of the

passive dynamics by the independent driving term Ω provides
a disturbance that ensures that
the adaptive bias estimate
converges to the true gyroscopes’ bias, a particularly useful
property in practical applications.

V. EXPLICIT ERROR FORMULATION OF THE PASSIVE
COMPLEMENTARY FILTER

A weakness of the formulation of both the direct and passive
and complementary ﬁlters is the requirement to reconstruct an
estimate of the attitude, Ry, to use as the driving term for the
error dynamics. The reconstruction cannot be avoided in the
direct ﬁlter implementation because the reconstructed attitude
is also used to map the velocity into the inertial frame. In this
section, we show how the passive complementary ﬁlter may be
reformulated in terms of direct measurements from the inertial
unit.

Let v0i ∈ {A}, i = 1, . . . , n, denote a set of n known
inertial directions. The measurements considered are body-
ﬁxed-frame observations of the ﬁxed inertial directions

where µi is a noise process. Since only the direction of the
measurement is relevant to the observer we assume that |v0i| =
1 and normalise all measurements to ensure |vi| = 1.

Let ˆR be an estimate of R. Deﬁne
ˆvi = ˆRT v0i

to be the associated estimate of vi. For a single direction vi,
the error considered is

Ei = 1 − cos(∠vi, ˆvi) = 1 − (cid:104)vi, ˆvi(cid:105)

which yields

Ei = 1 − tr( ˆRT v0ivT

0iR) = 1 − tr( ˜RRT v0ivT

0iR)

For multiple measures vi the following cost function is con-
sidered

Emes =

n(cid:88)

i=1

kiEi =

n(cid:88)

i=1

where

ki − tr( ˜RM ),

ki > 0,

(30)

M = RT M0R with M0 =

n(cid:88)

i=1

kiv0ivT
0i

(31)

Assume linearly independent inertial direction {v0i} then the
matrix M is positive deﬁnite (M > 0) if n ≥ 3. For n = 2
then M is positive semi-deﬁnite with one eigenvalue zero.
The weights ki > 0 are chosen depending on the relative
conﬁdence in the measurements vi. For technical reasons in the
proof of Theorem 5.1 we assume additionally that the weights
ki are chosen such that M0 has three distinct eigenvalues λ1 >
λ2 > λ3.

Theorem 5.1: [Explicit complementary ﬁlter with bias
correction.] Consider the rotation kinematics Eq. 4 for a time-
varying R(t) ∈ SO(3) and with measurements given by Eqn’s
29 and 11b. Assume that there are two or more, (n ≥ 2)
vectorial measurements vi available. Choose ki > 0 such

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

9

that M0 (deﬁned by Eq. 31) has three distinct eigenvalues.
Consider the ﬁlter kinematics given by
(cid:180)

(cid:179)

(Ωy − ˆb)× + kP (ωmes)×

,

ˆR(0) = ˆR0

(32a)

(32b)

˙ˆR = ˆR
˙ˆb = −kI ωmes
n(cid:88)

ωmes :=

kivi × ˆvi,

ki > 0.

(32c)

i=1

and let ( ˆR(t), ˆb(t)) denote the solution of Eqn’s 32. Assume
that Ω(t) is a bounded, absolutely continuous signal and that
the pair of signals (Ω(t), ˜RT ) are asymptotically independent
(see §II-A). Then:

1) There are three unstable equilibria of the ﬁlter charac-

terised by

( ˆR∗i, ˆb∗i) =

(cid:161)
U0DiU T

0 R, b

(cid:162)

, i = 1, 2, 3,

where D1 = diag(1, −1, −1), D2 = diag(−1, 1, −1)
and D3 = diag(−1, −1, 1) are diagonal matrices with
entries as shown and U0 ∈ SO(3) such that M0 =
U0ΛU T
0 where Λ = diag(λ1, λ2, λ3) is a diagonal
matrix.

2) The error ( ˜R(t), ˜b(t)) is locally exponentially stable to

(I, 0).

3) For almost all initial conditions ( ˜R0, ˜b0) (cid:54)= ( ˆRT

∗iR, b),
i = 1, . . . , 3, the trajectory ( ˆR(t), ˆb(t)) converges to the
trajectory (R(t), b).
Proof: Deﬁne a candidate Lyapunov-like function by

V =

n(cid:88)

i=1

ki − tr( ˜RM ) +

1
kI

˜b2 = Emes +

˜b2

1
kI

The derivative of V is given by

(cid:179)

˙V = − tr

(cid:180)

˙˜RM + ˜R ˙M
(cid:179)

2
kI
[ ˜RM, Ω×] − (˜b + kP ωmes)× ˜RM

˜bT ˙ˆb

−

= −tr

We prove next Eq. 35 implies either ˜R = I or tr( ˜R) = −1.

Since ˜R is a real matrix, the eigenvalues and eigenvectors

of ˜R verify

˜RT xk = λkxk and xH
k

˜R = λH

k xH
k

(36)

where λH
k (for k = 1 . . . 3) represents the complex conjugate
of the eigenvalue λk and xH
k represents the Hermitian trans-
pose of the eigenvector xk associated to λk. Combining Eq. 35
and Eq. 36, one obtains

˜RM xk = λH
k xH
xH
k
k M ˜RT xk = λkxH
xH

k M xk
k M xk = λH

k xH

k M xk

Note that for n ≥ 3, M > 0 is positive deﬁnite and
k M xk > 0, ∀k = {1, 2, 3}. One has λk = λH
xH
k for all k.
In the case when n = 2, it is simple to verify that two of the
three eigenvalues are real. It follows that all three eigenvalues
of ˜R are real since complex eigenvalues must come in complex
conjugate pairs. The eigenvalues of an orthogonal matrix are
of the form

eig( ˜R) = (1, cos(θ) + i sin(θ), cos(θ) − i sin(θ)),

where θ is the angle from the angle-axis representation. Given
that all the eigenvalues are real it follows that θ = 0 or θ =
±π. The ﬁrst possibility is the desired case ( ˜R, ˜b) = (I, 0).
The second possibility is the case where tr( ˜R) = −1.

When ωmes ≡ 0 then Eqn’s 32 and Eqn’s 13 lead to
identical error dynamics. Thus, we use the same argument
as in Theorem 4.2 to prove that ˜b = 0 on the invariant set.
To see that the only forward invariant subsets are the unstable
equilibria as characterised in part i) of the theorem statement
we introduce ¯R = R ˆRT . Observe that

˜RM = M ˜RT ⇒ ¯RM0 = M0 ¯RT

(cid:180)

−

˜bT ˙ˆb

2
kI

Analogous to Eq. 35, this implies ¯R = I3 or tr( ¯R) = −1 on
the set ωmes ≡ 0 and ¯R = ¯RT . Set ¯R(cid:48) = U T
0

¯RU0. Then

Recalling that the trace of a commutator is zero, the derivative
of the candidate Lyapunov function can be simpliﬁed to obtain
(cid:182)(cid:182)

(cid:181)

(cid:181)

(cid:179)

(cid:180)

˙V = kP tr

(ωmes)×Pa( ˜RM )

+tr

˜b×

Pa( ˜RM ) −

˙ˆb×

1
kI

(33)
Recalling the identities in Section II-A one may write ωmes

as

(ωmes)× =

n(cid:88)

i=1

ki
2

(ˆvivT

i − vi ˆvi

T ) = Pa( ˜RM )

(34)

Introducing the expressions of ωmes into the time derivative

of the Lyapunov-like function V , Eq. 33, one obtains

˙V = −kP ||Pa( ˜RM )||2.

The Lyapunov-like function derivative is negative semi-
deﬁnite ensuring that ˜b is bounded. Analogous to the proof
of Theorem 4.2, Barbalat’s lemma is invoked to show that
Pa( ˜RM ) tends to zero asymptotically. Thus, for ˙V = 0 one
has

˜RM = M ˜RT .

(35)

¯R(cid:48)Λ − Λ ¯R(cid:48) = 0 ⇒ ∀i, j (λi − λj) ¯R(cid:48)

ij = 0
As M0 has three distinct eigenvalues, it follows that ¯R(cid:48)
ij = 0
for all i (cid:54)= j and thus ¯R(cid:48) is diagonal. Therefore, there are
four isolated equilibrium points ¯R(cid:48)
0 , i = 1, . . . , 3
(where Di are speciﬁed in part i) of the theorem statement)
and ¯R(cid:48) = I that satisfy the condition ωmes ≡ 0. The case
¯R(cid:48)
(where D4 = I) corresponds to the
equilibrium ( ˜R, ˜b) = (I, 0) while we will show that the other
three equilibria are unstable.

0 = I = U0D4U T
0

0 = U0DiU T

We proceed by computing the dynamics of the ﬁlter in the
new ¯R variable and using these dynamics to prove the stability
properties of the equilibria. The dynamics associated to ¯R are

˙¯R = ˙R ˆRT + R

˙ˆRT

= RΩ× ˆRT − R(Ω + ˜b)× ˆRT − kP RPa( ˜RM ) ˆRT
= −R˜b× ˆRT − kP
= −R˜b×(RT R) ˆRT − kP
= −(R˜b)× ¯R − kP

2 R( ˜RM − M ˜RT ) ˆRT

2 R( ˆRT M0R − RT M0 ˆR) ˆRT

2 ( ¯RM0 ¯R − M0)

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

10

Setting ¯b = R˜b, one obtains

˙¯R = −¯b× ¯R −

kP
2
The dynamics of the new estimation error on the bias ¯b are

( ¯RM0 ¯R − M0).

(37)

= [(RΩ)×, ¯b×] +

˙¯b× = ˙R¯b×RT + R¯b× ˙RT + kI RPa( ˜RM )RT
kI
2
kI
2

= [(RΩ)×, ¯b×] +

( ¯RM0 − M0 ¯RT )

R( ˆRT M0R − RT M0 ˆR)RT

(38)

The dynamics of ( ¯R, ¯b) (Eqn’s 37 and 38) are an alternative
formulation of the error dynamics to ( ˜R, ˜b).

Consider a ﬁrst order approximation of ( ¯R, ¯b) (Eqn’s 37 and

38) around an equilibrium point ( ¯R0, 0)

¯R = ¯R0(I3 + x×),

¯b = −y.

The linearisation of Eq. 37 is given by

The combined error dynamic linearisation in the primed coor-
dinates is
(cid:33)
(cid:195)

(cid:33) (cid:195)

(cid:33)

(cid:195)

˙x(cid:48)
˙y(cid:48)

=

kP Ai
kI AiDi Ω(cid:48)(t)×

Di

x(cid:48)
y(cid:48)

,

i = 1, . . . , 4.

(39)
To complete the proof of part i) of the theorem statement we
will prove that the three equilibria associated with ( ¯R∗i, ¯b∗i)
for i = 1, 2, 3 are unstable. The demonstration is analogous to
the proof of the Chetaev’s Theorem (see [40, pp. 111–112]).
Consider the following cost function:

S =

1
2

kI x(cid:48)T Aix(cid:48) −

1
2

|y(cid:48)|2

It is straightforward to verify that its time derivative is always
positive

˙S = kP kI A2

i |x(cid:48)|2.

Note that for i = 1, . . . , 3 then Ai has at least one element of
the diagonal positive. For each i = 1, . . . , 3 and r > 0, deﬁne

( ¯R0x×M0 ¯R0 + ¯R0M0 ¯R0x×),

Ur = {ξ(cid:48) = (x(cid:48), y(cid:48))T : S(ξ(cid:48)) > 0, |ξ(cid:48)| < r}

¯R0 ˙x× = y× ¯R0 −

kP
2

and thus

˙x× = ¯RT

0 y× ¯R0 −

kP
2

(x×M0 ¯R0 + M0 ¯R0x×),

and ﬁnally

U T

0 ˙x×U0 = Di(U T

0 y)×Di−

kP
2

((U T

0 x)×ΛDi+ΛDi(U T

0 x)×)

for i = 1, . . . , 4 and where Λ is speciﬁed in part i) of the
theorem statement. Deﬁne

A1 = 0.5diag(λ2 + λ3, −λ1 + λ3, −λ1 + λ2)
A2 = 0.5diag(λ2 − λ3, λ1 − λ3, λ1 + λ2)
A3 = 0.5diag(−λ2 + λ3, λ1 + λ3, +λ1 − λ2)
A4 = 0.5diag(−λ2 − λ3, −λ1 − λ3, −λ1 − λ2)

Setting y(cid:48) = U T
linearisation Eq. 37 as

0 y and x(cid:48) = U T

0 x one may write the

˙x(cid:48) = kP Aix(cid:48) + Diy(cid:48),

i = 1, . . . , 4.

We continue by computing the linearisation of ˙¯b. Equation

(38) may be approximated to a ﬁrst order by

− ˙y× = [(RΩ)×, −y×] +

kI
2

( ¯R0x×M0 + M0x× ¯R0)

and thus

−U T

0 ˙y×U0 = [(U T

0 RΩ)×, −y(cid:48)

×] +

kI
2

Finally, for i = 1, . . . , 4

(Dix(cid:48)

×Λ + Λx(cid:48)

×Di).

U T

0 ˙y×U0 = −

kI
2

((Dix(cid:48))×DiΛ + ΛDi(Dix(cid:48))×) + [Ω(cid:48)

×, y(cid:48)

×].

Rewriting in terms of the variables x(cid:48), y(cid:48) and setting Ω(cid:48) =
U T

0 RΩ one obtains

and note that Ur is non-null for all r > 0. Let ξ(cid:48)
0 ∈ Ur such
0) > 0. A trajectory ξ(cid:48)(t) initialized at ξ(cid:48)(0) = ξ(cid:48)
that S(ξ(cid:48)
0
will diverge from the compact set Ur since ˙S(ξ(cid:48)) > 0 on Ur.
However, the trajectory cannot exit Ur through the surface
S(ξ(cid:48)) = 0 since S(ξ(cid:48)(t)) ≥ S(ξ(cid:48)
0) along the trajectory.
Restricting r such that the linearisation is valid, then the trajec-
tory must exit Ur through the sphere |ξ(cid:48)| = r. Consequently,
trajectories initially arbitrarily close to (0, 0) will diverge. This
proves that the point (0, 0) is locally unstable.

To prove local exponential stability of ( ¯R, ¯b) = (I, 0) we
consider the linearisation Eq. 39 for i = 4. Note that D4 = I
and A4 < 0. Set KP = − kP
2 A4. Then
KP , KI > 0 are positive deﬁnite and Eq. 39 may be written
as

2 A4 and KI = − kI

(cid:33) (cid:195)

(cid:33)

(cid:33)

(cid:195)

(cid:195)

d
dt

x(cid:48)
y(cid:48)

=

I3

−KP
−KI Ω(cid:48)(t)×

x(cid:48)
y(cid:48)

Consider a cost function V = ξ(cid:48)T P ξ(cid:48) with P given by Eq. 27.
Analogous to Eq. 28, the time derivative of V is given by

˙V = − (KP α1 − α2KI )|x(cid:48)|2 − α2|y(cid:48)|2

+ y(cid:48)T x(cid:48)(α1 + KP α2 − α3KI ) − α2x(cid:48)T (Ω(cid:48) × y(cid:48)).

Once again, it is straightforward to verify that

˙V ≤ −2(|x(cid:48)|, |y(cid:48)|)Q

(cid:195)

(cid:33)

|x(cid:48)|
|y(cid:48)|

where Q is deﬁned in Eq. 27 and this proves local exponential
stability of ( ¯R, ¯b) = (I, 0).

The ﬁnal statement of the theorem follows directly from the
above results along with classical dynamical systems theory
and the proof is complete.

Remark: If n = 3, the weights ki = 1, and the measured
i vj = 0, ∀i (cid:54)= j) then M = I3.

directions are orthogonal (vT
The cost function Emes becomes

˙y(cid:48) = kI AiDix(cid:48) + Ω(cid:48) × y(cid:48),

for i = 1, . . . , 4.

Emes = 3 − tr( ˜RM ) = tr(I3 − ˜R) = Etr.

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

11

In this case, the explicit complementary ﬁlter (Eqn’s 32) and
the passive complementary ﬁlter (Eqn’s 13) are identical. (cid:164)
Remark: It is possible to weaken the assumptions in Theo-
rem 5.1 to allow any choice of gains ki and any structure of the
matrix M0 and obtain analogous results. The case where all
three eigenvalues of M0 are equal is equivalent to the passive
complementary ﬁlter scaled by a constant. The only other case
where n > 2 has

M0 = U0diag(λ1, λ1, λ2)U T
0

Eqn’s 29 (for a single measurement v1 = va) and Eq. 11b. Let
( ˆR(t), ˆb(t)) denote the solution of Eqn’s 32. Assume that Ω(t)
is a bounded, absolutely continuous signal and (Ω(t), va(t))
are asymptotically independent (see §II-A). Deﬁne
˜Rv0a = −1, ˜b = 0}.

U1 = {( ˜R, ˜b) : vT
0a

Then:

1) The set U1 is forward invariant and unstable under the

closed-loop ﬁlter dynamics.

2) The estimate (ˆva, ˆb) is locally exponentially stable to

for λ1 > λ2 ≥ 0. (Note that the situation where n = 1
is considered in Corollary 5.2.) It can be shown that any
symmetry ¯R∗ = exp(πa∗×) with a∗ ∈ span{v01, v02} satisﬁes
ωmes ≡ 0 and it is relatively straightforward to verify that this
set is forward invariant under the closed-loop ﬁlter dynamics.
This invalidates part i) of Theorem 5.1 as stated, however,
it can be shown that the new forward invariant points are
unstable as expected. To see this, note that any ( ¯R∗, ¯b∗) in
this set corresponds to the minimal cost of Emes on U0.
Consequently, any neighbourhood of ( ¯R∗, ¯b∗) contains points
( ˜R, ˜b) such that V ( ˜R, ˜b) < V ( ¯R∗, ¯b∗) and the Lyapunov
decrease condition ensures instability. There is still a separate
isolated unstable equilibrium in U0, and the stable equilibrium,
that must be treated in the same manner as undertaken in the
formal proof of Theorem 5.1. Following through the proof
yields analogous results to Theorem 5.1 for arbitrary choice
(cid:164)
of gains {ki}.
The two typical measurements obtained from an IMU unit
are estimates of the gravitational, a, and magnetic, m, vector
ﬁelds

va = RT a0
|a0|

,

vm = RT m0
|m0|

.

In this case, the cost function Emes becomes

Emes = k1(1 − (cid:104)ˆva, va(cid:105)) + k2(1 − (cid:104)ˆvm, vm(cid:105))

The weights k1 and k2 are introduced to weight the conﬁdence
in each measure. In situations where the IMU is subject
to high magnitude accelerations (such as during takeoff or
landing manoeuvres) it may be wise to reduce the relative
weighting of the accelerometer data (k1 << k2) compared to
the magnetometer data. Conversely, in many applications the
IMU is mounted in the proximity to powerful electric motors
and their power supply busses leading to low conﬁdence in
the magnetometer readings (choose k1 >> k2). This is a very
common situation in the case of mini aerial vehicles with
electric motors. In extreme cases the magnetometer data is
unusable and provides motivation for a ﬁlter based solely on
accelerometer data.

A. Estimation from the measurements of a single direction

Let va be a measured body ﬁxed frame direction associated
with a single inertial direction v0a, va = RT v0a. Let ˆva be an
estimate ˆva = ˆRT v0a. The error considered is

Emes = 1 − tr( ˜RM ); M = RT v0avT

0aR

Corollary 5.2: Consider the rotation kinematics Eq. 4 for a
time-varying R(t) ∈ SO(3) and with measurements given by

(va, b).

3) For almost all initial conditions ( ˜R0, ˜b0) (cid:54)∈ U1 then

(ˆva, ˆb) converges to the trajectory (va(t), b).
Proof: The dynamics of ˆva are given by

˙ˆva = −(Ω + ˜b + kP va × ˆva) × ˆva

(40)

Deﬁne the following storage function
1
kI

V = Emes +

˜b2.

The derivative of V is given by

˙V = −kP ||(va × ˆRT v0a)×||2 = −2kP |va × ˆva|2
The Lyapunov-like function V derivative is negative semi-
deﬁnite ensuring that ˜b is bounded and va × ˆva → 0. The
set va × ˆv∗a = 0 is characterised by va = ±ˆv∗a and thus

∗ava = ±1 = vT
ˆvT
0a

ˆRT

∗ Rv0a = vT
0a

˜R∗v0a.

Consider a trajectory (ˆv∗a(t), b∗(t)) that satisﬁes the ﬁlter

dynamics and for which ˆv∗a = ±va for all time. One has
d
dt

(va × ˆv∗a) = 0

= −(Ω × va) × ˆv∗a − va × (Ω × ˆv∗a)
− va × (˜b∗ × ˆv∗a) − kP va × ((va × ˆv∗a) × ˆv∗a)
= ±va × (˜b∗ × va) = 0.

Differentiating this expression again one obtains

(cid:179)
(Ω × va) × (˜b∗ × va) + va × (˜b∗ × (Ω × va))

(cid:180)

= 0

Since the signals Ω and va are asymptotically independent it
follows that the functional expression on the left hand side is
degenerate. This can only hold if ˜b∗ ≡ 0. For ˆv∗a = −va, this
set of trajectories is characterised by the deﬁnition of U1. It is
straightforward to adapt the arguments in Theorems 4.1 and
4.2 to see that this set is forward invariant. Note that for ˜b∗ = 0
then V = Emes. It is direct to see that (ˆv∗a(t), b∗(t)) lies on a
local maximum of Emes and that any neighbourhood contains
points such that the full Lyapunov function V is strictly less
than its value on the set U1. This proves instability of U1 and
completes part i) of the corollary.

The proof of part ii) and part iii) is analogous to the proof

of Theorem 5.1 (see also [15]).

An important aspect of Corollary 5.2 is the convergence of
the bias terms in all degrees of freedom. This ensures that, for
a real world system, the drift in the attitude estimate around
the unmeasured axis v0a will be driven asymptotically by a
zero mean noise process rather than a constant bias term. This
makes the proposed ﬁlter a practical algorithm for a wide range
of MAV applications.

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

12

VI. EXPERIMENTAL RESULTS

In this section, we present experimental results to demon-

strate the performance of the proposed observers.

Experiments were undertaken on two real platforms to
demonstrate the convergence of the attitude and gyro bias
estimates.

1) The ﬁrst experiment was undertaken on a robotic ma-
nipulator with an IMU mounted on the end effector and
supplied with synthetic estimates of the magnetic ﬁeld
measurement. The robotic manipulator was programmed
to simulate the movement of a ﬂying vehicle in hover-
ing ﬂight regime. The ﬁlter estimates are compared to
orientation measurements computed from the forward
kinematics of the manipulator. Only the passive and
direct complimentary ﬁlters were run on this test bed.
2) The second experiment was undertaken on the VTOL
MAV HoverEye c(cid:176) developed by Bertin Technologies
(Figure 1). The VTOL belongs to the class of ‘sit
on tail’ ducted fan VTOL MAV, like the iSTAR9 and
Kestrel developed respectively by Allied Aerospace [41]
and Honeywell [42]. It was equipped with a low-cost
IMU that consists of 3-axis accelerometers and 3-axis
gyroscopes. Magnetometers were not integrated in the
MAV due to perturbations caused by electrical motors.
The explicit complementary ﬁlter was used in this ex-
periment.

For both experiments the gains of the proposed ﬁlters were
chosen to be: kP = 1rad.s−1 and kI = 0.3rad.s−1. The inertial
data was acquired at rates of 25Hz for the ﬁrst experiment and
50Hz for the second experiment. The quaternion version of the
ﬁlters (Appendix B) were implemented with ﬁrst order Euler
numerical integration followed by rescaling to preserve the
unit norm condition.

Experimental results for the direct and passive versions of
the ﬁlter are shown in Figures 6 and 7. In Figure 6 the only
signiﬁcant difference between the two responses lies in the
initial transient responses. This is to be expected, since both
ﬁlters will have the same theoretical asymptotic performance.
In practice, however, the increased sensitivity of the direct
ﬁlter to noise introduced in the computation of the measured
rotation Ry is expected to contribute to slightly higher noise
in this ﬁlter compared to the passive.

The response of the bias estimates is shown in Figure 7.
Once again the asymptotic performance of the ﬁlters is similar
after an initial transient. From this ﬁgure it is clear that the
passive ﬁlter displays slightly less noise in the bias estimates
than for the direct ﬁlter (note the different scales in the y-axis).

Figures 8 and 9 relate to the second experiment. The
experimental ﬂight of the MAV was undertaken under remote
control by an operator. The experimental ﬂight plan used was:
First, the vehicle was located on the ground, initially headed
toward ψ(0) = 0. After take off, the vehicle was stabilized
in hovering condition, around a ﬁxed heading which remains
close the initial heading of the vehicle on the ground. Then,
the operator engages a (cid:39) 90
-left turn manoeuvre, returns
to the initial heading, and follows with a (cid:39) 90
-right turn

o

o

Fig. 6. Euler angles from direct and passive complementary ﬁlters

Fig. 7. Bias estimation from direct and passive complementary ﬁlters

manoeuvre, before returning to the initial heading and landing
the vehicle. After landing, the vehicle is placed by hand at its
initial pose such that ﬁnal and initial attitudes are the identical.
Figure 8 plots the pitch and roll angles (φ, θ) estimated
directly from the accelerometer measurements against
the
estimated values from the explicit complementary ﬁlter. Note
the large amounts of high frequency noise in the raw attitude
estimates. The plots demonstrate that
the ﬁlter is highly
successful in reconstructing the pitch and roll estimates.

Figure 9 presents the gyros bias estimation verses the
predicted yaw angle (φ) based on open loop integration of the
gyroscopes. Note that the explicit complementary ﬁlter here
is based solely on estimation of the gravitational direction.
Consequently, the yaw angle is the indeterminate angle that is
not directly stabilised in Corollary 5.2. Figure 9 demonstrates
that the proposed ﬁlter has successfully identiﬁed the bias of
the yaw axis gyro. The ﬁnal error in yaw orientation of the
microdrone after landing is less than 5 degrees over a two
minute ﬂight. Much of this error would be due to the initial
transient when the bias estimate was converging. Note that the

0102030405060−50050roll φ (°)φmeasureφpassiveφdirect0102030405060−60−40−200204060pitch θ (°)θmeasureθpassiveθdirect0102030405060−100−50050100150200yaw ψ (°)time (s)ψmeasureψpassiveψdirect0102030405060−20−10010best−direct (°/s)time (s)b1b2b30102030405060−50510best−passive (°/s)time (s)b1b2b3IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

13

second part of the ﬁgure indicates that the bias estimates are
not constant. Although some of this effect may be numerical,
it is also to be expected that the gyro bias on low cost IMU
systems are highly susceptible to vibration effects and changes
in temperature. Under ﬂight conditions changing engine speeds
and aerodynamic conditions can cause quite fast changes in
gyro bias.

Fig. 8. Estimation results of the Pitch and roll angles.

into the estimator frame of reference. The resulting ob-
server kinematics are considerably simpliﬁed and avoid
coupling of constructed attitude error into the predictive
velocity update.

Explicit complementary ﬁlter: A reformulation of the passive
complementary ﬁlter in terms of direct vectorial measure-
ments, such as gravitational or magnetic ﬁeld directions
obtained for an IMU. This observer does not require on-
line algebraic reconstruction of attitude and is ideally
suited for implementation on embedded hardware plat-
forms. Moreover, the ﬁlter remains well conditioned in
the case where only a single vector direction is measured.

The performance of the observers was demonstrated in a
suite of experiments. The explicit complementary ﬁlter is now
implemented as the primary attitude estimation system on
several MAV vehicles world wide.

APPENDIX A
A REVIEW OF COMPLEMENTARY FILTERING

Complementary ﬁlters provide a means to fuse multiple
independent noisy measurements of the same signal
that
have complementary spectral characteristics [11]. For example,
consider two measurements y1 = x + µ1 and y2 = x + µ2 of a
signal x where µ1 is predominantly high frequency noise and
µ2 is a predominantly low frequency disturbance. Choosing a
pair of complementary transfer functions F1(s) + F2(s) = 1
with F1(s) low pass and F2(s) high pass, the ﬁltered estimate
is given by

ˆX(s) = F1(s)Y1+F2(s)Y2 = X(s)+F1(s)µ1(s)+F2(s)µ2(s).

The signal X(s) is all pass in the ﬁlter output while noise
components are high and low pass ﬁltered as desired. This type
of ﬁlter is also known as distorsionless ﬁltering since the signal
x(t) is not distorted by the ﬁlter [43]. Complementary ﬁlters
are particularly well suited to fusing low bandwidth position
measurements with high band width rate measurements for
ﬁrst order kinematic systems. Consider the linear kinematics

˙x = u.

(41)

Fig. 9. Gyros bias estimation and inﬂuence of the observer on yaw angle.

with typical measurement characteristics

VII. CONCLUSION

This paper presents a general analysis of attitude observer
design posed directly on the special orthogonal group. Three
non-linear observers, ensuring almost global stability of the
observer error, are proposed:
Direct complementary ﬁlter: A non-linear observer posed on
SO(3) that is related to previously published non-linear
observers derived using the quaternion representation of
SO(3).

Passive complementary ﬁlter: A non-linear ﬁlter equation that
takes advantage of the symmetry of SO(3) to avoid
transformation of the predictive angular velocity term

yx = L(s)x + µx,

yu = u + µu + b(t)

(42)

where L(s) is low pass ﬁlter associated with sensor character-
istics, µ represents noise in both measurements and b(t) is a
deterministic perturbation that is dominated by low-frequency
content. Normally the low pass ﬁlter L(s) ≈ 1 over the
frequency range on which the measurement yx is of interest.
The rate measurement is integrated yu
s to obtain an estimate of
the state and the noise and bias characteristics of the integrated
signal are dominantly low frequency effects. Choosing

F1(s) =

C(s)
C(s) + s

F2(s) = 1 − F1(s) =

s
C(s) + s

5060708090100110120130140−100−50050100time (s)φ (deg)φ (yaw angle) from gyrosφ from the estimator5060708090100110120130140−0.04−0.0200.020.04time (s)b (rd/s)bxbybzIEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

14

with C(s) all pass such that L(s)F1(s) ≈ 1 over the band-
width of L(s). Then

Abusing notation for the noise processes, and using ˜x = (x −
ˆx), and ˜b = (b0 − ˆb), one has

ˆX(s) ≈ X(s) + F1(s)µx(s) +

µu(s) + b(s)
C(s) + s

d
dt

L = −kP |˜x|2 − µu ˜x + µx(˜b − k˜x)

Note that even though F2(s) is high pass the noise µu(s)+b(s)
is low pass ﬁltered. In practice, the ﬁlter structure is imple-
mented by exploiting the complementary sensitivity structure
of a linear feedback system subject
to load disturbance.
Consider the block diagram in Figure 10. The output ˆx can

In the absence of noise one may apply Lyapunov’s direct
method to prove convergence of the state estimate. LaSalle’s
principal of invariance may be used to show that ˆb → b0.
When the underlying system is linear, then the linear form of
the feedback and adaptation law ensure that the closed-loop
system is linear and stability implies exponential stability.

Fig. 10. Block diagram of a classical complementary ﬁlter.

be written

ˆx(s) =

C(s)
s + C(s)

yx(s) +

= T (s)yx(s) + S(s)

yu(s)
s

s
C(s) + s
yu(s)
s

where S(s) is the sensitivity function of the closed-loop
system and T (s) is the complementary sensitivity. This archi-
tecture is easy to implement efﬁciently and allows one to use
classical control design techniques for C(s) in the ﬁlter design.
The simplest choice is a proportional feedback C(s) = kP . In
this case the closed-loop dynamics of the ﬁlter are given by
˙ˆx = yu + kP (yx − ˆx).

(43)

s+kP

and F2(s) = s

The frequency domain complementary ﬁlters associated with
this choice are F1(s) = kP
. Note that
s+kP
the crossover frequency for the ﬁlter is at kP rad.s−1. The gain
kP is typically chosen based on the low pass characteristics
of yx and the low frequency noise characteristics of yu to
choose the best crossover frequency to tradeoff between the
two measurements. If the rate measurement bias, b(t) = b0,
is a constant then it is natural to add an integrator to the
compensator to make the system type I
kI
s

C(s) = kP +

(44)

.

A type I system will reject the constant load disturbance b0
from the output. Gain design for kP and kI is typically based
on classical frequency design methods. The non-linear devel-
opment in the body of the paper requires a Lyapunov analysis
of closed-loop system Eq. 43. Applying the PI compensator,
Eq. 44, one obtains state space ﬁlter with dynamics
˙ˆb = −kI (yx − ˆx)

˙ˆx = yu − ˆb + k(yx − ˆx),

The negative sign in the integrator state is introduced to
indicate that the state ˆb will cancel the bias in yu. Consider
the Lyapunov function
1
2

|x − ˆx|2 +

|b0 − ˆb|2

L =

1
2kI

APPENDIX B
QUATERNION REPRESENTATIONS OF OBSERVERS

The unit quaternion representation of rotations is commonly
used for the realisation of algorithms on SO(3) since it offers
considerable efﬁciency in code implementation. The set of
quaternions is denoted Q = {q = (s, v) ∈ R × R3 : |q| = 1}.
The set Q is a group under the operation

(cid:34)

q1 ⊗ q2 =

(cid:35)

s1s2 − vT
s1v2 + s2v1 + v1 × v2

1 v2

with identity element 1 = (1, 0, 0, 0). The group of quater-
nions are homomorphic to SO(3) via the map

F : Q → SO(3), F (q) := I3 + 2sv× + 2v2
×

This map is a two to one mapping of Q onto SO(3) with
kernel {(1, 0, 0, 0), (−1, 0, 0, 0)}, thus, Q is locally isomorphic
to SO(3) via F . Given R ∈ SO(3) such that R = exp(θa×)
then F −1(R) = {±(cos( θ
2 ), sin( θ
2 )a)} Let Ω ∈ {A} de-
note a body-ﬁxed frame velocity, then the pure quaternion
p(Ω) = (0, Ω) is associated with a quaternion velocity.
Consider the rotation kinematics on SO(3) Eq. 4, then the
associated quaternion kinematics are given by

˙q =

1
2

q ⊗ p(Ω)

(45)

Let qy ≈ q be a low frequency measure of q, and Ωy ≈ Ω + b
(for constant bias b) be the angular velocity measure. Let ˆq
denote the observer estimate and quaternion error ˜q

˜q = ˆq−1 ⊗ q =

(cid:34)

(cid:35)

˜s

˜v

Note that

2˜s˜v = 2 cos(θ/2) sin(θ/2)a =

1
2

(sin θ)a = vex(Pa( ˜R))

where (θ, a) is the angle axis representation of ˜R = F (˜q).
The quaternion representations of the observers proposed in
this paper are:
Direct complementary ﬁlter (Eq. 12):

ˆq ⊗ p( ˜R(Ωy − ˆb) + 2kP ˜s˜v)

1
˙ˆq =
2
˙ˆb = −2kI ˜s˜v

(46a)

(46b)

yuC(s)-++Rˆxyx+IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

15

Passive complementary ﬁlter (Eq. 13):

ˆq ⊗ p(Ωy − ˆb + 2kP ˜s˜v)

1
˙ˆq =
2
˙ˆb = −2kI ˜s˜v

Explicit complementary ﬁlter (Eq. 32):

(cid:33)

ωmes = − vex

(vi ˆvi

T − ˆvivT
i )

(cid:195)

n(cid:88)

i=1

ki
2

ˆq ⊗ p(Ωy − ˆb + kP ωmes)

1
˙ˆq =
2
˙ˆb = −kI ωmes

(47a)

(47b)

(48a)

(48b)

(48c)

The error dynamics associated with the direct ﬁlter expressed
in the quaternion formulation are

˙˜q = −

1
2

(cid:179)

(cid:180)
p(˜b + kP ˜s˜v) ⊗ ˜q

.

(49)

The error dynamics associated with the passive ﬁlter are

(cid:179)

(cid:180)
˜q ⊗ p(Ω) − p(Ω) ⊗ ˜q − p(˜b + kP ˜s˜v) ⊗ ˜q

.

(50)

˙˜q =

1
2

There is a ﬁfteen year history of using the quaternion rep-
resentation and Lyapunov design methodology for ﬁltering
on SO(3) (for example cf. [9], [30], [32]). To the authors
knowledge the Lyapunov analysis in all cases has been based
around the cost function

Φ(˜q) = (|˜s| − 1)2 + |˜v|2.

Due to the unit norm condition it is straightforward to show
that

Φ(˜q) = 2(1 − |˜s|) = 2 (1 − | cos(θ/2)|)

The cost function proposed in this paper is Etr = (1 −
cos(θ)) (Eq. 3). It is straightforward to see that the quadratic
approximation of both cost functions around the point θ = 0 is
the quadratic θ2/2. The quaternion cost function Φ, however,
is non-differentiable at the point θ = ±π while the cost
tr(I − ˜R) has a smooth local maxima at this point. To the
authors understanding, all quaternion ﬁlters in the published
literature have a similar ﬂavour that dates back to the seminal
work of Salcudean [32]. The closest published work to that
undertaken in the present paper was published by Thienel in
her doctoral dissertation [44] and transactions paper [30]. The
ﬁlter considered by Thienel et al. is given by

ˆq ⊗ p( ˜R(Ωy − ˆb + kP sgn(˜s)˜v))

1
2

˙ˆq =
˙ˆb = −kI sgn(˜s)˜v

(51a)

(51b)

dt |˜s| = sgn(˜s) d

The sgn(˜s) term enters naturally in the ﬁlter design from the
differential, d
dt ˜s, of the absolute value term
in the cost function Φ, during the Lyapunov design process.
Consider the observer obtained by replacing sgn(˜s) in Eqn’s 51
by 2˜s. Note that with this substitution, Eq. 51b is transformed
into Eq. 46b. To show that Eq. 51a transforms to Eq. 46a it is
sufﬁcient to show that ˜R˜v = ˜v. This is straightforward from

2˜s ˜R˜v = ˜R(2˜s˜v) = ˜Rvex(Pa( ˜R))

= vex( ˜RPa( ˜R) ˜RT ) = vex(Pa( ˜R)) = 2˜s˜v

This demonstrates that the quaternion ﬁlter Eqn’s 51 is ob-
tained from the standard form of the complimentary ﬁlter
proposed Eq. 12 with the correction term Eq. 12c replaced
by

ωq = sgn(˜s)˜v,

˜q ∈ F −1( ˆRT R).

Note that the correction term deﬁned in Eq. 12c can be written
ω = 2˜s˜v. It follows that

ωq =

sgn(˜s)
2˜s

ω

The correction term for the two ﬁlters varies only by the
positive scaling factor sgn(˜s)/(2˜s). The quaternion correction
term ωq is not well deﬁned for ˜s = 0 (where θ = ±π) and
these points are not well deﬁned in the ﬁlter dynamics Eq. 51.
It should be noted, however, that |ωq| is bounded at ˜s = 0
and, apart from possible switching behaviour, the ﬁlter can
still be implemented on the remainder of SO(3) × R3. An
argument for the use of the correction term ωq is that the
resulting error dynamics strongly force the estimate away from
the unstable set U (cf. Eq. 14). An argument against its use is
that, in practice, such situations will only occur due to extreme
transients that would overwhelm the bounded correction term
ωq in any case, and cause the numerical implementation of
the ﬁlter to deal with a discontinuous argument. In practice,
it is an issue of little signiﬁcance since the ﬁlter will general
work sufﬁciently well to avoid any issues with the unstable
set U. For ˜s → 1, corresponding to θ = 0, the correction term
ωq scales to a factor of 1/2 the correction term ω. A simple
scaling factor like this is compensated for the in choice of ﬁlter
gains kP and kI and makes no difference to the performance
of the ﬁlter.

REFERENCES

[1] J. Vaganay, M. Aldon, and A. Fournier, “Mobile robot attitude estimation
by fusion of inertial data,” in Proceedigns of the IEEE Internation
Conference on Robotics and Automation ICRA, vol. 1, 1993, pp. 277–
282.

[2] E. Foxlin, M. Harrington, and Y. Altshuler, “Miniature 6-DOF inertial
system for tracking HMD,” in Proceedings of the SPIE, vol. 3362,
Orlando, Florida, 1998, pp. 214–228.

[3] J. Balaram, “Kinematic observers for articulated robers,” in Proceddings
of the IEEE International Conference on Robotics and Automation,
2000, pp. 2597–2604.

[4] J. L. Marins, X. Yun, E. R. Backmann, R. B. McGhee, and M. Zyda, “An
extended kalman ﬁlter for quaternion-based orientation estimation using
marg sensors,” in IEEE/RSJ International Conference on Intelligent
Robots and Systems, 2001, pp. 2003–2011.

[5] E. Lefferts, F. Markley, and M. Shuster, “Kalman ﬁltering for spacecraft
attitude estimation,” AIAA Journal of Guidance, Control and Navigation,
vol. 5, no. 5, pp. 417–429, September 1982.

[6] B. Barshan and H. Durrant-Whyte, “Inertial navigation systems for
mobile robots,” IEEE Transactions on Robotics and Automation, vol. 44,
no. 4, pp. 751–760, 1995.

[7] M. Zimmerman and W. Sulzer, “High bandwidth orientation measure-
ment and control ased on complementary ﬁltering,” in Proceedings of
Symposium on Roboitcs and Control, SYROCO, Vienna, Austria, 1991.
[8] A.-J. Baerveldt and R. Klang, “A low-cost and low-weight attitude
estimation system for an autonomous helicopter,” Intelligent Engineering
Systems, 1997.

[9] B. Vik and T. Fossen, “A nonlinear observer for gps and ins integration,”
teh IEEE Conference on Decisioin and Control,

in Proceedings of
Orlando, Florida, USA, December 2001, pp. 2956–2961.

[10] H. Rehbinder and X. Hu, “Nonlinear state estimation for rigid body
motion with low-pass sensors,” Systems and Control Letters, vol. 40,
no. 3, pp. 183–190, 2000.

IEEE TRANSACTIONS ON AUTOMATIC CONTROL, VOL. XX, NO. XX, MONTH YEAR

16

[11] E. R. Bachmann, J. L. Marins, M. J. Zyda, R. B. Mcghee, and X. Yun,
“An extended kalman ﬁlter for quaternion-based orientation estimation
using MARG sensors,” 2001.

[12] J.-M. Pﬂimlin, T. Hamel, P. Soueeres, and N. Metni, “Nonlinear attitude
and gyroscoples bias estimation for a VTOL UAV,” in Proceedings of
the IFAC world congress, 2005.

[13] H. Rehbinder and X. Hu, “Drift-free attitude estimation for accelerated

rigid bodies,” Automatica, 2004.

[14] N. Metni, J.-M. Pﬂimlin, T. Hamel, and P. Soueeres, “Attitude and gyro
bias estimation for a ﬂying UAV,” in IEEE/RSJ International Conference
on Intelligent Robots and Systems, August 2005, pp. 295–301.

[36] T. Hamel and R. Mahony, “Attitude estimation on SO(3) based on
direct inertial measurements,” in International Conference on Robotics
and Automation, ICRA2006, 2006.

[37] S. Bonnabel and P. Rouchon, Control and Observer Design for Non-
linear Finite and Inﬁnite Dimensional Systems, ser. Lecture Notes in
Control and Information Sciences. Springer-Verlag, 2005, vol. 322, ch.
On Invariant Observers, pp. 53–67.

[38] S. Bonnabel, P. Martin, and P. Rouchon, “A non-linear symmetry-
preserving observer for velocity-aided inertial navigation,” in American
Control Conference, Proceedings of the, June 2006, pp. 2910–2914.

[39] R. Murray, Z. Li, and S. Sastry, A mathematical introduction to robotic

[15] ——, “Attitude and gyro bias estimation for a VTOL UAV,” in Control

manipulation. CRC Press, 1994.

Engineering Practice, 2006, p. to appear.

[40] H. Khalil, Nonlinear Systems 2nd edition. New Jersey: Prentice Hall,

[16] J. Lobo and J. Dias, “Vision and inertial sensor cooperation using gravity
as a vertical reference,” IEEE Transactions on Pattern Analysis and
Machine Intelligence, vol. 25, no. 12, pp. 1597–1608, Dec. 2003.
[17] H. Rehbinder and B. Ghosh, “Pose estimation using line-based dynamic
vision and inertial sensors,” IEEE Transactions on Automatic Control,
vol. 48, no. 2, pp. 186–199, Feb. 2003.

[18] J.-H. Kim and S. Sukkarieh, “Airborne simultaneous localisation and
map building,” in Proceedings of the IEEE International Conference on
Robotics and Automation, Taipei, Taiwan, September 2003, pp. 406–411.
[19] P. Corke, J. Dias, M. Vincze, and J. Lobo, “Integration of vision and
inertial sensors,” in Proceedings of the IEEE International Conference
on Robotics and Automation, ICRA ’04., ser. W-M04, Barcellona, Spain,
April 2004, full day Workshop.

[20] R. Phillips and G. Schmidt, System Implications and Innovative Ap-
plications of Satellite Navigation, ser. AGARD Lecture Series 207.
<help@sti.nasa.gov>: NASA Center for Aerospace Information,
1996, vol. 207, ch. GPS/INS Integration, pp. 0.1–0.18.

[21] D. Gebre-Egziabher, R. Hayward, and J. Powell, “Design of multi-sensor
attitude determination systems,” IEEE Transactions on Aerospace and
Electronic Systems, vol. 40, no. 2, pp. 627–649, April 2004.

[22] J. L. Crassidis, F. L. Markley, and Y. Cheng, “Nonlinear attitude ﬁltering
methods,” Journal of Guidance, Control,and Dynamics, vol. 30, no. 1,
pp. 12–28, January 2007.

[23] M. Jun, S. Roumeliotis, and G. Sukhatme, “State estimation of an
autonomous helicopter using Kalman ﬁltering,” in Proc. 1999 IEEE/RSJ
International Conference on Robots and Systems (IROS 99), 1999.
[24] G. S. Sukhatme and S. I. Roumeliotis, “State estimation via sensor
modeling for helicopter control using an indirect kalman ﬁlter,” 1999.
[25] G. S. Sukhatme, G. Buskey, J. M. Roberts, P. I. Corke, and S. Sari-
palli, “A tale of two helicopters,” in IEEE/RSJ, International Robots
and Systems,, Los Vegas, USA, Oct. 2003, pp. 805–810, <http://www->
robotics.usc.edu/ srik/papers/iros2003.pdf.

[26] J. M. Roberts, P. I. Corke, and G. Buskey, “Low-cost ﬂight control
system for small autonomous helicopter,” in Australian Conference on
Robotics and Automation, Auckland, 27-29 Novembre, 2002, pp. 71–76.
[27] P. Corke, “An inertial and visual sensing system for a small autonomous
helicopter,” J. Robotic Systems, vol. 21, no. 2, pp. 43–51, February 2004.
[28] G. Creamer, “Spacecraft attitude determination using gyros and quater-
nion measurements,” The Journal of Astronautical Sciences, vol. 44,
no. 3, pp. 357–371, July 1996.

[29] D. Bayard, “Fast observers for spacecraft pointing control,” in Proceed-
ings of the IEEE Conference on Decision and Control, Tampa, Florida,
USA, 1998, pp. 4702–4707.

[30] J. Thienel and R. M. Sanner, “A coupled nonlinear spacecraft attitude
controller and observer with an unknow constant gyro bias and gyro
noise,” IEEE Transactions on Automatic Control, vol. 48, no. 11, pp.
2011 – 2015, Nov. 2003.

[31] G.-F. Ma and X.-Y. Jiang, “Spacecraft attitude estimation from vector
measurements using particle ﬁlter,” in Proceedings of the fourth Inter-
nation conference on Machine Learning and Cybernetics, Guangzhou,
China, August 2005, pp. 682–687.

[32] S. Salcudean, “A globally convergent angular velocity observer for rigid
body motion,” IEEE Trans. Auto. Cont., vol. 36, no. 12, pp. 1493–1497,
Dec. 1991.

[33] O. Egland and J. Godhaven, “Passivity-based adaptive attitude control
of a rigid spacecraft,” IEEE Transactions on Automatic Control, vol. 39,
pp. 842–846, April 1994.

[34] A. Tayebi and S. McGilvray, “Attitude stabilization of a four-rotor aerial
robot: Theory and experiments,” To appear in IEEE Transactions on
Control Systems Technology, 2006.

[35] R. Mahony, T. Hamel, and J.-M. Pﬂimlin, “Complimentary ﬁlter design
on the special orthogonal group SO(3),” in Proceedings of the IEEE
Conference on Decision and Control, CDC05. Seville, Spain: Institue
of Electrical and Electronic Engineers, December 2005.

1996.

[41] L. Lipera, J. Colbourne, M. Tischler, M. Mansur, M. Rotkowitz, and
P. Patangui, “The micro craft istar micro-air vehicle: Control system
design and testing,” in Proc. of the 57th Annual Forum of the American
Helicopter Society, Washington DC, USA, May 2001, pp. 1–11.
[42] J. Fleming, T. Jones, P. Gelhausen, and D. Enns, “Improving control
system effectiveness for ducted fan vtol uavs operating in crosswinds,”
in Proc. of the 2nd “Unmanned Unlimited” System. San Diego, USA:
AIAA, September 2003.

[43] R. G. Brown and P. Y. C. Hwang, Introduction to Random Signals and
Applied Kalman Filtering, 2nd ed. New York, NY: John Wiley and
Sons, 1992.

[44] J. Thienel, “Nonlinear observer/controller dsigns for spacecraft attitude
control systems with uncalibrated gyros,” PhD, Faculty of the Graduate
School of the University of Maryland, Dep. Aerospace Engineering,,
2004.

Robert Mahony is currently a reader in the De-
partment of Engineering at the Australian National
University. He received a PhD in 1995 (systems
engineering) and a BSc in 1989 (applied mathemat-
ics and geology) both from the Australian National
University. He worked as a marine seismic geo-
physicist and an industrial research scientist before
completing a two year postdoctoral fellowship in
France and a two year Logan Fellowship at Monash
University in Australia. He has held his post at ANU
since 2001. His research interests are in non-linear
control theory with applications in robotics, geometric optimisation techniques
and learning theory.

Tarek Hamel received his Bachelor of Engineering
from the University of Annaba, Algeria, in 1991.
He received his PhD in Robotics in 1995 from the
University of technology Compi`egne (UTC), France.
After two years as a research assistant at the UTC,
he joined the “Centre d’Etudes de M`ecanique d’Iles
de France” in 1997 as an associate professor. Since
2003, he has been a Professor at the I3S UNSA-
CNRS laboratory of the University of Nice-Sophia
Antipolis, France. His research interests include non-
linear control theory, estimation and vision-based
control with applications to Unmanned Aerial Vehicles and Mobile Robots.

Jean-Michel Pﬂimlin graduated from Supaero, the
French Engineering school in Aeronautics and Space
in 2003. He conducted his Ph.D. research at the Lab-
oratory for Analysis and Architecture of Systems,
LAAS-CNRS, in Toulouse, France and received the
PhD degree in automatic control from Supaero in
2006. He is currently working at Navigation de-
partment of Dassault Aviation in Saint Cloud, Paris.
His research interests include nonlinear control and
ﬁltering, advanced navigation systems and their ap-
plications to Unmanned Aerial Vehicles.
