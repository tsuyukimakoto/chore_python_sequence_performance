- macOS バージョン: 10.14.5（18F132）
- MacBook Pro (15-inch, Late 2016) 2.6GHz Core i7
- Python: sys.version_info(major=3, minor=7, micro=3, releaselevel='final', serial=0)

## timeit

基本的にはO(n)とO(1)なのでlistよりsetが速いのはわかるのだけれど、それにしてもループ遅いなという感想。

array.arrayでint指定したら少し良いことあるかな？と思ったけど遅い。

| data structure | loop | time | script |
|:---:|:---:|---:|:---|
| list | for | 450.540 | append_to_list_with_loop.py |
| list | Comprehension | 456.691 | append_to_list_with_comp.py |
| set | for | 0.909365004 | add_to_set_with_loop.py |
| set | Comprehension | 0.88970335 | add_to_set_with_comp.py |
| set | convert from list Comprehension | 0.88970335 | add_to_set_with_comp.py |
| array | for | 873.938 | append_to_array_with_loop.py |
| array | Comprehension | 867.495 | append_to_array_with_comp.py |

## cProfile

### 10万個のデータ生成

JavaのCollectionを使う場合にはキャパシティをあらかじめ指定ってのがよく言われることでしたが、あらかじめ数がわかっていてもわかっていなくてもあまり差はないのかな？

サイズが大きくてチェック回数が多いなら、setの生成コストは気にせずどんどんset生成してけばよい？

| data structure | loop | time | script |
|:---:|:---:|---:|:---|
| list | for | 0.251 | append_to_list_with_loop.py |
| list | Comprehension | 0.220 | append_to_list_with_comp.py |
| set | for | 0.259 | add_to_set_with_loop.py |
| set | Comprehension | 0.237 | add_to_set_with_comp.py |
| set | convert from list Comprehension | 0.237 | add_to_set_with_comp.py |
| array | for | 0.257 | append_to_array_with_loop.py |
| array | Comprehension | 0.227 | append_to_array_with_comp.py |


以下、cProfileの結果を時間順でソートして時間が少し掛かってそうなところまでのログ。

```
$ python3.7 -m cProfile -s cumulative append_to_list_with_loop.py

   3708930 function calls (3708887 primitive calls) in 445.759 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      4/1    0.000    0.000  445.759  445.759 {built-in method builtins.exec}
        1    0.000    0.000  445.759  445.759 append_to_list_with_loop.py:1(<module>)
        1    0.002    0.002  445.750  445.750 append_to_list_with_loop.py:24(<listcomp>)
        3  443.978  147.993  445.748  148.583 append_to_list_with_loop.py:12(proc)
   600000    0.320    0.000    1.638    0.000 random.py:218(randint)
   600000    0.583    0.000    1.317    0.000 random.py:174(randrange)
        3    0.102    0.034    0.753    0.251 append_to_list_with_loop.py:5(create_data)
   600000    0.481    0.000    0.735    0.000 random.py:224(_randbelow)
  1006801    0.189    0.000    0.189    0.000 {method 'getrandbits' of '_random.Random' objects}
   600000    0.065    0.000    0.065    0.000 {method 'bit_length' of 'int' objects}
   300000    0.031    0.000    0.031    0.000 {method 'append' of 'list' objects}
      9/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap>:978(_find_and_load)
      9/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
      9/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap>:663(_load_unlocked)
      3/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap_external>:722(exec_module)
     15/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
        1    0.000    0.000    0.008    0.008 random.py:38(<module>)
        9    0.000    0.000    0.005    0.001 <frozen importlib._bootstrap>:576(module_from_spec)
        1    0.000    0.000    0.004    0.004 hashlib.py:54(<module>)
        6    0.000    0.000    0.004    0.001 <frozen importlib._bootstrap_external>:1040(create_module)
        6    0.004    0.001    0.004    0.001 {built-in method _imp.create_dynamic}
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap>:882(_find_spec)
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
       33    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
       14    0.000    0.000    0.001    0.000 hashlib.py:116(__get_openssl_constructor)
        8    0.000    0.000    0.001    0.000 hashlib.py:73(__get_builtin_constructor)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:793(get_code)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:523(_compile_bytecode)
        3    0.001    0.000    0.001    0.000 {built-in method marshal.loads}
  -- snip
```


