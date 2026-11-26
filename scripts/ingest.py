# -*- coding: utf-8 -*-
"""接收回流结果：归档到 handoff/<时间>-<标签>/ 并登记索引"""
import argparse, os, sys, shutil, datetime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--file', required=True)
    ap.add_argument('--tag', default='result')
    ap.add_argument('--root', default=os.path.join(os.getcwd(), 'handoff'))
    a = ap.parse_args()

    src = os.path.abspath(a.file)
    if not os.path.exists(src):
        print('找不到文件:', src); return 1

    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    safe = ''.join(c if c.isalnum() or c in '-_' else '_' for c in a.tag)[:40]
    dst_dir = os.path.join(a.root, stamp + '-' + safe)
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(src))
    shutil.copy2(src, dst)

    size = os.path.getsize(dst)
    lines = 0
    head = ''
    try:
        with open(dst, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        lines = content.count('\n') + 1
        head = content.strip().split('\n')[0][:120]
    except Exception as e:
        head = '(无法按文本读取: %s)' % e

    idx = os.path.join(a.root, 'index.md')
    first = not os.path.exists(idx)
    with open(idx, 'a', encoding='utf-8') as f:
        if first:
            f.write('# 回流登记\n\n| 时间 | 标签 | 文件 | 大小 | 行数 | 首行 |\n| --- | --- | --- | --- | --- | --- |\n')
        f.write('| %s | %s | %s | %.1f KB | %d | %s |\n' % (
            stamp, a.tag, os.path.basename(dst), size / 1024.0, lines, head.replace('|', '/')))

    print('已归档:', dst)
    print('大小 %.1f KB，%d 行' % (size / 1024.0, lines))
    print('首行:', head)
    print('索引:', idx)
    return 0

if __name__ == '__main__':
    sys.exit(main())
