#!/bin/bash

tmpoutput="hvds_tex.txt"
> "${tmpoutput}"

for MZp in 300 500 800 1000
do
    for MDP in 20 40 60
    do
	for ctau in 1 100 500 1000 2500 5000 10000
	do
	    xsec=$( grep "${MZp} ${MDP} ${ctau} " hvds_xsecs.txt | cut -d " " -f 4)

	echo "/HVDS_MZp-${MZp}_MDP-${MDP}_Ctau-${ctau}mm_TuneCP5_13TeV-pythia8/\$/* & ${xsec} \\\\" >> "${tmpoutput}"
	done
    done
done