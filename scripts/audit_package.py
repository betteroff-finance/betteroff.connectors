#!/usr/bin/env python3
"""Offline package checks: Codex rules for plugin.json extensions.com.openai from developers.openai.com/plugins/deploy/submission
and submission-errors (read 2026-09-29), skill frontmatter, version drift, endpoint consistency, secrets.
Usage: python3 scripts/audit_package.py [repo_root]. Exits 1 on errors; warnings are submission-only gaps."""
import json, re, struct, sys, pathlib

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
P = root / "plugins/betteroff"
errs, warns = [], []
def e(c, m): errs.append(f"{c}: {m}")
def w(c, m): warns.append(f"{c}: {m}")

CATS = {"Productivity","Creativity","Developer Tools","Business & Operations","Data & Analytics","Communication",
        "Education & Research","Security","Finance","Healthcare","Travel","Entertainment","Other"}
SEMVER = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?"
https = lambda u: isinstance(u, str) and re.fullmatch(r"https://[^\s@/]+(/\S*)?", u) is not None
oneline = lambda s: isinstance(s, str) and s.strip() and "\n" not in s

# Codex reads OpenAI settings from the root manifest's extensions.com.openai and ignores .codex-plugin/plugin.json.
pm = json.loads((P / "plugin.json").read_text())
m = {**pm, "interface": pm.get("extensions", {}).get("com.openai", {}).get("interface")}
if (P / ".codex-plugin").exists(): e("codex_overlay_shadowed", ".codex-plugin/plugin.json is ignored when plugin.json sets extensions.com.openai")
def validate_manifest(m):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", m.get("name", "")): e("plugin_name_format", m.get("name"))
    if not re.fullmatch(SEMVER, m.get("version", "")) or len(m["version"]) > 64: e("plugin_version_not_semver", m.get("version"))
    if not m.get("description") or len(m["description"]) > 1024: e("plugin_description", "missing or >1024")
    if not (m.get("author") or {}).get("name"): e("plugin_developer_missing", "author.name")
    if "homepage" in m and not https(m["homepage"]): e("plugin_homepage_format", m["homepage"])
    if m.get("skills") not in (None, "./skills/", "./skills"): e("plugin_skills_path_unsupported", m["skills"])
    if m.get("mcpServers") not in (None, "./.mcp.json"): e("plugin_mcp_path_unsupported", m["mcpServers"])
    if "$schema" not in m and (P / ".mcp.json").exists() and "mcpServers" not in m: w("undeclared_mcp_manifest_ignored", ".mcp.json")
    if "apps" in m or (m.get("extensions", {}).get("com.openai", {}).get("hooks")): e("submission", "apps/hooks block ZIP submission")

    i = m.get("interface")
    if not isinstance(i, dict): e("plugin_interface_wrong_type", "interface required for Codex format"); i = {}
    for k, lim in [("displayName", 30), ("shortDescription", 30), ("developerName", 80)]:
        if not oneline(i.get(k)) or len(i[k]) > lim: e(f"submission_{k}", f"required, one line, <= {lim}: {i.get(k)!r}")
    if not i.get("longDescription") or len(i["longDescription"]) > 4000: e("plugin_long_description", "required <= 4000")
    if i.get("longDescription") == m.get("description"): w("longDescription", "identical to description; should cover tasks, users, limits")
    if i.get("category") not in CATS: e("plugin_category_unknown", i.get("category"))
    caps = i.get("capabilities")
    if not isinstance(caps, list) or len(caps) > 20 or any(not oneline(c) or len(c) > 120 for c in caps): e("plugin_capabilities", caps)
    for k in ["websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"]:
        if not https(i.get(k)) or len(i[k]) > 1024: e(f"mcp_review_{k}", f"required HTTPS <= 1024 for MCP review: {i.get(k)!r}")
    dp = i.get("defaultPrompt", [])
    dp = [dp] if isinstance(dp, str) else dp
    norm = [" ".join(p.split()).casefold() for p in dp]
    if len(dp) > 3 or len(set(norm)) != len(norm) or any(not oneline(p) or len(p) > 128 or "@" in p for p in dp): e("plugin_default_prompt", dp)
    for k in ["brandColor", "brandColorDark"]:
        if k in i and not re.fullmatch(r"#[0-9A-Fa-f]{6}", i[k]): e(f"plugin_{k}_format", i[k])
    for k in ["composerIcon", "logo", "composerIconDark", "logoDark"]:
        v = i.get(k)
        if v is None:
            if k in ("composerIcon", "logo"): e(f"plugin_{k}_path_missing", "required for Codex")
            continue
        f = P / v
        if not v.startswith("./") or ".." in v: e("declared_asset_path_unsafe", v); continue
        if not f.is_file(): e("declared_asset_file_missing", v); continue
        b = f.read_bytes()
        if len(b) > 5 * 2**20: e("image_file_too_large", v)
        if b[:8] == b"\x89PNG\r\n\x1a\n":
            wd, ht = struct.unpack(">II", b[16:24])
            if wd != ht or wd < 48 or wd > 4096: e("raster_image_dimensions", f"{v} {wd}x{ht}")
    if i.get("screenshots"): w("screenshots_not_allowed", "only with custom MCP UI")

    x = m.get("extensions", {}).get("com.openai", {})
    r = x.get("review", {})
    tc = r.get("test_cases") or {}
    if len(tc.get("positive", [])) != 5 or len(tc.get("negative", [])) != 3: w("review.test_cases", "need exactly 5 positive + 3 negative before MCP review")
    for c in tc.get("positive", []):
        if not all(c.get(k) for k in ("description", "prompt", "tools_triggered", "expected_behavior")): e("review.test_cases.positive", c)
        if set(c) - {"description", "prompt", "tools_triggered", "expected_behavior", "file_attachment_urls", "expected_output_url"}: e("review.test_cases.positive_fields", c)
    for c in tc.get("negative", []):
        if not all(c.get(k) for k in ("description", "prompt")): e("review.test_cases.negative", c)
        if set(c) - {"description", "prompt", "file_attachment_urls", "expected_output_url"}: e("review.test_cases.negative_fields", c)
    if not r.get("demo_recording_url"): w("review.demo_recording_url", "required for MCP review")
    if not x.get("publication", {}).get("release_notes"): w("publication.release_notes", "required for MCP review")
    for bad in ("test_credentials", "reviewer_instructions"):
        if bad in json.dumps(x): e("zip_metadata_rejected", bad)

