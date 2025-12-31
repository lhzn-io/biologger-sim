SPLASH10 (-F, AF, -BF, -L, -FL)
TDR10 (-DD, -F, -L, -X)
PAT-Mk10 with host version 1.26.3002
User Guide

This user guide will give you all the essential information
needed for interacting with, configuring, and deploying a
Wildlife Computers SPLASH10, TDR10, or PAT-Mk10 tag.

v.201901

Table of Contents
Introduction .......................................................................................................................................... 3

Definitions ............................................................................................................................................. 3

Overview of Functionality .................................................................................................................... 4

Communication .................................................................................................................................... 6

Communications Troubleshooting ..................................................................................................... 8

Programming and Testing ................................................................................................................. 10

Menu Items .......................................................................................................................................... 47

Deployment ........................................................................................................................................ 52

Verifying Function Prior to Deployment .......................................................................................... 52

Sealing the Communications Port ..................................................................................................... 53

Additional Deployment Information ................................................................................................ 53

Data Recovery ..................................................................................................................................... 53

Storing Tags ........................................................................................................................................ 54

Testing After Storage ......................................................................................................................... 54

Technical Specifications ..................................................................................................................... 76

Contacting Wildlife Computers ......................................................................................................... 78

The information contained in these documents is confidential, privileged and only for the information of the intended recipient
and may not be used, published or redistributed without the prior written consent of Wildlife Computers.

2

Introduction
Mk10Host is used to communicate with a variety of Wildlife Computers tags, including all versions of
SPLASH10s, TDR10s, and PAT-Mk10s. Mk10Host is used to set parameters, test sensors and other
hardware components, and download data archived on the tag to your PC.

As might be expected, Mk10Host has to be quite complex to support all the possible permutations of
modules. In order to simplify the user-interface, Mk10Host will only display the parameters
appropriate to the modules present on the connected tag. Therefore, there may be many places
where you cannot access features described in this manual because the necessary module is not
present.

Definitions

•  Host: The software running on a PC which displays information from the tag, downloads data

from the tag, and programs the tag.

•  Tagware: The firmware, or software, running on a tag.
•  Pressure: The unit force per square inch. Can be converted to a depth in sea water.
•  Depth: Distance below the surface.
•  Argos: A satellite-based tracking and data collection system (<www.argos-system.org>).
•  Sample: A single reading from a sensor.
•  Sample rate: Samples measured per unit time. For example, 0.5 samples per second.
•  Sample interval: The time between samples, also the inverse of sample rate. For example a 2

second sample interval is equivalent to sample rate 0.5 samples per second.

•  Duty cycle: Enabling and disabling functionality of the tag during a deployment. This is

typically done to save power or conserve data memory, and thus extend the total duration of a
deployment.

•  Wildlife Computers USB Communications Cable: The Wildlife Computers cable for

communicating with a tag. It provides power and communications.

•  Mk10Host: The name of the host for communicating with the tags covered in this user guide.
•  Wet/Dry sensor: Sensor on a tag which can determine if the tag is in or out of sea water.

Unique settings are required for brackish or freshwater.
.wch: File extension for data and setup files used by Wildlife Computers software.

•
•  GMT: Greenwich Mean Time. Global time standard that is based on the mean position of the

sun at noon at 0 degrees longitude. On Wildlife Computers tags, this is functionally equivalent
to UTC and UT1.

The information contained in these documents is confidential, privileged and only for the information of the intended recipient
and may not be used, published or redistributed without the prior written consent of Wildlife Computers.

3

Overview of Functionality

Operational Modes
Four main operational modes (Appendix F):

Communicating

For configuring tags. The tag is connected via a Wildlife Computers USB communications
cable interface to a PC which is running Mk10Host. In this mode the tag draws power from
the PC through the USB communications cable.

Standby

Deploy

Shut Down

For temporary suspension of tag activities. The tag runs in a very low power mode, and
does not archive samples or transmit. It can stay in this mode for a very long time without
consuming significant battery power. While in this mode the tag will automatically deploy if
it detects a high pressure reading* or a wet sensor reading. It can also be manually
deployed by appropriate application of a magnet.

In this mode, the tag actively collects data and transmits information to Argos, if configured
to do so. The tag should be in this mode when attached to a study animal or other platform
for an experiment. The tag can be returned to Standby mode by appropriate application of
a magnet.

This mode is used for long-term storage of a tag. The tag runs at the lowest-possible power
and does not monitor the environment. It can only come out of this state if it is connected
to a USB communications cable and a magnet is passed over the reset location on the tag
while Mk10Host is running.

 If you use high-power VHF radios near a tag with a depth sensor, it can generate depth spikes
which may cause the tag to deploy. You can choose the "Don't Deploy from Standby on Depth
Change" option to avoid this situation.

Sensors
Tags are configured with the following sensors as standard:

•  Depth
•
Internal (tag body) temperature
•  External (environmental) temperature
•  Depth sensor temperature

o  To internally correct drifts in the depth sensor due to temperature changes
o  No need to be set to sample for field deployments

4

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

4

4

•  Light level
•  Battery voltage

o  To internally monitor performance of the battery
o  No need to be set to sample for field deployments

•  Wet/dry

o  Used by the tag to correct drift in depth zero offset
o  Determines when the tag is out of water
o  No need to be set to sample for field deployments

Memory
Tags store data in flash memory. This data includes sensor readings, processed data, and satellite
messages. Contents of this memory are maintained even if the battery becomes discharged.

Data Collection Intervals
Data collection intervals can be set independently for each sensor. Intervals can range from 1/128th
second to 18 hours. Available range may vary between different tag types.

Decoding the Data
Wildlife Computers provides an analysis program, WC-DAP, to decode and display the data
downloaded from a recovered tag. WC-DAP will also export the data in other formats such as .csv,
Excel spreadsheet and Google Earth.

A Word on Version Numbers
The on-board software can be upgraded in our lab. Mk10Host code is upgraded in parallel, and is
generally distributed via email or our website. In order to keep the version of on-board software and
Mk10Host working seamlessly together, please note the following:

•  The Mk10Ware version numbers are in this format: x.yy
•  Mk10Host has version numbers in this format a.bb.cccc
•  When attempting to communicate with a tag use the following rules:

o  a  must be the same as x
o  bb must be greater than or equal to yy

It is best to use highest cccc available – see our website wildlifecomputers.com for the most
up-to-date Mk10Host

•

5

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

5

5

Communication
User parameters are programmed into the tag via a Windows-based program provided by Wildlife
Computers called Mk10Host. Mk10Host must be installed on your PC. Mk10Host has been tested
under Windows 2000 or later versions. Earlier versions of Windows may or may not work, depending
on the configuration of your PC. We do not support other operating systems (e.g., UNIX) or Windows
emulators.

Mk10Host works by:

•  downloading a copy of the set-up parameters from the tag to the PC
•  allowing you to edit these parameters in a standard Windows environment
•  uploading the changed parameters back to the tag

Mk10Host can be installed from our website wildlifecomputers.com. Follow the prompts provided.

Next install the USB Driver from our website. This allows you to use the USB communications cable
available only from Wildlife Computers. Install the driver before connecting the USB cable to the PC.

You should verify your communications with your tag before heading out to the field. Trying to debug
communications issues remotely with users who are “in the field” can be difficult.

Communications Connections Between the Tag and your PC
The communications port is a rectangular hole with chamfered edges in the epoxy casting of your tag.
It contains 4 gold-plated pins. Note the orientation of the pins in the communications port. There are
three pins in sequence, a “missing pin,” and a single pin. Note the orientation of the sockets in the flat
plug. One of the sockets is blocked. It is important that the flat plug is correctly oriented to the pins in
the communications port before inserting the plug. At the appropriate time, carefully insert the flat
plug from the USB communications cable into the communications port. IMPORTANT: Do not force the
plug.

Configuration with USB Communications Cable
Each time you start Mk10Host, you will be greeted with a Welcome screen. The first time you use the
Host, you will use this screen to configure your computer for communication with the tag.  If you are
using a USB communications cable, continue on with the instructions in this section. If using a Cable
Comm or Blue Box, see Appendix E.

6

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

6

6

If you are using a USB communications cable, click on OK.

You will see the Connection on the USB screen. Follow the instructions displayed.

Note: The Reset Switch is located near the communications port (except on the PAT-Mk10), so
passing a magnet in the vicinity of the communications port should activate the tag causing the
LED to glow. The Reset location on PAT-Mk10 is marked on the tag.

7

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

7

7

If the connections between the PC, USB communications cable and the tag are seated correctly, an
LED on the Mk10 will glow once the tag is ready for communication. The LED must be glowing before
clicking the Connect button.

Support for the USB Communications Cable
If you have previously installed the driver for another tag, and that device is connected, the
connection will default to that device. Optionally, the drop-down box in the COM /USB frame lets you
select the USB device you wish to use (if you have more than one connected) or to revert to a
previously defined COM port.

Communications Troubleshooting
Mk10Host may display additional prompts, such as the next screens illustrate, if there are difficulties in
establishing communications.

The ReBoot switch location is at the opposite end of the main tag board from the communications
connector (except on the PAT-Mk10). Refer to the appendices for more information on locating the
ReBoot location.

If you continue to have difficulty, you will eventually reach the following screen. At this point you
probably need to contact Wildlife Computers for technical support. Contact information is listed on
the last page of this manual.

8

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

8

8

Connecting to a File

If you click on the File  button in any the above dialogs, you can connect to a .wch file instead of a tag.
This feature provides you with a simple way to examine the set-up of a previous deployment, or to try
out the Mk10Host program.

9

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

9

9

Log On

After initial communications are established, you need to log on to your tag. You must correctly enter
your password and log on as Owner in order to read and update information from the tag. The default
password for all Mk10 tags is mk10. The password is not case-sensitive.

