# KYC Copy Brief — Risk Surfaces

**Product:** Ledgerly  
**Surface:** KYC verification step (individual freelancer tier)  
**Stage:** Copy audit before legal sign-off and eng implementation  
**Requested output:** Expert review of copy risks — legal exposure, user anxiety, conversion

## Flow summary

After bank penny-drop, users hitting ₹50k monthly payout volume must complete KYC:

1. PAN verification (auto-fetch from name + DOB)
2. Aadhaar OTP (Digio vendor)
3. Selfie liveness check
4. Address confirmation (Aadhaar-derived, editable with proof upload)

Average completion time: 4.2 minutes. Drop-off at Aadhaar OTP: 38%.

## Why copy matters here

KYC is where users decide if Ledgerly is a legitimate regulated platform or a data harvester. Support tickets mention:
- "Why do you need Aadhaar for invoicing?"
- "Is this shared with the government?"
- "I don't trust the selfie step"

Legal requires specific disclosures. Growth wants minimal friction. We need copy that satisfies both without terrifying users.

## Current copy (draft v2)

### Screen: KYC intro
**Headline:** Verify your identity  
**Body:** Indian regulations require us to verify your identity before processing high-value payouts. This keeps your account secure and compliant.  
**CTA:** Start verification

### Screen: Aadhaar
**Headline:** Confirm with Aadhaar  
**Body:** We'll send a one-time password to your Aadhaar-linked mobile number. We do not store your Aadhaar number.  
**Footer:** Powered by Digio, RBI-licensed KYC provider

### Screen: Selfie
**Headline:** Quick selfie check | **Body:** Confirms you're you. Encrypted, verification-only. **CTA:** Take photo

### Screen: Failure (OTP max attempts)
**Headline:** Verification paused | **Body:** Too many incorrect attempts. Try again in 30 minutes or contact support.

## Risk surfaces to review

### Legal / compliance
- Is "we do not store your Aadhaar number" accurate given Digio tokenization model?
- Do we need explicit RBI / PMLA reference on intro screen?
- Address edit flow requires "proof of address" — is helper text sufficient?
- Consent checkbox copy: "I agree to identity verification" — too vague?

### User anxiety
- "High-value payouts" — does this trigger fear of scrutiny?
- Selfie step has no preview of what happens to the image
- No estimate of how long data is retained
- Failure copy doesn't explain *why* attempts are limited

### Conversion
- No progress indicator on intro (4 sub-steps); no "do later" despite payout throttle
- PAN failure shows raw `NSDL_UNAVAILABLE` to users

## Stakeholder requirements

| Stakeholder | Requirement |
|-------------|-------------|
| Legal | Mandatory RBI KYC disclosure block on intro |
| Security | No overpromising on encryption specifics |
| Growth | Reduce Aadhaar step drop-off by 15pp |
| Support | Fewer "is this safe?" tickets |

## Open questions

1. Should we lead with benefit ("Unlock higher payout limits") vs obligation ("Regulations require")?
2. Is naming Digio in footer enough or do we need a "How we protect your data" expandable?
3. Can selfie copy reference liveness without sounding surveillance-heavy?
4. What failure copy is honest about fraud prevention without accusing the user?

**Artifacts:** `kyc-copy-v2.docx`, legal disclosure draft, Digio integration spec (retention section)
