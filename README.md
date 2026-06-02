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
| `differential_wrist_sample.tar.gz` | scikit-robot prototyping sample | (in-repo) | MIT |

> ⚠️ **Fetch is CC BY-NC-SA 4.0** (NonCommercial). The license is declared
> in `fetch_description/package.xml`, distinct from the umbrella
> `fetch_ros` repo which is BSD. Redistribution or commercial use
> requires honoring the NonCommercial clause.

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
```

## License

The packaging scripts and this README are MIT.
Each robot bundle inherits the license of its upstream source — see the
table above. By using a bundle you agree to honor that upstream license.

