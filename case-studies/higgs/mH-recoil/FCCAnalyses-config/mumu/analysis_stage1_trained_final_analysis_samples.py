#python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py
#Input directory where the files produced at the pre-selection level are
inputDir  = "/eos/user/l/lia/FCCee/MVA_Final/trainedNtuples_analysis_samples"

#Input directory where the files produced at the pre-selection level are
outputDir  = "/eos/user/l/lia/FCCee/MVA_Final/trainedNtuples_analysis_samples/final"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_spring2021_IDEA.json"
#Add MySample_p8_ee_ZH_ecm240 as it is not an offical process
procDictAdd={"mywzp6_ee_mumuH_ecm240": {"numberOfEvents": 1000000, "sumOfWeights": 1000000.0, "crossSection": 0.0067643, "kfactor": 1.0, "matchingEfficiency": 1.0}}
#procDictAdd={"wzp6_ee_mumuH_ecm240": {"numberOfEvents": 1000000, "sumOfWeights": 1000000.0, "crossSection": 0.0067643, "kfactor": 1.0, "matchingEfficiency": 1.0},
#              "p8_ee_ZZ_ecm240": {"numberOfEvents": 59800000, "sumOfWeights": 59800000, "crossSection": 1.35899, "kfactor": 1.0, "matchingEfficiency": 1.0},
#              "p8_ee_WW_mumu_ecm240": {"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 0.25792, "kfactor": 1.0, "matchingEfficiency": 1.0},
#              "wzp6_ee_mumu_ecm240": {"numberOfEvents": 49400000, "sumOfWeights": 49400000.0, "crossSection": 5.288, "kfactor": 1.0, "matchingEfficiency": 1.0},
#              "wzp6_egamma_eZ_Zmumu_ecm240": {"numberOfEvents": 5000000, "sumOfWeights": 5000000.0, "crossSection": 0.10368, "kfactor": 1.0, "matchingEfficiency": 1.0},
#              "wzp6_gammae_eZ_Zmumu_ecm240": {"numberOfEvents": 5000000, "sumOfWeights": 5000000.0, "crossSection": 0.10368, "kfactor": 1.0, "matchingEfficiency": 1.0}
#             }
###Process list that should match the produced files.
processList=['p8_ee_ZZ_ecm240',
              'p8_ee_WW_mumu_ecm240',
              'wzp6_ee_mumuH_ecm240',
              'wzp6_ee_mumu_ecm240',
              'wzp6_egamma_eZ_Zmumu_ecm240',
              'wzp6_gammae_eZ_Zmumu_ecm240']

###Add MySample_p8_ee_ZH_ecm240 as it is not an offical process

