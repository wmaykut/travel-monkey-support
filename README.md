# Support — Travel Monkey

**Travel Monkey** is an iPhone travel concierge for your household. It keeps your
travelers' preferences, your trip's itinerary and reservations, and a log of what you ate
and did, and uses Claude to recommend where to eat, what to do, and when to leave.

This page explains how to get help, report a problem, or request a feature. For how the
app handles your information, see the [Privacy Policy](privacy.md).

If you just need a quick answer, check the [FAQ](#faq) first.

---

## How to get help

| I want to… | Do this |
|---|---|
| **Report a bug** | [Open a bug report](https://github.com/wmaykut/travel-monkey-support/issues/new) and include the details below |
| **Request a feature** | [Open a feature request](https://github.com/wmaykut/travel-monkey-support/issues/new) describing what you'd like and why |
| **Ask a question** | Search [existing issues](https://github.com/wmaykut/travel-monkey-support/issues) first, then open a new one |
| **Report something private** (security or privacy) | See [Security & private reports](#security--private-reports). Please don't open a public issue |

**Please don't put personal details in a public issue.** That includes reservation
confirmation codes, addresses, travelers' names, or your API key.

---

## Reporting a bug

Please include:

1. **What happened** and **what you expected** to happen instead.
2. **Steps to reproduce**: the taps or the question that led to the problem.
3. **Device and iOS version**, e.g. *iPhone 16, iOS 26.1*.
4. **App version**, from the App Store page or iOS **Settings → Apps → Travel Monkey**.
5. **A screenshot or screen recording**, if the problem is visual. Crop out anything
   personal.

If a concierge answer was wrong, say what you asked, roughly where you were, and what it
recommended. Each answer keeps the context it was given, which helps track the problem
down.

---

## FAQ

**Do I need an Anthropic API key?**
Yes. The concierge is Claude, called directly from your iPhone with your own key. Create
one at [console.anthropic.com](https://console.anthropic.com) under **API keys**, then
paste it during setup or in **Profile → Settings**. Usage is billed to your Anthropic
account. A trip's worth of questions typically costs a few dollars.

**Is my API key safe?**
It is stored in the iOS Keychain, only its last four characters are ever shown, and it is
sent only to Anthropic. If you think it has been exposed, revoke it in the Anthropic
Console and paste a new one.

**What does the app send to Anthropic?**
Each concierge request includes the household profile, today's plans and upcoming
reservations, your current location, and the conversation. Full details are in the
[Privacy Policy](privacy.md#what-is-sent-to-anthropic) and in **Profile → Settings →
Privacy**.

**Why does it want "Always" location access?**
So it can notice when you set off, and warn you if you're still where you were when
it's time to leave for a flight, train, or booking. Recommendations and travel times work
with "While Using the App". You can change this in iOS Settings at any time.

**I'm not getting leave-by reminders.**
Check that notifications are allowed for Travel Monkey in iOS Settings, and that the
reservation has a time and a place. Reminders are scheduled on your phone ahead of time,
so open the app at least once after adding a reservation.

**Does it work offline?**
You can read your trip, reservations, and logs offline. The concierge needs a network
connection.

**How do I share a trip with the rest of my household?**
Your data syncs through your private iCloud account to devices signed in to the same
Apple Account. Make sure iCloud is on. **Profile → Settings** shows the sync status.

**Can I try it before entering my own trip?**
Yes. **Profile → Settings → Load sample data** adds a sample trip dated to today. You
can remove it from the same screen.

**Can it book things for me?**
No. Travel Monkey recommends and reminds; it doesn't book or buy anything. Directions
open in Apple Maps, or in Google Maps from the long-press menu.

---

## Security & private reports

**Please don't open a public issue** for security vulnerabilities or anything involving
someone's personal information. Instead, use
[GitHub private vulnerability reporting](https://github.com/wmaykut/travel-monkey-support/security/advisories/new).
Only the maintainer can see these reports.

---

## Response expectations

Travel Monkey is an independent project, and support is **best effort**, with no
guaranteed response time. Clear reports (steps, device, version, screenshots) get resolved
fastest. Thanks for helping make Travel Monkey better.
