# main.py

from model_manager import ModelManager
from command_processor import CommandProcessor
from colorama import Fore, init

def main():
    # Initialize colorama
    init(autoreset=True)

    model_manager = ModelManager()
    command_processor = CommandProcessor(model_manager)

    model_manager.choose_model()  # Prompt user to choose a model

    while True:
        command = input(f"{Fore.GREEN}Enter your command (or type 'quit' to exit):\n")
        if command.lower() == 'quit':
            break
        command_processor.process_command(command)

if __name__ == "__main__":
    main()