You can change your password any time after you have logged on as a user, by selecting the Password
menu item at top left of the Host screen. Acceptable passwords include entries up to 7 characters. If
you forget your password, you will have to return the tag to Wildlife Computers so we can reset it.

Note: The password entered will be remembered for each subsequent logon to successive tags for
the duration of the same session with Mk10Host.

If you do not know the password, you will only be able to see general information. You cannot change
any data or access any of the tag’s functions. Your only option after viewing the general information is
to click on Exit.

Disconnected Batteries and Dangerous Goods
Once you have successfully logged on to the tag, you may receive a warning about disconnected
batteries. This occurs when your tag is considered “Dangerous Goods” for shipping purposes due to
the number of lithium batteries used in the tag. See Appendix G for important information about
Dangerous Goods and disconnected batteries.

Programming and Testing
Mk10Host will display several sub-screens, identified by “tabs.” These tabs appear along the top of the
screen. Some of these tabs may be blank (and their captions enclosed in square braces), depending
upon the modules installed on the tag.

10

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

10

10

General Tab

This screen provides the main interface with the Tag. It is divided into several areas:

1.

Identification Information:  Configuration of the Tag, including the user’s identifier, which
you can change to identify each tag.

2. Tag’s Date and Time: Current state of the tag’s clock.
3. Last Deployment Info: Bytes of collected data.
4. Dangerous Goods information: See Appendix G.
5. Set-up and Report buttons: Explained below.

Copying Set-Up Information from One Tag to Another
The Save Setup button is useful if you are setting up a series of tags and wish them all to have the same
(or very similar) set-up. Set up the first tag, update, and then click Save Setup . You will be prompted for
a filename to save this set-up. You can use Read Setup on subsequent tags to load previously saved
set-up files. The format of these set-up files is compatible with the format used when saving data. Thus
you can restore a tag to the configuration used to gather a dataset by reading the set-up from that
archive record. These files use a .wch extension.

Create configuration report (.htm file)
It is important to archive the configuration of the tag (versions, parameters) prior to deployment so
that they can be used to correctly analyze the data. An abbreviated report is automatically generated
whenever deploying from Mk10Host. However, this full report also tests the integrity of the tag’s

11

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

11

11

internal table structure. Click Create Report and the following screen will appear, offering you a choice
on where to save the report prior to displaying it on the monitor or printing it out.

If you want to save the configuration to disk (as a .htm file which can be viewed with any web
browser) click Save, otherwise click Cancel.

Note: This configuration report only displays the tag parameters as stored by the Mk10Host on the
PC, not necessarily those on the tag. It does not perform any upload function. Mk10Host will
indicate (as shown below) if the report shows a change from what is on the tag. If so, be sure to save
the changes when you exit or deploy.

12

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

12

12

The File menu item at the top of the Hardware Configuration Report screen allows you to save or exit
this report. If you choose to save the report, the same Mk10 Configuration Report dialog box you saw
earlier will appear.

You must select PRINT at the top of the Hardware Configuration Report to get a hardcopy of your
report.

Set Tag’s Time and Date
It is important the tag’s time be accurately set to GMT. The date and time are used to label when the
data were collected.

There are two ways to set the tag’s clock. The best and most accurate way is to use the clock on your
PC. First ensure the clock on your PC is accurate. There are several websites that allow you to do this.
Alternatively, in Windows, select “Date and Time” in Control Panel, then select the “Internet Time” tab,
and follow the instructions.

Click the Change button on the Tag’s Date and Time frame to bring up the window to set the tag’s
clock:

13

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

13

13

Automatic Settings from PC’s Clock
Mk10Host will read the local settings of your computer and fill in the GMT offset. If you need to
override this, select the number of hours that need to be added to the time on your PC’s clock to
match GMT. For example, if your PC is set to GMT -7, select “7” in the drop-down box.

Click Update  in the Automatic setting frame.

Manual Setting of Time and Date
Alternately, enter the appropriate GMT date and time using an accurate time source,
clicking  Update  (in the Manual setting frame) to set the tag’s time and date to these values.

Identify Instrument
The User-Defined Identifier is an optional parameter. It can be used to identify the deployment. This
identifier will be displayed along with the data downloaded from the tag upon recovery.

Click the box next to the User Identifier label to enter a new identifier. The default value is as shown,
“…” The maximum number of characters allowed is 15. Any additional characters will be truncated.

14

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

14

14

Test Tab

Test Sensors Frame
Click the Test  button. The current values of each installed channel will be displayed:

15

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

15

15

Wet/Dry Sensor Threshold Frame
The tag can dynamically determine the appropriate threshold value for wet/dry determinations in sea
and brackish water. Leave this setting to Dynamic unless you are attempting deployment in unusual
water conditions. In such instances, contact Wildlife Computers for advice regarding this setting.

16

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

16

16

If you change the Wet/Dry Sensor Threshold to either 150 or 200, you will get a warning message. Be
sure you have this value set to what you need for the type of water in which the tag will be deployed.

Argos Side-Tab
This side-tab is visible from the testing tab for tags
configured with an Argos transmitter.

Immediate Test of Argos Transmitter
This function allows you to quickly verify the
Argos transmitter is functioning and the battery
voltage is at least 3.0 V. Click Transmit  and the
battery voltage and current drawn from the
battery are reported.

Unattended Test of Argos Transmitter
This function allows you to retest the tags
through the Argos system. This would be most
applicable for tags that have been stored for a
long period of time (several months).

When testing multiple tags concurrently, it is
important that tags do not transmit simultaneously. The “Auto-increment first transmission by” field
causes subsequent tags within the Mk10Host session to have their “First transmission at” field
automatically incremented to stop the tag’s transmissions from being simultaneous.

17

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

17

17

Fast-GPS Side-Tab
This function allows you to test the functionality of
the Fast-GPS module. Click on Test Fast-GPS  and
wait about 40 seconds, then click  Refresh . If results
are ready, the table will be updated and Fast-GPS
data displayed. If Status is still “processing,ˮ wait a
few seconds and click  Refresh  again. You will
probably not receive satellite signals if you are
running this test inside a building.

Stomach Temperature Side-Tab
This function allows you to test the functionality of the Stomach Temperature pill. When you start up a
pill, it may take an extended time before the tag recognizes it. Or, as shown in the first pane, the
receiver may be disabled. In either case, clicking Search for pill  will force the tag to restart the search, as
shown in the second pane. After the pill has transmitted, clicking Refresh  will display the new reading
from the pill. This is generally a more reliable method of interrogating the pill than using the Test
button (not shown here). Once a pill has been acquired by the tag (it knows the pill’s repetition rate),
then status will show “Acquired” and the Test button will work more reliably.

18

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

18

18

Corrosion Release Side-Tab
This function allows you to test the corrosion release on PAT-Mk10 tags. To start the test connect a
multi-meter between the release wire and the ground ring (next to the float), and click Start Test . The
corrosion release wire is now activated. The multi-meter should be set to measure current, and about
50mA of current should be flowing. Click on Stop Test  and the current should drop to zero. The Pin
state field should always read “Intactˮ but Pin 1 conversion and Pin 2 conversion values may vary from
the examples below.

With nothing between pin and ground ring:

With a 60-ohm resistor between pin and ground ring:

19

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

19

19

Archive Tab

Warning: If the tag has important data from a deployment that have not been downloaded, follow
instructions in the section: Download the Data before changing any parameters.

Setting the Data Collection Intervals
The tag processes sampling intervals as a 2-fold process:

•  Set the granularity of the sensor sampling to 1/128th (ultrafine), 1/64th (fine), or 1 second

(normal). 1/128th and 1/64th should only be used with Daily Diary tags (-DD). Click on the right
column to change the granularity of the sensor sampling.

•  Set the sensor with shortest sampling interval first, then the second shortest, and so on. This

way the available options will be the most obvious.

Having set the sampling intervals as desired, check the Sampling Duration frame to see how long it
will take to fill memory. If this value is longer than your anticipated deployment, you could sample
data faster. If this value is shorter than your anticipated deployment, you should probably sample data
slower or check the “Archive samples only when tag is wet” checkbox (see below).

20

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

20

20

Sampling Mode Frame
Use of memory can be optimized by programming the tag to Archive samples only when tag is wet.
This option should only be used if:

•  There is not enough memory to store the samplings at the desired sampling rate and

anticipated deployment duration

•  You are not interested in samples while the tag is dry
•  The tag has wet/dry sensors (this option will not be available if the tag does not have wet/dry

sensors)

•  Use caution when choosing to Archive samples only when tag is wet. If the wet/dry sensor is

damaged or obstructed, or the water conductivity is not as expected, you may not gather any
useful data.

This option is not available on PAT-Mk10 tags.

Sampling Duration Frame
Mk10Host will calculate and display:

•  How long data can be stored at the programmed sampling rate
•  How often the tag will “wake up” to take a sample

Automatic Correction of Depth Transducer Frame
Older pressure transducers have a tendency to drift over a deployment. These pressure transducers
are covered by a small black plug. For any other pressure sensor, do not enable depth correction. The
tag offers two strategies to monitor this drift so that it can automatically correct for it:

•  By most common shallow depth. This is appropriate if tag may not break the surface of the
water, (e.g. on a non-air-breathing animal) but you know that it will occasionally come to the
surface. This is your only choice if there isn’t a wet/dry sensor on your tag.

•  By first dry depth reading. This is appropriate when the tag is deployed on an air-breathing
animal and the tag is positioned such that the tag will be above the surface of the water when
the animal breathes. This option is not available on PAT-Mk10 tags.

The automatic correction of the depth transducer only affects data that will be processed into Argos
messages; corrections are not applied to the archive. Entries are made in the archive to indicate when
an automatic correction was made, and its value. These values are only used by analysis programs.

