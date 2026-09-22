import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "project")
os.makedirs(OUT, exist_ok=True)

W, H = 3456, 2304           # 36x24 in at 96 px/in
S = 1.9                     # base design units are scaled by S at the end
BW, BH = W / S, H / S

POUR = {
    "P": ("Perceivable", "#004b8d", "#e4ecf5", "Content reaches people through whatever senses they have."),
    "O": ("Operable", "#1f6f3f", "#e3efe7", "Anyone can run the controls, at their own pace."),
    "U": ("Understandable", "#6b2d7a", "#efe4f1", "Content and controls make sense and behave predictably."),
    "R": ("Robust", "#b3461a", "#f7e7df", "Code is clean enough for assistive technology to read."),
}

# (number, level, official name, one-liner)
SC = [
    ("1.1", "Text Alternatives", [
        ("1.1.1", "A", "Non-text Content", "Every image, icon, and chart has words that replace it."),
    ]),
    ("1.2", "Time-based Media", [
        ("1.2.1", "A", "Audio-only and Video-only (Prerecorded)", "Audio-only gets a transcript; video-only gets words or narration."),
        ("1.2.2", "A", "Captions (Prerecorded)", "Recorded video shows what is said and heard."),
        ("1.2.3", "A", "Audio Description or Media Alternative (Prerecorded)", "Blind viewers get the visuals described or written out."),
        ("1.2.4", "AA", "Captions (Live)", "Live video gets captions as it happens."),
        ("1.2.5", "AA", "Audio Description (Prerecorded)", "Recorded video narrates what matters on screen."),
        ('1.2.6', 'AAA', 'Sign Language (Prerecorded)', 'Recorded video comes with a sign language version.'),
        ('1.2.7', 'AAA', 'Extended Audio Description (Prerecorded)', 'Video pauses so narration can describe everything.'),
        ('1.2.8', 'AAA', 'Media Alternative (Prerecorded)', 'A full text version stands in for the video.'),
        ('1.2.9', 'AAA', 'Audio-only (Live)', 'Live audio gets a text version as it happens.'),
    ]),
    ("1.3", "Adaptable", [
        ("1.3.1", "A", "Info and Relationships", "Headings, lists, and tables are coded, not just styled."),
        ("1.3.2", "A", "Meaningful Sequence", "Reading order still makes sense when styling is gone."),
        ("1.3.3", "A", "Sensory Characteristics", "Instructions never rely on shape, size, place, or sound."),
        ("1.3.4", "AA", "Orientation", "Works in portrait and landscape; lock neither."),
        ("1.3.5", "AA", "Identify Input Purpose", "Common form fields are coded so browsers can autofill."),
        ('1.3.6', 'AAA', 'Identify Purpose', 'Icons, regions, and controls are coded so tools can relabel them.'),
    ]),
    ("1.4", "Distinguishable", [
        ("1.4.1", "A", "Use of Color", "Color never carries meaning by itself."),
        ("1.4.2", "A", "Audio Control", "Auto-playing sound can be paused, stopped, or turned down."),
        ("1.4.3", "AA", "Contrast (Minimum)", "Text stands out from its background, 4.5 to 1."),
        ("1.4.4", "AA", "Resize Text", "Text zooms to 200% and nothing breaks."),
        ("1.4.5", "AA", "Images of Text", "Use real text, not pictures of text."),
        ("1.4.10", "AA", "Reflow", "Zoom to 400% without scrolling sideways."),
        ("1.4.11", "AA", "Non-text Contrast", "Controls and icons stand out too, 3 to 1."),
        ("1.4.12", "AA", "Text Spacing", "Widening letters, lines, and paragraphs breaks nothing."),
        ("1.4.13", "AA", "Content on Hover or Focus", "Pop-ups can be dismissed, hovered, and stay put."),
        ('1.4.6', 'AAA', 'Contrast (Enhanced)', 'Text stands out even more, 7 to 1.'),
        ('1.4.7', 'AAA', 'Low or No Background Audio', 'Speech has no background sound, or it is very quiet.'),
        ('1.4.8', 'AAA', 'Visual Presentation', 'Readers can set colors, width, spacing, and zoom.'),
        ('1.4.9', 'AAA', 'Images of Text (No Exception)', 'Never use pictures of text unless decorative or essential.'),
    ]),
    ("2.1", "Keyboard Accessible", [
        ("2.1.1", "A", "Keyboard", "Everything works with a keyboard alone."),
        ("2.1.2", "A", "No Keyboard Trap", "Keyboard users can always tab back out."),
        ("2.1.4", "A", "Character Key Shortcuts", "Single-key shortcuts can be turned off or remapped."),
        ('2.1.3', 'AAA', 'Keyboard (No Exception)', 'Everything works by keyboard, no exceptions at all.'),
    ]),
    ("2.2", "Enough Time", [
        ("2.2.1", "A", "Timing Adjustable", "Time limits can be turned off, extended, or adjusted."),
        ("2.2.2", "A", "Pause, Stop, Hide", "Moving or updating content can be paused."),
        ('2.2.3', 'AAA', 'No Timing', 'Nothing is timed, except real-time events and recorded media.'),
        ('2.2.4', 'AAA', 'Interruptions', 'Alerts and updates can be postponed or turned off.'),
        ('2.2.5', 'AAA', 'Re-authenticating', 'Logging back in never loses your work.'),
        ('2.2.6', 'AAA', 'Timeouts', 'People are warned how long inactivity is allowed.'),
    ]),
    ("2.3", "Seizures and Physical Reactions", [
        ("2.3.1", "A", "Three Flashes or Below Threshold", "Nothing flashes more than three times a second."),
        ('2.3.2', 'AAA', 'Three Flashes', 'Nothing flashes more than three times a second, ever.'),
        ('2.3.3', 'AAA', 'Animation from Interactions', 'Motion triggered by actions can be turned off.'),
    ]),
    ("2.4", "Navigable", [
        ("2.4.1", "A", "Bypass Blocks", "Offer a way to skip repeated menus."),
        ("2.4.2", "A", "Page Titled", "Every page has a title that says what it is."),
        ("2.4.3", "A", "Focus Order", "Tabbing moves in an order that makes sense."),
        ("2.4.4", "A", "Link Purpose (In Context)", "Link text, with its context, says where it goes."),
        ("2.4.5", "AA", "Multiple Ways", "Offer more than one way to find a page."),
        ("2.4.6", "AA", "Headings and Labels", "Headings and labels describe what follows."),
        ("2.4.7", "AA", "Focus Visible", "You can always see which item has keyboard focus."),
        ("2.4.11", "AA", "Focus Not Obscured (Minimum)", "Sticky headers and pop-ups never completely hide the focused item."),
        ('2.4.8', 'AAA', 'Location', 'The site shows where you are within it.'),
        ('2.4.9', 'AAA', 'Link Purpose (Link Only)', 'Link text alone says where the link goes.'),
        ('2.4.10', 'AAA', 'Section Headings', 'Content is organized under headings, section by section.'),
        ('2.4.12', 'AAA', 'Focus Not Obscured (Enhanced)', 'Nothing ever covers any part of the focused item.'),
        ('2.4.13', 'AAA', 'Focus Appearance', 'The focus outline is thick and high contrast.'),
    ]),
    ("2.5", "Input Modalities", [
        ("2.5.1", "A", "Pointer Gestures", "Swipes and pinches have a simple tap alternative."),
        ("2.5.2", "A", "Pointer Cancellation", "Actions happen on release, so a slip can be undone."),
        ("2.5.3", "A", "Label in Name", "The visible label is part of the coded name."),
        ("2.5.4", "A", "Motion Actuation", "Shaking or tilting has a button alternative."),
        ("2.5.7", "AA", "Dragging Movements", "Anything you drag can also be done by clicking."),
        ("2.5.8", "AA", "Target Size (Minimum)", "Click targets are at least 24 by 24 pixels."),
        ('2.5.5', 'AAA', 'Target Size (Enhanced)', 'Click targets are at least 44 by 44 pixels.'),
        ('2.5.6', 'AAA', 'Concurrent Input Mechanisms', 'Switch between mouse, touch, and keyboard at any time.'),
    ]),
    ("3.1", "Readable", [
        ("3.1.1", "A", "Language of Page", "The page declares its language in code."),
        ("3.1.2", "AA", "Language of Parts", "Passages in another language are marked in code."),
        ('3.1.3', 'AAA', 'Unusual Words', 'Jargon and idioms come with definitions.'),
        ('3.1.4', 'AAA', 'Abbreviations', 'Abbreviations come with their expanded form.'),
        ('3.1.5', 'AAA', 'Reading Level', 'Text reads at lower-secondary level, or a simpler version exists.'),
        ('3.1.6', 'AAA', 'Pronunciation', 'Words whose meaning depends on pronunciation get help.'),
    ]),
    ("3.2", "Predictable", [
        ("3.2.1", "A", "On Focus", "Landing on a control never triggers a surprise."),
        ("3.2.2", "A", "On Input", "Changing a setting never triggers a surprise."),
        ("3.2.3", "AA", "Consistent Navigation", "Menus stay in the same place on every page."),
        ("3.2.4", "AA", "Consistent Identification", "The same thing looks and is named the same everywhere."),
        ("3.2.6", "A", "Consistent Help", "Help links sit in the same spot on every page."),
        ('3.2.5', 'AAA', 'Change on Request', 'Big changes happen only when you ask for them.'),
    ]),
    ("3.3", "Input Assistance", [
        ("3.3.1", "A", "Error Identification", "Errors are pointed out and described in text."),
        ("3.3.2", "A", "Labels or Instructions", "Fields say what to enter before you enter it."),
        ("3.3.3", "AA", "Error Suggestion", "When you err, the site suggests how to fix it."),
        ("3.3.4", "AA", "Error Prevention (Legal, Financial, Data)", "Big commitments can be checked, fixed, or undone."),
        ("3.3.7", "A", "Redundant Entry", "Never make people type the same thing twice."),
        ("3.3.8", "AA", "Accessible Authentication (Minimum)", "Logging in never depends on memory or puzzles."),
        ('3.3.5', 'AAA', 'Help', 'Context-sensitive help is available.'),
        ('3.3.6', 'AAA', 'Error Prevention (All)', 'Every submission can be checked, fixed, or undone.'),
        ('3.3.9', 'AAA', 'Accessible Authentication (Enhanced)', 'Logging in never needs memory, puzzles, or object recognition.'),
    ]),
    ("4.1", "Compatible", [
        ("4.1.2", "A", "Name, Role, Value", "Every control tells assistive tech what it is and does."),
        ("4.1.3", "AA", "Status Messages", "Updates are announced without stealing focus."),
    ]),
]
LEVEL_RANK = {"A": 0, "AA": 1, "AAA": 2}
def _numkey(n):
    return tuple(int(x) for x in n.split("."))
