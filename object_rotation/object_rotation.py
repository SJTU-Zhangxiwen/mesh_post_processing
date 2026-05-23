"""
基于 4x4 文本矩阵对 OBJ mesh 执行变换。

主要用于读取 `*.mat.txt` 中的矩阵，并将其直接应用到输入模型，
最后导出为新的 OBJ 文件。
"""

from pathlib import Path

import numpy as np


def read_matrix_txt(path: str | Path) -> np.ndarray:
    """
    读取文本矩阵文件，要求结果为 4x4。

    支持空格或逗号分隔，忽略空行。
    """
    rows: list[list[float]] = []
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            rows.append([float(v) for v in line.replace(",", " ").split()])

    matrix = np.array(rows, dtype=float)
    if matrix.shape != (4, 4):
        raise ValueError(f"期望 4x4 矩阵，实际为: {matrix.shape}")
    return matrix


def object_rotation(
    matrix_txt_path: str | Path,
    input_obj_path: str | Path,
    output_obj_path: str | Path,
    freeze: bool = True,
    compose: bool = False,
    save_textures: bool = True,
    save_wedge_texcoord: bool = True,
    save_wedge_normal: bool = True,
) -> Path:
    """
    将文本矩阵应用到输入 OBJ，并导出变换后的模型。

    :param matrix_txt_path: 4x4 变换矩阵 txt 路径
    :param input_obj_path: 输入 OBJ 路径
    :param output_obj_path: 输出 OBJ 路径
    :param freeze: 是否将变换冻结到顶点坐标
    :param compose: 是否与当前矩阵复合
    :return: 输出 OBJ 路径
    """
    try:
        import pymeshlab
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "未检测到 pymeshlab。请先安装：pip install pymeshlab"
        ) from e

    matrix = read_matrix_txt(matrix_txt_path)
    input_obj_path = Path(input_obj_path)
    output_obj_path = Path(output_obj_path)
    output_obj_path.parent.mkdir(parents=True, exist_ok=True)

    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(str(input_obj_path))

    applied = False
    # 优先尝试滤镜接口，兼容较常见的 pymeshlab 版本。
    if hasattr(ms, "apply_filter"):
        try:
            ms.apply_filter(
                "set_matrix",
                transformmatrix=matrix,
                compose=compose,
                freeze=freeze,
            )
            applied = True
        except Exception:
            applied = False

    # 某些版本直接暴露 set_matrix 方法，作为后备路径。
    if not applied and hasattr(ms, "set_matrix"):
        ms.set_matrix(
            transformmatrix=matrix,
            compose=compose,
            freeze=freeze,
        )
        applied = True

    if not applied:
        raise RuntimeError("无法应用矩阵：未找到可用的 set_matrix 接口/滤镜。")

    ms.save_current_mesh(
        str(output_obj_path),
        save_textures=save_textures,
        save_wedge_texcoord=save_wedge_texcoord,
        save_wedge_normal=save_wedge_normal,
    )
    ms.clear()
    return output_obj_path


transform_obj_by_matrix_txt = object_rotation
