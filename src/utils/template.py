from jinja2 import Template

def format(path: str, data: dict[any, any]) -> str:
    # Read contents of template file.
    try:
        with open(path) as f:
            tpl_contents = f.read()
    except Exception as e:
        raise Exception(f"Failed to open or read template path ({path}): {e}")
    
    # Generate template.
    try:
        tpl = Template(tpl_contents)
    except Exception as e:
        raise Exception(f"Failed to generate template: {e}")
    
    # Render template.
    try:
        ret = tpl.render(data)
    except Exception as e:
        raise Exception(f"Failed to render template: {e}")
    
    return ret
    