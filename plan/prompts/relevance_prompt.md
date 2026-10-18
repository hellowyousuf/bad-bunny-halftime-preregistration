# Relevance prompt (P0, first call) — plan_revision 1
Model: claude-opus-5-5 · default temperature · one segment per call · fresh context.

You will read one segment of closed-caption text from a US cable news program. Answer one question, in JSON only:
{"relevant": "yes|no"}

Is this segment about the Super Bowl halftime show, the selection of its headliner, reactions to that selection, or the rival show? Answer no for anything else, including the performer's music, tours or awards, other people named Benito, game coverage, advertising and schedules.

Segment:
{segment}
