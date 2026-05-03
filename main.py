import requests
from bs4 import BeautifulSoup
import ollama
import random

MODEL = "llama3.2:1b"


def get_random_quote():
    url = "https://quotes.toscrape.com/"
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        selected = random.choice(quotes)
        return f"{selected.find('span', class_='text').text} — {selected.find('small', class_='author').text}"
    except:
        return "The stars were silent tonight. — Unknown"


def generate_story(user_prompt):
    # This specific formatting helps the AI understand it MUST follow your prompt
    prompt_content = (
        f"Write a 3-sentence story specifically about this prompt: {user_prompt}. "
        "Do not write about anything else. Focus on the action."
    )

    response = ollama.generate(
        model=MODEL,
        prompt=prompt_content
    )
    return response['response']


print(f"--- INTERACTIVE STORY GEN ({MODEL}) ---")
print("Type a prompt or just press Enter for a random quote.")

while True:
    user_input = input("\n[Prompt] or [Enter] for random | [q] to quit: ")

    if user_input.lower() == 'q':
        break

    # If you didn't type anything, go scrape a quote
    if not user_input.strip():
        print("Scraping inspiration...")
        final_prompt = get_random_quote()
        print(f"Inspiration: {final_prompt}")
    else:
        final_prompt = user_input

    print("Generating...")
    story = generate_story(final_prompt)


    print(story)
