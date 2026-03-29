# pyright: reportUndefinedVariable=false
# sourced by config.example.py via config.source('theme.py')

# --- palette ---
# swap these to try a different look

bg_deep = "#0a0040"       # deepest background (tab bar, empty space)
bg_dim = "#2e2b00"        # dim row background
bg_mid = "#332f00"        # mid row background (alternating)
bg_active = "#4a4500"     # active/selected background
bg_bright = "#665e00"     # bright selection background
fg_dim = "#a07800"        # dim/inactive text
fg_active = "#e8a800"     # active/selected text
fg_match = "#ffcc00"      # highlighted match text

font_size = "14pt"
font_family = "monospace"
font_normal = f"{font_size} {font_family}"
font_bold = f"bold {font_size} {font_family}"

# --- tabs ---

c.fonts.tabs.selected = font_bold
c.fonts.tabs.unselected = font_normal
# selected
c.colors.tabs.selected.odd.bg = bg_active
c.colors.tabs.selected.odd.fg = fg_active
c.colors.tabs.selected.even.bg = bg_active
c.colors.tabs.selected.even.fg = fg_active
# unselected
c.colors.tabs.odd.bg = bg_dim
c.colors.tabs.odd.fg = fg_dim
c.colors.tabs.even.bg = bg_mid
c.colors.tabs.even.fg = fg_dim
# pinned
c.colors.tabs.pinned.odd.bg = bg_dim
c.colors.tabs.pinned.odd.fg = fg_dim
c.colors.tabs.pinned.even.bg = bg_mid
c.colors.tabs.pinned.even.fg = fg_dim
c.colors.tabs.pinned.selected.odd.bg = bg_active
c.colors.tabs.pinned.selected.odd.fg = fg_active
c.colors.tabs.pinned.selected.even.bg = bg_active
c.colors.tabs.pinned.selected.even.fg = fg_active
# tab bar background
c.colors.tabs.bar.bg = bg_deep

# --- completion ---

c.fonts.completion.entry = font_normal
c.fonts.completion.category = font_bold
c.colors.completion.fg = fg_active
c.colors.completion.odd.bg = bg_dim
c.colors.completion.even.bg = bg_mid
c.colors.completion.category.fg = fg_active
c.colors.completion.category.bg = bg_active
c.colors.completion.category.border.top = bg_active
c.colors.completion.category.border.bottom = bg_active
c.colors.completion.item.selected.fg = fg_active
c.colors.completion.item.selected.bg = bg_bright
c.colors.completion.item.selected.border.top = bg_bright
c.colors.completion.item.selected.border.bottom = bg_bright
c.colors.completion.item.selected.match.fg = fg_match
c.colors.completion.match.fg = fg_match
c.colors.completion.scrollbar.fg = fg_dim
c.colors.completion.scrollbar.bg = bg_dim
