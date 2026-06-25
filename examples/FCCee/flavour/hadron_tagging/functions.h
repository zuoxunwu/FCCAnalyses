#ifndef ZHfunctions_H
#define ZHfunctions_H

#include <cmath>
#include <vector>
#include <math.h>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "ReconstructedParticle2MC.h"
#include "MCParticle.h"
#include "myUtils.h"

namespace FCCAnalyses { namespace ZHfunctions {


// build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
// technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
struct resonanceBuilder_mass_recoil {
    float m_resonance_mass;
    float m_recoil_mass;
    float chi2_recoil_frac;
    float ecm;
    bool m_use_MC_Kinematics;
    resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics);
    Vec_rp operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) ;
};

resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_recoil_mass = arg_recoil_mass, chi2_recoil_frac = arg_chi2_recoil_frac, ecm = arg_ecm, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

Vec_rp resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil::operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) {

    Vec_rp result;
    result.reserve(3);
    std::vector<std::vector<int>> pairs; // for each permutation, add the indices of the muons
    int n = legs.size();
  
    if(n > 1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true); // helper variable for permutations
        do {
            std::vector<int> pair;
            rp reso;
            reso.charge = 0;
            TLorentzVector reso_lv; 
            for(int i = 0; i < n; ++i) {
                if(v[i]) {
                    pair.push_back(i);
                    reso.charge += legs[i].charge;
                    TLorentzVector leg_lv;

                    if(m_use_MC_Kinematics) { // MC kinematics
                        int track_index = legs[i].tracks_begin;   // index in the Track array
                        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
                        if (mc_index >= 0 && mc_index < mc.size()) {
                            leg_lv.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
                        }
                    }
                    else { // reco kinematics
                         leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                    }

                    reso_lv += leg_lv;
                }
            }

            if(reso.charge != 0) continue; // neglect non-zero charge pairs
            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.emplace_back(reso);
            pairs.push_back(pair);

        } while(std::next_permutation(v.begin(), v.end()));
    }
    else {
        std::cout << "ERROR: resonanceBuilder_mass_recoil, at least two leptons required." << std::endl;
        exit(1);
    }
  
    if(result.size() > 1) {
  
        Vec_rp bestReso;
        
        int idx_min = -1;
        float d_min = 9e9;
        for (int i = 0; i < result.size(); ++i) {
            
            // calculate recoil
            auto recoil_p4 = TLorentzVector(0, 0, 0, ecm);
            TLorentzVector tv1;
            tv1.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
            recoil_p4 -= tv1;
      
            auto recoil_fcc = edm4hep::ReconstructedParticleData();
            recoil_fcc.momentum.x = recoil_p4.Px();
            recoil_fcc.momentum.y = recoil_p4.Py();
            recoil_fcc.momentum.z = recoil_p4.Pz();
            recoil_fcc.mass = recoil_p4.M();
            
            TLorentzVector tg;
            tg.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
        
            float boost = tg.P();
            float mass = std::pow(result.at(i).mass - m_resonance_mass, 2); // mass
            float rec = std::pow(recoil_fcc.mass - m_recoil_mass, 2); // recoil
            float d = (1.0-chi2_recoil_frac)*mass + chi2_recoil_frac*rec;
            
            if(d < d_min) {
                d_min = d;
                idx_min = i;
            }

     
        }
        if(idx_min > -1) { 
            bestReso.push_back(result.at(idx_min));
            auto & l1 = legs[pairs[idx_min][0]];
            auto & l2 = legs[pairs[idx_min][1]];
            bestReso.emplace_back(l1);
            bestReso.emplace_back(l2);
        }
        else {
            std::cout << "ERROR: resonanceBuilder_mass_recoil, no mininum found." << std::endl;
            exit(1);
        }
        return bestReso;
    }
    else {
        auto & l1 = legs[0];
        auto & l2 = legs[1];
        result.emplace_back(l1);
        result.emplace_back(l2);
        return result;
    }
}    




struct sel_iso {
    sel_iso(float arg_max_iso);
    float m_max_iso = .25;
    Vec_rp operator() (Vec_rp in, Vec_f iso);
  };

