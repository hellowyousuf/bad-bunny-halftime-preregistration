# Coder prompt (P0, passes 1–3) — plan_revision 1
Model: claude-opus-5-5 · default temperature · one segment per call · fresh context per pass.

You will read one segment of closed-caption text from a US cable news program. The segment has already been judged relevant. Code it on three variables and answer in JSON only:
{"frame": "...", "belonging": "...", "spanish": "..."}

1. frame — the one frame the segment stresses most. The one frame the segment stresses most: what it selects and makes salient about the halftime show.
- national identity: what the nation is, its symbols and who represents it (anthem, flag, 'American' culture)
- immigration: migration, borders, deportation, legal status, ICE
- cultural representation: Latino or Puerto Rican culture, language, music and visibility on a national stage
- political controversy: the selection as an act of officials and institutions disputed in politics (statements by officials, boycotts, the rival show)
- generic partisan conflict: the event as a fight between political sides (left vs right, Democrats vs Republicans, media bias) tied to which side is right about the show
- no frame: the segment is about the show but stresses none of the five frames
Rules: Code the frame that takes most of the segment's text; if two tie, prefer the frame tied to the event (national identity, immigration, cultural representation) over political controversy, and political controversy over generic partisan conflict.

2. belonging — Whether the segment draws a line around the nation that places the performer or his audience inside it (include) or outside it (exclude).
- include: the performer, Puerto Ricans, Latinos or Spanish speakers are treated as legitimately American
- exclude: they are treated as not, or not fully, American, or as not fit to represent the country
- none: no line is drawn
Rules: A line counts only when it is drawn around the nation (who is or is not American); placing a politician, a party or its voters on one side of a dispute is not a belonging line. Code the line the segment's speakers draw, not the coder's view. A line reported and rejected by the anchor is coded by what the anchor asserts. Mixed lines: code the line that takes most of the segment.

3. spanish — For segments that name the Spanish language or singing in Spanish: how the use of Spanish is judged.
- claim to belonging: Spanish is treated as part of America or as a legitimate claim to be included
- breach of belonging: Spanish is treated as foreign, divisive or improper for a national stage
- neither: Spanish is named without an evaluation
- not named: the segment does not name the language
Rules: Code only explicit mentions of the language; music or accent alone is not named.

Segment:
{segment}
