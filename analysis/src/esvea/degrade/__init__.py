"""RO4a degradation operators (Table 3.4), built in S5 after the M4 freeze.

Kept as an empty package now so the separation rule is enforced from the start: nothing in
esvea.simulate may import from here, and these operators are sampled independently of the training
simulator (section 3.6). See tests/test_separation.py.
"""
