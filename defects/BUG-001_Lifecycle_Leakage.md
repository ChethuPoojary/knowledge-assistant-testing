# BUG-001: In-Review Policy Surfaced

## Severity

Critical

## Priority

P1

## Description

The assistant returned the APAC meal allowance from document D-003, which is marked In Review and should not be surfaced.

## Steps to Reproduce

1. Set region to APAC.
2. Set role to Employee.
3. Ask: "What is my daily meal allowance when I travel?"

## Expected Result

The assistant should refuse because no approved APAC travel policy exists.

## Actual Result

The assistant returned JPY 8,000 and cited D-003.

## Evidence

Screenshot and API response should be attached in the `evidence/` folder.

