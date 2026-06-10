# -*- coding: utf-8 -*-
import cairosvg

F = "WenQuanYi Zen Hei"

# ---------- 图1：整体在做什么 ----------
svg1 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="560" font-family="{F}">
<rect width="1040" height="560" fill="#f7f9fc"/>
<text x="520" y="50" font-size="34" fill="#1a2b4a" text-anchor="middle" font-weight="bold">① 这个系统到底在做什么？</text>
<text x="520" y="88" font-size="20" fill="#5a6b85" text-anchor="middle">上传一张自拍 → 机器帮你画出「还是你，但换了画风」的头像</text>

<!-- 自拍照 -->
<rect x="60" y="150" width="200" height="240" rx="14" fill="#ffffff" stroke="#c3d0e0" stroke-width="3"/>
<circle cx="160" cy="240" r="46" fill="#ffe0b2" stroke="#e0a060" stroke-width="3"/>
<circle cx="143" cy="232" r="7" fill="#3a3a3a"/><circle cx="177" cy="232" r="7" fill="#3a3a3a"/>
<path d="M140 262 Q160 280 180 262" stroke="#3a3a3a" stroke-width="4" fill="none"/>
<rect x="120" y="300" width="80" height="50" rx="10" fill="#88a4c8"/>
<text x="160" y="372" font-size="22" fill="#1a2b4a" text-anchor="middle" font-weight="bold">你的自拍照</text>

<!-- 箭头 -->
<polygon points="300,260 360,260 360,245 400,275 360,305 360,290 300,290" fill="#6a8fc0"/>

<!-- 机器盒子 -->
<rect x="420" y="170" width="200" height="200" rx="18" fill="#2d5fa8"/>
<text x="520" y="250" font-size="26" fill="#ffffff" text-anchor="middle" font-weight="bold">AI 头像</text>
<text x="520" y="285" font-size="26" fill="#ffffff" text-anchor="middle" font-weight="bold">生成系统</text>
<text x="520" y="325" font-size="16" fill="#cfe0ff" text-anchor="middle">(就是这个软件)</text>

<!-- 箭头 -->
<polygon points="640,260 700,260 700,245 740,275 700,305 700,290 640,290" fill="#6a8fc0"/>

<!-- 多风格头像 -->
<g>
<rect x="770" y="150" width="100" height="100" rx="12" fill="#ffd6e0" stroke="#d98aa0" stroke-width="2"/>
<circle cx="820" cy="195" r="26" fill="#ffe0b2"/><text x="820" y="240" font-size="15" fill="#7a3a4a" text-anchor="middle">动漫风</text>
<rect x="885" y="150" width="100" height="100" rx="12" fill="#d6ecff" stroke="#7aa8d9" stroke-width="2"/>
<rect x="800" y="178" width="40" height="40" fill="#88a" /><text x="935" y="240" font-size="15" fill="#2a4a7a" text-anchor="middle">像素风</text>
<rect x="770" y="270" width="100" height="100" rx="12" fill="#e6dcc8" stroke="#b39a6a" stroke-width="2"/>
<circle cx="820" cy="315" r="26" fill="#d8b890"/><text x="820" y="360" font-size="15" fill="#5a4a2a" text-anchor="middle">油画风</text>
<rect x="885" y="270" width="100" height="100" rx="12" fill="#d8f0e0" stroke="#7ab894" stroke-width="2"/>
<circle cx="935" cy="315" r="26" fill="#ffe0b2"/><text x="935" y="360" font-size="15" fill="#2a5a3a" text-anchor="middle">职业风</text>
</g>
<!-- fix pixel face -->
<rect x="905" y="180" width="60" height="40" fill="#9ab" opacity="0"/>

