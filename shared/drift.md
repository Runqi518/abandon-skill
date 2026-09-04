# Vocabulary Drift / 词表漂移

Teach mode stores user-specific drift outside the plugin so upgrades do not
overwrite it:

- `~/.claude/config/abandon-slop/teach-vocabulary.md`
- `~/.claude/config/abandon-slop/teach-allow-list.md`

## File Format

The vocabulary file uses the same `abandon:terms` block as reference files.
New entries default to `personal-NNNN|vagueness|medium|prior|<literal>` unless
the caller supplies category, severity, and provenance.

The allow-list uses an `abandon:allow` block with one literal per line. Empty
values and values containing a newline or `|` are rejected. UTF-8 is required.

## Commands

```bash
python3 shared/slop_count.py --teach-add "这个词也是 slop"
python3 shared/slop_count.py --allow-add "这个词别再标"
python3 shared/slop_count.py --teach-remove "旧词"
python3 shared/slop_count.py --allow-remove "旧豁免"
```

Mutation is atomic: write a sibling temporary file, flush and `fsync`, then
replace. A normalized key (`NFKC`, case-folded, collapsed whitespace) prevents
duplicates. Adding an allow entry removes the same literal from personal tells;
adding a tell removes it from the personal allow-list. Allow-list still wins if
the same entry exists in non-personal sources.

## Merge And Safety

The engine alone parses all bundled and personal vocabulary. Do not manually
interpret rule blocks in another script. Merge base, genre, and teach rules in
that order, then apply allow-list suppression. Never modify bundled profiles in
teach mode. Echo the action, normalized value, and destination path as JSON so
the user can confirm persistence.
