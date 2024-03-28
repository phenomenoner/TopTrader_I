import pandas as pd
import logging
import utils
from fubon_neo.sdk import FubonSDK, Order
from fubon_neo.constant import TimeInForce, OrderType, PriceType, MarketType, BSAction

global LOGGER


class TopTrader:
    global LOGGER

    def __init__(self, id, pwd, cert_filepath, certpwd):
        self.logger = LOGGER
        self.sdk = None
        self.credential = {
            "id": id,
            "pwd": pwd,
            "cert_filepath": cert_filepath,
            "certpwd": certpwd,
        }
        self.accounts = None  # 可使用帳號列表
        self.active_account = None  # 交易及帳務查詢時使用帳號
        self.trade_df = None  # 交易目標列表
        self.is_trade_active = False  # 是否交易正在進行

    # 登入
    def __login(self):
        # 重設可用帳號列表
        self.accounts = None

        # 連接主機
        self.sdk = FubonSDK("ws://10.81.70.178/TASP/XCPXWS")

        # 登入取得帳號列表
        response = self.sdk.login(
            self.credential["id"],
            self.credential["pwd"],
            self.credential["cert_filepath"],
            self.certpwd["certpwd"],
        )

        self.logger.info(f"登入回報:\n{response}")

        # 更新可用帳號列表
        if response.data is not None and len(response.data) > 0:
            self.accounts = response.data

    # 取得可用帳戶列表
    def get_accounts(self):
        if self.accounts is None:
            self.logger.error(f"無可用帳戶")

        return self.accounts

    # 設定使用帳戶
    # input: option_pos - 欲使用之帳號位置，例如第一個帳號輸入 0
    def set_active_accounts(self, option_pos):
        if self.accounts is None:
            self.logger.error(f"無可用帳戶")

        else:
            try:
                self.active_account = self.accounts[option_pos]
                self.logger.info(f"當前使用帳號\n{self.active_account}")
            except Exception as e:
                self.logger.error(f"設定使用帳號錯誤: {e}")

    # 設定交易列表
    def set_trade_list(self, filepath):
        # 確認是否交易正在進行
        if self.is_trade_active:
            self.logger.error(f"交易環節已啟動，無法設定交易列表")
            return

        # 重置交易列表
        self.trade_df = None

        # 讀取並設置交易列表
        try:
            self.trade_df = pd.read_excel(filepath, header=None)
        except FileNotFoundError as e:
            self.logger.error(f"找不到檔案 {filepath}, 錯誤訊息 {e}")
        except pd.errors.ParserError as e:
            self.logger.error(f"檔案格式解析錯誤, 錯誤訊息 {e}")

        # 清理交易列表格式

    # 啟動交易環節
    def activate_trade(self):
        # 確認是否已設置使用帳號
        if self.active_account is None:
            self.logger.error(f"未設置使用帳號，請先設置使用帳號")

        # 確認是否交易列表已設定成功
        if self.trade_df is None:
            self.logger.error(f"交易列表未設置，請先設定交易列表")
            return

        # 計算標的張數差額

        # 下單

    # -----------------------------------------------------------
    #                       API 串接相關功能
    # -----------------------------------------------------------


# 主程式
if __name__ == '__main__':
    global LOGGER

    utils.mk_folder("logs")
    LOGGER = utils.get_logger("TopTrader",
                              "logs/TopTrader.log",
                              log_level=logging.DEBUG
                              )
