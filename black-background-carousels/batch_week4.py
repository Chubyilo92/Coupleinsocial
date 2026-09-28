#!/usr/bin/env python3
"""CoupleIn week-4 batch: 90 carousels across three features.
Slide 1 = hook (claim / undercut). Slide 2 = the sharpening.
Slide 3 = the release + comment prompt. Slide 4 = app proof + closer.
"""

CLOSER = "7 days. Uninstall if nothing changes."

RELEASES = {
    "Calendar": [
        ("He's not refusing.", "It's just not in his week."),
        ("He doesn't forget on purpose.", "He has no system."),
        ("He's not careless.", "Nothing ever reminds him."),
        ("He's not lazy.", "Nobody nudges him but you."),
        ("It's not love that's missing.", "It's a shared calendar."),
    ],
    "Brownies": [
        ("He's not withholding.", "He doesn't know what counts."),
        ("He's not ignoring you.", "He's aiming blind."),
        ("He's guessing.", "You've never had to say it."),
        ("He'd do it.", "Nobody told him which one."),
        ("Effort isn't the problem.", "Aim is."),
    ],
    "Resolve": [
        ("He's not stonewalling.", "He's out of his depth."),
        ("He's not refusing to talk.", "He doesn't know the steps."),
        ("He shuts down when he's lost.", "He's not walking away."),
        ("It's not that he won't.", "It's that he can't yet."),
        ("He's not avoiding you.", "He's avoiding the mess."),
    ],
}

# she-directed rows get the same releases with the pronoun flipped
SHE_RELEASES = {
    "Calendar": [
        ("She's not disorganised.", "Nothing holds the plan."),
        ("She's not shutting you out.", "You were never in the diary."),
        ("She's not being difficult.", "She's carrying all of it."),
        ("She needs the nudge too.", "Not just you."),
        ("It's not the love.", "It's the order things get booked."),
    ],
    "Brownies": [
        ("She's not ungrateful.", "Nothing keeps score."),
        ("She can't say it plainly.", "Nobody taught her how."),
        ("You're not failing.", "You're aiming blind."),
        ("She'd tell you.", "If there were somewhere to."),
        ("She's not impossible.", "She's never been asked properly."),
    ],
    "Resolve": [
        ("She's not testing you.", "She's out of her depth."),
        ("She's not withholding.", "She doesn't know the steps."),
        ("She shuts down when she's lost.", "She's not walking away."),
        ("It's not that she won't.", "It's that she can't yet."),
        ("She's not avoiding you.", "She's avoiding the mess."),
    ],
}

PAYOFFS = {
    "Calendar": ["Now it's in his week.", "He gets the nudge. Not you.",
                 "One calendar. Both nudged."],
    "Brownies": ["Now he knows what counts.", "You list it. He does it.",
                 "Effort, with a scoreboard."],
    "Resolve": ["Seven steps. One timer.", "He knows what to say next.",
                "A fight with rules."],
}
SHE_PAYOFFS = {
    "Calendar": ["Now it's in her week.", "She gets the nudge too.",
                 "One calendar. Both nudged."],
    "Brownies": ["Now you know what counts.", "She lists it. You do it.",
                 "Effort, with a scoreboard."],
    "Resolve": ["Seven steps. One timer.", "You both know what's next.",
                "A fight with rules."],
}

KEYWORDS = {"Calendar": "NUDGE", "Brownies": "COUNTS", "Resolve": "CALM"}

