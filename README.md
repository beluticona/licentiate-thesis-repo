# 2021-re-pendleton-perovskite

## Description

This project is based on Pendleton et all (2020), a paper about ML understanding of halide perovskite crystal formation without accurate physicochemical features. We proposed a several of modifications and improvements (or at least we are trying).

Available at:

> Pendleton, I. M. *et al.* Can Machines “Learn” Halide Perovskite Crystal Formation without Accurate Physicochemical Features? *J. Phys. Chem. C* **124**, 13982–13992 (2020).


## Reproduction

Run:

`pip install pipenv`

`pipenv --three`

`pipenv install ipykernel`

`pipenv run python -m ipykernel install --user --name=re-pendleton`

Install all packages found by setup. In this case we want src to be importable from notebooks.

`pipenv install -e .`

## TODO

    1) Automatize output for case GBC
        - folder for
        - make_classifier
    2) Enable both intr and extr (now if one is on, the other has to be off)

    3) Merge stratified data and all data(run together)

    4) Create only needed folders, now creating all of them (knn only)

    5) RF features importances

    6) seed choose number of runs

## Subconjuntos de predictotes

    SolV                9 sc(3 diff)  + 67 feat -1 = 75 (72 comun)
    SolUD               9 sc (3 diff) + 67 feat -1 = 75 (72 comun)
    SolV + Chem         36 + 75
    SolUD + Chem        36 + 75
    SolV + Exp         192 (7 comun) + 
    SolUD + Exp        170 (7 comun) + 
    "_raw{'_v1-' if v1 else '_'}M_.*_final",

    SolV + Reag         123 (7 comun) + 75 - 3 raw_v0M = 195 (79 en comun)
    SolUD + Reag         141 (7 comun) +75 - 3 _rxn_M = 213 (79 en comun)

# to merge:
    - folder name case GBC
    - save_results for GBC



