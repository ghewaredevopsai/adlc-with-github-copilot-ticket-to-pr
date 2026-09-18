# Walk a deck's key path the way the trainer does - press k from slide 1 - and
# assert it never lands on a data-after="lab" slide while the after-lab toggle is off.
# A spoiler reachable by k is the failure this catches; page counts and geometry do not.
import subprocess, json, re, sys, html, glob, os

probe = r"""
(function(){
  function press(key){document.dispatchEvent(new KeyboardEvent('keydown',{key:key,bubbles:true}));}
  function cur(){var s=[].slice.call(document.querySelectorAll('.slide'));
    for(var i=0;i<s.length;i++) if(s[i].classList.contains('active')) return i+1; return -1;}
  var all=[].slice.call(document.querySelectorAll('.slide'));
  var afterLab=[]; all.forEach(function(s,i){if(s.dataset.after)afterLab.push(i+1);});
  function walk(){var seen=[],guard=0,prev=cur();
    while(guard++<all.length+5){press('k');var c=cur();if(c===prev)break;seen.push(c);prev=c;}
    return seen;}
  press('Home'); var off=walk();
  press('Home'); press('l'); var on=walk();
  var d=document.createElement('div');d.id='PROBE_RESULT';
  d.textContent=JSON.stringify({afterLab:afterLab,off:off,on:on});
  document.body.appendChild(d);
})();
"""

fail = 0
for path in sorted(glob.glob(sys.argv[1]) if len(sys.argv) > 1 else glob.glob('presentation/module-*.html')):
    # the copy runs from /tmp: <base> points the deck's ../assets/ links back at the real folder
    base = '<head>\n<base href="file://%s/">' % os.path.dirname(os.path.abspath(path))
    inj = open(path).read().replace('<head>', base, 1).replace('</body>', '<script>' + probe + '</script></body>')
    open('/tmp/_keypath.html', 'w').write(inj)
    dom = subprocess.run(['google-chrome', '--headless', '--disable-gpu', '--no-sandbox',
                          '--virtual-time-budget=5000', '--dump-dom', 'file:///tmp/_keypath.html'],
                         capture_output=True, text=True).stdout
    m = re.search(r'id="PROBE_RESULT">(.*?)</div>', dom, re.S)
    name = path.split('/')[-1]
    if not m:
        print('%-42s PROBE FAILED' % name); fail = 1; continue
    r = json.loads(html.unescape(m.group(1)))
    leak = [s for s in r['off'] if s in r['afterLab']]
    held = [s for s in r['on'] if s not in r['off']]
    if leak:
        print('%-42s LEAK - k reaches after-lab slides %s' % (name, leak)); fail = 1
    else:
        print('%-42s clean - %2d taught live, %s held until L' % (name, len(r['off']), held or 'none'))

sys.exit(fail)