# (direction, slide1a, slide1b, slide2a, slide2b)
CALENDAR = [
    ("he", "He'd take a bullet for you.", "He won't take the bins out.",
     "Bullets are hypothetical.", "Bins are Tuesday."),
    ("he", "He knows every kick-off time.", "He forgot your interview.",
     "He remembers what reminds him.", "Nothing reminds him of you."),
    ("he", "He's never missed a delivery slot.", "He missed your mum's birthday.",
     "Amazon texts him.", "You don't."),
    ("he", "You asked for a walk in March.", "It's September.",
     "He said yes that day.", "Then the week ate it."),
    ("he", "He says he's bad with dates.", "He's never missed a payday.",
     "He remembers what has a reminder.", "You've never had one."),
    ("he", "He booked the golf weekend.", "He didn't check with you.",
     "His diary knew.", "Yours found out late."),
    ("he", "He asked what's for dinner.", "He's never once planned it.",
     "Deciding is the work.", "He only sees the cooking."),
    ("he", "He'd drive two hours for his mate.", "He won't walk ten minutes with you.",
     "It isn't the distance.", "It's that nobody asked."),
    ("he", "\"Just remind me.\"", "You're not his PA.",
     "The reminding is the labour.", "He thinks it's the doing."),
    ("he", "He called it nagging.", "It was the fourth time.",
     "The fourth time isn't nagging.", "It's the first three failing."),
    ("he", "You stopped asking.", "He thinks that means sorted.",
     "That isn't peace.", "That's you giving up."),
    ("he", "He remembered the bins.", "Because you reminded him. Twice.",
     "That's not him remembering.", "That's you, outsourced."),
    ("he", "He's never late for work.", "He's always late for you.",
     "Work has consequences.", "He knows you'll wait."),
    ("he", "\"I'll do it later.\"", "That was three weeks ago.",
     "Later isn't a time.", "It's a way of not saying no."),
    ("he", "He'd notice the car pulling left.", "He hasn't noticed the bathroom.",
     "He services what gets booked in.", "Nothing books in the house."),
    ("he", "He made plans for Saturday.", "You found out from his mum.",
     "You're not in the loop.", "There isn't one."),
    ("he", "You carry the whole calendar.", "He carries his phone.",
     "You're the reminder system.", "That's a second job."),
    ("he", "\"You never told me.\"", "You told him twice. In writing.",
     "He heard it.", "It just never landed anywhere."),
    ("he", "He remembers what you owe him.", "Not what he promised you.",
     "One list lives in his head.", "The other never got written."),
    ("he", "He'd put up his mum's shelf.", "Yours has been down since May.",
     "It isn't unwillingness.", "Hers got asked once."),
    ("he", "He turned up empty-handed.", "He had eleven months' notice.",
     "It isn't thoughtlessness.", "It's a date nobody flagged."),
    ("she", "She fills every weekend.", "You find out on Friday.",
     "It isn't selfishness.", "You were never in the plan."),
    ("she", "She says you never plan anything.", "She's already booked the weekend.",
     "There's no room left.", "So you stopped trying."),
    ("she", "She remembers every date you missed.", "Not one you kept.",
     "The misses get logged.", "The rest evaporate."),
    ("she", "\"We should do that\" for months.", "You said yes every time.",
     "Yes isn't a date.", "Nothing got written down."),
    ("she", "She planned the whole weekend.", "Then resented doing it.",
     "She didn't want control.", "She wanted an offer."),
    ("she", "She said she'd handle it.", "She's handled it for years.",
     "Handling it isn't fine.", "It's just quieter."),
    ("she", "She asked you once.", "She's not asking again.",
     "That wasn't dropped.", "That was filed."),
    ("she", "She remembers your mum's birthday.", "Nobody remembers hers for her.",
     "She's the family calendar.", "Nobody runs hers."),
    ("she", "\"I'll just do it myself.\"", "That wasn't an offer.",
     "It's the sound of giving up.", "You heard permission."),
]

