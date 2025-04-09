from mcp.server.fastmcp import FastMCP
import sys


from tools import (
    fastqc_tool,
    salmon_index_tool,
    salmon_quantify_tool,
    read_directory_tool,
    read_file_lines_tool,
)


mcp = FastMCP("biotools")
print("Created MCP server", file=sys.stderr)


@mcp.tool()
async def get_fastqc(input_file: str, output_dir: str) -> str:
    """
    Perform quality control using FastQC on FASTQ files.

    Args:
        input_file: Path to the FASTQ file
        output_dir: Directory where FastQC results will be stored
    """
    try:
        result = fastqc_tool(input_file, output_dir)
        if result["returncode"] == 0:
            return (
                f"FastQC analysis completed successfully. "
                f"Results stored in {output_dir}"
            )
        else:
            return f"Error running FastQC: {result['stderr']}"
    except Exception as e:
        print(f"Error in get_fastqc: {str(e)}", file=sys.stderr)
        return f"Error running FastQC: {str(e)}"


@mcp.tool()
async def create_salmon_index(transcript_fasta: str, index_dir: str) -> str:
    """
    Create a Salmon index from a transcript FASTA file.

    Args:
        transcript_fasta: Path to the transcript FASTA file
        index_dir: Directory where the Salmon index will be created
    """
    try:
        result = salmon_index_tool(transcript_fasta, index_dir)
        if result["returncode"] == 0:
            return f"Salmon index created successfully in {index_dir}"
        else:
            return f"Error creating Salmon index: {result['stderr']}"
    except Exception as e:
        print(f"Error in create_salmon_index: {str(e)}", file=sys.stderr)
        return f"Error creating Salmon index: {str(e)}"


@mcp.tool()
async def quantify_with_salmon(index_dir: str, reads: str, output_dir: str) -> str:
    """
    Quantify transcript abundances using Salmon.

    Args:
        index_dir: Path to the Salmon index directory
        reads: Path to the FASTQ reads file
        output_dir: Directory where the quantification results will be stored
    """
    try:
        result = salmon_quantify_tool(index_dir, reads, output_dir)
        if result["returncode"] == 0:
            return (
                f"Salmon quantification completed successfully. "
                f"Results stored in {output_dir}"
            )
        else:
            return f"Error running Salmon quantification: {result['stderr']}"
    except Exception as e:
        print(f"Error in quantify_with_salmon: {str(e)}", file=sys.stderr)
        return f"Error running Salmon quantification: {str(e)}"


@mcp.tool()
async def list_directory(directory_path: str) -> str:
    """
    List files and directories within a specified directory path.

    Args:
        directory_path: Path to the directory to read
    """
    try:
        return read_directory_tool(directory_path)
    except Exception as e:
        print(f"Error in list_directory: {str(e)}", file=sys.stderr)
        return f"Error listing directory: {str(e)}"


@mcp.tool()
async def read_file_lines(file_path: str) -> str:
    """
    Read lines from a specified file.

    Args:
        file_path: Path to the file to read
    """
    try:
        result = read_file_lines_tool(file_path)
        if isinstance(result, str) and not result.startswith("Error"):
            return result  # Return the file content
        else:
            return f"Error reading file: {result}"
    except Exception as e:
        print(f"Error in read_file_lines: {str(e)}", file=sys.stderr)
        return f"Error reading file: {str(e)}"


if __name__ == "__main__":
    try:
        print("Starting MCP server with stdio transport...", file=sys.stderr)
        mcp.run(transport="stdio")
        print("Bioinformatics tools MCP server started!", file=sys.stderr)
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}", file=sys.stderr)
        sys.exit(1)
