#!/usr/bin/env python3
"""Periods to frequencies, MHz."""
import yaml


def main(name):
    yamlfile = name + ".yaml"
    with open(yamlfile) as fi:
        obj = yaml.safe_load(fi)
    if obj.get("tck"):
        obj["fck"] = 200/obj["tck"]/1e6
    if obj.get("tfb"):
        obj["fckfb"] = 8/obj["tfb"]/1e6
    if obj.get("vctrl_max") is not None and obj.get("vctrl_min") is not None:
        obj["vripple"] = obj["vctrl_max"] - obj["vctrl_min"]
    with open(yamlfile, "w") as fo:
        yaml.dump(obj, fo)
