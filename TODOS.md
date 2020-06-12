# TODOs

- [X] Compile extracted CSVs, add book_name, sheet_name, filedate fields
- [x] Extract CSVs from every collected XLSX
    - [ ] Modify extract_csvs.py to handle older xls files

- [ ] Manually hand make the demil tables
- [ ] Wrangling
    - in each successive compiled file, figure out what's been removed in the subsequent date
    - Remove unnecessary columns, e.g. station_type, book_name, sheet_name
    



## Later tasks

- [ ] Collect/stash the other county-level files from the marshallproject repo
- [ ] Write makefile instructions
- [ ] Compact repo size
- [ ] Should `compiled` be `fused`?



# Bash doodles

```sh

$ cat data/compiled/state-agencies.csv \
    | xsv select station_name \
    | sort | uniq -c | sort -rn | head -n 20

32278 LOS ANGELES POLICE DEPARTMENT
20260 OPERATION ALLIANCE TX
19721 SC LAW ENFORCEMENT DIVISION
18739 KY STATE POLICE
18432 FL HIGHWAY PATROL
16930 VENTURA COUNTY SHERIFF OFFICE
16394 OAKLAND COUNTY  SHERIFF OFFICE
16231 DHS/CBP/LSC EL PASO
14375 OH STATE HIGHWAY PATROL
13498 AUSTIN POLICE DEPT
12930 KERN COUNTY SHERIFF OFFICE
12394 HOUSTON POLICE DEPT
11371 LOS ANGELES COUNTY SHERIFF DEPT
11335 ARIZONA DEPT OF PUBLIC SAFETY
10059 DOJ/FBI SACRAMENTO
8319 OAKLAND CO SHERIFF DEPT
8303 CARROLL COUNTY SHERIFF DEPT
8030 ARIZONA DEPT OF PUBLIC SAFETY LEA
7947 WI STATE PATROL
7576 KNOX COUNTY SHERIFFS OFFICE
```

austin sample

```
cat data/compiled/state-agencies.csv | xsv search 'AUSTIN POLICE' --select station_name | xsv search 'TX' --select state  > data/archived/samples/compiled-austin-police.csv 
```



 cat data/compiled/state-agencies.csv \
    | xsv search 'HOUSTON POLICE DEPT' \
    | xsv search '2015-09-02' \
    | xsv search '2520-01-503-3672'

    \
    | xsv search '5855-01-448-5464'



## demil code count

```
xsv select 'demil_code' data/compiled/state-agencies.csv  | sort | uniq -c 
   2 ""
458469 A
82108 B
115319 C
1793431 D
4121 E
108433 F
77132 Q
   3 X
   1 demil_code
```
