#!/bin/bash
#source /cvmfs/sw.hsf.org/spackages4/key4hep-stack/2021-11-26/x86_64-centos7-gcc8.3.0-opt/mynqr2z/setup.sh
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
export PYTHONPATH=$PWD:$PYTHONPATH
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=$PWD/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH
export LOCAL_DIR=$PWD
export LD_LIBRARY_PATH=`python -m awkward.config --libdir`:$LD_LIBRARY_PATH