for _g in SC:
    _g[2].sort(key=lambda t: (LEVEL_RANK[t[1]], _numkey(t[0])))
NAME, LEVEL = {}, {}
for g, gname, leaves in SC:
    for n, lvl, name, one in leaves:
        NAME[n] = name
        LEVEL[n] = lvl

FPC = [
    # key, family, clause, name, one-liner, {P:[...],O:[...],U:[...],R:[...]}
    ("vision", "SEEING", "302.1", "Without Vision", "Works with no sight at all, by sound or touch.", {
        "P": "1.1.1 1.2.1 1.2.3 1.2.5 1.2.7 1.2.8 1.3.1 1.3.2 1.3.3 1.4.2",
        "O": "2.1.1 2.1.2 2.1.3 2.4.1 2.4.2 2.4.3 2.4.4 2.4.6 2.4.9 2.4.10 2.5.3",
        "U": "3.1.1 3.1.2 3.2.1 3.2.2 3.2.4 3.3.1",
        "R": "4.1.2 4.1.3"}),
    ("lowvision", "SEEING", "302.2", "With Limited Vision", "Works when you can see, but not well.", {
        "P": "1.1.1 1.2.1 1.2.3 1.2.5 1.2.7 1.3.1 1.4.1 1.4.3 1.4.4 1.4.5 1.4.6 1.4.8 1.4.9 1.4.10 1.4.11 1.4.12 1.4.13",
        "O": "2.4.7 2.4.11 2.4.12 2.4.13",
        "R": "4.1.2 4.1.3"}),
    ("color", "SEEING", "302.3", "Without Perception of Color", "Works if every color looked the same.", {
        "P": "1.3.3 1.4.1 1.4.3 1.4.6 1.4.11",
        "U": "3.3.1"}),
    ("nohear", "HEARING", "302.4", "Without Hearing", "Works with the sound off.", {
        "P": "1.2.1 1.2.2 1.2.4 1.2.6 1.2.8 1.2.9"}),
    ("lowhear", "HEARING", "302.5", "With Limited Hearing", "Works when sound is faint or muddy.", {
        "P": "1.2.1 1.2.2 1.2.4 1.2.9 1.4.2 1.4.7"}),
    ("cognition", "THINKING", "302.9", "With Limited Language, Cognitive, and Learning Abilities", "Works when reading, memory, or focus is hard.", {
        "P": "1.3.5 1.3.6 1.4.8 1.4.12",
        "O": "2.2.1 2.2.2 2.2.3 2.2.4 2.2.5 2.2.6 2.4.2 2.4.4 2.4.5 2.4.6 2.4.8 2.4.10",
        "U": "3.1.1 3.1.2 3.1.3 3.1.4 3.1.5 3.1.6 3.2.1 3.2.2 3.2.3 3.2.4 3.2.5 3.2.6 3.3.1 3.3.2 3.3.3 3.3.4 3.3.5 3.3.6 3.3.7 3.3.8 3.3.9"}),
    ("manip", "MOVING", "302.7", "With Limited Manipulation", "Works with shaky, slow, or one-handed control.", {
        "P": "1.3.4 1.3.5 1.4.13",
        "O": "2.1.1 2.1.2 2.1.3 2.1.4 2.2.1 2.2.3 2.2.5 2.4.1 2.4.3 2.4.7 2.4.11 2.4.12 2.4.13 2.5.1 2.5.2 2.5.3 2.5.4 2.5.5 2.5.6 2.5.7 2.5.8",
        "U": "3.3.7 3.3.8 3.3.9",
        "R": "4.1.2"}),
    ("reach", "MOVING", "302.8", "With Limited Reach and Strength", "Works without a long reach or a hard press.", {
        "P": "1.3.4",
        "O": "2.5.1 2.5.4 2.5.5 2.5.6 2.5.7 2.5.8"}),
    ("speech", "SPEAKING", "302.6", "Without Speech", "Works without ever speaking aloud.", {}),
]

