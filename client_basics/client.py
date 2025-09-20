import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client

URL = "http://localhost:8000/mcp/"

class MCPClient():
    def __init__(self, url):
        self.url =url
        self.stack = AsyncExitStack()
        self._session = None

    async def __aenter__(self):
        # set http connection with client - Connection Manage karna -  Baat cheet ka connection
        read, write, _ = await self.stack.enter_async_context(
            streamablehttp_client(self.url)
        )
        # set session - Session Manage karna
        self._session = await self.stack.enter_async_context(
            ClientSession(read,write)
        )
        # Initialize the session
        await self._session.initialize()
        return self
    
    async def list_tools(self) -> types.Tool:
        # async with self._session as sess:
        response = await self._session.list_tools()
        return response.tools
    
    async def call_tool(self, tool_name, *args, **kwrgs):
        print('args:',*args, 'kwrgs', **kwrgs)
        tool_response = await self._session.call_tool(tool_name, **kwrgs)
        return tool_response

    async def __aexit__(self, *args):
        await self.stack.aclose()
        

async def main():
    async with MCPClient(URL) as client:
        tools = await client.list_tools()
        print('tools:', tools)
        print("\n==================================")
        print("\n Call Read Document Tool")
        doc_content= await client.call_tool('read_doc_content', {'doc_id':'report.pdf'})
        print(doc_content)

asyncio.run(main())
    
