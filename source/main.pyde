from random import randint
class Card():
    def __init__(self,name,suit,whereX,whereY):
        self.name = name
        self.suit = suit
        self.whereX = whereX
        self.whereY = whereY
        self.valuedict = {"Ace":11,"2": 2,"3": 3,"4": 4,"5": 5,"6":6,"7":7,"8":8,"9":9,"10":10,"Jack":10,"Queen":10,"King":10}
    def giveValue(self):
        return self.valuedict[self.name]
    def changeValue(self):
        self.valuedict["Ace"] = 1
    def showCard(self,spotX,spotY):
        copy(allcards,self.whereX,self.whereY,79,123,spotX,spotY,79,123)


class Deck():
    def __init__(self):
        self.deck = [0 for i in range(52)]
        instructions = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]
        numcounter = 0
        suitslist = ["Spades","Clubs","Diamonds","Hearts"]
        suitsincrement = 0
        for i in range(52):
            if numcounter == 13:
                numcounter = 0
                suitsincrement += 1
            self.deck[i] = Card(instructions[numcounter],suitslist[suitsincrement],79*numcounter,123*suitsincrement)
            numcounter += 1

    def deal_one_card(self):
        card = self.deck[0]
        self.deck.pop(0)
        return card
    def shuffle(self):
        for i in range(len(self.deck)):
            tmp = self.deck[i]
            n = randint(0,len(self.deck)-1)
            self.deck[i] = self.deck[n]
            self.deck[n] = tmp

class Player():
    def __init__(self):
        self.bet = 0
        self.cards = []
        self.cash = 0
        self.reward = 0
    def addCard(self,card):
        self.cards.append(card)
    def resetCards(self):
        self.cards = []
    def Bet(self):
        self.cash -= self.bet
        self.reward = self.bet * 2
    def doubleReward(self):
        self.reward = self.reward * 2
    def collectReward(self):
        self.cash += self.reward
        self.reward = 0
        self.bet = 0
    def giveSum(self):
        adder = 0
        for card in self.cards:
            adder += card.giveValue()
        return adder
    def showCards(self,yval):
        for i in range(len(self.cards)):
            self.cards[i].showCard((300+(50*i)),yval)                
def setup():
    global allcards,cardback,mainplayer,gamedeck,phase,dealer,counter
    size(1200,800)
    allcards = loadImage("cards.png")
    cardback = Card("Back","Back",0,492)
    gamedeck = Deck()
    gamedeck.shuffle()
    mainplayer = Player()
    moneyfile = open("./usermoney.txt","r")
    startingmoney = ""
    for wordline in moneyfile:
        for character in wordline:
            startingmoney += character
    mainplayer.cash = int(startingmoney)
    moneyfile.close()
    dealer = Player()
    displaycard = cardback
    drewcard = False
    phase = 1
    counter = 0
    cursor(HAND)

def draw():
    global allcards,cardback,mainplayer,gamedeck,phase,dealer,counter
    background(0,100,0)
# ----- PLAYERS' HANDs -----------------------
    mainplayer.showCards(600)
    dealer.showCards(100)
