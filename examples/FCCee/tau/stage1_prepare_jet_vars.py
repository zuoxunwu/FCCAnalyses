import os, copy # tagging

#Mandatory: List of processes
processList = {

#              'p8_ee_Ztautau_ecm91': {'chunks':10, 'fraction':0.01} # 100M events in total
#              'p8_ee_Zbb_ecm91':     {'chunks':10, 'fraction':0.004}, # 500M events in total
#              'p8_ee_Zcc_ecm91':     {'chunks':10, 'fraction':0.004}, # 500M events in total
              'p8_ee_Zss_ecm91':     {'chunks':1, 'fraction':0.0000002}, # 500M events in total
#              'p8_ee_Zud_ecm91':     {'chunks':10, 'fraction':0.002} # 500M events in total
#              'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':12},
#              'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':12},
#              'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':11},
#              'p8_ee_Zbb_ecm91_EvtGen_Bs2TauTau': {'chunks':50, 'fraction':0.5}
            }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/tau/analysis_stage1/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/tau_test/flatNtuples_2024April/winter2023"


#Optional
nCPUS       = 8
runBatch    = False
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

               .Define("genTau",   "FCCAnalyses::MCParticle::sel_pdgID(15, true)(Particle)")
               .Define("genMuon",     "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
               .Define("genElectron", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
               .Define("n_genTaus",      "FCCAnalyses::MCParticle::get_n(genTau)")
               .Define("n_genMuons",     "FCCAnalyses::MCParticle::get_n(genMuon)")
               .Define("n_genElectrons", "FCCAnalyses::MCParticle::get_n(genElectron)")

               #.Filter("n_genTaus==0")

               .Define("genTau_px",     "FCCAnalyses::MCParticle::get_px(genTau)")
               .Define("genTau_py",     "FCCAnalyses::MCParticle::get_py(genTau)")
               .Define("genTau_pz",     "FCCAnalyses::MCParticle::get_pz(genTau)")
               .Define("genTau_phi",    "FCCAnalyses::MCParticle::get_phi(genTau)")
               .Define("genTau_eta",    "FCCAnalyses::MCParticle::get_eta(genTau)")
               .Define("genTau_energy", "FCCAnalyses::MCParticle::get_e(genTau)")
               .Define("genTau_mass",   "FCCAnalyses::MCParticle::get_mass(genTau)")
               .Define("genTau_charge", "FCCAnalyses::MCParticle::get_charge(genTau)")
               .Define("genTau_pdg",    "FCCAnalyses::MCParticle::get_pdg(genTau)")
               .Define("genTau_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(genTau,Particle,Particle0)")

               .Alias("Muon0",      "Muon#0.index")
               .Alias("Electron0",  "Electron#0.index")
               .Alias("Photon0",    "Photon#0.index")
               .Define("muons",     "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
               .Define("electrons", "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
               .Define("photons",   "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
 
               .Define("n_muons",     "ReconstructedParticle::get_n(muons)")
               .Define("n_electrons", "ReconstructedParticle::get_n(electrons)")
               .Define("n_photons",   "ReconstructedParticle::get_n(photons)")

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

               #############################################
               ##        Build Tau -> 3Pi candidates      ##
               #############################################
               .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")
               .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject,ReconstructedParticles,EFlowTrack_1,MCRecoAssociations0,MCRecoAssociations1)")
               .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0,MCRecoAssociations1,Particle)")
               .Define("RecoPartPIDAtVertex" ,"myUtils::get_RP_atVertex(RecoPartPID, VertexObject)")

               .Define("Tau23PiCandidates",         "myUtils::build_tau23pi(VertexObject,RecoPartPIDAtVertex)")
               .Define("nTau23PiCandidates",        "float(myUtils::getFCCAnalysesComposite_N(Tau23PiCandidates))")

               .Define("Tau23PiCandidates_mass",    "myUtils::getFCCAnalysesComposite_mass(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_q",       "myUtils::getFCCAnalysesComposite_charge(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_px",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,0)")
               .Define("Tau23PiCandidates_py",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,1)")
               .Define("Tau23PiCandidates_pz",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,2)")
               .Define("Tau23PiCandidates_p",       "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,-1)")
               .Define("Tau23PiCandidates_B",       "myUtils::getFCCAnalysesComposite_B(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex)")
               .Define("Tau23PiCandidates_track",   "myUtils::getFCCAnalysesComposite_track(Tau23PiCandidates, VertexObject)")
               .Define("Tau23PiCandidates_d0",      "myUtils::get_trackd0(Tau23PiCandidates_track)")
               .Define("Tau23PiCandidates_z0",      "myUtils::get_trackz0(Tau23PiCandidates_track)")

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
        df3 = jetFlavourHelper_kt2.inference(weaver_preproc, weaver_model, df3)
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
        df3 = df3.Define("pfcand_PID_kt2", "JetConstituentsUtils::get_PIDs(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle,_jet_kt2)")


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
        df3 = df3.Define("pfcand_PID_R5", "JetConstituentsUtils::get_PIDs(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle,_jet_R5)")
        ## tagging ----------------------------------


        return df3




    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "n_genTaus", "n_genMuons", "n_genElectrons", 
                 "genTau_px", "genTau_py", "genTau_pz", "genTau_phi", "genTau_eta", "genTau_energy", "genTau_mass", "genTau_charge", "genTau_pdg", "genTau_parentPDG",
                 "n_muons", "n_electrons", "n_photons",
                 "Emiss_energy", "Emiss_p", "Emiss_px", "Emiss_py", "Emiss_pz", "Emiss_phi", "Emiss_eta",
                ]

        branchList += [ 
                "nTau23PiCandidates", "Tau23PiCandidates_mass", "Tau23PiCandidates_B",
                "Tau23PiCandidates_px", "Tau23PiCandidates_py", "Tau23PiCandidates_pz", "Tau23PiCandidates_p", "Tau23PiCandidates_q",
                "Tau23PiCandidates_d0",  "Tau23PiCandidates_z0",

                "Tau23PiCandidates_pion1px", "Tau23PiCandidates_pion1py", "Tau23PiCandidates_pion1pz",
                "Tau23PiCandidates_pion1p", "Tau23PiCandidates_pion1q", "Tau23PiCandidates_pion1d0", "Tau23PiCandidates_pion1z0",
                "Tau23PiCandidates_pion2px", "Tau23PiCandidates_pion2py", "Tau23PiCandidates_pion2pz",
                "Tau23PiCandidates_pion2p", "Tau23PiCandidates_pion2q", "Tau23PiCandidates_pion2d0", "Tau23PiCandidates_pion2z0",
                "Tau23PiCandidates_pion3px", "Tau23PiCandidates_pion3py", "Tau23PiCandidates_pion3pz",
                "Tau23PiCandidates_pion3p", "Tau23PiCandidates_pion3q", "Tau23PiCandidates_pion3d0", "Tau23PiCandidates_pion3z0",         
                ]

        branchList += jetFlavourHelper_kt2.outputBranches() ## tagging
        branchList += jetFlavourHelper_R5. outputBranches()
        branchList += [obs for obs in jetFlavourHelper_kt2.definition.keys() if "pfcand_" in obs]## tagging
        branchList += [obs for obs in jetFlavourHelper_R5. definition.keys() if "pfcand_" in obs]
        branchList += ["pfcand_PID_kt2", "pfcand_PID_R5"]
        #branchList += [obs for obs in jetClusteringHelper_kt2.definition.keys() if "jet_" in obs and "_jet_" not in obs]
        #branchList += [obs for obs in jetClusteringHelper_R5.definition.keys() if "jet_" in obs and "_jet_" not in obs]
        #branchList = [item for item in branchList if item not in ["jet_kt2","jet_R5"]]
        branchList += ["jet_kt2_px", "jet_kt2_py", "jet_kt2_pz", "jet_kt2_phi", "jet_kt2_eta", "jet_kt2_energy", "jet_kt2_mass", "jet_kt2_flavor"]
        branchList += ["jet_R5_px", "jet_R5_py", "jet_R5_pz", "jet_R5_phi", "jet_R5_eta", "jet_R5_energy", "jet_R5_mass", "jet_R5_flavor"]
        branchList += ["n_jets_R5"]
        return branchList
