import sys
import asyncio
import json
from pydantic import AnyUrl
from typing import Optional, Any
from contextlib import AsyncExitStack
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client


class MCPClient:
    def __init__(
        self,
        server_url: str,
    ):
        self._server_url = server_url
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

    async def connect(self):
        streamable_transport = await self._exit_stack.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        _read, _write, _get_session_id = streamable_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_read, _write)
        )
        print('session', self._session)
        await self._session.initialize()

    def session(self) -> ClientSession:
        if self._session is None:
            raise ConnectionError(
                "Client session not initialized or cache not populated. Call connect_to_server first."
            )
        return self._session

    async def list_tools(self) -> types.ListToolsResult | list[types.Tool]:
        #  Return a list of tools defined by the MCP server
        result = await self.session().list_tools()
        return result.tools

    async def call_tool(
        self, tool_name: str, tool_input: dict
    ) -> types.CallToolResult | None:
        # TODO: Call a particular tool and return the result
        response =  await self.session().call_tool(tool_name, tool_input)
        return response

    async def list_prompts(self) -> list[types.Prompt]:
        # TODO: Return a list of prompts defined by the MCP server
        return []

    async def get_prompt(self, prompt_name, args: dict[str, str]):
        # TODO: Get a particular prompt defined by the MCP server
        return []
    
    async def list_resources(self)-> list[types.Resource]:
        assert self._session, "Session not available."
        result: types.ListResourcesResult = await self.session().list_resources()
        return result.resources
    
    async def list_resource_templates(self) -> list[types.ResourceTemplate]:
        assert self._session, "Session not available."
        result: types.ListResourceTemplatesResult = await self.session().list_resource_templates()
        return result.resourceTemplates
    
    async def read_resource(self, uri:str)-> types.ReadResourceResult:
        assert self._session, "Session not available."
        result = await self.session().read_resource(AnyUrl(uri))
        resource = result.contents[0]

        if isinstance(resource, types.TextResourceContents):
            if resource.mimeType == 'application/json':
                try:
                    return json.loads(resource.text)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")  
        
        return resource.text

    async def cleanup(self):
        await self._exit_stack.aclose()
        self._session = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()

# ----------------------------------------------------------------------
# MCP Lifecycle Overview:
# This MCPClient class adheres to the MCP lifecycle for robust connection management.
# - Initialization: The connect() method sets up the client session.
# - Operation: Core functions like list_tools() and call_tool() enable tool invocations.
# - Shutdown: The cleanup() method ensures the connection is gracefully closed.
#
# To test your implementation, run main.py to start the chat agent and see your tools in action.
# ----------------------------------------------------------------------

# For testing
async def main():
    async with MCPClient(
        server_url="http://localhost:8000/mcp/",
    ) as _client:
        # print("\n List Tools")
        # tools_list = await _client.list_tools()
        # print(tools_list)
        # print("\n==================================")
        # print("\n Call Read Document Tool")
        # doc_content= await _client.call_tool('read_doc_content', {'doc_id':'report.pdf'})
        # print(doc_content)

        # Resources
        resources = await _client.list_resources()
        print(resources[0].uri, " resources")

        # data = await _client.read_resource(resources[0].uri)
        # print(data, " data")

        # multiple static resources
        # for r in resources:
        #     print(f"Resource URI: {r.uri}")
        #     data = await _client.read_resource(r.uri)
        #     print(f"Data: {data}")

        # template = await _client.list_resource_templates()
        # print('templates: ', template)
        # intro_uri = template[0].uriTemplate.replace("{doc_id}", "spec.txt")
        # data = await _client.read_resource(intro_uri)
        # print("Intro Document:", data)



if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
