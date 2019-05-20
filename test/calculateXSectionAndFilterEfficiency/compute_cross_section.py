from optparse import OptionParser
import os
import sys
import commands
import re
import datetime
from time import sleep

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-f', '--dataset '      , dest="dataset",  default='/a/b/c', help='primary dataset name')
    parser.add_option('-i', '--instance'      , dest="instance", default="global", help='DAS instance, either \"global\" or \"phys03\"')
    parser.add_option('-n', '--events'        , dest="events",   default=int(1e6), help='number of events to calculate the cross section')
    parser.add_option('-d', '--debug'         , dest="debug",    default=False,    help='use debug options')

    (args, opts) = parser.parse_args(sys.argv)
    debug = str_to_bool(str(args.debug))
    
    if debug:
        print
        print 'RUNNING PARAMS: '
        print '                debug                 = ' + str(debug)
        print '                dataset               = ' + args.dataset
        print '                number of events      = ' + str(args.events)
        print

    das_cmd = "/cvmfs/cms.cern.ch/common/dasgoclient"
    command = das_cmd+" --limit=255 --query=\"file dataset="+args.dataset+" instance=prod/"+args.instance+"\" "
    infiles = commands.getstatusoutput(command)[1]
    
    if debug:
        print 'command\n',command,'\n\n','infiles',infiles,'\n\n'

    infiles = infiles.replace("\n",",").split(",")
    filelist = ''
    firstEntry = True

    for infile in infiles :
        infile = "root://xrootd-cms.infn.it/"+infile
        if firstEntry is False : 
            infile = ","+infile
        else :
            firstEntry = False
        filelist = filelist+infile

    # compute cross section
    primary_dataset_name = args.dataset.split('/')[1]
    command = 'nohup cmsRun genXsec_cfg.py inputFiles=\"'+filelist+'\" maxEvents='+str(args.events)+" >& xsec_"+primary_dataset_name+".log &"
    print command
