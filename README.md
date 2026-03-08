# mesh_post_processing
这是一个基于 `pymeshlab` 的 Python 脚本集，封装了 3D 网格/点云处理中常用的几何修复与简化功能。



环境依赖：运行此脚本需要安装 Python >= 3.7 以及 `pymeshlab` 库：

```
pip install pymeshlab
```



本脚本提供了以下 6 个独立的处理函数：

1. **`outlier_removal`**：离群点过滤。剔除游离噪声点，并自动执行补洞操作以尽量保持模型水密。
2. **`surface_reconstruction`**：表面重建。基于泊松（Screened Poisson）算法，从点云重新生成表面网格。
3. **`self_intersection_removal`**：移除自交面。自动检测并删除模型中内部穿模的面。
4. **`repair_non_manifold_edges`**：修复非流形边。提供删除多余面或分离顶点两种模式，并自动补洞。
5. **`simplify_mesh_without_texture`**：白模网格简化。用于在不改变整体形状的情况下，降低模型面数。
6. **`simplify_mesh_with_texture`**：带贴图网格简化。在减面的同时保持纹理 UV 映射不丢失。
