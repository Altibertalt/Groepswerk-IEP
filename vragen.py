## Questions groupproject

##############################
## 1. Trialhandler vs numpy ##
##############################

learning_trials = data.TrialHandler(learning_trial_list, nReps= nBlocks_training, method="random")
# and later on using addData
# or is it beter to use numpy stacking & repeat?
...
accuracy_response = numpy.repeat(accuracy, len(experiment_stimuli))
experiment_array = numpy.column_stack([experiment_stimuli, rule_stimuli, cor_resp, accuracy_response])



##################################################
## 2. Different approach to typing and deleting ##
##################################################

# String vs list approach
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

# VS #

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



##########################
## 3. Wait for response ##
##########################

# using maxWait param on waitkeys
response = event.waitKeys(keyList = ["f","j"], maxWait = 6)
# vs using clocks
timer = core.Clock()
timer.reset()
timer.add(TEST_TRIAL_TIME_PRESENTATION)

while timer.getTime() < 0:
    break



####################################################
## 4. Are there issues in using multiple addLoops ##
####################################################
thisExp.addLoop(learning_trials)
thisExp.addLoop(test_trials)