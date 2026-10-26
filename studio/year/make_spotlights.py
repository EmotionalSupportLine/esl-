"""Saturday spotlight posts that use Tracee's course and offer graphics (site/social/library/).

Adds one Saturday post per week (Nov 7, 2026 to Oct 30, 2027) to social-schedule.json and writes
separate Buffer bulk-upload CSVs (studio/year/buffer-csv/saturday-graphics-<channel>.csv), so the
already-uploaded CSVs stay untouched.

    python3 studio/year/make_spotlights.py
"""
import csv, json, pathlib

YEAR = pathlib.Path(__file__).resolve().parent
BASE = "https://theemotionalsupportline.com"
CRISIS = "Not a crisis line. If you're in danger or thinking about suicide, call or text 988 (US)."
CRISIS_SHORT = "Not a crisis line. In danger? Call or text 988 (US)."
TIME = "10:00"

L = {"calls": "/#calls", "nest": "/#nest", "forecast": "/#forecast", "chart": "/#chart", "yoy": "/year-of-yes"}

# (date, graphic, link, pinterest title, [paragraphs], [instagram hashtags])
# Paragraph 1 is the hook (also the Bluesky text). "Link in bio." is swapped for the URL off Instagram.
POSTS = [
 ("2026-11-07", "autumn-clearing", "forecast", "Autumn clearing: make space before winter",
  ["Before winter, a little clearing. 🌿",
   "Gather what you need. Let go of what you don't. Make one corner of your home feel like a nest.",
   "What's one thing you could clear this weekend?",
   "EmoOwl's Energy Forecast brings a question like this every Sunday, free. Link in bio."],
  ["#AutumnClearing", "#SeasonalReset", "#CozyHome", "#SlowLiving", "#LettingGo", "#EmotionalSupportLine"]),
 ("2026-11-14", "in-the-moment-support", "calls", "In-the-moment emotional support from a real person",
  ["When it's happening now, you need someone now. 💛",
   "Thirty minutes with a real, trained person who listens. Never AI. No sales call first.",
   "$75, or $50 for Nest members. Mondays and Tuesdays, noon to 7 pm Mountain. Link in bio."],
  ["#EmotionalSupport", "#YouAreNotAlone", "#HereToListen", "#RealPeople", "#TalkItOut", "#EmotionalSupportLine"]),
 ("2026-11-21", "nest-womens-wisdom", "nest", "The Nest: a collective for women, wisdom and practice",
  ["A space to learn, grow and belong. 🧡",
   "The Nest is our membership: daily sun and earthing tools, the sky where you live, a library of Year of YES! courses, and a monthly group call.",
   "Founding members pay $14 a month for as long as they stay. The founding price ends November 30. Link in bio."],
  ["#TheNest", "#WomensCircle", "#WomenSupportingWomen", "#Belonging", "#DailyHabits", "#EmotionalSupportLine"]),
 ("2026-11-28", "nest-come-as-you-are", "nest", "Come as you are. You don't have to do life alone.",
  ["Come as you are. You don't have to do life alone. 💛",
   "Last weekend for the founding price: the Nest is $14 a month for as long as you stay, until Monday, November 30. After that it's $19 a month or $190 a year.",
   "Link in bio."],
  ["#TheNest", "#YouAreNotAlone", "#WomensCircle", "#Belonging", "#SmallSteps", "#EmotionalSupportLine"]),
 ("2026-12-05", "nest-sundays-11am", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: our first Nest group call. 🦉",
   "Sunday, December 6, 11 am Mountain. For Nest members: bring a question, or just listen.",
   "Not a member yet? The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#WomensCircle", "#Community", "#HereToListen", "#EmotionalSupportLine"]),
 ("2026-12-12", "time-joygasm", "nest", "Time Joy-gasm: more pleasure, more productivity, more purpose",
  ["What if your time felt like pleasure instead of pressure? 🧡",
   "Time Joy-gasm is seven video classes from Tracee Sioux's Year of YES! library: more pleasure, more productivity, more purpose.",
   "It's included in the Nest, along with Soul-Conomics, Soul vs Ego Smackdown and Psychic Spring Clean. Link in bio."],
  ["#TimeJoygasm", "#YearOfYes", "#TimeManagement", "#Joy", "#HolidaySeason", "#EmotionalSupportLine"]),
 ("2026-12-19", "forecast-cover-woman", "forecast", "EmoOwl's Energy Forecast: the week's sky, free every Sunday",
  ["The longest night is Monday. 🌕",
   "EmoOwl's Energy Forecast arrives every Sunday: the moon, the sun, space weather and one question to sit with. Sky positions are real astronomy; what they mean for you is yours to decide.",
   "Free, weekly or monthly. Link in bio."],
  ["#EnergyForecast", "#WinterSolstice", "#MoonPhases", "#AstroWeather", "#Reflection", "#EmotionalSupportLine"]),
 ("2026-12-26", "100-things-2027", "forecast", "100 Things: a year-in-review exercise before 2027",
  ["Before 2027 begins, try the 100 Things exercise. 💛",
   "Remember. Record. Give yourself credit. Write down what you did this year and the challenges you survived, until you reach 100.",
   "Then read it back and notice what you want more of next year.",
   "More questions like this every Sunday in EmoOwl's Energy Forecast. Link in bio."],
  ["#YearInReview", "#NewYear2027", "#Journaling", "#GiveYourselfCredit", "#Reflection", "#EmotionalSupportLine"]),
 ("2027-01-02", "nest-first-sundays", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call. 🦉",
   "Sunday, January 3, 11 am Mountain. Start the year in good company: bring a question, or just listen.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#NewYear", "#WomensCircle", "#Community", "#EmotionalSupportLine"]),
 ("2027-01-09", "vision-board", "chart", "How to make a vision board that fits your Human Design",
  ["A vision board works better when it fits how you're built. 🌿",
   "Before you glue anything down, look at your Human Design chart. Your type and strategy can show you which dreams feel like yours and which ones you borrowed.",
   "See your free chart and Starter Report on our homepage. Link in bio."],
  ["#VisionBoard", "#HumanDesign", "#NewYearGoals", "#Intentions", "#DreamBoard", "#EmotionalSupportLine"]),
 ("2027-01-16", "year-of-yes-soul-contract", "yoy", "Year of YES! Coaching with Tracee Sioux",
  ["Say YES to the life your Soul came here to live. 🧡",
   "Year of YES! Coaching with Tracee Sioux: twelve months, two hours a month, guided by your Human Design chart.",
   "$555 a month for four founding clients, then $777. By application. Link in bio."],
  ["#YearOfYes", "#LifeCoaching", "#HumanDesign", "#WomenInBusiness", "#SoulPurpose", "#EmotionalSupportLine"]),
 ("2027-01-23", "hd-free-guide", "chart", "Free Human Design quick guide: a snapshot of your design",
  ["Your free Human Design snapshot. 🦉",
   "Your type, your strategy, your authority: how your energy works and how you're built to decide.",
   "Enter your birth details on our homepage for a free chart and Starter Report. A prompt for reflection, never a prediction. Link in bio."],
  ["#HumanDesign", "#HumanDesignChart", "#KnowYourself", "#FreeGuide", "#SelfDiscovery", "#EmotionalSupportLine"]),
 ("2027-01-30", "forecast-weekly-monthly", "forecast", "EmoOwl Energy Forecasts: weekly or monthly",
  ["Weekly or monthly: your choice. 🌕",
   "EmoOwl's Energy Forecast covers the moon, space weather, Human Design transits and one question to sit with.",
   "Pick how often it lands in your inbox. Free. Link in bio."],
  ["#EnergyForecast", "#Astrology", "#HumanDesign", "#SpaceWeather", "#MoonPhases", "#EmotionalSupportLine"]),
 ("2027-02-06", "nest-sundays-11am", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call. 🦉",
   "Sunday, February 7, 11 am Mountain. Bring a question, or just listen.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#WomensCircle", "#Community", "#HereToListen", "#EmotionalSupportLine"]),
 ("2027-02-13", "in-the-moment-support", "calls", "Lonely this weekend? Talk to a real person",
  ["Not everyone loves this weekend. 💙",
   "If February 14 stirs up something heavy, you can talk it through with a real, trained person. Never AI.",
   "30 minutes. $75, or $50 for Nest members. Mondays and Tuesdays, noon to 7 pm Mountain. Link in bio."],
  ["#Lonely", "#EmotionalSupport", "#YouAreNotAlone", "#HereToListen", "#TalkItOut", "#EmotionalSupportLine"]),
 ("2027-02-20", "nest-celestial", "nest", "Tonight's lunar eclipse, and the Nest",
  ["Tonight's lunar eclipse is a good night to look up. 🌕",
   "The Nest shows the real sky for where you live, tracks your morning sun and time outside, and gathers once a month for a group call.",
   "$19 a month or $190 a year. Link in bio."],
  ["#LunarEclipse", "#TheNest", "#MoonPhases", "#LookUp", "#WomensCircle", "#EmotionalSupportLine"]),
 ("2027-02-27", "time-joygasm-garden", "nest", "Time Joy-gasm: more joy, creativity and freedom",
  ["More joy. More creativity. More freedom. More you. 🧡",
   "Time Joy-gasm is Tracee Sioux's seven-class course on experiencing your time as pleasure. It's in the Nest library.",
   "Link in bio."],
  ["#TimeJoygasm", "#YearOfYes", "#Joy", "#Creativity", "#WomenInBusiness", "#EmotionalSupportLine"]),
 ("2027-03-06", "nest-sundays-11am", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call. 🦉",
   "Sunday, March 7, 11 am Mountain. Bring a question, or just listen.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#WomensCircle", "#Community", "#HereToListen", "#EmotionalSupportLine"]),
 ("2027-03-13", "psychic-spring-clean", "nest", "Psychic Spring Clean: clear your space, clear your energy",
  ["Clear your space. Clear your energy. 🌿",
   "Psychic Spring Clean is five video classes from the Year of YES! library on letting go of what's cluttering your home and your head.",
   "It's included in the Nest. Link in bio."],
  ["#SpringCleaning", "#PsychicSpringClean", "#Declutter", "#FreshStart", "#YearOfYes", "#EmotionalSupportLine"]),
 ("2027-03-20", "forecast-cover-owls", "forecast", "The spring equinox: EmoOwl's Energy Forecast",
  ["Today day and night are nearly equal. 🌿",
   "A good day for a balance check: where are you giving too much, and where could you give yourself more?",
   "EmoOwl's Energy Forecast brings a question like this every Sunday, free. Link in bio."],
  ["#SpringEquinox", "#EnergyForecast", "#Balance", "#Reflection", "#AstroWeather", "#EmotionalSupportLine"]),
 ("2027-03-27", "hd-free-guide-tall", "chart", "Free Human Design quick guide",
  ["How are you built to decide? 🦉",
   "Your Human Design authority is one of the most useful parts of your chart. See yours free, with a Starter Report, on our homepage.",
   "A prompt for reflection, never a prediction. Link in bio."],
  ["#HumanDesign", "#HumanDesignAuthority", "#Decisions", "#SelfDiscovery", "#FreeGuide", "#EmotionalSupportLine"]),
 ("2027-04-03", "nest-first-sundays", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call. 🦉",
   "Sunday, April 4, 11 am Mountain. Bring a question, or just listen.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#WomensCircle", "#Community", "#HereToListen", "#EmotionalSupportLine"]),
 ("2027-04-10", "dream-board", "chart", "How to make a dream board based on your Human Design",
  ["Spring is a good time to dream on paper. 🌿",
   "Make a dream board from what lights you up, not what you think you should want. Your Human Design chart can help you tell the difference.",
   "See your free chart on our homepage. Link in bio."],
  ["#DreamBoard", "#VisionBoard", "#HumanDesign", "#SpringReset", "#Intentions", "#EmotionalSupportLine"]),
 ("2027-04-17", "in-the-moment-support", "calls", "In-the-moment emotional support from a real person",
  ["All feelings allowed. 💛",
   "Grief, worry, a hard conversation, or a week that's just too much: talk it through with a real, trained person. Never AI.",
   "30 minutes. $75, or $50 for Nest members. Mondays and Tuesdays, noon to 7 pm Mountain. Link in bio."],
  ["#EmotionalSupport", "#AllFeelingsAllowed", "#YouAreNotAlone", "#HereToListen", "#TalkItOut", "#EmotionalSupportLine"]),
 ("2027-04-24", "nest-matriarchal-owls", "nest", "The Nest: a matriarchal collective",
  ["Come as you are. You don't have to do life alone. 🧡",
   "The Nest: live group calls, Year of YES! classes, Human Design and astrology, and tools for small daily habits.",
   "$19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#WomensCircle", "#Matriarch", "#Belonging", "#Community", "#EmotionalSupportLine"]),
 ("2027-05-01", "nest-first-sundays", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call. 🦉",
   "Sunday, May 2, 11 am Mountain. Bring a question, or just listen.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#WomensCircle", "#Community", "#HereToListen", "#EmotionalSupportLine"]),
 ("2027-05-08", "nest-come-as-you-are", "nest", "When Mother's Day is complicated",
  ["If tomorrow is complicated, you're not the only one. 💛",
   "Mother's Day can hold grief, distance and mixed feelings alongside the flowers. The Nest is a place to come as you are.",
   "$19 a month or $190 a year. Link in bio."],
  ["#MothersDay", "#Grief", "#YouAreNotAlone", "#TheNest", "#WomensCircle", "#EmotionalSupportLine"]),
 ("2027-05-15", "forecast-cover-woman", "forecast", "EmoOwl's Energy Forecast: your week of sky",
  ["How's the week ahead looking up there? 🌕",
   "EmoOwl's Energy Forecast: the moon, space weather, Human Design transits and one question to sit with. Reflection, never prediction.",
   "Free, weekly or monthly. Link in bio."],
  ["#EnergyForecast", "#MoonPhases", "#AstroWeather", "#HumanDesign", "#Reflection", "#EmotionalSupportLine"]),
 ("2027-05-22", "year-of-yes-soul-contract-2", "yoy", "Year of YES! Coaching with Tracee Sioux",
  ["Your time, energy and labor belong to you. 🧡",
   "Year of YES! Coaching with Tracee Sioux: a year of two-hour monthly sessions, guided by your Human Design, for capable women ready to build something that's theirs.",
   "Founding spots are $555 a month; after those, $777. By application. Link in bio."],
  ["#YearOfYes", "#LifeCoaching", "#HumanDesign", "#WomenInBusiness", "#SoulPurpose", "#EmotionalSupportLine"]),
 ("2027-05-29", "time-joygasm", "nest", "Time Joy-gasm: experience your time as pleasure",
  ["Summer is coming. What if your time felt like yours? 🌿",
   "Time Joy-gasm: seven video classes on more pleasure, more productivity and more purpose. In the Nest library.",
   "Link in bio."],
  ["#TimeJoygasm", "#YearOfYes", "#SummerPlans", "#Joy", "#TimeManagement", "#EmotionalSupportLine"]),
 ("2027-06-05", "nest-first-sundays", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call. 🦉",
   "Sunday, June 6, 11 am Mountain. Bring a question, or just listen.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#WomensCircle", "#Community", "#HereToListen", "#EmotionalSupportLine"]),
 ("2027-06-12", "in-the-moment-support", "calls", "In-the-moment emotional support from a real person",
  ["Some things get lighter the moment you say them out loud. 💛",
   "Thirty minutes with a real, trained person who listens. Never AI. No sales call first.",
   "$75, or $50 for Nest members. Mondays and Tuesdays, noon to 7 pm Mountain. Link in bio."],
  ["#EmotionalSupport", "#TalkItOut", "#YouAreNotAlone", "#HereToListen", "#RealPeople", "#EmotionalSupportLine"]),
 ("2027-06-19", "nest-celestial", "nest", "The summer solstice and the Nest",
  ["The longest day is Monday. 🌿",
   "The Nest helps you use it well: morning sun and earthing tracking, the real sky where you live, and a monthly group call.",
   "$19 a month or $190 a year. Link in bio."],
  ["#SummerSolstice", "#TheNest", "#MorningSun", "#Earthing", "#WomensCircle", "#EmotionalSupportLine"]),
 ("2027-06-26", "hd-free-guide", "chart", "Free Human Design quick guide",
  ["What's your Human Design type? 🦉",
   "Generator, Manifesting Generator, Projector, Manifestor or Reflector. See yours free, with a Starter Report, on our homepage.",
   "A prompt for reflection, never a prediction. Link in bio."],
  ["#HumanDesign", "#HumanDesignType", "#KnowYourself", "#FreeGuide", "#SelfDiscovery", "#EmotionalSupportLine"]),
 ("2027-07-03", "nest-first-sundays", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call, holiday edition. 🦉",
   "Sunday, July 4, 11 am Mountain. Bring a question, or just listen, before the fireworks.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#WomensCircle", "#Community", "#HereToListen", "#EmotionalSupportLine"]),
 ("2027-07-10", "forecast-weekly-monthly", "forecast", "EmoOwl Energy Forecasts: weekly or monthly",
  ["The sky, in plain words, once a week or once a month. 🌕",
   "EmoOwl's Energy Forecast: moon phases, space weather, Human Design transits and one question to sit with.",
   "Free. Link in bio."],
  ["#EnergyForecast", "#Astrology", "#HumanDesign", "#SpaceWeather", "#MoonPhases", "#EmotionalSupportLine"]),
 ("2027-07-17", "nest-womens-wisdom", "nest", "The Nest: a collective for women, wisdom and practice",
  ["Lonely as an adult is more common than anyone admits. 💛",
   "The Nest is a place to learn, grow and belong: a monthly group call, Year of YES! courses and small daily habits.",
   "$19 a month or $190 a year. Link in bio."],
  ["#Loneliness", "#TheNest", "#WomensCircle", "#Belonging", "#Community", "#EmotionalSupportLine"]),
 ("2027-07-24", "in-the-moment-support", "calls", "In-the-moment emotional support from a real person",
  ["You don't have to wait for a crisis to talk to someone. 💙",
   "Thirty minutes with a real, trained person who listens. Never AI.",
   "$75, or $50 for Nest members. Mondays and Tuesdays, noon to 7 pm Mountain. Link in bio."],
  ["#EmotionalSupport", "#TalkItOut", "#YouAreNotAlone", "#HereToListen", "#RealPeople", "#EmotionalSupportLine"]),
 ("2027-07-31", "nest-first-sundays", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call. 🦉",
   "Sunday, August 1, 11 am Mountain, the day before the total solar eclipse. Bring a question, or just listen.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#SolarEclipse", "#WomensCircle", "#Community", "#EmotionalSupportLine"]),
 ("2027-08-07", "year-of-yes-soul-contract", "yoy", "Year of YES! Coaching with Tracee Sioux",
  ["What did your Soul come here to do? 🧡",
   "Year of YES! Coaching with Tracee Sioux: twelve months, two hours a month, guided by your Human Design chart.",
   "Founding spots are $555 a month; after those, $777. By application. Link in bio."],
  ["#YearOfYes", "#LifeCoaching", "#HumanDesign", "#SoulPurpose", "#WomenInBusiness", "#EmotionalSupportLine"]),
 ("2027-08-14", "forecast-cover-owls", "forecast", "EmoOwl's Energy Forecast: free every Sunday",
  ["Meteor showers, eclipses and full moons, with one question to sit with. 🌕",
   "EmoOwl's Energy Forecast, free every Sunday. Sky positions are real astronomy; what they mean is yours to decide.",
   "Link in bio."],
  ["#EnergyForecast", "#Perseids", "#MoonPhases", "#AstroWeather", "#Reflection", "#EmotionalSupportLine"]),
 ("2027-08-21", "hd-free-guide-tall", "chart", "Free Human Design quick guide",
  ["Back to routines? Start with how you're built. 🦉",
   "Your Human Design chart shows how your energy works and how you make your best decisions. See yours free, with a Starter Report.",
   "A prompt for reflection, never a prediction. Link in bio."],
  ["#HumanDesign", "#BackToRoutine", "#KnowYourself", "#FreeGuide", "#SelfDiscovery", "#EmotionalSupportLine"]),
 ("2027-08-28", "in-the-moment-support", "calls", "In-the-moment emotional support from a real person",
  ["The strong one needs support too. 💙",
   "Thirty minutes with a real, trained person who listens and helps you find your next step. Never AI.",
   "$75, or $50 for Nest members. Mondays and Tuesdays, noon to 7 pm Mountain. Link in bio."],
  ["#EmotionalSupport", "#StrongWomen", "#YouAreNotAlone", "#HereToListen", "#TalkItOut", "#EmotionalSupportLine"]),
 ("2027-09-04", "nest-first-sundays", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call. 🦉",
   "Sunday, September 5, 11 am Mountain. Bring a question, or just listen.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#WomensCircle", "#Community", "#HereToListen", "#EmotionalSupportLine"]),
 ("2027-09-11", "nest-come-as-you-are", "nest", "Come as you are. You don't have to do life alone.",
  ["Come as you are. 💛",
   "The Nest: a monthly group call, Year of YES! courses, the real sky where you live and small daily habits that steady you.",
   "$19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#YouAreNotAlone", "#WomensCircle", "#Belonging", "#Community", "#EmotionalSupportLine"]),
 ("2027-09-18", "autumn-clearing", "forecast", "Autumn clearing: make space before winter",
  ["The equinox is this week. A good time to clear. 🌿",
   "Gather. Organize. Nourish. Rest. Make your home a nest for the darker months.",
   "What's one thing you're ready to let go of?",
   "EmoOwl's Energy Forecast brings a question like this every Sunday, free. Link in bio."],
  ["#AutumnEquinox", "#AutumnClearing", "#SeasonalReset", "#CozyHome", "#LettingGo", "#EmotionalSupportLine"]),
 ("2027-09-25", "forecast-cover-woman", "forecast", "EmoOwl's Energy Forecast: your week of sky",
  ["A small weekly pause so the year doesn't blur. 🌕",
   "EmoOwl's Energy Forecast: the moon, space weather, Human Design transits and one question to sit with.",
   "Free, weekly or monthly. Link in bio."],
  ["#EnergyForecast", "#MoonPhases", "#AstroWeather", "#HumanDesign", "#Reflection", "#EmotionalSupportLine"]),
 ("2027-10-02", "nest-first-sundays", "nest", "The Nest group call: first Sunday of every month",
  ["Tomorrow: the Nest group call. 🦉",
   "Sunday, October 3, 11 am Mountain. Bring a question, or just listen.",
   "For Nest members. The Nest is $19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#GroupCall", "#WomensCircle", "#Community", "#HereToListen", "#EmotionalSupportLine"]),
 ("2027-10-09", "time-joygasm", "nest", "Time Joy-gasm: more pleasure, more productivity, more purpose",
  ["Busy season again? Take your time back. 🧡",
   "Time Joy-gasm: seven video classes from the Year of YES! library on experiencing your time as pleasure. In the Nest.",
   "Link in bio."],
  ["#TimeJoygasm", "#YearOfYes", "#Busyness", "#Joy", "#TimeManagement", "#EmotionalSupportLine"]),
 ("2027-10-16", "in-the-moment-support", "calls", "In-the-moment emotional support from a real person",
  ["A neutral ear makes a difference. 💛",
   "Thirty minutes with a real, trained person who listens. Never AI. No sales call first.",
   "$75, or $50 for Nest members. Mondays and Tuesdays, noon to 7 pm Mountain. Link in bio."],
  ["#EmotionalSupport", "#TalkItOut", "#YouAreNotAlone", "#HereToListen", "#RealPeople", "#EmotionalSupportLine"]),
 ("2027-10-23", "year-of-yes-soul-contract-2", "yoy", "Year of YES! Coaching with Tracee Sioux",
  ["Ready for a year that's yours? 🧡",
   "Year of YES! Coaching with Tracee Sioux: twelve months, two hours a month, guided by your Human Design chart.",
   "Founding spots are $555 a month; after those, $777. By application. Link in bio."],
  ["#YearOfYes", "#LifeCoaching", "#HumanDesign", "#SoulPurpose", "#WomenInBusiness", "#EmotionalSupportLine"]),
 ("2027-10-30", "nest-matriarchal-collective", "nest", "The Nest: a matriarchal collective",
  ["A space to learn, grow and belong. Together we rise. 💛",
   "The Nest: a monthly group call, Year of YES! courses, Human Design and astrology, and small daily habits.",
   "$19 a month or $190 a year. Link in bio."],
  ["#TheNest", "#WomensCircle", "#Matriarch", "#Belonging", "#Community", "#EmotionalSupportLine"]),
]


