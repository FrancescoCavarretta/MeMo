#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .model import Model
from .link import Link
        
class MicroCircuit:
    def __init__(self, name):
        self.name = name
        self.models = set()
        self.links = set()
        
    def add(self, x):
        if isinstance(x, Link):
            self.links.add(x)
            self.add(x.input)
            self.add(x.output)
        elif isinstance(x, Model):
            self.models.add(x)
        else:
            raise Exception(f"The object {x} cannot be part of the Model")

