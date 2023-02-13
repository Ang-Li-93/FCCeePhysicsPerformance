#python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py
#Input directory where the files produced at the pre-selection level are
inputDir = "/eos/user/l/lia/FCCee/NewWorkFlow/BDT_analysis_samples"

#Input directory where the files produced at the pre-selection level are
outputDir = "/eos/user/l/lia/FCCee/NewWorkFlow/BDT_analysis_samples/final"

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
              #'wzp6_ee_mumuH_ecm240',
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
            "sel_Baseline":"zll_m > 86 && zll_m < 96 && zll_recoil_m > 120 &&zll_recoil_m <140 && zll_p > 20 && zll_p <70 && cosTheta_miss.size() >=1 && cosTheta_miss[0] > -0.98 && cosTheta_miss[0] < 0.98",
            "sel_Baseline_MVA02":"BDTscore>0.2 && zll_m > 86 && zll_m < 96 && zll_recoil_m > 120 &&zll_recoil_m <140 && zll_p > 20 && zll_p <70 && cosTheta_miss.size() >=1 && cosTheta_miss[0] > -0.98 && cosTheta_miss[0]  < 0.98",
            "sel_Baseline_MVA06":"BDTscore>0.6 && zll_m > 86 && zll_m < 96 && zll_recoil_m > 120 &&zll_recoil_m <140 && zll_p > 20 && zll_p <70 && cosTheta_miss.size() >=1 && cosTheta_miss[0] > -0.98 && cosTheta_miss[0]  < 0.98",
            ###APC3
            "sel0_MRecoil_Mll_73_120_pll_05":"zll_m > 73 && zll_m  < 120 && zll_recoil_m > 120 &&zll_recoil_m <140 && zll_p > 5",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA01":"BDTscore>0.1 && zll_m>73 && zll_m<120 && zll_recoil_m>120 && zll_recoil_m<140 && zll_p>5", 
            "sel0_MRecoil_Mll_73_120_pll_05_MVA02":"BDTscore>0.2 && zll_m>73 && zll_m<120 && zll_recoil_m>120 && zll_recoil_m<140 && zll_p>5", 
            "sel0_MRecoil_Mll_73_120_pll_05_MVA03":"BDTscore>0.3 && zll_m>73 && zll_m<120 && zll_recoil_m>120 && zll_recoil_m<140 && zll_p>5", 
            "sel0_MRecoil_Mll_73_120_pll_05_MVA04":"BDTscore>0.4 && zll_m>73 && zll_m<120 && zll_recoil_m>120 && zll_recoil_m<140 && zll_p>5", 
            "sel0_MRecoil_Mll_73_120_pll_05_MVA05":"BDTscore>0.5 && zll_m>73 && zll_m<120 && zll_recoil_m>120 && zll_recoil_m<140 && zll_p>5",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA06":"BDTscore>0.6 && zll_m>73 && zll_m<120 && zll_recoil_m>120 && zll_recoil_m<140 && zll_p>5",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA07":"BDTscore>0.7 && zll_m>73 && zll_m<120 && zll_recoil_m>120 && zll_recoil_m<140 && zll_p>5",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA08":"BDTscore>0.8 && zll_m>73 && zll_m<120 && zll_recoil_m>120 && zll_recoil_m<140 && zll_p>5",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA09":"BDTscore>0.9 && zll_m>73 && zll_m<120 && zll_recoil_m>120 && zll_recoil_m<140 && zll_p>5",
            ###APC3+costhetamissing
            "sel0_MRecoil_Mll_73_120_pll_05_costhetamiss":"  zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m  <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA01_costhetamiss":"BDTscore>0.1 &&   zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA02_costhetamiss":"BDTscore>0.2 &&   zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA03_costhetamiss":"BDTscore>0.3 &&   zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA04_costhetamiss":"BDTscore>0.4 &&   zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;", 
            "sel0_MRecoil_Mll_73_120_pll_05_MVA05_costhetamiss":"BDTscore>0.5 &&   zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA06_costhetamiss":"BDTscore>0.6 &&   zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA07_costhetamiss":"BDTscore>0.7 &&   zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA08_costhetamiss":"BDTscore>0.8 &&   zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;",
            "sel0_MRecoil_Mll_73_120_pll_05_MVA09_costhetamiss":"BDTscore>0.9 &&   zll_m  > 73 &&  zll_m  < 120  && zll_recoil_m  > 120 &&zll_recoil_m <140 && zll_p  > 5&& cosTheta_miss.size() >=1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98;",
            ###baseline without costhetamiss 
            "sel_Baseline_no_costhetamiss":"zll_m  > 86 && zll_m  < 96  && zll_recoil_m > 120 &&zll_recoil_m  <140 && zll_p  > 20 && zll_p  <70",
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "mz":{"name":"zll_m","title":"m_{Z} [GeV]","bin":125,"xmin":0,"xmax":250},
    "mz_zoom1":{"name":"zll_m","title":"m_{Z} [GeV]","bin":200,"xmin":80,"xmax":100},
    "mz_zoom2":{"name":"zll_m","title":"m_{Z} [GeV]","bin":100,"xmin":86,"xmax":96},
    "mz_zoom3":{"name":"zll_m","title":"m_{Z} [GeV]","bin":250,"xmin":75,"xmax":100},
    "mz_zoom4":{"name":"zll_m","title":"m_{Z} [GeV]","bin":235,"xmin":73,"xmax":120},
    "leptonic_recoil_m":{"name":"zll_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":0,"xmax":200},
    "leptonic_recoil_m_zoom1":{"name":"zll_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":80,"xmax":160},
    "leptonic_recoil_m_zoom2":{"name":"zll_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom3":{"name":"zll_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom4":{"name":"zll_recoil_m","title":"Z leptonic recoil [GeV]","bin":70,"xmin":123,"xmax":130},
    "leptonic_recoil_m_zoom5":{"name":"zll_recoil_m","title":"Z leptonic recoil [GeV]","bin":20,"xmin":124,"xmax":126}, 
    "leptonic_recoil_m_zoom6":{"name":"zll_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":110,"xmax":150}, 
    "BDT_Score":{"name":"BDTscore","title":"BDT Score","bin":100,"xmin":0,"xmax":1}, 
    "BDT_Score_zoom1":{"name":"BDTscore","title":"BDT Score","bin":110,"xmin":0,"xmax":1.1},  
    #more control variables
    "zll_leptons_acolinearity":{"name":"zll_leptons_acolinearity","title":"acolinearity","bin":100,"xmin":-5,"xmax":5},
    "zll_leptons_acoplanarity":{"name":"zll_leptons_acoplanarity","title":"acoplanarity","bin":100,"xmin":-5,"xmax":5},
    "cosTheta_miss":{"name":"cosTheta_miss","title":"cos#theta_{missing}","bin":200,"xmin":-1,"xmax":1},
    #plot fundamental varibales:
    "leading_zll_lepton_p":{"name":"leading_zll_lepton_p","title":"leading_zll_lepton_p","bin":200,"xmin":0,"xmax":200},
    "leading_zll_lepton_theta":{"name":"leading_zll_lepton_theta","title":"leading_zll_lepton_theta","bin":70,"xmin":-3.5,"xmax":3.5},
    "leading_zll_lepton_phi":{"name":"leading_zll_lepton_phi","title":"leading_zll_lepton_phi","bin":70,"xmin":-3.5,"xmax":3.5},
    "subleading_zll_lepton_p":{"name":"subleading_zll_lepton_p","title":"subleading_zll_lepton_p","bin":200,"xmin":0,"xmax":200},
    "subleading_zll_lepton_theta":{"name":"subleading_zll_lepton_theta","title":"subleading_zll_lepton_theta","bin":70,"xmin":-3.5,"xmax":3.5},
    "subleading_zll_lepton_phi":{"name":"subleading_zll_lepton_phi","title":"subleading_zll_lepton_phi","bin":70,"xmin":-3.5,"xmax":3.5},
    #Zed
    "zll_p":{"name":"zll_p","title":"zll_p","bin":200,"xmin":0,"xmax":200},
    "zll_theta":{"name":"zll_theta","title":"zll_theta","bin":70,"xmin":-3.5,"xmax":3.5},
    "zll_phi":{"name":"zll_phi","title":"zll_phi","bin":70,"xmin":-3.5,"xmax":3.5},
    #Higgsstrahlungness
    "H":{"name":"H","title":"Higgsstrahlungness","bin":200,"xmin":0,"xmax":200},
    #number of leptons
    "leps_no":{"name":"leps_no","title":"number of leptons","bin":6,"xmin":-0.5,"xmax":5.5},
}



