#!/usr/bin/env python3
"""
THE READING PUB CRAWL
A Roguelike Adventure through the legendary pubs of Reading, UK

Complete all 10 pubs. Make it to Perfect Fried Chicken. Become a legend.
"""

import random
import sys
import os
import textwrap

# ── ANSI colours ──────────────────────────────────────────────────────────────
class C:
    RST  = '\033[0m'
    BOLD = '\033[1m'
    DIM  = '\033[2m'
    RED  = '\033[91m'
    GRN  = '\033[92m'
    YLW  = '\033[93m'
    BLU  = '\033[94m'
    MAG  = '\033[95m'
    CYN  = '\033[96m'
    WHT  = '\033[97m'

def bold(s):   return f"{C.BOLD}{s}{C.RST}"
def red(s):    return f"{C.RED}{s}{C.RST}"
def green(s):  return f"{C.GRN}{s}{C.RST}"
def yellow(s): return f"{C.YLW}{s}{C.RST}"
def cyan(s):   return f"{C.CYN}{s}{C.RST}"
def magenta(s):return f"{C.MAG}{s}{C.RST}"
def dim(s):    return f"{C.DIM}{s}{C.RST}"

def wrap(text, width=72):
    return '\n'.join(textwrap.fill(p, width) for p in text.split('\n'))

def hr(char='─', width=72):
    return char * width

