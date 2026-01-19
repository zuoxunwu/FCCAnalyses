#Mandatory: List of processes
processList = {
             'p8_ee_Zss_ecm91':{'chunks':1, 'fraction':0.0000001},
#             'p8_ee_Zcc_ecm91':{'chunks':1, 'fraction':0.0000001},
#             'p8_ee_Zbb_ecm91':{'chunks':1, 'fraction':0.0000001},
#             'p8_ee_Zud_ecm91':{'chunks':1, 'fraction':0.0000001},

            }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/strange/analysis_stage1_1118/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/strange/displaced_vertex/flatNtuples/winter2023"

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

               #############################################################
               ##  these lines get truth info (generator info) of  kaons  ##
               ##  number of each kaon type per event, and their energy   ## 
               #############################################################
               ##  plot1_multi.py will use the following branches         ##
               #############################################################

               .Define("genK0",   "FCCAnalyses::MCParticle::sel_pdgID(311, true)(Particle)")
               .Define("genKL",   "FCCAnalyses::MCParticle::sel_pdgID(130, true)(Particle)")
               .Define("genKS",   "FCCAnalyses::MCParticle::sel_pdgID(310, true)(Particle)")
               .Define("genKpos", "FCCAnalyses::MCParticle::sel_pdgID(321, false)(Particle)")
               .Define("genKneg", "FCCAnalyses::MCParticle::sel_pdgID(-321, false)(Particle)")

               ## number of kaons in the event

               .Define("n_genK0s",      "FCCAnalyses::MCParticle::get_n(genK0)")
               .Define("n_genKLs",      "FCCAnalyses::MCParticle::get_n(genKL)")
               .Define("n_genKSs",      "FCCAnalyses::MCParticle::get_n(genKS)")
               .Define("n_genKposs",    "FCCAnalyses::MCParticle::get_n(genKpos)")
               .Define("n_genKnegs",    "FCCAnalyses::MCParticle::get_n(genKneg)")

               ## energy of kaons

               .Define("genKS_energy",     "FCCAnalyses::MCParticle::get_e   (genKS)")
               .Define("genKpos_energy",   "FCCAnalyses::MCParticle::get_e   (genKpos)")
               .Define("genKneg_energy",   "FCCAnalyses::MCParticle::get_e   (genKneg)")


               #########################################################
               ##  these lines get true vertex properties             ##
               ##  "MCVertexObject" is an vector of MC vertex objects ##
               ##  the rest are vector of float (or int) variables    ##
               #########################################################
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


                ########################################################
                ##           single out true Bs vertices              ##
                ##  The "MC_Vertex_isKSpipi" is a hacky way to check  ##
                ##  for each MC vertex if it is a K_S to pi pi decay  ##
                ##  A better way is to put this long line of for loop ##
                ##  into a function and call the function             ##
                ########################################################
                ##  plot2_decay.py will use the following branches    ##
                ########################################################

               .Define("MC_Vertex_isKSpipi",   "ROOT::VecOps::RVec<int> result; for (size_t i=0; i < MC_Vertex_PDGmother.size(); ++i) {int isKS=0; for (size_t j=0; j < MC_Vertex_PDGmother[i].size(); ++j) {if (abs(MC_Vertex_PDGmother[i][j])==310) isKS+=10;} for (size_t j=0; j < MC_Vertex_PDG[i].size(); ++j) {if (abs(MC_Vertex_PDG[i][j])==211) isKS+=1;} result.push_back(isKS);} return result;")

               .Define("MC_Vertex_KSflag", "1.0*(MC_Vertex_isKSpipi > 10 && MC_Vertex_isKSpipi % 10 !=0)")
               .Define("genKS_Vertex_x",   "MC_Vertex_x  [MC_Vertex_KSflag>0]") #find Bs meson
               .Define("genKS_Vertex_y",   "MC_Vertex_y  [MC_Vertex_KSflag>0]") #no implementation of abs() for vector
               .Define("genKS_Vertex_z",   "MC_Vertex_z  [MC_Vertex_KSflag>0]")
               .Define("genKS_Vertex_p",   "MC_Vertex_p  [MC_Vertex_KSflag>0]")
               .Define("genKS_Vertex_pt",  "MC_Vertex_pt [MC_Vertex_KSflag>0]")
               .Define("genKS_Vertex_r",   "sqrt(genKS_Vertex_x*genKS_Vertex_x + genKS_Vertex_y*genKS_Vertex_y)")
               .Define("genKS_Vertex_d",   "sqrt(genKS_Vertex_x*genKS_Vertex_x + genKS_Vertex_y*genKS_Vertex_y + genKS_Vertex_z*genKS_Vertex_z)")

               #############################################
               ##              Build Reco Vertex          ##
               #############################################
               .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject,ReconstructedParticles,EFlowTrack_1,MCRecoAssociations0,MCRecoAssociations1)")
               .Define("EVT_NVertex",   "float(VertexObject.size())")

               ####################################################
               ##    read RECO particles with PID at vertex      ##
               ####################################################
               .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0,MCRecoAssociations1,Particle)")
               .Define("RecoPartPIDAtVertex" ,"myUtils::get_RP_atVertex(RecoPartPID, VertexObject)")

               #############################################
               ##         Build vertex variables          ##
               #############################################

               ## these are the x,y,z positions of reconstructed vertices
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

               ## these are the true x,y,z positions of the MC vertices matched to the reco vertices
               .Define("Vertex_MCx",      "ROOT::VecOps::RVec<float> result; for (size_t i=0; i < Vertex_mcind.size(); ++i) result.push_back(MC_Vertex_x.at(Vertex_mcind[i])); return result;")
               .Define("Vertex_MCy",      "ROOT::VecOps::RVec<float> result; for (size_t i=0; i < Vertex_mcind.size(); ++i) result.push_back(MC_Vertex_y.at(Vertex_mcind[i])); return result;")
               .Define("Vertex_MCz",      "ROOT::VecOps::RVec<float> result; for (size_t i=0; i < Vertex_mcind.size(); ++i) result.push_back(MC_Vertex_z.at(Vertex_mcind[i])); return result;")
               .Define("Vertex_MCd",      "sqrt( (Vertex_MCx-Vertex_x)*(Vertex_MCx-Vertex_x) + (Vertex_MCy-Vertex_y)*(Vertex_MCy-Vertex_y) + (Vertex_MCz-Vertex_z)*(Vertex_MCz-Vertex_z)   )")
               .Define("Vertex_isMCKSpipi",   "ROOT::VecOps::RVec<int> result; for (size_t i=0; i < Vertex_mcind.size(); ++i) {int isKS=0; for (size_t j=0; j < MC_Vertex_PDGmother[Vertex_mcind[i]].size(); ++j) {if (abs(MC_Vertex_PDGmother[i][j])==310) isKS+=10;} for (size_t l=0; l < MC_Vertex_PDG[Vertex_mcind[i]].size(); ++l) {if (abs(MC_Vertex_PDG[i][l])==211) isKS+=1;} result.push_back(isKS);} return result;")

               .Define("Vertex_KSmatch",  "1.0*(Vertex_isMCKSpipi > 10 && Vertex_isMCKSpipi % 10 !=0 && Vertex_chi2<10 && Vertex_MCd<2)")

               ########################################################
               ##   check for mass reso for displaced vertices (KS)  ##
               ########################################################

               .Define("Vertex_rErr", "sqrt(Vertex_xErr*Vertex_xErr + Vertex_yErr*Vertex_yErr)")
               .Define("Vertex_dErr", "sqrt(Vertex_xErr*Vertex_xErr + Vertex_yErr*Vertex_yErr + Vertex_zErr*Vertex_zErr)")

               ## mass of all reconstructed vertices
               .Define("Vertex_r", "sqrt(Vertex_x*Vertex_x + Vertex_y*Vertex_y)")
               .Define("Vertex_d", "sqrt(Vertex_x*Vertex_x + Vertex_y*Vertex_y + Vertex_z*Vertex_z)")
               .Define("Vertex_mass_before_VerDet", "Vertex_mass[Vertex_chi2<10 && Vertex_r<13.7]") ## decays before first vertex detector layer
               .Define("Vertex_mass_within_VerDet", "Vertex_mass[Vertex_chi2<10 && Vertex_r>13.7 && Vertex_r<34]") ## decays within vertex detector volume
               .Define("Vertex_mass_within_DC",     "Vertex_mass[Vertex_chi2<10 && Vertex_r>35]")
               .Define("Vertex_mass_super_displaced", "Vertex_mass[Vertex_chi2<10 && Vertex_r>1000]")

               ## mass of reconstructed vertices that are matched as K_S decays
               .Define("recoKS_Vertex_r", "Vertex_r[Vertex_KSmatch>0]")
               .Define("recoKS_Vertex_z", "Vertex_z[Vertex_KSmatch>0]")
               .Define("recoKS_Vertex_mass", "Vertex_mass[Vertex_KSmatch>0]")
               .Define("recoKS_Vertex_mass_before_VerDet", "Vertex_mass[Vertex_KSmatch>0 && Vertex_r<13.7]")
               .Define("recoKS_Vertex_mass_within_VerDet", "Vertex_mass[Vertex_KSmatch>0 && Vertex_r>13.7 && Vertex_r<34]")
               .Define("recoKS_Vertex_mass_beyond_VerDet", "Vertex_mass[Vertex_KSmatch>0 && Vertex_r>35]")

        )
        return df2




    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "n_genK0s", "n_genKLs", "n_genKSs",
                 "n_genKposs", "n_genKnegs",
                 "genKS_energy", "genKpos_energy", "genKneg_energy",

                 "genKS_Vertex_x", "genKS_Vertex_y", "genKS_Vertex_z", "genKS_Vertex_r", "genKS_Vertex_d", "genKS_Vertex_p", "genKS_Vertex_pt",
                 "EVT_NVertex",
                 "MC_Vertex_mass", "MC_Vertex_p",
                 "Vertex_x", "Vertex_y", "Vertex_z", "Vertex_r", "Vertex_d",
                 "Vertex_xErr", "Vertex_yErr", "Vertex_zErr", "Vertex_rErr", "Vertex_dErr", 
                 "Vertex_chi2", "Vertex_isPV", "Vertex_ntrk", "Vertex_mass",
                 "Vertex_n",
                 "Vertex_mass_before_VerDet", "Vertex_mass_within_VerDet", "Vertex_mass_within_DC", "Vertex_mass_super_displaced",
                 "Vertex_pt", "Vertex_eta",
                 "Vertex_MCx", "Vertex_MCy", "Vertex_MCz",
                 "Vertex_isMCKSpipi",
                 "recoKS_Vertex_r", "recoKS_Vertex_z", "recoKS_Vertex_mass",
                 "recoKS_Vertex_mass_before_VerDet", "recoKS_Vertex_mass_within_VerDet", "recoKS_Vertex_mass_beyond_VerDet",
                ]
        return branchList