<rect x="60" y="430" width="920" height="90" rx="12" fill="#fff6e5" stroke="#f0c060" stroke-width="2"/>
<text x="90" y="468" font-size="20" fill="#8a5a10" font-weight="bold">两个关键词：</text>
<text x="90" y="500" font-size="19" fill="#5a4a20">「保人脸」= 生成出来还认得出是你　｜　「风格」= 画风可以是动漫 / 像素 / 油画 / 职业照…随你选</text>
</svg>'''

# ---------- 图2：两条路 ----------
svg2 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="600" font-family="{F}">
<rect width="1040" height="600" fill="#f7f9fc"/>
<text x="520" y="50" font-size="34" fill="#1a2b4a" text-anchor="middle" font-weight="bold">② 画图的「引擎」有两条路可选</text>
<text x="520" y="88" font-size="19" fill="#5a6b85" text-anchor="middle">系统的其他部分都一样，区别只在「谁来真正画这张图」</text>

<!-- 左：云端 -->
<rect x="60" y="120" width="430" height="420" rx="18" fill="#ffffff" stroke="#7aa8d9" stroke-width="3"/>
<rect x="60" y="120" width="430" height="64" rx="18" fill="#2d5fa8"/>
<text x="275" y="162" font-size="26" fill="#ffffff" text-anchor="middle" font-weight="bold">路 A：云端 API（租别人的电脑）</text>
<text x="90" y="225" font-size="20" fill="#1a2b4a">就像「叫外卖」：你把照片发过去，</text>
<text x="90" y="255" font-size="20" fill="#1a2b4a">别人的超级电脑画好再发回来。</text>
<text x="90" y="305" font-size="20" fill="#1a8a4a" font-weight="bold">✓ 优点</text>
<text x="110" y="335" font-size="18" fill="#2a5a3a">· 不用买显卡，任何电脑都行</text>
<text x="110" y="362" font-size="18" fill="#2a5a3a">· 几天就能上线，画质好</text>
<text x="110" y="389" font-size="18" fill="#2a5a3a">· 按张付钱，约 0.2–0.5 元 / 张</text>
<text x="90" y="435" font-size="20" fill="#b04a2a" font-weight="bold">✗ 缺点</text>
<text x="110" y="465" font-size="18" fill="#7a3a2a">· 照片要传到别人服务器</text>
<text x="110" y="492" font-size="18" fill="#7a3a2a">· 用得多长期有费用</text>
<text x="90" y="525" font-size="17" fill="#2d5fa8" font-weight="bold">代表：Replicate、fal.ai</text>

<!-- 右：本地 -->
<rect x="550" y="120" width="430" height="420" rx="18" fill="#ffffff" stroke="#b39a6a" stroke-width="3"/>
<rect x="550" y="120" width="430" height="64" rx="18" fill="#8a6a2a"/>
<text x="765" y="162" font-size="26" fill="#ffffff" text-anchor="middle" font-weight="bold">路 B：本地显卡（用你自己的电脑）</text>
<text x="580" y="225" font-size="20" fill="#1a2b4a">就像「自己在家做饭」：所有计算</text>
<text x="580" y="255" font-size="20" fill="#1a2b4a">都在你自己的机器上完成。</text>
<text x="580" y="305" font-size="20" fill="#1a8a4a" font-weight="bold">✓ 优点</text>
<text x="600" y="335" font-size="18" fill="#2a5a3a">· 出图免费（只费电）</text>
<text x="600" y="362" font-size="18" fill="#2a5a3a">· 照片不出门，最隐私</text>
<text x="580" y="408" font-size="20" fill="#b04a2a" font-weight="bold">✗ 缺点</text>
<text x="600" y="438" font-size="18" fill="#7a3a2a">· 要一张 NVIDIA 显卡（≥12GB）</text>
<text x="600" y="465" font-size="18" fill="#7a3a2a">· 配置麻烦，出图较慢</text>
<text x="600" y="492" font-size="18" fill="#7a3a2a">· 普通笔记本 / Mac 跑不动</text>
<text x="580" y="525" font-size="17" fill="#8a6a2a" font-weight="bold">代表：ComfyUI + Stable Diffusion</text>

<rect x="60" y="558" width="920" height="34" rx="8" fill="#e8f0ff"/>
<text x="520" y="582" font-size="19" fill="#1a3a6a" text-anchor="middle" font-weight="bold">💡 建议：先走「路 A 云端」快速上线，以后想省钱 / 更隐私再换「路 B 本地」，网站不用重做。</text>
</svg>'''

# ---------- 图3：多人网站的零件 + 排队 ----------
svg3 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="640" font-family="{F}">
<rect width="1040" height="640" fill="#f7f9fc"/>
<text x="520" y="48" font-size="34" fill="#1a2b4a" text-anchor="middle" font-weight="bold">③ 一个「多人能用的网站」由哪些零件组成</text>
<text x="520" y="84" font-size="19" fill="#5a6b85" text-anchor="middle">你和朋友打开网址 → 上传 → 等一会 → 拿到头像。背后是这样运转的：</text>

<!-- 1 网页前端 -->
<rect x="50" y="130" width="200" height="120" rx="14" fill="#dceeff" stroke="#7aa8d9" stroke-width="2"/>
<text x="150" y="170" font-size="22" fill="#1a3a6a" text-anchor="middle" font-weight="bold">网页（前端）</text>
<text x="150" y="202" font-size="16" fill="#2a4a6a" text-anchor="middle">你和朋友看到的</text>
<text x="150" y="226" font-size="16" fill="#2a4a6a" text-anchor="middle">上传 / 展示界面</text>

