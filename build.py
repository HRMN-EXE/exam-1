#!/usr/bin/env python3
"""Combine all code*.html mobile screens into one seamless SPA (index.html)."""
import re, glob, json

ORDER = ['code1', 'code2', 'code3', 'code4', 'code5', 'code8', 'code9', 'code6',
         'code10', 'code11', 'code11a', 'code11c', 'code12']

META = {
    'code1':  ('student-login',      'Student Login',        'login'),
    'code2':  ('student-profile',    'Candidate Profile',    'badge'),
    'code3':  ('student-exams',      'Exam List',            'list_alt'),
    'code4':  ('student-rules',      'Rules & Confirmation', 'rule'),
    'code5':  ('student-exam',       'Active Exam Session',  'edit_note'),
    'code8':  ('student-disconnect', 'Disconnection Alert',  'wifi_off'),
    'code9':  ('student-timeup',     'Time Expired',         'hourglass_bottom'),
    'code6':  ('student-done',       'Submission Verified',  'verified'),
    'code10': ('faculty-login',      'Faculty Login',        'lock'),
    'code11': ('faculty-new-exam',   'Create New Exam',      'add_circle'),
    'code11a':('faculty-basics',     'Exam Basics',          'description'),
    'code11c':('faculty-proctor',    'Proctor & Security',   'shield'),
    'code12': ('faculty-grading',    'Grading & Results',    'grading'),
}

# flow edges: (from, to, label) – rendered as a floating "next" pill
FLOW = [
    ('student-login', 'student-profile', 'Continue'),
    ('student-profile', 'student-exams', 'Save & Continue'),
    ('student-exams', 'student-rules', 'Take Exam'),
    ('student-rules', 'student-exam', 'Start Exam'),
    ('student-exam', 'student-disconnect', 'Demo: Disconnect'),
    ('student-disconnect', 'student-timeup', 'Demo: Time Up'),
    ('student-timeup', 'student-done', 'Demo: Submitted'),
    ('student-done', 'student-exams', 'Back to Exams'),
    ('student-login', 'faculty-login', 'Faculty?'),
    ('faculty-login', 'faculty-new-exam', 'Dashboard'),
    ('faculty-new-exam', 'faculty-basics', 'Next: Questions'),
    ('faculty-basics', 'faculty-proctor', 'Next: Proctor'),
    ('faculty-proctor', 'faculty-grading', 'Finish & View Grading'),
]

def load(key):
    return open(f'/workspace/{key}.html').read()

def head_parts(s):
    """Return (font_link_tags, style_blocks, tailwind_config_js)."""
    head = s.split('<body', 1)[0]
    fonts = re.findall(r'<link[^>]+fonts\.googleapis\.com[^>]*>', head)
    styles = re.findall(r'<style[^>]*>(.*?)</style>', head, re.S)
    cfgs = []
    for m in re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>', head, re.S):
        js = m.group(1)
        if 'tailwind.config' in js:
            cfgs.append(js)
    return fonts, styles, cfgs

def body_parts(s):
    body = re.search(r'<body[^>]*>(.*)</body>', s, re.S).group(1)
    # separate scripts/styles from markup (placeholder them so chunk spans include
    # any scripts that live inside the main container)
    stash = []
    def keep(m):
        stash.append(m.group(0))
        return f'\x00S{len(stash)-1}\x00'
    masked = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', keep, body, flags=re.S)
    # top-level chunks via depth scan over container tags
    tokens = list(re.finditer(r'<(/?)(div|main|section|nav|header|form)\b[^>]*?>', masked))
    depth = 0
    spans = []
    start = None
    for m in tokens:
        closing, tag = m.group(1), m.group(2)
        if not closing:
            if depth == 0:
                start = m.start()
            if not m.group(0).endswith('/>'):
                depth += 1
        else:
            depth -= 1
            if depth == 0 and start is not None:
                spans.append((start, m.end()))
                start = None
    def unmask(t):
        return re.sub(r'\x00S(\d+)\x00', lambda mm: stash[int(mm.group(1))], t)
    chunks = [unmask(masked[a:b]) for a, b in spans]
    scripts = re.findall(r'<script\b.*?</script>', body, re.S)
    return chunks, scripts

