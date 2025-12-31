# NOTE: This file was moved from the R_legacy directory to R on August 19, 2025.
# Git commit history for this file is preserved and can be viewed with:
#   git log --follow R/swordRED_pseudotrack-clean.R
# LIBRARIES AND FUNCTIONS ---------------------

#Need to pull these packages from Connor github not on CRAN
library(devtools)
#devtools::install_github("connorfwhite/TeleFunc/TeleFunc")
#devtools::install_github("MBayOtolith/gRumble/gRumble")

library(gRumble)
library(TeleFunc)
library(fields)
library(biwavelet)
library(signal)
library(data.table)
library(dplyr)

## and load a custom mag function

MagOffset<-function(Mag){
  ##Finding the hard iron offset
  A=cbind(Mag[,1]*2,
          Mag[,2]*2,
          Mag[,3]*2,1)
  f=matrix(Mag[,1]^2 + Mag[,2]^2 + Mag[,3]^2,ncol=1)

  C<-solve(crossprod(A), crossprod(A,f))

  rad = sqrt((C[1]^2 + C[2]^2 + C[3]^2) +C[4])

  return(c(C[1],C[2],C[3],rad))
}

# COMMAND LINE ARGUMENTS ---------------------

# Parse command line arguments
args <- commandArgs(trailingOnly = TRUE)

# Set defaults
default_input <- "./data/RED001_20220812_19A0564.csv"
default_output <- "./data/RED001_20220812_19A0564-corrected-R-diagnostic.csv"
default_meta <- "./data/biologger_meta.csv"

# Parse arguments: Rscript script.R input_file output_file [meta_file]
if (length(args) >= 1) {
  input_file <- args[1]
} else {
  input_file <- default_input
}

if (length(args) >= 2) {
  output_file <- args[2]
} else {
  output_file <- default_output
}

if (length(args) >= 3) {
  meta_file <- args[3]
} else {
  meta_file <- default_meta
}

# Extract tag ID from input filename for metadata lookup
uid <- sub(".*/(.*?)\\.csv$", "\\1", input_file)
# For test files like RED001_20220812_19A0564_early_deployment, extract base tag ID
tag_id_short <- sub("^(.*?_[0-9]{8}).*", "\\1", uid)  # Extract RED001_20220812 part
if (!grepl("_[0-9]{8}", tag_id_short)) {
  # If not in expected format, try original extraction
  tag_id_short <- sub("_.*", "", uid)
}

cat("Processing:", input_file, "\n")
cat("Output:", output_file, "\n")
cat("Metadata:", meta_file, "\n")
cat("UID:", uid, "\n")
cat("Tag ID:", tag_id_short, "\n")

# DATA PREP ---------------------

#setting the  location of where the .csv file is
#wd <- '~/Google Drive/Shared drives/MPG_WHOI/projects/sword-biologger-daniel/'
#setwd(wd)
wd <- getwd()

## get some metadata on the deployment
meta <- data.table::fread(meta_file)
meta <- meta %>% as.data.frame() %>% dplyr::filter(tag_id == tag_id_short)
meta$time_start_utc <- as.POSIXct(meta$time_start_utc, format='%m/%d/%y %H:%M', tz='UTC')
meta$time_end_utc <- as.POSIXct(meta$time_end_utc, format='%m/%d/%y %H:%M', tz='UTC')

## obviously could loop through a bunch of tags, if desired
dat <-fread(input_file, skip=3, fill=TRUE)
dat <- as.data.frame(dat)

dat <- dat[!is.na(dat$"int aX"),]
dat$DateTimeP <- as.POSIXct(dat$Date * 3600 * 24, origin='1899-12-30', tz='UTC')
## force add decimal seconds time to output
dat$DateTimeP.dec <- format(dat$DateTimeP, '%Y-%m-%d %H:%M:%OS4', tz='UTC')
dat <- dat %>% dplyr::filter(DateTimeP > meta$time_start_utc)
colnames(dat)<- c("Date", "Depth", "Temp",
                  "X_Mag", "Y_Mag", "Z_Mag",
                  "X_Accel", "Y_Accel", "Z_Accel",
                  "Light", "Velocity","CorDepth", "Wet", "Events","","DateTimeP","DateTimeP.dec")

