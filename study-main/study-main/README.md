# study

This project uses [uv](https://docs.astral.sh/uv/) for python version management.

## study内のディレクトリ構造
```
{LOCAL_DIR} or {REMOTE_DIR}
├── README.md
├── high-entropy-oxide
│   └── share
│       ├── busseiken_private
│       ├── HEO_default.sh
│       ├── share.py
│       ├── run_job.py
│       └── beyes_opt.py
└── {WORK_DIR} (until perovskite or spinel)
    ├── scripts
    │   └── run_dir (any name is fine)
    │       ├── exe.py
    │       └── .env
    ├── calc
    │   ├── data.csv
    │   ├── conditions
    │   │   ├── INCAR
    │   │   ├── KPOINTS
    │   │   └── POTCAR
    │   └── results
    │       ├── init
    │       │   └── (job directorys with ID name)
    │       └── BO
    │           └── (job directorys with ID name)
    └── structures
        ├── README.md (one_million_model directory is very large)
        └── one_million_models
            └── POSCARs
                └── (POSCAR_ID files in 1 ~ 1,000,000)
```

## spinel

### 実行方法

TK_POSCAR.shを実行する

```
bash TK_POSCAR.sh
```

### ファイル構成

`TK_POSCAR.sh`を実行すると、`TK_POSCAR.sh`から`spinel_poscar_generator.py`が実行され、`spinel_poscar_generator.py`から`spinel_count.py`が実行され
`spinel_count.py`から`check_features.py`が実行される





