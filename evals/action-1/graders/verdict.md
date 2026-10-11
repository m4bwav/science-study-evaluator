---
type: regex
name: 'verdict from the five-level scale'
flags: i
pattern: 'Verdict[\s\S]{0,200}(Solid|Real but overhyped|Weak|Junk|Fabricated)'
target: last_message
---