# -------------------------------------------
    if phase == 1:  #BETTING PHASE
        stroke(0,255,0)
        fill(500,1000,200)
        ellipse(150,450,100,100) #-10000
        ellipse(300,450,100,100) #-5000
        ellipse(150,600,100,100) #-1000
        ellipse(300,600,100,100) #-500
        ellipse(450,600,100,100) #-100
        ellipse(600,600,100,100) #BET
        ellipse(750,600,100,100) #+100
        ellipse(900,600,100,100) #+500
        ellipse(1050,600,100,100) #+1000
        ellipse(900,450,100,100) #+5000
        ellipse(1050,450,100,100) #+10000
        textSize(30)
        text("WELCOME TO BLACKJACK",420,100)
        textSize(20)
        fill(255)
        text("Press Q to Save and Quit",10,30)
        text("PRESS SPACE TO GO ALL IN",450,250)
        text("PRESS BACKSPACE TO CLEAR BET",450,300)
        fill(0)
        text("-$10000",100,450)
        text("- $5000",260,450)
        text("- $1000",105,600)
        text("- $500",265,600)
        text("- $100",415,600)
        text("BET",585,600)
        text("+ $100",715,600)
        text("+ $500",865,600)
        text("+ $1000",1005,600)
        text("+ $5000",860,450)
        text("+$10000",1000,450)
    if phase == 2: #DRAWING CARDS AND DECISIONS PHASE
        cardback.showCard(350,100)
        summ = mainplayer.giveSum()
        if summ == 21:
            phase = 11
        while summ > 21:
                something_done = False
                for card in mainplayer.cards:
                    if card.name == "Ace" and card.giveValue() == 11:
                        card.changeValue()
                        something_done = True
                        summ = mainplayer.giveSum()
                        break
                if something_done == False:
                    phase = 5
                    break
        if len(mainplayer.cards) > 1:
            fill(500,1000,200)
            ellipse(900,500,100,100)
            fill(0)
            text("STAND",870,500)
    if phase == 3: #DEALER PLAYING PHASE
        if mainplayer.giveSum() >= 16:
            if (dealer.giveSum() < mainplayer.giveSum()) or (dealer.giveSum() > 21):
                dealer.addCard(gamedeck.deal_one_card())
                while dealer.giveSum() > 21:
                    something_done = False
                    for card in dealer.cards:
                        if card.name == "Ace" and card.giveValue() == 11:
                            card.changeValue()
                            something_done = True
                            break
                    if something_done == False:
                        phase = 6
                        break
            else:
                if dealer.giveSum() > mainplayer.giveSum():
                    phase = 7
                else:
                    phase = 8
                
        else:
            if (dealer.giveSum() <= mainplayer.giveSum()) or (dealer.giveSum() > 21):
                dealer.addCard(gamedeck.deal_one_card())
                while dealer.giveSum() > 21:
                    something_done = False
                    for card in dealer.cards:
                        if card.name == "Ace" and card.giveValue() == 11:
                            card.changeValue()
                            something_done = True
                            break
                    if something_done == False:
                        phase = 6
                        break
            else:
                phase = 7
            
                
    if phase == 5: #BUSTED PHASE
        if counter == 200:
            phase = 12
            counter = 0
        text("BUST",450,550)
        counter += 1
        
    if phase == 6: #DEALER BUSTED PHASE
        if counter == 200:
            phase = 11
            counter = 0
        text("DEALER BUSTED",450,300)
        counter += 1
    
    if phase == 7: #DEALER WON PHASE
        if counter == 300:
            phase = 12
            counter = 0
        text("DEALER STANDS",450,300)
        counter += 1
    if phase == 8: #TIE
        textSize(25)
        text("PUSH",450,550)
        counter += 1
        if counter == 200:
            mainplayer.cash += mainplayer.bet
            mainplayer.bet = 0
            mainplayer.reward = 0
            gamedeck = Deck()
            gamedeck.shuffle()
            mainplayer.resetCards()
            dealer.resetCards()        
            counter = 0
            phase = 1
        
            
    if phase == 11: #WON ROUND PHASE
        textSize(25)
        text("YOU WON",450,550)
        counter += 1
        if counter == 100:
            mainplayer.collectReward()
            gamedeck = Deck()
            gamedeck.shuffle()
            mainplayer.resetCards()
            dealer.resetCards()        
            counter = 0
            phase = 1
        
    if phase == 12: #LOST ROUND PHASE
        mainplayer.bet = 0
        mainplayer.reward = 0
        gamedeck = Deck()
        gamedeck.shuffle()
        mainplayer.resetCards()
        dealer.resetCards()
        if mainplayer.cash <= 0:
            phase = 13
        else:
            phase = 1
    if phase == 13: #LOST ALL MONEY PHASE
        textSize(25)
        text("YOU'VE GONE BROKE",450,300)
        text("YOU LOSE",450,550)
        if counter == 300:
            output = createWriter("usermoney.txt")
            output.println(str(mainplayer.cash))
            output.flush()
            output.close()
            exit()
        counter += 1
        
# ----- SHOWING FACE DOWN DECK --------------
    cardback.showCard(545,350)
    cardback.showCard(547,350)
    cardback.showCard(550,350)
# ------ TEXT STUFF -------------------------
    textSize(20)
    fill(255)
    text("Money: "+ "$" + str(mainplayer.cash),50,750)
    text("Bet: "+ "$" + str(mainplayer.bet),50,700)
    fill(100,1000,100)
    text("Potential Reward: "+ "$" + str(mainplayer.reward),500,750)
    fill(255)

