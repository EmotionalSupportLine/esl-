// One place for every price and link. Change it here and the whole site follows.
window.ESL = {
  prices: {
    callPublic: 75,
    callMember: 50,
    nestMonthly: 19,
    nestFounding: 14,
    nestYearly: 190,
    steady: 180,
  },
  links: {
    // Google Calendar paid booking page for non-members ($75)
    bookCall: "https://calendar.app.google/gczW5R1ubjrYmJo7A",
    // Stripe Payment Links (filled in during account setup)
    nestMonthly: "https://buy.stripe.com/dRmdR9cNE7Ao3aU7vd0kE0e",
    nestFounding: "https://buy.stripe.com/aFaaEX4h8bQEcLu8zh0kE0d",
    nestYearly: "https://buy.stripe.com/6oU6oH6pg4ocbHq02L0kE0f",
    // Pay It Forward: gift a call to someone who can't afford one (existing Stripe donation link)
    payItForward: "https://donate.stripe.com/3cI9AT8xo4occLu2aT0kE0c",
    // Mailchimp embedded-form action URL for the free Forecast
    forecastForm: "https://traceesioux.us2.list-manage.com/subscribe/post?u=1518241fc7aee7782d17d61e9&id=bd683fce4d",
    // Stripe customer portal login link (members manage or cancel here)
    billingPortal: "https://billing.stripe.com/p/login/9B67sLdRI1c0aDm02L0kE00",
  },
  // Neutrino Human Design chart widget: paste the script URL and API key from
  // neutrinoplatform.com/app/widgets (add theemotionalsupportline.com to its allowed domains)
  neutrino: { script: "", key: "" },
  foundingOpen: true,
  email: "careteam@theemotionalsupportline.com",
};
