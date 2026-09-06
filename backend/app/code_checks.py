"""Structural checks on submitted code, on top of output-only grading.

Comparing stdout alone lets a learner "pass" by hardcoding the literal
expected output instead of writing the logic a problem is meant to
teach (e.g. printing "합: 8" instead of defining add/subtract/multiply
functions). This module inspects the submitted code's AST once and
answers yes/no questions like "did this define a function", "did this
call input()", "did this use a for-loop" — cheap, deterministic checks
that don't need to understand *whether* the logic is correct (output
matching already does that), only whether the *intended technique* was
used at all.

A requirement is a string "kind:value" (e.g. "node:For", "call:input",
"method:sort", "op:Mod", "import:math", "attr:shape", "kwarg:axis"), or
a tuple of such strings meaning "at least one of these" (OR).
"""

import ast

Requirement = str | tuple[str, ...]


class CodeFeatures:
    """One pass over a parsed AST, collecting everything the requirement
    checks below might ask about."""

    def __init__(self, code: str):
        self.node_types: set[str] = set()
        self.calls: set[str] = set()  # direct calls: input(), int(), max(), sorted()...
        self.methods: set[str] = set()  # dotted calls: x.sort(), np.array(), df.groupby()...
        self.attrs: set[str] = set()  # dotted access without a call: df.iloc, df.shape...
        self.ops: set[str] = set()  # operator class names: Add, Mod, And, In, BitAnd...
        self.imports: set[str] = set()  # top-level module names: math, numpy, pandas...
        self.kwargs: set[str] = set()  # keyword argument names used anywhere: axis, key, C...

        tree = ast.parse(code)
        for node in ast.walk(tree):
            self.node_types.add(type(node).__name__)

            if isinstance(node, ast.Attribute):
                self.attrs.add(node.attr)

            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    self.calls.add(func.id)
                elif isinstance(func, ast.Attribute):
                    self.methods.add(func.attr)
                for kw in node.keywords:
                    if kw.arg:
                        self.kwargs.add(kw.arg)

            if isinstance(node, ast.BinOp):
                self.ops.add(type(node.op).__name__)
            if isinstance(node, ast.BoolOp):
                self.ops.add(type(node.op).__name__)
            if isinstance(node, ast.UnaryOp):
                self.ops.add(type(node.op).__name__)
            if isinstance(node, ast.AugAssign):
                self.ops.add(type(node.op).__name__)
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    self.ops.add(type(op).__name__)

            if isinstance(node, (ast.Import, ast.ImportFrom)):
                module = getattr(node, "module", None)
                if module:
                    self.imports.add(module.split(".")[0])
                for alias in getattr(node, "names", []):
                    self.imports.add(alias.name.split(".")[0])

            if isinstance(node, ast.FunctionDef):
                if node.args.defaults or node.args.kw_defaults:
                    self.node_types.add("FunctionDef:default")
                if node.args.vararg is not None:
                    self.node_types.add("FunctionDef:vararg")

            if isinstance(node, ast.Try) and node.finalbody:
                self.node_types.add("Try:finally")

    def satisfies(self, requirement: str) -> bool:
        kind, _, value = requirement.partition(":")
        return {
            "node": value in self.node_types,
            "call": value in self.calls,
            "method": value in self.methods,
            "attr": value in self.attrs,
            "op": value in self.ops,
            "import": value in self.imports,
            "kwarg": value in self.kwargs,
        }.get(kind, False)


# kind:value -> Korean label shown to the learner when it's missing.
_LABELS: dict[str, str] = {
    "node:For": "for 반복문", "node:While": "while 반복문", "node:If": "조건문(if)",
    "node:IfExp": "삼항 표현식(if-else)", "node:Assign": "변수 할당(=)",
    "node:Subscript": "인덱싱/슬라이싱([ ])", "node:ListComp": "리스트 컴프리헨션",
    "node:FunctionDef": "함수 정의(def)", "node:FunctionDef:default": "기본값 매개변수",
    "node:FunctionDef:vararg": "가변 인자(*args)", "node:Return": "return문",
    "node:Lambda": "람다(lambda)", "node:Try": "try/except", "node:Try:finally": "finally 블록",
    "node:ClassDef": "클래스 정의(class)", "node:Pass": "pass문", "node:Break": "break문",
    "node:Compare": "비교 연산자", "node:JoinedStr": "f-string",
    "call:input": "input()", "call:int": "int()", "call:float": "float()",
    "call:set": "set()", "call:max": "max()", "call:open": "open()",
    "call:train_test_split": "train_test_split()", "call:LogisticRegression": "LogisticRegression()",
    "call:accuracy_score": "accuracy_score()",
    "method:sort": ".sort()", "method:count": ".count()", "method:get": ".get()",
    "method:keys": ".keys()", "method:values": ".values()", "method:items": ".items()",
    "method:write": ".write()", "method:read": ".read()", "method:array": "np.array()",
    "method:sum": ".sum()", "method:mean": ".mean()", "method:max": ".max()", "method:min": ".min()",
    "method:zeros": "np.zeros()", "method:eye": "np.eye()", "method:ones": "np.ones()",
    "method:Series": "pd.Series()", "method:DataFrame": "pd.DataFrame()",
    "method:isna": ".isna()", "method:isnull": ".isnull()", "method:fillna": ".fillna()",
    "method:groupby": ".groupby()", "method:sort_values": ".sort_values()", "method:isin": ".isin()",
    "method:describe": ".describe()", "method:value_counts": ".value_counts()", "method:agg": ".agg()",
    "method:to_csv": ".to_csv()", "method:read_csv": "pd.read_csv()", "method:head": ".head()",
    "method:astype": ".astype()", "method:cut": "pd.cut()", "method:map": ".map()",
    "method:fit": ".fit()", "method:predict": ".predict()",
    "method:strip": ".strip()", "method:replace": ".replace()",
    "attr:iloc": ".iloc", "attr:loc": ".loc", "attr:shape": ".shape",
    "op:Add": "+ 연산자", "op:Mod": "% 연산자", "op:FloorDiv": "// 연산자", "op:Pow": "** 연산자",
    "op:And": "and 연산자", "op:Or": "or 연산자", "op:Not": "not 연산자",
    "op:In": "in 연산자", "op:NotIn": "not in 연산자",
    "op:BitAnd": "& 연산자", "op:BitOr": "| 연산자", "op:Sub": "- 연산자",
    "import:math": "math 모듈", "import:numpy": "numpy", "import:pandas": "pandas",
    "import:sklearn": "scikit-learn",
    "kwarg:axis": "axis 인자", "kwarg:key": "key 인자", "kwarg:C": "C 인자",
}


def _label(requirement: str) -> str:
    return _LABELS.get(requirement, requirement)


def check_required_constructs(code: str, requirements: list[Requirement]) -> list[str]:
    """Returns Korean labels for the requirements NOT met — empty means
    everything required was used. An OR-group survives a JSON round-trip
    as a plain list (JSON has no tuple), so both tuple and list are
    treated as "at least one of these"."""
    try:
        features = CodeFeatures(code)
    except SyntaxError:
        return [
            _label(r) if isinstance(r, str) else " 또는 ".join(_label(alt) for alt in r)
            for r in requirements
        ]

    missing = []
    for r in requirements:
        if isinstance(r, (tuple, list)):
            if not any(features.satisfies(alt) for alt in r):
                missing.append(" 또는 ".join(_label(alt) for alt in r))
        else:
            if not features.satisfies(r):
                missing.append(_label(r))
    return missing
