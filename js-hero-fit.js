/* Page Hero — binary-search font-fitting.
   Все страницы с .page-hero-x подключают этот скрипт. */
(function(){
  function fitOne(){
    var heroes = document.querySelectorAll('.page-hero-x');
    heroes.forEach(function(hero){
      var h1 = hero.querySelector('.ph-h1');
      var lead = hero.querySelector('.ph-sub');
      var sw = hero.querySelector('.ph-search-wrap');
      var subDesk = hero.querySelectorAll('.ph-sub-desk');
      var subMob = hero.querySelectorAll('.ph-sub-mob');
      if (!h1) return;

      h1.style.cssText = '';
      [].slice.call(subDesk).concat([].slice.call(subMob)).forEach(function(s){ s.style.cssText = ''; });

      var isDesktop = window.innerWidth > 768;
      var dt = sw ? Math.round(sw.getBoundingClientRect().width) : 620;
      if (!dt) dt = 620;

      if (isDesktop) {
        h1.style.display = 'inline-block';
        h1.style.whiteSpace = 'nowrap';
        var lo = 8, hi = 80;
        for (var k=0;k<30;k++){
          var m = (lo+hi)/2;
          h1.style.fontSize = m+'px';
          if (h1.getBoundingClientRect().width < dt) lo = m;
          else hi = m;
        }
        h1.style.fontSize = Math.floor(lo)+'px';
        h1.style.display = '';
        h1.style.whiteSpace = '';

        if (lead) { lead.style.width = dt+'px'; lead.style.maxWidth = 'none'; }
        subDesk.forEach(function(line){
          line.style.display = 'inline';
          line.style.whiteSpace = 'nowrap';
          var lo2=8, hi2=40;
          for (var j=0;j<30;j++){
            var m2 = (lo2+hi2)/2;
            line.style.fontSize = m2+'px';
            if (line.getBoundingClientRect().width < dt) lo2 = m2;
            else hi2 = m2;
          }
          line.style.fontSize = Math.floor(lo2)+'px';
          line.style.display = 'block';
          line.style.whiteSpace = '';
        });
      } else {
        var inner = hero.querySelector('.page-hero-x-inner');
        var target = inner ? inner.getBoundingClientRect().width - 40 : window.innerWidth - 60;
        if (!target) return;

        h1.style.display = 'inline-block';
        h1.style.whiteSpace = 'nowrap';
        var loM=10, hiM=60;
        for (var i=0;i<30;i++){
          var mM = (loM+hiM)/2;
          h1.style.fontSize = mM+'px';
          if (h1.getBoundingClientRect().width < target) loM = mM;
          else hiM = mM;
        }
        h1.style.fontSize = Math.floor(loM)+'px';
        h1.style.display = '';
        h1.style.whiteSpace = '';

        subMob.forEach(function(line){
          line.style.display = 'inline';
          line.style.whiteSpace = 'nowrap';
          var lo3=8, hi3=30;
          for (var jj=0;jj<30;jj++){
            var m3 = (lo3+hi3)/2;
            line.style.fontSize = m3+'px';
            if (line.getBoundingClientRect().width < target) lo3 = m3;
            else hi3 = m3;
          }
          line.style.fontSize = Math.floor(lo3)+'px';
          line.style.display = 'block';
          line.style.whiteSpace = '';
        });
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fitOne);
  } else { fitOne(); }
  window.addEventListener('resize', fitOne, {passive: true});
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(fitOne);
  }
})();
