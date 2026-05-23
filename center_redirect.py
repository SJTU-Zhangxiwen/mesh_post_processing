"""
用于将 mesh 的包围盒中心平移到原点的工具脚本。

本脚本基于 `pymeshlab.MeshSet.compute_matrix_from_translation`
执行平移，其中 `traslmethod=1` 表示使用 mesh 的包围盒中心
作为平移参考点，并将其移动到世界坐标原点。
"""

from pathlib import Path


def _default_mesh_output_path(input_mesh_path: Path) -> Path:
    """
    为居中平移结果生成默认输出路径。

    例如：
    - input.obj -> input.center.obj
    """
    if input_mesh_path.suffix:
        return input_mesh_path.with_name(
            f"{input_mesh_path.stem}.center{input_mesh_path.suffix}"
        )
    return input_mesh_path.with_name(f"{input_mesh_path.name}.center")


def compute_center_redirect(ms) -> None:
    """
    将当前 mesh 的包围盒中心移动到原点。

    :param ms: pymeshlab.MeshSet 实例
    """
    ms.compute_matrix_from_translation(traslmethod=1)


def center_redirect(
    input_mesh_path: str | Path,
    output_mesh_path: str | Path | None = None,
    save_textures: bool = True,
    save_wedge_texcoord: bool = True,
    save_wedge_normal: bool = True,
) -> Path:
    """
    读取 mesh，将其包围盒中心平移到原点后导出。

    :param input_mesh_path: 输入 mesh 路径（如 .obj）
    :param output_mesh_path: 输出 mesh 路径（不传则生成 *.center.*）
    :param save_textures: 保存纹理引用（对带纹理 OBJ 建议为 True）
    :param save_wedge_texcoord: 保存 wedge 纹理坐标
    :param save_wedge_normal: 保存 wedge 法向
    :return: 输出 mesh 路径
    """
    try:
        import pymeshlab
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "未检测到 pymeshlab。请先安装：pip install pymeshlab"
        ) from e

    input_mesh_path = Path(input_mesh_path)
    resolved_output_path = (
        Path(output_mesh_path)
        if output_mesh_path is not None
        else _default_mesh_output_path(input_mesh_path)
    )
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)

    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(str(input_mesh_path))
    compute_center_redirect(ms)
    ms.save_current_mesh(
        str(resolved_output_path),
        save_textures=save_textures,
        save_wedge_texcoord=save_wedge_texcoord,
        save_wedge_normal=save_wedge_normal,
    )
    ms.clear()
    return resolved_output_path


if __name__ == "__main__":
    pass