validate_manifest(m)

mc = json.loads((P / ".mcp.json").read_text())
s = mc.get("mcpServers")
if not isinstance(s, dict) or not s: e("mcp_servers_missing", ".mcp.json")
else:
    if len(s) != 1: w("mcp", "only one MCP server can be connected per plugin")
    for n, v in s.items():
        if not n.strip() or not isinstance(v, dict): e("mcp_server", n)
        elif not https(v.get("url")): e("mcp_url", f"{n}: public HTTPS required")

skills = [d for d in (P / "skills").iterdir()] if (P / "skills").is_dir() else []
names = set()
for d in skills:
    if d.is_symlink() or not d.is_dir(): w("skill_file_ignored", d.name); continue
    if d.name.startswith("."): e("skill_directory_hidden", d.name)
    t = (d / "SKILL.md").read_text(encoding="utf-8") if (d / "SKILL.md").is_file() else None
    if t is None: e("skill_manifest_missing", d.name); continue
    fm = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    if not fm: e("skill_frontmatter_missing", d.name); continue
    kv = dict(re.findall(r"^(\w+):\s*(.+)$", fm.group(1), re.M))
    if not kv.get("name"): e("skill_name_missing", d.name)
    if not kv.get("description") or len(kv["description"]) > 1024: e("skill_description", d.name)
    if not fm.group(2).strip(): e("skill_body_empty", d.name)
    if kv.get("name") != d.name: w("skill_dir_name", f"{d.name} != {kv.get('name')}")
    if len(f"{m['name']}:{kv.get('name')}") > 64: e("skill_identity_too_long", kv.get("name"))
    if kv.get("name") in names: e("skill_identity_duplicate", kv.get("name"))
    names.add(kv.get("name"))

mk = json.loads((root / ".agents/plugins/marketplace.json").read_text())
if not mk.get("name"): e("marketplace", "top-level name required")
if not (mk.get("interface") or {}).get("displayName"): w("marketplace", "interface.displayName sets marketplace title")
for pe in mk.get("plugins", []):
    src = pe.get("source")
    path = src if isinstance(src, str) else (src or {}).get("path", "")
    if (isinstance(src, str) or (src or {}).get("source") == "local") and (not path.startswith("./") or ".." in path or not (root / path).is_dir()):
        e("marketplace_source_path", path)
    pol = pe.get("policy") or {}
    if pol.get("installation") not in ("AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE") or not pol.get("authentication") or not pe.get("category"):
        e("marketplace_entry", f"{pe.get('name')}: policy.installation, policy.authentication, category required")
    if pe.get("name") != m["name"]: w("marketplace_entry_name", f"{pe.get('name')} != {m['name']}")

vers = {m["version"]}
cp = P / ".claude-plugin/plugin.json"
if cp.exists(): vers.add(json.loads(cp.read_text())["version"])
cm = root / ".claude-plugin/marketplace.json"
if cm.exists(): vers |= {p.get("version") for p in json.loads(cm.read_text())["plugins"] if p.get("version")}

url = next(iter(s.values()))["url"] if isinstance(s, dict) and s else None
if pm.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json": e("portable_plugin_schema", pm.get("$schema"))
vers.add(pm.get("version"))
gx = json.loads((root / "gemini-extension.json").read_text())
vers.add(gx.get("version"))
if "contextFileName" in gx and not (root / gx["contextFileName"]).is_file(): e("gemini_context_missing", gx["contextFileName"])
for skill in (P / "skills").glob("*/SKILL.md"):
    native = root / "skills" / skill.relative_to(P / "skills")
    if not native.is_file() or native.read_bytes() != skill.read_bytes():
        e("gemini_skill_drift", str(native))
