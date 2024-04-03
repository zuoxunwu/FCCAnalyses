import os, copy # tagging

#Mandatory: List of processes
processList = {

#              'wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':6},
#              'wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ecm365': {'chunks':6},
#              'wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':6},
#              'wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ecm365': {'chunks':6},

              # inclusive samples in Pythia
              'p8_ee_tt_ecm365': {'chunks':5},
              'p8_ee_WW_ecm365': {'chunks':5},
              'p8_ee_ZZ_ecm365': {'chunks':5},

              # ZH samples, no inclusive ones
              'wzp6_ee_bbH_ecm365': {'chunks':5},
              'wzp6_ee_ccH_ecm365': {'chunks':5},
              'wzp6_ee_ssH_ecm365': {'chunks':5},
              'wzp6_ee_qqH_ecm365': {'chunks':5},
              'wzp6_ee_tautauH_ecm365': {'chunks':5},
              'wzp6_ee_mumuH_ecm365': {'chunks':5},
              'wzp6_ee_eeH_ecm365': {'chunks':5},
              'wzp6_ee_nunuH_ecm365': {'chunks':5}

            }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/top/topEWK/analysis_stage1/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topEWK/flatNtuples_2024April/winter2023"


#Optional
nCPUS       = 8
runBatch    = True
batchQueue = "nextweek"
compGroup = "group_u_FCC.local_gen"

## tagging -------------------------------
## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc_v1"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = (
    "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
)
local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)


weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
    InclusiveJetClusteringHelper,
)

jetFlavourHelper = None
jetClusteringHelper = None

jetClusteringHelper_kt2   = None
jetClusteringHelper_kt4   = None
jetClusteringHelper_kt6   = None
jetClusteringHelper_R5   = None
jetFlavourHelper_kt2   = None
jetFlavourHelper_kt4   = None
jetFlavourHelper_kt6   = None
jetFlavourHelper_R5   = None

