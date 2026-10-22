// One place for every price and link. Change it here and the whole site follows.
window.ESL = {
  prices: {
    callPublic: 75,
    callMember: 50,
    nestMonthly: 19,
    nestFounding: 14,
    nestYearly: 190,
    steady: 180,
    coaching: 555,
    coachingNext: 777,
  },
  links: {
    // Pay-first Stripe link for non-members ($75); after paying it opens the Google booking page
    bookCall: "https://book.stripe.com/5kQ00j3d47Ao4eY2aT0kE0i",
    bookingPage: "https://calendar.app.google/gczW5R1ubjrYmJo7A",
    // Stripe Payment Links (filled in during account setup)
    nestMonthly: "https://buy.stripe.com/dRmdR9cNE7Ao3aU7vd0kE0e",
    nestFounding: "https://buy.stripe.com/aFaaEX4h8bQEcLu8zh0kE0d",
    nestYearly: "https://buy.stripe.com/6oU6oH6pg4ocbHq02L0kE0f",
    // Pay It Forward: gift a call to someone who can't afford one (existing Stripe donation link)
    // Coaching: applications go to the care team inbox; Tracee sends the Stripe link after a fit call
    coachingPay: "https://buy.stripe.com/cNi14naFw6wk26Q2aT0kE0g",
    payItForward: "https://donate.stripe.com/3cI9AT8xo4occLu2aT0kE0c",
    // Mailchimp embedded-form action URL for the free Forecast
    forecastForm: "https://traceesioux.us2.list-manage.com/subscribe/post?u=1518241fc7aee7782d17d61e9&id=bd683fce4d",
    // Stripe customer portal login link (members manage or cancel here)
    billingPortal: "https://billing.stripe.com/p/login/9B67sLdRI1c0aDm02L0kE00",
  },
  // Neutrino Human Design chart widget: paste the script URL and API key from
  // neutrinoplatform.com/app/widgets (add theemotionalsupportline.com to its allowed domains)
  neutrino: { script: "", key: "" },
  // Founding coaching spots left at the current price (the Stripe link closes itself after 4)
  coachingSpots: 4,
  foundingOpen: true,
  email: "careteam@theemotionalsupportline.com",
  callHours: "Mondays and Tuesdays, noon to 7 pm Mountain",
};
