"""The search-plan posts (Oct 26, 2026): two a week, Tuesdays and Thursdays at 5:30 pm, Oct 27, 2026 to Oct 28, 2027.
Each targets a phrase people actually search ("I need someone to talk to", "feeling stuck in life", "nervous system reset"...)
and links only to pages that are always live: the quiz, the 10-Minute Human Reset, tonight's search pages, calls, the Nest.

Mix (from the research): about 40% searchable problems, 20% "you don't need to be in crisis to need someone to talk to",
15% nervous system / co-regulation, 10% Time/Money/Soul, 10% direct offers, 5% fun.

Run: python3 studio/year/search-posts.py   -> studio/year/search-posts.json (+ render list for render2.py)
"""
import json, pathlib, datetime
Y = pathlib.Path(__file__).resolve().parent
SITE = "https://theemotionalsupportline.com"
L = {"Q": "/quiz", "R": "/free/human-reset", "C": "/#calls", "N": "/#nest", "H": "/#chart", "Y": "/year-of-yes",
     "talk": "/blog/i-need-someone-to-talk-to", "vs": "/blog/therapist-vs-life-coach-vs-emotional-support",
     "co": "/blog/what-is-co-regulation", "ns": "/blog/nervous-system-regulation-in-real-life",
     "stuck": "/blog/feeling-stuck-in-life", "cost": "/blog/how-much-does-a-life-coach-cost",
     "done": "/blog/why-cant-i-get-anything-done", "call": "/blog/what-is-an-emotional-support-call"}
