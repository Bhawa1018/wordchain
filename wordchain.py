import time
import threading

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        return set(word.strip().lower() for word in file)

def get_machine_word(last_char, used_words, word_list):
    # Filter words that start with the given letter, are not used, and are in the word list
    available_words = [word for word in word_list if word.startswith(last_char) and word not in used_words]
    return available_words[0] if available_words else None

def input_with_timeout(prompt, timeout):
    def get_input():
        nonlocal user_input
        user_input = input(prompt)
    
    user_input = None
    timer = threading.Timer(timeout, lambda: None)
    timer.start()
    get_input()
    timer.cancel()
    return user_input

def countdown_timer(seconds, stop_event):
    for i in range(seconds, 0, -1):
        if stop_event.is_set():
            break
        print(f"Time left: {i} seconds", end='\r')
        time.sleep(1)
    if not stop_event.is_set():
        print("Time's up! Game over.")

def play_game(word_list):
    print("Welcome to the Word Chain Game!")
    print("Type a word. The next word should start with the last character of the previous word.")
    print("You have 30 seconds to type each word. The game ends if a wrong word is used or if a word is repeated. Good luck!")

    last_char = None
    used_words = set()
    
    start_time = time.time()

    while True:
        # Check if overall game time has exceeded 10 minutes
        if time.time() - start_time > 600:  # 600 seconds = 10 minutes
            print("10 minutes have passed. Game over.")
            break
        
        # Prepare countdown timer
        stop_event = threading.Event()
        countdown_thread = threading.Thread(target=countdown_timer, args=(30, stop_event))
        countdown_thread.start()

        # User's turn
        user_word = input_with_timeout("Your word: ", 30)
        stop_event.set()  # Stop the countdown timer once user input is received
        
        if user_word is None:
            print("Time's up! Game over.")
            break
        
        if not user_word.isalpha() or user_word not in word_list:
            print("Invalid word. Please enter a valid word from the dictionary. Game over.")
            break
        
        if last_char and user_word[0] != last_char:
            print(f"Word must start with '{last_char}'. Game over.")
            break
        
        if user_word in used_words:
            print("Word has already been used. Game over.")
            break
        
        used_words.add(user_word)
        last_char = user_word[-1]
        
        # Machine's turn
        machine_word = get_machine_word(last_char, used_words, word_list)
        
        if not machine_word:
            print(f"Machine: No valid word starts with '{last_char}'. You win!")
            break

        print(f"Machine: {machine_word}")
        
        used_words.add(machine_word)
        last_char = machine_word[-1]
        
        # Prepare for next round
        print("You have 30 seconds to respond with a word starting with the last letter of the machine's word.")

        # Wait for countdown to complete before the next iteration
        countdown_thread.join()

if __name__ == "__main__":
    word_list = load_word_list('/content/words_alpha.txt')  # Load your word list here
    play_game(word_list)
