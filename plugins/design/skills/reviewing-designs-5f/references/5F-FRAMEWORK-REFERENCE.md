# The 5F Principles for B2B SaaS Design
## Complete Framework Reference

**Source:** Razorpay User Research
**Context:** Evidence-based framework from Indian B2B SaaS user research
**Application:** B2B SaaS products, especially for emerging markets

🎶 [Framework Song](https://suno.com/s/91IKJ8L5FYZa94cF)

---

## Framework Overview

The 5F Principles help design B2B SaaS products that drive adoption, reduce friction, and build trust with professional users.

| Principle | Focus | Key Question |
|-----------|-------|--------------|
| **Make it Fast** | Convenience | Can users complete tasks effortlessly? |
| **Make it Focused** | Attention | Does the design guide attention to what matters? |
| **Make it Fun** | Delight | Does it feel good to use daily? |
| **Make it Fluent** | Learnability | Can users master it quickly? |
| **Make it Fair** | Trust | Do users feel the system is on their side? |

---

## 1. Make it Fast (Convenience)

Prioritise Proactive Feedback: Stop vague rejections and silent failures.
Meet Users Where They Are: Integrate actions into users' existing daily workflow tools (Slack, WhatsApp, Teams, email—whatever they already use) and deploy AI as an in-context workflow executor
Keep Help & Discovery In-Dashboard: Eliminate disruptive links to external FAQs. Use in-line tutorials and trigger new feature discovery
Design for Human Error: Build trust through forgiving software.

### Proactive Feedback over Reactive states

Proactive feedback to potential errors rather than reactive error states. Users expect warnings + reasoning over reactive error states.
Contextual "Why and How" vs. Vague Rejections:  Users are deeply frustrated by systems that reactively reject an input without providing a clear reason. Users want the system to immediately and proactively pop up with the exact rule violation, so they do not have to spend time figuring out what went wrong

Proactive Outage Alerts vs. Silent Failures: In high-stakes environments like payment gateways or e-commerce, users hate discovering system failures reactively, especially when they find out because their own end-customers call them to complain. Users demand that the product proactively sends out notifications (e.g., "we are having CDN issues") and follows up the moment the issue is resolved.

Anticipating Rejections in Onboarding Workflows: During complex setup or KYC (Know Your Customer) processes, waiting days just to receive a reactive document rejection is highly irritating. Users expect a proactive indication of which specific documents might be lacking or problematic.


Verbatims:

"Instead of making us figure it out, the system should pop up and say exactly what we did wrong, like applying for two different leaves in HR software, so we can change it immediately."

"I need to know why it is getting rejected. Is it a 1MB size limit issue, or am I attaching the wrong document entirely for the setup process?"

"Show me exactly what stage my account review is at. If documents are lacking, tell me early so I can prepare them firsthand, even before a rejection."

Design Examples:

Pre-emptive File Validation (Data Entry/Uploads):
Do not wait for the user to click "Upload" to tell them the file is too large. The drag-and-drop zone should proactively read the file metadata. If a user drops a 5MB file, immediately display: "This file is 5MB. The limit is 1MB. Please compress your PDF or upload a smaller version."
Tracker for Compliance Review:
Replace the static "Pending" status with a micro-step progress bar (e.g., 1. Uploaded -> 2. AI Verified -> 3. Compliance Team Queue -> 4. Final Approval). If the system knows the compliance queue is backlogged, proactively set the expectation: "You are #45 in the queue. Expected review completion: 48 hours."


### Meet Where the User Is

I. AI contextual experience
The best AI experiences do not just answer questions; they perform workflows and take automated actions on the user's behalf.

Positioning AI as a contextual specialist to ensure users know exactly where it excels and where it ends. This leads to believing AI output as high quality.
The 3 stages of framing a user journey to be more AI-centred:
The Hook (Contextual Triggers): Show Agentic AI value via small, "magic" moments inside the current dashboard (e.g., auto-resolving a dispute, auto-data summaries).
The Sandbox (Dedicated Tab): Once interested, users want a full-screen "Playground" to experiment without fear of breaking their live dashboard experience.
The Native Goal (Conversational UI/UX): Finally, Agentic AI becomes a native layer where the dashboard itself changes as the user talks to it.

    II. Integration with Users' Existing Workflow Tools:
Allow critical alerts and actions via tools users already use daily—identify which channels your users actually live in (e.g., Slack for tech teams, WhatsApp for Indian SMEs, Teams for enterprises, email for executives).

Enable these tools as command centers for dashboard actions: approvals, emergency alerts, doc uploads, etc. Users shouldn't have to log into the dashboard for time-sensitive actions.

**Pattern to evaluate:** Does the product meet users in their existing workflow, or force them to add another tool to check? B2B SaaS buying decisions increasingly depend on integration capabilities and fitting into each company's unique workflow ecosystem.

    III. Nobody reads these days:
Avoid Continuous Linking to External Documentation for any resolutions
Nobody likes/wants to read B2B documentation anymore.
Frustrating user workflow to redirect users to the documentation page, FAQs to resolve any issues, rather than resolving it inside the dashboard experience, which ends up disrupting the particular workflow.
Embed help diry into the UI. Use hover-states, tooltips, and in-app searchable side-panels so users can read documentation without leaving their active screen.

IV Contextual Product Discovery over Clutter:

Instead of sending an email about a new feature or cluttering the dashboard with cross-sells, discovery should happen contextually.

If an AI or system recognises a user is struggling with a workflow (e.g., analysing failed payments, copy-pasting manually), a non-intrusive pop-up or insight snippet should appear offering a new tool or feature specifically related to that task.
The AI acts as a navigator, instantly generating the data and exposing the user to the platform's deeper capabilities



Verbatims:

On seamless B2B tool integration: "No system lives in isolation. If a tool has a plugin or a connecting ecosystem to multiple feeder systems upstream or downstream, it is incredibly useful."

On in-app tutorials over manuals: "Instead of making me figure things out, give me a short 30-second interactive tutorial step-by-step when a new feature is launched. That makes it much easier."

On guided discovery: "We tend to forget a new widget exists unless someone holds our hand and informs us there at that moment, 'Hey, this is a new feature, would you like to try it?'"

On executing workflows: "Data giving data is not worth it. I want an AI that takes action, like executing a workflow, automating a refund, or resolving a settlement dispute."


Design Examples:

**Workflow Integration via User's Preferred Tool:**
An executive is travelling and won't open a heavy ERP to approve a vendor payout.
The system sends a rich message via the executive's preferred channel (e.g., WhatsApp for Indian SME owners, Slack for tech executives, Teams for enterprise) with an AI-generated micro-summary: "Vendor Payout: ₹45,000 for server maintenance (Note: 10% higher than last month)."
Below the text, native action buttons appear: [Approve], [Reject], or [Ask AI for itemised breakdown]. The executive taps "Approve," and the SaaS dashboard updates instantly via the backend.

**Key pattern:** The tool adapts to where the user already works, not the other way around.
Feature Discovery
Intercept pain, don't send emails.
Track "struggle metrics" (e.g., a user manually downloading and uploading thsame CSV format three times).
On the fourth try, trigger an inline pop-up next to the export button: "Tired of manual mapping? Try our 1-click automated sync."


### Accounting for Human Errors

i. Having escape workflows builds trust

In low-trust markets like India, users demand to have a clear 'Undo' route to rectify their workflows.
As a rule of thumb, most Indians, before they start any workflow for the first time, try it out as a "test" session, so enabling easier exit paths for 1st tries and being forgiving of their errors is important.
Less clear escape routes lead to a major trust breach among users as they perceive it as the company locking them in, thereby leading to lesser engagement

ii. Systemic Rigidity Destroys Trust

When a system is unforgiving regarding specific data structures (like locking an email ID, phone no. forever), users feel alienated and view the company as apathetic.
Users expect software to be malleable to human error and not hold any personal information as uneditablcompliance they are uneditable fields, then users expect a way forward workflow on how to make the changes too.


Verbatims:

If by mistake I make a profile using my email ID, throughout my lifetime as an employee I cannot use that email ID again or map it to a different ID. That email is lost forever... they just don't care."

"Somebody needs to have the power to verify our new address... speaking with bots, they do not have the ability and the approval to make those changes. It looks like something is getting stuck.

"Sometimes errors happen. The system should tell us exactly what we did wrong... it should straight away pop up on the screen so that we can change what we were doing instead of figuring it out on our own."

Design Examples: Subscriptions - old tier, workarounds to overcome compliance


---


## 2. Make it Focused (Attention)

### Hierarchy of Information as Glance >> Act >> Explore
A valuable dashboard organises information in a layered, progressive structure, preventing users from having to read dense walls of text all at once.

Top Level: The "10-Second Glance" (Sanity Metrics): The very top of the dashboard should be dedicated to high-level, visual summaries of business health.
Users want to roll their eyes over the screen and instantly see key metrics (e.g., total collections, failed payments, week-on-week growth) represented through pie charts, histograms, or simple line graphs.
Text should be minimal in this section.

Mid Level: The Action Zone: The dashboard should clearly separate passive "data viewing" from active "doing".
Below the core metrics, users expect a distinct section for daily action items, such as pending approvals, open tickets, or urgent failed transactions that require immediate intervention.

Bottom Level / Secondary Layer: The "Deep Dive": Raw, tabular data (like a list of 100 recent transactions) should not clutter the main homepage.
Instead, the dashboard should act as a headline summary.
If a user wants to investigate a specific spike in a graph, they should be able to click on it to open a dedicated, separate screen containing the dense tabular data with full sorting and filtering capabilities.

Verbatims:

"Visual graphs enable me to quickly grasp what's going on. If I need to dig a little deeper, I can always just click on the graph and view the raw data myself.

The first thing I do is check if there are any requests pending at my end, like leave approvals or regularisation requests, right on the main page so I don't have to check other tabs."

"When I look at a dashboard, if I roll my eyes for 10 seconds, I need to know what is happening through graphs. I'll only open up the raw data figures when I actually want to deep-dive."


Design Examples:


### Glance Zone experiences Banner Blindness

i. Dashboard top area experience banner blindness owing to less criticality

Users actively train their minds to completely ignore the top and right sections of their B2B dashboards because companies use that space to aggressively cross-sell irrelevant products, add salutations, d less critical updates.
Dedicate the top and side navigation bars purely to functional tools to maintain trust and utility (like Quick Links).


ii. Avoid Permanent Banners and Redundant Greetings

Users get annoyed when prime screen real estate is taken up by static text like "Good Morning" or a "Key Update" banner (e.g., "International payments enabled") that stays on the dashboard for a year without disappearing.
Static Salutation messages with no delighters are often ignored and have no value as Product salutation has become saturated across B2B or B2C products.
Enable Auto-dismiss informational banners after a set period or once the user interacts with them.
Replace pleasantries with actionable data summaries or attach meaningful pleasantries that add to user value.


Verbatims:

"The top-right section is always something my mind is tuned to completely ignore. Apart from occasional notifications, I have no necessity to look there at all."

"Once I've logged into the platform for the first time, my mind tends to ignore the top right section entirely unless I need to change a setting."

"They advertise a lot of their banking services and consumer offers. Why is screen space used for something I see every day that is completely irrelevant to my business?"

Design Examples:

### Feature Paralysis from the Everything Everywhere Sidebar

Users feel overwhelmed and alienated when they log into a suite (like ERPs, CRMs) and are greeted with 100 features on the sidebar, 99% of which they don't need.
This leads to user confusion on what action to take and overwhelms first time user and feels like they would need extensive handholding.

Hide advanced settings and group tools into collapsible menus, only showing the 3 to 5 core features relevant to that specific user's daily role. [More about this on Navigation]



Verbatims:

"The mega menu will sit on the left side, and everything is folded into that. Our old CMS had so many pages that we couldn't train new members without months of effort. That was a deal-breaker"

"We had to recode some of the workflow... A lot of features had to be removed for people to make it simple and follow the flow. After that, it didn't take long for people to get along and learn it"

Design Examples:

### Cultural relevance increases comprehension power

i. Defining culturally relevant semiotics for easier comprehension
Generic Western icons (like a 'floppy disk' for save or 'pancake' for menu) often don't resonate.
Design leaders use culturally suited iconography, such as a "Galla" (cash box) for earnings or a physical stamp for "Approved", to align with the user's offline mental models.
Similarly, direct translation into formal regional languages often sounds robotic. Using colloquial local scripts (eg: Hinglish etc) builds a sense of familiarity

ii. Creating designs that are Value Multipliers beyond Price
India is a price-sensitive market, but being cheap isn't enough; it must be vetted by other parameters.
Design leaders use Product Tags (e.g., Best Seller, 10k+ Sold, Most subscred, etc.) as social validators that move the user from price-sensitivity to value-certainty.
Some SME business owners often view software as a Cost Centre (a loss), not an Investment (a gain)
They lack knowledge & time of how to attribute small SAAS tool investment into leveraging their business growth.


iii. Minimalism vs GenZ loud = High brand perception
Minimalistic dashboards are seen as a Bougey Trust Signal, even though users expect data-rich interfaces.
In a market cluttered with loud, ad-heavy interfaces, minimalism acts as a premium trust signal.
Clean layouts and no raunchy colours suggest a sophisticated, high-end environment where the user isn't the product being sold. However, a balance of being data-heavy is also expected.
Colours must serve a direct functional purpose to guide the user's eye. Users heavily prefer calming palettes, such as rich whites, pastels, and soft blues/greens, over harsh contrasts, depending on the dashboard personality.
However, GenZ loud interfaces with bright colour schemes, quirky tone, see slower adoption in India as only high-tech-savvy users prefer them.

Verbatims:

"I'm a Class 5 student when it comes to math. An accounting software needs to match my exact business reality—like how my specific industry calculates 18% GST on a markup versus 5% on a total invoice—rather than throwing complex global terminology at me."

"Western products come highly standardised off-the-shelf. Indian businesses, however, demand complete localisation and custom plugins that adapt to their exact cultural operations and imagination."

"In a high-intensity work environment where one minute equals three messages, you need refined lines, clean transitions, and a soothing effect. An aesthetic, white-and-blue interface feels like driving a modern, premium EV compared to legacy tools."


Design Examples:

### Mapping a complete User journey to decrease Attention demand
Users do want to spend less attention on B2B dashboards to avoid cognitive fatigue from their daily tasks. Hence, ex a fully seamless user journey experience.

Some B2B tools lack end-to-end user journey mapping for each workflow and has half open feedback loops, making the user confused and stranded midway. Workflows outside the dashboard, such as
File uploads
Permissions/approvals
Cross-referencing other data
User role exchange, etc

Within a particular workflow, even within the dashboard interface, the journey is disconnected when:
Tasks go to cross-product functionality
Tasks go to another user role
Tasks with no feedback given
Tasks with no defined end state or exit state

Therefore, having a clearly mapped user journey both within and outside the system enables better feedback closure and demands less attention span from the user.


Verbatims:

"Data gathering is fragmented. We don't have a common tool, so we have to manually download reports from different channels and cross-reference them in Excel."

Dead-End Support Loops: "We raise a ticket, but it goes to a generic support mailbox with no clear owner. We waste days doing follow-ups because they don't understand our business urgency."

"Earlier, our agents extracted user data from different places, taking 8–9 minutes per call. By mapping everything into one single Customer Data Platform, the handling time decreased to 4–5 minutes."

Design Examples:


---


## 3. Make it Fun (Delight)

### Move at thought speed

B2B delight isn't only surprise; it's momentum. It's the product interface moving at the speed of the user's thoughts.
Both Actual and Perceived performance - The faster the product mirrors the users' mental model of intent & outcomes, the more it feels like it is working with them rather than demanding effort from them

i. Delight through Actual performance
Delight is achieved through Predictive Defaults.
Anticipating user needs and allowing faster task completion by skipping unnecessary input.

Humanize Errors and Celebrate Success
This counteracts the perception of a "lifeless" B2B tool personality.

Shift to Insight-First Tooltips to simplify cMaking it understandable without manual calculation, which is a key measure of delight.

ii. Delight through perceived performance

Temporal Smoothness (Consistency > Speed):
A system that consistently responds in 100ms feels "smoother" than a system that fluctuates between 20ms and 200ms

Spatial smoothness: Linear motion (robotic, constant speed) feels "stiff." Whereas Ease-in/Ease-out motion (starting slow, speeding up, slowing down) feels smooth because it mimics friction and inertia.

Cognitive resume: B2C apps are designed for single-session doomscrolling, but B2B tools are victims of the Multitasking Buffer.
Prioritise Persistence of State: The mental model expects the software to remember exactly where they were, including half-filled forms and specific filter settings, to reduce Resume-Cognitive Load.


Verbatims:

"Just refined lines, better transitions—all of it to have a soothing effect. We... we do a lot of high-intensity work... When you are in that possible space, the last thing you nee a bad effect on your screen."

"The synchronizing goes very well where I've stopped some place and I can, you know, work again with the same data. Sometimes we save, you know, we keep on saving"


Design Examples:

### B2B Dopamine Hits

i. Using Micro-Interactions and Haptic, Audio Feedback to create dopamine hits

B2B tasks are notoriously monotonous (e.g., moving tickets, doing data entry). Designing subtle, gamified feedback creates massive delight.
For example, Users love it when moving a ticket to "Complete," which triggers a slight screen shake and a satisfying sound.
Similarly, using "celebration poppers" and visual confetti when a project is closed, which acts as a powerful positive reinforcement for the team.


ii. The Utility-to-Engagement Paradox: Exit vs. Stay

B2C Success = Prolonged Engagement:
Consumer apps are designed to keep the user inside (the "doomscroll" effect), leveraging gamification and instant positive reinforcement to maximize time spent.

B2B Success = Rapid Exit:
In sometances, for the business user, the interface is a hurdle to the result. They value Time-to-Task Completion above all.
A B2B tool is considered magical when it's fun to use, and it also knows when to become invisible, allowing the user to execute complex data-heavy tasks and return to their core job functions immediately.

Passive Engagement = Hook factor
Passive engagement inside the B2B or B2C interface is always built to be the hook factor that doesn't disrupt the core workflow but gives an indirect sense of dopamine hit.
These engagements are centred around functional needs but marked as "good-to-haves" by users
Eg: Wishlists, Saved data tables, Calculators, Templates,B2B reels,  etc


    iii. Visualising meaningful empty states:

Users want a clean, meaningful visualisation of empty data states on why it's empty, rather than just an empty table or white space
A blank table makes users wonder if the app is broken; an explicit "Zero Activity" chart confirms it's working.
Silence is interpreted as an error.
Eg: Design explicit "All Caught Up" or "Zero Transactions Today" graphic states.

iv. Showing the WOW factor for their business growth:

Humanising Dry Data: Abstract business numbers can be boring. Delight can be injected by translating dry metrics into fun, relatable, real-world analogies.
Eg, Instead of just stating a company processed $3 million in volume, a dashboard might say, "If these were $1 bills, they would stack up to the height of the India Gate".
Proving Tangible Business Impact: True delight is showing the user the exact ROI of their actions.
For instance, if a user sets up an automation, the platform should proactively show them a week later exactly how much money or time that specific automation saved the business.


Verbatims:

"If you mark the status of a task as closed, then there is a celebration, a popper coming up on the screen...And if a project is moved to archive, then they show certain visual effects... it basically motivates the team that whenever they close a task…" attention span or the frequency of change is much quicker and faster on B2B; versus on personal apps, it's more like if you're on one thing, you're probably on it for a very, very long time... and then you're just, you know, doom scrolling"
"When somebody sets up an automation, we say, 'Hey, great, these are the actions you can expect in the next seven days, and this will be the business impact of the action.' that's where he gets the 'Oh, wow.' This is what I was told, like, seven days back, that this will be the impact of the automation."


Design Examples:

### Dashboard to have its own Personality

i. Operational capability, Performance, and Automation determine dashboard personality perception

Users categorise software based on the tension between capacity and speed. There is a distinct mental separation between the tools that carry the organisation and those that accelerate the workflow.
Operational Anchors (Buses/Trucks): For heavy, data-intensive tools like ERPs, CRMs, users prioritise steady rlity over fun or speed.
They view these as high-capacity vehicles designed to navigate business bumpers (compliance, complex data) safely.
In this category, a bulky interface is tolerated if it guarantees that the entire organisation reaches its destination without a breakdown.
Performance Enablers (Sports Cars): For transactional tools like Payment Gateways, Management tools, and Data analytics, users demand high-speed execution.
Success here is measured by a sleek, Ferrari-like craft that provides a premium, frictionless experience.
The Autonomous Ideal (EVs/Teslas) end state for B2B tools:
Modernity is personified as a silent, minimalistic, and proactive EV.
Users desire Hybrid Agency: a system that uses AI to self-drive through low-cognitive administrative tasks while allowing the user to take the wheel for high-stakes, strategic decisions.
A tool is considered modern only if it reduces the need for the user to manually shift gears through redundant processes.

ii. Designing to create a sense of belonging inside dashboards
Build Business Impact Feedback Loops for end-users to build a sense of belonging
In B2C apps, users get an immediate feedback loop (e.g., you like a reel, someone follows you back).
In B2B, the tasks are highly repetitive and often feel like a one-way street. To make the tool relatable, create positive reinforcements that show users the long-term value of their work
Eg: If an executive resolves a ticket, notify them a month later saying, "The customer whose issue you resolved just brought in two more referrals."

Remembering the user preferences over time
A user might log in every day at the same time and manually click through to open the exact same tab.
A relatable tool should learn these behavioural patterns and auto-suggest or automatically open their preferred tabs upon login.
Furthermore, the dashboard should act proactively by recommending specific data cuts based on the user's specific KPIs (e.g., auto-suggesting views for a product manager versus a finance lead, etc
Verbatims:

"I think of them like these electric vehicles of today. They are more modern, seamless, and silent. In essence, they are more minimal and simple to interact with. That's how I want every B2B dashboard to feel like"

"In social media, you like someone's reel and they follow you back. B2B is a very one-way process. It won't hurt to let an executive know after a month, 'Hey, the customer whose issue you resolved has increased revenue by X.'

"When I use Swiggy, it always shares customized suggestions based on my browsing. But in B2B, there is no personalization. If I have a pattern of logging in at a certain time and opening a specific tab, that tab should automatically open. It needs that kind of personalization."


Design Examples:

### Agentic AI to have its own Personality
AI Lacks Business Context to show Emotional Quotient currently:
Bots struggle to understand the nuances and specific context of a user's problem.
Explaining a complicated issue to an agent via text takes a lot of time and rt, whereas a human on a call can grasp the context and understand the user's pain points much faster.
A bot is perceived as not understanding a user's emotions, personality, or comfort level.
i. AI Archetypes as Emotional Anchors
Giving AI a distinct personality or archetype helps humanise the interaction.
This makes the system feel like a relatable companion rather than a sterile algorithm, especially in high-anxiety B2B Fin-tech environments.

Verbatims:

"The emotional touch should not be lost. The app doesn't recognise if the user is a chai vendor or a billionaire... That's where AI comes in, to capture your preferences, your past transactions, likes, dislikes, and give you a tailored solution."

"I do not want to spend my time typing and explaining to a chatbot what went wrong". "If my payments are down, I cannot just sit and have a text chat with an AI telling me to 'try this'; I need a human to step in quickly and guide us"

"Sometimes these B2B AI chatbots act like a 'grumpy shopkeeper' because they securely manage our work. Most of the time, they operate fine, but when they are grumpy, it gets very difficult to safely get them to do what you want"


Design Examples:


---


## 4. Make it Fluent (Learnability)

### Intuitive Interfaces = Easy to Learn
Improve the memorability of action workflows & performance efficiency of the dashboard that leads to being Intuitive.

Intuitive = Higher Learning rate + Efficiency + Memory retention rate + Subjective Delight
Repeated Usabilityof above = Intuitive interface
B2B interfaces have a steeper, longer learning curve than B2C, and Memory retention is poorer in B2B apps compared to B2C.
B2B systems often lack a dashboard feel and are seen as a machine, not an enabling assistant, unlike B2C personal apps.
Memory of workflows = happy end-users. That's why B2C apps are considered intuitive
So, test for learning curve over no.of steps taken. Users appreciate subtle, persistent visual indicators teaching them features contextually.


Verbatims:
"Instead of heavy training,ools should provide a short, 30-second contextual tutorial the moment you log in, pointing out every single icon step-by-step so you know exactly where to click."

"A truly user-friendly tool allows a fresh college graduate to learn and operate it within just a few days, rather than the six months of intense training required for legacy systems."

Design Examples:

### Persona-based customisation increases Learnability
Role-based Dashboard customisation enables higher user satisfaction in using dashboard interfaces over a generic dashboard

Modular, Persona-Specific Dashboards: The interface must be highly customizable, allowing the CEO to see macro-level revenue trends, while an admin, ops, finance, customer support etc can see and act on their microscopic daily tasks.
A single, generic dashboard is useless because different roles have entirely different priorities.

A tool becomes a daily habit only when it feels like a personalised command centre, entirely stripped of data that belongs to other departments.
Since the command centre customisation view is not clear in most B2B dashboards, decision makers across revenue growths resort to creating manual Excel sheet views or rely on an employee to process a bird's eye view for themselves.

    i. Design Scalability through Modular Customisation
Over-customisation kills a product's ability to scale. The solution is Modular Workspaces, where users can pin or hide pre-built components.

This gives the user a sense of agency and customisation without breaking the underlying Design System (DS) or complicating future updates for the engineering team.


    ii. Indian User Personas need carefully curated RBAC
Indian work culture has multiple levels of hierarchy,y and each level has one specific JTBD.
Hence, RBAC for larger enterprise softwares require master admin control centres and explicit communication of the same on the dashboard

A single SME user can access a system with different intents at different times (e.g., a Manager in the morning and a Contributor in thternoon).
Solving for these shifting user personas requires a UI&UX that adapts its density and navigation based on the current active goal.
Adaptive designs have to account for Tech saviness and city-specific cultural context to enable better role-based customisation.



Verbatims:

Every user has a different priority. From a management perspective, I want to know my daily sales and growth patterns, whereas an admin looks at the dashboard from a completely different perspective. I need to be able to customize the dashboard so I only see the three or four things relevant to my specific operational side."

"Dashboards need to be built role-wise. When I log in, depending on what kind of role access I have, I should be able to see a dashboard that is automatically configured specifically for my role and my daily workflows."

"The Managing Director would look at a completely different dashboard with different macro-information, whereas I, who am taking care of production quality, would want completely different numbers and categories displayed on my screen."

Design Examples:

### Remembering complex dashboard Navigation

i. Macro-to-Micro Navigation while processing information
Users prefer clicking a visual summary to open a detailed report rather than adjusting complex filters.
Progressive discovery matches human investigative behaviour (seeking context before details).
L0 1: AI Summary.
L1: Visual Chart.
L2: Click-to-expand raw data table.

Users rarely prefer using advanced filter boolean logic, searching manually at each table and list views.
The 1st entry point Macro navigation start point, is crucial to enable users to move through the architecture. The copy language has to be simple to grasp and match user intent over system outcome. Eg: Manage payroll vs Disperse amount
If the user enters via Search, then showcase the breadcrumb design of how they entered so they remember the workflow the next time, even if they re-enter via Search again.


Verbatims:

"When I look at a dashboard, if I roll my eyes for 10 seconds, I know what is happening through the graphs... The moment I want to deep dive and spend some quality time, definitely I'll open up data figures, metrics, and then I'll compare.

"If I have multiple modules... instead of going to tab number 5, opening the sub-module 6th one, and then locating where the information is, I can simply ask the AI here, and then it will give me a result."

Design Examples:

### Lite version of Navigation for memory retention
Designing the Navigation to enable a Lite version of the Dashboard

A lite experience ensures that users do not suffer from feature fatigue. Even if a software has 100 features, the interface must feel simple and familiar.
Familiar UI Placements: Users strongly rely on standard mental models. The primary navigation menu should always be placed on the left, and the universal search bar should be pinned to the top.


Hiding the Clutter to customise a Lite view: SaaS tools often build too many features, causing cognitive dissonance. A lite experience groups similar sub-features into a single collapsible menu item rather than expanding them all by default.
For instance, instead of listing "Payment Links," "Payment Pages," and "QR Codes" separately on the main menu, they should be nested under a single "Payments" tab to save real estate.
Advanced settings or rarely used features (based on past system activity) should be hidden behind a button or secondary tab.
Enabling the users to customise their dashboard such that features that matter stay, and an extensive view of features can be enabled as per the user's wants and needs.


Verbatims:

"The sidebar has 100 options, and you get overwhelmed... You don't know 99% of them, so you don't feel familiar anymore. 99 things, you don't even need... so cleaning it up is something.

"If you see limited options, which are more important and basically the use case... it's easier for someone to navigate. There is no need to show [secondary features] on the initial screen... put them into some tab or behind button."

"You don't put your sub-menus... or cross-sell items on the main navigation. If a sub-menu item is so important...you don't have to go through steps to reach there."

Design Examples:


---


## 5. Make it Fair (Trust)

### Trust through Emotional Intelligence

Managing the B2B Blackbox: Users value service more when they can see the work being done; a "black box" is less trusted
Repeated vague errors or a lack of error states cause users to stop self-diagnosing and immediately log support tickets, leading to high-maintenance users.
Halo Effect: Trust from an endorsing entity (e.g., RBI, ISO 27001, large brands) is extended by the merchant to all aspects of the tool, even untested ones.

Anticipatory System EQ: Trust is built when operational data is paired with a clear path forward.
Self manages to come up with possible next steps to help the user proactively, without the user reaching out.
Self-identifies problems and takes/directs accountability (Eg: your bank failed, bank system down etc)
Being socially empathetic by acknowledging users' emotional states such as relief, frustration, patience etc
Communicate via User-centred copy language that will build a passive relationship with the user



Verbatims:

"It gave a very random reason... it took me a day or two to understand why the system did not take [my input]. It should give us the right information on what we did wrong... straight away that should pop on the screen so that we change what we were doing.

"It should give you a trust factor by showing the progress or next steps. Now, what next? Will I have to wait for the next 72 hours...? It should be two-way communication; otherwise, the person will keep following up or get lost."

"While navigating the dashboard, something friendly is nice. But when transactions are getting processed, it feels good if it is a bit formal instead of 'Hey friend, we have sent you money!' That does not feel good."


Design Examples:

### Trust through Radical Transparency

i B2C mental model of micro-step progress tracking:
Uss expect backend business processes to be visualised exactly like an e-commerce delivery tracker.
Rather than a static "Under Review" page, users want to see the exact stage of their application (e.g., Uploaded -> AI Verified -> Manual Review -> Approved)
Having a step-by-step progress tracker makes it much easier to understand where the process is currently sitting, mirroring the transparency of the company


ii. Being data-rich while being less visually dense - an Indian ask
Building trust through radical data/information transparency (Show data on the face) is important to create consistency in dashboard performance and design.

Being proactive in showing alerts, fare breakdowns and giving feedforward feedback are seen as signs of trust
Simple to read information with fewer jargon words is perceived as not trying to hide behind the legality of words.
A cluttered screen feels like it's hiding something. A disciplined information hierarchy communicates that the organisation is confident in its data and has nothing to hide.
Crisp data visualisation that allows for 2-second skimming provides immediate assurance that "all is well," which is more effective than a long, detailed list view.

Verbatims:

"Show if it is under review at what stage your review is, similar to how a logistics company shows it's moving... it's much easier to understand which process I am at. If documents are lacking, I will prepare them firsthand even before rejection."

"They should talk the language which I understand... If they say our software improved productivity by 10%, I understand it. If they say we used a RAG model, I cannot make any sense out of it."

"You must always tell us the changes or effective things you are going to bring so we get to know beforehand... never charge hiddenly. Lack of transparency is something which can simply turn you off."

Design Examples:

### Trust through Language
i. Speaking the Business Language
Building user Confidence through copy. It must focus on their business outcomes and not backend engineering or product lingo
Handling error states with vague error messages creates more distress
It should state "why" the error is happening
"What" the user should check/do to overcome the error
Contextual Hinglish-like Tooltips: Use plain English or Hinglish for complex compliance terms (e.g., "TDS: Government ko dena hai"). It reduces the fear of legal errors.
    ii. Match the Tone to the Task:
A B2B tool should have a dynamic personality.
While navigating the dashboard or seeking help, the language should be friendly, conversational, and approachable (similar to a Slack bot).
However, when processing sensitive actions like financial transactions or data deletion, the tone must immediately shift to formal and serious to establish trust.





Verbatims:

"When it comes to accounting software... some of the terminology they use, I have never heard in my life. I was not very comfortable with the software. I took it off and preferred using Google Sheets instead."

When a document gets a vague 'invalint' rejection, I need to know why. Is it a size limit, a format compatibility issue, or the wrong document entirely? Not providing that information is very painful.

"I think even these apps are like employees who don't get too casual... they are extremely professional in nature, very organized, and work well when they maintain that professional boundary.

Design Examples:

### Building an AI that users can trust

    i. Attribute Trust and Accountability to an AI:
Users inherently trust human answers more and can hold them accountable for the issue they are facing. Simply put, they can put a human face to a problem.
Hence, designing Agentic AI to account for the means to build accountability for the solution it proposes
The problem with AI is that it can give wrong answers with confidence, whereas hearing a definitive "no" or receiving a resolution from a human carries much more trust.
Lack of Authority to Execute Changes: Even if an AI bot understands the issue, it often lacks the administrative ability or approval to actually make backend changes on behalf of the user (such as verifying a new address or processing a complex refund).
Because bots cannot execute these tasks, users prefer jumping straight to a human who has the power to solve the problem.


ii. Following a verifiable AI framework to build on User trust:
Users refuse to act on an AI interpretation unless they can quantify its certainty and trace its logic back to a trusted, static source.
Every AI-generated insight could be accompanied by a Probability Badge (e.g., "98% Confidence"). This allows the user to triage their thought process to the AI's
The interface could also provide a one-click journey to the Source of Truth with how AI arrived at the response, insight, etc. The conversational design shifts the AI from a Magic Tool to a Trusted Assistant in B2B.



Verbatims:

"Payment transaction is also a critical application, and you cannot 100% rely on the digital tools. You can 100% rely on a layman... because you know that he is a human a he can check it manually.

"Companies need to build trust... I don't trust directly. Whatever the analyzation, give me a good one; still, I will cross-check everything before proceeding further... you cannot directly rely on everything [just] because they used AI."

"I will say AI is better, but it should have an option to contact the POC itself. I believe in something called 'human in the loop.' Even in the AI sector, you have to have a human who is in the loop of everything.


Design Examples:


### High Switching Costs Create Forced Loyalty leads to Trust Loss

In the B2C world, a user will delete an annoying app in seconds.
In B2B, companies tolerate frustrating software for years because the cost of leaving is astronomical. B2B tools are deeply woven into a company's workflows.

Moving away from a tool with a bad UI means breaking multi-year enterprise contracts, spending months of developer effort to rebuild API integrations, and halting daily operations.
Because the inertia and risk associated with migrating sensitive data are so massive, companies simply accept and adapt to a poor UI/UX.
If poor UX/UI is causing monetary losses or falsified data, then it's considered an extreme case to move away from that tool.

Adapting to a poor UX/UI through forced loyalty leads to slower trust erosion, where users start downsizing their business engagement with the SAAS platform.
Instead of fully uninstalling a failing tool, merchants will keep it integrated but route their business away from it.


Verbatims:

Most of these tools are deeply integrated into the company's workflows... The amount of money that I will need to spend to fix my integrations to move out of the tool itself is so huge that it takes months of development effort... that inertia is there

We couldn't move out of the tool even when we didn't like it... we were stuck with Clevertap because there was a contractual play in play. The contract was signed before me... we couldn't move because of contractual obligations."

"It's too painful towitch all your work to some other tools, because the importing and exporting might not be there from their tools. So, we are not considering it because it's doing well. So, why... are we moving to another tool?"

Design Examples:

### Rebuilding trust after a poor user experience

i. Curate a Trust Probation experience when churn triggers are identified
When tools fail repeatedly, mature organisations put them on strict probation.
First, show a temporary fix if possible
Second, strictly categorising bugs (P0, P1) with guaranteed resolution times.
Third, proactively monitor the software's logs, and share updates with users on how well something earlier reported as a problem is performing

ii. Churn trigger isn't the technical bug itself, but the indifference of the company to resolve it.
Merchants don't view support as a Ticket; they view it as Operational Firefighting.
A 24-hour resolution for a mission-critical business issue is perceived as a lack of business empathy from the SAAS provider
Hence, Tier your support by Business Urgency, not Technical Severity.
A support lead who understands Diwali Sale pressure is more valuable than a developer who only sees a network lag.


Verbatims:

"We will ask them to give us an SLA SOP, market them P0, P1, P2, P3, and define the resolution time, expecting P0 to be fixed in the same day." "In our third warning, we mention that we will proactively observe the logs to check if the issue is still coming or not, giving them a one-month notice period."

"It took 24 hours for them to come back, which is pathetic for mission-critical services like payments." "The response time has to be in minutes, because if you wait for 24 hours and lose that revenue, that is not acceptable."

"When we raise tickets to the software company, the case goes to a generic support mailbox and the individual will never understand the business urgency…We waste days because they don't understand the severe impact on sales and consumers if we don't fix what seems like a small technical bug."

Desn Examples:

---

## Application Guidelines

### When to Use 5F Framework

**Emphasize 5F when:**
- Product is B2B SaaS (especially fintech, payments, ERP, CRM)
- Target market includes India or similar emerging markets
- Users are SME business owners, operations managers, finance teams
- Design involves dashboards, data-heavy interfaces, workflow automation

**De-emphasize 5F when:**
- Product is B2C consumer app
- Market is exclusively Western/developed with different cultural norms
- Design is purely visual identity work (branding, marketing pages)

### 5F Power Moves

Use these in "Soni on Shrooms" mode or Exploration Stage:

1. **Workflow Tool Integration** - Critical alerts, approvals, doc uploads via tools users already use (Slack for tech teams, WhatsApp for Indian SMEs, Teams for enterprises, email for executives)
2. **AI Workflow Executors** - AI that takes actions, not just answers questions
3. **Micro-Step Transparency Trackers** - E-commerce style progress visualization for B2B processes
4. **Cultural Icon Libraries** - Locally relevant iconography (Galla, stamps, etc.)
5. **Hinglish Copy Experiments** - Contextual tooltips in colloquial language (for Indian markets)
6. **Business Impact Feedback Loops** - Show users ROI of their actions weeks later
7. **Celebration States** - Confetti, sounds, haptics for completed workflows
8. **Persona-Based Modular Dashboards** - CEO view vs. ops view vs. finance view
9. **Confidence Scores for AI** - "98% confidence" badges with source tracing
10. **Lite Version Toggle** - Hide 90% of features, show only role-relevant tools

---

## Framework History

**Created:** Based on Razorpay user research with Indian B2B SaaS users
**Evidence Base:** User verbatims from merchants, SME owners, operations teams, finance professionals
**Market Context:** Indian B2B SaaS ecosystem, with applicability to emerging markets
**Integration Date:** 2026-03-02
**Used By:** Saurabh Soni Design Critique Agent (UX Reviewer skill)

---

**For questions or contributions to this framework, contact the Razorpay Research team.**