# ── PUB DATA ──────────────────────────────────────────────────────────────────
PUBS = [
    {
        "id": 0,
        "name": "The Three Guineas",
        "street": "Station Hill",
        "emoji": "🚂",
        "desc": (
            "A grand Victorian pub right outside Reading station. Named after the point "
            "where Berkshire, Oxfordshire and Buckinghamshire meet. Packed with commuters, "
            "stag dos and confused tourists who missed their train to London."
        ),
        "specialty": "London Pride",
        "pint_price": 5.50,
        "bouncer": False,
        "sticky_carpet": False,
        "music": "background jazz",
        "encounters": [
            "A stag do from Swindon piles in, wearing matching pink cowboy hats. You nod respectfully.",
            "A man in a suit stares at the departures board through the window, nursing his pint with quiet desperation.",
            "Someone announces 'I'm only staying for one' very loudly. They've clearly been here for four.",
            "A group of Reading FC fans are relitigating a match from 2012 in extraordinary detail.",
            "A delayed train announcement echoes faintly from outside. Half the pub check their phones.",
        ],
    },
    {
        "id": 1,
        "name": "The Greyfriar",
        "street": "Greyfriars Road",
        "emoji": "🍺",
        "desc": (
            "A proper old-school Reading boozer on Greyfriars Road. Real ales, proper locals, "
            "and a carpet that has seen things no carpet should see. The kind of pub where "
            "everyone knows everyone, and they're mildly suspicious of you."
        ),
        "specialty": "Brakspear Oxford Gold",
        "pint_price": 4.80,
        "bouncer": False,
        "sticky_carpet": True,
        "music": "jukebox",
        "encounters": [
            "A regular called Dave gives you a detailed history of the pub since 1987. You didn't ask.",
            "The jukebox blares early-2000s indie. Half the pub mouths along to Mr Brightside.",
            "A terrier under the bar table stares at you with unsettling intelligence.",
            "Someone wins the quiz machine and does a small, private victory dance.",
            "The landlord polishes a glass he's been polishing for twenty minutes. It is very clean.",
        ],
    },
    {
        "id": 2,
        "name": "The Nag's Head",
        "street": "Friar Street",
        "emoji": "🐴",
        "desc": (
            "Right on Friar Street, the Nag's Head is a Reading institution. Two floors, "
            "a proper bar, and the kind of Friday energy that starts at 5pm and does not stop. "
            "The beer garden is technically a fire escape, but nobody minds."
        ),
        "specialty": "Guinness",
        "pint_price": 5.20,
        "bouncer": True,
        "sticky_carpet": True,
        "music": "loud chart music",
        "encounters": [
            "A hen party sweeps through like a glittery tidal wave. The bride is wearing a veil and crying—in a good way.",
            "Someone loudly explains why Reading absolutely deserves a Premier League club.",
            "A man carries four pints back from the bar with the focus of a brain surgeon.",
            "Someone from your school appears. You immediately study your phone.",
            "Two people try to use the same table. After a brief standoff, they agree to share.",
        ],
    },
    {
        "id": 3,
        "name": "The Monk's Retreat",
        "street": "Friar Street",
        "emoji": "🍽️",
        "desc": (
            "Reading's Wetherspoon on Friar Street. Cavernous, cheap, and philosophically "
            "committed to the idea that pints should cost under £3. The menu is the size of "
            "a small novel. It's 4pm and the place is somehow already absolutely rammed."
        ),
        "specialty": "whatever's cheapest",
        "pint_price": 2.75,
        "bouncer": False,
        "sticky_carpet": False,
        "music": "none (blissfully)",
        "wetherspoons": True,
        "encounters": [
            "A table of pensioners are absolutely destroying a full breakfast at 4pm with complete serenity.",
            "Someone is having a work meeting here. In a Wetherspoon. On Friday afternoon. Deep respect.",
            "The app crashes when you try to order. You go to the bar like a normal person and feel good about it.",
            "A child runs past carrying a plate of chips. No parent is visible. The chips are gone.",
            "The price of a pint is displayed in very large font. You feel something like joy.",
        ],
    },
    {
        "id": 4,
        "name": "The Blagrave Arms",
        "street": "Blagrave Street",
        "emoji": "🎯",
        "desc": (
            "A proper boozer just off the main drag, named after the Blagrave family who once "
            "owned half of Reading. Good real ales, pub quiz on Wednesdays, and a dartboard "
            "that gets genuinely competitive. The kind of place where you accidentally stay "
            "for three extra pints."
        ),
        "specialty": "West Berkshire Good Old Boy",
        "pint_price": 4.90,
        "bouncer": False,
        "sticky_carpet": False,
        "music": "radio",
        "encounters": [
            "A quiz team argues whether a hedgehog is a mammal. It is. They refuse to believe you.",
            "The landlord knows everyone's name. He does not know yours but is trying very hard.",
            "Someone challenges you to darts. They are extraordinarily good at darts.",
            "A birthday party in the corner is on round eight and invites you to join them.",
            "A bloke at the bar says 'same again' and the barman is already pulling it.",
        ],
    },
    {
        "id": 5,
        "name": "The Butler",
        "street": "Broad Street",
        "emoji": "🎩",
        "desc": (
            "Right on Broad Street, The Butler occupies a converted bank building with high "
            "ceilings and prices to match. Popular with the after-work crowd and people who "
            "say 'craft beer' unironically. The cocktail list is extensive. The gin menu "
            "is a genuine commitment."
        ),
        "specialty": "rotating craft IPA",
        "pint_price": 6.00,
        "bouncer": False,
        "sticky_carpet": False,
        "music": "curated indie playlist",
        "encounters": [
            "A group of office workers are doing 'team bonding'. It is not working.",
            "The bartender explains the provenance of a hop variety for ninety seconds without pausing.",
            "Someone is on a first date. It appears to be going well. You give an encouraging nod.",
            "A bloke orders a Stella. The bartender's face does something involuntary.",
            "The bar sells fourteen types of gin. You choose the one you've heard of.",
        ],
    },
    {
        "id": 6,
        "name": "Allied Arms",
        "street": "St Mary's Butts",
        "emoji": "⚓",
        "desc": (
            "A no-nonsense pub on St Mary's Butts, one of Reading's oldest surviving boozers. "
            "Real ale, proper crisps (not 'artisan'), and a landlord who has no time for nonsense. "
            "The locals are deeply loyal. You are not a local. That is fine. Probably."
        ),
        "specialty": "Abbot Ale",
        "pint_price": 4.50,
        "bouncer": False,
        "sticky_carpet": True,
        "music": "none",
        "encounters": [
            "A man with a very impressive beard nods at you once. You feel assessed and, somehow, accepted.",
            "Someone is reading an actual newspaper. A physical, paper newspaper. Like a wizard.",
            "A dog of indeterminate breed and enormous dignity walks to the far corner and lies down.",
            "The fruit machine pays out. The winner does not react. This is not their first time.",
            "Someone orders a port and lemon. The barman doesn't even blink.",
        ],
    },
    {
        "id": 7,
        "name": "Purple Turtle",
        "street": "Gun Street",
        "emoji": "🐢",
        "desc": (
            "Reading's legendary dive bar on Gun Street. Dark, loud, and absolutely essential. "
            "The Purple Turtle has been fuelling Reading's nights since time immemorial. "
            "Famous for cheap drinks and a clientele that spans every walk of life imaginable. "
            "The carpet is a work of abstract art."
        ),
        "specialty": "Purple Rain cocktail",
        "pint_price": 4.20,
        "bouncer": True,
        "sticky_carpet": True,
        "music": "BANGING",
        "encounters": [
            "The DJ drops something that makes everyone simultaneously look up from their phones.",
            "You find a token on the floor. The bar staff say it's from 2009. They still honour it. +£2.",
            "A Reading Uni student explains their dissertation to the bar. The bar listens politely.",
            "Someone spills a drink on you. They are immediately and profusely apologetic. The vibes remain.",
            "A group in full cowboy fancy dress are committed to the bit with admirable intensity.",
            "The bass physically vibrates your pint glass. This is good.",
        ],
    },
    {
        "id": 8,
        "name": "The Back of Beyond",
        "street": "King's Road",
        "emoji": "🌍",
        "desc": (
            "Reading's second Wetherspoon, on King's Road near the Oracle. Massive, "
            "efficient, and democratically cheap. The name refers to its slightly odd "
            "location behind everything. The breakfast is served until noon. It is 11:47. "
            "You may still make it."
        ),
        "specialty": "whatever's cheapest (again)",
        "pint_price": 2.80,
        "bouncer": False,
        "sticky_carpet": False,
        "music": "none",
        "wetherspoons": True,
        "encounters": [
            "You are technically in two postcodes simultaneously in this pub.",
            "A family of German tourists are baffled but delighted by the prices.",
            "Someone orders a 'pint of lager' and when asked which one says 'the yellow one'.",
            "You find a full, abandoned pint on a table. No one is nearby. A moral dilemma.",
            "The Oracle shopping centre is visible through the window, dark and cavernous.",
        ],
    },
    {
        "id": 9,
        "name": "Zerodegrees",
        "street": "Bridge Street",
        "emoji": "🍕",
        "desc": (
            "A microbrewery and pizzeria by the Oracle and the River Kennet. Brews its own "
            "beer on-site in big visible tanks. The pizza is genuinely good. The Mango Beer "
            "is either brilliant or appalling depending on your current state of sobriety. "
            "The Kennet glitters outside. You are nearly there."
        ),
        "specialty": "Zerodegrees Black Lager",
        "pint_price": 5.80,
        "bouncer": False,
        "sticky_carpet": False,
        "music": "ambient",
        "encounters": [
            "You can see the actual brewing tanks from your seat. You pretend to understand them.",
            "A table orders the Mango Beer and immediately disagrees about whether it's nice.",
            "The Oracle River is right outside. Someone sits on the steps eating chips by the water.",
            "A couple share a pizza and look annoyingly content with life. Fair enough.",
            "A waiter offers you the food menu. You stare at it for a long time and then order another drink.",
        ],
    },
]

