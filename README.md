# scikit-robot-models

Pre-packaged URDF + mesh bundles for use with
[scikit-robot](https://github.com/iory/scikit-robot).

Each `*_description.tar.gz` extracts to `<robot>_description/{urdf,meshes}/`
with mesh URIs already rewritten to
`package://<robot>_description/meshes/...`, so the URDFs load directly
with `skrobot.models.urdf.RobotModelFromURDF`.

## Available models

| Bundle | Robot | Upstream | License |
|---|---|---|---|
| `pr2_description.tar.gz` | Willow Garage PR2 | [`PR2/pr2_common`](https://github.com/PR2/pr2_common) | BSD-3-Clause |
| `fetch_description.tar.gz` | Fetch Robotics Fetch | [`fetchrobotics/fetch_ros`](https://github.com/fetchrobotics/fetch_ros) | **CC BY-NC-SA 4.0** ⚠ |
| `franka_description.tar.gz` | Franka Emika Panda | [`frankaemika/franka_ros`](https://github.com/frankaemika/franka_ros) | Apache-2.0 |
| `nextage_description.tar.gz` | Kawada NEXTAGE OPEN | [`tork-a/rtmros_nextage`](https://github.com/tork-a/rtmros_nextage) | BSD-3-Clause |
| `hydrus_description.tar.gz` | JSK HYDRUS transformable multirotor | [`jsk-ros-pkg/jsk_aerial_robot`](https://github.com/jsk-ros-pkg/jsk_aerial_robot) | BSD |
| `tycoon_description.tar.gz` | JSK TYCOON modular robot | (JSK lab) | (TBD) |
| `griphis_description.tar.gz` | JSK GRIPHIS multi-joint modular robot | (JSK lab) | (TBD) |
| `aero_description.tar.gz` | SEED-Noid / AeroTypeFCESy (JSK config; with-hand & handless) | [`seed-solutions/aero-ros-pkg`](https://github.com/seed-solutions/aero-ros-pkg) | EPL |
| `jedy_description.tar.gz` | JSK Jedy reconfigurable dual-arm mobile robot | (JSK lab) | BSD |
| `jedy_light_description.tar.gz` | Jedy with lighter meshes, for simulators and browsers (see below) | (JSK lab) | BSD |
| `differential_wrist_sample.tar.gz` | scikit-robot prototyping sample | (in-repo) | MIT |

> ⚠️ **Fetch is CC BY-NC-SA 4.0** (NonCommercial). The license is declared
> in `fetch_description/package.xml`, distinct from the umbrella
> `fetch_ros` repo which is BSD. Redistribution or commercial use
> requires honoring the NonCommercial clause.

## Light bundles

`*_light_description.tar.gz` is a copy of a bundle with lighter meshes,
made by `tools/make_light.py`. It extracts to
`<robot>_light_description/` with its `package://` URIs rewritten, so it
can sit next to the original. Circuit boards and parts under 1 cm are
dropped; every other part is simplified with
[meshoptimizer](https://github.com/zeux/meshoptimizer) as far as it goes
without moving its surface more than 0.5 mm, and coloured with its
average colour. Joints, links and collision geometry are unchanged.

| Bundle | Faces | Size |
|---|---|---|
| `jedy_description.tar.gz` | 693,916 | 5.0 MB |
| `jedy_light_description.tar.gz` | 111,917 | 1.0 MB |

```sh
uv run tools/make_light.py jedy_description.tar.gz
```

The output is byte-for-byte reproducible from the same input.

## Citations

If you use these models in a publication, please cite the corresponding
upstream paper.

```bibtex
% --- PR2 (Willow Garage) ---
% De facto reference; Willow Garage does not mandate a specific paper.
@inproceedings{bohren2011pr2,
  author    = {Bohren, J. and Rusu, R. B. and Jones, E. G. and
               Marder-Eppstein, E. and Pantofaru, C. and Wise, M. and
               M{\"o}senlechner, L. and Meeussen, W. and Holzer, S.},
  title     = {Towards Autonomous Robotic Butlers: Lessons Learned with
               the {PR2}},
  booktitle = {Proc.\ IEEE Int.\ Conf.\ on Robotics and Automation (ICRA)},
  pages     = {5568--5575},
  year      = {2011},
  doi       = {10.1109/ICRA.2011.5980058},
}

% --- Fetch ---
@inproceedings{wise2016fetch,
  author    = {Wise, Melonee and Ferguson, Michael and King, Derek and
               Diehr, Eric and Dymesich, David},
  title     = {Fetch \& Freight: Standard Platforms for Service Robot
               Applications},
  booktitle = {Workshop on Autonomous Mobile Service Robots, IJCAI},
  year      = {2016},
}

% --- Franka Emika Panda ---
@article{haddadin2022franka,
  author  = {Haddadin, Sami and Parusel, Sven and Johannsmeier, Lars and
             Golz, Saskia and Gabl, Simon and Walch, Florian and
             Sabaghian, Mohammadreza and J{\"a}hne, Christoph and
             Hausperger, Lukas and Haddadin, Simon},
  title   = {The {Franka} {Emika} Robot: A Reference Platform for
             Robotics Research and Education},
  journal = {IEEE Robotics \& Automation Magazine},
  volume  = {29},
  number  = {2},
  pages   = {46--64},
  year    = {2022},
  doi     = {10.1109/MRA.2021.3138382},
}

% --- Nextage Open ---
% No canonical academic paper. Cite the upstream description package:
%   Kei Okada, TORK and contributors, "rtmros_nextage,"
%   https://github.com/tork-a/rtmros_nextage

% --- HYDRUS (JSK) ---
@article{zhao2018hydrus,
  author  = {Zhao, Moju and Kawasaki, Koji and Anzai, Tomoki and
             Chen, Xiangyu and Noda, Shintaro and Shi, Fan and
             Okada, Kei and Inaba, Masayuki},
  title   = {Transformable multirotor with two-dimensional multilinks:
             Modeling, control, and whole-body aerial manipulation},
  journal = {The International Journal of Robotics Research},
  volume  = {37},
  number  = {9},
  pages   = {1085--1112},
  year    = {2018},
  doi     = {10.1177/0278364918801639},
}

% --- TYCOON (JSK) ---
@article{matsuo2026tycoon,
  author    = {Matsuo, Kento and Makabe, Tasuku and Yanokura, Iori and
               Kojima, Kunio and Okada, Kei and Inaba, Masayuki},
  title     = {{TYCOON}: modular robot capable of torque synthesized
               collaboration with complementary intermittent gear
               mechanism},
  journal   = {Advanced Robotics},
  pages     = {1--25},
  year      = {2026},
  publisher = {Taylor \& Francis},
}

% --- GRIPHIS (JSK) ---
@inproceedings{morita2025griphis,
  author    = {Morita, Sousuke and Matsuo, Kento and Makabe, Tasuku and
               Yanokura, Iori and Kojima, Kunio and Okada, Kei},
  title     = {Development of Multi-joint Modular Robot Capable of
               Grasping Objects in Both Single and Combined States by
               Using Docking-Gripping Mechanism},
  booktitle = {JSME Conference on Robotics and Mechatronics},
  pages     = {1P1--E11},
  year      = {2025},
}

% --- SEED-Noid / Aero (JSK) ---
@article{sasabuchi2018seednoid,
  author    = {Sasabuchi, Kazuhiro and Yaguchi, Hiroaki and
               Nagahama, Kotaro and Hori, Shintaro and
               Mizohana, Hiroto and Inaba, Masayuki},
  title     = {The {SEEDNoid} Robot Platform: Designing a Multipurpose
               Compact Robot From Continuous Evaluation and Lessons From
               Competitions},
  journal   = {IEEE Robotics and Automation Letters},
  volume    = {3},
  number    = {4},
  pages     = {3983--3990},
  year      = {2018},
  publisher = {IEEE},
}

% --- Jedy (JSK / The University of Tokyo) ---
@inproceedings{yanokura2025jedy,
  author    = {Yanokura, Iori and Kojima, Kunio and Yamaguchi, Naoya and
               Nakane, Aoi and Makabe, Tasuku and Yamaguchi, Manami and
               Okada, Kei},
  title     = {Robot Programming Education Using the Tabletop Dual-Armed
               Wheely Robot ``{Jedy}'': A Practical Approach to Robotics
               Education and Emerging Challenges},
  booktitle = {JSME Conference on Robotics and Mechatronics (ROBOMECH)},
  pages     = {2A2--I08},
  year      = {2025},
}

@article{yanokura2026jedy,
  author    = {Yanokura, Iori and Makabe, Tasuku and Sawada, Tomoka and
               Sugihara, Kazuki and Kojima, Kunio and Okada, Kei},
  title     = {Design and Educational Impact of Reconfigurable Robot for
               Bridging Imagination and Implementation},
  journal   = {Journal of the Robotics Society of Japan},
  volume    = {44},
  number    = {3},
  pages     = {260--263},
  year      = {2026},
}
```

## License

The packaging scripts and this README are MIT.
Each robot bundle inherits the license of its upstream source — see the
table above. By using a bundle you agree to honor that upstream license.

