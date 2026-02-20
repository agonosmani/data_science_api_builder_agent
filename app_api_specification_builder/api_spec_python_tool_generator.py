import json
import re
from pathlib import Path


INPUT_FILE = "data/api_data_specifications.json"
OUTPUT_FILE = "agent_api_executor/api_executor_agent.py"


def to_snake_case(name: str) -> str:
    name = re.sub(r"[^\w\s]", "", name)
    name = name.strip().lower().replace(" ", "_")
    return name


def map_json_type_to_python(param_type: str) -> str:
    mapping = {
        # String types
        "string": "str",
        "str": "str",
        "text": "str",
        "varchar": "str",
        "char": "str",

        # Numeric types
        "number": "float",
        "float": "float",
        "double": "float",
        "numeric": "float",
        "real": "float",

        "integer": "int",
        "int": "int",
        "bigint": "int",
        "smallint": "int",

        # Boolean types
        "boolean": "bool",
        "bool": "bool",
    }
    return mapping.get(param_type, "str")


def generate_function(api: dict, endpoint: dict) -> str:
    api_name = api["name"]
    api_description = api.get("description", "")
    base_url = api["base_url"]

    func_name = to_snake_case(endpoint["name"])
    uri = endpoint["uri"]
    method = endpoint["method"].upper()
    endpoint_description = endpoint.get("description", "")

    parameters = endpoint.get("parameters", [])

    # ---- Build function signature ----
    param_defs = []
    param_docs = []
    param_names = []

    for param in parameters:
        name = param["name"]
        required = param.get("required", False)
        py_type = map_json_type_to_python(param["type"])
        description = param.get("description", "")

        if required:
            param_defs.append(f"{name}: {py_type}")
        else:
            param_defs.append(f"{name}: {py_type} | None = None")

        param_docs.append(f"{name}: {description}")
        param_names.append(name)

    params_signature = ",\n    ".join(param_defs)

    # ---- Build params dict ----
    params_dict = "\n    ".join(
        [f'if {p} is not None:\n        params["{p}"] = {p}' for p in param_names]
    )

    # ---- Build full docstring ----
    full_docstring = f"""{api_name}

{api_description}

Endpoint: {endpoint_description}

Parameters:
{chr(10).join(param_docs) if param_docs else "None"}
"""

    function_code = f"""
@api_executor_agent.tool
async def {func_name}(
    ctx: RunContext,
    {params_signature if params_signature else ""}
) -> Any:
    \"\"\"{full_docstring}\"\"\"

    url = f"{base_url}{uri}"
    params = {{}}

    {params_dict if params_dict else ""}

    async with httpx.AsyncClient() as client:
        response = await client.request("{method}", url, params=params)

    try:
        return response.json()
    except Exception:
        return response.text
"""

    return function_code



def generate_python_tool_all():
    with open(INPUT_FILE, "r") as f:
        api_specs = json.load(f)

    output = ""

    for api in api_specs:
        output += f"\n\n# === {api['name']} ===\n"

        for endpoint in api["endpoints"]:
            output += generate_function(api, endpoint) + "\n"

    with open("executor_python_template.txt", "r") as f:
        template = f.read()

    output = template + output

    with open(OUTPUT_FILE, "w") as f:
        f.write(output)

    print(f"✅ Generated tools written to {OUTPUT_FILE}")



def generate_python_tool_latest():
    with open(INPUT_FILE, "r") as f:
        api_specs = json.load(f)
    
    api_spec = api_specs[-1]

    output = f"\n\n# === {api_spec['name']} ===\n"

    for endpoint in api_spec["endpoints"]:
        output += generate_function(api_spec, endpoint) + "\n"

    # Append to the output file instead of overwriting
    with open(OUTPUT_FILE, "a") as f:
        f.write(output)

    print(f"✅ Appended latest API tools to {OUTPUT_FILE}")



if __name__ == "__main__":
    generate_python_tool_all()
    # generate_python_tool_latest()
