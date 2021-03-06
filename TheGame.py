import tkinter
import random


def bet_5():
    global player_bet
    player_bet += 5
    show_money_and_bet()


def bet_10():
    global player_bet
    player_bet += 10
    show_money_and_bet()


def bet_15():
    global player_bet
    player_bet += 15
    show_money_and_bet()


def load_images(card_images):
    suits = ["heart", "club", "diamond", "spade"]
    face_cards = ["jack", "queen", 'king']

    # if tkinter.TkVersion >= 8.6:
    # extension = "png"
    # else:
    extension = "ppm"

    for suit in suits:
        # First the number cards
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))

        # now face cards
        for card in face_cards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def _deal_card(frame):
    # pop the next card off the top of the list
    next_card = deck.pop(0)
    # and add back
    deck.append(next_card)
    # add image to frame
    tkinter.Label(frame, image=next_card[1], relief="raised").pack(side="left")
    return next_card


def show_money_and_bet():
    global player_money
    global player_bet
    score_frame = tkinter.Frame(mainWindow)
    score_frame.grid(row=6, column=0, columnspan=3, rowspan=3, sticky="w")

    money = tkinter.Label(score_frame, text=f"Player Money = {player_money}")
    money.grid(row=1, column=0, columnspan=2)

    bet = tkinter.Label(score_frame, text=f"Player Bet = {player_bet}")
    bet.grid(row=2, column=0, columnspan=2)


def deal_dealer():
    global player_bet
    global player_money
    dealer_score = score_hand(dealer_hand)

    while 0 < dealer_score < 17:
        show_money_and_bet()
        dealer_hand.append(_deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer wins. Ha!")
        player_money -= player_bet
        player_bet = 0
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("You win!")
        player_money += player_bet
        player_bet = 0
    elif dealer_score > player_score:
        result_text.set("Dealer wins. Ha!")
        player_money -= player_bet
        player_bet = 0
    else:
        result_text.set("Draw...")
        player_bet = 0


def deal_player():
    global player_bet
    global player_money
    # tells function to use the global variables
    # global player_score
    # global player_ace

    show_money_and_bet()

    player_hand.append(_deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    player_score_label.set(player_score)

    if player_score == 21 and len(player_hand) == 2:
        result_text.set("Blackjack, you win!")
        player_money += player_bet * 2
        player_bet = 0
    elif player_score > 21:
        result_text.set("Dealer wins. Ha!")
        player_money -= player_bet
        player_bet = 0


def score_hand(hand):
    # calculate total score for cards in list
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand

    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background="green")
    dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=2)

    result_text.set("")

    dealer_hand = []
    player_hand = []

    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def shuffle():
    random.shuffle(deck)


def play():
    show_money_and_bet()
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()

    mainWindow.mainloop()


mainWindow = tkinter.Tk()

# set up screen and frames for the dealer and player
mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.configure(background='green')

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")
card_frame.grid(row=1, column=0, sticky="ew", columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background="green", fg="white").grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)

# Embedded frame to hold card images
dealer_card_frame = tkinter.Frame(card_frame, background="green")
dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)

player_score_label = tkinter.IntVar()

tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)

# Embedded frame to hold card images
player_card_frame = tkinter.Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=2)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky="w")

dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)

new_game_button = tkinter.Button(button_frame, text="New Game", command=new_game)
new_game_button.grid(row=0, column=2)

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=3)

bet_frame = tkinter.Frame(mainWindow)
bet_frame.grid(row=4, column=0, columnspan=3, sticky="w")

five_button = tkinter.Button(bet_frame, text="$5 Bet", command=bet_5)
five_button.grid(row=1, column=1)

ten_button = tkinter.Button(bet_frame, text="$10 Bet", command=bet_10)
ten_button.grid(row=1, column=2)

fifteen_button = tkinter.Button(bet_frame, text="$15 Bet", command=bet_15)
fifteen_button.grid(row=1, column=3)

cards = []
load_images(cards)
# print(cards)

# Create a new deck of cards and shuffle them
deck = list(cards)
shuffle()

# Create a list to store the dealer and player hands
dealer_hand = []
player_hand = []

if __name__ == "__main__":
    player_money = 40
    player_bet = 0
    play()
