# Coder prompt, reworded (P0, pass 4) — plan_revision 1
Model: claude-opus-5-5 · default temperature · one segment per call · fresh context.

Below is a stretch of transcript from a cable news broadcast. It has already been judged relevant. Answer three questions about it. Reply with JSON only, using the exact labels given:
{"frame": "...", "belonging": "...", "spanish": "..."}

Question A (frame): Which single angle does this stretch put most weight on?
- national identity — what the nation is, its symbols and who represents it (anthem, flag, 'American' culture)
- immigration — migration, borders, deportation, legal status, ICE
- cultural representation — Latino or Puerto Rican culture, language, music and visibility on a national stage
- political controversy — the selection as an act of officials and institutions disputed in politics (statements by officials, boycotts, the rival show)
- generic partisan conflict — the event as a fight between political sides (left vs right, Democrats vs Republicans, media bias) tied to which side is right about the show
- no frame — the stretch is about the show but takes none of these angles
If two angles tie, prefer national identity, immigration or cultural representation over political controversy, and political controversy over generic partisan conflict. If no angle fits, answer no frame.

Question B (belonging): Do the speakers treat the singer, Puerto Ricans, Latinos or Spanish speakers as belonging to the nation?
- include — yes, as legitimately American
- exclude — no, or not fully, or as unfit to represent the country
- none — the stretch does not take a position
Only lines about who is or is not American count; putting a politician, party or voters on one side of a dispute does not. Answer for what the speakers assert, not for your own view; if mixed, answer for the position that takes most of the stretch.

Question C (spanish): If the stretch explicitly mentions the Spanish language or singing in Spanish, how is that judged?
- claim to belonging — Spanish is part of America or a fair claim to inclusion
- breach of belonging — Spanish is foreign, divisive or wrong for a national stage
- neither — mentioned without a judgment
- not named — the language is not mentioned (music or accent alone does not count)

Transcript:
{segment}