CHIP = {"Q": "Free 2-minute quiz", "R": "Free 10-Minute Human Reset", "C": "Book a 30-minute call", "N": "The Nest", "H": "Free Human Design chart", "Y": "Year of YES! Coaching"}
TAGS = {
    "talk": "#NeedSomeoneToTalkTo #TalkToSomeone #EmotionalSupport #YouAreNotAlone #FeelHeard #EmotionalSupportLine",
    "stuck": "#FeelingStuck #GetUnstuck #PersonalGrowth #Overwhelmed #LifeCoach #EmotionalSupportLine",
    "reg": "#NervousSystemRegulation #CoRegulation #NervousSystemReset #VagusNerve #CalmDown #EmotionalSupportLine",
    "tms": "#TimeManagement #MoneyMindset #SoulPurpose #YearOfYes #PersonalDevelopment #EmotionalSupportLine",
    "offer": "#EmotionalSupportLine #TalkToSomeone #LifeCoaching #SupportCall #TheNest #FeelHeard",
    "fun": "#EmoOwl #OwlLove #SelfCare #RealTalk #EmotionalSupportLine",
}
# (pillar, link, kicker, image headline, image subline, caption, owl pose)
P = [
 ("talk","talk","Real talk","I don't need therapy. I just need someone to talk to.","That's allowed.","That sentence is one of the most common things people search for. If it's you: you don't have to be in crisis to deserve a calm person who listens. Here are your options, from a friend with a clear ask to a 30-minute call.","phone"),
 ("stuck","Q","Quick check","Why can't I get anything done?","Maybe it's not motivation.","Three reasons you're stuck that have nothing to do with willpower: you don't know the next step, the next step brings up a feeling, or you're simply out of capacity. Take the free 2-minute quiz to find out which one is yours.","laptop"),
 ("reg","co","Nervous system","Sometimes another nervous system is the intervention.","Humans calm down with humans.","You've tried the breathing. You've tried the cold water. Still wired? That's not failure. Co-regulation is how humans settle: a steady voice, a calm presence, someone with you. Here's what it is and how to get more of it.","heart-hug"),
 ("stuck","stuck","Feeling stuck?","Stuck isn't lazy.","It usually means one of seven things.","Overwhelmed, unclear, afraid, under-supported, out of time, money-tight or disconnected from yourself. Each kind of stuck has a different first step. Here's how to tell which one you're in, and what to do next.","thinking"),
 ("talk","Q","Not sure?","You know you need something. But what?","Therapist, coach, friend or just someone to listen?","Six questions, two minutes, one plain answer. The free \"What do I need right now?\" quiz tells you what kind of support would help most this week, and gives you one thing to try today.","questions"),
 ("reg","R","Try this","Everything feels like too much.","10 minutes. 5 steps. No equipment.","Name it. Breathe out longer than you breathe in. Look around. Feel your feet. Reach for a human. That's the 10-Minute Human Reset, free and printable. The last step is the one most resets leave out.","tea-blanket"),
 ("stuck","done","For the overloaded","You're not lazy. You're overloaded.","Tired and wired at the same time is a sign.","Small tasks feel huge. You're busy all day and finish with nothing done. You feel guilty resting, so you never really rest. Sound familiar? Don't start with productivity. Start by settling, then pick one thing.","calm-glow"),
 ("offer","C","How it works","Pay. Pick a time. Talk to a real person.","Leave with a next step.","A support call is 30 minutes with a calm, trained human. Never AI. No sales call first. $75, and every call comes with a free month in the Nest. Book from the link.","headset-wink"),
 ("talk","talk","For the strong one","You've told your best friend three times already.","Who do you talk to now?","Not wanting to burden the people you love is one of the most common reasons people call us. A neutral person has no stake in what you decide, and you don't have to manage their feelings about your problem.","rain-cloud"),
 ("stuck","Q","Decision paralysis","Every option feels wrong.","That usually means every option protects something you care about.","Write the decision as one question. Under each option, write what it protects and what it costs. Notice which one your body leans toward. Still circling? Saying it out loud to someone neutral often breaks it open.","decisions"),
 ("reg","ns","Nervous system","Regulated doesn't mean calm all the time.","It means you can come back.","A regulated day still has stress in it. You just don't stay stuck there. Here's what nervous system regulation actually means, what dysregulation can feel like, and a reset that includes people.","rooted-tree"),
 ("tms","N","Time","Every hour belongs to someone else.","Including the ones you call free time.","Write down what you did yesterday, hour by hour. Circle one thing you could drop, delegate or do half as well this week. Time Joy-gasm in the Nest is ten short classes on getting your hours back.","compass"),
 ("talk","vs","Life coach vs therapist","Therapist, coach or someone to talk to?","Different jobs. Here's which is which.","Therapy treats mental health conditions. Coaching builds toward a goal over months. Emotional support is for the in-between: someone calm to listen and help you think it through this week. Here's a plain-English guide.","decisions"),
 ("stuck","Q","Overthinking?","You may not need to think harder.","You may need to think out loud.","Overthinking is often a mind trying to solve a feeling. Saying it out loud to a calm person helps you hear where the story gets stuck. Not sure what you need? The free 2-minute quiz will tell you.","thinking"),
 ("reg","R","Vagus nerve reset","Long exhale. Then another.","Free, and it takes two minutes.","Breathe in for four, out for six to eight, like blowing through a straw. Ten rounds. Slow exhales are one of the simplest ways people settle. It's step two of the free 10-Minute Human Reset.","joyful-meditation"),
 ("fun","Q","EmoOwl says","Hoo needs a hug?","Asking for a friend.","EmoOwl is two owls, because nobody should have to sit with the hard stuff alone. If today's heavy, take the 2-minute quiz and find out what would actually help.","love-wink"),
 ("talk","C","Not in crisis","You don't have to be falling apart to deserve support.","Not every hard day is an emergency.","Some days aren't a crisis. They're just heavy. A 30-minute call with a calm, real person can help you sort through what you're feeling and find one clear next step. Book from the link.","headphones"),
 ("stuck","stuck","How to get unstuck","You don't need a grand purpose.","You need one next step you can actually take.","Movement creates clarity, not the other way around. Finish this sentence: \"The smallest step I could take in ten minutes is...\" Then do it today.","north-star"),
 ("offer","cost","Life coach cost","How much does a life coach cost?","$75 to $300+ a session, often more.","Life coaching prices are all over the place. Here's what you get at each level, when coaching is worth it, and lower-cost ways to get real support, like a single call or a $19 membership.","compass"),
 ("reg","co","Co-regulation","Laughing together is a nervous system reset.","So is walking side by side.","Co-regulation between adults looks like a friend who listens without fixing, a partner sitting beside you, a slow steady voice on the phone. Who leaves you calmer than they found you? Spend more time near them.","flying-joy"),
 ("talk","talk","Lonely?","Lonely doesn't always mean alone.","Sometimes it means unheard.","You can be surrounded by people and still have no one to tell the real thing to. That's lonely too. If you need someone to talk to, here are your options.","rain-cloud"),
 ("stuck","Q","Overwhelmed","Too much to do. Too little left.","Which kind of overwhelmed are you?","Overwhelm has flavors: too many tasks, too many feelings, too many people needing you. Each one has a different first step. The free 2-minute quiz helps you find yours.","umbrella"),
 ("tms","N","Money","When I think about money, I feel...","Finish the sentence without numbers.","Money worries rarely stay about money. They bleed into sleep, relationships and how you see yourself. Soul-Conomics in the Nest looks at the feeling under the numbers. (Not financial advice. Just the human side.)","journaling"),
 ("talk","call","What happens on a call","What actually happens on a support call?","You talk. They listen. You find a next step.","No intake forms. No diagnosis. One issue, 30 minutes, a trained person who reflects back what they hear and helps you sort it out. Here's exactly what to expect.","headset-wink"),
 ("stuck","done","Procrastination","Procrastination is often a feeling, not a flaw.","Fear, dread or shame, wearing a to-do list.","If you know the next step but can't start, ask: what feeling am I avoiding? Name it out loud. A lot of \"procrastination\" dissolves once you've said the scary part to another person.","studying"),
 ("reg","R","Overwhelmed?","Name it. Three words.","\"Tight. Rushed. Scared.\"","Naming a feeling tends to turn the volume down a little. You don't have to fix it yet. It's step one of the free 10-Minute Human Reset.","journaling"),
 ("offer","N","The Nest","A library you'll actually use.","Because there's a human in it.","The Nest: Year of YES! courses with workbooks, guided meditations, daily tools for morning light and time outside, a live group call every month, and $50 support calls. $19 a month.","sunrise"),
 ("talk","vs","Is a life coach worth it?","Is a life coach worth it?","Depends what you need this week.","Coaching is worth paying for when you have a clear goal and want accountability for months. If what you need right now is to be heard, a single support call often does more, for a lot less. Here's how to choose.","questions"),
 ("stuck","stuck","Midweek check-in","Same job. Same arguments. Same to-do list.","There should be more than this.","Feeling stuck in life is one of the most common things people tell us. It almost never means lazy. Here's why it happens and what to do next.","rain-cloud"),
 ("reg","ns","Dysregulated?","Tired and wired at the same time?","Snapping, then feeling guilty?","These are common human responses to too much for too long, not a character flaw. Here's what dysregulation can look like, and what actually helps (including people).","calm-glow"),
 ("talk","talk","Who can I talk to?","Who can I talk to at 2 pm on a Tuesday?","When it's not an emergency, but it can't wait.","Friends are at work. Therapy has a waiting list. Crisis lines are for danger. For the in-between, there's a calm person and a 30-minute call. Here are your options.","phone"),
 ("stuck","Q","Burnout or a bad week?","Burnout or a bad week?","One rests away. One doesn't.","A bad week gets better after a weekend. Burnout doesn't. If rest isn't working anymore, take the free 2-minute quiz and see what you actually need.","sleeping"),
 ("tms","H","Be who you are","Stop being who you were conditioned to be.","Find out who you actually are.","Society taught you who to be: agreeable, busy, small enough to fit. Your Human Design chart shows who you were before all that. Learn it, explore it, and then don't apologize for it. Get your free chart in about a minute.","bodygraph"),
 ("reg","co","Co-regulation","Calm is contagious.","So is panic. Choose your people.","Our nervous systems pick up on each other's tone, pace and faces. That's co-regulation, and it's not just for babies. Here's how adults do it.","lotus-hug"),
 ("offer","C","Real people","Never AI.","A real, trained human on every call.","When you need to talk, you need a person. Every Emotional Support Line call is 30 minutes with a calm, real human. $75, plus a free month in the Nest.","headset-wink"),
 ("talk","talk","Permission slip","You're allowed to need someone.","Even if it \"isn't that bad.\"","Comparing your pain to other people's doesn't make it lighter. It just makes you lonelier. If you need someone to talk to, that's reason enough.","heart-wings"),
 ("stuck","Q","Get unstuck","Not sure what kind of stuck you are?","Two minutes. Six questions.","Overwhelmed? Unclear? Under-supported? Out of time? The free \"What do I need right now?\" quiz gives you a plain answer and one thing to try today.","idea"),
 ("reg","R","Look around","Five things you can see.","Three things you can hear.","Slowly turn your head and let your eyes land on five things. Then three sounds. It tells your body where you are: here, now, not inside the worry. Step three of the free 10-Minute Human Reset.","curious"),
 ("stuck","done","Productivity","Don't start with productivity.","Start with capacity.","If you're running on empty, a better planner won't fix it. Settle first, then choose one thing. Here's how to tell an information problem from an emotion or capacity problem.","laptop"),
 ("fun","C","EmoOwl fact","Owls can turn their heads 270 degrees.","We still recommend looking at one problem at a time.","One issue. One real person. 30 minutes. One next step. That's a support call. Book from the link.","curious"),
 ("talk","vs","What kind of help?","What kind of help do I need?","A quick guide.","Diagnosis or treatment? Therapist. In danger? 988. A goal over months? Coach. Someone to listen and help you think it through? Emotional support. Here's the full guide.","decisions"),
 ("stuck","stuck","Purpose","Purpose isn't a job title.","It's what lights you up on a Tuesday.","You don't need to find one grand purpose. Notice what you lose track of time doing. That's a clue. Here's what to do when you feel stuck.","north-star"),
 ("reg","ns","Nervous system reset","What a nervous system reset can and can't do.","Two minutes helps for two minutes.","Humming, long exhales, feet on the earth: simple, free and worth doing. But if your life has too much in it, a reset alone won't fix that. Here's the whole picture.","sound-meditation"),
 ("tms","N","White Space","Unscheduled time isn't wasted time.","It's where your capacity comes back.","White Space is a class in Time Joy-gasm, inside the Nest: why the empty hours on your calendar are the ones that keep you going.","hammock"),
 ("talk","C","Talk it through","Say it out loud.","Halfway through the sentence, the answer often shows up.","Thinking it through alone keeps it in a loop. Talking it through with a calm person helps you hear what you actually think. Book a 30-minute call.","headphones"),
 ("stuck","Q","Overloaded","3 signs you're overloaded, not lazy.","1. Small tasks feel huge. 2. Busy all day, nothing done. 3. Rest feels guilty.","If that's you, the answer isn't more discipline. Take the free 2-minute quiz to see what you need right now.","umbrella"),
 ("offer","Y","Year of YES!","Ready to make next year yours?","Year of YES! Coaching with Tracee Sioux.","Twelve months, two hours a month, one-on-one, guided by your Human Design chart. Includes the Nest. By application.","sun-heart"),
 ("reg","R","Feet on the ground","Press your feet into the floor.","Better yet, into the grass.","Notice the ground holding you up. Hand on your chest. A long, low hum on the exhale. Step four of the free 10-Minute Human Reset.","earthing"),
 ("talk","talk","Not a burden","Needing to talk doesn't make you a burden.","It makes you human.","If you've been the one everyone leans on, it's okay to lean too. Here's how to find someone to talk to when you don't want to burden friends.","heart-hug"),
 ("stuck","stuck","Feeling stuck in life","Movement creates clarity.","Not the other way around.","Waiting until you're sure before you move keeps you stuck. Take one small step and see what it tells you. Here's how to get unstuck.","sunrise"),
 ("reg","co","Humans regulate with humans","You weren't meant to do this alone.","Literally. Your nervous system agrees.","A lot of us learned to \"handle it ourselves.\" It works until it doesn't. Co-regulation is the other half of calming down. Here's what it is.","circle-of-people"),
 ("fun","Q","Owl wisdom","Wise owls ask for help.","The other kind just hoot louder.","Not sure what kind of help you need? The free 2-minute quiz is a good place to start.","love-wink"),
 ("tms","H","Human Design","No more apologizing for how you're built.","Your chart is a permission slip.","Some people decide from the gut, some need to sleep on it, some need to talk it out. None of those is wrong. Learn how YOU are designed to decide, then stop apologizing for it. Free chart in a minute.","hd-types"),
 ("talk","call","Support call","Not therapy. Not a crisis line.","A calm person, 30 minutes, one next step.","Emotional support is the in-between kind of help most of us need most often. Here's what an emotional support call is and who it's for.","headset-wink"),
 ("stuck","done","Can't focus?","Your to-do list isn't the problem.","Your capacity is.","When you're overloaded, every task feels like a mountain. Drop one thing this week, then see what's easier. Here's the full guide.","cozy-coffee"),
 ("reg","ns","Wired at night?","Racing thoughts at bedtime?","That's your system still on alert.","Slow exhales, dim lights and saying the worry out loud (even to a journal) help the body shift into rest. Here's nervous system regulation in real life.","moon-night"),
 ("offer","C","Free month","Every call comes with a free month in the Nest.","Talk it through, then keep going.","Book a $75 support call and your free month in the Nest starts: courses, meditations and the monthly group call. Book from the link.","sunrise"),
 ("talk","Q","Check in","How are you, really?","Not the polite answer.","If the honest answer is \"I don't know,\" the free 2-minute quiz can help you figure out what you need right now.","questions"),
 ("stuck","stuck","Stuck vs resting","Not every pause is stuck.","Sometimes it's winter.","Rest is part of every cycle. But if the pause feels heavy and endless, here's how to tell, and what to do next.","winter-cocoa"),
 ("reg","R","When it's all too much","Reach for a human.","Step 5. The one most resets skip.","Text someone steady. Call a friend for five minutes. Or book a call with a real person. The free 10-Minute Human Reset ends with people for a reason.","phone"),
 ("tms","N","Money mindset","Money worries are feelings too.","Look at the feeling under the numbers.","Soul-Conomics, inside the Nest, is seven classes on the emotional side of money. Not financial advice. The human part nobody else talks about.","journaling"),
 ("talk","talk","Someone to listen","Sometimes you don't need advice.","You need someone to listen.","\"Can I just talk for ten minutes?\" is a complete request. Here's how to find someone to talk to, including when you'd rather it be someone outside your life.","headphones"),
 ("stuck","Q","Decision time","Big decision coming up?","Find out what's really in the way.","Sometimes it's fear, sometimes it's missing information, sometimes you just need to say it out loud. The free 2-minute quiz helps you sort it.","decisions"),
 ("reg","co","Co-regulation","\"Can you just stay on the phone while I walk?\"","Is a complete request.","Ask for presence, not advice. It's one of the fastest ways to settle. Here's more on co-regulation between adults.","phone"),
 ("offer","cost","Support options","A support call, a membership or a coach?","Here's what each costs.","A 30-minute call is $75. The Nest is $19 a month. Year of YES! Coaching is a 12-month program. Most life coaches charge $75 to $300+ a session. Here's how to choose.","compass"),
 ("talk","vs","Category","Emotional support is its own thing.","It's not therapy, and it's not coaching.","It's for the in-between: when nothing is catastrophically wrong, but you need to talk it through. Here's how it compares.","heart-hug"),
 ("stuck","done","Monday energy","Can't start the week?","Start with the smallest possible step.","\"Sort out my life\" isn't a task. \"Find last month's bank statement\" is. Break it down until the first step takes under ten minutes.","laptop"),
 ("reg","R","Breathe","In for 4. Out for 8.","Ten rounds. That's it.","Long, slow exhales are one of the simplest ways to settle. Part of the free, printable 10-Minute Human Reset.","joyful-meditation"),
 ("fun","C","EmoOwl hours","EmoOwl doesn't do night shifts.","But real humans take calls Mondays and Tuesdays.","Book a 30-minute call with a calm, real person. Noon to 7 pm Mountain. Not a crisis line: in danger, call or text 988.","sleeping"),
 ("tms","Y","Soul","If no one would be disappointed...","What would you do with this year?","Write the first answer before your Ego edits it. Then, if you're ready to say YES! to it, Year of YES! Coaching with Tracee Sioux is by application.","sun-heart"),
 ("talk","talk","Grief, stress, change","Big change. No one to process it with.","You don't have to carry it alone.","Moves, breakups, layoffs, empty nests, diagnoses in the family. Life transitions need a place to land. Here's how to find someone to talk to.","umbrella"),
 ("stuck","stuck","How to get my life together","You don't have to fix your whole life today.","Just the next ten minutes.","\"Get my life together\" is too big to start. Pick one corner: one drawer, one email, one conversation. Here's how to get unstuck without overwhelm.","sunrise"),
 ("reg","ns","Shutdown","Scrolling for hours isn't laziness.","It can be a nervous system hitting pause.","Numb and checked-out is a state too, not a character flaw. Gentle movement, light and a kind voice help you come back. Here's how.","rest-with-cat"),
 ("offer","N","Group call","First Sunday of every month.","A live group call in the Nest.","Bring a question, or just listen. Being with other people working on the same things is powerful, and it's included in the Nest at $19 a month.","circle-of-people"),
 ("talk","C","No sales call","No intake form. No sales call.","Just book and talk.","Pay, pick a time, and a calm real person calls you. 30 minutes, one issue, one next step. Plus a free month in the Nest.","headset-wink"),
 ("stuck","Q","Mid-year check","Halfway through the year and nothing's moved?","Find out why.","Overwhelmed, unclear, afraid or under-supported: each needs a different first step. Take the free 2-minute quiz.","questions"),
 ("reg","co","Calm people","Who leaves you calmer than they found you?","Spend more time near them.","That's co-regulation in real life. Notice your calm people, and be one for someone else when you can.","lotus-hug"),
 ("tms","N","Phone rules","Your phone is not a to-do list.","(Even if it acts like one.)","Phone Rules is a class in Time Joy-gasm, inside the Nest: simple boundaries that give you back hours of your week.","smartphone"),
 ("talk","talk","Say the thing","The thing you haven't said out loud yet?","That's the one to talk about.","If it's been circling for weeks, it's probably time to say it to someone. Here's how to find someone to talk to.","heart-wings"),
 ("stuck","done","Busy vs productive","Busy all day. Nothing done.","Sound familiar?","Busyness can be a way to avoid the one thing that matters. Ask: what am I avoiding? Then do ten minutes of it. More here.","laptop"),
 ("reg","R","Hard day?","Ten minutes. Five steps.","Free and printable.","Name it, breathe out longer, look around, feel your feet, reach for a human. The 10-Minute Human Reset is free.","tea-blanket"),
 ("fun","Q","Owl poll","Which owl are you today?","Sleepy, wired or \"fine\"?","Whatever the answer, the free 2-minute quiz can help you figure out what you actually need.","excited"),
 ("offer","C","When it's happening now","When it's happening now, you need someone now.","Same-week calls with a real person.","30 minutes with a calm, trained human who listens. $75, or $50 for Nest members. Not a crisis line: in danger, call or text 988.","headset-wink"),
 ("talk","vs","Therapy alternative?","Not every problem needs a therapist.","Some need a good listener.","We'll always tell you if what we hear sounds like it needs a licensed professional. For everything else, there's emotional support. Here's how to choose.","decisions"),
 ("stuck","stuck","Purpose","How to find your purpose:","Stop looking for one big answer.","Purpose is a direction, not a destination. Follow what makes you curious this month. Here's how to get unstuck when you don't know what you want.","north-star"),
 ("reg","ns","Regulation","You can't think your way out of a body that's on alert.","Settle first. Then think.","That's why advice doesn't land when you're flooded. Here's what nervous system regulation looks like in real life.","calm-glow"),
 ("tms","H","Human Design","Generator, Projector, Manifestor or Reflector?","Then be that. Loudly.","Your free Human Design chart shows the you underneath the conditioning. Explore it, try it on, and BE who you are. Want the whole picture? Tracee offers 2-hour readings.","hd-types"),
 ("talk","talk","Hard conversation","Need to rehearse a hard conversation?","Practice it out loud first.","Saying it to a neutral person first helps you find the words, and the calm. Here's how to find someone to talk to.","phone"),
 ("stuck","Q","Fall reset","New season. Same stuck?","Two minutes to find out why.","Seasons change faster than we do. The free quiz gives you one plain answer and one thing to try today.","questions"),
 ("reg","co","Co-regulation","Walk and talk.","Side by side is easier than face to face.","Hard conversations often go better while walking. Moving together helps both nervous systems settle. More on co-regulation here.","earth"),
 ("offer","N","The Nest","Year of YES! courses, meditations and a monthly group call.","$19 a month.","Soul-Conomics, Time Joy-gasm, Soul vs Ego Smackdown, Harvest and more, plus daily tools for light and time outside. Come as you are.","sunrise"),
 ("talk","C","Today","If today is heavy, you can talk to someone today.","A calm, real person. 30 minutes.","Book a call, pick a time, and we'll call you. No membership needed. Not a crisis line: in danger, call or text 988.","headphones"),
 ("stuck","done","Time leak","Where does your time actually go?","Track one day. Just one.","Write down yesterday, hour by hour. You'll find the leak. Then drop, delegate or do half as well one thing. More on getting things done when you're overloaded.","compass"),
 ("reg","R","Reset","Step 1: Name it.","Step 5: Reach for a human.","Everything in between is in the free, printable 10-Minute Human Reset.","tea-blanket"),
 ("tms","Y","Year of YES!","What would you say YES! to?","If you weren't so busy saying yes to everyone else?","Year of YES! Coaching is twelve months with Tracee Sioux, guided by your Human Design chart. By application.","sun-heart"),
 ("talk","talk","Holidays","Family time can be lonely too.","Even in a full house.","If the holidays bring up old roles and old hurts, you're not the only one. Here's how to find someone to talk to.","winter-cocoa"),
 ("stuck","stuck","New year","Skip the resolution.","Take one small step instead.","You don't need to reinvent yourself on January 1. You need one next step. Here's how to get unstuck, any day of the year.","sunrise"),
 ("reg","ns","Overwhelm","Everything feels urgent?","That's the alarm, not the truth.","When your system is on high alert, everything looks like an emergency. Settle first, then sort. Here's how.","umbrella"),
 ("fun","C","EmoOwl","Two owls. One job.","Making sure you're not alone with it.","The Emotional Support Line: talking about feelings, brainstorming solutions, regulating nervous systems. Book a call.","love-wink"),
 ("talk","Q","One year in","A year of small steps adds up.","Where are you now?","Take the 2-minute quiz and see what you need right now. Then take one small step.","excited"),
 ("reg","R","Spring reset","New season, same tight shoulders?","Ten minutes. Five steps.","The free 10-Minute Human Reset: name it, breathe out longer, look around, feel your feet, reach for a human. Print it and keep it on the fridge.","gentle-stretch"),
 ("stuck","done","Summer slump","Can't get anything done in the heat?","It might be capacity, not character.","Energy rises and falls with the seasons. Work with it instead of against it. Here's how to tell what kind of stuck you're in.","beach"),
 ("talk","talk","Back to school","Everyone needs you. Who do you talk to?","The strong one needs someone too.","If you're the one holding everything together this season, you deserve a place to set it down. Here's how to find someone to talk to.","heart-hug"),
 ("offer","C","Talk it through","Need someone to talk to? Talk it through.","The Emotional Support Line.","Talking about feelings. Brainstorming solutions. Regulating nervous systems. With a real person, 30 minutes, plus a free month in the Nest.","headset-wink"),
]
assert len(P) >= 104, len(P)
CR = "Not a crisis line. If you're in danger or thinking about suicide, call or text 988 (US)."

