#!/usr/bin/env python3
"""
One-time script: replaces all Tiger Paw specific content with bracket tokens
across every .html file in this directory.
Run once from the repo root: python3 _tokenize.py
Delete this file after running.
"""
import os, re

html_files = sorted(f for f in os.listdir('.') if f.endswith('.html'))

# Order matters — longest/most-specific strings first to avoid partial matches
REPLACEMENTS = [
    # ── URLs ────────────────────────────────────────────────────────────────
    ('https://www.tigerpawma.com',                               '[SITE_URL]'),

    # ── GHL webhooks (single-quoted, inside onsubmit / JS var) ──────────────
    ("'https://services.leadconnectorhq.com/hooks/JnIWHyjZMYirq6yflQwH/webhook-trigger/691d545a-b5d7-49a3-95f3-1bce33ada3f0'",
     "'[TRIAL_WEBHOOK_URL]'"),
    ("'https://services.leadconnectorhq.com/hooks/JnIWHyjZMYirq6yflQwH/webhook-trigger/Ta6mCzoxZvwmZfhcW8aU'",
     "'[STARTER_KIT_WEBHOOK_URL]'"),
    ("'https://services.leadconnectorhq.com/hooks/JnIWHyjZMYirq6yflQwH/webhook-trigger/AoENcIMZUnMcBKYGpxoJ'",
     "'[QUIZ_WEBHOOK_URL]'"),
    # double-quoted variant (handleFinalForm JS var)
    ('"https://services.leadconnectorhq.com/hooks/JnIWHyjZMYirq6yflQwH/webhook-trigger/691d545a-b5d7-49a3-95f3-1bce33ada3f0"',
     '"[FINAL_CTA_WEBHOOK_URL]"'),
    # calendar redirect
    ("'https://api.leadconnectorhq.com/widget/group/0v7gsGRPNfa5WrQSFa7k'",
     "'[BOOKING_CALENDAR_URL]'"),
    # bare URL fallbacks (SWAP comments etc.)
    ('https://services.leadconnectorhq.com/hooks/JnIWHyjZMYirq6yflQwH/webhook-trigger/691d545a-b5d7-49a3-95f3-1bce33ada3f0',
     '[TRIAL_WEBHOOK_URL]'),
    ('https://services.leadconnectorhq.com/hooks/JnIWHyjZMYirq6yflQwH/webhook-trigger/Ta6mCzoxZvwmZfhcW8aU',
     '[STARTER_KIT_WEBHOOK_URL]'),
    ('https://services.leadconnectorhq.com/hooks/JnIWHyjZMYirq6yflQwH/webhook-trigger/AoENcIMZUnMcBKYGpxoJ',
     '[QUIZ_WEBHOOK_URL]'),
    ('https://api.leadconnectorhq.com/widget/group/0v7gsGRPNfa5WrQSFa7k',
     '[BOOKING_CALENDAR_URL]'),

    # ── Social links ─────────────────────────────────────────────────────────
    ('https://www.facebook.com/TigerPawMA/',    '[FACEBOOK_URL]'),
    ('https://www.instagram.com/tigerpaw_martial_arts/', '[INSTAGRAM_URL]'),

    # ── Program names — before generic "Taekwondo" sweep ────────────────────
    ('Teens &amp; Adult Taekwondo', '[PROGRAM 2 NAME]'),
    ('Teens & Adult Taekwondo',     '[PROGRAM 2 NAME]'),
    ('Kids Martial Arts',            '[PROGRAM 1 NAME]'),

    # ── Remaining martial art references ────────────────────────────────────
    ('Taekwondo and Tang Soo Do',   '[MARTIAL ART]'),
    ('Tang Soo Do',                 '[MARTIAL ART]'),
    ('Taekwondo',                   '[MARTIAL ART]'),

    # ── School identity ──────────────────────────────────────────────────────
    ('Tiger Paw Martial Arts',      '[SCHOOL NAME]'),
    ('Tiger Paw',                   '[SCHOOL NAME]'),     # catch any remaining bare refs

    # ── Contact ──────────────────────────────────────────────────────────────
    ('tel:(410) 248-0606',          'tel:[PHONE]'),       # href= variant first
    ('(410) 248-0606',              '[PHONE]'),
    ('mailto:mastershelley@tigerpawma.com', 'mailto:[EMAIL]'),
    ('mastershelley@tigerpawma.com','[EMAIL]'),
    ('117 Beacon Road, Victory Villa Shopping Center', '[ADDRESS LINE 1]'),
    ('Middle River, MD 21220',      '[CITY], [STATE] [ZIP]'),
    ('Middle River',                '[CITY]'),
    (' MD ',                        ' [STATE] '),          # " MD " (space-padded)

    # ── Hours ────────────────────────────────────────────────────────────────
    ('Mon–3:00pm–8:30pm \xb7 Sat 9:00am–12:00pm', '[HOURS]'),
    # ASCII fallback in case en-dash is stored differently
    ('Mon--Fri 3:00pm--8:30pm - Sat 9:00am--12:00pm', '[HOURS]'),

    # ── Images ───────────────────────────────────────────────────────────────
    ('images/logo.png',             '[LOGO_IMAGE]'),
    ('images/hero-image.webp',      '[HERO_IMAGE]'),
    ('images/kids-class-2.webp',    '[PROGRAM 1 PHOTO]'),
    ('images/adult-class.webp',     '[PROGRAM 2 PHOTO]'),
    ('images/coach-demo.webp',      '[INSTRUCTOR 1 PHOTO]'),
    ('images/younger-kids-class.webp', '[PROGRAM PHOTO]'),

    # ── Copyright year ───────────────────────────────────────────────────────
    ('© 2006 [SCHOOL NAME]',        '© [YEAR FOUNDED] [SCHOOL NAME]'),
]

changed = []
for filename in html_files:
    with open(filename, 'r', encoding='utf-8') as f:
        original = f.read()
    content = original
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    if content != original:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        n = sum(original.count(old) for old, _ in REPLACEMENTS)
        changed.append(filename)
        print(f'  ✓  {filename}')
    else:
        print(f'  –  {filename}  (no changes)')

print(f'\nDone. {len(changed)}/{len(html_files)} files updated.')