BROWNIES = [
    ("he", "He bought you flowers.", "You wanted the dishwasher emptied.",
     "He did something nice.", "Not the thing you asked for."),
    ("he", "He shows love his way.", "He's never asked how you receive it.",
     "Different isn't the problem.", "Guessing is."),
    ("he", "He tells his mates you're amazing.", "When did he last tell you?",
     "You hear it secondhand.", "That isn't hearing it."),
    ("he", "He thanks the delivery driver.", "He hasn't thanked you this month.",
     "Strangers get the manners.", "You get the defaults."),
    ("he", "He does the big gestures.", "You wanted the small, boring ones.",
     "Grand is easy once.", "Small is every week."),
    ("he", "He waited to be asked.", "Then said you should have asked.",
     "Being asked isn't initiative.", "It's instruction."),
    ("he", "He \"helped\" with the housework.", "It's his house too.",
     "Helping implies it's yours.", "That word is the problem."),
    ("he", "He noticed you got it wrong.", "Never when you got it right.",
     "Criticism gets voiced.", "Credit gets assumed."),
    ("he", "He did one nice thing.", "He's still waiting for credit.",
     "Effort isn't a favour.", "It's the rent."),
    ("he", "He loves you his way.", "You've been asking for yours.",
     "He isn't ignoring you.", "He's translating badly."),
    ("he", "\"I work hard for us.\"", "So do you. Unthanked.",
     "Two jobs get done here.", "One gets mentioned."),
    ("he", "He'd defend you to anyone.", "He laughed at his mate's dig.",
     "Defending you isn't loyalty.", "Not laughing is."),
    ("he", "He says he's not romantic.", "He was, for six months.",
     "That wasn't personality.", "That was effort."),
    ("he", "\"You never appreciate me.\"", "You thanked him on Sunday.",
     "He didn't hear it.", "Nothing kept score."),
    ("he", "He spends freely on his hobby.", "Yours gets called a treat.",
     "Same money.", "Different permission."),
    ("he", "He'd notice a haircut on telly.", "He's not noticed yours.",
     "He isn't blind.", "He's just not looking."),
    ("he", "He's generous with everyone.", "You get what's left.",
     "You're not last in his heart.", "You're last in the queue."),
    ("he", "He mocks the little rituals.", "He'd miss them if you stopped.",
     "The small stuff isn't silly.", "It's the whole relationship."),
    ("he", "He gave you a lie-in.", "He mentioned it four times.",
     "A gift with an invoice.", "Isn't a gift."),
    ("he", "\"I'd do anything for you.\"", "He's never asked what.",
     "Anything is easy to say.", "One specific thing isn't."),
    ("he", "He remembers your coffee order.", "Not one thing you've asked for.",
     "He can retain detail.", "Nothing points it at you."),
    ("she", "\"I don't need anything.\"", "She meant she shouldn't have to ask.",
     "It isn't a riddle.", "Nobody taught her to say it."),
    ("she", "She redid the washing you did.", "You stopped doing it.",
     "It wasn't the washing.", "It was the message."),
    ("she", "She praises her friend's husband.", "In front of you.",
     "She isn't comparing.", "It lands that way anyway."),
    ("she", "She wanted romance.", "She rolled her eyes at your last try.",
     "One eye-roll costs a year.", "She doesn't know that."),
    ("she", "She lists what you didn't do.", "What you did gets silence.",
     "You're not imagining it.", "Nothing records the wins."),
    ("she", "She said the gift was lovely.", "She's never once used it.",
     "She won't correct you.", "So you'll get it wrong again."),
    ("she", "She thanked you in March.", "You're still thinking about it.",
     "That's how rare it was.", "She has no idea."),
    ("she", "She notices everything you miss.", "Nothing you catch.",
     "The misses are loud.", "The rest is expected."),
    ("she", "She says she's easy to please.", "You've never once managed it.",
     "She isn't lying.", "She's just never said the thing."),
]

