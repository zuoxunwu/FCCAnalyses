
#analysis_extra
processList_analysis = {
    'p8_ee_Zbb_ecm91':{'chunks':50},
    'p8_ee_Zcc_ecm91':{'chunks':50},
    'p8_ee_Zuds_ecm91':{'chunks':50}

    }
prodTag_analysis     = "FCCee/spring2021/IDEA/"
outputDirEos_analysis   = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2021/prod_04/analysis_extra_bkg_composition/"


processList  = processList_analysis
outputDirEos = outputDirEos_analysis
prodTag      = prodTag_analysis
MVAFilter    = "EVT_MVA1>0.6"
MVA2Filter   = "EVT_MVA2_bu>0.6||EVT_MVA2_bc>0.6"

outputDir   = ""
nCPUS       = 8
runBatch    = True
batchQueue  = "workday"
compGroup   = "group_u_FCC.local_gen"

import ROOT
ROOT.gInterpreter.ProcessLine('''
TMVA::Experimental::RBDT<> bdt2("BuBc_BDT2", "/afs/cern.ch/work/x/xzuo/public/FCC_files/BuBc2TauNu/data/ROOT/xgb_bdt_stage2_Bu_vs_Bc_vs_qq_multi.root");
computeModel = TMVA::Experimental::Compute<21, float>(bdt2);

TMVA::Experimental::RBDT<> bdt1("BuBc_BDT", "/afs/cern.ch/work/x/xzuo/public/FCC_files/BuBc2TauNu/data/ROOT/xgb_bdt_BuBc_vtx.root");
computeModel1 = TMVA::Experimental::Compute<18, float>(bdt1);
''')

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
               .Define("MC_PDG",   "FCCAnalyses::MCParticle::get_pdg(Particle)")
               .Define("MC_n",     "int(MC_PDG.size())")
               .Define("MC_M1",    "myUtils::get_MCMother1(Particle,Particle0)")
               .Define("MC_M2",    "myUtils::get_MCMother2(Particle,Particle0)")
               .Define("MC_D1",    "myUtils::get_MCDaughter1(Particle,Particle1)")
               .Define("MC_D2",    "myUtils::get_MCDaughter2(Particle,Particle1)")
               .Define("MC_px",    "FCCAnalyses::MCParticle::get_px(Particle)")
               .Define("MC_py",    "FCCAnalyses::MCParticle::get_py(Particle)")
               .Define("MC_pz",    "FCCAnalyses::MCParticle::get_pz(Particle)")
               .Define("MC_mass",  "FCCAnalyses::MCParticle::get_mass(Particle)")
               .Define("MC_fromvert_x", "FCCAnalyses::MCParticle::get_vertex_x(Particle)")
               .Define("MC_fromvert_y", "FCCAnalyses::MCParticle::get_vertex_y(Particle)")
               .Define("MC_fromvert_z", "FCCAnalyses::MCParticle::get_vertex_z(Particle)")

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
               .Filter("EVT_NTau23Pi>0")


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
               .Define("EVT_thrust",        'Algorithms::getThrustPointing(RP_thrustangleNP, RP_e, EVT_thrustNP, 1.)')
               .Define("RP_thrustangle",    'Algorithms::getAxisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')


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

               .Define("EVT_Thrust_X",    "EVT_thrust.at(1)")
               .Define("EVT_Thrust_XErr", "EVT_thrust.at(2)")
               .Define("EVT_Thrust_Y",    "EVT_thrust.at(3)")
               .Define("EVT_Thrust_YErr", "EVT_thrust.at(4)")
               .Define("EVT_Thrust_Z",    "EVT_thrust.at(5)")
               .Define("EVT_Thrust_ZErr", "EVT_thrust.at(6)")


               ######################################################
               ### save which hemisphere gen particles belong to  ###
               ######################################################
               .Define("MC_p_thrust_angle",    "FCCAnalyses::Algorithms::getAxisCosTheta(EVT_thrust, MC_px, MC_py, MC_pz)")
               .Define("MC_vert_thrust_angle", "FCCAnalyses::Algorithms::getAxisCosTheta(EVT_thrust, MC_fromvert_x, MC_fromvert_y, MC_fromvertz)")

               .Define("DV_tracks", "myUtils::get_pseudotrack(VertexObject,RecoPartPIDAtVertex)")

               .Define("DV_d0",            "myUtils::get_trackd0(DV_tracks)")
               .Define("DV_z0",            "myUtils::get_trackz0(DV_tracks)")

               ###Build MVA with only thrust info
               .Define("MVAVec1", ROOT.computeModel1, ("EVT_ThrustEmin_E",        "EVT_ThrustEmax_E",
                                                     "EVT_ThrustEmin_Echarged", "EVT_ThrustEmax_Echarged",
                                                     "EVT_ThrustEmin_Eneutral", "EVT_ThrustEmax_Eneutral",
                                                     "EVT_ThrustEmin_Ncharged", "EVT_ThrustEmax_Ncharged",
                                                     "EVT_ThrustEmin_Nneutral", "EVT_ThrustEmax_Nneutral",
                                                     "EVT_NtracksPV",           "EVT_NVertex",
                                                     "EVT_NTau23Pi",            "EVT_ThrustEmin_NDV",
                                                     "EVT_ThrustEmax_NDV",      "EVT_dPV2DVmin",
                                                     "EVT_dPV2DVmax",           "EVT_dPV2DVave"))
               .Define("EVT_MVA1", "MVAVec1.at(0)")
               .Filter(MVAFilter)

               .Define("Tau23PiCandidates_mass",    "myUtils::getFCCAnalysesComposite_mass(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_q",       "myUtils::getFCCAnalysesComposite_charge(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_vertex",  "myUtils::getFCCAnalysesComposite_vertex(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_mcvertex","myUtils::getFCCAnalysesComposite_mcvertex(Tau23PiCandidates,VertexObject)")
               .Define("Tau23PiCandidates_px",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,0)")
               .Define("Tau23PiCandidates_py",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,1)")
               .Define("Tau23PiCandidates_pz",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,2)")
               .Define("Tau23PiCandidates_p",       "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,-1)")

               .Define("Tau23PiCandidates_track",   "myUtils::getFCCAnalysesComposite_track(Tau23PiCandidates, VertexObject)")
               .Define("Tau23PiCandidates_d0",      "myUtils::get_trackd0(Tau23PiCandidates_track)")
               .Define("Tau23PiCandidates_z0",      "myUtils::get_trackz0(Tau23PiCandidates_track)")

               .Define("Tau23PiCandidates_anglethrust", "myUtils::getFCCAnalysesComposite_anglethrust(Tau23PiCandidates, EVT_thrust)")
               .Define("CUT_hasCandEmin",           "myUtils::has_anglethrust_emin(Tau23PiCandidates_anglethrust)")
               .Filter("CUT_hasCandEmin>0")

               .Define("Tau23PiCandidates_rho",     "myUtils::build_rho(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex)")
               .Define("Tau23PiCandidates_rho1mass","myUtils::get_mass(Tau23PiCandidates_rho, 0)")
               .Define("Tau23PiCandidates_rho2mass","myUtils::get_mass(Tau23PiCandidates_rho, 1)")

               .Define("TrueTau23PiBc_vertex",        "myUtils::get_trueVertex(MCVertexObject,Particle,Particle0, 15, 541)")
               .Define("TrueTau23PiBc_track",         "myUtils::get_truetrack(TrueTau23PiBc_vertex, MCVertexObject, Particle)")
               .Define("TrueTau23PiBc_d0",            "myUtils::get_trackd0(TrueTau23PiBc_track)")
               .Define("TrueTau23PiBc_z0",            "myUtils::get_trackz0(TrueTau23PiBc_track)")

               .Define("TrueTau23PiBu_vertex",        "myUtils::get_trueVertex(MCVertexObject,Particle,Particle0, 15, 521)")


               .Define("CUT_CandInd",     "myFinalSel::selTauCand(Tau23PiCandidates_mass, Tau23PiCandidates_vertex, Vertex_chi2 )")
               .Filter("CUT_CandInd>-1")

               .Define("CUT_CandTruth",   "myFinalSel::selTauCandTM(Tau23PiCandidates_mcvertex, TrueTau23PiBc_vertex, CUT_CandInd)")
               .Define("CUT_CandTruth2",   "myFinalSel::selTauCandTM(Tau23PiCandidates_mcvertex, TrueTau23PiBu_vertex, CUT_CandInd)")

               .Define("CUT_CandRho",      "if ((Tau23PiCandidates_rho1mass.at(CUT_CandInd)<1. && Tau23PiCandidates_rho2mass.at(CUT_CandInd)>0.6 && Tau23PiCandidates_rho2mass.at(CUT_CandInd)<1.0)|| (Tau23PiCandidates_rho2mass.at(CUT_CandInd)<1. && Tau23PiCandidates_rho1mass.at(CUT_CandInd)>0.6 && Tau23PiCandidates_rho1mass.at(CUT_CandInd)<1.)) return 1; else return 0;")
               .Filter("CUT_CandRho>0")

               .Define("EVT_CandMass",     "Tau23PiCandidates_mass.at(CUT_CandInd)")
               .Filter("EVT_CandMass<1.8")

               .Define("LOCAL_CandVtxInd", "Tau23PiCandidates_vertex.at(CUT_CandInd)")
               ##LOCAL INDEX screwed up in prod02!!!! need -1 because PV is removed
               .Define("CUT_CandVtxThrustEmin", "Vertex_thrusthemis_emin.at(LOCAL_CandVtxInd)")
               .Filter("CUT_CandVtxThrustEmin>0")

               .Define("EVT_CandN",           "float(Tau23PiCandidates_vertex.size())")
               .Define("EVT_CandPx",          "Tau23PiCandidates_px.at(CUT_CandInd)")
               .Define("EVT_CandPy",          "Tau23PiCandidates_py.at(CUT_CandInd)")
               .Define("EVT_CandPz",          "Tau23PiCandidates_pz.at(CUT_CandInd)")
               .Define("EVT_CandP",           "Tau23PiCandidates_p.at(CUT_CandInd)")
               .Define("EVT_CandD0",          "Tau23PiCandidates_d0.at(CUT_CandInd)")
               .Define("EVT_CandZ0",          "Tau23PiCandidates_z0.at(CUT_CandInd)")
               .Define("EVT_CandAngleThrust", "Tau23PiCandidates_anglethrust.at(CUT_CandInd)")

               .Define("EVT_CandRho1Mass", "Tau23PiCandidates_rho1mass.at(CUT_CandInd)" )
               .Define("EVT_CandRho2Mass", "Tau23PiCandidates_rho2mass.at(CUT_CandInd)")

               .Define("EVT_CandVtxFD",    "Vertex_d2PV.at(LOCAL_CandVtxInd)")
               .Define("EVT_CandVtxFDErr", "Vertex_d2PVErr.at(LOCAL_CandVtxInd)")
               .Define("EVT_CandVtxChi2",  "Vertex_chi2.at(LOCAL_CandVtxInd)")

               .Define("EVT_Nominal_B_E", "float(91.1876 - EVT_ThrustEmin_E - EVT_ThrustEmax_E + sqrt(EVT_CandP*EVT_CandP + EVT_CandMass*EVT_CandMass))")
               .Define("EVT_DVd0_min", "myFinalSel::get_min(DV_d0, EVT_CandD0)")
               .Define("EVT_DVd0_max", "myFinalSel::get_max(DV_d0, EVT_CandD0)")
               .Define("EVT_DVd0_ave", "myFinalSel::get_ave(DV_d0, EVT_CandD0)")

               .Define("EVT_DVz0_min", "myFinalSel::get_min(DV_z0, EVT_CandZ0)")
               .Define("EVT_DVz0_max", "myFinalSel::get_max(DV_z0, EVT_CandZ0)")
               .Define("EVT_DVz0_ave", "myFinalSel::get_ave(DV_z0, EVT_CandZ0)")

               .Define("EVT_PVmass", "Vertex_mass.at(0)")

               .Define("MVAVec", ROOT.computeModel, ("EVT_CandMass",        "EVT_CandRho1Mass", "EVT_CandRho2Mass",
                                                     "EVT_CandN",           "EVT_CandVtxFD",    "EVT_CandVtxChi2",
                                                     "EVT_CandPx",          "EVT_CandPy",       "EVT_CandPz",
                                                     "EVT_CandP",           "EVT_CandD0",       "EVT_CandZ0",
                                                     "EVT_CandAngleThrust", "EVT_DVd0_min",     "EVT_DVd0_max",
                                                     "EVT_DVd0_ave",        "EVT_DVz0_min",     "EVT_DVz0_max",
                                                     "EVT_DVz0_ave",        "EVT_PVmass",       "EVT_Nominal_B_E"))


               .Define("EVT_MVA2_bkg", "MVAVec.at(0)")
               .Define("EVT_MVA2_bu", "MVAVec.at(1)")
               .Define("EVT_MVA2_bc", "MVAVec.at(2)")

               .Filter(MVA2Filter)
           )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                "MC_PDG","MC_M1","MC_M2","MC_n","MC_D1","MC_D2",
                "MC_px", "MC_py", "MC_pz", "MC_mass", 
                "MC_fromvert_x", "MC_fromvert_y", "MC_fromvert_z",
                "MC_p_thrust_angle", "MC_vert_thrust_angle",

                "EVT_ThrustEmin_E",          "EVT_ThrustEmax_E",
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
                "Vertex_mass",
                "EVT_MVA1", "EVT_MVA2_bkg", "EVT_MVA2_bu", "EVT_MVA2_bc"
                ]
        return branchList