## define the sampling frequency of the mag/accel
freq <- 16

## do some interpolating to fill most of the depth NAs
## first preserve the original raw depth values for comparison
dat$Depth_raw <- dat$Depth
dat$Depth <- eventInterp(dat$Depth,x = is.na(dat$Depth), ends=1)
dat$Depth <- stats::filter(dat$Depth, filter=rep(1,freq * 5) / (freq * 5))

#Defining when the tag was on the fish
deploymentLim <- c(meta$time_start_utc, meta$time_end_utc)
#deploymentLim[1] <- min(dat$DateTime)
#deploymentLim[2] <- as.POSIXct("2021-08-29 18:36:00", tz='UTC')

#Only grabbing the columns we need
dat <- dat %>% dplyr::select("DateTimeP","DateTimeP.dec","X_Accel","Y_Accel","Z_Accel", "X_Mag", "Y_Mag", "Z_Mag", "Depth","Depth_raw","Temp", "Light")

#Renaming the columns so they are the same ones I always use and easy for me to call
colnames(dat) <- c("DateTimeP","DateTimeP.dec","X_Accel","Y_Accel","Z_Accel","X_Mag","Y_Mag","Z_Mag","Depth","Depth_raw","Temp","Light")#,"BattVolt")
dat <- dat[which(dat$DateTimeP > deploymentLim[1] & dat$DateTimeP < deploymentLim[2]),]

# INITIAL CALCULATIONS ---------------------

#calulating the simple vertical velocity and then using a 5 second running mean to smooth it a bit
dat$vertical_velocity <- c(0, diff(dat$Depth))
dat$vertical_velocity <- c(stats::filter(dat$vertical_velocity, filter = rep(1,5) / 5))

#calculating the average acceleration of the tag to figure out its average position
#This should be indicative of attachment angle. Gravity should be aligned as x=0, y=0, z=1
posMean <- colMeans(dat[,c('X_Accel','Y_Accel','Z_Accel')])
posMeanOriginal <- posMean  # Preserve original values for diagnostics

#calculating the roll of the tag so that the Z axis is pointed downward
roll <- atan2(posMean[2], posMean[3])

#Rotating the acceleration data for roll so that is is in the fishes frame
datAccelR <- as.matrix(dat[,c('X_Accel','Y_Accel','Z_Accel')]) %*% Xb(roll)

#repeating same procedure for correcting for the minor pitch error ~5 degrees
posMean <- colMeans(datAccelR) ## recalc the mean
pitch <- atan(posMean[1] / posMean[3])
datAccelR <- datAccelR %*% Yb(pitch)

#checking the average position of the tag post correction to make sure it is pretty good
print(round(colMeans(datAccelR), digits=3))

## and add the new x,y,z to the dataframe
dat$X_Accel_rotate <- datAccelR[,1]
dat$Y_Accel_rotate <- datAccelR[,2]
dat$Z_Accel_rotate <- datAccelR[,3]
names(dat)[which(names(dat) %in% c('X_Accel','Y_Accel','Z_Accel'))] <- c('X_Accel_raw','Y_Accel_raw','Z_Accel_raw')

## separating static and dynamic acceleration, using a 100 point running mean, basically 4 seconds for this dataset

# ORIGINAL (INCORRECT: filter not normalized due to operator precedence)
# datG <- Gsep(dat[,c('X_Accel_rotate','Y_Accel_rotate','Z_Accel_rotate')], filt = rep(1, freq * 3) / freq * 3)

# FIXED: Parentheses ensure filter is normalized (sums to 1)
datG <- Gsep(dat[,c('X_Accel_rotate','Y_Accel_rotate','Z_Accel_rotate')], filt = rep(1, freq * 3) / (freq * 3))

## add static and dynamic components of accel to the data
print(dimnames(datG)[[2]])
dat <- cbind(dat, datG)

#Estimating the pitch and the roll of the tag based on the static acceleration
PR <- pitchRoll2(datG[,c(1:3)])
dat$pitch_radians <- c(PR[,1])
dat$roll_radians <- c(PR[,2])
dat$pitch_degrees <- c(PR[,1] * 180 / pi)
dat$roll_degrees <- c(PR[,2] * 180 / pi)

