import os, copy # tagging

#Mandatory: List of processes
processList = {
#             'wzp6_ee_SM_tt_tWbTWs_tallTlep_ecm365': {'chunks':1, 'fraction':0.0001}
             'wzp6_ee_SM_tt_tWbTWs_tallTlep_ecm365':   {'chunks':6},
             'wzp6_ee_SM_tt_tWbTWs_tallTlight_ecm365': {'chunks':6},
             'wzp6_ee_SM_tt_tWbTWs_tallTheavy_ecm365': {'chunks':6},
             'wzp6_ee_SM_tt_tWsTWb_tlepTall_ecm365':   {'chunks':6},
             'wzp6_ee_SM_tt_tWsTWb_tlightTall_ecm365': {'chunks':6},
             'wzp6_ee_SM_tt_tWsTWb_theavyTall_ecm365': {'chunks':6},

            }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/top/topVts/stage1_jet_tuples/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topVts/jet_tuples_2024March/winter2023"


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


#weaver_preproc = get_file_path(url_preproc, local_preproc)
#weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
    InclusiveJetClusteringHelper,
)


jetClusteringHelper_kt2   = None
jetClusteringHelper_R5   = None
jetFlavourHelper_kt2   = None
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
               .Define("genStrange",  "FCCAnalyses::MCParticle::sel_pdgID(3, true)(Particle)")
               .Define("genMuon",     "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
               .Define("genElectron", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
               .Define("n_genTops",      "FCCAnalyses::MCParticle::get_n(genTop)")
               .Define("n_genWs",        "FCCAnalyses::MCParticle::get_n(genW)")
               .Define("n_genBottoms",      "FCCAnalyses::MCParticle::get_n(genBottom)")
               .Define("n_genStranges",      "FCCAnalyses::MCParticle::get_n(genStrange)")
               .Define("n_genMuons",     "FCCAnalyses::MCParticle::get_n(genMuon)")
               .Define("n_genElectrons", "FCCAnalyses::MCParticle::get_n(genElectron)")

               .Filter("n_genTops==2")
               .Filter("n_genWs==2")
               #.Filter("n_genBottoms==1")
               #.Filter("n_genStranges==1")

               # This stupid function differentiate antiparticles in mother but only looks for absolute value in daughter
               .Define("Wp_elenu", "FCCAnalyses::MCParticle::get_decay( 24, 11, false)(Particle, Particle1)")
               .Define("Wp_munu",  "FCCAnalyses::MCParticle::get_decay( 24, 13, false)(Particle, Particle1)")
               .Define("Wp_taunu", "FCCAnalyses::MCParticle::get_decay( 24, 15, false)(Particle, Particle1)")
               .Define("Wp_d",     "FCCAnalyses::MCParticle::get_decay( 24, 1,  false)(Particle, Particle1)")
               .Define("Wp_s",     "FCCAnalyses::MCParticle::get_decay( 24, 3,  false)(Particle, Particle1)")
               .Define("Wp_b",     "FCCAnalyses::MCParticle::get_decay( 24, 5,  false)(Particle, Particle1)")
               .Define("Wm_elenu", "FCCAnalyses::MCParticle::get_decay(-24, 11, false)(Particle, Particle1)")
               .Define("Wm_munu",  "FCCAnalyses::MCParticle::get_decay(-24, 13, false)(Particle, Particle1)")
               .Define("Wm_taunu", "FCCAnalyses::MCParticle::get_decay(-24, 15, false)(Particle, Particle1)")
               .Define("Wm_d",     "FCCAnalyses::MCParticle::get_decay(-24, 1,  false)(Particle, Particle1)")
               .Define("Wm_s",     "FCCAnalyses::MCParticle::get_decay(-24, 3,  false)(Particle, Particle1)")
               .Define("Wm_b",     "FCCAnalyses::MCParticle::get_decay(-24, 5,  false)(Particle, Particle1)")

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

               .Alias("Muon0",      "Muon#0.index")
               .Alias("Electron0",  "Electron#0.index")
               .Define("muons",     "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
               .Define("electrons", "ReconstructedParticle::get(Electron0, ReconstructedParticles)")


        )


        ## tagging ----------------------------------
        df3 = (df2
               .Define("muons_15",     "FCCAnalyses::ReconstructedParticle::sel_p(15)(muons)")
               .Define("electrons_15", "FCCAnalyses::ReconstructedParticle::sel_p(15)(electrons)")
               .Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,muons_15)")
               .Define("ReconstructedParticlesNoLeps",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoMuons,electrons_15)")
        )

        global jetClusteringHelper_kt2
        global jetClusteringHelper_R5
        global jetFlavourHelper_kt2
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
        jetClusteringHelper_R5  = InclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 0.5, 1, "R5"
        )
        df3 = jetClusteringHelper_kt2.define(df3)
        df3 = jetClusteringHelper_R5. define(df3)

        ## define jet flavour tagging parameters

        jetFlavourHelper_kt2 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_kt2.jets,
            jetClusteringHelper_kt2.constituents,
            "kt2",
        )
        jetFlavourHelper_R5 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_R5.jets,
            jetClusteringHelper_R5.constituents,
            "R5",
        )

        ## define observables for tagger
        df3 = jetFlavourHelper_kt2.define(df3)
        df3 = jetFlavourHelper_R5. define(df3)

        ## tagger inference