Fast-GPS Tab
The Fast-GPS module incorporates Fastloc® technology. When appropriate conditions are met, a sub-
second “snapshot” of the GPS constellation is taken. Following the snapshot, the Fast-GPS module
processes the snapshot to determine the identity and range of the GPS satellites that were present.
This processing takes 12 seconds and continues after the animal has submerged.

A Fast-GPS acquisition is considered “successful” if 4 or more satellites are identified in the Fast-GPS
snapshot. If 4 or more satellites are identified, these data will still be saved to the archive and an Argos
message will be created. When 3 or fewer satellites are identified, no data is stored in the archive.

There is a lot of control regarding when a Fast-GPS acquisition is attempted, how many acquisitions
should be attempted, and how many successful acquisitions are targeted:

21

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

21

21

Parameters

Time between Fast-GPS measurements
This parameter controls how frequently the tag should attempt a Fast-GPS measurement. Selecting
“Disabled” means do not attempt any Fast-GPS measurements. When a snapshot fails because 3 or
fewer satellites are identified, a new snapshot will be attempted after 15 minutes or the Time
Between Fast-GPS measurements, whichever is shorter, and when the tag is next dry.

Time Between Fast-GPS Measurements After Release
This parameter controls how frequently the tag should attempt a Fast-GPS measurement after
releasing from an animal. This option only appears for a tag fitted with a release.

Fast-GPS Days Frame
Select the days of the month for which Fast-GPS measurements should be attempted.

Fast-GPS Hours Frame
Select the hours of the day for which Fast-GPS measurements should be attempted.

Maximum Number of Fast-GPSs per Hour
The tag will target this number of successful Fast-GPS measurements per hour.

Maximum Number of Fast-GPSs per Day
The tag will target this number of successful Fast-GPS measurements within a GMT day.

22

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

22

22

Maximum Number of Failed Fast-GPSs per Hour
The tag will stop attempting Fast-GPS measurements for an hour once this limit is reached. Remember
that a failed Fast-GPS measurement causes a new measurement to be made after 15 minutes have
elapsed or the Time between Fast-GPS measurements, whichever is smaller. This value includes
additional Fast-GPS attempts such as the default 15 minute retry or if “Retry a failed Fast-GPS
immediately” is enabled.

Maximum Number of Fast-GPS Attempts per Day
The tag will attempt this number of Fast-GPS measurements within a GMT day. This value includes
failed attempts and must also include all the retry settings outlined above.

Suppress Fast-GPS Measurements Once a Good Location has been Collected …
Check this box to avoid wasting power attempting Fast-GPS measurements when they are not going
to be useful because you are not interested in on-land locations after the initial haulout.

Deployment Information Frame
Fill in the starting location so that the Fast-GPS solver can generate good locations from the archive
seamlessly. Use decimal latitude and longitude with up to 2 decimal places and negative values for
South and West start locations, for example -39.66 ° is 39.66 ° south.

Advanced Features Frame

Take Extra Fast-GPS Measurements After Surfacing From a Qualifying Dive
The first parameters are used when a researcher is primarily interested in the heading and speed of
the study animal following a “qualifying” dive. Qualifying dives must have a minimum dive depth and
dive duration, and are set on the Data to Transmit tab. These snapshots count against the daily and
hourly GPS snapshot limits. This parameter will cause many Fast-GPS measurements to be
attempted and will exhaust your battery quite quickly. Do not enable this feature unless you
really need these extra measurements.

Haulout Location and Duration, and Post-Haulout Movement
This feature is used when the researcher is interested in haulout behavior and is especially relevant for
disturbance studies. When this feature is enabled, GPS messages will contain the location and
duration of haulouts and one or more post-haulout locations. The haulout is specified by the haulout
definition (see Haulout Control Tab on page 37) and the duration is reported from the first dry minute.
By setting Number of additional Fast-GPS measurements to one or more, the feature is enabled.  At
least one post-haulout location must be taken to enable this tool. A GPS snapshot is taken as soon as
the criteria for the haulout are met. When the haulout ends, GPS snapshots are attempted with the
settings specified here. They override the normal GPS settings. By setting the Time between Fast-GPS
measurements to Fast, the tag will take snapshots as fast as possible at a minimum interval of
approximately 30 seconds. Haulout snapshots count against the Fast-GPS budgets for hourly and daily
limits. If this feature is enabled, DAP will generate a Haulout.csv file that lists the haul out start time,
end time, and location. Post-haulout locations will be in included in the FastGPS.csv file.

23

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

23

23

Retry a Failed Fast-GPS Immediately
By default a failed Fast-GPS fix will instigate a new snapshot attempt after 15 minutes or the Time
Between Fast-GPS Measurements, whichever is shorter. If this box is ticked, the tag will attempt a
GPS fix immediately upon the next surfacing. It will continue to attempt fixes until a successful fix is
obtained or the maximum number of failed Fast-GPS fixes per hour or day is reached.

Only Transmit Latest Location
When this feature is selected the tag will only transmit the last location. This is useful when decoding
Argos messages in real-time to track a deployed tag; however, this will likely reduce the total number
of locations because the tag will not buffer transmissions. For tags with both a release pin and a GPS,
this setting applies to locations that occur before and after release.

Data to Transmit Tab
Data are summarized into histograms, timelines, light-based location curves, and/or Fast-GPS
acquisitions. Newer tags also include behavior messages. This tab allows you to select the types of
messages to transmit, the sampling interval for histograms and timelines (which is independent of the
data archiving sampling interval), dive definitions, number of days of data to keep in the buffer for
transmission, and the relative priority of location messages over other types of messages.

24

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

24

24

Histogram Data Sampling Interval
This is the main on/off switch for generating messages. Generally 1-sec intervals are recommended in
order to generate the most accurate histograms, but 10-sec intervals may be needed to maintain
compatibility with data collected from our previous satellite tags (SDR-T16, etc).

Histogram table
This table contains and controls many parameters. First set the number of bins required for each
histogram message type that you want to be generated by clicking on a cell in the # bins column. This
will define the number of editable squares in the table. Next fill in the upper (deeper/longer/hotter)
limits for the bins by clicking on non-grey bin-limit cells. When focus leaves a row, the bins will
automatically sort into ascending order. The last bin is never editable, and consists of the counts not
contained in any other bin. If histograms are not required then set # bins to off.

Dive Maximum Depth and Dive Duration bins hold the count of dives at that duration or depth. The
maximum valid value in any bin is 254. A bin reading of 255 indicates a count of 255 or more dives. In
other words, all bins get capped at 255 dives.

Time-at-Temperature (TAT) and Time-at-Depth (TAD) histograms are the % of time spent at the
specified temperature and depth. (in Celsius and meters). Note that each bin value is the upper limit of
the bin. E.g. With bin settings of 0, 5, 10 & 20 meters, a reading of 5.1 would appear in the 10 meter
bin. Also note that if any data occurs in a bin, that bin will indicate a ‘1’ even though scaling would
have rounded the bin down to ‘0’. This applies to Dive Maximum Depth, Dive Duration, TAT, and TAD
histograms.

Tip: It is easiest to enter values starting at bin #1, and then press Enter to move to the next field.
When you reach the last bin the row will then sort into ascending order

Note: The inherent units of Dive Duration are seconds. Minutes can be entered by following the
number with either m or ′ (e.g. 2m30 or 2′30 is 2 minutes 30 seconds).

Histogram Collection
You can collect between 1 and 24 of each kind of histogram (and Additional Messages Generated at
Histogram Sampling Interval) per day. This frame allows you to select this number, and at what time
(GMT) they should start. You can also restrict the generation of new histograms when the tag is
continuously dry throughout the collection period.

25

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

25

25

Histogram & Timeline & Behavior Definition

0

0

10

20

30

40

50

60

70

5

10

15

20

25

30

35

Depth reading to determine
start and end of dive

Ignore dives whose maximum
depth is shallower than this

Dive had to pass this
depth to qualify

Dive duration is measured between
these readings, if it is long enough,
the dive “qualifies”

Surface duration is measured
between these readings

Start/end depth and shallowest maximum dive depth are shown above. They, in combination with the
“Ignore dives whose overall duration is shorter than” drop-down list, define “Qualifying Dives.ˮ Qualifying
dives are used in processing:

•  Maximum dive depth histograms
•  Dive duration Histograms
•  Behavior messages
•  Advanced features of Fastloc® control

Timeline messages (messages that record time spent shallower and deeper than a specified depth)
use their own depth threshold.

Depth-Temperature Profiles
These messages are generated from data sampled at the Histogram Data Sampling Interval:

•  PAT-style Depth-Temperature Profiles  (PDTs)

o  Low Resolution: The minimum and maximum temperatures observed at 8 depths are
recorded and transmitted in one message. The depths are chosen dynamically to
include the minimum and maximum depths detected, and 6 other depths arranged
equally between them.

o  High Resolution: The minimum and maximum temperatures observed at 16 depths
are recorded and transmitted in two separate messages. Every other depth (with
corresponding temps) is in the first message, and the remaining depths are in the
second message. This allows you to see the entire range even if you only receive one
of the two messages.

26

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

26

26

•  PDT summary messages are oceanographic profiles. As the time and order of the values are
not transmitted it is not possible to “join the dots” and determine dive behavior using PDT
data.

•  Deepest Dive Depth-Temperature Profiles

o  Deepest Dive Depth-Temperature Profiles create many messages containing paired

depth and temperature readings. The number of messages created will depend on the
Histogram Data Sampling Interval and the duration of the deepest dive recorded in
the Histogram period. You also need to define the temperature range for the profiles
from the drop-down list.

