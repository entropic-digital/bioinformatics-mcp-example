1. Build docker stuff
```bash
docker build -t biotools-mcp .
```
2. To run the MCP server
```bash
docker run -it --rm \
    -v /Users/dionizijefa/Documents/entropic-dev/bioinformatics-mcp/data:/data \
    biotools-mcp
```
3. Add it to claude_desktop_config.json
claude_desktop_config.json
```
{
  "mcpServers": {
    "biotools-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "/Users/dionizijefa/Documents/entropic-dev/bioinformatics-mcp/data:/data",
        "biotools-mcp"
      ]
    }
  }
}
```

