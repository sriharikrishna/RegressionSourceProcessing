#!/usr/bin/env python

import os
import sys
import shutil
import re

sepLength=80
makeCmd="make"
globalBatchMode=False
globalIgnoreFailingCases=False
globalOfferAcceptAsDefault=False
globalAcceptAll=False
globalVerbose=False
globalUnstructured=False
globalOkCount=0
globalKnownFailCount=0
globalNewFailCount=0

class MultiColumnOutput:

    ourColumnSeparator=2
    
    @staticmethod
    def __getTermWidth():
        import termios, fcntl, struct, sys
        s = struct.pack("HHHH", 0, 0, 0, 0)
        fd_stdout = sys.stdout.fileno()
        cols=80
	try:
          x = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, s)
          (rows,cols,xPix,yPix)=struct.unpack("HHHH", x)
	except IOError:
	  if globalVerbose:
	    sys.stderr.write("Error: cannot detect terminal width\n")
	    sys.stderr.flush()
        return cols

    class ColumnInfo:

        ourMinimalWidth=2
        
        def __init__(self):
            self.width=self.ourMinimalWidth # minimal width

    def __init__(self,stringList) :
        self.stringList=stringList
        self.totalWidth=self.__getTermWidth()

    def __computeColumnInfos(self):
        goodColumnInfos=[]
        maxCols=self.totalWidth/self.ColumnInfo.ourMinimalWidth
        listLen=len(self.stringList)
        if listLen==0:
            return goodColumnInfos
        numCols=1 # 1 column to start with
        while (True) :
            if numCols>listLen:
                break
            columnInfos=[]
            colLength=listLen/numCols
            if (listLen%numCols>0):
                colLength+=1
            for i in xrange(0,numCols):
                columnInfos.append(self.ColumnInfo())
            for i in xrange(0,listLen):
                # determine the column:
                colForThis=i/colLength
                if columnInfos[colForThis].width<len(self.stringList[i])+self.ourColumnSeparator :
                    columnInfos[colForThis].width=len(self.stringList[i])+self.ourColumnSeparator
            totalColumnWidth=sum([ c.width for c in columnInfos ])
            if totalColumnWidth>self.totalWidth and numCols>1: 
              break
            goodColumnInfos=columnInfos[:]
            numCols+=1
        return goodColumnInfos
    
    def printIt(self):
        columnInfos=self.__computeColumnInfos()
        listLen=len(self.stringList)
        numCols=len(columnInfos)
        numRows=listLen/numCols
        if (listLen%numCols>0) :
            numRows+=1
        thisRow=0
        while thisRow<numRows:
            listPos=thisRow
            for columnInfo in columnInfos:
                if listPos>=listLen:
                    break
                outString=self.stringList[listPos]
                outString+=(' ' * (columnInfo.width - len(self.stringList[listPos])))
                sys.stdout.write(outString)
                listPos+=numRows
            sys.stdout.write('\n')
            thisRow+=1
        sys.stdout.flush()

class ComparisonError(Exception):
    """Exception thrown when the output comparison sees differences"""

class MakeError(Exception):
    """Exception thrown when the a make command fails"""

class CommandLineError(Exception):
    """Exception thrown when the script is invoked with bad command line arguments"""

class ConfigError(Exception):
    """Exception thrown when there is a problem with the environment configuration"""