RESOLVE = [
    ("he", "He'd fight anyone for you.", "He won't finish one conversation.",
     "Fighting for you is easy.", "Sitting in it isn't."),
    ("he", "He says he hates arguing.", "He hates losing.",
     "It isn't conflict he avoids.", "It's being wrong."),
    ("he", "He went quiet.", "He calls it keeping the peace.",
     "That isn't peace.", "That's you alone in it."),
    ("he", "He wins every argument.", "He's losing you.",
     "Being right is cheap.", "It costs the room."),
    ("he", "He said \"calm down.\"", "It has never once worked.",
     "He isn't dismissing you.", "He has no other line."),
    ("he", "He walked out to cool off.", "He came back in three days.",
     "A break has a return time.", "That was a disappearance."),
    ("he", "He apologised for how you took it.", "Not for what he said.",
     "That isn't an apology.", "It's a redirect."),
    ("he", "He says he's not a talker.", "He talks fine to his mates.",
     "It isn't the talking.", "It's not knowing where it ends."),
    ("he", "He said \"whatever you want.\"", "Then sulked about what you wanted.",
     "That wasn't agreement.", "It was a withdrawal."),
    ("he", "He brings up 2021.", "You've apologised for it twice.",
     "Nothing ever closed.", "So everything stays open."),
    ("he", "He listens until he can reply.", "That isn't listening.",
     "He's waiting for his turn.", "Nobody showed him another way."),
    ("he", "He says you're overreacting.", "You under-reacted for months.",
     "It isn't the size of it.", "It's the twelfth time."),
    ("he", "He agrees just to end it.", "Nothing changes by Thursday.",
     "Agreeing isn't resolving.", "It's an exit."),
    ("he", "You're crying.", "He's on his phone.",
     "He isn't cold.", "He's frozen."),
    ("he", "\"I said sorry.\"", "He did it again on Tuesday.",
     "Sorry without change.", "Is just a pause."),
    ("he", "He'd sleep on the sofa.", "Rather than finish the sentence.",
     "Avoiding it feels safer.", "It only moves the bill."),
    ("he", "He raised his voice.", "Then said you made him.",
     "Nobody makes anyone shout.", "He's never been shown otherwise."),
    ("he", "\"It's not a big deal.\"", "It's been a big deal for months.",
     "He's measuring his side.", "Not yours."),
    ("he", "He changes the subject.", "Every single time.",
     "It isn't disinterest.", "It's panic in a nice coat."),
    ("he", "He says \"we're fine.\"", "You've not spoken properly in weeks.",
     "Fine is what he needs.", "Not what's true."),
    ("he", "He can debate anyone at work.", "He can't do ten minutes with you.",
     "At work there are rules.", "At home there are none."),
    ("she", "She said \"I'm fine.\"", "She punished you for believing her.",
     "She isn't playing games.", "She's never had to say it."),
    ("she", "She wants you to open up.", "She used the last thing against you.",
     "Once was enough.", "Now you don't."),
    ("she", "She vents to her friends first.", "You're the last to know.",
     "By then it's settled.", "You're answering a verdict."),
    ("she", "She asks what's wrong.", "Then corrects your answer.",
     "That isn't asking.", "That's a quiz."),
    ("she", "She says she's over it.", "It's back next argument.",
     "It didn't close.", "It went quiet."),
    ("she", "She cried. You apologised.", "Neither of you knows for what.",
     "It ended.", "It didn't resolve."),
    ("she", "She says you never listen.", "She's never let you finish.",
     "You're both interrupting.", "Nobody's holding the floor."),
    ("she", "She wants to talk at midnight.", "You're up at six.",
     "It isn't the hour.", "There's never a right one."),
    ("she", "She says \"forget it.\"", "She has not forgotten it.",
     "Forget it means drop it.", "It never means resolved."),
]

THEMES = [("Calendar", CALENDAR), ("Brownies", BROWNIES), ("Resolve", RESOLVE)]


def build_rows(start_id=43):
    rows, n = [], start_id
    for feature, items in THEMES:
        for i, (direction, s1a, s1b, s2a, s2b) in enumerate(items):
            rel = (SHE_RELEASES if direction == "she" else RELEASES)[feature][i % 5]
            pay = (SHE_PAYOFFS if direction == "she" else PAYOFFS)[feature][i % 3]
            rows.append({
                "id": f"P{n:03d}",
                "feature": feature,
                "aimed_at": direction,
                "s1a": s1a, "s1b": s1b,
                "s2a": s2a, "s2b": s2b,
                "s3a": rel[0], "s3b": rel[1],
                "keyword": KEYWORDS[feature],
                "s4": pay,
                "closer": CLOSER,
            })
            n += 1
    return rows


if __name__ == "__main__":
    rows = build_rows()
    print(len(rows), "rows")
    for f, _ in THEMES:
        sub = [r for r in rows if r["feature"] == f]
        he = sum(1 for r in sub if r["aimed_at"] == "he")
        print(f"{f}: {len(sub)} rows — {he} he / {len(sub)-he} she")
