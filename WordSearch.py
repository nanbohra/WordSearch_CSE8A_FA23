import random
import sys
import time

# Fruits and Vegetables Themed Word Search

all_words = ["apple", "banana", "orange", "pear", "grape", "peach", "plum", "melon", "pomegranate",
         "strawberry", "blueberry", "raspberry", "blackberry", "grapefruit", "nectarine",
         "cherry", "watermelon", "pineapple", "mango", "kiwi", "apricot", "lychee",
         "papaya", "coconut", "lemon", "lime", "avocado", "tomato", "olive", "fig",
         "potato", "carrot", "broccoli", "cucumber", "lettuce", "mushroom", "guava",
         "onion", "pepper", "pumpkin", "radish", "spinach", "squash", "yam", "passionfruit",
         "zucchini", "eggplant", "celery", "corn", "garlic", "ginger", "peas", 
         "scallion", "beans", "beet", "cabbage", "cauliflower", "leek", "turnip", 
         "asparagus", "artichoke", "kale", "okra", "parsnip", "shallot", "chives", 
         "fennel", "rhubarb", "soybean", "cantaloupe", "jackfruit", "durian", "starfruit",
         "tangerine", "kumquat", "persimmon", "guava", "edamame", "arugula", "jalapeno", "chili", 
         "huckleberry", "cranberry", "mulberry", "prune", "honeydew", "dragonfruit", "basil", 
         "bokchoy", "gourd", "pomelo", "sprouts", "taro", "aubergine", "dill", "tamarind"]

def create_board(n):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    board = []
    if n < 10:
        horRef = ["0" + str(i) for i in range(0, n+1)]
    else:
        horRef = ["0" + str(i) for i in range(0, 10)] + [str(i) for i in range(10, n+1)]
    board.append(horRef)
    for i in range(1,n+1):
        if i < 10:
            row = ["0" + str(i)]
        else:
            row = [str(i)]
        for j in range(1,len(horRef)):
            n = random.randint(0,25)
            row.append(alphabet[n])
        board.append(row)
    return board
        
def choose_words(n):
    lst = []
    while len(lst) < n-5:
        num = random.randint(0,len(all_words)-1)
        if all_words[num] not in lst and len(all_words[num]) < n:
            lst.append(all_words[num])
    return lst

def check_placement(word, coor_lst, direction, start_coor):
    count = 0
    for i in range(len(word)):
        if direction == 0: # horizontal
            coor = (start_coor[0], start_coor[1]+i)
            if coor in coor_lst:
                count -= 1
        else: # vertical
            coor = (start_coor[0]+i, start_coor[1])
            if coor in coor_lst:
                count -= 1
    if count < 0:
        return False
    else:
        return True

def place_words(n, words):
    board = create_board(n)
    coor_lst = []

    for i in range(len(words)):
        word = words[i]
        row = random.randint(1,len(board)-1)
        col = random.randint(1,len(board)-1)
        direction = random.randint(0,1)
        check = check_placement(word, coor_lst, direction, (row,col))
        if direction == 0: # horizontal
            while (col+len(word) > len(board)-1) or check == False:
                col = random.randint(1,len(board)-1)
                row = random.randint(1,len(board)-1)
                check = check_placement(word, coor_lst, direction, (row,col))
            for j in range(len(word)):
                board[row][col+j] = word[j]
                coor_lst.append((row,col+j))
        else: # vertical
            while (row+len(word) > len(board)-1) or check == False:
                row = random.randint(1,len(board)-1)
                col = random.randint(1,len(board)-1)
                check = check_placement(word, coor_lst, direction, (row,col))
            for j in range(len(word)):
                board[row+j][col] = word[j]
                coor_lst.append((row+j,col))
    return board

def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if i == 0:
                print(board[i][j], end=" ")
            else:
                print(board[i][j], end="  ")
        print()

def check_answer(found_word, found_start, found_direction, board):
    word = found_word
    row = int(found_start[0])
    col = int(found_start[1])
    direction = int(found_direction)
    if direction == 0:
        for i in range(len(word)):
            if word[i] != board[row][col+i]:
                return False
    else:
        for i in range(len(word)):
            if word[i] != board[row+i][col]:
                return False
    return True

def update_board(found_word, found_start, found_direction, board):
    word = found_word
    row = int(found_start[0])
    col = int(found_start[1])
    direction = int(found_direction)
    check = check_answer(found_word, found_start, found_direction, board)
    if check:
        if direction == 0:
            for i in range(len(word)):
                board[row][col+i] = board[row][col+i].upper()
        else:
            for i in range(len(word)):
                board[row+i][col] = board[row+i][col].upper()
    return board

def loading():
    for _ in range(5):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.5)
    print()


def play_game():
    print("Welcome to Word Search!")
    print("You will be given a board with a list of words to find.")
    print("The words can be found horizontally or vertically.")
    print("You can find words by entering the word you found, the starting coordinate, and the direction it's written in.")
    length = int(input("Please enter a number between 6 and 20. This will be the length of the board: "))
    while length < 6 or length > 20:
        length = int(input("Please enter a number between 6 and 20: "))
    words = choose_words(length)
    board = place_words(length, words)
    print()
    print_board(board)
    print("\nHere is the list of words to find:")
    print(" ".join(list(words)))
    found_words = []
    while len(found_words) < (length - 5):
        print()
        found_word = (((str(input("Enter the word you found: "))).strip())).lower()
        if found_word not in words:
            print("Sorry, that word is not valid. Please try again.")
            found_word = str(input("Enter the word you found: "))
        found_start = tuple(((input("Enter the starting coordinate separated by a comma (row number, column number): ")).strip()).split(","))
        found_direction = int((input("Enter the direction (0 for horizontal and 1 for vertical): ")).strip())
        if found_direction != 0 and found_direction != 1:
            print("Sorry, that is not a valid direction. Please try again.")
            found_direction = int((input("Enter the direction (0 for horizontal and 1 for vertical): ")).strip())
        check = check_answer(found_word, found_start, found_direction, board)
        if check:
            found_words.append(found_word)
            board = update_board(found_word, found_start, found_direction, board)
            words.remove(found_word)
            print()
            print_board(board)
            if len(words) > 0:
                print()
                print("You found a word!")
                print("Here are the remaining words to find:")
                print(" ".join(list(words)))
        else:
            print("Sorry, that is not correct. Please try again.")
    print("\nCongratulations! You found all the words!")
    play_again = str(input("Would you like to play again? (Y/N): "))
    if play_again.lower() == "y":
        print()
        loading()
        print()
        play_game()
    else:
        print("Thank you for playing!")
        

play_game()