sel_iso::sel_iso(float arg_max_iso) : m_max_iso(arg_max_iso) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_iso::operator() (Vec_rp in, Vec_f iso) {
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if (iso[i] < m_max_iso) {
            result.emplace_back(p);
        }
    }
    return result;
}

 
// compute the cone isolation for reco particles
struct coneIsolation {

    coneIsolation(float arg_dr_min, float arg_dr_max);
    double deltaR(double eta1, double phi1, double eta2, double phi2) { return TMath::Sqrt(TMath::Power(eta1-eta2, 2) + (TMath::Power(phi1-phi2, 2))); };

    float dr_min = 0;
    float dr_max = 0.4;
    Vec_f operator() (Vec_rp in, Vec_rp rps) ;
};

coneIsolation::coneIsolation(float arg_dr_min, float arg_dr_max) : dr_min(arg_dr_min), dr_max( arg_dr_max ) { };
Vec_f coneIsolation::coneIsolation::operator() (Vec_rp in, Vec_rp rps) {
  
    Vec_f result;
    result.reserve(in.size());

    std::vector<ROOT::Math::PxPyPzEVector> lv_reco;
    std::vector<ROOT::Math::PxPyPzEVector> lv_charged;
    std::vector<ROOT::Math::PxPyPzEVector> lv_neutral;

    for(size_t i = 0; i < rps.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(rps.at(i).momentum.x, rps.at(i).momentum.y, rps.at(i).momentum.z, rps.at(i).energy);
        
        if(rps.at(i).charge == 0) lv_neutral.push_back(tlv);
        else lv_charged.push_back(tlv);
    }
    
    for(size_t i = 0; i < in.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z, in.at(i).energy);
        lv_reco.push_back(tlv);
    }

    
    // compute the isolation (see https://github.com/delphes/delphes/blob/master/modules/Isolation.cc#L154) 
    for (auto & lv_reco_ : lv_reco) {
    
        double sumNeutral = 0.0;
        double sumCharged = 0.0;
    
        // charged
        for (auto & lv_charged_ : lv_charged) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_charged_.Eta(), lv_charged_.Phi());
            if(dr > dr_min && dr < dr_max) sumCharged += lv_charged_.P();
        }
        
        // neutral
        for (auto & lv_neutral_ : lv_neutral) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_neutral_.Eta(), lv_neutral_.Phi());
            if(dr > dr_min && dr < dr_max) sumNeutral += lv_neutral_.P();
        }
        
        double sum = sumCharged + sumNeutral;
        double ratio= sum / lv_reco_.P();
        result.emplace_back(ratio);
    }
    return result;
}
 
 
 
// returns missing energy vector, based on reco particles
Vec_rp missingEnergy(float ecm, Vec_rp in, float p_cutoff = 0.0) {
    float px = 0, py = 0, pz = 0, e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        px += -p.momentum.x;
        py += -p.momentum.y;
        pz += -p.momentum.z;
        e += p.energy;
    }
    
    Vec_rp ret;
    rp res;
    res.momentum.x = px;
    res.momentum.y = py;
    res.momentum.z = pz;
    res.energy = ecm-e;
    ret.emplace_back(res);
    return ret;
}

// calculate the cosine(theta) of the missing energy vector
float get_cosTheta_miss(Vec_rp met){
    
    float costheta = 0.;
    if(met.size() > 0) {
        
        TLorentzVector lv_met;
        lv_met.SetPxPyPzE(met[0].momentum.x, met[0].momentum.y, met[0].momentum.z, met[0].energy);
        costheta = fabs(std::cos(lv_met.Theta()));
    }
    return costheta;
}

 
ROOT::VecOps::RVec<TLorentzVector> build_p4(ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz, ROOT::VecOps::RVec<float> mass) {
    ROOT::VecOps::RVec<TLorentzVector> p4;
    for (size_t i = 0; i < px.size(); ++i) {
        TLorentzVector tlv;
        tlv.SetXYZM(px[i], py[i], pz[i], mass[i]);
        p4.push_back(tlv);
    }
    return p4;
} 

