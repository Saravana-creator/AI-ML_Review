"""
Training Manager - Choose which model to train
"""
import sys
import os

def show_menu():
    print("🤖 DeepFake Model Training Manager")
    print("=" * 40)
    print("1. Quick Train (10 epochs, ~30 min)")
    print("2. Basic Train (20 epochs, ~1 hour)")
    print("3. Advanced Train (50 epochs, ~3 hours)")
    print("4. Exit")
    print("=" * 40)

def main():
    while True:
        show_menu()
        choice = input("Choose training option (1-4): ").strip()
        
        if choice == '1':
            print("🚀 Starting Quick Training...")
            os.system('python quick_train.py')
            
        elif choice == '2':
            print("🚀 Starting Basic Training...")
            os.system('python basic_model.py')
            
        elif choice == '3':
            print("🚀 Starting Advanced Training...")
            os.system('python advanced_model.py')
            
        elif choice == '4':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")
        
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()