#!/usr/bin/env python3
"""
Article Summarizer using multiple AI providers
Summarizes blog posts/articles using AI and copies output to clipboard
Supports: Ollama, OpenAI, Anthropic
"""

# Import necessary libraries
import requests      # For making HTTP requests to AI APIs
import json         # For handling JSON data from API responses
import pyperclip    # For copying text to the system clipboard
import sys          # For system operations like exiting the program
import os           # For accessing environment variables
from dotenv import load_dotenv  # For loading API keys from .env file


def select_ai_provider():
    """Let user select which AI provider to use for summarization"""
    # Display the available AI provider options to the user
    print("Select AI provider:")
    print("1. Ollama (local)")    # Runs on your computer, requires Ollama installation
    print("2. OpenAI")           # Uses OpenAI's API, requires API key
    print("3. Anthropic")        # Uses Anthropic's API, requires API key
    
    # Keep asking until user provides a valid choice
    while True:
        choice = input("Enter choice (1-3): ").strip()  # Get user input and remove whitespace
        if choice == "1":
            return "ollama"      # Return the provider name for Ollama
        elif choice == "2":
            return "openai"     # Return the provider name for OpenAI
        elif choice == "3":
            return "anthropic"  # Return the provider name for Anthropic
        else:
            # If user enters invalid choice, show error and ask again
            print("Invalid choice. Please enter 1, 2, or 3.")


def get_user_input():
    """Get article text from user input - allows multi-line text entry"""
    print("Please paste your article text below (press Ctrl+D when finished):")
    print("-" * 50)

    lines = []  # Create empty list to store each line of text
    try:
        # Keep reading lines until user presses Ctrl+D (EOF - End of File)
        while True:
            line = input()          # Read one line from user
            lines.append(line)      # Add the line to our list
    except EOFError:
        # This happens when user presses Ctrl+D, which is expected
        pass

    # Join all lines together with newline characters to recreate the original text
    return "\n".join(lines)


def create_summary_prompt(article_text):
    """Create the formatted prompt that tells the AI how to summarize the article"""
    # This is the instruction template we send to the AI
    # It specifies exactly how we want the summary formatted
    prompt = f"""Please summarize the following article using this exact format. IMPORTANT Use only this format and no other:

> [!Abstract]- 
>**Summary:**
	>>[One-sentence overview of the article's main point in 30-45 words.] 
	>
>**The details:** 
	> - [Key point #1]
	> - [Key point #2]
	> - [Key point #3]                                                                                     
(Include 3--5 concise bullet points highlighting the most important factual or contextual details.)
>
>**Why it matters:**                                                                                  
     >>[Briefly explain the significance or impact of the article's content. Focus on why readers should care or what the broader implications are.]

Make sure the summary is:
- Succinct (no fluff)
- Fact-based
- Easy to skim
- Written in plain, neutral, professional language
- Written in markdown format

Article to summarize:
{article_text}"""

    return prompt


def query_ollama(prompt, model="gemma3:latest"):
    """Send prompt to Ollama (local AI) and get response"""
    # Ollama runs locally on your computer at this address
    url = "http://localhost:11434/api/generate"

    # Prepare the data to send to Ollama
    payload = {
        "model": model,        # Which AI model to use (gemma3:latest by default)
        "prompt": prompt,      # The text we want the AI to process
        "stream": False       # Get complete response at once, not streaming
    }

    try:
        # Set up headers to tell Ollama we're sending JSON data
        headers = {"Content-Type": "application/json"}
        
        # Send the request to Ollama
        response = requests.post(url, json=payload, headers=headers)
        
        # Debug information to help troubleshoot if something goes wrong
        print(f"Debug: Response status: {response.status_code}")
        print(f"Debug: Response URL: {response.url}")
        
        # Check if the request was successful (status code 200-299)
        response.raise_for_status()

        # Parse the JSON response from Ollama
        result = response.json()
        
        # Extract the actual AI response text from the JSON
        return result.get("response", "")

    except requests.exceptions.ConnectionError:
        # This happens if Ollama isn't running or isn't installed
        print("Error: Could not connect to Ollama. Make sure Ollama is running.")
        sys.exit(1)  # Exit the program with error code
    except requests.exceptions.RequestException as e:
        # Handle other network/request errors
        print(f"Error querying Ollama: {e}")
        print(
            f"Debug: Response content: {response.text if 'response' in locals() else 'No response'}"
        )
        sys.exit(1)
    except json.JSONDecodeError:
        # This happens if Ollama returns invalid JSON
        print("Error: Invalid response from Ollama")
        sys.exit(1)


