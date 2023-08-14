echo "Lancer chaque run un par un"

i=1
while read line; do
#  echo $i
  cd "./simu$i"
  echo "We are in simu :" $i
#  starttime="date +%s"
  ./testphys1d_29_phymars_seq.e > log
#  endtime="date +%s"
#  runtime=$(($endtime-$starttime))
#  echo "This took :" $runtime
  echo "We are leaving simu :" $i
  cd ..
  i=$(($i+1))
done < ./indexarray.txt


