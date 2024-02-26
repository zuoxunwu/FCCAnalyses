#Mandatory: List of processes
processList = {
#             'wzp6_ee_tt_pol_ecm365':{'chunks':50},
#             'wzp6_ee_Z_tt_leplep_pol_ecm365':{'chunks':10},
#             'wzp6_ee_Z_tt_tlepThad_pol_ecm365':{'chunks':10,},
#             'wzp6_ee_Z_tt_thadTlep_pol_ecm365':{'chunks':10},
#             'wzp6_ee_Z_tt_hadhad_pol_ecm365':{'chunks':50},
#             'wzp6_ee_gamma_tt_leplep_pol_ecm365':{'chunks':10},
#             'wzp6_ee_gamma_tt_tlepThad_pol_ecm365':{'chunks':10},
#             'wzp6_ee_gamma_tt_thadTlep_pol_ecm365':{'chunks':10},
#             'wzp6_ee_gamma_tt_hadhad_pol_ecm365':{'chunks':50},
#             'wzp6_ee_SM_tt_leplep_pol_ecm365':{'chunks':50},
#             'wzp6_ee_SM_tt_tlepThad_pol_ecm365':{'chunks':50},
#             'wzp6_ee_SM_tt_thadTlep_pol_ecm365':{'chunks':50},
#             'wzp6_ee_SM_tt_hadhad_pol_ecm365':{'chunks':50}

#              'wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':65},
#              'wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ecm365': {'chunks':65},
#              'wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':65},
#              'wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ecm365': {'chunks':65},

              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ta_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_tv_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_vr_ttZup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {'chunks':5},
          
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ta_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_tv_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_vr_ttZup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {'chunks':5},
          
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ta_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_tv_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_vr_ttZup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {'chunks':5},
          
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ta_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_tv_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_vr_ttZup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {'chunks':5},
            }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/top/hadronic/analysis_stage1/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topEWK/flatNtuples/winter2023"
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topEWK/flatNtuples_20240108/winter2023"