start = datetime.date(2026, 10, 27)  # a Tuesday
dates = []
d = start
while len(dates) < len(P):
    dates.append(d)
    d += datetime.timedelta(days=2 if d.weekday() == 1 else 5)  # Tue -> Thu -> next Tue

# Seasonal posts go on the right week, not wherever they fall in the list
SEASON = {"Holidays": "2026-12-15", "New year": "2026-12-31", "Spring reset": "2027-03-23", "Mid-year check": "2027-06-29",
          "Summer slump": "2027-07-15", "Back to school": "2027-08-17", "Fall reset": "2027-09-21", "One year in": "2027-10-21",
          "Fall reset ": "", "Midweek check-in": ""}
seasonal = {SEASON[p[2]]: p for p in P if SEASON.get(p[2])}
rest = [p for p in P if not SEASON.get(p[2])]
iso = [x.isoformat() for x in dates]
P = []
for day in iso:
    P.append(seasonal.pop(day) if day in seasonal else rest.pop(0))
assert not seasonal, seasonal

def bsky(head, sub, cap, url, invites):
    tail = f"\n\n{url}" + ("\n\nNot a crisis line. In danger? Call or text 988 (US)." if invites else "")
    text, room = f"{head} {sub}\n\n{cap}", 295 - len(tail)
    if len(text) > room:
        text = text[:room - 1].rsplit(" ", 1)[0].rstrip(".,;:") + "…"
    return text + tail


