"""
Create Gradle Tasks Automatically.
"""

import re

import config
from directories import exists


def make_task(task_name, package_name=None):
    if package_name:
        main = f"{package_name}.{task_name}"
    else:
        main = task_name
    return (
        task_name,
        f"""
task {task_name}(type: JavaExec) {{
    classpath javaClassPath
    main = '{main}'
}}
""",
    )


def create_tasks():
    tasks = """
def javaClassPath = sourceSets.main.runtimeClasspath

"""
    task_dict = {}
    print("Creating tasks.gradle ...")
    print(exists(config.example_dir))
    for java_file in config.example_dir.rglob("*.java"):
        text = java_file.read_text()
        lines = text.splitlines()
        if not re.search(r"public\s+static\s+void\s+main", text):
            continue
        package_name = None
        for line in lines:
            if line.startswith("package "):
                package_name = line.split()[1][:-1]
        k, v = make_task(java_file.stem, package_name)
        task_dict[k] = v
    for k in sorted(task_dict):
        tasks += task_dict[k]
    tasks += """
task run (dependsOn: [
"""
    for k in sorted(task_dict):
        tasks += f"    '{k}',\n"
    tasks = tasks[:-1]  # Strip last comma
    tasks += """
    ]) {
    doLast {
        println '*** run complete ***'
    }
}
"""
    (config.example_dir / "gradle" / "tasks.gradle").write_text(tasks)
    print(f"{len(task_dict)} tasks")