def build():
    posts = []
    for date, img, key, ptitle, paras, tags in POSTS:
        url = BASE + L[key]
        body = "\n\n".join(paras)
        ig = f"{body}\n\n{CRISIS}\n\n{' '.join(tags)}"
        fb_tags = [t for t in tags if t != "#EmotionalSupportLine"][:2] + ["#EmotionalSupportLine"]
        fb_body = body.replace("Link in bio.", url)
        fb = f"{fb_body}\n\n{CRISIS}\n\n{' '.join(fb_tags)}"
        bsky = f"{paras[0]}\n\n{url}\n\n{CRISIS_SHORT}"
        if len(paras) > 1 and len(bsky) + len(paras[1]) + 2 <= 290:
            bsky = f"{paras[0]}\n\n{paras[1].replace('Link in bio.', '').strip()}\n\n{url}\n\n{CRISIS_SHORT}"
        pin = {"title": ptitle, "description": f"{body.replace('Link in bio.', 'theemotionalsupportline.com').strip()}\n\n{CRISIS}"}
        posts.append({"id": f"{date}-sat-{img}", "date": date, "time": TIME, "type": "spotlight", "status": "approved",
                      "images": [f"{BASE}/social/library/{img}.jpg"], "link": url, "instagram": ig, "facebook": fb,
                      "bluesky": bsky, "pinterest": pin, "buffer": None})
    return posts