def prefix_scope(css, scope):
    out = []
    i, n = 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j == -1:
            break
        prelude = css[i:j]
        k = j + 1; d = 1
        while k < n and d:
            if css[k] == '{': d += 1
            elif css[k] == '}': d -= 1
            k += 1
        block = css[j+1:k-1]
        if '@media' in prelude or prelude.lstrip().startswith('@'):
            at = prelude.strip().split()[0]
            inner = prefix_scope(block, scope)
            out.append(f'{prelude.strip()} {{ {inner} }}')
        else:
            sels = []
            for sel in prelude.split(','):
                sel = sel.strip()
                if not sel: continue
                if sel.startswith('html'):
                    s = sel.replace('html', scope, 1)
                elif sel.startswith('body'):
                    s = sel.replace('body', scope, 1)
                else:
                    s = f'{scope} {sel}' if sel else scope
                sels.append(s)
            out.append(', '.join(sels) + ' {' + block + '}')
        i = k
    return '\n'.join(out)

def merge_tw_configs(cfg_list):
    """Evaluate every original tailwind.config object (via JSON5-ish parsing) and
    deep-merge them into a single config."""
    import json as _json
    merged = {}

    def deep_merge(a, b):
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(a.get(k), dict):
                deep_merge(a[k], v)
            else:
                a[k] = v
        return a

    for js in cfg_list:
        # strip JS comments
        js = re.sub(r'//[^\n]*', '', js)
        start = js.find('{')
        if start == -1: continue
        depth = 0
        for i in range(start, len(js)):
            if js[i] == '{': depth += 1
            elif js[i] == '}':
                depth -= 1
                if depth == 0:
                    obj_src = js[start:i+1]
                    break
        else:
            continue
        # convert JS object literal to JSON: quote bare keys, single->double quotes, drop trailing commas
        s = re.sub(r"'", '"', obj_src)
        s = re.sub(r'(?<![\w"\'])([A-Za-z_$][\w$]*)\s*:', r'"\1":', s)
        s = re.sub(r',(\s*[}\]])', r'\1', s)
        try:
            obj = _json.loads(s)
        except Exception:
            # last resort: extract flat color map only
            obj = {'theme': {'extend': {'colors': {m.group(1): m.group(2)
                    for m in re.finditer(r'"([a-zA-Z0-9\-]+)":\s*"((?:[^"\\]|\\.)*)"', s)}}}}
        deep_merge(merged, obj)
    # ensure font family defaults
    ext = merged.setdefault('theme', {}).setdefault('extend', {})
    ext.setdefault('fontFamily', {'sans': ['"Plus Jakarta Sans"', 'sans-serif'],
                                  'serif': ['"Newsreader"', 'serif']})
    body = _json.dumps({'darkMode': 'class', 'theme': merged.get('theme', {})}, indent=2)
    return 'tailwind.config = ' + body + ';'

NAV_LABEL = {'student-login':'Login','student-profile':'Profile','student-exams':'Exams',
             'student-rules':'Rules','student-exam':'Exam','student-disconnect':'Offline',
             'student-timeup':'Time Up','student-done':'Receipt','faculty-login':'F. Login',
             'faculty-new-exam':'New Exam','faculty-basics':'Basics','faculty-proctor':'Security',
             'faculty-grading':'Grading'}

screens_html = []
all_css = []
head_fonts = set()
tw_cfgs = []

