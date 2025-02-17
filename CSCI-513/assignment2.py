import sys

def Enter(msg, n):
    c = -1
    while not (c >= 1 and c <= n):
        try:
            c = int(input(msg))
        except ValueError: None
        if not (c >= 1 and c <= n):
            print("You choose poorly!")
    return c - 1

S = [0, 0, 0, 0]
C = ('wishlist', 'work', 'playlist', 'miscellaneous')
welcome_choice = """Welcome to the Bookmark Manager:\n\t(1) Add a bookmark\n\t(2) Statistics\n\t(3) View bookmarks\n\t(4) Exit Program\n\tEnter 1-4: """
enter_category = "Enter Category, [1] Wishlist, [2] Work, [3] Playlist, [4] Miscellaneous: "
choice = None
try:
    while choice != 3:
        choice = Enter(welcome_choice, 4)
        if choice == 0:
            webpage_link = input("Enter the bookmark's link: ")
            bookmark_title = input("Enter the bookmark's title: : ")
            c = Enter(enter_category, 4)
            with open(C[c] + ".txt", "a") as file:
                file.write(bookmark_title + '\t' + webpage_link + '\n')
            S[c] += 1
        elif choice == 1: print(f"\nWe have:\n{S[0]} wishlist\n{S[1]} work\n{S[2]} playlist\n{S[3]} miscellaneous\n")
        elif choice == 2:
            c = Enter(enter_category, 4)
            try:
                with open(C[c] + ".txt", "r") as file:
                    while bookmark := file.readline():
                        print(bookmark, end='')
            except: None
        elif choice == 3: None # Exit
        print()
    print('Goodbye!')
except KeyboardInterrupt: print('\n\nWell then... Bye!')