def esc(s):
    return html.escape(s, quote=True)


# ======================= layout (base units; the whole page is scaled by S at the end) =======================
import re

def esc(s):
    return html.escape(s, quote=True)


# ======================= layout (base units; the whole page is scaled by S at the end) =======================
import re

def esc(s):
    return html.escape(s, quote=True)

# ---- FPC icons: 24x24 stroke glyphs, ink colored, inline so nothing depends on <use> support ----
ICON_PATHS = {
    "vision":    '<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="3"/><path d="M4 4l16 16"/>',
    "lowvision": '<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><path d="M12 9a3 3 0 0 0 0 6z" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="3"/>',
    "color":     '<circle cx="12" cy="12" r="9"/><circle cx="8.5" cy="10" r="1.3" fill="currentColor" stroke="none"/><circle cx="13" cy="7.5" r="1.3" fill="currentColor" stroke="none"/><circle cx="16" cy="12" r="1.3" fill="currentColor" stroke="none"/><path d="M4 4l16 16"/>',
    "nohear":    '<path d="M6 10a6 6 0 0 1 12 0c0 3-2.5 4-3.5 6S13.5 21 11 21"/><path d="M9.5 10a2.5 2.5 0 0 1 5 0c0 2-2.5 2.5-2.5 5"/><path d="M4 4l16 16"/>',
    "lowhear":   '<path d="M6 10a6 6 0 0 1 12 0c0 3-2.5 4-3.5 6S13.5 21 11 21"/><path d="M9.5 10a2.5 2.5 0 0 1 5 0c0 2-2.5 2.5-2.5 5"/><path d="M20 5q1.5 2 0 4" stroke-dasharray="1.5 1.5"/>',
    "speech":    '<path d="M4 5h16v10H10l-5 4v-4H4z"/><path d="M4 4l16 16"/>',
    "manip":     '<path d="M7 12V6a1.5 1.5 0 0 1 3 0v5"/><path d="M10 11V4a1.5 1.5 0 0 1 3 0v7"/><path d="M13 11V5a1.5 1.5 0 0 1 3 0v6"/><path d="M16 12v-1a1.5 1.5 0 0 1 3 0v5c0 4-3 6-6 6h-1c-2 0-3.5-1-4.5-2.5L4.5 15a1.5 1.5 0 0 1 2.5-1.7L8 14"/>',
    "reach":     '<path d="M4 20l7-7 6-6"/><circle cx="18.5" cy="5.5" r="2.5"/><path d="M4 20l2-5M4 20l5-2"/>',
    "cognition": '<path d="M9 21v-3H7a1 1 0 0 1-1-1v-2H4.5l1.8-3.6V10a6 6 0 0 1 12 0c0 3-2.3 4-2.3 6v5"/><circle cx="11" cy="9" r="1" fill="currentColor" stroke="none"/><circle cx="14.5" cy="8" r="1" fill="currentColor" stroke="none"/><circle cx="13" cy="12" r="1" fill="currentColor" stroke="none"/>',
    "nofpc":     '<circle cx="12" cy="12" r="8.5" stroke-dasharray="3 2.5"/><path d="M8 12h8"/>',
    "no508":     '<text x="12" y="15.5" text-anchor="middle" font-family="Libre Franklin, Arial, sans-serif" font-size="10.5" font-weight="800" fill="currentColor" stroke="none" letter-spacing="-0.3">508</text><path d="M3.5 20.5L20.5 3.5" stroke-width="2.4"/>',
}
FPC_ORDER = ["vision", "lowvision", "color", "nohear", "lowhear", "speech", "manip", "reach", "cognition"]
FPC_BY_KEY = {f[0]: f for f in FPC}

