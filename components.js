/* components.js — runtime injection for development (no build step required).
 *
 * On pages that ALREADY were rendered by build.py, this script is a no-op:
 * BEGIN/END markers contain the up-to-date HTML, so nothing needs to change.
 *
 * On pages that contain a `<!-- @include NAME -->` directive WITHOUT a
 * following BEGIN/END block (e.g. brand-new page being authored), this
 * script fetches the partial and inserts a basic rendered version.
 *
 * NOTE: variable substitution here is intentionally minimal. For full
 * fidelity (i18n, active nav, lang switches) always run `python build.py`
 * before publishing.
 */
(function () {
  'use strict';

  var INC_RE = /<!--\s*@include\s+([a-zA-Z0-9_-]+)([^->]*)-->/gi;
  // Detect site path prefix for fetching partials (root vs ru/ vs en/).
  var path = location.pathname.replace(/\\/g, '/');
  var prefix = '';
  if (/\/(ru|en)\//.test(path)) prefix = '../';

  function alreadyRendered(node, name) {
    var n = node.nextSibling;
    while (n && n.nodeType === 3 && !n.textContent.trim()) n = n.nextSibling;
    return n && n.nodeType === 8 && /^\s*BEGIN:\s*/.test(n.nodeValue) &&
           n.nodeValue.indexOf(name) !== -1;
  }

  function inject(name, params, comment) {
    fetch(prefix + '_partials/' + name + '.html', { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.text() : Promise.reject(r.status); })
      .then(function (tpl) {
        // Strip {{var}} -> empty (dev mode shows raw structure).
        var html = tpl.replace(/\{\{[^}]+\}\}/g, '');
        var begin = document.createComment(' BEGIN: ' + name + ' (dev injected) ');
        var end   = document.createComment(' END: ' + name + ' ');
        var tmp = document.createElement('div');
        tmp.innerHTML = html;
        var parent = comment.parentNode;
        parent.insertBefore(begin, comment.nextSibling);
        var ref = begin;
        while (tmp.firstChild) {
          parent.insertBefore(tmp.firstChild, ref.nextSibling);
          ref = ref.nextSibling;
        }
        parent.insertBefore(end, ref.nextSibling);
      })
      .catch(function (e) {
        console.warn('[components.js] failed to load partial', name, e);
      });
  }

  function walk() {
    var iter = document.createNodeIterator(document.body, NodeFilter.SHOW_COMMENT);
    var node;
    while ((node = iter.nextNode())) {
      var m = /^\s*@include\s+([a-zA-Z0-9_-]+)([^->]*)$/i.exec(node.nodeValue);
      if (!m) continue;
      var name = m[1].toLowerCase();
      if (alreadyRendered(node, name)) continue;
      inject(name, m[2] || '', node);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', walk);
  } else {
    walk();
  }
})();
