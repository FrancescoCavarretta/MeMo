#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MicroCircuit:
    def __init__(self, name):
        self.name = name
        self.models = set()
        self.links = set()
        
    def add(self, x):
        from memo.model import Model
        from memo.link import Link
        
        if isinstance(x, Link):
            self.links.add(x)
            self.add(x.input)
            self.add(x.output)
        elif isinstance(x, Model):
            self.models.add(x)
        else:
            raise Exception(f"The object {x} cannot be part of the Model")

