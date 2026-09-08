"""Verify the real MCP handshake and read the open Blender scene."""
import asyncio
import json
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]

async def main():
    params = StdioServerParameters(
        command=str(ROOT / 'integrations/blender-mcp-env/bin/blender-mcp'),
        env={'DISABLE_TELEMETRY': 'true', 'BLENDER_HOST': '127.0.0.1', 'BLENDER_PORT': '9876'},
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as client:
            initialized = await client.initialize()
            listing = await client.list_tools()
            names = [t.name for t in listing.tools]
            assert 'get_scene_info' in names
            result = await client.call_tool('get_scene_info', {'user_prompt': 'Verify Blender MCP installation by reading the current scene.'})
            if result.isError:
                raise RuntimeError(result.model_dump_json())
            report = {'server': initialized.serverInfo.model_dump(),
                      'tool_count': len(names), 'tools': names,
                      'scene_result': result.model_dump(mode='json')}
            out = ROOT / 'output/setup_check/mcp_report.json'
            out.write_text(json.dumps(report, indent=2) + '\n')
            print(json.dumps(report, indent=2))

asyncio.run(main())
