#analysis_stage1

# list of samples to process

processList_full = {
    'p8_ee_Zbb_ecm91_EvtGen_Bu2Inclusive':{'chunks':100},
    'p8_ee_Zbb_ecm91_EvtGen_Bd2Inclusive':{'chunks':100},
    'p8_ee_Zbb_ecm91_EvtGen_Bs2Inclusive':{'chunks':100},
    'p8_ee_Zbb_ecm91_EvtGen_Bc2Inclusive':{'chunks':100},
    'p8_ee_Zbb_ecm91_EvtGen_Lb2Inclusive':{'chunks':100},
#    'p8_ee_Zbb_ecm91':{'chunks':100, 'fraction':0.1},
#    'p8_ee_Zbb_ecm91_EvtGen_Bc2Inclusive':{'chunks':100},
#    'p8_ee_Zcc_ecm91':{'chunks':100},
#    'p8_ee_Zss_ecm91':{'chunks':100},
#    'p8_ee_Zud_ecm91':{'chunks':100},
#    'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU':{'chunks':5, 'fraction':0.05},
#    'p8_ee_Zbb_ecm91_EvtGen_Bs2PhiMuMu':{'chunks':2, 'fraction':0.1},
#    'p8_ee_Zbb_ecm91_EvtGen_Bs2PhiNuNu':{'chunks':2, 'fraction':0.1},
#    'p8_ee_Zbb_ecm91_EvtGen_Bs2D0KS':{'chunks':5, 'fraction':0.1},
}

processList_test = {
    'p8_ee_Zbb_ecm91':{'chunks':1, 'fraction':0.0000001},
}

doStage1Cut = False

nCPUS       = 8
runBatch    = True
batchQueue  = "nextweek"
compGroup   = "group_u_FCC.local_gen"

processList  = processList_full
if not runBatch:
    processList  = processList_test

# tag for MC production campaign
prodTag     = "FCCee/winter2023/IDEA/"

# if runBatch = True, save output on eos
#outputDirEos   = "/eos/experiment/fcc/ee/analyses_storage/flavor/Bs2TauTau/flatNtuples/winter2023/analysis_stage1_noFilter_fullP4/"
outputDirEos   = "/eos/experiment/fcc/ee/analyses_storage/flavor/hadron_tagging/flatNtuples/winter2023/all_tags_PVbackinVert_allEvtGenInc"

# if runBatch = False, save output locally
outputDir   = "outputs/FCCee/flavor/hadron_tagging/analysis_stage1/"

includePaths = ["functions.h"]

import ROOT
ROOT.gInterpreter.ProcessLine('''
TMVA::Experimental::RBDT<> bdt("BDT", "/afs/cern.ch/work/x/xzuo/public/FCC_files/Bs2TauTau/BDT/xgb_bdt_trained_iteration_16.root");
computeModel1 = TMVA::Experimental::Compute<18, float>(bdt);
''')


MVAFilter   = "EVT_MVA1>0.6"