for key in ORDER:
    nav_id, title, icon = META[key]
    src = load(key)
    fonts, styles, cfgs = head_parts(src)
    head_fonts.update(fonts)
    tw_cfgs.extend(cfgs)
    chunks, scripts = body_parts(src)

    content = []
    for ch in chunks:
        plain = re.sub(r'<script\b.*?</script>', '', ch, flags=re.S)
        plain = re.sub(r'<[^>]+>', '', plain).strip()
        cls_m = re.search(r'class="([^"]*)"', ch)
        classes = cls_m.group(1) if cls_m else ''
        if not plain or 'snapdom' in classes or 'fixed inset-0' in classes:
            continue  # empty helpers / sandboxes / decorative overlays
        # keep only the first meaningful container per screen
        if content:
            break
        # neutralise viewport-fixed positioning so it lives inside the phone frame
        ch2 = re.sub(r'\bfixed\b', 'sticky', ch)
        ch2 = re.sub(r'\bmin-h-screen\b', 'min-h-full', ch2)
        ch2 = re.sub(r'\bh-screen\b', 'h-full', ch2)
        content.append(ch2)

    scope = f'#screen-{nav_id}'
    keep_idx = 0 if key in ('code1', 'code2') else None
    for idx, st in enumerate(styles):
        if st.strip().startswith('@layer base'):
            continue  # shared global base added once below
        scoped = prefix_scope(st, scope)
        all_css.append(f'/* ---- {key} ---- */\n{scoped}')

    inner = '\n'.join(content)
    # collect body scripts that were NOT already inside the kept chunk
    kept_html = re.sub(r'<script\b.*?</script>', '', inner, flags=re.S)
    leftover_scripts = []
    for sc in scripts:
        core = re.search(r'>(.*)</script>', sc, re.S)
        snippet = (core.group(1).strip()[:80] if core else '')
        if 'snapdom' in sc.lower():
            continue
        if snippet and snippet not in kept_html and snippet[:40] not in inner:
            leftover_scripts.append(sc)
    screens_html.append(
        f'<!-- ===== {key}: {title} ===== -->\n'
        f'<section id="screen-{nav_id}" class="screen" data-title="{title}" data-icon="{icon}" aria-label="{title}">\n'
        f'<div class="screen-scroll">{inner}</div>\n'
        + '\n'.join(leftover_scripts) + '\n</section>')

# ---------- assemble ----------
fonts_block = '\n'.join(sorted(head_fonts))
css_block = '\n'.join(all_css)
nav_btns = ''.join(
    f'<button class="nav-btn" data-nav="{nid}" type="button"><span class="material-symbols-outlined">{META[k][2]}</span>{NAV_LABEL[nid]}</button>'
    for k, nid, _, _ in [(k, META[k][0], META[k][1], META[k][2]) for k in ORDER])

flow_map = {}
for a, b, label in FLOW:
    flow_map.setdefault(a, []).append((b, label))
flow_json = {a: [{'to': b, 'label': lb} for b, lb in v] for a, v in flow_map.items()}

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" name="viewport">
<meta name="theme-color" content="#fff8f5">
<title>ExamPortal — Student &amp; Faculty Mobile App</title>
{fonts_block}
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script>
{merge_tw_configs(tw_cfgs)}
</script>
<style>
@layer base {{
  html, body {{ width:100%; height:100%; margin:0; padding:0; overscroll-behavior:none; }}
}}
* {{ box-sizing:border-box; }}
::-webkit-scrollbar {{ display:none; }}
html, body {{
  height:100%;
  background:#171412;
  font-family:'Plus Jakarta Sans', system-ui, sans-serif;
  color:#1E1B18;
  overflow:hidden;
}}
#app {{
  position:relative;
  width:100%;
  max-width:430px;
  height:100dvh;
  margin:0 auto;
  background:#fff8f5;
  overflow:hidden;
}}
@media (min-width:480px) {{
  body {{ display:flex; align-items:center; justify-content:center; }}
  #app {{ height:min(92dvh, 932px); border-radius:44px; border:8px solid #2b2724;
         box-shadow:0 30px 80px rgba(0,0,0,.55); }}
}}
/* app bar */
#appbar {{
  position:sticky; top:0; z-index:80;
  display:flex; align-items:center; gap:10px;
  padding:calc(env(safe-area-inset-top,0px) + 10px) 14px 10px;
  background:rgba(255,248,245,.85); backdrop-filter:blur(16px);
  border-bottom:1px solid rgba(30,27,24,.06);
}}
#appbar .ab-title {{ font-weight:800; font-size:16px; letter-spacing:-.02em; flex:1; min-width:0;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
#appbar button {{ border:0; background:transparent; color:inherit; cursor:pointer;
  width:38px; height:38px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}