FINAL_DEST = {
    "name": "Perfect Fried Chicken",
    "street": "Oxford Road",
    "desc": (
        "Perfect Fried Chicken, Oxford Road. The lights are fluorescent and entirely unforgiving. "
        "The queue is twenty deep. You order a large chips and a piece of chicken. "
        "It is, in this moment, the single greatest meal you have ever eaten in your life. "
        "You have done it. You have completed the Reading Pub Crawl."
    ),
}

DRINKS = {
    "p": {
        "name": "Pint",
        "label": "Pint of something good",
        "sobriety": -15,
        "bladder": 20,
        "charm_effect": 3,
        "desc": "A proper pint. The cornerstone of the evening.",
    },
    "d": {
        "name": "Double",
        "label": "Double spirit & mixer",
        "sobriety": -25,
        "bladder": 10,
        "charm_effect": 2,
        "desc": "Shots in a longer format. The civilised option.",
    },
    "s": {
        "name": "Shot",
        "label": "Shot (down in one)",
        "sobriety": -30,
        "bladder": 5,
        "charm_effect": 1,
        "desc": "Why do you do this to yourself. Why.",
    },
    "h": {
        "name": "Half",
        "label": "Half pint",
        "sobriety": -7,
        "bladder": 10,
        "charm_effect": 1,
        "desc": "Pacing yourself. Sensible.",
    },
    "w": {
        "name": "Water",
        "label": "Tap water (FREE)",
        "fixed_cost": 0.0,
        "sobriety": 10,
        "bladder": 10,
        "charm_effect": 0,
        "desc": "Free. Essential. The smartest thing you've done all night.",
    },
    "c": {
        "name": "Soft drink",
        "label": "Soft drink (Coke/lemonade)",
        "fixed_cost": 2.50,
        "sobriety": 5,
        "bladder": 12,
        "charm_effect": 0,
        "desc": "Sensible. People will judge you. You don't care.",
    },
    "j": {
        "name": "Jägerbomb",
        "label": "Jägerbomb",
        "fixed_cost": 6.50,
        "sobriety": -35,
        "bladder": 8,
        "charm_effect": 5,
        "desc": "No. And yet.",
    },
}

