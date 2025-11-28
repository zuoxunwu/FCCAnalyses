#Mandatory: List of processes
processList = {
             'p8_ee_Zss_ecm91':{'chunks':1, 'fraction':0.0000001},
             'p8_ee_Zcc_ecm91':{'chunks':1, 'fraction':0.0000001},
             'p8_ee_Zbb_ecm91':{'chunks':1, 'fraction':0.0000001},
             'p8_ee_Zud_ecm91':{'chunks':1, 'fraction':0.0000001},

            }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/strange/analysis_stage1_1118/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topEWK/flatNtuples/winter2023"


#Optional
nCPUS       = 8
runBatch    = False
batchQueue = "workday"
compGroup = "group_u_FCC.local_gen"

includePaths = ["functions.h"]

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

               
               .Define("genK0",   "FCCAnalyses::MCParticle::sel_pdgID(311, true)(Particle)")
               .Define("genKL",   "FCCAnalyses::MCParticle::sel_pdgID(130, true)(Particle)")
               .Define("genKS",   "FCCAnalyses::MCParticle::sel_pdgID(310, true)(Particle)")
               .Define("genKpos", "FCCAnalyses::MCParticle::sel_pdgID(321, false)(Particle)")
               .Define("genKneg", "FCCAnalyses::MCParticle::sel_pdgID(-321, false)(Particle)")
               .Define("genPhi",    "FCCAnalyses::MCParticle::sel_pdgID(1020, true)(Particle)")
               .Define("genLambda", "FCCAnalyses::MCParticle::sel_pdgID(3122, true)(Particle)")
               .Define("genSigma0", "FCCAnalyses::MCParticle::sel_pdgID(3212, true)(Particle)")
               .Define("genSigmapos", "FCCAnalyses::MCParticle::sel_pdgID(3222, true)(Particle)")
               .Define("genSigmaneg", "FCCAnalyses::MCParticle::sel_pdgID(3112, true)(Particle)")

               .Define("n_genK0s",      "FCCAnalyses::MCParticle::get_n(genK0)")
               .Define("n_genKLs",      "FCCAnalyses::MCParticle::get_n(genKL)")
               .Define("n_genKSs",      "FCCAnalyses::MCParticle::get_n(genKS)")
               .Define("n_genKposs",    "FCCAnalyses::MCParticle::get_n(genKpos)")
               .Define("n_genKnegs",    "FCCAnalyses::MCParticle::get_n(genKneg)")
               .Define("n_genPhis",     "FCCAnalyses::MCParticle::get_n(genPhi)")
               .Define("n_genLambdas",  "FCCAnalyses::MCParticle::get_n(genLambda)")
               .Define("n_genSigma0s",  "FCCAnalyses::MCParticle::get_n(genSigma0)")
               .Define("n_genSigmaposs",  "FCCAnalyses::MCParticle::get_n(genSigmapos)")
               .Define("n_genSigmanegs",  "FCCAnalyses::MCParticle::get_n(genSigmaneg)")

               .Define("genPipm",       "FCCAnalyses::MCParticle::sel_pdgID(211, true)(Particle)")
               .Define("n_genPipms",    "FCCAnalyses::MCParticle::get_n(genPipm)")

               .Define("genKS_energy",     "FCCAnalyses::MCParticle::get_e   (genKS)")
               .Define("genKpos_energy",   "FCCAnalyses::MCParticle::get_e   (genKpos)")
               .Define("genKneg_energy",   "FCCAnalyses::MCParticle::get_e   (genKneg)")
               .Define("genLambda_energy", "FCCAnalyses::MCParticle::get_e   (genLambda)")
               .Define("genSigma0_energy", "FCCAnalyses::MCParticle::get_e   (genSigma0)")
               .Define("genSigmapos_energy", "FCCAnalyses::MCParticle::get_e   (genSigmapos)")
               .Define("genSigmaneg_energy", "FCCAnalyses::MCParticle::get_e   (genSigmaneg)")




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
               .Define("MC_Vertex_mass",  "FCCAnalyses::ZHfunctions::get_MC_Vertex_mass(MCVertexObject, Particle)")
               .Define("MC_Vertex_p",     "FCCAnalyses::ZHfunctions::get_MC_Vertex_p(MCVertexObject, Particle)")
               .Define("MC_Vertex_pt",    "FCCAnalyses::ZHfunctions::get_MC_Vertex_pt(MCVertexObject, Particle)")


                ############################################
                ##           single out Bs vertices       ##
                ############################################

               .Define("MC_Vertex_isKSpipi",   "ROOT::VecOps::RVec<int> result; for (size_t i=0; i < MC_Vertex_PDGmother.size(); ++i) {int isKS=0; for (size_t j=0; j < MC_Vertex_PDGmother[i].size(); ++j) {if (abs(MC_Vertex_PDGmother[i][j])==310) isKS+=10;} for (size_t j=0; j < MC_Vertex_PDG[i].size(); ++j) {if (abs(MC_Vertex_PDG[i][j])==211) isKS+=1;} result.push_back(isKS);} return result;")
               .Define("MC_Vertex_isLambda",   "ROOT::VecOps::RVec<int> result; for (size_t i=0; i < MC_Vertex_PDGmother.size(); ++i) {int isLm=0; for (size_t j=0; j < MC_Vertex_PDGmother[i].size(); ++j) {if (abs(MC_Vertex_PDGmother[i][j])==3122) isLm+=10;} for (size_t j=0; j < MC_Vertex_PDG[i].size(); ++j) {if (abs(MC_Vertex_PDG[i][j])==211) isLm+=1; if (abs(MC_Vertex_PDG[i][j])==2212) isLm+=1;} result.push_back(isLm);} return result;")

               .Define("MC_Vertex_KSflag", "1.0*(MC_Vertex_isKSpipi > 10 && MC_Vertex_isKSpipi % 10 !=0)")
               .Define("MC_Vertex_Lmflag", "1.0*(MC_Vertex_isLambda > 10 && MC_Vertex_isLambda % 10 !=0)")
               .Define("genKS_Vertex_x",   "MC_Vertex_x  [MC_Vertex_KSflag>0]") #find Bs meson
               .Define("genKS_Vertex_y",   "MC_Vertex_y  [MC_Vertex_KSflag>0]") #no implementation of abs() for vector
               .Define("genKS_Vertex_z",   "MC_Vertex_z  [MC_Vertex_KSflag>0]")
               .Define("genKS_Vertex_p",   "MC_Vertex_p  [MC_Vertex_KSflag>0]")
               .Define("genKS_Vertex_pt",  "MC_Vertex_pt [MC_Vertex_KSflag>0]")
               .Define("genKS_Vertex_r",   "sqrt(genKS_Vertex_x*genKS_Vertex_x + genKS_Vertex_y*genKS_Vertex_y)")
               .Define("genKS_Vertex_d",   "sqrt(genKS_Vertex_x*genKS_Vertex_x + genKS_Vertex_y*genKS_Vertex_y + genKS_Vertex_z*genKS_Vertex_z)")

               .Define("genLm_Vertex_x",   "MC_Vertex_x  [MC_Vertex_Lmflag>0]") #find Bs meson
               .Define("genLm_Vertex_y",   "MC_Vertex_y  [MC_Vertex_Lmflag>0]") #no implementation of abs() for vector
               .Define("genLm_Vertex_z",   "MC_Vertex_z  [MC_Vertex_Lmflag>0]")
               .Define("genLm_Vertex_p",   "MC_Vertex_p  [MC_Vertex_Lmflag>0]")
               .Define("genLm_Vertex_pt",  "MC_Vertex_pt [MC_Vertex_Lmflag>0]")
               .Define("genLm_Vertex_r",   "sqrt(genLm_Vertex_x*genLm_Vertex_x + genLm_Vertex_y*genLm_Vertex_y)")
               .Define("genLm_Vertex_d",   "sqrt(genLm_Vertex_x*genLm_Vertex_x + genLm_Vertex_y*genLm_Vertex_y + genLm_Vertex_z*genLm_Vertex_z)")

               #############################################
               ##              Build Reco Vertex          ##
               #############################################
               .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject,ReconstructedParticles,EFlowTrack_1,MCRecoAssociations0,MCRecoAssociations1)")

               #############################################
               ##          Build PV var and filter        ##
               #############################################
               .Define("EVT_NVertex",   "float(VertexObject.size())")

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
               .Define("Vertex_pt",       "FCCAnalyses::ZHfunctions::get_Vertex_pt(VertexObject,RecoPartPIDAtVertex)")
               .Define("Vertex_eta",      "FCCAnalyses::ZHfunctions::get_Vertex_eta(VertexObject,RecoPartPIDAtVertex)")

               .Define("Vertex_MCx",      "ROOT::VecOps::RVec<float> result; for (size_t i=0; i < Vertex_mcind.size(); ++i) result.push_back(MC_Vertex_x.at(Vertex_mcind[i])); return result;")
               .Define("Vertex_MCy",      "ROOT::VecOps::RVec<float> result; for (size_t i=0; i < Vertex_mcind.size(); ++i) result.push_back(MC_Vertex_y.at(Vertex_mcind[i])); return result;")
               .Define("Vertex_MCz",      "ROOT::VecOps::RVec<float> result; for (size_t i=0; i < Vertex_mcind.size(); ++i) result.push_back(MC_Vertex_z.at(Vertex_mcind[i])); return result;")
               .Define("Vertex_MCd",      "sqrt( (Vertex_MCx-Vertex_x)*(Vertex_MCx-Vertex_x) + (Vertex_MCy-Vertex_y)*(Vertex_MCy-Vertex_y) + (Vertex_MCz-Vertex_z)*(Vertex_MCz-Vertex_z)   )")
               .Define("Vertex_isMCKSpipi",   "ROOT::VecOps::RVec<int> result; for (size_t i=0; i < Vertex_mcind.size(); ++i) {int isKS=0; for (size_t j=0; j < MC_Vertex_PDGmother[Vertex_mcind[i]].size(); ++j) {if (abs(MC_Vertex_PDGmother[i][j])==310) isKS+=10;} for (size_t l=0; l < MC_Vertex_PDG[Vertex_mcind[i]].size(); ++l) {if (abs(MC_Vertex_PDG[i][l])==211) isKS+=1;} result.push_back(isKS);} return result;")
               .Define("Vertex_isMCLambda",   "ROOT::VecOps::RVec<int> result; for (size_t i=0; i < Vertex_mcind.size(); ++i) {int isLm=0; for (size_t j=0; j < MC_Vertex_PDGmother[Vertex_mcind[i]].size(); ++j) {if (abs(MC_Vertex_PDGmother[i][j])==3122) isLm+=10;} for (size_t l=0; l < MC_Vertex_PDG[Vertex_mcind[i]].size(); ++l) {if (abs(MC_Vertex_PDG[i][l])==211) isLm+=1; if (abs(MC_Vertex_PDG[i][l])==2212) isLm+=1;} result.push_back(isLm);} return result;")

               .Define("Vertex_KSmatch",  "1.0*(Vertex_isMCKSpipi > 10 && Vertex_isMCKSpipi % 10 !=0 && Vertex_chi2<10 && Vertex_MCd<2)")
               .Define("Vertex_Lmmatch",  "1.0*(Vertex_isMCLambda > 10 && Vertex_isMCLambda % 10 !=0 && Vertex_chi2<10 && Vertex_MCd<2)")

               ########################################################
               ##   check for mass reso for displaced vertices (KS)  ##
               ########################################################

               .Define("Vertex_rErr", "sqrt(Vertex_xErr*Vertex_xErr + Vertex_yErr*Vertex_yErr)")
               .Define("Vertex_dErr", "sqrt(Vertex_xErr*Vertex_xErr + Vertex_yErr*Vertex_yErr + Vertex_zErr*Vertex_zErr)")

               .Define("Vertex_r", "sqrt(Vertex_x*Vertex_x + Vertex_y*Vertex_y)")
               .Define("Vertex_d", "sqrt(Vertex_x*Vertex_x + Vertex_y*Vertex_y + Vertex_z*Vertex_z)")
               .Define("Vertex_mass_before_VerDet", "Vertex_mass[Vertex_chi2<10 && Vertex_r<13.7]") ## decays before first vertex detector layer
               .Define("Vertex_mass_within_VerDet", "Vertex_mass[Vertex_chi2<10 && Vertex_r>13.7 && Vertex_r<34]") ## decays within vertex detector volume
               .Define("Vertex_mass_within_DC",     "Vertex_mass[Vertex_chi2<10 && Vertex_r>35]")
               .Define("Vertex_mass_super_displaced", "Vertex_mass[Vertex_chi2<10 && Vertex_r>1000]")

               .Define("Vertex_mass_pipi", "Vertex_mass[Vertex_chi2<10 && Vertex_ntrk==2 && Vertex_d>30]")

               .Define("recoKS_Vertex_r", "Vertex_r[Vertex_KSmatch>0]")
               .Define("recoKS_Vertex_z", "Vertex_z[Vertex_KSmatch>0]")
               .Define("recoKS_Vertex_mass", "Vertex_mass[Vertex_KSmatch>0]")
               .Define("recoKS_Vertex_mass_before_VerDet", "Vertex_mass[Vertex_KSmatch>0 && Vertex_r<13.7]")
               .Define("recoKS_Vertex_mass_within_VerDet", "Vertex_mass[Vertex_KSmatch>0 && Vertex_r>13.7 && Vertex_r<34]")
               .Define("recoKS_Vertex_mass_beyond_VerDet", "Vertex_mass[Vertex_KSmatch>0 && Vertex_r>35]")

               .Define("recoLm_Vertex_r", "Vertex_r[Vertex_Lmmatch>0]")
               .Define("recoLm_Vertex_z", "Vertex_z[Vertex_Lmmatch>0]")
               .Define("recoLm_Vertex_mass", "Vertex_mass[Vertex_Lmmatch>0]")
               .Define("recoLm_Vertex_mass_before_VerDet", "Vertex_mass[Vertex_Lmmatch>0 && Vertex_r<13.7]")
               .Define("recoLm_Vertex_mass_within_VerDet", "Vertex_mass[Vertex_Lmmatch>0 && Vertex_r>13.7 && Vertex_r<34]")
               .Define("recoLm_Vertex_mass_beyond_VerDet", "Vertex_mass[Vertex_Lmmatch>0 && Vertex_r>35]")


        )
        return df2




    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "n_genK0s", "n_genKLs", "n_genKSs",
                 "n_genKposs", "n_genKnegs", "n_genPhis", "n_genLambdas",
                 "n_genSigma0s", "n_genSigmaposs", "n_genSigmanegs",
                 "n_genPipms", #"genPiPm_fromKs"
                 "genKS_energy", "genKpos_energy", "genKneg_energy",
                 "genLambda_energy", "genSigma0_energy", "genSigmapos_energy", "genSigmaneg_energy",

                 "genKS_Vertex_x", "genKS_Vertex_y", "genKS_Vertex_z", "genKS_Vertex_r", "genKS_Vertex_d", "genKS_Vertex_p", "genKS_Vertex_pt",
                 "genLm_Vertex_x", "genLm_Vertex_y", "genLm_Vertex_z", "genLm_Vertex_r", "genLm_Vertex_d", "genLm_Vertex_p", "genLm_Vertex_pt",
                 "EVT_NVertex",
                 "MC_Vertex_mass", "MC_Vertex_p",
                 "Vertex_x", "Vertex_y", "Vertex_z", "Vertex_r", "Vertex_d",
                 "Vertex_xErr", "Vertex_yErr", "Vertex_zErr", "Vertex_rErr", "Vertex_dErr", 
                 "Vertex_chi2", "Vertex_isPV", "Vertex_ntrk", "Vertex_mass",
                 "Vertex_n",
                 "Vertex_mass_before_VerDet", "Vertex_mass_within_VerDet", "Vertex_mass_within_DC", "Vertex_mass_super_displaced",
                 "Vertex_mass_pipi",
                 "Vertex_pt", "Vertex_eta",
                 "Vertex_MCx", "Vertex_MCy", "Vertex_MCz",
                 "Vertex_isMCKSpipi",
                 "recoKS_Vertex_r", "recoKS_Vertex_z", "recoKS_Vertex_mass",
                 "recoKS_Vertex_mass_before_VerDet", "recoKS_Vertex_mass_within_VerDet", "recoKS_Vertex_mass_beyond_VerDet",
                 "recoLm_Vertex_r", "recoLm_Vertex_z", "recoLm_Vertex_mass",
                 "recoLm_Vertex_mass_before_VerDet", "recoLm_Vertex_mass_within_VerDet", "recoLm_Vertex_mass_beyond_VerDet",
                ]
        return branchList
