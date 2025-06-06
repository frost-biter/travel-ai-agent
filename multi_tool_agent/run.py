from agent import root_agent, logger

def main():
    logger.info("Starting Travel Services Agent")
    print("Travel Services Agent")
    print("====================")
    print("Type 'exit' to quit")
    print()
    
    while True:
        try:
            user_input = input("How can I help you with your travel plans? ")
            if user_input.lower() == 'exit':
                logger.info("User requested to exit")
                break
                
            response = root_agent.run(user_input)
            print("\nAgent:", response)
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            print(f"\nError: {str(e)}")
        print()
    
    logger.info("Travel Services Agent shutting down")

if __name__ == "__main__":
    main()