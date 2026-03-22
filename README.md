# rosclaw-g1-dds-mcp

ROSClaw MCP Server for **Unitree G1 Humanoid Robot** via DDS protocol.

Part of the [ROSClaw](https://github.com/ros-claw) Embodied Intelligence Operating System.

## Overview

This MCP server enables LLM agents (Claude, GPT-4, etc.) to control a Unitree G1 humanoid robot through the Model Context Protocol. It communicates with the robot using DDS (Data Distribution Service) — the same protocol used by Unitree's official SDK.

```
LLM Agent  ──MCP──►  rosclaw-g1-dds-mcp  ──DDS──►  Unitree G1
```

## Features

- **Full body control**: 23 joints (legs, waist, arms)
- **High-level actions**: stand, sit, walk, wave hand
- **Safety guards**: joint limits enforced before every command
- **Real-time state**: battery, mode, joint positions, IMU at 100Hz
- **DDS protocol**: CycloneDDS / FastDDS compatible
- **Async design**: non-blocking MCP tools with background state thread

## Hardware

| Field | Value |
|-------|-------|
| Robot | Unitree G1 Humanoid |
| Protocol | DDS (Data Distribution Service) |
| Domain ID | 0 (configurable) |
| State Rate | 100 Hz |
| Topics | `/lowstate`, `/lowcmd`, `/sportmodestate` |

## Installation

```bash
# Clone
git clone https://github.com/ros-claw/rosclaw-g1-dds-mcp.git
cd rosclaw-g1-dds-mcp

# Install with uv (recommended)
uv venv --python python3.10
source .venv/bin/activate
uv pip install -e .

# Or with pip
pip install -e .
```

## Quick Start

### Run as MCP Server

```bash
# stdio transport (for Claude Desktop / MCP clients)
python src/g1_mcp_server.py

# Or using the installed entry point
rosclaw-g1-mcp
```

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rosclaw-g1": {
      "command": "python",
      "args": ["/path/to/rosclaw-g1-dds-mcp/src/g1_mcp_server.py"],
      "transportType": "stdio"
    }
  }
}
```

### MCP Inspector (Testing)

```bash
mcp dev src/g1_mcp_server.py
```

## Available Tools

| Tool | Description |
|------|-------------|
| `connect_g1` | Connect to G1 via DDS domain |
| `disconnect_g1` | Disconnect from G1 |
| `stand_up` | Command G1 to stand up |
| `sit_down` | Command G1 to sit down |
| `walk_with_velocity` | Walk with linear/angular velocity |
| `move_joint` | Move a single joint to target angle |
| `move_joints` | Move multiple joints simultaneously |
| `stop_movement` | Stop and hold current position |
| `emergency_stop` | Emergency halt (use with caution!) |
| `wave_hand` | Perform waving gesture |

## Available Resources

| Resource | Description |
|----------|-------------|
| `g1://status` | Battery, mode, joint positions |
| `g1://joints` | Joint limits for all 23 joints |
| `g1://connection` | DDS connection status |

## Joint Reference

```
Left Leg:   left_hip_yaw, left_hip_roll, left_hip_pitch, left_knee, left_ankle
Right Leg:  right_hip_yaw, right_hip_roll, right_hip_pitch, right_knee, right_ankle
Waist:      waist_yaw, waist_roll, waist_pitch
Left Arm:   left_shoulder_pitch, left_shoulder_roll, left_shoulder_yaw, left_elbow
Right Arm:  right_shoulder_pitch, right_shoulder_roll, right_shoulder_yaw, right_elbow
```

## Safety

- All joint commands are validated against hardware limits before execution
- Velocity limits enforced: legs ≤ 10 rad/s, waist ≤ 5 rad/s, arms ≤ 10 rad/s
- `emergency_stop` will disable motors — robot may fall

## Dependencies

- Python 3.10+
- `mcp[fastmcp]` — MCP framework
- `unitree_sdk2` — Unitree DDS SDK (install separately from hardware package)
- `cyclonedds` or `fastdds` — DDS middleware

## Architecture

```
g1_mcp_server.py
├── G1State          — Robot state dataclass
├── StateBuffer      — Thread-safe ring buffer for DDS data
├── G1DDSBridge      — DDS communication bridge
│   ├── connect()    — Initialize DDS participant
│   ├── _dds_listener() — Background thread at 100Hz
│   └── publish_command() — Send /lowcmd
└── MCP Tools        — FastMCP tool definitions
```

## License

MIT License — See [LICENSE](LICENSE)

## Part of ROSClaw

- [rosclaw-g1-dds-mcp](https://github.com/ros-claw/rosclaw-g1-dds-mcp) — Unitree G1 (DDS)
- [rosclaw-ur-ros2-mcp](https://github.com/ros-claw/rosclaw-ur-ros2-mcp) — UR5 arm (ROS2)
- [rosclaw-gimbal-mcp](https://github.com/ros-claw/rosclaw-gimbal-mcp) — GCU Gimbal (Serial)
