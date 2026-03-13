.json files structure:

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
|                               #everything below is general data about the session, conditions of the experiment, survey results, etc
|
├─ anonymised_id                #the id of the anonymised files used during the annotation process (str)
├─ condition                    #the confederate condition, either "robot" or "human" (str)
├─ dilemma                      #the dilemma discussed during this session (str)
├─ engagment_condition          #the confederate's engagement level either "low", "normal", or "high" (str)
├─ opinion_change               #the amount of change in opinion after the session, can be either "more_against", "no_change", or "more_pro" (str)
├─ rating1                      #the rate of agreement before the session rated 1-4 (str)
├─ rating2                      #the rate of agreement after the session rated 1-4  (str)
├─ operator_opinion             #opinion held by the confederate during the conversation, can be either "against", "neutral" or "pro" (str)
├─ run                          #which session with the subject 01-03   (str)
├─ subject_id                   #the subject id number for the experiment 01-55 (str)

*NOTE: Although the starting time for any event will be the same for all annotation tiers within it, it does NOT mean that the ending time and duration of those annotations will be the same. Tiers in different events may overlap in time.
