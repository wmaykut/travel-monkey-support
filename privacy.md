# Privacy Policy — Travel Monkey

Last updated: October 3, 2026

Travel Monkey is an iPhone travel concierge for a household. It keeps your travelers'
preferences, your trip's itinerary and reservations, and a log of meals and activities,
and it uses Claude, an AI model made by Anthropic, to recommend where to eat, what to do,
and when to leave. This policy explains what the app handles, where that information
goes, and what choices you have.

## Summary

- Travel Monkey has no servers of its own. The developer does not receive, see, or store
  your information.
- Your household profile, trips, reservations, logs, and conversations are stored on your
  iPhone and, if iCloud is on, in your own private iCloud account.
- When you ask the concierge something, the app sends that request **directly from your
  phone to Anthropic**, using an Anthropic API key you supply. That request includes
  personal information, including your current location. Details are below.
- Location is used for recommendations, travel times, and leave-by reminders. It is sent
  to Apple for maps and weather, and to Anthropic as part of your concierge requests.
- No advertising, no analytics, no tracking, and no third-party SDKs. Your information is
  never sold.

## Information the app handles

You enter, or the app records, the following:

- **Household profile:** travelers' names, food and activity preferences, dislikes,
  dietary needs, allergies, ratings, and notes, plus corrections you have asked the
  concierge to remember.
- **Trips:** itinerary days, lodging, and reservations such as flights, trains,
  restaurants, and tours, including addresses, times, and confirmation codes.
- **Logs:** meals and activities you record, with ratings and notes.
- **Conversations:** your messages to the concierge, its replies, and the context that
  was sent with each request.
- **Location:** your device's location, when you allow it.
- **Shared bookings:** pasted or shared text, screenshots or photos, PDFs, and Safari
  page titles, addresses, and visible text, held in a device-local inbox for review.
- **Your Anthropic API key**, which is stored in the iOS Keychain.

## Where it is stored

Everything above is stored on your iPhone. If you are signed in to iCloud, the app syncs
your household data through Apple's CloudKit to your own **private** iCloud database, so
it appears on your other devices signed in to the same Apple Account. The developer
cannot access your private iCloud database. Apple's handling of iCloud data is governed
by [Apple's Privacy Policy](https://www.apple.com/legal/privacy/).

Shared-booking files and their parsed proposals stay in an inbox on the receiving
phone until you save or discard them; they do not sync through iCloud. Saving adds the
extracted trip records, not the original image or PDF, to your trip. Shared images and
PDFs are not stored as conversation attachments.

Your API key is kept only in the iOS Keychain on your device. It is never shown in full
in the app, never logged, and sent only to Anthropic, with your requests.

## What is sent to Anthropic

The concierge is Claude, called directly from your phone over an encrypted connection to
Anthropic's API, and billed to your own Anthropic account. Each time you ask the
concierge something, or use a feature that relies on it (such as adding reservations
from pasted or shared material or summarizing your logs), the app sends Anthropic:

- the concierge's instructions, which are fixed text bundled with the app;
- your household profile, including travelers' names, preferences, dietary needs, and
  allergies;
- a context block with the current date and time, your current location (coordinates),
  today's itinerary and upcoming reservations, nearby weather, and recent logs;
- the conversation so far; and
- the results of lookups the concierge asks the app to make, such as nearby places,
  travel times, or a specific reservation.

For booking reading, the request includes the text, screenshot, photo, PDF, or Safari
page information you supplied, including any confirmation codes in it. The share sheet
stores it locally without a network request. When you open Travel Monkey with sharing
permission, a working key, and a connection, the app sends waiting bookings to Anthropic
for reading before you decide whether to save them. Discarding a booking afterward
does not recall that request. In ordinary chat, stored reservation confirmation codes
are sent when the concierge asks for that specific reservation.

To check opening hours, events, and other current details, the concierge may use
Anthropic's web search and web fetch tools. Those searches are run by Anthropic, not by
the app.

Before sending personal information to Anthropic, Travel Monkey discloses what it sends
and asks you to explicitly allow sharing. Permission is recorded separately on each
phone. The disclosure now includes pasted or shared text, screenshots, and documents,
so permission given before this update is requested again. Skipping onboarding or
adding an API key does not grant permission. Checking a
pasted key sends only a fixed “ping” to Anthropic, without your household information.

You can stop future personal-information requests in **Profile → Settings → Privacy →
Withdraw permission**, or remove your saved API key in **Profile → Settings → Anthropic
API key → Remove key**. Removing the key also withdraws permission on that phone. You
can also revoke the key in the [Anthropic Console](https://console.anthropic.com). These
choices do not recall requests already sent. Without permission or a working key, you
can still read and edit your trip and logs, but features that call the concierge do not
work.

Anthropic processes these requests under its own terms and privacy policy, which apply to
your Anthropic account: [Anthropic Privacy Policy](https://www.anthropic.com/legal/privacy).

## Apple services

The app uses Apple's own frameworks, which send some information to Apple to work:

- **MapKit** for place search, directions, travel times, map images, and Look Around.
  Search terms and locations are sent to Apple.
- **WeatherKit** for forecasts. The location of the forecast is sent to Apple.
- **CloudKit** for iCloud sync, as described above.
- **Local notifications** for leave-by reminders and similar alerts. These are scheduled
  on your iPhone, and no push server is involved.

These services are governed by [Apple's Privacy Policy](https://www.apple.com/legal/privacy/).

When you tap Directions, the app opens Apple Maps with the destination, or Google Maps if
it is installed and you choose it from the long-press menu. From then on, that app's own privacy policy
applies.

## Location

Travel Monkey asks for location access so it can recommend places near you, estimate
travel times, and tell you when to leave. If you grant "Always" access, it can also
notice when you set off and warn you if you are still where you were when it is time to
leave for a flight, train, or booking. Your location is never shared with the developer
or used for advertising. You can change or remove location access at any time in iOS
**Settings → Privacy & Security → Location Services → Travel Monkey**.

## What the app does not do

- It does not send your information to the developer or to any server operated by the
  developer.
- It does not include advertising, analytics, crash-reporting, or tracking SDKs.
- It does not track you across other companies' apps or websites.
- It does not sell or rent your information.

Apple may provide the developer with aggregated, anonymous App Store and crash statistics
if you have chosen to share analytics with app developers in iOS Settings.

## Your choices

You can:

- Edit your household profile and trips in the app, and remove travelers and remembered
  corrections.
- Delete a trip's conversations with **Profile → Reset memory**.
- Withdraw sharing permission or remove your saved API key in **Profile → Settings**.
- Revoke your API key in the Anthropic Console to stop all requests using that key.
- Turn off location access or notifications in iOS Settings.
- Delete the app's iCloud data in iOS **Settings → [your name] → iCloud → Manage
  Storage**.
- Delete the app to remove its data from your iPhone.

Data you have already sent to Anthropic is held under Anthropic's policies. Contact
Anthropic about it.

## Children

Travel Monkey is not directed at children under 13, and the developer does not knowingly
collect information from them. Because the developer receives no information through the
app, there is nothing held by the developer to delete. If you have questions, use the
contact below.

## Security

Data on your device is protected by iOS. Requests to Anthropic, Apple Maps, and
WeatherKit use encrypted connections, and the API key is held in the iOS Keychain. No
system is perfectly secure, so keep your device locked and your Anthropic API key
private.

## Changes to this policy

If this policy changes, the new version will be posted here with a new "Last updated"
date. Material changes will also be noted in the app's release notes.

## Contact

For privacy questions, see the [Travel Monkey support page](README.md). For anything
private, such as a security report, please use the private channel described there
rather than a public issue.
