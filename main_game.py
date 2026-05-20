

def start_main():
    while True:
        
        print("\n--- CHOOSE A GAME ---")
        print("Press 1 for Snake")
        print("Press 2 for Frog Jump")
        print("Press 3 for Tetris")
        print("Press 4 to breakout")
        print("Press 5 to Exit")
        print("---------------------")
        
        
        user_choice = input("Enter number: ")
        
        if user_choice == "1":
            import snake
            
        elif user_choice == "2":
            import frog_jump
            
        elif user_choice == "3":
            import tetris
            
        elif user_choice == "4":
            import breakout   
        
        elif user_choice == "5":
            print("Exiting suite.")
            break 
            
        else:
            print("Wrong button! Please choose 1, 2, 3, or 4.")


start_main()