```
$ python3.7 -m cProfile -s cumulative append_to_list_with_comp.py

   3408800 function calls (3408757 primitive calls) in 436.936 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      4/1    0.000    0.000  436.936  436.936 {built-in method builtins.exec}
        1    0.000    0.000  436.936  436.936 append_to_list_with_comp.py:1(<module>)
        1    0.002    0.002  436.903  436.903 append_to_list_with_comp.py:21(<listcomp>)
        3  435.203  145.068  436.900  145.633 append_to_list_with_comp.py:9(proc)
   600000    0.303    0.000    1.634    0.000 random.py:218(randint)
   600000    0.598    0.000    1.331    0.000 random.py:174(randrange)
   600000    0.472    0.000    0.733    0.000 random.py:224(_randbelow)
        3    0.000    0.000    0.660    0.220 append_to_list_with_comp.py:5(create_data)
        3    0.064    0.021    0.659    0.220 append_to_list_with_comp.py:6(<listcomp>)
  1006668    0.198    0.000    0.198    0.000 {method 'getrandbits' of '_random.Random' objects}
   600000    0.062    0.000    0.062    0.000 {method 'bit_length' of 'int' objects}
      9/1    0.000    0.000    0.033    0.033 <frozen importlib._bootstrap>:978(_find_and_load)
      9/1    0.000    0.000    0.033    0.033 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
      9/1    0.000    0.000    0.033    0.033 <frozen importlib._bootstrap>:663(_load_unlocked)
      3/1    0.000    0.000    0.033    0.033 <frozen importlib._bootstrap_external>:722(exec_module)
     15/1    0.000    0.000    0.032    0.032 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
        1    0.000    0.000    0.032    0.032 random.py:38(<module>)
        9    0.000    0.000    0.027    0.003 <frozen importlib._bootstrap>:576(module_from_spec)
        6    0.000    0.000    0.027    0.005 <frozen importlib._bootstrap_external>:1040(create_module)
        6    0.027    0.005    0.027    0.005 {built-in method _imp.create_dynamic}
        1    0.000    0.000    0.024    0.024 hashlib.py:54(<module>)
       14    0.000    0.000    0.004    0.000 hashlib.py:116(__get_openssl_constructor)
        8    0.000    0.000    0.004    0.000 hashlib.py:73(__get_builtin_constructor)
        3    0.000    0.000    0.002    0.001 <frozen importlib._bootstrap_external>:793(get_code)
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap>:882(_find_spec)
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:914(get_data)
        3    0.001    0.000    0.001    0.000 {method 'read' of '_io.FileIO' objects}
        1    0.000    0.000    0.001    0.001 bisect.py:1(<module>)
       33    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:523(_compile_bytecode)
  - snip
```

```
$ python3.7 -m cProfile -s cumulative add_to_set_with_loop.py

   3709198 function calls (3709155 primitive calls) in 1.473 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      4/1    0.000    0.000    1.473    1.473 {built-in method builtins.exec}
        1    0.000    0.000    1.473    1.473 add_to_set_with_loop.py:1(<module>)
        1    0.008    0.008    1.465    1.465 add_to_set_with_loop.py:23(<listcomp>)
        3    0.092    0.031    1.456    0.485 add_to_set_with_loop.py:11(proc)
   600000    0.203    0.000    1.204    0.000 random.py:218(randint)
   600000    0.415    0.000    1.001    0.000 random.py:174(randrange)
        3    0.104    0.035    0.777    0.259 add_to_set_with_loop.py:5(create_data)
   600000    0.379    0.000    0.586    0.000 random.py:224(_randbelow)
  1007069    0.154    0.000    0.154    0.000 {method 'getrandbits' of '_random.Random' objects}
   300000    0.056    0.000    0.056    0.000 {method 'add' of 'set' objects}
   600000    0.053    0.000    0.053    0.000 {method 'bit_length' of 'int' objects}
      9/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap>:978(_find_and_load)
      9/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
      9/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap>:663(_load_unlocked)
      3/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap_external>:722(exec_module)
     15/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
        1    0.000    0.000    0.008    0.008 random.py:38(<module>)
        9    0.000    0.000    0.005    0.001 <frozen importlib._bootstrap>:576(module_from_spec)
        6    0.000    0.000    0.005    0.001 <frozen importlib._bootstrap_external>:1040(create_module)
        6    0.005    0.001    0.005    0.001 {built-in method _imp.create_dynamic}
        1    0.000    0.000    0.004    0.004 hashlib.py:54(<module>)
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap>:882(_find_spec)
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
       33    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
       14    0.000    0.000    0.001    0.000 hashlib.py:116(__get_openssl_constructor)
        8    0.000    0.000    0.001    0.000 hashlib.py:73(__get_builtin_constructor)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:793(get_code)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:523(_compile_bytecode)
        3    0.001    0.000    0.001    0.000 {built-in method marshal.loads}
  - snip
```

