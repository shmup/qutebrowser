# pyright: reportUndefinedVariable=false
# sourced by config.example.py via config.source('theme.py')

# --- palette ---
# swap these to try a different look

# --- hotpink ---
# bg_deep = "#000000"       # deepest background (tab bar, empty space)
# bg_dim = "#0d0d0d"        # dim row background
# bg_mid = "#141414"        # mid row background (alternating)
# bg_active = "#2a0a1a"     # active/selected background
# bg_bright = "#3d1028"     # bright selection background
# fg_dim = "#b05080"        # dim/inactive text
# fg_active = "#ff69b4"     # active/selected text
# fg_match = "#ff96cb"      # highlighted match text

# --- white ---
# bg_deep = "#e0e0e0"       # deepest background (tab bar, empty space)
# bg_dim = "#f0f0f0"        # dim row background
# bg_mid = "#e8e8e8"        # mid row background (alternating)
# bg_active = "#ffffff"     # active/selected background
# bg_bright = "#d0d0d0"     # bright selection background
# fg_dim = "#666666"        # dim/inactive text
# fg_active = "#111111"     # active/selected text
# fg_match = "#000000"      # highlighted match text

# --- dark green ---
# bg_deep = "#091413"       # deepest background (tab bar, empty space)
# bg_dim = "#0e1e1a"        # dim row background
# bg_mid = "#132924"        # mid row background (alternating)
# bg_active = "#285A48"     # active/selected background
# bg_bright = "#408A71"     # bright selection background
# fg_dim = "#408A71"        # dim/inactive text
# fg_active = "#B0E4CC"     # active/selected text
# fg_match = "#d4f5e6"      # highlighted match text

# --- win95 ---
bg_deep = "#868686"       # deepest background (tab bar, empty space)
bg_dim = "#c0c0c0"        # dim row background
bg_mid = "#c8c8c8"        # mid row background (alternating)
bg_active = "#000080"     # active/selected background
bg_bright = "#a0a0a0"     # bright selection background
fg_dim = "#555555"        # dim/inactive text
fg_active = "#f0f0f0"     # active/selected text
fg_match = "#000080"      # highlighted match text

font_size = "10pt"
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
c.colors.completion.fg = fg_dim
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
