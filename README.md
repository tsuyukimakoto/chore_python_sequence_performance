- macOS バージョン: 10.14.5（18F132）
- MacBook Pro (15-inch, Late 2016) 2.6GHz Core i7
- Python: sys.version_info(major=3, minor=7, micro=3, releaselevel='final', serial=0)

| data structure | loop | time | script |
|:---:||:---:|---:|:---|
| list | for | 450.540 | append_to_list_with_loop.py |
| list | Comprehension | 456.691 | append_to_list_with_comp.py |
| set | for | 0.909365004 | add_to_set_with_loop.py |
| set | Comprehension | 0.88970335 | add_to_set_with_comp.py |
| set | convert from list Comprehension | 0.88970335 | add_to_set_with_comp.py |
| array | for | 873.938 | append_to_array_with_loop.py |
| array | Comprehension | 776.432 | append_to_array_with_comp.py |
