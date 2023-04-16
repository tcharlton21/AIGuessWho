import tkinter as tk

from PIL import ImageTk, ImageDraw

from ImageGeneration import get_images, place_images
from chat import Chat

class UI:
    """
    UI for program
    """
    def __init__(self):
        """
        Initializes screen
        """
        # Create a new Tkinter root window
        self.root = tk.Tk()

        # Set the window title
        self.root.title("Guess Who")

        # Set the window background color
        self.root.configure(bg="light blue")

        # Configure the grid geometry manager's weights for the root window
        self.root.grid_columnconfigure(0, weight=1)  # Give column 0 a weight of 1
        self.root.grid_columnconfigure(1, weight=20)  # Give column 1 a weight of 1
        self.root.grid_rowconfigure(0, weight=1)  # Give row 0 a weight of 1
        self.root.grid_rowconfigure(1, weight=1)  # Give row 1 a weight of 0
        self.root.grid_rowconfigure(2, weight=1)

        # Create the game board
        self.boxes = self.create_board()

        # Initialize the selected box variable
        self.selected_box = None

        self.box_selected = False

        # Create Select and Eliminate buttons
        self.create_action_buttons()

        # Create the chat window
        self.create_chat()

    def run(self):
        """
        Runs the Tkinter event loop to display the UI.
        """
        # Set the size of the window

        self.root.geometry("1600x900")
        self.root.resizable(False, False)
        self.root.mainloop()

    def create_board(self):
        """
        Creates the game board with 16 equally-sized boxes and populates them with images of characters.
        Written by Trent with help from GPT-4.

        Returns:
        boxes (list): A list of Tkinter frames representing the boxes on the game board.
        """
        # Calculate the dimensions of each box based on the size of the screen
        box_width = int(self.root.winfo_screenwidth() * 0.75 / 7) - 10  # 144
        box_height = box_width

        # Set the size of the gap between boxes
        gap_size = box_width // 10

        # Calculate the total height of the board
        total_height = 4 * 144 + 3 * gap_size


        # Create a frame to hold the board
        board_frame = tk.Frame(self.root, bg="gray", height=total_height)

        # Use grid geometry manager instead of pack
        board_frame.grid(row=0, column=0, sticky="nsew", padx=190, pady=(50,0))

        board_frame.grid_columnconfigure(0, weight=1)
        board_frame.grid_columnconfigure(1, weight=1)
        board_frame.grid_columnconfigure(2, weight=1)
        board_frame.grid_columnconfigure(3, weight=1)
        board_frame.grid_rowconfigure(0, weight=1)
        board_frame.grid_rowconfigure(1, weight=1)
        board_frame.grid_rowconfigure(2, weight=1)
        board_frame.grid_rowconfigure(3, weight=1)

        # Create a list to hold the box frames
        boxes = []

        # Loop through each row and column on the board and create a box frame
        for i in range(4):
            for j in range(4):
                # Create a new frame for the box
                box_frame = tk.Frame(board_frame, width=box_width, height=box_height, bg="white", highlightthickness=1,
                                     highlightbackground="black")

                # Position the box frame in the correct row and column with some padding
                box_frame.grid(row=i, column=j, padx=gap_size, pady=gap_size)

                # Add the box frame to the list of boxes
                boxes.append(box_frame)

        # Get the images for the characters and place them in the boxes
        # Get the images and place them in the boxes
        images, names = get_images()
        place_images(images, names, board_frame, self)

        return boxes

    def create_chat(self):
        """
        Creates the chat window on the right side of the window. Written by GPT-4 and edited by Trent.
        """
        # Create a frame to hold the chat window
        chat_frame = tk.Frame(self.root, bg="light blue")

        # Use grid geometry manager instead of pack
        chat_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Create a text widget to display the chat history
        chat_history = tk.Text(chat_frame, width = 55, height=40, state="disabled")

        # Position the chat history widget at the top of the chat frame with some padding
        chat_history.grid(row=0, column=0, padx=20, pady=(10,0))

        # Create an entry widget for users to type their messages
        chat_entry = tk.Text(chat_frame, height=5, width=49, wrap='word', font=('Helvetica', 12))
        self.chat = Chat(chat_frame)  # Pass chat_frame as the parent

        # Bind the <Return> event to the chat entry widget
        chat_entry.bind("<Return>", self.handle_chat_input)

        # Position the chat entry widget at the bottom of the chat frame with some padding
        chat_entry.grid(row=1, column=0, padx=10, pady=(0,10))

        # Set the focus to the chat entry widget
        chat_entry.focus_set()

        # Save references to the chat history and chat entry widgets in the Chat object
        self.chat.chat_history = chat_history
        self.chat.chat_entry = chat_entry
        self.chat.add_message("AI: Pick your character then ask me your first question! (Let the AI know you have chosen and make sure it has too!)")

    def handle_chat_input(self, event):
        """
         Handles input from the chat entry widget. -GPT-4
        """
        # Get the user's input from the chat entry widget
        input_text = event.widget.get("1.0", "end-1c")

        # Call the Chat object's get_response method to generate a response
        self.chat.messages.append({"role": "user", "content": "Remember, we are playing Guess Who.  When I ask a question, answer with accurate information about the person you chose and do not forget who you have chosen. Then, ask questions and remember my answers to try to figure out who I picked. Always maintain the response format of answering the question and replying with a question of your own. Always double check your answer is correct before replying." + input_text}) #Add a reminder before each input_text
        response = self.chat.get_response()

        # Add the user's input and the AI's response to the chat history widget
        self.chat.chat_history.config(state="normal")
        self.chat.chat_history.insert("end", f"\nUser: {input_text}")
        self.chat.chat_history.insert("end", f"\nAI: {response}")
        self.chat.chat_history.config(state="disabled")

        # Clear the chat entry widget
        event.widget.delete("1.0", "end-1c")

    def create_action_buttons(self):
        """
        creates select and eliminate buttons -Trent & GPT-4
        """
        action_frame = tk.Frame(self.root, bg="light blue")
        action_frame.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        button_width = 17  # Set the width of the buttons

        select_button = tk.Button(action_frame, command=self.select_box, width=button_width, text="Select",
                                  bg="#679356", relief="flat")
        select_button.pack(side="right", padx=(1, 100), pady=(5, 50), anchor="se")

        eliminate_button = tk.Button(action_frame, text="Eliminate", command=self.eliminate_box, width=button_width,
                                     bg="#C54E57", relief="flat")
        eliminate_button.pack(side="right", padx=(100, 1), pady=(5, 50), anchor="se")

    def select_box(self):
        """
            Selecting box behavior - GPT-4. A yellow highlight is applied to selected name.
        """
        if self.selected_box is not None:
            if self.selected_box != self.box_selected and self.box_selected == False:
                self.box_selected = True
                self.selected_box.winfo_children()[1].config(bg="yellow")

        self.selected_box.selected = True
        self.root.after_idle(self.root.update)

    def eliminate_box(self):
        """
            Eliminating box behavior - GPT-4. A red X is applied on top of image to signify elimination.
        """
        if self.selected_box is not None:
            label = self.selected_box.winfo_children()[0]
            img = label.image
            width, height = img.width(), img.height()

            # Convert the PhotoImage object to a PIL Image
            img_pil = ImageTk.getimage(img)

            # Draw a red X on top of the image
            draw = ImageDraw.Draw(img_pil)
            draw.line((0, 0, width, height), fill="red", width=5)
            draw.line((0, height, width, 0), fill="red", width=5)

            # Convert the PIL Image back to a PhotoImage object
            tk_image = ImageTk.PhotoImage(img_pil)
            label.config(image=tk_image)
            label.image = tk_image


