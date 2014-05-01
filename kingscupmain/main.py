"""
IMPORTANT: this requires the deck module I wrote for python to be in python/lib/deck.  
I've included it in the repos until I figure out how to have it populate automagically

notes for the potential pre-pre-pre-pre-pre-alpha tester:

This is a game that emulates a deck of cards and manages a game of king's cup 
(also known as Circle of Death, Ring of Fire, Heroes, being an undergrad)
while adding some extra functionality and convenience features.

Things that are coming once the basics are sorted out:
Randomized rules: 'Irish roulette' and 'random player drinks' rules that are hard 
to implement w/o a computer handy

Minigames: The only one I've thought of so far I'm calling 'Disarm the bomb'...
the players are each prompted, round robin, to enter increasingly long and complicated
random alphanumeric strings, on a timer.  First one to have the bomb 'explode' before 
finishing must drink

Powerups: Players will be able to recieve powerups such as 
shield (defends against one drink)
sniper(gives one drink to whomever when you want)
mirror(returns a given drink to sender)
generosity!(can be used to force everyone to drink)
you get the idea...

Rule Administration:
Some rules can be directed and managed by the computer, so you can keep playing well 
past the point where you forget how to math.  These include but are not limited to...
Pick a mate - the program prompts you to select another player from a list, and if it knows 
you have to drink, it will tell them to do so as well.
Make a rule - if you want the game to remember your rules for you (esp. in the case of 'captain dickhead')
it will provide the player with an input and remember the rule for you.
Most likely to - instead of having pointing fingers, there will be an option to 'vote silently' by passing the phone
around.

Finally, there are going to be icons and other graphical updates later on.  The cut circle you see on the game screen will
rotate based on whose turn it is (and the size of the gap will be determined by the number of players)

anyway, I'm open to any and all suggestions, sorry for the rambling (and practically uninformative) docstring.   cheers, m8s!
"""

from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from deck import Deck
from kivy.uix.spinner import SpinnerOption
from kivy.factory import Factory
from kivy.graphics import Color
from kivy.base import runTouchApp
from kivy.config import Config

settings = JsonStore('settings.json')


settings['general'] = {'current profile' : '1', 'number of players' : 8}

settings['playernames'] = {}

if 'rules' in settings:

    print 'RULES FOUND IN SETTINGS'