STREET_EVENTS = [
    ("You spot a kebab van on Friar Street. A donor wrap for £6 sobers you up slightly.",
     "food", 6.0, +12),
    ("You find a fiver on the pavement outside The Oracle. Today IS your day.",
     "money_found", 5.0, 0),
    ("It starts drizzling. Classic Reading. You walk faster.",
     "flavor", 0, 0),
    ("A night bus rumbles past. You briefly consider going home. You don't.",
     "flavor", 0, 0),
    ("A group of lads in Reading FC shirts cheer at you from across the road. You cheer back.",
     "flavor", 0, 0),
    ("Broad Street is heaving. You navigate through a river of people.",
     "flavor", 0, 0),
    ("A chip shop. You buy a small chips for £3. Salt and vinegar. Life-affirming.",
     "food", 3.0, +8),
    ("There's a cash machine on Broad Street. You withdraw £20 (plus a £1.75 fee you barely notice).",
     "cash_machine", 21.75, +20),
    ("A taxi driver shouts 'Y'alright mate?' You are, broadly speaking, alright.",
     "flavor", 0, 0),
    ("You stub your toe on a kerb. Ow.",
     "flavor", 0, 0),
    ("Someone from school recognises you. You can't remember their name. Neither can they. Perfect.",
     "flavor", 0, 0),
    ("A burger van. One onion ring for £1.50. Just the one. It's enormous.",
     "food", 1.5, +3),
    ("The Oracle fountain is lit up. It's actually quite beautiful at night.",
     "flavor", 0, 0),
    ("You pass the IDR underpass. It smells like all underpasses smell. You walk through quickly.",
     "flavor", 0, 0),
]

READING_MAP = """
╔═══════════════════════════════════════════════════════════╗
║              READING TOWN CENTRE                          ║
║                                                           ║
║  ← OXFORD RD ═══════ ST MARY'S BUTTS ══ BROAD STREET →   ║
║       │                    │                  │           ║
║  [6] Allied Arms    [7] Purple Turtle   [5] Butler        ║
║                                                           ║
║                    ══ FRIAR STREET ══                     ║
║                   [2] Nag's Head                         ║
║                   [3] Monk's Retreat                     ║
║                         │                                ║
║          [4] Blagrave Arms                               ║
║                         │                                ║
║  ════════════════ KING'S ROAD ════════════════           ║
║       [8] Back of Beyond      [9] Zerodegrees            ║
║                                    │                     ║
║         [1] Greyfriar        READING STATION             ║
║         (Greyfriars Rd)      [0] Three Guineas ← START   ║
║                                                           ║
║  FINISH: Perfect Fried Chicken, Oxford Road ←            ║
╚═══════════════════════════════════════════════════════════╝
"""

