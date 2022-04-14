from psychopy import visual, core, data, event, gui
import os

## Constants
AMOUNT_OF_LEARNING_BLOCKS = 2
AMOUNT_OF_TEST_BLOCKS = 1
# Files
LEARNING_FILE_NAME = "learning_phase.csv"
TEST_FILE_NAME = "test_phase.csv"
LEARNING_TRIAL_TIME_PRESENTATION = 3
TEST_TRIAL_TIME_PRESENTATION = 6
# Text
EXPERIMENT_TEXT = {
    "welcome_text": "Welcome to the experiment. Press the spacebar to continue.",
    "learning_text": "We will start with a learning phase. Then, you will be presented with a sequence of letters.\n" +
                    "You are supposed to repeat the sequence you just saw. Use the keyboard for your response and \n" + 
                    "press enter when you finished typing your answer. Press space to start",
    "experiment_text": "Now the real experiment will start. The sequences you will ee get generated following a specific rule.\n" +
                "This time you are supposed to indicate for each sequence whether it is generated based on the same rule as \n" + 
                "the training set (press f) or based on another rule (press j). \nPress space to start the experiment.",
    "goodbye_text": "Thank you for participating! Press the spacebar to leave the experiment.",
    "correct_text": "Correct answer!",
    "wrong_text" : "Wrong answer!",
    "to_slow_text" : "To slow!",
}

# GUI to collect participant data
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
    OUTPUT_FILE_NAME = dir_path + "/Lexical_Grammar_Task" + str(info["Participant number"])
        
    ## check whether the name of the data file has already been used
    if not os.path.isfile(OUTPUT_FILE_NAME + ".csv"):
        
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

# Visual information
win = visual.Window()
textStim = visual.TextStim(win)

# Create timer
timer = core.Clock()

# Implement the ExperimentHandler
thisExp = data.ExperimentHandler(dataFileName = OUTPUT_FILE_NAME)

# Randomization
learning_trials_data = data.importConditions(LEARNING_FILE_NAME)
test_trials_data = data.importConditions(TEST_FILE_NAME)

learning_trials = data.TrialHandler(learning_trials_data, AMOUNT_OF_LEARNING_BLOCKS, method="random")
test_trials = data.TrialHandler(test_trials_data, AMOUNT_OF_LEARNING_BLOCKS, method="random")

# Link  both learning & test trials to the ExperimentHandler
thisExp.addLoop(learning_trials)
thisExp.addLoop(test_trials)

## Functions
def drawText(text):
    textStim.text = text
    textStim.draw()
    win.flip()

def setTextColorTo(color):
    textStim.color = color
    win.flip()

################
## EXPERIMENT ##
################
drawText(EXPERIMENT_TEXT["welcome_text"])
event.waitKeys(keyList="spacebar")

drawText(EXPERIMENT_TEXT["learning_text"])
event.waitKeys(keyList="spacebar")

# Learning logic
for trial in learning_trials:
    correctAnwser = False

    while correctAnwser is not True:
        trial_text = trial["LearningStim"]
        drawText(trial_text)

        core.wait(LEARNING_TRIAL_TIME_PRESENTATION)

        drawText("Type the text")

        # Show letters
        typed_response = ""
        while len(typed_response) < len(trial_text):
            pressed_key = event.waitKeys()[0]

            if pressed_key == "backspace":
                typed_response = typed_response[:-1]

            # Avoid special characters such as "return"
            if len(pressed_key) == 1:
                typed_response += pressed_key.upper()
            
            # Draw input
            drawText(typed_response)

        # Check if pressed enter
        event.waitKeys(keyList="return")

        if trial_text == typed_response:
            correctAnwser = True
        else:
            textStim.color = "red"
            drawText("incorrect, try again")
            core.wait(.6)
            setTextColorTo("white")

    thisExp.nextEntry()

drawText(EXPERIMENT_TEXT["experiment_text"])
event.waitKeys(keyList="spacebar")

# Test logic
for trial in test_trials:
    # Get trial info
    trial_info = trial["TestStim"].split(",")
    trial_text = trial_info[0]
    cor_resp = int(trial_info[1])
    
    # Show stimuli
    drawText(trial_text)

    # Countdown
    timer.reset()
    timer.add(TEST_TRIAL_TIME_PRESENTATION)
    
    responseValue = None
    responseKey = None
    respRT = None

    while timer.getTime() < 0:
        pressedKey = event.getKeys(keyList= ["f", "j"])

        if len(pressedKey) > 0:
            respRT = TEST_TRIAL_TIME_PRESENTATION - abs(timer.getTime())
            responseKey = pressedKey[-1]
            if responseKey == "f" and cor_resp == 0:
                responseValue = 1
            elif responseKey == "j" and cor_resp == 1:
                responseValue = 1
            else:
                responseValue = 0
            break

    # Draw feedback
    if responseValue ==  None:
        setTextColorTo("red")
        drawText(EXPERIMENT_TEXT["to_slow_text"])
    elif responseValue == 0:
        setTextColorTo("red")
        drawText(EXPERIMENT_TEXT["wrong_text"])
    elif responseValue == 1:
        setTextColorTo("green")
        drawText(EXPERIMENT_TEXT["correct_text"])
    core.wait(.25)
    setTextColorTo("white")

    # Data export
    thisExp.addData("stimuli_text", trial_text)
    thisExp.addData("response", respRT)
    thisExp.addData("correct_response", cor_resp)
    thisExp.addData("resp_accuracy", responseValue)
    thisExp.addData("resp_RT", respRT)

    thisExp.nextEntry()

drawText(EXPERIMENT_TEXT["goodbye_text"])
event.waitKeys(keyList="spacebar")

# Close experiment
win.close()
core.quit()