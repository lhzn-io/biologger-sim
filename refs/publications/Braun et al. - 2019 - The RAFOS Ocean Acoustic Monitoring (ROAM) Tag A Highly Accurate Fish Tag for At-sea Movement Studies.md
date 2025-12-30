North Pacific Anadromous Fish Commission
Technical Report No. 15: 168–170, 2019

The RAFOS Ocean Acoustic Monitoring (ROAM) Tag: A Highly Accurate Fish Tag
for At-sea Movement Studies

Camrin D. Braun1, Godi Fischer2, H. Thomas Rossby3, Heather Furey4, Amy Bower4, and Simon R. Thorrold5

1School of Aquatic and Fishery Sciences, University of Washington, Seattle, WA, USA

2Department of Electrical, Computer and Biomedical Engineering, University of Rhode Island, Kingston, RI, USA

3Graduate School of Oceanography, University of Rhode Island, Narragansett, RI, USA

4Physical Oceanography, Woods Hole Oceanographic Institution, Woods Hole, MA, USA

5Biology Department, Woods Hole Oceanographic Institution, Woods Hole, MA, USA

Keywords: animal telemetry, ocean observing, acoustics, oceanography

Introduction

Animal migrations are some of the most fascinating and impressive biological phenomena on the planet.

Nonetheless, until recently, marine ecologists have known remarkably little about the specific movements of large
pelagic fishes due to the logistic challenges of tracking fish in a vast, largely opaque ocean.  Light-level geolocation
techniques using current generation pop-up satellite archival transmitting (PSAT) tags generally exhibit poor
accuracy (±100–200 km; ~10,000 km2) even under best-case situations when movements are confined to surface
waters (< 100 m) during daytime hours (Braun et al. 2015, 2018).  Poor accuracy has, in turn, led to a paucity of
mechanistic studies addressing the mechanisms influencing at-sea habitat use by salmonids.  Similarly, identifying
the location and cause of ocean-phase mortality remains a critical question for improving salmon management and
conservation efforts.  This knowledge is critical as we continue to lean heavily on marine-capture fisheries to sustain
human populations worldwide while experiencing drastic changes in the Earth’s climate and oceans.

We are developing a new satellite archival tag technology—the RAFOS Ocean Acoustic Monitoring
(ROAM) tag—to solve both accuracy and depth constraints inherent in conventional PSAT tags that will provide
accurate geolocations of fish throughout the water column across ocean basins.

Fig. 1.  Sound speed profile for the region indicating the deep sound channel used to propagate sound, and an
example RAFOS array used to study deep circulation in the Gulf of Mexico using RAFOS floats (from Hamilton
et al. 2018).

All correspondence should be addressed to C. Braun.
email: <cbraun@apl.uw.edu>
doi:10.23849/npafctr15/168.170.

168

Braun et al.                                                                                                                                                                      Technical Report No. 15

Proven oceanographic instruments and infrastructure: the RAFOS system

The technical approach of RAFOS1 builds on decades of research and development for tracking ocean currents

by means of subsurface drifters capable of receiving sound (Rossby et al. 1986).

RAFOS float-tracking networks have been used to study the physical oceanography of several ocean basins

from the Gulf of Mexico (Fig. 1) (Hamilton et al. 2018; Furey et al. 2018) to under-ice environments in the Southern
Ocean (Chamberlain et al. 2018).  These networks rely on moored acoustic transmitting units that emit a unique
acoustic signal.  A hydrophone onboard the RAFOS float detects the sounds from the network, and a triangulation
algorithm uses the differential sound reception from multiple
moorings to calculate position onboard the float (Fig. 2).

Fig. 2.  Differential reception time of acoustic signals from 3 different
sound sources can be used to triangulate a position with error < 1km.

Fig. 3.  Example ROAM tag components and assembled
prototype tag.  Adapted from Rossby et al 2017.

The ROAM Tag

The ROAM tag employs the same acoustic technology and infrastructure that is widely used for tracking

RAFOS oceanographic floats to geolocate fish.  The ROAM tag contains a hydrophone that listens for low
frequency “pongs” from the sound source network and differential reception of these sounds are used to triangulate
tag position.  In other words, the ROAM tag is the reverse of acoustic telemetry systems widely used in aquatic
telemetry today.  In order for this approach to work, we have miniaturized current RAFOS technology through the
development of a new single board receiver and enclosed the tag in a cylindrical housing which functions as the
hydrophone (Fig. 3) that is duty-cycled to match the sound source signals.  We modeled the rest of the tag after pop-
up satellite archival tags by equipping the new micro-printed circuit board (“fish-chip”) with the capability to log
pressure and temperature and added an electronic burn wire for predetermined pop-off and an Argos satellite
transmitter for data recovery through the Argos satellite system as is conventional with animal telemetry technology.
With two 1.5 V batteries the tag can, for example, listen a dozen times per day for two years while also sampling
pressure and temperature every 30 minutes in order to capture vertical movements in the water column (Rossby et
al. 2017).  The fish tag can operate at almost any depth, depending upon the rating of the pressure sensor.  By using
pop-up technology and an Argos transmitter, rather than an archival tag only, the tag will transmit a summarized