def check(posts):
    allowed = set("🌿💛🧡💙🌕🦉")
    for p in posts:
        assert (YEAR.parents[1] / "site" / "social" / "library" / p["images"][0].split("/")[-1]).exists(), p["id"]
        n = sum(1 for t in p["instagram"].split() if t.startswith("#"))
        assert 5 <= n <= 8, (p["id"], n)
        emo = [c for c in p["instagram"] if ord(c) > 0x2600 and c not in "’"]
        assert len(emo) <= 1 and all(c in allowed for c in emo), (p["id"], emo)
        assert "988" in p["instagram"] and len(p["bluesky"]) <= 300, p["id"]
        for bad in ("therapy", "heal", "cure", "clinical", "diagnos", "treatment", "Magdalene", "proven"):
            assert bad not in p["instagram"].lower().replace("magdalene", "Magdalene"), (p["id"], bad)


if __name__ == "__main__":
    posts = build()
    check(posts)
    sched_path = YEAR / "social-schedule.json"
    sched = [p for p in json.loads(sched_path.read_text()) if p.get("type") != "spotlight"]
    sched = sorted(sched + posts, key=lambda p: (p["date"], p["time"]))
    sched_path.write_text(json.dumps(sched, indent=1, ensure_ascii=False) + "\n")
    out = YEAR / "buffer-csv"
    rows = {"instagram": [], "facebook": [], "linkedin": [], "bluesky": [], "pinterest": []}
    for p in posts:
        when = f"{p['date']} {p['time']}"
        img = p["images"][0]
        rows["instagram"].append({"Text": p["instagram"], "Image URL": img, "Tags": "", "Posting Time": when})
        rows["facebook"].append({"Text": p["facebook"], "Image URL": img, "Tags": "", "Posting Time": when})
        rows["linkedin"].append({"Text": p["facebook"], "Image URL": img, "Tags": "", "Posting Time": when})
        rows["bluesky"].append({"Text": p["bluesky"], "Image URL": img, "Tags": "", "Posting Time": when})
        rows["pinterest"].append({"Text": p["pinterest"]["description"], "Image URL": img, "Tags": "", "Posting Time": when,
                                  "Board Name": "Quick Saves", "Title": p["pinterest"]["title"], "Link": p["link"]})
    for ch, r in rows.items():
        with open(out / f"saturday-graphics-{ch}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(r[0].keys()), quoting=csv.QUOTE_MINIMAL)
            w.writeheader()
            w.writerows(r)
    print(f"{len(posts)} Saturday posts added; CSVs written for {', '.join(rows)}")