def query_openai(prompt, model="gpt-4"):
    """Send prompt to OpenAI's API and get response"""
    # Get the API key from environment variables (stored in .env file)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please add your OpenAI API key to the .env file")
        sys.exit(1)
    
    # OpenAI's chat completions API endpoint
    url = "https://api.openai.com/v1/chat/completions"
    
    # Prepare the data for OpenAI's API
    payload = {
        "model": model,     # Which OpenAI model to use (gpt-4 by default)
        "messages": [{"role": "user", "content": prompt}],  # Format required by chat API
        "max_tokens": 1000  # Maximum length of response
    }
    
    try:
        # Set up headers with API key for authentication
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"  # Authentication using API key
        }
        
        # Send the request to OpenAI
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        
        # Parse the JSON response
        result = response.json()
        
        # Extract the AI's response from the nested JSON structure
        # OpenAI returns: {"choices": [{"message": {"content": "actual response"}}]}
        return result["choices"][0]["message"]["content"]
        
    except requests.exceptions.RequestException as e:
        # Handle network errors, authentication errors, etc.
        print(f"Error querying OpenAI: {e}")
        sys.exit(1)
    except (KeyError, IndexError):
        # Handle cases where the response structure is unexpected
        print("Error: Unexpected response format from OpenAI")
        sys.exit(1)


def query_anthropic(prompt, model="claude-3-sonnet-20240229"):
    """Send prompt to Anthropic's Claude API and get response"""
    # Get the API key from environment variables (stored in .env file)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please add your Anthropic API key to the .env file")
        sys.exit(1)
    
    # Anthropic's messages API endpoint
    url = "https://api.anthropic.com/v1/messages"
    
    # Prepare the data for Anthropic's API
    payload = {
        "model": model,         # Which Claude model to use
        "max_tokens": 1000,    # Maximum length of response
        "messages": [{"role": "user", "content": prompt}]  # Message format for Claude
    }
    
    try:
        # Set up headers with API key and required version
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,                    # Anthropic uses this header for API key
            "anthropic-version": "2023-06-01"        # Required API version
        }
        
        # Send the request to Anthropic
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        
        # Parse the JSON response
        result = response.json()
        
        # Extract Claude's response from the nested JSON structure
        # Anthropic returns: {"content": [{"text": "actual response"}]}
        return result["content"][0]["text"]
        
    except requests.exceptions.RequestException as e:
        # Handle network errors, authentication errors, etc.
        print(f"Error querying Anthropic: {e}")
        sys.exit(1)
    except (KeyError, IndexError):
        # Handle cases where the response structure is unexpected
        print("Error: Unexpected response format from Anthropic")
        sys.exit(1)


def copy_to_clipboard(text):
    """Copy the generated summary to the system clipboard for easy pasting"""
    try:
        # Use pyperclip library to copy text to system clipboard
        pyperclip.copy(text)
        print("\n✓ Summary copied to clipboard!")  # Confirm success to user
    except Exception as e:
        # If clipboard access fails, warn user but don't crash the program
        print(f"Warning: Could not copy to clipboard: {e}")


def get_ai_response(provider, prompt):
    """Route the request to the appropriate AI provider based on user's choice"""
    # Call the appropriate function based on which provider the user selected
    if provider == "ollama":
        # Use local Ollama with gemma3 model
        return query_ollama(prompt, "gemma3:latest")
    elif provider == "openai":
        # Use OpenAI's GPT-4 model
        return query_openai(prompt, "gpt-4")
    elif provider == "anthropic":
        # Use Anthropic's Claude model
        return query_anthropic(prompt, "claude-3-sonnet-20240229")
    else:
        # This should never happen if select_ai_provider() works correctly
        print(f"Error: Unknown provider '{provider}'")
        sys.exit(1)


def main():
    """Main program function - coordinates the entire summarization process"""
    # Load API keys and other settings from .env file
    load_dotenv()
    
    # Welcome message
    print("Article Summarizer with Multiple AI Providers")
    print("=" * 50)

    # Step 1: Ask user which AI provider they want to use
    provider = select_ai_provider()
    print(f"\nUsing {provider.title()} for summarization")
    print("-" * 30)

    # Step 2: Get the article text that user wants to summarize
    article_text = get_user_input()

    # Validate that user actually provided some text
    if not article_text.strip():  # strip() removes whitespace
        print("No article text provided. Exiting.")
        sys.exit(1)

    # Step 3: Create the instruction prompt for the AI
    prompt = create_summary_prompt(article_text)

    print("\nGenerating summary...")  # Let user know we're working

    # Step 4: Send the prompt to the selected AI provider
    summary = get_ai_response(provider, prompt)

    # Check that we actually got a response
    if not summary:
        print(f"Error: No summary received from {provider}")
        sys.exit(1)

    # Step 5: Display the summary to the user
    print("\n" + "=" * 50)
    print("ARTICLE SUMMARY")
    print("=" * 50)
    print(summary)  # Print the actual summary
    print("=" * 50)

    # Step 6: Copy summary to clipboard for easy pasting elsewhere
    copy_to_clipboard(summary)


# This special check ensures main() only runs when script is executed directly,
# not when imported as a module by another Python file
if __name__ == "__main__":
    main()  # Start the program
