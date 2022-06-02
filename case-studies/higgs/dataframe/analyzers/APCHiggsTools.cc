#include "APCHiggsTools.h"
#include "ReconstructedParticle.h"

#include <algorithm>

using namespace APCHiggsTools;

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  APCHiggsTools::muon_quality_check(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
	ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  //at least one muon + and one muon - in each event
  int n_muon_plus = 0;
	int n_muon_minus = 0;
	int n = in.size();
	for (int i = 0; i < n; ++i) {
		if (in[i].charge == 1.0){
			++n_muon_plus;
		}
		else if (in[i].charge == -1.0){
			++n_muon_minus;
		}
	}
	if (n_muon_plus >= 1 && n_muon_minus >= 1){
		result = in;
	}
	return result;
}

ROOT::VecOps::RVec<float> APCHiggsTools::get_cosTheta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
   ROOT::VecOps::RVec<float> result;
	 for (auto & p: in) {
		 TLorentzVector tlv;
		 tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
		 result.push_back(tlv.CosTheta());
	 }
	 return result;
}

ROOT::VecOps::RVec<float> APCHiggsTools::get_cosTheta_miss(ROOT::VecOps::RVec<Float_t>Px, ROOT::VecOps::RVec<Float_t>Py, ROOT::VecOps::RVec<Float_t>Pz, ROOT::VecOps::RVec<Float_t>E) {
  ROOT::VecOps::RVec<float> result;
  for (int i =0; i < Px.size(); ++i) {
		TLorentzVector tlv;
		tlv.SetPxPyPzE(Px.at(i), Py.at(i), Pz.at(i), E.at(i));
    result.push_back(tlv.CosTheta());
  }
  return result;
} 


APCHiggsTools::resonanceZBuilder::resonanceZBuilder(float arg_resonance_mass) {m_resonance_mass = arg_resonance_mass;}
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> APCHiggsTools::resonanceZBuilder::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      edm4hep::ReconstructedParticleData reso;
      //set initial charge == 0
      reso.charge = 0;
      TLorentzVector reso_lv;
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
                                //prevent +2 and -2 charged Z 
            if (reso.charge == legs[i].charge) continue;
            reso.charge += legs[i].charge;
            TLorentzVector leg_lv;
            leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
            reso_lv += leg_lv;
          }
      }
      reso.momentum.x = reso_lv.Px();
      reso.momentum.y = reso_lv.Py();
      reso.momentum.z = reso_lv.Pz();
      reso.mass = reso_lv.M();
      result.emplace_back(reso);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
                std::sort(result.begin(), result.end(), resonancesort);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
    return onlyBestReso;
  } else {
    return result;
  }
}



APCHiggsTools::resonanceZBuilder2::resonanceZBuilder2(float arg_resonance_mass, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_use_MC_Kinematics = arg_use_MC_Kinematics;}
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> APCHiggsTools::resonanceZBuilder2::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
				ROOT::VecOps::RVec<int> recind ,
				ROOT::VecOps::RVec<int> mcind ,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco ,
				ROOT::VecOps::RVec<edm4hep::MCParticleData> mc )   {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      edm4hep::ReconstructedParticleData reso;
      //set initial charge == 0
      reso.charge = 0;
      TLorentzVector reso_lv; 
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
    				//prevent +2 and -2 charged Z 
            if (reso.charge == legs[i].charge) continue;
            reso.charge += legs[i].charge;
            TLorentzVector leg_lv;

		// Ideal detector resolution: use the kinematics of the MC particle instead
		if ( m_use_MC_Kinematics) {

		     // ugly: particles_begin is not filled in RecoParticle.
		     // hence: either need to keep trace of the index of the legs into the RecoParticle collection,
		     // or (as done below) use the track index to map the leg to the MC particle :-(

		     int track_index = legs[i].tracks_begin ;   // index in the Track array
		     int mc_index = FCCAnalyses::ReconstructedParticle2MC::getTrack2MC_index( track_index, recind, mcind, reco );
		     if ( mc_index >= 0 && mc_index < mc.size() ) {
			 int pdgID = mc.at( mc_index).PDG;
		         leg_lv.SetXYZM(mc.at(mc_index ).momentum.x, mc.at(mc_index ).momentum.y, mc.at(mc_index ).momentum.z, mc.at(mc_index ).mass );
		     }
		}

		else {   //use the kinematics of the reco'ed particle
		     leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
		}

            reso_lv += leg_lv;
          }
      }
      reso.momentum.x = reso_lv.Px();
      reso.momentum.y = reso_lv.Py();
      reso.momentum.z = reso_lv.Pz();
      reso.mass = reso_lv.M();
      result.emplace_back(reso);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
		std::sort(result.begin(), result.end(), resonancesort);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
    return onlyBestReso;
  } else {
    return result;
  }
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  APCHiggsTools::sort_greater(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
	ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  //at least one muon + and one muon - in each event
	
  int n = in.size();
  if (n == 0 ){
    return result;
  }
  ROOT::VecOps::RVec<float> pT = FCCAnalyses::ReconstructedParticle::get_pt(in);
  std::vector< std::pair <float, edm4hep::ReconstructedParticleData> > vect;
  for (int i = 0; i<n ; ++i){
    vect.push_back(std::make_pair(pT.at(i),in.at(i)));
  }
  std::stable_sort(vect.begin(), vect.end(),
                 [](const auto& a, const auto& b){return a.first > b.first;});
  //std::sort(vect.begin(), vect.end());
  for (int i = 0; i<n ; ++i){
    result.push_back(vect.at(i).second);
  } 
  return result;
}



