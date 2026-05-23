# object_rotation

该目录提供基于 `txt` 矩阵对 `OBJ` 模型做旋转/变换的简洁实现。

## 核心函数

文件：`object_rotation.py`

```python
object_rotation(
    matrix_txt_path,
    input_obj_path,
    output_obj_path,
    freeze=True,
    compose=False,
    save_textures=True,
    save_wedge_texcoord=True,
    save_wedge_normal=True,
)
```

功能：

- 读取 `matrix_txt_path` 中的 4x4 矩阵
- 将矩阵应用到输入 `OBJ`
- 将结果保存到 `output_obj_path`

别名：

```python
transform_obj_by_matrix_txt = object_rotation
```

## 矩阵文件格式

要求为 4 行 4 列的文本矩阵，支持空格或逗号分隔，例如：

```txt
0.000000000000 0.000000000000 1.000000000000 0.000000000000
1.000000000000 0.000000000000 0.000000000000 0.000000000000
0.000000000000 1.000000000000 0.000000000000 0.000000000000
0.000000000000 0.000000000000 0.000000000000 1.000000000000
```

## 使用示例

```python
from object_rotation import object_rotation

object_rotation(
    matrix_txt_path=r"g:\university\innovation\scan\mesh_post_processing\object_rotation\y_positive.mat.txt",
    input_obj_path=r"g:\university\innovation\scan\mesh_post_processing\data_for_test\mesh_without_texture.obj",
    output_obj_path=r"g:\university\innovation\scan\mesh_post_processing\data_for_test\mesh_without_texture_y_positive.obj",
)
```

## 参数说明

- `matrix_txt_path`: 4x4 变换矩阵文件路径
- `input_obj_path`: 输入模型路径
- `output_obj_path`: 输出模型路径
- `freeze`: 是否将变换直接写入顶点坐标，默认 `True`
- `compose`: 是否与当前矩阵叠加，默认 `False`

## 依赖

需要先安装：

```bash
pip install pymeshlab
```