# ── PLAYER ────────────────────────────────────────────────────────────────────
class Player:
    def __init__(self):
        self.sobriety  = 100   # 0 = pass out = game over
        self.cash      = 40.0  # starting money
        self.bladder   = 0     # 100 = urgent
        self.charm     = 50    # 0-100, affects bouncer checks
        self.visited   = []    # pub ids completed
        self.location  = 0     # current pub index (or -1 = street)
        self.on_street = True

    def sober_str(self):
        s = self.sobriety
        if s >= 90: return green("Stone cold sober")
        if s >= 75: return green("Feeling fine")
        if s >= 60: return yellow("Nicely warmed up")
        if s >= 45: return yellow("Getting there")
        if s >= 30: return red("Noticeably wobbly")
        if s >= 15: return red("Quite drunk")
        return red("DANGEROUSLY DRUNK")

    def bladder_str(self):
        b = self.bladder
        if b <= 20: return green("Fine")
        if b <= 50: return green("Manageable")
        if b <= 70: return yellow("Getting urgent")
        if b <= 89: return red("URGENT")
        return red("CRITICAL — FIND TOILET NOW")

    def charm_str(self):
        c = self.charm
        if c >= 75: return green("Charming")
        if c >= 50: return green("Friendly")
        if c >= 30: return yellow("Passable")
        return red("Rough-looking")

    def status_bar(self):
        pubs_done = len(self.visited)
        bar = hr()
        sb  = f" Sobriety: {self.sober_str():<30}  Cash: {yellow('£'+f'{self.cash:.2f}')}"
        bl  = f" Bladder:  {self.bladder_str():<30}  Charm: {self.charm_str()}"
        pb  = f" Pubs: {cyan(str(pubs_done))}/10  {'  '.join(bold('★') if i in self.visited else dim('☆') for i in range(10))}"
        return f"{bar}\n{sb}\n{bl}\n{pb}\n{bar}"

# ── HELPERS ───────────────────────────────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg="Press ENTER to continue..."):
    input(f"\n{dim(msg)}")

def prompt(options_text):
    return input(f"\n{bold('> ')}").strip().lower()

def narrate(text):
    print(f"\n{wrap(text)}")

def event_box(title, text):
    print(f"\n{yellow('┌─ ' + title + ' ' + '─'*(60-len(title)) + '┐')}")
    for line in wrap(text, 68).split('\n'):
        print(f"{yellow('│')} {line}")
    print(f"{yellow('└' + '─'*70 + '┘')}")

def stat_change(label, before, after, unit=""):
    arrow = "▲" if after > before else "▼"
    colour = green if after > before else red
    delta = after - before
    sign = "+" if delta > 0 else ""
    return f"  {label}: {before}{unit} {colour(f'{arrow}{sign}{delta}{unit}')} → {after}{unit}"

# ── DRINK LOGIC ───────────────────────────────────────────────────────────────
def do_drink(player, pub, choice):
    if choice not in DRINKS:
        print(red("That's not on the menu."))
        return False

    drink = DRINKS[choice]
    name  = drink["name"]

    # price
    if "fixed_cost" in drink:
        cost = drink["fixed_cost"]
    else:
        base = pub["pint_price"]
        if name == "Double":  cost = round(base * 1.25, 2)
        elif name == "Shot":  cost = round(base * 0.70, 2)
        elif name == "Half":  cost = round(base * 0.55, 2)
        else:                 cost = base

    if player.cash < cost and cost > 0:
        narrate(red(f"You can't afford a {name.lower()} (£{cost:.2f}). You have £{player.cash:.2f}."))
        return False

    # apply effects
    sob_before = player.sobriety
    bld_before = player.bladder
    chm_before = player.charm

    player.cash      = round(player.cash - cost, 2)
    player.sobriety  = max(0, min(100, player.sobriety  + drink["sobriety"]))
    player.bladder   = max(0, min(100, player.bladder   + drink["bladder"]))
    player.charm     = max(0, min(100, player.charm      + drink["charm_effect"]))

    print(f"\n  {bold('You order a ' + drink['label'] + '.')}")
    if cost > 0:
        print(f"  {dim('The barman takes')} {yellow('£'+f'{cost:.2f}')} {dim('from your hand.')}")
    else:
        print(f"  {dim('It')}{green(' costs nothing')}. {dim('Wonderful.')}")
    print(f"  {dim(drink['desc'])}")
    print()
    print(stat_change("Sobriety", sob_before, player.sobriety))
    print(stat_change("Bladder",  bld_before, player.bladder,  "%"))
    if drink["charm_effect"] != 0:
        print(stat_change("Charm",  chm_before, player.charm))
    return True