#Optional
nCPUS       = 8
runBatch    = True
batchQueue = "workday"
compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")

               .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(3)( Particle )" )
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               # the recoParticles corresponding  to the tracks that are primaries, according to MC-matching :
               .Define("MC_PrimaryTracks_RP",  "VertexingUtils::SelPrimaryTracks(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, MC_PrimaryVertex)" )
               # and the corresponding tracks :
               .Define("MC_PrimaryTracks",  "ReconstructedParticle2Track::getRP2TRK( MC_PrimaryTracks_RP, EFlowTrack_1)" )
               .Define("n_PrimaryTracks", "ReconstructedParticle::get_n(MC_PrimaryTracks_RP)")

               .Define("genTop",      "FCCAnalyses::MCParticle::sel_pdgID(6, true)(Particle)")
               .Define("genW",        "FCCAnalyses::MCParticle::sel_pdgID(24, true)(Particle)")
               .Define("genBottom",   "FCCAnalyses::MCParticle::sel_pdgID(5, true)(Particle)")
               .Define("genStrange",  "FCCAnalyses::MCParticle::sel_pdgID(3, true)(Particle)")
               .Define("genMuon",     "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
               .Define("genElectron", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
               .Define("n_genTops",      "FCCAnalyses::MCParticle::get_n(genTop)")
               .Define("n_genWs",        "FCCAnalyses::MCParticle::get_n(genW)")
               .Define("n_genBottoms",      "FCCAnalyses::MCParticle::get_n(genBottom)")
               .Define("n_genStranges",      "FCCAnalyses::MCParticle::get_n(genStrange)")
               .Define("n_genMuons",     "FCCAnalyses::MCParticle::get_n(genMuon)")
               .Define("n_genElectrons", "FCCAnalyses::MCParticle::get_n(genElectron)")

               .Define("genTop_px",     "FCCAnalyses::MCParticle::get_px(genTop)")
               .Define("genTop_py",     "FCCAnalyses::MCParticle::get_py(genTop)")
               .Define("genTop_pz",     "FCCAnalyses::MCParticle::get_pz(genTop)")
               .Define("genTop_phi",    "FCCAnalyses::MCParticle::get_phi(genTop)")
               .Define("genTop_eta",    "FCCAnalyses::MCParticle::get_eta(genTop)")
               .Define("genTop_energy", "FCCAnalyses::MCParticle::get_e(genTop)")
               .Define("genTop_mass",   "FCCAnalyses::MCParticle::get_mass(genTop)")
               .Define("genTop_pdg",    "FCCAnalyses::MCParticle::get_pdg(genTop)")

               .Define("genBottom_px",     "FCCAnalyses::MCParticle::get_px(genBottom)")
               .Define("genBottom_py",     "FCCAnalyses::MCParticle::get_py(genBottom)")
               .Define("genBottom_pz",     "FCCAnalyses::MCParticle::get_pz(genBottom)")
               .Define("genBottom_phi",    "FCCAnalyses::MCParticle::get_phi(genBottom)")
               .Define("genBottom_eta",    "FCCAnalyses::MCParticle::get_eta(genBottom)")
               .Define("genBottom_energy", "FCCAnalyses::MCParticle::get_e(genBottom)")
               .Define("genBottom_mass",   "FCCAnalyses::MCParticle::get_mass(genBottom)")
               .Define("genBottom_pdg",    "FCCAnalyses::MCParticle::get_pdg(genBottom)")

               .Define("genStrange_px",     "FCCAnalyses::MCParticle::get_px(genStrange)")
               .Define("genStrange_py",     "FCCAnalyses::MCParticle::get_py(genStrange)")
               .Define("genStrange_pz",     "FCCAnalyses::MCParticle::get_pz(genStrange)")
               .Define("genStrange_phi",    "FCCAnalyses::MCParticle::get_phi(genStrange)")
               .Define("genStrange_eta",    "FCCAnalyses::MCParticle::get_eta(genStrange)")
               .Define("genStrange_energy", "FCCAnalyses::MCParticle::get_e(genStrange)")
               .Define("genStrange_mass",   "FCCAnalyses::MCParticle::get_mass(genStrange)")
               .Define("genStrange_pdg",    "FCCAnalyses::MCParticle::get_pdg(genStrange)")

               .Define("genW_px",     "FCCAnalyses::MCParticle::get_px(genW)")
               .Define("genW_py",     "FCCAnalyses::MCParticle::get_py(genW)")
               .Define("genW_pz",     "FCCAnalyses::MCParticle::get_pz(genW)")
               .Define("genW_phi",    "FCCAnalyses::MCParticle::get_phi(genW)")
               .Define("genW_eta",    "FCCAnalyses::MCParticle::get_eta(genW)")
               .Define("genW_energy", "FCCAnalyses::MCParticle::get_e(genW)")
               .Define("genW_mass",   "FCCAnalyses::MCParticle::get_mass(genW)")
               .Define("genW_charge", "FCCAnalyses::MCParticle::get_charge(genW)")

               .Define("genMuon_px",        "FCCAnalyses::MCParticle::get_px(genMuon)")
               .Define("genMuon_py",        "FCCAnalyses::MCParticle::get_py(genMuon)")
               .Define("genMuon_pz",        "FCCAnalyses::MCParticle::get_pz(genMuon)")
               .Define("genMuon_phi",       "FCCAnalyses::MCParticle::get_phi(genMuon)")
               .Define("genMuon_eta",       "FCCAnalyses::MCParticle::get_eta(genMuon)")
               .Define("genMuon_energy",    "FCCAnalyses::MCParticle::get_e(genMuon)")
               .Define("genMuon_mass",      "FCCAnalyses::MCParticle::get_mass(genMuon)")
               .Define("genMuon_charge",    "FCCAnalyses::MCParticle::get_charge(genMuon)")
               .Define("genMuon_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(genMuon,Particle,Particle0)")

               .Define("genElectron_px",        "FCCAnalyses::MCParticle::get_px(genElectron)")
               .Define("genElectron_py",        "FCCAnalyses::MCParticle::get_py(genElectron)")
               .Define("genElectron_pz",        "FCCAnalyses::MCParticle::get_pz(genElectron)")
               .Define("genElectron_phi",       "FCCAnalyses::MCParticle::get_phi(genElectron)")
               .Define("genElectron_eta",       "FCCAnalyses::MCParticle::get_eta(genElectron)")
               .Define("genElectron_energy",    "FCCAnalyses::MCParticle::get_e(genElectron)")
               .Define("genElectron_mass",      "FCCAnalyses::MCParticle::get_mass(genElectron)")
               .Define("genElectron_charge",    "FCCAnalyses::MCParticle::get_charge(genElectron)")
               .Define("genElectron_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(genElectron,Particle,Particle0)") 

               .Alias("Muon0",      "Muon#0.index")
               .Alias("Electron0",  "Electron#0.index")
               .Alias("Photon0",    "Photon#0.index")
               .Define("muons",     "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
               .Define("electrons", "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
               .Define("photons",   "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
 
               .Define("n_muons",     "ReconstructedParticle::get_n(muons)")
               .Define("n_electrons", "ReconstructedParticle::get_n(electrons)")
               .Define("n_photons",   "ReconstructedParticle::get_n(photons)")
               .Define("n_jets_default",      "ReconstructedParticle::get_n(Jet)")
               # default jets are reconstructed with anti-kT inclusive clustering, R = 1.5. 

               .Define("muon_px",          "ReconstructedParticle::get_px(muons)")
               .Define("muon_py",          "ReconstructedParticle::get_py(muons)")
               .Define("muon_pz",          "ReconstructedParticle::get_pz(muons)")
               .Define("muon_phi",         "ReconstructedParticle::get_phi(muons)")
               .Define("muon_eta",         "ReconstructedParticle::get_eta(muons)")
               .Define("muon_energy",      "ReconstructedParticle::get_e(muons)")
               .Define("muon_mass",        "ReconstructedParticle::get_mass(muons)")
               .Define("muon_charge",      "ReconstructedParticle::get_charge(muons)")
               .Define("muon_d0",          "ReconstructedParticle2Track::getRP2TRK_D0(muons,EFlowTrack_1)")
               .Define("muon_d0variance",  "ReconstructedParticle2Track::getRP2TRK_D0_cov(muons,EFlowTrack_1)")
               .Define("muon_d0signif",    "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(muons,EFlowTrack_1))") #significance
               .Define("muon_z0",          "ReconstructedParticle2Track::getRP2TRK_Z0(muons,EFlowTrack_1)")
               .Define("muon_z0variance",  "ReconstructedParticle2Track::getRP2TRK_Z0_cov(muons,EFlowTrack_1)")
               .Define("muon_z0signif",    "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(muons,EFlowTrack_1))") #significance
               
               .Define("muon_tracks",       "ReconstructedParticle2Track::getRP2TRK(muons,EFlowTrack_1)")
               # which of the tracks are primary according to the MC-matching
               .Define("muon_IsPrimary_truth",  "VertexFitterSimple::IsPrimary_forTracks( muon_tracks,  MC_PrimaryTracks )")

               .Define("electron_px",          "ReconstructedParticle::get_px(electrons)")
               .Define("electron_py",          "ReconstructedParticle::get_py(electrons)")
               .Define("electron_pz",          "ReconstructedParticle::get_pz(electrons)")
               .Define("electron_phi",         "ReconstructedParticle::get_phi(electrons)")
               .Define("electron_eta",         "ReconstructedParticle::get_eta(electrons)")
               .Define("electron_energy",      "ReconstructedParticle::get_e(electrons)")
               .Define("electron_mass",        "ReconstructedParticle::get_mass(electrons)")
               .Define("electron_charge",      "ReconstructedParticle::get_charge(electrons)")
               .Define("electron_d0",          "ReconstructedParticle2Track::getRP2TRK_D0(electrons,EFlowTrack_1)")
               .Define("electron_d0variance",  "ReconstructedParticle2Track::getRP2TRK_D0_cov(electrons,EFlowTrack_1)")
               .Define("electron_d0signif",    "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(electrons,EFlowTrack_1))") #significance
               .Define("electron_z0",          "ReconstructedParticle2Track::getRP2TRK_Z0(electrons,EFlowTrack_1)")
               .Define("electron_z0variance",  "ReconstructedParticle2Track::getRP2TRK_Z0_cov(electrons,EFlowTrack_1)")
               .Define("electron_z0signif",    "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(electrons,EFlowTrack_1))") #significance

               .Define("electron_tracks",       "ReconstructedParticle2Track::getRP2TRK(electrons,EFlowTrack_1)")
               # which of the tracks are primary according to the MC-matching
               .Define("electron_IsPrimary_truth",  "VertexFitterSimple::IsPrimary_forTracks( electron_tracks,  MC_PrimaryTracks )")

               .Define("photon_px",          "ReconstructedParticle::get_px(photons)")
               .Define("photon_py",          "ReconstructedParticle::get_py(photons)")
               .Define("photon_pz",          "ReconstructedParticle::get_pz(photons)")
               .Define("photon_phi",          "ReconstructedParticle::get_phi(photons)")
               .Define("photon_eta",          "ReconstructedParticle::get_eta(photons)")
               .Define("photon_energy",      "ReconstructedParticle::get_e(photons)")
               .Define("photon_mass",        "ReconstructedParticle::get_mass(photons)")
               .Define("photon_charge",      "ReconstructedParticle::get_charge(photons)")

               .Define("Emiss_energy",  "ReconstructedParticle::get_e(MissingET)")
               .Define("Emiss_p",       "ReconstructedParticle::get_p(MissingET)")
               .Define("Emiss_px",      "ReconstructedParticle::get_px(MissingET)") #x-component of RecoMissingEnergy
               .Define("Emiss_py",      "ReconstructedParticle::get_py(MissingET)") #y-component of RecoMissingEnergy
               .Define("Emiss_pz",      "ReconstructedParticle::get_pz(MissingET)") #z-component of RecoMissingEnergy
               .Define("Emiss_phi",     "ReconstructedParticle::get_phi(MissingET)")
               .Define("Emiss_eta",     "ReconstructedParticle::get_eta(MissingET)")

               .Define("jet_default_px",          "ReconstructedParticle::get_px(Jet)")
               .Define("jet_default_py",          "ReconstructedParticle::get_py(Jet)")
               .Define("jet_default_pz",          "ReconstructedParticle::get_pz(Jet)")
               .Define("jet_default_phi",         "ReconstructedParticle::get_phi(Jet)")
               .Define("jet_default_eta",         "ReconstructedParticle::get_eta(Jet)")
               .Define("jet_default_energy",      "ReconstructedParticle::get_e(Jet)")
               .Define("jet_default_mass",        "ReconstructedParticle::get_mass(Jet)")
               .Define("jet_default_charge",      "ReconstructedParticle::get_charge(Jet)")

               .Alias("Jet3","Jet#3.index")
               .Define("jet_default_btag", "ReconstructedParticle::getJet_btag(Jet3, ParticleIDs, ParticleIDs_0)")

               # Alternative jet reconstructions
               .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
               .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
               .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
               .Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")
               .Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")
               .Define("RP_q",           "ReconstructedParticle::get_charge(ReconstructedParticles)")
               .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")

               # exclusive kT, R = 0.4, exactly njets = 6, sort by E
               # clustering_kt(float arg_radius = 0.5, int arg_exclusive = 0, float arg_cut = 5, int arg_sorted = 0, int arg_recombination = 0);
               .Define("FCCAnalysesJets_kt", "JetClustering::clustering_kt(0.4, 2, 6, 1, 10)(pseudo_jets)")
               .Define("jet_kt_exactly6",           "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_kt)")
               .Define("n_jets_kt_exactly6",        "return jet_kt_exactly6.size()")
               .Define("jet_kt_exactly6_px",        "JetClusteringUtils::get_px(jet_kt_exactly6)")
               .Define("jet_kt_exactly6_py",        "JetClusteringUtils::get_py(jet_kt_exactly6)")
               .Define("jet_kt_exactly6_pz",        "JetClusteringUtils::get_pz(jet_kt_exactly6)")
               .Define("jet_kt_exactly6_phi",       "JetClusteringUtils::get_phi(jet_kt_exactly6)")
               .Define("jet_kt_exactly6_eta",       "JetClusteringUtils::get_eta(jet_kt_exactly6)")
               .Define("jet_kt_exactly6_energy",    "JetClusteringUtils::get_e(jet_kt_exactly6)")
               .Define("jet_kt_exactly6_mass",      "JetClusteringUtils::get_m(jet_kt_exactly6)")
               .Define("jet_kt_exactly6_flavor",    "JetTaggingUtils::get_flavour(jet_kt_exactly6, Particle)")

               # exclusive kT, R = 0.8, up to njets = 6, sort by E
               # clustering_kt(float arg_radius = 0.5, int arg_exclusive = 0, float arg_cut = 5, int arg_sorted = 0, int arg_recombination = 0);
               .Define("FCCAnalysesJets_kt_upto", "JetClustering::clustering_kt(0.8, 3, 6, 1, 10)(pseudo_jets)")
               .Define("jet_kt_upto6",           "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_kt_upto)")
               .Define("n_jets_kt_upto6",        "return jet_kt_upto6.size()")
               .Define("jet_kt_upto6_px",        "JetClusteringUtils::get_px(jet_kt_upto6)")
               .Define("jet_kt_upto6_py",        "JetClusteringUtils::get_py(jet_kt_upto6)")
               .Define("jet_kt_upto6_pz",        "JetClusteringUtils::get_pz(jet_kt_upto6)")
               .Define("jet_kt_upto6_phi",       "JetClusteringUtils::get_phi(jet_kt_upto6)")
               .Define("jet_kt_upto6_eta",       "JetClusteringUtils::get_eta(jet_kt_upto6)")
               .Define("jet_kt_upto6_energy",    "JetClusteringUtils::get_e(jet_kt_upto6)")
               .Define("jet_kt_upto6_mass",      "JetClusteringUtils::get_m(jet_kt_upto6)")
               .Define("jet_kt_upto6_flavor",    "JetTaggingUtils::get_flavour(jet_kt_upto6, Particle)")

               # ee_genkt (anti-kT here) R= 0.4, inclusive, pt>1, sort by E
               # clustering_ee_genkt(float arg_radius = 0.5, int arg_exclusive = 0, float arg_cut = 5., int arg_sorted = 0, int arg_recombination = 0, float arg_exponent = 0.);
               .Define("FCCAnalysesJets_ee_genkt",  "JetClustering::clustering_ee_genkt(0.4, 0, 1, 1, 0, -1)(pseudo_jets)")
               .Define("jet_ee_genkt04",            "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_ee_genkt)")
               .Define("n_jets_ee_genkt04",         "return jet_ee_genkt04.size()")
               .Define("jet_ee_genkt04_px",         "JetClusteringUtils::get_px(jet_ee_genkt04)")
               .Define("jet_ee_genkt04_py",         "JetClusteringUtils::get_py(jet_ee_genkt04)")
               .Define("jet_ee_genkt04_pz",         "JetClusteringUtils::get_pz(jet_ee_genkt04)")
               .Define("jet_ee_genkt04_phi",        "JetClusteringUtils::get_phi(jet_ee_genkt04)")
               .Define("jet_ee_genkt04_eta",        "JetClusteringUtils::get_eta(jet_ee_genkt04)")
               .Define("jet_ee_genkt04_energy",     "JetClusteringUtils::get_e(jet_ee_genkt04)")
               .Define("jet_ee_genkt04_mass",       "JetClusteringUtils::get_m(jet_ee_genkt04)")
               .Define("jet_ee_genkt04_flavor",     "JetTaggingUtils::get_flavour(jet_ee_genkt04, Particle)")

               # valencia_algorithm, R=0.5, exclusive clustering with dcut = 6, sort by E, recombination E-scheme
               # clustering_valencia(float arg_radius = 0.5, int arg_exclusive = 0, float arg_cut = 5., int arg_sorted = 0, int arg_recombination = 0, float arg_beta = 1., float arg_gamma = 1.);
               .Define("FCCAnalysesJets_valencia",  "JetClustering::clustering_valencia(0.5, 1, 6, 1, 0, 1., 1.)(pseudo_jets)")
               .Define("jet_valencia",              "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_valencia)")
               .Define("n_jets_valencia",           "return jet_valencia.size()")
               .Define("jet_valencia_px",           "JetClusteringUtils::get_px(jet_valencia)")
               .Define("jet_valencia_py",           "JetClusteringUtils::get_py(jet_valencia)")
               .Define("jet_valencia_pz",           "JetClusteringUtils::get_pz(jet_valencia)")
               .Define("jet_valencia_phi",          "JetClusteringUtils::get_phi(jet_valencia)")
               .Define("jet_valencia_eta",          "JetClusteringUtils::get_eta(jet_valencia)")
               .Define("jet_valencia_energy",       "JetClusteringUtils::get_e(jet_valencia)")
               .Define("jet_valencia_mass",         "JetClusteringUtils::get_m(jet_valencia)")
               .Define("jet_valencia_flavor",       "JetTaggingUtils::get_flavour(jet_valencia, Particle)")

               # jade_algorithm, R=0.5, exclusive clustering, exactly 6 jets, sorted by E, recombination E0-scheme
               # clustering_jade(float arg_radius = 0.5, int arg_exclusive = 0, float arg_cut = 5., int arg_sorted = 0, int arg_recombination = 0);
               .Define("FCCAnalysesJets_jade",  "JetClustering::clustering_jade(0.5, 2, 6, 1, 10)(pseudo_jets)")
               .Define("jet_jade",              "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_jade)")
               .Define("n_jets_jade",           "return jet_jade.size()")
               .Define("jet_jade_px",           "JetClusteringUtils::get_px(jet_jade)")
               .Define("jet_jade_py",           "JetClusteringUtils::get_py(jet_jade)")
               .Define("jet_jade_pz",           "JetClusteringUtils::get_pz(jet_jade)")
               .Define("jet_jade_phi",          "JetClusteringUtils::get_phi(jet_jade)")
               .Define("jet_jade_eta",          "JetClusteringUtils::get_eta(jet_jade)")
               .Define("jet_jade_energy",       "JetClusteringUtils::get_e(jet_jade)")
               .Define("jet_jade_mass",         "JetClusteringUtils::get_m(jet_jade)")
               .Define("jet_jade_flavor",       "JetTaggingUtils::get_flavour(jet_jade, Particle)")

        )
        return df2


    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "n_genTops", "n_genWs", "n_genBottoms", "n_genStranges", "n_genMuons", "n_genElectrons", 
                 "genTop_px", "genTop_py", "genTop_pz", "genTop_phi", "genTop_eta", "genTop_energy", "genTop_mass", "genTop_pdg",
                 "genBottom_px", "genBottom_py", "genBottom_pz", "genBottom_phi", "genBottom_eta", "genBottom_energy", "genBottom_mass", "genBottom_pdg",
                 "genStrange_px", "genStrange_py", "genStrange_pz", "genStrange_phi", "genStrange_eta", "genStrange_energy", "genStrange_mass", "genStrange_pdg",
                 "genW_px", "genW_py", "genW_pz", "genW_phi", "genW_eta", "genW_energy", "genW_mass", "genW_charge",
                 "genMuon_px", "genMuon_py", "genMuon_pz", "genMuon_phi", "genMuon_eta", "genMuon_energy", "genMuon_mass", "genMuon_charge", "genMuon_parentPDG",
                 "genElectron_px", "genElectron_py", "genElectron_pz", "genElectron_phi", "genElectron_eta", "genElectron_energy", "genElectron_mass", "genElectron_charge", "genElectron_parentPDG",
                 "n_muons", "n_electrons", "n_photons", "n_jets_default",
                 "muon_px", "muon_py", "muon_pz", "muon_phi", "muon_eta", "muon_energy", "muon_mass", "muon_charge", "muon_d0", "muon_d0variance", "muon_d0signif", "muon_z0", "muon_z0variance", "muon_z0signif",
                 "electron_px", "electron_py", "electron_pz", "electron_phi", "electron_eta", "electron_energy", "electron_mass", "electron_charge", "electron_d0", "electron_d0variance", "electron_d0signif", "electron_z0", "electron_z0variance", "electron_z0signif",
                 "photon_px", "photon_py", "photon_pz", "photon_phi", "photon_eta", "photon_energy", "photon_mass", "photon_charge",
                 "Emiss_energy", "Emiss_p", "Emiss_px", "Emiss_py", "Emiss_pz", "Emiss_phi", "Emiss_eta",
                 "jet_default_px", "jet_default_py", "jet_default_pz", "jet_default_phi", "jet_default_eta", "jet_default_energy", "jet_default_mass", "jet_default_charge", "jet_default_btag",
                 "n_jets_kt_exactly6", "n_jets_kt_upto6",  "n_jets_ee_genkt04", "n_jets_valencia", "n_jets_jade",
                 "jet_kt_exactly6_px", "jet_kt_exactly6_py", "jet_kt_exactly6_pz", "jet_kt_exactly6_phi", "jet_kt_exactly6_eta", "jet_kt_exactly6_energy", "jet_kt_exactly6_mass", "jet_kt_exactly6_flavor",
                 "jet_kt_upto6_px", "jet_kt_upto6_py", "jet_kt_upto6_pz", "jet_kt_upto6_phi", "jet_kt_upto6_eta", "jet_kt_upto6_energy", "jet_kt_upto6_mass", "jet_kt_upto6_flavor",
                 "jet_ee_genkt04_px", "jet_ee_genkt04_py", "jet_ee_genkt04_pz", "jet_ee_genkt04_phi", "jet_ee_genkt04_eta", "jet_ee_genkt04_energy", "jet_ee_genkt04_mass", "jet_ee_genkt04_flavor",
                 "jet_valencia_px", "jet_valencia_py", "jet_valencia_pz", "jet_valencia_phi", "jet_valencia_eta", "jet_valencia_energy", "jet_valencia_mass", "jet_valencia_flavor",
                 "jet_jade_px", "jet_jade_py", "jet_jade_pz", "jet_jade_phi", "jet_jade_eta", "jet_jade_energy", "jet_jade_mass", "jet_jade_flavor"
                ]
        return branchList