// addition to myUtils
ROOT::VecOps::RVec<TLorentzVector> get_Vertex_p4(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex,
                                                   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco){

  ROOT::VecOps::RVec<TLorentzVector> result;
  for (auto &p:vertex){
    ROOT::VecOps::RVec<int> reco_ind = p.reco_ind;
    TLorentzVector tlv = myUtils::build_tlv(reco, reco_ind);
    result.push_back(tlv);
  }
  return result;
}


// addition to myUtils
ROOT::VecOps::RVec<int> get_RP_isfromPV(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex,
                                                   ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco){

  ROOT::VecOps::RVec<int> result;
  result.resize(reco.size(),-1);
  for (auto &p:vertex){ 
    ROOT::VecOps::RVec<int> reco_ind = p.reco_ind;
    if (p.vertex.primary == 1)
	    for (size_t j = 0; j < reco_ind.size(); ++j)
		    result[reco_ind.at(j)] = 1;
    else
            for (size_t j = 0; j < reco_ind.size(); ++j)
                    result[reco_ind.at(j)] = 2;
  }
  // return -1 for not belonging to any vertex, 1 for PV, 2 for SV 
  return result;
}

ROOT::VecOps::RVec<int> get_RP_Vert_Ind(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex,
                                        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco){

  ROOT::VecOps::RVec<int> result;
  result.resize(reco.size(),-1);
  for (size_t iv = 0; iv < vertex.size(); ++iv){
    auto & p = vertex[iv];
    ROOT::VecOps::RVec<int> reco_ind = p.reco_ind;
    for (size_t ip=0;ip<reco_ind.size();ip++){
	result[reco_ind.at(ip)] = iv;
    }
  }
  // return number of descendants from a given set of ancestors
  return result;
}


ROOT::VecOps::RVec<int> getRP2MC_nMC(ROOT::VecOps::RVec<int> recind,
                                            ROOT::VecOps::RVec<int> mcind,
                                            ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco) {

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> result;
  for (size_t i=0; i<reco.size();i++) {
    ROOT::VecOps::RVec<int> tmp;
    result.push_back(tmp);
  }

  for (size_t i=0; i<recind.size();i++) {
    result[recind.at(i)].push_back(mcind.at(i));
  }

  ROOT::VecOps::RVec<int> count;
  for (size_t i=0; i<reco.size();i++) {
    count.push_back(int(result[i].size()));
  }

  return count;
}




struct get_RP_isDescendant {
    get_RP_isDescendant(int arg_pdg, bool arg_chargeconjugate);
    int m_pdg = 13;
    bool m_chargeconjugate = true;
    ROOT::VecOps::RVec<int>  operator() (ROOT::VecOps::RVec<int> reco_mcidx, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind);
};


get_RP_isDescendant::get_RP_isDescendant(int arg_pdg, bool arg_chargeconjugate) : m_pdg(arg_pdg), m_chargeconjugate( arg_chargeconjugate )  {};
ROOT::VecOps::RVec<int> get_RP_isDescendant::operator() (ROOT::VecOps::RVec<int> reco_mcidx,
		                                         ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind ) {


  //first find all stable decay descendants
  ROOT::VecOps::RVec<int> descd;
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if ( m_chargeconjugate ) {
        if ( std::abs( p.PDG ) == std::abs( m_pdg)  ) {
		std::vector<int> rr = MCParticle::get_list_of_stable_particles_from_decay( i, in, ind) ;
		descd.insert( descd.end(), rr.begin(), rr.end() );
	}
    }
    else {
        if ( p.PDG == m_pdg ) {
		std::vector<int> rr = MCParticle::get_list_of_stable_particles_from_decay( i, in, ind) ;
                descd.insert( descd.end(), rr.begin(), rr.end() );
	}
    }
  }

  //then check for reco if they are matched to any
  ROOT::VecOps::RVec<int> result;
  result.resize(reco_mcidx.size(), 0);
  for (size_t i = 0; i < reco_mcidx.size(); ++i)
	  if(std::find(descd.begin(), descd.end(), reco_mcidx[i]) != descd.end())
		  result[i] = 1;

  return result;  
}


