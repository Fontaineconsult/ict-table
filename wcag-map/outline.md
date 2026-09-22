# WCAG 2.2 x Section 508 FPC — Poster Outline (v0.5: two trees, all 86 criteria incl. AAA)

Sibling project to `poster/`. Print target: 11x17 tabloid, LANDSCAPE.
Scope: WCAG 2.2 Level A + AA + AAA (86 success criteria; 4.1.1 removed). AAA leaves are drawn
with a dashed border on the Person tree because Section 508 binds only Level AA. The 31 AAA
names, one-liners, and FPC assignments live in gen.py (sections 4-5 below predate AAA).
FPC: nine Section 508 Functional Performance Criteria, 36 CFR 1194 App. C, 302.1-302.9.
No grids, no tables. Two trees share one set of leaves.

---------------------------------------------------------------------------------------

## 0. The graphic idea: The Standard tree and The Person tree

The same 55 criteria hang on two different trees, and the poster shows both.

  LEFT (~6.5 in): THE STANDARD                RIGHT (~10 in): THE PERSON
  How W3C organizes the rules.                How Section 508 organizes the people.
  Root -> 4 principles -> 13 guidelines       Root -> 5 ability families -> 9 FPC
       -> 55 leaves, each with a one-liner.        -> POUR twigs -> leaves (SC chips).

  A leaf is the same object in both trees: number + short name, colored by principle.
  On the left it appears once with its one-liner. On the right it appears on every
  FPC branch it serves, as a small chip. The number and the color are the cross-reference;
  no lines cross the gutter between the trees.

### Left tree: THE STANDARD (dendrogram, trunk at the left edge, growing rightward)

  WCAG 2.2 AA ─┬─ PERCEIVABLE  ─┬─ 1.1 Text Alternatives ── 1.1.1 ...one-liner
               │                ├─ 1.2 Time-based Media ─┬─ 1.2.1 ...
               │                │                        ├─ 1.2.2 ...
               │                ├─ 1.3 Adaptable ...
               │                └─ 1.4 Distinguishable ...
               ├─ OPERABLE ...
               ├─ UNDERSTANDABLE ...
               └─ ROBUST ...

  - Branch thickness at the principle level is proportional to leaf count (21/20/12/2), so
    the tree's silhouette already says where the weight of WCAG sits.
  - Each principle branch carries its underlined one-liner where it leaves the trunk.
  - Leaves are one text row each: level chip, number, the OFFICIAL W3C criterion name in
    bold, then the one-liner in a lighter weight. Names are never abbreviated on the poster. 55 rows in ~9.5 in of height = 0.17 in per row, ~8 pt. Tight but it is
    exactly the density Intopia already prints.
  - Numeric order is preserved top to bottom, so it doubles as an index.

### Right tree: THE PERSON (radial mind-map, root at center)

  Center node: "One person, nine ways of working" (or simply the 508 FPC citation).

  Five limbs leave the center, one per ability family, each splitting into its FPC:

        SEEING  ──┬─ Without Vision          (24 leaves)
                  ├─ With Limited Vision     (17)
                  └─ Without Color           (5)
        HEARING ──┬─ Without Hearing         (3)
                  └─ With Limited Hearing    (4)
        SPEAKING ─── Without Speech          (0)   <- bare branch
        MOVING  ──┬─ With Limited Manipulation (20)
                  └─ Limited Reach & Strength  (5)
        THINKING ─── Limited Cognition       (21)

  Each FPC branch then forks into POUR twigs, colored by principle, and only the twigs
  that carry leaves are drawn. Leaves are chips: number + short name. Example:

        Without Vision ─┬─ P ─ 1.1.1 Non-text Content, 1.2.1, 1.2.3, 1.2.5, 1.3.1, 1.3.2, 1.3.3, 1.4.2
                        ├─ O ─ 2.1.1, 2.1.2, 2.4.1, 2.4.2, 2.4.3, 2.4.4, 2.4.6, 2.5.3
                        ├─ U ─ 3.1.1, 3.1.2, 3.2.1, 3.2.2, 3.2.4, 3.3.1
                        └─ R ─ 4.1.2, 4.1.3

        Without Hearing ─── P ─ 1.2.1, 1.2.2, 1.2.4        (one twig only)

        Without Speech  ─── (no leaves) "No WCAG criterion applies. Voice-only
                            interfaces fall to 508's technical chapters."

  Why this answers the brief
  - Lookup by FPC is a branch read: find "Without Vision", and the twig colors show the
    POUR spread before you read a single number. Vision has four twigs; hearing has one
    (all Perceivable); moving is almost all Operable; thinking is mostly Understandable.
    The tree's shape IS the FPC-to-POUR mapping. No cell, no count needed.
  - Branch length or leaf count per FPC is visible as canopy size, so "how much of WCAG
    serves this person" is read at a glance.
  - The bare Speaking branch and the fallen leaf (2.3.1, drawn on the ground below the
    tree with the note "no FPC names photosensitivity") make the two gaps unmissable.
  - Leaf chips repeat across branches on purpose: a person who is blind needs 1.1.1 and
    so does a person with low vision. Duplication is the point of the Person view.
  - Total chips: 99 (24+17+5+3+4+0+20+5+21). At chip size ~0.9 x 0.16 in that is a
    comfortable fit in a 10 x 9.5 in radial field.

  Layout notes
  - Radial order (clockwise from top): Seeing, Hearing, Speaking, Moving, Thinking. The
    two big limbs (Seeing, Thinking) sit on opposite sides so the canopy balances.
  - Twig order within every branch is always P, O, U, R, so the color sequence is
    predictable and readable without a legend once seen once.
  - Chips within a twig run in numeric order.
  - Family labels (Seeing, Hearing...) sit on the outer rim as quiet caps; the FPC name and
    its one-liner sit at the branch fork.
  - No FPC glyphs are needed: the family limb and the branch label carry identity.

