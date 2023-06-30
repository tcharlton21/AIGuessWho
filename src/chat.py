import openai
import tkinter as tk

class Chat:
    """
        Chat box implemented here, initial prompting & loop.
    """
    def __init__(self, parent):
        """
            Initializes GPT 3.5 with rules. Written by Trent.
        """
        openai.api_key = "" #Removed for upload
        self.frame = tk.Frame(parent)
        self.text = tk.Text(self.frame, wrap=tk.WORD, height=10, width=40, state="disabled")

        self.messages = [
            {
                "role": "system",
                "content": "You are going to play against me in Guess Who. I will provide you with 16 descriptions of people, both you and I will choose one to be the subject of guessing, we will not tell each other our picked person. Then, we will alternate asking yes or no questions about the group of people. Choose your person now from one of these descriptions and remember these for the game: The first one to guess the other’s subject of guessing wins. Here are the descriptions:  A: Andy - A cartoon head of a young white man with a shaved head, a beard, and a scar on his cheek. (male, young, no accessory, facial hair) B: Brenda - A cartoon head of a middle-aged Asian woman with short, curly black hair, and a mole on her chin. (not young, not old, female, no accessory, short hair) C: Chloe - A cartoon head of a young white girl with long pigtails, braces, and freckles. (young, female, no accessory, long hair) D: Derek - A cartoon head of an older white man with a bald head, a goatee, and a nose ring. (old, male, accessory, facial hair) E: Ethan - A cartoon head of a teenage white boy with spiky blonde hair, a baseball cap, and a tattoo on his neck. (young, male, accessory, no facial hair) F: Felicia - A cartoon head of a young African American woman with long afro hair, hoop earrings, and a nose piercing. (young, female, accessory, long hair) G: George - A cartoon head of a middle-aged Asian man with a bushy mustache, a monocle, and a bowler hat. (not young, not old, male, accessory, facial hair) H: Hannah - A cartoon head of a young white girl with long blonde hair, a tiara, and a polka dot dress. (young, female, accessory, long hair) I: Ivan - A cartoon head of an elderly Indian man with a bald head, a handlebar mustache, and a pipe. (old, male, accessory, facial hair) J: Julia - A cartoon head of a middle-aged white woman with long curly brown hair, cat-eye glasses, and a pearl necklace. (not young, not old, female, accessory, long hair) K: Kevin - A cartoon head of a young Hispanic boy with a buzz cut, a bandana, and a missing tooth. (young, male, accessory, no facial hair) L: Lisa - A cartoon head of a teenage Indian girl with short purple hair, a nose stud, and a leather jacket. (young, female, accessory, short hair) M: Martha - A cartoon head of an older black woman with gray hair in a bun, a magnifying glass, and a brooch. (old, female, accessory, long hair) N: Nathan -A cartoon head of a young Hispanic man with a crew cut, a gold chain, and a baseball jersey. (young, male, accessory, no facial hair) O: Oliver -  A cartoon head of a middle-aged black man with a bald spot, a soul patch, and a fedora. (not young, not old, male, accessory, facial hair) P: Penelope - A cartoon head of a young Asian girl with long red hair, green eyes, and a smile. (young, female, no accessory, long hair) The structure of our conversation is as follows: I will ask a question and you will answer, then you will ask a question which I will answer - we will continue this pattern until one of us guesses the other's person. When I ask a question, answer with accurate information about the person you chose and do not forget who you have chosen. "
            }
        ]

    def get_response(self):
        """
            Gets response from user query. -GPT-4
        """
        # Call the OpenAI API to generate a response

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the response text from the OpenAI API response object
        response_text = response['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": response_text})
        return response_text

    def add_message(self, msg):
        """
            Adds to chat history -GPT-4.
        """
        self.chat_history.configure(state="normal")
        self.chat_history.insert(tk.END, msg + "\n")
        self.chat_history.configure(state="disabled")

    def update_feedback(self, msg):
        """
            Updates chat_entry -GPT-4.
        """
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, msg + "\n")
        self.text.configure(state="disabled")