```
$ python3.7 -m cProfile -s cumulative add_to_set_with_comp.py

   3409552 function calls (3409509 primitive calls) in 1.463 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      4/1    0.000    0.000    1.463    1.463 {built-in method builtins.exec}
        1    0.000    0.000    1.463    1.463 add_to_set_with_comp.py:1(<module>)
        1    0.008    0.008    1.455    1.455 add_to_set_with_comp.py:21(<listcomp>)
        3    0.106    0.035    1.447    0.482 add_to_set_with_comp.py:9(proc)
   600000    0.214    0.000    1.249    0.000 random.py:218(randint)
   600000    0.433    0.000    1.035    0.000 random.py:174(randrange)
        3    0.000    0.000    0.712    0.237 add_to_set_with_comp.py:5(create_data)
        3    0.092    0.031    0.712    0.237 add_to_set_with_comp.py:6(<setcomp>)
   600000    0.393    0.000    0.602    0.000 random.py:224(_randbelow)
  1007420    0.160    0.000    0.160    0.000 {method 'getrandbits' of '_random.Random' objects}
   600000    0.048    0.000    0.048    0.000 {method 'bit_length' of 'int' objects}
      9/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap>:978(_find_and_load)
      9/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
      9/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap>:663(_load_unlocked)
      3/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap_external>:722(exec_module)
     15/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
        1    0.000    0.000    0.007    0.007 random.py:38(<module>)
        9    0.000    0.000    0.004    0.000 <frozen importlib._bootstrap>:576(module_from_spec)
        6    0.000    0.000    0.004    0.001 <frozen importlib._bootstrap_external>:1040(create_module)
        6    0.004    0.001    0.004    0.001 {built-in method _imp.create_dynamic}
        1    0.000    0.000    0.004    0.004 hashlib.py:54(<module>)
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap>:882(_find_spec)
        9    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
        9    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
       33    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
       14    0.000    0.000    0.001    0.000 hashlib.py:116(__get_openssl_constructor)
        8    0.000    0.000    0.001    0.000 hashlib.py:73(__get_builtin_constructor)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:793(get_code)
  - snip
```

```
$ python3.7 -m cProfile -s cumulative append_to_list_with_comp_and_create_set.py

   3407468 function calls (3407425 primitive calls) in 1.432 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      4/1    0.000    0.000    1.432    1.432 {built-in method builtins.exec}
        1    0.000    0.000    1.432    1.432 append_to_list_with_comp_and_create_set.py:1(<module>)
        1    0.008    0.008    1.425    1.425 append_to_list_with_comp_and_create_set.py:21(<listcomp>)
        3    0.096    0.032    1.416    0.472 append_to_list_with_comp_and_create_set.py:9(proc)
   600000    0.214    0.000    1.232    0.000 random.py:218(randint)
   600000    0.430    0.000    1.018    0.000 random.py:174(randrange)
        3    0.020    0.007    0.712    0.237 append_to_list_with_comp_and_create_set.py:5(create_data)
        3    0.068    0.023    0.692    0.231 append_to_list_with_comp_and_create_set.py:6(<listcomp>)
   600000    0.383    0.000    0.588    0.000 random.py:224(_randbelow)
  1005336    0.159    0.000    0.159    0.000 {method 'getrandbits' of '_random.Random' objects}
   600000    0.046    0.000    0.046    0.000 {method 'bit_length' of 'int' objects}
      9/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap>:978(_find_and_load)
      9/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
      9/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap>:663(_load_unlocked)
      3/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap_external>:722(exec_module)
     15/1    0.000    0.000    0.006    0.006 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
        1    0.000    0.000    0.006    0.006 random.py:38(<module>)
        9    0.000    0.000    0.004    0.000 <frozen importlib._bootstrap>:576(module_from_spec)
        1    0.000    0.000    0.004    0.004 hashlib.py:54(<module>)
        6    0.000    0.000    0.004    0.001 <frozen importlib._bootstrap_external>:1040(create_module)
        6    0.004    0.001    0.004    0.001 {built-in method _imp.create_dynamic}
        9    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap>:882(_find_spec)
        9    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
        9    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
       33    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
       14    0.000    0.000    0.001    0.000 hashlib.py:116(__get_openssl_constructor)
        8    0.000    0.000    0.001    0.000 hashlib.py:73(__get_builtin_constructor)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:793(get_code)
  - snip
```