else:

    print'RULES NOT FOUND IN SETTINGS, SETTING THE SETTINGS LOLOLOLOLOLOL'


    settings['rules'] = {
            'waterfall' : 'The current player starts drinking. Everyone must begin drinking when the person to their right begins, and may only stop when the person to their right puts down their glass.',
            'give 1': 'Current player hands out a drink',
            'give 2' : 'Current player hands out 2 drinks as they choose',
            'give 3' : 'Current player hands out 3 drinks as they choose',
            'reach for the sky' : 'All players put a hand up in the air.  Last one to do so takes a drink',
            'touch the table' : 'All players put a hand on the table (or floor).  Last one to do so takes a drink.',
            'touch your nose' : 'All players touch their noses.  Last one to do so must take a drink.',
            'pick a mate' : 'Current player picks a "mate".  Any time current player drinks for the rest of the game, mate must join them in drinking.',
            'going on a picnic' : 'We\'re going on an alphabetical picnic! Current player brings something beginning with \'A\'. Player to the left repeats this and adds something beginning with \'B\'.  This continues until alphabet is exhausted (everybody drinks) or someone screws up (that player drinks).',
            'make a rule' : 'Current player makes a rule, which will be in effect until the end of the game.  Internet points for more ridiculous rules.',
            'guys drink' : 'All players with a Y chromosome drink',
            'girls drink' : 'All players the same gender as their mothers drink',
            'social' : 'All players, regardless of race, gender, or creed, drink.',
            'nickname' : 'Current player assigns a nickname to any other player.  Any time that player is referred to as anything other than said nickname the offender must drink.',
            'spelling bee' : 'Current chooses a word and picks someone who must spell it.  If they succeed, current player drinks.  If they fail, they must drink (and reattend primary school).',
            'hot seat' : 'Current player is in the hot seat!  All other players ask them one question (the more intrusive and personal the better).  For each question, they either answer or drink.',
            'most likely to' : 'Current player picks a \'most likely to\' (become a crazy cat person, puke tonight, date their sibling).  All players point to the person they believe is most likely to do this thing - then everyone drinks an amount equal to the fingers pointing at them.',
            'international house' : 'Each player adopts an accent (not their own / native accent) for the rest of the game.  Any player to break character must drink (but may resume normal speech.)',
            'reverse rotation' : 'Play reverses order.',
            'slow motion' : 'Welcome to the Matrix!  All players move at half speed, and the first to break the momentum drinks.',
            'staring contest' : 'Current player picks someone and a staring contest begins.  First to break eye contact must drink.  Play may continue, but does not end the staring contest (only the shame of failure can do that).',
            'moose' : 'All players make moose antlers with their hands.  Last to do so drinks.',
            'all hail captain dickhead' : 'Current player is now Captain Dickhead!  You may make up any rules you like, at any time, with no restrictions.  These rules are in effect until the next Captain is chosen, at which time they expire.',
            '7 is fuck you' : 'Starting with the current player, players count in sequence from one.  Any time a number that\'s a multiple of seven is called, it must be replaced with \'fuck you\'.  First to screw up drinks.  Internet points for going fast.',
            'snake eyes' : 'Current player has the magic snake eyes!  Gazing directly into these eyes for the rest of the game means you must drink.',
            'never have i ever' : 'All players hold up three fingers.  Starting with current player and continuing to the left, players state something they have never done; any players that have done this lower a finger.  First person to drop all three drinks.',
            'thrift tranny' : 'All players exchange an article of clothing with a member of the opposite sex.  No trading back; all outgoing articles must be your own. (If there is a gender inbalance, some players may opt out by taking a drink.)',
            'shuffle' : 'All players take new seats before play continues.  Play resumes to the left of the current player.',
            'chinese fire drill' : 'All players run once around the table and sit in the next seat down from them (the seat to the left of their original seat.) Last to sit down drinks, and play continues to the left of the current player (they do not go twice).',
            'strip' : 'All players remove an article of clothing.  Hats, jewelry, and watches do not count.  Shoes, socks, and any other \'paired\' items must be removed together (as if they were one item).',
            'jackass' : 'Hee-Haw! Current player is now the Jackass, and must drink any time another player drinks (drink does not stack with \'everybody drinks\' rules).',
            'questions' : 'Current player asks a player of their choosing a question.  That player turns to someone else and asks another question - this continues until someone screws up (answers a question or makes a statement in the form of a question).  The offending player drinks.',
            'categories' : 'Current player picks a category (i.e. makes of car, beers, sexual positions).  Starting with the current player and continuing left, players name things in that category until someone screws up (repeats something said before, says something not in that category, can\'t think of something). Offending player drinks.',
            'question master' : 'Current player is now the Question Master!  Any time the Q.M. asks another player a question, they must drink if they answer it.',
            'kings cup' : 'Current player adds their drink to the King\'s Cup in the middle.',
            'magic thumb' : 'Current player\'s thumb is now imbued with the power to compel others! Any time your thumb touches the table, others must place their thumb on the table, and the last one to do so must drink.' 
            }

    settings['profiles'] = {'1' : {'1':'moose',
                                '2':'questions',
                                '3':'slow motion',
                                '4':'all hail captain dickhead',
                                '5':'guys drink',
                                '6':'girls drink',
                                '7':'social',
                                '8':'nickname',
                                '9':'international house',
                                '10':'magic thumb',
                                '11':'waterfall',
                                '12':'question master',
                                '13':'kings cup'}}


currentprofile = '1'

#players business to follow

players = []

print 'PRINTING SETTINGS'

print settings

for i in settings:
    print i
    print settings[i]

Builder.load_file('kingscup.kv')


class MainMenu(Screen):

    class MeatSpin(SpinnerOption):
        background_color = [1,1,1,0.35]
        color = [0.001,0.5,0.75,1]
        
    def startbutt(*args):
        sm.current = 'gamestart'

    def settingsbutt(*args):
        sm.current = 'settingsscreen'


class GameStart(Screen):

    settings = JsonStore('settings.json')

    rules = settings['rules']

    profiles = settings['profiles']

    currentprofile = settings['general']['current profile']

    def setplayers(self,number,*args):
        settings['general']['number of players'] = number
        print 'PLAYERS SET TO' + str(settings['general']['number of players'])

    def grp(self, card, *args):
        return settings['profiles'][settings['general']['current profile']][card]
    
    class MeatSpin(SpinnerOption):
        background_color = [1,1,1,0.35]
        color = [0.001,0.5,0.75,1]
        
    def startgame(*args):
        sm.current = 'playerscreen'

    def navsettings(*args):
        sm.current = 'settingsscreen'

 

class PlayerScreen(Screen):

    playiter = 1

    def rotwheel1(self, *args):
        print 'DRAWING playwheel WITH' + str(settings['general']['number of players']) + 'SEGMENTS'
        return ((self.playiter - 1) * (360 / settings['general']['number of players']))

    def rotwheel2(self, *args):
        return (self.playiter * (360 / settings['general']['number of players']))

    def enterplayer(self, number, name, *args):
        playlist = settings['playernames']
        playlist[str(number)] = str(name)
        settings['playernames'] = playlist
        print 'player ' + str(number) + 'added as ' + str(name)

    def startgame(*args):
        sm.current = 'gamescreen'

    def iterplay(self, *args):
        if self.playiter <= settings['general']['number of players']: 
            self.playiter +=1

        else: 
            startgame()
       
