# Transaction Verification Flow (TI-ULA)

## Overview
This document outlines the cryptographic and forensic verification flow for incident `CASE-MACHERET-1997-2026`.

## Flow Steps
1. **Detection:** Unauthorized gateway shift from `FinComBank S.A.` to `Moldindconbank S.A.` involving `25,210,256.15 MDL`.
2. **Card Conflict:** Card `5929_BLOCKED` vs `6089_ACTIVE` with auth token `MD-APPLEPAY-6089-20260403`.
3. **Serialization & Hashing:** Payload serialized to normalized JSON and hashed via SHA-256 (`d47b8e1f5c3a2990b6a84c71d9e2b4f510a8d6e3c1b7f9a2d8e4c5b6a7f8e9d0`).
4. **Freeze-Point Commit:** Public timestamp registered under node `0x4FA3-2026-04`.