<polygon points="252,185 300,185 300,173 330,195 300,217 300,205 252,205" fill="#6a8fc0"/>

<!-- 2 后端 -->
<rect x="332" y="130" width="200" height="120" rx="14" fill="#fff0d6" stroke="#d9a85a" stroke-width="2"/>
<text x="432" y="170" font-size="22" fill="#6a4a10" text-anchor="middle" font-weight="bold">管事的（后端）</text>
<text x="432" y="202" font-size="16" fill="#6a4a20" text-anchor="middle">收照片、检查、</text>
<text x="432" y="226" font-size="16" fill="#6a4a20" text-anchor="middle">安排任务、管账号</text>

<polygon points="534,185 582,185 582,173 612,195 582,217 582,205 534,205" fill="#6a8fc0"/>

<!-- 3 排队 -->
<rect x="614" y="130" width="200" height="120" rx="14" fill="#ffe0e0" stroke="#d98a8a" stroke-width="2"/>
<text x="714" y="168" font-size="22" fill="#8a2a2a" text-anchor="middle" font-weight="bold">排队区</text>
<text x="714" y="198" font-size="15" fill="#7a3a3a" text-anchor="middle">画一张要 10–60 秒，</text>
<text x="714" y="220" font-size="15" fill="#7a3a3a" text-anchor="middle">太慢不能让你干等，</text>
<text x="714" y="242" font-size="15" fill="#7a3a3a" text-anchor="middle">先排队、画好再通知</text>

<polygon points="714,252 714,300 702,300 724,330 746,300 734,300 734,252" fill="#6a8fc0"/>

<!-- 4 画图worker -->
<rect x="614" y="332" width="200" height="110" rx="14" fill="#e0e0ff" stroke="#8a8ad9" stroke-width="2"/>
<text x="714" y="372" font-size="22" fill="#2a2a8a" text-anchor="middle" font-weight="bold">画图引擎</text>
<text x="714" y="404" font-size="16" fill="#3a3a7a" text-anchor="middle">真正出图的地方</text>
<text x="714" y="428" font-size="15" fill="#3a3a7a" text-anchor="middle">（云端 或 本地，见图②）</text>

<polygon points="612,387 564,387 564,375 534,397 564,419 564,407 612,407" fill="#6a8fc0"/>

<!-- 5 图库+数据库 -->
<rect x="332" y="330" width="200" height="114" rx="14" fill="#d8f0e0" stroke="#7ab894" stroke-width="2"/>
<text x="432" y="368" font-size="21" fill="#1a5a3a" text-anchor="middle" font-weight="bold">仓库</text>
<text x="432" y="398" font-size="15" fill="#2a5a3a" text-anchor="middle">图库：存生成的头像</text>
<text x="432" y="422" font-size="15" fill="#2a5a3a" text-anchor="middle">数据库：存账号、记录</text>

<!-- 朋友访问 -->
<rect x="50" y="500" width="940" height="110" rx="16" fill="#ffffff" stroke="#7aa8d9" stroke-width="3"/>
<text x="80" y="540" font-size="22" fill="#1a2b4a" font-weight="bold">朋友怎么打开？</text>
<circle cx="130" cy="578" r="18" fill="#ffe0b2" stroke="#e0a060" stroke-width="2"/>
<text x="175" y="572" font-size="18" fill="#3a3a3a">你的朋友（手机/电脑）</text>
<polygon points="330,567 380,567 380,557 405,577 380,597 380,587 330,587" fill="#6a8fc0"/>
<rect x="415" y="552" width="180" height="52" rx="10" fill="#fff0d6" stroke="#d9a85a" stroke-width="2"/>
<text x="505" y="575" font-size="16" fill="#6a4a10" text-anchor="middle">一条安全网址</text>
<text x="505" y="595" font-size="14" fill="#6a4a20" text-anchor="middle">(Cloudflare 隧道)</text>
<polygon points="600,567 650,567 650,557 675,577 650,597 650,587 600,587" fill="#6a8fc0"/>
<rect x="685" y="552" width="270" height="52" rx="10" fill="#dceeff" stroke="#7aa8d9" stroke-width="2"/>
<text x="820" y="575" font-size="16" fill="#1a3a6a" text-anchor="middle">你家里 / 服务器上跑的系统</text>
<text x="820" y="595" font-size="14" fill="#2a4a6a" text-anchor="middle">不用懂路由器设置，朋友点网址就能用</text>
</svg>'''

for name, svg in [("diagram1_what.png", svg1), ("diagram2_engine.png", svg2), ("diagram3_system.png", svg3)]:
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to="/home/user/attention/"+name, output_width=1040)
    print("wrote", name)