# ── BOUNCER ───────────────────────────────────────────────────────────────────
def bouncer_check(player):
    challenges = [
        "The bouncer squints at you. 'How much have you had tonight, mate?'",
        "The bouncer crosses their arms. 'I'm not sure about this one.'",
        "The bouncer looks you up and down. Very slowly.",
        "'ID?' You show your ID. They examine it like it's a peace treaty.",
    ]
    narrate(yellow("🚷  " + random.choice(challenges)))

    # charm-based probability check
    threshold = 40 - (player.charm - 50) // 3
    roll = random.randint(1, 100)
    if roll > threshold or player.sobriety >= 50:
        print(f"  {green('You straighten up, smile with conviction, and are waved through.')}")
        return True
    else:
        print(f"  {red('\"Not tonight, mate.\" You are denied entry.')}")
        player.charm = max(0, player.charm - 5)
        return False

# ── TOILET ───────────────────────────────────────────────────────────────────
def use_toilet(player):
    before = player.bladder
    relief = min(player.bladder, random.randint(55, 80))
    player.bladder = max(0, player.bladder - relief)
    player.charm = min(100, player.charm + 2)
    narrate(
        f"You find the toilet (past the bar, down the stairs, left, "
        f"then right, past the fire exit door). "
        f"Relief washes over you."
    )
    print(stat_change("Bladder", before, player.bladder, "%"))

# ── PUB VISIT ────────────────────────────────────────────────────────────────
def visit_pub(player, pub):
    clear()
    print(player.status_bar())

    wethers = pub.get("wetherspoons", False)
    print(f"\n{bold(cyan('═══  ' + pub['emoji'] + '  ' + pub['name'].upper() + '  ═══'))}")
    print(dim(f"  {pub['street']}"))
    narrate(pub["desc"])

    if pub.get("sticky_carpet"):
        print(dim("  (The carpet makes a faint peeling sound with every step.)"))
    if pub["music"] != "none":
        print(dim(f"  Music: {pub['music']}"))

    # bouncer
    if pub.get("bouncer") and player.sobriety < 70:
        print()
        if not bouncer_check(player):
            pause()
            return False   # refused entry

    # random encounter on entry
    if pub["encounters"]:
        enc = random.choice(pub["encounters"])
        narrate(f"  {magenta('👀 ')}  {enc}")

    # track that we've been here (get the drink first)
    already_visited = pub["id"] in player.visited
    had_drink_here = already_visited

    print(f"\n{bold('You are at the bar.')}")
    if wethers:
        print(dim("  The prices are eye-wateringly good."))

    while True:
        print(f"\n{bold('What do you do?')}")
        pint_p = pub['pint_price']
        print(f"  {bold('[P]')} Pint of {pub['specialty']} (£{pint_p:.2f})")
        print(f"  {bold('[D]')} Double spirit & mixer (£{round(pint_p*1.25,2):.2f})")
        print(f"  {bold('[S]')} Shot (£{round(pint_p*0.70,2):.2f})")
        print(f"  {bold('[H]')} Half pint (£{round(pint_p*0.55,2):.2f})")
        print(f"  {bold('[W]')} Tap water (FREE)")
        print(f"  {bold('[C]')} Soft drink (£2.50)")
        print(f"  {bold('[J]')} Jägerbomb (£6.50)")
        print(f"  {bold('[T]')} Find the toilet  (Bladder: {player.bladder}%)")
        print(f"  {bold('[L]')} Leave the pub")
        if not had_drink_here:
            print(f"  {dim('  ↳ you need at least one drink to count this pub!')}")

        choice = prompt("")

        if choice == "l":
            if not had_drink_here:
                narrate(red("You haven't had a drink here yet! You can't count this pub on the crawl."))
                ans = input(f"  {dim('Leave anyway? (y/n): ')}").strip().lower()
                if ans != 'y':
                    continue
            break

        elif choice == "t":
            use_toilet(player)

        elif choice in DRINKS:
            success = do_drink(player, pub, choice)
            if success:
                if not had_drink_here:
                    had_drink_here = True
                    if pub["id"] not in player.visited:
                        player.visited.append(pub["id"])
                    narrate(green(f"  ★  You've drunk in {pub['name']}!  ({len(player.visited)}/10)"))

                # random mid-pub event
                if random.random() < 0.35 and pub["encounters"]:
                    enc = random.choice(pub["encounters"])
                    narrate(f"  {magenta('👀 ')}  {enc}")

                # bladder warning
                if player.bladder >= 85:
                    narrate(red("⚠️  Your bladder is at critical levels. FIND THE TOILET."))

                # sobriety check
                if player.sobriety <= 0:
                    return "passed_out"
        else:
            print(dim("  (Type a letter from the menu above)"))

    # bladder emergency on exit
    if player.bladder >= 95:
        narrate(red("You rush out and there's an incident in the doorway. Charm -10."))
        player.charm = max(0, player.charm - 10)
        player.bladder = max(0, player.bladder - 40)

    return True

