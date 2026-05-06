import ezdxf
from ezdxf.enums import TextEntityAlignment
import json
import os
import re


def generate_cad_with_cargo():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    LAYER_OFFSETS = {
        1: (0.0, 0.0),
        2: (0.0, 52639.5044),
        3: (0.0, 99075.9797),
        4: (788.8605, 147416.7386)
    }

    json_filepath = "algorithm_output.json"
    algo_data = {}
    if os.path.exists(json_filepath):
        try:
            with open(json_filepath, 'r', encoding='utf-8') as f:
                algo_data = json.load(f)
            print(f"成功读取 {json_filepath}")
        except Exception as e:
            print(f"读取 JSON 失败 ({e})")
            return
    else:
        print(f"未找到 {json_filepath}，请确保该文件存在！")
        return

    irregular_shape = [
        (105779.5104, 1469.4236), (116436.8356, 1469.4236),
        (116436.8356, 4406.2734), (124638.8488, 4406.2734),
        (124638.8488, 7337.8315), (129554.7649, 7337.8315),
        (129554.7649, 20852.6325), (124798.0599, 20852.6325),
        (124638.8488, 23789.4823), (116436.8356, 23789.4823),
        (116436.8356, 25990.7967), (105779.5104, 25990.7967)
    ]
    msp.add_lwpolyline(irregular_shape + [irregular_shape[0]], dxfattribs={'color': 8})

    rectangles_data = """
    (0, 0), (29500.1448, 0), (29500.1448, 27461.8676), (0, 27461.8676)
    (31977.2678, 1.9988), (71336.347, 1.9988), (71336.347, 27461.8676), (31977.2678, 27461.8676)
    (73796.9509, 1.9988), (103318.9065, 1.9988), (103318.9065, 27461.8676), (73796.9509, 27461.8676)
    (0, 52639.5044), (29516.6638, 52639.5044), (29516.6638, 80097.7274), (0, 80097.7274)
    (31977.2678, 52639.5044), (71336.347, 52639.5044), (71336.347, 80097.7274), (31977.2678, 80097.7274)
    (73796.9509, 52639.5044), (98330.0029, 52639.5044), (98330.0029, 80097.7274), (73796.9509, 80097.7274)
    (0, 99075.9797), (29516.6638, 99075.9797), (29516.6638, 126534.2027), (0, 126534.2027)
    (31977.2678, 99075.9797), (71336.347, 99075.9797), (71336.347, 126534.2027), (31977.2678, 126534.2027)
    (73796.9509, 99075.9797), (98330.0029, 99075.9797), (98330.0029, 126534.2027), (73796.9509, 126534.2027)
    (-39360.3625, 146574.3435), (-28650.4293, 146574.3435), (-28650.4293, 178525.3651), (-39360.3625, 178525.3651)
    (-25988.9158, 147451.3555), (-20913.9961, 147451.3555), (-20913.9961, 176151.3555), (-25988.9158, 176151.3555)
    (-20913.9961, 147451.3555), (-14884.0752, 147451.3555), (-14884.0752, 176151.3555), (-20913.9961, 176151.3555)
    (-14799.8878, 147817.0441), (-8604.2239, 147817.0441), (-8604.2239, 176161.8596), (-14799.8878, 176161.8596)
    (-8588.4354, 147817.0441), (-3652.9543, 147817.0441), (-3652.9543, 176151.3555), (-8588.4354, 176151.3555)
    (788.8605, 147416.7386), (7350.3915, 147416.7386), (7350.3915, 176151.7386), (788.8605, 176151.7386)
    (7366.1818, 147416.7386), (14635.4361, 147416.7386), (14635.4361, 176151.7386), (7366.1818, 176151.7386)
    (14719.6263, 147816.6395), (22157.2614, 147816.6395), (22157.2614, 176151.7386), (14719.6263, 176151.7386)
    (22170.42, 147816.6395), (28326.7883, 147816.6395), (28326.7883, 176151.7386), (22170.42, 176151.7386)
    (33118.9789, 147816.6395), (40099.2477, 147816.6395), (40099.2477, 176152.9778), (33118.9789, 176152.9778)
    (40115.6216, 147930.2234), (48239.397, 147930.2234), (48239.397, 176152.9778), (40115.6216, 176152.9778)
    (48324.3975, 147282.6838), (59865.3738, 147282.6838), (59865.3738, 176152.9778), (48324.3975, 176152.9778)
    (59880.0048, 147282.6838), (69859.9675, 147282.6838), (69859.9675, 176152.9778), (59880.0048, 176152.9778)
    (74940.2202, 147791.0543), (81096.2828, 147791.0543), (81096.2828, 176151.0543), (74940.2202, 176151.0543)
    (81112.0716, 147791.0543), (88380.9657, 147922.5941), (88380.9657, 176151.0543), (81112.0716, 176151.0543)
    (88465.1517, 147417.5006), (95902.4173, 147417.5006), (95902.4173, 176151.0543), (88465.1517, 176151.0543)
    (95915.5713, 147417.5006), (102071.6380, 147417.5006), (102071.6380, 176151.0543), (95915.5713, 176151.0543)
    (106817.6037, 149660.0003), (111539.494, 149660.0003), (111539.494, 174683.982), (106817.6037, 174683.982)
    (111552.9658, 149659.1567), (117258.3031, 149659.1567), (117258.3031, 174683.982), (111552.9658, 174683.982)
    (117507.533, 152594.6053), (124798.057, 152594.6053), (124798.057, 172483.5769), (117507.533, 172483.5769)
    """
    for line in rectangles_data.strip().split('\n'):
        line = line.strip()
        if not line: continue
        coords = re.findall(r'\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)', line)
        if len(coords) >= 4:
            shape_pts = [(float(x), float(y)) for x, y in coords]
            shape_pts.append(shape_pts[0])
            msp.add_lwpolyline(shape_pts, dxfattribs={'color': 8})

    bypass_boards = algo_data.get("bypassBoardPosition", [])
    for board in bypass_boards:
        layer_idx = board.get("layer", 1)
        offset_x, offset_y = LAYER_OFFSETS.get(layer_idx, (0.0, 0.0))

        pts = []
        for i in range(1, 5):
            pt = board[str(i)]
            pts.append((pt["x"] + offset_x, pt["y"] + offset_y))
        pts.append(pts[0])

        msp.add_lwpolyline(pts, dxfattribs={'color': 4})

        cx = sum(p[0] for p in pts[:-1]) / 4
        cy = sum(p[1] for p in pts[:-1]) / 4
        msp.add_text(f"Board-{board.get('label', '')}", dxfattribs={
            'height': 800, 'color': 4
        }).set_placement((cx, cy), align=TextEntityAlignment.MIDDLE_CENTER)

    cargo_items = algo_data.get("cargoPosition", [])
    for item in cargo_items:
        layer_idx = item.get("Layer", 1)
        offset_x, offset_y = LAYER_OFFSETS.get(layer_idx, (0.0, 0.0))

        pts = []
        coords_dict = item.get("coordinate", {})
        for i in range(1, 5):
            pt = coords_dict[str(i)]
            pts.append((pt["x"] + offset_x, pt["y"] + offset_y))
        pts.append(pts[0])

        c_color = 3
        msp.add_lwpolyline(pts, dxfattribs={'color': c_color})

        cx = sum(p[0] for p in pts[:-1]) / 4
        cy = sum(p[1] for p in pts[:-1]) / 4

        c_name = item.get("cargoName", "Unknown")
        tier = item.get("tier", 1)
        label_text = f"{c_name}" if tier == 1 else f"{c_name} (Tier {tier})"

        l = item.get("length", 10000)
        w = item.get("width", 4000)

        char_count = max(1, len(label_text))
        char_width_factor = 0.8
        max_h_by_length = (l * 0.8) / (char_count * char_width_factor)
        max_h_by_width = w * 0.4
        text_h = min(max_h_by_length, max_h_by_width)

        msp.add_text(label_text, dxfattribs={
            'height': text_h,
            'color': c_color
        }).set_placement((cx, cy), align=TextEntityAlignment.MIDDLE_CENTER)

    # 保存并输出
    output_filename = "loading_result.dxf"
    doc.saveas(output_filename)
    return output_filename


if __name__ == "__main__":
    generate_cad_with_cargo()