#        df3 = jetFlavourHelper_kt2.inference(weaver_preproc, weaver_model, df3)
#        df3 = jetFlavourHelper_R5. inference(weaver_preproc, weaver_model, df3)



        df3 = (df3.Define("jet_kt2_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_dPhi_b",       "3.1416 - abs(3.1416 - abs(jet_kt2_phi - genBottom_phi.at(0)))")
                  .Define("jet_kt2_dEta_b",       "abs(jet_kt2_eta - genBottom_eta.at(0))")
                  .Define("jet_kt2_dR_b",         "sqrt(jet_kt2_dPhi_b*jet_kt2_dPhi_b + jet_kt2_dEta_b*jet_kt2_dEta_b)")  
                  .Define("jet_kt2_dPhi_s",       "3.1416 - abs(3.1416 - abs(jet_kt2_phi - genStrange_phi.at(0)))")
                  .Define("jet_kt2_dEta_s",       "abs(jet_kt2_eta - genStrange_eta.at(0))")
                  .Define("jet_kt2_dR_s",         "sqrt(jet_kt2_dPhi_s*jet_kt2_dPhi_s + jet_kt2_dEta_s*jet_kt2_dEta_s)")
        )
        df3 = df3.Define("jet_kt2_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt2.jets) )

        df3 = (df3.Define("jet_R5_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_dPhi_b",       "3.1416 - abs(3.1416 - abs(jet_R5_phi - genBottom_phi.at(0)))")
                  .Define("jet_R5_dEta_b",       "abs(jet_R5_eta - genBottom_eta.at(0))")
                  .Define("jet_R5_dR_b",         "sqrt(jet_R5_dPhi_b*jet_R5_dPhi_b + jet_R5_dEta_b*jet_R5_dEta_b)")
                  .Define("jet_R5_dPhi_s",       "3.1416 - abs(3.1416 - abs(jet_R5_phi - genStrange_phi.at(0)))")
                  .Define("jet_R5_dEta_s",       "abs(jet_R5_eta - genStrange_eta.at(0))")
                  .Define("jet_R5_dR_s",         "sqrt(jet_R5_dPhi_s*jet_R5_dPhi_s + jet_R5_dEta_s*jet_R5_dEta_s)")
        )
        df3 = df3.Define("jet_R5_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_R5.jets) )
        df3 = df3.Define("n_jets_R5",           "return jet_R5_flavor.size()")

        ## tagging ----------------------------------


        return df3




    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "n_genTops", "n_genWs", "n_genBottoms", "n_genStranges", "n_genMuons", "n_genElectrons", 
                 "Wp_elenu", "Wp_munu", "Wp_taunu", "Wp_d", "Wp_s", "Wp_b",
                 "Wm_elenu", "Wm_munu", "Wm_taunu", "Wm_d", "Wm_s", "Wm_b",
                 "genBottom_px", "genBottom_py", "genBottom_pz", "genBottom_phi", "genBottom_eta", "genBottom_energy", "genBottom_mass", "genBottom_pdg",
                 "genStrange_px", "genStrange_py", "genStrange_pz", "genStrange_phi", "genStrange_eta", "genStrange_energy", "genStrange_mass", "genStrange_pdg",
                ]

        branchList += jetFlavourHelper_kt2.definition.keys()
        branchList += jetFlavourHelper_R5. definition.keys()
        branchList += [obs for obs in jetClusteringHelper_kt2.definition.keys() if "jet_" in obs and "_jet_" not in obs]
        branchList += [obs for obs in jetClusteringHelper_R5.definition.keys() if "jet_" in obs and "_jet_" not in obs]
        branchList = [item for item in branchList if item not in ["jet_kt2","jet_R5"]] 
        branchList += ["jet_kt2_px", "jet_kt2_py", "jet_kt2_pz", "jet_kt2_phi", "jet_kt2_eta", "jet_kt2_energy", "jet_kt2_mass", "jet_kt2_flavor", "jet_kt2_dR_b", "jet_kt2_dR_s"]
        branchList += ["jet_R5_px", "jet_R5_py", "jet_R5_pz", "jet_R5_phi", "jet_R5_eta", "jet_R5_energy", "jet_R5_mass", "jet_R5_flavor", "jet_R5_dR_b", "jet_R5_dR_s"]
        return branchList