#appbar button:active {{ background:rgba(30,27,24,.08); }}
#brand-chip {{ font-size:11px; font-weight:800; letter-spacing:.08em; padding:4px 10px; border-radius:999px;
  background:#1E1B18; color:#fff8f5; }}
/* screens */
.screen {{ display:none; position:absolute; inset:0; top:0; }}
.screen.active {{ display:block; animation:fadein .28s ease; }}
@keyframes fadein {{ from {{ opacity:0; transform:translateY(6px); }} to {{ opacity:1; transform:none; }} }}
.screen-scroll {{ height:100%; overflow-y:auto; -webkit-overflow-scrolling:touch; padding-top:58px;
  scrollbar-width:none; }}
.screen-scroll > *:first-child {{ margin-top:0 !important; }}
/* bottom tab bar */
#tabbar {{
  position:absolute; left:0; right:0; bottom:0; z-index:90;
  display:flex; justify-content:space-around; align-items:stretch;
  padding:6px 6px calc(env(safe-area-inset-bottom,0px) + 6px);
  background:rgba(255,252,250,.92); backdrop-filter:blur(18px);
  border-top:1px solid rgba(30,27,24,.07);
  box-shadow:0 -6px 24px rgba(0,0,0,.06);
}}
.nav-btn {{ flex:1; border:0; background:transparent; cursor:pointer; display:flex; flex-direction:column;
  align-items:center; gap:2px; padding:6px 2px; border-radius:14px; color:#8a817b;
  font-family:inherit; font-size:10px; font-weight:700; letter-spacing:.01em; }}
.nav-btn .material-symbols-outlined {{ font-size:22px; }}
.nav-btn.active {{ color:#fff8f5; background:#1E1B18; }}
/* next-flow pill */
#next-pill {{
  position:absolute; right:14px; bottom:86px; z-index:95;
  display:none; gap:8px; flex-direction:column; align-items:flex-end;
}}
#next-pill.show {{ display:flex; }}
#next-pill button {{
  border:0; cursor:pointer; font-family:inherit; font-weight:800; font-size:13px;
  padding:12px 18px; border-radius:999px; color:#fff8f5; background:#6750A4;
  box-shadow:0 8px 22px rgba(103,80,164,.45); display:flex; align-items:center; gap:6px;
}}
#next-pill button.alt {{ background:#1E1B18; box-shadow:0 8px 22px rgba(0,0,0,.35); }}
#next-pill button .material-symbols-outlined {{ font-size:18px; }}
{css_block}
</style>
</head>
<body>
<div id="app">
  <header id="appbar">
    <button id="btn-back" type="button" aria-label="Back"><span class="material-symbols-outlined">arrow_back</span></button>
    <span id="brand-chip">EXAMPORTAL</span>
    <span class="ab-title" id="ab-title">Student Login</span>
    <button id="btn-menu" type="button" aria-label="All screens"><span class="material-symbols-outlined">apps</span></button>
  </header>

  {''.join(screens_html)}

  <div id="next-pill"></div>

  <nav id="tabbar" aria-label="Primary">
    <button class="nav-btn" data-nav="__drawer_home" type="button" onclick="showScreen('student-login')">
      <span class="material-symbols-outlined">school</span>Student</button>
    <button class="nav-btn" data-nav="student-exams" type="button"><span class="material-symbols-outlined">list_alt</span>Exams</button>
    <button class="nav-btn" data-nav="student-exam" type="button"><span class="material-symbols-outlined">edit_note</span>Exam</button>
    <button class="nav-btn" data-nav="faculty-login" type="button"><span class="material-symbols-outlined">lock</span>Faculty</button>
    <button class="nav-btn" data-nav="faculty-grading" type="button"><span class="material-symbols-outlined">grading</span>Results</button>
  </nav>

  <!-- screen drawer -->
  <div id="drawer" style="display:none;position:absolute;inset:0;z-index:120;">
    <div onclick="closeDrawer()" style="position:absolute;inset:0;background:rgba(23,20,18,.5);"></div>
    <div style="position:absolute;left:0;right:0;bottom:0;max-height:75%;overflow:auto;background:#fffcfa;
                border-radius:28px 28px 0 0;padding:18px 16px calc(env(safe-area-inset-bottom,0px) + 18px);">
      <div style="font-weight:800;font-size:15px;margin-bottom:4px;">All screens</div>
      <div style="font-size:12px;color:#8a817b;margin-bottom:14px;">Every original page, combined seamlessly.</div>
      <div id="drawer-list" style="display:flex;flex-direction:column;gap:8px;"></div>
    </div>
  </div>