ICON_ALT = {"vision": "Without vision", "lowvision": "With limited vision", "color": "Without perception of color",
            "nohear": "Without hearing", "lowhear": "With limited hearing", "speech": "Without speech",
            "manip": "With limited manipulation", "reach": "With limited reach and strength",
            "cognition": "With limited language, cognitive, and learning abilities",
            "nofpc": "No Section 508 functional performance criterion names this need",
            "no508": "Not required by Section 508"}
PRINT = bool(os.environ.get("PREVIEW"))
def icon_svg_text(key, color="#3f4a5a"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS[key]}</svg>')
def icon(key, size=11):
    if PRINT:
        return f'<span class="icb"><img class="ic" src="icons/{key}.svg" alt="{ICON_ALT[key]}" width="{size}px" height="{size}px"></span>'
    return (f'<span class="icb"><svg class="ic" viewBox="0 0 24 24" width="{size}px" height="{size}px" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON_PATHS[key]}</svg></span>')

os.makedirs(os.path.join(ROOT, "icons"), exist_ok=True)
for _k in ICON_PATHS:
    with open(os.path.join(ROOT, "icons", f"{_k}.svg"), "w", encoding="utf-8") as _f:
        _f.write(icon_svg_text(_k))
with open(os.path.join(ROOT, "icons", "no508.svg"), "w", encoding="utf-8") as _f:
    _f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 42 22"><text x="21" y="16.5" text-anchor="middle" font-family="Libre Franklin, Arial, sans-serif" font-size="15" font-weight="800" fill="#4a4437">508</text>'
             '<line x1="1" y1="21" x2="41" y2="1" stroke="#4a4437" stroke-width="2.4" stroke-linecap="round"/></svg>')

