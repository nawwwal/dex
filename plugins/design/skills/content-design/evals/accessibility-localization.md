## Prompt

```md
Use $content-design to review this UI copy:
Button: Click here
Tooltip: You can only do this if your settlement is delayed.
Toast: Your KYC was rejected because your PAN name did not match. Upload a corrected PAN by 12 June.
Alt: Image of search icon
```

## Expected behavior

The skill should flag vague link/button text, essential instructions hidden in tooltip/toast, and visual-format alt text.

## Pass criteria

- Replaces `Click here` with an action or destination.
- Moves critical KYC rejection copy out of a disappearing toast.
- Flags tooltip as the wrong place for essential eligibility information.
- Changes alt text to the action or meaning.
- Checks localization risks and variables.

## Fail signals

- Treats accessibility as only alt text.
- Leaves critical content in a toast.
- Keeps `Image of`.
