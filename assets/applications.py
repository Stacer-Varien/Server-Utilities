from nextcord import *


class invite_button(ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(ui.Button(style=ButtonStyle.url,
                      label="Moderator", url="https://forms.gle/ws7d8CE5jnzqASGN8"))
        self.add_item(ui.Button(style=ButtonStyle.url,
                      label="Marketer", url="https://forms.gle/J1mDj3UYXWPkpdKT9"))
        self.add_item(ui.Button(style=ButtonStyle.url,
                      label="Partnership Manager", url="https://forms.gle/Dc3V9DmMCTszi3T89"))
        self.add_item(ui.Button(style=ButtonStyle.url,
                      label="Security Manager", url="https://forms.gle/g6Pa9uFBEEz12a6z8"))
        self.add_item(ui.Button(style=ButtonStyle.url,
                      label="Human Resources", url="https://forms.gle/NEbjtQcL9nhh3PaCA"))
