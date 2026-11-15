#!/usr/bin/env python3
"""批量数值口径格式化验收探针。

契约：
  from humanize.batch import format_many
  res = format_many([(1024, "bytes"), (3600, "seconds")])
  res.texts   每项格式化结果，如 "1.0 kB"、"an hour"
  res.unknown 不支持的单位列表
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
FAIL = 0


def probe(code, desc, fn):
    global FAIL
    try:
        fn()
        print(f"[PASS] {code} {desc}")
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {code} {desc}\n        {type(exc).__name__}: {exc}")
        FAIL += 1


def main():
    try:
        from humanize.batch import format_many  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] P0 导入 humanize.batch 失败：{type(exc).__name__}: {exc}")
        print("-" * 60)
        print("探针汇总：0/4 通过")
        return 1

    def p1():
        res = format_many([(1024, "bytes")])
        assert len(res.texts) == 1 and "kB" in res.texts[0], res.texts

    def p2():
        res = format_many([(3600, "seconds")])
        assert "hour" in res.texts[0], res.texts

    def p3():
        res = format_many([(1, "furlongs")])
        assert res.unknown == ["furlongs"], res.unknown

    def p4():
        import humanize
        assert humanize.naturalsize(1024) in ("1.0 kB", "1.0 KB")

    probe("P1", "字节口径", p1)
    probe("P2", "时长口径", p2)
    probe("P3", "未知单位留痕", p3)
    probe("P4", "既有 naturalsize 不变", p4)

    print("-" * 60)
    print(f"探针汇总：{4 - FAIL}/4 通过")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
