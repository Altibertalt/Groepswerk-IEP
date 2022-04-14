from psychopy import visual, core, data, event, gui
import time, os

# file management + participant info

## set my directory
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

## initialize the participant information dialog box
info = {"Participant name":"", "Participant number":0, "Age":0, "Gender":["male", "female", "third gender"]}

## make sure the data file has a novel name
already_exists = True
while already_exists:
    
    ## present the dialog box
    my_dlg = gui.DlgFromDict(dictionary = info, title = "Lexical Grammar Task")
    
    ## construct the name of the data file
    file_name = dir_path + "/Lexical_Grammar_Task" + str(info["Participant number"])
        
    ## check whether the name of the data file has already been used
    if not os.path.isfile(file_name + ".csv"):
        
        ## if there isn't a data file with this name used yet, we're ready to start
        already_exists = False
        
    else:
        
        ## if the data file name has already been used, ask the participant to inser a different participant number
        my_dlg2 = gui.Dlg(title = "Error")
        my_dlg2.addText("Try another participant number")
        my_dlg2.show()

## extract the name of the participant from the dialog box information
subject_name = info["Participant name"]
## remove the name of the participant from the dialog box information (anonimity!)
info.pop("Participant name")

## experimentHandler + output info 
thisExp = data.ExperimentHandler(dataFileName = file_name, extraInfo = info)

# define constants 
nBlocks_training = 2
nblocks_test = 1
responses = ["f","j"]
duration_learning = 3
duration_test = 6
duration_feedback = 0.25

# import conditions
input_learning_fase = "learning_phase.csv"
learning_trial_list = data.importConditions(input_learning_fase)
input_testing_fase = "test_phase.csv"
test_trial_list = data.importConditions(input_testing_fase)

# making the trailhandlers 
learning_trials = data.TrialHandler(learning_trial_list, nReps= nBlocks_training, method="random")
print(learning_trials)
test_trials = data.TrialHandler(test_trial_list, nReps= nblocks_test, method="random") 
print(test_trials) 
thisExp.addLoop(learning_trials)
thisExp.addLoop(test_trials)

#initialize window 
win = visual.Window((600,600), color="black")

# graphic elements 
msg = visual.TextStim(win, text="", color="white", pos=(0,0))
welcome_text = "Welcome to the experiment. Press the spacebar to continue."
practice_text = ("We will start with a learning phase. Then, you will be presented with a sequence of letters.\n" +
                "You are supposed to repeat the sequence you just saw. Use the keyboard for your response and \n" + 
                "press enter when you finished typing your answer. Press space to start ")
experiment_text = ("Now the real experiment will start. The sequences you will ee get generated following a specific rule.\n" +
                "This time you are supposed to indicate for each sequence whether it is generated based on the same rule as \n" + 
                "the training set (press f) or based on another rule (press j). Press space to start the experiment.")
goodbye_text = "Thank you for participating! Press space to leave the experiment."
correct_text = "Correct answer!"
wrong_text  = "Wrong answer!"

# Definition to draw text on screen
def showText(text):
    msg.text = text
    msg.draw()
    win.flip()

# the experiment
showText(text = welcome_text)
event.waitKeys(keyList = "space")

# learning trials loop 
showText(text = practice_text) 
event.waitKeys(keyList = "space")
for trial in learning_trials:
    
    correct = 0 
    while correct == 0   :
    
        # stimulus on screen 
        showText(text = trial["LearningStim"])
    
        # 3 seconden tonen
        time.sleep(duration_learning)
        event.clearEvents(eventType = "keyboard")

        showText(text = "Give answer")

        keys = []
        while "return" not in keys:
            key = event.waitKeys(keyList = None)
            keys.append(key[0])
            # use backspace for deleting an answer 
            if "backspace" in keys:
                del keys[-2:]
            keylist_string = "".join(keys)
            showText(text = keylist_string)
        
        # Collect typed keys by PP
        keysAsString = "".join(keys[:-1]).upper() ## [:-1] => remove last ("return") elem from list
    
        # Compare response with stim
        if keysAsString == trial["LearningStim"]:
            showText(text="correct")
            correct = 1
        else:
            showText(text="wrong!")
            correct = 0 ## set to 0 if you want to repeat trial
    
    time.sleep(duration_feedback)
    
showText(text = experiment_text)
event.waitKeys(keyList = "space")

# test_phase 
for trial in test_trials:
    
    # stimulus on screen 
    showText(text = trial["TestStim"])
    
    # clear keyboard 
    event.clearEvents(eventType = "keyboard")
    
    # wait for response (6 sec) 
    response = event.waitKeys(keyList = responses, maxWait = 6)
    print(response) 
    
    # feedback + accuracy
    if response == ["j"]:
        CorResp = 0 #not rule based
    else: 
        CorResp = 1 # rulebased
    
    # feedback (accuracy) 
    if CorResp == trial["Rulebased"]:
        showText(text = "Correct")
        # trials.addData("ACC", 1)
    else:
        showText(text = "Wrong!") 
        #trials.addData("ACC", 0)
    time.sleep(duration_feedback)

# end experiment
core.quit()
win.close() 