for n, v in gx.get("mcpServers", {}).items():
    if v.get("httpUrl") != url: e("gemini_mcp_server", f"{n}: httpUrl must be {url}")
cur = P / ".cursor-plugin/plugin.json"
if cur.exists():
    cu = json.loads(cur.read_text())
    vers.add(cu.get("version"))
    if cu.get("name") != m["name"]: e("cursor_plugin_name", cu.get("name"))
    if not (P / cu.get("logo", "")).is_file(): e("cursor_logo_missing", cu.get("logo"))
for f in (cp, cur):
    if f.exists():
        fm = json.loads(f.read_text())
        for k in ("description", "author", "homepage", "repository", "license"):
            if fm.get(k) != m.get(k): e("metadata_drift", f"{f.relative_to(root)}: {k}")
if gx.get("description") != m.get("description"): e("metadata_drift", "gemini-extension.json: description")
gmk = root / ".grok-plugin/marketplace.json"
for f in (cm, root / ".cursor-plugin/marketplace.json", gmk):
    if f.exists():
        for pe in json.loads(f.read_text())["plugins"]:
            if pe.get("description") != m.get("description"): e("metadata_drift", f"{f.relative_to(root)}: {pe.get('name')} description")
# Registry metadata (server.json) can take its own version for a metadata-only republish.
if (root / "tools.json").exists(): vers.add(json.loads((root / "tools.json").read_text()).get("version"))
if len(vers) > 1: e("version_drift", sorted(map(str, vers)))
cmk = root / ".cursor-plugin/marketplace.json"
# Grok Build reads the same marketplace shape; it also accepts .claude-plugin/plugin.json manifests.
for label, mk_path in (("cursor", cmk), ("grok", gmk)):
    if not mk_path.exists(): continue
    if mk_path.stat().st_size > 10 * 2**20: e(f"{label}_marketplace_size", "over 10 MB")
    ck = json.loads(mk_path.read_text())
    if not re.fullmatch(r"[a-z0-9]([a-z0-9.-]*[a-z0-9])?", ck.get("name", "")): e(f"{label}_marketplace_name", ck.get("name"))
    if not (ck.get("owner") or {}).get("name"): e(f"{label}_marketplace_owner", "owner.name required")
    for pe in ck.get("plugins", []):
        src = pe.get("source")
        path = src if isinstance(src, str) else (src or {}).get("path", "")
        if not path.startswith("./") or ".." in path or not (root / path).is_dir(): e(f"{label}_marketplace_source_path", path)
        if pe.get("name") != m["name"]: e(f"{label}_marketplace_entry_name", pe.get("name"))
        if pe.get("description") != m.get("description"): e(f"{label}_marketplace_description", "differs from plugin description")
authors = {pm["author"]["name"], m["interface"]["developerName"]}
for f, key in [(P / ".claude-plugin/plugin.json", "author"), (P / ".cursor-plugin/plugin.json", "author"),
               (cm, "owner"), (cmk, "owner"), (gmk, "owner")]:
    if f.exists(): authors.add(json.loads(f.read_text())[key]["name"])
if len(authors) > 1: e("developer_name_drift", sorted(authors))
pmc = json.loads((P / "mcp.json").read_text())
if pmc.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json": e("portable_mcp_schema", pmc.get("$schema"))
if set(pmc.get("mcpServers", {})) != set(s or {}): e("portable_mcp_servers_missing", "portable and compatibility server names must match")
for n, v in pmc.get("mcpServers", {}).items():
    if v.get("type") != "streamable-http" or v.get("url") != url: e("portable_mcp_server", f"{n}: needs type streamable-http and url {url}")
agent_yaml = sorted((P / "skills").glob("*/agents/openai.yaml")) + sorted((root / "skills").glob("*/agents/openai.yaml"))
for f in agent_yaml:
    if f'url: "{url}"' not in f.read_text(): e("endpoint_mismatch", f"{f.relative_to(root)}: dependency url must be {url}")
endpoint_files = [root / "README.md", root / "tools.json", root / "integrations/directories/server.json",
                  P / "README.md", *sorted((root / "docs").rglob("*.md")), *agent_yaml]
for doc in endpoint_files:
    if not doc.is_file(): continue
    for u in re.findall(r"https://api\.[^\s`)\"]+/mcp", doc.read_text()):
        if u != url and "/.well-known/" not in u: e("endpoint_mismatch", f"{doc.relative_to(root)}: {u} != {url}")
SECRET = re.compile(r"sk_live_|sk-[A-Za-z0-9]{20}|client_secret|Bearer [A-Za-z0-9._-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY")
for f in root.rglob("*"):
    if ".git" in f.parts or ".private" in f.parts or "__pycache__" in f.parts or f.name == "todo-mcp.txt" or not f.is_file() or f.suffix in (".png", ".svg") or f.parent.name == "scripts": continue
    if SECRET.search(f.read_text(errors="ignore")): e("secret_like_string", str(f.relative_to(root)))

print("\n".join(["ERRORS:"] + errs + ["WARNINGS:"] + warns))
sys.exit(1 if errs else 0)
