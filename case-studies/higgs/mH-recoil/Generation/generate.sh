#!/bin/bash

export det=$1
echo '---- Using detector configuration of: '$det
export process=$2
echo '---- Producing the process:   '$process
export id=$3

wd=${PWD}

source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
export LD_LIBRARY_PATH=/cvmfs/sw.hsf.org/spackages6/libtirpc/1.2.6/x86_64-centos7-gcc11.2.0-opt/6mvhk/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/cvmfs/sw.hsf.org/spackages6/openloops/2.1.2/x86_64-centos7-gcc11.2.0-opt/clg3p/lib:$LD_LIBRARY_PATH

#det='IDEA'
FCC_Config='/afs/cern.ch/work/l/lia/private/FCC/MVA/FCC-config/'
Whizard_Config=$FCC_Config'FCCee/Generator/Whizard/v2.8.5/'
Pythia_Config=$FCC_Config'FCCee/Generator/Pythia8/'
Delphes_card='/afs/cern.ch/work/l/lia/private/FCC/MVA/FCC-config/FCCee/Delphes/'
outputDirEos='/eos/user/l/lia/FCCee/MVA/training_samples/'
eosType='eosuser'

if ! [ -d "$outputDirEos" ]; then
  # Take action if $DIR exists. #
  echo "Creating repository ${outputDirEos}..."
  mkdir $outputDirEos 
fi

if ! [ -d "$outputDirEos$process" ]; then
  # Take action if $DIR exists. #
  echo "Creating repository ${outputDirEos}${process}..."
  mkdir $outputDirEos$process 
fi


if [[ $process == *"p8"* ]]
then
  echo "Working on Pythia8!"
  wd=${PWD}
  mkdir $process
  cd $process
  pythiaCard=$Pythia_Config$process
  DelphesPythia8_EDM4HEP ${Delphes_card}/card_${det}.tcl ${Delphes_card}/edm4hep_${det}.tcl ${pythiaCard}.cmd events_${id}.root 
  xrdcp  events_${id}.root root://${eosType}.cern.ch/${outputDirEos}${process}
elif [[ $process == *"wzp6"* ]]
then
  echo "Working on Whizard + Pythia6!"
  mkdir $process
  cd $process
  echo "Starting Whizard"
  whizard ${Whizard_Config}/${process}.sin
  #cd $wd
  echo "Starting Pythia6!"
  DelphesSTDHEP_EDM4HEP ${Delphes_card}/card_${det}.tcl ${Delphes_card}/edm4hep_${det}.tcl events_${id}.root proc.stdhep
  echo "xrdcp events_${id}.root root://${eosType}.cern.ch/${outputDirEos}${process}"
  xrdcp events_${id}.root root://${eosType}.cern.ch/${outputDirEos}${process}
else
  echo "Unknown process type"
fi
