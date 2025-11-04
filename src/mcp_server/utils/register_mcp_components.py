import importlib
import inspect
from pathlib import Path

def register_mcp_components(mcp_instance, base_dir: Path):
    """
    Auto-discover and register all MCP components (tools, prompts, resources).
    
    This function automatically registers all three types of MCP components
    in one call by scanning the standard directories for modules with
    registration functions (functions that start with 'register_').
    
    Args:
        mcp_instance: The FastMCP server instance
        base_dir: The base directory of the mcp_server package (usually Path(__file__).parent)
    
    Example:
        >>> from pathlib import Path
        >>> base_dir = Path(__file__).parent
        >>> register_mcp_components(mcp, base_dir)
        🔍 Auto-discovering and registering MCP components...
        ✅ Registered: mcp_server.tools.itinerary.register_itinerary_tools
        ✅ Registered: mcp_server.prompts.travel_prompts.register_travel_prompts
        ✅ Registered: mcp_server.resources.weather.register_weather_resources
        ✨ All MCP components registered!
    """
    print("🔍 Auto-discovering and registering MCP components...")
    
    # Define component directories and their module prefixes
    components = [
        (base_dir / "tools", "mcp_server.tools"),
        (base_dir / "prompts", "mcp_server.prompts"),
        (base_dir / "resources", "mcp_server.resources"),
    ]
    
    # Scan and register each component type
    for component_dir, module_prefix in components:
        if not component_dir.exists():
            continue
        
        # Find all Python files except __init__.py and private modules
        for file_path in component_dir.glob("*.py"):
            if file_path.name.startswith("_"):
                continue
            
            module_name = file_path.stem
            full_module_path = f"{module_prefix}.{module_name}"
            
            try:
                # Import the module
                module = importlib.import_module(full_module_path)
                
                # Look for registration functions (functions that start with 'register_')
                for name, obj in inspect.getmembers(module):
                    if (inspect.isfunction(obj) and 
                        name.startswith('register_') and 
                        obj.__module__ == full_module_path):
                        # Call the registration function
                        obj(mcp_instance)
                        print(f"✅ Registered: {full_module_path}.{name}")
            except Exception as e:
                print(f"⚠️  Warning: Could not register {full_module_path}: {e}")
    
    print("✨ All MCP components registered!")