def fileCompare(fcfileName,fcmode,ignoreString):
    referenceFile = os.path.join("Reference",fcmode + fcfileName)
    if not (os.path.exists(referenceFile)):
	sys.stdout.write("   "+referenceFile +" not available")
	if not (globalBatchMode):
            answer=""
            if globalAcceptAll:
                answer="y"
            else:    
                if (globalOfferAcceptAsDefault) :
                    answer = (raw_input(", copy and hg add it? (y)/n: "))
                    if (answer != "n") :
                        answer="y"
                else:
                    answer = (raw_input(", copy and hg add it? y/(n): "))
                    if (answer != "y") :
                        answer="n"
            if (answer == "n"):
		sys.stdout.write("   cannot verify %s\n" % fcfileName)
                sys.stdout.flush()
		return 0
	    else:
		shutil.copy(fcfileName,referenceFile)
		if (os.system("hg add "+referenceFile)):
		    raise RuntimeError, "\"hg add "+referenceFile+" not successful" 
	else: # BATCHMODE
	    sys.stdout.write("\n")
            sys.stdout.flush()
            return 0
    cmd="diff -I '"+ignoreString+"' "+fcfileName+" "+referenceFile        
    hasDiff = os.system(cmd)
    if (hasDiff == 512):
	raise RuntimeError, "command "+cmd+" not successful"
    elif (hasDiff == 256):
	sys.stdout.write("   Transformation -- diff "+fcfileName+" "+referenceFile+"\n")
	if not (globalBatchMode):
            answer=""
            if globalAcceptAll:
                answer="y"
            else:    
                if (globalOfferAcceptAsDefault) :
                    answer = raw_input("   accept/copy new %s to %s? (y)/n: " % (fcfileName,referenceFile))
                    if (answer != "n"):
                        answer="y"
                else:
                    answer = raw_input("   accept/copy new %s to %s? y/(n): " % (fcfileName,referenceFile))
                    if (answer != "y"):
                        answer="n"
            if (answer == "n"):
		sys.stdout.write("   skipping change\n")
	    else:
		shutil.copy(fcfileName,referenceFile)
    sys.stdout.flush()


def printSep(sepChar,msg,sepLength):
    sys.stdout.write(msg)
    i = 0
    while (i < sepLength - len(msg)):
	sys.stdout.write(sepChar)
	i = i + 1
    sys.stdout.write("\n")
    sys.stdout.flush()

def numberedList(list):
    numberedList=[]
    digits=len(str(len(list)+1))
    format='%'+str(digits)+'d:%s'
    for (c,e) in enumerate(list):
        numberedName=format%(c+1,e)
        numberedList.append(numberedName)
    return numberedList

def populateExamplesList(args):
    import glob
    cleanUpFiles = glob.glob("*pre*")
#    cleanUpFiles = cleanUpFiles + glob.glob("*.B")
    for i in cleanUpFiles:
        os.remove(i)
    allExamples = glob.glob(os.path.join("TestSources","*.f"))
    allExamples = allExamples + glob.glob(os.path.join("TestSources","*.f90"))
    allExamples = [ os.path.split(e)[1] for e in allExamples]
    allExamples.sort(key=str.lower) # default sort is case sensitive, this one isn't
    rangeStart = 1
    rangeEnd = len(allExamples)
    examples = []
    exampleRegexs = []
    if (len(args) == 0): # no arguments
	if (globalBatchMode):
	    examples = allExamples
	else:
	    done = False
	    while not (done):
		done = True
		sys.stdout.write("pick from the following examples:\n")
		sys.stdout.flush()
                examples = allExamples
                MultiColumnOutput(numberedList(examples)).printIt()    
		examplesInput = raw_input("enter one or more regular expressions here or '(all [%i | %i %i])': ").split()
		if (len(examplesInput) == 0):			# no arguments
		    examples = allExamples
		elif (examplesInput[0] == "all"):		# the first argument is "all"
		    try:
			if (len(examplesInput) >= 2):
			    rangeStart = int(examplesInput[1])
			if (len(examplesInput) >= 3):
			    rangeEnd = int(examplesInput[2])
		    except ValueError:
			sys.stdout.write("\"all\" must be followed by zero, one, or two integers which specify the start and end range, e.g. 'all [%i | %i %i]'\n")
			sys.stdout.flush()
			done = False
			rangeStart = 1
			rangeEnd = len(allExamples)
		    if (rangeStart < 1 or rangeEnd > len(allExamples)):
			sys.stdout.write("invalid range (%i-%i)\n" % (rangeStart,rangeEnd))
			sys.stdout.flush()
			done = False
			rangeStart = 1
			rangeEnd = len(allExamples)
		    examples = allExamples
		else:						# one or more arguments, and the first one isn't "all"
		    exampleRegexs = examplesInput
    else: # at least one argument
	if (args[0] == "all"): # the first argument was all
	    examples = allExamples
	    try:
		if (len(args) >= 2): # A range START is given
		    rangeStart = int(args[1])
		if (len(args) >= 3): # A range END is also given
		    rangeEnd = int(args[2])
	    except ValueError:
		raise CommandLineError, "\"all\" must be followed by zero, one, or two integers which specify the start and end range, e.g. 'all [%i | %i %i]'"
	else: # each argument is treated as a regex
	    exampleRegexs = args

    # user running examples specified by one or more regular expressions
    if (len(examples) == 0):
	for regex in exampleRegexs:
	    for ex in allExamples:
		if (re.search(regex,ex,re.IGNORECASE)):
		    examples.append(ex)
	if (len(examples) == 0):
	    raise RuntimeError, "No examples match the given regular expressions"
	exampleSet = set(examples)
	examples = list(exampleSet)
	examples.sort(key=str.lower)
	rangeStart = 1

	rangeEnd = len(examples)
	printSep("=","",sepLength)
	sys.stdout.write("The following examples match the given regular expression(s):\n")
        MultiColumnOutput(numberedList(examples)).printIt()    
	printSep("=","",sepLength)
    else:
	printSep("=","",sepLength)
	sys.stdout.write("Running all examples with a range of (%i-%i):\n" % (rangeStart,rangeEnd))
        MultiColumnOutput(numberedList(examples)[rangeStart-1:rangeEnd]).printIt()    
	printSep("=","",sepLength)
    return (examples,rangeStart,rangeEnd)