posts, render = [], []
for k, ((pillar, lk, kicker, head, sub, cap, pose), day) in enumerate(zip(P, dates)):
    pid = f"s{k + 1:03d}-{day:%b%d}".lower()
    url = SITE + L[lk]
    chip = CHIP.get(lk, "Read the guide")
    invites = lk in ("C", "talk", "call", "co") or "talk" in cap.lower() or "call" in cap.lower()
    body = cap + ("\n\n" + CR if invites and "988" not in cap else "")
    tags = TAGS[pillar]
    posts.append({"id": pid, "date": day.isoformat(), "time": "17:30", "type": "search", "pillar": pillar, "link": url,
                  "image": f"{SITE}/social/search/{pid}.jpg",
                  "instagram": f"{head} {sub}\n\n{body}\n\nLink in bio.\n\n{tags}",
                  "facebook": f"{head} {sub}\n\n{body}\n\n{url}\n\n{' '.join(tags.split()[:2])} #EmotionalSupportLine",
                  "linkedin": f"{head} {sub}\n\n{body}\n\n{url}",
                  "bluesky": bsky(head, sub, cap, url, invites),
                  "pinterest": {"title": (head if len(head) <= 95 else head[:92] + "..."), "description": f"{sub} {cap}"[:470]}})
    render.append({"id": f"{pid}", "type": "relatable", "text": head, "sub": sub, "kicker": kicker, "cta": chip, "pose": pose,
                   "owl": ["You're not alone.", "I hear you.", "Been there.", "Same, friend.", "Hoo, me too."][k % 5]})
(Y / "search-posts.json").write_text(json.dumps(posts, indent=1, ensure_ascii=False))
(Y / "search-render.json").write_text(json.dumps(render, indent=1, ensure_ascii=False))
print(len(posts), "posts from", posts[0]["date"], "to", posts[-1]["date"])
