#!/bin/bash

module unload python
module load python/3.6-anaconda50

echo "Petit script pour lancement script python en boucle"
echo "You are here : "
cwd=$(pwd)
path_here=$cwd
echo $path_here
parent=$(dirname $cwd)
echo $cwd
echo "Figures will be saved in :"
if [ ! -d $cwd/figures ]
then
    mkdir -p $cwd/figures
fi
path_save=$cwd/figures/
export path_save
echo $path_save

#DIRLIST=$(ls -d */ -I figures)
SIMULIST=$(ls -d */ | grep -v figures)
SIMULIST=$(ls -d simu*/ | sort -V)
echo "Liste des simus disponibles :" 
echo $SIMULIST

export SIMULIST


python diagram_tmax.py
#i=1
#while read line; do
#  cd "./simu$i"
#  echo "We are in simu :" $i
#  name=${PWD##*/}
#  export name
#  cp ../ice_sublim.py .
#  python ice_sublim.py
#  echo "We are leaving simu :" $i
#  cd ..
#  i=$(($i+1))
##done < dummy.txt
#done < indexarray.txt