def runTest(exName,exNum,totalNum,compiler,optimizeFlag,extraObjs):
    import filecmp
    preProcess=os.path.join(os.environ['OPENADFORTTK_BASE'],'tools','SourceProcessing','preProcess.py')
    sys.stdout.flush()
    basename,ext=os.path.splitext(exName)
    failCountAdjusted=False
    haveRef=os.path.exists(os.path.join('Reference',basename+'.pre'+ext))
    if not haveRef :
        if globalIgnoreFailingCases : 
            printSep("*","** skipping %i of %i (%s) - no reference file" % (exNum,totalNum,exName),sepLength)
            if (os.path.exists(os.path.join('Reference',exName+'.FAIL'))):
                sys.stdout.write("   failure reason:")
                sys.stdout.flush()
                os.system("cat "+os.path.join('Reference',exName+'.FAIL'))
            return 0
        else: 
            printSep("*","** testing %i of %i (%s)" % (exNum,totalNum,exName),sepLength)
        if (os.path.exists(os.path.join('Reference',exName+'.FAIL'))):
                sys.stdout.write("   failure reason:")
                sys.stdout.flush()
                os.system("cat "+os.path.join('Reference',exName+'.FAIL'))
	sys.stdout.write("   reference file: "+basename+'.pre'+ext+' unavailable')
	if not (globalBatchMode):
            answer=""
            if globalAcceptAll:
                answer="y"
            else:    
                if (globalOfferAcceptAsDefault) :
                    answer = (raw_input(", run it anyway? (y)/n: "))
                    if (answer != "n") :
                        answer="y"
                else:
                    answer = (raw_input(", run it anyway? y/(n): "))
                    if (answer != "y") :
                        answer="n"
            if (answer == "n"):
                sys.stdout.flush()
		return 0
	else:
            if ( not globalAcceptAll): 
                sys.stdout.write("\n")
                sys.stdout.flush()
                return 0
        global globalKnownFailCount
        globalKnownFailCount+=1
        global globalNewFailCount
        globalNewFailCount-=1
        failCountAdjusted=True
    else:
        printSep("*","** testing %i of %i (%s)" % (exNum,totalNum,exName),sepLength)
    cmd="ln -sf "+os.path.join("TestSources",exName) + " " + exName
    if globalVerbose :
        print cmd
    if (os.system(cmd)):
	raise MakeError, "Error while executing \"" + cmd + "\""

    originalSource = basename+ext
    originalExec = basename+'.run'
    originalOutput = basename+'.out'
    preprocessedSource = basename+'.pre'+ext
    preprocessedExec = basename+'.pre.run'
    preprocessedOutput = basename+'.pre.out'

    # compile and run original
    cmd=compiler+" "+optimizeFlag+" "+os.environ['F90FLAGS']+' -o '+originalExec+' '+exName+' '+extraObjs
    if globalVerbose: print cmd
    if (os.system(cmd)): raise MakeError, "Error while executing \"" + cmd + "\""

    cmd='./'+originalExec+' > '+originalOutput
    if globalVerbose: print cmd
    if (os.system(cmd)): raise MakeError, "Error while executing \"" + cmd + "\""
    fileCompare(originalOutput,'','')

    # set free/fixed
    freeFlag = re.search('free',basename) and '--free ' or ''
    # set verbose
    verbosePreProcess = globalVerbose and ' -v' or ''

    # perform preprocessing
    cmd=preProcess+' '+originalSource+' '+freeFlag+'-o '+preprocessedSource+verbosePreProcess
    if globalVerbose: print cmd
    if (os.system(cmd)): raise MakeError, "Error while executing \"" + cmd + "\""
    fileCompare(preprocessedSource,'','')

    # compile and run preprocessed
    cmd=compiler+" "+optimizeFlag+" "+os.environ['F90FLAGS']+" -o " +preprocessedExec+' '+preprocessedSource+' '+extraObjs
    if globalVerbose: print cmd
    if (os.system(cmd)): raise MakeError, "Error while executing \"" + cmd + "\""
    cmd='./'+preprocessedExec+' > '+preprocessedOutput
    if globalVerbose: print cmd
    if (os.system(cmd)): raise MakeError, "Error while executing \"" + cmd + "\""
    fileCompare(preprocessedOutput,'','')

    # compare results
    if (filecmp.cmp(originalOutput,preprocessedOutput)!=1):
        raise ComparisonError,'diff '+originalOutput+' '+preprocessedOutput
    printSep("*","",sepLength)
    global globalOkCount
    globalOkCount+=1
    if failCountAdjusted:
        globalKnownFailCount-=1
        globalNewFailCount+=1
        failCountAdjusted=True