def keyReleased():
    global mainplayer,phase
    if phase == 1:
        if keyCode == 32:
            mainplayer.bet = mainplayer.cash
        if keyCode == 8:
            mainplayer.bet = 0
        if key == "q":
            output = createWriter("usermoney.txt")
            output.println(str(mainplayer.cash))
            output.flush()
            output.close()            
            exit()
    if keyCode == 107:
        mainplayer.cash += 100          
        
def mouseReleased():
    global mainplayer,phase,dealer,gamedeck
    if phase == 1: #Betting Phase
        if (mouseX >= 100 and mouseX <= 200) and (mouseY >= 400 and mouseY <= 500): #if he clicks on -10000 circle, bring bet down by $10000
            if mainplayer.bet >= 10000:
                mainplayer.bet = mainplayer.bet - 10000
        if (mouseX >= 250 and mouseX <= 350) and (mouseY >= 400 and mouseY <= 500): #if he clicks on -5000 circle, bring bet down by $5000
            if mainplayer.bet >= 5000:
                mainplayer.bet = mainplayer.bet - 5000
        if (mouseX >= 100 and mouseX <= 200) and (mouseY >= 550 and mouseY <= 650): #if he clicks on -1000 circle, bring bet down by $1000
            if mainplayer.bet >= 1000:
                mainplayer.bet = mainplayer.bet - 1000
        if (mouseX >= 250 and mouseX <= 350) and (mouseY >= 550 and mouseY <= 650): #if he clicks on -500 circle, bring bet down by $500
            if mainplayer.bet >= 500:
                mainplayer.bet = mainplayer.bet - 500
        if (mouseX >= 400 and mouseX <= 500) and (mouseY >= 550 and mouseY <= 650): #if he clicks on -100 circle, bring bet down by $100
            if mainplayer.bet >= 100:
                mainplayer.bet = mainplayer.bet - 100
        if (mouseX >= 700 and mouseX <= 800) and (mouseY >= 550 and mouseY <= 650): #if he clicks on +100 circle, bring bet up by $100
            if mainplayer.bet <= (mainplayer.cash-100):
                mainplayer.bet = mainplayer.bet + 100
        if (mouseX >= 850 and mouseX <= 950) and (mouseY >= 550 and mouseY <= 650): #if he clicks on +500 circle, bring bet up by $500
            if mainplayer.bet <= (mainplayer.cash-500):
                mainplayer.bet = mainplayer.bet + 500
        if (mouseX >= 1000 and mouseX <= 1100) and (mouseY >= 550 and mouseY <= 650): #if he clicks on +1000 circle, bring bet up by $1000
            if mainplayer.bet <= (mainplayer.cash-1000):
                mainplayer.bet = mainplayer.bet + 1000
        if (mouseX >= 850 and mouseX <= 950) and (mouseY >= 400 and mouseY <= 500): #if he clicks on +5000 circle, bring bet up by $5000
            if mainplayer.bet <= (mainplayer.cash-5000):
                mainplayer.bet = mainplayer.bet + 5000
        if (mouseX >= 1000 and mouseX <= 1100) and (mouseY >= 400 and mouseY <= 500): #if he clicks on +10000 circle, bring bet up by $10000
            if mainplayer.bet <= (mainplayer.cash-10000):
                mainplayer.bet = mainplayer.bet + 10000
        
        if (mouseX >= 550 and mouseX <= 650) and (mouseY >= 550 and mouseY <= 650): #if he clicks on BET circle, enter playing phase (phase 2)
            if mainplayer.bet > 0:
                mainplayer.Bet()
                phase = phase + 1
                dealer.addCard(gamedeck.deal_one_card())
    if phase == 2:
        if (mouseX >= 545 and mouseX <= 630) and (mouseY >= 350 and mouseY <= 480): #if he clicks on the deck
            mainplayer.addCard(gamedeck.deal_one_card())
        if (mouseX >= 850 and mouseX <= 950) and (mouseY >= 450 and mouseY <= 550): #if he clicks STAND
            phase = 3
            dealer.addCard(gamedeck.deal_one_card())
        
        
        
        
        
    
    
    
        
    