#Number of CPUs to use
nCPUS = 2
#produces ROOT TTrees, default is False
doTree = False

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = { "sel0":"return true;",
            #"sel_MVA02":"MVAScore0>0.2;",
            #"sel_MVA04":"MVAScore0>0.4;",
            #"sel_MVA06":"MVAScore0>0.6;",
            #"sel_MVA08":"MVAScore0>0.8;",
            #"sel_MVA09":"MVAScore0>0.9;", 
            "sel_Baseline":"Z_leptonic_m  > 86 && Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70 && missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98",
            "sel_Baseline_MVA02":"MVAScore0>0.2 && Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70 && missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98",
            "sel_Baseline_MVA06":"MVAScore0>0.6 && Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70 && missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98",
            #"sel_Baseline":"Z_leptonic_m  > 86 && Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70 && missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98",
            #"sel_Baseline_MVA02":"MVAScore0>0.2 && Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70 && missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98",
            #"sel_Baseline_MVA06":"MVAScore0>0.6 && Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70 && missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98", 
            #"sel_APC1":"  Z_leptonic_m  > 86 && Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",
            #"sel_APC1_MVA02":"MVAScore0>0.2 && Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",
            #"sel_APC1_MVA06":"MVAScore0>0.6 && Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",
            #"sel_APC1_MVA02_mll_80_100":"MVAScore0>0.2 &&   Z_leptonic_m  > 80 &&  Z_leptonic_m  < 100 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",
            #"sel_APC1_MVA02_mll_75_100":"MVAScore0>0.2 &&   Z_leptonic_m  > 75 &&  Z_leptonic_m  < 100 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70", 
            #"sel_APC1_MVA02_mll_73_120":"MVAScore0>0.2 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70", 
            #"sel_APC1_MVA02_mll_80_100_nopT":"MVAScore0>0.2 && Z_leptonic_m  > 80 &&  Z_leptonic_m  < 100 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140",
            #"sel_APC1_MVA02_mll_80_100_pT20":"MVAScore0>0.2 && Z_leptonic_m  > 80 &&  Z_leptonic_m  < 100 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20",
            #"sel_APC1_MVA02_mll_80_100_pT10":"MVAScore0>0.2 && Z_leptonic_m  > 80 &&  Z_leptonic_m  < 100 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 10",
            #"sel0_MRecoil":"zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140",
            #"sel0_MRecoil_MVA02":"MVAScore0>0.2 && zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140",
            #"sel0_MRecoil_Mll":"Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140",
            #"sel0_MRecoil_Mll_MVA02":"MVAScore0>0.2 &&   Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140",
            #"sel0_MRecoil_pTll":"zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",
            #"sel0_MRecoil_pTll_MVA02":"MVAScore0>0.2 && zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",
            #"sel0_Mll":"  Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96",
            #"sel0_Mll_MVA02":"MVAScore0>0.2 &&   Z_leptonic_m  > 86 &&  Z_leptonic_m  < 96",
            #"sel0_pTll":"  Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",
            #"sel0_pTll_MVA02":"MVAScore0>0.2 &&   Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",
            #"sel0_MRecoil_Mll_80_100":"  Z_leptonic_m  > 80 &&  Z_leptonic_m  < 100 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140",            
            #"sel0_MRecoil_Mll_75_100":"  Z_leptonic_m  > 75 &&  Z_leptonic_m  < 100 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140", 
            #"sel0_MRecoil_Mll_73_120":"  Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140",
            #"sel0_MRecoil_pTll_20":"zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20",
            #"sel0_MRecoil_pTll_15":"zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 15",
            #"sel0_MRecoil_pTll_10":"zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 10",
            #"sel0_MRecoil_pTll_05":"zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5",
            "sel0_MRecoil_Mll_73_120_pTll_05":"  Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA01":"MVAScore0>0.1 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5", 
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA02":"MVAScore0>0.2 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5", 
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA03":"MVAScore0>0.3 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5", 
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA04":"MVAScore0>0.4 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5", 
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA05":"MVAScore0>0.5 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA06":"MVAScore0>0.6 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA07":"MVAScore0>0.7 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA08":"MVAScore0>0.8 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA09":"MVAScore0>0.9 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5",
            #"sel0_MRecoil_Mll_73_120_pTll_05":"  Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA01":"MVAScore0>0.1 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA02":"MVAScore0>0.2 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA03":"MVAScore0>0.3 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5", 
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA04":"MVAScore0>0.4 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA05":"MVAScore0>0.5 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA06":"MVAScore0>0.6 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA08":"MVAScore0>0.8 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA09":"MVAScore0>0.9 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5",
            
            #"sel_MVA02_costhetamiss":"MVAScore0>0.2&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            #"sel_MVA04_costhetamiss":"MVAScore0>0.4&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            #"sel_MVA06_costhetamiss":"MVAScore0>0.6&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            #"sel_MVA08_costhetamiss":"MVAScore0>0.8&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            #"sel_MVA09_costhetamiss":"MVAScore0>0.9&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;", 
            "sel0_MRecoil_Mll_73_120_pTll_05_costhetamiss":"  Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA01_costhetamiss":"MVAScore0>0.1 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA02_costhetamiss":"MVAScore0>0.2 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA03_costhetamiss":"MVAScore0>0.3 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA04_costhetamiss":"MVAScore0>0.4 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;", 
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA05_costhetamiss":"MVAScore0>0.5 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA06_costhetamiss":"MVAScore0>0.6 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA07_costhetamiss":"MVAScore0>0.7 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA08_costhetamiss":"MVAScore0>0.8 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pTll_05_MVA09_costhetamiss":"MVAScore0>0.9 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            #"sel0_MRecoil_Mll_73_120_pTll_05_costhetamiss":"  Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA02_costhetamiss":"MVAScore0>0.2 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;", 
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA04_costhetamiss":"MVAScore0>0.4 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA06_costhetamiss":"MVAScore0>0.6 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA08_costhetamiss":"MVAScore0>0.8 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            #"sel0_MRecoil_Mll_73_120_pTll_05_MVA09_costhetamiss":"MVAScore0>0.9 &&   Z_leptonic_m  > 73 &&  Z_leptonic_m  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 5&& missingET_costheta.size() ==1 && missingET_costheta[0]  > -0.98 && missingET_costheta[0]  < 0.98;",
            
            "sel_Baseline_no_costhetamiss":"Z_leptonic_m  > 86 && Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",
            #"sel_Baseline_no_costhetamiss":"Z_leptonic_m  > 86 && Z_leptonic_m  < 96 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 110 &&zed_leptonic_recoil_m[0]  <150 && Z_leptonic_pt  > 20 && Z_leptonic_pt  <70",


              
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "mz":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":125,"xmin":0,"xmax":250},
    "mz_zoom1":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":200,"xmin":80,"xmax":100},
    "mz_zoom2":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":100,"xmin":86,"xmax":96},
    "mz_zoom3":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":250,"xmin":75,"xmax":100},
    "mz_zoom4":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":235,"xmin":73,"xmax":120},
    "leptonic_recoil_m":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":0,"xmax":200},
    "leptonic_recoil_m_zoom1":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":80,"xmax":160},
    "leptonic_recoil_m_zoom2":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom3":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom4":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":70,"xmin":123,"xmax":130},
    "leptonic_recoil_m_zoom5":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":20,"xmin":124,"xmax":126}, 
    "leptonic_recoil_m_zoom6":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":110,"xmax":150}, 
    "BDT_Score":{"name":"MVAScore0","title":"BDT Score","bin":100,"xmin":0,"xmax":1}, 
    "BDT_Score_zoom1":{"name":"MVAScore0","title":"BDT Score","bin":110,"xmin":0,"xmax":1.1},  
    #more control variables
    "muon_acolinearity":{"name":"muon_acolinearity","title":"acolinearity","bin":100,"xmin":-5,"xmax":5},
    "muon_acoplanarity":{"name":"muon_acoplanarity","title":"acoplanarity","bin":100,"xmin":-5,"xmax":5},
    "missingET_costheta":{"name":"missingET_costheta","title":"cos#theta_{missing}","bin":200,"xmin":-1,"xmax":1}   
}



