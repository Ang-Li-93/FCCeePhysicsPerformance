import ROOT
import os, sys
import time
import subprocess
import datetime

date=datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d_%H-%M-%S')

#__________________________________________________________
def getCommandOutput(command):
    p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE,universal_newlines=True)
    (stdout,stderr) = p.communicate()
    return {"stdout":stdout, "stderr":stderr, "returncode":p.returncode}


#__________________________________________________________
def SubmitToCondor(cmd,nbtrials):
    submissionStatus=0
    cmd=cmd.replace('//','/') # -> dav : is it needed?
    for i in range(nbtrials):
        outputCMD = getCommandOutput(cmd)
        stderr=outputCMD["stderr"].split('\n')
        stdout=outputCMD["stdout"].split('\n') # -> dav : is it needed?

        if len(stderr)==1 and stderr[0]=='' :
            print ("----> GOOD SUBMISSION")
            submissionStatus=1
        else:
            print ("----> ERROR submitting, will retry")
            print ("----> Trial : "+str(i)+" / "+str(nbtrials))
            print ("----> stderr : ",len(stderr))
            print (stderr)

            time.sleep(10)

        if submissionStatus==1:
            return 1

        if i==nbtrials-1:
            print ("failed sumbmitting after: "+str(nbtrials)+" trials, stop trying to submit")
            return 0

#__________________________________________________________
def Generate(Detector, process, n):
    localDir = os.environ["MH_RECOIL_DIR"]
    logDir   = localDir+"/BatchOutputs/{}/{}".format(date,process)
    if not os.path.exists(logDir):
        os.system("mkdir -p {}".format(logDir))

    condor_file_str=''

    frunname='/afs/cern.ch/work/l/lia/private/FCC/MVA/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/Generation/generate.sh'
    print('----> script to run : ',frunname)
    condor_file_str+=frunname+" "
    condor_file_str+="{} {}".format(Detector, process)

    condor_file_str=condor_file_str.replace("//","/")
    frunname_condor = 'job_desc_{}.cfg'.format(process)
    frunfull_condor = '%s/%s'%(logDir,frunname_condor)
    frun_condor = None
    try:
        frun_condor = open(frunfull_condor, 'w')
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        time.sleep(10)
        frun_condor = open(frunfull_condor, 'w')
    frun_condor.write('universe         = vanilla\n')
    frun_condor.write('Log              = {}/condor_job.{}.$(ClusterId).$(ProcId).log\n'.format(logDir,process))
    frun_condor.write('Output           = {}/condor_job.{}.$(ClusterId).$(ProcId).out\n'.format(logDir,process))
    frun_condor.write('Error            = {}/condor_job.{}.$(ClusterId).$(ProcId).error\n'.format(logDir,process))
    frun_condor.write('getenv           = True\n')
    frun_condor.write('environment      = "LS_SUBCWD={}"\n'.format(logDir)) # not sure
    frun_condor.write('requirements     = ( (OpSysAndVer =?= "CentOS7") && (Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) )\n')
    frun_condor.write('on_exit_remove   = (ExitBySignal == False) && (ExitCode == 0)\n')
    frun_condor.write('max_retries      = 3\n')
    frun_condor.write('+JobFlavour      = "{}"\n'.format("tomorrow"))
    frun_condor.write('+AccountingGroup = "{}"\n'.format("group_u_FCC.local_gen"))
    frun_condor.write('RequestCpus      = {}\n'.format("4"))
    frun_condor.write('executable       = {}\n'.format(frunname))
    #for process in processes:
    for i in range(n):
        frun_condor.write('arguments        = {} {} {}\n'.format(Detector,process,'$(ClusterId)$(ProcId)'))
        frun_condor.write('queue\n') 
    frun_condor.close()

    cmdBatch="condor_submit {}".format(frunfull_condor)
    print ('----> batch command  : ',cmdBatch)
    job=SubmitToCondor(cmdBatch,10)

#__________________________________________________________
if __name__ == "__main__":
    
    Processes = [   'wzp6_ee_mumuH_ecm240',
                    'p8_ee_WW_mumu_ecm240',
                    'wzp6_egamma_eZ_Zmumu_ecm240',
                    'wzp6_gammae_eZ_Zmumu_ecm240',
                    'wzp6_ee_mumu_ecm240',
                    'p8_ee_ZZ_ecm240'
    ]
    n_files = 10
    for Process in Processes:
        Generate("IDEA",Process,n_files)

