"""Maps each concept_id to the code construct(s) a correct solution must
use — not just the output it must produce. Without this, a learner can
pass any problem by hardcoding the literal expected output (e.g.
`print("합: 8")` instead of defining add/subtract/multiply functions).

A requirement is a "kind:value" string, or a tuple of such strings
meaning "at least one of these satisfies it" (OR). See
app/code_checks.py for what each kind checks. Concepts not listed here
(print-basics, string-quotes, escape-chars, ...) have no structural
requirement — their "answer" IS the literal text, so there's nothing to
hardcode around.

PROBLEM_OVERRIDES adds extra requirements for specific problems whose
concept_id doesn't capture everything the *mini* version of that
concept combines (e.g. a mini-project mixing two techniques from its
level). Overrides are additive to the concept's own requirements, never
a replacement.
"""

REQUIRED_BY_CONCEPT: dict[str, list] = {
    # Phase 1 — fundamentals
    "variables": ["node:Assign"],
    "input-basics": ["call:input"],
    "string-concat": ["op:Add"],
    "string-index-slice": ["node:Subscript"],
    "fstring-and-functions": ["node:JoinedStr"],
    "numbers": ["op:Add"],
    "type-conversion": [("call:int", "call:float"), "call:input"],
    "power-floordiv-mod": [("op:Pow", "op:FloorDiv", "op:Mod")],
    "booleans": ["node:Compare"],
    "if-basics": ["node:If"],
    "if-else": ["node:If"],
    "elif": ["node:If"],
    "logical-operators": [("op:And", "op:Or")],
    "membership": [("op:In", "op:NotIn")],
    "ternary": ["node:IfExp"],
    "for-range": ["node:For"],
    "for-range-start-stop": ["node:For"],
    "for-loop-variable": ["node:For"],
    "pass-statement": ["node:Pass"],
    "while-basics": ["node:While"],
    "while-break": ["node:While", "node:Break"],
    "while-input": ["node:While", "call:input"],
    "while-else": ["node:While"],
    "list-basics": ["node:Subscript"],
    "list-functions": [("method:sort", "method:count")],
    "list-comprehension": ["node:ListComp"],
    "tuple-basics": ["node:Subscript"],
    "set-basics": ["call:set"],
    "set-operations": [("op:BitAnd", "op:BitOr", "op:Sub")],
    "dict-basics": ["node:Subscript"],
    "dict-get": ["method:get"],
    "dict-iteration": [("method:keys", "method:values", "method:items")],
    "def-basics": ["node:FunctionDef"],
    "def-params": ["node:FunctionDef"],
    "def-return": ["node:FunctionDef", "node:Return"],
    "scope": ["node:FunctionDef"],
    "default-param": ["node:FunctionDef:default"],
    "args": ["node:FunctionDef:vararg"],
    "lambda": ["node:Lambda"],
    "try-except-basics": ["node:Try"],
    "specific-exceptions": ["node:Try"],
    "finally": ["node:Try:finally"],
    "class-instance": ["node:ClassDef"],
    "init-self": ["node:ClassDef"],
    "methods": ["node:ClassDef"],
    "file-write": ["call:open", "method:write"],
    "file-read": ["call:open", "method:read"],
    "import-module": ["import:math"],
    # Phase 2 — numpy / pandas
    "ndarray-basics": ["import:numpy", "method:array"],
    "ndarray-index-slice": ["import:numpy", "node:Subscript"],
    "ndarray-stats": ["import:numpy", ("method:sum", "method:mean", "method:max", "method:min")],
    "special-arrays": ["import:numpy", ("method:zeros", "method:eye", "method:ones")],
    "broadcasting": ["import:numpy", "op:Add"],
    "array-array-op": ["import:numpy", "op:Add"],
    "boolean-filtering": ["import:numpy", "node:Subscript", "node:Compare"],
    "axis-aggregation": ["import:numpy", "method:sum", "kwarg:axis"],
    "series-basics": ["import:pandas", "method:Series"],
    "dataframe-basics": ["import:pandas", "method:DataFrame"],
    "dataframe-filter": ["import:pandas", "node:Subscript", "node:Compare"],
    "iloc": ["import:pandas", "attr:iloc"],
    "loc": ["import:pandas", "attr:loc"],
    "multi-condition-mask": ["import:pandas", ("op:BitAnd", "op:BitOr")],
    "missing-values": ["import:pandas", ("method:isna", "method:fillna")],
    "groupby": ["import:pandas", "method:groupby"],
    "sort-values": ["import:pandas", "method:sort_values"],
    "isin": ["import:pandas", "method:isin"],
    "describe": ["import:pandas", "method:describe"],
    "value-counts": ["import:pandas", "method:value_counts"],
    "agg": ["import:pandas", "method:agg"],
    # Phase 3 — Kaggle
    "kaggle-files": ["import:pandas", "method:DataFrame"],
    "csv-read-write": ["import:pandas", "method:to_csv", "method:read_csv"],
    "shape-head": ["import:pandas", ("attr:shape", "method:head")],
    "check-missing": ["import:pandas", ("method:isnull", "method:isna", "method:fillna")],
    "check-outliers": ["import:pandas", "method:describe"],
    "target-relationship": ["import:pandas", "method:groupby", "method:mean"],
    "encoding": ["import:pandas", "method:map"],
    "derived-feature": ["import:pandas", ("method:astype", "method:cut")],
    "scaling": ["import:pandas", "method:min", "method:max"],
    "train-test-split": ["import:sklearn", "call:train_test_split"],
    "model-fit": ["import:sklearn", "call:LogisticRegression", "method:fit", "method:predict"],
    "accuracy": ["import:sklearn", "call:accuracy_score"],
    "compare-experiments": ["import:sklearn", "call:LogisticRegression"],
    "record-experiments": ["call:max"],
    "validate-submission": ["node:Compare"],
}

# problem_id -> extra requirements merged on top of its concept's own list.
PROBLEM_OVERRIDES: dict[str, list] = {
    "p5-mini-discount-total": ["node:FunctionDef:vararg"],
    "p1-compare-c": ["kwarg:C"],
}

# problem_id -> requirements that fully replace its concept's own list —
# for a "mini" that shares a concept_id but doesn't actually use that
# concept's defining construct (e.g. this one uses string methods, not
# the f-string the rest of "fstring-and-functions" is about).
PROBLEM_REPLACEMENTS: dict[str, list] = {
    "p5-mini-string-functions": ["method:strip", "method:replace"],
}


def compute_required(problem: dict) -> list:
    if problem["id"] in PROBLEM_REPLACEMENTS:
        return list(PROBLEM_REPLACEMENTS[problem["id"]])
    base = REQUIRED_BY_CONCEPT.get(problem["concept_id"], [])
    extra = PROBLEM_OVERRIDES.get(problem["id"], [])
    combined = list(base)
    for r in extra:
        if r not in combined:
            combined.append(r)
    return combined
