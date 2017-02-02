from numpy.random import permutation
from random import choice
from psychopy import visual, core, event, logging
from optparse import OptionParser

######################################################################################################
#  Option Parser
######################################################################################################
parser = OptionParser()

parser.add_option("--list", dest="List", type="string", help="which list is our participant running?", default=None)
parser.add_option("--SubjNo", dest="SubjNo", type="string", help="What participant number?", default=None)
(options, args) = parser.parse_args()

assert options.List is not None # Forgot the List Argument
assert options.SubjNo is not None # Forgot the SubjNo Argument

######################################################################################################
#  Run Time Functions
######################################################################################################
# Make window and clock
w = visual.Window(units='deg', monitor='testMonitor', fullscr=True, waitBlanking=False)
w.setMouseVisible(False)

event.Mouse(visible=False)
expTime = core.Clock()

# Check diagnostics
msPframe = w.getMsPerFrame()
assert msPframe[0] < 8 # The frame rate is off!!!
print msPframe
print w.getActualFrameRate()

# Stories should load now
def loadStory(loc):
    with open(loc) as f:
        story = f.readlines()
    return story[0].decode('utf-8')

sentence = 'I am not a happy man. Humanity does not ask us to be happy. It merely asks us to be brilliant on its behalf. Survival first, then happiness as we can manage it.'
practice = 'Life is to be lived, not controlled; and humanity is won by continuing to play in face of certain defeat.'
practice2 = 'We were the people who were not in the papers. We lived in the blank white spaces at the edges of print. It gave us more freedom. We lived in the gaps between stories.'
island = loadStory('Stories/Island.txt')
up = loadStory('Stories/UP.txt')
sharper = loadStory('Stories/Sharper.txt')
grammar = loadStory('Stories/Grammar.txt')

MS = 150
ExpList = {'1': [('island', 0, MS, True), [('up', 1, MS, False), ('sharper', 1, MS, True), ('grammar', 5, MS, True)]],
           '2': [('up', 0, MS, True), [('island', 5, MS, True), ('sharper', 1, MS, False), ('grammar', 1, MS, True)]],
           '3': [('sharper', 0, MS, True), [('island', 1, MS, True), ('up', 5, MS, True), ('grammar', 1, MS, False)]],
           '4': [('grammar', 0, MS, True), [('island', 1, MS, False), ('up', 1, MS, True), ('sharper', 5, MS, True)]] }

fix = []
sylalphabet = ['@', '#', '$', '%', '&', '@', '#', '$', '%', '&', '@', '#', '$', '%', '&']
alphabetA = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
alphabet = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
for _ in xrange(100):
    p = permutation(alphabet)[0:14]
    fix.append(visual.TextStim(w, text=''.join(p), color='black'))