1RAFOS is the reverse of the acronym SOFAR (SOund Fixing And Ranging)—which refers to float tracking methodology
that has been reversed since the invention of SOFAR.

169

Braun et al.                                                                                                                                                                      Technical Report No. 15

version of the high-resolution data it collects.  Thus, we will ensure that the tag does not need to be recovered for
data acquisition, making it applicable to a number of species where tag physical recovery rates are typically very
low.

Testing a new fish tag

We recently performed a preliminary field test of this technology in the Mississippi River Delta (USA), which

is a notoriously challenging acoustic environment due to alternating layers of warmer and cooler water as well as
saline and fresh lenses.  Despite the challenges inherent in this environment, we were able to hear acoustic signals as
far away as 60 km (Rossby et al. 2017).  The accuracy of this prediction ranged from 70 m to 560 m which depends
critically on clock accuracy in the tags.  Using standard RAFOS clock error recovery techniques, clock errors can be
kept to a few seconds on yearlong missions.  Our preliminary testing suggests this technology may be able to
accurately locate tagged fish, even at depth, with error bounds (±5 km2) that are unmatched by any current tag
geolocation technique. In addition, long-range transmission testing in RAFOS float studies suggests leveraging the
deep sound channel in the open ocean can render the acoustic source signals detectable by the fish tag up to 1,000
km range.

Additional testing of the prototype ROAM tag is scheduled for 2020 in which we plan to tag an oceanographic

glider and program it to conduct vertical movements through the water column similar to some representative fish
taxa.  Such a test will confirm the range and accuracy of the ROAM tag when idealized fish behavior is added to the
geolocation problem.

Summary

Current technologies are restricted to organisms that frequent the surface layer or photic zone to acquire
position estimates, and accuracy using light geolocation is often ±100-200 km (~10,000 km2).  Our inability to
provide position estimates below the photic zone with existing technologies further inhibits our understanding of
meso- and bathypelagic organisms.  The resulting data from initial deployments are enabling us to assess the
feasibility of this technique for improving position estimation and resolving location at depth that are both beyond
the capability of current animal telemetry technologies.  Once proven, the ROAM tag should provide a
transformative view of fish movements in the global ocean by increasing accuracy of movement studies by ~ 4
orders of magnitude while retaining functionality at depth.  In addition, the ROAM tag will be applicable to all large
and medium-sized pelagic fish species, as it does not require the fish to occupy surface waters to determine accurate
positions.  Using these improvements in location accuracy, ROAM tag deployments will foster in-depth
understanding of biophysical drivers of fish movements (e.g., prey aggregation along fronts or vertically migrating
mesopelagic biota), habitat association (e.g., seamounts), sociality among tagged individuals, and other currently
cryptic behavior (e.g., spawning aggregation and location).  This knowledge will greatly improve our understanding
of data-deficient, commercially valuable species and will have far-reaching impacts on science and industry by
revolutionizing the way we are able to study these species in the open ocean.

REFERENCES

Braun, C.D., G.B. Skomal, S.R. Thorrold, and M.L. Berumen.  2015.  Movements of the reef manta ray (Manta

alfredi) in the Red Sea using satellite and acoustic telemetry.  Mar. Biol. 162: 2351–2362

Braun, C.D., B. Galuardi, and S.R. Thorrold.  2018.   HMMoce: An R package for improved geolocation of

archival-tagged fishes using a hidden Markov method.  Methods Ecol. Evol. 9: 1212–1220

Chamberlain, P.M., L.D. Talley, M.R. Mazloff, K. Speer, A.R. Gray, A. Schwartzman, and S.C. Riser.  2018.

Observing the Ice-Covered Weddell Gyre with Profiling Floats: Position Uncertainties and Correlation
Statistics Special Section: 8383–8410

Furey, H., A. Bower, P. Perez-Brunius, P. Hamilton, and R. Leben.  2018.  Deep eddies in the Gulf of Mexico

observed with floats.  J. Phys. Oceanogr. 48: 2703–2719

Hamilton, P., R. Leben, A. Bower, H. Furey, and P. Pérez-Brunius.  2018.  Hydrography of the Gulf of Mexico

using autonomous floats.  J. Phys. Oceanogr. 48: 773–794

Rossby, T., D. Dorson, and J. Fontaine.  1986.  The RAFOS System.  J. Atmos. Ocean. Technol. 3: 672–679
Rossby, T., G. Fischer, and M.M. Omand.  2017.  A new technology for continuous long-range tracking of fish and

lobster.  Oceanography 30: 36–37

170
