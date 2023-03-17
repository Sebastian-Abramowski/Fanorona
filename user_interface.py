from constants import ROWS, COLS


def user_interface():
    """Taking inputs for Fanorona game"""
    print("Welcome to Fanorona game")

    random_play_user_choice = 0
    if ROWS == 3 and COLS == 3:
        msg = ("Do you want to play",
               "vs computer? (1 - yes, 0 - no): ")

        comp_user_choice = input(" ".join(msg))

        try:
            comp_user_choice = int(comp_user_choice)
        except Exception:
            print("Your input must be number, 0 or 1...")

        while comp_user_choice not in [0, 1]:
            comp_user_choice = input(msg + " Try again: ")

            try:
                comp_user_choice = int(comp_user_choice)
            except Exception:
                print("Your input must be number, 0 or 1...")
    else:
        msg = "Do you want to play vs computer? (1 - yes, 0 - no): "
        comp_user_choice = input(msg)

        try:
            comp_user_choice = int(comp_user_choice)
        except Exception:
            print("Your input must be number, 0 or 1...")

        while comp_user_choice not in [0, 1]:
            comp_user_choice = input(msg + " Try again: ")

            try:
                comp_user_choice = int(comp_user_choice)
            except Exception:
                print("Your input must be number, 0 or 1...")

        if comp_user_choice == 1:
            msg = ("Do you want to play vs computer",
                   "that makes random or good moves?",
                   "(1 - random moves, 0 -",
                   "good moves): ")
            random_play_user_choice = input(" ".join(msg))

            try:
                random_play_user_choice = int(random_play_user_choice)
            except Exception:
                print("Your input must be number, 0 or 1...")

            while random_play_user_choice not in [0, 1]:
                random_play_user_choice = input(" ".join(msg) + " Try again: ")

                try:
                    random_play_user_choice = int(random_play_user_choice)
                except Exception:
                    print("Your input must be number, 0 or 1...")

    print("The game is started... If you don't see the window,",
          "see under this screen or click the icon in the taskbar :)")
    return comp_user_choice, random_play_user_choice
