"""Password-lock the proposal for public hosting.
Reads index.plain.html (the full self-contained page) and writes index.html as an
AES-GCM encrypted page that only decrypts client-side with the correct passphrase.
Usage: python lock.py "your passphrase"
The published index.html contains only ciphertext + a password screen — no readable content.
"""
import base64, os, sys, hashlib, secrets, json
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except Exception:
    print("Need 'cryptography'. Install: python -m pip install cryptography"); raise SystemExit(1)

root = os.path.dirname(os.path.abspath(__file__))
passphrase = sys.argv[1] if len(sys.argv) > 1 else None
if not passphrase:
    print("Pass a passphrase: python lock.py \"...\""); raise SystemExit(1)

src = open(os.path.join(root, "index.plain.html"), encoding="utf-8").read()
salt = secrets.token_bytes(16)
iv = secrets.token_bytes(12)
iters = 310000
key = hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, iters, 32)
ct = AESGCM(key).encrypt(iv, src.encode("utf-8"), None)  # tag appended
payload = {"s": base64.b64encode(salt).decode(), "i": base64.b64encode(iv).decode(),
           "c": base64.b64encode(ct).decode(), "n": iters}

WRAP = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow, noarchive, noimageindex, nosnippet">
<meta name="googlebot" content="noindex, nofollow">
<meta name="description" content="Private proposal — by invitation only.">
<title>Private proposal</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{min-height:100vh;display:flex;align-items:center;justify-content:center;background:#08090C;color:#EEF2F6;
font-family:'Segoe UI',system-ui,-apple-system,sans-serif;padding:24px}
.card{width:100%;max-width:400px;text-align:center}
.mark{font-family:'Arial Narrow',sans-serif;font-weight:800;font-size:22px;letter-spacing:.04em;color:#EEF2F6;
border:1.5px solid #E4342B;border-radius:9px;padding:3px 11px;display:inline-block;margin-bottom:26px}
h1{font-size:19px;font-weight:600;letter-spacing:.02em;margin-bottom:8px}
p.sub{color:#7C8A96;font-size:13.5px;margin-bottom:26px}
form{display:flex;flex-direction:column;gap:12px}
input{width:100%;padding:14px 16px;border-radius:11px;border:1px solid #252E39;background:#141A22;color:#EEF2F6;
font-size:15px;outline:none;transition:border-color .2s}
input:focus{border-color:#E4342B}
button{padding:14px 16px;border:0;border-radius:11px;cursor:pointer;font-weight:600;font-size:15px;color:#fff;
background:linear-gradient(120deg,#E4342B,#FF5C4E);transition:transform .15s}
button:hover{transform:translateY(-1px)}
.err{color:#FF5C4E;font-size:13px;min-height:18px;margin-top:4px}
.foot{margin-top:26px;color:#55616C;font-size:11px;letter-spacing:.05em}
</style></head><body>
<div class="card">
  <span class="mark">NQ</span>
  <h1>Private proposal</h1>
  <p class="sub">This page is by invitation. Enter the passphrase to view.</p>
  <form id="f" autocomplete="off">
    <input id="pw" type="password" placeholder="Passphrase" autofocus aria-label="Passphrase">
    <button type="submit">Unlock</button>
    <div class="err" id="e"></div>
  </form>
  <div class="foot">Nicola Quaye · 360cycling</div>
</div>
<script>
var P=__PAYLOAD__;
function b64(x){var b=atob(x),a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return a;}
async function unlock(pass){
  var enc=new TextEncoder();
  var km=await crypto.subtle.importKey('raw',enc.encode(pass),'PBKDF2',false,['deriveKey']);
  var key=await crypto.subtle.deriveKey({name:'PBKDF2',salt:b64(P.s),iterations:P.n,hash:'SHA-256'},km,{name:'AES-GCM',length:256},false,['decrypt']);
  var pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:b64(P.i)},key,b64(P.c));
  return new TextDecoder().decode(pt);
}
document.getElementById('f').addEventListener('submit',async function(ev){
  ev.preventDefault();
  var e=document.getElementById('e'); e.textContent='';
  try{
    var html=await unlock(document.getElementById('pw').value);
    document.open();document.write(html);document.close();
  }catch(err){ e.textContent='Incorrect passphrase. Try again.'; }
});
</script></body></html>"""

out = WRAP.replace("__PAYLOAD__", json.dumps(payload))
open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(out)
print("locked index.html written:", round(len(out.encode("utf-8"))/1048576, 2), "MB")
