## 1. Get the `riscv-ctg` sources



### Option A — Clone `riscv-ctg` directly

```bash
git clone https://github.com/riscv-software-src/riscv-ctg.git
cd riscv-ctg
```

### Option B — Clone `riscv-arch-test` and navigate to the CTG folder

```bash
git clone https://github.com/riscv-non-isa/riscv-arch-test.git
cd riscv-arch-test/riscv-ctg/riscv_ctg
```

---

## 2. Place the script

Copy `test.py` into the `riscv-ctg` source directory:

- If you used **Option A** place it inside the cloned `riscv-ctg/`
- If you used **Option B** place it inside `riscv-arch-test/riscv-ctg/riscv_ctg/`

---



## 3. Run the script

From the directory containing `test.py`:

```bash
python test.py
```

Tests for `add` and `addi` will be placed inside the `tests_add` folder