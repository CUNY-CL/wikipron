# Morphology scripts

The scripts in this directory are responsible for downloading morphological
paradigms from [UniMorph](https://unimorph.github.io/).

## How to use

[`grab_unimorph_data.py`](graph_unimorph_data.py) downloads UniMorph data as
three-column TSV files:

    кошка   кошек   N;GEN;PL
    кошка   кошка   N;NOM;SG
    кошка   кошкам  N;DAT;PL
    кошка   кошками N;INS;PL
    кошка   кошках  N;ESS;PL
    кошка   кошке   N;DAT;SG
    кошка   кошке   N;ESS;SG
    кошка   кошки   N;GEN;SG
    кошка   кошки   N;NOM;PL
    кошка   кошкой  N;INS;SG
    кошка   кошку   N;ACC;SG

## Shared tasks

Specific configurations for shared tasks are stored [here](shared_tasks).