# invert FPC -> SC into SC -> [fpc keys] in FPC_ORDER
SERVES = {}
for key, fam, clause, name, one, rows in FPC:
    for v in rows.values():
        for n in v.split():
            SERVES.setdefault(n, []).append(key)
for n in SERVES:
    SERVES[n].sort(key=FPC_ORDER.index)
NO_FPC = {"2.3.1", "2.3.2", "2.3.3"}
VINTAGE = {}
for n in "1.3.4 1.3.5 1.3.6 1.4.10 1.4.11 1.4.12 1.4.13 2.1.4 2.2.6 2.3.3 2.5.1 2.5.2 2.5.3 2.5.4 2.5.5 2.5.6 4.1.3".split():
    VINTAGE[n] = "2.1"
for n in "2.4.11 2.4.12 2.4.13 2.5.7 2.5.8 3.2.6 3.3.7 3.3.8 3.3.9".split():
    VINTAGE[n] = "2.2"
NO508_IMG = '<span class="icb no508" title="Not required by Section 508"><img src="icons/no508.svg" alt="Not required by Section 508" width="21px" height="11px" style="display: block;"></span>'
NO508 = ('<span class="icb no508" title="Not required by Section 508"><span class="sr">Not required by Section 508. </span><span aria-hidden="true">508</span>'
         '<svg class="slash" viewBox="0 0 10 10" preserveAspectRatio="none" aria-hidden="true">'
         '<line x1="0" y1="10" x2="10" y2="0" stroke="#4a4437" stroke-width="2.4" vector-effect="non-scaling-stroke" stroke-linecap="round"/></svg></span>')
def vin(n):
    return (NO508_IMG if PRINT else NO508) if (n in VINTAGE or LEVEL[n] == "AAA") else ""

# ---------------- leaves ----------------
def leaf_html(n, lvl, name, one, color):
    keys = SERVES.get(n, [])
    icons = "".join(icon(k) for k in keys)
    if n in NO_FPC:
        icons = icon("nofpc")
    lvlcls = "lvl lvl3" if lvl == "AAA" else "lvl"
    served = [FPC_BY_KEY[k][3] for k in keys]
    sr = ('Serves: ' + '; '.join(served) + '.') if served else ('Serves a need no functional performance criterion names.' if n in NO_FPC else '')
    return (
        f'<li class="leaf" style="border-left: 2px solid {color};">'
        f'<p class="l1"><span class="row"><span class="{lvlcls}"><span class="sr">Level </span>{lvl}</span><span class="num" style="color: {color};">{n}</span><span class="nm">{esc(name)}</span></span></p>'
        f'<p class="l2"><span class="row"><span class="icons">{icons}<span class="sr">{esc(sr)}</span></span><span class="one">{esc(one)}</span>{vin(n)}</span></p>'
        f'</li>'
    )

def principle_block(key, guidelines, subcols):
    pname, color, tint, one = POUR[key]
    body = []
    for g, gname, leaves in guidelines:
        body.append(f'<div class="gblk"><h3 class="gl" style="color: {color};"><span class="gnum">{g}</span> {esc(gname)}</h3><ul class="leaves">'
                    + "".join(leaf_html(n, lvl, name, one, color) for n, lvl, name, one in leaves) + '</ul></div>')
    # explicit sub-columns (not CSS multicol): keeps the tag tree intact in the PDF export
    if subcols > 1:
        k = SPLIT[key]
        cols = (f'<div class="pcolm" style="flex: 1 1 0; min-width: 0;">{"".join(body[:k])}</div>'
                f'<div class="pcolm" style="flex: 1 1 0; min-width: 0;">{"".join(body[k:])}</div>')
        inner = f'<div class="pbody" style="display: flex; gap: 14px;">{cols}</div>'
    else:
        inner = f'<div class="pbody">{"".join(body)}</div>'
    return (f'<div class="prin" style="border-left: 6px solid {color};">'
            f'<h2 class="pn" style="color: {color};">{pname.upper()}</h2>'
            f'<p class="po">{esc(one)}</p></div>' + inner)

SPLIT = {"P": 3, "O": 3, "U": 2}   # guidelines in the left sub-column: 1.1-1.3 | 1.4; 2.1-2.3 | 2.4-2.5; 3.1-3.2 | 3.3
by_p = {"P": [], "O": [], "U": [], "R": []}
for g, gname, leaves in SC:
    by_p[{"1": "P", "2": "O", "3": "U", "4": "R"}[g[0]]].append((g, gname, leaves))

# ---------------- the key panel (under Robust) ----------------
def key_row(k):
    _, fam, clause, name, one, rows = FPC_BY_KEY[k]
    note = ''
    if k == "speech":
        note = '<p class="kn">No WCAG criterion requires a non-voice alternative; voice-only kiosks and phone systems fall to 508&#8217;s technical chapters.</p>'
    return (f'<li class="krow"><span class="kic">{icon(k, 16)}</span><div><p class="kname">{esc(name)} <span class="kcl">{clause}</span></p>'
            f'<p class="kone">{esc(one)}</p>{note}</div></li>')

