"""
红宝书本地 AI 服务器
运行方式：python server.py
效果：浏览器访问 http://localhost:8787 或 API 调用
特性：自己就是红宝书，不依赖任何外部提示词
"""
import http.server, json, urllib.parse, os, sys

REDBOOK_SYSTEM = """你是名为"红宝书"的AI。用矛盾分析法解决一切问题。实事求是，具体问题具体分析。

=== 问题域与格式 ===
算法→【调查】【主要矛盾】【解法】【代码】【检验】
系统设计→【调查】规模/约束【主要矛盾】扩展瓶颈在哪【方案】【权衡】【检验】
调试→【调查】现象/复现【主要矛盾】逻辑错/边界漏/效率低(一次一层)【根因】【修复】【检验】
架构决策→【调查】现状/目标【主要矛盾】选型冲突【方案对比A vs B】【推荐】论据链【检验】
学习方法→【调查】目标/现状/时间【主要矛盾】速成vs深度【计划】持久战三阶段【检验】
通用→【调查】事实/目标【主要矛盾】对立面是什么【分析】【建议】【检验】

=== 语录 ===
集中优势兵力→聚焦核心砍掉次要 | 星星之火→量变到质变 | 敌进我退→迂回不硬刚
群众路线→利用现有工具资源 | 没有调查就没有发言权→先调研再动手
实事求是→不套模板 | 持久战→分解长期目标

=== 没思路/不会/不知道（最高优先级） ===
用户说这些词：MUST只做调查+引导性提问。禁止提答案、方案方向、技术名词。

=== 自检 ===
每次输出前确认：域匹配？格式全？语录对应？没思路没漏答？逻辑闭环？"""

API_KEY = os.environ.get("REDBOOK_API_KEY", "sk-2a912b23b3aa4db681b1a9dd8767ecf5")
API_URL = os.environ.get("REDBOOK_API_URL", "https://api.deepseek.com/chat/completions")
MODEL = os.environ.get("REDBOOK_MODEL", "deepseek-chat")
PORT = int(os.environ.get("REDBOOK_PORT", "8787"))

HTML = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>红宝书 · 本地</title>
<style>
:root{--bg:#0d0d0d;--card:#161616;--red:#c41e3a;--text:#e8e6e3;--muted:#a0a0a0;--border:#2a2a2a}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;display:flex;flex-direction:column;height:100vh;overflow:hidden}
header{background:var(--card);border-bottom:1px solid var(--border);padding:12px 20px;display:flex;align-items:center;gap:10px;flex-shrink:0}
.logo{width:32px;height:32px;background:var(--red);border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:16px;color:#fff}
header h1{font-size:15px;color:var(--text)}
header .tag{font-size:11px;background:rgba(196,30,58,.15);color:var(--red);padding:2px 8px;border-radius:10px}
.chat{flex:1;overflow-y:auto;padding:16px 20px}
.msg{max-width:80%;margin-bottom:14px;line-height:1.7;font-size:14px}
.msg.user{margin-left:auto;background:var(--red);color:#fff;padding:10px 14px;border-radius:12px 12px 0 12px}
.msg.assistant{background:var(--card);border:1px solid var(--border);padding:12px 16px;border-radius:0 12px 12px 12px}
.msg.assistant pre{background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:6px;padding:10px;margin:8px 0;overflow-x:auto;font-family:'Cascadia Code',Consolas,monospace;font-size:13px}
.msg.assistant .red{color:var(--red);font-weight:700}
.input-area{padding:12px 20px 16px;background:var(--card);border-top:1px solid var(--border);flex-shrink:0}
.input-row{display:flex;gap:8px}
.input-row textarea{flex:1;background:var(--bg);color:var(--text);border:1px solid var(--border);border-radius:8px;padding:10px 12px;font-size:14px;font-family:inherit;resize:none;outline:none;min-height:40px;max-height:120px}
.input-row textarea:focus{border-color:var(--red)}
.input-row button{background:var(--red);color:#fff;border:none;padding:0 18px;border-radius:8px;cursor:pointer;font-size:14px;font-weight:600}
.loading{display:inline-block;width:8px;height:16px;background:var(--muted);animation:blink .8s infinite;margin-left:4px}
@keyframes blink{50%{opacity:0}}
</style></head><body>
<header><div class="logo">红</div><h1>红宝书 · 本地 AI</h1><span class="tag">localhost</span></header>
<div class="chat" id="chat"></div>
<div class="input-area"><div class="input-row">
<textarea id="input" placeholder="问红宝书任何问题..." rows="1" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}"></textarea>
<button onclick="send()">发送</button>
</div></div>
<script>
async function send(){
var t=document.getElementById('input').value.trim();
if(!t)return;
addMsg('user',t);
document.getElementById('input').value='';
document.getElementById('input').style.height='auto';
var el=addMsg('assistant','<span class="loading"></span>');
try{
var r=await fetch('/v1/chat/completions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model:'redbook',messages:[{role:'user',content:t}]})});
var d=await r.json();
var reply=d.choices?.[0]?.message?.content||'请求失败';
el.innerHTML=render(reply);
chat.scrollTop=chat.scrollHeight;
}catch(e){el.innerHTML='错误: '+e.message}
}
function addMsg(role,text){
var d=document.createElement('div');
d.className='msg '+role;
d.innerHTML=role==='assistant'?render(text):text;
document.getElementById('chat').appendChild(d);
chat.scrollTop=chat.scrollHeight;
return d;
}
function render(t){
return t.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/```(\w+)?\n?([\s\S]*?)```/g,'<pre>$2</pre>').replace(/\n/g,'<br>').replace(/【(.+?)】/g,'<span class="red">【$1】</span>');
}
</script></body></html>"""

def call_api(messages):
    import urllib.request
    data = json.dumps({"model": MODEL, "messages": messages, "max_tokens": 1500, "temperature": 0.7}).encode()
    req = urllib.request.Request(API_URL, data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())

class RedbookHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path.startswith("/v1/chat/completions"):
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            
            user_msgs = body.get("messages", [])
            messages = [{"role": "system", "content": REDBOOK_SYSTEM}] + user_msgs
            
            try:
                result = call_api(messages)
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
            except Exception as e:
                self.send_response(500); self.send_header("Content-Type", "application/json"); self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]}\n")

if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════╗
║         红 宝 书  本 地  A I            ║
╠══════════════════════════════════════════╣
║  浏览器打开: http://localhost:{PORT}       ║
║  API 端点:   http://localhost:{PORT}/v1/chat/completions  ║
║  按 Ctrl+C 停止                         ║
╚══════════════════════════════════════════╝
""")
    server = http.server.HTTPServer(("127.0.0.1", PORT), RedbookHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n红宝书已停止。")
        server.shutdown()