# SOME ACCELEROMETER QC FIGURES ---------------------

#Histogram showing body positions
#Can clearly see the three peaks of the fish swimming upright, swimming on one side and swimming on its other side
png(paste0(wd, '/figures/bodyposition_', uid, '.png'), height=10, width=12, units='in', res=300)
par(mfrow=c(1,2), mar=c(4,4,1,1))
hist(dat$roll_degrees, xlim = c(-110, 110), main="", xlab = "Body Roll", xaxt = "n")
axis(side=1, at = seq(-90, 90, by=30))

hist(dat$pitch_degrees, xlim=c(-110, 110), main="", xlab="Body Pitch", xaxt="n")
axis(side=1, at = seq(-90, 90, by=30))
invisible(dev.off())

###
### Plotting overview of depth, temperature, pitch and roll and ODBA
###
#grabbing only every 100th point to just make plotting faster
xloc <- seq(1, nrow(PR), by=100)

## quick look summary of the overall data
png(paste0(wd, '/figures/summary_', uid, '.png'), height=20, width=12, units='in', res=300)
layout(matrix(c(1,2,3), nrow=3, ncol=1), heights=c(1,1,1,1))
par(mar=c(2,5,0,1))
plot(dat$Depth[which(!is.na(dat$Temp))] ~ dat$DateTimeP[which(!is.na(dat$Temp))], col=color.scale(dat$Temp[which(!is.na(dat$Temp))]), ylim=c(650,0), bty="n", xlab="", ylab=" ", las=1, mgp=c(0.5,1.5,0))
mtext(side=2, text = "Depth(m)", line = 3)

plot(dat$pitch_degrees[xloc] ~ dat$DateTimeP[xloc], bty="n", las=1, ylim=c(-90,90), type="l", ylab="", yaxt="n", xaxt="n", col="red")
axis(side=2, at = c(-90,-45,0,45,90), las=1)
mtext(side=2, text = "Pitch(deg)", line = 3)

plot(dat$roll_degrees[xloc] ~ dat$DateTimeP[xloc], bty="n", las=1, ylim=c(-90,90), type="l", ylab="", yaxt="n", xaxt="n", col="blue")
axis(side=2, at= c(-90,-45,0,45,90), las=1)
mtext(side=2, text = "Roll(deg)", line = 3)
invisible(dev.off())

## simple XYZ accel fig
png(paste0(wd, '/figures/summary_', uid, 'xyz.png'), height=20, width=12, units='in', res=300)
layout(matrix(c(1,2,3), nrow=3, ncol=1), heights=c(1,1,1,1))
par(mar=c(2,5,0,1))
plot(dat$Depth[which(!is.na(dat$Temp))] ~ dat$DateTimeP[which(!is.na(dat$Temp))], col=color.scale(dat$Temp[which(!is.na(dat$Temp))]), ylim=c(650,0), bty="n", xlab="", ylab=" ", las=1, mgp=c(0.5,1.5,0))
mtext(side=2, text = "Depth(m)", line = 3)

plot(dat$X_Accel_rotate ~ dat$DateTimeP, bty="n", las=1, type="l", ylab="", col="red")
lines(dat$Y_Accel_rotate ~ dat$DateTimeP, col='blue')#, bty="n", las=1, type="l", ylab="", yaxt="n", xaxt="n", col="red")
lines(dat$Z_Accel_rotate ~ dat$DateTimeP, col='green')#, bty="n", las=1, type="l", ylab="", yaxt="n", xaxt="n", col="red")
#axis(side=2, at = c(-90,-45,0,45,90), las=1)
#mtext(side=2, text = "Pitch(deg)", line = 3)

plot(dat$X_Mag ~ dat$DateTimeP, bty="n", las=1, type="l", ylab="", col="red")
lines(dat$Y_Mag ~ dat$DateTimeP, col='blue')#, bty="n", las=1, type="l", ylab="", yaxt="n", xaxt="n", col="red")
lines(dat$Z_Mag ~ dat$DateTimeP, col='green')#, bty="n", las=1, type="l", ylab="", yaxt="n", xaxt="n", col="red")
invisible(dev.off())