ROOT::VecOps::RVec<int> get_Vertex_containDescendant(ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex> vertex,
                                                     ROOT::VecOps::RVec<int> rp_isDescendant){

  ROOT::VecOps::RVec<int> result;
  for (auto &p:vertex){
    ROOT::VecOps::RVec<int> reco_ind = p.reco_ind;
    int contain = 0;
    for (size_t i=0;i<reco_ind.size();i++){
	contain += rp_isDescendant[reco_ind.at(i)];   
    }
    result.push_back(contain);
  }
  // return number of descendants from a given set of ancestors
  return result;
}


ROOT::VecOps::RVec<float> get_RP_dndx(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
                                      ROOT::VecOps::RVec<edm4hep::Quantity> dNdx,       // ETrackFlow_2
                                      ROOT::VecOps::RVec<edm4hep::TrackData> trackdata) // Eflowtrack
{
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in)
  {
    if (p.tracks_begin<trackdata.size() && p.charge!=0)
	result.push_back(dNdx.at(trackdata.at(p.tracks_begin).dxQuantities_begin).value / 1000.);
    else
	result.push_back(-9.);
  }
  return result;
}




ROOT::VecOps::RVec<float> get_RP_mtof(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
                                      ROOT::VecOps::RVec<float> track_L,
                                      ROOT::VecOps::RVec<edm4hep::TrackData> trackdata,
                                      ROOT::VecOps::RVec<edm4hep::TrackerHitData> trackerhits,
                                      ROOT::VecOps::RVec<edm4hep::ClusterData> gammadata,
                                      ROOT::VecOps::RVec<edm4hep::ClusterData> nhdata,
                                      ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> calohits,
                                      TLorentzVector V) // primary vertex posotion and time in mm)
{
    ROOT::VecOps::RVec<float>  result;
    for (int j = 0; j < in.size(); ++j)
    {
      //if (in.at(j).clusters_begin < nhdata.size() + gammadata.size()) // condition in original code. charge particles have cluster begin 0, why not exclude? Ask Michele. 
      if (in.at(j).charge == 0 and in.at(j).clusters_begin < nhdata.size() + gammadata.size())
      {
        if (in.at(j).type == 130)
        {
          // this assumes that in converter photons are filled first and nh after
          float T = calohits.at(nhdata.at(in.at(j).clusters_begin - gammadata.size()).hits_begin).time;
          float X = calohits.at(nhdata.at(in.at(j).clusters_begin - gammadata.size()).hits_begin).position.x;
          float Y = calohits.at(nhdata.at(in.at(j).clusters_begin - gammadata.size()).hits_begin).position.y;
          float Z = calohits.at(nhdata.at(in.at(j).clusters_begin - gammadata.size()).hits_begin).position.z;

          float tof = T;
          // compute path length wrt to PV
          float L = std::sqrt((X - V.X()) * (X - V.X()) + (Y - V.Y()) * (Y - V.Y()) + (Z - V.Z()) * (Z - V.Z())) * 0.001;
          // std::cout << "tof n: " << T << "  -  L: " << L << std::endl;
          float beta = L / (tof * 2.99792458e+8);
          float E = in.at(j).energy;
          // std::cout << "tof: " << tof << " - L: " << L << " - beta: " << beta << " - energy: " << E <<" - true PID: "<<abs(pids.at(j))<<std::endl;
          if (beta < 1. && beta > 0.)
          {
            result.push_back(E * std::sqrt(1 - beta * beta));
            // std::cout << "mtof n:" << E * std::sqrt(1-beta*beta)<< std::endl;
          }
          else
          {
            // std::cout << "problem" << std::endl;
            result.push_back((-9.));
          }
        }
        else if (in.at(j).type == 22)
        {
          result.push_back((0.));
        }
	else
	{
          result.push_back((-8.));
        }
      }

      else if (in.at(j).charge != 0 and in.at(j).tracks_begin < trackdata.size())
      {
        if (abs(in.at(j).charge) > 0 and abs(in.at(j).mass - 0.000510999) < 1.e-05)
        {
          result.push_back(0.000510999);
        }
        else if (abs(in.at(j).charge) > 0 and abs(in.at(j).mass - 0.105658) < 1.e-03)
        {
          result.push_back(0.105658);
        }
        else
        {

          // this is the time of the track origin from MC
          // float Tin = trackerhits.at(trackdata.at(in.at(j).tracks_begin).trackerHits_begin).time;

          // time given by primary vertex
          float Tin = V.T() * 1e-3 / 2.99792458e+8;

          float Tout = trackerhits.at(trackdata.at(in.at(j).tracks_begin).trackerHits_end - 1).time; // one track and 3 hits per recon. particle are assumed
          float tof = (Tout - Tin);

          // TODO: path length will have to be re-calculated from vertex position
          float L = track_L.at(in.at(j).tracks_begin) * 0.001;
          // std::cout << "tof: " << tof << "  -  L: " << L << std::endl;
          float beta = L / (tof * 2.99792458e+8);
          float p = std::sqrt(in.at(j).momentum.x * in.at(j).momentum.x + in.at(j).momentum.y * in.at(j).momentum.y + in.at(j).momentum.z * in.at(j).momentum.z);
          // std::cout << "tof: " << tof << " - L: " << L << " - beta: " << beta << " - momentum: " << p << " - mtof: " << p * std::sqrt(1/(beta*beta)-1) << std::endl;
          if (beta < 1. && beta > 0.)
          {
            result.push_back(p * std::sqrt(1 / (beta * beta) - 1));
          }
          else
          {
            result.push_back(0.13957039);
          }
        }
      }
      else // cluster or track out of range
      {
	    result.push_back(-7.);
      }
    }
    return result;
}


