float APCHiggsTools::Reweighting_wzp_kkmc(float pT, float m) {
  float scale;
  if (m > 220.){
    if ( pT > 0. && pT <= 1.){scale = 1.0032322;}
    else if ( pT > 1. && pT <= 2.){scale = 0.95560480;}
    else if ( pT > 2. && pT <= 3.){scale = 0.94986398;}
    else if ( pT > 3. && pT <= 4.){scale = 0.95134129;}
    else if ( pT > 4. && pT <= 5.){scale = 0.94456404;}
    else if ( pT > 5. && pT <= 6.){scale = 0.94726464;}
    else if ( pT > 6. && pT <= 7.){scale = 0.94101542;}
    else if ( pT > 7. && pT <= 8.){scale = 0.91753618;}
    else if ( pT > 8. && pT <= 9.){scale = 0.91804730;}
    else if ( pT > 9. && pT <= 10.){scale = 0.92097238;}
    else if ( pT > 10. && pT <= 11.){scale = 0.91521958;}
    else if ( pT > 11. && pT <= 12.){scale = 0.94550474;}
    else if ( pT > 12. && pT <= 13.){scale = 0.91403417;}
    else if ( pT > 13. && pT <= 14.){scale = 0.87701843;}
    else if ( pT > 14. && pT <= 15.){scale = 0.89537075;}
    else if ( pT > 15. && pT <= 16.){scale = 0.90811988;}
    else if ( pT > 16. && pT <= 17.){scale = 0.90657018;}
    else if ( pT > 17. && pT <= 18.){scale = 0.93739754;}
    else if ( pT > 18. && pT <= 19.){scale = 0.98795371;}
    else if ( pT > 19. && pT <= 20.){scale = 2.6656045;}
    else {scale = 1.;}
  }
  else {scale = 1.;}

  return scale;
}

ROOT::VecOps::RVec<float> acolinearity(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<float> result;
  if(in.size() != 2) return result;

  TLorentzVector p1;
  p1.SetXYZM(in[0].momentum.x, in[0].momentum.y, in[0].momentum.z, in[0].mass);

  TLorentzVector p2;
  p2.SetXYZM(in[1].momentum.x, in[1].momentum.y, in[1].momentum.z, in[1].mass);

  float acol = abs(p1.Theta() - p2.Theta());

  result.push_back(acol);
  return result;
}



ROOT::VecOps::RVec<float> acoplanarity(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<float> result;
  if(in.size() != 2) return result;

  TLorentzVector p1;
  p1.SetXYZM(in[0].momentum.x, in[0].momentum.y, in[0].momentum.z, in[0].mass);

  TLorentzVector p2;
  p2.SetXYZM(in[1].momentum.x, in[1].momentum.y, in[1].momentum.z, in[1].mass);

  float acop = abs(p1.Phi() - p2.Phi());
  if(acop > M_PI) acop = 2 * M_PI - acop;
  acop = M_PI - acop;

  result.push_back(acop);
  return result;
}