o  Since the tag is working to capture the deepest dive and since the tag does real-time
processing, it only knows a dive's maximum depth AFTER the animal starts its ascent.
For each histogram summary period the tag will select a single deepest dive. So, if the
current dive is deeper than the previous deepest dive, data collected from the current
dive overwrites the data in the DivePDT buffer. At the end of the histogram summary
period, the data in the DivePDT buffer by definition will be from the deepest dive. The
buffer reserved for the DivePDT contains 2000 bins. Each bin can only hold the LATEST
temperature reading at each depth during an ascent. Data are continuously sampled
at the histogram sample interval but only added to the buffer during the ascent of the
deepest dive.

o  At the end of the histogram summary period the buffer is processed into Argos

messages. The number of messages created is a function of the depth-temp pairs and
which can range from a couple of pairs to 2000! In other words, selecting this option
may create hundreds of messages which may swamp other collected data. It is
not generally recommended to use this option.

Other Messages

•  Hourly % Timelines record the percentage of time spent above a threshold depth within 24

1-hour blocks per day. These percentages are rounded to the nearest 10% (low resolution) or
1% (high resolution), but all-deep and all-shallow are identified independently.

•  20-minute timelines record whether the tag was on average deeper or shallower than a

threshold depth within 72 20-minute blocks per day. Alternately wet/dry can be used as the
threshold instead of a specific depth.

•  Light-Level Locations create messages that can be used to locate your study animal using the

times of dawn and dusk. This should be set for PAT-Mk10 tags.

With the exception of haul-out data in status messages, wet/dry sensor values are not transmitted and
are only available if the tag is recovered.

27

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

27

27

Behavior Collection
If behavior collection is enabled, then messages will be created describing the diving behavior of the
study animal. Diving behavior is subdivided into 2 modes:

•

In a qualified dive as defined above in the Histogram & Timeline & Behavior Definition
section, the following are reported:

o  Dive Duration
o  Maximum dive depth
o  The shape of the dive (see Dive Shape Classification below)

  Square

“V”

“U”

 Unclassified

•  At the surface, the following are reported:

o  Time spent at the surface. Surface is defined as the time between qualifying dives as
described above in the Histogram & Timeline & Behavior Definition section.

o  Time spent shallow. This is the time spent at or above the defined start/end depth of a
dive, or time dry if using the wet/dry sensor to start/end dives, while in a surface
interval.

o  Time spent deep. This is the time spent below the defined start/end depth of a dive, or

time wet, while in a surface interval.

You can expect about 5 dives with associated surface periods to be encoded into a single Argos
message. If your dive definition is inaccurate, you could end up with no messages (qualifying dive
definition is too broad, so no dives qualify), or too many messages (qualifying dive definition is too
narrow, so every vertical movement the animal makes is a “dive”). This could result in a holey dataset.

Dive Shape Classification
Dives are classified into one of three simple dive shapes (square, V, U) by assuming the bottom of a
dive is any depth reading >= 80% of the maximum reading observed for the dive.  If the total duration
for the dive is T, the total time between the first bottom reading and the last bottom reading is B:

Classification

Bottom Time

Square

B > 50% T

U

V

20% T < B <= 50% T

B <= 20% T

Stomach Temperature
This section will be disabled unless you have the –L module installed to link data from a stomach
temperature pill. There are three types of messages that can be generated; they can be selected in any
combination. The processing will recognize “ingestion events” from a rapid drop in stomach
temperature (ST). You set this threshold. An ingestion event ends when the ST returns to within 0.5°C

28

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

28

28

of pre-ingestion temperatures or when the event exceeds a maximum duration (that you also set). The
message types are:

•

Ingestion event records. These records are created as an ingestion event finishes and
contains the following parameters:

o  The time and date of the ingestion event
o  The ST immediately before the ingestion event started
o  The first ST of the ingestion event
o  The depth immediately before the ingestion event started
o  Whether the tag was ascending or descending when the ingestion event started
o  The deepest depth measured during the ingestion event
o  The seawater temperature at this deepest depth
o  The time of this deepest depth
o  The overall duration of the feeding event
o  The last ST of the feeding event
o  The lowest ST recorded
o  The time of the lowest ST recorded

•  Fine-scale ST samples during an ingestion event. During a recognized ingestion event, the
ST readings will be saved as a time-series at 1-min intervals. Temperature resolution is 0.1°C.

•  Course-scale ST messages when not fine-scale. This is the default method of encoding ST

readings as a time-series. Data are stored at 2-min intervals, but small changes in temperature
(< ±0.5°C) will be reported as “no change.ˮ This allows much greater compression of data.

The message types can be selected independently. Selecting or deselecting the “Ingestion events
records” just affects the generation of such messages, not the recognition of ingestion events. You can
deselect “Ingestion events records” and select “fine-scale ST...” The fine-scale messages will still be
generated during an ingestion event. The table below shows how the fine- and coarse-scale messages
interact.

Coarse-scale disabled

Coarse-scale enabled

Fine-scale disabled

Fine-scale enabled

No time-series data are generated.
Ingestion events can still be
generated if enabled.

No time-series data will be
generated unless an ingestion
event is underway.

Coarse-scale data will be generated
throughout the deployment. No
special action will take place during
an ingestion event.

Coarse-scale data will be generated
between ingestion events, and
fine-scale data will be generated
during ingestion events.

29

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

29

29

Time-Series Data
Time-series data is available on some tags. If this option is available to you, you will see the following
Data to Transmit screen, with a Time-Series tab.

On the Time-Series tab, you will choose

•  whether or not to enable Time-Series message generation
•  what duty-cycling settings to use
•
the time-series sampling interval

Time-Series Data is not generally recommended on Fastloc tags as the volume of both Time-Series
Data and Fastloc data is too high for the limited Argos bandwidth.

Detailed information on Time-Series data options and what the parameters mean is available in
Appendix D.

Dry-Deep-Neither Timeline
The Dry-Deep-Neither Timeline (or DDN Timeline) categorizes each hour of the day as Dry, Deep, or
Neither. The statistics are based on data collected at the histogram sampling interval.

30

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

30

30

On the DDN Timeline tab you will define:

•  Dry hour – the percentage of the hour that must be dry in order for the hour to be considered

“Dry.”

•  Depth threshold– the depth used to determine “Deep”.
•  Deep hour – the percentage of the hour that must be below the depth threshold in order for

the hour to be considered “Deep.”

Any hours that do not qualify as Dry or Deep will be considered Neither.

At the end of each day, each hour is marked as Dry, Deep, or Neither. This message is generated once
per day and contains data from the previous 5 days.

In the example below, the tag will tally each 10 second sample in an hour. If more than 90% of those
600 samples are “dry” the hour will be marked as “Dry.” Or if more than 50% of those 600 samples are
deeper than 10 meters,the hour will be marked as “Deep.”

Transmission Control

•  Sets the number of days of data to hold in the transmission buffer
•  Sets the priorities for the different kinds of messages

Together, these parameters determine the likelihood that a given message type will be sent from a
given period of the deployment.

31

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

31

31

The current version of the control uses relative priorities where high = 3×, medium = 2×, and low = 1×.
Thus if the behavior priority is set to high, and location priority is set to low, the transmission of data
will be adjusted so that all the behavior messages (in the transmit buffer) will be transmitted three
times for every time the entire set of location messages (in the transmit buffer) are transmitted. Note
that setting all priorities to high, will have no impact. Priorities must be set to different values to create
a difference in the likelihood that a message type will be received by an Argos satellite. You can also
set the number of days of Argos data to hold in the transmit buffer.

When to Collect Tab
Mk10Host allows you to control which day of each month to collect and process Argos messages for
later transmission.

The default setting is to collect on all days. Only use other set-ups if you are sure that you only want to
sub-sample the overall Argos message creation (to extend battery life, for instance).

When to Transmit Tab
This tab controls when Argos messages should be transmitted, how many should be transmitted, and
how they should be constructed.

32

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

32

32

Use the controls in the Transmit Days and Transmit Hours to control the dates and times of
transmissions.

The Daily Allowance field allows you to limit the number of transmissions per day on a month-by-
month basis.

Note: Set the Daily Allowance for each month to 0 to disable all Argos transmissions.

The Accumulate check boxes determine whether unused daily allowances of transmissions should
roll-over to the next transmission day (checked), or whether just the specified allowance should be
used each day (unchecked). Regardless of this state, the daily transmission allowance is accumulated
at 00h (tag time) only on days that are checked in the Transmit Days frame. Additionally one day’s
transmission allowance is allocated when the tag is deployed (assuming the deployment day is
enabled, or the number of days to transmit regardless of other settings is not set to “no”).

The Optimize for Battery Life check boxes determine how the tag builds Argos Messages. If
unchecked, the tag will attempt to pack as many different message types into a single Argos message
as it can, using a complex packing scheme. This will generally result in Argos messages close to the
maximum of 31 bytes long. If the optimize boxes are checked, then the tag will stop packing in
additional message types once the Argos message is 15 bytes long. Longer messages are more
efficient for retrieving data through the Argos system, but discharge the battery faster. These boxes

33

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

33

33

should only be checked when your deployment is only going to generate comparatively little data,
and you need the tag to continue to provide locations for as long as possible.

The control for the PAT-Mk10 and PAT-Mk10-F tags is a little different:

The Transmit Days setting and the Transmit Control are for pre-release only, only the Transmit
Hours affect both the pre- and post-release phases. In post-release mode the tag will transmit every
day as often as possible until the battery is flattened, regardless of these settings.

This allows the PAT-Mk10-F tag to be set up for “opportunistic transmissions” by setting the Daily
Allowance to a small (non-zero) number, like 10 or 20, for the months you are interested in getting
occasional messages through the Argos system.

