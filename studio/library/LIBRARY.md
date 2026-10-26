# Tracee's graphics library (course and offer art)

Added Oct 26, 2026. Originals live on Tracee's Mac: Desktop/ESL - The Emotional Support LIne/ESL OWL Course and Product Library.

Two web copies of each graphic, by the same name:
- `site/assets/library/<name>.jpg`: up to 1200 px, for the website, blog and emails. URL: https://theemotionalsupportline.com/assets/library/<name>.jpg
- `site/social/library/<name>.jpg`: 1080 px wide and Instagram-safe (tall ones padded to 4:5). URL: https://theemotionalsupportline.com/social/library/<name>.jpg

Every agent follows BRAND.md when writing words to go with these. A graphic is never a reason to invent a price, product or link: if the offer isn't live on the site, don't advertise it.

## Ready to use

| Name | What it shows | Use it for | Link to |
|---|---|---|---|
| in-the-moment-support | "In The Moment Support", women on the phone; Vulnerability, Grief, Anxiety, Grounding, Values | Support calls (the default call image) | /#calls |
| nest-come-as-you-are | The Nest, "Come as you are. You don't have to do life alone." | The Nest (the default Nest image) | /#nest |
| nest-matriarchal-owls | The Nest, a matriarchal collective, "Come as you are" | The Nest | /#nest |
| nest-celestial | The Nest, a collective: women, wisdom, connection, practice; sleeping owls | The Nest, sky moments (eclipses, solstices) | /#nest |
| nest-matriarchal-collective | Same scene, owls awake, "A matriarchal collective" | The Nest | /#nest |
| nest-womens-wisdom | Landscape: woman and owls, "The Nest, a collective" | The Nest, loneliness, women's circle themes | /#nest |
| nest-first-sundays | "Join The Nest Collective Calls every first Sunday of the month" (no time printed) | Monthly group call reminders, any month | /#nest |
| nest-sundays-11am | "First Sundays of every month at 11 am MST" | Group call reminders **November to early March only** (it says MST; from mid-March to early November Mountain time is MDT) | /#nest |
| forecast-cover-owls | EmoOwl's Energy Forecast, owls only | The Forecast (default) | /#forecast or /forecast/ |
| forecast-cover-woman | EmoOwl's Energy Forecast with a woman | The Forecast | /#forecast |
| forecast-weekly-monthly | "EmoOwl Energy Forecasts, weekly & monthly guidance" | Sign-ups (people choose weekly or monthly) | /#forecast |
| year-of-yes-soul-contract | Year of YES! Soul Contract, "Say YES to the life your Soul came here to live" | Year of YES! Coaching (default) | /year-of-yes |
| year-of-yes-soul-contract-2 | Same design (a near-duplicate) | Year of YES! Coaching | /year-of-yes |
| hd-free-report | "FREE Human Design Report", two owls in a nest (added Oct 26) | The free report in the Neutrino widget | /#chart |
| in-the-moment-circle | "In The Moment Emotional Support"; Nervous System Regulation, Anonymity, Touchstone, Real People in Real Time (Never AI), Evidence Based Methods | Support calls | /#calls |
| in-the-moment-community | "In The Moment Emotional Support, ALL feelings allowed!" with the same labels | Support calls | /#calls |
| hd-free-guide | Human Design free quick guide, square | The free chart and Starter Report | /#chart |
| hd-free-guide-tall | Human Design free quick guide, portrait | The free chart and Starter Report | /#chart |
| time-joygasm | Landscape, flying owl, "More pleasure, more productivity, more purpose" | Time Joy-gasm course (in the Nest library) | /#nest |
| time-joygasm-garden | Portrait, woman with owl, Time Joy-gasm | Time Joy-gasm course | /#nest |
| psychic-spring-clean | Owl sweeping, "Clear your space, clear your energy" | Psychic Spring Clean course (in the Nest library); spring | /#nest |
| autumn-clearing | Owl in a cozy autumn kitchen, "Let go, get organized" | Psychic Autumn Clearing course (4 videos in the Nest library); autumn and equinox posts | /#nest |
| 3-minute-miracle | Two owls, "3 Minute Miracle, a very short manifesting practice" | The 3-Minute Miracle video in the Nest library (added Oct 26) | /#nest |
| vision-board | How to make a vision board that works, "based on your design" | New year, goals, Human Design | /#chart |
| dream-board | Same design, "Dream Board" title | Spring planning, reinvention | /#chart |
| 100-things-2027 | "100 Things of 2027, a year-in-review exercise" | Late December 2027 (Tracee plans a separate 2026 version for this December) | /forecast/ |