#Nice (mostly) linear relationship between Body pitch and vertical velocity which is good
png(paste0(wd, '/figures/swimspeed_', uid, '.png'), height=10, width=12, units='in', res=300)
plot(dat$vertical_velocity ~ I(dat$pitch_degrees), las=1, ylab="Vertical Velocity(m/s)", xlab="Body Pitch")
m <- lm(dat$vertical_velocity ~ I(dat$pitch_degrees))
text(-50, -.5, paste(round(coef(m)[2] * 90, 2), 'm/s'))
invisible(dev.off())

# MAGNETOMETER QC CALCS ---------------------

## calc intial offsets
magOff <- MagOffset(dat[,c("X_Mag", "Y_Mag", "Z_Mag")])
magX <- (sin(seq(0, 2 * pi, length.out=100)) * magOff[4]) + magOff[1]
magY <- (cos(seq(0, 2 * pi, length.out=100)) * magOff[4]) + magOff[2]
magZ <- (cos(seq(0, 2 * pi, length.out=100)) * magOff[4]) + magOff[3]

## look at the raw mag data
## and look at offsets
png("./figures/Raw Magnetic Heading_Sphere.png",height=10,width=7,res=200,units="in",bg="transparent")
par(mfrow=c(2,1),mar=c(4,4,1,1))
plot(dat$X_Mag[seq(1, nrow(dat), by=100)] ~ dat$Y_Mag[seq(1, nrow(dat), by=100)],
     asp=1, ylab="Magnetometer X", xlab="Magnetometer Y")
lines(magX ~ magY, col="red")
points(magOff[1] ~ magOff[2], col="red", pch=15)
plot(dat$Z_Mag[seq(1, nrow(dat), by=100)] ~ dat$X_Mag[seq(1, nrow(dat), by=100)],
     asp=1, ylab="Magnetometer Z", xlab="Magnetometer X")
lines(magZ ~ magX, col="red")
points(magOff[3] ~ magOff[1], col="red", pch=15)
invisible(dev.off())

## Correcting for hard iron offsets
# Preserve original X/Y/Z_Mag, store corrected values in new columns

dat$X_Mag_adj <- (dat$X_Mag - magOff[1]) / magOff[4]
dat$Y_Mag_adj <- (dat$Y_Mag - magOff[2]) / magOff[4]
dat$Z_Mag_adj <- (dat$Z_Mag - magOff[3]) / magOff[4]

png("./figures/Magnetic Heading_Corrected.png",height=10,width=7,res=200,units="in",bg="transparent")
par(mfrow=c(2,1),mar=c(4,4,1,1))
plot(dat$X_Mag_adj[seq(1, nrow(dat), by=100)] ~ dat$Y_Mag_adj[seq(1, nrow(dat), by=100)],
     asp=1, ylab="Magnetometer X", xlab="Magnetometer Y")
plot(dat$Z_Mag_adj[seq(1,nrow(dat),by=100)] ~ dat$X_Mag_adj[seq(1,nrow(dat),by=100)],
     asp=1, ylab="Magnetometer Z", xlab="Magnetometer X")
invisible(dev.off())

# Rotating the magnetometer data for roll and pitch (attachment angle)
datMag <- as.matrix(dat[,c('X_Mag_adj','Y_Mag_adj','Z_Mag_adj')]) %*% Xb(roll)
datMag <- datMag %*% Yb(pitch)

## and add the new mag x,y,z to the dataframe
dat$X_Mag_rotate <- datMag[,1]
dat$Y_Mag_rotate <- datMag[,2]
dat$Z_Mag_rotate <- datMag[,3]
names(dat)[which(names(dat) %in% c('X_Mag','Y_Mag','Z_Mag'))] <- c('X_Mag_raw','Y_Mag_raw','Z_Mag_raw')

## now plot the corrected for attachment angle
png("./figures/Magnetic Heading_Corrected_AttachmentAngle2.png", height=10,width=7,res=200,units="in",bg="transparent")
par(mfrow=c(2,1),mar=c(4,4,1,1))
plot(dat$X_Mag_rotate[seq(1, nrow(dat), by=100)] ~ dat$Y_Mag_rotate[seq(1,nrow(dat),by=100)],
     asp=1,ylab="Magnetometer X", xlab="Magnetometer Y")
