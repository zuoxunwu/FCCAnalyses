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

processList_test = {
    'p8_ee_Zbb_ecm91_EvtGen_Bs2TauTauTAUHADNU':{'chunks':1, 'fraction':0.001},
}

nCPUS       = 8
runBatch    = False
batchQueue  = "workday"
compGroup   = "group_u_FCC.local_gen"

processList  = processList_full
if not runBatch:
    processList  = processList_test

# tag for MC production campaign
prodTag     = "FCCee/winter2023/IDEA/"

# if runBatch = True, save output on eos
outputDirEos   = "/eos/experiment/fcc/ee/analyses_storage/flavor/Bs2TauTau/flatNtuples/winter2023/analysis_stage1/"

# if runBatch = False, save output locally
outputDir   = "outputs/FCCee/flavor/Bs2TauTau/analysis_stage1/"




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
               .Define("EVT_thrust",        'Algorithms::getThrustPointing(1.)(RP_thrustangleNP, RP_e, EVT_thrustNP)')
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



               .Define("Tau23PiCandidates_mass",    "myUtils::getFCCAnalysesComposite_mass(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_q",       "myUtils::getFCCAnalysesComposite_charge(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_vertex",  "myUtils::getFCCAnalysesComposite_vertex(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_mcvertex","myUtils::getFCCAnalysesComposite_mcvertex(Tau23PiCandidates,VertexObject)")
               .Define("Tau23PiCandidates_px",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,0)")
               .Define("Tau23PiCandidates_py",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,1)")
               .Define("Tau23PiCandidates_pz",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,2)")
               .Define("Tau23PiCandidates_p",       "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,-1)")
               .Define("Tau23PiCandidates_B",       "myUtils::getFCCAnalysesComposite_B(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex)")

               .Define("Tau23PiCandidates_track",   "myUtils::getFCCAnalysesComposite_track(Tau23PiCandidates, VertexObject)")
               .Define("Tau23PiCandidates_d0",      "myUtils::get_trackd0(Tau23PiCandidates_track)")
               .Define("Tau23PiCandidates_z0",      "myUtils::get_trackz0(Tau23PiCandidates_track)")

               .Define("Tau23PiCandidates_anglethrust", "myUtils::getFCCAnalysesComposite_anglethrust(Tau23PiCandidates, EVT_thrust)")
               .Define("EVT_ThrustEmin_NTau23PiCand",   "float(myUtils::get_Npos(cos(Tau23PiCandidates_anglethrust)))")
               .Define("EVT_ThrustEmax_NTau23PiCand",   "float(myUtils::get_Nneg(cos(Tau23PiCandidates_anglethrust)))")

               .Define("CUT_hasCandEmin",           "myUtils::has_anglethrust_emin(Tau23PiCandidates_anglethrust)")
               .Filter("CUT_hasCandEmin>0")

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

           )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                "MC_PDG","MC_M1","MC_M2","MC_n","MC_D1","MC_D2",

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

                "Tau23PiCandidates_mass", "Tau23PiCandidates_vertex", "Tau23PiCandidates_mcvertex", "Tau23PiCandidates_B",
                "Tau23PiCandidates_px", "Tau23PiCandidates_py", "Tau23PiCandidates_pz", "Tau23PiCandidates_p", "Tau23PiCandidates_q",
                "Tau23PiCandidates_d0",  "Tau23PiCandidates_z0","Tau23PiCandidates_anglethrust",

                "Tau23PiCandidates_rho1px", "Tau23PiCandidates_rho1py", "Tau23PiCandidates_rho1pz","Tau23PiCandidates_rho1mass",
                "Tau23PiCandidates_rho2px", "Tau23PiCandidates_rho2py", "Tau23PiCandidates_rho2pz","Tau23PiCandidates_rho2mass",

                "Tau23PiCandidates_pion1px", "Tau23PiCandidates_pion1py", "Tau23PiCandidates_pion1pz",
                "Tau23PiCandidates_pion1p", "Tau23PiCandidates_pion1q", "Tau23PiCandidates_pion1d0", "Tau23PiCandidates_pion1z0",
                "Tau23PiCandidates_pion2px", "Tau23PiCandidates_pion2py", "Tau23PiCandidates_pion2pz",
                "Tau23PiCandidates_pion2p", "Tau23PiCandidates_pion2q", "Tau23PiCandidates_pion2d0", "Tau23PiCandidates_pion2z0",
                "Tau23PiCandidates_pion3px", "Tau23PiCandidates_pion3py", "Tau23PiCandidates_pion3pz",
                "Tau23PiCandidates_pion3p", "Tau23PiCandidates_pion3q", "Tau23PiCandidates_pion3d0", "Tau23PiCandidates_pion3z0",
                ]
        return branchList