The Nest library course covers (site/assets/covers/) are cut from the meditation collection tiles: Time Joy-gasm, Harvest, Joy R.O.I., Keeper of the Purpose (meditations), Soul vs Ego Smackdown, Psychic Spring Clean, Soul-Conomics.

## Waiting for Tracee (do not use yet)

| Name | Why it's waiting |
|---|---|
| what-we-are-not | Tracee to OK it first. It names a real person ("Not Oprah") and has political lines ("Not tech oligarch surveillance", "Not run by the state", "Not controlled by the government"). Perfect for the Aug 31, 2027 blog post "What is an emotional support call?" and a pinned post once approved. Any caption must carry the 988 line. |
| course-collection, course-collection-2 (12-tile grids) | One tile is "Perfect Match Magnetism ... from Love", a retired topic in BRAND.md; three tiles (Creation Cycle, Autumn Clearing, Perfect Match) aren't in the Nest library. Individual tiles are fine (they're the course covers). |
| hd-comprehensive-report, hd-comprehensive-report-reading, hd-career-purpose-report, hd-relationship-composite-report, hd-comprehensive-guide, hd-career-outlook-guide, hd-whos-in-your-nest, hd-guide-collection | Paid Human Design reports and guides with no price or checkout link on the site yet. Use them once each one has a page and a Stripe link. "Includes a live 2 hour reading" needs a price and booking details first. |

## Where they're used (Oct 26, 2026)

- Social: one Saturday post a week, Nov 7, 2026 to Oct 30, 2027 (type "spotlight" in studio/year/social-schedule.json, built by studio/year/make_spotlights.py). Buffer upload files: studio/year/buffer-csv/saturday-graphics-<channel>.csv.
- Blog: `banner:` in a post's front matter puts a graphic under the title (20 posts). Every call, Nest, Forecast and coaching call-to-action box shows its default graphic (CTA_ART in publish.py).
- Forecast emails: on the first Sunday of each month (from Dec 6, 2026) a "Today, 11 am Mountain: the Nest group call" block with the Nest call graphic.
- Welcome series (5 emails): one or two graphics each (welcome-series.md, rebuilt with make_welcome.py).
- The Nest app library: new course covers.

## Course workbooks (Oct 26, 2026)

Rebranded PDFs in `site/assets/workbooks/`, linked from the Nest library. Built by `studio/workbooks/build.py` from `studio/workbooks/src/*.md` (Tracee's 2014–2015 text, cleaned) and `studio/workbooks/originals/` (the old PDFs from traceesioux.com and yoy.traceesioux.com).

- time-joygasm.pdf (cover: time-joygasm-garden), harvest.pdf (cover: autumn owl art, titled Harvest), soul-vs-ego.pdf (cover: year-of-yes-soul-contract), joy-roi.pdf (cover: Joy ROI tile), soul-conomics-1 to -7.pdf (Tracee's Keynote slides with the old Sioux Ink logo replaced by EmoOwl).
- Edits from the originals (retired topics and dated details): "Time Sex" became "Time Joy-gasm"; "lovers", "sex" and "a date with your honey" removed from Time Joy-gasm; in Harvest, the marriage/boyfriend examples in Class 3 were replaced with short neutral versions of the same lesson, "2015" became "the new year", Facebook became social media, and the Maxcelerators Facebook group became the Nest group call; typos fixed. Edit the .md files and rerun build.py to change anything.