## tagging ------------------------------



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
               .Define("genMuon",     "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
               .Define("genElectron", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
               .Define("n_genTops",      "FCCAnalyses::MCParticle::get_n(genTop)")
               .Define("n_genWs",        "FCCAnalyses::MCParticle::get_n(genW)")
               .Define("n_genBottoms",      "FCCAnalyses::MCParticle::get_n(genBottom)")
               .Define("n_genMuons",     "FCCAnalyses::MCParticle::get_n(genMuon)")
               .Define("n_genElectrons", "FCCAnalyses::MCParticle::get_n(genElectron)")

               #.Filter("n_genTops==2")
               #.Filter("n_genWs==2")

               .Define("Wp_elenu", "FCCAnalyses::MCParticle::get_decay( 24, 11, false)(Particle, Particle1)")
               .Define("Wp_munu",  "FCCAnalyses::MCParticle::get_decay( 24, 13, false)(Particle, Particle1)")
               .Define("Wp_taunu", "FCCAnalyses::MCParticle::get_decay( 24, 15, false)(Particle, Particle1)")
               .Define("Wm_elenu", "FCCAnalyses::MCParticle::get_decay(-24, 11, false)(Particle, Particle1)")
               .Define("Wm_munu",  "FCCAnalyses::MCParticle::get_decay(-24, 13, false)(Particle, Particle1)")
               .Define("Wm_taunu", "FCCAnalyses::MCParticle::get_decay(-24, 15, false)(Particle, Particle1)")

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


               # Alternative jet reconstructions
               .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
               .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
               .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
               .Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")
               .Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")
               .Define("RP_q",           "ReconstructedParticle::get_charge(ReconstructedParticles)")
               .Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")


        )


        ## tagging ----------------------------------
        df3 = (df2
               .Define("muons_15",     "FCCAnalyses::ReconstructedParticle::sel_p(15)(muons)")
               .Define("electrons_15", "FCCAnalyses::ReconstructedParticle::sel_p(15)(electrons)")
               .Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,muons_15)")
               .Define("ReconstructedParticlesNoLeps",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoMuons,electrons_15)")
        )

        global jetClusteringHelper_kt2
        global jetClusteringHelper_kt4
        global jetClusteringHelper_kt6
        global jetClusteringHelper_R5
        global jetFlavourHelper_kt2
        global jetFlavourHelper_kt4
        global jetFlavourHelper_kt6
        global jetFlavourHelper_R5
        ## define jet and run clustering parameters
        ## name of collections in EDM root files
        collections = {
            "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticles",
            "PFTracks": "EFlowTrack",
            "PFPhotons": "EFlowPhoton",
            "PFNeutralHadrons": "EFlowNeutralHadron",
            "TrackState": "EFlowTrack_1",
            "TrackerHits": "TrackerHits",
            "CalorimeterHits": "CalorimeterHits",
            "dNdx": "EFlowTrack_2",
            "PathLength": "EFlowTrack_L",
            "Bz": "magFieldBz",
        }
        collections_noleps = copy.deepcopy(collections)
        collections_noleps["PFParticles"] = "ReconstructedParticlesNoLeps"

        ## def __init__(self, coll, njets, tag="")
        jetClusteringHelper_kt2 = ExclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 2, "kt2"
        )
        jetClusteringHelper_kt4 = ExclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 4, "kt4"
        )
        jetClusteringHelper_kt6 = ExclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 6, "kt6"
        )
        jetClusteringHelper_R5  = InclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 0.5, 1, "R5"
        )
        df3 = jetClusteringHelper_kt2.define(df3)
        df3 = jetClusteringHelper_kt4.define(df3)
        df3 = jetClusteringHelper_kt6.define(df3)
        df3 = jetClusteringHelper_R5. define(df3)

        ## define jet flavour tagging parameters

        jetFlavourHelper_kt2 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_kt2.jets,
            jetClusteringHelper_kt2.constituents,
            "kt2",
        )
        jetFlavourHelper_kt4 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_kt4.jets,
            jetClusteringHelper_kt4.constituents,
            "kt4",
        )
        jetFlavourHelper_kt6 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_kt6.jets,
            jetClusteringHelper_kt6.constituents,
            "kt6",
        )
        jetFlavourHelper_R5 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_R5.jets,
            jetClusteringHelper_R5.constituents,
            "R5",
        )
        ## define observables for tagger
        df3 = jetFlavourHelper_kt2.define(df3)
        df3 = jetFlavourHelper_kt4.define(df3)
        df3 = jetFlavourHelper_kt6.define(df3)
        df3 = jetFlavourHelper_R5. define(df3)

        ## tagger inference
        df3 = jetFlavourHelper_kt2.inference(weaver_preproc, weaver_model, df3)
        df3 = jetFlavourHelper_kt4.inference(weaver_preproc, weaver_model, df3)
        df3 = jetFlavourHelper_kt6.inference(weaver_preproc, weaver_model, df3)
        df3 = jetFlavourHelper_R5. inference(weaver_preproc, weaver_model, df3)

        # is this needed?
        # no, this is just variables for output
        df3 = df3.Define(
            "jets_kt2_p4",
            "JetConstituentsUtils::compute_tlv_jets({})".format(
                jetClusteringHelper_kt2.jets
            ),
        )
        


        df3 = (df3.Define("jet_kt2_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt2.jets))
        )
        df3 = df3.Define("jet_kt2_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt2.jets) )

        df3 = (df3.Define("jet_kt4_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt4.jets))
        )
        df3 = df3.Define("jet_kt4_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt4.jets) )

        df3 = (df3.Define("jet_kt6_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt6.jets))
        )
        df3 = df3.Define("jet_kt6_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt6.jets) )

        df3 = (df3.Define("jet_R5_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_R5.jets))
        )
        df3 = df3.Define("jet_R5_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_R5.jets) )
        df3 = df3.Define("n_jets_R5",           "return jet_R5_flavor.size()")

        ## tagging ----------------------------------


        return df3




    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "n_genTops", "n_genWs", "n_genBottoms", "n_genMuons", "n_genElectrons", 
                 "Wp_elenu", "Wp_munu", "Wp_taunu", "Wm_elenu", "Wm_munu", "Wm_taunu",
                 "genTop_px", "genTop_py", "genTop_pz", "genTop_phi", "genTop_eta", "genTop_energy", "genTop_mass", "genTop_pdg",
                 "genBottom_px", "genBottom_py", "genBottom_pz", "genBottom_phi", "genBottom_eta", "genBottom_energy", "genBottom_mass", "genBottom_pdg",
                 "genW_px", "genW_py", "genW_pz", "genW_phi", "genW_eta", "genW_energy", "genW_mass", "genW_charge",
                 "genMuon_px", "genMuon_py", "genMuon_pz", "genMuon_phi", "genMuon_eta", "genMuon_energy", "genMuon_mass", "genMuon_charge", "genMuon_parentPDG",
                 "genElectron_px", "genElectron_py", "genElectron_pz", "genElectron_phi", "genElectron_eta", "genElectron_energy", "genElectron_mass", "genElectron_charge", "genElectron_parentPDG",
                 "n_muons", "n_electrons", "n_photons",
                 "muon_px", "muon_py", "muon_pz", "muon_phi", "muon_eta", "muon_energy", "muon_mass", "muon_charge", "muon_d0", "muon_d0variance", "muon_d0signif", "muon_z0", "muon_z0variance", "muon_z0signif",
                 "electron_px", "electron_py", "electron_pz", "electron_phi", "electron_eta", "electron_energy", "electron_mass", "electron_charge", "electron_d0", "electron_d0variance", "electron_d0signif", "electron_z0", "electron_z0variance", "electron_z0signif",
                 "photon_px", "photon_py", "photon_pz", "photon_phi", "photon_eta", "photon_energy", "photon_mass", "photon_charge",
                 "Emiss_energy", "Emiss_p", "Emiss_px", "Emiss_py", "Emiss_pz", "Emiss_phi", "Emiss_eta",
                ]

        branchList += jetFlavourHelper_kt2.outputBranches() ## tagging
        branchList += jetFlavourHelper_kt4.outputBranches()
        branchList += jetFlavourHelper_kt6.outputBranches()
        branchList += jetFlavourHelper_R5. outputBranches()
        branchList += ["jet_kt2_px", "jet_kt2_py", "jet_kt2_pz", "jet_kt2_phi", "jet_kt2_eta", "jet_kt2_energy", "jet_kt2_mass", "jet_kt2_flavor"]
        branchList += ["jet_kt4_px", "jet_kt4_py", "jet_kt4_pz", "jet_kt4_phi", "jet_kt4_eta", "jet_kt4_energy", "jet_kt4_mass", "jet_kt4_flavor"]
        branchList += ["jet_kt6_px", "jet_kt6_py", "jet_kt6_pz", "jet_kt6_phi", "jet_kt6_eta", "jet_kt6_energy", "jet_kt6_mass", "jet_kt6_flavor"]
        branchList += ["jet_R5_px", "jet_R5_py", "jet_R5_pz", "jet_R5_phi", "jet_R5_eta", "jet_R5_energy", "jet_R5_mass", "jet_R5_flavor"]
        branchList += ["n_jets_R5"]
        return branchList