key_panel = ('<div class="key"><h2 class="kh">FUNCTIONAL LIMITATION KEY</h2>'
             '<p class="ks">Section 508 functional performance criteria, 36 CFR 1194 App. C &#167;302. An icon on a criterion means that criterion is one the person depends on.</p>'
             + '<ul>' + "".join(key_row(k) for k in FPC_ORDER) +
             f'<li class="krow"><span class="kic">{icon("nofpc", 16)}</span><div><p class="kname">No 508 counterpart</p>'
             '<p class="kone">Photosensitivity and motion sensitivity (2.3.x) are named by no functional performance criterion.</p></div></li>'
             f'<li class="krow"><span class="kic">{NO508}</span><div><p class="kname">Not required by Section 508</p>'
             '<p class="kone">Section 508 cites WCAG 2.0 Levels A and AA. Criteria added in WCAG 2.1 and 2.2, and all Level AAA criteria, carry this mark.</p></div></li>'
             '</ul></div>')

about_panel = ('<div class="about"><h2 class="kh">ABOUT WCAG</h2>'
    '<p class="ap">The Web Content Accessibility Guidelines are the W3C&#8217;s technical standard for making digital content usable by people with disabilities. '
    'Version 2.0 (2008, also ISO/IEC 40500) was extended by 2.1 (2018) and 2.2 (2023); each version adds criteria and keeps the earlier ones, except that 2.2 retires 4.1.1 Parsing. '
    'Success criteria are testable statements, grouped under the four principles, and each is assigned a conformance level.</p>'
    '<h3 class="ah">What it applies to</h3>'
    '<p class="ap"><b>Directly:</b> web content of every kind: pages, web applications, and anything delivered through a browser, including HTML, scripts, media, and documents such as PDF or Office files published on the web.</p>'
    '<p class="ap"><b>By adoption:</b> native mobile apps, desktop software, and electronic documents outside the web, through the W3C&#8217;s WCAG2ICT guidance and standards that cite it, including Section 508, EN 301 549, and the ADA Title II web rule.</p>'
    '<p class="ap"><b>Not covered:</b> hardware, physical products, and closed devices such as kiosks and printers. Those are handled by the technical chapters of Section 508 and EN 301 549 rather than by WCAG.</p>'
    '</div>')

# ---------------- page ----------------
GAP_IN = 14
GAP_OUT = 22
PAD = 12                                   # inner padding of each tinted principle column
RW = 250                                   # Robust + key column (incl. padding)
SUB = int((BW - 80 - 3 * GAP_OUT - RW - 3 * GAP_IN - 6 * PAD) / 6)   # sub-column width (base px)
COLW = SUB * 2 + GAP_IN + 2 * PAD
FAINT = {"P": "#eef3f8", "O": "#edf4ef", "U": "#f3eef5", "R": "#f8f0ea"}
ART_LOCAL = {"P": "images/alpha/perceivable-white.png", "O": "images/alpha/operable-white.png", "U": "images/alpha/understandable-white.png"}
try:
    ART = json.load(open(os.path.join(ROOT, "assets.json"), encoding="utf-8"))
except FileNotFoundError:
    ART = {}
if os.environ.get("PREVIEW"):
    ART = {k: v for k, v in ART_LOCAL.items() if os.path.exists(os.path.join(ROOT, v))}
# Per-image placement (base px). scale > 1 enlarges and center-crops the sides; lift raises the
# image off the box bottom. Chosen so the topmost ink of every drawing sits at the same height.
ART_FIT = {
    # scale > 1 enlarges; crop_left = fraction of the source width cut off on the left (0 = centered
    # crop); lift raises the image off the box bottom. Set so the topmost ink of every drawing sits at
    # the same height: Perceivable ink starts 37.6% down its image, Operable 60.7% down.
    "P": {"scale": 1.0, "crop_left": None, "lift": 0},
    "O": {"scale": 1.92, "crop_left": 130 / 1376, "lift": 0},
    "U": {"scale": 1051 / 897, "crop_left": 16 / 1051, "lift": -30 / S},   # placement set by hand on the canvas (Sep 22)
}
def art_html(k):
    src = ART.get(k)
    if not src:
        return ""
    fit = ART_FIT.get(k, {"scale": 1.0, "crop_left": None, "lift": 0})
    sc = fit["scale"]
    cl = fit["crop_left"] if fit["crop_left"] is not None else (sc - 1) / (2 * sc)
    return (f'<img class="art" src="{src}" alt="" style="position: absolute; left: {-cl * sc * 100:.2f}%; bottom: {fit["lift"]}px; '
            f'width: {sc * 100:g}%; height: auto; opacity: 1; pointer-events: none;">')
