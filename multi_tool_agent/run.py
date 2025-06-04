from agent import root_agent

def main():
    print("Travel Services Agent")
    print("====================")
    print("Type 'exit' to quit")
    print()
    
    while True:
        user_input = input("How can I help you with your travel plans? ")
        if user_input.lower() == 'exit':
            break
            
        try:
            response = root_agent.run(user_input)
            print("\nAgent:", response)
        except Exception as e:
            print(f"\nError: {str(e)}")
        print()

if __name__ == "__main__":
    main()