```
$ python3.7 -m cProfile -s cumulative append_to_array_with_loop.py

   3709251 function calls (3709208 primitive calls) in 877.921 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      4/1    0.000    0.000  877.921  877.921 {built-in method builtins.exec}
        1    0.000    0.000  877.921  877.921 append_to_array_with_loop.py:1(<module>)
        1    0.000    0.000  877.912  877.912 append_to_array_with_loop.py:25(<listcomp>)
        3  876.089  292.030  877.912  292.637 append_to_array_with_loop.py:13(proc)
   600000    0.299    0.000    1.663    0.000 random.py:218(randint)
   600000    0.613    0.000    1.364    0.000 random.py:174(randrange)
        3    0.104    0.035    0.771    0.257 append_to_array_with_loop.py:6(create_data)
   600000    0.488    0.000    0.751    0.000 random.py:224(_randbelow)
  1006905    0.195    0.000    0.195    0.000 {method 'getrandbits' of '_random.Random' objects}
   600000    0.068    0.000    0.068    0.000 {method 'bit_length' of 'int' objects}
   300000    0.056    0.000    0.056    0.000 {method 'append' of 'array.array' objects}
     10/2    0.000    0.000    0.009    0.005 <frozen importlib._bootstrap>:978(_find_and_load)
     10/2    0.000    0.000    0.009    0.005 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
     10/2    0.000    0.000    0.009    0.004 <frozen importlib._bootstrap>:663(_load_unlocked)
     17/3    0.000    0.000    0.008    0.003 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
      3/1    0.000    0.000    0.007    0.007 <frozen importlib._bootstrap_external>:722(exec_module)
        1    0.000    0.000    0.007    0.007 random.py:38(<module>)
       10    0.000    0.000    0.006    0.001 <frozen importlib._bootstrap>:576(module_from_spec)
        7    0.000    0.000    0.006    0.001 <frozen importlib._bootstrap_external>:1040(create_module)
        7    0.006    0.001    0.006    0.001 {built-in method _imp.create_dynamic}
        1    0.000    0.000    0.004    0.004 hashlib.py:54(<module>)
       10    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap>:882(_find_spec)
       10    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
       10    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
       37    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
       14    0.000    0.000    0.001    0.000 hashlib.py:116(__get_openssl_constructor)
        8    0.000    0.000    0.001    0.000 hashlib.py:73(__get_builtin_constructor)
        3    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:793(get_code)
  - snip
```

