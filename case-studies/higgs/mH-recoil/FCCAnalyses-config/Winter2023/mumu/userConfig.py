import os
#repo = os.getenv('PWD')
repo = "/eos/user/l/lia/FCCee/Winter2023/mumu"
#repo can be changed, but by default writes locally
class loc : pass
loc.ROOT = repo+'/'
loc.OUT = loc.ROOT+'output_trained/'
loc.DATA = loc.ROOT+'data'
loc.CSV = loc.DATA+'/csv'
loc.PKL = loc.DATA+'/pkl'
loc.PKL_Val = loc.DATA+'/pkl_val'
loc.ROOTFILES = loc.DATA+'/ROOT'
loc.PLOTS = loc.DATA+'/plots'
#loc.PLOTS = loc.OUT+'plots'
loc.PLOTS_Val = loc.OUT+'plots_val'
loc.TEX = loc.OUT+'tex'
loc.JSON = loc.OUT+'json'

#EOS location for files used in analysis
loc.EOS = "/eos/user/l/lia/FCCee/Winter2023/mumu"

#Output BDT model location - used in official sample production to assign MVA weights
loc.BDT = f"{loc.EOS}/BDT"

#Loaction of prod_04 tuples used in analysis
loc.PROD = f"{loc.EOS}"

#Samples for first stage BDT training
loc.TRAIN = f"{loc.PROD}/MVANtuples"

#Samples for second stage training
loc.TRAIN2 = f"{loc.PROD}/Training_4stage2/"

#Samples for final analysis
loc.ANALYSIS = f"{loc.PROD}/BDT_analysis_samples/"

#First stage BDT including event-level vars
train_vars = [
              #leptons
              "leading_zll_lepton_p",
              "leading_zll_lepton_theta",
              "subleading_zll_lepton_p",
              "subleading_zll_lepton_theta",
              "zll_leptons_acolinearity",
              "zll_leptons_acoplanarity",
              #Zed
              "zll_m",
              "zll_p",
              "zll_theta"
              #Higgsstrahlungness
              #"H",
              ]

#First stage BDT including event-level vars and vertex vars
#This is the default list used in the analysis
train_vars_vtx = ["EVT_ThrustEmin_E",
                  "EVT_ThrustEmax_E",
                  "EVT_ThrustEmin_Echarged",
                  "EVT_ThrustEmax_Echarged",
                  "EVT_ThrustEmin_Eneutral",
                  "EVT_ThrustEmax_Eneutral",
                  "EVT_ThrustEmin_Ncharged",
                  "EVT_ThrustEmax_Ncharged",
                  "EVT_ThrustEmin_Nneutral",
                  "EVT_ThrustEmax_Nneutral",
                  "EVT_NtracksPV",
                  "EVT_NVertex",
                  "EVT_NTau23Pi",
                  "EVT_ThrustEmin_NDV",
                  "EVT_ThrustEmax_NDV",
                  "EVT_dPV2DVmin",
                  "EVT_dPV2DVmax",
                  "EVT_dPV2DVave"
                  ]


#Decay modes used in first stage training and their respective file names
mode_names = {"mumuH": "wzp6_ee_mumuH_ecm240",
              "ZZ": "p8_ee_ZZ_ecm240",
              "WWmumu": "p8_ee_WW_mumu_ecm240",
              "Zll": "wzp6_ee_mumu_ecm240",
              "egamma": "wzp6_egamma_eZ_Zmumu_ecm240",
              "gammae": "wzp6_gammae_eZ_Zmumu_ecm240",
              "gaga_mumu": "wzp6_gaga_mumu_60_ecm240"}

#Second stage training variables
train_vars_2 = ["EVT_CandMass",
                "EVT_CandRho1Mass",
                "EVT_CandRho2Mass",
                "EVT_CandN",
                "EVT_CandVtxFD",
                "EVT_CandVtxChi2",
                "EVT_CandPx",
                "EVT_CandPy",
                "EVT_CandPz",
                "EVT_CandP",
                "EVT_CandD0",
                "EVT_CandZ0",
                "EVT_CandAngleThrust",
                "EVT_DVd0_min",
                "EVT_DVd0_max",
                "EVT_DVd0_ave",
                "EVT_DVz0_min",
                "EVT_DVz0_max",
                "EVT_DVz0_ave",
                "EVT_PVmass",
                "EVT_Nominal_B_E"
               ]

#Hemipshere energy difference cut, applied offline prior to MVA2 optimisation
Ediff_cut = ">10."