def main():
    import glob
    from optparse import OptionParser
    usage = '%prog [options] '
    compilers=['ifort','gfortran','g95','f95','openf95']
    compilerOpts='[ '
    for i in compilers :
        compilerOpts+=i
        if  i != compilers[-1]:
            compilerOpts+=" | "
    compilerOpts+=" ]"        
    opt = OptionParser(usage=usage)
    opt.add_option('-i','--ignoreFailingCases',dest='ignoreFailingCases',
                   help="don't if we should try to run  the cases known to fail",
                   action='store_true',default=False)
    opt.add_option('-a','--offerAcceptAsDefault',dest='offerAcceptAsDefault',
                   help="offer accept as default for updating reference files",
                   action='store_true',default=False)
    opt.add_option('-A','--acceptAll',dest='acceptAll',
                   help="accept all changes without confirmation",
                   action='store_true',default=False)
    opt.add_option('-b','--batchMode',dest='batchMode',
                   help="run in batchMode suppressing output",
                   action='store_true',default=False)
    opt.add_option('-v','--verbose',dest='verbose',
                   help="let the pipeline components produce some extra output",
                   action='store_true',default=False)
    opt.add_option('-c','--compiler',dest='compiler',
                   type='choice', choices=compilers,
                   help="pick a compiler (defaults to ifort) from the following list: " +compilerOpts+" - the compiler should be in PATH; we use F90FLAGS when set in the environment",
                   default='ifort')
    opt.add_option('-O','--optimize',dest='optimize',
                   help="turn compiler optimization on (default off)",
                   action='store_true',default=False)
    opt.add_option('-u','--unstructure',dest='unstructured',
                   help="translate as unstructured control flow (default off)",
                   action='store_true',default=False)
    (options, args) = opt.parse_args()
    global globalNewFailCount
    globalNewFailCount=0
    try:
        if os.environ.has_key('BATCHMODE') or options.batchMode :
            global globalBatchMode
            globalBatchMode=True
        if options.ignoreFailingCases :
            global globalIgnoreFailingCases
            globalIgnoreFailingCases=True
        if options.offerAcceptAsDefault :
            global globalOfferAcceptAsDefault
            globalOfferAcceptAsDefault=True
        if options.acceptAll :
            global globalAcceptAll
            globalAcceptAll=True
        if options.verbose :
            global globalVerbose
            globalVerbose=True
        if options.unstructured :
            global globalUnstructured
            globalUnstructured=True
        if options.optimize :
            os.environ['OPTIMIZE']='true'
	if not (os.environ.has_key('OPENADFORTTK_BASE')):
	    raise ConfigError, "environment variable OPENADFORTTK_BASE not defined"
	if not (os.environ.has_key('F90FLAGS')):
            os.environ['F90FLAGS']=''
        optimizeFlag='-O0 -g'
        if options.optimize:
	  optimizeFlag='-O3'
        extraFiles = glob.glob(os.path.join('Extras','*.f90'))
        extraObjs=""
        for extraFile in extraFiles:
            cmd=options.compiler+" "+optimizeFlag+" "+os.environ['F90FLAGS']+" -c "+ extraFile
            if (os.system(cmd)):
                raise MakeError, "Error while executing \"" + cmd + "\""
            extraObjs+=(os.path.splitext(os.path.basename(extraFile)))[0]+".o "
	(examples,rangeStart,rangeEnd) = populateExamplesList(args[0:])
	# Run the examples
	j = rangeStart-1
	while (j < rangeEnd):
	    try:
		runTest(examples[j],j+1,len(examples), options.compiler, optimizeFlag, extraObjs)
	    except ConfigError, errMsg:
		print "ERROR (environment configuration) in test %i of %i (%s): %s" % (j+1,len(examples),examples[j],errMsg)
	        globalNewFailCount+=1
		if not (globalBatchMode):
		    if (raw_input("Do you want to continue? (y)/n: ") == "n"):
			return -1
		else:
		    return -1
	    except MakeError, errMsg:
		print "ERROR in test %i of %i (%s) while executing \"%s\"." % (j+1,len(examples),examples[j],errMsg)
	        globalNewFailCount+=1
		if not (globalBatchMode):
		    if (raw_input("Do you want to continue? (y)/n: ") == "n"):
			return -1
		else:
		    return -1
	    except ComparisonError, errMsg:
		print "ERROR in test %i of %i (%s): %s." % (j+1,len(examples),examples[j],errMsg)
	        globalNewFailCount+=1
		if not (globalBatchMode):
		    if (raw_input("Do you want to continue? (y)/n: ") == "n"):
			return -1
	    except RuntimeError, errMsg:
		print "ERROR in test %i of %i (%s): %s." % (j+1,len(examples),examples[j],errMsg)
	        globalNewFailCount+=1
		if not (globalBatchMode):
		    if (raw_input("Do you want to continue? (y)/n: ") == "n"):
			return -1
		else:
			return -1
	    j = j + 1
    except ConfigError, errMsg:
	print "ERROR (environment configuration):",errMsg
	return -1
    except CommandLineError, errMsg:
	print "ERROR (command line arguments):",errMsg
	return -1
    except RuntimeError, errMsg:
	print 'caught exception: ',errMsg
	return -1
    print "total: "+str(rangeEnd-rangeStart+1)+", ran  OK:"+str(globalOkCount)+", known errors:"+str(globalKnownFailCount)+", new errors:"+str(globalNewFailCount)
    return 0

if __name__ == "__main__":
    sys.exit(main())