class GameScreen(Screen):

    def getrule(self, name, *args):
        rul = settings['rules']
        return rul[name]

    suits = {1:'spades',
             2:'clubs',
             3:'hearts',
             4:'diamonds',
             5:'joker'
             }

    faces = {
            1 : '2',
            2 : '3',
            3 : '4',
            4 : '5',
            5 : '6',
            6 : '7',
            7 : '8',
            8 : '9',
            9 : '10',
            10 : 'Jack',
            11 : 'Queen',
            12 : 'King',
            13 : 'Ace',
            }


    class MeatSpin(SpinnerOption):
        background_color = [1,1,1,0.35]
        color = [0.001,0.5,0.75,1]

    def quitgame(*args):
        sm.current = 'mainmenu'
        #this function needs to be implemented

    def menubutt(*args):
        sm.current = 'mainmenu'

    def settingsbutt(*args):
        sm.current = 'settingsscreen'

    def endgame(*args):
        ##WHAT DO I DO HEEEEERE?
        grflmrghhbr = 1

    def grp(self, card, *args):
        print 'Getting ' + str(card) + ' rule from profile ' + str(settings['general']['current profile'])
        return settings['profiles'][settings['general']['current profile']][card]

    deck = Deck()
    currentcard = [1,5]

    def drawacard(self,*args):

        if len(self.deck.drawpile) <= 0:

            #put the func to display the endgame popup here
            sm.current = 'mainmenu'
        
        else:

            return self.deck.drawcard()
        



class SettingsScreen(Screen):

    def getrule(self, name, *args):
        rul = settings['rules']
        return rul[name]

    #get rule from profile
    def grp(self, card, *args):
        return settings['profiles'][settings['general']['current profile']][card]

    #set rule to profile
    def srp(self, card, rule, *args):
        print ('SAVING RULE %s' %rule)
        settings['profiles'][settings['general']['current profile']][card] = rule
        print  'Rule is now: '
        print settings['profiles'][settings['general']['current profile']][card]

    facevalues = {
        '2':'1',
        '3':'2',
        '4':'3',
        '5':'4',
        '6':'5',
        '7':'6',
        '8':'7',
        '9':'8',
        '10':'9',
        'Jack':'10',
        'Queen':'11',
        'King':'12',
        'Ace':'13',
        }

    def menubutt(*args):
        sm.current = 'mainmenu'

    def startbutt(*args):
        sm.current = 'gamestart'  

    deck = Deck()

    ruleslist = (
        'waterfall' ,
        'give 1' ,
        'give 2' ,
        'give 3' ,
        'reach for the sky' ,
        'touch the table' ,
        'touch your nose' ,
        'pick a mate' ,
        'going on a picnic' ,
        'make a rule' ,
        'guys drink' ,
        'girls drink' ,
        'social' ,
        'nickname' ,
        'spelling bee' ,
        'hot seat' ,
        'most likely to' ,
        'international house' ,
        'reverse rotation' ,
        'slow motion' ,
        'staring contest' ,
        'moose' ,
        'all hail captain dickhead' ,
        '7 is fuck you' ,
        'snake eyes' ,
        'never have i ever' ,
        'thrift tranny' ,
        'shuffle' ,
        'chinese fire drill' ,
        'strip' ,
        'jackass' ,
        'questions' ,
        'categories' ,
        'question master' ,
        'kings cup' ,
        'kings cup final',
        'magic thumb' 
        )
           
    class MeatSpin(SpinnerOption):
        background_color = [1,1,1,0.35]
        color = [0.001,0.5,0.75,1]

class MeatText(Label):
    def __init__(self, **kwargs):        
        self.background_color = [0,0,0,0]
        self.color = [0.001,0.5,0.75,1]
        self.font_size = 14
        self.bold = True
        super(MeatText, self).__init__(**kwargs)
    def update_self(self,*args):
        print 'updating label textures...'
        super(MeatText, self).texture_update(*args)


class MeatButt(Button):
    def __init__(self, **kwargs):        
        self.background_color = [0,0,0,0]
        self.color = [0.001,0.5,0.75,1]
        self.font_size = 14
        self.bold = True
        super(MeatButt, self).__init__(**kwargs)


sm = ScreenManager()
sm.add_widget(GameScreen(name = 'gamescreen'))
sm.add_widget(GameStart(name = 'gamestart'))
sm.add_widget(SettingsScreen(name = 'settingsscreen'))
sm.add_widget(MainMenu(name = 'mainmenu'))
sm.add_widget(PlayerScreen(name = 'playerscreen'))
sm.current = 'mainmenu'

class Play(App):

    def __init__(self,**kwargs):
        super(Play, self).__init__(**kwargs)

    def build(self):
        return sm
 
if __name__ == '__main__':
    Play().run()
