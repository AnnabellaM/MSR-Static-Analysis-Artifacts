import datetime

FRAMEWORK_SPECIFIC_WORDS = [
    'wala',
    'soot',
    'opal',
    'flowdroid',
    'phasar',
    'sootup',
    'infer',
    'doop',
    'amandroid',
    'tajs',
    'code2flow',
    'pycg',
    'droidsafe',
    'cbmc',
]

LANGUAGE_SPECIFIC_WORDS = [
    'python',
    '.py',
    'java',
    '.c',
    '.cpp',
    'c++',
    'javascript',
    '.js',
    'ruby',
    '.rb',
    'php'
]

TOOLS_ORDER = [
    'Soot',
    'SootUp',
    'WALA',
    'DOOP',
    'OPAL',
    'SpotBugs',
    'FlowDroid',
    'Amandroid',
    'DroidSafe',
    'Phasar',
    'CBMC',
    'SCS',
    'PyCG',
    'Code2Flow',
    'TAJS',
    'PHPStan',
    'Infer',
    'PMD',
]

GROUPS_ORDER = [
    'Language Features',
    'Unsupported Framework/Library',
    'Static Analysis Tasks',
    'Tool Capabilities',
    'Software Artifacts',
    'Build Issues',
    'Performance and Usability',
    'Maintenance Tasks',
    'No Group'
]

GROUP_ACRONYMS = {
    'Language Features': 'LF',
    'Unsupported Framework/Library': 'UFL',
    'Static Analysis Tasks': 'SAT',
    'Tool Capabilities': 'TC',
    'Software Artifacts': 'SA',
    'Build Issues': 'BI',
    'Performance and Usability': 'PU',
    'Maintenance Tasks': 'MT',
    'No Group': 'NG'
}

GROUP_TOPIC_MAPPING = {
    "Language Features": [
        "Unused Imports", "Annotation", "Property", "Inheritance", "Loops", "Iterables",
        "Constants", "Closures", "Reflections", "Callables", "Generic Types", "List",
        "Array Handling", "Stubs Related", "Try-with-resources (Java)", "Yield",
        "ImmutableField", "Ternary Operator", "Strict Comparison"
    ],
    "Unsupported Framework/Library": [
        "DateFormat", "XPath", "Apex", "Explode()", "Lombok", "setCookie()",
        "curl API", "DOM", "json API", "XML"
    ],
    "Static Analysis Tasks": [
        "Type Inference", "Nullability Analysis", "Exposure Check", "Taint Analysis",
        "IR", "Call Graph", "Code Slicing"
    ],
    "Tool Capabilities": [
        "Class Loading", "(Android) Instrumentation", "Rule Definitions", "Template Issues",
        "Error Management", "Parsing Errors", "Unexpected Results", "Missing Results",
        "Exception Handling", "IDE Plugin", "Multi-Language Support", "Language Version Support"
    ],
    "Software Artifacts": [
        "Documentation", "Logs", "Config Files", "Test Suites"
    ],
    "Build Issues": [
        "Docker", "Build System", "Compilation", "Dependency"
    ],
    "Performance and Usability": [
        "Memory", "Speed", "Usability Issues"
    ],
    "Maintenance Tasks": [
        "New Release", "Cleanup Deprecations", "Error Messages Refinement", "Output Format"
    ]
}

DATA_DOWNLOAD_DATE = datetime.datetime(2025, 6, 2)