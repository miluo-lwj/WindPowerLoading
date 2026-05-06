import streamlit as st
import pandas as pd
import os
import time
import traceback

from loading_result import generate_cad_with_cargo
from algorithm import MockLoadingAlgorithm, LoadingAlgorithm

st.set_page_config(page_title="风电智能配载", page_icon="", layout="wide")

if 'step' not in st.session_state:
    st.session_state.step = 1

if 'cargo_df' not in st.session_state:
    st.session_state.cargo_df = pd.DataFrame([
        {"set_id": "WTG_001", "id": "WTG_001_Nacelle", "type": "nacelle", "desc": "主机舱", "length": 12.5,
         "width": 4.2, "height": 4.5, "weight": 135.0, "quantity": 1},
        {"set_id": "WTG_001", "id": "WTG_001_Tower_Bot", "type": "tower", "desc": "底段塔筒", "length": 25.0,
         "width": 5.0, "height": 5.0, "weight": 85.0, "quantity": 1}
    ])

if 'generated_dxfs' not in st.session_state:
    st.session_state.generated_dxfs = []


def next_step():
    st.session_state.step += 1


def prev_step():
    st.session_state.step -= 1


def reset_and_start_over():
    st.session_state.step = 1
    st.session_state.generated_dxfs = []


st.progress(st.session_state.step / 2.0)
st.write("")

# 录入货物清单
if st.session_state.step == 1:
    st.title("录入航次货物清单")
    st.markdown("---")

    st.caption("请在下方表格中贴入本航次需要配载的货物明细：")

    st.session_state.cargo_df = st.data_editor(
        st.session_state.cargo_df,
        num_rows="dynamic",
        column_config={"type": st.column_config.SelectboxColumn("类型", options=["nacelle", "tower", "blade", "hub"],
                                                                required=True)},
        use_container_width=True,
        height=350
    )

    st.markdown("---")
    col_spacer, col_btn_next = st.columns([8, 2])
    with col_btn_next:
        st.button("生成配载方案", on_click=next_step, type="primary", use_container_width=True)



# 显示 CAD 图片页面

elif st.session_state.step == 2:
    st.title("配载方案与 CAD 导出")
    st.markdown("---")

    # 算法执行与 CAD 生成
    if not st.session_state.generated_dxfs:
        with st.spinner("算法引擎：正在执行三维空间排样与碰撞检测..."):
            time.sleep(1.5)

            # 实例化算法类
            # 真实算法接入后替换为LoadingAlgorithm
            # solver = LoadingAlgorithm()
            solver = MockLoadingAlgorithm()
            current_algo = solver.solve(st.session_state.cargo_df)

            try:
                output_filename = generate_cad_with_cargo(current_algo)

                dxf_cache = []
                if os.path.exists(output_filename):
                    with open(output_filename, "rb") as f:
                        dxf_cache.append({"name": output_filename, "data": f.read()})

                st.session_state.generated_dxfs = dxf_cache
            except Exception as e:
                st.error("图纸生成失败")
                st.code(traceback.format_exc(), language="python")


    if st.session_state.generated_dxfs:
        st.success("配载方案已生成。")

        st.markdown("#### 可下载 CAD 选项")
        cols = st.columns(3)
        for i, dxf_file in enumerate(st.session_state.generated_dxfs):
            with cols[i % 3]:
                st.download_button(
                    label=f"下载图纸: {dxf_file['name']}",
                    data=dxf_file['data'],
                    file_name=dxf_file['name'],
                    mime="application/dxf",
                    use_container_width=True
                )

    st.markdown("---")
    col_spacer, col_back, col_reset = st.columns([6, 2, 2])
    with col_back:
        st.button("返回修改货物", on_click=prev_step, use_container_width=True)
    with col_reset:
        st.button("开启新一轮配载", on_click=reset_and_start_over, use_container_width=True)