Beware: Given that the PAT-Mk10 tag is not designed for opportunistic transmissions, and is only
likely to be successful in such transmissions if the study animal remains stationary at the surface for
extended periods of time (a minute to hours), we do not generally recommend setting the Pre-
Release Daily Transmit allowance to any non-zero number. Doing so incurs additional battery drain
as the tag attempts to detect the surface so that it can transmit.

Note: Because the Transmit Hours controls both post-and pre-release, we recommend that these
are set to All On.

34

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

34

34

Pop-Up Tab
The PAT-Mk10 tag can be instructed to pop-up (or release from the study animal) either on a specific
date:

35

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

35

35

Or after a specified number of days following deployment:

Premature Release Set-Up
An important part of successful deployment of a PAT-Mk10 tag is having the premature release
controls set up appropriately. A premature release is determined to have happened when the depth
reading hasn’t been variable enough. This indicates that the tagged animal is not moving in the water
column (dead) or that the PAT-Mk10 has become detached from the animal. After premature release is
detected, the PAT-Mk10 corrodes off its tether and starts to transmit immediately. The depth
measurement for premature release detection is taken every minute (for detection periods up to, and
including, 96 hours) and every two minutes (for detection periods over 96 hours). This happens
regardless of the other settings on the tag.

The Hours permissible at a constant depth before PAT-Mk10 starts to corrode off its tether field sets the
sensitivity of the premature release.  A short number of hours will cause a premature release to be
detected sooner, but may be subject to false detection.

Note: If you do not wish to enable premature release detection, set the Hours permissible at a
constant depth before PAT-Mk10 starts to corrode off its tether to forever

Use the Minimum depth to start premature release detection control to disable premature release
detection before the tag is actually deployed on a study animal. Be careful if you have a very shallow
diving animal to make sure this threshold will be passed. DO NOT press on the pressure sensors to
test the release.

36

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

36

36

If the animal is dead and resting on the seafloor, then depth will still continue to change due to tidal
variation. Use the PAT-Mk10 thinks it is at a constant depth even if depth varies within this range
control to allow for this tidal variation, and set it to a number larger than expected tides.

We generally recommend enabling the Release even if there are a few outliers. This allows a few
readings to be outside the prescribed range without stopping the premature release. This can be
useful where a tag is washed up on a beach and is tumbling among rocks, and occasional waves cause
high pressure readings. Do not enable this if you have an animal that stays at the surface almost
constantly, with very rare dives.

Depths deeper than a specified value can be treated as if the tag remained at this value using the
Treat all depths deeper than this value as if they are this value field. This can be useful where a
study animal is known never to go deeper than some value, and that premature release detection
should start detection immediately this threshold is passed. This will not cause an immediate release.
It will still have to stay the specified hours, above, deeper than this value. However, variations in depth
that might have postponed a premature release detection are effectively masked out.

Newer versions of Mk10Ware (v1.22 on) allow the user to initiate a premature release based on an
internal calculation of the amount of battery power consumed. This is only relevant for experiments
which include opportunistic transmissions, as otherwise no appreciable current is consumed by the
tag during data sampling.

You may be very interested in what took place immediately preceding a premature release detection,
e.g., in a mortality study. The Number of days to transmit with doubled priority allows you to
specify this history window.

Haulout Control Tab
The tag can have different regimes when the animal is “hauled out.ˮ This includes the transmission
repetition rate and the creation of new histograms and Fast-GPS messages.

The parameters on this tab define when the tag switches to haulout mode, whether Argos
transmissions should be paused after a certain number of hours in haulout mode, and whether
informative Argos transmissions should be made on every 8th day of haulout (to indicate the tag is still
functioning). Set the ‘Pause transmissions’ parameter to ‘Never’ to transmit for entire haul out.

37

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

37

37

Haulout is defined to start when a predefined number of consecutive minutes pass in which the tag is
“sufficiently dry.ˮ “Sufficiently dry” is in turn defined as having enough dry readings, measured once
per second, in a minute. These dry readings do not have to be consecutive. Haulout ends in a similar
manner, when enough wet readings occur in a minute.

Haulout definitions do not apply to PAT-Mk10 tags.

Battery Tab
This tab is designed to let you forecast how long the tag batteries will last. As this is a new addition to
the feature set, early tags may not have their battery configuration pre-encoded. In this case, manually
select the battery installed on your tag from the drop-down list.

38

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

38

38

You may also use the battery selector to see how long your tag would have lasted, had it been
configured with different batteries.

The area shaded represents the expected performance of the tag. The upper limit is the optimistic
view. The lower limit is a pessimistic view of the battery capacity. Actual life is usually somewhere
between these extremes.

If your tag is considered dangerous goods for shipping, you will have the ability to indicate if the
dangerous-goods screw is placed. See Appendix G for details.

39

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

39

39

Exit Tab
You will always use this tab when disconnecting the tag. Future versions of the software may include
warnings about parameters that seem to be poorly set. Absence of a warning does not necessarily
indicate that the tag has been set up optimally!

There are three options for deployment modes:  Shutdown, Standby and Deploy.

Shutdown Mode
Use this mode for storage between deployments. You must re-establish communications to deploy
the tag or put it into Standby mode. The clock is maintained. The data in memory are maintained.
Depending on whether or not you have changed any parameters during your Host session with the
tag, you will see one or the other of these messages.

40

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

40

40

Standby Mode
In this mode the tag is not entirely “turned off,” but monitors for a signal to activate it into Deployed
mode. The signals are described below. Depending on whether or not you have changed any
parameters during your Host session with the tag, you will see one or the other of these messages.

If you have any previously collected data in memory, you will receive the following prompt:

If you do not erase previously-collected data, the new data will be appended. The new data will be
marked as a new deployment.

Finally, you will receive this confirmation:

41

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

41

41

An abbreviated report file and a set-up file will be automatically created. They have filenames of
serialnumber.date.htm and serialnumber.date.wch respectively. The report is saved into the Report
directory, the set-up file into the Backup Directory, see page 46

Activating the Tag from Standby Mode
The tag can now be activated into deploy mode without re-establishing communications. There are
three ways to do this:

•  Applying a magnet in a specific way:

o  Pass a magnet near the communications port (on the PAT-Mk10, pass the magnet over
the indicated location on the tag label). The LED will quickly double-flash three times,
followed by one long flash, indicating it is in Standby mode.

o

o

If you pass a magnet over the same location during the long LED flash, the tag will go
into Deploy mode. The LED will flash quickly 10 times, followed by one long flash. It
will then glow dimly until the next full minute, indicating it is deployed.

If you do not time the magnet passes correctly, the tag remains in Standby mode.

•  Depth sensor reads a 20m change in depth

o

If you use high-power VHF radios near a tag with a depth sensor, it can generate
depth spikes which may cause the tag to deploy. You can choose the "Don't Deploy
from Standby on Depth Change" option to avoid this situation.

•  Wet/dry sensor senses a pre-set minimum change in conductivity.

Note: Daily Diary tags use a laser rather than magnet to switch modes because they contain a
magnetometer. Other tags with magnetometers will also use a laser. See Appendix C for more
details and additional options.

Deployed Mode
The tag initializes and immediately begins to sample. This mode automatically updates the tag (if
parameters have changed) and erases memory. A report file and a set-up file will also be automatically
created. They have filenames of serialnumber.date.htm and serialnumber.date.wch respectively. The
report is saved into the Report directory and the set-up file into the Backup Directory, see page 46.

42

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

42

42

WARNING: You should never turn off the Blue Box or disconnect a tag from a USB communications
cable, Cable Comm, or Blue Box without clicking on either the Deploy, Standby or Shutdown
buttons. Doing so may leave your tag in a mode that will rapidly deplete its internal battery.

Don’t Deploy From Standby on Depth Change
Checking this box prevents a depth change from triggering deployment. A change in the wet/dry
sensor readings or magnet swipe will still active the tag.

Blinks When Deployed
Once deployed, the tag begins data collection and flashes whenever it wakes up to take a sample.
How long the blinks run for is customizable.  Selections are in increments of 10 minutes, from never up
to 3 days. Once the tag reaches depth, the LED will stop flashing after 31 hours regardless of the set
blink duration.

Download Tab
There are two ways you can examine your collected data.

1. Use the built-in data viewer (only recommended for small data sets, such as for verification of

the sensors).

2. Download the collected data to a file and use other utilities (such as WC-DAP) to decode/view

the data for analysis.

43

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

43

43

Viewing the Data

To view at least some of your data, click on a radio button in the Select Dataset to View frame. If you
have more than 50,000 bytes of data in your archive, you will be limited to viewing only those initial
data.

Viewing Archive data will generate a view that looks similar to this:

44

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

44

44

You can change the fields displayed using the checkboxes. The column separator can be changed in
the Options menu. You can cut-and-paste data from the data display textbox into Excel, or other
programs. If you press Ctrl-A after clicking somewhere inside the data display textbox, all data are
copied to the clipboard (even data that were not displayed due to constraints of the textbox control).

You may also view Histogram, PDT, Location or Behavior records in a similar manner.

Download the Data
Use the Save collected data to File  button to Download your data. This will save the data in our
standard .wch format. These data can then be viewed graphically using WC-DAPAudit Tab

This shows the history of commands and responses that occurred during communications.

New information is appended. This can be a useful diagnostic tool when trying to figure out how or
when a parameter was changed.

45

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

45

45

File Tab
This tab allows you to see (and change) the default location to which Mk10Host saves data. Half of the
options shown will not affect you, and are only used during initial testing by Wildlife Computers.

The files affected by these settings that are pertinent to your use of Mk10Host are:

Audit
Backup

Configuration

Download
Report