SelectionCut = "EVT_ThrustEmin_NTau23PiCand==2 and recoEmiss_e>3.5 and EVT_ThrustEmin_E<38 and EVT_ThrustEmin_Eneutral<10 and EVT_ThrustEmin_Nneutral<13"
if not doStage1Cut:
    SelectionCut = ""

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df
               #############################################
               ##          Aliases for # in python        ##
               #############################################
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")

               #############################################
               ##MC record to study the Z->bb events types##
               #############################################
               .Define("MC_PDG", "FCCAnalyses::MCParticle::get_pdg(Particle)")
               .Define("MC_n",   "int(MC_PDG.size())")
               .Define("MC_M1",  "myUtils::get_MCMother1(Particle,Particle0)")
               .Define("MC_M2",  "myUtils::get_MCMother2(Particle,Particle0)")
               .Define("MC_D1",  "myUtils::get_MCDaughter1(Particle,Particle1)")
               .Define("MC_D2",  "myUtils::get_MCDaughter2(Particle,Particle1)")

               #############################################
               ##   gen b quark and Bs meson info         ##
               #############################################

               .Define("genBottom",   "FCCAnalyses::MCParticle::sel_pdgID(5, true)(Particle)")
               .Define("n_genBottoms",     "FCCAnalyses::MCParticle::get_n(genBottom)")
               .Define("genBottom_px",     "FCCAnalyses::MCParticle::get_px(genBottom)")
               .Define("genBottom_py",     "FCCAnalyses::MCParticle::get_py(genBottom)")
               .Define("genBottom_pz",     "FCCAnalyses::MCParticle::get_pz(genBottom)")
               .Define("genBottom_phi",    "FCCAnalyses::MCParticle::get_phi(genBottom)")
               .Define("genBottom_eta",    "FCCAnalyses::MCParticle::get_eta(genBottom)")
               .Define("genBottom_energy", "FCCAnalyses::MCParticle::get_e(genBottom)")
               .Define("genBottom_mass",   "FCCAnalyses::MCParticle::get_mass(genBottom)")
               .Define("genBottom_pdg",    "FCCAnalyses::MCParticle::get_pdg(genBottom)")

               .Define("genBs",   "FCCAnalyses::ZHfunctions::sel_PDG_no_osc(531, true)(Particle, Particle1)")
               .Define("n_genBs",     "FCCAnalyses::MCParticle::get_n   (genBs)")
               .Define("genBs_px",    "FCCAnalyses::MCParticle::get_px  (genBs)")
               .Define("genBs_py",    "FCCAnalyses::MCParticle::get_py  (genBs)")
               .Define("genBs_pz",    "FCCAnalyses::MCParticle::get_pz  (genBs)")
               .Define("genBs_phi",   "FCCAnalyses::MCParticle::get_phi (genBs)")
               .Define("genBs_eta",   "FCCAnalyses::MCParticle::get_eta (genBs)")
               .Define("genBs_energy","FCCAnalyses::MCParticle::get_e   (genBs)")
               .Define("genBs_mass",  "FCCAnalyses::MCParticle::get_mass(genBs)")
               .Define("genBs_pdg",   "FCCAnalyses::MCParticle::get_pdg (genBs)")

               .Define("genBc",   "FCCAnalyses::MCParticle::sel_pdgID(541, true)(Particle)")
               .Define("n_genBc",     "FCCAnalyses::MCParticle::get_n   (genBc)")
               .Define("genBc_px",    "FCCAnalyses::MCParticle::get_px  (genBc)")
               .Define("genBc_py",    "FCCAnalyses::MCParticle::get_py  (genBc)")
               .Define("genBc_pz",    "FCCAnalyses::MCParticle::get_pz  (genBc)")

               .Define("genBu",   "FCCAnalyses::MCParticle::sel_pdgID(521, true)(Particle)")
               .Define("n_genBu",     "FCCAnalyses::MCParticle::get_n   (genBu)")
               .Define("genBu_px",    "FCCAnalyses::MCParticle::get_px  (genBu)")
               .Define("genBu_py",    "FCCAnalyses::MCParticle::get_py  (genBu)")
               .Define("genBu_pz",    "FCCAnalyses::MCParticle::get_pz  (genBu)")

               .Define("genBd",   "FCCAnalyses::ZHfunctions::sel_PDG_no_osc(511, true)(Particle, Particle1)")
               .Define("n_genBd",     "FCCAnalyses::MCParticle::get_n   (genBd)")
               .Define("genBd_px",    "FCCAnalyses::MCParticle::get_px  (genBd)")
               .Define("genBd_py",    "FCCAnalyses::MCParticle::get_py  (genBd)")
               .Define("genBd_pz",    "FCCAnalyses::MCParticle::get_pz  (genBd)")

               .Define("genLb",   "FCCAnalyses::MCParticle::sel_pdgID(5122, true)(Particle)")
               .Define("n_genLb",     "FCCAnalyses::MCParticle::get_n   (genLb)")
               .Define("genLb_px",    "FCCAnalyses::MCParticle::get_px  (genLb)")
               .Define("genLb_py",    "FCCAnalyses::MCParticle::get_py  (genLb)")
               .Define("genLb_pz",    "FCCAnalyses::MCParticle::get_pz  (genLb)")

               #############################################
               ##               Build MC Vertex           ##
               #############################################
               .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")
               .Define("MC_Vertex_x",    "myUtils::get_MCVertex_x(MCVertexObject)")
               .Define("MC_Vertex_y",    "myUtils::get_MCVertex_y(MCVertexObject)")
               .Define("MC_Vertex_z",    "myUtils::get_MCVertex_z(MCVertexObject)")
               .Define("MC_Vertex_ind",  "myUtils::get_MCindMCVertex(MCVertexObject)")
               .Define("MC_Vertex_ntrk", "myUtils::get_NTracksMCVertex(MCVertexObject)")
               .Define("MC_Vertex_n",    "int(MC_Vertex_x.size())")
               .Define("MC_Vertex_PDG",  "myUtils::get_MCpdgMCVertex(MCVertexObject, Particle)")
               .Define("MC_Vertex_PDGmother",  "myUtils::get_MCpdgMotherMCVertex(MCVertexObject, Particle)")
               .Define("MC_Vertex_PDGgmother", "myUtils::get_MCpdgGMotherMCVertex(MCVertexObject, Particle)")

                ############################################
                ##           single out Bs vertices       ##
                ############################################

               .Define("MC_Vertex_isBs",    "ROOT::VecOps::RVec<int> result; for (size_t i=0; i < MC_Vertex_PDGmother.size(); ++i) {int isBs=0; for (size_t j=0; j < MC_Vertex_PDGmother[i].size(); ++j) {if (abs(MC_Vertex_PDGmother[i][j])==531) isBs+=1;} result.push_back(isBs);} return result;")
               .Define("genBs_Vertex_x",   "MC_Vertex_x  [MC_Vertex_isBs>0]") #find Bs meson
               .Define("genBs_Vertex_y",   "MC_Vertex_y  [MC_Vertex_isBs>0]") #no implementation of abs() for vector
               .Define("genBs_Vertex_z",   "MC_Vertex_z  [MC_Vertex_isBs>0]")

               #############################################
               ##    true PV position and time            ##
               #############################################

               .Define("MC_PV_xyzt",      "FCCAnalyses::MCParticle::get_EventPrimaryVertexP4()(Particle)")

               #############################################
               ##              Build Reco Vertex          ##
               #############################################
               .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject,ReconstructedParticles,EFlowTrack_1,MCRecoAssociations0,MCRecoAssociations1)")

               #############################################
               ##          Build PV var and filter        ##
               #############################################
               .Define("EVT_hasPV",    "myUtils::hasPV(VertexObject)")
               .Define("EVT_NtracksPV", "float(myUtils::get_PV_ntracks(VertexObject))")
               .Define("EVT_NVertex",   "float(VertexObject.size())")
               .Filter("EVT_hasPV==1")

               #############################################
               ##         Full 3D missing energy          ##
               #############################################

               .Define("missingEnergy", "FCCAnalyses::ZHfunctions::missingEnergy(91.188, ReconstructedParticles)") ## 91.188 GeV total energy in pythia cards
               .Define("recoEmiss_px",  "missingEnergy[0].momentum.x")
               .Define("recoEmiss_py",  "missingEnergy[0].momentum.y")
               .Define("recoEmiss_pz",  "missingEnergy[0].momentum.z")
               .Define("recoEmiss_e",   "missingEnergy[0].energy")
               .Define("recoEmiss_p4",  "TLorentzVector(recoEmiss_px, recoEmiss_py, recoEmiss_pz, recoEmiss_e)")
               .Define("recoEmiss_m",   "recoEmiss_p4.M()")

               #############################################
               ##          Build RECO P with PID          ##
               #############################################
               .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0,MCRecoAssociations1,Particle)")

               #############################################
               ##    Build RECO P with PID at vertex      ##
               #############################################
               .Define("RecoPartPIDAtVertex" ,"myUtils::get_RP_atVertex(RecoPartPID, VertexObject)")

               #############################################
               ##         Build vertex variables          ##
               #############################################
               .Define("Vertex_x",        "myUtils::get_Vertex_x(VertexObject)")
               .Define("Vertex_y",        "myUtils::get_Vertex_y(VertexObject)")
               .Define("Vertex_z",        "myUtils::get_Vertex_z(VertexObject)")
               .Define("Vertex_xErr",     "myUtils::get_Vertex_xErr(VertexObject)")
               .Define("Vertex_yErr",     "myUtils::get_Vertex_yErr(VertexObject)")
               .Define("Vertex_zErr",     "myUtils::get_Vertex_zErr(VertexObject)")

               .Define("Vertex_chi2",     "myUtils::get_Vertex_chi2(VertexObject)")
               .Define("Vertex_mcind",    "myUtils::get_Vertex_indMC(VertexObject)")
               .Define("Vertex_ind",      "myUtils::get_Vertex_ind(VertexObject)")
               .Define("Vertex_isPV",     "myUtils::get_Vertex_isPV(VertexObject)")
               .Define("Vertex_ntrk",     "myUtils::get_Vertex_ntracks(VertexObject)")
               .Define("Vertex_n",        "int(Vertex_x.size())")
               .Define("Vertex_mass",     "myUtils::get_Vertex_mass(VertexObject,RecoPartPIDAtVertex)")
               .Define("Vertex_p4",       "FCCAnalyses::ZHfunctions::get_Vertex_p4(VertexObject,RecoPartPIDAtVertex)")
               .Define("Vertex_px",       "ROOT::VecOps::RVec<float> result; for (auto & p: Vertex_p4) {result.push_back(p.Px());} return result;")
               .Define("Vertex_py",       "ROOT::VecOps::RVec<float> result; for (auto & p: Vertex_p4) {result.push_back(p.Py());} return result;")
               .Define("Vertex_pz",       "ROOT::VecOps::RVec<float> result; for (auto & p: Vertex_p4) {result.push_back(p.Pz());} return result;")
               .Define("Vertex_e",        "ROOT::VecOps::RVec<float> result; for (auto & p: Vertex_p4) {result.push_back(p.E ());} return result;")
               .Define("Vertex_vec",      "FCCAnalyses::ZHfunctions::build_p4(Vertex_x, Vertex_y, Vertex_z, Vertex_mass)")
               .Define("Vertex_phi",      "ROOT::VecOps::RVec<float> result; for (auto & p: Vertex_vec) {result.push_back(p.Phi());} return result;")
               .Define("Vertex_theta",    "ROOT::VecOps::RVec<float> result; for (auto & p: Vertex_vec) {result.push_back(p.Theta());} return result;")

               .Define("Vertex_d2PV",     "myUtils::get_Vertex_d2PV(VertexObject,-1)")
               .Define("Vertex_d2PVx",    "myUtils::get_Vertex_d2PV(VertexObject,0)")
               .Define("Vertex_d2PVy",    "myUtils::get_Vertex_d2PV(VertexObject,1)")
               .Define("Vertex_d2PVz",    "myUtils::get_Vertex_d2PV(VertexObject,2)")

               .Define("Vertex_d2PVErr",  "myUtils::get_Vertex_d2PVError(VertexObject,-1)")
               .Define("Vertex_d2PVxErr", "myUtils::get_Vertex_d2PVError(VertexObject,0)")
               .Define("Vertex_d2PVyErr", "myUtils::get_Vertex_d2PVError(VertexObject,1)")
               .Define("Vertex_d2PVzErr", "myUtils::get_Vertex_d2PVError(VertexObject,2)")

               .Define("Vertex_d2PVSig",  "Vertex_d2PV/Vertex_d2PVErr")
               .Define("Vertex_d2PVxSig", "Vertex_d2PVx/Vertex_d2PVxErr")
               .Define("Vertex_d2PVySig", "Vertex_d2PVy/Vertex_d2PVyErr")
               .Define("Vertex_d2PVzSig", "Vertex_d2PVz/Vertex_d2PVzErr")

               .Define("Vertex_d2MC",     "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,-1)")
               .Define("Vertex_d2MCx",    "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,0)")
               .Define("Vertex_d2MCy",    "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,1)")
               .Define("Vertex_d2MCz",    "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,2)")

               .Define("EVT_dPV2DVmin",   "myUtils::get_dPV2DV_min(Vertex_d2PV)")
               .Define("EVT_dPV2DVmax",   "myUtils::get_dPV2DV_max(Vertex_d2PV)")
               .Define("EVT_dPV2DVave",   "myUtils::get_dPV2DV_ave(Vertex_d2PV)")

               #############################################
               ##              Build the thrust           ##
               #############################################
               .Define("RP_e",              "ReconstructedParticle::get_e(RecoPartPIDAtVertex)")
               .Define("RP_m_true",         "ReconstructedParticle::get_mass(RecoPartPIDAtVertex)")
               .Define("RP_m_reco",         "ReconstructedParticle::get_mass(ReconstructedParticles)")
               .Define("RP_px",             "ReconstructedParticle::get_px(RecoPartPIDAtVertex)")
               .Define("RP_py",             "ReconstructedParticle::get_py(RecoPartPIDAtVertex)")
               .Define("RP_pz",             "ReconstructedParticle::get_pz(RecoPartPIDAtVertex)")
               .Define("RP_eta",            "ReconstructedParticle::get_eta(RecoPartPIDAtVertex)")
               .Define("RP_phi",            "ReconstructedParticle::get_phi(RecoPartPIDAtVertex)")
               .Define("RP_theta",          "ReconstructedParticle::get_theta(RecoPartPIDAtVertex)")
               .Define("RP_charge",         "ReconstructedParticle::get_charge(RecoPartPIDAtVertex)")
               .Define("RP_fromPV",         "FCCAnalyses::ZHfunctions::get_RP_isfromPV(VertexObject,RecoPartPIDAtVertex)")
               .Define("RP_vert_ind",       "FCCAnalyses::ZHfunctions::get_RP_Vert_Ind(VertexObject,RecoPartPIDAtVertex)")
               .Define("RP_vert_e",         "ROOT::VecOps::RVec<float> result; for (auto & i: RP_vert_ind) {if (i==-1) result.push_back(-1); else result.push_back(Vertex_e.at(i));} return result;")
               .Define("RP_vert_mass",      "ROOT::VecOps::RVec<float> result; for (auto & i: RP_vert_ind) {if (i==-1) result.push_back(-1); else result.push_back(Vertex_mass.at(i));} return result;")

               .Define("RP_trk_d0",         "ReconstructedParticle2Track::getRP2TRK_D0       (RecoPartPIDAtVertex,EFlowTrack_1)")
               .Define("RP_trk_z0",         "ReconstructedParticle2Track::getRP2TRK_Z0       (RecoPartPIDAtVertex,EFlowTrack_1)")
               .Define("RP_trk_phi",        "ReconstructedParticle2Track::getRP2TRK_phi      (RecoPartPIDAtVertex,EFlowTrack_1)")
               .Define("RP_trk_omega",      "ReconstructedParticle2Track::getRP2TRK_omega    (RecoPartPIDAtVertex,EFlowTrack_1)")
               .Define("RP_trk_tanLambda",  "ReconstructedParticle2Track::getRP2TRK_tanLambda(RecoPartPIDAtVertex,EFlowTrack_1)")
               .Define("RP_dndx",           "FCCAnalyses::ZHfunctions::get_RP_dndx(RecoPartPIDAtVertex, EFlowTrack_2, EFlowTrack)")
               .Define("RP_mtof",           "FCCAnalyses::ZHfunctions::get_RP_mtof(RecoPartPIDAtVertex, EFlowTrack_L, EFlowTrack, TrackerHits, EFlowPhoton, EFlowNeutralHadron, CalorimeterHits, MC_PV_xyzt)") #constituent, PathLength, PFTrack, TrackerHits, PFPhoton, PFNeutralHadrons, Calorimeterhits, PV 4-vec, potision time

               .Define("EVT_thrustNP",      'Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define("RP_thrustangleNP",  'Algorithms::getAxisCosTheta(EVT_thrustNP, RP_px, RP_py, RP_pz)')
               .Define("EVT_thrust",        'Algorithms::getThrustPointing(1.)(RP_thrustangleNP, RP_e, EVT_thrustNP)')
               .Define("RP_thrustangle",    'Algorithms::getAxisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')
               .Define("EVT_thrust_phi",    'FCCAnalyses::ZHfunctions::getAxisPhi(EVT_thrust)')
               .Define("EVT_thrust_theta",  'FCCAnalyses::ZHfunctions::getAxisTheta(EVT_thrust)')

               ###################################################
               ##    check MC mathc with certain decay chains   ##
               ###################################################

               .Define("RP_nMC",        "FCCAnalyses::ZHfunctions::getRP2MC_nMC(MCRecoAssociations0,MCRecoAssociations1,RecoPartPIDAtVertex)")
               .Define("RP_MCidx",      "ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,RecoPartPIDAtVertex)")
               .Define("RP_fromBc",     "FCCAnalyses::ZHfunctions::get_RP_isDescendant(541, true)(RP_MCidx, Particle, Particle1)")
               .Define("RP_fromBs",     "FCCAnalyses::ZHfunctions::get_RP_isDescendant(531, true)(RP_MCidx, Particle, Particle1)")
               .Define("RP_fromBu",     "FCCAnalyses::ZHfunctions::get_RP_isDescendant(521, true)(RP_MCidx, Particle, Particle1)")
               .Define("RP_fromBd",     "FCCAnalyses::ZHfunctions::get_RP_isDescendant(511, true)(RP_MCidx, Particle, Particle1)")
               .Define("RP_fromLb",     "FCCAnalyses::ZHfunctions::get_RP_isDescendant(5122, true)(RP_MCidx, Particle, Particle1)")

               .Define("Vertex_fromBc", "FCCAnalyses::ZHfunctions::get_Vertex_containDescendant(VertexObject, RP_fromBc)")
               .Define("Vertex_fromBs", "FCCAnalyses::ZHfunctions::get_Vertex_containDescendant(VertexObject, RP_fromBs)")
               .Define("Vertex_fromBu", "FCCAnalyses::ZHfunctions::get_Vertex_containDescendant(VertexObject, RP_fromBu)")
               .Define("Vertex_fromBd", "FCCAnalyses::ZHfunctions::get_Vertex_containDescendant(VertexObject, RP_fromBd)")
               .Define("Vertex_fromLb", "FCCAnalyses::ZHfunctions::get_Vertex_containDescendant(VertexObject, RP_fromLb)")

               #############################################
               ##      thrust angle of gen b, Bs          ##
               #############################################

               .Define("genBd_thrustangle",        'Algorithms::getAxisCosTheta(EVT_thrust, genBd_px, genBd_py, genBd_pz)')
               .Define("genBu_thrustangle",        'Algorithms::getAxisCosTheta(EVT_thrust, genBu_px, genBu_py, genBu_pz)')
               .Define("genBs_thrustangle",        'Algorithms::getAxisCosTheta(EVT_thrust, genBs_px, genBs_py, genBs_pz)')
               .Define("genBc_thrustangle",        'Algorithms::getAxisCosTheta(EVT_thrust, genBc_px, genBc_py, genBc_pz)')
               .Define("genLb_thrustangle",        'Algorithms::getAxisCosTheta(EVT_thrust, genLb_px, genLb_py, genLb_pz)')
               .Define("recoEmiss_thrustangle",    'Algorithms::getAxisCosTheta(EVT_thrust, recoEmiss_px, recoEmiss_py, recoEmiss_pz)')

               #############################################
               ##        Get thrust related values        ##
               #############################################
               ##hemis0 == negative angle == max energy hemisphere if pointing
               ##hemis1 == positive angle == min energy hemisphere if pointing
               .Define("EVT_thrusthemis0_n",    "Algorithms::getAxisN(0)(RP_thrustangle, RP_charge)")
               .Define("EVT_thrusthemis1_n",    "Algorithms::getAxisN(1)(RP_thrustangle, RP_charge)")
               .Define("EVT_thrusthemis0_e",    "Algorithms::getAxisEnergy(0)(RP_thrustangle, RP_charge, RP_e)")
               .Define("EVT_thrusthemis1_e",    "Algorithms::getAxisEnergy(1)(RP_thrustangle, RP_charge, RP_e)")

               .Define("EVT_ThrustEmax_E",         "EVT_thrusthemis0_e.at(0)")
               .Define("EVT_ThrustEmax_Echarged",  "EVT_thrusthemis0_e.at(1)")
               .Define("EVT_ThrustEmax_Eneutral",  "EVT_thrusthemis0_e.at(2)")
               .Define("EVT_ThrustEmax_N",         "float(EVT_thrusthemis0_n.at(0))")
               .Define("EVT_ThrustEmax_Ncharged",  "float(EVT_thrusthemis0_n.at(1))")
               .Define("EVT_ThrustEmax_Nneutral",  "float(EVT_thrusthemis0_n.at(2))")

               .Define("EVT_ThrustEmin_E",         "EVT_thrusthemis1_e.at(0)")
               .Define("EVT_ThrustEmin_Echarged",  "EVT_thrusthemis1_e.at(1)")
               .Define("EVT_ThrustEmin_Eneutral",  "EVT_thrusthemis1_e.at(2)")
               .Define("EVT_ThrustEmin_N",         "float(EVT_thrusthemis1_n.at(0))")
               .Define("EVT_ThrustEmin_Ncharged",  "float(EVT_thrusthemis1_n.at(1))")
               .Define("EVT_ThrustEmin_Nneutral",  "float(EVT_thrusthemis1_n.at(2))")


               .Define("Vertex_thrust_angle",   "myUtils::get_Vertex_thrusthemis_angle(VertexObject, RecoPartPIDAtVertex, EVT_thrust)")
               .Define("DVertex_thrust_angle",  "myUtils::get_DVertex_thrusthemis_angle(VertexObject, RecoPartPIDAtVertex, EVT_thrust)")
               ###0 == negative angle==max energy , 1 == positive angle == min energy
               .Define("Vertex_thrusthemis_emin",    "myUtils::get_Vertex_thrusthemis(Vertex_thrust_angle, 1)")
               .Define("Vertex_thrusthemis_emax",    "myUtils::get_Vertex_thrusthemis(Vertex_thrust_angle, 0)")

               .Define("EVT_ThrustEmin_NDV", "float(myUtils::get_Npos(DVertex_thrust_angle))")
               .Define("EVT_ThrustEmax_NDV", "float(myUtils::get_Nneg(DVertex_thrust_angle))")

               .Define("EVT_Thrust_Mag",  "EVT_thrust.at(0)")
               .Define("EVT_Thrust_X",    "EVT_thrust.at(1)")
               .Define("EVT_Thrust_XErr", "EVT_thrust.at(2)")
               .Define("EVT_Thrust_Y",    "EVT_thrust.at(3)")
               .Define("EVT_Thrust_YErr", "EVT_thrust.at(4)")
               .Define("EVT_Thrust_Z",    "EVT_thrust.at(5)")
               .Define("EVT_Thrust_ZErr", "EVT_thrust.at(6)")

               .Define("DV_tracks", "myUtils::get_pseudotrack(VertexObject,RecoPartPIDAtVertex)")

               .Define("DV_d0",            "myUtils::get_trackd0(DV_tracks)")
               .Define("DV_z0",            "myUtils::get_trackz0(DV_tracks)")

               ##############################
               ##    PV info as event var  ##
               ##############################

               .Define("PV_x",              "Vertex_x           [Vertex_isPV==1]")
               .Define("PV_y",              "Vertex_y           [Vertex_isPV==1]")
               .Define("PV_z",              "Vertex_z           [Vertex_isPV==1]")
               .Define("PV_ntrk",           "Vertex_ntrk        [Vertex_isPV==1]")
               .Define("PV_mass",           "Vertex_mass        [Vertex_isPV==1]")
               .Define("PV_px",             "Vertex_px          [Vertex_isPV==1]")
               .Define("PV_py",             "Vertex_py          [Vertex_isPV==1]")
               .Define("PV_pz",             "Vertex_pz          [Vertex_isPV==1]")
               .Define("PV_e",              "Vertex_e           [Vertex_isPV==1]")
               .Define("PV_thrust_angle",   "Vertex_thrust_angle[Vertex_isPV==1]")
               .Define("PV_Dphi",           "Vertex_phi         [Vertex_isPV==1] - EVT_thrust_phi")
               .Define("PV_Dtheta",         "Vertex_theta       [Vertex_isPV==1] - EVT_thrust_theta")

               .Define("PV_x_offset",       "PV_x - MC_PV_xyzt.X()")
               .Define("PV_y_offset",       "PV_y - MC_PV_xyzt.Y()")
               .Define("PV_z_offset",       "PV_z - MC_PV_xyzt.Z()")

               .Define("RP_e_Emin",              "RP_e     [RP_thrustangle>0]")
               .Define("RP_m_true_Emin",         "RP_m_true[RP_thrustangle>0]")
               .Define("RP_m_reco_Emin",         "RP_m_reco[RP_thrustangle>0]")
               .Define("RP_px_Emin",             "RP_px    [RP_thrustangle>0]")
               .Define("RP_py_Emin",             "RP_py    [RP_thrustangle>0]")
               .Define("RP_pz_Emin",             "RP_pz    [RP_thrustangle>0]")
               .Define("RP_Dphi_Emin",           "RP_phi   [RP_thrustangle>0] - EVT_thrust_phi")
               .Define("RP_Dtheta_Emin",         "RP_theta [RP_thrustangle>0] - EVT_thrust_theta")
               .Define("RP_charge_Emin",         "RP_charge[RP_thrustangle>0]")
               .Define("RP_fromPV_Emin",         "RP_fromPV[RP_thrustangle>0]")
               .Define("RP_vert_ind_Emin",       "RP_vert_ind [RP_thrustangle>0]")
               .Define("RP_vert_e_Emin",         "RP_vert_e   [RP_thrustangle>0]")
               .Define("RP_vert_mass_Emin",      "RP_vert_mass[RP_thrustangle>0]")
               .Define("RP_trk_d0_Emin",         "RP_trk_d0       [RP_thrustangle>0]")
               .Define("RP_trk_z0_Emin",         "RP_trk_z0       [RP_thrustangle>0]")
               .Define("RP_trk_phi_Emin",        "RP_trk_phi      [RP_thrustangle>0]")
               .Define("RP_trk_omega_Emin",      "RP_trk_omega    [RP_thrustangle>0]")
               .Define("RP_trk_tanLambda_Emin",  "RP_trk_tanLambda[RP_thrustangle>0]")
               .Define("RP_dndx_Emin",           "RP_dndx         [RP_thrustangle>0]")
               .Define("RP_mtof_Emin",           "RP_mtof         [RP_thrustangle>0]")
               .Define("RP_nMC_Emin",            "RP_nMC   [RP_thrustangle>0]")
               .Define("RP_MCidx_Emin",          "RP_MCidx [RP_thrustangle>0]")
               .Define("RP_fromBc_Emin",         "RP_fromBc[RP_thrustangle>0]")
               .Define("RP_fromBs_Emin",         "RP_fromBs[RP_thrustangle>0]")
               .Define("RP_fromBu_Emin",         "RP_fromBu[RP_thrustangle>0]")
               .Define("RP_fromBd_Emin",         "RP_fromBd[RP_thrustangle>0]")
               .Define("RP_fromLb_Emin",         "RP_fromLb[RP_thrustangle>0]")
               .Define("RP_thrustangle_Emin",    "RP_thrustangle[RP_thrustangle>0]")
               .Define("Vertex_isPV_Emin",       "Vertex_isPV     [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_mass_Emin",       "Vertex_mass     [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_px_Emin",         "Vertex_px       [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_py_Emin",         "Vertex_py       [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_pz_Emin",         "Vertex_pz       [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_e_Emin",          "Vertex_e        [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_x_Emin",          "Vertex_x        [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_y_Emin",          "Vertex_y        [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_z_Emin",          "Vertex_z        [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_xErr_Emin",       "Vertex_xErr     [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_yErr_Emin",       "Vertex_yErr     [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_zErr_Emin",       "Vertex_zErr     [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_ntrk_Emin",       "Vertex_ntrk     [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_chi2_Emin",       "Vertex_chi2     [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_d2PV_Emin",       "Vertex_d2PV     [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_d2PVSig_Emin",    "Vertex_d2PVSig  [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_Dphi_Emin",       "Vertex_phi      [Vertex_thrust_angle>0 || Vertex_isPV==1] - EVT_thrust_phi")
               .Define("Vertex_Dtheta_Emin",     "Vertex_theta    [Vertex_thrust_angle>0 || Vertex_isPV==1] - EVT_thrust_theta")
               .Define("Vertex_thrustangle_Emin","Vertex_thrust_angle    [Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_fromBc_Emin",     "Vertex_fromBc[Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_fromBs_Emin",     "Vertex_fromBs[Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_fromBu_Emin",     "Vertex_fromBu[Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_fromBd_Emin",     "Vertex_fromBd[Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("Vertex_fromLb_Emin",     "Vertex_fromLb[Vertex_thrust_angle>0 || Vertex_isPV==1]")
               .Define("n_Bc_Emin",              "int(genBc_thrustangle[genBc_thrustangle>0].size())")
               .Define("n_Bs_Emin",              "int(genBs_thrustangle[genBs_thrustangle>0].size())")
               .Define("n_Bu_Emin",              "int(genBu_thrustangle[genBu_thrustangle>0].size())")
               .Define("n_Bd_Emin",              "int(genBd_thrustangle[genBd_thrustangle>0].size())")
               .Define("n_Lb_Emin",              "int(genLb_thrustangle[genLb_thrustangle>0].size())")
               .Define("label_Bc_Emin",          "int(n_Bc_Emin==1 && n_Bs_Emin==0 && n_Bu_Emin==0 && n_Bd_Emin==0 && n_Lb_Emin==0)" )
               .Define("label_Bs_Emin",          "int(n_Bc_Emin==0 && n_Bs_Emin==1 && n_Bu_Emin==0 && n_Bd_Emin==0 && n_Lb_Emin==0)" )
               .Define("label_Bu_Emin",          "int(n_Bc_Emin==0 && n_Bs_Emin==0 && n_Bu_Emin==1 && n_Bd_Emin==0 && n_Lb_Emin==0)" )
               .Define("label_Bd_Emin",          "int(n_Bc_Emin==0 && n_Bs_Emin==0 && n_Bu_Emin==0 && n_Bd_Emin==1 && n_Lb_Emin==0)" )
               .Define("label_Lb_Emin",          "int(n_Bc_Emin==0 && n_Bs_Emin==0 && n_Bu_Emin==0 && n_Bd_Emin==0 && n_Lb_Emin==1)" )
               .Define("label_light_Emin",       "int(n_Bc_Emin==0 && n_Bs_Emin==0 && (n_Bu_Emin>0 || n_Bd_Emin>0) && n_Lb_Emin==0)" )
               .Define("label_hasBc_Emin",       "int(n_Bc_Emin>0)" )
               .Define("label_has1Bc_Emin",      "int(n_Bc_Emin==1)" )


               .Define("RP_e_Emax",              "RP_e     [RP_thrustangle<0]")
               .Define("RP_m_true_Emax",         "RP_m_true[RP_thrustangle<0]")
               .Define("RP_m_reco_Emax",         "RP_m_reco[RP_thrustangle<0]")
               .Define("RP_px_Emax",             "RP_px    [RP_thrustangle<0]")
               .Define("RP_py_Emax",             "RP_py    [RP_thrustangle<0]")
               .Define("RP_pz_Emax",             "RP_pz    [RP_thrustangle<0]")
               .Define("RP_Dphi_Emax",           "RP_phi   [RP_thrustangle<0] + EVT_thrust_phi")
               .Define("RP_Dtheta_Emax",         "RP_theta [RP_thrustangle<0] + EVT_thrust_theta - 3.14159")
               .Define("RP_charge_Emax",         "RP_charge[RP_thrustangle<0]")
               .Define("RP_fromPV_Emax",         "RP_fromPV[RP_thrustangle<0]")
               .Define("RP_vert_ind_Emax",       "RP_vert_ind [RP_thrustangle<0]")
               .Define("RP_vert_e_Emax",         "RP_vert_e   [RP_thrustangle<0]")
               .Define("RP_vert_mass_Emax",      "RP_vert_mass[RP_thrustangle<0]")
               .Define("RP_trk_d0_Emax",         "RP_trk_d0       [RP_thrustangle<0]")
               .Define("RP_trk_z0_Emax",         "RP_trk_z0       [RP_thrustangle<0]")
               .Define("RP_trk_phi_Emax",        "RP_trk_phi      [RP_thrustangle<0]")
               .Define("RP_trk_omega_Emax",      "RP_trk_omega    [RP_thrustangle<0]")
               .Define("RP_trk_tanLambda_Emax",  "RP_trk_tanLambda[RP_thrustangle<0]")
               .Define("RP_dndx_Emax",           "RP_dndx         [RP_thrustangle<0]")
               .Define("RP_mtof_Emax",           "RP_mtof         [RP_thrustangle<0]")
               .Define("RP_nMC_Emax",            "RP_nMC   [RP_thrustangle<0]")
               .Define("RP_MCidx_Emax",          "RP_MCidx [RP_thrustangle<0]")
               .Define("RP_fromBc_Emax",         "RP_fromBc[RP_thrustangle<0]")
               .Define("RP_fromBs_Emax",         "RP_fromBs[RP_thrustangle<0]")
               .Define("RP_fromBu_Emax",         "RP_fromBu[RP_thrustangle<0]")
               .Define("RP_fromBd_Emax",         "RP_fromBd[RP_thrustangle<0]")
               .Define("RP_fromLb_Emax",         "RP_fromLb[RP_thrustangle<0]")
               .Define("RP_thrustangle_Emax",    "- RP_thrustangle[RP_thrustangle<0]")
               .Define("Vertex_isPV_Emax",       "Vertex_isPV     [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_mass_Emax",       "Vertex_mass     [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_px_Emax",         "Vertex_px       [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_py_Emax",         "Vertex_py       [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_pz_Emax",         "Vertex_pz       [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_e_Emax",          "Vertex_e        [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_x_Emax",          "Vertex_x        [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_y_Emax",          "Vertex_y        [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_z_Emax",          "Vertex_z        [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_xErr_Emax",       "Vertex_xErr     [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_yErr_Emax",       "Vertex_yErr     [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_zErr_Emax",       "Vertex_zErr     [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_ntrk_Emax",       "Vertex_ntrk     [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_chi2_Emax",       "Vertex_chi2     [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_d2PV_Emax",       "Vertex_d2PV     [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_d2PVSig_Emax",    "Vertex_d2PVSig  [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_Dphi_Emax",       "Vertex_phi      [Vertex_thrust_angle<0 || Vertex_isPV==1] - EVT_thrust_phi")
               .Define("Vertex_Dtheta_Emax",     "Vertex_theta    [Vertex_thrust_angle<0 || Vertex_isPV==1] - EVT_thrust_theta")
               .Define("Vertex_thrustangle_Emax","- Vertex_thrust_angle    [Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_fromBc_Emax",     "Vertex_fromBc[Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_fromBs_Emax",     "Vertex_fromBs[Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_fromBu_Emax",     "Vertex_fromBu[Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_fromBd_Emax",     "Vertex_fromBd[Vertex_thrust_angle<0 || Vertex_isPV==1]")
               .Define("Vertex_fromLb_Emax",     "Vertex_fromLb[Vertex_thrust_angle<0 || Vertex_isPV==1]")

               .Define("n_Bc_Emax",              "int(genBc_thrustangle[genBc_thrustangle<0].size())")
               .Define("n_Bs_Emax",              "int(genBs_thrustangle[genBs_thrustangle<0].size())")
               .Define("n_Bu_Emax",              "int(genBu_thrustangle[genBu_thrustangle<0].size())")
               .Define("n_Bd_Emax",              "int(genBd_thrustangle[genBd_thrustangle<0].size())")
               .Define("n_Lb_Emax",              "int(genLb_thrustangle[genLb_thrustangle<0].size())")
               .Define("label_Bc_Emax",          "int(n_Bc_Emax==1 && n_Bs_Emax==0 && n_Bu_Emax==0 && n_Bd_Emax==0 && n_Lb_Emax==0)" )
               .Define("label_Bs_Emax",          "int(n_Bc_Emax==0 && n_Bs_Emax==1 && n_Bu_Emax==0 && n_Bd_Emax==0 && n_Lb_Emax==0)" )
               .Define("label_Bu_Emax",          "int(n_Bc_Emax==0 && n_Bs_Emax==0 && n_Bu_Emax==1 && n_Bd_Emax==0 && n_Lb_Emax==0)" )
               .Define("label_Bd_Emax",          "int(n_Bc_Emax==0 && n_Bs_Emax==0 && n_Bu_Emax==0 && n_Bd_Emax==1 && n_Lb_Emax==0)" )
               .Define("label_Lb_Emax",          "int(n_Bc_Emax==0 && n_Bs_Emax==0 && n_Bu_Emax==0 && n_Bd_Emax==0 && n_Lb_Emax==1)" )
               .Define("label_light_Emax",       "int(n_Bc_Emax==0 && n_Bs_Emax==0 && (n_Bu_Emax>0 || n_Bd_Emax>0) && n_Lb_Emax==0)" )
               .Define("label_hasBc_Emax",       "int(n_Bc_Emax>0)" )
               .Define("label_has1Bc_Emax",      "int(n_Bc_Emax==1)" )


           )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [

                "recoEmiss_px", "recoEmiss_py", "recoEmiss_pz", "recoEmiss_e", "recoEmiss_m",
                "recoEmiss_thrustangle",

                "PV_x_offset",
                "PV_y_offset",
                "PV_z_offset",

                "RP_e_Emin",             
                "RP_m_true_Emin",
                "RP_m_reco_Emin",
                "RP_px_Emin", 
                "RP_py_Emin", 
                "RP_pz_Emin", 
                "RP_Dphi_Emin",          
                "RP_Dtheta_Emin",        
                "RP_charge_Emin",
                "RP_fromPV_Emin",
                "RP_vert_ind_Emin",
                "RP_vert_e_Emin",
                "RP_vert_mass_Emin",
                "RP_trk_d0_Emin",
                "RP_trk_z0_Emin",
                "RP_trk_phi_Emin",
                "RP_trk_omega_Emin",
                "RP_trk_tanLambda_Emin",
                "RP_dndx_Emin",
                "RP_mtof_Emin",
                "RP_nMC_Emin",   
                "RP_MCidx_Emin", 
                "RP_fromBc_Emin",
                "RP_fromBs_Emin",
                "RP_fromBu_Emin",
                "RP_fromBd_Emin",
                "RP_fromLb_Emin",
                "RP_thrustangle_Emin",
                "Vertex_isPV_Emin",
                "Vertex_mass_Emin", 
                "Vertex_px_Emin",
                "Vertex_py_Emin",
                "Vertex_pz_Emin",
                "Vertex_e_Emin",
                "Vertex_x_Emin",   
                "Vertex_y_Emin",   
                "Vertex_z_Emin",   
                "Vertex_xErr_Emin",
                "Vertex_yErr_Emin",
                "Vertex_zErr_Emin",
                "Vertex_ntrk_Emin",      
                "Vertex_chi2_Emin",      
                "Vertex_d2PV_Emin",
                "Vertex_d2PVSig_Emin",
                "Vertex_Dphi_Emin",      
                "Vertex_Dtheta_Emin",    
                "Vertex_thrustangle_Emin",
                "Vertex_fromBc_Emin",
                "Vertex_fromBs_Emin",
                "Vertex_fromBu_Emin",
                "Vertex_fromBd_Emin",
                "Vertex_fromLb_Emin",

                "n_Bc_Emin",             
                "n_Bs_Emin",             
                "n_Bu_Emin",             
                "n_Bd_Emin",             
                "n_Lb_Emin",       
                "label_Bc_Emin",    
                "label_Bs_Emin",   
                "label_Bu_Emin",   
                "label_Bd_Emin",   
                "label_Lb_Emin",   
                "label_light_Emin",
                "label_hasBc_Emin",
                "label_has1Bc_Emin",

                "RP_e_Emax",             
                "RP_m_true_Emax",
                "RP_m_reco_Emax",
                "RP_px_Emax", 
                "RP_py_Emax", 
                "RP_pz_Emax", 
                "RP_Dphi_Emax",          
                "RP_Dtheta_Emax",        
                "RP_charge_Emax",
                "RP_fromPV_Emax",
                "RP_vert_ind_Emax",
                "RP_vert_e_Emax",
                "RP_vert_mass_Emax",
                "RP_trk_d0_Emax",
                "RP_trk_z0_Emax",
                "RP_trk_phi_Emax",
                "RP_trk_omega_Emax",
                "RP_trk_tanLambda_Emax",
                "RP_dndx_Emax",
                "RP_mtof_Emax",
                "RP_nMC_Emax",   
                "RP_MCidx_Emax", 
                "RP_fromBc_Emax",
                "RP_fromBs_Emax",
                "RP_fromBu_Emax",
                "RP_fromBd_Emax",
                "RP_fromLb_Emax",
                "RP_thrustangle_Emax",
                "Vertex_isPV_Emax",
                "Vertex_mass_Emax",
                "Vertex_px_Emax",
                "Vertex_py_Emax",
                "Vertex_pz_Emax",
                "Vertex_e_Emax",
                "Vertex_x_Emax",   
                "Vertex_y_Emax",   
                "Vertex_z_Emax",   
                "Vertex_xErr_Emax",
                "Vertex_yErr_Emax",
                "Vertex_zErr_Emax",
                "Vertex_ntrk_Emax",      
                "Vertex_chi2_Emax",      
                "Vertex_d2PV_Emax",
                "Vertex_d2PVSig_Emax",
                "Vertex_Dphi_Emax",      
                "Vertex_Dtheta_Emax",    
                "Vertex_thrustangle_Emax",
                "Vertex_fromBc_Emax",
                "Vertex_fromBs_Emax",
                "Vertex_fromBu_Emax",
                "Vertex_fromBd_Emax",
                "Vertex_fromLb_Emax",

                "n_Bc_Emax",             
                "n_Bs_Emax",             
                "n_Bu_Emax",             
                "n_Bd_Emax",             
                "n_Lb_Emax",
                "label_Bc_Emax",   
                "label_Bs_Emax",   
                "label_Bu_Emax",   
                "label_Bd_Emax",   
                "label_Lb_Emax",   
                "label_light_Emax",
                "label_hasBc_Emax",
                "label_has1Bc_Emax",

                ]
        return branchList
