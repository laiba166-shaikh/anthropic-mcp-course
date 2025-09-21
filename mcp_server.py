from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", stateless_http=True)

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

#  Write a tool to read a doc
@mcp.tool(name='read_doc_content', description="Read the content of the requested document.")
def read_doc(doc_id: str) -> str:
    if doc_id not in docs.keys():
        raise ValueError(f"Document with id {doc_id} is not found")
    return docs[doc_id]

#  Write a tool to edit a doc
@mcp.tool(name='update_doc_content', description="Update the content of the document by the content that is passed.")
def update_doc(doc_id: str, content: str) -> str:
    if doc_id not in docs.keys():
        raise ValueError(f"Document with id {doc_id} is not found")
    
    docs[doc_id] = docs[doc_id] = content
    return "Successfully updated the document"

# TODO: Write a resource to return all doc id's
@mcp.resource("docs://documents", mime_type='application/json')
def list_docs()-> list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
# template resource
@mcp.resource('docs://{doc_id}', mime_type='text/plain')
def get_doc(doc_id: str)-> str:
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc

mcp_app = mcp.streamable_http_app()