</div>

<script>
const FLOW = {json.dumps(flow_json)};
const ORDER = {json.dumps([META[k][0] for k in ORDER])};
const TITLES = {json.dumps({META[k][0]: META[k][1] for k in ORDER})};
const ICONS = {json.dumps({META[k][0]: META[k][2] for k in ORDER})};
let historyStack = [];
let current = null;

function showScreen(id, pushHistory) {{
  if (pushHistory !== false && current && current !== id) historyStack.push(current);
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  const el = document.getElementById('screen-' + id);
  if (!el) return;
  el.classList.add('active');
  el.querySelector('.screen-scroll').scrollTop = 0;
  current = id;
  document.getElementById('ab-title').textContent = TITLES[id] || '';
  document.getElementById('brand-chip').textContent =
      id.indexOf('faculty') === 0 ? 'FACULTY' : 'STUDENT';
  // tab highlight
  const tabs = {{'student-login':'__drawer_home','student-profile':'__drawer_home',
    'student-exams':'student-exams','student-rules':'student-exams',
    'student-exam':'student-exam','student-disconnect':'student-exam','student-timeup':'student-exam',
    'student-done':'student-exam','faculty-login':'faculty-login','faculty-new-exam':'faculty-login',
    'faculty-basics':'faculty-login','faculty-proctor':'faculty-login','faculty-grading':'faculty-grading'}};
  document.querySelectorAll('#tabbar .nav-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.nav === tabs[id]));
  // next pill(s)
  const pill = document.getElementById('next-pill');
  pill.innerHTML = '';
  (FLOW[id] || []).forEach((f, i) => {{
    const b = document.createElement('button');
    if (i > 0) b.className = 'alt';
    b.type = 'button';
    b.innerHTML = f.label + '<span class="material-symbols-outlined">arrow_forward</span>';
    b.onclick = () => showScreen(f.to);
    pill.appendChild(b);
  }});
  pill.classList.toggle('show', !!(FLOW[id] || []).length);
  closeDrawer();
  try {{ history.replaceState(null, '', '#' + id); }} catch (e) {{}}
}}

function goBack() {{
  if (historyStack.length) showScreen(historyStack.pop(), false);
  else showScreen('student-login', false);
}}
document.getElementById('btn-back').onclick = goBack;

function openDrawer() {{
  const list = document.getElementById('drawer-list');
  list.innerHTML = '';
  ORDER.forEach(id => {{
    const b = document.createElement('button');
    b.type = 'button';
    b.style.cssText = 'display:flex;align-items:center;gap:12px;width:100%;text-align:left;' +
      'border:1px solid rgba(30,27,24,.08);background:#fff;border-radius:16px;padding:12px 14px;' +
      'font-family:inherit;font-weight:700;font-size:14px;color:#1E1B18;cursor:pointer;';
    b.innerHTML = '<span class="material-symbols-outlined" style="color:#6750A4">' + ICONS[id] +
      '</span>' + TITLES[id];
    b.onclick = () => showScreen(id);
    list.appendChild(b);
  }});
  document.getElementById('drawer').style.display = 'block';
}}
function closeDrawer() {{ document.getElementById('drawer').style.display = 'none'; }}
document.getElementById('btn-menu').onclick = openDrawer;

// tab bar wiring
document.querySelectorAll('#tabbar .nav-btn').forEach(b => {{
  const t = b.dataset.nav;
  if (t !== '__drawer_home') b.onclick = () => showScreen(t);
}});

// init from hash
const start = (location.hash || '').slice(1);
showScreen(ORDER.includes(start) ? start : 'student-login', false);
</script>
</body>
</html>
"""

open('/workspace/index.html', 'w').write(html)
print('written', len(html), 'bytes')
