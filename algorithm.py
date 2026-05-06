from abc import ABC, abstractmethod
import pandas as pd


class BaseLoadingAlgorithm(ABC):
    """
    风电智能配载算法
    """

    @abstractmethod
    def solve(self, cargo_data: pd.DataFrame) -> dict:
        """
        cargo_data: 从前端传入的航次货物清单 (DataFrame格式)
        return: 包含货物三维坐标和旁通板铺设状态的字典 (dict格式)
        """
        pass


class LoadingAlgorithm(BaseLoadingAlgorithm):
    """
    基于三维装箱和启发式规则的真实配载算法
    """
    def solve(self, cargo_data: pd.DataFrame) -> dict:
        return {

        }

class MockLoadingAlgorithm(BaseLoadingAlgorithm):
    def solve(self, cargo_data: pd.DataFrame) -> dict:
        # 测试数据
        result = {
            "totalSetCount": 1,
            "cargoPosition": [
                {
                    "cargoType": "T110",
                    "cargoName": "Tower Demo",
                    "cargoLabel": "Tower",
                    "length": 26210,
                    "width": 4550,
                    "height": 4630,
                    "weight": 64.1,
                    "Layer": 1,
                    "coordinate": {
                        "1": {"x": 0.0, "y": 0.0, "z": 0},
                        "2": {"x": 0.0, "y": 4550.0, "z": 0},
                        "3": {"x": 26210.0, "y": 4550.0, "z": 0},
                        "4": {"x": 26210.0, "y": 0.0, "z": 0}
                    },
                    "tier": 1
                }
            ],
            "bypassBoardPosition": [
                {
                    "1": {"x": 77.91, "y": 79.11, "z": 0},
                    "2": {"x": 77.91, "y": 27379.0, "z": 0},
                    "3": {"x": 4928.0, "y": 27379.0, "z": 0},
                    "4": {"x": 4928.0, "y": 79.11, "z": 0},
                    "layer": 2,
                    "label": 1
                }
            ]
        }
        return result