Audit files. Naming convention is AuditOfxxAxxxx.tag
Automatically generated set-up files when you Standby or Deploy a tag.
Naming convention is xxAxxxx.dd-mmm-yyyy.wch
Manually generated set-up files from the General tab. Naming convention is
xxAxxxxconfig.wch
Downloaded data files. Naming convention is xxAxxxx.wch
Manually and automatically created report files. Naming convention is
xxAxxxx.htm for manually created reports, xxAxxxx.dd-mmm-yyyy.htm for
automatic (where xxAxxxx is serial number, and dd-mmm-yyyy is today’s date).

To change a default folder, click on its name and the following dialog will appear. Browse to choose
the desired location.

46

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

46

46

Menu Items

Password

You may change your password anytime you are logged on as a user, by selecting the Password
menu item at top left of the Host screen. Acceptable passwords include entries up to 7 characters. If
you forget your password, you will have to return the tag to Wildlife Computers so we can reset it.
Passwords are not case sensitive. The default password is mk10.

47

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

47

47

Resync

On occasion, your tag may get out of sync with the Host program. You will get a message warning you
about this. Clicking on the ReSync menu item should resynchronize communications. When you have
successfully re-synchronized your tag, you will get the following notice.

Options – List Separator

You may choose your preferred separator for displaying viewed data on the Download tab.

48

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

48

48

Options – Suppress Time-Error Warnings

If you have a tag whose clock has failed, you may be plagued with error messages warning you that
the clock is not advancing correctly. Clicking this menu item will suppress these messages so you can
continue to work with the tag.

Options – Allow Updates to Modify Source .wch File

This menu item only appears if you are connected to a file rather than a real tag. Normally you are
prevented from modifying the .wch file to which you are connected in order to protect the integrity of
the data in that file. Checking this menu item overrides this restriction. Use with extreme caution.

Maintenance - Update Host…

This provides a route for re-downloading parameters from the tag to the PC. Use this if you make
mistakes while setting your parameters and want to start over.

49

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

49

49

Maintenance - Update Tag…

This provides a manual route for forcing an immediate update of the tag with any changed
parameters on your PC.

Maintenance - Clear Tag’s Memory

This menu item may be used to clear collected data from a tag. It is not generally necessary to do this,
as data is automatically erased when a tag is re-deployed and you are prompted to erase when
putting a tag into Standby mode.

Maintenance - Read Version Numbers

50

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

50

50

This allows you to view all the version number information for the tag and Mk10Host

Help

The Help item will display the following Host version and contact information:

51

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

51

51

Deployment

Setting up Communications
Follow the instructions in the detailed description of the Mk10Host program.

Setting Up the Tag
Follow the instructions in the detailed description of the Mk10Host program.

Changing Modes With a Magnet
Pass a magnet once across the tag near the communications port. The LED will flash in a sequence
that displays the mode of the tag:

•  Shutdown mode LED pattern:  The LED will illuminate constantly as long as the magnet is

present.∗

•  Standby mode LED pattern: 2 blinks, a 1 second pause, 2 blinks, a 1 second pause, and 2

more blinks (You may not see all three sets, as this occurs quite rapidly.)

•  Deployed mode LED pattern: 10 blinks

Once the Standby or Deployed mode has been displayed, the LED will pause for another second and
then stay on for 2 seconds.

•

•

If you keep the magnet away from the tag during the 2 seconds that the LED is on, the tag will
stay in its current mode.

If you pass a magnet across the board during the 2 seconds that the LED is on, you will toggle
the mode between Standby and Deploy. The mode identification blink sequence of the new
mode will be displayed.

In summary, a single pass of the magnet over the tag displays the mode of the tag. It takes two
specifically timed passes of the magnet to change the mode.

Verifying Function Prior to Deployment
You should always confirm the tag is sampling before deployment.

Pass a magnet once across the tag near the communications port. The LED will flash, showing its
current state, as described above. After the next minute has rolled-over, the tag begins data collection
and flashes whenever it wakes up to take a sample. How long the LED flashes is user customizable.
Selections are in increments of 10 minutes, from never up to 3 days. Once the tag reaches depth, the
LED will stop flashing after 31 hours regardless of the set blink duration. DO NOT press on the
pressure sensors to test.

∗ If the magnet is present for an extended period of time, the LED will turn off to save power. When this
happens, the LED no longer responds to the presence of a magnet and you will have to use 2 magnets
(in ReBoot and Reset locations) to get a response from the tag.

52

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

52

52

Sealing the Communications Port
The communications port is where the Wildlife Computers Communications Cable connects to the
tag. Prior to a deployment, this port should be sealed with the plug provided. Smear a small amount of
the silicone grease supplied onto the sides and bottom of the plug, align the plug and pins, and
carefully push the plug into the port. If it does not align easily with the pins, rotate it 180° and try
again. The plug prevents corrosion of the pins during the deployment; however, the plug is not
required for the tag to function normally.

Additional Deployment Information
Wildlife Computers recommends that all tags initially be set up in the lab, when there is plenty of time
and conditions are at their best. Once the tags are set up, they can be placed in Standby until ready to
use. Just prior to deployment, the user can deploy them using a magnet.

Note:  Be sure that all previous data are erased prior to redeploying if you want the entire memory
available for data collection.

Alternatively, since tag batteries have plenty of capacity, if the tags will be deployed within a month,
they can be set up and deployed at the same time. The user should then use a magnet to verify the tag
is sampling before deploying it on the study animal or gear.

WARNING: If you are programming PAT-Mk10 tags, and have set the tags with premature release
parameters, it is STRONGLY recommended to leave the tags in Standby mode and not in Deploy
mode to prevent accidental premature release detection, which may burn the corrodible pin and/or
start transmissions, which will drain the battery.

Data Recovery

Basic Recovery Information
If the tag has been out for a long deployment (months to years), it is possible that contamination of
the communications port may cause some communication difficulties. The following instructions, in
addition to describing how to recover the data, explain possible problems that might occur during the
recovery and how to fix them. Even if all attempts to communicate with the tag fail, your deployment
data are probably still in memory, and can be retrieved by Wildlife Computers.

Preparation for Post-Deployment Communication
When you recover your tag full of valuable deployment data, there are several steps to perform before
attempting to connect it to the USB communications cable.

53

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

53

53

As a precaution, it is advised to have the following on hand:

•  Compressed air in a can
•  Electronic contact cleaner, if available

1. Thoroughly dry the tag with a paper towel.
2. Remove the communications port protection plug.
3. Blow out any water in the communication port. Make sure the port is clean and dry.

Compressed air in a can works well for this. Note that communicating with a tag which has
saltwater in the communications port will cause the pins to corrode very fast!

4. Count the number of pins in the communications port. If there are not four pins, one or more
have corroded or broken off. Send the tag to Wildlife Computers, and we will download your
data.

5. Examine the pins in the communications port. If they are rusty or corroded, send the tag back

6.

to Wildlife Computers for downloading.
If all four pins look clean and golden, you can continue and attempt to establish
communications.

7. You may wish to spray some contact cleaner into the communications port as a precaution.

Download Your Data
Follow the instructions in the detailed description of the Mk10Host program.

It is very important to save the collected deployment data in the .wch format. This is the only format
that can be processed by Wildlife Computers analysis programs.

Put your tag into Shutdown or Standby mode after downloading the data.

Storing Tags
Tags that will not be deployed for an extended period of time (more than one month) should be
Shutdown and stored in a refrigerator or freezer (5° C to -20° C). This minimizes the battery passivation
and extends the life of the tag.

If you tag has a battery isolator screw (see Appendix  G), place the screw before storing your tags.

Testing After Storage
Tags should be tested after storage, prior to deployment. It is not necessary to warm up the tag prior
to proceeding with the test.

Establish communications with the tag. If the tag has an Argos transmitter, test the Argos transmitter
(page 17) and check the battery voltage reported. It should read 3.0V or greater. The battery voltage
may be a little low initially, but should increase after testing the transmitter several times. If the tag has
a Fast-GPS module, initiate a Fast-GPS test (page 18). Then test the sensors to read the battery voltage
while the Fast-GPS processing it taking place. Again the battery voltage should stay above 3.0V
throughout the test. Repeat as necessary.

54

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

54

54

Appendix A. SPLASH10-F: Argos Transmitter & Fast-GPS
The SPLASH10-F includes the Wildlife Computers Cricket Argos transmitter plus the Fastloc™  fast-
acquisition GPS module. In addition to the standard archival functions, the Mk10-AF takes snapshots
of the GPS constellation. These GPS snapshots, along with summarized depth and temperature data,
can be transmitted to the Argos satellite system.

Fast-response
thermistor (under
shield)

GPS antenna

Wet/dry
sensor

Communications
port

LED

Notes:

Argos
antenna

Wet/dry sensor
and ReBoot
switch

Light sensor

Depth sensor

Reset switch
(side of tag)

•  Do not put anything over any of the sensors or the GPS antenna
•  Ensure the wet/dry sensors are free of oils and epoxy
•  Place magnet on the side of the tag by the communications port to trigger the reset switch
•  LED is best visible from the side of the tag

55

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

55

55

Appendix B. PAT-Mk10: Pop-up Archival Tag
The PAT-Mk10 is designed for deployments on animals that do not regularly come to the surface and
for which recovery of the tag is unlikely. The PAT-Mk10 is attached to the animal by a tether through
the corrodible attachment link. The attachment link will corrode and release the tag from the tether
on a pre-programmed release date, or optionally when the PAT-Mk10 determines it is no longer
attached to an animal.

In addition to the standard archival functions, depth, temperature and light-level data are collected
and summarized for later transmission through the Argos system during the deployment.
Transmission to the Argos satellites occurs after the release of the tag from the tether, and while it is
floating in the ocean, unless the tag has been programmed for opportunistic transmissions. In that
case, an Argos message will be sent during the deployment when conditions meet the programmed
parameters.

