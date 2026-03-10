- # 3D Mesh Post-Processing Scripts

  这是一个基于 `pymeshlab` 的 Python 脚本集，封装了 3D 网格/点云处理中常用的几何修复与简化功能。本脚本既提供了单一功能的独立接口，也提供了组合好的一键处理流程。

  ## 环境依赖

  运行此脚本需要安装 Python >= 3.7 以及 `pymeshlab` 库：

  ```
  pip install pymeshlab
  ```

  ## 功能特性

  ### 1. 一键处理流程 (Pipelines)

  脚本中封装了针对不同模型类型的一键处理流程，方便直接调用：

  - **`pipline_default_without_texture`**：适用于白模的默认处理流程。支持按需串联执行：网格简化、离群点过滤、表面重建、自交移除以及非流形边修复功能。
  - **`pipline_default_with_texture`**：适用于带有纹理的网格默认处理流程。在减面的同时保持纹理 UV 映射不丢失。

  ### 2. 独立处理函数 (Core Functions)

  如果需要精细化控制，可以单独调用以下 6 个基础函数：

  1. **`outlier_removal`**：离群点过滤。剔除游离噪声点，并自动执行补洞操作以尽量保持模型水密。
  2. **`surface_reconstruction`**：表面重建。基于泊松（Screened Poisson）算法，从点云重新生成表面网格。
  3. **`self_intersection_removal`**：移除自交面。自动检测并删除模型中内部穿模的面。
  4. **`repair_non_manifold_edges`**：修复非流形边。提供删除多余面或分离顶点两种模式，并自动补洞。
  5. **`simplify_mesh_without_texture`**：白模网格简化。用于在不改变整体形状的情况下，降低模型面数。
  6. **`simplify_mesh_with_texture`**：带贴图网格简化。在减面的同时保持纹理 UV 映射不丢失。

  *(注：脚本内部还提供了 `ms_load_and_save` 实用工具函数，用于快速加载、处理并保存模型文件。)*

  ## 测试数据

  项目中附带了 `data_for_test` 文件夹，包含了以下测试用模型，供快速验证脚本功能及性能测试：

  - **`mesh_without_texture.obj`**：约 30 万面的纯白模数据，适合用来测试基础清理、修复和白模减面功能。
  - **`mesh_with_texture.obj`**：约 30 万面的带贴图模型数据。*(注意：同目录下需包含对应的 `.mtl` 和 `.jpg/.png` 贴图文件才能正确读取纹理)*，专门用于测试 `simplify_mesh_with_texture` 功能。
  - **`mesh_without_texture_3.5m_faces.obj`**：约 350 万面的高精度纯白模数据，数据量较大，用于压力测试。