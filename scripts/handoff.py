# -*- coding: utf-8 -*-
"""生成交接卡：复杂分析 -> WorkBuddy(hy4flash)，图片 -> 豆包"""
import argparse, os, sys, datetime

LANES = {
    'analysis': {
        'to': 'WorkBuddy / hy4flash',
        'head': '请基于下面的资料做分析，按最后要求的格式输出。',
    },
    'image': {
        'to': '豆包（图片生成）',
        'head': '请按下面描述生成图片，不要加水印，不要多余文字。',
    },
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', default='analysis', choices=['analysis', 'image'])
    ap.add_argument('--goal', required=True)
    ap.add_argument('--input', action='append', default=[], help='输入清单，可重复')
    ap.add_argument('--format', default='markdown 表格 + 三条结论')
    ap.add_argument('--out', default='handoff-card.md')
    a = ap.parse_args()

    lane = LANES[a.lane]
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    lines = []
    lines.append('# 交接卡 · ' + ('复杂分析' if a.lane == 'analysis' else '图片生成'))
    lines.append('')
    lines.append('- 生成时间：' + now)
    lines.append('- 交给：' + lane['to'])
    lines.append('- 目标：' + a.goal)
    lines.append('')
    lines.append('## 可直接粘贴的提示词')
    lines.append('')
    lines.append('@@@text')
    lines.append(lane['head'])
    lines.append('')
    lines.append('目标：' + a.goal)
    if a.input:
        lines.append('')
        lines.append('已知资料（只需基于这些字段推理，不必重述）：')
        for x in a.input:
            lines.append('- ' + x)
    lines.append('')
    lines.append('输出要求：' + a.format)
    lines.append('@@@')
    lines.append('')
    if a.input:
        lines.append('## 输入清单')
        lines.append('')
        for x in a.input:
            lines.append('- ' + x)
        lines.append('')
    lines.append('## 回流方式')
    lines.append('')
    lines.append('把结果存成文件（.md / .json / .csv），然后：')
    lines.append('')
    lines.append('@@@bash')
    lines.append('python scripts/ingest.py --file <结果文件> --tag <标签>')
    lines.append('@@@')

    text = '\n'.join(lines).replace('@@@', chr(96) * 3)
    out = os.path.abspath(a.out)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text + '\n')
    print('交接卡已生成:', out)
    print('长度 %d 字符' % len(text))
    print('')
    print(text[:800])
    return 0

if __name__ == '__main__':
    sys.exit(main())