// perturb the scale of the particles
APCHiggsTools::momentum_scale::momentum_scale(float arg_scaleunc) : scaleunc(arg_scaleunc) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  APCHiggsTools::momentum_scale::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    /*
     TLorentzVector lv;
     lv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
     lv *= (1. + scaleunc);
     p.momentum.x = lv.Px();
     p.momentum.y = lv.Py();
     p.momentum.z = lv.Pz();
     //p.energy = lv.E();
    */
    p.momentum.x = p.momentum.x*(1. + scaleunc);
    p.momentum.y = p.momentum.y*(1. + scaleunc);
    p.momentum.z = p.momentum.z*(1. + scaleunc);
    result.emplace_back(p);
  }
  return result;
}

/// to be added to your ReconstructedParticle.cc
sel_type::sel_type( int arg_pdg, bool arg_chargeconjugate) : m_pdg(arg_pdg), m_chargeconjugate( arg_chargeconjugate )  {};

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  APCHiggsTools::sel_type::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if ( m_chargeconjugate ) {
        if ( std::abs( p.type ) == std::abs( m_pdg)  ) result.emplace_back(p);
    }
    else {
        if ( p.type == m_pdg ) result.emplace_back(p);
    }
  }
  return result;
}

ROOT::VecOps::RVec<float> Isolation( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particles, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in ) {

  ROOT::VecOps::RVec<float> result;

  float DeltaRMax = 0.5 ;
  float PTMin = 0.5 ;

  for (size_t i = 0; i < particles.size(); ++i) {

    auto & par1 = in[i];
    float pt1 = sqrt( pow(par1.momentum.x, 2) + pow(par1.momentum.y, 2) ) ;

    TVector3 p1(in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z );
    float sum = 0;

    for (size_t j = 0; j < in.size(); ++j) {
      auto & par2 = in[j];
      if ( par1.energy == par2.energy && par1.momentum.x == par2.momentum.x && par1.momentum.y == par2.momentum.y && par1.momentum.z == par2.momentum.z ) continue;

      TVector3 p2( in.at(j).momentum.x, in.at(j).momentum.y, in.at(j).momentum.z );
      if ( sqrt( pow(par2.momentum.x, 2) + pow(par2.momentum.y, 2) ) < PTMin ) continue;
      float delta_ij = fabs( p1.DeltaR( p2 ) );
      if ( delta_ij < DeltaRMax)  sum +=  sqrt( pow(par2.momentum.x, 2) + pow(par2.momentum.y, 2) ) ;

    }

    float isolation = sum / pt1 ;
    result.push_back( isolation );
  }

  return result;
}

sel_isol::sel_isol( float arg_isocut ) : m_isocut (arg_isocut) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> APCHiggsTools::sel_isol::operator() (  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particles, ROOT::VecOps::RVec<float> var ) { 
  
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  for (size_t i=0; i < particles.size(); ++i) {
    auto & p = particles[i];
    if ( var[i] < m_isocut) result.emplace_back( p );
  }

  return result;
}

BoostAngle::BoostAngle( float arg_angle ) : m_angle ( arg_angle ) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> APCHiggsTools::BoostAngle::operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in ) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  float ta =  tan( m_angle ) ;
  for ( size_t i=0; i < in.size(); ++i) {
    auto & p = in[i];
    edm4hep::ReconstructedParticleData newp = p;
    float e = p.energy ;
    float px = p.momentum.x;
    float e_prime = e * sqrt( 1 + ta*ta ) + px * ta ;
    float px_prime = px * sqrt( 1 + ta*ta ) + e * ta ;
    newp.momentum.x = px_prime;
    newp.energy = e_prime;
    result.push_back( newp );
  }
  return result;
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> Merger( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in ) {
  // cf Delphes Merger module. Returns a vector with one single RecoParticle corresponding to the global
  // sum (cf the "MissingET" object in the Delphes files )
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  edm4hep::ReconstructedParticleData sum;
  float px=0;
  float py=0;
  float pz=0;
  float energy=0;

  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    px = px + p.momentum.x;
    py = py + p.momentum.y;
    pz = pz + p.momentum.z;
    energy = energy + p.energy ;
  }

  sum.momentum.x = px;
  sum.momentum.y = py;
  sum.momentum.z = pz;
  sum.energy = energy;
  sum.charge = 0;
  sum.mass = 0;

  result.push_back( sum );
  return result;
}



