//std::vector<int> get_MCpdgMCVertex(std::vector<std::vector<int>> vertex_mother_PDG,
//                                   std::vector<std::vector<int>> vertex_daughter_PDG,
//				   int require_mother,
//				   int require_daughter){  //TODO: need to change daughter to a vector
//  std::vector<int> result;
//  for (size_t i=0; i < vertex_mother_PDG.size(); ++i){
//    int mo_yes=0;
//    int da_yes=0;
//    for (size_t j=0; j < )
//    std::vector<int> tmp;
//    for (size_t i = 0; i < p.mc_ind.size(); ++i) tmp.push_back(mc.at(p.mc_ind.at(i)).PDG);
//    for (size_t i = 0; i < p.mc_indneutral.size(); ++i) tmp.push_back(mc.at(p.mc_indneutral.at(i)).PDG);
//    result.push_back(tmp);
//  }
//  return result;
//}


//ROOT::VecOps::RVec<edm4hep::TrackerHitData> CollectTrackerHits(const ROOT::VecOps::RVec<edm4hep::TrackData>& tracks,
//                                                           const ROOT::VecOps::RVec<edm4hep::TrackerHitData>& allHits) {   // in RDF this class is made into <edm4hep::TrackerHitData> instead of <edm4hep::TrackerHit>
//    ROOT::VecOps::RVec<edm4hep::TrackerHitData> result;
//    for (auto & trk : tracks) {
//	for (auto it_hit = trk.trackerHits_begin; it_hit != trk.trackerHits_end; ++it_hit) { 
//          result.emplace_back(allHits.at(it_hit));   
//        }
//    }
//    return result;
//}
//
//ROOT::VecOps::RVec<float> get_x(const ROOT::VecOps::RVec<edm4hep::TrackerHitData>& in) {
//  ROOT::VecOps::RVec<float> result;
//  for (auto & hit: in) {
//    result.push_back(hit.position.x);
//  }
//  return result;
//}
//
//ROOT::VecOps::RVec<float> get_y(const ROOT::VecOps::RVec<edm4hep::TrackerHitData>& in) {
//  ROOT::VecOps::RVec<float> result;
//  for (auto & hit: in) {
//    result.push_back(hit.position.y);
//  }
//  return result;
//}
//
//ROOT::VecOps::RVec<float> get_z(const ROOT::VecOps::RVec<edm4hep::TrackerHitData>& in) {
//  ROOT::VecOps::RVec<float> result;
//  for (auto & hit: in) {
//    result.push_back(hit.position.z);
//  }
//  return result;
//}
//
//
//ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> CollectCaloHits(const ROOT::VecOps::RVec<edm4hep::ClusterData>& clusters,
//                                                                const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& allHits) {   // in RDF this class is made into <edm4hep::TrackerHitData> instead of <edm4hep::TrackerHit>
//    ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> result;
//    for (auto & clu : clusters) {
//        for (auto it_hit = clu.hits_begin; it_hit != trk.hits_end; ++it_hit) {
//          result.emplace_back(allHits.at(it_hit));
//        }
//    }
//    return result;
//}
//
//
//
//
//ROOT::VecOps::RVec<float> sel_CaloHits (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in,
//                                        const ROOT::VecOps::RVec<int>& hit_idx ){
//  ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> result;
//  for (auto & i: hit_idx){
//    result.push_back(in.at(i));
//  }
//  return result;
//}
//
//ROOT::VecOps::RVec<float> sel_CaloHit_x (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in,
//		                         const ROOT::VecOps::RVec<int>& hit_idx ){
//  ROOT::VecOps::RVec<float> result;
//  for (int i=0; i< hit_idx.size(); ++i){ 
//    result.push_back(in.at(hit_idx.at(i)).position.x);
//  }
//  return result;
//}
//
//ROOT::VecOps::RVec<float> sel_CaloHit_y (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in,
//                                         const ROOT::VecOps::RVec<int>& hit_idx ){
//  ROOT::VecOps::RVec<float> result;
//  for (auto & idx: hit_idx){
//    result.push_back(in.at(idx).position.y);
//  }
//  return result;
//}
//
//ROOT::VecOps::RVec<float> sel_CaloHit_z (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in,
//                                         const ROOT::VecOps::RVec<int>& hit_idx ){
//  ROOT::VecOps::RVec<float> result;
//  for (auto & idx: hit_idx){
//    result.push_back(in.at(idx).position.z);
//  }
//  return result;
//}