```
$ python3.7 -m cProfile -s cumulative append_to_array_with_comp.py

   3407629 function calls (3407586 primitive calls) in 870.033 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      4/1    0.000    0.000  870.033  870.033 {built-in method builtins.exec}
        1    0.000    0.000  870.033  870.033 append_to_array_with_comp.py:1(<module>)
        1    0.000    0.000  869.989  869.989 append_to_array_with_comp.py:22(<listcomp>)
        3  868.303  289.434  869.989  289.996 append_to_array_with_comp.py:10(proc)
   600000    0.283    0.000    1.602    0.000 random.py:218(randint)
   600000    0.594    0.000    1.319    0.000 random.py:174(randrange)
   600000    0.476    0.000    0.725    0.000 random.py:224(_randbelow)
        3    0.021    0.007    0.682    0.227 append_to_array_with_comp.py:6(create_data)
        3    0.064    0.021    0.662    0.221 append_to_array_with_comp.py:7(<listcomp>)
  1005280    0.189    0.000    0.189    0.000 {method 'getrandbits' of '_random.Random' objects}
   600000    0.060    0.000    0.060    0.000 {method 'bit_length' of 'int' objects}
     10/2    0.000    0.000    0.044    0.022 <frozen importlib._bootstrap>:978(_find_and_load)
     10/2    0.000    0.000    0.044    0.022 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
     10/2    0.000    0.000    0.043    0.021 <frozen importlib._bootstrap>:663(_load_unlocked)
     17/3    0.000    0.000    0.042    0.014 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
      3/1    0.000    0.000    0.040    0.040 <frozen importlib._bootstrap_external>:722(exec_module)
        1    0.000    0.000    0.039    0.039 random.py:38(<module>)
       10    0.000    0.000    0.037    0.004 <frozen importlib._bootstrap>:576(module_from_spec)
        7    0.000    0.000    0.036    0.005 <frozen importlib._bootstrap_external>:1040(create_module)
        7    0.036    0.005    0.036    0.005 {built-in method _imp.create_dynamic}
        1    0.000    0.000    0.030    0.030 hashlib.py:54(<module>)
       14    0.000    0.000    0.006    0.000 hashlib.py:116(__get_openssl_constructor)
        8    0.000    0.000    0.005    0.001 hashlib.py:73(__get_builtin_constructor)
       10    0.000    0.000    0.003    0.000 <frozen importlib._bootstrap>:882(_find_spec)
       10    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1272(find_spec)
       10    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1240(_get_spec)
        3    0.000    0.000    0.002    0.001 <frozen importlib._bootstrap_external>:793(get_code)
       37    0.000    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
        1    0.000    0.000    0.002    0.002 bisect.py:1(<module>)
        3    0.000    0.000    0.002    0.001 <frozen importlib._bootstrap_external>:914(get_data)
        3    0.001    0.000    0.001    0.000 {method 'read' of '_io.FileIO' objects}
       50    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:74(_path_stat)
       50    0.001    0.000    0.001    0.000 {built-in method posix.stat}
       10    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:93(_path_isfile)
       10    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:84(_path_is_mode_type)
        1    0.001    0.001    0.001    0.001 {built-in method _hashlib.openssl_sha1}
       47    0.000    0.000    0.001    0.000 <frozen importlib._bootstrap_external>:1203(_path_importer_cache)
       10    0.001    0.000    0.001    0.000 {built-in method posix.getcwd}
  - snip
```

## line_profiler

