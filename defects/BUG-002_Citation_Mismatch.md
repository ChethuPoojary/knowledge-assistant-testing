# BUG-002: Citation Does Not Support Claim

## Severity

High

## Priority

P1

## Description

The assistant stated "Remote work is allowed 1 day per week" while citing D-004. However, D-004 states 3 days per week; 1 day per week belongs to retired document D-005.

## Steps to Reproduce

1. Set any valid region and role.
2. Ask: "How many days a week can I work remotely?"

## Expected Result

The answer should state 3 days per week and cite D-004.

## Actual Result

The answer stated 1 day per week while citing D-004.