float getAxisPhi(const ROOT::VecOps::RVec<float> & axis){

  TLorentzVector tlv;
  tlv.SetXYZM(axis[1], axis[3], axis[5], 0);
  return tlv.Phi();
}

float getAxisTheta(const ROOT::VecOps::RVec<float> & axis){

  TLorentzVector tlv;
  tlv.SetXYZM(axis[1], axis[3], axis[5], 0);
  return tlv.Theta();
}


// Select MCParticles by PDG, dropping those whose daughter is their own charge
// conjugate (oscillation parent), so an oscillating chain like
// Bs -> Bsbar -> X is counted once. Useful for Bs (531) and Bd (511), which mix.
// `in`  is the full MCParticle collection (e.g. Particle).
// `ind` is the daughter index array (e.g. Particle#1.index, aliased as Particle1).
struct sel_PDG_no_osc {
    sel_PDG_no_osc(int arg_pdg, bool arg_chargeconjugate);
    int m_pdg = 531;
    bool m_chargeconjugate = true;
    ROOT::VecOps::RVec<edm4hep::MCParticleData> operator()(
        ROOT::VecOps::RVec<edm4hep::MCParticleData> in,
        ROOT::VecOps::RVec<int> ind);
};

sel_PDG_no_osc::sel_PDG_no_osc(int arg_pdg, bool arg_chargeconjugate)
    : m_pdg(arg_pdg), m_chargeconjugate(arg_chargeconjugate) {}

ROOT::VecOps::RVec<edm4hep::MCParticleData>
sel_PDG_no_osc::operator()(ROOT::VecOps::RVec<edm4hep::MCParticleData> in,
                           ROOT::VecOps::RVec<int> ind) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
  for (size_t i = 0; i < in.size(); ++i) {
    const auto & p = in[i];
    bool pdg_match = m_chargeconjugate
                     ? (std::abs(p.PDG) == std::abs(m_pdg))
                     : (p.PDG == m_pdg);
    if (!pdg_match) continue;

    // Skip if any immediate daughter has the same |PDG| with opposite sign
    // (i.e. the particle oscillated into its own anti-particle).
    bool osc_parent = false;
    for (unsigned int d = p.daughters_begin; d < p.daughters_end; ++d) {
      if (d >= ind.size()) break;
      int didx = ind.at(d);
      if (didx < 0 || (size_t)didx >= in.size()) continue;
      if (in.at(didx).PDG == -p.PDG) {
        osc_parent = true;
        break;
      }
    }
    if (osc_parent) continue;
    result.push_back(p);
  }
  return result;
}

}}

#endif
