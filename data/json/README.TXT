These files contains annotation data extracted from ELAN combined with experimental conditions during the data production process.
The annotation branch is subdivided into events. Each event may have one or more annotation tiers. Tthe annotation tiers corespond to the annotation tiers in the ELAN annotation:
    participant             the orthographic trascription of the subject speaking, divided into IPUs
    operator                the orthographic transcription of the subjects confederate speaking divided into IPUs
    production_annotation   the level of engagement of the subject during that speaking turn
    confidence_production   the annotators confidence in the annotation value for that speaking turn
    backchannels            a backchanneling signal.

The following is the structure of the json files. the data type is expressed in parenthesis after the description when applicable 


├─ annotation                   #the annotation data 
│  ├─ event                     #an event in the annotation, defined by the time it started, rounded to nearest 0.1s*
│  │  ├─ annotation tier        #an annotation tier, can be either "participant", "operator", "production_annotation", "confidence_production" or "backchannels"
│  │  │  ├─ begin               #time for the beginning of the annotation
│  │  │  │  ├─ hhmmssddd        #time expressed as hours:minutes:seconds.milliseconds (str)
│  │  │  │  ├─ hhmmssff         #time expressed as hours:minutes:seconds.frames (str)
│  │  │  │  ├─ msec             #time expressed in milliseconds (int)
│  │  │  │  ├─ sec              #time expressed in seconds and up to three decimal seconds (float)
│  │  │  ├─ duration            #the duration of the annotation
│  │  │  │  ├─ ...              #same expressions of time as in "begin"
│  │  │  ├─ end                 #the end of the annotation
│  │  │  │  ├─ ...              #same expressions of time as in "begin"
│  │  │  ├─ value               #the annotation value, either a number, a series of words, or an empty string (str)
│  │  ├─ annotation tier        #possible additional annotation tier
│  │  │  ├─ ...                 #contains "begin", "duration", "end", and "value"
│  │  ├─ annotation tier        #possible additional annotation tier
│  │  │  ├─ ...                 #contains "begin", "duration", "end", and "value"                 
│  ├─ event                    
│  │  ├─ ...                    #an event can have five tiers of annotations, in practise it should have either 1, 2, or 3
│  ├─ event/
│  │  ├─ ...
│  ├─ ...                       #one session contains many events
|
|                               #everything bellow is general data about the session, conditions of the experiment, survey results etc
|
├─ anonymised_id                #the id of the anonymised files (str)
├─ condition                    #the operator condition, either "robot" or "human" (str)
├─ dilemma                      #the dilemma discussed during this session (str)
├─ engagement_condition          #the operator engagement level either "low", "normal", or "high" (str)
├─ opinion_change               #the amount of change in opinion after the session, can be either "more_against", "no_change", or "more_pro" (str)
├─ rating1                      #the rate of agreement before the session rated 1-4 (str)
├─ rating2                      #the rate of agreement after the session rated 1-4  (str)
├─ operator_opinion             #opinion held by the operator during the conversation either "against", "neutral" or "pro" (str)
├─ run                          #which session with the subject 01-03   (str)
├─ subject_id                   #the subject id number for the experiment 01-55 (str)

*NOTE: although the starting time fore any event will be the same for all annotation tiers within it,
    it does NOT mean that the ending time and duration of those annotations will be the same.
    tiers in different events may overlap in time.















when these data files were made, 
angels wept over their beauty,
and the poets wrote prose,
and the bards sang songs ,
and Ozimandias said "look upon my work ye mighty and dispair" before seeing these files and quickly erased the words. 