queries = {'up': [(1, 'Was it fall when Nicholas White was trapped in an elevator?', 'y'),
                  (2, 'When Nicholas pulled the emergency button out, did the alarm stop?', 'n'),
                  (3, 'Did Nicholas have two rolaids with him in the elevator?', 'y'),
                  (4, 'Did the elevator in the McGraw Hill building free fall in 1945 due to a plane crash?', 'n'),
                  (5, 'Did a woman die in an elevator free fall because the hydraulic truncheon gave out?', 'n'),
                  (6, 'Can an elevator crash at the top of the shaft when equiptment lodges in the break?', 'y'),
                  (7, "Did Nicholas' aural hallucinations tell him he was going to die?", 'n'),
                  (8, 'Do most elevator related deaths result from airplane crashes?', 'y'),
                  (9, 'Do traction elevators hang from ropes?', 'y'),
                  (10, "Was there a fire in the elevators a week before Nicholas was trapped?", 'n')],
           'island' : [(1, "Was Jorgen's horse about to give birth?", 'n'),
                       (2, 'Was there a trapdoor at the top of the last ladder?', 'y'),
                       (3, 'Were the rotors on as Jorgen climbed the turbine?', 'n'),
                       (4, 'Do the farmers on Samso grow strawberries?', 'y'),
                       (5, 'According to the article, is the conventional attitude toward energy apathy?', 'y'),
                       (6, 'Before 2000, did the people of Samso get their electricity from hydroelectric plants?', 'n'),
                       (7, 'Can a weak acid harm reef building coral?', 'y'),
                       (8, 'Do snow melt and glacial runoff provide water for billions of people?', 'y'),
                       (9, 'Are the melting ice in West Virginia and the beetle infestations in Canada a result of global'
                        + 'warming?', 'n'),
                       (10, 'Are the Samsingers a proud, conservative, white-collar people?', 'n')],
           'sharper' : [(1, "Are most Master Bladesmith's chefs?", 'n'),
                        (2, 'To become a Master Bladesmith, does your knife have to cut rope before shaving arm hair?', 'y'),
                        (3, 'Are the two capabilities of a blade tested by the American Bladesmith Society, flexibility and sharpness?', 'n'),
                        (4, 'Did the knife Kramer made for Cook magazine cost $475?', 'y'),
                        (5, 'Do most Master Bladesmiths come from Japan?', 'n'),
                        (6, 'Was Kramer successful in landing a contract with La Sur despite his allergy to planning?', 'y'),
                        (7, 'Did Kramer meet with a sailor at his shop in downtown Olympia?', 'n'),
                        (8, 'Does Kramer make about five knives a week?', 'y'),
                        (9, 'Is cutting paper an irreplicable feat of a master bladesmith?', 'n'),
                        (10, 'Can Kramer work without a pyrometer?', 'y')],
           'grammar' : [(1, 'According to the article, is NASDAQ surrounded by cars with bright colors and custom license plates?', 'y'),
                        (2, 'Was Gears of War the first game for Sony Playstation 3?', 'n'),
                        (3, 'Did CliffyB announce a sequel game weilding a replica weapon?', 'y'),
                        (4, 'Is CliffyB a clean cut entrepenuer with an occasional cowlick?', 'n'),
                        (5, 'Are video games founded upon transference of persona?', 'y'),
                        (6, 'Does the article imply game developers are nocturnal, cavernous creatures?', 'y'),
                        (7, "Did CliffyB's parents throw parties without him?", 'n'),
                        (8, 'Does CliffyB drive slow because he just got a speeding ticket?', 'n'),
                        (9, 'Was CliffyB a pornstar before becoming a game design director?', 'n'),
                        (10, "Did CliffyB's dad die while Cliff was playing a Nintendo game?", 'y')]}

def nPaced(stori='sentence', n=5, ms=100, mask='True'):
    s = visual.TextStim(w, text='+', color='black')
    s.draw()
    w.flip()
    story = eval(stori)
    results = []
    tokens = story.split(' ')
    sentoken = [visual.TextStim(w, text=t, color='black') for t in tokens]
    trials = [tokens[i:i+n] for i in xrange(0, len(tokens), n)]
    stimuli = [sentoken[i:i+n] for i in xrange(0, len(sentoken), n)]
    if eval(mask):
        for s, text, stim in zip(range(len(trials)), trials, stimuli):
            for token in stim + [choice(fix)]:
                for i in xrange(int(ms/7)): # How many frames should the stim go up for
                    token.draw()
                    w.flip()
                    if i == 0: expTime.reset()
            rt = 1000*event.waitKeys(keyList=['space'], timeStamped=expTime)[0][1]
            event.clearEvents()
            results.append(', '.join([options.SubjNo, options.List, stori, str(n), mask, str(s), ' '.join(text).replace(',','').encode('ascii', 'ignore').decode('ascii'), str(rt)]))
    else:
        for s, text, stim in zip(range(len(trials)), trials, stimuli):
            for token in stim:
                for i in xrange(int(ms/7)): # How many frames should the stim go up for
                    token.draw()
                    w.flip()
                    if i == 0: expTime.reset()
            rt = 1000*event.waitKeys(keyList=['space'], timeStamped=expTime)[0][1]
            event.clearEvents()
            results.append(', '.join([options.SubjNo, options.List, stori, str(n), mask, str(s), ' '.join(text).replace(',','').encode('ascii', 'ignore').decode('ascii'), str(rt)]))
    return results

def Scroll(stori=sentence):
    story = eval(stori) + '\n Press ENTER when you are finished reading'
    reading = True
    s = visual.TextStim(w, text=story, color='black', wrapWidth=35, alignVert='top', pos=(0, 10))
    expTime.reset()
    while reading:
        s.draw()
        w.flip()
        key, rt = event.waitKeys(keyList=['up','down', 'return'], timeStamped=expTime)[0]
        if key == 'return':
            reading = False
        if key == 'down':
            s.pos += (0, 1)
        if key == 'up':
            s.pos += (0, -1)
    return [', '.join([options.SubjNo, options.List, stori, '0', 'False', '0', stori, str(1000*rt)])]

