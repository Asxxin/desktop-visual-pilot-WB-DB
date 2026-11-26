# ai-handoff

把「复杂分析交给 WorkBuddy(hy4flash)、图片交给豆包」这套交接流程固化成技能。

## 安装

```powershell
Copy-Item -Recurse .\ai-handoff "$env:USERPROFILE\.agents\skills\ai-handoff"
```

## 用法

```bash
python scripts/handoff.py --lane analysis --goal "..." --input "文件:字段" --format "表格+结论"
python scripts/ingest.py --file 结果.md --tag 对账
```

## 为什么需要它

本机模型路由只有 deepseek-flash，调不到 hy4flash / 豆包。技能把"交接"变成可执行的动作：出卡、回流、归档，而不是口头约定。