事前にcythonをpipでインストールしてから [書いてある通りに](https://github.com/rkern/line_profiler#installation) インストールした。

@profileはkernprofがいい感じに処理をする（pythonとしては実行できない）

### list

```
$ kernprof -l append_to_list_with_loop.py
append_to_list_with_loop.py
sys.version_info(major=3, minor=7, micro=3, releaselevel='final', serial=0)
Wrote profile results to append_to_list_with_loop.py.lprof

$ python -m line_profiler append_to_list_with_loop.py.lprof
Timer unit: 1e-06 s

Total time: 443.405 s
File: append_to_list_with_loop.py
Function: proc at line 12

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    12                                           @profile
    13                                           def proc():
    14         3          9.0      3.0      0.0      cnt = 0
    15         3    1558856.0 519618.7      0.4      data = create_data()
    16    300003     205982.0      0.7      0.0      for i in range(100000):
    17    300000  441637215.0   1472.1     99.6          if randint(1, 10000000) in data:
    18      3039       3107.0      1.0      0.0              cnt += 1
```


### set

```
$ kernprof -l add_to_set_with_loop.py
add_to_set_with_loop.py
sys.version_info(major=3, minor=7, micro=3, releaselevel='final', serial=0)
Wrote profile results to add_to_set_with_loop.py.lprof

$ python -m line_profiler add_to_set_with_loop.py.lprof
Timer unit: 1e-06 s

Total time: 3.30561 s
File: add_to_set_with_loop.py
Function: proc at line 11

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    11                                           @profile
    12                                           def proc():
    13         3          8.0      2.7      0.0      cnt = 0
    14         3    1593041.0 531013.7     48.2      data = create_data()
    15    300003     114824.0      0.4      3.5      for i in range(100000):
    16    300000    1596492.0      5.3     48.3          if randint(1, 10000000) in data:
    17      2936       1242.0      0.4      0.0              cnt += 1
```

### array.array

```
$ kernprof -l append_to_array_with_loop.py
append_to_array_with_loop.py
sys.version_info(major=3, minor=7, micro=3, releaselevel='final', serial=0)
Wrote profile results to append_to_array_with_loop.py.lprof

$ python -m line_profiler append_to_array_with_loop.py.lprof
Timer unit: 1e-06 s

Total time: 874.929 s
File: append_to_array_with_loop.py
Function: proc at line 13

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    13                                           @profile
    14                                           def proc():
    15         3          5.0      1.7      0.0      cnt = 0
    16         3    1586118.0 528706.0      0.2      data = create_data()
    17    300003     200262.0      0.7      0.0      for i in range(100000):
    18    300000  873139503.0   2910.5     99.8          if randint(1, 10000000) in data:
    19      2905       2835.0      1.0      0.0              cnt += 1
```

## memory_profiler

list と set と array.array サイズが大きく違って面白い。

array.array、流石にint縛りにしたarrayのメモリ消費量少ない。
遅いけれどメモリ1/10で済むなら用途あるよな。間違ってないよね？

@profileはmemory_profilerがいい感じにする。

### list with for loop

```
$ python -m memory_profiler append_to_list_with_loop.py
append_to_list_with_loop.py
Filename: append_to_list_with_loop.py

Line #    Mem usage    Increment   Line Contents
================================================
     5   35.980 MiB   35.980 MiB   @profile
     6                             def create_data():
     7   35.980 MiB    0.000 MiB       l = list()
     8   41.668 MiB    0.000 MiB       for i in range(100000):
     9   41.668 MiB    0.699 MiB           l.append(randint(1, 10000000))
    10   41.668 MiB    0.000 MiB       return l
```

### list comprehension

```
$ python -m memory_profiler append_to_list_with_comp.py
append_to_list_with_comp.py
Filename: append_to_list_with_comp.py

Line #    Mem usage    Increment   Line Contents
================================================
     5   35.984 MiB   35.984 MiB   @profile
     6                             def create_data():
     7   41.645 MiB    0.699 MiB       return [randint(1, 10000000) for i in range(100000)]
```

### list comprehension and convert it to set

```
$ python -m memory_profiler append_to_list_with_comp_and_create_set.py
append_to_list_with_comp_and_create_set.py
Filename: append_to_list_with_comp_and_create_set.py

Line #    Mem usage    Increment   Line Contents
================================================
     5   36.047 MiB   36.047 MiB   @profile
     6                             def create_data():
     7   47.770 MiB    6.043 MiB       return set([randint(1, 10000000) for i in range(100000)])
```

### set with for loop

```
$ python -m memory_profiler add_to_set_with_loop.py
add_to_set_with_loop.py
Filename: add_to_set_with_loop.py

Line #    Mem usage    Increment   Line Contents
================================================
     5   36.062 MiB   36.062 MiB   @profile
     6                             def create_data():
     7   36.062 MiB    0.000 MiB       s = set()
     8   45.277 MiB    0.000 MiB       for i in range(100000):
     9   45.277 MiB    4.000 MiB           s.add(randint(1, 10000000))
    10   45.277 MiB    0.000 MiB       return s
```

### set comprehension

```
$ python -m memory_profiler add_to_set_with_comp.py
add_to_set_with_comp.py
Filename: add_to_set_with_comp.py

Line #    Mem usage    Increment   Line Contents
================================================
     5   36.094 MiB   36.094 MiB   @profile
     6                             def create_data():
     7   45.312 MiB    4.000 MiB       return {randint(1, 10000000) for i in range(100000)}
```

### array.array with for loop

```
$ python -m memory_profiler append_to_array_with_loop.py
append_to_array_with_loop.py
Filename: append_to_array_with_loop.py

Line #    Mem usage    Increment   Line Contents
================================================
     6   36.051 MiB   36.051 MiB   @profile
     7                             def create_data():
     8   36.059 MiB    0.008 MiB       a = array('i')
     9   36.484 MiB    0.000 MiB       for i in range(100000):
    10   36.484 MiB    0.070 MiB           a.append(randint(1, 10000000))
    11   36.484 MiB    0.000 MiB       return a
```

### list comprehension and create array.array from it

```
$ python -m memory_profiler append_to_array_with_comp.py
append_to_array_with_comp.py
Filename: append_to_array_with_comp.py

Line #    Mem usage    Increment   Line Contents
================================================
     6   36.109 MiB   36.109 MiB   @profile
     7                             def create_data():
     8   41.797 MiB    0.699 MiB       return array('i', [randint(1, 10000000) for i in range(100000)])
```