def colstyle(k, w):
    return (f'width: {w}px; flex: 0 0 auto; box-sizing: border-box; background: {FAINT[k]}; padding: {PAD}px {PAD}px {PAD + 4}px {PAD}px; '
            f'border: 1px solid #d9d2c3; border-radius: 3px; box-shadow: 0 2px 5px rgba(40, 32, 16, 0.10), 0 0.5px 1px rgba(40, 32, 16, 0.06); position: relative; overflow: hidden;')

def lvl_row(chip, cls, word, text):
    return (f'<li style="display: flex; align-items: baseline; gap: 7px; font-size: 10px; color: #3f4a5a; font-weight: 500;">'
            f'<span class="{cls}" style="width: 22px; text-align: center; box-sizing: border-box;">{chip}</span>'
            f'<span><b style="color: #101c2c; font-weight: 800;">{word}</b> &#183; {text}</span></li>')
legend = ('<ul style="display: flex; flex-direction: column; gap: 4px; align-items: stretch;">'
          + lvl_row("A", "lvl", "Level A", "the minimum level of conformance")
          + lvl_row("AA", "lvl", "Level AA", "clears the most common barriers while staying achievable for every kind of content")
          + lvl_row("AAA", "lvl lvl3", "Level AAA", "the highest level: extra criteria that reach people the lower levels still leave out")
          + '</ul>')

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>WCAG 2.2 Success Criteria Map</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Franklin:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500&amp;display=swap">
  <style>
    body {{ margin: 0; }}
    a {{ color: #004b8d; }} a:hover {{ color: #00335f; }}
    @page {{ size: 36in 24in; margin: 0; }}
    @media print {{ html, body {{ margin: 0; padding: 0; width: 36in; height: 24in; overflow: hidden; -webkit-print-color-adjust: exact; print-color-adjust: exact; }} }}
    .prin {{ padding: 2px 0 2px 9px; margin-bottom: 6px; }}
    h1, h2, h3 {{ margin: 0; font-size: inherit; font-weight: inherit; }}
    ul {{ list-style: none; margin: 0; padding: 0; }}
    p {{ margin: 0; }}
    .sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
    .pn {{ font-size: 19px; font-weight: 900; letter-spacing: 1.8px; line-height: 1; }}
    .po {{ font-size: 11px; font-weight: 600; color: #101c2c; margin-top: 4px; line-height: 1.25; }}
    .pbody {{ position: relative; z-index: 1; }}
    .prin {{ position: relative; z-index: 1; }}
    .gblk {{ break-inside: avoid; margin-bottom: 9px; }}
    .gl {{ font-size: 9px; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; margin: 3px 0 5px 0; padding-left: 2px; }}
    .gnum {{ font-weight: 900; }}
    .leaf {{ padding: 0 0 0 6px; margin-bottom: 7px; break-inside: avoid; }}
    .l1 .row {{ display: flex; align-items: baseline; gap: 4px; line-height: 1.15; }}
    .no508 {{ position: relative; font-size: 7.5px; font-weight: 800; letter-spacing: 0.2px; color: #4a4437; padding: 1px 3px; margin-left: auto; align-self: flex-start; overflow: hidden; }}
    .no508 .slash {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; display: block; }}
    .lvl {{ font-size: 7px; font-weight: 800; color: #ffffff; background: #4a4437; border: 1px solid #4a4437; padding: 1px 3px; letter-spacing: 0.5px; flex-shrink: 0; line-height: 1.1; }}
    .lvl3 {{ color: #4a4437; background: #ffffff; }}
    .num {{ font-size: 9.5px; font-weight: 800; flex-shrink: 0; }}
    .nm {{ font-size: 10px; font-weight: 700; color: #101c2c; }}
    .vin {{ font-size: 6.5px; font-weight: 800; color: #4a4437; border: 1px solid #8a8272; background: #faf7f1; padding: 0 2px; line-height: 1.3; letter-spacing: 0.3px; flex-shrink: 0; vertical-align: 1px; }}
    .l2 {{ margin-top: 1px; }}
    .l2 .row {{ display: flex; align-items: flex-start; gap: 6px; }}
    .icons {{ display: inline-flex; gap: 3px; flex-shrink: 0; color: #3f4a5a; }}
    .icb {{ display: inline-flex; align-items: center; justify-content: center; background: #ffffff; border: 1px solid #a89f8c; border-radius: 2px; padding: 2px; box-sizing: content-box; }}
    .ic {{ display: block; }}
    .one {{ font-size: 9px; font-style: italic; color: #3f4a5a; line-height: 1.2; padding-top: 2px; flex: 1 1 auto; }}
    .key {{ margin-top: 0; border-top: 2px solid #8a8272; padding-top: 8px; }}
    .lvl3 {{ background: #faf7f1; }}
    .kh {{ font-size: 11px; font-weight: 900; letter-spacing: 1.8px; color: #101c2c; }}
    .ks {{ font-size: 8.5px; color: #3f4a5a; line-height: 1.3; margin: 3px 0 9px 0; }}
    .krow {{ display: flex; gap: 7px; align-items: flex-start; margin-bottom: 9px; }}
    .kic {{ flex-shrink: 0; color: #3f4a5a; display: inline-flex; }}
    .kname {{ font-size: 10px; font-weight: 800; color: #101c2c; line-height: 1.15; }}
    .kcl {{ font-size: 8px; font-weight: 700; color: #4a4437; letter-spacing: 0.4px; margin-left: 3px; }}
    .kone {{ font-size: 9px; font-style: italic; color: #3f4a5a; line-height: 1.25; margin-top: 1px; }}
    .kn {{ font-size: 8px; color: #3f4a5a; line-height: 1.25; margin-top: 2px; }}
    .about {{ border-top: 2px solid #8a8272; padding-top: 8px; }}
    .ah {{ font-size: 9px; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; color: #101c2c; margin: 6px 0 3px 0; }}
    .ap {{ font-size: 8.5px; color: #3f4a5a; line-height: 1.35; margin: 0 0 5px 0; }}
    .ap b {{ color: #101c2c; font-weight: 800; }}
  </style>
</helmet>
<div style="width: {BW}px; height: {BH}px; box-sizing: border-box; display: flex; flex-direction: column; background: #faf7f1; padding: 30px 40px 16px 40px; font-family: 'Libre Franklin', 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif; color: #18202b;">

  <div style="display: flex; justify-content: space-between; align-items: flex-end; gap: 30px;">
    <div style="flex: 0 0 auto;">
      <div style="font-size: 11px; letter-spacing: 2.4px; font-weight: 700; color: #004b8d;">WCAG 2.2 AAA &#215; SECTION 508 &#183; A QUICK REFERENCE</div>
      <h1 style="margin: 4px 0 0 0; font-size: 42px; font-weight: 900; line-height: 0.95; letter-spacing: -1px; color: #101c2c;">WCAG 2.2 Success Criteria Map</h1>
    </div>
    <div style="flex: 1 1 auto;"></div>
    <div style="display: flex; flex-direction: column; gap: 6px; padding-bottom: 4px; flex: 0 0 auto; align-items: flex-end;">
      {legend}
    </div>
  </div>
  <div style="height: 4px; background: #f2a900; margin: 10px 0 14px 0;"></div>

  <div style="flex: 1 1 auto; min-height: 0; display: flex; gap: {GAP_OUT}px;">
    <div style="{colstyle("P", COLW)}">{principle_block("P", by_p["P"], 2)}{art_html("P")}</div>
    <div style="{colstyle("O", COLW)}">{principle_block("O", by_p["O"], 2)}{art_html("O")}</div>
    <div style="{colstyle("U", COLW)}">{principle_block("U", by_p["U"], 2)}{art_html("U")}</div>
    <div style="width: {RW}px; flex: 0 0 auto; display: flex; flex-direction: column; gap: 22px;">
      <div style="{colstyle("R", RW)}">{principle_block("R", by_p["R"], 1)}</div>
      <div style="padding: 0 {PAD}px;">{key_panel}</div>
      <div style="padding: 0 {PAD}px; margin-top: auto;">{about_panel}</div>
    </div>
  </div>

  <div style="display: flex; justify-content: space-between; font-size: 8px; color: #4a4437; margin-top: 8px; border-top: 1px solid #d9d2c3; padding-top: 4px;">
    <span>Sources: W3C Web Content Accessibility Guidelines 2.2 (w3.org/TR/WCAG22) &#183; 36 CFR Part 1194, Appendix C, Chapter 3 (access-board.gov/ict).</span>
    <span>Inspired by the Intopia WCAG 2.2 Map, intopia.digital &#183; CC BY-SA 4.0</span>
  </div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''

def _scale(m):
    return f"{float(m.group(1)) * S:g}px"
page = re.sub(r'(-?\d+(?:\.\d+)?)px', _scale, page)

with open(os.path.join(OUT, "Main.dc.html"), "w", encoding="utf-8") as f:
    f.write(page)

canvas = {
    "v": 3,
    "createdOnFiles": {"v": 1, "at": "2026-09-18T18:30:00Z"},
    "title": "WCAG x 508 Two Trees",
    "launch": {"view": "canvas"},
    "pages": [],
    "boards": {"Main.dc.html": {"x": 0, "y": 0, "w": W, "h": H, "title": "WCAG 2.2 Success Criteria Map — 36x24 in"}},
    "order": ["Main.dc.html"],
    "notes": {
        "brief": {"x": W + 80, "y": 0, "w": 360, "text": "v4: single tree. The Person side is gone; each criterion carries the Section 508 FPC icons it serves.\nFour principle columns, guidelines flow in two sub-columns each.\nKey with the nine FPC one-liners sits under Robust.\nAAA = outlined level chip. 2.3.x carry the dashed 'no 508 counterpart' mark."}
    },
    "designSystems": []
}
with open(os.path.join(OUT, "canvas.json"), "w", encoding="utf-8") as f:
    json.dump(canvas, f, indent=1)

leaves = sum(len(l) for _, _, l in SC)
icons_n = sum(len(v) for v in SERVES.values())
print("sheet", W, "x", H, "leaves", leaves, "icon placements", icons_n, "html bytes", len(page))