def Instruct(text=''):
    s = visual.TextStim(w, text=text, color='black', wrapWidth=35)
    s.draw()
    w.flip()
    instructing = True
    while instructing:
        key = event.waitKeys(keyList=['return'])[0]
        if key == 'return':
            instructing = False


def Questions(story):
    acc = []
    for itemNo, item, correct in permutation(queries[story]):
        listening = True
        s = visual.TextStim(w, text=item, color='black', wrapWidth=35)
        i = visual.TextStim(w, text='Press (Y for Yes) or (N for No)', pos=(0,-10))
        expTime.reset()
        while listening:
            s.draw()
            i.draw()
            w.flip()
            key, rt = event.waitKeys(keyList=['y', 'n'], timeStamped=expTime)[0]
            if key == 'y':
                acc.append(', '.join([options.SubjNo, options.List, story, str(itemNo), str(rt), str(correct=='y')]))
                listening = False
            if key == 'n':
                acc.append(', '.join([options.SubjNo, options.List, story, str(itemNo), str(rt), str(correct=='n')]))
                listening = False
    return acc
######################################################################################################
#  Run Time Code
######################################################################################################
ACC = ['SubjNo, List, Story, ItemNo, RT, ACC']
RT = ['SubjNo, List, Story, PerPress, Mask, Position, Text, RT']
stimuli = ExpList[options.List]

# Present scroll story
Instruct('First, we are going to ask you to read a passage of text. Use the up and down arrow keys to scroll. '
         + 'When you are finished reading, press Enter. You will then be asked comprehension questions.' +
         '\n\n To Begin press ENTER')
data_1_rt = Scroll(stimuli[0][0])
data_1_q = Questions(stimuli[0][0])

RT.extend(data_1_rt)
ACC.extend(data_1_q)

Instruct('In this next section, you will be reading a passage presented to you word by word in the middle of the '
    + 'screen very quickly. When you press the spacebar a sequence of words will appear followed by a string of '
    + 'random uppercase letters. To see the next sequence of words from the passage, press the spacebar again. '
    + 'Once you have finished the passage, you will be asked comprehension questions.')

for s, n, ms, mask in [('sentence', 1, 250, 'True'),('practice', 1, 200, 'True'),('practice2', 1, 175, 'True')] + list(permutation(stimuli[1])):
    if s in ['sentence','practice','practice2']:
        Instruct('Now we will do a practice trial. Press ENTER to continue.')
        rt = nPaced(s, n=int(n), ms=int(ms), mask=mask)
        RT.extend(rt)
    elif mask:
        Instruct('Please go find your experimenter to continue the experiment :)')
        Instruct('In this next section, you will be reading a passage presented to you word by word in the middle of the '
        + 'screen very quickly. When you press the spacebar a sequence of words will appear followed by a string of '
        + 'random lowercase letters. To see the next sequence of words from the passage, press the spacebar again. '
        + 'Once you have finished the passage, you will be asked comprehension questions.')
        rt = nPaced(s, n=int(n), ms=int(ms), mask=mask)
        acc = Questions(s)
        ACC.extend(acc)
        RT.extend(rt)
    else:
        Instruct('Please go find your experimenter to continue the experiment :)')
        Instruct('In this next section, you will be reading a passage presented to you word by word in the middle of the '
        + 'screen very quickly. When you press the spacebar a word will appear. '
        + 'To see the next word from the passage, press the spacebar again. '
        + 'Once you have finished the passage, you will be asked comprehension questions.')
        rt = nPaced(s, n=int(n), ms=int(ms), mask=mask)
        acc = Questions(s)
        ACC.extend(acc)
        RT.extend(rt)
    

with open('Data/RT_List_'+options.List+'_Subj_'+options.SubjNo+'.csv', 'w') as f:
    f.write('\n'.join(RT))

with open('Data/ACC_List_' + options.List + '_Subj_' + options.SubjNo + '.csv', 'w') as f:
    f.write('\n'.join(ACC))

w.close()
core.quit()

