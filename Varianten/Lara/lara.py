from psychopy import visual, event, core, data
import pandas, numpy, os, random

##initialize window

win = visual.Window (size = (700,1000), color = [1,1,1], units = "norm")
my_directory = os.getcwd()

##define graphical elements

message_template = visual.TextStim (win, text = "")

##define function for the messages

def message(message_text = "", response_key = "space", duration = 0, height = None, pos = (0.0, 0.0), color = "black"):
    
    message_template.text    = message_text
    message_template.height  = height
    message_template.pos     = pos
    message_template.color   = color
    
    message_template.draw()
    win.flip()
    if duration == 0:
        event.waitKeys(keyList = response_key)
    else:
        core.wait(duration)
##initilize message text

welcome_text = "Welcome to the experiment. Press the spacebar to continue"
practice_text = "We will start with a practice phase. You will be presented with a sequence of letters. You are than supposed to repeat the sequnce you just saw. Use the keyboard for your response and press enter when you finished typing your answer. Press space to start the practice phase"
experiment_text = "Now the real experiment will start. The sequences you will ee get generated following a specific rule. This time you are supposed to indicate for each sequence whether it is generated based on the same rule as the training set (press f) or based on another rule (press j). Press space to start the experiment."
goodbye_text = "Thank you for participating! Press space to leave the experiment."
correct_text = "Correct answer!"
wrong_text  = "Wrong answer!"
n_experiment_blocks = 1

##initialize stimulus attributes

practice_stimuli = ["PVV","TXS", "TSXS", "PTTVV", "PTVPS", "PVPXVV", "TSSSXS", "TXTVPS", "PTTTVPS", "PTVPXVV", "PVPXVPS", "TSSXXVV", "TSXXTVV", "TXXTVPS", "PVPXTVPS", "TSSSXXVV", "TSSXXVPS", "TSXXTVPS", "TXXTTTVV", "TXXVPXVV"]
n_practice_stimuli = len(practice_stimuli) 
n_practice_blocks = 1
experiment_stimuli = ["PVV" , "TXS" , "TPVV" , "PVPS" , "TSSXS" , "TXXVV" , "PTTTVV" , "PTTVPS" , "TXXTVV" , "PVPXVV" , "TSXXVV" , "TXXTVPS" , "TSXXVPS" , "TXXTTVV" , "TSSSSXS" , "PTTTTVPS" , "TSXXTTVV" , "TSSXXTVV" , "PTTTTTVV" , "PVPXTTVV" , "PTTVPXVV" , "TSXXTVPS", "PVPXTVPS", "PTVPXVPS", "TSSXXVPS", "TXV", "TTVV", "PSXS", "TXPV", "PVTVV", "PTTPS", "XXSVT", "TXXVX", "TXVPS", "TPTXS", "PTTTVT", "TSXXPV", "SXXVPS", "PTVVVV", "VPXTVV", "PTVPPPS", "SVPXTVV", "PVTTTVV", "VSTXVVS", "TXXTVPT", "PTTTVPVS", "TSSXXVSS", "PVXPVXPX", "PTVPXVSP", "PXPVXVTT"]
n_experiment_blocks = 1
n_experiment_stimuli = len(experiment_stimuli)
rules = [0,1]
response = ["f", "j"]
accuracy = [-99]
rule_stimuli = numpy.repeat(rules, len(experiment_stimuli)/2)
cor_resp = numpy.repeat(response,len(experiment_stimuli)/2)
accuracy_response = numpy.repeat(accuracy, len(experiment_stimuli))
experiment_array = numpy.column_stack([experiment_stimuli, rule_stimuli, cor_resp, accuracy_response])


##same with data frame

experiment_design = pandas.DataFrame.from_records(experiment_array)
index = list(experiment_design.index)
numpy.random.shuffle(index)
experiment_design = experiment_design.iloc[index]
experiment_design.columns = ["stimulus", "rule", "corresp", "accuracy"]
experiment_list = pandas.DataFrame.to_dict(experiment_design, orient = "records") ##list consisting of dictionaries
test_trials = data.TrialHandler(trialList = experiment_list, nReps=1, method="sequential")
print(test_trials)

##greeting participant

message(message_text = welcome_text)

##present practice block

answer = []
for j in range(2):
    numpy.random.shuffle(practice_stimuli)
    message(message_text = "This is the beginning of the practice block {}. Press the spacebar to start.".format(j+1))
    for i in range(n_practice_stimuli):
        correct = False
        while correct == False: 
            answer.clear()
            message(message_text = practice_stimuli[i], duration = 2)
            message(message_text = "if you are ready to type your answer press space. Press return to submit your answer.", response_key = "space")
            event.clearEvents()
            while "return" not in answer:
                key = event.waitKeys()
                answer.append(key[0])
                if "backspace" in answer:
                    del answer[-2:]
                answer_string = "".join(answer).upper()
                message(message_text = answer_string, duration= 0.01)
                answer_comparison = "".join(answer[:-1]).upper()
            if answer_comparison == practice_stimuli[i]:
                message(message_text = correct_text, duration = 1)
                correct = True
            else:
                message(message_text = "Wrong! Try again.", duration = 1)
                correct = False

##experimental block

message(message_text = "This is the beginning of the experimental block. Press f if you think that the sequence is generated following the same rule as the practice stimuli. Press j if you don´t think so.")

for k in test_trials:
    event.clearEvents()
    stimulus = k["stimulus"]
    message(message_text = stimulus, duration = 0.01)
    response = event.waitKeys(keyList = ["f","j"], maxWait = 6)
    if response == None:
        response = "t"
    if response[0] == k["corresp"]:
        message(message_text = correct_text, duration = 1)
        k["accuracy"] = "correct"
    elif response[0] == "t":
        message(message_text = "too slow", duration = 1)
        k["accuracy"] = "too slow"
    else:
        message(message_text = wrong_text, duration = 1)
        k["accuracy"] = "wrong"
        
##say goodbye

message(message_text = goodbye_text)

##end the experiment

win.close()