### Color
  - Four hues, POUR only, used identically in both trees for branches, twigs, and chips.
  - FPC branches, limbs, and the trunk are ink/neutral. The Person tree is a grey tree with
    colored leaves; the Standard tree is a colored tree. Same leaves, different plant.

### Alternative considered (not recommended)
  "Roots and canopy": one tree where the nine FPC are roots below ground, the POUR trunk and
  guideline branches rise above, and 55 leaves sit at the top; ribbons run from each root up
  through the trunk to the leaves it feeds. It is a single striking image, but 99 ribbons
  through one trunk need hierarchical bundling to stay legible, and the lookup by FPC
  becomes a trace, not a read. The two-tree layout keeps every lookup local.

## 1. Masthead (runs across the top, above both trees)
- Title: "WCAG 2.2 AA, Two Ways: The Standard and The Person"
- Subtitle: "Left: how W3C arranges the 55 A/AA success criteria. Right: the same criteria
  hung on the nine Section 508 Functional Performance Criteria."
- Version line: WCAG 2.2 (W3C, Dec 2023); Section 508 Refresh (2017), 36 CFR 1194 App. C.
- Credit: adapted from the Intopia WCAG 2.2 Map, CC BY-SA 4.0 (derivative keeps license).

## 2. POUR principle one-liners (underlined, at each principle branch)

  PERCEIVABLE     Content reaches people through whatever senses they have.
  OPERABLE        Anyone can run the controls, at their own pace.
  UNDERSTANDABLE  Content and controls make sense and behave predictably.
  ROBUST          Code is clean enough for assistive technology to read.

## 3. FPC one-liners (at each FPC branch fork)

  302.1  Without Vision            Works with no sight at all, by sound or touch.
  302.2  With Limited Vision       Works when you can see, but not well.
  302.3  Without Color Perception  Works if every color looked the same.
  302.4  Without Hearing           Works with the sound off.
  302.5  With Limited Hearing      Works when sound is faint or muddy.
  302.6  Without Speech            Works without ever speaking aloud.
  302.7  With Limited Manipulation Works with shaky, slow, or one-handed control.
  302.8  Limited Reach & Strength  Works without a long reach or a hard press.
  302.9  Limited Cognition         Works when reading, memory, or focus is hard.

## 4. THE STANDARD tree: 55 leaves with one-liners (numeric order)

### PERCEIVABLE — Content reaches people through whatever senses they have.
1.1 Text Alternatives
  A  1.1.1  Non-text Content          Every image, icon, and chart has words that replace it.
1.2 Time-based Media
  A  1.2.1  Audio-only and Video-only (Prerecorded)  Audio-only gets a transcript; video-only gets words or narration.
  A  1.2.2  Captions (Prerecorded)    Recorded video shows what is said and heard.
  A  1.2.3  Audio Description or Media Alternative (Prerecorded)  Blind viewers get the visuals described or written out.
  AA 1.2.4  Captions (Live)           Live video gets captions as it happens.
  AA 1.2.5  Audio Description (Prerecorded)  Recorded video narrates what matters on screen.
