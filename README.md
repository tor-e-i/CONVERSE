# CONVERSE: Dataset for Multimodal Conversational Engagement Analysis in Human-Human and Human-Robot Interaction

This repository contains the CONVERSE dataset of conversational engagement annotations in 25 hours of unscripted participant-confederate conversations in Swedish, alongside the supporting code. This dataset extends the multimodal brain imaging [NeuroEngage](https://openneuro.org/datasets/ds004996) dataset, which includes fMRI, audio, confederate video, and eyetracking recordings. CONVERSE dataset can be used together with fMRI data or on its own.

## Data

The dataset includes the data from 48 participants conversing with a single female confederate: 28 participants in the human-human group and 20 in the human-robot group (where the confederate remotely operated a Furhat robot via a VR-mediated Wizard-of-Oz interface). Each participant held three unscripted conversations centered around ethical dilemmas, each lasting 10 minutes. In each conversation, the level of engagement was varied via the confederate's verbal and non-verbal behavior. Turns of both speakers were segmented, and the level of participant's conversational engagement at every turn was annotated using a novel 5-point annotation scheme, together with annotator's confidence for every turn. Additionally, participant's backchannels were annotated for future analysis. The annotation scheme, as well as detailed experiment design, can be found in the accompanying LREC paper (see Cite Us).

## Structure

The dataset includes .csv, .json, and .eaf files. Naming of every file has the following structure: 
```
[subject-id]_[run-id]_[group]_[engagement]
```
where 1) indicates participant id (1-55); 2) indicates run/conversation id (1-3); 3) indicates participant's group (human-human, human-robot); 4) indicates predefined engagement condition (high, medium, low).

Data structure:
```
|- data
|  |- eaf                       #contains .eaf files with the following tiers: participants' and confederate's turns transcriptions, engagement annotations, annotation confidence, backchannels.
|  |  |- human-human
|  |  |  |- ...
|  |  |- human-robot
|  |  |  |- ...
|  |- csv                       #contains .csv files for every tier separately 
|  |  |- ...
|  |- json                      #contains .json files for every conversation, which includes timestamps of the turns, transcriptions, annotations, and metadata about the session
|  |  |- ...

```

Notes:
- Media files are not necessary for opening .eaf files, but can be accessed at https://openneuro.org/datasets/ds004996.
- Several subject indices are excluded from the dataset: sub-04, sub-09, sub-10, sub-16, sub-17, sub-36, sub-39.
- To refer to confederate's data, the dataset uses "operator".

## Cite Us
Ekaterina Torubarova, Oskar Ljung, Julia Uddén and André Pereira (2026): CONVERSE: Annotation Scheme and Dataset for Multimodal Conversational Engagement Analysis in Human-Human and Human-Robot Interaction. Accepted to LREC 2026, Palma, Spain.
