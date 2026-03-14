# Living PGP: Micro IA (Veto Policy) Specification

## Overview
The Micro IA is a lightweight, local-first artificial intelligence component responsible for the final "Safety Scan" of decrypted content. It acts as a fail-safe veto mechanism within the Living PGP protocol.

## 1. Local-Only Execution
- To maintain the integrity of the **Sneakernet** and **32Hybrid** transport layers, the Micro IA must execute entirely offline.
- No decrypted data or metadata should ever leave the local secure enclave during the scan.

## 2. Scanning Parameters (Veto Triggers)
The Micro IA is trained to identify and veto the following:
- **PII Leakage**: Unauthorized Names, SSNs, or physical addresses not explicitly whitelisted for the "Reveal" event.
- **Key Material**: Accidental inclusion of private keys, passphrases, or high-entropy strings that resemble authentication tokens.
- **Policy Mismatch**: Content that violates the specific "Directive" associated with the session key.

## 3. Veto Workflow
1. **Input**: Decrypted plaintext from the AES-512 engine.
2. **Analysis**: Rapid scan against locally stored weights/regex patterns.
3. **Decision**:
   - `PASS`: Content is released to the Elector.
   - `VETO`: Content is immediately scrubbed from memory; an audit event `POLICY_VETO_TRIGGERED` is logged in `audit.jsonl`.

## 4. Integration
- The Micro IA interface is defined in `core/policy.py`.
- Final authorization is a binary `AND` operation: `(Quorum Reached) AND (Micro IA Approval)`.