1.3 Adaptable
  A  1.3.1  Info and Relationships    Headings, lists, and tables are coded, not just styled.
  A  1.3.2  Meaningful Sequence       Reading order still makes sense when styling is gone.
  A  1.3.3  Sensory Characteristics   Instructions never rely on shape, size, place, or sound.
  AA 1.3.4  Orientation               Works in portrait and landscape; lock neither.
  AA 1.3.5  Identify Input Purpose    Common form fields are coded so browsers can autofill.
1.4 Distinguishable
  A  1.4.1  Use of Color              Color never carries meaning by itself.
  A  1.4.2  Audio Control             Auto-playing sound can be paused, stopped, or turned down.
  AA 1.4.3  Contrast (Minimum)        Text stands out from its background, 4.5 to 1.
  AA 1.4.4  Resize Text               Text zooms to 200% and nothing breaks.
  AA 1.4.5  Images of Text            Use real text, not pictures of text.
  AA 1.4.10 Reflow                    Zoom to 400% without scrolling sideways.
  AA 1.4.11 Non-text Contrast         Controls and icons stand out too, 3 to 1.
  AA 1.4.12 Text Spacing              Widening letters, lines, and paragraphs breaks nothing.
  AA 1.4.13 Content on Hover or Focus  Pop-ups can be dismissed, hovered, and stay put.

### OPERABLE — Anyone can run the controls, at their own pace.
2.1 Keyboard Accessible
  A  2.1.1  Keyboard                  Everything works with a keyboard alone.
  A  2.1.2  No Keyboard Trap          Keyboard users can always tab back out.
  A  2.1.4  Character Key Shortcuts   Single-key shortcuts can be turned off or remapped.
2.2 Enough Time
  A  2.2.1  Timing Adjustable         Time limits can be turned off, extended, or adjusted.
  A  2.2.2  Pause, Stop, Hide         Moving or updating content can be paused.
2.3 Seizures and Physical Reactions
  A  2.3.1  Three Flashes or Below Threshold  Nothing flashes more than three times a second.
2.4 Navigable
  A  2.4.1  Bypass Blocks             Offer a way to skip repeated menus.
  A  2.4.2  Page Titled               Every page has a title that says what it is.
  A  2.4.3  Focus Order               Tabbing moves in an order that makes sense.
  A  2.4.4  Link Purpose (In Context)  Link text, with its context, says where it goes.
  AA 2.4.5  Multiple Ways             Offer more than one way to find a page.
  AA 2.4.6  Headings and Labels       Headings and labels describe what follows.
  AA 2.4.7  Focus Visible             You can always see which item has keyboard focus.
  AA 2.4.11 Focus Not Obscured (Minimum)  Sticky headers and pop-ups never hide the focused item.
2.5 Input Modalities
  A  2.5.1  Pointer Gestures          Swipes and pinches have a simple tap alternative.
  A  2.5.2  Pointer Cancellation      Actions happen on release, so a slip can be undone.
  A  2.5.3  Label in Name             The visible label is part of the coded name.
  A  2.5.4  Motion Actuation          Shaking or tilting has a button alternative.
  AA 2.5.7  Dragging Movements        Anything you drag can also be done by clicking.
  AA 2.5.8  Target Size (Minimum)     Click targets are at least 24 by 24 pixels.

### UNDERSTANDABLE — Content and controls make sense and behave predictably.
3.1 Readable
  A  3.1.1  Language of Page          The page declares its language in code.
  AA 3.1.2  Language of Parts         Passages in another language are marked in code.
3.2 Predictable
  A  3.2.1  On Focus                  Landing on a control never triggers a surprise.
  A  3.2.2  On Input                  Changing a setting never triggers a surprise.
  A  3.2.6  Consistent Help           Help links sit in the same spot on every page.
  AA 3.2.3  Consistent Navigation     Menus stay in the same place on every page.
  AA 3.2.4  Consistent Identification The same thing looks and is named the same everywhere.
