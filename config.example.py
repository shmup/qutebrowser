# pyright: reportUndefinedVariable=false
# flake8: noqa: F821

config.load_autoconfig()

c.auto_save.session = True
c.session.lazy_restore = True
c.aliases["tc"] = "tab-close"

# enter insert mode when a page loads with a focused input
c.input.insert_mode.auto_load = False

# spoof chrome UA globally - qtwebengine is chromium anyway
c.content.headers.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"

# --- security/privacy hardening ---

# block page loads on TLS certificate errors instead of prompting
c.content.tls.certificate_errors = "block"

# reject third-party cookies
c.content.cookies.accept = "no-3rdparty"

# prevent WebRTC from leaking local IPs
c.content.webrtc_ip_handling_policy = "default-public-interface-only"

# use both brave adblock and hosts-based blocking
c.content.blocking.method = "both"

# disable canvas fingerprinting by default
# toggle per-site with :set -u <pattern> content.canvas_reading true
c.content.canvas_reading = False
config.set('content.canvas_reading', True, 'https://challenges.cloudflare.com/*')
config.bind("yoc", "config-cycle -p content.canvas_reading true false")
config.bind("yot", "config-cycle -p tabs.position left top")
config.bind("yob", "jseval -q (function(){var s=document.getElementById('qb-dark');if(s){s.remove();return}s=document.createElement('style');s.id='qb-dark';s.textContent='html,body,*:not(img):not(video):not(canvas):not(svg):not(picture):not(figure){background-color:#000!important;color:#aaa!important;border-color:#333!important;box-shadow:none!important}h1,h2,h3,h4,h5,h6{color:#ccc!important}a{color:#6a9fb5!important}a:visited{color:#8a7fb5!important}img,video,canvas,svg,picture{opacity:0.9}input,textarea,select,button{background-color:#111!important;color:#aaa!important;border-color:#333!important}code,pre{background-color:#111!important;color:#aaa!important}';document.head.appendChild(s)})()")

c.window.hide_decoration = True # hide the macOS title bar

# --- tab layout ---
c.tabs.show = "multiple" # hide tab bar when there's only one tab
c.tabs.width = 250 # vertical tab width
# tab title format
c.tabs.title.format = "{audio}{index}: {current_title}"
c.tabs.padding = {"top": 2, "bottom": 2, "left": 2, "right": 2}
c.tabs.pinned.shrink = True
c.tabs.indicator.width = 0 # hide the loading indicator strip
c.tabs.favicons.show = "always" # always | never | pinned

# --- theme (fonts + colors for tabs, completion, etc.) ---
config.source('theme.py')

# <space>1-9 and :1-9 to jump to tab by number
for i in range(1, 10):
    config.bind(f" {i}", f"tab-focus {i}")
    c.aliases[str(i)] = f"tab-focus {i}"

config.bind(" rv", "quickmarks-reload ;; bookmarks-reload ;; greasemonkey-reload ;; config-source")
config.bind(" tm", "cmd-set-text -s :tab-move")
config.bind(" tO", "tab-only")
config.bind(" wO", "window-only")
config.bind(" tn", "open -t")
config.bind(" tp", "tab-pin")
