# 3D Mesh Post-Processing Scripts

基于 `pymeshlab` 的一组 Python 脚本，用于处理 3D 网格与点云常见问题，包括：

- 网格清洗
- 自交与非流形修复
- 表面重建
- 白模/带纹理模型减面
- 主惯性轴对齐

项目当前主要包含 3 个脚本，分别面向通用处理、完整清洗流程和主轴对齐示例。

## 仓库结构

```text
mesh_post_processing/
├─ post_processing.py
├─ mesh_clean_process.py
├─ principal_axis.py
└─ readme.md
```

## 环境依赖

建议使用 Python 3 环境，并安装 `pymeshlab`：

```bash
pip install pymeshlab
```

## 文件说明

### `post_processing.py`

通用网格后处理脚本，提供可复用的基础函数和两个默认流程。

基础函数：

- `outlier_removal`：移除点云离群点，并补洞
- `surface_reconstruction`：基于 Screened Poisson 的表面重建
- `self_intersection_removal`：删除自交面
- `repair_non_manifold_edges`：修复非流形边，并补洞
- `simplify_mesh_without_texture`：白模减面
- `simplify_mesh_with_texture`：保留纹理的减面
- `ms_load_and_save`：统一的加载、处理、保存辅助函数

默认流程：

- `pipline_default_without_texture`：面向白模，可按开关依次执行减面、离群点过滤、表面重建、自交移除和非流形修复
- `pipline_default_with_texture`：面向带纹理模型，执行保留纹理的减面

适用场景：

- 快速调用单个处理步骤
- 将多个基础步骤串成简化流程
- 为其他脚本或项目提供可复用函数

### `mesh_clean_process.py`

面向带纹理原始网格的完整清洗与减面流程，核心函数为 `clean_and_decimate_mesh`。

默认处理顺序：

1. 删除重复顶点、重复面和空面
2. 移除较小噪声连通域
3. 修复非流形边与非流形顶点
4. 删除自相交面
5. 合并极近顶点
6. 补洞
7. 执行 Screened Poisson 表面重建
8. 执行高保真减面
9. 拉普拉斯平滑
10. 重建后再次清理并重算法向

函数签名：

```python
clean_and_decimate_mesh(
    input_path: str,
    output_path: str,
    target_face_num: int = 1000000,
)
```

参数说明：

- `input_path`：输入网格路径，通常是带纹理的 `.obj`
- `output_path`：输出网格路径；脚本会自动创建目标目录
- `target_face_num`：目标面数，默认 `1000000`

导出时会显式保留：

- 纹理坐标
- wedge 法向
- 贴图文件引用

适用场景：

- 扫描得到的原始带纹理网格清理
- 泊松重建后的统一后处理
- 大面数模型减面后导出为可继续使用的 OBJ

### `principal_axis.py`

用于演示如何调用 `pymeshlab` 的主惯性轴对齐能力。

包含函数：

- `align_to_principal_axis`：执行主轴对齐矩阵计算
- `align_axis`：加载模型、执行对齐并保存结果

适用场景：

- 在后处理前统一模型朝向
- 将模型对齐到主惯性轴，便于后续分析或批处理

## 快速使用

### 1. 白模默认流程

```python
from post_processing import pipline_default_without_texture

pipline_default_without_texture(
    input_mesh_path="input.obj",
    output_mesh_path="output.obj",
    bool_outlier_removal=True,
    bool_surface_reconstruction=False,
    bool_self_intersection_removal=True,
    bool_repair_non_manifold_edges=True,
    bool_simplify_mesh_without_texture=True,
    targetfacenum=300000,
)
```

### 2. 带纹理模型减面

```python
from post_processing import pipline_default_with_texture

pipline_default_with_texture(
    input_mesh_path="textured_input.obj",
    output_mesh_path="textured_output.obj",
    targetfacenum=300000,
)
```

### 3. 完整清洗与减面

```python
from mesh_clean_process import clean_and_decimate_mesh

clean_and_decimate_mesh(
    input_path="textured_input.obj",
    output_path="cleaned_output.obj",
    target_face_num=1000000,
)
```

### 4. 主惯性轴对齐

```python
from principal_axis import align_axis

align_axis(
    input_mesh_path="input.obj",
    output_mesh_path="aligned_output.obj",
)
```

## 直接运行脚本

三个脚本都保留了 `__main__` 示例，可直接运行：

```bash
python post_processing.py
python mesh_clean_process.py
python principal_axis.py
```

运行前建议先将脚本底部示例中的输入输出路径改成你自己的文件路径。

## 使用建议

- 白模处理优先从 `post_processing.py` 开始，便于按步骤组合功能
- 带纹理原始扫描网格优先使用 `mesh_clean_process.py`
- 若输入为带纹理 OBJ，请确保 `.mtl` 和贴图文件可正常访问
- Screened Poisson 重建会改变网格表面结构，结果质量依赖输入模型质量
- 超大模型在重建和减面时可能占用较多内存并耗时较长

## 说明

- 当前仓库更偏向脚本集合，而不是封装好的命令行工具或 Python 包
- 如需批处理，建议在现有函数基础上自行封装循环和日志逻辑