3.3 Input Assistance
  A  3.3.1  Error Identification      Errors are pointed out and described in text.
  A  3.3.2  Labels or Instructions    Fields say what to enter before you enter it.
  A  3.3.7  Redundant Entry           Never make people type the same thing twice.
  AA 3.3.3  Error Suggestion          When you err, the site suggests how to fix it.
  AA 3.3.4  Error Prevention (Legal, Financial, Data)  Big commitments can be checked, fixed, or undone.
  AA 3.3.8  Accessible Authentication (Minimum)  Logging in never depends on memory or puzzles.

### ROBUST — Code is clean enough for assistive technology to read.
4.1 Compatible
  A  4.1.2  Name, Role, Value         Every control tells assistive tech what it is and does.
  AA 4.1.3  Status Messages           Updates are announced without stealing focus.

## 5. THE PERSON tree: branches, twigs, leaves

SEEING
  Without Vision — Works with no sight at all, by sound or touch.
    P  1.1.1  1.2.1  1.2.3  1.2.5  1.3.1  1.3.2  1.3.3  1.4.2
    O  2.1.1  2.1.2  2.4.1  2.4.2  2.4.3  2.4.4  2.4.6  2.5.3
    U  3.1.1  3.1.2  3.2.1  3.2.2  3.2.4  3.3.1
    R  4.1.2  4.1.3
  With Limited Vision — Works when you can see, but not well.
    P  1.1.1  1.2.1  1.2.3  1.2.5  1.3.1  1.4.1  1.4.3  1.4.4  1.4.5  1.4.10  1.4.11  1.4.12  1.4.13
    O  2.4.7  2.4.11
    R  4.1.2  4.1.3
  Without Color Perception — Works if every color looked the same.
    P  1.3.3  1.4.1  1.4.3  1.4.11
    U  3.3.1

HEARING
  Without Hearing — Works with the sound off.
    P  1.2.1  1.2.2  1.2.4
  With Limited Hearing — Works when sound is faint or muddy.
    P  1.2.1  1.2.2  1.2.4  1.4.2

SPEAKING
  Without Speech — Works without ever speaking aloud.
    (bare branch) No WCAG 2.2 criterion requires a non-voice alternative. Voice-driven
    kiosks and phone systems fall to 508's technical chapters, not to WCAG.

MOVING
  With Limited Manipulation — Works with shaky, slow, or one-handed control.
    P  1.3.4  1.3.5  1.4.13
    O  2.1.1  2.1.2  2.1.4  2.2.1  2.4.1  2.4.3  2.4.7  2.4.11  2.5.1  2.5.2  2.5.3  2.5.4  2.5.7  2.5.8
    U  3.3.7  3.3.8
    R  4.1.2
  With Limited Reach and Strength — Works without a long reach or a hard press.
    P  1.3.4
    O  2.5.1  2.5.4  2.5.7  2.5.8

THINKING
  With Limited Language, Cognitive, and Learning Abilities — Works when reading, memory, or focus is hard.
    P  1.3.5  1.4.12
    O  2.2.1  2.2.2  2.4.2  2.4.4  2.4.5  2.4.6
    U  3.1.1  3.1.2  3.2.1  3.2.2  3.2.3  3.2.4  3.2.6  3.3.1  3.3.2  3.3.3  3.3.4  3.3.7  3.3.8

ON THE GROUND (below the Person tree)
  2.3.1 Three Flashes — a fallen leaf. No functional performance criterion names
  photosensitivity; Section 508 reaches flashing only by incorporating WCAG.

## 6. Reading-guide (three sentences, in the gutter between the trees)
WCAG says what to build; the FPC say what a person must be able to do. Section 508 binds
WCAG 2.0 AA directly and uses the FPC where the technical rules are silent (E204.1). Find
a criterion on the left to learn what it means; find a person on the right to learn which
criteria they depend on.

## 7. Footer
- Sources: W3C WCAG 2.2; 36 CFR Part 1194 App. C Ch. 3 (access-board.gov/ict).
- License: CC BY-SA 4.0. "Adapted from the Intopia WCAG 2.2 Map, intopia.digital."
- Author, program, date.

## 8. Still open
- Person tree: radial mind-map (recommended) vs. a second left-to-right dendrogram mirrored
  against the first. Radial reads as a different organism; mirrored reads as a comparison.
- Whether leaf chips on the Person tree carry the short name or the number only. Name is
  better for reading, number only fits more; test at print size.
- Whether the Standard tree also shows tiny FPC ticks per leaf for reverse lookup. Current
  answer: no, the Person tree is the reverse lookup.
