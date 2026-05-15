/**
 * Cloudflare Worker — Klinik Psixiatriya term corrections endpoint
 * ──────────────────────────────────────────────────────────────
 * What it does:
 *   1. Accepts POST {original, proposed, note, url, rowKind} from the site's
 *      Düzəlt widget.
 *   2. Reads _corrections/PENDING.json from the GitHub repo.
 *   3. Appends the new entry with status: "pending".
 *   4. Commits the updated file back to the repo via GitHub API.
 *
 * Setup (one-time, ~5 minutes):
 *   1. GitHub: github.com/settings/tokens → "Generate new token (fine-grained)"
 *      - Repository access: kentavr34/ragimoff.org only
 *      - Permissions → Repository permissions → Contents: Read and write
 *      - Generate → copy the token (github_pat_...)
 *   2. Cloudflare: dash.cloudflare.com → Workers & Pages → Create
 *      - Hello World template → Deploy
 *      - Click on your worker → Edit code
 *      - Paste THIS file's contents → Save and Deploy
 *      - Note the URL: https://<name>.<account>.workers.dev
 *   3. Cloudflare: Worker → Settings → Variables → Add Secret
 *      - Name: GH_TOKEN
 *      - Value: paste your GitHub token
 *      - Save → Deploy
 *   4. Send me the Worker URL — I'll plug it into duzelis.js.
 *
 * Approval workflow (after setup):
 *   • Student clicks ✎ Düzəlt → submits correction
 *   • Entry lands in _corrections/PENDING.json with status: "pending"
 *   • You open the file on GitHub web UI (1 click — Edit pencil)
 *   • Change "status": "pending" → "status": "approved" for entries you accept
 *   • Commit (1 click)
 *   • Next agent session — runs _term_sync.py — applies approved corrections
 *     across the entire site/book and marks them "status": "applied".
 */

const REPO = "kentavr34/ragimoff.org";
const FILE_PATH = "_corrections/PENDING.json";
const BRANCH = "main";

export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === "OPTIONS") {
      return cors(new Response(null, { status: 204 }));
    }
    if (request.method !== "POST") {
      return cors(json({ ok: false, error: "POST only" }, 405));
    }

    let payload;
    try {
      payload = await request.json();
    } catch (e) {
      return cors(json({ ok: false, error: "bad json" }, 400));
    }

    const original = String(payload.original || "").trim();
    const proposed = String(payload.proposed || "").trim();
    if (!original || !proposed) {
      return cors(json({ ok: false, error: "missing original/proposed" }, 400));
    }

    if (!env.GH_TOKEN) {
      return cors(json({ ok: false, error: "GH_TOKEN secret not configured" }, 500));
    }

    const entry = {
      ts:       new Date().toISOString(),
      status:   "pending",
      original: original.slice(0, 500),
      proposed: proposed.slice(0, 500),
      note:     String(payload.note || "").slice(0, 2000),
      url:      String(payload.url || "").slice(0, 500),
      rowKind:  String(payload.rowKind || "").slice(0, 50),
      ua:       String(payload.ua || "").slice(0, 200),
    };

    try {
      // 1. Read current PENDING.json (if exists)
      const ghHeaders = {
        Authorization: `token ${env.GH_TOKEN}`,
        "User-Agent": "klinik-corrections-worker",
        Accept: "application/vnd.github.v3+json",
      };
      const getRes = await fetch(
        `https://api.github.com/repos/${REPO}/contents/${FILE_PATH}?ref=${BRANCH}`,
        { headers: ghHeaders }
      );

      let existing = [];
      let sha = null;
      if (getRes.ok) {
        const fileData = await getRes.json();
        sha = fileData.sha;
        try {
          existing = JSON.parse(b64decode(fileData.content));
          if (!Array.isArray(existing)) existing = [];
        } catch (e) {
          existing = [];
        }
      } else if (getRes.status !== 404) {
        const t = await getRes.text();
        return cors(json({ ok: false, error: "github GET failed", status: getRes.status, detail: t.slice(0, 200) }, 502));
      }

      // 2. Append new entry
      existing.push(entry);

      // 3. Commit back
      const newContent = JSON.stringify(existing, null, 2) + "\n";
      const putBody = {
        message: `term suggestion: ${original.slice(0, 60)}`,
        content: b64encode(newContent),
        branch: BRANCH,
      };
      if (sha) putBody.sha = sha;

      const putRes = await fetch(
        `https://api.github.com/repos/${REPO}/contents/${FILE_PATH}`,
        {
          method: "PUT",
          headers: { ...ghHeaders, "Content-Type": "application/json" },
          body: JSON.stringify(putBody),
        }
      );

      if (!putRes.ok) {
        const t = await putRes.text();
        return cors(json({ ok: false, error: "github PUT failed", status: putRes.status, detail: t.slice(0, 300) }, 502));
      }

      return cors(json({ ok: true, count: existing.length }));
    } catch (e) {
      return cors(json({ ok: false, error: "exception", detail: String(e).slice(0, 300) }, 500));
    }
  },
};

function cors(res) {
  const h = new Headers(res.headers);
  h.set("Access-Control-Allow-Origin", "*");
  h.set("Access-Control-Allow-Methods", "POST, OPTIONS");
  h.set("Access-Control-Allow-Headers", "Content-Type");
  return new Response(res.body, { status: res.status, headers: h });
}
function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
function b64encode(s) {
  // unicode-safe base64 encode for the GitHub PUT body
  return btoa(unescape(encodeURIComponent(s)));
}
function b64decode(s) {
  // GitHub returns base64 with newlines — strip them, then decode unicode-safely
  return decodeURIComponent(escape(atob(s.replace(/\s+/g, ""))));
}