plot(dat$Z_Mag_rotate[seq(1, nrow(dat), by=100)] ~ dat$X_Mag_rotate[seq(1,nrow(dat),by=100)],
     asp=1,ylab="Magnetometer Z", xlab="Magnetometer X")
invisible(dev.off())

#Correcting the field at each time step for the calculated Pitch and Roll
MagCor <- as.matrix(dat[, c("X_Mag_rotate","Y_Mag_rotate","Z_Mag_rotate")])
for(i in 1:nrow(MagCor)){
  MagCor[i,]<- MagCor[i,] %*% Yb(-dat$pitch_radians[i]) ## pitch
  MagCor[i,]<- MagCor[i,] %*% Xb(dat$roll_radians[i]) ## roll
}

## and finally the corrected for pitch/roll
png("./figures/Magnetic Heading_Corrected_PitchRoll2.png", height=10, width=7, res=200, units="in", bg="transparent")
par(mfrow=c(2,1),mar=c(4,4,1,1))
plot(MagCor[seq(1, nrow(datMag), by=40), 1] ~ MagCor[seq(1, nrow(datMag), by=40), 2],
     asp=1, ylab="Magnetometer X", xlab="Magnetometer Y")
plot(MagCor[seq(1, nrow(datMag), by=40), 3] ~ MagCor[seq(1, nrow(datMag), by=40), 2],
     asp=1, ylab="Magnetometer Z", xlab="Magnetometer X")
invisible(dev.off())


## and add the new mags to the dataframe
dat$X_Mag_corrected <- MagCor[,1]
dat$Y_Mag_corrected <- MagCor[,2]
dat$Z_Mag_corrected <- MagCor[,3]

## add heading, convert radians to degrees
dat$heading_radians <- atan2(-dat$Y_Mag_corrected, dat$X_Mag_corrected)
dat$heading_degrees <- dat$heading_radians * 180 / pi

## example zoom in of heading sway
#png("./figures/Heading_Sway2.png", height=6,width=10,res=200,units="in",bg="transparent")
#par(mfrow=c(2,1),mar=c(4,4,1,1))
#plot(dat$heading, type="l", ylab= "Heading (deg)", bty="l", xlab="")
#plot(datG[,5], type="l", col=rgb(0,.8,.5), ylab="Sway (g)", bty="l", xlab="")
#invisible(dev.off())


png("./figures/Heading_Overview2.png", height=5,width=8,res=200,units="in",bg="transparent")
par(mar=c(4,4,1,1))
plot(dat$heading_degrees[seq(1, nrow(dat), by=freq)],
     ylab= "Heading (deg)", bty="l", xlab="", pch=16, cex=0.5)
invisible(dev.off())

## calculate pseudo x/y
dat$pseudo_x <- cumsum(cos(dat$heading_radians) * (1 / freq) * 1)
dat$pseudo_y <- cumsum(sin(dat$heading_radians) * (1 / freq) * 1)

# ==================== DIAGNOSTIC COLUMNS FOR PYTHON COMPARISON ====================
# Add diagnostic information about the attachment angle calibration process
# These columns help compare with the Python progressive/adaptive calibration system

# 1. CALIBRATION WINDOW DIAGNOSTICS - Show how much data was used
dat$r_attachment_calibration_samples <- nrow(dat)  # R uses full dataset
dat$r_attachment_calibration_duration_min <- nrow(dat) / freq / 60

# 2. CALIBRATION METHOD METADATA
# Document the R calibration approach for comparison with Python variance-based system
# Document the R calibration method
dat$r_calibration_method <- "full_dataset_batch"
dat$r_calibration_samples <- nrow(dat)
dat$r_calibration_duration_min <- nrow(dat) / freq / 60

# 3. CALIBRATION DATA QUALITY METRICS
# Show stability/quality of calibration data for comparison with Python diagnostics
calibration_data <- dat[,c('X_Accel_raw','Y_Accel_raw','Z_Accel_raw')]
dat$r_calibration_data_std_x <- sd(calibration_data[,1])
dat$r_calibration_data_std_y <- sd(calibration_data[,2])
dat$r_calibration_data_std_z <- sd(calibration_data[,3])

