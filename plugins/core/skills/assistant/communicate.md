# Communication Mode

Draft and send messages in the user's voice.

## Steps

1. Load `memory/voice.md`
2. Resolve recipient from `memory/people.md` — get Slack ID
3. Draft in the user's voice: short, "hey [name]" opener, no sign-off, Hinglish when natural
4. Show draft with recipient + channel context
5. Wait for "send" / "go" / "yep"
6. Send via `slack_send_dm` or `slack_send_message`
7. Confirm: "Sent to [name] in [channel/DM]"

## Exception: Sending to self

DM to U09KQAFK740 (standup drafts, bulletin drafts, EOD recaps) — send directly without asking.
