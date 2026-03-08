import pymeshlab

def outlier_removal(input_mesh_path, 
                    output_mesh_path, 
                    propthreshold = 0.980000, 
                    knearest = 16,
                    maxholesize = 30,
                    refineholeedgelen_percent =3.000000
                    ):
    """
    用于过滤点云中的离群点，保留大多数点的邻域内的点。
    注意，操作后易于导致模型非水密，故后加入补洞。
    :param input_mesh_path: 输入网格文件路径
    :param output_mesh_path: 输出网格文件路径
    :param propthreshold: 离群点的比例阈值，默认为0.98
    :param knearest: 用于计算邻域的最近邻数量，默认为16
    :param maxholesize: 补洞时允许的最大洞穴大小，默认为30
    :param refineholeedgelen_percent: 补洞时细化边长的百分比，默认为3.0
    """
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_mesh_path)
    ms.compute_selection_point_cloud_outliers(propthreshold = propthreshold, knearest = knearest)
    ms.meshing_remove_selected_vertices()
    ms.meshing_close_holes(maxholesize = maxholesize, refineholeedgelen = pymeshlab.PercentageValue(refineholeedgelen_percent))
    ms.save_current_mesh(output_mesh_path)

def surface_reconstruction(
        input_mesh_path, 
        output_mesh_path, 
        depth = 8, 
        samplespernode = 1.200000, 
        pointweight = 4.000000, 
        threads = 15):
    """
    用于从点云重建表面网格。
    :param input_mesh_path: 输入网格文件路径
    :param output_mesh_path: 输出网格文件路径
    :param depth: 八叉树的深度，默认为8
    :param samplespernode: 每个八叉树节点的采样点数量，默认为1.2
    :param pointweight: 点权重，默认为4.0
    :param threads: 使用的线程数量，默认为15
    """
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_mesh_path)
    ms.generate_surface_reconstruction_screened_poisson(depth = depth, samplespernode = samplespernode, pointweight = pointweight, preclean = True, threads = threads)
    ms.save_current_mesh(output_mesh_path)

def self_intersection_removal(input_mesh_path, 
                              output_mesh_path):
    """
    用于移除网格中的自交部分。
    :param input_mesh_path: 输入网格文件路径
    :param output_mesh_path: 输出网格文件路径
    """
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_mesh_path)
    ms.compute_selection_by_self_intersections_per_face()
    ms.meshing_remove_selected_faces()
    ms.save_current_mesh(output_mesh_path)

def repair_non_manifold_edges(input_mesh_path, 
                              output_mesh_path, 
                              method = 0,
                              maxholesize = 30,
                              refineholeedgelen_percent =3.000000
                              ):
    """
    用于修复网格中的非流形边。
    注意，操作后易于导致模型非水密，故后加入补洞。
    :param input_mesh_path: 输入网格文件路径
    :param output_mesh_path: 输出网格文件路径
    :param method: 修复方法，默认为0
    0: 通过删除面来移除非流形边（对于每一条非流形边，算法会反复迭代删除面积最小的面，直到它变成正常的 2-流形结构），
    1: 或者通过分离顶点来移除（这样每一条非流形边链都会变成一个开放边界）
    :param maxholesize: 补洞时允许的最大洞穴大小，默认为30
    :param refineholeedgelen_percent: 补洞时细化边长的百分比，默认为3.0
    """
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_mesh_path)
    ms.meshing_repair_non_manifold_edges(method = method)
    ms.meshing_close_holes(maxholesize = maxholesize, refineholeedgelen = pymeshlab.PercentageValue(refineholeedgelen_percent))
    ms.save_current_mesh(output_mesh_path)

def simplify_mesh_without_texture(input_mesh_path, 
                  output_mesh_path, 
                  targetfacenum = 300000, 
                  targetperc = 0.000000, 
                  qualitythr = 0.300000, 
                  boundaryweight = 1.000000, 
                  planarweight = 0.002000):
    """
    适用于白模，用于简化网格以减少面数。
    :param input_mesh_path: 输入网格文件路径
    :param output_mesh_path: 输出网格文件路径
    :param targetfacenum: 目标面数，默认为300000
    :param targetperc: 目标面数的百分比，默认为0.0
    :param qualitythr: 面质量阈值，默认为0.3
    :param boundaryweight: 边界权重，默认为1.0
    :param planarweight: 平面权重，默认为0.002000
    """
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_mesh_path)
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum = targetfacenum, targetperc = targetperc, qualitythr = qualitythr, boundaryweight = boundaryweight, planarweight = planarweight)
    ms.save_current_mesh(output_mesh_path)

def simplify_mesh_with_texture(input_mesh_path, 
                  output_mesh_path, 
                  targetfacenum = 300000, 
                  targetperc = 0.000000, 
                  qualitythr = 0.300000, 
                  boundaryweight = 1.000000, 
                  planarweight = 0.002000):
    """
    适用于带有纹理的网格，用于简化网格以减少面数。
    注意，同文件夹下需保存mtl和贴图的jpg或png文件。
    :param input_mesh_path: 输入网格文件路径
    :param output_mesh_path: 输出网格文件路径
    :param targetfacenum: 目标面数，默认为300000
    :param targetperc: 目标面数的百分比，默认为0.0
    :param qualitythr: 面质量阈值，默认为0.3
    :param boundaryweight: 边界权重，默认为1.0
    :param planarweight: 平面权重，默认为0.002000
    """
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_mesh_path)
    ms.meshing_decimation_quadric_edge_collapse_with_texture(targetfacenum = targetfacenum, targetperc = targetperc, qualitythr = qualitythr, boundaryweight = boundaryweight, planarweight = planarweight)
    ms.save_current_mesh(output_mesh_path)

if __name__ == "__main__":
    # 示例用法
    input_mesh_path = "input_mesh.obj"
    output_mesh_path = "output_mesh.obj"
    
    # 离群点过滤
    outlier_removal(input_mesh_path, output_mesh_path)
    
    # 表面重建
    surface_reconstruction(input_mesh_path, output_mesh_path)
    
    # 自交移除
    self_intersection_removal(input_mesh_path, output_mesh_path)
    
    # 非流形边修复
    repair_non_manifold_edges(input_mesh_path, output_mesh_path)
    
    # 网格简化（无纹理）
    simplify_mesh_without_texture(input_mesh_path, output_mesh_path)
    
    # 网格简化（有纹理）
    simplify_mesh_with_texture(input_mesh_path, output_mesh_path)