# Magnitude error: how close to unit magnitude gravity
accel_magnitude <- sqrt(calibration_data[,1]^2 + calibration_data[,2]^2 + calibration_data[,3]^2)
mean_magnitude <- mean(accel_magnitude, na.rm=TRUE)
dat$r_accel_magnitude_error <- abs(mean_magnitude - 10.0)  # Expected ~10 in 0.1g units

# 4. ATTACHMENT ANGLE VALUES - Expose the actual calculated attachment angles
dat$r_attachment_roll_deg <- roll * 180 / pi
dat$r_attachment_pitch_deg <- pitch * 180 / pi

# 5. MAGNETOMETER CALIBRATION VALUES - Add offset values as columns for direct comparison
dat$r_mag_offset_x <- magOff[1]
dat$r_mag_offset_y <- magOff[2]
dat$r_mag_offset_z <- magOff[3]
dat$r_mag_sphere_radius <- magOff[4]

# 6. MEAN ACCELEROMETER VALUES - Expose the mean values used for attachment angle calculation
dat$r_mean_accel_x_raw <- posMeanOriginal[1]  # From initial calculation before any rotations
dat$r_mean_accel_y_raw <- posMeanOriginal[2]
dat$r_mean_accel_z_raw <- posMeanOriginal[3]

# Print diagnostic summary for comparison with Python results
cat("R Batch Processing Diagnostic Summary:\n")
cat(sprintf("Full dataset calibration: roll=%.2f°, pitch=%.2f°\n",
            roll * 180/pi, pitch * 180/pi))
cat(sprintf("Calibration samples: %d (%.1f minutes)\n",
            nrow(dat), nrow(dat) / freq / 60))
cat(sprintf("Accel magnitude error: %.3f\n", dat$r_accel_magnitude_error[1]))
cat(sprintf("Magnetometer calibration: mag_offset_x=%f, mag_offset_y=%f, mag_offset_z=%f, mag_sphere_radius=%f\n",
            magOff[1], magOff[2], magOff[3], magOff[4]))
cat("================================================================================\n")

## and plot it
png("./figures/PseudoTrack2.png", height=8, width=8, res=200, units="in", bg="transparent")
par(mar=c(4,4,1,1))
plot(dat$pseudo_x[seq(1, nrow(dat), by=freq)] ~ dat$pseudo_y[seq(1, nrow(dat), by=freq)], ylab="Pseudo Latitude", xlab="Pseudo Longitude")
invisible(dev.off())

# Write output using command line argument
data.table::fwrite(dat, file=output_file)
cat("Output written to:", output_file, "\n")

# 3d plotting -----------
# rgl::plot3d(x=pseudo_x[seq(1,nrow(datMag),by=16)],
#             y=pseudo_y[seq(1,nrow(datMag),by=16)],
#             z=datMag$Depth[seq(1,nrow(datMag),by=16)],
#             col=color.scale(datMag$Depth[seq(1,nrow(datMag),by=16)], zlim=c(0,500), col=rev(tim.colors(64))),
#             xlab="X",
#             ylab="Y",
#             zlab="Z",
#             ylim=c(-1000,100),xlim=c(-5000,5000))
#
# rgl::plot3d(x=pseudo_x[seq(7,length(pseudo_x),by=16)],
#             y=pseudo_y[seq(7,length(pseudo_x),by=16)],
#             z=datMag$Depth[seq(7,length(pseudo_x),by=16)],
#             col=color.scale(datMag$Depth[seq(7,length(pseudo_x),by=16)], zlim=c(0,500), col=rev(tim.colors(64))),
#             xlab="X",
#             ylab="Y",
#             zlab="Z")#,
# ylim=c(-1000,100),xlim=c(-5000,5000))
#
#
#
# rgl::plot3d(x=MagCor[seq(1,nrow(datMag),by=40),1],
#             y=MagCor[seq(1,nrow(datMag),by=40),2],
#             z=MagCor[seq(1,nrow(datMag),by=40),3],
#             col=color.scale(PR[seq(1,nrow(datMag),by=40),2]),
#             xlab="Magnetic X",
#             ylab="Magnetic Y",
#             zlab="Magnetic Z")
#
#
