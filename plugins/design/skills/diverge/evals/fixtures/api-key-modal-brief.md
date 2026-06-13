# API Key Creation Modal Brief

Surface: one-time API secret reveal after key creation.

User role: developer integrating with the product API.

Core job: copy or securely store the secret before the modal closes.

Product objects:
- API key
- Secret value
- Project/workspace
- Permission scope

Known states:
- secret visible once
- secret copied
- secret not copied on close attempt
- key created success
- copy failed
- permission denied

Constraints:
- secret cannot be recovered after close
- no email fallback for the raw secret
- must work on mobile and desktop
- accessibility labels required

Pain point:
Users forget to save the secret and later file support tickets.

Risk level: high — credential loss blocks integration.
