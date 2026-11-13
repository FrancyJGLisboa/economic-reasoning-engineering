# Operations profile

Use this profile for process execution, delivery feasibility, capacity, dependencies, and failure controls.
Keep the shared evidence workflow and portable package contract.
Do not require an economic claim before accepting an operational episode.

## Episode selection

Identify the process objective, current state, completion condition, and required deadline.
Extract stages, dependencies, queues, resources, capacities, handoffs, and known failure modes when supported.
Separate a source's example from an observed shipment or measured service level.
Retain financial constraints when they affect process execution. Do not infer insolvency from a margin scenario.

## Method operations

1. Locate the item within the process. Separate completed work from remaining work.
2. Identify sequential dependencies and parallel activities. Do not add overlapping durations.
3. Check quantities, capacity units, operating calendars, and queue assumptions before calculating duration.
4. Compare remaining duration with the deadline. Identify missing evidence and alternative routes or inventory positions.
5. Define observable control points, expected outputs, failure tests, and abstention conditions.

Distinguish processing time, waiting time, transit time, and buffer time.
A charter tender and production planning may overlap. Do not assume overlap without evidence.
Do not count a buffer twice or treat a best-case estimate as a delivery guarantee.
Check arithmetic independently. Preserve the source's number and label any investigator correction.
Do not manufacture a consistent timeline when the source changes dates, quantities, or assumptions.

## Expected outputs

Write named results in `expected_outputs`, with units and interpretation when relevant.
Useful results include a remaining-stage map, a conditional delivery range, a capacity test, or a delivery-evidence checklist.
Mark reconstructed dependencies, proposed controls, and new calculations as investigator additions.
Unknown durations remain unknown. A useful qualitative result can still identify the evidence required for a decision.

## Failure checks and abstention

Test double-counted duration, incompatible capacity units, assumed resource availability, and forecast dates treated as commitments.
Abstain from a delivery guarantee when current stage, dependencies, or material durations remain unknown.
Abstain from a bottleneck claim when comparable stage capacities or demand rates are missing.
A transfer probe must change an operational condition, such as current location, inventory, queue, or deadline.
A hypothetical probe does not verify performance on real operations.
