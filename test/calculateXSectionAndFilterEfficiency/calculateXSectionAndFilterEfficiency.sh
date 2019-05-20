#!/bin/bash

FILE="datasets.txt"
INSTANCE="global"
EVENTS="1000000"
DEBUG="False"

while getopts ":f:i:n:d:" option
do
    case "${option}" in
	f) FILE=${OPTARG}
	    ;;
	i) INSTANCE=${OPTARG}
	    ;;
        n) EVENTS=${OPTARG}
	    ;;
	d) DEBUG=${OPTARG}
	    ;;
	\? ) echo "Example usage: ./calculateXSectionAndFilterEfficiency.sh -f datasets.txt -i global -n 100000 -d False"
    esac
done

function compute_xsec ()
{
    local dataset=${1}
    local name=${2}

    local output=$( python compute_cross_section.py -f "${dataset}" -i "${INSTANCE}" -n "${EVENTS}" -d "${DEBUG}")
    local outfile="log_${name}.txt"

    if [[ "${DEBUG}" != "True" ]]
    then
	if [[ "${output}" == *"cmsRun"* ]] 
	then
            eval "${output}"
	else
	    echo "FAILED for dataset: ${dataset}" > "${outfile}"
	fi
    else
	echo "compute_cross_section.py -f ${dataset} -i ${INSTANCE} -n ${EVENTS} --debug ${DEBUG}" > "${outfile}"
	echo "   --> output: " >> "${outfile}"
	echo "${output}" >> "${outfile}"
    fi
}
export -f compute_xsec

while read -r dataset
do
    name=$( echo "${dataset}" | cut -d "/" -f 2 )
    echo "Working on: ${name}"
    compute_xsec "${dataset}" "${name}" &
done < "${FILE}"
