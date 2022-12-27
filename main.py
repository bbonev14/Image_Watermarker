from tkinter import *
from tkinter import filedialog, messagebox

import PIL
from PIL import Image, ImageTk, ImageOps, ImageFont, ImageDraw

FONTS = ['arial.ttf', 'bahnschrift.ttf', 'comic.ttf', 'consola.ttf', 'segoesc.ttf', 'segoeuil.ttf', 'sylfaen.ttf']
COLORS = [(0, 0, 0, 80), (0, 55, 0, 80), (55, 0, 0, 80), (0, 0, 100, 80), (55, 55, 0, 80), (55, 180, 180, 80)]
OPACITIES = [25, 50, 75, 100, 150, 200]


class Editor:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1200x750")
        self.window.title("Image Watermarker")
        self.window.config(padx=40, pady=10,)

        self.canvas = Canvas(width=990, height=680, highlightthickness=0,)
        self.canvas.config(highlightthickness=1, highlightbackground="black")
        self.canvas.grid(column=1, row=1, rowspan=4, columnspan=3)
        self.label1 = Label(self.canvas)

        self.current_image = None
        self.image_copy = None
        self.text_size = 80

        self.text_font_index = 0
        self.text_font = FONTS[0]

        self.text_color_index = 0
        self.text_color = COLORS[0]

        self.text_opacity_index = 0
        self.text_opacity = OPACITIES[0]

        choose_btn = Button(width=14, text="Choose Image", command=self.display_picture)
        choose_btn.grid(row=5, column=1, sticky=EW, pady=10, padx=(0, 5))
        self.text = Entry(width=31)
        self.text.grid(row=5, column=2, sticky=EW, padx=(5, 5))
        place_wtrmrk_btn = Button(width=14, text="Place Watermark", command=self.edited_image)
        place_wtrmrk_btn.grid(row=5, column=3, sticky=EW, padx=(5, 0))

        self.enabled_btns = False
        self.size_up_btn = Button(width=14, text="SIZE UP", command=self.text_up)
        self.size_up_btn.grid(row=1, column=0, sticky=N, padx=(0, 10))
        self.size_dw_btn = Button(width=14, text="SIZE DOWN", command=self.text_down)
        self.size_dw_btn.grid(row=1, column=0, sticky=N, pady=35, padx=(0, 10))
        self.style_btn = Button(width=14, text="STYLE", command=self.text_fonts)
        self.style_btn.grid(row=1, column=0, sticky=N, pady=70, padx=(0, 10))
        self.color_btn = Button(width=14, text="COLOR", command=self.text_colors)
        self.color_btn.grid(row=1, column=0, sticky=N, pady=105, padx=(0, 10))
        self.opacity_btn = Button(width=14, text="OPACITY", command=self.text_opacities)
        self.opacity_btn.grid(row=1, column=0, sticky=N, pady=140, padx=(0, 10))
        self.save_btn = Button(width=14, text="EXPORT", command=self.file_save)
        self.save_btn.grid(row=5, column=0, sticky=N, pady=(10, 0), padx=(0, 10))
        self.buttons_state()

        self.window.mainloop()

    # Buttons State ------------------------------
    def buttons_state(self):
        if self.enabled_btns == False:
            self.size_up_btn['state'] = "disabled"
            self.size_dw_btn['state'] = "disabled"
            self.style_btn['state'] = "disabled"
            self.color_btn['state'] = "disabled"
            self.opacity_btn['state'] = "disabled"
            self.save_btn['state'] = "disabled"
        else:
            self.size_up_btn['state'] = "active"
            self.size_dw_btn['state'] = "active"
            self.style_btn['state'] = "active"
            self.color_btn['state'] = "active"
            self.opacity_btn['state'] = "active"
            self.save_btn['state'] = "active"

    # Button Commands ------------------------------
    def text_down(self):
        self.text_size -= 25
        self.edited_image()

    def text_up(self):
        self.text_size += 25
        self.edited_image()

    def text_fonts(self):
        if self.text_font_index < len(FONTS)-1:
            self.text_font_index += 1
        else:
            self.text_font_index = 0
        self.text_font = FONTS[self.text_font_index]
        self.edited_image()

    def text_colors(self):
        if self.text_color_index < len(COLORS)-1:
            self.text_color_index += 1
        else:
            self.text_color_index = 0
        self.text_color = COLORS[self.text_color_index]
        self.edited_image()

    def text_opacities(self):
        if self.text_opacity_index < len(COLORS)-1:
            self.text_opacity_index += 1
        else:
            self.text_opacity_index = 0
        x = OPACITIES[self.text_opacity_index]
        new_opacity = list(self.text_color)[:-1]
        new_opacity.append(x)
        self.text_color = tuple(new_opacity)
        self.edited_image()

    def file_save(self):
        f = filedialog.asksaveasfile(mode='wb', defaultextension="*.jpg",
                                     filetypes=(("PNG file", "*.png"), ('JPG File', '*.jpg'), ("All Files", "*.*")))
        if f:
            img = self.image_copy
            img.save(f)

    def choose_img(self):
        filename = filedialog.askopenfilename(initialdir='C:/Users/Thrace Tactical Gear/Desktop',
                                              title='Select an Image:',
                                              filetypes=(('JPG File', '*.jpg'), ('PNG File', '*.png')))
        if filename:
            return filename

    def display_picture(self):
        self.current_image = self.choose_img()
        if self.current_image:
            img = Image.open(self.current_image)
            img = PIL.ImageOps.exif_transpose(img)
            img.thumbnail((990, 680))
            img = ImageTk.PhotoImage(img)
            self.label1.config(image=img)
            self.label1.image = img
            self.label1.grid(column=1, row=1, rowspan=4, columnspan=3)

    def display_new(self, image):
        img = image
        img = PIL.ImageOps.exif_transpose(img)
        img.thumbnail((990, 680))
        img = ImageTk.PhotoImage(img)
        self.label1.config(image=img)
        self.label1.image = img
        self.label1.grid(column=1, row=1, rowspan=4, columnspan=3)

    def edited_image(self):
        try:
            if not self.text.get():
                messagebox.showinfo(title="Error",
                                    message="Please input a message in the text field.")
            else:
                img = Image.open(self.current_image)
                img = PIL.ImageOps.exif_transpose(img)
                # Make image copy
                self.image_copy = img.copy().convert("RGBA")
                txt = Image.new('RGBA', self.image_copy.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(txt)
                # Creating text and font object
                text = self.text.get()
                font = ImageFont.truetype(self.text_font, self.text_size)
                # Positioning Text
                _, _, textwidth, textheight = draw.textbbox((0, 0), text, font=font)
                width, height = self.image_copy.size
                x = (width - textwidth) / 2
                y = (height - textheight) / 2
                # Applying text on image via draw object
                draw.text((x, y), text, fill=self.text_color, font=font)
                self.image_copy = Image.alpha_composite(self.image_copy, txt, )
                # Forwarding the new image
                self.display_new(self.image_copy)
                #enable buttons
                self.enabled_btns = True
                self.buttons_state()
        except AttributeError:
            messagebox.showinfo(title="Error", message="Please choose an image and input a message in the text field below.")


Editor()
