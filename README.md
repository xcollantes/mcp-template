# MCP Template

MY_MCP_DESCRIPTION

## Template Setup

*Remove the Template Setup section after you have replaced all the variables.*

Find All and Replace these variables throughout the project:

| Variable | Description | Example |
|----------|-------------|---------|
| `TODO` | General placeholders |  |
| `MY_MCP_NAME` | Human-readable name | `Weather MCP` |
| `MY_MCP_DESCRIPTION` | One-liner description | `MCP server for interacting with the Weather API.` |
| `MY_MCP_REPO_URL` | Full GitHub repo URL | `https://github.com/xcollantes/weather-mcp` |
| `MY_MCP_PACKAGE_NAME` | Package name for CLI/binaries | `weather-mcp` |
| `MY_MCP_SERVER_KEY` | Key in mcpServers JSON config | `weather` |
| `MY_MCP_ENV_VAR_PREFIX` | Prefix for environment variables | `WEATHER` |
| `MY_MCP_AUTHOR` | Author name for LICENSE | `Xavier Collantes` |

**See more under [Development](#development) section for CI/CD, formatting,
tests, logging, and setup for pre-commit hooks.**

## Installation

### Install MY_MCP_NAME

MY_MCP_NAME requires no additional dependencies to be installed.

TODO: Add any additional installation instructions for your MCP server. For
example, many MCPs may use the CLI tool.

### MCP Server: Option 1: Download binaries (Recommended)

Download the latest release for your operating system from the [Releases
page](MY_MCP_REPO_URL/releases).

| Operating System | Binary |
|------------------|--------|
| Linux | `MY_MCP_PACKAGE_NAME-linux` |
| Windows | `MY_MCP_PACKAGE_NAME-windows.exe` |
| macOS (Apple Silicon) | `MY_MCP_PACKAGE_NAME-macos-apple-silicon-arm64` |
| macOS (Intel) | `MY_MCP_PACKAGE_NAME-macos-x64` |

#### Linux

```bash
# Download the binary.
curl -L -o MY_MCP_PACKAGE_NAME-linux MY_MCP_REPO_URL/releases/latest/download/MY_MCP_PACKAGE_NAME-linux

# Make it executable.
chmod +x MY_MCP_PACKAGE_NAME-linux

# Move to a directory in your PATH (optional).
sudo mv MY_MCP_PACKAGE_NAME-linux /usr/local/bin/
```

Add to your LLM client configuration:

**NOTE:** Make sure to replace `/usr/local/bin/MY_MCP_PACKAGE_NAME-linux` with
the path to the binary on your machine if you moved it to a different location.

```json
{
  "mcpServers": {
    "MY_MCP_SERVER_KEY": {
      "command": "/usr/local/bin/MY_MCP_PACKAGE_NAME-linux"
    }
  }
}
```

#### macOS

```bash
# For Apple Silicon (M1/M2/M3).
curl -L -o MY_MCP_PACKAGE_NAME MY_MCP_REPO_URL/releases/latest/download/MY_MCP_PACKAGE_NAME-macos-apple-silicon-arm64

# For Intel Macs.
curl -L -o MY_MCP_PACKAGE_NAME MY_MCP_REPO_URL/releases/latest/download/MY_MCP_PACKAGE_NAME-macos-x64

# Make it executable.
chmod +x MY_MCP_PACKAGE_NAME

# Move to a directory in your PATH (optional).
sudo mv MY_MCP_PACKAGE_NAME /usr/local/bin/
```

**Note:** macOS may block the binary on first run. If you see a security
warning, go to **System Settings > Privacy & Security** and click **Allow
Anyway**, or run:

```bash
xattr -d com.apple.quarantine /usr/local/bin/MY_MCP_PACKAGE_NAME
```

Add to your LLM client configuration:

**NOTE:** Make sure to replace `/usr/local/bin/MY_MCP_PACKAGE_NAME` with the
path to the binary on your machine if you moved it to a different location.

```json
{
  "mcpServers": {
    "MY_MCP_SERVER_KEY": {
      "command": "/usr/local/bin/MY_MCP_PACKAGE_NAME"
    }
  }
}
```

#### Windows

1. Download `MY_MCP_PACKAGE_NAME-windows.exe` from the [Releases
   page](MY_MCP_REPO_URL/releases).
2. Move the executable to a convenient location (e.g., `C:\Program
   Files\MY_MCP_PACKAGE_NAME\`).

Add to your LLM client configuration:

```json
{
  "mcpServers": {
    "MY_MCP_SERVER_KEY": {
      "command": "C:\\Program Files\\MY_MCP_PACKAGE_NAME\\MY_MCP_PACKAGE_NAME-windows.exe"
    }
  }
}
```

**NOTE:** Make sure to replace `C:\\Program
Files\\MY_MCP_PACKAGE_NAME\\MY_MCP_PACKAGE_NAME-windows.exe` with the path to
the binary on your machine if you moved it to a different location.

### MCP Server: Option 2: Development setup with uv

Get repo:

```bash
git clone MY_MCP_REPO_URL.git
cd MY_MCP_PACKAGE_NAME
```

Add MCP server to your choice of LLM client:

**NOTE:** You will need to look up for your specific client on how to add MCPs.

Usually the JSON file for the LLM client will look like this:

```json
{
  "mcpServers": {
    "MY_MCP_SERVER_KEY": {
      "command": "uv",
      "args": ["--directory", "/ABSOLUTE/PATH/TO/REPO/ROOT", "run", "python", "-m", "src.main"]
    }
  }
}
```

This will tell your LLM client application that there's a tool that can be
called by calling `uv --directory /ABSOLUTE/PATH/TO/REPO run python -m
src.main`.

Install UV: <https://docs.astral.sh/uv/getting-started/installation/>

### MCP Server: Option 3: Install globally with pipx

```bash
# Install pipx if you haven't already.
brew install pipx
pipx ensurepath

# Clone and install the MCP server.
git clone MY_MCP_REPO_URL.git
cd MY_MCP_PACKAGE_NAME
pipx install -e .
```

## How it works

1. You enter some questions or prompt to a LLM Client such as the Claude
   Desktop, Cursor, Windsurf, or ChatGPT.
2. The client sends your question to the LLM model (Sonnet, Grok, ChatGPT)
3. LLM analyzes the available tools and decides which one(s) to use
   - The LLM you're using will have a context of the tools and what each tool is
     meant for in human language.
   - Alternatively without MCPs, you could include in the prompt the endpoints
     and a description on each endpoint for the LLM to "call on". Then you could
     copy and paste the text commands into the terminal on your machine.
   - MCPs provide a more deterministic and standardized method on LLM-to-server
     interactions.
4. The client executes the chosen tool(s) through the MCP server.
   - The MCP server is either running local on your machine or an endpoint
     hosting the MCP server remotely.
5. The results are sent back to LLM.
6. LLM formulates a natural language response and one or both of the following
   happen:
   - The response is displayed to you with data from the MCP server
   - Some action is performed using the MCP server

## Development

### Testing In Cursor/Windsurf

To test the MCP server in Cursor/Windsurf, you can use the MCP client to test
the MCP server.

Add this to the MCP client configuration in Cursor/Windsurf:

```json
{
  "mcpServers": {
    "MY_MCP_SERVER_KEY": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/REPO/ROOT",
        "run",
        "python",
        "-m",
        "src.main",
        "--debug"
      ]
    }
  }
}
```

This will start the MCP server and you can then use the MCP server in
Cursor/Windsurf. You may need to restart in the MCP settings to see the changes.

### CI/CD

Setup for CI/CD to build and release the MCP server on multiple operating
systems and architectures.

- The `.github/workflows/ci.yml` file is used to run the tests and linting
  checks.
- The `.github/workflows/release.yml` file is used to build and release the MCP
server on multiple operating systems and architectures.
  - Tag the release with the format `vX.X.X`.
  - The release will be built and released to the Releases page on your GitHub
    repository.

### Formatting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and
formatting. The `.pre-commit-config.yaml` file is used to run the linting and
formatting checks before each commit.

To set up pre-commit hooks:

```bash
uv sync
uv run pre-commit install
```

Once installed, ruff will automatically run when you commit. To run checks
manually on all files:

```bash
uv run pre-commit run --all-files
```

NOTE: A developer can skip installing pre-commit hook and formatting checks but
the CI/CD workflow will fail if the checks are not passed.

### Tests

This project uses [pytest](https://docs.pytest.org/) for testing. The `tests`
directory is used to store the test files.

To run the tests:

```bash
uv run pytest
```

To run the tests with coverage:

```bash
uv run pytest --cov=src
```

### Logging

Do not use `print` statements for logging. Use the logging module instead.
Writing to stdout will corrupt the JSON-RPC messages and break your server.

### Pre-commit

This project uses [pre-commit](https://pre-commit.com/) to run
[ruff](https://docs.astral.sh/ruff/) linting and formatting checks, and
[pytest](https://docs.pytest.org/) tests before each commit.

To set up pre-commit hooks:

```bash
uv sync
uv run pre-commit install
```

Once installed, ruff and pytest will automatically run when you commit. To run
checks manually on all files:

```bash
uv run pre-commit run --all-files
```

## Docstrings / Tool decorator parameters

MCP.tools decorator parameters are especially important as this is the human
readable text that the LLM has context of. This will be treated as part of the
prompt when fed to the LLM and this will decide when to use each tool.

## Architecture

MCP follows a client-server architecture where an **MCP host** (an AI
application like Cursor or ChatGPT desktop) establishes connections to one or
more **MCP servers**. The **MCP host** accomplishes this by creating one **MCP
client** for each **MCP server**. Each MCP client maintains a dedicated
connection with its corresponding MCP server.

<https://modelcontextprotocol.io/docs/learn/architecture>

## Pitfalls / Troubleshooting

### Edit the jira-cli config file

On MacOS:

```text
/Users/<your-username>/.config/.jira/.config.yml
```

### 404 error when using `jira init`

If you get a 404 error when using `jira init`, you may need to edit the jira-cli
config file to point to the correct Jira instance. There are only 3 possible
values for the auth type so try each one. `basic`, `password`, or `bearer`.

### Environment Variables

Make sure to set any required environment variables. Copy `env.example` to
`.env` and fill in the values:

```bash
cp env.example .env
```

### Server Not Starting

If the MCP server is not starting, check:

1. You have Python 3.12+ installed
2. All dependencies are installed (`uv sync`)
3. Environment variables are set correctly
