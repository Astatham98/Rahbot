import discord


def split_text_pages(text: str, max_chars: int = 1000):
    """Split text into page-sized chunks."""
    splittext = text.split("\n")
    page_content = []
    lines = ""

    for line in splittext:
        if len(lines) + len(line) > max_chars:
            page_content.append(lines)
            lines = line
        else:
            lines += line + "\n"

    if lines:
        page_content.append(lines)

    return page_content if page_content else ["No content available."]


class ButtonPaginationView(discord.ui.View):
    def __init__(self, pages, create_embed_func, author_id=None, timeout=300):
        super().__init__(timeout=timeout)
        self.pages = pages if pages else [""]
        self.current_page = 0
        self.create_embed = create_embed_func
        self.author_id = author_id
        self.message = None
        self._update_buttons()

    def _update_buttons(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= len(self.pages) - 1

    def current_embed(self):
        return self.create_embed(self.pages[self.current_page], self.current_page, len(self.pages))

    async def interaction_check(self, interaction: discord.Interaction):
        if self.author_id is not None and interaction.user.id != self.author_id:
            if interaction.response.is_done():
                await interaction.followup.send(
                    "Only the command author can control this pagination.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "Only the command author can control this pagination.",
                    ephemeral=True,
                )
            return False
        return True

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

        if self.message is not None:
            try:
                await self.message.edit(view=self)
            except Exception:
                pass

    @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.primary)
    async def prev_button(self, button, interaction):
        if self.current_page > 0:
            self.current_page -= 1
            self._update_buttons()
            await interaction.response.edit_message(embed=self.current_embed(), view=self)

    @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.primary)
    async def next_button(self, button, interaction):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self._update_buttons()
            await interaction.response.edit_message(embed=self.current_embed(), view=self)
