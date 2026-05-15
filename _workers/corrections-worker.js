/**
 * Cloudflare Worker — Klinik Psixiatriya term corrections endpoint (v2)
 * ────────────────────────────────────────────────────────────────────
 * Endpoints:
 *
 *   POST /                              ← Student submission
 *     body: {original, proposed, note?, url?, rowKind?}
 *     → appends entry {status:"pending", ...} to _corrections/PENDING.json
 *
 *   GET  /?action=list&admin_token=...  ← Admin list (for admin-page)
 *     → returns {ok:true, entries:[...]}
 *
 *   POST /  (with admin_token)          ← Admin action
 *     body: {action: "approve" | "reject", ts: "<entry ts>", admin_token}
 *     → updates that entry's status, commits back to GitHub
 *
 * Required secrets in Cloudflare Worker:
 *   GH_TOKEN     — GitHub fine-grained PAT (contents: read+write on ragimoff.org)
 *   ADMIN_TOKEN  — any random string (e.g. "kenan-2026-secret-abc123")
 *                  used by admin-corrections.html to authenticate.
 */

const REPO = "kentavr34/ragimoff.org";
const FILE_PATH = "_corrections/PENDING.json";
const BRANCH = "main";

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return cors(new Response(null, { status: 204 }));
    }

    const url = new URL(request.url);

    // ── GET ?action=list — admin lists entries
    if (request.method === "GET") {
      if (url.searchParams.get("action") === "list") {
        if (!validAdmin(url.searchParams.get("admin_token"), env)) {
          return cors(json({ ok: false, error: "unauthorized" }, 401));
        }
        try {
          const { entries } = await readEntries(env);
          return cors(json({ ok: true, entries }));
        } catch (e) {
          return cors(json({ ok: false, error: "read failed", detail: String(e).slice(0, 300) }, 502));
        }
      }
      return cors(json({ ok: false, error: "POST only (GET supports ?action=list)" }, 405));
    }

    if (request.method !== "POST") {
      return cors(json({ ok: false, error: "POST only" }, 405));
    }

    let payload;
    try { payload = await request.json(); }
    catch (e) { return cors(json({ ok: false, error: "bad json" }, 400)); }

    if (!env.GH_TOKEN) {
      return cors(json({ ok: false, error: "GH_TOKEN not configured" }, 500));
    }

    // ── POST action=approve|reject — admin mutates entry status
    if (payload.action === "approve" || payload.action === "reject") {
      if (!validAdmin(payload.admin_token, env)) {
        return cors(json({ ok: false, error: "unauthorized" }, 401));
      }
      if (!payload.ts) {
        return cors(json({ ok: false, error: "missing ts" }, 400));
      }
      try {
        const result = await mutateStatus(env, payload.ts,
          payload.action === "approve" ? "approved" : "rejected");
        return cors(json(result));
      } catch (e) {
        return cors(json({ ok: false, error: "mutate failed", detail: String(e).slice(0, 300) }, 502));
      }
    }

    // ── POST without action — student submission
    const original = String(payload.original || "").trim();
    const proposed = String(payload.proposed || "").trim();
    if (!original || !proposed) {
      return cors(json({ ok: false, error: "missing original/proposed" }, 400));
    }

    const entry = {
      ts: new Date().toISOString(),
      status: "pending",
      original: original.slice(0, 500),
      proposed: proposed.slice(0, 500),
      note: String(payload.note || "").slice(0, 2000),
      url: String(payload.url || "").slice(0, 500),
      rowKind: String(payload.rowKind || "").slice(0, 50),
      ua: String(payload.ua || "").slice(0, 200),
    };

    try {
      const { entries, sha } = await readEntries(env);
      entries.push(entry);
      await writeEntries(env, entries, sha,
        `term suggestion: ${original.slice(0, 60)}`);
      return cors(json({ ok: true, count: entries.length }));
    } catch (e) {
      return cors(json({ ok: false, error: "write failed", detail: String(e).slice(0, 300) }, 502));
    }
  },
};

// ── Helpers ──────────────────────────────────────────────────────────

function validAdmin(token, env) {
  if (!env.ADMIN_TOKEN) return false;
  return token && token === env.ADMIN_TOKEN;
}

async function readEntries(env) {
  const headers = {
    Authorization: `token ${env.GH_TOKEN}`,
    "User-Agent": "klinik-corrections-worker",
    Accept: "application/vnd.github.v3+json",
  };
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/contents/${FILE_PATH}?ref=${BRANCH}`,
    { headers }
  );
  if (res.status === 404) {
    return { entries: [], sha: null };
  }
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`GET failed ${res.status}: ${t.slice(0, 200)}`);
  }
  const fileData = await res.json();
  let entries = [];
  try {
    entries = JSON.parse(b64decode(fileData.content));
    if (!Array.isArray(entries)) entries = [];
  } catch (e) {
    entries = [];
  }
  return { entries, sha: fileData.sha };
}

async function writeEntries(env, entries, sha, message) {
  const headers = {
    Authorization: `token ${env.GH_TOKEN}`,
    "User-Agent": "klinik-corrections-worker",
    Accept: "application/vnd.github.v3+json",
    "Content-Type": "application/json",
  };
  const body = {
    message,
    content: b64encode(JSON.stringify(entries, null, 2) + "\n"),
    branch: BRANCH,
  };
  if (sha) body.sha = sha;
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/contents/${FILE_PATH}`,
    { method: "PUT", headers, body: JSON.stringify(body) }
  );
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`PUT failed ${res.status}: ${t.slice(0, 200)}`);
  }
}

async function mutateStatus(env, ts, newStatus) {
  const { entries, sha } = await readEntries(env);
  const idx = entries.findIndex(e => e.ts === ts);
  if (idx === -1) {
    return { ok: false, error: "entry not found", ts };
  }
  entries[idx].status = newStatus;
  entries[idx].reviewed_ts = new Date().toISOString();
  await writeEntries(env, entries, sha,
    `${newStatus} term suggestion: ${entries[idx].original.slice(0, 60)}`);
  return { ok: true, status: newStatus, count: entries.length };
}

function cors(res) {
  const h = new Headers(res.headers);
  h.set("Access-Control-Allow-Origin", "*");
  h.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  h.set("Access-Control-Allow-Headers", "Content-Type");
  return new Response(res.body, { status: res.status, headers: h });
}
function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
function b64encode(s) { return btoa(unescape(encodeURIComponent(s))); }
function b64decode(s) { return decodeURIComponent(escape(atob(s.replace(/\s+/g, "")))); }
