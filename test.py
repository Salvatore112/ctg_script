#!/usr/bin/env python3

import os
import sys
import ruamel.yaml

from riscv_isac.utils import combineReader
from riscv_ctg.generator import Generator
from riscv_ctg import constants

RISCV_CTG_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RISCV_CTG_PATH)


def generate_add_tests():

    out_dir = "./tests_add"
    os.makedirs(out_dir, exist_ok=True)

    template_files = [
        f
        for f in constants.template_files
        if "fd.yaml" not in f and "inx.yaml" not in f
    ]

    yaml = ruamel.yaml.YAML(typ="rt")
    yaml.default_flow_style = False
    yaml.allow_unicode = True

    op_template = {}
    with combineReader(template_files) as fp:
        op_template = dict(yaml.load(fp))

    xlen = 32
    flen = 32
    base_isa = "rv32i"
    randomize = True

    all_regs = ["x" + str(x) for x in range(1, 32)]

    if "add" in op_template:
        op_node = op_template["add"]

        node = {
            "config": ["check ISA:=regex(.*RV32.*I.*)"],
            "mnemonics": {"add": 0},
            "rs1": all_regs[:8],
            "rs2": all_regs[8:16],
            "rd": all_regs[16:24],
            "op_comb": [
                "rs1 != rs2",
                "rs1 != rd",
                "rs1 != rd or rs1 > rd",
                "rs2 != rd",
                "rs1 != rs2 and rs1 != rd and rs2 != rd",
            ],
            "val_comb": {
                "rs1_val == 0 and rs2_val == 0": 0,
                "rs1_val == 1 and rs2_val == 1": 0,
                "rs1_val == -1 and rs2_val == -1": 0,
                "rs1_val == 2147483647 and rs2_val == 2147483647": 0,
                "rs1_val == -2147483648 and rs2_val == -2147483648": 0,
                "rs1_val == 0x12345678 and rs2_val == 0x87654321": 0,
            },
        }

        gen = Generator(
            op_node["formattype"],
            op_node,
            "add",
            randomize,
            xlen,
            flen,
            0,
            base_isa,
            False,
        )

        op_comb = gen.opcomb(node)
        val_comb = gen.valcomb(node)
        instr_dict = gen.gen_inst(op_comb, val_comb, node)
        instr_dict = gen.swreg(instr_dict)
        instr_dict = gen.testreg(instr_dict)
        instr_dict = gen.correct_val(instr_dict)
        instr_dict = gen.reformat_instr(instr_dict)

        fprefix = os.path.join(out_dir, "add_basic")

        usage_str = "// placehodler"

        gen.write_test(fprefix, node, "add_basic", instr_dict, op_node, usage_str, None)

    if "addi" in op_template:
        op_node = op_template["addi"]

        node = {
            "config": ["check ISA:=regex(.*RV32.*I.*)"],
            "mnemonics": {"addi": 0},
            "rs1": all_regs[:8],
            "rd": all_regs[8:16],
            "op_comb": [
                "rs1 != rd",
            ],
            "val_comb": {
                "rs1_val == 0 and imm_val == 0": 0,
                "rs1_val == 1 and imm_val == 1": 0,
                "rs1_val == -1 and imm_val == -1": 0,
                "rs1_val == 2147483647 and imm_val == 2047": 0,
                "rs1_val == -2147483648 and imm_val == -2048": 0,
                "rs1_val == 0x12345678 and imm_val == 0x123": 0,
                "rs1_val == 0x87654321 and imm_val == -0x456": 0,
            },
        }

        gen = Generator(
            op_node["formattype"],
            op_node,
            "addi",
            randomize,
            xlen,
            flen,
            0,
            base_isa,
            False,
        )

        op_comb = gen.opcomb(node)
        val_comb = gen.valcomb(node)
        instr_dict = gen.gen_inst(op_comb, val_comb, node)
        instr_dict = gen.swreg(instr_dict)
        instr_dict = gen.testreg(instr_dict)
        instr_dict = gen.correct_val(instr_dict)
        instr_dict = gen.reformat_instr(instr_dict)

        fprefix = os.path.join(out_dir, "addi_basic")

        usage_str = "// placeholder"

        gen.write_test(
            fprefix, node, "addi_basic", instr_dict, op_node, usage_str, None
        )


if __name__ == "__main__":
    generate_add_tests()
