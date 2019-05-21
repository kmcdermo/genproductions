from optparse import OptionParser
import os
import sys
import commands
import re
import datetime
from time import sleep

def str_to_bool(s) :
    if s == "True" :
        return True
    elif s == "False" :
        return False
    else :
        print "String ",s," is NOT a bool!"
        exit

if __name__ == "__main__":

    # parse options
    parser = OptionParser()
    parser.add_option("-f", "--dataset "      , dest="dataset",  default="/a/b/c", help="primary dataset name")
    parser.add_option("-i", "--instance"      , dest="instance", default="global", help="DAS instance, either \"global\" or \"phys03\"")
    parser.add_option("-n", "--events"        , dest="events",   default=int(1e6), help="number of events to calculate the cross section")
    parser.add_option("-d", "--debug"         , dest="debug",    default=False,    help="use debug options")

    (args, opts) = parser.parse_args(sys.argv)
    debug = str_to_bool(str(args.debug))
    
    # dump input options
    if debug :
        print "\n","Input parameters"
        print "  dataset          : " + args.dataset
        print "  DAS instance     : " + args.instance
        print "  number of events : " + str(args.events)
        print "  debug            : " + str(debug),"\n"

    # DAS commands + infiles
    das_command = "/cvmfs/cms.cern.ch/common/dasgoclient --limit=255 --query=\"file dataset="+args.dataset+" instance=prod/"+args.instance+"\""
    infiles = commands.getstatusoutput(das_command)[1]
    
    # dump DAS commands + input files
    if debug :
        print "DAS Command\n",das_command,"\n\n","List of input files\n",infiles,"\n\n","XSec Command"

    # parse input files into single string
    infiles = infiles.replace("\n",",").split(",")
    filelist = ""
    firstEntry = True
    for infile in infiles :
        infile = "root://xrootd-cms.infn.it/"+infile
        if firstEntry is False : 
            infile = ","+infile
        else :
            firstEntry = False
        filelist = filelist+infile

    # make xsec computation command
    xsec_command = "nohup cmsRun genXsec_cfg.py inputFiles="+filelist+" maxEvents="+str(args.events)
    print xsec_command
