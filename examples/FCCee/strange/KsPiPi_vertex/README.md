## Example code for reconstructing displaced K\_S decays

### set up the code

Follow instruction at [central FCCAnalyses git](https://github.com/HEP-FCC/FCCAnalyses?tab=readme-ov-file#pre-generated-samples)  
specifically for this branch, use

```
git clone --branch Kaon_decays git@github.com:zuoxunwu/FCCAnalyses.git
cd FCCAnalyses
source ./setup.sh
fccanalysis build -j 8
```

Once compiling is done, each time you ssh to a new terminal, you need to set up the environment by going to `FCCAnalysse\` directory and 
```
source ./setup.sh
```


### scripts

##### analysis scripts

`analysis_stage1_simple_example.py` is a simple script to process data. It reads raw sample files, calculate necessary variable, and save output files as a flat ROOT tree.
It contains some (hopefully self-explanatory) comments for each step of calculation.
The goal of the exercise is to expand this script to also study the properties of Lambda hadron decays, in a similar manner that is done for K\_S.

`analysis_stage1_full_from_Xunwu.py` is the full script, or the "solution" to the exercise.

You can run these scripts with 
```
fccanalysis run analysis_stage1_simple_example.py
```

##### function definition
`functions.h` provides custome defined functions.  
More "standard" functions, e.g. the namespace `myUtils`, are defined and compiled in `FCCAnalyses/analyzers/dataframe/src/`

##### plotting scripts
All plotting scripts read the same ROOT files produced by `analysis_stage1_simple_example.py`  
`plot1_multi.py` makes plots similar to [these ones](https://xzuo.web.cern.ch/FCC/strange/plots/plot1_multiplicity/)    
`plot2_decay.py` makes plots similar to [these ones](https://xzuo.web.cern.ch/FCC/strange/plots/plot2_decay/)  
`plot3_vertexreco.py` makes plots similar to [these ones](https://xzuo.web.cern.ch/FCC/strange/plots/plot3_vertexreco/)  
`plot4_massreso.py` makes plots similar to [these ones](https://xzuo.web.cern.ch/FCC/strange/plots/plot4_massres/)  

Run them with `python plot1_multi.py` without arguements

Note: plotting scripts may rely on packages not available in the stack with which you ran the FCCAnalyses. In that case you can source a different (more recent) stack, or set up your own python virtual environment.


### Contact
In case of questions, ask

Xunwu Zuo <xunwu.zuo@cern.ch> \
Radoslav Marchevski <radoslav.marchevski@cern.ch> \
Michele Selvaggi <Michele.Selvaggi@cern.ch> \
Stephane Monteil <monteil@in2p3.fr> \