# ── STREET WALK ──────────────────────────────────────────────────────────────
def walk_street(player, from_pub, to_pub):
    clear()
    print(player.status_bar())

    from_name = PUBS[from_pub]["name"] if from_pub < len(PUBS) else "the last pub"
    to_name   = PUBS[to_pub]["name"]   if to_pub   < len(PUBS) else FINAL_DEST["name"]

    narrate(bold(f"You head from {from_name} towards {to_name}..."))
    narrate(dim("The streets of Reading stretch ahead. The night air is cool and the pavement "
                "is busy with other souls on their own Saturday night odysseys."))

    # 0-2 street events
    num_events = random.randint(0, 2)
    used = set()
    for _ in range(num_events):
        idx = random.randint(0, len(STREET_EVENTS)-1)
        if idx in used:
            continue
        used.add(idx)
        ev_text, ev_type, ev_cost, ev_bonus = STREET_EVENTS[idx]
        narrate(f"  🚶 {ev_text}")
        if ev_type == "food":
            player.cash = round(player.cash - ev_cost, 2)
            player.sobriety = min(100, player.sobriety + ev_bonus)
            print(dim(f"     Cost: £{ev_cost:.2f}  |  Sobriety +{ev_bonus}"))
        elif ev_type == "money_found":
            player.cash = round(player.cash + ev_cost, 2)
            print(dim(f"     Cash +£{ev_cost:.2f}"))
        elif ev_type == "cash_machine":
            player.cash = round(player.cash + ev_bonus - ev_cost, 2)
            print(dim(f"     Cash +£{ev_bonus:.2f} (fee: -£{ev_cost-ev_bonus:.2f})"))

    # bladder warning on walk
    if player.bladder >= 80:
        narrate(yellow("⚠️  You are in dire need of a toilet. Get inside fast."))

    pause(f"Press ENTER to arrive at {to_name}...")

# ── WIN SCREEN ────────────────────────────────────────────────────────────────
def win_screen(player):
    clear()
    print(f"""
{bold(yellow('★'*72))}

{bold(cyan('  CONGRATULATIONS! YOU HAVE COMPLETED THE READING PUB CRAWL!'))}

{FINAL_DEST['desc']}

  Final stats:
    Sobriety remaining: {player.sobriety}/100
    Cash remaining:     £{player.cash:.2f}
    Charm:              {player.charm}/100
    Pubs completed:     {len(player.visited)}/10

{bold(yellow('★'*72))}
""")
    if player.sobriety >= 60:
        print(green("  You're barely even drunk. Legendary constitution."))
    elif player.sobriety >= 35:
        print(yellow("  You're pleasantly wobbly. A dignified performance."))
    elif player.sobriety >= 15:
        print(red("  You are extremely drunk. The chicken is helping."))
    else:
        print(red("  You can barely hold the chips. A true hero."))
    print()

# ── GAME OVER ────────────────────────────────────────────────────────────────
def game_over(player, reason):
    clear()
    print(f"""
{bold(red('━'*72))}

{bold(red('  GAME OVER'))}

{reason}

  You made it to {len(player.visited)}/10 pubs.
  Pubs visited: {', '.join(PUBS[i]['name'] for i in player.visited) or 'None'}

  {dim('(Run the game again to try again)')}

{bold(red('━'*72))}
""")

