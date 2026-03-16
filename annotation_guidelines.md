The annotator received the following instruction before the annotations. The annotator was also familiar with the study design from the paper Torubarova, E., Arvidsson, C., Berrebi, J., Uddén, J., & Pereira, A. (2025, March). Neuroengage: A multimodal dataset integrating fmri for analyzing conversational engagement in human-human and human-robot interactions. In 2025 20th ACM/IEEE International Conference on Human-Robot Interaction (HRI) (pp. 849-858). IEEE.s
==================================================================
You are going to annotate conversational engagement in this dataset. 

In the folder “awaiting_annotations”, you will find files united by a unique ID. Each ID contains one 10-minute conversation. Download the folder to you computer: you need all the files belonging to the same ID.

## Step 1.
Open one id-XX_turns.eaf file in ELAN. It includes:
- 3 audio tracks: 1 for operator, 1 denoised participant sound and 1 raw participant sound. You can use raw sound in cases if denoising made participant’s speech hard to hear. For a few subjects, raw sound is missing. Keep operator and participant-denoised audio on and participant-raw muted and turn it on if necessary in the controls panel

- 2 transcription tiers: 1 for operator, 1 for participant
- 1 empty engagement annotation tier for production
- 1 empty annotation confidence tier 
- 1 empty backchannels tier 

## Step 2.
You will annotate participant’s production. Listen to the conversation and rate participant’s level of conversational engagement in each turn on the scale of 1-5:

- Level 1: strongly disengaged
- Level 2: disengaged
- Level 3: neutral
- Level 4: engaged
- Level 5: strongly engaged

Put one number (1-5) in each segment of production_annotation tier.

When annotating engagement, remember to keep these questions in mind:
1) How willing is the participant to contribute to the progress of the conversation?
2) How invested is the participant in what he/she is saying?
3) How interested is he/she in the conversation?
But remember, you are rating the overall level of participant’s conversational engagement, not these individual questions. 
## Step 3.
After giving engagement score, rate how confident you are in your score for this turn on the scale of 1-5:
- Level 1: not confident at all
- Level 2: somewhat not confident
- Level 3: moderately confident
- Level 4: confident
- Level 5: completely confident

Put one number (1-5) in each segment of production_confidence tier.

## Step 4.
Go through all the production turns in the conversation. Remember to save the project frequently. After completing a conversation, copy the corresponding .eaf file to the folder “annotated’.
