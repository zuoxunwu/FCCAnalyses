#analysis_stage1

# list of samples to process
processList_full = {
    'p8_ee_Zbb_ecm91':{'chunks':10, 'fraction':0.01},
    'p8_ee_Zcc_ecm91':{'chunks':10, 'fraction':0.01},
    'p8_ee_Zss_ecm91':{'chunks':10, 'fraction':0.01},
    'p8_ee_Zud_ecm91':{'chunks':10, 'fraction':0.01},
    'p8_ee_Zbb_ecm91_EvtGen_Bs2TauTauTAUHADNU':{'chunks':10, 'fraction':0.1},
    'p8_ee_Zbb_ecm91_EvtGen_Bs2TauTau':{'chunks':10, 'fraction':0.1},
}

#processList_full = {
#    'p8_ee_Zbb_ecm91':{'chunks':100},
#    'p8_ee_Zcc_ecm91':{'chunks':100},
#    'p8_ee_Zss_ecm91':{'chunks':100},
#    'p8_ee_Zud_ecm91':{'chunks':100},
#    'p8_ee_Zbb_ecm91_EvtGen_Bs2TauTauTAUHADNU':{'chunks':20},
#    'p8_ee_Zbb_ecm91_EvtGen_Bs2TauTau':{'chunks':20},
#}

processList_test = {
    'p8_ee_Zbb_ecm91_EvtGen_Bs2TauTauTAUHADNU':{'chunks':1, 'fraction':0.001},
}

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
outputDirEos   = "/eos/experiment/fcc/ee/analyses_storage/flavor/Bs2TauTau/flatNtuples/winter2023/analysis_stage1_noFilter_fullP4/"

# if runBatch = False, save output locally
outputDir   = "outputs/FCCee/flavor/Bs2TauTau/analysis_stage1/"

includePaths = ["functions.h"]

import ROOT
ROOT.gInterpreter.ProcessLine('''
TMVA::Experimental::RBDT<> bdt("BDT", "/afs/cern.ch/work/x/xzuo/public/FCC_files/Bs2TauTau/BDT/xgb_bdt_trained_iteration_16.root");
computeModel1 = TMVA::Experimental::Compute<18, float>(bdt);
''')


MVAFilter   = "EVT_MVA1>0.6"

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

               .Define("genBs",   "FCCAnalyses::MCParticle::sel_pdgID(531, true)(Particle)")
               .Define("n_genBs",     "FCCAnalyses::MCParticle::get_n   (genBs)")
               .Define("genBs_px",    "FCCAnalyses::MCParticle::get_px  (genBs)")
               .Define("genBs_py",    "FCCAnalyses::MCParticle::get_py  (genBs)")
               .Define("genBs_pz",    "FCCAnalyses::MCParticle::get_pz  (genBs)")
               .Define("genBs_phi",   "FCCAnalyses::MCParticle::get_phi (genBs)")
               .Define("genBs_eta",   "FCCAnalyses::MCParticle::get_eta (genBs)")
               .Define("genBs_energy","FCCAnalyses::MCParticle::get_e   (genBs)")
               .Define("genBs_mass",  "FCCAnalyses::MCParticle::get_mass(genBs)")
               .Define("genBs_pdg",   "FCCAnalyses::MCParticle::get_pdg (genBs)")


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
               ##        Build Tau -> 3Pi candidates      ##
               #############################################
               .Define("Tau23PiCandidates",         "myUtils::build_tau23pi(VertexObject,RecoPartPIDAtVertex)")

               #############################################
               ##       Filter Tau -> 3Pi candidates      ##
               #############################################
               .Define("EVT_NTau23Pi",              "float(myUtils::getFCCAnalysesComposite_N(Tau23PiCandidates))")