# ── TITLE ────────────────────────────────────────────────────────────────────
def title_screen():
    clear()
    print(bold(cyan("""
  ╔════════════════════════════════════════════════════════════╗
  ║                                                            ║
  ║       T H E   R E A D I N G   P U B   C R A W L          ║
  ║                                                            ║
  ║         A Roguelike Adventure — Reading, UK               ║
  ║                                                            ║
  ╚════════════════════════════════════════════════════════════╝
""")))
    print(wrap(
        "Your goal: visit all 10 legendary pubs of Reading town centre "
        "and make it to Perfect Fried Chicken on Oxford Road. "
        "Watch your Sobriety, manage your Cash, relieve your Bladder, "
        "and keep your Charm high enough to get past the bouncers.\n"
        "\nGood luck. You're going to need it."
    ))
    print(f"""
  Stats:
    {bold('Sobriety')}  — your health. Hits 0 and you pass out. Game over.
    {bold('Cash')}      — money for drinks. Start with £40.
    {bold('Bladder')}   — fills as you drink. Find toilets or face consequences.
    {bold('Charm')}     — affects bouncers and encounters. Be nice.

  In each pub: order at least one drink to count it on the crawl.
    {dim('(Water and soft drinks DO NOT count — you need the real thing)')}

  Tip: Tap water is free and restores sobriety. Use it wisely.
""")
    pause("Press ENTER to begin the crawl...")

# ── MAIN GAME ────────────────────────────────────────────────────────────────
def show_map(player):
    clear()
    print(bold(cyan("  MAP — READING TOWN CENTRE")))
    print(READING_MAP)
    visited_ids = player.visited
    print("  Pubs remaining:")
    for pub in PUBS:
        marker = bold(green("  ★ DONE")) if pub["id"] in visited_ids else dim("  ☆ todo")
        print(f"  [{pub['id']}] {pub['name']:30s}  {marker}")
    print()
    pause()

def main():
    title_screen()

    player = Player()

    # determine pub order (follow a sensible geographic route)
    crawl_order = list(range(len(PUBS)))
    # shuffle slightly — start at Three Guineas, end at Zerodegrees
    # but let player choose their route from a shortlist
    # For simplicity: fixed route that makes geographic sense
    route = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Three Guineas → ... → Zerodegrees

    for i, pub_id in enumerate(route):
        pub = PUBS[pub_id]

        # walk there (except first pub)
        if i > 0:
            walk_street(player, route[i-1], pub_id)

        # check sobriety before entering
        if player.sobriety <= 0:
            game_over(player, "You pass out on the pavement outside "
                      f"{pub['name']}. A kind stranger calls you a taxi.")
            return

        # pub visit loop (retry if bounced)
        attempts = 0
        while True:
            result = visit_pub(player, pub)
            if result == "passed_out":
                game_over(player,
                    f"You order one too many in {pub['name']} and slide gently "
                    "off your barstool. The barman calls you a cab.")
                return
            if result is False and attempts < 2:
                # bounced — try neighbouring pub or wait
                narrate(yellow(f"You hang around outside {pub['name']} for a bit..."))
                player.sobriety = min(100, player.sobriety + 5)
                narrate(dim("(Sobriety +5 from the fresh air)"))
                attempts += 1
                pause("Try again? (Press ENTER)")
            else:
                break

        # bladder check after leaving
        if player.bladder >= 100:
            narrate(red("You don't make it to the next pub in time. An embarrassing incident "
                        "outside the Civic Centre. Charm -15."))
            player.charm  = max(0, player.charm - 15)
            player.bladder = 20

        # running out of money?
        if player.cash < 2.75:
            narrate(yellow(f"⚠️  You're nearly skint (£{player.cash:.2f}). "
                           "There's a cash machine on Broad Street if you need it."))

        # map check
        clear()
        print(player.status_bar())
        narrate(bold(f"Pub {i+1}/10 done: {pub['name']} ✓"))
        if i < len(route) - 1:
            next_pub = PUBS[route[i+1]]
            narrate(f"Next stop: {bold(next_pub['name'])} on {next_pub['street']}.")
        print()
        choice = input(f"  {bold('[M]')} Map   {bold('[C]')} Continue   > ").strip().lower()
        if choice == 'm':
            show_map(player)

    # final walk to Perfect Fried Chicken
    walk_street(player, route[-1], len(PUBS))

    if player.sobriety <= 0:
        game_over(player, "You pass out on Oxford Road within sight of Perfect Fried Chicken. "
                  "So close. So very close.")
        return

    win_screen(player)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{dim('You abandon the crawl and go home. Sensible.')}\n")
        sys.exit(0)
