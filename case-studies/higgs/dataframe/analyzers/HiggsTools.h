
#ifndef  HiggsTools_ANALYZERS_H
#define  HiggsTools_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"

#include "ReconstructedParticle2MC.h"

namespace HiggsTools{
	///build the resonance from 2 particles from an arbitrary list of input ReconstructedPartilces. Keep the closest to the mass given as input
	struct resonanceZBuilder {
		float m_resonance_mass;
		resonanceZBuilder(float arg_resonance_mass);
		ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) ;
	};

        // temporary duplication. When arg_use_MC_Kinematics = true, the true kinematics will be used instead of the track momenta
        struct resonanceZBuilder2 {
                float m_resonance_mass;
                bool m_use_MC_Kinematics;
                resonanceZBuilder2(float arg_resonance_mass, bool arg_use_MC_Kinematics);
                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
                                ROOT::VecOps::RVec<int> recind,
                                ROOT::VecOps::RVec<int> mcind,
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                                ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) ;
        };


	/// return the costheta of the input ReconstructedParticles
	ROOT::VecOps::RVec<float> get_cosTheta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

	/// return the costheta of the input missing momentum 
  ROOT::VecOps::RVec<float> get_cosTheta_miss(ROOT::VecOps::RVec<Float_t>Px, ROOT::VecOps::RVec<Float_t>Py, ROOT::VecOps::RVec<Float_t>Pz, ROOT::VecOps::RVec<Float_t>E);
  ///return muon_quality_check result (at least one muon plus and one muon minus)
	ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  muon_quality_check(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sort_greater(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  //ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  get_subleading(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  float Reweighting_wzp_kkmc(float pT, float m);

  ///get acolinearity
  ROOT::VecOps::RVec<float> acolinearity(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  
  ///get acoplanarity
  ROOT::VecOps::RVec<float> acoplanarity(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
 
  /// muon scale shifts
  struct momentum_scale {
    momentum_scale(float arg_scaleunc);
    float scaleunc = 1.;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };
  /// to be added to your ReconstructedParticle.h :
  
  /// select ReconstructedParticles with a given type 
  struct sel_type {
    sel_type( int arg_pdg, bool arg_chargeconjugate);
    int m_pdg = 13;
    bool m_chargeconjugate = true;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
  };

  /// isolation of a RecoPrticle wrt the others
  ROOT::VecOps::RVec<float> Isolation( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particles, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in );
  
  struct sel_isol {
    sel_isol(float arg_isocut);
    float m_isocut = 9999.;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particles, ROOT::VecOps::RVec<float> var ) ;
  
  };
  
  /// cf Delphes Merger module - used for glbal sum
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> Merger( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in ) ;
  
  /// boost along x of the ReconstructedParticles 
  struct BoostAngle {
    BoostAngle( float arg_angle );
    float m_angle = -0.015 ;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in );
  };




}
#endif