PAT-Mk10 Diagram 1: Communications Port Side View

Corrodible
attachment link
(under protective
thi bl )

Argos
Antenna

Communications
Port

Pressure
Sensor

Fast-
response
Thermistor

Ground

Wet / Dry
Sensor

56

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

56

56

PAT-Mk10 Diagram 2: Light Sensor Side View (Internal Label)

LED

ReBoot Switch

Reset Switch

PAT-Mk10 Diagram 3: LED Side View (External Label)

Reset Switch

LED

ReBoot Switch

Light Sensor

Light Sensor

57

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

57

57

RD1800 Release Device for PAT-Mk10
Wildlife Computers has developed a mechanical release device, called the RD1800, which prevents the
PAT-Mk10 from being towed to depths that could crush it. The RD1800 acts as a guillotine, severing an
internal shear pin when it is exposed to a depth of 1800-2000 meters. At these depths, water pressure
overcomes an internal support within the RD1800, the center section of the RD1800 snaps down and
cuts the pin, separating the RD1800. This releases the PAT-Mk10 so that it can float to the surface. The
Premature Release feature eventually recognizes a “constant depth” situation and initiates
transmission.

RD1800 Installation Instructions
The RD1800 release devices are supplied pre-assembled, but not connected to the PAT tags.

This device has been designed to work with both monofilament and stainless steel leadering
materials. We recommend:

•

.046 inch stainless steel cable so that it can be pulled tightly around the RD1800 thimbles.

•  Monofilament should be no greater than .070 inches in diameter so that it will fit through the

holes in the RD1800. This includes some 300 lb. test monofilament, depending on the
manufacturer.

When leadering your tags, it is important to be sure to pull whichever leader material you use tight
around all three thimbles, one on the tag and two on the RD1800, prior to crimping the crimps.

Stainless Steel Cable

Monofilament leader

Appendix C. TDR10-DD (Daily Diary) and TDR10-X
Daily Diary and TDR10-X Tags

58

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

58

58

Daily Diary and TDR10-X tags form the range of Wildlife Computers accelerometer datalogging tags. In
addition to the 3-axis accelerometer, these tags may contain 3-axis magnetometers, depth,
temperature, velocity, wet/dry, battery voltage and light-level sensors.

Daily Diary Setup

Daily Diary tags contain a magnetometer and use a laser rather than a magnet to switch modes or
initiate a reset. The laser reset location is just to the right and above of the communication port.

Use the laser when Mk10 Host, or this manual, mention a magnet swipe. Running the laser beam over
the reset location will perform the same function. These tags will not respond to magnets and using a
magnet near the tag may have an effect on the performance of the magnetometers.

We recommend disabling the laser reset when the tag is not connected to host. Refracted sunlight,
such as found 1-2 meters below the sea surface, is intense enough to activate the reset switch.
Disabling the laser can be done by checking the “Ignore laser-pointer…” box on the Exit Tab. With this
feature enabled, the tag can only be deployed when connected to host, when the tag exceeds 20 m in
depth, or the tag senses sea water with the wet/dry sensor. A magnet will not deploy the tag or put
the tag into standby mode.

59

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

59

59

Sensor Configuration

Daily Diary is a name given to our MK10 based TDR tag implying additional motion and attitude
sensors. The additional sensors measure 3 axes of accelerations, 3 axes of magnetic field strength, and
paddle wheel speed. These 7 data channels are archived onboard the tag in addition to the standard
Light Level, External Temperature, and Depth measurements and can be exported in various formats
using the WC-DAP Processor.

 These additional sensors allow for an expanding field of applications. For example, under acceptable
conditions and with the appropriate data post processing, the attitude (tilt and roll) of the tag and
animal can be derived from the static acceleration data. The accelerometers could also be used in a
dynamic sense to detect head strike events (lunges). Attitudinal information (tilt and roll) can be used
to rotate magnetometer measurements made in the sensor frame into the Earth's coordinate frame to
determine magnetic heading and other magnetic field strength components used for navigation
(magnetic dip angle). Change-in-Depth readings can be treated with the paddle wheel speed
measurements to derive the horizontal and vertical components of the animal's swimming speed.

Typical sense and assignment of the tag axes are illustrated in the following picture. Note that positive
X axis indicates the direction of travel for optimal paddle wheel performance.

60

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

60

60

Daily Diary

Orient this
end in
direction of
travel.

TDR10-X

+Y

+Z

+X

Measured Data (Sensors)

61

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

61

61

External Temperature
Range:
Resolution:
Accuracy:
Sample Rate:   32/second maximum, 1/second typical

-40°C to +60°C
0.05°C
±0.1°C

Depth
Range:
Resolution:
Accuracy:
Sample Rate:   32/second maximum, 1/second typical

0  to 2000 meters
0.5 meters
±1% of Reading

Light Level
Range:
Resolution:
Passband:
Sample Rate:   32/second maximum, 1/second typical

5 x 10-10 W.cm-2 to 5 x 10-2 W.cm-2 (8 decades)
20 units/decade
430 nanometers

3 Axes Acceleration
Range:
Resolution:
Sample Rate:   32/second maximum
Sensor Coordinate Frame: Right-Handed

±2g (-20m/s/s to 20 m/s/s)
0.05 m/s/s

Note that sitting the tag on a desk (motionless) will produce the following static acceleration values.
X = 0, Y = 0, Z = -9.8 m/s/s

3 Axes Magnetic Field Strength
±100 nanoTesla
Range:
Resolution:
0.2 nanoTesla
Sample Rate:   8/second maximum
Sensor Coordinate Frame: Right-Handed

Paddle Wheel Speed
Range:
Resolution:
Sample Rate:   1/second maximum

0 to 5 m/s
0.01 m/s

Battery/Memory Capacity

The Daily Diary configuration is based on the Mk10 platform employing a 1 gigabyte memory chip
used to store the sensor values.  Typically the tag is fitted with 2 x AA batteries with a capacity of
5.2Ah. The following details typical battery life and memory fill times which vary with sample rate.
Note: The expected battery life is impacted dramatically based on the actual speed of the animal.
The velocity paddle wheel consumes more power at extremely slow speeds, dictating the
"minimum" battery life.

62

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

62

62

Case1

Accelerometer @ 32 Hz
Magnetometer @ 4 Hz
Depth, Temperature, Paddle Wheel @ 1 Hz
Memory Fill = 70 days
Battery Life = 21 to 28 days

Case2
               Accelerometer @ 16 Hz
               Magnetometer @ 4 Hz

 Depth, Temperature, Paddle Wheel @ 1 Hz

               Memory Fill = 122 days
               Battery Life = 35 to 46 days

Case 3.

Accelerometer @ 8 Hz
              Magnetometer @ 2 Hz

Depth, Temperature, Paddle Wheel @ 1 Hz

              Memory Fill = 234 days
              Battery Life = 56 to 75 days

Derived Data

The WC-DAP Processor will attempt to calculate (post process) several derived values from the
archived acceleration and magnetic field strength data. These derived values are only available when
the tilt (i.e. pitch and roll) of the tag can be reliably determined.  Since the accelerometers are sensitive
to both static and dynamic accelerations, DAP will only process data when the total acceleration
measures 9.8 + 0.2 m/s/s. Under this condition DAP assumes that the acceleration reading is mostly
static and therefore tilt can be determined.

Once the tilt of the tag is known, its components (i.e. Pitch and Roll) can be reported along with
various magnetic readings as follows. Note that in special cases, the static acceleration can be isolated
from the total acceleration readings using methods such as low pass filtering. This technique is not
employed by the DAP Processor.

Heading
This is the direction in which the nose of the tag is pointing. The value is expressed in degrees on a
scale from 0 to 360. Magnetic North corresponds to a reading of 0 with a clockwise rotation increasing
the value (consistent with navigational headings).

Magnetic_Vertical
This is the value of the vertical component of earth’s magnetic field strength, derived from the total
magnetic field strength. The value is given in microteslas.

Magnetic_Horizontal
This is the value of the horizontal component of earth’s magnetic field strength, derived from the total
magnetic field strength. The value is given in microteslas.

63

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

63

63

Magnetic_Dip
This is the angle at which the earth’s magnetic flux lines enter the earth’s surface. This value is given in
degrees, from -90 to +90 with 0 being completely horizontal to the earth’s surface. +90 corresponds to
the tag resting directly over the magnetic north pole while a -90 reading means the tag is over the
magnetic south pole.

Pitch
This is the counterclockwise rotation of the tag about its Y axis (see Figure 1). This value is given in
degrees from -90 to +90 (where a horizontal tag reads 0 degrees).

Roll
This is the counterclockwise rotation of the tag about its X axis (see Figure 1). This value is given in
degrees from -180 to +180 (where a tag flat on its base reads 0 degrees).

Magnetic_Magnitude
This is the overall strength of the earth’s magnetic field. It is the vector sum of the three
magnetometer channels. The value is presented in microteslas.
TDR10-X Tags
TDR10-X tags consist of a 3-axis accelerometer with optional depth sensing and also temperature and
light-level sensors. As these tags do not contain a magnetometer they are activated via a magnet.

Battery/Memory Capacity

TDR10-X configuration tags are based on the Mk10 platform employing a 1 gigabyte memory chip
used to store the sensor values. These tags are typically powered by a single 2.1Ah AA battery. The
following details typical battery life and memory fill times which vary with sample rate.

Case 1

Accelerometer @ 32 Hz

               Depth, Temperature, light-level @ 1 Hz
               Memory Fill = 79 days
               Battery Life = 9 days.

Case 2
               Accelerometer @ 16 Hz

Depth, Temperature, light-level @ 1 Hz

               Memory Fill = 154 days
               Battery Life = 17 days.

