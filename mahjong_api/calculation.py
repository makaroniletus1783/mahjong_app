# 計算
from mahjong.hand_calculating.hand import HandCalculator
# 麻雀牌
from mahjong.tile import TilesConverter
# 役, オプションルール
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
# 鳴き
from mahjong.meld import Meld
# 風(場&自)
from mahjong.constants import EAST, SOUTH, WEST, NORTH
# HandCalculator(計算用クラス)のインスタンスを生成
calculator = HandCalculator()
results = {}
# 結果出力用


class Calculation:
    def __init__(self, man, pin, sou, honors):
        self.man = man
        self.pin = pin
        self.sou = sou
        self.honors = honors
        self.rise = '5'
        self.melds = None
        self.dora = None
        self.config = None
        # アガリ形(man=マンズ, pin=ピンズ, sou=ソーズ, honors=字牌)
        self.tiles = TilesConverter.string_to_136_array(
            man=self.man, pin=self.pin, sou=self.sou, honors=self.honors)

        # アガリ牌(ソーズの5)
        self.win_tile = TilesConverter.string_to_136_array(sou=self.rise)[0]

        # 鳴き(なし)
        self.melds = self.melds

        # ドラ(なし)
        self.dora_indicators = self.dora

        # オプション(なし)
        self.config = self.config

        self.hand_result = calculator.estimate_hand_value(
            self.tiles, self.win_tile, self.melds, self.dora_indicators, self.config)

    def print_hand_result(self):
        # 翻数, 符数
        # print(hand_result.han, hand_result.fu)
        results['han'] = self.hand_result.han
        results['fu'] = self.hand_result.fu
        # 点数(ツモアガリの場合[左：親失点, 右:子失点], ロンアガリの場合[左:放銃者失点, 右:0])
        # print(hand_result.cost['main'], result.cost['additional'])
        results['parent'] = self.hand_result.cost['main']
        results['child'] = self.hand_result.cost['additional']
        # 役
        # print(hand_result.yaku)
        results['yaku'] = self.hand_result.yaku
        # 符数の詳細
        # for fu_item in hand_result.fu_details:
        # print(fu_item)
        # print(results)
        return results
