# Reusing robot_grasp1

ROS 2 perception, tracking and grasping workspace.

**Current scope:** Research workspace for xArm and RGB-D sensing; dependency exports contain machine-specific entries.

This repository is a fork of [QC2002/graduate_pro](https://github.com/QC2002/graduate_pro). Original authorship, citations and upstream notices are retained. Changes here apply to this fork.

## Environment

The launch scripts target ROS 2 Humble. Install and source the appropriate ROS distribution before building the packages under `src/`. The root `requirements.txt` and `full_environment.yml` are historical environment exports: they contain ROS system packages and local `file://` paths. They are not portable one-command installers.

Reconstruct Python/model dependencies inside a compatible ROS environment, using each package's `package.xml` and `setup.py` as additional evidence. Install the actual camera and robot SDKs for your equipment. SAM/SAM2/YOLO weights and camera/robot calibration require separate local configuration.

```bash
python scripts/check_repository.py
```

This is the hardware-free initial check. Do not run the launch scripts merely to verify installation.

## Workspace map

| Path | Purpose |
|---|---|
| `src/vision_ai_interfaces/` | Custom message/service definitions |
| `src/vision_ai/` | Scan planning, stitching, detection, tracking and grasp logic |
| `src/camera_node/` | RGB-D camera publisher |
| `src/xarm_controller/` | Physical robot communication |
| `build_interfaces.sh` | Interface build helper; inspect local paths first |
| `dev.sh`, `integrated_launch.sh` | System launch orchestration |
| `test_scenarios_metadata/` | Recorded evaluation-scenario descriptions |

The detailed Chinese README below retains algorithm and operational explanations. Its source links now use repository-relative paths so they work outside the original developer's computer.

## Configuration and first run

Review workspace paths, sourced environment files, device addresses, model/configuration paths, topic/service names, camera intrinsics and hand-eye calibration. Build interfaces before dependent nodes. Verify camera input and coordinate transforms independently before enabling a robot controller or an automatic grasp trigger.

Scripts named `test`, `restart` or `one_click` can start or terminate processes and communicate with devices. Read them before use. Historical results and logs are examples from an existing experiment, not evidence of performance on another setup.

## Reproducibility and troubleshooting

Record ROS distribution, Python/CUDA versions, model weights, calibration, scene IDs and evaluation thresholds. Build/import errors may come from unsourced ROS workspaces or unbuilt interfaces. Incorrect grasp coordinates often come from depth scale, frame conventions or hand-eye calibration; inspect them before attempting another motion.

A full build and hardware execution have not been performed by the structural check. Use the existing algorithm-specific diagnostics only in the configured environment, and retain raw observations separately from generated reports.

## Attribution and reuse permissions

No repository-wide licence file is included in this checkout. Confirm reuse and redistribution permissions with the relevant rights holders; this maintenance update does not add a licence or relicense upstream code, data or assets.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the local workflow and what to include with a proposed change.