Case 3
                Accelerometer @ 8 Hz
                Depth, Temperature, light-level @ 1 Hz
                Memory Fill = 297 days
                Battery Life = 32 days

64

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

64

64

Appendix D. Time-Series Data in Detail
Some versions of transmitting tags have the ability to send time series depth and/or temperature data
through Argos.  This feature is designed to provide low-frequency reporting of sensor data for
instruments which may never be recovered.

You can choose from one of five time series sample rates.  A single point sample is taken at the chosen
sample rate, for example every 5 minutes. The sample rate determines the number of messages
generated per day.  The Min/Max values for the message period are determined and used to set the
range of values. This range is divided into 16 bins to which each sample point is fitted.

65

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

65

65

48 summarized samples will fit into 1 Argos message. This time series sample rate is completely
independent of and unrelated to the archive sample rate.

Sample Rate
(minutes)

Argos Messages Per Day

Depth or Temp

Depth & Temp

(1 channel)

(2 channels)

Message
Period
(hours)

1 ¼

2 ½

5

7 ½

10

24

12

6

4

3

48

24

12

8

6

1

2

4

6

8

For example, 12 time series messages per day are created if both depth and temperature data are
sampled every 5 minutes; six messages per day would be transmitted if temperature were omitted.
Messages are transmitted in sequential order to maximize the probability of receiving continuous runs
of data.

Selecting a short (75-second) Time-Series Sampling Interval rapidly generates a need for lots of
messages. This might be acceptable for a short deployment. However if too many messages are
generated too quickly, the tag will be unable to transmit all of them. The result will be random gaps of
time during the deployment for which there is no time-series data. Selecting a longer Sampling
Interval so that fewer than 1250 messages are needed to transmit the Time-Series will improve the
odds that there will be no gaps in your Time-Series data set. However, the temporal resolution of each
datum will be reduced. Different study objectives will warrant different trade-offs between coverage
and temporal resolution.

Each time series message contains:

•  48 instantaneous points sampled at the specified sample rate for that message period.
•  The minimum and maximum values encountered during the message period for the channel

which are determined from all archived values in that message period.

Note: that the absolute Min/Max values and point sample values may not match as the Min/Max
value is determined from all archived data during the message period.

66

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

66

66

Three duty cycling parameters are available to control the time series data generation as shown
below:

Deploy

DAYS

ON

DAYS

OFF

DAYS

ON

Duty cycling is by days, each day is defined as the passage of 00:00 on the instrument clock.  The
instrument supports time series generation being turned ON for zero or more days immediately after
deploy, OFF for zero or more days, followed by ON for zero or more days.  The instrument can be set
to sample for only a predetermined time after deploy (and never again) by setting the topmost ON
block to the desired value and setting the two lower blocks to zero.  Alternatively, the instrument can
be set to sample during the entire deployment by setting the topmost ON block to any value, the OFF
block to NEVER, and the bottom ON block to a value such as 10.

Note: The duty-cycle settings are for Time-Series Data message creation only and do not affect the
tags archive sample rates or Argos transmission settings.

67

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

67

67

Appendix E. Configuration with Cable Comm or Blue Box Communications Hardware
Each time you start Mk10Host, you will be greeted with a Welcome screen. The first time you use the
Host, you will use this screen to configure your computer for communication with the tag. If you are
using a Cable Comm or Blue Box, proceed to the configuration instructions in this section. If you are
using a USB communications cable, return to the instructions in the previous section.

If using a Cable Comm or Blue Box, click on Configure COM and proceed to the ‟Define which COM
port to use” instructions. Do not connect to a tag until instructed to do so. Note: the Host program uses
the word "recorder" instead of "tag" in the instructions, but includes all types of tags.

Define Which COM Port to Use

If you are not using the default USB device, the first time you run Mk10Host, you will need to configure
the program by telling it which COM port to use to communicate with the Cable Comm/Blue Box. The
OK Button on the Welcome screen will be grayed-out until you complete this step. Click the Configure
COM... button to start the Connection Wizard.

68

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

68

68

When using a Cable Comm, follow the prompts on this tab:

When using a Blue Box, follow the prompts on this tab:

When attempting to configure your COM port, you will be notified (as shown on the Cable Comm
screen print previously) if you have chosen an invalid port number. Select a different port to try again.

69

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

69

69

Once Mk10Host is properly configured, you will be returned to Welcome Screen. Since you will have
completed configuration of your communications hardware at that point, the OK button will then be
accessible, and you will proceed to connect to your tag.

Mk10Host will remember the COM port, so you do not need to repeat these steps unless you want to
change the communications port to which your interface is configured.

70

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

70

70

After pressing OK on the welcome screen, this screen is displayed:

Follow the instructions displayed.

Note: The Reset Switch is located near the communications port (except on the PAT-Mk10), so
passing a magnet in the vicinity of the communications port should activate the tag causing the
LED to glow. The Reset location on the PAT-Mk10 is marked on the tag.

If the cables between the PC, Cable Comm or Blue Box, and the tag are connected correctly, an LED on
the tag will glow once it is ready for communication. The LED must be glowing before clicking the
Connect button.

71

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

71

71

Appendix F. Tag Modes

72

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

72

72

Appendix G. Disconnected Batteries and Dangerous Goods
Summary

In order to comply with lithium battery shipping regulations, certain Wildlife Computers tags include a
battery isolator screw. Tags with the isolator can be transported with their power cells disconnected. It
is critical that you communicate with these tags and connect the batteries before deployment.

A tag with disconnected batteries can only be put into Shutdown mode. This prevents accidental
deployment of the tag without first connecting the batteries.

Connecting to a Tag for the First Time

When you connect to a tag that has disconnected batteries, host will prompt you to place the screw
that connects the batteries. By clicking “Ok” you acknowledge that the screw is placed. The tag can
now be placed in Standby or Deploy mode.

You may also choose to cancel at this point and leave the batteries disconnected (with the screw
unplaced). This allows you to change the tag settings but you will only be able to put the tag into
deep kill. You might want to do this if you were setting up tags and then shipping them to your field
site.

The next time you connect to the tag with host you will be prompted with this message again.

73

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

73

73

General Tab

The general tab will display the status of the batteries. A red warning will indicate the batteries are not
connected.

Exit Tab

If you have not acknowledged placement of screw connecting, only shutdown mode will be available.
We do not recommend storing the tags without first connecting the batteries; however, you are able
to put the tag into Shutdown. If you attempt to place the tags into Standby or Deploy mode, you will
again have the opportunity to place the screw.

74

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

74

74

Instructions for Connecting the Batteries

1. You will need a 3/32” Allen key and the included titanium bolt and lock washer.

2. For each tag, insert the bolt and lock washer into the cylindrical metal socket as shown below.

3. Hand-tighten the bolt until the lock washer is compressed and the bolt is firmly seated. The

bolt will be flush or slightly recessed. Do not over tighten.

4. The battery isolator bolt is intended to be inserted up to 10 times. Once inserted, take care not

to unnecessarily remove and reinsert the bolt.

75

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

75

75

Technical Specifications

The TDR10 is configurable with a wide variety of sensors. Fastloc® GPS is available on several
configurations. Below are the general physical specifications of TDR10 tags.

Attachment type

Externally mounted***

Sensors

Depth, Temperature, Light-level, 3D

Depth sensor range

0-200 m, 0-1700 m, 0-2000 m ***

Depth sensor resolution

0.5 m

Depth sensor accuracy

±1% of reading

Temperature sensor range

-40 to 60° C

Temperature sensor resolution

Temperature sensor accuracy

0.05° C

± 0.1° C

Light sensor

5 x 10-12 W.cm-2 to 5 x 10-2 W.cm-2

3D Accelerometer range

3D Accelerometer resolution

± 2 g

0.05 m

3D Magnetometer range

± 100 nanotesla

3D Magnetometer resolution

0.2 nanotesla

Speed sensor range

Speed sensor resolution

Stomach temperature range

Stomach temperature resolution

Stomach temperature accuracy

0-5.0 m·s-1

0.01 m·s-1

0 to 50° C

±0.1° C

± 0.3° C

Maximum sampling rate

32 Hertz (32 samples/sec)

Length (mm), width (mm), height (mm),

***

Pressure rating (m)

Up to 2000 m ***

Operating temperature rating (°C)

-20 to 50°

76

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

76

76

Recommended storage temperature range

5 to -20°

Conductivity operational limits

0.1 to 5 S/m

Memory

Maximum deployment length

1 GB

***

*** indicates the specification is dependent upon the configuration model

77

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

77

77

Contacting Wildlife Computers

U.S. and International
Members of the Wildlife Computers technical sales and support team are located in Redmond, WA,
USA, and Havelock North, New Zealand, allowing us to cover promptly a wide range of time zones.

Mailing and Shipping
Wildlife Computers
8310 154th Avenue NE, Suite 150
Redmond, WA 98052 USA

Email
Sales, Quotes, and Inquiries: <tags@wildlifecomputers.com>
Technical Support: <support@wildlifecomputers.com>

Phone

Website

+1 (425) 881 3048

WildlifeComputers.com

For Asian Clients
While we welcome your direct correspondence, we recommend that you contact our colleague, Yong
Huang, for assistance. Mr. Huang understands the special purchase processes for your countries, and
will provide you with the best service for the best price. He also is fluent in Japanese, Chinese, and
English.

Mailing address—Please ship tags to our main office in Redmond.
Yong Huang
Enfotran Corporation
2608 79th Ave NE
Medina, WA 98039 USA

E-mail
<yong.huang@enfo.us>

Phone
+1 (425) 456 0101

78

The  information  contained  in  these  documents  is  confidential,  privileged  and  only  for  the
information of the intended recipient and may not be used, published or redistributed without
the prior written consent of Wildlife Computers.

78

78
