import openai
from PIL import Image, ImageTk
import requests
import tkinter as tk

any_box_selected = False
openai.api_key = "" #Removed for github

def generate_images(prompt, n=1, size="256x256"):
    """
    Generates images using OpenAI's DALL-E API. Code written by GPT-4.

    Args:
        prompt (str): The prompt to generate the image from.
        n (int): The number of images to generate.
        size (str): The size of the images in the format "WIDTHxHEIGHT".

    Returns:
        A list of URLs for the generated images.
    """
    response = openai.Image.create(prompt=prompt, n=n, size=size)
    image_urls = [r['url'] for r in response['data']]
    return image_urls

def get_images():
    """
    Gets a list of 16 images of cartoon heads of people with distinct features. Code written by both Trent and GPT-4

    Returns:
        A list of PIL Image objects.
    """
    prompt = ["A cartoon head of a young white man with a shaved head, a beard, and a scar on his cheek. (no accessory, facial hair)",
               "A cartoon head of a middle-aged Asian woman with short, curly black hair, and a mole on her chin. (no accessory, short hair)",
               "A cartoon head of a young white girl with long pigtails, braces, and freckles. (no accessory, long hair)",
               "A cartoon head of an older white man with a bald head, a goatee, and a nose ring. (accessory, facial hair)",
               "A cartoon head of a teenage white boy with spiky blonde hair, a baseball cap, and a tattoo on his neck. (accessory, no facial hair)",
               "A cartoon head of a young African American woman with long afro hair, hoop earrings, and a nose piercing. (accessory, long hair)",
               "A cartoon head of a middle-aged Asian man with a bushy mustache, a monocle on his one eye, and a bowler hat. (accessory, facial hair)",
               "A cartoon head of a young white girl with long blonde hair, a tiara, and a polka dot dress. (accessory, long hair)",
               "A cartoon head of an elderly Indian man with a bald head, a handlebar mustache, and a pipe. (accessory, facial hair)",
               "A cartoon head of a middle-aged white woman with long curly brown hair, cat-eye glasses, and a pearl necklace. (accessory, long hair)",
               "A cartoon head of a young Hispanic boy with a buzz cut, a bandana, and a missing tooth. (accessory, no facial hair)",
               "A cartoon head of a teenage Indian girl with short purple hair, a nose stud, and a leather jacket. (accessory, short hair)",
               "A cartoon head of an older black woman with gray hair in a bun, holding a magnifying glass in her hand, and a brooch. (accessory, long hair)",
               "A cartoon head of a young Hispanic man with a crew cut, a gold chain, and a baseball jersey. (accessory, no facial hair)",
               "A cartoon head of a middle-aged black man with a bald spot, a soul patch, and a fedora. (accessory, facial hair)",
               "A cartoon head of a young Asian girl with long red hair, green eyes, and a smile. (no accessory, long hair)"]

    image_urls1 = generate_images(prompt[0], n=1, size="256x256")
    image_urls2 = generate_images(prompt[1], n=1, size="256x256")
    image_urls3 = generate_images(prompt[2], n=1, size="256x256")
    image_urls4 = generate_images(prompt[3], n=1, size="256x256")
    image_urls5 = generate_images(prompt[4], n=1, size="256x256")
    image_urls6 = generate_images(prompt[5], n=1, size="256x256")
    image_urls7 = generate_images(prompt[6], n=1, size="256x256")
    image_urls8 = generate_images(prompt[7], n=1, size="256x256")
    image_urls9 = generate_images(prompt[8], n=1, size="256x256")
    image_urls10 = generate_images(prompt[9], n=1, size="256x256")
    image_urls11 = generate_images(prompt[10], n=1, size="256x256")
    image_urls12 = generate_images(prompt[11], n=1, size="256x256")
    image_urls13= generate_images(prompt[12], n=1, size="256x256")
    image_urls14 = generate_images(prompt[13], n=1, size="256x256")
    image_urls15 = generate_images(prompt[14], n=1, size="256x256")
    image_urls16 = generate_images(prompt[15], n=1, size="256x256")

    image_urls = image_urls1 + image_urls2 + image_urls3 + image_urls4 + \
                 image_urls5 + image_urls6 + image_urls7 + image_urls8 + image_urls9 \
                 + image_urls10 + image_urls11 + image_urls12 + \
                 image_urls13 + image_urls14 + image_urls15 + image_urls16

    images = []
    names = [
        "Andy", "Brenda", "Chloe", "Derek",
        "Ethan", "Felicia", "George", "Hannah",
        "Ivan", "Julia", "Kevin", "Lisa",
        "Martha", "Nathan", "Oliver", "Penelope"
    ]
    for url in image_urls:
        img = Image.open(requests.get(url, stream=True).raw)
        img = img.resize((140, 120), Image.ANTIALIAS)
        images.append(img)

    return images, names


def place_images(images, names, board_frame, ui):
    """
        Places images and their behavior onto UI. About half of code written by Trent; other half by GPT-4.
    :param images: Images generated by DALLE
    :param names: Names of said images
    :param board_frame: board UI to place onto
    :param ui: context
    """

    boxes = board_frame.winfo_children()

    def add_hover_behavior(box, tk_image, name):
        def select_box(event):
            nonlocal ui

            if ui.selected_box and ui.selected_box != ui.box_selected:
                ui.selected_box.config(highlightbackground="black", highlightthickness=1)

            ui.selected_box = box
            box.config(highlightbackground="blue", highlightthickness=2)
            ui.chat.update_feedback(f"Box {boxes.index(box) + 1} selected")

        label = tk.Label(box, image=tk_image)
        label.image = tk_image
        label.pack(side="top")

        name_label = tk.Label(box, text=name, bg="white")
        name_label.pack(side="bottom")

        label.bind("<Button-1>", select_box)

    for i in range(16):
        tk_image = ImageTk.PhotoImage(images[i])

        box = boxes[i]
        box.selected = False
        add_hover_behavior(box, tk_image, names[i])