#               .Filter("EVT_NTau23Pi>1")


               #############################################
               ##              Build the thrust           ##
               #############################################
               .Define("RP_e",          "ReconstructedParticle::get_e(RecoPartPIDAtVertex)")
               .Define("RP_px",         "ReconstructedParticle::get_px(RecoPartPIDAtVertex)")
               .Define("RP_py",         "ReconstructedParticle::get_py(RecoPartPIDAtVertex)")
               .Define("RP_pz",         "ReconstructedParticle::get_pz(RecoPartPIDAtVertex)")
               .Define("RP_charge",     "ReconstructedParticle::get_charge(RecoPartPIDAtVertex)")

               .Define("EVT_thrustNP",      'Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define("RP_thrustangleNP",  'Algorithms::getAxisCosTheta(EVT_thrustNP, RP_px, RP_py, RP_pz)')
               .Define("EVT_thrust",        'Algorithms::getThrustPointing(1.)(RP_thrustangleNP, RP_e, EVT_thrustNP)')
               .Define("RP_thrustangle",    'Algorithms::getAxisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')


               #############################################
               ##      thrust angle of gen b, Bs          ##
               #############################################

               .Define("genBottom_thrustangle",    'Algorithms::getAxisCosTheta(EVT_thrust, genBottom_px, genBottom_py, genBottom_pz)')
               .Define("genBs_thrustangle",        'Algorithms::getAxisCosTheta(EVT_thrust, genBs_px, genBs_py, genBs_pz)')
               .Define("genBs_Vertex_thrustangle", 'Algorithms::getAxisCosTheta(EVT_thrust, genBs_Vertex_x, genBs_Vertex_y, genBs_Vertex_z)')
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


               .Define("MVAVec1", ROOT.computeModel1, ["EVT_ThrustEmin_E",
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
                                                       "EVT_dPV2DVave"]) 
               .Define("EVT_MVA1", "MVAVec1.at(0)")
#               .Filter(MVAFilter)

               .Define("Tau23PiCandidates_mass",    "myUtils::getFCCAnalysesComposite_mass(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_q",       "myUtils::getFCCAnalysesComposite_charge(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_vertex",  "myUtils::getFCCAnalysesComposite_vertex(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_mcvertex","myUtils::getFCCAnalysesComposite_mcvertex(Tau23PiCandidates,VertexObject)")
               .Define("Tau23PiCandidates_px",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,0)")
               .Define("Tau23PiCandidates_py",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,1)")
               .Define("Tau23PiCandidates_pz",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,2)")
               .Define("Tau23PiCandidates_p",       "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,-1)")
               .Define("Tau23PiCandidates_B",       "myUtils::getFCCAnalysesComposite_B(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex)")
 
               .Define("Tau23PiCandidates_x",       "ROOT::VecOps::RVec<float> result; for (auto & p: Tau23PiCandidates_vertex) {result.push_back(Vertex_x.at(p));} return result;")
               .Define("Tau23PiCandidates_y",       "ROOT::VecOps::RVec<float> result; for (auto & p: Tau23PiCandidates_vertex) {result.push_back(Vertex_y.at(p));} return result;")
               .Define("Tau23PiCandidates_z",       "ROOT::VecOps::RVec<float> result; for (auto & p: Tau23PiCandidates_vertex) {result.push_back(Vertex_z.at(p));} return result;")
               .Define("Tau23PiCandidates_xErr",    "ROOT::VecOps::RVec<float> result; for (auto & p: Tau23PiCandidates_vertex) {result.push_back(Vertex_xErr.at(p));} return result;")
               .Define("Tau23PiCandidates_yErr",    "ROOT::VecOps::RVec<float> result; for (auto & p: Tau23PiCandidates_vertex) {result.push_back(Vertex_yErr.at(p));} return result;")
               .Define("Tau23PiCandidates_zErr",    "ROOT::VecOps::RVec<float> result; for (auto & p: Tau23PiCandidates_vertex) {result.push_back(Vertex_zErr.at(p));} return result;")
               .Define("Tau23PiCandidates_chi2",    "ROOT::VecOps::RVec<float> result; for (auto & p: Tau23PiCandidates_vertex) {result.push_back(Vertex_chi2.at(p));} return result;")
               .Define("Tau23PiCandidates_hemEmin", "ROOT::VecOps::RVec<float> result; for (auto & p: Tau23PiCandidates_vertex) {result.push_back(Vertex_thrusthemis_emin.at(p));} return result;")

               .Define("Tau23PiCandidates_track",   "myUtils::getFCCAnalysesComposite_track(Tau23PiCandidates, VertexObject)")
               .Define("Tau23PiCandidates_d0",      "myUtils::get_trackd0(Tau23PiCandidates_track)")
               .Define("Tau23PiCandidates_z0",      "myUtils::get_trackz0(Tau23PiCandidates_track)")

               .Define("Tau23PiCandidates_anglethrust", "myUtils::getFCCAnalysesComposite_anglethrust(Tau23PiCandidates, EVT_thrust)")
               .Define("EVT_ThrustEmin_NTau23PiCand",   "float(myUtils::get_Npos(cos(Tau23PiCandidates_anglethrust)))")
               .Define("EVT_ThrustEmax_NTau23PiCand",   "float(myUtils::get_Nneg(cos(Tau23PiCandidates_anglethrust)))")

               .Define("CUT_hasCandEmin",           "myUtils::has_anglethrust_emin(Tau23PiCandidates_anglethrust)")
#               .Filter("CUT_hasCandEmin>0")

               .Define("Tau23PiCandidates_rho",     "myUtils::build_rho(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex)")
               .Define("Tau23PiCandidates_rho1mass","myUtils::get_mass(Tau23PiCandidates_rho, 0)")
               .Define("Tau23PiCandidates_rho2mass","myUtils::get_mass(Tau23PiCandidates_rho, 1)")
               .Define("Tau23PiCandidates_rho1px",  "myUtils::get_px(Tau23PiCandidates_rho, 0)")
               .Define("Tau23PiCandidates_rho2px",  "myUtils::get_px(Tau23PiCandidates_rho, 1)")

               .Define("Tau23PiCandidates_rho1py",  "myUtils::get_py(Tau23PiCandidates_rho, 0)")
               .Define("Tau23PiCandidates_rho2py",  "myUtils::get_py(Tau23PiCandidates_rho, 1)")

               .Define("Tau23PiCandidates_rho1pz",  "myUtils::get_pz(Tau23PiCandidates_rho, 0)")
               .Define("Tau23PiCandidates_rho2pz",  "myUtils::get_pz(Tau23PiCandidates_rho, 1)")

               .Define("Tau23PiCandidates_pion1px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 0)")
               .Define("Tau23PiCandidates_pion1py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 1)")
               .Define("Tau23PiCandidates_pion1pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 2)")
               .Define("Tau23PiCandidates_pion1p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, -1)")
               .Define("Tau23PiCandidates_pion1q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0)")
               .Define("Tau23PiCandidates_pion1d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 0)")
               .Define("Tau23PiCandidates_pion1z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 0)")

               .Define("Tau23PiCandidates_pion2px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 0)")
               .Define("Tau23PiCandidates_pion2py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 1)")
               .Define("Tau23PiCandidates_pion2pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 2)")
               .Define("Tau23PiCandidates_pion2p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, -1)")
               .Define("Tau23PiCandidates_pion2q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1)")
               .Define("Tau23PiCandidates_pion2d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 1)")
               .Define("Tau23PiCandidates_pion2z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 1)")

               .Define("Tau23PiCandidates_pion3px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 0)")
               .Define("Tau23PiCandidates_pion3py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 1)")
               .Define("Tau23PiCandidates_pion3pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 2)")
               .Define("Tau23PiCandidates_pion3p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, -1)")
               .Define("Tau23PiCandidates_pion3q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2)")
               .Define("Tau23PiCandidates_pion3d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 2)")
               .Define("Tau23PiCandidates_pion3z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 2)")


               ###############################
               ##   collinear mass cal      ##
               ###############################

               .Define("Tau23PiCandidates_p4",  "FCCAnalyses::ZHfunctions::build_p4(Tau23PiCandidates_px, Tau23PiCandidates_py, Tau23PiCandidates_pz, Tau23PiCandidates_mass)")

               .Define("TauCand_hemEmin_x",          "Tau23PiCandidates_x          [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_y",          "Tau23PiCandidates_y          [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_z",          "Tau23PiCandidates_z          [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_q",          "Tau23PiCandidates_q          [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_chi2",       "Tau23PiCandidates_chi2       [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_thrustangle","Tau23PiCandidates_anglethrust[Tau23PiCandidates_hemEmin>0]")

               .Define("TauCand_hemEmin_p4",  "Tau23PiCandidates_p4  [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_px",  "ROOT::VecOps::RVec<float> result; for (auto & p: TauCand_hemEmin_p4) {result.push_back(p.Px());} return result;")
               .Define("TauCand_hemEmin_py",  "ROOT::VecOps::RVec<float> result; for (auto & p: TauCand_hemEmin_p4) {result.push_back(p.Py());} return result;")
               .Define("TauCand_hemEmin_pz",  "ROOT::VecOps::RVec<float> result; for (auto & p: TauCand_hemEmin_p4) {result.push_back(p.Pz());} return result;")
               .Define("TauCand_hemEmin_p",   "ROOT::VecOps::RVec<float> result; for (auto & p: TauCand_hemEmin_p4) {result.push_back(p.P ());} return result;")
               .Define("TauCand_hemEmin_e",   "ROOT::VecOps::RVec<float> result; for (auto & p: TauCand_hemEmin_p4) {result.push_back(p.E ());} return result;")
               .Define("TauCand_hemEmin_m",   "ROOT::VecOps::RVec<float> result; for (auto & p: TauCand_hemEmin_p4) {result.push_back(p.M ());} return result;")
               .Define("mDiTau_Vis",          "if (EVT_ThrustEmin_NTau23PiCand>1) return (TauCand_hemEmin_p4.at(0)+TauCand_hemEmin_p4.at(1)).M(); else return (-9999.9);")

               .Define("TauCand_hemEmin_pion1px",   "Tau23PiCandidates_pion1px [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion1py",   "Tau23PiCandidates_pion1py [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion1pz",   "Tau23PiCandidates_pion1pz [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion1q",    "Tau23PiCandidates_pion1q  [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion1d0",   "Tau23PiCandidates_pion1d0 [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion1z0",   "Tau23PiCandidates_pion1z0 [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion2px",   "Tau23PiCandidates_pion2px [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion2py",   "Tau23PiCandidates_pion2py [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion2pz",   "Tau23PiCandidates_pion2pz [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion2q",    "Tau23PiCandidates_pion2q  [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion2d0",   "Tau23PiCandidates_pion2d0 [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion2z0",   "Tau23PiCandidates_pion2z0 [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion3px",   "Tau23PiCandidates_pion3px [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion3py",   "Tau23PiCandidates_pion3py [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion3pz",   "Tau23PiCandidates_pion3pz [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion3q",    "Tau23PiCandidates_pion3q  [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion3d0",   "Tau23PiCandidates_pion3d0 [Tau23PiCandidates_hemEmin>0]")
               .Define("TauCand_hemEmin_pion3z0",   "Tau23PiCandidates_pion3z0 [Tau23PiCandidates_hemEmin>0]")


               .Define("TauCand1_x",           "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_x.          at(0); else return (float(+999.9) );")
               .Define("TauCand1_y",           "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_y.          at(0); else return (float(+999.9) );")
               .Define("TauCand1_z",           "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_z.          at(0); else return (float(+999.9) );")
               .Define("TauCand1_chi2",        "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_chi2.       at(0); else return (float(+999.9) );")
               .Define("TauCand1_thrustangle", "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_thrustangle.at(0); else return (float(+999.9) );")
               .Define("TauCand2_x",           "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_x.          at(1); else return (float(-999.9) );")
               .Define("TauCand2_y",           "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_y.          at(1); else return (float(-999.9) );")
               .Define("TauCand2_z",           "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_z.          at(1); else return (float(-999.9) );")
               .Define("TauCand2_chi2",        "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_chi2.       at(1); else return (float(-999.9) );")
               .Define("TauCand2_thrustangle", "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_thrustangle.at(1); else return (float(-999.9) );")

               .Define("TauCand1_px",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_px.at(0); else return (float(+999.9) );")
               .Define("TauCand1_py",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_py.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pz",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pz.at(0); else return (float(+999.9) );")
               .Define("TauCand1_p",    "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_p. at(0); else return (float(+999.9) );")
               .Define("TauCand1_m",    "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_m. at(0); else return (float(+999.9) );")
               .Define("TauCand1_q",    "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_q. at(0); else return (0             );")
               .Define("TauCand2_px",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_px.at(1); else return (float(-999.9) );")
               .Define("TauCand2_py",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_py.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pz",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pz.at(1); else return (float(-999.9) );")
               .Define("TauCand2_p",    "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_p. at(1); else return (float(-999.9) );")
               .Define("TauCand2_m",    "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_m. at(1); else return (float(-999.9) );")
               .Define("TauCand2_q",    "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_q. at(1); else return (0             );")

               .Define("TauCand1_pion1px",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion1px.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion1py",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion1py.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion1pz",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion1pz.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion1q",    "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion1q. at(0); else return (0             );")
               .Define("TauCand1_pion1d0",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion1d0.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion1z0",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion1z0.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion2px",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion2px.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion2py",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion2py.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion2pz",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion2pz.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion2q",    "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion2q. at(0); else return (0             );")
               .Define("TauCand1_pion2d0",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion2d0.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion2z0",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion2z0.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion3px",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion3px.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion3py",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion3py.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion3pz",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion3pz.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion3q",    "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion3q. at(0); else return (0             );")
               .Define("TauCand1_pion3d0",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion3d0.at(0); else return (float(+999.9) );")
               .Define("TauCand1_pion3z0",   "if (EVT_ThrustEmin_NTau23PiCand>0) return TauCand_hemEmin_pion3z0.at(0); else return (float(+999.9) );")

               .Define("TauCand2_pion1px",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion1px.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion1py",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion1py.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion1pz",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion1pz.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion1q",    "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion1q. at(1); else return (0             );")
               .Define("TauCand2_pion1d0",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion1d0.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion1z0",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion1z0.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion2px",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion2px.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion2py",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion2py.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion2pz",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion2pz.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion2q",    "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion2q. at(1); else return (0             );")
               .Define("TauCand2_pion2d0",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion2d0.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion2z0",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion2z0.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion3px",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion3px.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion3py",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion3py.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion3pz",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion3pz.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion3q",    "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion3q. at(1); else return (0             );")
               .Define("TauCand2_pion3d0",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion3d0.at(1); else return (float(-999.9) );")
               .Define("TauCand2_pion3z0",   "if (EVT_ThrustEmin_NTau23PiCand>1) return TauCand_hemEmin_pion3z0.at(1); else return (float(-999.9) );")

               .Define("ratio_Emiss",  "(recoEmiss_px * TauCand1_px + recoEmiss_py * TauCand1_py + recoEmiss_pz * TauCand1_pz) / (recoEmiss_p4.P() * TauCand1_p)")
               .Define("mDiTau_full",  "if (EVT_ThrustEmin_NTau23PiCand>1) return (TauCand_hemEmin_p4.at(0)+TauCand_hemEmin_p4.at(1)+ratio_Emiss*recoEmiss_p4).M(); else return (-9999.9);")


               .Define("T1xT2_x",    "TauCand1_py*TauCand2_pz-TauCand1_pz*TauCand2_py")
               .Define("T1xT2_y",    "TauCand1_pz*TauCand2_px-TauCand1_px*TauCand2_pz")
               .Define("T1xT2_z",    "TauCand1_px*TauCand2_py-TauCand1_py*TauCand2_px")
               .Define("T1xEm_x",    "TauCand1_py*recoEmiss_pz-TauCand1_pz*recoEmiss_py")
               .Define("T1xEm_y",    "TauCand1_pz*recoEmiss_px-TauCand1_px*recoEmiss_pz")
               .Define("T1xEm_z",    "TauCand1_px*recoEmiss_py-TauCand1_py*recoEmiss_px")
               .Define("EmxT2_x",    "recoEmiss_py*TauCand2_pz-recoEmiss_pz*TauCand2_py")
               .Define("EmxT2_y",    "recoEmiss_pz*TauCand2_px-recoEmiss_px*TauCand2_pz")
               .Define("EmxT2_z",    "recoEmiss_px*TauCand2_py-recoEmiss_py*TauCand2_px")

               .Define("T1xT2_M2",   "T1xT2_x * T1xT2_x + T1xT2_y * T1xT2_y + T1xT2_z * T1xT2_z")
               .Define("denom",      "(T1xT2_x + EmxT2_x)*(T1xT2_x + T1xEm_x) + (T1xT2_y + EmxT2_y)*(T1xT2_y + T1xEm_y) + (T1xT2_z + EmxT2_z)*(T1xT2_z + T1xEm_z)")

               .Define("mDiTau_collinear3D",    "mDiTau_Vis/sqrt(T1xT2_M2/denom)") 


           )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                "MC_PDG","MC_M1","MC_M2","MC_n","MC_D1","MC_D2",

                "n_genBottoms",
                "genBottom_px", "genBottom_py", "genBottom_pz", "genBottom_eta", "genBottom_phi",
                "genBottom_energy", "genBottom_mass", "genBottom_pdg",
                "genBottom_thrustangle",

                "n_genBs",
                "genBs_px", "genBs_py", "genBs_pz", "genBs_eta", "genBs_phi",
                "genBs_energy", "genBs_mass", "genBs_pdg",
                "genBs_thrustangle",

                "genBs_Vertex_x", "genBs_Vertex_y", "genBs_Vertex_z",
                "genBs_Vertex_thrustangle",

                "EVT_ThrustEmin_E",            "EVT_ThrustEmax_E",
                "EVT_ThrustEmin_Echarged",     "EVT_ThrustEmax_Echarged",
                "EVT_ThrustEmin_Eneutral",     "EVT_ThrustEmax_Eneutral",
                "EVT_ThrustEmin_N",            "EVT_ThrustEmax_N",
                "EVT_ThrustEmin_Ncharged",     "EVT_ThrustEmax_Ncharged",
                "EVT_ThrustEmin_Nneutral",     "EVT_ThrustEmax_Nneutral",
                "EVT_ThrustEmin_NDV",          "EVT_ThrustEmax_NDV",
                "EVT_ThrustEmin_NTau23PiCand", "EVT_ThrustEmax_NTau23PiCand",
                "EVT_Thrust_Mag",
                "EVT_Thrust_X",  "EVT_Thrust_XErr",
                "EVT_Thrust_Y",  "EVT_Thrust_YErr",
                "EVT_Thrust_Z",  "EVT_Thrust_ZErr",

                "EVT_NtracksPV", "EVT_NVertex", "EVT_NTau23Pi",

                "EVT_dPV2DVmin","EVT_dPV2DVmax","EVT_dPV2DVave",

                "MC_Vertex_x", "MC_Vertex_y", "MC_Vertex_z",
                "MC_Vertex_ntrk", "MC_Vertex_n",

                "MC_Vertex_PDG","MC_Vertex_PDGmother","MC_Vertex_PDGgmother",

                "Vertex_x", "Vertex_y", "Vertex_z",
                "Vertex_xErr", "Vertex_yErr", "Vertex_zErr",
                "Vertex_isPV", "Vertex_ntrk", "Vertex_chi2", "Vertex_n",
                "Vertex_thrust_angle", "Vertex_thrusthemis_emin", "Vertex_thrusthemis_emax",

                "Vertex_d2PV", "Vertex_d2PVx", "Vertex_d2PVy", "Vertex_d2PVz",
                "Vertex_d2PVErr", "Vertex_d2PVxErr", "Vertex_d2PVyErr", "Vertex_d2PVzErr",
                "Vertex_mass",
                "DV_d0","DV_z0",

                "EVT_MVA1",

                "recoEmiss_px", "recoEmiss_py", "recoEmiss_pz", "recoEmiss_e", "recoEmiss_m",
                "recoEmiss_thrustangle",

                "Tau23PiCandidates_mass", "Tau23PiCandidates_vertex", "Tau23PiCandidates_mcvertex", "Tau23PiCandidates_B",
                "Tau23PiCandidates_px", "Tau23PiCandidates_py", "Tau23PiCandidates_pz", "Tau23PiCandidates_p", "Tau23PiCandidates_q",
                "Tau23PiCandidates_d0",  "Tau23PiCandidates_z0","Tau23PiCandidates_anglethrust",

                "Tau23PiCandidates_x",    "Tau23PiCandidates_y",    "Tau23PiCandidates_z",
                "Tau23PiCandidates_xErr", "Tau23PiCandidates_yErr", "Tau23PiCandidates_zErr",
                "Tau23PiCandidates_chi2", "Tau23PiCandidates_hemEmin",

                "Tau23PiCandidates_rho1px", "Tau23PiCandidates_rho1py", "Tau23PiCandidates_rho1pz","Tau23PiCandidates_rho1mass",
                "Tau23PiCandidates_rho2px", "Tau23PiCandidates_rho2py", "Tau23PiCandidates_rho2pz","Tau23PiCandidates_rho2mass",

                "Tau23PiCandidates_pion1px", "Tau23PiCandidates_pion1py", "Tau23PiCandidates_pion1pz",
                "Tau23PiCandidates_pion1p", "Tau23PiCandidates_pion1q", "Tau23PiCandidates_pion1d0", "Tau23PiCandidates_pion1z0",
                "Tau23PiCandidates_pion2px", "Tau23PiCandidates_pion2py", "Tau23PiCandidates_pion2pz",
                "Tau23PiCandidates_pion2p", "Tau23PiCandidates_pion2q", "Tau23PiCandidates_pion2d0", "Tau23PiCandidates_pion2z0",
                "Tau23PiCandidates_pion3px", "Tau23PiCandidates_pion3py", "Tau23PiCandidates_pion3pz",
                "Tau23PiCandidates_pion3p", "Tau23PiCandidates_pion3q", "Tau23PiCandidates_pion3d0", "Tau23PiCandidates_pion3z0",
              
                "TauCand1_x",  "TauCand1_y",  "TauCand1_z", "TauCand1_chi2", "TauCand1_thrustangle",
                "TauCand2_x",  "TauCand2_y",  "TauCand2_z", "TauCand2_chi2", "TauCand2_thrustangle",
                "TauCand1_px", "TauCand1_py", "TauCand1_pz", "TauCand1_p", "TauCand1_m", "TauCand1_q",
                "TauCand2_px", "TauCand2_py", "TauCand2_pz", "TauCand2_p", "TauCand2_m", "TauCand2_q",

                "TauCand1_pion1px", "TauCand1_pion1py", "TauCand1_pion1pz", "TauCand1_pion1q", "TauCand1_pion1d0", "TauCand1_pion1z0",
                "TauCand1_pion2px", "TauCand1_pion2py", "TauCand1_pion2pz", "TauCand1_pion2q", "TauCand1_pion2d0", "TauCand1_pion2z0",
                "TauCand1_pion3px", "TauCand1_pion3py", "TauCand1_pion3pz", "TauCand1_pion3q", "TauCand1_pion3d0", "TauCand1_pion3z0",
                "TauCand2_pion1px", "TauCand2_pion1py", "TauCand2_pion1pz", "TauCand2_pion1q", "TauCand2_pion1d0", "TauCand2_pion1z0",
                "TauCand2_pion2px", "TauCand2_pion2py", "TauCand2_pion2pz", "TauCand2_pion2q", "TauCand2_pion2d0", "TauCand2_pion2z0",
                "TauCand2_pion3px", "TauCand2_pion3py", "TauCand2_pion3pz", "TauCand2_pion3q", "TauCand2_pion3d0", "TauCand2_pion3z0",

                "mDiTau_Vis", "mDiTau_collinear3D",

                #"T1xT2_x", "T1xT2_y", "T1xT2_z",
                #"T1xEm_x", "T1xEm_y", "T1xEm_z",
                #"EmxT2_x", "EmxT2_y", "EmxT2_z",
                #"T1xT2_M2", "denom",

                "ratio_Emiss", "mDiTau_full",

                ]
        return branchList
